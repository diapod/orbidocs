# Corpus

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/003-question-envelope-and-answer-channel.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/067-shared-offer-catalog-over-agora.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/036-room/036-room.md`

Planned extension:

- `doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`

Related schemas:

- `topic-taxonomy.v1`
- `topic-resolution.v1`
- `corpus-reasoning-query.v1`
- `corpus-reasoning-bid.v1`
- `corpus-reasoning-bid-state.v1`
- `corpus-reasoning-answer.v1`
- `corpus-deliberation-review-claims.v1`
- `corpus-reasoning-experiment-review.v3`
- `corpus-reasoning-room-policy.v1`
- `corpus-reasoning-room-policy.v2`
- `corpus-reasoning-chair-control-policy.v1`
- `corpus-reasoning-room-invite.v1`
- `corpus-reasoning-turn-proposal.v1`
- `service-offer.v1`
- `procurement-offer.v1`
- `procurement-contract.v1`
- `room.v1`
- `room-policy.v1`
- `room-membership-attestation.v1`
- `agent.binding.v1`
- `agent.binding.v2`
- `agent.outcome.v1`
- `corpus-chair-admission.v1`
- `corpus-agent-answer-draft.accept.request.v1`
- `corpus-agent-answer-draft.v1`
- `classification.v1`
- `room-moderation-intent.v1`
- `room-moderation-audit.v1`
- `inference-execution-posture.v1` (planned)
- `inference-execution-provenance.v1` (planned)

## Status

Hard-MVP solution implemented; node-local live-deliberation slice implemented.

The hard-MVP procurement slice is implemented and accepted as the solution-level
contract for topic-routed collaborative reasoning. The post-MVP live-deliberation
control plane now has Corpus policy, signed invite, AD admission, local
join/readiness, append-only persistence, typed failure mapping, AD-owned
transport idempotency, Corpus-owned semantic replay by signed `invite/id`,
canonical signer-key and exact-grant validation, configured remote
trust-root verification, stable invite/delivery replay after recipient restart,
and a bounded node-local WSS Room carrier with authority-visible metadata-only
observations. Stable authority bind, subject sequence checkpoints, exact send
replay, and controlled session rejoin make the carrier restart-safe. The bounded
Agent-backed chair and selected-participant joins are implemented. Participant
turns remain inert until admitted through `corpus.room.turn`; the chair observes
them through a bounded host-owned Interaction Broker Room source. Module watches
require daemon-issued grant material bound to the exact Room, while local control
retains an explicit administrative path. Turn expiry shares the Room membership
clock-skew tolerance without widening Room lifetime. Transport `seq/no`, rather
than a second ephemeral `turn/no` store, owns monotonic replay. Inert Corpus
outcome-draft acceptance through the existing answer envelope is implemented;
a separate Corpus-owned local-control transition now validates ready quorum,
room high-water, chair identity, evidence, and idempotency before signing and
publishing the signed outcome. The Agent still has no publication authority.
The optional Agent-chair moderation profile is also implemented. Distributor and
operator ceilings resolve requested controls once into an immutable effective policy.
Room policy v2 binds its exact ref and digest; Agent binding v2 separately binds that
policy and the current membership/delegation evidence. Corpus maps organic, moderated,
and baton modes to Room's open, moderated, and round-robin modes, while voice, kick,
ban, and floor proposals remain inert until canonical Room admission. Every use
rechecks current policy, binding, review floor, scoped delegation, target, generation,
high-water, TTL, and the current distributor/operator ceilings. A changed monotone
intersection invalidates the old policy generation and requires explicit re-admission;
it is neither honored until expiry nor silently rewritten. Chair loss revokes
delegation and floor authority without electing a replacement from connected presence.
The v1 Room policy remains valid without v2 Chair-control fields; their absence maps to
Room's `open` floor and never to an implicit controlled denial. Only v2 requires and
resolves the exact Chair-control policy binding.

## Date

2026-07-16

## Executive Summary

Corpus is the topic-routed collaborative reasoning component. It lets a node
resolve a question into a governed topic, discover providers advertising
Corpus competence on that topic, broadcast a bounded reasoning query, collect
signed bids, and bridge the selected offer into the ordinary procurement path.

Corpus does not replace the offer catalog, Artifact Delivery, Room, Inquirium,
or Agent. It composes them:

- topic taxonomy and resolution name the problem space;
- Shared Offer Catalog indexes Corpus-capable `service-offer.v1` records;
- Artifact Delivery carries query/bid/answer envelopes;
- procurement contracts settle selected work;
- Room and Agent provide the implemented node-local live deliberation surface;
  federated transport, remote Room-authority trust, arbiter election, and N-way
  settlement remain later extensions.

The durable output of Corpus reasoning is the signed outcome carried by the existing
answer envelope, together with its traceable provenance. Live room chatter is not a
protocol fact unless another component
explicitly stores it under its own policy.

### Domain and Outcome Boundary

Corpus is domain-general. A technical repair session using an admitted Sensorium
Interface is one optional profile, not the component's defining workflow. The same
coordination contract can serve scientific inquiry, social or mutual-aid problem
solving, creative collaboration such as collective literary work, and other topics;
these examples are illustrative and non-exhaustive.

Corpus owns topic routing, participation, bounded deliberation policy, provenance,
disagreement preservation, and signed outcome formation. Ordinary deliberation on an
arbitrary topic uses the default general-prose mode: bounded plain text or Markdown,
including code fragments, with no domain claim profile. When a consumer instead needs
machine interpretation, adjudication, publication, or effects, an optional namespaced
and versioned thematic profile must own its vocabulary, evidence or critique rules,
success criteria, and accountable policy. The signed outcome carried by the answer
envelope is bounded: depending on the consumer semantics it may carry a synthesis, preserved
alternatives, a recommendation, a hypothesis set, an assistance plan, or a creative
artifact. Its name does not imply one objectively best answer.

The present role and overlay algebra remains closed V1, and operator configuration
may only narrow it; thematic-profile openness does not mint new participant roles.
Operators or communities may propose a thematic profile, but under the current
contract a new namespaced profile requires an explicit Corpus revision and local
receiver resolution. A general profile-admission, lifecycle, and conformance seam is
future work, not an implemented capability claim. The closed boundary governs carrier,
authority, and executable interpretation, not the vocabulary of legitimate topics.

## Context and Problem Statement

Orbiplex already had marketplace procurement, offer catalog projection, Artifact
Delivery, Room, Inquirium, and Agent building blocks. What was missing was the
thin coordination protocol that turns "I need an answer about this topic" into:

1. deterministic topic resolution;
2. provider discovery by topic;
3. bounded query broadcast;
4. signed bid collection;
5. selected procurement;
6. optional live deliberation and signed outcome acceptance.

Without Corpus, each story would have to glue these strata ad hoc, creating
parallel query, topic, room, pricing, and answer semantics.

## Proposed Model / Decision

Corpus is a role plus protocol layer. It is not a separate marketplace
authority and it is not a model runtime.

The hard-MVP path is procurement-oriented:

```text
question keywords
  -> topic-resolution.v1
  -> Shared Offer Catalog topic index
  -> corpus-reasoning-query.v1 over Artifact Delivery
  -> corpus-reasoning-bid.v1 responses
  -> corpus-reasoning-bid-state.v1 requester projection
  -> selected procurement-offer.v1
  -> procurement-contract.v1 / receipt path
