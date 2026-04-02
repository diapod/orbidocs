# Node Middleware Init and Capability Reporting

This memo captures one missing extension-host contract for Orbiplex Node:
middleware modules should not remain opaque after startup.

When the Node starts and binds a middleware executor or plugin-process surface, it
should emit a host-owned `middleware-init` message. After receiving it, the module
should report:

- module name,
- short module description,
- offered capabilities,
- and optional implementation-local notes.

## Why this matters

Without an init/report handshake:

- the host cannot tell what newly attached modules actually provide,
- operator tooling sees only executor ids or local process config,
- capability routing becomes guesswork,
- and extension surfaces drift toward black-box plugin folklore.

The goal is not rich orchestration yet. The goal is simple visibility and a stable
minimum contract.

## Proposed shape

### Host-owned init message

The Node should emit a local init artifact such as:

- `middleware-init`

It should include at least:

- middleware contract version,
- host/runtime version,
- executor id,
- executor transport kind,
- optional `node-id`,
- and any narrow host capabilities the module may rely on.

### Module report

The module should return one report such as:

- `middleware-module-info-report`

It should include at least:

- module name,
- module description,
- offered capabilities.

## Semi-open capability catalog

Capability identifiers exposed by middleware modules should be semi-open.

This means:

1. some capability classes are constrained,
2. some remain open-ended.

### `base` capability class

Capabilities in the `base` class should require a stable output or behavior
contract.

Examples:

- a redaction module returning one redaction artifact shape,
- a routing policy module returning one route proposal shape,
- a transcript monitor returning one transcript-derived shape.

`base` capabilities therefore need:

- a stable capability id,
- and a reference to the expected output contract.

### `other` capability class

Capabilities in the `other` class remain open-ended.

They still need:

- a stable capability id,
- a short description,
- and output compatible with the generic middleware host contract.

But they do not need a special protocol-level output shape in MVP.

## Placement in the architecture

This contract belongs in two places:

1. `orbidocs`
   - as the canonical semantic contract,
2. `node`
   - as the implementation-facing host and runtime documentation.

The canonical rule should live in `orbidocs`, because it is part of the Node
extension model rather than one repository-specific coding trick.

The implementation specifics should also live in:

- `node/middleware/README.md`
- and typed Rust contracts under `node/middleware`

because the host/runtime details are repository-local.

## Transport-defined chain attachments

Middleware registration should describe transport attachment points, not domain
labels leaked into the router.

The preferred report surface is now `input_chains`, where each entry declares:

- `chain`
- optional `message_types`
- optional `filter`
- optional `invoke_path`

Current host-owned chain set:

- `pre-input`
- `inbound-peer`
- `inbound-broadcast`
- `inbound-local`
- `pre-send`
- `audit`

This keeps transport and semantics separate:

- the router knows only which channel the message arrived on,
- handlers decide whether the content means "capability invoke", "ledger
  query", "offer fetch", or anything else.

### Peer path

When the Node receives an inbound peer message, the daemon may forward it to
middleware via `POST /v1/middleware/invoke` with `envelope_kind:
"peer-message"` on the relevant chain.

The forwarded request carries:

- `schema_version: "v1"`
- `envelope_kind: "peer-message"`
- `msg`
- `chain_kind`
- `correlation_id`
- `remote_node_id`
- `payload`

The peer path is now stratified:

1. `pre-input`
2. built-in Rust peer handlers
3. middleware on `inbound-peer`
4. `pre-send`
5. `audit`

That split lets decorating middleware run without losing its chance to a
terminal handler later in the chain.

### Non-peer transport chains

The same `input_chains` projection now also drives two additional daemon-owned
transport adapters:

- `inbound-broadcast`
  - the daemon evaluates `message_types` and compiled `filter` before the
    sidecar round-trip,
  - `allow`, `annotate`, `rewrite`, `drop`, and `defer` are meaningful there,
  - current implementation runs this direct chain before the older
    `on-broadcast-received` hook runtime so compatibility stays intact.
- `inbound-local`
  - the daemon evaluates the registration after local auth classification and
    before routing the HTTP request to control or module-capability handlers,
  - the forwarded envelope is `local-input-invoke.v1`,
  - `allow`, `rewrite`, `return`, and `reject` are meaningful there.

`pre-send` and `audit` are currently wired to the peer response path only.

### Pre-filter shape

`input_chains[].filter` is one small JSON tree:

- `{ "msg": "offer-catalog.fetch.request" }`
- `{ "capability_id": "network-ledger" }`
- `{ "AND": [ ... ] }`
- `{ "OR": [ ... ] }`
- `{ "NOT": { ... } }`

Semantics:

- `msg` is special and matches the peer envelope kind itself,
- every other field matches `payload[field]`,
- equality is exact JSON equality; MVP does not add pattern, prefix, or range
  operators.

Example:

```json
{
  "input_chains": [
    {
      "chain": "inbound-peer",
      "message_types": [
        "capability.passport.present.request"
      ],
      "filter": {
        "AND": [
          { "msg": "capability.passport.present.request" },
          { "capability_id": "network-ledger" }
        ]
      }
    }
  ]
}
```

This means:

