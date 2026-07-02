# Seed Directory

`Seed Directory` is the discovery facade for Orbiplex node reachability,
capability availability, revocation feeds, and subject-to-node routing
projections.

Status: `mvp-ready`

Date: `2026-05-19`

## Executive Summary

Seed Directory answers discovery questions without becoming the source of
cryptographic truth:

```text
signed domain artifacts
  -> Seed Directory admission policy
  -> local temporal accepted-fact store
  -> discovery projections
  -> client-side independent verification
```

It indexes signed `node-advertisement.v1`, passport-backed capability
registrations, official-service endorsements, capability revocations,
node-address attestations, and the public/operator subject projections needed
by routing, Artifact Delivery, Contact Catalog, and capability consumers.

The component is deliberately a semantic facade. Agora can relay accepted Seed
Directory facts, and daemon consumers can query multiple trusted directories,
but Seed Directory remains the layer that understands node advertisements,
capability passports, revocations, endpoint joins, subject projections, and
local directory trust policy.

## Scope

This solution combines:

- Proposal 025, which defines Seed Directory as the capability catalog and
  revocation surface;
- Proposal 054, which defines user-maintained/federated directories, trusted
  Agora replay, multi-directory policy, and query attestations.

Seed Directory owns:

- node advertisement admission and lookup;
- passport-backed capability registration and lookup;
- official-service endorsement attach/projection and endorsement revocation
  feeds;
- capability passport revocation admission and feed projection;
- optional `node-address-attestation.v1` evidence;
- Seed Directory bootstrap as capability `seed-directory`;
- public/operator participant and routing-subject projections;
- trusted directory configuration, query policy, and replay diagnostics;
- optional signed query attestations for critical reads.

It does not own:

- capability semantics beyond indexing and verification of presented evidence;
- final consumer authorization after a peer connects;
- contact catalog domain policy or people-directory mappings;
- Agora storage semantics;
- TLS trust lifecycle beyond producing endpoint evidence consumed by TLS Trust
  Policy and peer supervision;
- reputation algorithms for directory operators.

## Must Implement

### Node Advertisement Catalog

Based on:

- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`

Related schemas:

- `node-advertisement.v1`

Responsibilities:

- accept and store signed node advertisements;
- reject stale or malformed updates;
- expose current `node-id -> endpoints` projections;
- keep advertisements as reachability candidates, not identity truth.

Status:

- `done` — Node runtime has an embedded Seed Directory store and HTTP surface,
  startup/bootstrap integration, endpoint lookup consumers, and temporal
  accepted-fact storage.

### Passport-Backed Capability Catalog

Based on:

- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/60-solutions/007-capability-advertisement/007-capability-advertisement.md`

Related schemas:

- `capability-advertisement.v1`
- `capability-passport.v1`
- `seed-capability-registration.v1`

Responsibilities:

- accept one capability registration per `(node_id, capability_id)` pair;
- order replacements with positive request-level `sequence/no`, expose the
  accepted sequence in read projections, reject stale conflicts with
  `current/sequence-no` and `submitted/sequence-no`, and keep identical
  `(passport_id, sequence/no)` republishes idempotent;
- omit expired capability registrations from runtime lookup projections;
- enforce a bounded active-registration limit per node, with `64` as the
  daemon hard-MVP default;
- require valid passport evidence for passport-backed capabilities;
- join capability registrations with current node endpoints;
- expose capability lookup for `capability-first` and `capability-many`
  consumers;
- keep consumers responsible for independent passport and peer identity
  verification.

Status:

- `done` — Node implements capability registration, monotonic replacement,
  stale-sequence diagnostics, daemon-side sequence counters with retry
  advancement, active-read filtering, bounded active entries, capability
  lookup, bootstrap capability passport verification, capability sync, and
  capability resolver consumers for daemon, middleware, and Artifact Delivery
  paths.

### Official-Service Endorsements

Based on:

- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`

Related schemas:

- `federation-service-endorsement.v1`
- `federation-service-endorsement-revocation.v1`
- `capability-proof-presentation-batch.v1`

Responsibilities:

- accept scoped endorsement attach for an existing capability registration;
- project `official` status only from verified active
  `federation-service-endorsement.v1` artifacts;
- expose endorsement revocations through the shared revocation feed shape;
- support metadata-only proof presentation facts for peer-delivered
  endorsement/passport refresh;
- record the ingress-enforced install `source`; caller-supplied provenance is
  optional `source/detail`, never a replacement for the audited acquisition
  surface;
- require explicit bounded `max/bytes` on outbound
  `capability-proof-presentation-batch.v1` allows, capped by daemon validation
  at 256 KiB;
- keep final official-status verification at the consumer boundary.

Status:

- `done` — Seed Directory attach/read consumes `federation-service-endorsement.v1`
  as the sole official-status proof, daemon consumers re-verify official status
  before use, endorsement revocations flow through the shared revocation feed,
  participant-sovereign operators can issue non-own endorsements through the
  daemon API, and Artifact Delivery can admit mixed proof refresh batches via
  `capability-proof-presentation-batch.v1`.

### Revocation Feed

Based on:

- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/60-solutions/014-key-delegation-passports/014-key-delegation-passports.md`

Related schemas:

- `capability-passport-revocation.v1`
- `federation-service-endorsement-revocation.v1`

Responsibilities:

- accept issuer- and subject-signed revocation artifacts;
- expose bounded revocation feeds for consumers;
- make revocation monotonic during multi-directory reconciliation;
- feed dispatch gates and capability lookup suppression.

Status:

- `done` — Seed Directory accepts revocation artifacts, exposes revocation
  feeds, integrates with daemon revocation sources, and suppresses revoked
  capability observations across multi-directory query policy.

### Seed Directory Bootstrap Capability

Based on:

- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md`

Related schemas:

- `capability-passport.v1`

Responsibilities:

- model Seed Directory itself as capability `seed-directory`;
- verify shipped or configured Seed Directory passports at daemon startup;
- degrade to isolated/bootstrap mode when no usable directory remains;
- keep static endpoint-only bootstrap as an explicit compatibility path.

Status:

- `done` — Daemon verifies configured Seed Directory passport entries,
  tolerates endpoint-only static bootstrap when explicitly configured, and
  reports isolated bootstrap mode when no usable entry remains.

### Subject and Routing Projections

Based on:

- `doc/project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md`

Related schemas:

- `node-operator-binding.v1`
- `routing-subject-binding.v1`

Responsibilities:

- expose participant-to-node candidates only for explicit public/operator
  disclosure paths;
- accept routing-subject bindings as privacy-preserving delivery projections;
- keep root participant disclosure out of default contact and routing flows;
- support Artifact Delivery participant, routing-subject, org, and contact
  lookup resolver paths without making Seed Directory contact-aware.

Status:

- `done` — Daemon and Seed Directory support participant and routing-subject
  lookup surfaces, public-unlinked routing-subject projections, and AD
  host-composed subject lookups with local query policy.

### Node Address Attestation and Endpoint Evidence

Based on:

- `doc/project/40-proposals/043-node-address-attestation-fallback.md`
- `doc/project/40-proposals/056-orbiplex-tls-trust-policy.md`
- `doc/project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md`

Related schemas:

- `node-address-attestation.v1`

Responsibilities:

- probe candidate endpoints when policy requires fresh reachability evidence;
- produce signed endpoint observations for node-address mappings;
- include TLS leaf evidence where available;
- feed peer supervisor endpoint evidence and TLS trust policy without becoming
  the transport trust root.

Status:

- `done` — Seed Directory can issue `node-address-attestation.v1`, daemon
  consumers import endpoint evidence, peer supervisor enforces endpoint pins,
  and TLS Trust Policy owns transport validation semantics.

### Trusted Agora Replay

Based on:

- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/60-solutions/008-agora/008-agora.md`

Related schemas:

- `agora-record.v1`
- `node-advertisement.v1`
- `seed-capability-registration.v1`
- `capability-passport-revocation.v1`

Responsibilities:

- publish accepted facts after Seed Directory admission;
- replay trusted Agora lanes into local Seed Directory projections;
- keep direct-write and trusted-replay projections equivalent for the same
  accepted fact stream;
