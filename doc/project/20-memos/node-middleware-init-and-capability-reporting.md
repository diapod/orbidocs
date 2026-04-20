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

It may also declare module-owned operator UI extensions. This is especially
important for non-native middleware modules that are not shipped with the Node:
the built-in operator UI should not need to know about new modules at compile
time in order to expose their local management screens.

The report is the right registration boundary for a future optional
operator-UI declaration because it is already the host-owned startup handshake
where a module says: "this is what I provide". The declaration should describe
UI routes, templates, navigation labels, and required local operator
capabilities as data. It should not require the Node UI to import module code or
hard-code module-specific pages.

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

## Factory config, node config, and runtime projection

Middleware config layering should stay explicit and stratified.

Three layers exist:

1. `factory_config`
   - comes from bundled middleware defaults under
     `middleware-modules/<service-dir>/config/*.json`
   - expresses only the module's own typed defaults such as `dator` or `arca`
2. `node_config`
   - comes from `<data_dir>/config/*.json`
   - expresses operator overrides and node-level policy
3. `effective_runtime_config`
   - built by the daemon as `deep_merge(factory_config, node_config)`
   - then enriched with host-owned runtime projections

Seeded node-level middleware fragments should therefore stay narrow. When the
daemon materializes a missing `50-<module-key>.json`, that file should contain
only `{ "<module-key>": { ...factory defaults... } }`. Only factory entries
with `seed_config = true` should be materialized this way; bundled modules
without that flag remain opt-in until the operator defines their top-level
subtree in node config.

Host-owned runtime sections such as:

- `middleware_http_local_services`

belong to the runtime projection layer. They may be visible in resolved daemon
config and diagnostics, but they should not be persisted back into the seeded
factory fragments. That keeps the operator-facing files clean and preserves the
boundary between module defaults, node overrides, and host execution strategy.

The same separation now applies to daemon-state checkpointing:

- operator config may set `state_checkpoint_interval_ms`,
- the resulting checkpoint artifact lives under
  `<data_dir>/storage/checkpoints/daemon-state.v1.json`,
- the checkpoint file is part of runtime state and diagnostics,
- it is not part of factory middleware config and must never be projected back
  into seeded `50-<module-key>.json` fragments.

The same principle applies to machine-readable contract artifacts published by
the host:

- runtime read models such as the local service-offer snapshot may be exposed as
  read-only JSON Schema under endpoints like `/v1/schemas/service-offer-snapshot`,
- middleware may consume those artifacts for validation and diagnostics,
- but the schema artifacts remain host-owned runtime surfaces, not module
  factory config.

## Operator UI extension declarations

Middleware operator UI should be registered as another host-owned projection,
not as hidden coupling between a module and the built-in Node UI.

A future `middleware-module-report` extension should allow a module to declare:

- module-scoped UI routes such as `/modules/{module_id}/settings` or
  `/modules/{module_id}/templates`,
- template or fragment identifiers served from the module package or from a
  host-materialized module UI directory,
- optional static assets under a module-owned namespace,
- navigation labels and grouping hints for the operator shell,
- required local operator capabilities or permissions for each route,
- whether the route renders host-side templates, proxies a bounded module
  endpoint, or links to an externally supervised local surface.

The Node UI owns:

- route collision prevention,
- the common operator shell and navigation,
- authentication and session boundaries,
- CSRF and form-submission protection,
- the daemon authtok boundary,
- template sandboxing and allowed helper functions,
- and audit-visible registration diagnostics.

The middleware module owns:

- the meaning of its own operator screens,
- its own templates or fragment descriptors,
- module-specific validation labels and help text,
- and any module endpoint that is explicitly proxied by the host.

The route namespace must stay bounded. The default mount should be under a
module-scoped path such as `/modules/{module_id}/...`; arbitrary claims over the
root operator UI are not part of the contract. This mirrors `inbound-local`
`local_routes` on the daemon side, but it is a separate UI projection contract:
claiming a daemon HTTP route does not automatically claim an operator UI route.

Until this field is added to the committed Rust and JSON Schema contracts,
implementations should treat operator UI extension registration as a design
direction, not as a valid wire field in `middleware-module-report`.

## Transport-defined chain attachments

Middleware registration should describe transport attachment points, not domain
labels leaked into the router.

The preferred report surface is now `input_chains`, where each entry declares:

- `chain`
- optional `message_types`
- optional `filter`
- optional `invoke_path`
- optional `local_routes` (only valid on `inbound-local`)
- optional `skip_generic_chain` (only valid on `inbound-local`)

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
  - `allow`, `rewrite`, `return`, and `reject` are meaningful there,
  - a module may claim one or more exclusive HTTP paths through `local_routes`;
    relative paths such as `"pong-game"` resolve to `/v1/enact/pong-game`,
  - only one module may own one `(METHOD, path)` pair; the daemon returns `503`
    with `Retry-After` when the owning module is not yet ready,
  - `skip_generic_chain` controls whether the entry also participates in the
    generic dispatch loop (see "Generic dispatch on `inbound-local`" below).

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

### Generic dispatch on `inbound-local`

A module that declares `local_routes` on `inbound-local` but sets no
`message_types` and no `filter` would otherwise participate in the generic
dispatch loop for *every* local HTTP request — an unintended side-effect of
empty `message_types` matching all messages.

`skip_generic_chain` provides explicit control:

- **absent** (`null`): auto-infer. The daemon skips the entry from generic
  dispatch when all of the following hold: `chain == inbound-local`,
  `local_routes` is non-empty, `message_types` is empty, `filter` is absent.
  This is the sensible default for claimed-route-only modules.
- **`false`**: force participation in generic dispatch even when the auto-infer
  conditions are met. Use this when a module claims routes *and* wants to act
  as a generic fallback or auditing layer on all other local requests.
- **`true`**: unconditional early skip. The daemon skips the entry from generic
  dispatch without evaluating any conditions.

The field is only valid on `inbound-local`; the daemon rejects it on any other
chain.

## MVP boundary

This memo does **not** require:

- dynamic network-wide module discovery,
- capability negotiation across the federated network,
- or automatic loading of arbitrary plugin classes.

It only requires that once a Node binds a local middleware module, the host can ask:

- who are you,
- what do you do,
- and which capability ids should the host attach to you.
