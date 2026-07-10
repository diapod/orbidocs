# Proposal 081: Horizontal Protocol Primitives for Causality, Federated Synchronization, and Scoped Nym Claims

Based on:

- `doc/normative/30-core-values/en/CORE-VALUES.en.md`
- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/040-custodial-redelivery-and-tombstones.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/053-raw-signal-access.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/40-proposals/062-temporal-storage-convention.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md`
- `doc/project/40-proposals/076-federation-identity-and-network-selector.md`
- `doc/project/40-proposals/079-cross-federation-alliance.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`

## Status

Proposed (Hard-MVP Blocker)

## Date

2026-07-09

## Executive Summary

Orbiplex has strong vertical components and host-owned runtime primitives, but three
horizontal protocol gaps now recur across otherwise separate domains:

1. causal identity and execution evidence are represented by several related but
   non-canonical fields and domain-specific outcomes;
2. federated replay and convergence are implemented separately by Seed Directory,
   Contact Catalog, Agora, Room, Shared Offer Catalog, and adjacent stores;
3. nyms can prove scoped authorship through certificates, but cannot yet present a
   reusable, suite-neutral proof of a contextual claim without disclosing a root
   participant identity.

This proposal defines three small protocol families and their implementation
boundaries:

- `causal-context.v1` plus immutable `execution-receipt.v1` facts;
- bounded replication summary/delta/apply contracts for signed immutable facts;
- suite-neutral scoped-claim request and presentation contracts for nyms.

These are related because all three make independently owned components composable
without centralizing their authority. They MUST remain separate libraries and policy
boundaries. This proposal is an umbrella contract, not permission to create one
framework that owns workflow state, domain merge rules, identity policy, or
authorization.

The minimal slice defined under *Hard-MVP Scope* is a release blocker. Full
cross-relay mesh replication, stronger anonymous-credential cryptography, universal
consumer migration, and a global trace or transaction service are explicitly not
hard-MVP requirements.

## Context and Problem Statement

### Causality Is Present but Not Yet Canonical

Orbiplex already carries causal and correlation metadata through many surfaces:

- Temporal Storage distinguishes local `causation_tx_id` from cross-store
  `correlation_id`;
- Raw Signal Access carries `causality_id` and an append-only component path;
- Middleware channel frames carry `trace/correlation-id`;
- Deferred Operations, Artifact Delivery, Sensorium, Workbench, Agent, Arca, Room,
  and Corpus each have operation, request, outcome, or continuation identifiers;
- Proposal 074 intends to infer strong, medium, and weak links across those stores.

The concepts are valid, but their shapes and trust semantics differ. The trace
explorer therefore needs adapter-specific knowledge and sometimes heuristic links.
Fan-in also demonstrates that a causal operation may have more than one predecessor,
while several local stores currently model only one prior transaction.

The missing primitive is not a global transaction registry. It is one small,
portable causal context that components can preserve or derive at boundaries, plus
an immutable receipt that links a host-observed transition to existing domain
outcomes.

### Federated Synchronization Is Repeated Domain by Domain

The project already contains useful pieces:

- Contact Catalog has a transport-neutral provider synchronizer with cursor,
  high-water, tombstone, sequence, origin, and loop-prevention semantics;
- Agora exposes count and digest primitives and anticipates future cross-relay
  anti-entropy;
- Seed Directory replays advertisements, capabilities, revocations, endorsements,
  and routing facts;
- Room tracks per-room sequence and high-water;
- Shared Offer Catalog consumes append-only offer snapshots and withdrawals;
- Memarium defines replication scope but deliberately keeps domain policy local.

Without a shared bounded exchange contract, each new replicated fact family still
needs its own summary, cursor, batch, retry, retention-gap, loop-prevention, and
diagnostic vocabulary. The missing layer should generalize mechanics only. It must
not generalize domain admission or merge semantics.

### Nym Privacy Stops Before Contextual Claims

The existing `nym-authorship-proof.v1` correctly binds a proof to an audience and
context and reserves `proof/suite` for future cryptographic profiles. The nym
roadmap also names accumulators, non-revocation proofs, group-scoped nullifiers, and
anonymous credentials as later directions.

What is missing is the protocol between those two layers: a request says which
claim must be demonstrated in which context, and a presentation proves only that
claim under an explicit linkability budget. Without it, Room, Contact Catalog,
marketplace, federation admission, and governance are likely to invent incompatible
proof envelopes or expose the participant root as a shortcut.

## Goals

- Freeze one causal-context vocabulary that distinguishes grouping, hierarchy, and
  causal predecessors.
- Preserve multi-parent causality for fan-in rather than forcing a false linear
  history.
- Define immutable execution receipts that reference domain outcomes without
  replacing them.
- Provide bounded, resumable, transport-neutral anti-entropy contracts over signed
  immutable facts and tombstones.
- Keep replication authority local: every receiver revalidates every fact and
  applies its own admission and merge policy.
- Define suite-neutral scoped claim requests and presentations for nyms.
- Bind scoped proofs to nonce, audience, context, expiry, and declared linkability.
- Reuse the current Ed25519 nym-certificate suite for the first implementation
  while preserving a clean path to stronger suites.
- Give Proposal 074 strong explicit links wherever participating components adopt
  the causal context.
- Make all three families bounded, schema-gated, replay-aware, and diagnosable.

## Non-Goals

- No global transaction manager, global operation database, or distributed ACID
  promise.
- No universal workflow engine and no replacement for Arca, Agent, Scheduler,
  Deferred Operations, Interaction Broker, or Sensorium.
- No universal CRDT and no generic merge policy for arbitrary domain objects.
- No automatic trust transfer from the replication source, Seed Directory,
  federation, or alliance.
- No automatic cross-federation Memarium widening.
- No anonymous public dump of private Contact Catalog, relationship, messaging, or
  personal-memory data.
- No requirement to implement BBS+, Idemix, AnonCreds, accumulator proofs, or another
  zero-knowledge suite in hard MVP.
- No globally stable nym nullifier or correlation handle.
- No claim proof that directly grants a capability. A verified claim remains policy
  evidence consumed by a local admission decision.
- No migration of every existing schema before hard-MVP release.

## Proposed Model

### 1. Causal Context Is Carrier Metadata, Not Authority

`causal-context.v1` gives one operation a locally meaningful causal identity. It
separates four relations that must not be conflated:

- `correlation/id` groups operations belonging to one workflow, saga, user intent,
  or support case;
- `operation/id` identifies the current operation;
- `parent/operation-id` represents structural containment, such as a workflow step
  spawning a delivery;
- `causation/refs[]` names one or more facts or receipts that caused this operation.

A fan-in operation may carry several `causation/refs`. Ordering the array has no
semantic meaning; canonicalization sorts it before digest or signature calculation.

The host mints or canonicalizes the local context at every authority boundary. A
remote or middleware-supplied context is evidence only. The receiving host creates a
new local context and preserves the accepted upstream context by digest or reference;
it MUST NOT adopt a remote `origin/actor-ref` as an authenticated local actor.

Conceptual shape:

```json
{
  "schema": "causal-context.v1",
  "schema/v": 1,
  "context/id": "causal-context:01K0...",
  "correlation/id": "corr:story011:fish-water",
  "operation/id": "operation:01K0...",
  "parent/operation-id": "operation:01JZ...",
  "causation/refs": [
    "execution-receipt:01JZ...",
    "artifact:sha256:..."
  ],
  "origin/actor-ref": "component:arca",
  "idempotency/digest": "sha256:...",
  "classification/ref": "classification:public",
  "created/at": "2026-07-09T12:00:00Z"
}
```

`idempotency/digest` is optional and carries a digest rather than a raw key so trace
exports do not disclose replay credentials. It is diagnostic metadata; the owning
domain's idempotency store remains authoritative.

### 2. Execution Receipts Are Immutable Links

`execution-receipt.v1` records one host-observed transition. It does not become the
domain result and it does not claim that an external-world effect occurred unless it
references evidence from the domain that owns that claim.

Conceptual shape:

```json
{
  "schema": "execution-receipt.v1",
  "schema/v": 1,
  "receipt/id": "execution-receipt:01K0...",
  "causal/context": {
    "context/id": "causal-context:01K0...",
    "correlation/id": "corr:story011:fish-water",
    "operation/id": "operation:01K0...",
    "causation/refs": ["execution-receipt:01JZ..."]
  },
  "operation/id": "operation:01K0...",
  "capability/id": "artifact.delivery.send",
  "transition/from": "accepted",
  "transition/to": "completed",
  "attempt/no": 1,
  "recorded/by": "node:did:key:z6Mk...",
  "recorded/at": "2026-07-09T12:00:01Z",
  "policy/decision-ref": "policy-decision:01K0...",
  "effect/refs": ["delivery:01K0..."],
  "outcome/refs": ["artifact-delivery-outcome:01K0..."],
  "previous/receipt-ref": "execution-receipt:01JZ..."
}
```

Receipts are append-only facts. Retrying, cancelling, denying, or superseding an
operation appends another receipt; it never rewrites the prior receipt. A domain may
project a current operation state from those facts, but the generic receipt family
does not own that projection.

The first closed transition vocabulary is:

```text
proposed | accepted | rejected | deferred | running |
completed | failed | cancelled | timed-out | superseded
```

Domains may map richer states to this diagnostic vocabulary while preserving their
own authoritative state machine.

### 3. Bounded Anti-Entropy Exchanges Signed Facts, Not Trust

The replication family consists of:

- `replication-summary.v1`;
- `replication-delta-request.v1`;
- `replication-delta-batch.v1`;
- `replication-apply-report.v1`.

Each configured dataset has a `replication/profile-id`. The profile defines:

- accepted artifact families;
- ordering or sequence interpretation;
- whether tombstones are required;
- digest profile;
- retention-gap behavior;
- source authorization and admission policy references;
- maximum batch items and bytes.

The generic protocol treats cursors as opaque. It may compare equality and preserve
them, but only the profile interprets ordering. This prevents a local SQLite `tx_id`,
an Agora topic high-water, and a Contact Catalog sequence from becoming one false
global sequence type.

Conceptual summary:

```json
{
  "schema": "replication-summary.v1",
  "schema/v": 1,
  "summary/id": "replication-summary:01K0...",
  "dataset/id": "seed-directory:revocations",
  "dataset/epoch": 3,
  "replication/profile-id": "seed-directory-revocations@v1",
  "source/node-id": "node:did:key:z6Mk...",
  "federation/id": "orbiplex-main",
  "high-water/cursor": "cursor:opaque:...",
  "retention/floor": "cursor:opaque:...",
  "records/count": 1832,
  "tombstones/high-water": "cursor:opaque:...",
  "digest": {
    "profile": "canonical-sequence-sha256-v1",
    "value": "sha256:..."
  },
  "generated/at": "2026-07-09T12:00:00Z",
  "expires/at": "2026-07-09T12:05:00Z",
  "signature": {}
}
```

Conceptual request and batch:

```json
{
  "schema": "replication-delta-request.v1",
  "schema/v": 1,
  "request/id": "replication-request:01K0...",
  "dataset/id": "seed-directory:revocations",
  "known/summary-ref": "replication-summary:01JZ...",
  "after/cursor": "cursor:opaque:...",
  "limits": { "max/items": 256, "max/bytes": 262144 },
  "include/tombstones": true,
  "causal/context": {
    "context/id": "causal-context:01K0...",
    "correlation/id": "corr:replication:revocations",
    "operation/id": "operation:01K0...",
    "causation/refs": []
  }
}
```

```json
{
  "schema": "replication-delta-batch.v1",
  "schema/v": 1,
  "batch/id": "replication-batch:01K0...",
  "request/ref": "replication-request:01K0...",
  "dataset/id": "seed-directory:revocations",
  "items": [
    {
      "item/id": "revocation:...",
      "item/kind": "fact",
      "artifact/schema": "capability-passport-revocation.v1",
      "artifact/digest": "sha256:...",
      "origin/node-id": "node:did:key:z6Mk...",
      "sequence/ref": "cursor:opaque:...",
      "artifact": {}
    }
  ],
  "next/cursor": "cursor:opaque:...",
  "complete": false,
  "batch/digest": "sha256:...",
  "signature": {}
}
```

Every item is schema-gated and domain-verified independently. Batch signature
validity does not make an item valid. A batch may therefore partially succeed, and
`replication-apply-report.v1` records bounded counts and item-level refusal codes
without echoing sensitive artifact bodies.

Conceptual apply report:

```json
{
  "schema": "replication-apply-report.v1",
  "schema/v": 1,
  "report/id": "replication-apply-report:01K0...",
  "batch/ref": "replication-batch:01K0...",
  "outcomes": {
    "inserted": 12,
    "replaced": 2,
    "stale": 1,
    "rejected": 1
  },
  "refusals": [
    { "item/id": "revocation:...", "reason/code": "signature-invalid" }
  ],
  "accepted/cursor": "cursor:opaque:...",
  "recorded/at": "2026-07-09T12:00:02Z"
}
```

The hard-MVP digest profile is `canonical-sequence-sha256-v1`: reuse each artifact's
canonical digest and digest the profile-ordered sequence of
`(item-id, artifact-digest, item-kind)`. Merkle range proofs are a compatible later
profile, not a first-slice requirement.

### 4. Scoped Claims Prove Predicates Without Becoming Capabilities

The scoped-claim family consists of:

- `scoped-claim-request.v1`;
- `scoped-claim-presentation.v1`;
- a suite registry and verifier interface;
- a later `claim-revocation-state.v1` profile for suites that use accumulators or
  independently distributed non-revocation state.

A verifier asks for predicates, not a complete credential. The request binds the
proof to one audience, context, nonce, and validity window.

```json
{
  "schema": "scoped-claim-request.v1",
  "schema/v": 1,
  "request/id": "scoped-claim-request:01K0...",
  "audience": "room-membership-admission",
  "context/domain": "room:participant:did:key:z6MkAuthority:01JROOM",
  "nonce": "base64url:...",
  "claims/requested": [
    {
      "claim/type": "nym/certificate-current",
      "predicate": "equals",
      "value": true
    }
  ],
  "linkability/max": "group-scoped",
  "issued/at": "2026-07-09T12:00:00Z",
  "expires/at": "2026-07-09T12:01:00Z"
}
```

```json
{
  "schema": "scoped-claim-presentation.v1",
  "schema/v": 1,
  "presentation/id": "scoped-claim-presentation:01K0...",
  "request/ref": "scoped-claim-request:01K0...",
  "request/digest": "sha256:...",
  "subject/kind": "nym",
  "subject/id": "nym:did:key:z6Mk...",
  "audience": "room-membership-admission",
  "context/domain": "room:participant:did:key:z6MkAuthority:01JROOM",
  "nonce": "base64url:...",
  "claims/proven": [
    {
      "claim/type": "nym/certificate-current",
      "predicate": "equals",
      "value": true
    }
  ],
  "proof/suite": "orbiplex.nym-ed25519-cert.v1",
  "proof/material": {
    "nym/certificate": {},
    "nym/signature": { "alg": "ed25519", "value": "base64url:..." }
  },
  "linkability/scope": "group-scoped",
  "nullifier": null,
  "revocation/evidence-ref": "nym-certificate:...",
  "issued/at": "2026-07-09T12:00:03Z",
  "expires/at": "2026-07-09T12:01:00Z"
}
```

The first suite maps existing nym-certificate scope into the limited claims it can
honestly prove. It does not simulate zero knowledge and it does not claim
non-revocation stronger than certificate freshness and the available revocation
reference. The initial claim registry contains:

- `nym/certificate-current`: the certificate is fresh, accepted under the configured
  issuer policy, and the presenter proved possession of the certified nym key by
  signing the request-bound presentation;
- `nym/context-authorized`: the certificate's existing scope fields cover the
  requested audience and context. The suite emits this claim only when those fields
  actually express the requested context.

For the first Room consumer, `nym/certificate-current` is evidence about the nym;
Room membership remains a separate membership-attestation and local-policy decision.
For the Agora consumer, `nym/context-authorized` may additionally be emitted when the
certificate's topic, record-kind, content-schema, disclosure, and federation scope
cover the ingest context.

The nym signature covers a domain-separated canonical digest of the request and the
presentation without `nym/signature`. A verifier recomputes `request/digest`; a
request id alone is not a content binding. The first suite may report
`linkability/scope = group-scoped` only when the certificate's declared
`privacy/linkability` and `privacy/context-domain` constrain the nym to the same
request context. Otherwise it reports the wider supported class or rejects a request
whose `linkability/max` would be exceeded.

Future suites may prove richer predicates or use a scoped nullifier. A nullifier MUST
be domain-separated by audience and context. A globally reusable nullifier is invalid
even if its underlying cryptographic proof verifies.

### 5. Verification, Admission, and Authority Stay Separate

All three families provide evidence and mechanics:

- causal context explains how operations relate;
- replication transports candidate facts and reports divergence;
- scoped claims prove bounded predicates.

None answers the local authorization question. Capability Binding, Room authority,
Artifact Delivery admission, federation-root policy, restriction policy, and domain
stores remain responsible for their existing decisions. A valid presentation can
still be denied. A valid replication batch can be fully refused. A valid causal
context can describe an unauthorized operation without authorizing it.

## Hard-MVP Scope

P081 is a hard-MVP release blocker with the following bounded completion contract:

| Area | Required for hard MVP | Explicitly deferred |
|---|---|---|
| Causal contracts | Accepted schemas, protocol mirrors, schema-gate coverage, pure context derivation/join helpers, immutable receipt validation | Rewriting every historical domain artifact |
| Causal adoption | Scheduler, Bounded Deferred Operations, Artifact Delivery, and Sensorium preserve or derive context and append receipt links | Universal adoption by every middleware and UI surface |
| Trace consumption | P074 normalized trace adapters consume canonical context as strong links | Production global trace collection |
| Replication contracts | Summary, delta request, delta batch, and apply report schemas with bounded limits and typed failures | Universal CRDT or arbitrary-object merge |
| Replication runtime | One generic core plus two profiles: Contact Catalog trusted-provider sync and Seed Directory revocation/capability fact sync | Agora cross-relay mesh and federated Memarium replication |
| Scoped-claim contracts | Request/presentation schemas, verifier registry, replay cache, and existing Ed25519 nym-certificate suite | BBS+, Idemix, AnonCreds, accumulator, or ZK suite |
| Scoped-claim adoption | One nym-authored Agora verification path and one Room admission path consume the common verifier result | Marketplace, governance, reputation, and all Contact Catalog consumers |
| Acceptance | One repeatable multi-node smoke covers causal propagation, interrupted/resumed delta sync, digest mismatch, proof audience binding, nonce replay, expiry, and revocation-stale refusal | Production-scale performance and adversarial cryptographic audit |

Hard-MVP readiness requires all non-deferred tracker rows below to be `done` and the
acceptance smoke to pass from clean profiles.

## Required Changes to Existing Proposals

The following documents require targeted synchronization during implementation. The
listed change is normative for P081 adoption; unrelated parts of each proposal remain
owned by that proposal.

| Proposal(s) | Required change during P081 implementation |
|---|---|
| [P033](033-workflow-fan-out-and-temporal-orchestration.md) | Carry canonical causal context through fan-out and model fan-in with multiple `causation/refs`; append receipts without replacing `WorkflowStepDispatch`. |
| [P045](045-sensorium-local-enaction-stratum.md), [P071](071-sensorium-workbench.md), [P073](073-agent-orchestration-organ.md) | Link directives, Workbench operations, agent steps, effect proposals, and domain outcomes through the causal context and execution receipts. |
| [P053](053-raw-signal-access.md), [P080](080-multiplexed-middleware-channel-executor.md) | Project current `causality_id`, `trace.causality_id`, and `trace/correlation-id` fields into the canonical context; keep transport-local sequence and request ids distinct. |
| [P055](055-bounded-deferred-operation-contract.md), [P062](062-temporal-storage-convention.md) | Preserve context across continuation/recovery and map receipts into local temporal transactions without creating a global transaction registry. |
| [P074](074-multi-node-federation-harness-and-trace-explorer.md) | Make `trace-event.v1` and `trace-link.v1` consume canonical context and classify adopted links as strong rather than heuristic. |
| [P025](025-seed-directory-as-capability-catalog.md), [P054](054-user-maintained-federated-seed-directory.md) | Define Seed Directory replication profiles for capability and revocation facts, including source trust, rollback, retention-gap, and multi-directory semantics. |
| [P035](035-agora-topic-addressed-record-relay.md), [P040](040-custodial-redelivery-and-tombstones.md) | Align topic count/digest and future cross-relay anti-entropy with the shared replication family; keep automatic mesh replication deferred from hard MVP. |
| [P036](036-memarium.md), [P067](067-shared-offer-catalog-over-agora.md), [P070](070-room-primitive.md) | Reuse replication profiles where these domains later exchange signed fact streams; preserve explicit space promotion and domain-specific sequence/merge authority. |
| [P058](058-contact-catalog.md) | Adapt `CatalogSynchronizer` mechanics to the shared summary/delta/apply contracts without weakening provider authentication or private lookup policy. |
| [P076](076-federation-identity-and-network-selector.md), [P079](079-cross-federation-alliance.md) | Bind replication profiles to the active federation and state again that alliance is only admission input and never widens replication automatically. |
| [P015](015-nym-certificates-and-renewal-baseline.md), [P035](035-agora-topic-addressed-record-relay.md) | Map nym-certificate scope and Agora authorship verification into the first scoped-claim suite. |
| [P018](018-layered-capability-limited-participant-restrictions.md), [P024](024-capability-passports-and-network-ledger-delegation.md), [P051](051-swarm-membership-and-reputation-bootstrap.md) | Define that verified claims are evidence only; negative or non-revocation claims require fresh suite-specific evidence and never bypass current restrictions or passport policy. |
| [P058](058-contact-catalog.md), [P061](061-contact-attestation-service.md), [P065](065-local-relationship-layer.md), [P070](070-room-primitive.md) | Reuse scoped presentations for context-bound nym evidence while preserving local relationship and admission decisions. |
| [P059](059-participant-and-nym-key-role-derivation.md) | Store any suite-private holder material in the Pseudonym Vault without adding public participant recovery metadata or a new standing `participant/dh` projection. |

## Security and Privacy Invariants

1. Caller-supplied causal metadata never becomes authenticated actor identity.
2. Correlation and causation metadata grants no capability and carries no trust.
3. Exported traces use digests and refs by default; raw payloads and raw idempotency
   keys remain local.
4. A replication source is a transport peer, not an authority. Every item is
   independently schema-gated, signature-verified, freshness-checked, and admitted.
5. Replication is bounded by item count, byte count, deadline, retry budget, and
   configured dataset/profile allowlists.
6. Cursor rollback, epoch rollback, digest mismatch, retention gaps, and stale
   tombstones are explicit typed outcomes.
7. Private datasets require an authenticated direct profile; the generic protocol
   exposes no anonymous listing endpoint.
8. A scoped claim presentation never contains `participant:did:key:...` unless a
   future explicit disclosure mode separately authorizes that disclosure. The
   hard-MVP schemas forbid it.
9. Audience, context, nonce, request reference, and expiry are verification inputs,
   not advisory metadata.
10. A proof suite cannot widen requested predicates or linkability. The effective
    result is the intersection of request, presentation, suite capability, and local
    policy.
11. No negative claim such as "not restricted" is accepted without current,
    suite-defined non-revocation evidence.
12. Unknown replication profiles, claim types, proof suites, receipt transitions,
    or artifact families fail closed.

## Trade-offs

Benefits:

- components compose through shared evidence contracts without sharing mutable
  runtime state;
- Proposal 074 receives stronger causal links and fewer heuristic adapters;
- retries, continuation, fan-in, and effect outcomes become easier to diagnose;
- new replicated components reuse bounded sync mechanics instead of inventing a
  private protocol;
- public and private replication profiles share mechanics without sharing policy;
- nyms can accumulate contextual utility without making participant roots public;
- stronger privacy suites can replace certificate-based proof material without
  changing every consumer contract.

Costs:

- more schema families and registry surfaces;
- existing components need adapters and migration tests;
- causal metadata can become noisy unless receipt production is selective;
- generic replication must resist pressure to absorb domain merge policy;
- nonce/replay and replication cursor state require bounded durable storage;
- cryptographic suite evolution needs conformance vectors and independent review.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Causal context becomes a global state service | Keep context value-like and receipts local; P074 remains a read-only projection. |
| Remote actor spoofing through propagated context | Receiving host derives local actor and stores remote context only as upstream evidence. |
| Fan-in is flattened to one false cause | `causation/refs[]` is bounded, unique, canonicalized, and multi-valued. |
| Receipt claims external success without evidence | `completed` receipts for effectful operations require domain `outcome/refs`. |
| Replication framework absorbs domain semantics | Generic core handles summary/delta/bounds only; profile and sink own validation and merge. |
| A valid batch signature launders invalid facts | Verify and admit every item independently; apply report supports partial success. |
| Cursor or epoch rollback resurrects stale state | Persist highest accepted epoch/cursor per source and profile; reject rollback before apply. |
| Retention gap is mistaken for an empty delta | Return `retention-gap` with current floor and stop hard-MVP delta application; snapshot recovery belongs to a domain-owned or post-MVP profile. |
| Sync loop amplifies traffic | Preserve origin and path metadata, reject self-originated items, cap hops and retries. |
| Claim presentation is replayed in another context | Require nonce, request ref, audience, context, short expiry, and bounded replay cache. |
| Scoped nullifier becomes globally correlatable | Domain-separate it by audience and context; reject wider-than-requested linkability. |
| First certificate suite is marketed as zero knowledge | Suite metadata states its actual disclosure and revocation properties; UI and docs label it honestly. |
| Revocation freshness is unavailable | Fail closed for claims whose validity depends on current non-revocation state. |

## Frozen Initial Decisions

1. P081 is one umbrella proposal but three implementation modules and policy
   boundaries.
2. `correlation/id`, `operation/id`, `parent/operation-id`, and
   `causation/refs[]` remain distinct concepts.
3. Causal context and execution receipts are metadata/evidence, never authority.
4. No global transaction or trace registry is introduced.
5. Hard-MVP replication uses opaque cursors and
   `canonical-sequence-sha256-v1`; Merkle profiles are deferred.
6. Contact Catalog and Seed Directory are the first replication consumers.
7. Replication items are independently verified and may partially succeed.
8. `orbiplex.nym-ed25519-cert.v1` is the first scoped-claim suite.
9. The first suite proves only predicates supported by existing certificate scope.
10. Proof verification and admission policy remain separate calls and data types.
11. Stronger anonymous-credential and non-revocation suites are post-MVP.
12. The hard-MVP acceptance pack is multi-node and exercises all three families.

## Resolved Deferred Decisions

Resolved on 2026-07-10:

1. `execution-receipt.v1` emission is selective. Hard-MVP receipts are emitted at
   authority boundaries, external effects, retry/cancel transitions, and terminal
   states. Components MAY keep richer local diagnostics, but P081 does not require a
   receipt for every internal diagnostic transition.
2. `replication/retention-gap` in hard MVP is a typed refusal/recovery condition,
   not an automatic data-repair flow. Snapshot transfer or other recovery policy is
   post-MVP unless a consuming domain already owns a stricter profile.
3. Runtime promotion after implementation should create three separate solution or
   capability surfaces for causal context, bounded replication, and scoped claims,
   after at least two consumers prove each boundary. P081 remains the umbrella
   proposal, not a monolithic runtime component.
4. Scoped-claim nonce replay cache retention is `expires/at` plus configured
   clock-skew, and the cache is durable across daemon restart for that window.
5. The first scoped-claim consumers are the nym-authored Agora ingest path and the
   Room admission path.
6. `canonical-sequence-sha256-v1` reuses the existing artifact canonical digest. The
   replication profile defines only the ordered sequence of
   `(item-id, artifact-digest, item-kind)`.

## Open Questions

No open question blocks the hard-MVP slice. The following decisions are deliberately
deferred:

1. Whether the first stronger anonymous suite uses an accumulator-based credential,
   Idemix/AnonCreds-style presentation, BBS+, or another independently reviewed
   construction.
2. Whether Agora cross-relay synchronization adopts range digests, Merkle segments,
   or both after the canonical-sequence profile is measured.
3. Whether exported cross-node execution receipts require node signatures by default
   or only when they leave a mutually authenticated session and local trace bundle.
4. Whether claim-type lifecycle belongs in a dedicated registry or a checked policy
   sidecar after the first two claim types prove the boundary.

## Next Actions

1. Add accepted schemas and positive/negative fixtures for the hard-MVP contract
   families.
2. Mirror the schemas into Node protocol contracts and register all boundary uses in
   schema-gate.
3. Implement the pure causal context, replication, and scoped-claim verification
   cores before daemon integration.
4. Migrate the named first consumers without changing their domain authority.
5. Add the P081 multi-node acceptance pack and connect its trace output to P074.
6. Synchronize every affected proposal row above as its implementation lands.

## Implementation Guidance

### Layering and Ownership

Recommended strata:

```text
protocol
  schema-backed DTOs, canonical payloads, constants, error vocabulary

