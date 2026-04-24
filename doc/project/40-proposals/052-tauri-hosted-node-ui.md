# Proposal 052: Tauri-Hosted Node UI

Based on:

- `doc/project/20-memos/node-ui-htmx-hateoas-architecture.md`
- `doc/project/30-stories/story-008-cool-site-comment.md`
- `doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/050-local-readiness-gate.md`
- `doc/project/60-solutions/node-ui.md`
- `node/DEV-GUIDELINES.md`

## Status

Draft

## Date

2026-04-24

## Executive Summary

Orbiplex Node should add an optional desktop shell built with Tauri.

The shell is not a new application runtime and not a replacement for the
existing Node UI architecture. It is a thin native host around the current
web-based operator console:

- Rust host,
- system webview,
- host-owned window and panel management,
- native integrations where useful,
- strict origin and capability boundaries.

The Node already has the right shape for this:

- the core application is Rust,
- the operator console is web UI served locally,
- middleware modules are supervised HTTP services,
- the browser is only a client of the console.

Electron would introduce Node.js as another central runtime even though
Orbiplex already has a Rust daemon and supervised services. Tauri fits the
existing strata better: the desktop process remains a small host for a web UI
whose semantic authority still lives in the daemon.

The preferred direction is:

- keep Node UI as HTMX/HATEOAS over server-rendered HTML,
- host the operator surface in a Tauri-managed main webview,
- avoid putting untrusted web content into the operator webview,
- use a separate low-privilege external-content webview or window when a user
  needs to inspect a public URL,
- consider a custom app protocol for the operator hypermedia space so the
  desktop UI can present one coherent origin without exposing daemon control
  endpoints as ordinary browser-reachable localhost APIs.

## Problem

The current browser-based UI works, but it has three frictions:

1. It looks and behaves like a browser tab even when it is the operator's local
   control panel.
2. Localhost control surfaces are easy to overexpose by accident.
3. Story-008-style resource opinion flows need a convenient way to show or
   inspect an external web resource without merging that external page with the
   operator control origin.

The naive desktop migration would be to embed the existing localhost UI and call
it done. That keeps the useful development path, but it does not name the
security boundary. If the same webview can navigate from trusted operator UI to
an arbitrary remote page, then that page can try to reach loopback endpoints,
trigger browser-mediated requests, probe ports, or exploit weak CORS/CSRF
settings.

This proposal separates two questions:

- how Orbiplex presents its own operator hypermedia,
- how Orbiplex previews or comments on foreign web resources.

Those are different trust domains and should be different webviews or windows.

## Goals

- Provide a native desktop host for Node UI without introducing Node.js as an
  application runtime.
- Preserve the HTMX/HATEOAS architecture and server-side rendering model.
- Keep daemon and middleware semantics outside the desktop shell.
- Reduce reliance on browser-exposed localhost as the primary UI origin.
- Provide a safe path for external web preview/commenting flows.
- Use Tauri capabilities as explicit boundaries between trusted operator UI and
  untrusted or semi-trusted content.
- Keep the desktop shell optional; browser access remains useful for development
  and diagnostics.

## Non-Goals

- This proposal does not replace the daemon HTTP API.
- This proposal does not require rewriting Node UI as a SPA.
- This proposal does not define a final visual design system.
- This proposal does not make the Tauri shell a protocol authority.
- This proposal does not give remote web content access to Tauri commands,
  daemon authtok, signer material, local files, or operator actions.
- This proposal does not define mobile thin-client behavior; that belongs to the
  pod-backed access layer.

## Decision

Orbiplex SHOULD add a Tauri desktop host for Node UI.

The first implementation SHOULD use three strata:

```text
Tauri desktop shell
  - window lifecycle
  - split/panel layout
  - native menus, tray, notifications, file dialogs where needed
  - app protocol or controlled localhost bridge

Node UI web server
  - Axum + MiniJinja
  - HTMX fragments
  - HATEOAS navigation
  - daemon proxy
  - browser session and CSRF boundary

Node daemon
  - protocol authority
  - local readiness gate
  - middleware supervision
  - signer and capability registry
  - source of truth for node state
```

