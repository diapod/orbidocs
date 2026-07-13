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

Hard-MVP closure note: the public record relay, content addressing,
signature verification, local store, subject index, SSE subscription,
Matrix-backed relay, Agora Vault, daemon supervision, and Story-008 resource
opinion path are implemented in the reference Node runtime. Aggregate status
surfaces and hot-path optimizations remain product-layer or scale-driven
extensions; they are not prerequisites for the hard-MVP Agora deployment.

Agora also exposes a separate **Agora Vault** surface for encrypted opaque
artifacts. Vault entries are not ordinary `agora-record.v1` records: they do
not publish author, participant, nym, topic, or domain metadata. The public
outer shape is `agora-vault-entry.v1`; it exposes only opaque artifact ids and
the cryptographic envelope. Scoped list/get/delete are controlled by
`agora-vault@v1` authority over an opaque `vault/subject`.

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

Public contract artifacts:

- `doc/project/60-solutions/008-agora/agora-record-relay.v1.openapi.yaml` is
  a legacy test/reference fixture for the pre-P068 standalone Agora HTTP
  surface. Canonical OpenAPI projection is daemon-owned and served through
  `GET /v1/openapi.json`.
- `agora-vault-entry.v1` and `agora-vault-ref.v1` define the generic encrypted
  artifact vault and its sealed recovery reference.
- `doc/project/60-solutions/008-agora/008-agora-backlog.md` is the granular
  solution-local implementation backlog for P-items that are too detailed for
  this overview.

## Agora Vault

Agora Vault is the encrypted-artifact sibling of the public Agora record
relay. It is used when a component needs durable, admission-controlled storage
and lookup by an opaque artifact id, but ordinary `agora-record.v1` would leak
too much by design: author identity, participant or nym ids, topic keys, and
domain metadata.

Vault entries are schema-gated as `agora-vault-entry.v1`. The outer entry is
intentionally small and may expose only:

- `vault-entry/id`;
- opaque `artifact/id`;
- generic `artifact/kind`;
- encryption envelope metadata;
- ciphertext.

The encrypted payload contains the artifact itself and all domain metadata.
Agora MUST reject a vault entry that is not valid JSON, does not validate
against `agora-vault-entry.v1`, contains plaintext payload fields, lacks
ciphertext, or lacks at least one key envelope. The runtime currently accepts
`xchacha20-poly1305` entries and validates the envelope at ingest and export
boundaries. The MVP recorded-message writer may emit `key-wrap =
"dev-key-commitment"`; that value is a non-recoverable development custody
commitment to the discarded symmetric key, not recipient key wrapping. Durable
recipient recovery requires `x25519-hkdf-sha256+xchacha20-poly1305`.

The public lookup surface is:

- `GET /v1/agora/vault-artifacts/{artifact_id}`.

It returns ciphertext-bearing entries for the opaque artifact id and reports
the public metadata class as `artifact/id`, `artifact/kind`, `vault-entry/id`,
`encryption`, and `ciphertext`. It MUST NOT return `vault/subject`,
participant ids, nym ids, author ids, topic keys, or plaintext payload
metadata. The reference service filters public lookup entries to that public
field set even though ingress schema validation already rejects known
identity/topic metadata keys.

Scoped vault operations are:

- `POST /v1/agora/vaults/{vault_subject}/artifacts`;
- `GET /v1/agora/vaults/{vault_subject}/artifacts`;
- `GET /v1/agora/vaults/{vault_subject}/artifacts/{artifact_id}`;
- `DELETE /v1/agora/vaults/{vault_subject}/artifacts/{artifact_id}`.

`vault_subject` is opaque and currently must use the `agora-vault:` prefix
with safe id characters. In the supervised local runtime these endpoints are
gated by the Agora client token. Remote/provider deployments bind the same
semantic operations to the `agora-vault@v1` capability/passport profile,
scoped to the opaque `vault/subject` and allowed operations.

