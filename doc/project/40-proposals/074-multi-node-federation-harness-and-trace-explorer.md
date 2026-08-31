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
host-local literal product bind address, and SSH control endpoint. The bind
address is distinct from the routable hostname used in advertised endpoints and
TLS identity; preflight must prove that it is one non-loopback unicast address
owned by the selected host, and wildcard or DNS-derived implicit binding is
refused. It must not contain private keys, bearer tokens,
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
      "product/bind-address": "192.0.2.10",
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
2. Physical macOS process supervision retains the non-forwarding SSH control
   session for each supervised child. This preserves the responsible execution
   context covered by macOS Local Network privacy's documented SSH-child
   exception; it does not turn SSH into product transport. Losing that context
   produced `EHOSTUNREACH` from an otherwise healthy `reqwest` client in the
   measured 2026-08-27 run. System-wide Local Network CIDR preferences and
   `launchd` deployment remain explicit operator alternatives, never ambient
   harness effects.

Resolved 2026-08-29:

1. Interrupted-run recovery is represented by a closed, typed local checkpoint,
   not by re-running a Story script and inferring progress from surviving files.
   The checkpoint binds the run, topology, profile, repository revision, exact
   next Story-owned step, retained component identities and dependencies,
   authority expiries, completed effects, ambiguous effects, and cleanup-owned
   resources. The generic harness computes only reuse, invalidation, dependent
   restart, refusal, and cleanup plans. A Story adapter names its own resumable
   steps and reconstructs Story values from durable facts; it does not move Room,
   Sensorium, VM, or deliberation semantics into the harness core.
2. `exploration-retain` is one live diagnostic passage. A retained control session
   is part of a process component's identity on platforms where it carries the
   responsible execution context. A new orchestrator may inspect and clean an
   interrupted checkpoint, but it must not represent an unattached surviving
   process as reusable supervision. Loss of a required control session therefore
   refuses resume and leaves bounded cleanup available.
3. Resume is fail-closed for topology, profile, repository revision, target-byte,
   storage-policy, lease, authority, clock, or completed-effect drift. A code
   repair that changes the repository revision deliberately invalidates this V1
   checkpoint and starts a new passage; parameter repair is resumable when the
   bound profile and authority facts remain unchanged. A future reviewed repair
   transition may bind old and new revisions while restarting every code-derived
   stratum, but it is not ambient V1 behavior.
4. A resumed diagnostic passage never becomes acceptance evidence. Completion of
   P074-022 requires deterministic fault-injection coverage, one physical
   interrupted/resumed exercise, an explicit bounded cleanup exercise, and then a
   fresh default run from preflight through post-effect revalidation and cleanup.

Resolved 2026-08-29 (lease recovery refinement):

1. Retaining a checkpoint first renews the same orchestrator's run leases with a
   bounded exploration TTL and records the resulting exact expiries as checkpoint
   authorities. Renewal never changes run identity or orchestrator identity.
2. An unexpired active lease cannot be taken over. After expiry, or after an
   explicit `interrupted` release, another orchestrator may acquire only a
   cleanup-scoped lease for the same run, topology, and profile identity. That
   lease admits the closed cleanup command set, cleanup-ledger append, checkpoint
   tombstone, and lease release; it cannot start, resume, or revalidate product
   work. This keeps cleanup available without treating expiry as process adoption.
3. Cleanup takeover is an operator action over the already-authorized host control
   channel. It is not a new product authority and does not weaken the checkpoint's
   refusal of lost required supervision.
4. Cleanup progress is a separate owner-host atomic journal bound to the checkpoint
   sequence and its closed resource set. Each successful idempotent resource cleanup
   is recorded before moving on; retry skips journaled resources. The checkpoint
   remains immutable until every resource is journaled, after which the cleanup fact,
   checkpoint tombstone, and failed lease release close the passage in that order.

Implementation evidence recorded 2026-08-28:

1. The first retained real-model three-physical-host Story 012 run passed at
   `federation-run:story-012-physical-real-model:20260828T183021Z`. Its redacted
   aggregate is retained as
   `report://story-012-physical-real-model/T1BTIvqtM8RjVsEN-55Z/federation-run.v1.json`
   with content SHA-256
   `5bc78032d40d8549ac5dd08308de58314a0fd4a81c5768e328ffa8fdf525c4b6`;
   the paired Story report has content SHA-256
   `f546c4acd6761ca5f8ecbfc38539dca0eecfefceba741e017bbc898a48e32b92`.
   All three node reports, all three model post-effect revalidations, and all ten
   scenario assertions passed. The measured wall time was 744,166 ms, including
   536,105 ms of real deliberation over two cycles and two experiments.
2. The passing profile used the grammar-constrained Qwen2.5-Coder 3B fallback
   admitted by P074-026 on `node-a`; the Bielik MLX binding remains retained
   evidence and a separately incomplete qualification item. This physical
   choice is evidence for one accepted profile, not a product deployment
   default.
3. The run exercised direct Room/Corpus WSS and Sensorium/Workbench traffic,
   independent model stores, solver/reviewer/Chair model products, the planned
   `node-c` restart and reconnect, authority revocation, APFS-cloned vfkit
   preparation and cleanup, and the absence of an SSH product proxy. It also
   live-proved the `operator-trusted-shared-managed` model-store posture on
   `node-b`, including final storage-policy revalidation.
4. Optional communication recordings remain private to their owner hosts. The
   Story-owned evaluator executes on each owner host and only its closed result
   crosses the control channel. The passing run produced complete evidence for
   all required `node-a`, `node-b`, and `node-c` communication seams.

Implementation state recorded 2026-08-29 (not yet closure evidence):

