# Bounded Local Server Runtime

**Status:** Implemented (MVP)
**Based on:** internal node code audit finding A01
**Date:** 2026-04-29

## Executive Summary

A shared sync TCP/HTTP mini-server primitive (`bounded-server` crate) replaces
ad-hoc `thread::spawn` accept loops in the daemon health endpoint, Seed
Directory, Agora service, and daemon peer listener. Python supervised
middleware uses the analogous `bounded_http.py` helper around the stdlib
`ThreadingHTTPServer`. Every server surface governed by these primitives gets
bounded accepts or active-request permits, fast overload rejection, and
first-class shutdown drain or daemon-supervised shutdown with metrics.

## Context and Problem Statement

Before this solution, four server surfaces used unbounded or separately bounded
`thread::spawn` accept/session loops without a shared resource contract:

1. Daemon health endpoint (`daemon/src/endpoint_routes.rs`)
2. Seed Directory (`seed-directory/src/lib.rs`)
3. Agora service (`agora-service/src/main.rs`)
4. Daemon peer listener (`daemon/src/peer_supervisor.rs`)
5. Bundled Python middleware (`middleware-modules/*/service.py`)

A small number of slow or malicious clients could exhaust the process thread
limit, memory, or both. Shutdown was not coordinated — active handlers could
continue running after the accept loop exited.

## Proposed Model

A single `bounded-server` crate providing:

- **`BoundedServerConfig`** — resource contract: `max_connections`, per-socket
  read/write timeouts, handler timeout, shutdown grace period, backoff intervals.
- **`BoundedServerHandle`** — running server: `local_addr`, `stop()`,
  `wait()` for externally owned stop tokens, `stop_token()`, and `metrics()`
  snapshot.
- **`ConnectionHandler` trait** — single-method handler interface. Each accepted
  connection acquires a permit; the permit is released automatically when the
  handler returns.
- **Overload behaviour**: when all permits are held, new connections receive a
  fast HTTP 503 before the TCP socket is closed. No thread is spawned for
  rejected connections.
- **Shutdown**: the stop signal closes the accept loop. Workers poll a shared
  stop flag on a 250ms interval and exit when the receiver disconnects. The
  server joins worker threads and returns final metrics. This sync primitive
  does not preempt a handler thread; handlers must enforce read/write deadlines
  and return.
- **Thread pool**: a fixed-size pool of `max_connections` worker threads pulls
  from a bounded `sync_channel`. The channel depth equals `max_connections`,
  doubling as an overload signal when `try_send` fails.
- **Metrics**: `active_connections`, `accepted_total`,
  `rejected_over_capacity_total`, `handler_errors_total`, `shutdown_drain_ms`,
  `last_accept_error`, `last_handler_error`.
- **Daemon resource pressure surface**: `/v1/runtime-metrics` exposes a
  `resource_pressure` object with OS parallelism, best-effort process thread
  count where available, supervised middleware HTTP totals, and scheduler
  active/queued/registered job counts. Node UI mirrors that summary on the
  Status page.

For Python middleware, `BoundedThreadingHTTPServer` keeps the familiar stdlib
`BaseHTTPRequestHandler` programming model but gates active requests with
`ORBIPLEX_MIDDLEWARE_MAX_CONNECTIONS` (default: 32). When no permit is
available it writes a minimal HTTP 503 response and closes the socket without
starting another handler thread.

## Production Invariant

No production local server path may create one unbounded thread per accepted
connection or request. A sync server must either use the Rust `bounded-server`
primitive, the Python `BoundedThreadingHTTPServer` helper, or an equivalent
bounded executor with explicit overload behavior. Reload and restart paths must
use cooperative bounded drain. If a supervised process cannot be stopped within
its configured stop/kill budget, the daemon/operator surface must report the
remaining process rather than hiding it as a successful shutdown.

## Trade-offs

| Benefit | Risk / Constraint |
|---|---|
| Single contract for all sync mini-servers | Thread-per-connection still used; bounded but not async |
| No new dependency (pure std) | `sync_channel` + `Arc<Mutex<Receiver>>` adds contention at high scale |
| Fast 503 rejection before thread spawn | 503 body may not reach client if TCP buffers are full |
| First-class shutdown drain | Worker exit latency up to 250ms while idle; active handlers must return cooperatively |
| Simple `ConnectionHandler` trait | Does not support streaming responses natively |

## Failure Modes and Mitigations

- **Channel disconnect**: workers notice `RecvTimeoutError::Disconnected` and
  exit gracefully. The server join thread waits for all workers.
- **Worker panic**: handler panics are caught at the per-connection boundary,
  counted as `handler_errors_total`, stored as `last_handler_error`, and the
  worker continues serving later connections.
- **Accept error**: logged to `last_accept_error` metric; accept loop sleeps
  for `accept_error_backoff` and retries.
- **Slow handler during shutdown**: the server does **not** preempt handlers.
  It waits for them to finish. The `shutdown_grace` value is the intended
  operational budget and is reflected in metrics, but handler code remains
  responsible for honoring socket deadlines and returning.

## Deferred Questions

1. Should a later async runtime add a handler deadline that the server enforces (e.g., via
   `set_read_timeout` already applied, but no preemption)?
2. Should the peer supervisor's session worker lifecycle also share a richer
   cooperative shutdown token, or is the listener-level bounded gate sufficient
   for M23-M25/A01 closure?

## Next Actions

- [x] Implement `bounded-server` crate with contract tests.
- [x] Migrate daemon health endpoint.
- [x] Migrate Seed Directory server.
- [x] Migrate Agora service.
- [x] Migrate daemon peer listener.
- [x] Migrate bundled Python middleware to `BoundedThreadingHTTPServer`.
- [x] Expose daemon resource pressure in runtime metrics and Node UI status.
- [x] Add bounded Python HTTP helper test for fast 503 rejection.
- [ ] Add integration test that verifies 503 under load in a real daemon context.