The supervised service also exposes daemon-dispatchable host capability
handlers:

- `agora.vault.put`;
- `agora.vault.list`;
- `agora.vault.get`;
- `agora.vault.delete`.

The reference implementation stores entries in `agora-vault.v1.sqlite` with
`(vault_subject, artifact_id)` as the scoped uniqueness boundary. Deletion is a
soft delete: scoped get/list and public lookup ignore deleted entries. The
same `artifact/id` may exist under more than one `vault_subject`; scoped
list/get/delete remains subject-bound, while public lookup by artifact id may
return ciphertext entries from every non-deleted matching subject without
revealing those subjects.

Recovery metadata is not stored in public Agora records. A node that needs to
recover vault access seals `agora-vault-ref.v1` records into the Pseudonym
Vault. Those refs bind a recovered participant or nym context to the opaque
provider, `vault/subject`, capability references, and allowed artifact kinds.
Possession of only a public participant id is not sufficient for list/get/delete.
Recovery requires restored key or recovery material that can open the sealed
vault reference.

Recorded messaging is the first production profile that uses Agora Vault: a
recorded `message-envelope.v1` is encrypted as a generic vault artifact and
stored best-effort through `agora.vault.put`. Delivery of the message is not
rolled back if the vault write is temporarily unavailable; the messaging layer
tracks `vault.pending`, `vault.stored`, or failure/retry state and retries
failed-retryable vault jobs from its outbox worker.

## Scope

This document defines solution-level responsibilities of the Agora component.

It does not define:

- the semantic meaning of any specific `content/schema` carried inside an
  Agora record (that lives in the per-kind proposal, e.g. proposal 026 for
  `resource-opinion.v1`),
- namespace-level authority roots and publish/subscribe capability profiles —
  those are defined in
  `doc/project/60-solutions/021-agora-authority/021-agora-authority.md`,
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

Signing placeholder contract:
- unsigned builders and `POST /v1/agora/records.sign` MAY use
  `record/id = "sha256:pending"` and `signature.value = "pending"` as
  input placeholders,
- `records.sign` MUST overwrite both fields before returning the record,
- every final ingest, replay, and federation path MUST reject a record that
  still carries `sha256:pending`; syntactic `sha256:*` shape is not enough,
  because the declared `record/id` must match the canonical content address.

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
  listings over stable cursor semantics. The `record/about` index is a
  derived, rebuildable relay-local view over the persisted records, not a
  source of truth; a dedicated persisted subject-index projector remains a
  later optimization if rebuild cost or query volume justifies it.

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
- treat Matrix as transport provenance only: the receiver trusts the
  `agora-record.v1` envelope after local verification, not the donor relay,
- expose canonical-topic, cache-topic, and origin-topic behaviors as
  deployment-configurable roles.

Status:
- `done` in the Node reference implementation. `agora-matrix-client` and
  `agora-relay-matrix` provide Matrix-backed publish, inbound sync, and
  store-and-forward relay behavior. Inbound Matrix records are admitted through
  the same envelope/signature/delegation, content-schema, topic ACL,
  authority/capability/revocation, and idempotency checks as local HTTP ingest;
  Matrix event signatures and donor relay identity are diagnostics and transport
  provenance, not sufficient record validity.

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

### Domain Accepted-Fact Adapters