1. The pure Rust core now validates the closed checkpoint and computes a
   deterministic provider-first reuse/restart dependency closure. The host/runtime
   strata implement exact lease renewal and revalidation, atomic owner checkpoint
   persistence, durable per-resource cleanup progress, cleanup-only takeover,
   model/storage/vfkit target-byte revalidation, and redacted status/cleanup
   operator commands.
2. The thin Story 012 adapter maps the checked `run-story-012` step, bootstrap
   receipt, supervised processes, vfkit workspace, and run-private cleanup roots.
   Its explicit fault profile stops only the `node-c` daemon, requires the generic
   plan to isolate that component, restarts it through the Story lifecycle seam,
   proves a second all-reuse checkpoint, and then cleans the passage. The profile
   remains `diagnostic-not-promotable` by construction.
   A host-local issuer refreshes only the exact-run inventory envelope around
   unchanged qualified model bindings; it preserves slot/scenario/profile
   identity, writes atomically with owner-only permissions, and never emits
   private locators. An inventory-backed requalifier resolves those locators
   host-locally and reruns the existing real role samples when the underlying
   behavioral evidence expires instead of extending its timestamp.
3. Focused validation is green on all three physical participants at Node revision
   `af33b57ef2cf8f1681c6f6f8f5c47e676d2405ec`: 19 Rust core tests and 332 Python
   harness/Story tests cover both macOS hosts and the GNU/Linux reviewer host.
   This is implementation and portability evidence only.
   P074-008 and P074-022 remain open until the required three-host physical
   fault/resume/cleanup exercise and subsequent fresh default green Story run are
   retained.
5. The selected Qwen2.5-Coder 3B reviewer subsequently passed two fresh,
   no-retry, production-shaped five-sample populations on the two-core Broadwell
   `node-c`: 5/5 complete-plan acceptances and 5/5 repairable-plan
   `request-regeneration` verdicts. The respective observed p95/max durations
   were 156,195 ms and 156,728 ms. These populations did not exercise the later
   reviewer-only correction from a host-refused false denial to `accept`; that
   distinct recovery path remains unqualified under P074-027.

Implementation evidence corrected 2026-08-30:

1. Repeated fresh physical passages showed that the Qwen2.5-Coder 3B reviewer can
   contradict literal proposed listener directives and can emit internally
   inconsistent evidence after the host front-loads the immutable plan and
   pre-effect facts. The one permitted reviewer-only correction then failed to
   recover reliably within the bound deliberation passage.
2. Inspection of the retained qualification corpus established that the reported
   5/5 "repairable corrections" population covered an ordinary defective-plan
   `request-regeneration` case. It did not cover the production recovery contract
   in which the host refuses a semantically false review and requires a corrected
   `accept` over the unchanged plan and facts. P074-025 is therefore `partial`,
   while its complete-plan, defective-plan, Facilitator, immutable binding, and
   retained 2026-08-28 acceptance evidence remain valid.
3. P074-027 owns the missing contract and qualification. The implementation must
   extract one pure shared correction-prompt constructor consumed by both the
   Story runner and the reviewer bench, add a redacted production-shaped listener
   case with a host-required verdict, and qualify the exact physical binding with
   a fresh no-retry population. Host validation remains authoritative: it must
   neither synthesize nor coerce `accept`, and a second invalid review continues
   to fail closed.
4. The 2026-08-30 Qwen2.5-Coder 3B correction population failed the strengthened
   semantic gate on its first no-retry sample: the review returned formal
   `accept` and acknowledged `HOST_FACTS`, but omitted the exact proposed
   `local-address` fact. Further answer-template shaping would turn the reviewer
   into a host-prose echo rather than qualify independent correction. P074-027
   therefore proceeds with the already retained and role-qualified P074-014
   Qwen2.5-Coder 7B binding before considering a new uncached candidate.
5. The retained 7B binding then exceeded the unchanged 330-second request budget
   on its first correction sample on the two-core `node-c`; the runtime remained
   healthy, but produced no completed marker before timeout. P074-027 therefore
   admits the already pinned reviewer-only Phi-4 Mini Q4_K_M candidate as the next
   bounded comparison. Its exact manifest-driven download, digest verification,
   semantic correction population, role qualification, and lifecycle/package
   admission must complete before it can replace either retained Qwen binding.
6. Cross-candidate inspection then exposed accidental complexity in the correction
   boundary itself: the prompt serialized the same `HOST_FACTS` twice, expressed
   field rules as a meta-JSON object, and reused a generic guard whose record rule
   read as an unconditional true statement even when the projected record fact was
   false. P074-027 now uses a compact data-derived correction guard with explicit
   per-field attribution constraints and one facts projection. The production-shaped
   Phi-4 prompt fell from approximately 3,886 to 2,618 bytes, and the Story-012 suite
   passes 470/470 tests. This is a contract clarification, not an answer template: the
   host still does not author findings, evidence prose, redundant actions, or the next
   test, and the independent semantic validator remains the admission boundary.
7. The bounded post-simplification Phi-4 sample completed within the unchanged
   budget in 215,327 ms, but returned formal `accept` with effectively empty
   findings, supporting evidence, and next test. The host correctly refused it for
   missing `HOST_FACTS` attribution. The exact ledger is retained under
   `${ORBIPLEX_ACCEPTANCE_REPORT_ROOT}/p074-027/phi4-correction-compact-20260830.jsonl`
   with SHA-256
   `ef7d4e7b11b0ff684ba612b2c54a437b1c46a4545f3192eb5d12c6045ba3ed56`.
   Together with the failed 3B semantic sample, the 7B timeout, and the earlier
   253,141 ms Phi-4 semantic failure, this closes prompt-shape exploration without
   qualifying a binding. No further prompt tuning is admitted under P074-027 unless
   a reviewed contract change first demonstrates that it does not author the review.
