# Proposal 074: Multi-Node Federation Harness and Trace Explorer

Based on:

- `doc/project/30-stories/story-000-node-handshake.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/30-stories/story-011-corpus-fish.md`
- `doc/project/30-stories/story-012-agents-share-chair-terminal.md`
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

1. a hermetic **multi-node federation harness** that can bring up an N-node
   network either locally in CI or across explicitly configured physical hosts
   and exercise federated flows without production-like manual setup;
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

- Provide a declarative N-node federation harness usable locally in CI or across
  explicitly configured physical hosts by operators and developers.
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

### Physical Multi-Host Execution Profile

The same checked execution plan may be realized on separate physical hosts. This
is an additive deployment profile, not a second harness architecture. The
physical profile separates two values that story-specific scripts have often
combined:

- an operator-owned topology maps stable acceptance slots such as `node-a`,
  `node-b`, and `node-c` to reachable hosts and platform classes;
- a story profile maps scenario duties, services, models, images, and evidence
  requirements to those slots.

The reusable topology is selected with `ORBIPLEX_ACCEPTANCE_TOPOLOGIES`, while each
host identifies its own slot with `ORBIPLEX_ACCEPTANCE_SLOT`. Implementations
must also accept `--topology`; explicit CLI input takes precedence over the
environment. Absence of both inputs is an explicit local-profile selection or a
typed refusal, never an implicit discovery of machines on the operator network.

Every participating host must resolve the same topology bytes and digest. The
topology contains infrastructure facts only: slot, hostname, platform reference,
and SSH control endpoint. It must not contain private keys, bearer tokens,
grants, story roles, model paths, image paths, or story-specific ports. Real
operator topology files remain outside the repository; checked examples use
reserved example hostnames.

The orchestrator runs on whichever participating host invokes the acceptance
command. It executes the local slot directly and remote slots through a uniform
executor backed by SSH. SSH owns harness lifecycle, preflight, log collection,
and evidence transfer only. Room, Corpus, WSS, Sensorium Interfaces, and other
product traffic must flow directly between the daemons over their declared
product transports; tunneling product traffic through the control executor does
not prove multi-host behavior.

Any-host invocation does not create multiple authorities. A run has one
canonical lease, run id, topology digest, and append-only step ledger, anchored
on the scenario owner slot unless the story declares another owner. A second
orchestrator may resume idempotent work after proving the same run identity and
lease state, but cannot start a competing execution. Each node emits local
evidence; the orchestrator assembles an aggregate manifest without pretending
to have ambient access to private node-local traces.

Host-local roots are resolved data, not ambient child-process configuration.
The executor may consume `ORBIPLEX_MODEL_ROOT` as a planning input, but must
remove it from every inherited daemon environment and inject one canonical,
non-overlapping writable model-store root per slot. The model store has one
owner marker and exclusive writer; shared read-only model/package source bytes
do not authorize daemons to share one writable `managed/` tree. Equal,
overlapping, symlink-aliased, or already-owned roots on the same host filesystem
fail before process start. Equal path text on independent hosts is not itself a
conflict.

Durable run state and an effectful VMM workspace are separate roots. A vfkit
workspace uses a short canonical path selected against the longest derived
Unix-domain socket path, while leases, ledgers, logs, and reports may remain in a
descriptive hierarchy. On macOS the workspace must also share an APFS volume
with the verified base image so guest-disk creation can use `clonefile`; an image
on another filesystem is first staged and digest-verified on the selected APFS
volume. Topology files contain none of these host-local paths.

### Shared/removable-volume trust posture

The strict default remains exclusive host-owned storage. A deployment that uses
an automatically mounted or removable volume with other legitimate writers may
opt into a distinct `operator-authorized-shared` posture through a host-local,
run-scoped policy file. This proposal does not admit a global boolean that skips
ownership or writable-ancestor validation. The policy is a closed data contract,
is absent by default, and its implementation is tracked under P074-011.

Storage roles remain stratified:

- control and authority roots stay exclusive: daemon state, keys, leases, the
  append-only step ledger, operator-extension code, writable P066 `managed/`
  model stores, and report-signing material cannot use the shared posture;
- immutable bulk inputs may use it: verified model weights, base VM images, and
  package source blobs are bound by exact digest, size, and manifest, copied or
  snapshotted into a private run-owned location, and consumed only after the
  target snapshot bytes have been verified against trust metadata anchored
  outside the shared-writable source;
- ephemeral effect workspaces may use it: a VMM clone/workspace lives in a
  private run directory with a slot binding, owner marker, lease, and explicit
  preflight and post-run evidence. It is not represented as equivalent to an
  exclusive root.