Based on:
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/60-solutions/031-seed-directory/031-seed-directory.md`

Related schemas:
- `agora-record.v1`
- `service-offer.v1`
- `node-advertisement.v1`
- `seed-capability-registration.v1`
- `capability-passport-revocation.v1`

Responsibilities:
- keep `agora-record.v1` as the generic public/federated envelope, not as a
  home for domain policy,
- emit accepted Seed Directory facts as records:
  `seed.node-advertisement.accepted`,
  `seed.capability-registration.accepted`, and
  `seed.capability-revocation.accepted`,
- emit provider service-offer snapshots as `offer-snapshot` records,
- replay those records into domain projections (`SeedDirectoryStore`,
  `ObservedCatalogStore`) rather than making discovery or marketplace clients
  query raw Agora topics,
- treat `offer-snapshot` as the durable public/federated publication record,
  not as the full source of truth for a provider's standing offer,
- preserve offer provenance during replay so marketplace trust admission can
  use the provider participant id, provider node id, record author,
  publisher/origin node id, topic key, record id, observation time, and inner
  `service-offer.v1` signature verification result,
- let the domain engines continue to own passport checks, sovereign policy,
  trust admission, TTL/sequence semantics, endpoint joins, and query shape.

Status:
- `done` for the reference adapter layer. `seed-directory::agora` maps accepted
  Seed Directory advertisements, capability registrations, and revocations to
  `agora-record.v1` and can replay them into the existing store. `catalog::agora`
  maps `service-offer.v1` snapshots to `offer-snapshot` records and can replay
  them into the observed catalog projection. The schema gate recognizes these
  content schemas in strict Agora content-validation mode. M2 uses
  deterministic-as-of-record-acceptance replay: domain projections trust records
  already accepted by the local relay, with revocation freshness checked at the
  publish/ingest boundary. Local authoritative stores remain local; observed or
  federated read models use `agora-primary` replay where configured.

M2 replay-fed projections cover this canonical domain set:

- Seed Directory accepted facts,
- Offer Catalog observed/federated snapshots,
- moderation markers,
- comments,
- resource opinions,
- public gossip.

Seed Directory and Offer Catalog carry hard equivalence tests because both have
pre-Agora domain stores. Agora-native domains (moderation markers, comments,
opinions, gossip) use fixture replay tests into an empty projection store instead
of inventing a legacy model. The reference implementation exposes projection
status and domain query endpoints under `/v1/agora/projections/*`; operational
diagnostics include counters for malformed/skipped/rejected/deferred records,
cursor pruning, cursor state, last error, and last successful replay age.

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
- `done` for M2b verification parity: envelope fields, fail-closed verifier
  hook, capability grant, bridge verifier, delegated examples, Rust
  service/relay accept paths, `records.sign` with `key_delegation`, Rust
  Matrix-only ingest parity, and host `agora.record.verify` capability for
  non-Rust middleware are implemented. Bundled Python middleware has a
  `HostAgoraClient.verify_record()` helper for that verifier, and committed
  delegated fixtures assert the same decisions across Rust, Matrix, SQLite
  replay, and Python host-capability transport. M3 adds high-level
  `agora.record.admit` as a read-only host capability that composes verifier
  output with content-schema checks, optional publish/subscribe profile checks,
  and node-local authority-policy evaluation for supervised middleware
  diagnostics.

### Replay-Fed Public Domain Projections

Based on:
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/60-solutions/008-agora/008-agora-dir-simplify-impl.md`

Related schemas:
- `agora-record.v1`
- `plain-comment.v1`
- `comment-thread-policy.v1`
- `resource-opinion.v1`
- `public-gossip.v1`
- `moderation-marker.v1`
- `agora-public-rejection.v1`
- `reputation-snapshot.v1`

Responsibilities:
- replay accepted public Agora records into local read models without querying
  raw topics from domain logic,
- keep comments, opinions, public gossip, and moderation markers in separate
  tables while sharing cursor and diagnostic mechanics,
- preserve orphan queue behavior for comments/opinions and deterministic
  promotion when parents arrive,
- clamp gossip TTL/decay through local projection policy,
- expose operator and API status for projection health.

Status:
- `done` for M2 reference mechanics. The Node implementation uses
  `<agora_data_dir>/agora-projections.v1.sqlite`, projects comments/thread
  policies, resource opinions, public gossip, and moderation markers, and
  exposes `/v1/agora/operator/projections/replay` plus read-model query surfaces
  under `/v1/agora/projections/*`. Public moderation markers remain signals:
  M2 does not define automatic hide/delete policy from marker content.

### Agora M4: Story-005 Public Signal Closure

Based on:
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/60-solutions/011-whisper/011-whisper.md`

Related schemas:
- `agora-record.v1`
- `whisper-signal.v1`
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`
- `public-gossip.v1`

Responsibilities:
- use Agora as the public/federated substrate for disclosure-safe Whisper/public
  signal records without making Agora the owner of Whisper semantics,
- carry `whisper-signal.v1` directly for the M4 public/federated smoke rather
  than substituting generic `public-gossip.v1`,
- keep private/direct or `private-correlation` whispers off public Agora topics,
- replay accepted public Whisper signals into a domain projection with cursor,
  lag, malformed/skipped/rejected/deferred diagnostics,
- derive deterministic threshold state from compatible public/federated signals
  using the M4 rule: two distinct eligible nodes, same `topic/class`, same
  `signal/similarity-key`, bounded time window,
- emit deterministic `whisper-threshold-reached.v1` and
  `association-room-proposal.v1` records as projection-authority-signed,
  issuer-scoped derived claims while preserving explicit human opt-in,
- prevent derived-record loops with deterministic derived ids, source-record-kind
  exclusion, and derivation refs,
- treat threshold/proposal artifacts as replayable public meta-signals and
  coordination records, not as `public-gossip.v1` social narratives,
- keep `public-gossip.v1` as an explicit publication act that can be produced
  independently or after opt-in association, but never automatically from a
  threshold/proposal projection,
- provide a three-node laptop smoke where node A and node B submit similar signals
  and node C runs the Agora relay/server.

Status:
- `done` for M4 in the Node reference implementation. The public/federated
  direct-HTTP smoke path is implemented: node A and node B submit
  nym-authored, signed `whisper-signal.v1` records to node C's Agora service,
  and node C projects signal, threshold, and association-room proposal state.
  Agora verifies inline-first nym proofs at the envelope/policy boundary,
  rejects private/direct-only Whisper signals on public Agora topics, emits
  deterministic `whisper-threshold-reached.v1` and
  `association-room-proposal.v1` records through the host signer, and prevents
  derived-record loops through source-kind exclusion and deterministic
  derivation ids. Story-005 now has a three-node laptop operator pack with
  durable profiles and English/Polish runbooks. Matrix-backed Agora sync parity
  is covered separately so Matrix remains a transport, not a trust source.
  Story-009 Agora-primary smoke remains the regression guard for the existing
  Agora substrate.

### Agora Post-MVP: Whisper Trace Carrier Contract

Related schema:
- `whisper-trace.v1`

Agora may carry public or federation-scoped Whisper trace statements under:

- `record/kind = "whisper-trace"`,
- `content/schema = "whisper-trace.v1"`,
- `topic/key = ai.orbiplex.whisper-traces/<trace-kind>`.

Agora remains a signed record carrier and schema/disclosure gate. It does not
turn a trace into a receipt, validate an opaque sender-local consent decision,
or project trace statements into Whisper similarity and threshold state.
Public ingress must reject `private-correlation` traces and must not infer that
digest-only disclosure is anonymous or non-sensitive.

Status: `implemented`. Agora registers the trace record kind and schema, enforces
the conventional public topic and disclosure posture at ingress, and exposes a
metadata-only list/detail projection that is excluded from Whisper signal
threshold and association state. Story-005 proves the public carrier together
with a private AD/INAC trace using the same signed envelope family.

### Projection Authority for Derived Records

Derived public records are signed by a projection authority. In M4 the authority
may be the local projection node or a short-lived delegated projection key, but
that is an implementation choice, not the permanent protocol model. The derived
record is an issuer-scoped claim that a deterministic projection rule was applied
to listed source records; it is not a global social-truth assertion.

Root authority configuration establishes which identities may grant projection
publication rights. Routine derived records should be signed by operational
delegated keys whenever possible, keeping long-lived authority material out of
the hot path.

The contract must remain compatible with future committee authority. A later
static committee or reputation-selected committee can sign the same derived
records by carrying inline selection and quorum proofs in derivation/authority
metadata. This lets local policy move from "trust this projection authority" to
"trust this quorum of community-trusted authorities" without changing the
meaning of `whisper-threshold-reached.v1` or `association-room-proposal.v1`.

### Operator-Local Rejection Feed

Based on:
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Responsibilities:
- persist local rejection diagnostics without publishing a public rejection
  oracle,
- keep request bodies, passports, proof bundles, and internal policy traces out
  of the store by default,
- expose bounded operator diagnostics through the Agora service status/API.

Status:
- `done` for M2b. Rejections are stored in
  `<agora_data_dir>/agora-rejections.v1.sqlite` and exposed through
  `/v1/agora/status` and `GET /v1/agora/operator/rejections`. The default store
  is digest-only; payload capture, if ever enabled locally, is an operator
  debugging mode rather than a public protocol feature. A public rejection feed
  is explicitly out of scope for M2/M2b.

### Correlated Action Trace

Based on:
- `doc/project/30-stories/story-008-cool-site-comment.md`
- `doc/project/50-requirements/requirements-014-resource-opinions.md`

Responsibilities:
- correlate the local resource-opinion flow across daemon capability lookup,
  Agora signing, ingest, duplicate ingest, subject query, and record fetch,
- keep the canonical trace in daemon-owned append-only storage under
  `trace/agora`,
- use `X-Orbiplex-Correlation-Id` as the caller-supplied correlation seam,
- reject trace append payloads that are malformed, oversized, or contain
  sensitive-looking keys,
- expose append degradation in `/v1/agora/status` without coupling Agora to the
  daemon's storage internals.

Status:
- `done` for Story-008 hard-MVP. The daemon exposes module-authenticated
  `POST /v1/host/capabilities/agora.trace.append` for the supervised
  `agora-service`, instruments `GET /v1/host/capabilities/agora.relay`
  lookup, and exposes operator readback through
  `GET /v1/traces/agora?correlation_id=...&record_id=...&limit=...`.
  Malformed or policy-rejected trace appends fail as HTTP 422, while daemon
  storage failures fail as HTTP 500; `agora-service` counts failed append
  attempts and reports trace status as `ok` or `degraded`.
  The public Agora API itself remains storage-agnostic: it emits events through
  the host capability channel and never writes the daemon commit log directly.

### Org Authority Custody

Org authority roots do not name "keys that may publish" directly. They name an
organization identity that may establish authority under a referenced custody
policy:

```json
{
  "id": "org:...",
  "kind": "org",
  "custody_policy_ref": "org-custody:example:v1",
  "namespaces": ["ai.orbiplex.reputation/**"]
}
```

The referenced `org-custody-policy.v1` artifact defines which participants or
keys may authorize `agora-authority` actions and whether the rule is
`any-authorized` or `threshold`. Threshold rules require an inline
`org-custody-decision.v1` bundle carried beside the key-delegation proof. The
decision bundle signs the target record digest, policy ref, org id, purpose,
topic key, and optional delegation id; duplicate signers count once. Unknown
policy refs, unknown modes, missing decisions, target mismatches, and
insufficient quorum fail closed.

M2b implementation status: `agora-service` loads `org_custody_policies` from
its runtime config, resolves `custody_policy_ref` fail-closed, validates
`org-custody-policy.v1` and inline `org-custody-decision.v1` through the Node
schema gate, and has regression coverage for valid threshold, missing signer,
duplicate signer, signer outside policy, target digest mismatch, unknown
policy ref, and unknown mode.

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
- listener-side filtering, automatic moderation decisions, or reputation
  weighting,
- payment / settlement of record ingest,
- long-running workflow execution driven by record content,
- replacement of the seed directory or the offer catalog — those are
  separate relay roles that may later migrate onto Agora but do not today.

## Consumes

- `agora-record.v1`
- `resource-ref.v1`
- `moderation-marker.v1`
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
