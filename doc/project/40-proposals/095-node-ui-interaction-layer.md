# Proposal 095: Node UI Interaction Layer

Based on:

- [Challenge 095: UI Workspace Continuity](../10-challenges/095-ui-workspace-continuity.md)
- [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md)
- [HTMX/HATEOAS architecture memo](../20-memos/node-ui-htmx-hateoas-architecture.md)
- [P052: Tauri-Hosted Node UI](052-tauri-hosted-node-ui.md)
- [P091: File-backed Configuration](091-file-backed-configuration-and-explainable-composition.md)
- [Solution 001: Node UI](../60-solutions/001-node-ui/001-node-ui.md)
- [Solution 019: Middleware](../60-solutions/019-middleware/019-middleware.md)
- `node:DEV-GUIDELINES.md` (Layering; Data and Contracts; thin UI boundaries)

## Status

**Proposed**. This document plans implementation; it does not claim a
working Stimulus integration or measured usability improvement.

## Date

2026-10-09

## Executive Summary

Add a small, reusable interaction layer above HTMX, not a replacement frontend.
Keep server-rendered HTML and HATEOAS, the optional Tauri host, and daemon-owned
authority. Prefer **Stimulus without Turbo**, conditional on the compatibility
gate below, to organize local behavior around existing HTML fragments.

The first slice preserves a conversation while opening, navigating and closing
a detail panel. Its purpose is lower cognitive load and stronger human agency:
the interface preserves context without deciding domain outcomes for the user.

## Context and Problem Statement

`node:node-ui/README.md` already describes modal slots, focus and transition
helpers; `node:node-desktop/README.md` separates the user-facing `/app` window
from the browser-first operator console. Consolidate those mechanics rather than
introducing parallel implementations. Conversational clients inspire continuity
of interaction, not claims about their internal architecture or dependencies.

### Current implementation baseline (inspected 2026-10-09)

Facts observed in the Node repository on this date; P095-001 re-verifies them
before any migration:

- HTMX 2.0.8 is vendored together with `response-targets` and the SSE extension
  (`htmx-ext-sse@2.2.4`). SRI appears on an SSE include, but not consistently
  across layouts; the user base also loads SSE without SRI.
- Interaction behavior lives in hand-written global scripts:
  `orbiplex-modal.js` (82 lines), `orbiplex-user.js` (626),
  `orbiplex-user-transitions.js` (86), `orbiplex-question-deadline.js` (26) and
  `orbiplex-csrf.js`. They attach document/body listeners and timers that are
  mostly live for the document lifetime, without a shared per-fragment lifecycle.
  Some timers are released: chat polling stops after detecting a detached history,
  fetch timeouts are cleared, and the question countdown stops on expiry. Global
  delegation alone is not a leak; inventory each owner's acquisition and cleanup.
- The user conversation is a modal (`user/fragments/contact_chat_modal.html`)
  rendered into `#orb-modal-slot`, and `orbiplex-user.js` opens it through its
  own `fetch`, outside HTMX. A detail panel opened "beside" the conversation
  cannot satisfy the proposed non-modal workspace contract without a layout
  decision. The separate chat-history polling fetch also overlaps HTMX/SSE
  refreshes; a manual fetch alone does not prove duplicate request ownership.
  Where the conversation lives is therefore
  a first-slice decision, not a detail (P095-009).
- The operator console and the `/app` shell navigate with `hx-boost` and
  `hx-push-url`. No `hx-history` attribute or `htmx.config` override exists.
  The vendored 2.0.8 implementation uses `sessionStorage` for `htmx-history-cache`.
  *Inference, not a runtime observation:* its enabled default snapshot cache can
  therefore already retain rendered operator, identity and consent pages. This
  exposure is independent of Stimulus and is addressed first (P095-007).
