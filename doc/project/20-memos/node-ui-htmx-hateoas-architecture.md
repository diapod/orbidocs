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
- **Templates**: Askama — compile-time typed templates. Template errors surface
  at compile time, not in production.
- **Frontend**: HTMX loaded from CDN or bundled statically. No build toolchain,
  no bundler, no JS framework.
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

The daemon does not yet have an SSE event stream. For hard MVP, HTMX polling
covers operator-visible liveness:

```html
<div hx-get="/executions/{{id}}"
     hx-trigger="every 3s [status == 'in_progress']"
     hx-swap="outerHTML">
```

Polling should be conditional: active only when the execution is in a
non-terminal state. Once a terminal state is reached the trigger should not
fire.

When the daemon gains a `/v1/events` SSE endpoint, the template switches to
`hx-ext="sse"` without changes to the rest of the UI structure.

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

## Next Actions

1. Add `node-ui` crate to the node workspace with Axum and Askama dependencies.
2. Implement daemon proxy client reusing the authtok file read pattern from
   `launcher/src/daemon_control.rs`.
3. Implement initial template set covering: daemon status, execution list,
   execution detail with state-conditional action forms, offer catalog,
   account and hold summary.
4. Add `node-ui` startup to the launcher alongside the daemon.
5. Replace polling with SSE once the daemon exposes `/v1/events`.

Promote to: proposal when the template surface and the operator control
affordances are stable enough to freeze as a Node-side local contract.