The shell MUST remain a host and coordinator. It MUST NOT implement protocol
semantics, sign protocol artifacts directly, hold procurement state, or become a
second control-plane authority.

## Existing Node Contracts to Reuse

The desktop shell should reuse the current Node implementation contracts instead
of inventing parallel discovery, lifecycle, or credential paths.

| Existing mechanism | Current owner | Desktop use |
| --- | --- | --- |
| `<data_dir>/health/daemon-health.json` | daemon | discover daemon control endpoint indirectly through Node UI, not in the webview |
| `<data_dir>/authtok` | daemon | remains server-side; read by Node UI and launcher/client code only |
| `<data_dir>/node-ui/bind` | node-ui runtime | discover the Node UI listening address |
| `<data_dir>/node-ui/control/direct-spawn.log` | launcher/node-ui target | surface startup failures without scraping daemon state |
| `orbiplex-node-ui-launcher` | launcher crate | start, stop, restart, and status for the UI target |
| `orbiplex-node-launcher` | launcher crate | start, stop, restart, and status for the daemon target |
| `node_ui.start_with_node` config behavior | node control tooling | preserve existing "node brings UI up" operator workflow |
| Node UI routes | node-ui crate | remain the canonical operator HTML/HATEOAS surface |
| middleware UI package registry | node-ui crate | continue loading module UI surfaces from `middleware-packages` |

The desktop host should therefore treat `data_dir` as the root of local
coordination. It may accept `--data-dir` and `--profile` in the same spirit as
the existing CLI, but it should not create a separate desktop-only instance
registry.

### Discovery Contract

For the first implementation, desktop startup should follow this order:

1. Resolve `data_dir` from an explicit argument, a profile, or the existing Node
   default used by local control tooling.
2. Query launcher status for the daemon target.
3. Start the daemon through the launcher if policy says the desktop owns this
   session.
4. Query launcher status for the `node-ui` target.
5. Start `node-ui` through `orbiplex-node-ui-launcher` if it is not running.
6. Read `<data_dir>/node-ui/bind`.
7. Load the operator webview from the discovered Node UI URL or from the app
   protocol bridge that maps to it.

This keeps the desktop implementation close to today's browser path:

```text
daemon -> writes health/authtok
node-ui -> reads health/authtok, writes node-ui/bind
desktop -> reads node-ui/bind, hosts webview
```

The browser still never receives `X-Orbiplex-Authtok`; Node UI remains the
server-side daemon client.

### Lifecycle Ownership Modes

The desktop host should support two lifecycle modes:

| Mode | Meaning | Use case |
| --- | --- | --- |
| `attach` | use already-running daemon and Node UI; fail visibly if absent | development, supervised production |
| `supervise-local` | start/stop daemon and Node UI through launcher contracts | packaged local desktop |

`supervise-local` should still call the launcher crate or launcher binaries. The
Tauri shell must not embed `launchd`, `systemd --user`, Windows service, or
direct-spawn semantics inside UI code. Those are lower-level process lifecycle
adapters already owned by `launcher`.

### Failure Classes

The host should distinguish failures before rendering:

| Failure | Detection | Operator surface |
| --- | --- | --- |
| `daemon-launcher-unreachable` | launcher status/start fails | desktop bootstrap error |
| `daemon-control-unreachable` | Node UI cannot discover/read daemon health | Node UI degraded status |
| `node-ui-launcher-unreachable` | UI launcher operation fails | desktop bootstrap error |
| `node-ui-bind-missing` | no `<data_dir>/node-ui/bind` after timeout | desktop bootstrap error with log pointer |
| `node-ui-http-unreachable` | bind exists but HTTP connect fails | desktop retry/error panel |
| `local-readiness-gate` | daemon phase reported through Node UI | normal operator UI state |

This split follows the existing project rule: do not conflate launcher state,
control-plane reachability, and protocol/runtime readiness.

## Workspace Placement

The implementation should live in the Node workspace as a new edge crate, for
example:

```text
node/desktop
```

or:

```text
node/node-desktop
```

Recommended ownership:

