# Orbiplex Memarium

`Orbiplex Memarium` is the local memory-and-knowledge organ of an Orbiplex Node. Its constitutional mandate is to "preserve what should not disappear." Memarium manages four constitutionally defined memory spaces (personal, community, public, crisis) with space-specific policies for encryption, replication, retention, anonymization, and right-to-forget.

Memarium is an in-process Rust crate compiled with the daemon. It participates in the Node's middleware chain as a post-chain observer (with an optional PreInput context enricher), gaining observational and enrichment access to the peer message pipeline without ever acting as a dispatch-blocking handler. It stands on the existing storage trait boundary rather than inventing a parallel persistence mechanism.

## Purpose

The component is responsible for the solution-level execution path of:
- local knowledge storage across four constitutionally defined memory spaces,
- space-specific policy enforcement (encryption, retention, replication, forget),
- middleware chain observation and context enrichment,
- host capability exposure for agents and middleware (`memarium.read`, `memarium.write`, `memarium.index`, `memarium.cache`),
- Agora synchronization tracking (recording outbound submissions and their confirmation status as local facts),
- archival integration (recording handoff provenance and caching retrieval results),
- crisis space management as a constitutional obligation.

## Scope

This document defines solution-level responsibilities of the Memarium component.

It does not define:
- concrete module layout in an implementation repository,
- federated Memarium replication between nodes (future work),
- full curation or training pipeline (downstream consumers),
- specific full-text search or vector index implementation (runtime concern),
- frozen archival contract schemas (builds on current draft proposals).

## Must Implement

### Memory Space Management

Based on:
- `doc/normative/20-vision/en/VISION.en.md` (Memarium, memory spaces)
- `doc/normative/40-constitution/en/CONSTITUTION.en.md` (Art. II.4, V.7)
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- manage four memory spaces (personal, community, public, crisis) as policy envelopes over the shared storage boundary,
- enforce space-specific encryption policy (mandatory for personal, community, crisis; optional for public),
- enforce space-specific retention policy (operator-controlled, group-governed, constitutional-minimum),
- enforce space-specific forget policy (immediate, governed, tombstone, restricted),
- validate cross-space promotion as an explicit transition requiring appropriate autonomy level,
- record promotion provenance as append-only facts.

Status:
- `partial` — four memory spaces, encryption/retention/forget policy enforcement, cross-space promotion, append-only provenance, crisis seed population, and crisis status/resolve read models are implemented. Remaining work is operational hardening: published wire schemas/examples, operator grant installation flow, observer smoke coverage, focused detector-transition lifecycle coverage, and a non-scan read model if datasets outgrow MVP scale.

### Observer-Based Chain Integration