- Node UI responses carry `Content-Security-Policy: frame-ancestors 'none'`
  only; there is no `script-src`. The desktop host configures Tauri with
  `csp: null` and `withGlobalTauri: true`, and base templates contain inline
  scripts. Script in the same JavaScript context can access the exposed IPC API;
  this is not proof that every command is authorized. Window/webview permissions
  and host command checks remain separate. Current middleware paths return HTML
  through `Html(...)` and `fragment | safe`; `normalize_server_html_fragment`
  rewrites presentation and is not an HTML sanitizer. Package admission is not
  fragment isolation. P095-008 must establish a checked boundary, not assume one.
- The desktop proxy's `FORWARDED_RESPONSE_HEADERS` omits CSP, `Cache-Control`
  and `Vary`; server-side header changes alone do not reach the custom-origin
  document. The bootstrap embeds `/app` in an iframe, so blindly forwarding
  `frame-ancestors 'none'` would also break its current handoff.

Baseline evidence: `node:node-ui/static/htmx.min.js`,
`node:node-ui/static/orbiplex-user.js`, `node:node-ui/templates/user/base.html`,
`node:node-ui/src/handlers/ui_surfaces.rs`,
`node:node-ui/templates/middleware/surface.html`,
`node:node-ui/src/security.rs`, `node:node-desktop/tauri.conf.json` and
`node:node-desktop/src/main.rs` (`FORWARDED_RESPONSE_HEADERS`).

## Proposed Model and Decisions

### 1. Preserve ownership

| Owner | Responsibility |
| --- | --- |
| Daemon/services | Domain state, authorization, validation and execution |
| Node UI + HTMX | Server representations, links/forms, requests, swaps and URL history |
| Interaction controllers | Panel visibility, focus, scroll and bounded ephemeral presentation state |
| Tauri under P052 | Native windows, menus and explicitly authorized host integration |

Local presentation state is legitimate; a second domain state machine is not.
Controllers must not infer grants, advance workflows or replay mutations on
reconnect. No daemon credentials reach client JavaScript. A visible action is
not authorization; its owning service checks current authority when invoked.

### 2. Bound the workspace

V1 has a stable main surface, one detail panel and the existing modal slot.
Opening details does not replace the conversation/composer. Panel navigation
uses server-provided links and HTMX requests; close restores focus to the opener
or a documented safe fallback. A bounded, in-memory panel back stack holds only
same-origin route references, not HTML, grants or form contents, and refetches on
return. Panel steps do not write browser history; HTMX alone owns top-level URL
history. Full-page GET representations remain available for those links.

Preserve unsent text during panel operations and transient disconnection; never
automatically submit it. Warn before intentional navigation that would discard
it. Full-reload/crash recovery of drafts is not promised by this slice. Streaming
updates respect a user who has scrolled away from the end and expose an explicit
return-to-latest action rather than forcibly scrolling.

Command palettes, resizable layouts and extra native windows are future clients
of these mechanics, not prerequisites. Arbitrary docking, an SPA router, a UI
description language for plugins and a native-client rewrite are non-goals.

### 3. Stimulus and HTMX can complement each other

The upstream contracts are compatible: Stimulus attaches behavior to HTML and
observes DOM changes; HTMX requests and replaces HTML. This is a design inference
from their documented mechanisms, not a completed Orbiplex integration test.

- Start one Stimulus application per document. Let its DOM observer discover
  swapped controllers; do not rescan/restart it after every HTMX swap.
- Stimulus lifecycle callbacks run asynchronously. `htmx:afterSwap` is not proof
  that a newly inserted controller is connected; use controller/target connection
  callbacks for initialization and an explicit handshake if cross-controller
  readiness is needed. Do not encode timing with arbitrary sleeps.
- Make connection/reconnection idempotent. Release controller-owned listeners,
  timers and subscriptions on disconnect. A stable shell can keep presentation
  state while its child targets change; DOM replacement does not preserve a new
  element's controller instance automatically.
- Each action has one request owner. Controllers may trigger an existing HTMX
  action, but must not also fetch/submit it. Do not introduce Turbo Drive/Frames
  or a second history router. Late responses must not reopen a closed panel or
  overwrite a newer navigation; cancel or reject superseded reads.