```

The post-MVP path adds live deliberation:

```text
selected participants
  -> room.v1 + corpus-reasoning-room-policy.v1
  -> live Room transport
  -> Agent/Inquirium-backed participant reasoning
  -> corpus-reasoning-turn-proposal.v1 through corpus.room.turn
  -> Interaction Broker room-event watch -> chair Agent
  -> corpus-reasoning-answer.v1
```

Corpus wire contracts reuse existing money, procurement, classification,
canonical JSON, and Room conventions. It does not introduce a Corpus-specific
canonicalization profile or a new settlement rail.

The additive Proposal 090 slice will keep offer posture and realized execution
provenance separate. `corpus/model-class` remains a compatibility projection,
not proof of locality. Corpus will consume Shared Offer Catalog posture filters,
then validate and preserve the per-result provenance supplied by Inquirium or
Agent through bids/products, contributions, drafts, signed answers, and
publication candidates.

## Must Implement

### Topic Taxonomy and Resolution

Based on:

- `doc/project/40-proposals/069-corpus.md`

Related schemas:

- `topic-taxonomy.v1`
- `topic-resolution.v1`

Responsibilities:

- define a signed, versioned, federation-scoped taxonomy artifact;
- resolve keywords to a canonical topic term or explicit ambiguity;
- keep resolution deterministic and auditable;
- reject arbitrary topic strings that do not belong to the pinned taxonomy.

Status:

- `done`

### Corpus-Capable Offer Indexing

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md`