Based on:
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md` (chain architecture, observer slots)
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- implement a daemon-side `MemariumPostChainAdapter` that sees the effective payload (after all middleware mutations), the response, and the dispatch outcome, then forwards the Memarium-domain slice into `memarium-runtime`,
- compile declarative observe rules from merged middleware configuration at startup,
- match post-chain observations against compiled rules and record `MemariumFact` entries in the declared space with extracted fields,
- optionally register as per-phase observer for fine-grained visibility into where mutations occurred,
- optionally add a daemon-side `PreInput` adapter for `MemariumContextEnricher` semantics to annotate inbound messages with cached knowledge artifacts,
- never block, drop, reject, or mutate peer messages from any chain or observer position.

The observers and handlers are in-process trait implementations compiled into the daemon. They do not use loopback HTTP and share the same `StorageRuntime` as the rest of the daemon. The daemon owns chain-private traits such as `PostChainObserver`; `memarium-runtime` owns the neutral `observe_dispatch(message_kind, correlation_id, effective_payload)` port. This follows the trait-pipeline architecture documented in proposal 027 and the middleware README.

For stratification reasons, the post-chain adapter lives on the daemon side (it bridges daemon-private `PostChainEvent`/`PostChainObserver` types into `memarium-runtime`), while the semantic observer contract stays in `memarium-runtime`. The runtime crate never depends on daemon-private peer-message types.

Status:
- `partial` — post-chain observer and declarative rule compilation are wired (daemon-side adapter over a runtime trait). Per-phase observer registration and the optional `MemariumContextEnricher` (PreInput) are infrastructure-ready but not yet registered by the runtime.

### Declarative Observe Rules

Based on:
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- define an `ObserveRule` contract specifying: message types, fact kind, target space, field extraction paths, optional condition predicate, enabled flag,
- compile observe rules from the `memarium` section of each middleware's configuration, merged through the daemon's standard `deep_merge(factory_config, node_config)` strategy,
- validate rules at startup: reject unknown space ids, validate extract path syntax, warn on unreachable rules,
- support operator overrides: node config can disable, modify, or add observe rules for any middleware.

Each middleware is the semantic expert for its own domain. Agora declares that `agora-record.v1` messages are `agora-submission` facts in the public space. Dator declares that `service-offer.v1` messages are offer-tracking facts. Memarium compiles and executes these rules without domain-specific knowledge.

Implementation note: runtime rule compilation currently logs and skips malformed rules (warn-level) rather than rejecting the whole rule set at startup; space ids are validated structurally via enum deserialization. A missing extract path yields a field absent from the recorded fact (not an explicit JSON `null`). Hard-reject semantics for unknown space ids and explicit-null preservation are open decisions.

Status:
- `partial` — `ObserveRule` contract, config merge, and runtime matching + field extraction are implemented. Hard-validation of unknown space ids and explicit-null preservation are open design points (see *Implementation note* above).

### Host Capabilities

Based on:
- `doc/normative/50-constitutional-ops/en/AUTONOMY-LEVELS.en.md` (memarium.read, memarium.index at A1/A2)
- `doc/project/40-proposals/036-memarium.md`

Related capabilities:
- `memarium.read`
- `memarium.write`
- `memarium.index`
- `memarium.cache`
- `memarium.promote`
- `memarium.forget`
- `memarium.crisis_status`
- `memarium.crisis_resolve`

Responsibilities:
- expose `memarium.read` (A1+): query entries by id, tag, artifact kind, within a space,
- expose `memarium.write` (A1+): append new entries subject to space policy validation,
- expose `memarium.index` (A2+): query index projections for entry counts, tag distributions, recent activity,
- expose `memarium.cache` (A1+): read-through cache with index lookup fallback to full scan,
- expose `memarium.promote` (A0): cross-space promotion requiring operator approval,
- expose `memarium.forget` (A0): right-to-forget requests subject to explicit operator approval and space forget policy,
- expose `memarium.crisis_status` (A1): operator-visible crisis seed and active finding view,
- expose `memarium.crisis_resolve` (A0): append-only operator force-resolution fact for a named detector,
- register capabilities through the daemon's host capability binding mechanism,
- serve in-process callers (agents, NSE hooks) through direct trait methods and out-of-process callers (middleware modules) through the host capability HTTP surface.

All eight capabilities are exposed as `POST /v1/host/capabilities/memarium.<op>` endpoints and run through the same passport-gated dispatch as Sealer (`capability-binding::authorize`, six-step pipeline). Revocation is integrated against local, static-file, Seed Directory, and delegation-target-id sources. The operator-vocabulary target tag is `memarium:space:<space>[:community:<id>][:kind:<kind>][:entry:<id>]`; crisis status and resolve use the crisis space target.

#### Built-In Module Passport Bootstrap

Built-in modules MAY ship publisher-signed templates describing the Memarium
capabilities they normally need, for example `memarium.write` to a bounded
community space. Such a template is not a Memarium write passport. It is only a
signed recommendation that local policy may use when installing or enabling the
module.

The daemon authorizes Memarium host-capability calls from one of these authority
sources:

1. a local executable passport installed by the operator or local deployment
   policy,
2. an executable passport fetched from an operator-configured trusted source,
   such as an organization policy server or community governance issuer,
3. a local passport auto-issued from a publisher template when local policy
   explicitly enables auto-issuance for that built-in module.

Local deny or local disable always wins. A local executable passport also
shadows the publisher template, so updating local authority does not require
changing the packaged software. If no executable passport can be resolved,
`passport_lookup_failed` remains the correct denial status; an operator UI MAY
surface the matching publisher template as an installation recommendation, but
the dispatch gate still denies the request.

A module MUST NOT bootstrap Memarium write authority by fetching its own
passport from an arbitrary network endpoint. External passports are valid only
when the source and issuer are named by local policy for the exact capability
and scope.

#### Host API Wire Contract

The host API keeps the `endpoint + op` shape. Each request is sent to one of
the eight `memarium.*` endpoints and carries an `op` field identifying the
operation inside that capability. Successful responses carry `status: "ok"`;
error responses carry a stable `status: string`, a free-form human `reason`,
and may carry structured `details`. Clients should parse `status`
programmatically and must not parse `reason`.

For HTTP target-bearing operations, `community_id` is required when
`space == "community"`, even though the local runtime storage shape does not
need it. The daemon needs it to build the authorization target. `entry_kind` is
required for `memarium.write` / `write_entry` through the mandatory
`artifact_kind` field, and optional elsewhere; when present, it participates in
profile matching. `attributes` are an open-world `map<string,string>` with
bounded key count, key size, and value size. `fields` are an open-world JSON
object with bounded key count, key size, encoded size, and depth. Runtime domain
types and HTTP wire schemas remain separate contracts.

Entries and facts carry a first-class `classification: classification.v1`
label. The label is not encoded in `attributes` or `fields`. During the
migration window, write requests that omit `classification` are accepted and
stamped as `Personal` with ingress quarantine; once producers have been
refactored, the contract should move to strict-required labels. All HTTP wire
timestamp fields are RFC3339 strings; Rust `SystemTime`'s serde object shape is
an implementation detail and is not part of the Memarium host-capability
contract.

##### Response Status Codes

The enumeration below is closed for host-capability contract v1. Adding a new
status is a minor version bump; removing or renaming a status is breaking. Codes
from the dispatch gate map to exactly one audit decision string.

| Status | HTTP | Audit decision | Retryable | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| `invalid_request` | `400 Bad Request` | - | no | Malformed JSON, missing required field, wrong type, or enum outside the accepted range. |
| `unsupported_op` | `400 Bad Request` | - | no | Envelope shape is valid, but the `op` does not exist for this `memarium.*` host capability. |
| `invalid_operator_reason` | `422 Unprocessable Entity` | - | no | `memarium.crisis_resolve` reason is empty, longer than 2048 bytes, or contains unsupported control characters. |
| `passport_lookup_failed` | `403 Forbidden` | `denied:passport-lookup-failed` | no | Caller is identified, but no matching `memarium-space-access` passport is installed for this caller/capability target. |
| `passport_invalid` | `403 Forbidden` | `denied:passport-invalid-signature` | no | Passport structure or signature does not verify. |
| `passport_expired` | `403 Forbidden` | `denied:passport-expired` | no | Passport is outside its validity window. |
| `binding_mismatch` | `403 Forbidden` | `denied:binding-mismatch` | no | Passport does not bind to the resolved caller. |
| `allowed_callers_mismatch` | `403 Forbidden` | `denied:allowed-callers-mismatch` | no | Caller is not present in the passport's allowed caller set. |
| `no_profile_matched` | `403 Forbidden` | `denied:no-profile-matched` | no | No passport profile matches the grant and structured Memarium target. |
| `policy_denied` | `403 Forbidden` | `denied:policy-denied` | no | Issuer policy denied the request after the more specific denial classes did not apply. |
| `revocation_stale` | `503 Service Unavailable` | `denied:revocation-stale` | yes | Revocation view is outside the configured freshness budget. |
| `revoked` | `410 Gone` | `denied:revoked` | no | Passport id or delegation target id is revoked. |
| `operator_only` | `403 Forbidden` | `denied:operator-only` | no | Capability requires A0; module callers cannot invoke it directly. |
| `space_policy_violation` | `422 Unprocessable Entity` | - | no | Memarium space policy rejects the operation, e.g. plaintext write into an encryption-required space. |
| `promotion_denied` | `403 Forbidden` | - | no | Cross-space promotion would violate Memarium promotion rules. Details may classify specific cases such as crisis-closed promotion. |
| `not_found` | `404 Not Found` | - | no | Requested entry, fact, or cache key does not exist. |
| `unknown_detector` | `422 Unprocessable Entity` | - | no | `memarium.crisis_resolve.detector` is outside the detector whitelist. `details.valid_detector_ids` lists accepted ids. |
| `memarium_unavailable` | `503 Service Unavailable` | - | yes | Memarium host capability runtime is disabled or not currently available. |
| `storage_unavailable` | `503 Service Unavailable` | - | yes | Transient storage failure. |
| `storage_error` | `500 Internal Server Error` | - | no | Non-retryable storage failure. |
| `internal_error` | `500 Internal Server Error` | - | no | Unexpected host-side state. The response must not leak stack traces or secrets. |

Authorization-level enforcement for `memarium.forget` is A0 in the current
daemon: modules cannot call it directly even when they hold a passport grant.
The runtime still gates the actual effect through the space `ForgetPolicy`:
personal requests erase the read view, public requests tombstone, and
community/crisis requests are rejected until governed or restricted workflows
exist. The next authorization hardening step is to replace the coarse
`is_a0(grant_type)` check with a decision function that considers space,
expected outcome, caller authority, participant scope, artifact kind, and
remembered operator approvals. A remembered approval is an explicit operator
policy fact such as "always allow this participant or module to forget this class
of personal entries"; it must carry scope, reason, issuer, audit trace, and a
revocation path.

Status:
- `partial` — all eight capabilities are live over real HTTP with passport-gated dispatch, audit sink, and four revocation sources. Open points: contextual autonomy enforcement for `forget` (see above), implementation and operator UI for the passport installation/bootstrap flow described above, and a non-scan read-model/index sidecar for large datasets.

### Agora Synchronization Tracking

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md` (Agora orthogonality)
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- record Agora-bound submissions as `MemariumFact` entries in the public space, driven by observe rules declared in Agora's middleware configuration,
- record confirmation or failure as subsequent facts (`sync-confirmed`, `sync-failed`, `sync-timeout`) through additional observe rules,
- derive current synchronization status from the latest fact in the chain (append-only, no mutation),
- serve as the local cache of what the node contributed to Agora, queryable through `memarium.read`.

