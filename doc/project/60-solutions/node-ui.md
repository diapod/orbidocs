# Orbiplex Node UI

`Orbiplex Node UI` is a thin control and inspection client for the Node component. It is not the protocol source of truth; it is an operator-facing surface that consumes Node APIs and exposes bounded control, diagnostics, and visibility.

## Purpose

The Node UI exists to:
- inspect Node state and protocol flows,
- expose safe operator controls,
- present provenance and policy context without re-implementing protocol semantics,
- present settlement policy health and disclosure trail context for paid flows,
- adapt to different host environments as thin clients.

## Scope

This document defines solution-level responsibilities of the Node UI component.

It does not define:
- network protocol semantics,
- canonical persistence of protocol artifacts,
- training or archival logic as a source of truth.

## Architecture Direction

The chosen hard-MVP implementation direction is recorded in:

- `doc/project/20-memos/node-ui-htmx-hateoas-architecture.md`

In summary: the Node UI is a thin HTMX web client backed by a server-side
template renderer (`node-ui` crate, Rust + Axum + MiniJinja) that proxies the
daemon HTTP control API and renders HTML fragments. HATEOAS is the navigational
model. The daemon remains the sole authority; the web server holds no protocol
state.

## Middleware Operator UI Extensions

The built-in Node UI should not need compile-time knowledge of every middleware
module and its operator-facing screens. Middleware modules, especially
non-native modules that are not shipped as part of the Node itself, should be
able to contribute their own operator UI fragments through a host-owned
extension surface.

The intended shape is stratified, data-driven registration:

- a middleware package may contribute host-rendered HTML(X) fragments through
  `middleware.package.json` and the `UiSurfaceRegistry`,
- a live middleware module may declare `operator_surfaces` in its
  `middleware-module-report`,
- the Node UI derives a bounded mount point such as
  `/middleware/{surface_id}/...`,
- the Node UI provides the shell, navigation, layout, session boundary, CSRF
  protection, daemon proxy, and route-collision checks,
- the module owns only the semantics and presentation of its own operator views.

Recommended middleware package layout:

```text
middleware.package.json
config/
  *.json
ui/
  index.html
  fragments/
  static/
ui-op/
  operator-surfaces.json
```

`ui/` is the renderable HTML(X) root. `ui-op/` is the package-local root for
operator surface declarations, examples, and binding notes corresponding to
runtime `operator_surfaces`. Keeping them separate prevents HTML fragments,
runtime discovery metadata, and daemon config fragments from collapsing into one
ambiguous directory.

The rendering modes are:

- `host-mediated`
  - Node UI renders the concrete representation, often from built-in templates
    or from a package's `ui/` directory,
  - the live module report provides presence, navigation, and capability
    metadata.
- `server-html`
  - the middleware module owns the HATEOAS/HTMX representation,
  - Node UI maps the surface through a bounded same-origin route and keeps
    auth/proxy policy host-owned,
  - this is the preferred mode for supervised Python middleware packages that
    render their own operator pages.

This keeps the UI stratified. The Node UI remains a thin host-owned projection
layer, while module-specific operator experience stays with the module that owns
the domain. Adding a new externally supplied middleware module should therefore
require package metadata, runtime `operator_surfaces`, or both; it should not
require editing Rust code in the built-in UI to teach it that the module exists.

Template execution must remain sandboxed and host-owned. A module-provided UI
extension must not receive the daemon authtok, raw ambient filesystem access, or
an unrestricted server-side execution hook. It may render against a bounded
operator context and call daemon or module endpoints only through explicit
host-owned routes.

Python middleware packages may reuse the shared stdlib helper from
`node/middleware-modules/lib/ui/python` to declare `server-html` surfaces, read
the supervised middleware environment, render small HTML documents, and call
host capabilities server-side. The helper is a developer convenience, not a new
UI runtime: state and representation still belong to the middleware service,
while the public route, proxy policy, navigation, and auth boundary remain owned
by Node UI.

## Must Implement

### Node Control Surface

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/project/20-memos/pod-backed-thin-clients.md`

Related schemas:
- `answer-room-metadata.v1`
- `response-envelope.v1`

Responsibilities:
- expose bounded controls for room participation and answer review,
- show enough room metadata for an operator to understand scope and policy,
- avoid becoming a second protocol authority beside the Node.

Status:
- `partial` — Node UI exposes daemon status, execution lists/details,
  participant accept/reject/dispute controls, review/promotion panels,
  receipts, component registry, workflow runs, and settlement-linked details.
  It remains thin over daemon APIs and is not a protocol authority.

### Provenance and Policy Inspection

Based on:
- `doc/project/40-proposals/004-human-origin-flags-and-operator-participation.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/50-requirements/requirements-005.md`

Related schemas:
- `transcript-segment.v1`
- `transcript-bundle.v1`
- `learning-outcome.v1`
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`

Responsibilities:
- render provenance and human-origin markers in operator-visible views,
- expose policy and scope information without flattening semantics,
- make unresolved and quarantined states clearly distinguishable,
- render settlement policy degradation, suspension, and manual-review conditions before an operator commits to a paid path.

Status:
- `partial` — execution detail renders status, review state, learning outcomes,
  linked receipts, participant limits, trace/provenance, and settlement context.
  Full transcript/human-origin inspection remains downstream of transcript
  monitoring.

### Settlement Policy Inspection

Based on:
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/50-requirements/requirements-007.md`
- `doc/project/50-requirements/requirements-008.md`

Related schemas:
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`

Responsibilities:
- show the active settlement policies attached to a paid procurement path,
- surface recent settlement disclosure events with their scope and impact mode,
- let the operator inspect why a paid path is blocked, degraded, or forced into manual review,
- preserve audit joins from procurement contracts and receipts back to their governing settlement policies.

Status:
- `partial` — paid execution detail, receipts, ledger accounts/holds, gateway
  top-ups, and manual settlement actions are visible in Node UI. Broader
  disclosure exploration is still an operator-surface hardening item.

## May Implement

### Archivist and Retrieval Views

Based on:
- `doc/project/30-stories/story-003.md`
- `doc/project/50-requirements/requirements-003.md`

Related schemas:
- `archival-package.v1`
- `retrieval-request.v1`
- `retrieval-response.v1`

Responsibilities:
- show archival status and retrieval metadata,
- provide bounded operator affordances for archival handoff and retrieval inspection.

Status:
- `optional`

## Consumes

- `answer-room-metadata.v1`
- `response-envelope.v1`
- `learning-outcome.v1`
- `archival-package.v1`
- `retrieval-response.v1`
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`

## Produces

- no canonical protocol artifacts by default

## Related Capability Data

- `node-ui-caps.edn`

## Notes

Different host-specific clients may exist for desktop, browser, terminal, or pod-backed thin-client contexts, but they should remain thin surfaces over Node behavior.

Settlement inspection belongs in the UI because operators need a bounded view of
why paid actions are available, delayed, or suspended. The UI still must not
become an independent settlement authority.