Related schemas:

- `service-offer.v1`
- `topic-taxonomy.v1`

Responsibilities:

- treat Corpus provider offers as normal `service-offer.v1` records with a
  Corpus extension;
- index active offers by canonical topic term and taxonomy digest;
- apply supersession, full withdrawal, expiry, and partial-topic removal as
  offer-catalog read-model rules;
- expose topic-index query surfaces without making Corpus a second catalog.

Status:

- `done`

### Query, Bid, and Bid-State Flow

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `corpus-reasoning-query.v1`
- `corpus-reasoning-bid.v1`
- `corpus-reasoning-bid-state.v1`
- `question-envelope.v1`
- `procurement-offer.v1`

Responsibilities:

- send Corpus queries as bounded Artifact Delivery fan-out;
- keep `corpus-reasoning-query.v1` as a decorator over `question-envelope.v1`;
- represent bids as signed envelopes around `procurement-offer.v1`;
- keep requester bid state as a local read model so silence, refusal, policy
  denial, timeout, and delivery failure are not conflated.

Status:

- `done`

### Procurement Bridge

Based on:

- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/069-corpus.md`

Related schemas:

- `procurement-offer.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`

Responsibilities:

- convert a selected Corpus bid into the ordinary procurement contract path;
- keep price, currency, unit, contract, and receipt semantics owned by
  procurement;
- reject counter prices outside the query bracket unless explicitly selected
  by the requester;
- preserve query and correlation identifiers through the settlement path.

Status:

- `done`

### Inference Posture and Result Provenance

Based on:

- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`

Related schemas:

- current `service-offer.v1` and `corpus-reasoning-answer.v1` do not carry the
  Proposal 090 values and are not extended in place;
- `inference-execution-posture.v1` (planned)
- `inference-execution-provenance.v1` (planned)
- a compatible service-offer and answer successor or admitted immutable sidecar
  ref (planned)

Responsibilities:

- route and filter through the offer's signed, extensible pre-execution posture
  with exact assertion owner, offer subject/generation/scope, and processing-
  boundary ref without treating it as a realized fact;
- compare boundaries explicitly and keep unrelated boundaries non-matching or
  `unknown` rather than interpreting another operator's locality as the buyer's;
- keep `corpus/model-class` as a compatibility projection only;
- validate delivered provenance against the selected offer and local buyer or
  Room policy with explicit refuse, quarantine, or warn outcomes;
- preserve or conservatively join provenance through contributions, Agent
  drafts, signed answers, publication candidates, and settlement evidence;
- preserve known non-local or mixed execution when provider identity is
  redacted and treat missing legacy metadata as unknown;
- keep provider refs, domain profiles, evidence policies, and success criteria
  open and locally admitted rather than globally enumerated.

Status:

- `planned`; no current Corpus schema, runtime, or acceptance evidence carries
  the P090 result-level contract end to end.