Agora does not depend on Memarium. Memarium does not depend on Agora. Agora declares observe rules in its config; Memarium compiles and executes them without Agora-specific knowledge.

Status:
- `partial` — the Memarium side of the channel (rule compilation, post-chain matching, fact append) is implemented. Agora's middleware configuration must publish concrete `ObserveRule` entries (`agora-submission`, `sync-confirmed`, `sync-failed`, `sync-timeout`) for the feature to light up end-to-end.

### Archival Integration

Based on:
- `doc/project/30-stories/story-003.md`
- `doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`
- `doc/project/50-requirements/requirements-003.md`

Related schemas:
- `archival-package.v1`
- `archivist-advertisement.v1`
- `retrieval-request.v1`
- `retrieval-response.v1`
- `learning-outcome.v1`
- `knowledge-artifact.v1`

Responsibilities:
- accept promoted `KnowledgeArtifact` entries from the learning outcome pipeline,
- record archival package preparation and handoff results as facts with provenance,
- cache `ArchivistAdvertisement` entries from peer archivists in the community or public space,
- serve as local cache for previously retrieved archival material to avoid redundant remote retrieval.

Status:
- `todo`

### Crisis Space Management

Based on:
- `doc/normative/40-constitution/en/CONSTITUTION.en.md` (Art. V.7)
- `doc/normative/20-vision/en/VISION.en.md` (escape kit)
- `doc/project/40-proposals/036-memarium.md`
- `doc/project/40-proposals/039-crisis-space-seed-v1.md` (review candidate for the first constitutional seed bundle)

