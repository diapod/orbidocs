# Proposal 074: Multi-Node Federation Harness and Trace Explorer

Based on:

- `doc/project/30-stories/story-000-node-handshake.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/30-stories/story-011-corpus-fish.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/056-orbiplex-tls-trust-policy.md`
- `doc/project/40-proposals/060-messaging-middleware.md`
- `doc/project/40-proposals/062-temporal-storage-convention.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `node/tools/acceptance/README.md`

## Status

Draft

## Date

2026-06-26

## Executive Summary

Orbiplex already has the primitives needed for federated auditability:
canonical JSON digests, temporal event logs, capability passports, query
attestations, Seed Directory replay, Artifact Delivery, INAC, Room, Messaging,
Corpus, Matrix carriers, and per-story acceptance tooling.

What is missing is a common consumer for those primitives:

1. a hermetic **multi-node federation harness** that can bring up a local
   N-node network in CI and exercise federated flows without relying on
   production-like manual setup;
2. a read-only **trace explorer** that can collect node-local evidence from
   multiple data directories and render one causal timeline across nodes,
   transports, attestations, artifacts, and storage logs.

Without this layer, the project risks testing federation mostly through
story-specific scripts, manual inspection, or production incidents. This
proposal defines a stratified harness and trace explorer that treat existing
node stores as sources of truth and build a diagnostic read model over them.

The harness is not a new runtime authority, scheduler, or federation control
plane. It is a test and diagnostic tool. The trace explorer is not a source of
truth. It is a redaction-aware projection over already committed facts.

## Context and Problem Statement

The Vision speaks about a global network of nodes. The stories already exercise
federated scenarios:

- Story 000 covers baseline node handshake.
- Story 005 exercises multi-node Whisper and service execution.
- Story 010 exercises contactability, Contact Catalog, Messaging, INAC, and
  private delivery.
- Story 011 exercises Corpus procurement, topic taxonomies, Seed Directory, and
  multi-node answer production.

The implementation also contains the required low-level seams:

- `node/tools/acceptance/*` contains per-story local profile runners;
- `node/tools/matrix-fixture` can provide a local Matrix test fixture;
- `node/xtask trace-delivery` already contains a focused trace collector for
  Messaging, Artifact Delivery, and INAC;
- `temporal-event-log` provides reusable transaction/event/replay mechanics;
- operator storage diagnostics expose temporal status, events, correlation, and
  replay checks for selected stores.

These are valuable, but they remain fragmented. A story script knows how to run
one scenario. A temporal store knows its own events. An Artifact Delivery ledger
knows one delivery. A Room projection knows one room. The operator still lacks
one bounded way to answer:

> What happened across the participating nodes, in what causal order, with which
> artifacts, attestations, passports, decisions, retries, refusals, and
> transport hops?

The absence of that view makes distributed debugging too late and too local.
For federation, "works on one node" is not enough.

## Goals

- Provide a declarative N-node local federation harness usable in CI and by
  operators/developers.
- Reuse existing story acceptance knowledge instead of replacing it with a
  parallel framework.
- Build one normalized trace event model over existing node-local audit stores,
  ledgers, attestations, and protocol records.
- Render a partial-order causal timeline, not a fake total global clock.
- Export redaction-aware trace bundles that can be attached to bug reports or
  operator support workflows without leaking raw payloads by default.
- Make federation failures reproducible before production deployment.

## Non-Goals

- Not a production federation orchestrator.
- Not a replacement for Seed Directory, peer supervisor, Matrix, Room, AD, INAC,
  or story-specific acceptance flows.
- Not a global tracing daemon that observes every production node by default.
- Not a new authority layer for passports, attestations, membership, or routing.
- Not a raw-payload export tool. Raw payload inclusion is a separate, explicit,
  operator-controlled debug mode and is outside the MVP.

## Proposed Model

### Layer 1: Federation Harness Core

`federation-harness-core` should own pure data contracts and deterministic
planning:

- run specification;
- node roles;
- port allocation plan;
- service matrix;
- topology;
- scenario assertions;
- expected capabilities and readiness gates.

It should not spawn processes, write profiles, or perform HTTP calls. It should
turn a declarative input into a checked execution plan.

### Layer 2: Federation Harness Runtime

`federation-harness-runtime` should execute the plan:

- create temporary or configured data directories;
- render node profiles;
- generate or reuse local development TLS trust material;
- start and stop daemons and supervised services;
- start optional Matrix fixtures;
- wait for readiness;
- run scenario steps;
- collect exit statuses and logs;
- clean up processes and temporary stores.

The runtime should be usable by CLI and CI, but should remain below operator UI.

### Layer 3: Trace Explorer Core

`trace-explorer-core` should define the normalized trace model and source
adapters. It should collect from local data directories and daemon APIs where
available, but it should treat each source as an append-only or replayable fact
source.

Initial source adapters should cover:

- temporal event logs exposed through operator storage diagnostics;
- Artifact Delivery ledgers and diagnostics;
- INAC decisions, invitations, stream chunks, and refusals;
- Agora records and query attestations;
- Seed Directory replay cursors, capability registrations, advertisements, and
  revocations;
- Room membership, policy, live-plane, and attestation audit facts;
- Messaging outbox/inbox temporal facts;
- Contact Catalog lookup and provider-sync redacted audit;
- Corpus rounds, bids, settlement handoff, and requester satisfaction;
- notification audit facts when they explain operator-visible remediation.

### Layer 4: Trace Explorer CLI

`trace-explorer-cli` should provide the first user-facing surface:

```text
orbiplex-trace collect --run RUN_DIR --out trace-bundle.json
orbiplex-trace timeline trace-bundle.json
orbiplex-trace graph trace-bundle.json --format mermaid
orbiplex-trace explain --correlation-id ...
```

The CLI should produce:

- a normalized JSON bundle;
- a compact text timeline;
- a failure summary grouped by node, component, delivery, and correlation id;
- optional Mermaid sequence/state diagrams for small traces.

### Layer 5: Operator Trace Explorer

The operator UI should later expose the same read model:

- `/admin/federation-runs`;
- `/admin/federation-runs/{run_id}`;
- `/admin/traces/{trace_id}`;
- filters by node, component, correlation id, delivery id, room id, query id,
  artifact digest, attestation id, passport id, and failure class;
- drill-down to redacted details and source references.

The UI should not invent a new storage authority. It should read bundles or
daemon-exposed diagnostics.

## Data Contracts

### `federation-run.v1`

```json
{
  "schema": "federation-run.v1",
  "run/id": "federation-run:story-010:2026-06-26T10:00:00Z",
  "scenario/ref": "story-010",
  "nodes": [],
  "topology": {},
  "started/at": "2026-06-26T10:00:00Z",
  "ended/at": null,
  "status": "running"
}
```

### `federation-node.v1`

```json
{
  "schema": "federation-node.v1",
  "run/id": "federation-run:...",
  "node/ref": "node-a",
  "node/id": "node:did:key:...",
  "data-dir/ref": "run://node-a",
  "daemon/base-url": "http://127.0.0.1:...",
  "services": ["daemon", "agora-service", "seed-directory", "messaging"],
  "capabilities": ["core/messaging", "seed-directory", "contact-catalog"]
}
```

### `trace-event.v1`

```json
{
  "schema": "trace-event.v1",
  "trace/event-id": "trace-event:...",
  "run/id": "federation-run:...",
  "node/ref": "node-a",
  "source/store": "artifact-delivery",
  "component/id": "daemon",
  "event/time": "2026-06-26T10:00:03Z",
  "event/seq": 42,
  "correlation/id": "corr:...",
  "causality/id": "cause:...",
  "delivery/id": "delivery:...",
  "artifact/digest": "sha256:...",
  "record/id": null,
  "attestation/id": null,
  "passport/id": null,
  "room/id": null,
  "event/kind": "delivery-admitted",
  "status": "accepted",
  "failure/class": null,
  "detail/redacted": {}
}
```

### `trace-link.v1`

```json
{
  "schema": "trace-link.v1",
  "from/event-id": "trace-event:...",
  "to/event-id": "trace-event:...",
  "relation": "caused-by",
  "confidence": "strong",
  "basis": ["same delivery/id", "matching artifact/digest"]
}
```

## Correlation Rules

The trace explorer should correlate by explicit identifiers first and by derived
evidence second.

Strong links:

- same `correlation/id`;
- same `causality/id`;
- same `delivery/id`;
- same `record/id`;
- same `room/id`;
- same `query/id`;
- same `attestation/id`;
- same `passport/id`;
- exact `artifact/digest`;
- explicit parent/child or continuation references.

Medium links:

- same canonical JSON digest over a known payload shape;
- same peer session id plus adjacent sequence windows;
- same Matrix event id referenced by an INAC/Room/Messaging fact;
- same service-order/procurement id.

Weak links:

- close timestamps without shared ids;
- same node pair and same capability in a bounded time window.

Weak links must be labelled as weak and must never be used as proof of causal
responsibility.

## Time Model

The explorer must not pretend that a distributed run has one perfect clock.

Ordering should be derived in this order:

1. explicit sequence numbers and transaction ids inside one store;
2. explicit causal links and continuation ids;
3. signed or attested timestamps with declared issuer;
4. local wall-clock timestamps with node identity;
5. bounded, labelled clock-skew heuristics.

The default output is a partial order. Linear text timelines are presentation
views and should mark ambiguous ordering.

## Redaction and Privacy

Trace bundles are operator artifacts and may still contain sensitive metadata.
The default export policy is:

- no raw message bodies;
- no raw contact handles;
- no raw prompts or model outputs;
- no private keys, auth tokens, bearer tokens, cookies, or passphrases;
- payloads by digest/ref only;
- redacted excerpts only when the source store already carries a safe
  projection;
- explicit `debug/raw-payloads = true` required for any future raw export mode.

The trace model should preserve enough evidence to diagnose failure without
turning diagnostics into a data exfiltration tool.

## Harness Scenario Shape

A scenario should be data-first:

```json
{
  "schema": "federation-scenario.v1",
  "scenario/id": "story-010",
  "nodes": [
    {"node/ref": "node-a", "roles": ["user-node"]},
    {"node/ref": "node-b", "roles": ["seed-directory", "contact-catalog", "messaging"]}
  ],
  "fixtures": ["matrix"],
  "steps": [
    {"kind": "start-nodes"},
    {"kind": "wait-ready"},
    {"kind": "run-story-smoke"},
    {"kind": "collect-trace"},
    {"kind": "assert-trace"}
  ],
  "assertions": [
    {"kind": "event-present", "event/kind": "contact-request-delivered"},
    {"kind": "no-failure-class", "failure/class": "revocation-stale"}
  ]
}
```

Scenario files should be ordinary data that the harness can validate before
starting processes.

## Failure Injection

The harness should support controlled failure injection in later phases:

- restart one node between send and receive;
- expire a passport;
- force revocation stale;
- drop one INAC stream chunk;
- delay Matrix delivery;
- rotate endpoint evidence;
- deny one Room membership attestation;
- corrupt one local projection and require replay repair.

Failure injection is essential for federation confidence because most real
federation bugs are partial-failure bugs.

## CI Profiles

The harness should support explicit CI profiles:

| Profile | Purpose | Expected runtime |
|---|---|---:|
| `smoke` | One small 2-node scenario without Matrix | short |
| `federated-smoke` | 2-3 nodes with Seed Directory, AD/INAC, and one app protocol | medium |
| `matrix-smoke` | 2-3 nodes using a local Matrix fixture | medium |
| `nightly-chaos` | Failure-injection and replay repair checks | long |

CI should start with `smoke` and `federated-smoke`. Matrix and chaos profiles
can become nightly gates once stable.

## Implementation Phases

### Phase 0: Inventory

- List all traceable stores and APIs.
- Document source ownership, redaction posture, correlation ids, and replay
  semantics.
- Identify missing correlation ids in existing subsystems.

### Phase 1: Harness Core

- Add Rust `federation-harness-core` contracts for pure
  scenario/run/node/topology DTOs.
- Add deterministic port and data-dir planning.
- Add validation for role/service combinations.
- Add golden examples for Story 000 and Story 010.

### Phase 2: Harness Runtime

- Add process spawn/stop/wait/cleanup.
- Add readiness wait primitives.
- Add local TLS material setup.
- Add optional Matrix fixture lifecycle as a profile, not as the hard-MVP
  baseline.
- Wrap Story 010 as the first generic harness target.

### Phase 3: Trace Explorer Core

- Add canonical `trace-event.v1` and `trace-link.v1` schemas under
  `doc/schemas/`.
- Add adapters for AD, INAC, Messaging temporal logs, Agora records, and Seed
  Directory state.
- Add deterministic correlation and partial-order sorting.
- Add redaction tests.

### Phase 4: CLI and Bundle Export

- Add `collect`, `timeline`, `explain`, and `bundle` commands.
- Add JSON bundle fixture tests.
- Start with trace bundle import/read from disk; daemon collection APIs are a
  later extension after source adapters stabilize.
- Extend or replace the current focused `xtask trace-delivery` path with the
  generic explorer.

### Phase 5: Operator UI

- Add read-only `/admin/federation-runs` and `/admin/traces` surfaces.
- Add timeline filters and drill-down.
- Link story acceptance output to trace bundles.

### Phase 6: CI Adoption

- Add `federation-smoke` to CI.
- Add nightly Matrix/chaos profile.
- Require trace bundle artifact upload on failure.

## Trade-offs

| Option | Benefit | Cost |
|---|---|---|
| Keep per-story scripts only | Low immediate effort | Federation debugging stays fragmented |
| Build a harness without trace explorer | Better CI startup | Failures still require manual forensic work |
| Build trace explorer without harness | Useful for incidents | Reproducibility remains weak |
| Build both as one proposal | Aligns test and diagnosis | Larger initial scope, needs phased delivery |

The recommended path is to specify both now, but implement in narrow phases:
first harness core/runtime for one existing story, then trace explorer core over
the stores already used by that story.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Harness becomes a hidden production orchestrator | Keep it under tooling/test crates; no production authority, no passport issuance except through existing host APIs |
| Trace explorer leaks private payloads | Digest/ref by default, explicit redaction tests, no raw export in MVP |
| Timeline implies false total ordering | Use partial-order model; mark ambiguous ordering in text views |
| Story scripts and harness diverge | Wrap existing story packs first; migrate gradually |
| Adapter drift as stores evolve | Each adapter has schema/version probes and fixture tests |
| CI becomes too slow | Separate smoke, federated-smoke, matrix-smoke, and nightly-chaos profiles |
| Trace bundle becomes unactionable noise | Provide failure summary, component grouping, and correlation filters |

## Open Questions

None for the current proposal revision.

Resolved 2026-07-02:

1. The first harness implementation uses a Rust core for contracts and
   deterministic planning. Runtime wrappers may reuse existing acceptance code
   where that avoids a rewrite.
2. `trace-event.v1` and `trace-link.v1` are canonical schemas from the start
   because trace bundles are support/audit artifacts.
3. Operator UI starts with trace bundle import/read from disk. Daemon collection
   APIs are deferred until the source adapters stabilize.
4. Story 010 is the first generic harness target.
5. Matrix support is an optional smoke profile, not a hard-MVP blocker.

## Next Actions

1. Create an inventory table of trace sources, store paths, public diagnostics
   APIs, identifiers, and redaction posture.
2. Extract common N-node setup concepts from Story 000, Story 010, and Story 011
   acceptance packs.
3. Define `federation-run.v1`, `federation-node.v1`, `trace-event.v1`, and
   `trace-link.v1` schemas.
4. Generalize `xtask trace-delivery` into the first trace explorer adapter set.
5. Add a read-only CLI that can produce one trace bundle for an existing Story
   010 acceptance run.
6. Add optional Matrix smoke profile support after the local/direct Story 010
   profile is stable.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Item | Status | Notes |
|---|---|---|---|
| P074-001 | Create Rust `federation-harness-core` contracts and deterministic planning | todo | Scenario/run/node/topology DTOs, deterministic port/data-dir planning, and role/service validation. |
| P074-002 | Wrap Story 010 as the first generic harness target | todo | Reuse existing acceptance code where practical; Story 010 is the first integration target because it exercises the broadest federated surface without the Story 009 workflow stack. |
| P074-003 | Define canonical trace schemas | todo | Add `federation-run.v1`, `federation-node.v1`, `trace-event.v1`, and `trace-link.v1` under `doc/schemas/`. |
| P074-004 | Add disk-bundle trace explorer import/read path | todo | Operator/read-only tooling starts from support bundles on disk; daemon collection APIs remain post-adapter-stabilization. |
| P074-005 | Add trace adapters for first Story 010 sources | todo | AD, INAC, Messaging temporal logs, Agora records, and Seed Directory state with redaction tests. |
| P074-006 | Add optional Matrix smoke profile | todo | Matrix fixture support is optional for smoke coverage and not a hard-MVP blocker. |