## May Implement

### Live Deliberation on Room

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/60-solutions/036-room/036-room.md`

Related schemas:

- `room.v1`
- `room-policy.v1`
- `corpus-reasoning-room-policy.v1`
- `corpus-reasoning-room-invite.v1`
- `corpus-reasoning-answer.v1`

Responsibilities:

- open a Room for selected Corpus participants;
- bind deliberation policy, access list, role assignments, and answer
  acceptance to Room records;
- keep live chat ephemeral by default;
- emit a signed, content-addressed answer as the durable reasoning artifact.

Status:

- `done` for the node-local live-deliberation slice: policy, signed invite, AD
  delivery/admission, live WSS join/readiness/messages, metadata-only authority
  projection, exact replay, fixed-high-water paged room recovery, validated
  subject checkpoints, and authority/recipient process recovery are covered.
  Relocatable federated WSS/TLS relay epochs and failover are owned by P070 Phase 6A/6B;
  Matrix remains an optional Room bridge profile. Corpus adds no relay selection,
  NAT traversal, ordering, or carrier authority of its own.

### Agent-Assisted Chairing

Based on:

- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/60-solutions/047-agent/047-agent.md`

Related schemas:

- `agent.binding.v1`
- `agent.binding.v2`
- `agent.outcome.v1`
- `room-membership-attestation.v1`
- `corpus-chair-admission.v1`
- `corpus-agent-answer-draft.accept.request.v1`
- `corpus-agent-answer-draft.v1`
- `corpus-reasoning-role-assignment.v1`
- `corpus-reasoning-instruction-overlay.v1`
- `corpus-reasoning-answer.v1`
- `corpus-reasoning-chair-control-policy.v1`
- `corpus-reasoning-room-policy.v2`
- `room-moderation-intent.v1`
- `room-moderation-audit.v1`

Responsibilities:

- allow the requester to appoint its own bounded Agent as chair delegate;
- resolve requester controls under distributor/operator ceilings and bind the exact
  effective policy to Room policy v2 and Agent binding v2;
- map Corpus voice, kick, ban, and floor vocabulary into generic Room scopes and
  generation-bound intents without teaching `agent-core` Corpus semantics;
- require a pre-existing local Corpus round and signed, fresh Room evidence from
  that round's node-local authority, with a canonical Ed25519 `did:key` signer;
- keep the accountable chair subject explicit in Room policy;
- require local participant or local-policy acceptance before a role assignment
  becomes effective, with the first slice resolving a closed host-owned policy
  catalog;
- keep per-turn instruction-overlay source text inert until a local prompt policy
  accepts it and emits bounded `instruction/rendered`; verify that deterministic
  rendering during recovery and immediately before passing it through Inquirium
  host framing rather than caller metadata or direct adapter prompting;
- persist role and overlay transitions as bounded append-only delta facts and
  recover only sequential, semantically valid revisions;
- let Agent/Inquirium assist reasoning without becoming the authority root;
- admit the terminal Agent product only as an inert, content-addressed Corpus
  answer draft through local-control authority, strict embedded-evidence schema
  validation, and actor-bound idempotent replay, with publication authority fixed
  false;
- accept only text output blocks in the first publication profile and sign the
  bounded outcome carried by the answer envelope under
  `corpus-reasoning-answer-signature.v1`, independently of the artifact schema
  name;
- route sensitive effects through host-owned human-in-loop gates.

Status:

- `done` for the requester-appointed node-local Agent-chair path through locally
  accepted role assignments and instruction overlays, restart-safe append-only
  delta projection, registered policy evaluation, role-aware Inquirium
  operation-scope prompt framing, inert draft acceptance, and separately
  authorized signed answer publication;
- `done` for optional operator-bounded Chair moderation: exact current-policy recovery,
  scoped Room delegation, HIL-gated effects, voice revoke/restore, bounded ban expiry,
  floor-generation invalidation, metadata-only audit, and lifecycle reconciliation.
  Story 011 is the process acceptance consumer; Room's member-visible and sealed
  carrier profiles remain the transport evidence rather than Corpus-local transport
  implementations. Remote Room-authority trust and arbiter election remain post-MVP.