Responsibilities:
- enforce constitutional minimum retention for crisis entries (must not expire without explicit operator action),
- use operator-held encryption keys for crisis material (accessible without group consensus),
- maintain explicit crisis replication policy separate from general federation replication,
- pre-populate crisis procedures from a constitutional seed set on first node start,
- support updates through explicit operator or federation action only.

Status:
- `done` — the crisis space enforces its policies like the other three spaces, and the daemon now applies the reviewed constitutional seed synchronously during startup after storage and the Node AEAD key are ready. Autonomous detector facts, `memarium.crisis_status`, and `memarium.crisis_resolve` provide the first operator-facing crisis management loop.

## May Implement

### Context Enrichment (PreInput)

Based on:
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- implement `PeerMessageHandler` on the `PreInput` chain to annotate inbound messages with cached knowledge artifacts relevant to the message type or topic,
- return `Passthrough` or `Annotate` (enrich context without modifying payload),
- never block or drop.

This handler may be deferred until agent integration patterns stabilize.

Status:
- `optional`

### Federated Replication

Responsibilities:
- replicate community space entries among trusted federation peers,
- replicate public space entries through peer-to-peer replication as an alternative to Agora,
- enforce space policy on replication scope (personal never leaves node without explicit export),
- track replication status as facts.

This is future work after the local organ is stable.

Status:
- `future`

## Payload Envelope Contract

Memarium entries carry a `PayloadEnvelope` with a discriminated `PayloadEncoding`:

- `PlaintextJson` — caller-supplied JSON body, admissible only in spaces whose `EncryptionPolicy` allows plaintext (public space, operator-opt-in elsewhere),
- `SealedJsonV1` / `SealedBytesV1` — an `EncryptionEnvelope { sealed_by, key_ref, suite, ciphertext, nonce, aad_digest }` produced by an upstream AEAD component (typically Sealer),