causal-context core
  root/child/join derivation, canonicalization, receipt validation

replication core
  summary comparison, bounded delta planning, apply reports, profile traits

scoped-claims core
  request/presentation validation, verifier registry, verified-claim values

domain adapters
  Seed Directory, Contact Catalog, Room, Agora, AD, Sensorium, Agent

daemon / attached services
  authenticated caller binding, persistence, scheduling, transport, policy, audit
```

The first implementation may place very small causal types in `protocol` or
`host-vocabulary` rather than creating a crate prematurely. Replication and scoped
claim verification are substantial enough to justify substrate-free core crates once
their traits have two consumers. None of these core crates may depend on daemon,
HTTP, SQLite, async runtimes, UI, or a domain service.

### Causal Core Shapes

Illustrative Rust interfaces:

```rust
pub trait CausalContextCarrier {
    fn causal_context(&self) -> Option<&CausalContext>;
}

pub trait CausalContextFactory {
    fn root(&self, input: RootContextInput) -> Result<CausalContext, CausalError>;
    fn child(&self, parent: &CausalContext, input: ChildContextInput)
        -> Result<CausalContext, CausalError>;
    fn join(&self, parents: &[CausalContextRef], input: JoinContextInput)
        -> Result<CausalContext, CausalError>;
}

pub trait ExecutionReceiptSink {
    fn append(&self, receipt: &ExecutionReceipt) -> Result<(), ReceiptStoreError>;
}
```

`join` MUST deduplicate and canonicalize parent refs and enforce a configured maximum.
It does not inspect domain payloads. Receipt sinks append to the owning component's
temporal log or commit log; they do not all write to one database.

Receipt emission is intentionally selective. The hard-MVP minimum is: append receipts
at authority boundaries, external effects, retry/cancel transitions, and terminal
states. Domains may emit additional local diagnostics, but P081 does not turn every
internal state transition into a shared protocol receipt.

Adapters should map existing fields without destructive migration:

```text
existing correlation/id         -> causal-context.correlation/id
existing causality_id           -> accepted upstream ref or context/id mapping
deferred operation/id           -> causal-context.operation/id or child operation
delivery/id / directive/id      -> effect/outcome refs, not replacement operation ids
local causation_tx_id           -> store-local projection link
```

### Replication Core Shapes

Illustrative interfaces:

```rust
pub trait ReplicatedFact {
    fn item_id(&self) -> &str;
    fn artifact_schema(&self) -> &str;
    fn canonical_digest(&self) -> &ArtifactDigest;
    fn origin_node_id(&self) -> Option<&str>;
    fn sequence_ref(&self) -> Option<&str>;
    fn item_kind(&self) -> ReplicationItemKind;
}