Executable artifacts, including a model-runtime PEX, are never executed
directly from a shared-writable ancestry. They are digest-verified and staged
into an exclusive execution root first. This closes the avoidable time-of-check
to time-of-use window without forcing large immutable weights or VM images back
onto the system disk. Package or source trees capable of invoking build hooks,
plugins, import-time code, or generated executables are classified as executable
inputs rather than immutable bulk data and follow the same exclusive staging
rule.

For V1, selecting `operator-authorized-shared` is an explicit operator assertion
that every admitted co-writer is authorized and trusted to be non-adversarial,
though still capable of mistakes or concurrent edits. The private snapshot and
verification protect the run from such accidental source mutation; they do not
claim resistance to a co-writer who can deliberately replace, rename, or delete
the snapshot through a shared-writable ancestor. A potentially hostile co-writer
is outside this posture and requires either an exclusive snapshot root or an
operating-system-enforced immutable/read-only snapshot that the co-writer cannot
replace, with the consumed target bytes still verified against independently
anchored trust metadata.

The host-local policy binds the canonical volume or mount identity, every
effective writer admitted by the operator, allowed storage roles, story/profile
scope, expiry, and required pre-effect and post-effect checks. Platform adapters
must account for POSIX ownership and ACLs on GNU/Linux and macOS ACL principals;
unknown writers, an uninspectable ACL, remount/autofs identity drift, or changed
content fail closed. Reusable topology files contain none of these paths or
principal names. The run manifest and acceptance report retain a redacted policy
reference and digest, selected posture, mount identity, role bindings, and check
results so an operator-authorized shared run is auditable but never silently
reported as exclusive-storage evidence.

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

### `orbiplex-acceptance-topology.v1`

```json
{
  "schema": "orbiplex-acceptance-topology.v1",
  "topology/ref": "acceptance-topology:three-host-example",
  "topology/revision": 1,
  "nodes": {
    "node-a": {
      "host/name": "node-a.example.test",
      "platform/ref": "macos-arm64",
      "ssh": {"host": "node-a.example.test", "port": 22, "user": "acceptance"}
    }
  }
}
```