| Crate/module | Responsibility |
| --- | --- |
| `desktop` / `node-desktop` | Tauri shell, window policy, app protocol bridge, native integrations |
| `launcher` | daemon and node-ui lifecycle adapters |
| `node-ui` | HTML rendering, HTMX routes, middleware UI registry, daemon proxy |
| `control` | transport-agnostic daemon DTOs used by Node UI and launcher clients |
| `daemon` | local control API, orchestration, protocol authority |

The desktop crate may depend on `launcher` and small shared DTO crates, but it
should avoid depending on `daemon` internals. If the desktop shell needs a
control operation, the preferred path is:

```text
desktop -> launcher/client contract -> daemon or node-ui process
desktop webview -> node-ui HTML route -> daemon control API
```

not:

```text
desktop -> daemon internal module
```

This keeps the shell as an adapter and preserves the ability to run the same
Node UI in a normal browser.

## UI Origin Model

The operator UI should appear under one app-owned hypermedia origin:

```text
orbiplex://localhost/...
```

or the equivalent Tauri app URL shape:

```text
tauri://localhost/...
```

The exact scheme is an implementation decision. The contract is that the
operator sees one coherent Orbiplex UI space, while the host can map paths under
that space to the Node UI server or to embedded static assets.

For example:

| Visible UI path | Host-owned mapping |
| --- | --- |
| `orbiplex://localhost/` | Node UI index |
| `orbiplex://localhost/executions/...` | Node UI HTMX route |
| `orbiplex://localhost/local-readiness-gate` | Node UI local readiness view |
| `orbiplex://localhost/modules/{module_id}/...` | Node UI module extension route |
| `orbiplex://localhost/assets/...` | bundled or Node UI static asset |

This preserves HATEOAS. Links and forms stay inside the operator hypermedia
space. The desktop shell can still proxy or map the request to a localhost
server under the hood, but the browser-visible contract is not "call the daemon
on a random loopback port".

### Bridge Shape

The app protocol bridge should be an HTTP-shaped adapter, not a semantic
interpreter.

For each request under the app-owned UI origin, the bridge should preserve:

- method,
- path,
- query string,
- request body,
- relevant HTMX headers such as `HX-Request`, `HX-Target`, `HX-Current-URL`,
- response status,
- response body,
- response headers needed by HTMX such as `HX-Redirect`, `HX-Location`,
  `HX-Push-Url`, `HX-Replace-Url`, `HX-Trigger`, `HX-Retarget`, and
  `HX-Reswap`.

The bridge may rewrite the visible origin, but it should not rewrite Node UI
application semantics. In particular, it should not parse operator forms,
interpret daemon JSON, or inspect protocol records except for generic security
policy checks.

### IPC Boundary: Do Not Replace Hypermedia with `invoke`

Tauri IPC (`invoke`) should not become the primary routing mechanism for the
operator console.

The operator console's main interaction model is still:

```text
link/form/HTMX request -> URL -> HTML fragment or page
```

not:

```text
button/script -> invoke("operator_action", payload) -> JSON -> client-side render
```

`invoke` is a typed RPC channel from frontend JavaScript into Rust commands. It
is useful for native host actions, but it is not a hypermedia transport. Using it
as the main console API would turn Node UI from a HATEOAS/HTMX projection into a
desktop-specific RPC client. That would introduce the same class of problems the
project is intentionally avoiding:

- a second UI state model,
- a second route/action table beside Node UI routes,
- loss of ordinary links and forms as visible state transitions,
- weaker browser fallback and diagnostics,
- more JavaScript glue around flows that are currently expressed as HTML,
- harder reuse of middleware UI packages that expect Node UI routing.

The desktop rule is therefore:

```text
orbiplex://... / app URL  = operator hypermedia space
Tauri custom/app protocol = HTTP-shaped bridge for that hypermedia
Tauri invoke              = side channel for native host capabilities
```

The `operator` webview may call `invoke` only for bounded host operations that
do not duplicate Node UI or daemon semantics.

### Absolute Path Discipline

Current Node UI templates use origin-relative paths such as:

```html
<link rel="stylesheet" href="/static/node-ui.css">
<a href="/status">Status</a>
```

That is compatible with an app-owned origin as long as the bridge maps the root
path to Node UI. The first app-protocol slice should therefore prefer preserving
the existing root-mounted route layout rather than introducing a `/node-ui`
prefix that would force broad template churn.

