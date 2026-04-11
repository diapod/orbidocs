# Proposal 027: Middleware Peer-Message Dispatch

## Status

Accepted for MVP.

## Problem

Orbiplex Node already has three middleware integration shapes:

- host-owned workflow envelope execution through `POST /v1/module-dispatch/execute`,
- local middleware gate decisions through `POST /v1/middleware/invoke`,
- built-in in-process peer protocol handlers through the daemon-owned
  `PeerMessageHandler` chain.

Without one bridge between the peer message chain and local sidecars, every new
peer-facing capability must either:

- be compiled into the daemon as a Rust handler,
- or open a parallel network surface outside the authenticated peer session.

That would grow the trusted daemon core and duplicate transport channels.

## Decision

Middleware modules attach to transport-defined host chains, not to
domain-labeled router branches.

The preferred registration surface is `input_chains` in
`middleware-module-report`.

For the peer path the relevant chains are:

- `pre-input`
- `inbound-peer`
- `pre-send`
- `audit`

Modules may still use the older peer-only compatibility fields:

- `handles_peer_message_types`
- `peer_message_filter`
- `peer_message_phase`

but the daemon projects those into the transport-defined chain model.

For each claimed `msg` kind, the daemon may forward the inbound peer message to
the module through the existing loopback middleware invoke endpoint:

- `POST /v1/middleware/invoke`

The daemon sends a new host-owned request envelope:

- `peer-message-invoke.v1`

with fields:

- `schema_version`
- `envelope_kind = "peer-message"`
- `msg`
- `chain_kind`
- `correlation_id`
- `remote_node_id`
- `payload`

The module responds with the existing `MiddlewareDecision` contract.

Each registration may also override the executor-level invoke endpoint through
optional `input_chains[].invoke_path`. When absent, the daemon reuses the
default `http.invoke_path`.

## Pre-Dispatch Filtering

`input_chains[].filter` is compiled by the daemon once, at middleware
registration time. The compiled predicate is evaluated before any loopback HTTP
call is made.

Supported predicate nodes:

- `{ "msg": "..." }`
- `{ "field": value }`
- `{ "AND": [ ... ] }`
- `{ "OR": [ ... ] }`
- `{ "NOT": { ... } }`

Semantics:

- `msg` matches the peer envelope kind itself,
- every other field matches `payload[field]`,
- comparison is exact JSON equality.

Evaluation order:

1. `pre-input` middleware runs first,
2. built-in Rust handlers get next chance,
3. `inbound-peer` sidecar routes are considered only if `msg` appears in the
   claimed `message_types`,
4. if present, the compiled `filter` is evaluated locally,
5. only then does the daemon call `/v1/middleware/invoke`,
6. response traffic may then flow through `pre-send`,
7. `audit` runs after send as fire-and-forget observation.

This keeps the sidecar path cheap for hot sessions while still letting module
authors describe domain-local interest declaratively.

The same projection mechanism now also feeds `inbound-broadcast` and
`inbound-local`; this proposal remains peer-focused, but the runtime no longer
special-cases peer registration as a one-off shape.

## Outbound counterpart

The node now also carries one generic outbound host capability:

- `peer.message.dispatch`

This is not a new public transport surface. It is one local host-owned write
contract that lets middleware ask the daemon to send one peer message either:

- to one explicit `node_id`, or
- to one capability-selected peer set resolved through Seed Directory.

The outbound contract intentionally separates:

- candidate selection:
  - `selection_mode = first-n | last-n`
  - `limit`
- delivery semantics:
  - `delivery_mode = one | all`

That avoids overloading one field with both "which targets are considered" and
"how many successful sends are required".

Capability-routed dispatch may also carry:

- optional `seed_filter` using the same JSON predicate tree shape as inbound
  middleware filters,
- optional `cache_ttl_ms` for discovery-result memoization,
- `execution_mode = async | blocking`.

`seed_filter` is evaluated against the Seed Directory entry JSON itself, so
there is no special `msg` meaning on that path; dotted paths such as
`passport.capability_id` are the intended form.

## Decision Semantics For Peer Messages

In peer-message context only three decisions are meaningful:

- `return`
  - the module handled the message,
  - `patch` is used as the payload of the peer response sent back to the
    remote node,
- `drop`
  - the module handled the message,
  - no peer response is sent,
- `allow`
  - the module does not claim the message,
  - the daemon continues to the next peer handler in the chain.

Other decision kinds remain valid in the generic middleware contract, but the
daemon treats them as unexpected for peer-message dispatch and falls through.

## Ordering In The Chain

The daemon-owned peer message chain is ordered:

1. `pre-input` middleware,
2. built-in capability handlers,
3. middleware sidecar handlers on `inbound-peer`,
4. `pre-send` middleware,
5. `audit` middleware.

This preserves a small trusted core while still allowing decorating middleware
to run deterministically before terminal handlers claim a message.

## Rust Middleware

This proposal does not force all middleware through loopback HTTP.

Rust-native middleware can still implement the daemon-owned `PeerMessageHandler`
trait directly and join the chain in-process. The HTTP bridge exists for
supervised local sidecars, not as the only extension surface.

## Operational Boundaries

- The session worker currently runs in a dedicated `std::thread`, so the
  loopback call uses `reqwest::blocking`.
- Sidecars claiming peer messages must respond within the configured local HTTP
  timeout budget.
- Sidecars should treat `remote_node_id` as an informational trust input, not
  as an authority stronger than the already-authenticated peer session.

## Consequences

Positive:

- one authenticated peer channel for network-ledger, offer-catalog, and future
  middleware-backed capabilities,
- no extra public TCP listeners,
- a smaller daemon core with a stable extension seam,
- compatibility with existing supervised HTTP middleware modules.

Additional positive effect:

- one sidecar can cheaply subscribe to one narrow payload family without
  re-parsing and rejecting every matching `msg` inside its own request handler.

Trade-off:

- a slow sidecar can temporarily head-of-line block one session worker thread.

This is acceptable for MVP and bounded local handlers such as `arca`.
