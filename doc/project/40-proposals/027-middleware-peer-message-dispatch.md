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

The chain is a trait-based pipeline: `PeerMessageChain` holds ordered vectors of
trait objects (`PeerMessageHandler`, `PreSendHandler`, `AuditHandler`). The chain
does not distinguish between in-process handlers (Rust structs compiled into the
daemon) and out-of-process handlers (loopback HTTP wrappers around supervised
sidecars). Both implement the same trait interface and produce the same
`PeerHandlerOutcome`. This makes the chain a trait pipeline, not an HTTP
pipeline, and enables:

- protocol-core and constitutional concerns (identity verification, network
  ledger, memory organ observation) to participate without serialization overhead,
- operator-replaceable extensions (marketplace workflows, content processing) to
  participate through supervised sidecars with language independence and fault
  isolation.

The preferred registration surface for out-of-process modules is `input_chains`
in `middleware-module-report`.

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

## Well-Known Capability Schema Messages

The generic peer-message envelope is also the transport for capability schema
retrieval. This keeps schema exchange inside the authenticated Node-to-Node
session instead of making runtime behavior depend on an external HTTP URL.

Reserved message kinds:

| Message kind | Response kind | Intended owner |
|---|---|---|
| `capability.schema.present.request` | `capability.schema.present.response` | built-in daemon handler first, middleware fallback for custom capability stores |

Request payload:

```json
{
  "schema/ref": "orbiplex:blob:sha256:...",
  "schema/id": "urn:orbiplex:capability-profile:audio-transcription:v1",
  "accepted/media-types": [
    "application/schema+json"
  ]
}
```

Response payload:

```json
{
  "schema": "capability-schema-present.v1",
  "status": "ok",
  "artifact": {
    "schema": "capability-schema.v1"
  }
}
```

Error payload:

```json
{
  "schema": "capability-schema-present.v1",
  "status": "error",
  "error": {
    "kind": "schema-unavailable",
    "detail": "local node cannot present requested capability schema"
  }
}
```

Dispatch semantics:

- the request MUST use the same `PeerMessageEnvelope.correlation_id` response
  matching as other request/response peer messages,
- `schema/ref` is the preferred lookup key because it is content-addressed,
- `schema/id` is an optional logical-contract hint and MUST NOT replace the
  hash check implied by `schema/ref`,
- the returned `artifact` MUST conform to `capability-schema.v1`,
- the response payload MUST conform to `capability-schema-present.v1`,
- receivers MUST verify the artifact content against `schema/ref` before using
  it for scope, input, output, error, or retry validation.

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

## Observer Slots

Handlers participate in chain dispatch and may short-circuit the flow via
`Handled` or `Respond`. This is intentional: a handler that owns a message
class should be able to claim it. But short-circuiting means downstream
handlers on the same chain never see the message, and the existing audit chain
receives a frozen copy of the original input payload, not the effective payload
after mutations.

Observer slots are separate registration lists invoked unconditionally,
regardless of whether a handler returned `Handled`, `Respond`, or `Passthrough`.
Observers are fire-and-forget and cannot influence dispatch flow.

### Phase observers

Each chain phase (`pre-input`, `inbound-peer`, `pre-send`) has an optional
observer list invoked once after the phase completes (including after early
exits). Phase observers receive:

- the envelope as it entered the phase,
- the envelope as it left the phase (after mutations),
- the phase outcome (`completed`, `handled`, `responded`, `dropped`),
- the identity of the handler that claimed the message (when applicable).

Phase observers answer: "what happened during this specific phase?"

### Post-chain observers

A global observer list invoked once per dispatch, after all phases complete
(and after send, when a response was produced). Post-chain observers receive:

- the original input payload,
- the effective payload after all chain mutations,
- the response envelope (if any, after `pre-send` mutations),
- the final dispatch outcome,
- total dispatch duration.

Post-chain observers answer: "what was the final result of the full dispatch?"
This is the primary integration point for constitutional organs like Memarium
that need to see what actually happened rather than what was originally
submitted.

### Relationship to audit

The existing audit chain remains unchanged for backward compatibility.
Post-chain observers are a strict superset of audit events, carrying both the
original and effective payloads plus structured outcome metadata. New consumers
should prefer post-chain observer registration over audit registration.

### Observer registration

In-process observers implement the observer trait directly (same trait-pipeline
duality as handlers). Out-of-process observers may declare observation interest
through a dedicated `observe_chains` section in the middleware module report,
or through an `observer: true` flag on `input_chains` entries. The daemon
dispatches observer events to out-of-process modules through the same loopback
HTTP contract, but using fire-and-forget semantics (no response parsing, no
timeout blocking of the dispatch thread).

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