If a prefix becomes necessary later, it should be introduced as one explicit
Node UI base-path option and tested against HTMX boosted navigation, fragment
loads, and history restoration.

### MVP Compatibility Mode

The first implementation MAY load the existing Node UI `http://127.0.0.1:{port}`
directly in the main webview while the custom protocol bridge is being built.

That mode MUST be treated as a compatibility phase, not the final security
posture. In that phase:

- bind Node UI and daemon control ports to loopback only,
- use unpredictable per-run ports where practical,
- keep daemon authtok server-side in Node UI,
- reject broad CORS,
- use CSRF protection on operator mutations,
- prevent navigation of the main operator webview to remote URLs,
- open external resources only in a separate low-privilege webview or external
  system browser.

## Webview Partitioning

The desktop host should use separate webviews or windows for separate trust
domains.

| Webview | Content | Capability posture |
| --- | --- | --- |
| `operator` | Orbiplex Node UI | local app capabilities needed for window/UI integration |
| `external-preview` | arbitrary or allowlisted public URLs | no Tauri IPC, no daemon credentials, no local operator capabilities |
| `diagnostics` | optional local trace/status panels | read-only unless explicitly granted |

The `operator` webview MUST NOT navigate to arbitrary remote pages. Links to
external resources should either:

- open in `external-preview`, or
- open in the system browser, depending on policy and operator preference.

The `external-preview` webview MUST be considered hostile by default. It should
not receive:

- Tauri command permissions,
- daemon authtok,
- Node UI session cookies scoped to the operator origin,
- ambient access to local files,
- broad `localhost` exceptions,
- ability to call operator mutation endpoints.

When Story 008 needs to show `https://randomseed.io/` while composing an opinion,
the composition form remains in `operator`; the remote page is shown in
`external-preview`. The action "comment on this resource" is performed by the
operator UI with an explicit resource reference, not by the remote page.

### External Resource Handoff

The external preview should hand resource references to the operator UI as data,
not as authority.

Minimal handoff shape:

```json
{
  "schema": "orbiplex.desktop.resource-ref-handoff.v1",
  "resource/kind": "url",
  "resource/id": "https://randomseed.io/",
  "source": {
    "webview": "external-preview",
    "observed/title": "optional page title",
    "observed/at": "2026-04-24T00:00:00Z"
  }
}
```

This handoff is not a protocol artifact. It is a desktop-local UI convenience
that pre-fills the existing Node UI resource opinion form. Node UI and daemon
still build and sign the real `agora-record.v1` / `resource-opinion.v1`
artifact through the existing Story-008 path.

The handoff should be explicit: a remote page load must not automatically create
an opinion draft or trigger a POST.

## Security Boundary

### Localhost Risk

Loopback is a transport locality, not an authority boundary.

A foreign page loaded in a browser-like renderer can attempt requests to
`127.0.0.1`, `localhost`, or private addresses. If Orbiplex exposes privileged
operator actions on localhost without a strong browser boundary, then ordinary
web behavior can become a confused-deputy path.

The desktop host should therefore reduce the browser-visible localhost surface
for privileged UI paths.

### Required Invariants

- The daemon authtok MUST NOT be exposed to browser JavaScript.
- Operator mutations MUST require a Node UI session boundary and CSRF defense.
- Daemon control endpoints MUST reject direct browser access unless the caller
  has the expected server-side credential.
- CORS MUST default to deny for daemon and middleware control endpoints.
- Local services MUST bind to loopback or a stricter local transport unless
  explicitly configured otherwise.
- External webviews MUST have no Tauri IPC capability by default.
- Capabilities MUST be scoped per webview/window label, not globally granted to
  every renderer.
- Content Security Policy MUST be strict for the operator UI.
- Remote scripts, CDN assets, and untrusted module UI assets MUST NOT be allowed
  into the operator origin by default.

### Credential and Cookie Rules

The desktop shell should not introduce a new privileged browser credential.

Rules:

- `X-Orbiplex-Authtok` remains a server-side credential read by Node UI or
  launcher/control clients.
- Agora client tokens remain server-side in Node UI when proxying Agora streams
  or records.
- The operator webview may use ordinary Node UI session cookies once Node UI
  has them, but those cookies must be scoped to the operator origin and not sent
  to external preview pages.