pub trait ReplicationSource<F: ReplicatedFact> {
    fn summary(&self, dataset: &DatasetRef) -> Result<ReplicationSummary, SourceError>;
    fn delta(&self, request: &ReplicationDeltaRequest)
        -> Result<ReplicationDeltaBatch<F>, SourceError>;
}

pub trait ReplicationSink<F: ReplicatedFact> {
    fn admit(&self, fact: F, context: &ReplicationAdmissionContext)
        -> ReplicationItemOutcome;
}

pub trait ReplicationProfile<F: ReplicatedFact> {
    fn profile_id(&self) -> &str;
    fn compare_sequence(&self, current: Option<&F>, candidate: &F)
        -> MergeDisposition;
    fn requires_tombstones(&self) -> bool;
    fn limits(&self) -> ReplicationLimits;
}
```

The source trait may gain an async adapter at the service layer, but the profile and
comparison logic should remain pure. HTTP, INAC, Artifact Delivery, or Matrix are
transports under the same contract, not part of the profile semantics.

The hard-MVP digest profile, `canonical-sequence-sha256-v1`, reuses each artifact's
canonical digest and canonicalizes only the profile-ordered sequence of
`(item-id, artifact-digest, item-kind)`. P081 does not define a second artifact
canonicalization system.

`replication/retention-gap` is a typed outcome that stops hard-MVP delta application.
Automatic snapshot transfer is not part of the shared hard-MVP core unless a
consuming domain already defines and owns that recovery profile.

Persist per `(profile-id, dataset-id, source-node-id)`:

- highest accepted dataset epoch;
- last accepted cursor and summary digest;
- retention floor last observed;
- latest successful and failed sync time;
- bounded failure class and retry metadata;
- counted apply outcomes;
- no private artifact body in operator diagnostics.

### Scoped-Claim Core Shapes

Illustrative interfaces:

```rust
pub trait ScopedClaimVerifier {
    fn suite_id(&self) -> &str;
    fn verify(
        &self,
        request: &ScopedClaimRequest,
        presentation: &ScopedClaimPresentation,
        context: &ClaimVerificationContext,
    ) -> Result<VerifiedClaims, ClaimVerificationError>;
}

