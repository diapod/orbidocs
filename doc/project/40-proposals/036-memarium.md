# Proposal 036: Memarium — Local Memory Organ for the Orbiplex Node

Based on:
- `doc/normative/20-vision/en/VISION.en.md` (Memarium definition, memory spaces)
- `doc/normative/40-constitution/en/CONSTITUTION.en.md` (Art. II.4, V.7 — Memarium as constitutional organ)
- `doc/normative/50-constitutional-ops/en/AUTONOMY-LEVELS.en.md` (memarium.read, memarium.index at A1/A2)
- `doc/project/30-stories/story-003.md` (remote memory preservation)
- `doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md` (archival contract family)
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md` (Agora orthogonality)
- `doc/project/50-requirements/requirements-003.md` (archival handoff requirements)
- `doc/project/60-solutions/node.md` (node-attached roles, archivist/vault handoff)
- `doc/project/60-solutions/SOLUTIONS.en.md` (memarium provider as attached role)

## Status

Draft

## Date

2026-04-14

## Executive Summary

Memarium is the local memory-and-knowledge organ of an Orbiplex Node. Its
constitutional mandate is to "preserve what should not disappear." This proposal
defines Memarium as an in-process Rust crate that participates in the Node's
middleware chain as a first-class `PeerMessageHandler`, giving it observational and
enrichment access to the message pipeline without introducing out-of-process
communication overhead.

The key decisions are:

1. Memarium is an **in-process crate** compiled with the daemon, not a separate
   sidecar process.
2. Memarium participates in the **middleware chain** by implementing
   `PeerMessageHandler`, gaining observation and enrichment capabilities on the
   peer message pipeline.
3. Memarium manages **four constitutionally defined memory spaces** (personal,
   community, public, crisis), each with its own encryption, replication,
   retention, anonymization, and right-to-forget policies.
4. Memarium is the Node's **local public memory**, orthogonal to Agora (remote
   public memory). An Agora client may record outbound submissions and their
   synchronization status as local Memarium facts.
5. Memarium exposes **host capabilities** (`memarium.read`, `memarium.write`,
   `memarium.index`, `memarium.cache`) consumable by agents at autonomy levels
   A1/A2 and by other middleware modules.
6. Memarium stands on the existing **storage trait boundary** (`StorageWrite`,
   `StorageRead`, `StorageReplay`) rather than inventing a parallel persistence
   mechanism.

## Context and Problem Statement

The Orbiplex vision document defines Memarium as "the memory-and-knowledge layer
whose purpose is to preserve what should not disappear." The constitution
(Art. II.4) elevates it to a named organ alongside Agent and Sensorium. Autonomy
level documents reference `memarium.read` and `memarium.index` as routine agent
operations.

Yet no implementation proposal exists. The current Node workspace has:

- a generic storage trait boundary (`storage/src/lib.rs`) with append-only commit
  log semantics, replay, import/export, and opaque payloads,
- storage backends (JSONL commit log, SQLite read model, projector, runtime),
- archival contract proposals (`ArchivalPackage`, `ArchivistAdvertisement`,
  `RetrievalRequest/Response`) in draft status,
- a middleware chain (`PeerMessageChain`) with `PreInput`, `InboundPeer`,
  `PreSend`, and `Audit` phases driven by `PeerMessageHandler` trait objects,
- Agora (proposal 035) as a topic-addressed record relay for remote public
  records.

What is missing:

- a domain layer that maps the four constitutionally defined memory spaces onto
  the storage boundary with space-specific policies,
- host capabilities for agents and middleware to read, write, index, and cache
  knowledge artifacts,
- chain participation that lets Memarium observe and enrich the peer message
  pipeline,
- a local record of Agora-bound submissions and their synchronization status,
- crisis space management as a constitutional duty.

## Goals

- Define Memarium as a full L2 organ with a clear trait boundary and runtime.
- Map the four memory spaces onto the existing storage boundary with explicit
  policy contracts.
- Integrate Memarium into the middleware chain as an in-process chain participant.
- Define host capabilities for agent and middleware consumption.
- Establish the Memarium-Agora relationship: local memory with optional remote
  publication tracking.
- Specify crisis space obligations and availability guarantees.

## Non-Goals

- This proposal does not define federated Memarium replication between nodes.
  That is future work once the local organ is stable.
- This proposal does not define the full curation or training pipeline. Those are
  downstream consumers of Memarium artifacts.
- This proposal does not require a specific full-text search or vector index
  implementation. Indexing strategy is a runtime concern.
- This proposal does not freeze the archival contract schemas; it builds on them
  as currently proposed.

## Decision

### 1. In-Process Crate, Not Sidecar

Memarium is implemented as Rust crates compiled into the daemon binary:

- `memarium` — trait boundary, domain types, space policies, capability contracts
- `memarium-runtime` — default implementation over `StorageRuntime`

Rationale:

- Memarium is a constitutional organ, not an optional plugin. If the daemon is
  alive, Memarium must be alive. An out-of-process deployment adds a failure
  point to a component that has crisis-space obligations.
- Agents at A1/A2 perform `memarium.read` routinely within budgets. In-process
  calls avoid JSON serialization overhead on every read.
- The storage boundary (`StorageWrite`/`StorageRead`) is already in-process.
  Memarium adds a domain layer on top without duplicating persistence.
- The middleware chain's `PeerMessageHandler` trait is transport-agnostic. An
  in-process implementation is a first-class chain participant alongside
  out-of-process HTTP-backed handlers.

### 2. Middleware Chain Participation

Memarium integrates with the middleware chain through **observer slots** and an
optional **chain handler**, not through the main dispatch pipeline.

#### 2.1. Post-Chain Observation

Memarium participates in post-chain observation through a daemon-side adapter
(see proposal 027). The daemon owns the `PostChainObserver` trait and
`PostChainEvent` shape; `memarium-runtime` exposes the Memarium-domain
`observe_dispatch(message_kind, correlation_id, effective_payload)` entry point.
The adapter is invoked once per dispatch, after all chain phases complete
(including send, when a response was produced). At the daemon layer it can see:

- `input_payload` — the original envelope before any handler mutations,
- `effective_payload` — the envelope after all chain mutations,
- `response` — the response envelope (if any), after `pre-send` mutations,
- `outcome` — final dispatch outcome (`completed`, `handled`, `responded`,
  `dropped`, `unhandled`),
- `handler_id` — which handler claimed the message (when applicable),
- `message_kind`, `remote_node_id`, `correlation_id`, `elapsed`.

This is the primary integration point for fact recording. The daemon adapter
passes the Memarium-relevant slice of the event into the runtime, so Memarium
sees **what actually happened** (the effective payload, including modifications
by other middleware), not just what was originally submitted. This means
middleware that runs earlier in the chain (e.g. Agora on `PreInput` or
`InboundPeer`) can modify or annotate a message, and Memarium records the
modified version without depending on daemon-private dispatch types.

Future note: if the observation contract needs to grow beyond the current
`observe_dispatch(message_kind, correlation_id, effective_payload)` arguments,
the runtime-side abstraction should be a Memarium-domain value such as
`MemariumObservation`, not the daemon-private `PostChainObserver` or
`PostChainEvent`. `PostChainObserver` remains a daemon adapter concern;
`MemariumObservation` would be the stable semantic input understood by
`memarium-runtime`.

#### 2.2. Deklaratywne observe rules

Memarium does not hardcode which message types are worth remembering. Instead,
**each middleware declares what is a fact worth remembering** through a
`memarium` section in its own configuration.

Example: Agora declares in its config that `agora-record.v1` messages are
Agora-submission facts for the public space:

```json
{
  "agora": {
    "memarium": {
      "observe": [
        {
          "message_types": ["agora-record.v1"],
          "fact_kind": "agora-submission",
          "space": "public",
          "extract": {
            "topic": "payload.topic/key",
            "record_id": "payload.record/id",
            "content_hash": "payload.content/hash"
          }
        }
      ]
    }
  }
}
```

The daemon's existing configuration merge strategy (`deep_merge(factory_config,
node_config)`) naturally combines `memarium` sections from all middleware
configs into one effective observe rule set. Memarium compiles these rules at
startup, just as the daemon compiles `Predicate` filters for middleware
dispatch.

At runtime, when a post-chain observer event arrives:

1. match `message_kind` against compiled `message_types`,
2. optionally evaluate a `condition` predicate,
3. extract fields from the **effective payload** using declared paths,
4. build a `MemariumFact` with the declared `fact_kind` and `space`,
5. append to the target space.

This design has three consequences:

- **Memarium knows no semantics.** It is a fact-recording machine driven by
  data. Adding a new middleware that wants facts recorded requires zero changes
  to Memarium.
- **Middleware is the semantic expert.** Agora knows that `agora-record.v1` on
  topic X is worth remembering. Dator knows that `service-offer.v1` is worth
  tracking. Each module defines this at its own boundary.
- **The operator has control.** Node config can override any middleware's
  `memarium` section: disable observation, add new types, change target space.
  Standard `deep_merge` semantics apply.

#### 2.3. Phase Observers (optional)

For fine-grained observation, Memarium may also register as a **phase observer**
on specific chain phases (`pre-input`, `inbound-peer`, `pre-send`). Phase
observers are invoked after each phase completes — including when a handler
caused an early exit. They receive the input and effective envelopes for that
phase, plus the phase outcome and claiming handler identity.

Phase observers are optional in MVP. The post-chain observer covers the primary
use case (recording what happened). Phase observers add visibility into *where*
in the pipeline mutations occurred.

#### 2.4. PreInput Chain Handler — `MemariumContextEnricher` (optional)

Registers on the `PreInput` chain as a standard `PeerMessageHandler`. Before
inbound messages reach domain handlers, Memarium may annotate or enrich the
message context with cached knowledge artifacts relevant to the message type or
topic.

Returns `Passthrough` or `Annotate` (enrich context without modifying
payload). Never blocks or drops.

This handler is optional in MVP and may be deferred until agent integration
matures.

#### 2.5. What Memarium Does NOT Do in the Chain

- Does not implement `ServiceDispatchExecute`. Memarium is not a service
  processor; it does not handle work orders.
- Does not return `Drop`, `Reject`, `Return`, `Rewrite`, or `Respond` from any
  handler position. Memarium observes and enriches; it does not gate or mutate
  the pipeline.
- Does not participate as a handler in `InboundPeer`, `InboundBroadcast`,
  `InboundLocal`, or `PreSend` chains. Its handler surface is minimal: PreInput
  (optional enrichment only). Its observation surface is post-chain observer
  (always) and optionally per-phase observers.

### 3. Four Memory Spaces

Each memory space is a policy-governed domain partition within Memarium's storage
layer. Spaces are not separate databases; they are policy envelopes over the
shared storage boundary.

#### 3.1. Space Definitions

| Space | Purpose | Encryption | Replication | Retention | Right to Forget |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Personal** | Notes, world models, private idiolect, personal knowledge artifacts | Mandatory, operator-held key | Never leaves node without explicit export | Operator-controlled | Immediate on operator request |
| **Community** | Survival guides, legal knowledge, first-contact protocols, shared group knowledge | Mandatory, group-held key | Federated among trusted peers (future) | Group policy | Group-governed procedure |
| **Public** | Culture, texts, recordings, maps, libraries, Agora sync status | Optional (integrity-only by default) | May use Agora as remote substrate | Policy-controlled, defaults to durable | Tombstone with trace |
| **Crisis** | Emergency caches, triage procedures, survival knowledge, escape kits | Mandatory, operator-held key | Explicit crisis-replication policy | Constitutional minimum: must not expire without operator action | Restricted: crisis material persists unless operator overrides |

#### 3.2. Space as Policy Envelope

A `MemariumSpace` is not a storage backend; it is a typed policy contract:

```
MemariumSpace {
    space_id:          SpaceId,          // personal | community | public | crisis
    encryption_policy: EncryptionPolicy, // mandatory | optional | integrity-only
    replication_scope: ReplicationScope, // local-only | federated | agora-eligible
    retention_policy:  RetentionPolicy,  // operator | group | constitutional-minimum
    forget_policy:     ForgetPolicy,     // immediate | governed | tombstone | restricted
}
```

The storage layer sees opaque `StreamId` values. Memarium maps
`(SpaceId, artifact_kind)` to stream naming conventions and attaches policy
metadata through `RecordMetadata.policy_refs` and `RecordMetadata.attributes`.

#### 3.3. Space Boundaries Are Enforcement Points

Cross-space operations (e.g., promoting a personal artifact to community or
public) are explicit transitions with policy checks. A personal artifact does not
become public by accident. Promotion requires:

- explicit operator or agent action with sufficient autonomy level,
- policy validation at the target space boundary,
- a new Memarium fact recording the promotion with provenance.

### 4. Domain Types

#### 4.1. `MemariumEntry`

The unit of knowledge stored in Memarium. This is an internal domain type, not
the public wire schema:

```
MemariumEntry {
    id:            EntryId,
    space:         SpaceId,
    artifact_kind: ArtifactKind,       // knowledge-artifact | learning-outcome |
                                       // agora-sync-record | archival-receipt |
                                       // crisis-procedure | free-form-note | ...
    tags:          Vec<Tag>,
    classification: Classification,    // classification.v1 source/effective label
    payload:       PayloadEnvelope,    // opaque body, explicit encoding/encryption envelope
    attributes:    Map<String, String>,// filterable/indexable metadata
    occurred_at:   Timestamp,          // domain time
    recorded_at:   Option<Timestamp>,  // storage acceptance time
}
```

Entries are immutable facts. Updates are new entries with provenance links to
prior entries. `classification.source_tier` is stamped at write/ingress time and
is immutable; declassification is represented by append-only policy facts and a
derived read view, not by rewriting the entry.

The entry payload is normalized before storage:

```
PayloadEnvelope {
    encoding:   PayloadEncoding,        // plaintext-json | sealed-json-v1 | sealed-bytes-v1
    media_type: Option<String>,
    body:       JsonValue,
    encryption: Option<EncryptionEnvelope>,
}
```

Earlier sketches placed `content_hash` and `provenance` directly on
`MemariumEntry`. MVP keeps those concerns stratified:

- content hashing belongs below or beside the Memarium domain contract until a
  canonical digest policy is defined for plaintext bodies, sealed envelopes,
  storage records, and higher-level artifacts;
- entry provenance is represented through attributes such as `source/entry-id`,
  `source/space`, and `promotion/reason`, or through a future provenance
  envelope once multiple concrete provenance modes justify it.

#### 4.2. `MemariumFact`

A lightweight record of an observed event relevant to memory. This is an
internal domain type, not the public wire schema:

```
MemariumFact {
    id:                    FactId,
    space:                 SpaceId,
    fact_kind:             FactKind,     // agora-submission | sync-confirmed |
                                         // archival-handoff | promotion |
                                         // agent-read | agent-cache-miss | ...
    tags:                  Vec<Tag>,
    classification:        Classification,
    fields:                Map<String, JsonValue>,
    source_message_kind:   Option<String>,
    source_correlation_id: Option<String>,
    recorded_at:           Timestamp,
}
```

Facts are the primary output of the post-chain observer. When a dispatch event
matches a compiled observe rule, Memarium builds a `MemariumFact` from the
extracted fields and appends it to the declared space. For example, Agora's
observe rule for `agora-record.v1` produces a fact of kind `agora-submission`
in the public space with topic, record id, and content hash extracted from the
effective payload.

Subsequent events (relay confirmation, failure, timeout) produce follow-up facts
(`sync-confirmed`, `sync-failed`, `sync-timeout`). No entry is mutated; the
current status is derived from the latest fact in the chain.

Like entries, facts carry first-class `classification.v1` labels. The label is
not stored inside `fields`; `fields` remain fact-kind-specific open-world data.
During the compatibility window, unlabeled producers may be stamped as
`Personal` with ingress quarantine, but the stable direction is explicit
classification on every write path.

Earlier sketches used top-level `subject` and `detail` fields. MVP represents
those concepts through fact-kind-specific `fields`: an entry-related fact may
carry `entry_id`, while an Agora fact may carry `topic`, `record_id`, and
`content_hash`. `source_message_kind` and `source_correlation_id` record the
minimal observer provenance without forcing every fact into an entry-subject
shape.

#### 4.3. `MemariumIndex`

An eventually-consistent read model derived from entries and facts:

```
MemariumIndex {
    space:           SpaceId,
    entry_count:     u64,
    last_updated_at: Timestamp,
    // Backend-specific index structures (tags, full-text, semantic)
    // are runtime concerns, not protocol contracts.
}
```

The index is a projection, not a source of truth. It can be rebuilt from the
commit log at any time.

### 5. Host Capabilities

Memarium exposes the following capabilities to agents and middleware through the
daemon's host capability surface:

| Capability | Autonomy | Description |
| :--- | :--- | :--- |
| `memarium.read` | A1+ | Read entries by id, by tag, by artifact kind, within a space. Returns matching entries respecting space policy. |
| `memarium.write` | A1+ | Append a new entry to a space. Subject to space policy validation. |
| `memarium.index` | A2+ | Query the index for entry counts, tag distributions, recent activity within a space. |
| `memarium.cache` | A1+ | Read-through cache: attempt index lookup, fall back to full scan, cache result. |
| `memarium.promote` | A0 | Promote an entry from one space to another. Requires operator approval by default (A0) because it crosses policy boundaries. |
| `memarium.forget` | contextual | Request right-to-forget on an entry. The required autonomy depends on space, outcome, and caller authority: personal immediate forget may be delegated through tightly scoped passports; public tombstone and shared-memory forget requests require operator approval or governed workflow; crisis forget is restricted. |
| `memarium.declassify` | A0 | Append a declassification/quarantine policy fact. Declassification never rewrites the source fact; it is authorized through `memarium-declassify@v1`, bound by space, surface, topic class, mode, and tier transition. |

These capabilities are registered through the same host capability binding
mechanism used by middleware modules (`/v1/host/capabilities/memarium.*`).
In-process callers (agents, NSE hooks) invoke them directly through trait
methods; out-of-process callers (middleware modules) invoke them through the
existing host capability HTTP surface.

For `memarium.forget`, "operator approval" may later be represented as a
remembered operator decision rather than a one-click prompt for every request.
For example, the operator may allow a participant, agent, or module to forget a
bounded class of entries by default: one participant's personal entries, one
artifact kind, one memory class (`personal`, `community`, `public`), or a wider
scope explicitly accepted by the operator. Such remembered approvals are policy
facts with scope, reason, issuer, and revocation path; they do not let an agent
self-escalate beyond its contract.

### 6. Memarium-Agora Relationship

Agora is remote public memory (a topic-addressed record relay operated by
umbrella operators). Memarium is local memory of the Node.

Their relationship:

1. **Agora does not depend on Memarium.** A node may operate Agora without
   Memarium, and vice versa.
2. **Memarium records Agora-bound submissions through observe rules.** Agora
   declares in its configuration which message types are facts worth
   remembering. Memarium's post-chain observer matches these rules against
   dispatch events and records `MemariumFact` entries in the public space.
   Memarium itself has no knowledge of Agora semantics.
3. **Memarium tracks synchronization status.** Confirmation or failure of Agora
   relay acceptance is recorded as subsequent facts (`sync-confirmed`,
   `sync-failed`, `sync-timeout`) through additional observe rules. The current
   status of an Agora-bound entry is derived from the latest fact in the chain.
4. **Memarium is the local cache of what the node contributed to Agora.**
   An agent can query Memarium for "what did I submit to topic X?" without
   querying the remote relay.
5. **Agora is one possible substrate for Memarium's public space**, but not
   the only one. Memarium may also use direct peer replication, archivist
   handoff, or local-only retention for public artifacts.

### 7. Archival Integration

Memarium integrates with the archival contract family (proposal 012) as follows:

1. `LearningOutcome` from room correction flows may be promoted to
   `KnowledgeArtifact` and stored as a `MemariumEntry` in the appropriate space.
2. When an entry is selected for archival handoff, Memarium records the
   `ArchivalPackage` preparation as a fact and the handoff result
   (`StorageConfirmation`) as a subsequent fact.
3. `ArchivistAdvertisement` records received from peer archivists may be cached
   in the community or public space for later archivist selection.
4. `RetrievalRequest`/`RetrievalResponse` for previously archived material may
   be served from Memarium's local cache when available, avoiding redundant
   remote retrieval.

### 8. Crisis Space Obligations

The constitution (Art. V.7) states that Memarium may maintain crisis spaces and
emergency caches if they serve to protect people. This proposal treats the crisis
space as a constitutional obligation, not an optional feature:

1. Crisis entries have a constitutional minimum retention: they must not expire
   without explicit operator action.
2. Crisis space encryption uses operator-held keys, not group keys. In a crisis,
   the operator must be able to access the material without group consensus.
3. Crisis replication policy is explicit and separate from general federation
   replication. A node may replicate crisis material to designated crisis peers
   without general federation membership.
4. Crisis procedures (triage, shelter info, legal contacts, escape kits) are
   pre-populated from a constitutional seed set and updated through explicit
   operator or federation action.

### 9. Crate Boundary

#### `memarium` crate

Defines:
- `MemariumSpace`, `SpaceId`, policy types
- `MemariumEntry`, `EntryId`, `ArtifactKind`
- `MemariumFact`, `FactId`, `FactKind`
- `MemariumRead` trait (query entries, facts, index)
- `MemariumWrite` trait (append entries, record facts)
- `MemariumIndex` trait (query projections)
- `MemariumError` error model
- Host capability request/response types

Does not depend on storage backend crates.

#### `memarium-runtime` crate

Implements:
- `MemariumRead`, `MemariumWrite`, `MemariumIndex` over `StorageRuntime`
- Space-to-stream mapping and policy enforcement
- `MemariumRuntime::observe_dispatch(...)` as the neutral post-chain observation
  port over Memarium-domain data
- `ObserveRuleCompiler` — compiles observe rules from merged middleware config
- optional `MemariumContextEnricher` semantics over Memarium-domain input
  (daemon-side chain adapters remain outside this crate)
- Index projection from commit log (via `storage-projector` patterns)

Depends on: `memarium`, `storage`, `storage-runtime`. It does not depend on the
daemon crate or daemon-private peer-message chain traits.

#### `daemon` integration layer

Implements:
- `MemariumPostChainAdapter` implementing the daemon-private
  `PostChainObserver` trait
- mapping from `PostChainEvent` to
  `MemariumRuntime::observe_dispatch(message_kind, correlation_id,
  effective_payload)`
- runtime construction from effective daemon/middleware config

Depends on: `memarium`, `memarium-runtime`, `storage-runtime`, and daemon-private
peer-message chain types.

The post-chain adapter is daemon-side because `PostChainEvent` and
`PostChainObserver` are daemon-private peer-message types. Hosting the adapter in
`memarium-runtime` would force the runtime crate to take a dependency on daemon
internals, violating the stratification contract: the L2 runtime does not depend
on L3 daemon types.

## Proposed Crate Layout

```
node/
  memarium/
    Cargo.toml
    src/
      lib.rs          -- trait boundary, domain types, policy contracts,
                         ObserveRule, ObserveRuleSet
  memarium-runtime/
    Cargo.toml
    src/
      lib.rs          -- runtime implementation and observe_dispatch port
      compiler.rs     -- ObserveRuleCompiler (config → compiled rules), if split out
      enricher.rs     -- future Memarium-domain enrichment semantics, if needed
      projection.rs   -- index projection from commit log
    tests/
      ...
  daemon/
    src/
      memarium_adapter.rs -- daemon-side PostChainObserver adapter:
                            PostChainEvent → MemariumRuntime::observe_dispatch(...)