Compatibility sources, inspected 2026-10-09:
[Stimulus introduction](https://stimulus.hotwired.dev/handbook/introduction),
[lifecycle](https://stimulus.hotwired.dev/reference/lifecycle-callbacks),
[HTMX integration](https://htmx.org/docs/#3rd-party),
[HTMX events](https://htmx.org/events/).

### 4. Privacy, authority and extension boundaries

Ephemeral focus, panel and scroll state stays in memory and is cleared on
logout/identity change. Do not persist conversation text, receipts or sensitive
HTML in browser storage. Disable HTMX history snapshots for sensitive surfaces
with `hx-history="false"`; verify that the pinned version and custom protocol
behave as intended. Navigation restoration always preserves current server-side
authorization and never revives an expired approval.

Durable behavioral preferences belong behind P091's file-backed contract, not
a parallel `localStorage` settings database. Until that owner supports a setting,
keep it session-only or defer it. No broad P091 completion dependency is needed
for the ephemeral first slice.

The middleware HTML extension model remains supported, subject to an explicit
compatibility review of existing executable surfaces. The host owns slots and
allowlisted controllers; module HTML is not permission to register executable
controllers, address unrelated shell targets or invoke Tauri commands. Preserve
existing admission, session and CSRF boundaries, and establish the fragment
isolation missing from the baseline before exposing shared controllers to module
content. Namespaced data attributes are conventions, not security isolation.

## Trade-offs

Stimulus offers lifecycle structure without replacing HTML rendering, at the cost
of a dependency and asynchronous lifecycle coordination. Plain JavaScript remains
the fallback if the spike adds more complexity than it removes. Alpine is an
alternative for local reactive widgets, not a second library to add alongside
Stimulus in this slice. No performance advantage is claimed without measurement.
Plain-JS fallback and UI rollback must retain the independent P095-007/008
privacy/security hardening; rollback never re-enables unsafe snapshots or scripts.

## Failure Modes and Mitigations

| Failure | Required evidence |
| --- | --- |
| Repeated swaps duplicate handlers or requests | Repeated mount/unmount/reconnect produces one action and no residual subscriptions |
| Out-of-order response changes the wrong view | Delayed reads, redirects/triggers and OOB effects after close/new navigation/identity change are rejected before effects |
| Details erase drafts or scroll | Preserve unsent text and intentional scroll; failed Back retains the previous entry; edits after discard consent require fresh consent |
| Modal loses keyboard users | Focus containment/return, Escape, labels and keyboard traversal work; reduced motion is respected |
| Back/logout exposes another identity's content | Old-cache cleanup, cache-disabled history restore, bfcache/pageshow and multi-window identity-transition tests; offline restoration stays locked |
| UI replay revives approval or repeats a write | Expired/refused/ambiguous outcomes stay explicit; no automatic mutation retry |
| Middleware activates privileged shell behavior | Reject scripts, declarative action/target injection, same-origin script sources and response-header/OOB escapes; host commands still enforce authority |

## Implementation Recommendations

1. Inventory `orbiplex-modal.js`, `orbiplex-user.js`, transitions, CSRF helpers and
   current HTMX extensions first. Reuse `#orb-modal-slot`; assign one owner per
   behavior and retire overlapping listeners when migrating it.
2. Keep controllers with `node-ui/static/` and contracts/examples in
   `node:node-ui/README.md` (longer material in its `docs/`). Use explicit
   host-owned registration, small controllers and declarative HTML bindings.
3. Pin and serve Stimulus locally with version, license and integrity recorded;
   no runtime CDN or mandatory new frontend build pipeline. Check compatibility
   against the repository's actual HTMX/extensions and CSP, not just latest docs.
4. Scope shortcuts away from text editing and IME composition. Distinguish a
   non-modal detail panel from a modal focus trap. Announce loading/errors without
   reading every streamed token to assistive technology.
5. Prefer real DOM/browser tests for lifecycle and history. Retain a Tauri
   custom-origin run separately; browser success alone is not WebView acceptance.
   Compare startup, interaction latency and resource use with the same baseline.
6. Keep runnable acceptance beside `node:tools/acceptance/` harnesses and results
   under `node:docs/evidence/`. Update the Node implementation ledger and relevant
   MVP rows only as actual adoption/evidence changes; regenerate derived views.

### Workspace slot topology

The host shell owns three slots. Fragments never create slots; they fill one.

```html
<div class="orb-workspace" data-controller="orb-workspace"
     data-orb-workspace-max-entries-value="8">
  <main id="app-main" data-orb-workspace-target="main">
    <!-- conversation history, composer -->
  </main>
  <aside id="orb-detail-panel" role="complementary"
         aria-labelledby="orb-detail-title"
         data-orb-workspace-target="panel" hidden></aside>
</div>
<div id="orb-modal-slot" class="orb-modal-slot"></div>
```

- `#app-main` keeps the existing `hx-select`/`hx-push-url` navigation and is the
  only target that changes top-level URL history. Moving it inside the stable
  workspace wrapper must also move its replacement templates: one live main and
  panel ID after every swap, with the wrapper outside the replaceable subtree.
- `#orb-detail-panel` is non-modal: no focus trap, no `aria-modal`, Escape
  closes it only when focus is inside it, and the main surface stays operable.
- `#orb-modal-slot` stays the one modal owner for confirmations and short forms.
  A detail panel never opens inside a modal; a modal may open above a panel.

### Panel link and fragment contract

Every panel link keeps a full-page representation in `href` and a fragment
request in `hx-get`. HTMX remains the only request owner; `hx-sync` cancels a
superseded panel read before a controller has to reason about it:

```html
<a href="/app/evidence/{ref}"
   hx-get="/app/evidence/{ref}"
   hx-target="#orb-detail-panel"
   hx-swap="innerHTML transition:false swap:0ms ignoreTitle:true"
   hx-push-url="false" hx-select="unset" hx-boost="false"
   hx-select-oob="unset"
   hx-sync="#orb-detail-panel:replace">Evidence</a>
```

The server selects the representation from `HX-Request: true` and
`HX-Target: orb-detail-panel`, never from a query flag, and answers both forms
with `Vary: HX-Request, HX-Target` and `Cache-Control: no-store` on authority,
identity, consent and conversation surfaces. The fragment root is fixed:

```html
<section class="orb-panel" data-orb-panel-fragment
         data-orb-panel-href="/app/evidence/{ref}">
  <h2 id="orb-detail-title">…</h2>
  …
</section>
```

`data-orb-panel-href` must match the normalized requested path and permitted query,
not an arbitrary response URL. Reject credentials, scheme-relative URLs, unowned
routes and authority-bearing query values. These endpoints are illustrative, not
implemented. Representation headers never grant authorization. The panel title
comes from its heading; it does not change the document title.

Fence the entire panel response, not just its final target: disallow
`HX-Redirect`, `HX-Location`, `HX-Refresh`, URL push/replace, retarget/reswap,
unapproved trigger headers and out-of-band swaps. The host maps authentication
loss separately to a locked shell. `response-targets`, inherited `hx-select`
and response headers must not redirect panel output into the composer or modal.
Keep V1 swaps immediate; delayed/view-transition commits require a fresh ordering
check at the actual DOM commit. `hx-sync` alone does not cover these effects.

### Ephemeral presentation state

Controller instances hold these values in memory only; nothing is written to
`localStorage`, `sessionStorage`, IndexedDB or the URL:

```text
PanelEntry = { href: same-origin path, at most 2048 bytes,
               opener: element id or null }
PanelState = { entries: PanelEntry[0..8], epoch: opaque context token,
               generation: non-wrapping safe integer, open: bool }
TailState  = { pinned: bool, unseen: u16 }
DraftState = { dirty: bool, revision: non-wrapping safe integer }
                                      # per composer element; holds no text
```

- One owner hook at `htmx:beforeRequest` admits the panel read, increments
  `generation` and captures `{epoch, generation, href}` plus the opener in a
  local `WeakMap` keyed by XHR before sending. Derive the opener from the request
  source element or explicit host-owned context, not the ordering of Stimulus
  and HTMX click listeners; an unready owner cancels the request. Close/context
  invalidation advances the fence independently. No wire header is necessary.
  The bundled 2.0.8 does expose
  `requestConfig.headers` on response event details, but local ordering need not
  become a server-facing protocol. Rotate the epoch on identity/context change
  or counter exhaustion; never reuse it when controllers reconnect.
- Reject stale, closed or wrong-epoch responses with `preventDefault()` at
  `htmx:beforeOnLoad`, before response headers cause effects. `beforeSwap` is too
  late for `HX-Redirect`/`HX-Trigger` and extensions can change its swap decision.
  Retain a final exact-slot/epoch check; close/disconnect also aborts in-flight
  reads. Abort alone cannot retract a response already being processed.
- Back refetches the previous `href`; commit the pop/push only after the current
  response is accepted. On failure retain the prior entry and expose the error.
  Eight entries are an upper bound; an accepted ninth drops the oldest.
- The composer text stays in the DOM element that the panel never replaces.
  `DraftState` drives discard confirmation before replacing that composer, using
  `htmx:confirm`. Bind consent to its revision and recheck before destructive
  swap, so typing while navigation is pending cannot silently lose new text.
  Attach `beforeunload` only while dirty; it is best-effort, not a guarantee for
  browser history or native-window closure. P095-004 must cover those paths
  explicitly. It never copies, persists or resubmits the text.
- `TailState.pinned` is true while the history scroller is within 32 px of its
  end, measured before content growth. When new messages arrive unpinned, the
  controller increments `unseen` (saturating at 65535, displayed as `65535+`),
  counting message identities rather than tokens or repeated snapshots,
  and reveals a "Jump to latest (N)" button. A polite live region announces at
  most one count change per two seconds, never streamed tokens.
- Logout, identity change/lock and `orb:local-unlock-required` invalidate pending
  work, clear all four states, remove prior identity content including composer
  text, and close the panel. Privacy invalidation is not vetoed by a dirty-draft
  prompt. Unlock begins a fresh context, never restores an old epoch's draft.

### Controller catalog and registration

V1 registers a closed set of host controllers from one static file,
`node-ui/static/orbiplex-controllers.js`, that calls `Application.start()` once
per document:

| Identifier | Owns | Migrates from |
| --- | --- | --- |
| `orb-workspace` | panel open, close, back, opener focus return, `PanelState` | new; panel logic only |
| `orb-modal` | modal focus containment, Escape, backdrop close, focus return | `orbiplex-modal.js` |
| `orb-follow-tail` | scroll pinning, jump-to-latest, `TailState` | chat-history code in `orbiplex-user.js` |
| `orb-draft-guard` | dirty flag and discard confirmation, `DraftState` | new |
| `orb-shortcuts` | global keys, suppressed in editable fields and during IME composition (`event.isComposing`) | new behavior for existing footer hints |

CSRF stays a non-controller global script because it must cover every request,
including ones issued outside any controller. Stimulus connects only registered
identifiers, so unknown `data-controller` values in fragments stay inert. That
is not sufficient isolation by itself, because an untrusted element inside a
host controller's scope could still name its actions:

- Before DOM insertion, a parser-based admission policy must strip scripts,
  event handlers and unauthorized behavioral attributes (Stimulus controller,
  action, target, outlet and value bindings; existing host `data-*` hooks;
  HTMX executable hooks, target/history/OOB escapes and unsafe URLs). Allowed
  module links/forms stay within their host-mediated mount. Filter response
  control headers too. This policy is new work, not an existing sanitizer.
- Mark the admitted subtree with a host-owned `[data-orb-untrusted]` boundary;
  host controllers reject actions from it, including synthetic event paths.
  Closing is a host-owned control outside that subtree, not a blanket exception.
  Event checks alone do not prevent injected Stimulus targets or values.
- Same-context executable module code cannot be isolated by these attributes or
  CSP alone. If an existing module needs such code, explicitly treat it as
  trusted host code or keep it outside the privileged shell under a separately
  reviewed isolated surface. Do not silently break it or claim it is sandboxed.
- No controller wraps the Tauri bridge. Native integration stays in its own
  host-owned script under P052.

### Browser hardening that precedes the controller layer

These changes reduce existing exposure, need no Stimulus and can land first:

- Disable HTMX history snapshot storage globally, for example with
  `<meta name="htmx-config" content='{"historyCacheSize":0,"refreshOnHistoryMiss":true}'>`
  (both option names are confirmed in the vendored 2.0.8 source). Load before
  HTMX starts. Remove the known `htmx-history-cache` key from current
  `sessionStorage` and legacy `localStorage` at upgrade and identity invalidation,
  together with the owned `htmx-current-path-for-history` metadata;
  never clear unrelated origin storage. Missing-history navigation reloads under
  current authorization. Per-surface `hx-history="false"` is an extra guard.
- Treat HTMX snapshots, HTTP cache and browser back/forward cache as different
  mechanisms. `no-store` and the HTMX options are not a universal bfcache ban.
  Cover `pageshow` restoration, other open windows and offline failure with a
  locked/redacted state until the current identity is revalidated. Record actual
  browser/WebView results, including absence of a stale-content flash before
  revalidation (redact before leaving where required). Do not promise erasure of
  already exported copies.
- Add matching integrity metadata for vendored HTMX, response-targets, SSE and
  the selected Stimulus asset in every owning layout. SRI checks bytes, not the
  trust of a same-origin script supplied by a module.
- Move inline scripts **and event-handler attributes** to static handlers, then
  enforce a tested CSP (including `script-src 'self'`, and a reviewed nonce/hash
  only where unavoidable). Inventory HTMX eval-dependent features and remove or
  replace them; do not enable `unsafe-eval`/`unsafe-inline` to silence breakage.
  Pin an explicit policy for `allowEval` and `allowScriptTags` after that migration.
  Same-origin script URLs must still pass fragment admission.
- P095-007/008 also own desktop forwarding or host reconstruction of cache and
  script policy. Cover bootstrap, `/app` iframe and settings documents without
  accidentally breaking framing or allowing arbitrary embedding.
- Decide `withGlobalTauri` independently of IPC authorization: removing
  `window.__TAURI__` does not remove `__TAURI_INTERNALS__` or isolate scripts
  sharing `/app`. Audit all registered commands, caller window/webview/frame
  context, arguments and permissions in the host. A private wrapper is not a
  security boundary. Keep P052's trusted-shell/native-command boundary explicit.

Additional references: [HTMX history](https://htmx.org/attributes/hx-history/),
[Tauri capabilities](https://v2.tauri.app/security/capabilities/),
[Tauri configuration](https://v2.tauri.app/reference/config/#withglobaltauri),
[beforeunload limitations](https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event).

### Test structure

- Keep the pure parts as plain modules with no DOM access: panel stack
  push/pop/limit, generation comparison, tail pinning arithmetic and the
  draft confirmation predicate. Test them with Node; the existing
  `node:tools/test-node-ui-question-deadline.cjs` demonstrates the lightweight
  runner but mocks DOM access, so it is not itself a pure-module example.
- Test lifecycle, history and focus in a real browser through one pinned driver
  (for example Playwright) recorded as an optional development dependency in
  P095-002. Keep native WebView evidence separate. Direct `tauri-driver` supports
  Windows/Linux, not macOS; on macOS select a pinned test-only embedded driver
  (such as the documented WebdriverIO Tauri service) or retain explicit manual
  evidence. Browser WebKit is not proof of the app's WKWebView/IPC behavior.
  See [Tauri WebDriver support](https://v2.tauri.app/develop/tests/webdriver/).
- Serve interaction fixtures only from test builds, never from a production
  route; exclude embedded drivers/test IPC from release artifacts too. Label any
  mocked backend and untested platform explicitly in the evidence.

## Implementation Tracker

Statuses: `todo`, `partial`, `done`, `blocked`. All rows start `todo`; upstream
documentation compatibility is not runtime completion. P095-007 and P095-008 are
framework-independent hardening steps. The isolated test-only spike may precede
them; production controller adoption may not. P095-001 to P095-005 and P095-007
to P095-011 form the first slice; P095-006 gates broader reuse rather than
expanding it silently. Hardening is not evidence that the workspace is complete.

| ID | Status | Depends on | Task and completion gate |
| --- | --- | --- | --- |
| P095-001 | todo | — | Inventory helpers; select an existing conversation/detail pair and freeze slot, history, draft lifetime and trust boundaries in the Node UI contract. Record listener/timer inventory per script, baseline measurements and rollback path. |
| P095-002 | todo | 001 | Spike pinned Stimulus + HTMX in isolated browser/Tauri fixtures: swaps, reconnect, errors, history, SSE and exactly one request per action. Verify both library initialization orders, early XHR fencing before redirects/triggers and target confinement despite response-targets/OOB. Exercise the source-confirmed history options. Record adopt/reject, driver/platform and mock boundaries; retain plain-JS fallback if rejected. |
| P095-003 | todo | 002, 007, 008, 009, 010, 011 | Implement the controller catalog and conversation/detail/return slice using the pure state modules; preserve composer, scroll and focus; retire duplicate legacy handlers, including separate chat-open and overlapping chat-history fetches. |
| P095-004 | todo | 003, 007, 008 | Retain executable evidence for every failure row, including identity change, malicious fragments, stale authority and delayed responses; verify keyboard/IME, accessibility and reduced motion. |
| P095-005 | todo | 004 | Verify browser and desktop task completion and bounded resource use against baseline; test rollback without changing domain state; synchronize Solution 001, Node UI docs, ledger and applicable MVP evidence. |
| P095-006 | todo | 005 | Reuse the same mechanics on one existing configuration or Corpus inspection surface before extracting a general library; keep writes with their current owners and document remaining platform limits. |
| P095-007 | todo | — | Disable snapshots; purge known prior history/cache keys; add no-store/Vary and desktop propagation; cover all asset includes with integrity. Gate: pre-seeded old snapshots, bfcache, offline Back and other windows after identity change cannot restore prior content; actual browser/WebView limits are recorded. |
| P095-008 | todo | — | Implement parsed fragment/response confinement or explicitly isolate incompatible surfaces; migrate inline scripts/event attributes and eval features; enforce CSP through HTTP and desktop host pages. Inventory IPC commands and enforce caller/argument scope independently of withGlobalTauri. Gate: script, same-origin src, declarative target/action/OOB and header injections cannot cross module/shell/native boundaries; framing and legitimate settings still work. |
| P095-009 | todo | 001 | Decide where the conversation lives: move it from `#orb-modal-slot` into `#app-main`, or record why the first slice uses another pair. Gate: opening details never stacks a panel inside a modal, and closing a modal restores focus to its opener. |
| P095-010 | todo | 001, 009 | Implement panel representation negotiation, authorized full-page fallbacks, validated href metadata, Vary/no-store including desktop transport, and confined response effects. Gate: direct/full/fragment requests, spoofed HX headers, unwanted response headers and OOB are tested; shell IDs remain unique after navigation. |
| P095-011 | todo | 002 | Extract pure stack/epoch/generation, tail and draft predicates. Gate: bounds, drop-oldest, failed navigation, recreated-controller stale reads, safe counter exhaustion, message-count saturation, and typing after discard consent are tested without a browser. |

## Open Questions

- Which existing conversation/detail pair avoids introducing new domain endpoints?
  P095-001 owns this selection; a mocked backend must be labelled as such.
- Does the pinned Stimulus integration simplify maintenance in practice?
  P095-002 decides; do not substitute a broad framework migration on failure.
- Should the conversation leave the modal slot for the main surface (P095-009),
  and does that change the operator console as well as `/app`?
- Can the desktop host drop the global convenience API without breaking existing
  native integration, and which command/window/frame permissions are required?
  P095-008 must resolve actual IPC authority separately from that flag.

## Next Actions

Land P095-007 first: it removes an existing history exposure and does not depend
on the framework decision. Start P095-001 in parallel, then the compatibility
spike. Do not add docking, persistent draft storage or arbitrary native windows
until the first slice passes its gates.
