# Orbiplex Agora

`Orbiplex Agora` is a Node-attached solution component that provides a
**topic-addressed, content-addressed, signature-verified record relay** and
shared record substrate for the swarm. It is the common ground under multiple
existing record families — resource opinions, comments, whisper signals,
seed-directory announcements, federated offer listings — that today each
invent their own bespoke store.

Agora does not own the meaning of any particular record kind. It owns the
envelope, the topic shape, the canonicalization rules, the signature domain,
the content addressing, and the ingest/query/subscribe surface. Per-kind
semantics (what a `resource-opinion.v1` *means*, what a `plain-comment.v1`
answers) live in their own proposals and schemas and travel as
`content/schema` + `content` inside the Agora envelope.

The v1 deployment runs as a supervised middleware service under the Node
daemon (`http_local_json`-style executor), reachable on loopback, discovered
by clients through the Node's host capability API under the capability id
`agora.relay`.

## Purpose

The component is responsible for the solution-level execution path of:

- accepting signed `agora-record.v1` envelopes from local authors (host signer
  binding the author's primary participant key),
- validating envelope structure, content-schema conformance, topic ACLs,
  content-addressing, and signature domain,
- persisting accepted records in a local-first backend,
- serving record-by-id, topic listing, subject-index (`record/about`)
  listing, and SSE subscription surfaces,
- federating over a Matrix-based relay transport for canonical / cache / origin
  relay roles,
- honoring per-topic retention policy with a periodic sweep,
- being discoverable through the node's capability-routing surface under a
  uniform capability id (`agora.relay`), with optional `agora.relay` capability
  passport for federation discoverability.

## Scope

This document defines solution-level responsibilities of the Agora component.

It does not define:

- the semantic meaning of any specific `content/schema` carried inside an
  Agora record (that lives in the per-kind proposal, e.g. proposal 026 for
  `resource-opinion.v1`),
- content moderation, reputation weighting, or listener-side filtering —
  these are the listener's concern,
- whether the relay runs in-process with the daemon or as a separate program;
  v1 bundles it as a supervised Rust binary, but the solution contract does
  not require that shape,
- how federation topology is chosen at the capability-passport / seed-directory
  layer — Agora only offers the relay endpoint; the passport model decides who
  gets routed to whom.

## Must Implement

### Agora Record Signing

Based on:
- `doc/project/30-stories/story-008-cool-site-comment.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Related schemas:
- `agora-record.v1`

Responsibilities:
- canonicalize the unsigned `agora-record.v1` payload (schema, topic/key,
  author/participant-id, authored/at, content/schema, content, record/about)
  into the canonical signing bytes for the `agora.record.v1` domain,
- obtain an Ed25519 signature through the daemon's host signer using
  `KeyRef::PrimaryParticipant` (MVP) or, at a future layer, through a proxy
  key bound by `key-delegation.v1` (see `may-implement`),
- verify that the public key returned by the signer matches the author's
  `participant/did:key` fingerprint,
- compute `record/id` as
  `sha256:<base64url-no-pad(sha256(canonical_content_address_bytes))>` and
  return it with the signature to the caller.

Status:
- `done` in the Node reference implementation. `agora-core` owns canonical
  bytes, record-id derivation, and `sign_agora_record_via_host`; `agora-service`
  exposes `POST /v1/agora/records.sign` over the daemon HostSigner path.

### Agora Record Ingest

Based on:
- `doc/project/30-stories/story-008-cool-site-comment.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Related schemas:
- `agora-record.v1`

Responsibilities:
- re-verify envelope structure and canonical `record/id` on ingest,
- verify the `signature.value` against the author's public key in the
  `agora.record.v1` domain,
- apply the topic ACL gate (who may post what `record/kind` to which
  `topic/key`),
- reject duplicates idempotently (same `record/id` → `200 OK`),
- persist the record in the local relay backend,
- hand off to the federation transport when policy so requires.

Status:
- `done` in the Node reference implementation. `agora-service` gates ingest
  through topic ACL, content-schema validation, signature verification,
  idempotent persistence, and the configured relay backend.

### Agora Record Query

Based on:
- `doc/project/30-stories/story-008-cool-site-comment.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Related schemas:
- `agora-record.v1`
- `resource-ref.v1`

Responsibilities:
- serve `record/id`-keyed exact lookup,
- serve bounded topic listings with cursor pagination,
- serve `record/about` subject-index listings
  (`{resource/kind, resource/id}` pair → records mentioning that subject),
- keep paging semantics stable across backends (SQLite v1, pluggable later).

Status:
- `done` in the Node reference implementation. The HTTP surface serves
  record-id lookup, bounded topic listings, and `record/about` subject-index
  listings over stable cursor semantics.

### Topic Subscribe Stream

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Related schemas:
- `agora-record.v1`

Responsibilities:
- hold a server-sent events (SSE) connection open per subscriber,
- deliver newly accepted records on the subscribed `topic/key` in
  authored-at order,
- honor subscription start cursors (`from-now`, `from-record-id`),
- enforce backpressure / lag bounds per subscription.

Status:
- `done` in the Node reference implementation. Topic SSE subscription is live
  through the Agora HTTP API and proxied by Node UI for browser clients.

### Topic ACL Gate

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Responsibilities:
- enforce `(topic/key, record/kind, content/schema)` admission rules,
- decide whether a relay role (canonical / cache / origin) is authoritative
  for a given topic,
- keep ACL evaluation implementation-agnostic of transport (same rules for
  local ingest and federated ingress).

Status:
- `done` in the Node reference implementation. `agora-service` applies the
  data-driven topic ACL before local ingest and uses the same rule family for
  federated ingress decisions.

### Matrix Relay Transport

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Related schemas:
- `agora-record.v1`

Responsibilities:
- publish accepted records as Matrix state/timeline events under topic-keyed
  rooms per the relay-role model (canonical / cache / origin),
- ingest inbound Matrix events, re-validate as ordinary Agora records, and
  apply the same ingest contract as the local path,
- expose canonical-topic, cache-topic, and origin-topic behaviors as
  deployment-configurable roles.

Status:
- `done` in the Node reference implementation. `agora-matrix-client` and
  `agora-relay-matrix` provide Matrix-backed publish, inbound sync, and
  store-and-forward relay behavior.

### Retention Policy Sweep

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Responsibilities:
- run a periodic sweep per configured `retention_sweep_interval_secs`,
- evict records older than `max_age_secs` per topic,
- trim topics exceeding `max_count` entries,
- preserve canonical-role durability contracts where applicable.

Status:
- `done` in the Node reference implementation. `agora-service` starts the
  configured retention sweep over per-topic retention policies.

## May Implement

### Agora Relay Capability Passport

Based on:
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Related schemas:
- `capability-passport.v1`

Responsibilities:
- advertise `agora.relay` as a capability offered by this relay for
  federation-scoped discoverability,
- expose the relay endpoint, supported topics, and relay role through the
  passport payload,
- remain optional: a relay without an `agora.relay` passport is still a valid
  local relay (see proposal 035 §5.7).

Status:
- `optional`

### Proxy-Key Delegated Signing

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`

Related schemas:
- `agora-record.v1`
- `key-delegation.v1`

Responsibilities:
- accept sign requests that carry a `DelegationProof` instead of signing with
  `PrimaryParticipant`,
- verify the proof through a pluggable `DelegationProofVerifier`
  (fail-closed fallback by default; capability-bridge verifier in production),
- bind the proxy public key to the record, keep the principal's participant
  id as the author, and attach the inline proof so verifiers can check the
  delegation without remote lookups.

Status:
- `partial`: envelope fields, fail-closed verifier hook, capability grant,
  bridge verifier, and delegated example fixture are implemented. Accept
  paths, `records.sign` with `key_delegation`, Python delegated verifier,
  and UI support remain pending.

### Aggregate Status Surface

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Responsibilities:
- expose `/v1/agora/status` with relay role, configured topics, backend
  health, last sweep timestamp, and outbound Matrix transport state,
- remain cheap, cacheable, and suitable for operator inspection.

Status:
- `optional`

## Future Hot-Path Optimizations

The v1 loopback HTTP shape is acceptable for record traffic where the
per-record cost is already dominated by Ed25519 signing and backend
durability — story-008-style comments are a representative example. For
producers that emit records at a rate where loopback round-trips become
the dominant cost (any high-frequency, bounded-latency record source),
two deferred options are available without changing the envelope, the
signing domain, or the `record/id` formula.

### Batch Ingest

A single `POST /v1/agora/records` can accept N records in one request
instead of one. The loopback round-trip amortizes across the batch, and
after roughly fifty records the per-record transport cost falls below
the per-record canonicalization and signing cost. This is the dominant
optimization in comparable systems and keeps every other contract
untouched: topic ACL, content-schema validation, signature verification,
and idempotent persistence are applied per-record inside the batch, and
the backend still sees one-record-at-a-time semantics. If the v1 HTTP
surface does not already accept batched bodies, this should be a small
dedicated proposal rather than a change to proposal 035.

### Agora as In-Process Daemon Library

The solution contract (see `Scope` above) explicitly allows Agora to run
either as a supervised separate program or as an in-process module of
the daemon. Moving the in-process shape from "allowed" to "delivered"
removes the second loopback hop: producers still speak HTTP to the
daemon over loopback, but the daemon resolves `agora.relay` to an
in-process call into `agora-core` plus the configured relay backend,
rather than to a second HTTP client pointed at
`orbiplex-node-agora-service`.

The cost is a narrower deployment envelope:

- Agora must be built in the same language as the daemon. Today this is
  Rust for both, so the constraint is not binding.
- Independent restart of the relay is lost; relay lifecycle is fused
  with the daemon's lifecycle.
- Operator-visible component boundaries shift: `middleware.agora` stops
  being a separately supervisable process.

For the smallest useful deployment described in proposal 035 §5.7
(local-only, one node, one relay, no passport, one topic, one author)
the in-process shape is arguably a better default than the supervised
binary: it removes a process, removes a port, and removes the second
loopback hop, while preserving every observable semantic of the relay.

Neither optimization is required for v1, and neither changes the
`agora-record.v1` envelope, the `agora.record.v1` signing domain, the
`record/id` formula, the topic ACL semantics, or any consumer-visible
capability contract. They are orthogonal knobs on transport cost, not
on meaning.

## Out of Scope

- per-kind semantic interpretation (opinion meaning, comment threading,
  whisper thresholds),
- listener-side filtering, moderation, or reputation weighting,
- payment / settlement of record ingest,
- long-running workflow execution driven by record content,
- replacement of the seed directory or the offer catalog — those are
  separate relay roles that may later migrate onto Agora but do not today.

## Consumes

- `agora-record.v1`
- `resource-ref.v1`
- `capability-passport.v1`

## Produces

- `agora-record.v1`

## Related Capability Data

- `agora-caps.edn`

## Notes

Agora may be implemented as an in-process module of the daemon or as a
separate supervised program/process attached to Node through explicit
contracts. The v1 delivery is a supervised Rust binary
(`orbiplex-node-agora-service`) reached on loopback, announced by the daemon
under capability id `agora.relay`; solution semantics are stable either way.

The smallest useful Agora deployment is local-only: one node, one relay, no
passport, one topic, one author. Proposal 035 §5.7 explicitly treats this as a
first-class configuration rather than a degraded fallback. Story-008
exercises exactly this shape end-to-end.

Federated deployment layers on top without replacing the envelope or the
signer contract: the same `agora-record.v1`, the same `agora.record.v1`
signing domain, the same `record/id` formula. The only thing that grows is
the number of relays and the topology that capability-routing resolves to.