Corpus role policies and instruction overlays are selected through two
Corpus-owned semantic registries. The distribution installs only the closed V1
roles and bounded overlay profiles already defined by Corpus; operator policy may
narrow those sets but cannot mint a role or inject an unregistered overlay. The
daemon checks the selected role and overlay both when a proposal is admitted and
when its decision is applied, preventing a proposal accepted under an older
effective set from remaining executable after a restart-bound policy change.

These registries reuse the shared P085 selection mechanics, while their schemas,
meaning, prompt rendering, chair authority, disclosure rules, and refusal policy
remain owned by Corpus. A namespaced federated extension still requires an
explicit Corpus contract revision and receiver-side resolution evidence.

That federation revision is `corpus-reasoning-room-policy.v3`. It binds an exact
node-signed `node-extension-federation-publication.v1`, declaration digest, and
required Corpus registry entries into the signed invitation. Receiver admission
rechecks peer trust, posture validity, modified-baseline policy, sanctions, and every
domain/ref/revision/implementation/digest tuple against the local Corpus registry.
Unknown, modified, revoked, or locally substituted implementations refuse without
semantic fallback. The persisted invitation read model retains only the bounded
prompt-free local/peer comparison needed for operator inspection and trace.

### Optional Shared Enacted Views — First Technical Thematic Acceptance Profile

Corpus may compose a Room deliberation with an explicitly published Sensorium
Interface, but ordinary Corpus deliberation does not require one. Corpus owns neither
the source, grant, projection, observation runtime, nor actuation. Room membership and
interface authority remain independent, and a shared view never turns prose into an
effect.

[Story 012](../../30-stories/story-012-agents-share-chair-terminal.md) is the first
concrete three-node foundation and first **technical thematic acceptance profile**
above the general-prose mode, not Corpus's defining workflow. Its implementation
composes Workbench, Room, Sensorium Interfaces, Agent's
substrate-neutral observation port, and daemon-owned resolvers while keeping each
authority in its owning layer. The baseline composed-process runner proves independent
participant observation, revocation and audience convergence, dirty recipient restart,
newer-state admission, local-only repair, and an unpublished signed outcome draft.
External host-TLS relay deployment remains P070 evidence rather than a Corpus claim.

The technical evidence lineage is intentionally summarized here; its detailed
contracts, matrices, and retained reports belong to Story 012, P069, P074, and the
owning component proposals:

- the vfkit v2 `single-runtime-vertical` report proves the digest-pinned guest,
  bounded observation, exclusive repair, revocation, restart, stale-generation
  refusal, artifact export, and inert outcome draft through one Workbench runtime;
- the retained 2026-07-24 PowerDNS/Bielik and role-aware reports prove distinct Agent
  products, solver/reviewer turns, terminal-feedback correction, HIL-gated P083
  `claim -> invoke -> release`, exact guest behavior, and zero effects derived from
  Room prose under the `single-host-full-system` evidence boundary;
- the critique-gated successor is `ready`: its retained 2026-07-25 26-check run
  proves Agent-authored CandidatePlan carriage, typed review and Chair gating, one
  failed experiment followed by revision, lease release, and no direct prose effect;
- the model-authored discovery successor has one retained 2026-08-01 30-check run
  using two separately supervised Qwen2.5-Coder 7B runtimes. It removes the closed
  solution template from model-facing inputs and proves a failed experiment followed
  by a distinct successful plan informed by fresh terminal evidence. Repeatable seeded
  success remains open; the ten-pair critique/regeneration bench promoted only one
  successor, below the `0.6` threshold.