```

## Design Principles

1. **Facts over state**: Memarium stores immutable facts and entries. Status is
   derived from the latest fact in a chain, not from mutable state.
2. **Spaces are policy, not storage**: All four spaces share the storage
   boundary. Spaces are enforcement envelopes that govern what happens to data,
   not where it physically lives.
3. **Observation through observer slots, not dispatch handlers**: Memarium uses
   post-chain and per-phase observer slots that are invoked unconditionally,
   regardless of handler short-circuits. It does not participate in dispatch
   decisions.
4. **Declarative observe rules, not hardcoded semantics**: Memarium does not
   know what is worth remembering. Each middleware declares its own observe
   rules. Memarium compiles and executes them. This eliminates coupling between
   the memory organ and the semantic modules it observes.
5. **Agora orthogonality preserved**: Memarium does not depend on Agora. Agora
   does not depend on Memarium. Agora declares observe rules in its config;
   Memarium executes them without Agora-specific knowledge.
6. **Crisis is a duty, not a feature**: Crisis space has constitutional retention
   guarantees. It is not gated behind configuration or feature flags.

## Trade-offs

1. **In-process vs. out-of-process**:
   - Benefit: zero serialization overhead, guaranteed co-lifecycle with daemon,
     direct storage access.
   - Cost: Memarium is coupled to the Rust toolchain and daemon binary. A future
     operator who wants a non-Rust Memarium provider would need to introduce a
     proxy layer.
   - Mitigation: the trait boundary is thin and transport-agnostic. A future
     `MemariumHttpProxy` implementing the same traits is straightforward.

2. **Observer slots vs. dedicated API only**:
   - Benefit: Memarium sees the full message flow, including effective payloads
     after middleware mutations, without explicit notification plumbing.
   - Cost: Memarium depends on the observer slot contract and chain lifecycle.
   - Mitigation: Observers are fire-and-forget with no influence on dispatch.
     The coupling is observational, not decisional.

3. **Declarative observe rules vs. hardcoded fact recording**:
   - Benefit: zero coupling between Memarium and middleware semantics. Adding
     a new middleware that wants facts recorded requires no Memarium changes.
   - Cost: more configuration surface; observe rules must be validated at
     startup.
   - Mitigation: rule compilation is one-time at startup; the rule contract
     is small (message types, fact kind, space, extract paths, optional
     condition).

3. **Four spaces with policies vs. one flat store**:
   - Benefit: constitutionally correct, explicit enforcement boundaries, clear
     audit semantics.
   - Cost: more validation surface, policy management complexity.
   - Mitigation: spaces share one storage boundary; the overhead is in policy
     checks, not in storage duplication.

4. **Facts-over-state vs. mutable status fields**:
   - Benefit: append-only semantics, full audit trail, "as of" queries, no lost
     updates.
   - Cost: deriving current status requires scanning fact chain (mitigated by
     index projection).
   - Mitigation: `MemariumIndex` is a projection that caches derived state.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
| :--- | :--- | :--- |
| Storage backend unavailable | Memarium cannot record facts or entries | Daemon enters degraded state; Memarium audit observer logs warnings but does not block pipeline (Audit is fire-and-forget). |
| Index projection falls behind commit log | Stale query results from `memarium.index` and `memarium.cache` | Index staleness is visible; consumers may fall back to direct scan. Projection catch-up is automatic on recovery. |
| Crisis entries accidentally deleted by operator | Loss of constitutional-minimum material | Forget policy for crisis space is `restricted`; deletion requires explicit constitutional override, not standard forget flow. |
| Personal entry promoted to public without operator consent | Privacy breach | Promotion requires A0 (operator approval). Cross-space promotion is never automatic. |
| Agora sync fact chain diverges from actual relay state | Node believes submission succeeded when it failed, or vice versa | Periodic reconciliation: agent may compare local sync facts against Agora relay query results and record correction facts. |
| Post-chain observer adds latency to message pipeline | Degraded peer message throughput | Observers are fire-and-forget by design. Writes are asynchronous appends to the commit log. |
| Observe rule extract path references a missing field | Fact recorded with incomplete fields | Extract paths that resolve to `null` are preserved as explicit `null` in the fact fields. Rule compilation validates path syntax at startup; missing runtime values are not errors. |
| Middleware config declares observe rule for non-existent space | Rule rejected at startup | Observe rule compiler validates space ids against the known space set and rejects unknown spaces with a startup warning. |

## Open Questions

1. Should `MemariumContextEnricher` (PreInput) be part of the MVP, or deferred
   until agent integration patterns stabilize?
2. What is the minimal crisis seed set that must be pre-populated on first node
   start?
3. Should community space group keys be managed by Memarium or by a separate
   key management component?
4. What reconciliation frequency is appropriate for Agora sync fact chains?
5. Should selected `MemariumFact.fields` maps gain structured validation schemas
   per `FactKind`, or remain open JSON maps throughout v1?
6. What is the right granularity for `ArtifactKind`? Should it be an open enum
   or a closed set in v1?
7. Should observe rules support extract path expressions beyond simple
   `payload.field` dot-paths (e.g. array indexing, conditional extraction)?
8. Should observer slots be implementable by out-of-process modules in MVP, or
   only by in-process trait implementations? (The contract supports both, but
   the fire-and-forget loopback dispatch path is additional work.)

## Next Actions

1. Implement observer slot infrastructure in daemon (post-chain + per-phase).
2. Add v1 Rust trait boundary in `memarium/src/lib.rs`.
3. Add v1 runtime implementation in `memarium-runtime/src/lib.rs`.
4. Implement the daemon-side `MemariumPostChainAdapter` and runtime
   `ObserveRuleCompiler`.
5. Add host capability routes (`memarium.read`, `memarium.write`,
   `memarium.index`, `memarium.cache`) to daemon control plane.
6. Add `memarium` config section support to middleware config merge.
7. Add crisis space seed population on first node start.
8. Add integration tests: entry lifecycle, fact chain derivation, space policy
   enforcement, cross-space promotion, observe rule compilation and matching.
9. Add example observe rules to Agora middleware config.
10. Update `node/docs/implementation-ledger.toml` with Memarium capability rows.
11. Align self-custody defaults with proposal 040 §4: a node's Memarium MUST
    by default retain, indefinitely, the envelopes of its own participant's
    own Agora-published records, so that proposal 040's custodial
    redelivery pattern has a guaranteed byte-identical source. Operator
    override is allowed but must be explicit.
12. Expose a memarium-to-memarium transfer endpoint for the custody flow
    defined in proposal 040 §3, honoring the `memarium.custody`
    capability-passport scope and preserving encrypted payloads as opaque
    bytes.