The contract describes where a slot can be controlled, not what it is allowed
to do in a story. Host-local storage roots are configuration, with reusable
defaults under `$HOME/var/orbiplex`: `ORBIPLEX_ACCEPTANCE_STATE_ROOT` defaults
to `acceptance`, `ORBIPLEX_MODEL_ROOT` to `models`,
`ORBIPLEX_ACCEPTANCE_IMAGE_ROOT` to `images`, and
`ORBIPLEX_ACCEPTANCE_REPORT_ROOT` to `acceptance-reports`. A story derives its
own bounded run directories below those roots and records the resolved paths in
the run manifest; topology files do not encode them.

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
- Add a uniform local/SSH executor and an any-host resumable orchestrator.
- Fence each physical run with one canonical lease and topology digest.
- Collect node-local evidence into an aggregate manifest without relaying
  product traffic over SSH.

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
| Two hosts start competing orchestrators | Fence the run with one canonical lease and idempotent append-only step ledger |
| Participating hosts use different topology revisions | Require an exact topology digest before preflight or process start |
| A host declares the wrong local slot | Match host identity and platform facts to the selected slot before effects |
| SSH accidentally substitutes for product networking | Restrict SSH to control and evidence collection; assert direct daemon endpoints for product traffic |
| A checked topology leaks machine-specific secrets | Keep credentials and private roots in host-local configuration; schema and fixtures contain only non-secret infrastructure fields |
| Daemons inherit one writable `ORBIPLEX_MODEL_ROOT` | Strip the inherited variable and inject a distinct canonical slot-owned model root into each daemon child; share source bytes read-only only |
| A descriptive run path exceeds the vfkit socket bound | Separate durable run metadata from a short canonical VMM workspace and preflight the longest derived socket path in bytes |
| A macOS VM workspace cannot APFS-clone its image | Require same-volume APFS source and workspace, or stage and re-verify the immutable base image on the selected APFS volume before cloning |
| An auto-mounted/removable volume has legitimate co-writers | Keep strict refusal by default; require the host-local policy to bind mount identity, all effective writers, scope, expiry, and allowed non-authority roles |
| A runtime executable or build-hook-capable source tree is sourced from shared-writable ancestry | Treat it as executable input, verify its admitted identity, and stage it into an exclusive execution root before launch or build; shared authorization covers immutable bulk inputs, not direct or indirect code execution |
| A shared immutable input changes between check and use ([CWE-367](https://cwe.mitre.org/data/definitions/367.html)) | Copy or snapshot it into a private run-owned location, verify the target bytes against trust metadata anchored outside the shared source, and consume only that verified target; source revalidation alone is insufficient |
| Mount identity, ACLs, or immutable input change after preflight | Refuse new effects, retain post-effect evidence, and abort rather than converting drift into a relaxed success |
| A potentially hostile co-writer is admitted as merely shared | Refuse the `operator-authorized-shared` posture; require an exclusive root or an OS-enforced immutable/read-only snapshot that the co-writer cannot replace, plus independently anchored verification |

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

Resolved 2026-08-25:

1. Physical multi-host execution reuses the generic harness plan and adds a
   local/SSH executor profile; it is not a parallel story-specific harness.
2. Topology is reusable infrastructure data. Story profiles map semantic duties
   and services to stable node slots separately.
3. The orchestrator runs on the host that starts the command. One scenario-owned
   lease and append-only step ledger make the run resumable without introducing
   competing authorities.
4. SSH is a harness control and evidence channel only. Product protocols must
   cross the physical network through their real transports.
5. Real hostnames, users, credentials, and storage paths remain in local operator
   configuration. Repository examples use sanitized values.

Resolved 2026-08-26:

1. P074 admits the `operator-authorized-shared` posture for immutable bulk
   inputs and ephemeral VMM workspaces while retaining exclusive roots for code,
   control state, authority, and writable model stores. The posture requires a
   closed run-scoped policy, private verified snapshots, and an explicit
   `trusted-non-adversarial` assertion for every admitted co-writer. This is an
   accepted design decision; P074-011 remains `todo` until its contract,
   implementation, platform tests, and evidence are complete.
2. The Story 012 physical-host planning baseline assigns Bielik MLX to the
   `node-a` Chair role, Qwen3-Coder MLX to the `node-b` solver role, and
   Qwen2.5-Coder GGUF to the `node-c` reviewer/facilitator role. These are
   accepted planned bindings, not deployment defaults or runtime evidence. Each
   receives an independent qualification item before P074-010 integration.

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
7. Freeze `orbiplex-acceptance-topology.v1` and add a sanitized three-host
   example plus host-local environment conventions.
8. Implement the any-host local/SSH executor with canonical run leasing,
   idempotent resume, and per-node evidence assembly.
9. Add a three-physical-host transport-conformance profile before a real-model
   Story 012 consumer is promoted.
10. Qualify the three accepted Story 012 model-slot bindings independently,
    reusing P064 package/lifecycle machinery and admitting only exact
    artifact-specific and role-specific evidence before P074-010 integration.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Item | Status | Notes |
|---|---|---|---|
| P074-001 | Create Rust `federation-harness-core` contracts and deterministic planning | partial | The foundation implements the pure topology DTO, canonical digest, closed validation, CLI/environment precedence, exact local-host fencing, deterministic `Local`/`Ssh` target planning, dependency guard, and narrow CI workflow. Scenario/run DTOs, service validation, and deterministic port/data-dir planning remain. |
| P074-002 | Wrap Story 010 as the first generic harness target | todo | Reuse existing acceptance code where practical; Story 010 is the first integration target because it exercises the broadest federated surface without the Story 009 workflow stack. |
| P074-003 | Define canonical trace schemas | in-progress | `trace-event.v1` and `trace-link.v1` are canonical, mirrored into Node, schema-gated, consumed by `trace-explorer-core`, and emitted as metadata-only checks by the P081 acceptance runner. `federation-run.v1` and `federation-node.v1` remain with the generic harness slice. |
| P074-004 | Add disk-bundle trace explorer import/read path | todo | Operator/read-only tooling starts from support bundles on disk; daemon collection APIs remain post-adapter-stabilization. |
| P074-005 | Add trace adapters for first Story 010 sources | partial | `trace-explorer-core` now projects P081 execution receipts from Artifact Delivery, Scheduler, and Sensorium into redacted events and explicit strong links; the P081 acceptance runner exercises those adapters' source contracts and emits a redacted bundle. INAC, Messaging temporal logs, Agora records, and Seed Directory state remain for the full Story 010 adapter set. |
| P074-006 | Add optional Matrix smoke profile | todo | Matrix fixture support is optional for smoke coverage and not a hard-MVP blocker. |
| P074-007 | Freeze the reusable physical-host topology contract | partial | `orbiplex-acceptance-topology.v1`, Schema Gate import/export admission, canonical topology-digest validation, pure CLI-over-environment precedence, secret/story-field refusal fixtures, and a sanitized three-host example are implemented. The shared Python acceptance boundary now strips inherited `ORBIPLEX_MODEL_ROOT` from existing local three-node daemon children, resolves stable image-set leaves below `ORBIPLEX_ACCEPTANCE_IMAGE_ROOT`, keeps report output below the independent report root, and rejects empty or relative root inputs. Remaining generic root materialization must assign distinct canonical writable roots per daemon slot from the checked run plan, record them in the run manifest, and keep host-local VMM workspace paths outside topology data. Depends on the remaining P074-001 planning contracts. |
| P074-008 | Add an any-host resumable local/SSH orchestrator | todo | Execute the local slot directly and remote slots through SSH, fence one canonical scenario-owned lease, persist an append-only idempotent step ledger, and assemble per-node evidence. Child environments must carry explicit per-slot model roots. vfkit execution must preflight the longest derived socket path and same-volume APFS clone capability. SSH must not proxy product traffic. A selected shared/removable volume additionally requires an accepted and implemented P074-011 policy; absence of that policy retains strict refusal. Depends on P074-007. |
| P074-009 | Prove direct transport across three physical hosts | todo | Run a deterministic transport-conformance profile over three independent host failure domains, including topology drift, restart, stale lease, WSS reconnect, and partial-host failure refusals. Depends on P074-008 and the relevant P056/P070 deployment contracts. |
| P074-010 | Add Story 012 as the first real-model physical-host consumer | todo | Integrate the independently qualified P074-012 through P074-014 bindings; retain a closed report proving direct Room/Corpus/WSS/Sensorium traffic, independent per-slot writable model stores, short vfkit socket-safe workspace paths, APFS-cloned guest preparation on macOS, restart, revocation, and no SSH product proxy. When shared/removable storage is selected, evidence must identify the P074-011 posture and its pre-effect and post-effect checks. Depends on P074-009, P074-012, P074-013, P074-014, and the Story 012 substrate gates. |
| P074-011 | Implement the accepted shared/removable-volume acceptance trust policy | todo | Freeze the accepted design as a closed host-local policy contract with strict default behavior, canonical mount identity, enumeration of all effective writers, an explicit `trusted-non-adversarial` co-writer assertion, role-scoped authorization, expiry, remount/ACL drift refusal, and redacted run-manifest/report evidence. Close CWE-367 by copying or snapshotting immutable bulk input into a private run-owned location, verifying the consumed target bytes against trust metadata anchored outside the shared source, and never relying on source revalidation alone. Treat build-hook/plugin/import-capable sources as executable inputs and stage them into exclusive roots. Potentially hostile co-writers require an exclusive root or OS-enforced non-replaceable immutable/read-only snapshot. Cover macOS ACL/removable-volume and GNU/Linux POSIX ACL/udev/autofs cases. The policy may authorize immutable bulk inputs and ephemeral VMM workspaces, never authority/control roots or writable P066 `managed/` stores. Depends on P074-001 and P074-007; gates P074-008 and P074-010 whenever shared/removable storage is selected. |
| P074-012 | Qualify the `node-a` Bielik MLX Chair binding | todo | Pin the exact `speakleash/Bielik-1.5B-v3.0-Instruct-MLX-8bit` revision, immutable `model-card/ref`, asset digests and sizes, MLX runtime build, package/lifecycle report, adapter conformance, and host resource budget. Retain Chair-specific quality evidence under the admitted Story prompt/output contract and prove inference remains host-native while the VM is used only for PowerDNS. Reuse P064 package/lifecycle machinery; Bielik GGUF evidence does not transfer to the MLX artifact. Gates P074-010; P074-011 additionally applies when shared/removable storage is selected. |
| P074-013 | Qualify the `node-b` Qwen3-Coder MLX solver binding | todo | Pin the exact `mlx-community/Qwen3-Coder-30B-A3B-Instruct-5bit` revision, immutable `model-card/ref`, asset digests and sizes, MLX runtime build, package/lifecycle report, adapter conformance, and measured host resource budget. Retain solver-specific correctness and regeneration evidence under the admitted Story contract. Reuse the P064 MLX qualification machinery without inheriting Qwen2.5-Coder evidence across model identities. Gates P074-010; P074-011 additionally applies when shared/removable storage is selected. |
| P074-014 | Qualify the `node-c` Qwen2.5-Coder GGUF reviewer/facilitator binding | todo | Pin the exact `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF` revision and `Q4_K_M` artifact, immutable `model-card/ref`, digest and size, `llama-server` build, package/lifecycle report, adapter conformance, and measured GNU/Linux host resource budget. Retain separate evidence for every reviewer and facilitator role the binding claims. Reuse exact matching P064 lifecycle evidence where available, but do not infer qualification from MLX or another quantization. Gates P074-010; P074-011 additionally applies when shared/removable storage is selected. |