The current executable effectful passage admits only `observe_only` and
`local_agent`. `deterministic_host_compiler`, `remote_chair_agent`, and
`designated_participant_agent` remain fail-closed until equivalent passage adapters
have implementation evidence. Every admitted effect rechecks the current Corpus
binding, proposal and passage, exact P083 interface authority, generation, operational
context, method and payload schema, classification, budget, HIL decision, lease,
idempotency, and receipt. No lease spans inference.

Corpus retains an append-only metadata join from proposal and compiled flow node
through Agent binding to the P083 operation and receipt. Exact terminal replay returns
the retained receipt without another effect. Startup converts unfinished
`prepared` or `dispatched` joins to `unknown`, uses bounded recovery pages, and
fails closed on ambiguous, refused, concurrent, or over-budget recovery instead of
reinvoking the target.

The additive v3 correction profile uses the optional structured
`corpus-deliberation-review-claims.v1` envelope. It is a domain-neutral,
provenance-bearing review envelope over opaque claim and next-move references, not
Corpus's universal outcome format and not a mandatory grammar for deliberation. Corpus
validates shape, signatures, exact proposal/plan/terminal bindings, and regeneration
lineage; the admitted profile owns vocabulary, evidence rules, legal claim
combinations, disposition mapping, and accountable adjudication.

The first such consumer, `review-claim-profile:story-012-powerdns-v1`, is a closed
`catalog-select` technical profile over host-projected immutable facts. Ordinary
scientific, social or mutual-aid, creative, or other general-prose deliberation needs
no such profile. If a future consumer requires machine-interpreted evidence,
adjudication, publication, or effects in one of those domains, its specialized
contract needs a separate revision, local admission, and its own readiness evidence.
In particular, creative collaboration need not use a truth-claim review envelope at
all.

The retained 2026-08-31 diagnostic passage
`federation-run:story-012-physical-two-host-three-node-real-model:20260831T193333Z`
completed this first profile over three real model runtimes on two physical hosts.
Four model-authored experiments carried four host-checked typed envelopes with inert
empty commentary and no fallback; the final experiment passed the exact
`a.localdomain`, `b.localdomain`, and `c.localdomain` A-record assertions. The paired
Story report has content SHA-256
`759145ed615bf6d4a823d30b501f655c159456691ee0bbc25f39a063867fe3e7`.
This is technical-profile runtime evidence, not a universal Corpus outcome contract,
not generic domain-profile admission, and not three-physical-failure-domain evidence.

The baseline composed runner's A/B/C loopback addresses and certificate bindings are
multi-address single-host evidence. P074 separately retains both a true
three-physical-host profile and the explicit two-host diagnostic profile described
above. Evidence from the latter preserves its shared `node-b`/`node-c` failure domain
and cannot be promoted to the former. These evidence limitations and the post-MVP
repeatability gaps do not reopen the completed baseline Story 012 gate.

The implemented P082 operational-context extension remains owned by Sensorium
Interfaces. Corpus preserves the exact source context and generation without adding a
TTL or interpreting the context as authority. Superseded, withdrawn, expired, or
generation-mismatched views fail closed; participant hosts apply their own P064 caution
policy before inference.

## Out of Scope

- owning the curated/training `corpus-entry.v1` corpus;
- replacing Room membership, presence, live transport, or attestation;
- replacing Inquirium or Agent runtime semantics;
- defining N-way contribution settlement;
- persisting live deliberation chatter as a protocol fact by default.

## Consumes

- topic taxonomy artifacts;
- Corpus-capable offer catalog projections;
- Artifact Delivery delivery results;
- procurement offer/contract/receipt records;
- Room membership and policy records for post-MVP deliberation;
- signed offer inference-posture characteristics and realized inference
  provenance refs after P090 contract admission.

## Produces

- topic resolution records;
- Corpus query and bid records;
- requester bid-state projections;
- selected procurement bridges;
- Corpus answer records in the live-deliberation layer;
- provenance-preserving Corpus products and answer lineage after P090
  implementation.

## Related Capability Data

- `038-corpus-caps.edn`