8. P074-028 reused the exact package-described Qwen3-Coder MLX bytes on `self.local`
   through an additive physical-package adapter in the production-shaped Reviewer
   bench. The adapter verifies package assets, runtime identity, the 48 GiB host
   memory envelope, and a distinct private PEX root, while retaining the source
   binding's existing `solver` role rather than implying Reviewer admission. The
   unchanged no-retry five-sample population completed quickly (p95/max 3,996 ms),
   and every response selected `accept`, named the required `local-address` fact,
   and proposed a bounded next test. All five nevertheless omitted the mandatory
   `ORBIPLEX_REVIEW_JSON=` marker and closed `redundant-actions` field, so the host
   correctly refused the population at the typed-marker boundary. The ledger is
   retained under
   `${ORBIPLEX_ACCEPTANCE_REPORT_ROOT}/p074-028/qwen3-colocated-reviewer-20260830.jsonl`
   with SHA-256
   `3bdbdaa4beb562cd68bedc790f9a95e4be9399d77500726ebb2b2d0e97bc63e5`.
   This rejects the current Qwen3-without-native-grammar path for P074-027 without
   converting the near-miss into host-authored output. The full co-located Story
   profile and second concurrent MLX process were therefore not started.

Resolved 2026-08-30 (two-host diagnostic topology):

1. P074 admits an explicit `physical-two-host-three-node` diagnostic profile in
   which three independently identified Node slots are placed on two physical
   hosts. The topology must represent the shared host directly; aliases that make
   one physical host appear to be two hosts are refused. Planning and evidence
   derive both logical-node and physical-host cardinality and retain the shared
   failure domain. This profile is always `diagnostic-not-promotable` and cannot
   satisfy a `physical-three-host-full-system` claim.
2. Co-located slots retain separate Node and Agent identities, data and report
   roots, mutable model-store roots, ports, leases, process supervision, model
   bindings, sessions, budgets, and evidence. They may consume the same verified
   immutable model bytes. A shared model-runtime process is permitted only when
   the selected Story binding declares it explicitly and the report records the
   correlated runtime failure domain; it is not independent-runtime evidence.
   The first profile prefers a separate supervised runtime endpoint over shared
   immutable Qwen3-Coder MLX bytes when the measured memory envelope permits it.
   Existing private model-binding and storage-policy locators may contain one
   literal `{slot}` placeholder for a multi-slot host. The host agent expands it
   only from its validated slot argument; the topology and retained report never
   carry the resulting path. A locator without the placeholder preserves the
   ordinary one-slot contract, while unknown placeholders fail closed.
   The same validated slot selection may specialize the mutable state, report,
   and managed-model base roots. The planner still receives and compares the
   expanded roots, so shared-host overlap remains a refusal rather than an
   authority implied by templating.
3. The profile first qualifies the co-located Reviewer against the unchanged
   P074-027 semantic correction gate. Runtime-native constrained output or a
   reviewed typed structured-response boundary may change framing, but the host
   must not add a marker, default a missing field, write review prose, or coerce a
   verdict. Full execution remains blocked until a fresh no-retry population
   reaches 5/5 contract admission within its reviewed budget.
4. A passing two-host passage proves three logical Nodes, direct product traffic
   over a real LAN, real Chair/Solver/Reviewer deliberation, slot-scoped process
   loss, deterministic resume closure, and bounded cleanup. It does not prove
   tolerance of losing the co-located physical host or three independent physical
   failure domains. It therefore advances P074-022 implementation evidence but
   leaves its existing three-physical-host closure clause open.

Implementation evidence recorded 2026-08-30 (two-host diagnostic passage):

1. The retained exploration run
   `federation-run:story-012-physical-two-host-three-node-real-model:20260830T014817Z`
   created checkpoint sequences 1 and 2, injected loss of only the `node-c`
   daemon, restarted only that invalid component, reached an all-reuse second
   plan, journaled cleanup of every retained resource, and finished with a
   `cleaned` checkpoint. It retained the mandatory
   `diagnostic-not-promotable` ceiling.
2. The subsequent fresh run
   `federation-run:story-012-physical-two-host-three-node-real-model:20260830T033741Z`
   passed all ten Story assertions and all three model post-effect
   revalidations. The Schema-Gate-valid redacted aggregate is
   `report://story-012-physical-two-host-three-node-real-model/Etmikd4KEeqUfnd3zEhm/federation-run.v1.json`
   with content SHA-256
   `0f2b15b8d991837f9a352481262f151a205a7c4dbe06fc587afa452ce5350c4a`;
   the paired Story report has content SHA-256
   `27dfbe58dcc183c1032ee6df8998b93ac33c54b8757643f1fd066f109a95e8ef`.
   Its 902,920 ms passage included 676,872 ms of real model deliberation over
   four cycles and four experiments.
3. The aggregate records three logical Nodes, two physical hosts, the shared
   `node-b`/`node-c` failure domain, and the
   `diagnostic-not-promotable` ceiling. It therefore completes P074-032 while
   leaving the exact three-physical-host closure clauses of P074-008 and
   P074-022 open.

## Next Actions

1. Wrap Story 010 as the first generic harness target under P074-002.
2. Finish the trace-source inventory and disk-bundle import path under P074-004,
   then complete the remaining Story 010 adapters under P074-005.
3. Complete P074-033 by migrating or retiring the compatible critique-gated v2 prose
   path, then implement and qualify the bounded Codex-backed Reviewer adapter under
   P074-029 using the already implemented typed-v3 claim boundary before the exact
   three-host P074-022 closure. P074-030 through the implemented P074-033 slice retain
   the completed two-host
   diagnostic evidence without weakening the three-host evidence requirement.
   Story-owned ephemeral state remains in the thin Story adapter.
