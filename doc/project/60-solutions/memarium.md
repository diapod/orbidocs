# Orbiplex Memarium

`Orbiplex Memarium` is the local memory-and-knowledge organ of an Orbiplex Node. Its constitutional mandate is to "preserve what should not disappear." Memarium manages four constitutionally defined memory spaces (personal, community, public, crisis) with space-specific policies for encryption, replication, retention, anonymization, and right-to-forget.

Memarium is an in-process Rust crate compiled with the daemon. It participates in the Node's middleware chain as a first-class `PeerMessageHandler`, gaining observational and enrichment access to the peer message pipeline. It stands on the existing storage trait boundary rather than inventing a parallel persistence mechanism.

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
- `todo`

### Observer-Based Chain Integration

Based on:
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md` (chain architecture, observer slots)
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- implement `MemariumPostChainObserver` as a post-chain observer that sees the effective payload (after all middleware mutations), the response, and the dispatch outcome,
- compile deklaratywne observe rules from merged middleware configuration at startup,
- match post-chain observer events against compiled rules and record `MemariumFact` entries in the declared space with extracted fields,
- optionally register as per-phase observer for fine-grained visibility into where mutations occurred,
- optionally implement `PeerMessageHandler` as `MemariumContextEnricher` on the `PreInput` chain to annotate inbound messages with cached knowledge artifacts,
- never block, drop, reject, or mutate peer messages from any chain or observer position.

The observers and handlers are in-process trait implementations compiled into the daemon. They do not use loopback HTTP and share the same `StorageRuntime` as the rest of the daemon. This follows the trait-pipeline architecture documented in proposal 027 and the middleware README.

Status:
- `todo`

### Declarative Observe Rules

Based on:
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- define an `ObserveRule` contract specifying: message types, fact kind, target space, field extraction paths, optional condition predicate, enabled flag,
- compile observe rules from the `memarium` section of each middleware's configuration, merged through the daemon's standard `deep_merge(factory_config, node_config)` strategy,
- validate rules at startup: reject unknown space ids, validate extract path syntax, warn on unreachable rules,
- support operator overrides: node config can disable, modify, or add observe rules for any middleware.

Each middleware is the semantic expert for its own domain. Agora declares that `agora-record.v1` messages are `agora-submission` facts in the public space. Dator declares that `service-offer.v1` messages are offer-tracking facts. Memarium compiles and executes these rules without domain-specific knowledge.

Status:
- `todo`

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

Responsibilities:
- expose `memarium.read` (A1+): query entries by id, tag, artifact kind, within a space,
- expose `memarium.write` (A1+): append new entries subject to space policy validation,
- expose `memarium.index` (A2+): query index projections for entry counts, tag distributions, recent activity,
- expose `memarium.cache` (A1+): read-through cache with index lookup fallback to full scan,
- expose `memarium.promote` (A0): cross-space promotion requiring operator approval,
- expose `memarium.forget` (A0): right-to-forget requests subject to space forget policy,
- register capabilities through the daemon's host capability binding mechanism,
- serve in-process callers (agents, NSE hooks) through direct trait methods and out-of-process callers (middleware modules) through the host capability HTTP surface.

Status:
- `todo`

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
- `todo`

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

Responsibilities:
- enforce constitutional minimum retention for crisis entries (must not expire without explicit operator action),
- use operator-held encryption keys for crisis material (accessible without group consensus),
- maintain explicit crisis replication policy separate from general federation replication,
- pre-populate crisis procedures from a constitutional seed set on first node start,
- support updates through explicit operator or federation action only.

Status:
- `todo`

## May Implement

### Context Enrichment (PreInput)

Based on:
- `doc/project/40-proposals/036-memarium.md`

Responsibilities:
- implement `PeerMessageHandler` on the `PreInput` chain to annotate inbound messages with cached knowledge artifacts relevant to the message type or topic,
- return `Allow` (passthrough) or `Annotate` (enrich context without modifying payload),
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

## Consumes

- `learning-outcome.v1`
- `knowledge-artifact.v1`
- `archivist-advertisement.v1`
- `retrieval-response.v1`
- Post-chain observer events (effective payloads after middleware mutations)
- Declarative observe rules from middleware configuration sections

## Produces

- `MemariumEntry` (internal domain type, not a wire schema)
- `MemariumFact` (internal domain type, not a wire schema)
- Host capability responses for `memarium.read`, `memarium.write`, `memarium.index`, `memarium.cache`

## Related Capability Data

- `memarium.read` — read entries within a space (A1+)
- `memarium.write` — append entries to a space (A1+)
- `memarium.index` — query index projections (A2+)
- `memarium.cache` — read-through cache (A1+)
- `memarium.promote` — cross-space promotion (A0)
- `memarium.forget` — right-to-forget request (A0)

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
- `MemariumPostChainObserver` — post-chain observer driven by compiled observe rules
- `ObserveRuleCompiler` — compiles observe rules from merged middleware config
- `MemariumContextEnricher` implementing `PeerMessageHandler` for the `PreInput` chain (optional)
- Index projection from commit log

Depends on: `memarium`, `storage`, `storage-runtime`, `middleware`.

## Notes

Memarium is a constitutional organ at layer L2 in the system stratification (L0: Node, L1: Agent, L2: Memarium, L3: Swarm Protocol). Its implementation as an in-process crate reflects the constitutional requirement for co-lifecycle with the daemon and the operational requirement for low-latency agent access.

The chain integration follows the observer slot pattern (proposal 027): Memarium registers as a post-chain observer that sees effective payloads after all middleware mutations, not as a dispatch handler. Fact recording is driven by declarative observe rules declared by each middleware in its own configuration, merged through the daemon's standard deep-merge strategy. This eliminates coupling between the memory organ and the semantic modules it observes.

Implementation-specific decomposition, file ownership, and delivery status belong in the concrete Node repository's implementation ledger.

Implementation-specific decomposition, file ownership, and delivery status belong in the concrete Node repository's implementation ledger.
