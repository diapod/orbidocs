# Node UI: HTMX and HATEOAS Web Client Architecture

Based on:
- `doc/project/60-solutions/node-ui.md`
- `doc/project/20-memos/pod-backed-thin-clients.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`

Date: `2026-03-30`
Status: Accepted architecture note

## Purpose

This memo records the chosen architectural direction for the Node UI component
and the reasoning behind it. The `node-ui.md` solution document intentionally
does not freeze a toolkit or deployment shell. This note fills that gap for the
hard-MVP implementation path.

## Decision

The Node UI should be implemented as a thin HTMX web client backed by a
server-side template renderer, using HATEOAS as the navigational model.

The three-layer shape is:

```
browser (HTMX)
      ↕  HTML fragments
  web server  (template renderer + daemon proxy)
      ↕  JSON + authtok
    daemon  (source of truth)
```

The web server has one responsibility: translate daemon JSON responses into HTML
fragments and route operator actions back to the daemon. It holds no protocol
state of its own.

## Rationale

### No second state model to synchronize

The daemon already owns all meaningful state: executions, offers, receipts,
holds, policies, and settlement outcomes. A SPA-style client would introduce a
second in-browser state model that must be kept in sync with the daemon. HTMX
with server-side rendering avoids this entirely: HTML is the state, the daemon
is the source of truth, and the web server is a stateless projection layer.

### HATEOAS is already a project preference

The project CLAUDE.md states: *"preferujemy HATEOAS: hipermedia ma prowadzić
klienta przez dozwolone przejścia stanu i operacje, zamiast wymagać twardo
zakodowanej wiedzy o przepływach"*. The Node daemon already models resources
with bounded state transitions: execution lifecycle, offer catalog, hold states,
dispute resolution. HATEOAS is the natural expression of what the daemon already
provides, not an imposed pattern.

### Toolkit alignment

The web server lives in the same Rust workspace as the rest of the node. It
reuses the existing daemon HTTP client pattern and the authtok auth model. No
new runtime dependency is introduced.

## Recommended Implementation Stack

- **Web server**: Rust + Axum, as a separate `node-ui` crate and binary within
  the node workspace.
- **Templates**: MiniJinja with runtime file loading. This keeps Jinja-style
  templates on disk and removes the "edit template -> recompile the whole UI
  binary" loop that would otherwise slow down HTMX-oriented operator UI work.
- **Template reload**: `minijinja-autoreload` in the `node-ui` process. In
  development, template edits should become visible on refresh without a Rust
  rebuild.
- **Frontend**: vendored HTMX plus the `response-targets` extension served from
  local static files. No build toolchain, no bundler, no JS framework.
- **Deployment**: separate binary started by the launcher alongside the daemon,
  bound to loopback only.

## Authtok Boundary

The authtok must never reach the browser. The web server reads the authtok from
the local file (same as the launcher) and uses it server-side for all daemon
calls. The browser holds only a web server session, which on localhost may be
simplified to no-auth or a minimal cookie-based session for the MVP.

Exposing the authtok to the browser would allow any page running in the browser
to reach the daemon control plane directly. This must be prevented by
construction, not by convention.

## Real-Time Updates

The daemon already exposes `/v1/events` as a local SSE stream, but the first
hard-MVP `node-ui` slice can still rely on simple HTMX polling for execution
detail fragments:

```html
<div hx-get="/executions/{{id}}/fragment"
     hx-trigger="every 3s"
     hx-swap="outerHTML">
```

Polling should be conditional: active only when the execution is in a
non-terminal state. Once a terminal state is reached the trigger should not
fire.

The existence of `/v1/events` means later migration to SSE is now an integration
step rather than a daemon prerequisite. The UI structure should stay compatible
with that later swap.

## What the Web Server Must Not Do

- implement any protocol semantics,
- make procurement or settlement decisions,
- sign or author any protocol artifacts,
- hold procurement state independently of the daemon,
- expose the authtok to the browser.

The web server is a projection and routing layer. The daemon remains the sole
authority for all node behavior.

## Failure Modes

**Daemon unreachable**: the web server should render a clear degraded state
rather than a blank page or an unhandled error. The operator needs to know
whether the daemon is down or the UI layer itself has failed.

**Stale polling view**: if the polling interval is too long, the operator may
act on a stale execution state. The web server should pass the daemon's
`last-modified` or sequence marker through to the rendered fragment so the
browser can detect staleness.

**Authtok rotation**: if the daemon rotates its authtok, the web server must
reload it from disk before the next daemon call fails. A simple retry-on-401
with a fresh file read is sufficient.

**Slow template iteration**: compile-time templates would make frequent HTMX UI
tweaks unnecessarily expensive because every markup change would require a Rust
rebuild. Runtime-loaded MiniJinja templates avoid that failure mode for this
component.

## Next Actions

1. Keep the `node-ui` crate on Axum plus MiniJinja rather than reverting to
   compile-time templates.
2. Preserve the authtok boundary strictly server-side in every handler and
   rendered template.
3. Keep execution polling conditional on non-terminal execution state.
4. Add `node-ui` startup to the launcher alongside the daemon.
5. Integrate `/v1/events` into the UI once the initial polling-backed operator
   flow stabilizes.

Promote to: proposal when the template surface and the operator control
affordances are stable enough to freeze as a Node-side local contract.