pub trait ClaimAdmissionPolicy {
    fn decide(
        &self,
        claims: &VerifiedClaims,
        operation: &ClaimedOperation,
    ) -> ClaimAdmissionDecision;
}
```

`VerifiedClaims` is deliberately not a capability grant and should expose no method
named `authorize`. The admission adapter combines verified claims with current
restrictions, revocation freshness, federation policy, Room policy, passport state,
and caller binding as required by the consuming operation.

The first consumers are the nym-authored Agora ingest path and the Room admission
path. Both consume `VerifiedClaims` as evidence and then call their own admission
policy; neither path treats a verified claim as an authorization grant.

The first suite adapter should reuse existing nym certificate verification and map
only:

- certificate validity plus a nym-key signature over the request-bound
  presentation;
- presentation audience/request binding and certificate context scope;
- certificate-authorized record or action class;
- available revocation/expiry evidence.

It MUST NOT derive participant identity, reputation, unrestricted federation
membership, or absence of sanctions from a certificate that does not assert them.

### Boundary Validation and Error Classes

All ingress and egress artifacts pass through schema-gate before typed parsing.
Runtime semantic validation additionally freezes at least these classes:

```text
causal/context-invalid
causal/actor-spoofed
causal/predecessor-limit-exceeded
receipt/invalid-transition
receipt/missing-domain-evidence