- The external preview must use a separate data store / browsing context where
  the platform allows it.
- If the app protocol bridge is used, it should not attach daemon authtok to
  requests originating from arbitrary webviews; only the Node UI server process
  should talk to daemon control endpoints.

### Navigation Policy

The operator webview should allow only:

- app-owned URLs,
- Node UI compatibility localhost URL in MVP mode,
- static assets served by Node UI,
- explicit file downloads emitted by trusted Node UI routes.

Everything else should be intercepted and routed by policy:

| URL class | Default action |
| --- | --- |
| `http://127.0.0.1:{node-ui-port}/...` | allow only in MVP compatibility mode |
| `orbiplex://localhost/...` | allow |
| `tauri://localhost/...` | allow if selected as app URL form |
| `https://...` | open external preview or system browser |
| `http://...` non-loopback | open external preview or system browser with warning policy |
| `file://...` | deny unless triggered by explicit trusted file-open flow |
| unknown custom scheme | deny or ask the OS only through an explicit opener policy |

This policy should be tested with ordinary links, HTMX boosted links, redirects,
and `HX-Redirect` / `HX-Location` responses.

### Capability Model

Tauri capabilities should be used as an explicit host boundary:

- the `operator` webview may receive only the minimal commands needed for the
  desktop shell,
- `external-preview` receives no privileged commands,
- any future remote-content capability must be separately reviewed and
  allowlisted by URL pattern and operation,
- multi-webview windows should scope capabilities by webview label rather than
  by broad window label.

This matches the project rule: authority is a contract at the boundary, not an
ambient property of being displayed inside the application.

### Appropriate Uses of `invoke`

Allowed `invoke` commands should be small native host affordances, for example:

- open or close `external-preview`,
- read the current `external-preview` URL as an explicit resource-reference
  handoff,
- open a system file picker for an import/export flow initiated by Node UI,
- show an OS notification,
- update tray/window state,
- request desktop bootstrap status,
- ask the launcher to start or stop daemon/Node UI in `supervise-local` mode.

`invoke` commands should not:

- call daemon control endpoints directly from frontend code,
- carry `X-Orbiplex-Authtok` into the webview,
- sign Agora records or capability passports,
- implement operator mutation semantics already owned by Node UI routes,
- render Node UI fragments,
- load middleware UI package manifests or route module surfaces,
- become a generic `invoke("http", { method, path, body })` tunnel available to
  unreviewed frontend code.

If an operation has a meaningful URL, form, or HTMX fragment in Node UI, it
should stay in the hypermedia path. If it controls the desktop host itself, it
belongs in `invoke`.

## Development Model

Tauri supports a development URL for frontend work and a distribution path or
URL for production assets. Orbiplex should use that pragmatically:

- during development, the shell may load the local Node UI server through
  `devUrl` or an equivalent configured URL,
- in packaged builds, the shell should start or discover the local daemon and
  Node UI process and then load the app-owned UI origin,
- static shell assets may be bundled; dynamic operator views remain served by
  Node UI.

No JavaScript bundler is required by this proposal. If the existing Node UI stays
HTMX plus vendored static assets, the desktop shell should preserve that
simplicity.

## Node UI Changes Required for Smooth Desktop Hosting

The desired migration is mostly additive. Node UI should remain browser-usable.

Recommended small changes:

| Change | Reason |
| --- | --- |
| Add an optional `--base-url` or `--public-origin` only if app-protocol history requires it | avoid hard-coding localhost in generated absolute URLs |
| Add an optional `--desktop-mode` flag only for presentation affordances, not semantics | allow minor UI chrome adjustments without changing routes |
| Add a lightweight `/desktop/ready` or reuse `/status` for shell smoke checks | let desktop detect "HTML surface up" separately from daemon readiness |
| Keep `/static/*`, HTMX routes, and fragment routes root-relative | minimize template churn |
| Preserve middleware UI package loading from `<data_dir>/middleware-packages` | do not fork module UI extension model |
| Add tests for important headers through the bridge | HTMX depends on response headers as part of the hypermedia contract |

Avoid these changes:

- moving daemon calls from Node UI into the Tauri frontend JavaScript,
- exposing authtok through rendered templates,
- adding a SPA state store to mirror daemon state,
- duplicating middleware UI registration in the desktop crate,
- making desktop-only routes the only way to reach operator actions.

## App Protocol Migration Plan

The migration from current localhost browser UI to app-owned desktop origin
should be staged so each step is reversible.

### Stage A: Current Browser Contract

```text
browser -> http://127.0.0.1:7766 -> node-ui -> daemon
```

No desktop shell is required. This stays supported.

### Stage B: Tauri Compatibility Shell

```text
operator webview -> http://127.0.0.1:{node-ui-bind} -> node-ui -> daemon
```

New code:

- desktop crate,
- launcher integration,
- navigation policy,
- external URL interception.

No Node UI route changes should be required.

### Stage C: App Protocol Reverse Proxy

```text
operator webview -> orbiplex://localhost/... -> desktop bridge
                 -> http://127.0.0.1:{node-ui-bind}/... -> node-ui -> daemon
```

New code:

- custom/app protocol handler,
- request/response header preservation,
- bridge tests for HTMX.

Node UI should still be the only HTML interpreter.

Before Stage C is promoted beyond spike status, the project should verify that
HTMX behaves consistently over the selected app URL form on the supported
desktop platforms. The spike must cover:

- `hx-get` fragment load,
- `hx-post` form submit,
- non-2xx response rendering,
- `HX-Redirect`,
- `HX-Location`,
- `HX-Push-Url` and browser history,
- boosted links,
- static assets,
- file download initiated by a trusted Node UI route.

If a raw `orbiplex://localhost/...` custom scheme behaves inconsistently across
WebView2, WKWebView, or WebKitGTK, the implementation may use Tauri's
platform-compatible app URL form such as `http://orbiplex.localhost/...` or
`https://orbiplex.localhost/...` where appropriate. The architectural
requirement is app-owned origin and HATEOAS preservation, not one literal scheme
spelling on every platform.

A first local harness for this check lives in:

```text
node/spikes/tauri-htmx-app-protocol/
```

It keeps `orbiplex://...` as the HTMX/HATEOAS transport and uses
`invoke("host_ping")` only as a separate native host side channel.

The first macOS manual pass is encouraging: startup, static HTMX loading,
boosted navigation, home navigation, `hx-get`, `hx-post`, `HX-Redirect`,
`HX-Location`, and `HX-Push-Url` work over the custom protocol without Node.js,
npm, Vite, or a frontend dev server. Tauri `invoke("host_ping")` also works as
a separate native side channel, confirming the intended split between
hypermedia transport and host IPC. The default `422` response path does not swap
content, which matches ordinary HTMX default behavior and should be configured
explicitly where Node UI wants error fragments to render. The download route
rendered inline in WKWebView, so file downloads should be treated as an explicit
host-policy/native-integration surface rather than assumed to behave like
ordinary browser downloads under a custom protocol.

### Stage D: Optional Local Transport Hardening

If supported cleanly by Tauri and the Node workspace, the bridge may later talk
to Node UI over a less browser-addressable transport:

```text
operator webview -> orbiplex://localhost/... -> desktop bridge
                 -> Unix domain socket / named pipe / in-process adapter
                 -> node-ui service layer -> daemon
```

This is an optimization and hardening step, not an MVP dependency. It should not
collapse Node UI into the Tauri crate unless the same service layer remains
usable by the standalone `orbiplex-node-ui` binary.

## Host Responsibilities

The Tauri host is responsible for:

- starting or attaching to the local Node daemon profile,
- starting or attaching to the Node UI server,
- exposing the main operator window,
- managing external preview windows or panels,
- enforcing navigation policy,
- applying CSP and capability configuration,
- providing native menus, tray integration, notifications, and file dialogs when
  those are explicitly needed,
- surfacing daemon unreachable and local readiness gate states early.

The host is not responsible for:

- protocol validation,
- procurement decisions,
- settlement logic,
- signing Agora records,
- evaluating middleware semantics,
- storing canonical protocol state.

## Trace and Diagnostics

The desktop host should produce local operational traces, but not protocol
facts.

Candidate trace events:

| Event | Meaning |
| --- | --- |
| `desktop/daemon-launcher-status` | launcher status was queried |
| `desktop/daemon-start-requested` | shell requested daemon start |
| `desktop/node-ui-start-requested` | shell requested Node UI start |
| `desktop/node-ui-bind-observed` | bind file was read successfully |
| `desktop/operator-navigation-blocked` | operator webview attempted disallowed navigation |
| `desktop/external-preview-opened` | external URL opened in preview |
| `desktop/resource-ref-handoff` | operator accepted a preview URL as a resource reference |
| `desktop/app-protocol-proxy-error` | app URL bridge failed to reach Node UI |

These traces should live in a desktop/runtime log under the instance `data_dir`,
for example:

```text
<data_dir>/desktop/control/desktop.log
```

They should be exportable and diagnostically useful, but they must not leak
daemon authtok, Agora client tokens, passphrases, seed material, request bodies
from sensitive forms, or remote page contents.

## Operator Flows

### Open Node UI

1. Operator starts Orbiplex Desktop.
2. Tauri host starts or discovers the daemon.
3. Tauri host starts or discovers Node UI.
4. The main `operator` webview loads the app-owned operator URL.
5. Node UI renders daemon status, local readiness blockers, and available
   operator actions.

### Comment on an External Resource

1. Operator opens or pastes an external URL.
2. Tauri host loads that URL in `external-preview` or the system browser.
3. Operator invokes "New opinion" from the trusted operator UI.
4. Node UI receives the resource reference as data.
5. Node UI follows the existing Agora/resource-opinion flow.
6. External content never receives authority to submit the opinion itself.

### Local Readiness Gate

1. Daemon starts in `local_readiness_gate`.
2. Tauri host still opens the operator webview.
3. Node UI renders blockers and safe actions.
4. Operator resolves or rejects blockers.
5. Daemon restarts or reloads through an explicit control operation.

This is one of the strongest reasons to keep the desktop host thin: even when
the full runtime is blocked, the local control surface remains small and
understandable.

## Proposed Implementation Slices

### Slice 1: Desktop Host MVP

- Add a `node-desktop` or `orbiplex-desktop` Tauri crate/binary in the Node
  workspace.
- Accept `--data-dir`, optional `--profile`, and lifecycle mode
  `attach|supervise-local`.
- Reuse launcher contracts to start or discover daemon and Node UI.
- Wait for `<data_dir>/node-ui/bind` and load the discovered Node UI URL.
- Deny navigation of the operator webview to remote URLs.
- Open remote links in the system browser or a separate preview window.
- Keep all daemon credentials server-side in Node UI.
- Add smoke tests for bind discovery and URL policy as pure Rust where possible.

### Slice 2: External Preview Panel

- Add an `external-preview` webview/window.
- Give it no Tauri IPC capabilities.
- Add explicit "use current URL as resource reference" bridge through the
  trusted host, not through remote page JavaScript.
- Clear preview browsing data on request and optionally per session.
- Pre-fill the existing Node UI Agora/resource opinion route with the selected
  `resource/kind=url` and `resource/id=<url>` rather than adding a desktop-only
  publication path.

### Slice 3: App Protocol Bridge

- Serve the operator UI under an app-owned scheme such as
  `orbiplex://localhost/`.
- Map app URL paths to Node UI routes or bundled assets.
- Keep HATEOAS links inside the app-owned origin.
- Tighten CORS and direct localhost exposure further.
- Preserve HTMX request and response headers end to end.
- Test boosted navigation, fragment swaps, form posts, redirects, and downloads.
- Confirm whether the selected app URL form is raw `orbiplex://localhost/...`
  or a Tauri/platform-specific localhost-shaped app origin.

### Slice 4: Native Integrations

- Add tray/status indication.
- Add OS notifications for readiness blockers and completed long-running tasks.
- Add file picker integration only for explicit import/export flows.
- Add deep-link handling only after the resource-reference security model is
  stable.

### Slice 5: Node-Side Ledger and Docs Alignment

When implementation begins in `node`, update:

- `node/docs/implementation-ledger.toml`,
- regenerated `node/docs/IMPLEMENTATION-LEDGER.md`,
- `node/README.md` operational commands,
- `node/DEV-GUIDELINES.md` only if a new reusable guideline emerges.