4. Complete P074-011 for immutable shared inputs, shared VMM workspace roles,
   executable/build-hook staging, and retained udev/autofs/remount evidence.
5. Decide whether to finish the Bielik-specific P074-012 admission branch or
   retain it as non-gating alternative evidence beside the completed P074-026
   profile.
6. Add the optional Matrix smoke profile under P074-006 after the generic Story
   010 consumer is stable.
7. Implement the optional macOS signing/firewall hardening in P074-020 without
   coupling it to product transport or weakening Local Network privacy.

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
| P074-008 | Add an any-host resumable local/SSH orchestrator | partial | `federation_harness_runtime.py` and the bounded host agent share one local/SSH control interface, parallel preflight, checked planning, owner-first leases, host-local execution fences, an idempotent hash-chained owner ledger, sanitized child environments, supervised PID-reuse-safe processes, and bounded private evidence transfer. Physical identity accepts only the expected hostname/FQDN or an expected non-loopback DNS address owned by the local kernel; SSH carries control/evidence and never product traffic. The interrupted-run boundary is now implemented as a pure closed checkpoint/resume planner, exact host lease/clock/revision/model/storage/target-byte revalidation, atomic checkpoint persistence, durable cleanup progress, cleanup-only recovery authority, and redacted operator status/cleanup. Unit coverage includes dependency-closure restart, supervision loss, authority drift, ambiguous effects, competing/stale/cleanup leases, partial cleanup retry, ledger conflicts, path escape, partial-host aggregation, shell noise, clock skew, host identity, host-only locator stripping, and no forwarding. The same revision passes focused suites on `node-a` and `node-b`. Retained deterministic and real-model physical runs already prove host-local model roots, vfkit lifecycle, direct product traffic, restart, evidence, cleanup, and lease release. It remains `partial` until the new boundary itself completes the required three-host physical fault/resume/cleanup exercise; P074-022 owns that optional non-promotable posture. |
| P074-009 | Prove direct transport across three physical hosts | done | The Story-012-shaped deterministic profile composes the generic checked plan and any-host executor, binds its exact three-assertion contract before effects, builds the existing P070 deployment binary per host, binds a host-TLS Room relay to the planned topology endpoint on `node-a`, compares DNS identity case-insensitively, publishes four `room-live-message.v2` deliveries from `node-b`, receives the exact replay under observation-only authority on `node-c`, gracefully restarts the relay, reconnects at the exact checkpoint, records redacted assertion results, removes private credential/key material, and retains a Schema-Gate-validated redacted `federation-run.v1` manifest. Unit evidence covers topology/profile and assertion drift surfaces, stale and competing leases, partial-host preflight, clock skew, PID reuse, path escape, and absence of SSH forwarding. The first physical joins exposed a lower Room-WSS portability defect: `handle_connection` replaced the bounded first-frame read timeout with the 10 ms established-session poll cadence before receiving `join`, causing GNU/Linux `EAGAIN` and a client-visible reset without close handshake. The short poll timeout is now installed only after the first application frame; its delayed-first-frame regression passes on macOS and GNU/Linux. On 2026-08-27 the clean synchronized Node revision `98f38f74385ab9c1733f47fb22e89ea6198208fa` completed the full three-host profile and retained `report://story-012-physical-transport/1rFld2mbqbPojxQpvZ70/federation-run.v1.json` with content SHA-256 `9a18eef280c846c0d080d3bbd2421e670cdaf3b44595404230d7bcaaccfb4e0f`. The owner ledger records all three required assertions and the complete ten-step chain; the exact retained bytes pass Schema Gate, contain no forbidden secret/path markers, and remain after strict private credential/key cleanup and successful lease release. The separate P070 Sensorium host-projection requalification remains open and does not weaken this explicitly Room-only result. Depends on the implemented P074-008 substrate and the relevant P056/P070 deployment contracts. |
| P074-010 | Add Story 012 as the first real-model physical-host consumer | done | The existing Story-012 runner composes the P074-016 physical adapter and checked scenario rather than forking Story semantics. The retained 2026-08-28 run `federation-run:story-012-physical-real-model:20260828T183021Z` passed on three physical hosts with real deliberation: all three node reports, all three model post-effect revalidations, and all ten exact scenario assertions passed. The Schema-Gate-valid redacted aggregate is `report://story-012-physical-real-model/T1BTIvqtM8RjVsEN-55Z/federation-run.v1.json` with content SHA-256 `5bc78032d40d8549ac5dd08308de58314a0fd4a81c5768e328ffa8fdf525c4b6`; the paired Story report has content SHA-256 `f546c4acd6761ca5f8ecbfc38539dca0eecfefceba741e017bbc898a48e32b92`. The 744,166 ms passage included 536,105 ms of model deliberation over two cycles and two experiments and proved direct Room/Corpus WSS, direct Sensorium/Workbench, independent model stores, solver/reviewer/Chair products, restart/reconnect, revocation, vfkit preparation/cleanup, and no SSH product proxy. P074-012 remains an optional Bielik-specific qualification gap and does not weaken this completed Qwen-backed profile. |
| P074-011 | Implement the accepted shared/removable-volume acceptance trust policy | partial | The canonical import-only `orbiplex-acceptance-storage-policy.v1` contract, strict absent-policy default, private host-only locator, closed manual boundary validator, and redacted pre/post-effect evidence are implemented. The `operator-trusted-shared-managed` model-store slice binds an expiring run/story/profile/slot policy to the canonical root, mount identity, POSIX mode, and macOS/GNU/Linux ACL writer set and refuses policy-byte, expiry, remount, ACL, or co-writer drift without changing operator permissions. The 2026-08-28 green P074-010 run live-proved this posture for the group-writable removable APFS model store on `node-b`, including passing post-effect storage revalidation in the retained report. Still open: private snapshot/copy plus target-byte verification for other immutable shared inputs, shared ephemeral VMM workspaces, exclusive staging for executable/build-hook inputs, and retained udev/autofs/remount evidence. P066 owner markers, registry, one active Orbiplex writer, managed-object verification, and distinct per-slot roots remain duties of their existing strata rather than authority granted by this policy. |
| P074-012 | Qualify the `node-a` Bielik MLX Chair binding | partial | The exact `speakleash/Bielik-1.5B-v3.0-Instruct-MLX-8bit` revision, immutable model-card identity, asset digests/sizes, staged MLX runtime, canonical package, lifecycle/conformance reports, resource envelope, and Chair refusal/revision real-output check are retained and prove host-native inference. Production work exposed that this qualification does not yet prove exact accepted/revised-candidate admission under the bounded host-owned decision projection; repeated deterministic attempts also alternated between conservative refusal and malformed JSON. P074-010 therefore completed with the separately qualified P074-026 Qwen fallback. To mark this item `done`, qualify both refusal/revision and exact reviewed-candidate admission without treating model output as host authority, then refresh the private evidence. This branch is now non-gating alternative evidence. |
| P074-013 | Qualify the `node-b` Qwen3-Coder MLX solver binding | done | The exact `mlx-community/Qwen3-Coder-30B-A3B-Instruct-5bit` revision, immutable model-card identity, asset digests/sizes, staged MLX runtime, canonical package, lifecycle/conformance reports, resource envelope, and Solver correctness/regeneration checks are retained and admitted on `node-b`; incomplete artifacts are refused before hashing or package projection. The 2026-08-28 P074-010 run used this exact binding for both model-generated experiments and passed its post-effect revalidation. Private evidence remains host-local and the checked descriptor carries only stable non-secret identity. |
| P074-014 | Qualify the `node-c` Qwen2.5-Coder GGUF reviewer/facilitator binding | done | The exact `Qwen/Qwen2.5-Coder-7B-Instruct-GGUF` revision and `Q4_K_M` artifact, immutable identity, staged `llama-server`, canonical package, lifecycle/conformance reports, GNU/Linux resource envelope, and separate Reviewer plus Facilitator real-output checks are retained and admitted on `node-c`. The lifecycle covers install, inference, dirty adoption, upgrade, rollback, retirement, removal, recovery, and final CAS revalidation; shared transition deadlines strictly contain profile warmup. The 7B binding remains correctness evidence but was not selected for the completed physical profile because P074-025 established the faster 3B binding under the same host-validation boundary. |
| P074-015 | Freeze the host-local Node checkout locator | done | Repository paths remain outside the reusable topology. The remote control agent resolves through explicit host-local `ORBIPLEX_ACCEPTANCE_NODE_ROOT`, requires an absolute canonical Git worktree whose agent path is below that root, compares exact revision/profile evidence across hosts, and removes the locator from product child environments and retained aggregates. The local executor binds its own current checkout directly. Live preflight on 2026-08-27 reached all three configured roots at one clean synchronized revision and proceeded through planning and execution; missing, non-canonical, divergent, dirty, or child-inherited locator cases remain fail-closed. Supports P074-008. |
| P074-016 | Extract a reusable physical story-runtime adapter | done | `federation_story_runtime.py` is the story-neutral stratum over checked plans and host executors for parallel builds, node-local materialization/evidence, bounded process lifecycle, private credential retrieval, scoped cleanup, redacted manifests, and exact-origin direct product calls. Both deterministic P074-009 and real-model P074-010 consume it. The retained 2026-08-28 Story 012 run completed the second live consumer, including restart, authenticated product calls, vfkit lifecycle, evidence assembly, cleanup, and lease release. Optional communication recordings are evaluated on their owner hosts and only closed results cross the control channel; this preserves the same ownership boundary instead of widening the adapter with remote private-path access. |
| P074-017 | Add private qualified model-binding inventory and host admission | done | The closed host-only `ORBIPLEX_ACCEPTANCE_MODEL_BINDINGS` inventory joins stable binding refs to checked public descriptors and private runtime, model, package, lifecycle, qualification, and execution-root evidence through the shared P064 validators. Admission and post-effect revalidation reject incomplete, extra, symlinked, digest-drifted, stale, platform-incompatible, under-resourced, or non-executable material while returning only closed redacted evidence. The 2026-08-28 physical run admitted all three exact bindings and retained passing post-effect revalidation for `node-a`, `node-b`, and `node-c`. Selected shared-managed storage remains governed independently by P074-011. |
| P074-018 | Add reusable physical vfkit image and workspace admission | done | `federation_vfkit_admission.py` verifies one closed digest-bound vfkit bundle, refuses symlinked/incomplete input, derives an owner-exclusive short same-volume workspace within the Unix-socket budget, APFS-clones the guest disk and mutable EFI/NVRAM template, and verifies the consumed target bytes. The leased host-agent prepare/cleanup operations are consumed through `PhysicalStoryRuntime`, while `federation-node.v1` retains only redacted paired evidence. The 2026-08-28 physical run passed live clone preparation, actual PowerDNS guest consumption, workspace cleanup, and final evidence validation. This completes the vfkit role needed by P074-010; P074-011 still tracks broader shared-input roles. |
| P074-019 | Separate physical product bind addresses from routable host identity | done | The private topology carries one digest-bound literal `product/bind-address` per slot; checked planning and host preflight reject DNS, loopback, multicast, wildcard, non-unicast, or non-owned values. Product listeners bind this address while advertised peer endpoints and TLS identity retain `host/name`. Corpus keeps its plaintext backend private and advertises the planned `wss://` Room service through the bounded supervised TLS terminator. The retained 2026-08-28 run proved cross-host join and send, restart/reconnect, direct product routing, and cleanup without SSH forwarding. Single-host profiles retain their loopback defaults. |
| P074-020 | Stabilize macOS acceptance-daemon identity and firewall admission | todo | Define and implement an operator-owned local signing profile for acceptance binaries that listen on the physical network. Use one persistent macOS code-signing identity, a stable bundle identifier/designated requirement, an explicit post-build signing step, and a bounded verification command before launch. Provide an idempotent, separately invoked operator script for one-time Application Firewall `--add`/`--unblockapp` admission of the exact signed executable; never disable the firewall or grant a path whose signature does not match the declared identity. Preflight reports only redacted signature and firewall posture, distinguishes a missing operator setup from a product failure, and retains Linux/no-firewall portability. The current 2026-08-27 probe found linker-generated ad-hoc identities on both macOS builds; `turbo.local` had an allow rule for the checkout path while `self.local` had the Application Firewall disabled, so path-only consent is not evidence of stable code identity. Add macOS rebuild coverage proving that two binaries signed by the same local identity retain admission, and document certificate creation/import, rotation, revocation, and non-interactive CI limitations. The operator runbook must distinguish Application Firewall admission from Local Network privacy. Apple documents automatic Local Network admission for `launchd` daemons, root programs, and CLI tools run from Terminal or SSH; as a broader machine policy, macOS 15.5+ also supports root-owned `AllowedEthernetLocalNetworkAddresses` and `AllowedWiFiLocalNetworkAddresses` CIDR preferences that require restart. The harness must never mutate those system-wide preferences; it may diagnose and document them as an explicit operator alternative for dedicated acceptance hosts. This is an operational hardening follow-up and does not gate the current explicitly supervised P074-010 run. |
| P074-021 | Supervise detached physical-host processes explicitly | done | A bounded host-local supervisor remains the direct parent and process-group owner, preserves the sanitized environment and host-owned cwd, records locale/timezone-stable identities, and exits with the child. The any-host executor retains and reaps the local/SSH control session as process ownership only; product traffic is never forwarded. Status/signaling fence PID reuse and termination covers the owned group. Regression tests cover readiness, normal exit, signals, logs, session reaping, and survivor refusal. The retained 2026-08-28 run proved the exact macOS HTTP clients and listeners remained usable under this supervision through the complete passage and that cleanup left no supervised product survivors. This closes lifecycle supervision; P074-020 remains separate optional signing/firewall hardening. |
| P074-022 | Add an explicit resumable exploration passage distinct from acceptance evidence | in-progress | Implement the reviewed non-default `exploration-retain` posture as four strata: a pure closed checkpoint and deterministic resume-plan contract; owner-host atomic checkpoint persistence plus inspection; runtime `retain`, `status`, `resume-plan`, and bounded `cleanup`; and a thin Story-012 adapter that maps Story-owned steps, effects, authorities, and ephemeral resources without teaching them to the core. The checkpoint binds retained process/control-session identity, component dependencies, model/image target-byte receipts, storage-policy identity, repository revision, clock/lease facts, completed and ambiguous effects, cleanup-owned resources, and the exact next Story step. Resume revalidates those facts, restarts only the invalidated dependency closure, and refuses changed topology/profile/repository digests, expired or widened authority, uncertain effect completion, lost required supervision, or a checkpoint after cleanup. Retention renews only the same orchestrator's leases with a bounded exploration TTL; an expired or explicitly interrupted run admits a same-identity cleanup-scoped takeover whose closed command set cannot resume product work. V1 code changes start a new passage; resumable parameter repair must preserve the bound profile. A new orchestrator may inspect and clean but cannot adopt an unattached surviving process as supervised. Closure requires deterministic fault injection, one physical interrupt/resume and cleanup exercise, and a subsequent fresh default green run; retained evidence is never promotable. Depends on P074-008 and P074-021 and does not retroactively change P074-010 evidence. |
| P074-023 | Bind Story-owned native output constraints without weakening host validation | done | The physical model-start contract accepts an optional Story-owned GBNF path plus digest, snapshots and revalidates the regular file in the private per-slot run tree, and rejects symlinks, path escape, digest drift, unsupported runtimes, incomplete pairs, and mutation. Only the closed `--grammar-file <snapshot>` pair reaches qualified `llama_server`; host parsing and policy remain the semantic admission boundary. Receipts retain the grammar digest and `runtime-gbnf+host-validated` posture without private paths or grammar text. Local/SSH parity, no-constraint behavior, cleanup, and refusal paths are covered. The retained 2026-08-28 physical report carries exact constraint receipts for both constrained runtime owners, `node-a` and `node-c`, and their ordinary post-effect model revalidations passed. |
| P074-024 | Separate full Sensorium observation evidence from its bounded model-facing projection | done | After complete schema admission, the host now derives a closed `agent-observation-terminal-viewport-projection.v1` value bound to the full content digest. It retains terminal/session and sequence identity plus viewport geometry, cursor, and text, omits duplicated classification/provenance already carried by prompt tiers and operational caution, rejects unsupported schemas, and enforces a separate 4 KiB projection ceiling. The full payload remains host-owned evidence; persistent operational traces record only projection schema/digest and full-content digest. Pure projection, oversized refusal, end-to-end prompt assembly, trace persistence, and exact production-strata tests are green. Review also removed a duplicated lower-authority copy of both the role instruction and terminal bytes and made solver-claimed fields explicit. The final 2026-08-28 Qwen2.5-Coder 3B bench used 1,095 prompt tokens, compared with 1,172 before the deduplication. Depends on P074-017. |
| P074-025 | Qualify a hardware-appropriate physical reviewer binding for `node-c` | partial | P074-014's Qwen2.5-Coder 7B remains immutable correctness evidence but exceeded the current two-core Broadwell timing envelope. The selected Qwen2.5-Coder 3B Q4_K_M candidate uses native GBNF plus host semantic validation, a conservative 6 GiB host minimum, and exact Reviewer plus Facilitator role qualification. Production-shaped work exposed that narrative-first grammar anchored verdicts on the pre-effect `NXDOMAIN`; placing `verdict` first for non-revision reviews fixed that representation without weakening the JSON contract or host authority. On the actual two-core Broadwell `node-c`, fresh no-retry populations passed 5/5 complete-plan acceptances and 5/5 defective-plan `request-regeneration` verdicts, with observed p95/max durations of 156,195 ms and 156,728 ms. The retained 2026-08-28 P074-010 run admitted this exact binding, produced the real reviewer product, and passed its post-effect revalidation. Later physical passages exposed that those populations did not qualify the distinct reviewer-only correction from a host-refused false denial to `accept`; P074-027 and P074-031 completed that recovery contract with a different co-located binding. The earlier GGUF evidence remains valid but partial for this additional semantic population, while a second invalid review still fails closed and the host never synthesizes or coerces `accept`. |
| P074-026 | Qualify a grammar-constrained Qwen2.5-Coder 3B Chair fallback for `node-a` | done | The exact Qwen2.5-Coder 3B Q4_K_M bytes were transferred over the LAN through an `.incomplete` target, rehashed before atomic publication, and packaged with the pinned self-contained `c588c4f4` macOS arm64 Metal `llama-server`. The canonical package, P064 v2 lifecycle/conformance, 6 GiB resource envelope, and Chair qualification are green. The startup grammar is the closed union of Chair, Experiment Executor, and final inert-draft operation contracts; each caller still accepts only its own exact marker, and a marker from another operation is a typed refusal. The retained 2026-08-28 run proved ordinary execution of this grammar across both experiments, exact Chair admission, final inert draft production, and post-effect binding revalidation. The Bielik MLX evidence remains retained under P074-012 as a non-gating alternative rather than being rewritten as this completed fallback. |
| P074-027 | Qualify reviewer-only semantic correction over immutable host facts | done | The Story-012 runner and production-shaped reviewer bench share one pure correction-prompt constructor and one independent semantic validator. The validator keeps mutation scope anchored only in current host evidence, admits package-owned syntax examples only as directive evidence, and evaluates proposal-scoped claims clause by clause so a true statement about the pre-effect configuration cannot be mistaken for a false statement about the proposed fix. It refuses incompatible verdicts, absent attribution, retained false assumptions, invented post-effect evidence, or a missing bounded next test. The selected P074-031 Qwen3-Coder MLX Reviewer subsequently passed the unchanged correction contract 5/5 with no retry through the reviewed whole-JSON response boundary; the host added no marker, field, default, verdict, finding, or test. The fresh P074-032 run then exercised that binding through four real deliberation cycles and passed the model-generated Reviewer-product assertion. Earlier 3B, 7B, Phi-4, and marker-framed Qwen3 failures remain valid negative evidence rather than being rewritten as qualification. |
| P074-028 | Evaluate a co-located Reviewer node on `self.local` with the solver-admitted Qwen3-Coder bytes | partial | The production-shaped Reviewer bench added an MLX physical-package path that verifies exact package assets, runtime identity, host memory, and a distinct private PEX root while retaining the source binding's existing `solver` role. Its first marker-framed gate ran the unchanged P074-027 prompt and host validator as five no-retry samples on `self.local`: p95/max was 3,996 ms, but all five responses omitted the mandatory typed marker and `redundant-actions`, yielding 0/5 contract admissions. The host refused every near-miss and granted no Reviewer role. The ledger is `${ORBIPLEX_ACCEPTANCE_REPORT_ROOT}/p074-028/qwen3-colocated-reviewer-20260830.jsonl`, SHA-256 `3bdbdaa4beb562cd68bedc790f9a95e4be9399d77500726ebb2b2d0e97bc63e5`. P074-031 subsequently superseded only that framing choice with a reviewed whole-JSON boundary and qualified a distinct Reviewer binding; P074-032 then completed the co-located profile with a separate runtime. This item remains partial historical evidence for the rejected marker-framed variant rather than being relabeled as its successor. One shared server remains rejected as evidence for the current independent-runtime claim. |
| P074-029 | Add a Codex-backed Reviewer adapter for the physical `node-c` profile | todo | Implement a bounded model-provider adapter on the weaker `node-c` host so its distinct Reviewer Agent can use Codex while `node-c` remains the third real physical Node, Room participant, authority boundary, and owner of its acceptance evidence. Preserve the Story-owned Reviewer role contract, P074-033 typed host-claim validation, correction limit, timeout/cost/action budgets, and fail-closed behavior; the adapter must not inherit ambient Node authority, expose operator credentials in reports, or turn Codex output into host-authored evidence. Qualify the adapter independently with fresh production-shaped no-retry populations, then run the exact three-physical-host Story-012 profile over the real network and retain node-local plus aggregate evidence. Report this as Codex-backed three-node interoperability evidence, not as local-model or offline acceptance, and keep the existing GGUF binding as separate retained evidence rather than silently replacing its identity. Depends on a reviewed Codex adapter contract, P074-008, P074-017, P074-021, P074-022, P074-027, and P074-033. |
| P074-030 | Add an explicit `physical-two-host-three-node` diagnostic topology | done | The topology schema and pure Rust planner now accept only an explicit `shared-physical-hosts` posture for co-location, derive logical/physical cardinality, preserve the shared failure domain in the aggregate, and force `diagnostic-not-promotable` at the export schema. Host preflight compares the configured and observed partitions so DNS/SSH aliases cannot inflate evidence. The Story adapter selects the explicit profile, keeps unique endpoints and roots, and supports slot-selected private inventories and policies through one fail-closed `{slot}` locator placeholder. Valid co-location, undeclared duplication, alias inflation, false co-location, overlapping roots, duplicate endpoints, report ceiling, and unchanged three-host behavior pass the focused Python, Rust, and schema-gate suites. |
| P074-031 | Qualify the co-located Qwen3-Coder MLX Reviewer binding | done | The exact P074-013 Qwen3-Coder MLX model and runtime bytes now have a distinct `node-c` Reviewer binding and runtime ref. Because MLX 0.30.2 exposes no native grammar/JSON-schema request boundary, the reviewed `typed-json-object` framing requires one whole-response closed JSON value and never adds a marker, field, default, verdict, finding, or test. The independent host validator still checks exact shape and P074-027 host-fact semantics. After the host-fact validator fixes were reviewed, a fresh production-shaped five-sample population passed 5/5 with no retry (warmup 2,391 ms; p95/max 3,005 ms; total sample time 9,167 ms). Its prompt-bearing private ledger is `${ORBIPLEX_ACCEPTANCE_REPORT_ROOT}/p074-031/qwen3-colocated-reviewer-overlay-20260830.jsonl`, SHA-256 `9bb677dd72465c261d455a7225b67001705a830b53f3d4bb39be54707be31618`. The 24-hour private qualification report has SHA-256 `7144fa39cb8ce6a5fb73719e5695dea947eaaedca39b4b32552cbc0c497246fb`; the ordinary binding validator rechecked its descriptor, package, lifecycle, role, memory, and output-contract identity. |
| P074-032 | Exercise Story-012 resume and fresh deliberation over two physical hosts and three logical Nodes | done | The retained exploration run `federation-run:story-012-physical-two-host-three-node-real-model:20260830T014817Z` injected loss of only the co-located `node-c` daemon, moved from checkpoint 1 to checkpoint 2 after restarting only that component, proved an all-reuse second plan, journaled every cleanup resource, and finished `cleaned`. The subsequent fresh run `federation-run:story-012-physical-two-host-three-node-real-model:20260830T033741Z` passed all ten Story assertions, all three model post-effect revalidations, and all node cleanup. Its redacted aggregate has SHA-256 `0f2b15b8d991837f9a352481262f151a205a7c4dbe06fc587afa452ce5350c4a`; its paired Story report has SHA-256 `27dfbe58dcc183c1032ee6df8998b93ac33c54b8757643f1fd066f109a95e8ef`. The report records three logical Nodes, two physical hosts, the shared `node-b`/`node-c` failure domain, and `diagnostic-not-promotable`; it therefore does not satisfy P074-010 or the exact three-host closure clause of P074-022. Depends on P074-008, P074-017, P074-021, P074-022, P074-030, and P074-031. |
| P074-033 | Replace Reviewer prose adjudication with typed host-checked claims | partial | The generic `corpus-deliberation-review-claims.v1` envelope and signed `corpus-reasoning-experiment-review.v3` are canonical, mirrored into Node, Schema-Gate admitted, and validated by the pure Corpus core. They carry opaque subject, predicate, object, modality, evidence, disposition, and next-move refs plus bounded semantically inert commentary; they install no PowerDNS or universal domain ontology. Story 012 owns the first closed `review-claim-profile:story-012-powerdns-v1` catalog-select specialization. The host projects immutable admissible claims from the same plan, policy, lifecycle, and observation facts used for effect admission, and accepts only exact catalog entries and a profile-legal next move. Unknown combinations, contradictions, duplicates, missing evidence, unsupported subjects, or narrative attempts to select disposition/effect/test fail closed. Typed correction state, signed v3 lineage, report projection, qualification identity, and focused malformed/correction tests are implemented. Reviewer-contract selection is now an explicit task-profile property independent of runtime topology, every current discovery transport uses v3, prompt and bench helpers require an explicit mode, and the bench defaults to typed JSON. The compatible critique-gated v2 path still uses prose adjudication, including `_review_claims_proposal_omits_directive`; therefore the replacement criterion is not yet complete. P074-031 supplied the fresh 5/5 no-retry whole-JSON Reviewer qualification because MLX 0.30.2 has no native grammar or JSON-Schema boundary; this retained measurement used the typed path despite the previously weaker generic bench default. The full run `federation-run:story-012-physical-two-host-three-node-real-model:20260831T193333Z` then passed with three real runtimes, four model-authored experiments, four typed envelopes with empty inert commentary, no fallback, exact `a`/`b`/`c` DNS assertions, closed traces, cleanup, 701,996 ms of deliberation, and 958,375 ms total. Its paired Story report has SHA-256 `759145ed615bf6d4a823d30b501f655c159456691ee0bbc25f39a063867fe3e7`. The real passage used the direct valid typed path; correction retry remains focused-test evidence. Closure requires migrating or retiring the v2 prose path and deleting its NL adjudicator after its compatibility decision. The two-host evidence remains `diagnostic-not-promotable`; generic profile admission is P069-DOMAIN-005 and the Codex-backed third-host adapter remains P074-029. Depends on completed P069-CLAIM-001, P074-027, and P074-031. |