replication/profile-unknown
replication/cursor-rollback
replication/epoch-rollback
replication/digest-mismatch
replication/retention-gap
replication/item-invalid
replication/source-unauthorized

claim/suite-unsupported
claim/audience-mismatch
claim/context-mismatch
claim/nonce-replay
claim/expired
claim/proof-invalid
claim/revocation-stale
claim/linkability-too-wide
```

Retryability is explicit. Retention gaps, stale revocation state, and transient source
unavailability may be retryable after refresh or a domain-owned snapshot transfer.
Invalid proof, digest mismatch, rollback, actor spoofing, and unsupported profiles
are not retried without a changed input or policy.

### Storage, Replay, and Bounds

- Causal contexts are immutable values. A component may inline them in a local fact
  or store them once by digest and reference them.
- Execution receipts use the Temporal Storage Convention and replay into
  component-local projections.
- Replication cursors and summaries are durable operational state, but replicated
  domain facts remain in domain-owned stores.
- Nonce replay state is bounded by `expires/at` plus configured clock-skew and
  survives daemon restart for that proof window.
- All arrays have explicit item caps; all artifacts have byte caps; all remote work
  has deadlines and bounded retries.
- Trace exports redact proof material, credential bodies, private artifacts, and raw
  idempotency keys.

### Acceptance Shape

The first repeatable acceptance profile should run at least two nodes and prove:

1. a scheduler-launched deferred operation retains canonical context through one AD
   delivery and Sensorium outcome;
2. P074 projection links those facts only through explicit strong identifiers;
3. Contact Catalog or Seed Directory sync resumes after interruption from its stored
   cursor without duplicate current facts;
4. cursor rollback, digest mismatch, and retention gap fail with distinct classes;
5. a valid scoped nym presentation succeeds only for its requested audience and
   context;
6. nonce replay, expiry, widened linkability, stale revocation evidence, and hidden
   participant-id leakage all fail closed;
7. operator diagnostics expose refs, digests, counts, and failure classes but no
   private payloads or proof secrets.

## Implementation Tracker

Status values: `todo`, `in-progress`, `done`, `deferred`.

| ID | Deliverable | Status | Done criteria / evidence |
|---|---|---|---|
| P081-001 | Freeze umbrella architecture, boundaries, hard-MVP scope, affected proposals, and implementation guidance | done | This proposal defines three separate primitives, explicit non-goals, initial contracts, first consumers, and blocker criteria. |
| P081-002 | Add canonical causal-context and execution-receipt schemas with fixtures | todo | Positive fixtures plus negative multi-parent-limit, actor-spoof, invalid-transition, missing-evidence, and unknown-field cases pass schema validation. |
| P081-003 | Add replication summary, delta request, delta batch, and apply-report schemas with fixtures | todo | Bounded item/byte limits, opaque cursors, digest profile, tombstones, partial apply, rollback, and retention-gap examples are covered. |
| P081-004 | Add scoped-claim request and presentation schemas plus suite/claim registry seed | todo | Audience, context, nonce, expiry, linkability, proof suite, and participant-id leak rejection have schema plus semantic privacy-guard coverage. |
| P081-005 | Mirror all hard-MVP schemas into Node protocol contracts and register schema-gate boundaries | todo | Contract mirror tests and ingress/egress/import/export boundary tests pass; unsupported boundaries fail closed. |
| P081-006 | Implement pure causal-context derivation, child, fan-in join, canonicalization, and receipt validation | todo | Substrate-free unit/property tests cover deterministic ids/digests, unordered parent equivalence, limits, and immutable transitions. |
| P081-007 | Adopt causal context and receipts in Scheduler, Bounded Deferred Operations, Artifact Delivery, and Sensorium | todo | Context survives launch, continuation, retry, delivery, and outcome; actor binding is host-derived and no domain state machine is replaced. |
| P081-008 | Align P074 trace schemas and first adapters with canonical causal context | todo | Adopted paths produce strong explicit links; trace export privacy tests pass; no global trace source of truth is introduced. |
| P081-009 | Implement transport-neutral bounded replication core and profile traits | todo | Summary comparison, delta planning, partial apply reports, limits, loop prevention, rollback, digest mismatch, and retention gaps have focused tests. |
| P081-010 | Adapt Contact Catalog trusted-provider sync to the shared replication contracts | todo | Existing privacy, provider trust, tombstone, cursor, high-water, and no-public-dump invariants remain green. |
| P081-011 | Add Seed Directory capability/revocation replication profiles | todo | Signed fact batches, multi-directory source identity, rollback, revocation dominance, and restart replay are covered. |
| P081-012 | Implement scoped-claim verifier registry and bounded durable nonce replay cache | todo | Unknown suites fail closed; nonce state survives restart for the proof window; verification returns evidence values, not authorization. |
| P081-013 | Implement `orbiplex.nym-ed25519-cert.v1` scoped-claim adapter | todo | Adapter proves only certificate-supported predicates and fails on audience/context mismatch, expiry, stale revocation evidence, and widened claims. |
| P081-014 | Adopt scoped-claim verification in the nym-authored Agora ingest path and one Room admission path | todo | Both consumers call the same verifier core and then their own local policy; valid proof can still be denied by policy. |
| P081-015 | Add repeatable multi-node P081 acceptance smoke and failure matrix | todo | Clean-profile runner covers the seven acceptance points above and emits a redacted trace bundle. |
| P081-016 | Synchronize affected proposals, Node implementation ledger/MVP tracker, architecture map, and MVP readiness snapshot | todo | Every affected proposal records its adopted boundary; generated docs and cross-repo trackers are in sync with implementation evidence. |
| P081-017 | Promote stable runtime ownership into solution components and capability sidecars | todo | Promotion creates separate causal-context, bounded-replication, and scoped-claims surfaces after at least two consumers prove each boundary; no speculative component shell. |
| P081-018 | Add Agora cross-relay mesh and range/Merkle digest profiles | deferred | Post-MVP resilience layer after bounded canonical-sequence profile measurements. |
| P081-019 | Add stronger anonymous-credential and non-revocation suites | deferred | Requires independent cryptographic review, conformance vectors, migration plan, and explicit privacy analysis. |
| P081-020 | Migrate additional Room, Marketplace, Contact Catalog, Messaging, Reputation, Governance, and Memarium consumers | deferred | Domain-by-domain post-MVP adoption; no blanket migration. |
