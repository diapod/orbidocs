# Horizontal Protocol Primitives

Based on:

- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `node:horizontal-protocol-core`
- `node:scoped-claim-runtime`
- `node:scoped-claim-ed25519-cert`
- `node:trace-explorer-core`

Related schemas:

- `causal-context.v1`
- `execution-receipt.v1`
- `replication-summary.v1`
- `replication-delta-request.v1`
- `replication-delta-batch.v1`
- `replication-apply-report.v1`
- `scoped-claim-request.v1`
- `scoped-claim-presentation.v1`
- `scoped-claim-type-registry.v1`
- `trace-event.v1`
- `trace-link.v1`

## Status

Hard-MVP implementation complete. Stronger anonymous-credential suites,
cross-relay Agora mesh synchronization, and universal consumer migration remain
post-MVP layers.

## Date

2026-07-10

## Purpose

This solution owns three small horizontal evidence surfaces. They make
independently owned components composable without centralizing their authority:

1. causal context and immutable execution receipts;
2. bounded replication mechanics for signed immutable fact streams;
3. suite-neutral scoped nym claims with bounded durable replay protection.

The three surfaces share contract discipline and acceptance tooling, but remain
separate APIs and policy boundaries. None is a workflow engine, global event
store, trust registry, domain merge authority, or authorization decision.

## Causal Context Surface

`horizontal-protocol-core` owns deterministic root, child, and fan-in context
derivation, canonical causation refs, exact schema and major-version admission,
operation-context conflict checks, actor binding, distinct unknown-schema,
unsupported-version and non-canonical-causation refusals, one-way receipt
transitions, component-domain-separated deterministic receipt identifiers, and
known effect/outcome ref families.
Scheduler, Bounded Deferred Operations, Artifact Delivery, and Sensorium are the
first consumers. `trace-explorer-core` projects their receipts into redacted
P074 events and explicit strong links; committed domain facts remain the source
of truth.

## Bounded Replication Surface

The replication core owns opaque cursor syntax, bounded contiguous delta
planning, canonical ordered sequence digests, artifact-digest verification,
route-loop checks, typed summary comparison, and partial apply reports. It does
not decide whether a fact is trusted or how it merges.

Contact Catalog supplies the private trusted-provider profile and preserves its
no-public-dump, provider-authentication, tombstone, cursor, and SQLite merge
policy. Seed Directory supplies signed capability and revocation profiles,
independently verifies every artifact, preserves revocation dominance, and
supports restart-safe cursor resume. Source identity and original fact identity
remain distinct concepts; a direct profile may bind them explicitly.

## Scoped Claims Surface

The shared runtime schema-gates request and presentation values, dispatches a
suite from an allowlisted verifier registry, checks audience, context, request
digest, validity windows, linkability, and participant-id non-disclosure, then
atomically records the nonce in a bounded durable SQLite cache. Consumers keep
separate node-owned stores under host-managed data directories instead of
sharing a global replay authority. Cache exhaustion fails closed and never
evicts a live replay entry.

The first suite, `orbiplex.nym-ed25519-cert.v1`, verifies trusted council
certificate signatures, proof of possession of the certified nym key,
certificate freshness, supported predicates, and fresh local revocation
evidence. It is certificate-based selective evidence, not zero knowledge. The
suite rejects nullifiers because this first profile cannot prove their domain
separation. Revocation snapshots are host-verified inputs to the suite; snapshot
signature admission does not silently occur inside the verifier.

Agora and Room consume the same verified evidence and retain independent local
policy. Agora verifies the signed record before consuming a nonce and binds the
scoped request to the canonical ingest candidate. Room binds the proof to the
room and joining nym before local membership policy and transport authorization.
A valid proof can therefore still be denied by either domain.

## Acceptance

`node/tools/acceptance/p081-horizontal-protocol/run.py` is the repeatable
hard-MVP gate. Its 13 checks include one real Scheduler -> Artifact Delivery ->
Sensorium causal chain plus component receipts, Contact Catalog, Seed Directory,
restart/resume, digest/source/rollback, audience/expiry/replay/revocation, and
Agora/Room checks. The Seed check exercises distinct source and target node
identities and stores, including target restart; a process-level federation
harness remains owned by P074. Every run emits a metadata-only trace bundle
containing `trace-event.v1` values and output digests, never command output,
payloads, secrets, or local paths.

## Invariants

- Evidence never grants capability by itself.
- Domain admission and merge policy remain with the consuming component.
- Caller-supplied actor identity is not trusted as host identity.
- Replication source identity does not automatically become fact authority.
- Every replicated artifact digest is recomputed before admission.
- Scoped claim request validity bounds presentation validity.
- A nonce is consumed only after the enclosing signed candidate is valid.
- Revocation freshness failure and replay-cache unavailability fail closed.
- A scoped-claim suite cannot imply snapshot authenticity it did not verify.
- Exported trace details are metadata-only and bodyless.

## Deferred Layers

- Merkle/range profiles and automatic Agora cross-relay anti-entropy;
- BBS+, Idemix, AnonCreds, accumulator, or other independently reviewed suites;
- dynamic claim-type governance beyond the initial registry seed;
- signed revocation-snapshot admission after its host ownership is decided;
- domain-by-domain adoption in Inquirium, Marketplace, Messaging, Reputation,
  Governance, and Memarium;
- production-scale performance and adversarial cryptographic audits.