- the sidecar is not even considered unless `msg` matches one claimed type,
- then the daemon checks the compiled predicate locally,
- only matching envelopes cause one loopback HTTP round-trip.

### `input_chains` registration semantics

A few rules follow directly from the array structure:

**Same chain, multiple registrations.** The same chain identifier may appear more
than once in `input_chains`. The daemon builds one `MiddlewarePeerMessageRoute` per
entry, so a module can route different message classes to different HTTP handlers
within the same sidecar process.

**Empty `message_types` on `audit`.** An `audit` entry with an empty
`message_types` list and no `filter` intercepts every envelope on that chain.
Every outbound call is fire-and-forget, so this is safe but should be limited to
modules that genuinely need full visibility.

**`invoke_path` is optional.** When absent the executor-level `http.invoke_path`
(default: `/v1/middleware/invoke`) is used. A module may therefore mix explicit
per-chain paths with the executor default: only the registrations that need a
dedicated handler require an `invoke_path` override.

Backward compatibility:

- `handles_peer_message_types`
- `peer_message_filter`
- `peer_message_phase`

remain accepted for older modules and are projected by the daemon into the new
chain model.

### Session worker threading constraint

The peer message chain runs inside a dedicated `std::thread` session worker.
`MiddlewarePeerMessageHandler` therefore uses `reqwest::blocking` for the HTTP
round-trip. This means the session worker is blocked for the duration of the
sidecar call.

**Current approach (Option A — MVP):** Accept the blocking constraint. Sidecars
that declare `handles_peer_message_types` must respond within a tight timeout
(target: ≤ 50 ms). This is documented as a contract requirement. It is
sufficient for local SQLite-backed catalog operations.

**Future path (Option B — post-MVP):** Replace the blocking call with a
channel-based dispatch: `MiddlewarePeerMessageHandler` sends the envelope to a
dedicated worker thread via `std::sync::mpsc`, then returns
`PeerHandlerOutcome::Handled` immediately. The worker thread performs the
blocking HTTP call and injects the response back through the existing
`pending_responses` map in the session worker. This eliminates head-of-line
blocking and keepalive starvation under slow sidecar conditions.

Option B should be implemented when either: (a) a sidecar handler exceeds the
50 ms budget in production, or (b) a sidecar handles messages that do not
require a synchronous response to the session (pure side-effects).

## Generic outbound peer dispatch

The same middleware contract family now also includes one host-owned outbound
write capability:

- `peer.message.dispatch`

This is deliberately transport-owned, not domain-owned. A module may ask the
daemon to send one peer message either:

- to one explicit `node_id`, or
- to any peer that exposes one `capability_id`.

Capability-addressed routing lets the daemon keep ownership of:

- Seed Directory discovery,
- discovery-result memoization with TTL,
- peer-session establishment and reuse,
- one-way outbound peer send.

The typed request adds:

- `execution_mode`
  - `async`
  - `blocking`
- destination by capability with:
  - `capability_id`
  - optional `seed_filter`
  - `selection_mode`
    - `first-n`
    - `last-n`
  - `limit`
  - `delivery_mode`
    - `one`
    - `all`
  - optional `cache_ttl_ms`

`seed_filter` reuses the same JSON predicate tree shape as ingress filters, but
it is evaluated against one Seed Directory capability entry JSON object. There
is no special `msg` meaning there; dotted paths such as
`passport.capability_id` are valid.

This keeps middleware in the role of describing intent and payload, while the
daemon stays the owner of discovery and transport concerns.

## Decision semantics on `inbound-local`

### `Allow` means "continue, not stop"

`Allow` on any chain — including `inbound-local` — means "I am done with my
concern; pass to the next handler". It does not mean "I did not process this".
A middleware module may have fully validated, logged, or transformed the request
and still return `Allow`. The chain continues to the next handler regardless.

This is distinct from `Return` or `Stop`, which are the only decisions that
announce "I own the response".

### `Rewrite` + `Allow` as a pass-through with side-effect

`Rewrite` modifies the request body in place. Combined with `Allow` it becomes
a composable primitive: the module applies a transformation (validation,
normalization, enrichment) and lets the chain proceed with the modified payload.
The next handler — whether another middleware or the host core — sees the
rewritten request and acts on it as if it were the original.

This pattern is the idiomatic way to inject middleware logic into a flow without
taking ownership of the final response:

```
module validates and normalises offer draft
  → Rewrite (normalized body) + Allow
  → chain continues
  → core receives normalized offer, saves and dispatches
  → core produces the HTTP response to the caller
```

No new decision kind is needed; `Rewrite` + `Allow` covers the "transform and
delegate" use case cleanly.

### Catch-all `inbound-local` handlers

A module registered on `inbound-local` without `local_routes` receives every
request that has not been stopped by an earlier handler. This is the natural
extension point for path-agnostic concerns: generic audit trails, fallback
responders, or experimental handlers that do not yet own a specific path.

## MVP boundary

This memo does **not** require:

- dynamic network-wide module discovery,
- capability negotiation across the federated network,
- or automatic loading of arbitrary plugin classes.

It only requires that once a Node binds a local middleware module, the host can ask:

- who are you,
- what do you do,
- and which capability ids should the host attach to you.