The ledger row should describe the desktop shell as an edge/client capability,
not as a new protocol layer.

## Open Questions

- Should the first app-owned scheme be `orbiplex://localhost` or should the host
  use Tauri's default app URL form until external protocol registration is
  needed?
- Does raw `orbiplex://localhost/...` preserve all required HTMX behavior on
  WebView2, WKWebView, and WebKitGTK, or should MVP use a localhost-shaped app
  origin while keeping the same semantic namespace?
- Should external preview be an in-app split panel by default, or should the
  safer default be the system browser with in-app preview as an opt-in?
- Should the app protocol bridge proxy to Node UI over HTTP, Unix domain socket,
  or an in-process service adapter?
- Which native integrations are essential for MVP and which are merely desktop
  polish?
- Should the packaged desktop host own daemon supervision, or should it delegate
  to the existing launcher in the first slice?
- Should `node-ui` grow a shared library entry point for an eventual in-process
  adapter, or should the standalone HTTP process remain the only supported
  rendering boundary until there is measured need?
- Should desktop traces live under `<data_dir>/desktop/control/` or reuse the
  launcher control log layout more directly?

## Acceptance Criteria

| # | Criterion | Verification |
| --- | --- | --- |
| 1 | Operator UI runs in a Tauri main webview without changing Node UI into a SPA. | Manual desktop smoke test; HTMX flows still work. |
| 2 | Daemon authtok is never visible to browser JavaScript. | Code review; browser devtools/session inspection. |
| 3 | Remote URLs cannot load inside the operator webview. | Navigation policy test with `https://example.org/`. |
| 4 | External preview receives no privileged Tauri capabilities. | Tauri capability configuration review. |
| 5 | Operator mutations remain protected by Node UI session and CSRF boundary. | Mutation tests from foreign origin fail. |
| 6 | Story-008 resource opinion composition can use an external URL without giving the remote page authority. | End-to-end resource opinion flow. |
| 7 | Local readiness gate remains visible in desktop mode. | Start daemon with blockers and inspect desktop UI. |
| 8 | Browser access to Node UI remains available for development/diagnostics. | Existing local browser workflow still works. |
| 9 | Desktop startup reuses `<data_dir>/node-ui/bind` rather than hard-coding the UI port. | Start Node UI on a non-default port and open desktop. |
| 10 | Desktop lifecycle operations delegate to launcher contracts. | Code review; launcher contract tests remain the lifecycle authority. |
| 11 | App protocol bridge preserves HTMX headers and status codes. | Bridge tests for boosted navigation, form POST, fragment swap, and redirect. |
| 12 | Middleware UI package surfaces still render through Node UI in desktop mode. | Install a package manifest under `middleware-packages` and inspect nav/routes. |
| 13 | External URL handoff pre-fills an existing Node UI resource opinion flow without a desktop-only publish path. | Story-008 smoke test from preview to signed opinion. |
| 14 | Tauri `invoke` is limited to native host affordances and does not duplicate Node UI operator routes. | Code review; route/action inventory. |
| 15 | Selected app URL form supports HTMX over all target desktop webviews. | Cross-platform spike covering `hx-get`, `hx-post`, `HX-*` headers, history, static assets, and downloads. |

## References

- Tauri v2 configuration: `devUrl`, `frontendDist`, and app/custom URL shapes:
  <https://v2.tauri.app/reference/config/>
- Tauri v2 frontend-to-Rust commands and `invoke`:
  <https://v2.tauri.app/develop/calling-rust/>
- Tauri v2 frontend model: Tauri acts as a static web host for web assets:
  <https://v2.tauri.app/start/frontend/>
- Tauri v2 capability ACL: permissions can be scoped to windows and webviews:
  <https://v2.tauri.app/reference/acl/capability/>
- Tauri runtime authority for command/capability checks:
  <https://v2.tauri.app/security/runtime-authority/>
- Tauri v2 CSP guidance:
  <https://v2.tauri.app/security/csp/>
- Tauri v2 webview versions: WebView2 on Windows, WebKit/WKWebView family on
  Apple platforms, WebKitGTK on Linux:
  <https://v2.tauri.app/reference/webview-versions/>
