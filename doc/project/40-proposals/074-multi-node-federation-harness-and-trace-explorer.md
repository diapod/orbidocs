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
owner marker and one active Orbiplex writer. Other trusted operating-system
principals may have write access only under the explicit
`operator-trusted-shared-managed` posture defined below; that trust assertion
does not authorize two daemons or control registries to govern one writable
`managed/` tree. Equal, overlapping, symlink-aliased, or already-owned roots on
the same host filesystem fail before process start. Equal path text on
independent hosts is not itself a conflict.

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
opt into one of two explicit postures through a host-local, run-scoped policy
file:

- `operator-authorized-shared` admits immutable bulk inputs and ephemeral
  effect workspaces under the snapshot and verification rules below;
- `operator-trusted-shared-managed` additionally admits a writable P066
  `managed/` model store when the operator declares every effective co-writer
  trusted, acknowledges the residual mutation and time-of-check/time-of-use
  risk, and accepts those principals as part of the run's trusted computing
  base.

This proposal does not admit a global boolean that skips ownership,
writable-ancestor, identity, or digest validation. The posture is a closed data
contract, is absent by default, and its implementation is tracked under
P074-011.

An effective ancestry writer is a principal able to alter the admitted root or
replace its existing path entry. A POSIX sticky ancestor alone, such as `/tmp`,
permits creation of sibling entries but does not make their creators effective
writers of an existing private child root. The admitted root itself is always
inspected; non-sticky writable ancestors and broader ACL grants remain subject
to the policy.

Storage roles remain stratified:

- control and authority roots stay exclusive: daemon state, the asset-store
  control registry, keys, leases, the append-only step ledger,
  operator-extension code, and report-signing material cannot use either
  shared posture;
- a writable P066 `managed/` model store may use only
  `operator-trusted-shared-managed`. It retains one root marker, one
  `control-plane/owner-id`, one governing asset-store registry, one active
  Orbiplex writer, and a root distinct from every other slot. Ambient trusted
  co-writers do not become additional Orbiplex owners or gain authority over
  pinning, garbage collection, installation, or activation;
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

For V1, selecting either shared posture is an explicit operator assertion that
every admitted co-writer is authorized and trusted to be non-adversarial,
though still capable of mistakes or concurrent edits. Under
`operator-authorized-shared`, the private snapshot and verification protect the
run from accidental source mutation; they do not claim resistance to a
co-writer who can deliberately replace, rename, or delete the snapshot through
a shared-writable ancestor.

`operator-trusted-shared-managed` deliberately accepts a narrower integrity
claim. The store still verifies descriptor-bound model bytes, root identity,
and managed-object invariants before use and refuses new effects after detected
mount, ACL, marker, or content drift. Because an admitted co-writer can mutate
or replace shared-managed bytes after a successful check, those checks do not
close CWE-367 against that trusted principal. Selecting the posture is the
operator's explicit acknowledgement of this residual risk, not a technical
claim that the race has disappeared. Evidence produced under it must identify
the downgraded trust posture and cannot satisfy an acceptance criterion that
requires exclusive-store or adversarial-co-writer resistance.

A potentially hostile or unknown co-writer is outside both shared postures and
requires either an exclusive snapshot root or an operating-system-enforced
immutable/read-only snapshot that the co-writer cannot replace, with the
consumed target bytes still verified against independently anchored trust
metadata.

The host-local policy binds the selected posture, canonical volume or mount
identity, every effective writer admitted by the operator, allowed storage
roles, story/profile and slot scope, expiry, and required pre-effect and
post-effect checks. `operator-trusted-shared-managed` additionally requires a
versioned risk acknowledgement whose semantics include trusted co-writers,
accepted residual mutation/TOCTOU risk, and the absence of exclusive-store
evidence. Platform adapters must account for POSIX ownership and ACLs on
GNU/Linux and macOS ACL principals; unknown writers, an uninspectable ACL,
remount/autofs identity drift, or changed content fail closed. Reusable topology
files contain none of these paths or principal names. The run manifest and
acceptance report retain a redacted policy reference and digest, selected
posture, risk-acknowledgement version, mount identity, role bindings, and check
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