- persist replay cursors and diagnostics per federation/lane.

Status:

- `done` — Node has Seed Directory Agora adapters, accepted-fact replay,
  persisted replay cursors/status, and equivalence tests covering
  advertisements, capability registrations, and revocations.

### Multi-Directory Trust Policy

Based on:

- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`

Related schemas:

- `seed-directory-trust.v1`

Responsibilities:

- configure trusted directory candidates with trust tier, weight, federation
  id, policy refs, endorsements, and reputation refs;
- support `preferred-directory`, `quorum`, and `weighted-trust` query modes;
- prevent embedded local directory self-voting unless explicitly enabled;
- reconcile observations deterministically and fail closed for malformed or
  unverifiable records.

Status:

- `done` — Daemon config and consumers implement trusted directory entries,
  source eligibility, quorum/weighted merge, revocation suppression,
  diagnostics, and safe operator-visible status.

### Query Attestation

Based on:

- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`

Related schemas:

- `seed-directory-query-attestation.v1`

Responsibilities:

- optionally attest critical Seed Directory responses on request;
- bind normalized query, canonical response digest, projection high-water mark,
  issue time, expiry, signer id, and signature;
- leave legacy response shapes unchanged when attestation is not requested;
- document that query attestation proves the served view, not global truth.

Status:

- `done` — Seed Directory supports opt-in query attestations for advertisement,
  capability, and revocation reads, and schema-gate validates the attestation
  contract.

### Temporal Accepted-Fact Store

Based on:

- `doc/project/40-proposals/062-temporal-storage-convention.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`

Related schemas:

- `storage-manifest.v1`

Responsibilities:

- store accepted Seed Directory facts and operator retractions as temporal
  records;
- treat HTTP/API tables as rebuildable projections;
- expose temporal status, event feed, and replay-check diagnostics;
- keep compaction policy explicit.

Status:

- `done` — Embedded Seed Directory uses temporal transaction/event tables,
  writes a storage manifest, exposes temporal diagnostics, and keeps accepted
  facts under bounded/no-op compaction semantics.

## May Implement

### Merkle/Page Proofs for Large Directory Views

Based on:

- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`

Related schemas:

- `seed-directory-query-attestation.v1`

Responsibilities:

- extend query attestations with partial page proofs if large
  multi-directory comparisons require them.

Status:

- `deferred` — Canonical response-body digest is sufficient for the current
  MVP and hard-MVP query-attestation contract.

### Reputation-Backed Directory Scoring

Based on:

- `doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`

Related schemas:

- `reputation-snapshot.v1`

Responsibilities:

- feed directory operator reputation into local trust policy;
- convert endorsement and reputation references into a future
  `ReputationProjection`.
- support future peer-presentation delivery of capability passport and
  federation-service endorsement proofs as a degraded-discovery channel, while
  keeping local verification authoritative.

Status:

- `deferred` — MVP supports `endorsement_refs`, `reputation_ref`, and
  `required_directory_endorsements` as local policy inputs, while full
  reputation projection and peer-presentation delivery remain later layers.

## Consumes

- `node-advertisement.v1`
- `capability-advertisement.v1`
- `capability-passport.v1`
- `capability-passport-revocation.v1`
- `federation-service-endorsement.v1`
- `federation-service-endorsement-revocation.v1`
- `capability-proof-presentation-batch.v1`
- `node-operator-binding.v1`
- `routing-subject-binding.v1`
- `agora-record.v1`
- `seed-directory-trust.v1`

## Produces

- `seed-capability-registration.v1`
- `seed-directory-query-attestation.v1`
- `node-address-attestation.v1`
- Seed Directory HTTP projections for advertisements, capabilities,
  revocations, participants, routing subjects, and trusted-directory
  diagnostics.

## Related Capability Data

- `031-seed-directory-caps.edn`

## Notes

Seed Directory is a directory, not an authority substitute. A consumer may use
it to find a peer, endpoint, capability, provider, or routing subject, but the
consumer must still verify the presented passport, revocation freshness, peer
identity, endpoint evidence, and domain-specific policy at the boundary where
authority matters.

This keeps discovery useful without turning any user-maintained directory into a
global truth oracle.