Memarium does **not** perform AEAD itself. Its responsibility at write time is to validate that the envelope matches the space's `EncryptionPolicy` (reject plaintext into a required space), record the envelope verbatim, and re-emit it on read. Every space whose policy requires encryption therefore depends on a caller that already speaks the sealed envelope — the dispatch-gate pattern in the daemon is the integration point.

## Consumes

- `learning-outcome.v1`
- `knowledge-artifact.v1`
- `archivist-advertisement.v1`
- `retrieval-response.v1`
- Post-chain observations (effective payloads after middleware mutations)
- Declarative observe rules from middleware configuration sections
- `PayloadEnvelope` values produced by Sealer or other AEAD-speaking callers

## Produces

- `MemariumEntry` (internal domain type, not a wire schema)
- `MemariumFact` (internal domain type, not a wire schema)
- Host capability responses for `memarium.read`, `memarium.write`, `memarium.index`, `memarium.cache`, `memarium.promote`, `memarium.forget`, `memarium.crisis_status`, `memarium.crisis_resolve`

## Related Capability Data

- `memarium.read` — read entries within a space (A1+)
- `memarium.write` — append entries to a space (A1+)
- `memarium.index` — query index projections (A2+)
- `memarium.cache` — read-through cache (A1+)
- `memarium.promote` — cross-space promotion (A0)
- `memarium.forget` — right-to-forget request (A0, then constrained by space policy)
- `memarium.crisis_status` — crisis seed and active finding view (A1)
- `memarium.crisis_resolve` — append-only operator force-resolution (A0)

## Crate Boundary

### `memarium` crate

Defines the trait boundary and domain types:
- `MemariumSpace`, `SpaceId`, policy types (encryption, retention, replication, forget)
- `MemariumEntry`, `EntryId`, `ArtifactKind`
- `MemariumFact`, `FactId`, `FactKind`
- `ObserveRule`, `ObserveRuleSet` — declarative fact-recording rule contract
- `MemariumRead` trait (query entries, facts, index)
- `MemariumWrite` trait (append entries, record facts)
- `MemariumIndex` trait (query projections)
- `MemariumError` error model
- Host capability request/response types

Does not depend on storage backend crates.

### `memarium-runtime` crate

Implements:
- `MemariumRead`, `MemariumWrite`, `MemariumIndex` over `StorageRuntime`
- Space-to-stream mapping and policy enforcement
- `MemariumRuntime::observe_dispatch(...)` — neutral post-chain observation port driven by compiled observe rules
- `ObserveRuleCompiler` — compiles observe rules from merged middleware config
- optional `MemariumContextEnricher` semantics over Memarium-domain input; daemon-side chain adapters remain outside this crate
- Index projection from commit log

Depends on: `memarium`, `storage`, `storage-runtime`. It does not depend on the daemon crate or daemon-private peer-message chain traits.

### `daemon` integration layer

Implements:
- `MemariumPostChainAdapter` implementing the daemon-private `PostChainObserver` trait
- mapping from `PostChainEvent` to `MemariumRuntime::observe_dispatch(message_kind, correlation_id, effective_payload)`
- Memarium runtime construction from effective daemon/middleware config

Depends on: `memarium`, `memarium-runtime`, `storage-runtime`, and daemon-private peer-message chain types.

## Notes

Memarium is a constitutional organ at layer L2 in the system stratification (L0: Node, L1: Agent, L2: Memarium, L3: Swarm Protocol). Its implementation as an in-process crate reflects the constitutional requirement for co-lifecycle with the daemon and the operational requirement for low-latency agent access.

The chain integration follows the observer slot pattern (proposal 027): the daemon registers a Memarium post-chain adapter that sees effective payloads after all middleware mutations, not a dispatch handler. Fact recording is driven by declarative observe rules declared by each middleware in its own configuration, merged through the daemon's standard deep-merge strategy. This eliminates coupling between the memory organ and the semantic modules it observes.

Future note: if `observe_dispatch(message_kind, correlation_id, effective_payload)` becomes too narrow, the runtime-side expansion point should be a Memarium-domain `MemariumObservation` value. `PostChainObserver` and `PostChainEvent` should remain daemon adapter concepts, not runtime dependencies.

Implementation-specific decomposition, file ownership, and delivery status belong in the concrete Node repository's implementation ledger.