The Node checkout locator follows the same host-local rule. Remote execution
requires `ORBIPLEX_ACCEPTANCE_NODE_ROOT` to resolve to the canonical Git
worktree containing the installed host agent. The locator is neither topology
data nor product configuration: preflight binds it to the observed revision and
agent path, then removes it from product child environments and retained
aggregate evidence.

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
| Daemons inherit one writable `ORBIPLEX_MODEL_ROOT` | Strip the inherited variable and inject a distinct canonical slot-owned model root into each daemon child; a shared-writable `managed/` tree additionally requires `operator-trusted-shared-managed`, but remains governed by one slot, one owner, and one active Orbiplex writer |
| A descriptive run path exceeds the vfkit socket bound | Separate durable run metadata from a short canonical VMM workspace and preflight the longest derived socket path in bytes |
| A macOS VM workspace cannot APFS-clone its image | Require same-volume APFS source and workspace, or stage and re-verify the immutable base image on the selected APFS volume before cloning |
| An auto-mounted/removable volume has legitimate co-writers | Keep strict refusal by default; require the host-local policy to bind mount identity, all effective writers, scope, expiry, allowed roles, and either the ordinary shared posture or the stronger shared-managed risk acknowledgement |
| A runtime executable or build-hook-capable source tree is sourced from shared-writable ancestry | Treat it as executable input, verify its admitted identity, and stage it into an exclusive execution root before launch or build; neither shared posture authorizes direct or indirect code execution from shared-writable ancestry |
| A shared immutable input changes between check and use ([CWE-367](https://cwe.mitre.org/data/definitions/367.html)) | Copy or snapshot it into a private run-owned location, verify the target bytes against trust metadata anchored outside the shared source, and consume only that verified target; source revalidation alone is insufficient |
| Mount identity, ACLs, or immutable input change after preflight | Refuse new effects, retain each affected slot's closed post-effect `passed` or `refused` outcome and refusal code even in a failed run, and abort rather than converting drift into a relaxed success |
| A shared-managed run is reported as exclusive-store evidence | Retain the posture and risk-acknowledgement version in redacted evidence and reject any criterion that requires exclusive-store or adversarial-co-writer resistance |
| A potentially hostile co-writer is admitted as merely shared | Refuse both shared postures; require an exclusive root or an OS-enforced immutable/read-only snapshot that the co-writer cannot replace, plus independently anchored verification |

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
   control state, authority, and, at that revision, writable model stores. The
   posture requires a closed run-scoped policy, private verified snapshots, and
   an explicit `trusted-non-adversarial` assertion for every admitted co-writer.
   The writable-model-store restriction is superseded by the narrower
   2026-08-27 decision below; the ordinary shared posture is unchanged.
2. The Story 012 physical-host planning baseline assigns Bielik MLX to the
   `node-a` Chair role, Qwen3-Coder MLX to the `node-b` solver role, and
   Qwen2.5-Coder GGUF to the `node-c` reviewer/facilitator role. These are
   accepted planned bindings, not deployment defaults or runtime evidence. Each
   receives an independent qualification item before P074-010 integration.

Resolved 2026-08-27:

1. P074 additionally admits `operator-trusted-shared-managed` for a writable
   P066 `managed/` model store in acceptance runs. Selection is an explicit
   assertion that every effective co-writer is trusted and part of the run's
   trusted computing base, plus a versioned acknowledgement that residual
   mutation and CWE-367 risk remain. One active Orbiplex writer, owner marker,
   control registry, and distinct per-slot root remain mandatory. The posture
   never extends to control/authority roots or executable input, and evidence
   produced under it cannot be represented as exclusive-store or
   adversarial-co-writer-resistant evidence. This is an accepted design
   decision. P074-011 is now `partial`: the writable shared-managed vertical
   slice is implemented and platform-exercised, while immutable-input snapshot
   consumption and shared VMM workspaces remain open.

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
11. Extract one reusable physical story-runtime adapter over the checked
    local/SSH harness so existing three-node story packs can materialize
    per-slot configuration, start and restart processes, call direct product
    endpoints, and collect evidence without treating SSH as product transport.
12. Add a private host-local model-binding inventory and a redacted admission
    probe that joins stable Story binding refs to exact P064 package, lifecycle,
    conformance, artifact, platform, and resource evidence without placing
    local paths in topology or scenario data.
13. Add the reusable vfkit image/workspace admission needed by the physical
    Story 012 profile: short canonical socket-safe paths, same-volume APFS clone
    proof, private snapshot or copy plus target-byte verification for selected
    shared inputs, and exclusive staging for executable inputs.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

| ID | Item | Status | Notes |
|---|---|---|---|
| P074-001 | Create Rust `federation-harness-core` contracts and deterministic planning | done | `orbiplex-node-federation-harness-core` now owns closed topology/scenario/run/node DTOs, RFC 8785 topology and profile digests, CLI-over-environment topology selection, exact local-slot target planning, deterministic physical-host-scoped product ports, closed node-evidence statuses, host-local run paths, role-to-service validation, dependency-cycle refusal, structurally validated plan-carried assertions, same-host writable-root overlap refusal, and a narrow planning CLI. Physical host identity is compared case-insensitively for DNS names, so co-located slots cannot collide through case drift. Runtime filesystem canonicalization and assertion evaluation remain correctly owned by the runtime and Story profile rather than the pure core. |
| P074-002 | Wrap Story 010 as the first generic harness target | todo | Reuse existing acceptance code where practical; Story 010 is the first integration target because it exercises the broadest federated surface without the Story 009 workflow stack. |
| P074-003 | Define canonical trace schemas | done | `trace-event.v1`, `trace-link.v1`, `federation-run.v1`, and `federation-node.v1` are canonical, mirrored into Node, and schema-gated. The run/node contracts retain redacted slot and product refs rather than unrestricted hostnames or local paths; `federation-node.v1` now also carries closed redacted P074-011 policy evidence and its paired post-effect revalidation outcome without making the private import policy an export contract. Trace contracts remain consumed by `trace-explorer-core` and the P081 acceptance runner. |
| P074-004 | Add disk-bundle trace explorer import/read path | todo | Operator/read-only tooling starts from support bundles on disk; daemon collection APIs remain post-adapter-stabilization. |
| P074-005 | Add trace adapters for first Story 010 sources | partial | `trace-explorer-core` now projects P081 execution receipts from Artifact Delivery, Scheduler, and Sensorium into redacted events and explicit strong links; the P081 acceptance runner exercises those adapters' source contracts and emits a redacted bundle. INAC, Messaging temporal logs, Agora records, and Seed Directory state remain for the full Story 010 adapter set. |
| P074-006 | Add optional Matrix smoke profile | todo | Matrix fixture support is optional for smoke coverage and not a hard-MVP blocker. |
| P074-007 | Freeze the reusable physical-host topology contract | done | `orbiplex-acceptance-topology.v1` and `federation-scenario.v1` are canonical, mirrored, Schema Gate admitted, canonically digested, and covered by sanitized positive plus secret/story-field refusal fixtures. The checked P074-001 plan assigns distinct slot-owned writable roots and redacted run refs. The host runtime canonicalizes effective roots, rejects broad, symlinked, wrong-owner, broadly writable, and known removable/automatic authority roots before effects, strips inherited host-only configuration, and keeps equal path text on independent hosts distinct. Story duties, ports, SSH secrets, and host-local paths remain outside topology. Shared/removable opt-in semantics remain correctly owned by P074-011 rather than this strict topology contract. |
| P074-008 | Add an any-host resumable local/SSH orchestrator | partial | `federation_harness_runtime.py` and the bounded host agent now share one local/SSH control interface, run parallel host/platform/revision/topology/profile/root/clock preflight, invoke the checked Rust planner, acquire the owner lease before identical host-local execution fences, retain an idempotent append-only hash-chained owner ledger, sanitize child environments, bind effects to a live lease and host-owned cwd, and fence PID reuse. Physical identity accepts an exact hostname/FQDN or an expected non-loopback DNS address that the local kernel can bind; loopback, multicast, and wildcard aliases cannot prove host identity. Strict preflight rejects symlinked, group/world-writable, and known removable/automatic authority roots without changing permissions; selected shared/removable model storage still requires P074-011. Unit coverage proves competing and stale lease refusal, idempotent/conflicting ledger behavior, path escape refusal, partial-host aggregation, shell-noise refusal, clock skew, hostname-versus-interface-address handling, host-only locator stripping, and absence of SSH forwarding. On 2026-08-27 one clean synchronized invocation from `node-b` completed preflight, checked planning, leases, parallel builds, direct product traffic, restart, evidence collection, report retention, and lease release across all three physical hosts. The run retained node-local evidence and the owner ledger without exposing private material. Physical interrupted-run resume, real-model per-slot root injection, and vfkit-specific checks remain before `done`; P074-009 closes only the deterministic Room transport consumer of this partial substrate. Depends on P074-007. |
| P074-009 | Prove direct transport across three physical hosts | done | The Story-012-shaped deterministic profile composes the generic checked plan and any-host executor, binds its exact three-assertion contract before effects, builds the existing P070 deployment binary per host, binds a host-TLS Room relay to the planned topology endpoint on `node-a`, compares DNS identity case-insensitively, publishes four `room-live-message.v2` deliveries from `node-b`, receives the exact replay under observation-only authority on `node-c`, gracefully restarts the relay, reconnects at the exact checkpoint, records redacted assertion results, removes private credential/key material, and retains a Schema-Gate-validated redacted `federation-run.v1` manifest. Unit evidence covers topology/profile and assertion drift surfaces, stale and competing leases, partial-host preflight, clock skew, PID reuse, path escape, and absence of SSH forwarding. The first physical joins exposed a lower Room-WSS portability defect: `handle_connection` replaced the bounded first-frame read timeout with the 10 ms established-session poll cadence before receiving `join`, causing GNU/Linux `EAGAIN` and a client-visible reset without close handshake. The short poll timeout is now installed only after the first application frame; its delayed-first-frame regression passes on macOS and GNU/Linux. On 2026-08-27 the clean synchronized Node revision `98f38f74385ab9c1733f47fb22e89ea6198208fa` completed the full three-host profile and retained `report://story-012-physical-transport/1rFld2mbqbPojxQpvZ70/federation-run.v1.json` with content SHA-256 `9a18eef280c846c0d080d3bbd2421e670cdaf3b44595404230d7bcaaccfb4e0f`. The owner ledger records all three required assertions and the complete ten-step chain; the exact retained bytes pass Schema Gate, contain no forbidden secret/path markers, and remain after strict private credential/key cleanup and successful lease release. The separate P070 Sensorium host-projection requalification remains open and does not weaken this explicitly Room-only result. Depends on the implemented P074-008 substrate and the relevant P056/P070 deployment contracts. |
| P074-010 | Add Story 012 as the first real-model physical-host consumer | todo | Compose the existing Story 012 semantics through P074-016 rather than creating a second story harness, and integrate only the independently qualified P074-012 through P074-014 bindings admitted by P074-017. Retain one closed green report proving direct Room/Corpus/WSS/Sensorium traffic, independent per-slot writable model stores, model-generated solver/reviewer products, Chair admission, short vfkit socket-safe workspace paths, APFS-cloned guest preparation on macOS through P074-018, restart, revocation, and no SSH product proxy. When shared/removable storage is selected, evidence must identify the P074-011 posture and its pre-effect and post-effect checks. The report must carry per-slot binding identities and resource/timing measurements without private paths, prompts, model output, credentials, or principal ids. Depends on P074-009, P074-011 for every selected shared role, P074-012 through P074-014, and P074-016 through P074-018. |
| P074-011 | Implement the accepted shared/removable-volume acceptance trust policy | partial | The canonical import-only `orbiplex-acceptance-storage-policy.v1` contract, valid/invalid fixtures, Schema Gate family, strict absent-policy default, private host-only locator, closed manual boundary validator, and redacted `federation-node.v1` evidence are implemented. The `operator-trusted-shared-managed` vertical slice issues an expiring run/story/profile/slot-scoped policy from the observed canonical root, mount identity, POSIX mode, and macOS/GNU/Linux ACL writer principals; preflight and parallel post-effect revalidation refuse policy-byte, expiry, root, remount, ACL, or co-writer drift without relaxing permissions. The harness preserves exact preflight checks, adds exact post-effect checks before a passing report, and retains per-slot `passed` or typed `refused` revalidation outcomes in failed reports; partial-host success is not discarded. It strips the policy locator from children and retains posture, risk version, policy/mount digests, role, and writer count without paths or principal ids. ACL coverage includes GNU/Linux access/default masks, macOS principal names containing spaces, and the intentional POSIX sticky-ancestor distinction: sibling creation alone is not write authority over an existing private selected root. Unit evidence covers bypasses, malformed policy data, scope and writer drift, symlinks, world-write, private-file custody, both ACL parsers, response-slot binding, partial aggregation, and report redaction. Live 2026-08-27 platform probes passed on the group-writable removable APFS model root on `node-b` and an isolated group-writable GNU/Linux root on `node-c`; changing the latter writer set produced `storage-co-writer-drift`. This does not yet constitute a retained Story-012 model run. Still open: `operator-authorized-shared` private snapshot/copy and target-byte verification for immutable model/image inputs, same-volume ephemeral VMM workspace handling, executable/build-hook staging into an exclusive root, udev/autofs/remount exercise with retained evidence, and evidence-grade distinction in a P074-010 run. One P066 owner marker, registry, active Orbiplex writer, managed-object verification, and distinct per-slot root remain duties of the existing asset-store/planner/runtime strata rather than permissions granted by this policy. Depends on P074-001 and P074-007; gates P074-008 and P074-010 only for the still-unimplemented selected roles. |
| P074-012 | Qualify the `node-a` Bielik MLX Chair binding | todo | Pin the exact `speakleash/Bielik-1.5B-v3.0-Instruct-MLX-8bit` revision, immutable `model-card/ref`, asset digests and sizes, MLX runtime build, package/lifecycle report, adapter conformance, and host resource budget. Retain Chair-specific quality evidence under the admitted Story prompt/output contract and prove inference remains host-native while the VM is used only for PowerDNS. Reuse P064 package/lifecycle machinery; Bielik GGUF evidence does not transfer to the MLX artifact. Gates P074-010; P074-011 additionally applies when shared/removable storage is selected. |
| P074-013 | Qualify the `node-b` Qwen3-Coder MLX solver binding | todo | Pin the exact `mlx-community/Qwen3-Coder-30B-A3B-Instruct-5bit` revision, immutable `model-card/ref`, asset digests and sizes, MLX runtime build, package/lifecycle report, adapter conformance, and measured host resource budget. Preflight must refuse the selected model tree while any `*.incomplete` artifact exists; it must never hash or admit partial download bytes as the pinned package. Retain solver-specific correctness and regeneration evidence under the admitted Story contract. Reuse the P064 MLX qualification machinery without inheriting Qwen2.5-Coder evidence across model identities. Gates P074-010; P074-011 additionally applies when shared/removable storage is selected. |
| P074-014 | Qualify the `node-c` Qwen2.5-Coder GGUF reviewer/facilitator binding | todo | Pin the exact `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF` revision and `Q4_K_M` artifact, immutable `model-card/ref`, digest and size, `llama-server` build, package/lifecycle report, adapter conformance, and measured GNU/Linux host resource budget. Retain separate evidence for every reviewer and facilitator role the binding claims. Reuse exact matching P064 lifecycle evidence where available, but do not infer qualification from MLX or another quantization. Gates P074-010; P074-011 additionally applies when shared/removable storage is selected. |
| P074-015 | Freeze the host-local Node checkout locator | done | Repository paths remain outside the reusable topology. The remote control agent resolves through explicit host-local `ORBIPLEX_ACCEPTANCE_NODE_ROOT`, requires an absolute canonical Git worktree whose agent path is below that root, compares exact revision/profile evidence across hosts, and removes the locator from product child environments and retained aggregates. The local executor binds its own current checkout directly. Live preflight on 2026-08-27 reached all three configured roots at one clean synchronized revision and proceeded through planning and execution; missing, non-canonical, divergent, dirty, or child-inherited locator cases remain fail-closed. Supports P074-008. |
| P074-016 | Extract a reusable physical story-runtime adapter | todo | Define one narrow acceptance-only behavior boundary over the existing checked plan and host executors for per-slot configuration materialization, process start/status/signal/restart, bounded private credential retrieval, direct authenticated host API calls over planned product endpoints, cleanup, and node-local evidence. Keep local three-node profiles behaviorally compatible and keep SSH limited to control/evidence; the adapter must not proxy Room, Corpus, WSS, Sensorium, or model-runtime traffic. The first consumer is P074-010, but the seam must remain story-neutral and reusable by later physical Story 010 or other N-node profiles. Depends on P074-008 and P074-009. |
| P074-017 | Add private qualified model-binding inventory and host admission | todo | Define a closed import-only host-local inventory selected through an explicit host-only locator. Stable binding refs resolve to private runtime, model, package-manifest, lifecycle-report, and conformance locations; topology, scenario, plans, children, and retained reports receive no local paths. A family-neutral host probe joins those locations to the Story-owned public descriptor, refuses missing or extra identities, `*.incomplete` artifacts, platform drift, digest/size drift, stale or failed lifecycle/conformance evidence, insufficient resource budget, and runtime executables not staged under an exclusive execution root. Family handlers reuse P064 MLX and llama package/lifecycle validators rather than duplicate trust logic. Returned evidence is closed and redacted. P074-012 through P074-014 provide the exact three binding instances and role-quality evidence; P074-010 consumes only admitted results. Depends on P074-011 for selected shared model stores and the P064 lifecycle substrate. |
| P074-018 | Add reusable physical vfkit image and workspace admission | todo | Extend the physical host preflight with a short canonical workspace chosen against the longest derived socket path, exact base-image identity, same-volume APFS clone capability, and redacted pre/post-effect evidence. When a selected base image or workspace uses the ordinary shared posture, create a private run-owned snapshot or copy, verify the consumed target bytes against independently anchored metadata, and use only that target. Stage guest helpers, build-hook-capable sources, and other executable inputs into an exclusive execution root before use. Do not weaken the existing local vfkit profile or represent cross-volume copy as APFS-clone evidence. This closes only the image/workspace portion of P074-011 needed by P074-010; broader shared-input roles remain separately trackable. Depends on P074-008 and P074-011. |
