# Proposal 094: Operator Task Packs for Bounded Problem Solving

Based on:

- [Proposal 024: Capability Passports and Network Ledger Delegation](024-capability-passports-and-network-ledger-delegation.md)
- [Proposal 049: JSON-e Middleware](049-json-e-middleware-transformer-executor.md)
- [Proposal 058: Contact Catalog](058-contact-catalog.md)
- [Proposal 062: Temporal Storage Convention](062-temporal-storage-convention.md)
- [Proposal 069: Corpus](069-corpus.md)
- [Proposal 071: Sensorium Workbench](071-sensorium-workbench.md)
- [Proposal 072: Capability Registry](072-capability-registry.md)
- [Proposal 073: Agent](073-agent-orchestration-organ.md)
- [Proposal 083: Sensorium Interactive Interfaces](083-sensorium-interactive-interfaces.md)
- [Proposal 085: Operator-Sovereign Extensibility and Experiment Packages](085-operator-sovereign-extensibility-and-experiment-packages.md)
- [Proposal 088: Pull-Based Artifact Acquisition](088-pull-based-artifact-acquisition.md)
- [Proposal 090: Inference Execution Provenance](090-inference-execution-provenance-and-non-local-disclosure.md)
- [Proposal 091: File-Backed Configuration and Explainable Composition](091-file-backed-configuration-and-explainable-composition.md)
- [Solution 028: Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md)
- [Solution 038: Corpus](../60-solutions/038-corpus/038-corpus.md)
- [Solution 048: Operator-Sovereign Extensibility](../60-solutions/048-operator-sovereign-extensibility/048-operator-sovereign-extensibility.md)
- `node:DEV-GUIDELINES.md`

Related:

- [Story 013: An Operator Task Pack Repairs qmail Local Delivery in a Disposable VM](../30-stories/story-013-qmail-task-pack.md),
  the accepted qmail reference story and acceptance contract (`P094-002`).
- [Proposal 093: Package-Scoped Private Capabilities](093-package-scoped-private-capabilities.md),
  when a future task pack exports new callable package behaviour. Version 1 of this
  proposal composes registered host capabilities and does not depend on P093.

## Status

`draft`

This proposal defines a candidate contract and implementation sequence. Names of new
schemas, Rust crates, routes, and DTOs below are design candidates, not claims about
currently registered schemas or implemented APIs. Existing P069, P071, P083, P085,
P088, P090, and P091 mechanisms are antecedents, not evidence that this composition
already exists.

## Date

`2026-09-25`

## Executive Summary

An Orbiplex operator should be able to install a reviewed package that says, in effect:

> This node is prepared to deliberate about a bounded class of problems, advertise
> that readiness, run experiments in a pinned Sensorium environment, verify results,
> and restore the environment afterwards.

Today the required mechanisms exist separately. Corpus can describe a domain-general
deliberation. Agent and Inquirium can execute bounded reasoning. Sensorium Workbench can
run exact command profiles and patches in an isolated environment. Sensorium Interfaces
can expose observations and actuators through explicit grants and leases. P085 can
install, validate, activate, revoke, and roll back a signed operator experiment package.
The Service Offer Catalog can advertise services. What is missing is a small,
cross-domain contract that composes those mechanisms into one operator-understandable
product without becoming a second authority system.

This proposal introduces an **operator task pack**. Its portable core is an immutable,
signed set of exact references and digests carried as a semantic entry in an existing
P085 package. A separate **local binding** selects machine-local paths, image variants,
runtime choices, publication identity, pricing, and human-in-the-loop policy. A resolved
task plan is therefore the intersection of:

1. the portable package ceiling;
2. current local operator intent;
3. current host capability, grant, lease, revocation, and resource state.

The pack never turns prose into ambient shell authority. Prose may describe the goal,
constraints, and requested outcome of a deliberation. Every observation and effect still
crosses its existing typed boundary. Commands are admitted by exact Workbench command
profiles, patches by artifact-backed patch policy, and interactive operations by current
Sensorium Interface grants and leases. Missing authority, substituted content, stale
bindings, unavailable verifiers, and runtime egress not explicitly admitted all refuse.

The first complete exemplar is a qmail problem-solving pack. It prepares a pinned VM,
admits read-only inspection first, permits only reviewed qmail configuration and service
operations, verifies local delivery and the absence of an open relay, and tears down or
recreates the VM as rollback. The qmail example validates a domain-independent contract;
qmail semantics do not enter the shared core.

## Problem Statement

### Mechanisms exist, but the operator must compose them by hand

An operator can already configure a Workbench command profile, prepare a VM, activate an
experiment package, configure Corpus, select an inference flow, and publish a service
offer. These are separate acts with separate identifiers and failure modes. Their
correctness depends on the operator manually preserving relationships such as:

- the advertised thematic profile matching the one admitted by Corpus;
- the VM image matching the command and verifier assumptions;
- the inference flow staying within the package and local resource ceilings;
- the current command profiles matching the exact scripts or executables tested by the
  package author;
- publication being withdrawn when activation, operator authority, or local readiness
  disappears;
- a verifier observing the intended result without gaining mutation authority;
- rollback being possible after a partially completed experiment.

This is excessive cognitive load for a reusable operator product. It also encourages
configuration by convention: matching strings, local paths, and prose become an implicit
contract that no single boundary validates.

### Prose is useful evidence, not executable authority

A request such as "configure qmail to accept mail from the local host" is a valid
problem statement. It is not a safe execution plan. It leaves unresolved:

- which qmail installation and operating system are in scope;
- which files and service manager may be changed;
- whether networking is disabled, isolated, or externally reachable;
- which commands can inspect or mutate state;
- what "accept mail" means operationally;
- how to prove the node did not create an open relay;
- which state must be retained as evidence;
- how to restore the environment after failure.

The system must preserve the expressiveness of prose while compiling effects into a
closed, inspectable plan. A model may propose a plan, but only host-owned validators and
current grants may admit it.

### A task pack must not become a new plugin framework

P085 already owns signed package ingress and activation. P069 owns thematic semantics.
P071 owns Workbench command and patch execution. P083 owns interactive observation and
actuation. P072 and P024 own host and delegated authority. A task pack that reimplements
any of these would create a parallel authority path and make revocation ambiguous.

The missing layer is composition: exact identities, compatibility, local binding,
readiness, publication coordination, and evidence linkage.

## Goals

- Let an operator install one signed package describing a bounded problem-solving
  capability across Corpus, Agent, Inquirium, Workbench, and Sensorium Interfaces.
- Preserve a domain-general Corpus contract: programming, mail administration,
  scientific analysis, media work, and other domains use the same composition model.
- Separate portable package facts from machine-local operator choices and transient
  execution authority.
- Produce an inspectable readiness result explaining exactly why a task profile is or is
  not publishable or runnable, led by one decisive blocker and its next operator action.
- Keep operator-authored configuration to choices that have no safe default. Digests,
  generations, capability lists, and portable facts are derived, never hand-copied.
- Create ordinary Service Offer Catalog entries without making package activation itself
  a publication action.
- Compile prose and model proposals into a closed experiment plan made from exact,
  registered action kinds.
- Recheck mutable authority and revocation at every effect boundary.
- Reuse P085 lifecycle, Bounded Deferred Operations, Replay Scheduler, Artifact Delivery,
  Host-Owned Module Store, Schema Gate, and existing domain stores.
- Make refusal, verification, rollback, and degraded operation first-class.
- Provide one complete qmail exemplar and acceptance profile before general promotion.

## Non-Goals

- A general package manager, shell-script marketplace, or universal plugin framework.
- Treating natural-language instructions, model output, package signatures, or service
  offers as execution authority.
- Defining qmail-specific semantics in shared Node crates.
- Installing interpreters, system packages, VM images, or models implicitly during
  package activation.
- Allowing a task pack to mint primitive capabilities, passports, grants, leases, or
  operator bindings.
- Replacing Corpus thematic profiles, Workbench command profiles, Sensorium Interface
  descriptors, or P085 activation records with task-pack-local equivalents.
- Publishing automatically when a package becomes active.
- Hiding local pricing, resource, privacy, HIL, or egress decisions inside the portable
  package.
- Full autonomous remediation of the operator's host. Version 1 runs experiments only
  inside explicitly bound Sensorium environments.
- Defining package-scoped callable capabilities. P093 owns that optional future surface.

## Terminology

- **Task pack** – a signed P085 package containing one or more task-profile semantic
  entries and their immutable assets.
- **Task profile** – the portable, content-addressed composition contract for one class of
  problems.
- **Local binding** – host-owned operator configuration that maps a task profile to local
  environments, runtimes, publication identity, limits, and HIL policy.
- **Resolved task plan** – immutable result of intersecting the task profile, current
  package activation, local binding, capability state, and current runtime inventory.
- **Readiness** – prompt-free host evaluation of whether a profile is currently
  installable, publishable, runnable, verifiable, and rollback-capable.
- **Candidate plan** – untrusted Agent or model output naming closed action kinds and
  profile refs; it carries no digests, capabilities, effect classes, HIL flags, or
  binding identity.
- **Experiment plan** – host-validated plan derived from a candidate: every step carries
  its exact profile digest, derived effect class, and derived HIL requirement. No
  free-form command string is executable merely because it appears in a plan.
- **Contained environment** – an exclusive, disposable Sensorium environment instance
  that satisfies the containment predicate in
  [Containment, rollback, and uncertain outcomes](#containment-rollback-and-uncertain-outcomes).
  Recovery is classified for the instance as a resource, not for each change inside it.
- **Effective value** – the result of narrowing one axis (HIL, network, limits, impact
  class, runtime selection) across the portable, local, and current-use layers, recorded
  with the layer that decided it.
- **Verifier** – read-only or otherwise explicitly constrained observer whose result is
  evidence consumed by a host-owned evaluator.
- **Offer draft** – unsigned, non-public projection assembled from the portable profile
  and local binding before ordinary Service Offer signing and publication.
- **Task run** – one causally linked deliberation and experiment attempt under an exact
  resolved task plan.

## Resolved Decisions

Recorded on `2026-09-25`.

1. **Carrier.** Version 1 task profiles are P085 semantic entries. The existing
   `operator-experiment-package.v1` remains the portable container. No parallel package
   lifecycle is introduced.
2. **Schema stability.** The first slice does not modify the P085 package schema. The
   package's existing semantic-entry tuple binds the task profile by exact domain, ref,
   revision, implementation, and digest. If implementation proves that envelope
   insufficient, a versioned P085 contract change is required rather than a hidden
   sidecar convention.
3. **One schema, many domains.** The shared task profile describes composition and exact
   artifact identities. Domain meaning stays in thematic profiles, command profiles,
   interface descriptors, verifier contracts, and package assets owned by their domains.
4. **Portable/local split.** Machine paths, credentials, live endpoints, provider
   identity, pricing, local runtime choice, current grants, and current leases are never
   portable task-profile authority. They belong to the local binding or current runtime.
5. **No prose execution.** Prose is admitted as a problem statement or reasoning input.
   It may propose actions, but it cannot name arbitrary shell commands or widen an
   allowed action.
6. **No free-form shell.** Version 1 experiment plans use a closed action algebra whose
   process and service operations resolve to exact Workbench command profiles. Support
   scripts are immutable package assets with pinned digests and narrow command profiles.
7. **Current-use fencing.** Activation generation, operator binding, task-profile digest,
   local-binding digest, capabilities, grants, leases, revocations, command profiles,
   image identity, verifier identity, and resource ceilings are rechecked before every
   effect.
8. **Publication is separate.** Activation can make a profile locally resolvable. It
   cannot advertise it. Ordinary host-owned Service Offer creation, signing, and
   publication remains a distinct operator action.
9. **Withdrawal is monotone locally.** Once local readiness or authority disappears, new
   local admission refuses immediately. Catalog withdrawal is reconciled asynchronously
   and remains operator-visible; catalog lag never restores local authority.
10. **Network default.** Runtime network access uses the Workbench environment
    `network/profile` vocabulary and is `none` or `isolated`: an explicitly isolated
    backend network with no uplink, NAT, or default route. `egress-allowlisted` and any
    other external egress require a separately reviewed capability and runtime contract;
    the task pack cannot create it. The per-process `network` policy of a command
    profile is a different layer and not this axis.
11. **Verifier separation.** A verifier emits bounded observations. A host-owned evaluator
    decides pass or fail. A verifier that requires mutation must use an explicit action
    profile and cannot be presented as read-only verification.
12. **Rollback preference.** Teardown and recreation from a pinned image or prepared
    system is preferred over reverse mutation. An exact bounded rollback profile is
    allowed where recreation is impractical.
13. **Storage.** P085 remains the source of truth for package lifecycle. Domain owners
    retain task-run, Agent, Corpus, Workbench, and Interface facts. A task-pack service may
    build projections and causal links but must not duplicate those logs.
14. **No hidden fallback.** A missing profile, image, runtime, command profile, verifier,
    grant, or lease refuses. The host must not silently substitute a similar local
    resource.
15. **Qmail first.** The first acceptance pack targets local qmail administration in a
    pinned VM and proves that no qmail-specific branch exists in the shared core.
16. **Derived, not declared, effect semantics.** A step's capability, effect class, and
    HIL requirement are derived from owner-owned sources: the Sensorium action-semantics
    map, the command profile's effect mode, the patch policy, and the Interface
    descriptor. A candidate plan cannot state them; a model claiming `read-only` for a
    mutating command would otherwise invert trust. Where an owner's effect source is
    missing, the derivation takes the more restrictive value (`mutation`) instead of
    guessing. A missing action-semantics row has no restrictive default, because no
    capability can be derived: pack-fact derivation fails and conformance does not pass.
17. **Version 1 recovery scope.** The first slice admits only `observation` steps and
    `contained-mutation` steps inside a contained environment. The environment instance,
    not each change inside it, carries the P080 class `ephemeral-revertible`, through a
    versioned P080 extension adding resource kind `isolated-environment` with the typed
    disposer `environment.destroy` (`P094-018`). Any other effect, including every
    Interface actuation, refuses with `plan/recovery-class-not-admitted` until
    `P094-017` admits it under the P080 recovery contract and P093 outcome semantics.
    Version 1 therefore needs no per-step domain reconciliation, but it still needs one
    owner reconciliation: the environment owner must durably confirm destruction before a
    run with an uncertain step terminalizes.
18. **One narrowing rule per axis algebra.** Every value that appears on more than one
    layer belongs to an axis with an explicit algebra: `meet` for restriction axes,
    `member` for set-valued choices, and `bounded-by` for the impact-class check. None
    relies on declaration order or a derived `Ord`. A local binding that states a less
    restrictive value than the portable ceiling is refused, not silently clamped;
    current-use state may narrow further without refusal.
19. **Operators do not author digests or generations.** The bind operation fills the
    accepted task-profile digest from the current package. Activation generation is a
    current-use fact and never appears in the binding, so reactivation and P085 rollback
    do not stale operator configuration. A changed profile digest blocks the binding
    until the operator reviews a ceiling diff and re-accepts it.
20. **Pause is reversible; revoke is terminal.** A binding may be `paused`: new runs
    refuse, withdrawal of its offer is requested, and a running run stops at its next
    step boundary and has its instance destroyed. Resuming requires no reinstallation,
    activation, or rebinding. P085 revocation remains the terminal stop.
21. **Observation is enforced, never declared.** A step or verifier counts as
    `observation` only when the Workbench enforces its command profile's
    `effect/mode: observation`. A pack author's declaration is not accepted as an
    interim substitute, even though a signed author is more trusted than a model: a
    mislabelled verifier could repair the system and fake success, and a mislabelled
    mutation would bypass HIL. Until the owner enforcement exists (`P094-019`), the
    affected profiles are blocked in readiness, not weakened.

## Authority and Ownership

### Ownership matrix

| Concern | Owner | Task-pack role |
| :--- | :--- | :--- |
| Package signature, install, activation, revoke, rollback | P085 operator-extension service | Carries exact task-profile and asset bindings. |
| Thematic role and deliberation semantics | Corpus/P069 | Supplies exact thematic profile and role/overlay refs. |
| Passage lifecycle and effects proposed by an Agent | Agent/P073 | Executes only under its ordinary grants, budgets, and HIL rules. |
| Inference invocation and model/runtime ceilings | Inquirium/P064 and P085 reusable flows | Resolves exact flow and intersects package/local/runtime ceilings. |
| Command and patch execution | Sensorium Workbench/P071 | Admits exact command or patch profiles and records results. |
| Interactive observation and actuation | Sensorium Interfaces/P083 | Requires current descriptor, grant, control session, and lease. |
| Capability authority | Capability Registry/P072 and passports/P024 | Remains the only origin of host and delegated authority. |
| VM image and prepared-system identity | Sensorium Virt contracts | Supplies exact image, provenance, guest-agent, and prepared-state evidence. |
| Service discovery | Service Offer Catalog | Publishes an ordinary signed offer derived from an operator-approved draft. |
| Large immutable assets | Artifact Delivery/object store/P088 | Transfers content-addressed images, fixtures, scripts, and corpora. |
| Local source composition | P091 | Supplies explainable local bindings without becoming authority. |
| Composition and readiness | P094 | Validates exact cross-domain linkage and produces immutable resolved plans. |

### Three distinct layers

```text
portable task profile
        | exact refs/digests and package ceilings
        v
local operator binding
        | local paths, variants, prices, HIL and narrower limits
        v
current-use admission
        | activation, grants, leases, revocation, inventory and budgets
        v
resolved task plan -> existing domain owners execute their own operations
```

No layer can widen the one above it. The local binding may choose among explicitly
admitted variants or narrow limits. Current-use admission may only narrow or refuse.

### Portable material forbidden from carrying authority

A task profile must not contain:

- secrets, tokens, private keys, passwords, or decryption material;
- machine-local absolute paths;
- live network endpoints or DHCP-derived addresses;
- node, participant, or organization identifiers presented as implicit authority;
- operator signatures or node-operator bindings;
- current grants, leases, sessions, or capability passports;
- a pre-signed Service Offer tied to a local provider identity;
- arbitrary shell source or an unbounded command string;
- an instruction to enable external network egress;
- an ambient model or runtime selector without a closed package ceiling.

These values either belong to an admitted local source, are resolved at current use, or
remain unavailable.

## Contract Family

All names in this section are proposed. Every ingress crosses Schema Gate before semantic
validation. Schemas close security-significant objects with
`additionalProperties: false`; extension fields, where deliberately allowed, are
namespaced and byte bounded.

### `operator-task-profile.v1`

The profile is a portable, immutable composition contract. It contains identifiers and
digests, not the referenced large content.

```json
{
  "schema/v": 1,
  "profile/ref": "operator-task-profile:qmail-local-administration",
  "profile/revision": 1,
  "thematic-profile": {
    "domain": "corpus",
    "entry/ref": "corpus-profile:qmail-administration",
    "entry/revision": 1,
    "implementation/ref": "corpus-profile-implementation:qmail-v1",
    "entry/digest": "sha256:THEMATIC_PROFILE_DIGEST"
  },
  "catalog": {
    "service/type": "orbiplex.problem-solving",
    "offer-template/ref": "operator-task-offer-template:qmail-v1",
    "offer-template/digest": "sha256:OFFER_TEMPLATE_DIGEST",
    "taxonomy/ref": "taxonomy:qmail-administration-v1",
    "taxonomy/digest": "sha256:TAXONOMY_DIGEST",
    "topics": ["mail/qmail", "mail/local-delivery", "mail/relay-policy"]
  },
  "deliberation": {
    "inference-flow/ref": "operator-inference-flow:qmail-plan-v1",
    "inference-flow/digest": "sha256:FLOW_DIGEST",
    "agent-policy/ref": "agent-policy:qmail-experiment-v1",
    "agent-policy/digest": "sha256:AGENT_POLICY_DIGEST",
    "roles": ["requester", "solver", "reviewer"],
    "limits": {
      "max/passages": 18,
      "max/experiments": 6,
      "max/wall-time-ms": 1800000
    }
  },
  "environment": {
    "image-variants": [
      {
        "variant/ref": "image-variant:qmail-debian13-amd64",
        "image-manifest/ref": "sensorium-virt-image:qmail-debian13-amd64-v1",
        "image-manifest/digest": "sha256:IMAGE_MANIFEST_DIGEST"
      }
    ],
    "prepared-system/ref": "sensorium-prepared-system:qmail-v1",
    "prepared-system/digest": "sha256:PREPARED_SYSTEM_DIGEST",
    "runtime-network/ceiling": "none",
    "impact-class/max": "test"
  },
  "workbench": {
    "command-profiles": [
      {
        "ref": "sensorium-command-profile:qmail-showctl-v1",
        "digest": "sha256:COMMAND_PROFILE_DIGEST"
      }
    ],
    "patch-policy/ref": "sensorium-patch-policy:qmail-control-files-v1",
    "patch-policy/digest": "sha256:PATCH_POLICY_DIGEST"
  },
  "interfaces": {
    "observation-descriptors": [],
    "actuation-descriptors": []
  },
  "experiment": {
    "input-schema/ref": "schema:operator-task-qmail-input.v1",
    "input-schema/digest": "sha256:INPUT_SCHEMA_DIGEST",
    "candidate-schema/ref": "schema:operator-task-experiment-candidate.v1",
    "candidate-schema/digest": "sha256:CANDIDATE_SCHEMA_DIGEST",
    "first-step/class": "observation",
    "hil/mode": "each-mutation"
  },
  "verifier": {
    "ref": "operator-task-verifier:qmail-local-delivery-v1",
    "digest": "sha256:VERIFIER_DIGEST",
    "command-profile/ref": "sensorium-command-profile:qmail-verify-v1",
    "command-profile/digest": "sha256:VERIFY_COMMAND_PROFILE_DIGEST",
    "result-schema/ref": "schema:operator-task-verifier-result.v1",
    "result-schema/digest": "sha256:VERIFY_RESULT_SCHEMA_DIGEST"
  },
  "rollback": {
    "mode": "recreate-prepared-system",
    "ref": "operator-task-rollback:qmail-v1",
    "digest": "sha256:ROLLBACK_DIGEST"
  },
  "required-capability/ids": [
    "sensorium.workbench.terminal",
    "sensorium.workbench.file",
    "sensorium.workbench.patch",
    "sensorium.virt.host"
  ],
  "resource-envelope/ref": "resource-envelope:qmail-experiment-v1",
  "resource-envelope/digest": "sha256:RESOURCE_ENVELOPE_DIGEST",
  "refusal-corpus/ref": "refusal-corpus:qmail-task-pack-v1",
  "refusal-corpus/digest": "sha256:REFUSAL_CORPUS_DIGEST"
}
```

Every digest and the `required-capability/ids` list above are build outputs, not
hand-authored values; see [Authoring and binding tooling](#authoring-and-binding-tooling).
The profile does not restate the package's `operational/class`, which P085 defines as a
caution floor composed by `max` with every participating source's impact class. It
answers a different question: `environment.impact-class/max` names the highest
environment impact class for which the pack is qualified. The two are not merged: the
first raises caution, the second refuses an environment. A profile that
admits more than one image variant lets the local binding choose one; with exactly one
variant, the binding carries no image choice.

The semantic-entry registration binds this file using domain
`operator-task-profile`. Its exact tuple `(domain, entry/ref, entry/revision,
implementation/ref, entry/digest)` supplies the canonical profile identity. The payload
therefore does not contain its own digest or its containing package digest; either would
create a circular content-addressing dependency. Registration does not activate, bind,
publish, or execute the profile. The profile bytes are an immutable package asset. The
domain-owned registry loads those bytes only after verifying the exact tuple and digest;
the tuple is not a substitute for carrying or validating the referenced payload.

The containing P085 manifest must list a superset of every profile
`required-capability/ids` value in its own `required-capability/ids`, must list every
referenced resource envelope in `resource-envelope/refs`, and must bind every
package-owned reusable inference flow used by the profile. Mismatch is package conformance failure, not a reason
to infer or copy the missing declaration.

### `operator-task-local-binding.v1`

The local binding is host-owned and source-aware. It is a P091-resolved projection, not
a portable package asset and not authority by itself.

```json
{
  "schema/v": 1,
  "binding/ref": "operator-task-local-binding:qmail-on-workbench-a",
  "binding/state": "enabled",
  "package/ref": "extension-package:qmail-operator-pack",
  "task-profile/ref": "operator-task-profile:qmail-local-administration",
  "task-profile/digest": "sha256:PROFILE_DIGEST",
  "workspace": {
    "root/ref": "workspace-root:qmail-lab",
    "backend/ref": "sensorium-virt-backend:cloud-hypervisor"
  },
  "inference": {
    "model-profile/ref": "model-profile:qwen-coder-local",
    "runtime/ref": "model-runtime:local-openai-compatible"
  },
  "publication": {
    "enabled": true,
    "provider/participant-ref": "participant:LOCAL_PROVIDER",
    "price-policy/ref": "price-policy:qmail-lab-v1",
    "availability-policy/ref": "availability-policy:qmail-lab-v1"
  },
  "safety": {
    "hil/mode": "each-mutation",
    "runtime-network": "none",
    "max/concurrent-runs": 1
  }
}
```

The binding contains only choices the profile leaves open. It cannot restate a portable
fact such as the prepared-system ref, the single image variant, or the verifier: such
fields are not representable, so a package upgrade cannot leave a stale copy behind.

Field ownership is explicit:

- **Operator choices without a safe default:** workspace root and backend, and the
  inference model/runtime when the flow's package ceiling admits more than one. A
  binding lacking one of them is refused with `local-binding/incomplete`.
- **Operator choices with a safe default:** `safety` values default to the most
  restrictive admissible value (strictest HIL, runtime network `none`, one concurrent
  run); `publication.enabled` defaults to `false`; `binding/state` defaults to
  `enabled`. The operator widens a default only by an explicit edit, which inspection
  foregrounds as widening.
- **Host-filled on bind or re-accept:** `task-profile/digest`, copied from the current
  package's resolved semantic entry. The operator never types a digest.
- **Absent by design:** activation generation, local binding digest, and revision
  counters. The generation is read at resolution and recorded in the resolved plan and
  run facts; the binding digest is computed from the canonical resolved binding and
  identifies the revision.

The stored binding may use stable logical roots such as `workspace-root:qmail-lab`.
Resolution to an absolute local path happens inside the owning Workbench or environment
provider and is omitted from portable inspection and remote status.

### Narrowing axes

One table governs every value that exists on more than one layer. Each axis names its
algebra; inspection shows the effective value and the layer that decided it.

| Axis | Portable | Local binding | Current use | Algebra |
| :--- | :--- | :--- | :--- | :--- |
| HIL mode | `experiment.hil/mode` | `safety.hil/mode` | current host policy, for example risk-raised HIL from the P085 caution class | `meet`; `each-step` restricts more than `each-mutation` |
| Runtime network | `environment.runtime-network/ceiling` | `safety.runtime-network` | environment inventory | `meet`; `none` restricts more than `isolated` |
| Deliberation limits | `deliberation.limits` | optional narrower `deliberation.limits` | remaining Agent and Inquirium budgets | `meet` by `min` per limit |
| Concurrency | resource envelope | `safety.max/concurrent-runs` | capacity reservation | `meet` by `min`, minimum 1 |
| Model and runtime | package ceiling of the reusable flow | `inference` selection | runtime inventory | `member` |
| Image variant | `environment.image-variants` | selection when more than one | image inventory | `member` |
| Impact class | `environment.impact-class/max` | – | effective `impact/class` of the bound Workbench environment | `bounded-by` under the P085 risk order `research < experimental < test < production < critical` |

`meet` takes the more restrictive value through an explicit per-axis rank or `min`.
`member` requires the choice to be admitted by the portable set and present in current
inventory. `bounded-by` does not choose a value: the environment keeps its own class,
and the check refuses with `environment/impact-class-exceeded` when that class ranks
above the pack's qualification. Impact class and restriction are different algebras and
share no ordering code.

Version 1 closes HIL to two modes; plan-level approval is a deferred extension. A local
value less restrictive than its ceiling refuses with
`local-binding/outside-package-ceiling` naming the axis; current-use narrowing is
recorded but does not refuse unless the result is empty.

The P085 operator attention budget is not an axis. The effective HIL mode decides
whether a step needs a question; a separate attention gate then decides whether that
question is delivered, grouped, deferred, or denied, and only the operator's answer
approves. When no question can currently be delivered, readiness reports the `effects`
stage as `degraded` with `hil/attention-unavailable`.

### `operator-task-readiness.v1`

Readiness is an explainable projection of one local binding, not a grant:

```json
{
  "schema/v": 1,
  "binding/ref": "operator-task-local-binding:qmail-on-workbench-a",
  "local-binding/digest": "sha256:LOCAL_BINDING_DIGEST",
  "task-profile/ref": "operator-task-profile:qmail-local-administration",
  "task-profile/digest": "sha256:PROFILE_DIGEST",
  "activation/generation": 7,
  "evaluated-at": "2026-09-25T12:00:00Z",
  "stages": {
    "package": {"state": "ready", "evidence/refs": ["audit:package-7"]},
    "binding": {"state": "ready", "evidence/refs": ["config:qmail-on-workbench-a"]},
    "environment": {"state": "ready", "evidence/refs": ["image:verified"]},
    "deliberation": {"state": "ready", "evidence/refs": ["flow:conformant"]},
    "effects": {"state": "ready", "evidence/refs": ["command-profiles:current"]},
    "verification": {"state": "ready", "evidence/refs": ["verifier:current"]},
    "rollback": {"state": "ready", "evidence/refs": ["recreate:available"]},
    "publication": {"state": "blocked", "refusal/code": "publication/policy-missing"}
  },
  "blockers": [
    {
      "stage": "publication",
      "refusal/code": "publication/policy-missing",
      "next-action": "edit-binding"
    }
  ],
  "advertisement": {"state": "none"},
  "runnable": true,
  "publishable": false
}
```

Each stage is `ready`, `degraded`, `blocked`, `not-applicable`, or `not-evaluated`:

- `degraded` means usable under a narrower effective value than the binding requested,
  for example reduced concurrency; it carries a code and never masks `blocked`;
- `not-applicable` means the profile or binding does not use the stage, for example
  `publication` when `publication.enabled` is `false`;
- `not-evaluated` means a stage it depends on is blocked. `package` precedes `binding`;
  both precede the six execution stages; all precede `publication`. One root cause
  therefore produces one blocker, not a cascade.

Two effect-mode checks are static, so readiness catches them before any deliberation
is spent:

- a profile whose `first-step/class` is `observation` needs at least one admitted
  command profile with Workbench-enforced `effect/mode: observation`; otherwise the
  `effects` stage is `blocked` with `workbench/effect-mode-missing`;
- the verifier's command profile must have Workbench-enforced `effect/mode:
  observation`; otherwise the `verification` stage is `blocked` with
  `verifier/effect-mode-missing`.

The run-time refusal `plan/first-step-not-observation` remains for a candidate that
ignores an observation profile that does exist.

The derived fields follow closed rules:

- `runnable` holds when `package`, `binding`, `environment`, `deliberation`, `effects`,
  `verification`, and `rollback` are each `ready` or `degraded`, and `binding/state` is
  `enabled`;
- `publishable` holds when `runnable` holds and `publication` is `ready`;
- `blockers` lists every `blocked` stage in stage order; the first entry is the decisive
  blocker, and its `next-action` comes from the refusal table, not from prose;
- `advertisement.state` is `none`, `publication-pending`, `committed`, or
  `withdrawal-pending`, projected from the publication facts.

Readiness cannot conceal an omitted or unknown stage. It is computed on read from
current snapshots by the pure resolver and is not persisted; only slow inventory facts,
such as image presence, are cached by their owners with an observation time.

### `operator-task-offer-draft.v1`

An offer draft combines package-owned descriptive facts with local price, availability,
provider identity, and accepted policy annotations. It is unsigned and non-public. The
ordinary catalog host validates it, emits the canonical Service Offer, obtains the
required signature, and publishes it through the existing path.

The resulting Service Offer must carry an exact task-profile identity in a reviewed,
namespaced extension field. Whether this becomes an explicit Service Offer field or a
bounded `policy_annotations` member is left to `P094-007`; it must not be introduced as
an undocumented convention. Receiver admission compares the exact profile ref and digest
before accepting a task request.

### `operator-task-experiment-candidate.v1` and `operator-task-experiment-plan.v1`

Two shapes separate untrusted proposal from admitted plan. The Agent or model emits a
**candidate**; the host validates it and emits the **plan**. A profile may bind a
task-specific candidate schema that narrows the shared one, for example by closing the
admitted kinds or argument shapes; it may not widen it.

Action kinds and their operations are closed:

| Kind | Owner | Candidate names | Host derives |
| :--- | :--- | :--- | :--- |
| `observe` | Workbench | command-profile ref and arguments | digest; capability from the action-semantics map; class `observation` only if the profile's owner-enforced effect mode is `observation`, otherwise refused as not an observation |
| `observe` | Sensorium Interface | descriptor ref and operation `read` or `subscribe` | digest; operation must be in the descriptor's `access/modes`; capability from the map; class `observation`; current grant |
| `process` | Workbench | command-profile ref and arguments | digest; capability from the map; class from the profile's effect mode, `mutation` when absent |
| `patch` | Workbench | patch-policy ref and patch artifact ref | digest; capability from the map; class `mutation`; bounded target set from the patch policy |
| `service-control` | Workbench | command-profile ref and action | digest; capability from the map; class `mutation`; no ambient service-manager shell |
| `actuate` | Sensorium Interface | descriptor ref, operation `invoke`, and `method/name` | digest; capability from the map; outside containment, so refused in Version 1 |

Interface management operations, such as grants, control sessions, and leases, are
host and operator operations, never candidate operations. A `mutation` becomes
`contained-mutation` only when the bound environment is contained; otherwise it refuses
with `plan/recovery-class-not-admitted`.

A candidate names only refs that occur in the resolved task plan. It never carries
digests, capabilities, effect classes, HIL flags, binding identity, or activation
generation; those fields are not representable in its schema, which also keeps the
model's output small:

```json
{
  "schema/v": 1,
  "steps": [
    {
      "step/id": "inspect-qmail",
      "kind": "observe",
      "profile/ref": "sensorium-command-profile:qmail-showctl-v1",
      "arguments": []
    },
    {
      "step/id": "apply-control-patch",
      "kind": "patch",
      "profile/ref": "sensorium-patch-policy:qmail-control-files-v1",
      "patch/ref": "artifact:sha256:PATCH_DIGEST"
    }
  ]
}
```

The host stores the patch bytes as a content-addressed artifact before validation. The
validated plan stamps identity and derived facts:

```json
{
  "schema/v": 1,
  "plan/ref": "operator-task-plan:run-01",
  "candidate/digest": "sha256:CANDIDATE_DIGEST",
  "task-profile/digest": "sha256:PROFILE_DIGEST",
  "local-binding/digest": "sha256:LOCAL_BINDING_DIGEST",
  "activation/generation": 7,
  "steps": [
    {
      "step/id": "inspect-qmail",
      "kind": "observe",
      "profile/ref": "sensorium-command-profile:qmail-showctl-v1",
      "profile/digest": "sha256:COMMAND_PROFILE_DIGEST",
      "arguments": [],
      "capability/id": "sensorium.workbench.terminal",
      "effect/class": "observation",
      "effect/source": "owner-enforced",
      "hil/required": false
    },
    {
      "step/id": "apply-control-patch",
      "kind": "patch",
      "profile/ref": "sensorium-patch-policy:qmail-control-files-v1",
      "profile/digest": "sha256:PATCH_POLICY_DIGEST",
      "patch/ref": "artifact:sha256:PATCH_DIGEST",
      "capability/id": "sensorium.workbench.patch",
      "effect/class": "contained-mutation",
      "effect/source": "owner-enforced",
      "hil/required": true
    }
  ]
}
```

In Version 1, `effect/class` is `observation` or `contained-mutation`. The recovery of a
`contained-mutation` is the environment's `environment.destroy` disposer; the step is not
separately classified under P080. `hil/required` is a pure function of the effective
HIL mode and the class: `each-step` requires HIL for every step, `each-mutation` for
every step whose class is not `observation`. Validation refuses a candidate whose ref is outside the resolved plan
(`plan/outside-profile`), whose first step is not of the profile's `first-step/class`
(`plan/first-step-not-observation`), or whose derived class is outside the Version 1
recovery scope (`plan/recovery-class-not-admitted`).
The stamped `capability/id` is what the current-use fence checks. `effect/source` is
`owner-enforced` when the class comes from an owner contract, or
`missing-source-default` when the owner source is absent and the step fell back to
`mutation`. Inspection and HIL requests show it, so a question about an apparently
read-only command explains itself.

The host validates the whole plan before the first effect, then rechecks each step at
use. A valid earlier step does not authorize a later one. A changed replay under the same
idempotency key is a terminal conflict.

### `operator-task-experiment-result.v1`

The result links existing domain evidence rather than copying raw transcripts:

- exact task-profile, local-binding, activation-generation, and plan digests;
- Agent passage and Corpus deliberation refs;
- Workbench directive/result refs;
- Interface receipt refs where applicable;
- verifier result and host evaluation refs;
- rollback outcome;
- bounded timings, resource accounting, and typed refusals;
- disclosure metadata indicating which fields may enter a Service Offer or operator
  diagnostic.

Prompts, secrets, raw VM files, command stdout containing private material, and model
chain-of-thought are not copied into the shared result.

### `operator-task-conformance-report.v1`

Conformance binds the exact task-profile digest, package digest, implementation digest,
schema set, `sensorium-action-semantics.v1` map digest, refusal corpus, fixture set,
runtime identity, and result. The profile does not pin the map: when the owner revises
it, the report stops being current and readiness shows `package/conformance-missing`
with `run-conformance`, so a map revision costs one conformance run, not a repackaged
pack. It distinguishes:

- structural schema validity;
- cross-reference and digest validity;
- compatibility and inventory validity;
- refusal-corpus result;
- positive dry-run result;
- optional full environment acceptance result.

Only a current fully passing report may satisfy activation or publication policy where
the profile marks conformance as required.

### Owner-side contracts this proposal requires

P094 consumes, but does not own, several contracts that do not exist yet. Each belongs to
its domain owner and is registered through that owner's review, not as a P094 sidecar:

| Contract | Owner | Purpose | Tracker |
| :--- | :--- | :--- | :--- |
| `sensorium-patch-policy.v1` (new) | Sensorium Workbench | Closed path set, file size, ownership, mode, and accepted content shape for patch admission. Today only patch artifacts and stage/apply results exist. Mirrored in the P071 tracker. | `P094-003`, `P094-008` |
| `sensorium-command-profile.v2` effect mode (new field) | Sensorium Workbench | `effect/mode: observation \| mutation`. `observation` is enforced by the Workbench, not trusted as a label. Absent means `mutation`. Mirrored in the P071 tracker. | `P094-019` |
| `sensorium-action-semantics.v1` (new) | Sensorium Workbench and Interfaces | Versioned map from `(owner, kind, operation)` to a registered capability id and to the effect-class rule: fixed, from the command profile's effect mode, or from the descriptor. Mirrored in the P071 tracker; Interface rows co-owned with P083. | `P094-003`, `P094-008` |
| P080 `isolated-environment` resource kind (extension) | P080 with Sensorium Virt as implementer | `ephemeral-revertible` host-local resource with typed idempotent disposer `environment.destroy` and durable destruction confirmation. | `P094-018` |

Until an owner contract exists, the dependent P094 behaviour refuses or takes the more
restrictive derivation; P094 never supplies the missing semantics itself.

## Lifecycle and State Transitions

The task-pack status of one binding is a projection over facts owned by existing
services, not one mutable enum stored as a second source of truth. The projection takes
the first row whose condition holds, top to bottom:

| Projection | Holds when (owner facts) | New runs | Offer |
| :--- | :--- | :--- | :--- |
| `revoked` | P085 revocation of the package, or of the profile's semantic entry | refuse, terminal | withdrawal requested until committed |
| `draining` | binding `paused`, activation superseded, or readiness lost while runs are still admitted | refuse | withdrawal requested until committed |
| `paused` | binding `paused` and no admitted runs remain | refuse with `local-binding/paused` | withdrawn |
| `advertised` | runnable binding with a committed, not withdrawn offer | admit | committed |
| `bound` | runnable binding, no committed offer | admit local runs | none, or draft pending approval |
| `activated` | current P085 activation, binding missing or not runnable | refuse with the decisive blocker | none |
| `installed` | package stored, not currently active, or conformance not passing | refuse | none |

`publishable` is a readiness field, not a lifecycle state. Leaving `draining` or `paused`
by resuming the binding or restoring readiness requires no reinstallation or
reactivation. `revoked` is terminal under P085; only a new P085 install and activation
can make a profile resolvable again.

Exact retry of a lifecycle operation is idempotent. Reuse of an idempotency key with a
different digest is a terminal conflict. Timeout after an effect's durable admission
point is `unknown` until owner reconciliation; it is never treated as safe refusal.

## Resolution and Admission Logic

### Pure resolution

The pure resolver receives values, not live services:

```text
resolve(task profile,
        package activation snapshot,
        local binding,
        capability snapshot,
        runtime inventory,
        policy ceilings)
  -> ResolvedTaskPlan | TaskPackRefusal
```

Resolution performs:

1. schema and canonical digest verification;
2. exact package semantic-entry binding verification;
3. activation generation and operator-binding comparison;
4. exact cross-reference and implementation availability checks;
5. local choice containment under portable ceilings, one narrowing axis at a time;
6. capability and resource intersection;
7. readiness stage derivation;
8. construction of one immutable plan containing no unresolved alternatives.

The resolver does not read files, contact peers, open databases, start VMs, or mutate
stores. Effectful providers obtain the facts, call the resolver, and recheck current
mutable authority before use.

### Current-use fence

Before every effect, the owning host verifies at least:

- package digest, activation generation, and current operator binding;
- task-profile and local-binding digests, and `binding/state` still `enabled`; a
  paused binding stops a run at the next step boundary, while host-owned environment
  rollback still runs;
- package and implementation revocation;
- required base capabilities and restrictions;
- Agent grant and budget state;
- Workbench command or patch profile digest;
- Sensorium Interface grant, control session, and lease where used;
- image/prepared-system and guest-agent identity, and the containment predicate;
- runtime network ceiling;
- verifier identity and declared non-mutation property;
- task-run cancellation, expiry, and remaining aggregate budgets.

A cache may accelerate lookup but cannot replace this fence. Cache invalidation is
advisory; current authority checks are normative.

### Refusal vocabulary

The implementation uses a closed typed refusal enum. One table gives every code its
readiness stage, retry class, and next operator action; readiness blockers, run results,
CLI, and UI all project this table and author no separate explanation. Stage `run` marks
codes that arise only while validating or executing a run and never appear as readiness
blockers.

Retry classes are closed: `terminal` (the same request never succeeds),
`after-operator-action`, `after-deferred-operation` (a bounded host operation such as
image preparation must finish), `after-owner-reconcile` (an owning domain must change or
reconcile state that the operator cannot change locally), and `transient`.

| Code | Stage | Retry class | Next action |
| :--- | :--- | :--- | :--- |
| `package/not-active` | package | after-operator-action | `activate-package` |
| `package/conformance-missing` | package | after-operator-action | `run-conformance` |
| `package/profile-digest-mismatch` | package | terminal | `inspect-package` |
| `operator/binding-lost` | package | after-operator-action | `rebind-operator` |
| `local-binding/missing` | binding | after-operator-action | `create-binding` |
| `local-binding/incomplete` | binding | after-operator-action | `edit-binding` |
| `local-binding/outside-package-ceiling` | binding | after-operator-action | `edit-binding` |
| `local-binding/profile-changed` | binding | after-operator-action | `review-profile-change` |
| `local-binding/conflict` | binding | after-operator-action | `resolve-binding-sources` |
| `local-binding/paused` | binding | after-operator-action | `resume-binding` |
| `environment/image-mismatch` | environment | terminal | `inspect-environment` |
| `environment/prepared-system-unavailable` | environment | after-deferred-operation | `prepare-environment` |
| `environment/runtime-egress-denied` | environment | after-operator-action | `edit-binding` |
| `environment/impact-class-exceeded` | environment | after-operator-action | `edit-binding` |
| `environment/not-contained` | environment | after-operator-action | `edit-binding` |
| `deliberation/flow-unavailable` | deliberation | after-operator-action | `inspect-deliberation` |
| `capability/missing` | effects | after-operator-action | `grant-capability` |
| `capability/revoked` | effects | after-operator-action | `inspect-capability` |
| `workbench/command-profile-missing` | effects | after-operator-action | `inspect-effects` |
| `workbench/effect-mode-missing` | effects | after-owner-reconcile | `inspect-effects` |
| `interface/grant-missing` | effects | after-operator-action | `grant-interface` |
| `hil/attention-unavailable` | effects | transient | `inspect-attention-budget` |
| `verifier/unavailable` | verification | after-operator-action | `inspect-verification` |
| `verifier/effect-mode-missing` | verification | after-owner-reconcile | `inspect-verification` |
| `rollback/unavailable` | rollback | after-deferred-operation | `prepare-environment` |
| `rollback/destroy-unconfirmed` | rollback | after-owner-reconcile | `inspect-environment` |
| `publication/policy-missing` | publication | after-operator-action | `edit-binding` |
| `publication/disabled` | publication | after-operator-action | `edit-binding` |
| `offer/withdrawal-pending` | publication | after-owner-reconcile | `none` |
| `package/generation-stale` | run | terminal | `start-new-run` |
| `plan/unknown-action-kind` | run | terminal | `none` |
| `plan/outside-profile` | run | terminal | `none` |
| `plan/first-step-not-observation` | run | terminal | `none` |
| `plan/recovery-class-not-admitted` | run | terminal | `none` |
| `plan/changed-replay` | run | terminal | `none` |
| `workbench/patch-outside-policy` | run | terminal | `none` |
| `interface/lease-lost` | run | after-owner-reconcile | `start-new-run` |
| `hil/denied` | run | terminal | `none` |
| `hil/expired` | run | after-operator-action | `start-new-run` |
| `verifier/check-missing` | run | terminal | `inspect-verification` |
| `verifier/mutation-not-admitted` | run | terminal | `inspect-verification` |
| `verifier/timeout` | run | transient | `retry-verification` |
| `run/cancelled` | run | terminal | `none` |
| `run/budget-exhausted` | run | terminal | `start-new-run` |

A next action is a pointer to an operator operation, never an automatic action. The
host does not act on it. `inspect-capability` leads to the revocation fact and its
issuer; a revocation is resolved by that authority, never overridden by a new local
grant. `retry-verification` is admitted only for a verifier whose command profile is
Workbench-enforced `observation`, in the unchanged instance, within the run deadline,
and up to the verifier contract's bounded retry count; the host may perform those
bounded retries itself before reporting the code. When they are exhausted, the run
terminalizes, the instance is destroyed, and the operator starts a new run. `publication/disabled` is reported only when a publication
request is made for a binding with publication off; readiness shows that stage as
`not-applicable` instead.

Unknown codes fail schema validation. A drift check compares this table with the enum. Operator diagnostics may add bounded refs and
digests but never raw secrets, prompts, signatures, absolute paths, or private payloads.

## Service Offer Publication

Activation and publication remain separate for both safety and operator comprehension.
The publication flow is:

1. resolve current task readiness;
2. produce an unsigned offer draft;
3. show portable facts separately from local price, availability, and provider facts;
4. obtain an authenticated operator action and ordinary signing authority;
5. publish through the existing catalog path;
6. retain the returned offer and publication refs in the task projection;
7. reconcile withdrawal when activation or publishability disappears, or the binding
   is paused.

The offer describes readiness to solve a class of problems. It does not promise that
every future request will be admitted. Request admission still checks current capacity,
price policy, thematic-profile compatibility, trust, sanctions, grants, revocations, and
the exact task-profile digest.

## Experiment Semantics

### Prose-to-plan boundary

Natural language can supply:

- desired outcome;
- relevant facts and constraints;
- explanation requested from the solver;
- acceptance criteria that map to a registered verifier schema.

Natural language cannot directly supply:

- an executable path;
- shell syntax;
- environment variables;
- filesystem roots;
- network destinations;
- capability identifiers treated as already granted;
- HIL bypass;
- verifier success.

Agent or model output is parsed as an `operator-task-experiment-candidate.v1`.
Schema Gate rejects unknown action kinds and fields. The task resolver checks that every
action is contained by the exact task profile and local binding. The owning Workbench or
Interface boundary then performs its ordinary authorization again.

### Support scripts

A task pack may include support scripts only as immutable content-addressed artifacts.
Each executable script must have:

- an exact digest and executable identity;
- a narrow Workbench command profile;
- a closed argument schema;
- explicit filesystem roots and environment policy;
- time, output-byte, process, and resource limits;
- a Workbench-enforced effect mode; without one, the script is a mutation;
- positive and refusal fixtures;
- no implicit network access.

The task profile refers to that command profile. It does not embed or concatenate shell
fragments at runtime.

### Verification

The verifier runs after the last admitted mutation and before success is committed. Its
result contains bounded observations and named checks. The host evaluator verifies the
result schema and required check set. Missing checks, unknown checks, digest mismatch,
timeout, mutation outside the verifier profile, or an unavailable verifier refuse
success.

Verification evidence is not equivalent to universal truth. It means only that the
exact verifier observed the exact prepared environment under the recorded plan.

### Containment, rollback, and uncertain outcomes

An environment instance is **contained** when all of the following hold at admission
and are rechecked before each step:

- it is an exclusive instance created for this run from the pinned image and prepared
  system, never reused across runs or shared with another tenant;
- it has no writable host share or shared mount; read-only inputs are content-addressed;
- its effective runtime network is `none`;
- the run uses no Interface actuation and no credential that carries authority outside
  the instance;
- its owner exposes the idempotent `environment.destroy` disposer with durable
  destruction confirmation (`P094-018`).

A binding whose environment cannot be contained, for example one selecting
`isolated` network, is blocked for mutating profiles with
`environment/not-contained`. Version 1 does not attempt to prove that an `isolated`
network reaches nothing outside the instance.

Preferred rollback destroys the instance and recreates it from the pinned image and
prepared-system contract. Where state must survive, an exact rollback profile may
restore declared files or service state; such a profile is outside the Version 1
recovery scope. Compensation is an explicit admitted operation, not inferred Agent
authority.

If a transport or host crashes after an effect admission point, that step's outcome is
`unknown`. Version 1 does not reconcile the step with a domain owner, but it does
reconcile the environment:

1. the run enters `rollback-pending`, and the step stays recorded as `unknown`;
2. the host issues `environment.destroy` for the exact instance;
3. the run terminalizes only after the environment owner durably confirms destruction;
4. restart recovery re-issues the idempotent disposer for every run whose destruction is
   unconfirmed;
5. while destruction stays unconfirmed beyond its bound, the `rollback` stage is
   `blocked` with `rollback/destroy-unconfirmed`, so the binding admits no new run.

The step is never repeated, and a run never resumes inside a recreated instance; a new
run starts from the baseline in a fresh instance. When `P094-017` admits other recovery
classes, recovery consults the owning domain's idempotency and recovery contract under
P080 and P093 semantics and still never blindly repeats the effect.

## qmail Reference Pack

The qmail pack is an exemplar, not a special case in the shared implementation.
[Story 013](../30-stories/story-013-qmail-task-pack.md) is its accepted acceptance
contract: roles, concrete fixture, verifier checks, refusal cases, retained
evidence, and the local and federated profiles.

### Advertised scope

The initial thematic profile covers:

- qmail configuration diagnosis;
- local delivery and queue diagnosis;
- bounded changes to reviewed qmail control files;
- local SMTP injection and delivery verification;
- relay-policy review and verification.

It does not advertise Internet-facing deployment, DNS provisioning, TLS certificate
management, spam filtering, arbitrary package installation, or host repair.

### Prepared environment

The package binds:

- one Debian-based amd64 image manifest with build provenance and guest-agent identity;
- one prepared-system manifest proving the expected qmail installation and baseline
  files;
- `runtime-network/ceiling: none` for the first acceptance profile;
- fixture mailboxes and test messages as content-addressed artifacts;
- absence claims for files or listeners that would invalidate the baseline.

Image acquisition and preparation may happen before a task run. Runtime egress does not
follow from the ability to acquire an image.

### Command and patch profiles

Candidate command profiles include:

- `qmail-showctl` for normalized configuration observation;
- `qmail-qread` for queue observation;
- exact service-status observation;
- bounded local SMTP injection against the prepared instance;
- verifier-only listener and relay checks;
- exact service restart or reload actions where the prepared environment requires them.

The patch policy may admit only declared files such as `control/locals`,
`control/rcpthosts`, `control/defaultdomain`, and their prepared-system equivalents. It
must constrain file size, path set, ownership, mode, and accepted content shape. It must
not admit arbitrary writes below `/etc` or an unrestricted editor command.

### Required execution order

Every qmail step derives `observation` or `contained-mutation`; the pack needs no
recovery class beyond the Version 1 scope. Its observation steps and verifier rely on
command profiles whose Workbench-enforced effect mode is `observation`.

1. inspect the baseline without mutation;
2. produce a typed diagnosis and candidate plan;
3. validate the whole plan against profile and local binding;
4. request HIL for every mutation in the first profile;
5. apply one bounded mutation at a time;
6. observe service and queue state;
7. inject a local test message;
8. run the exact verifier;
9. emit a result linking the deliberation, plan, effects, and verifier evidence;
10. tear down or recreate the VM.

### Verifier checks

The first verifier requires all of:

- the qmail service is healthy under the prepared service manager;
- a local test message is accepted and reaches the expected local mailbox or queue state;
- the listener scope matches the profile;
- relay attempts outside the admitted local policy are rejected;
- no unexpected qmail control files changed;
- runtime network remained within the declared ceiling;
- the verifier itself performed no mutation outside its exact profile.

## Implementation Recommendations

This section is informative design guidance. Implementers must still follow
`node:DEV-GUIDELINES.md` and the owning contracts.

### Strata

#### L0: `operator-task-pack-core`

A small pure Rust crate should own data and deterministic logic:

- DTOs for task profiles, local bindings, inventory snapshots, readiness, resolved
  plans, action plans, and typed refusals;
- semantic validation after Schema Gate;
- exact digest and cross-reference checks;
- ceiling intersection;
- compatibility and readiness resolution;
- action containment validation;
- no Axum, Tokio runtime, SQLite, filesystem, process, clock, randomness, network, or
  daemon dependency.

Illustrative shape:

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExactRef<T> {
    pub reference: T,
    pub digest: Sha256Digest,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ArtifactRef(String);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct TaskProfileRef(String);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PackageRef(String);

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum TaskAction {
    Observe(ObserveAction),
    Process(ProcessAction),
    Patch(PatchAction),
    ServiceControl(ServiceControlAction),
    Actuate(ActuateAction),
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ResolvedTaskPlan {
    pub task_profile: ExactRef<TaskProfileRef>,
    pub package: ExactRef<PackageRef>,
    pub local_binding_digest: Sha256Digest,
    pub activation_generation: u64,
    pub deliberation: ResolvedDeliberation,
    pub environment: ResolvedEnvironment,
    pub admitted_actions: Vec<AdmittedActionProfile>,
    pub verifier: ResolvedVerifier,
    pub rollback: ResolvedRollback,
    pub effective_limits: EffectiveTaskLimits,
}

pub fn resolve_task_plan(
    input: &TaskResolutionInput,
) -> Result<ResolvedTaskPlan, TaskPackRefusal>;

pub fn validate_experiment_plan(
    resolved: &ResolvedTaskPlan,
    candidate: &ExperimentPlan,
) -> Result<ValidatedExperimentPlan, TaskPackRefusal>;

pub fn build_offer_draft(
    resolved: &ResolvedTaskPlan,
    publication: &ResolvedPublicationBinding,
) -> Result<OfferDraft, TaskPackRefusal>;

pub fn derive_readiness(
    input: &TaskResolutionInput,
) -> TaskReadiness;
```

Derived step facts are typed so that no call site can take them from the candidate:

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum StepClass {
    /// Owner-enforced observation: Interface read/subscribe, or a command profile
    /// whose Workbench-enforced effect mode is `observation`.
    Observation,
    /// Mutation inside a contained environment; recovery is the instance's
    /// `environment.destroy` disposer, not a per-step P080 class.
    ContainedMutation,
    /// Any other effect. Version 1 refuses it (`plan/recovery-class-not-admitted`);
    /// mapping it to P080 classes belongs to `P094-017`.
    Uncontained,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedStep {
    pub step_id: StepId,
    /// Exact ref and digest resolved from the plan, not copied from the candidate.
    pub action: TaskAction,
    /// From the owner-owned `sensorium-action-semantics.v1` map.
    pub capability: CapabilityId,
    /// From the map's effect rule and the owner source it names; `mutation` when the
    /// owner source is absent, then contained or not by the environment predicate.
    pub class: StepClass,
    /// `OwnerEnforced` or `MissingSourceDefault`; shown to the operator.
    pub class_source: EffectSource,
    /// `hil_required(effective_hil_mode, class)`; never read from input.
    pub hil_required: bool,
}
```

The refusal table is one exhaustive `match`, so a new code cannot compile without a
stage, retry class, and next action:

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct RefusalSpec {
    pub stage: RefusalStage,
    pub retry: RetryClass,
    pub next_action: NextAction,
}

impl TaskPackRefusalCode {
    pub const fn spec(self) -> RefusalSpec {
        use RefusalStage as S;
        use RetryClass as R;
        use NextAction as N;
        match self {
            Self::PackageNotActive => RefusalSpec { stage: S::Package, retry: R::AfterOperatorAction, next_action: N::ActivatePackage },
            Self::PlanOutsideProfile => RefusalSpec { stage: S::Run, retry: R::Terminal, next_action: N::None },
            // every other variant, with no wildcard arm
        }
    }
}
```

Each axis algebra is a separate, explicit operation. None relies on a derived `Ord`,
because declaration order is an accident of the source and impact class is not a
restriction order:

```rust
/// Restriction axes: HIL mode, runtime network, limits, concurrency.
pub trait RestrictionAxis: Copy + Eq {
    const AXIS: AxisName;
    /// The more restrictive of two values. Enums implement it through an explicit
    /// rank table; numeric limits through `min`.
    fn meet(self, other: Self) -> Self;
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Effective<T> {
    pub value: T,
    pub decided_by: Layer, // Portable | Local | CurrentUse
}

/// Refuses when `local.meet(ceiling) != local`, i.e. the binding asks for more than the
/// ceiling; current use may only narrow.
pub fn meet_layers<T: RestrictionAxis>(
    ceiling: T,
    local: Option<T>,
    current: Option<T>,
) -> Result<Effective<T>, TaskPackRefusal>;

/// Set-valued choices: model/runtime and image variant.
pub fn member<T: Copy + Eq>(
    admitted: &[T],
    local: Option<T>,
    available: &[T],
) -> Result<Effective<T>, TaskPackRefusal>;

/// Impact class is checked, not chosen: the environment keeps its own class.
/// `risk_rank` is an explicit table of the P085 order.
pub fn bounded_by_impact_max(
    environment: ImpactClass,
    max: ImpactClass,
) -> Result<ImpactClass, TaskPackRefusal>;
```

Security-significant variants use exhaustive enums. Unknown wire values are rejected,
not mapped to permissive defaults. Conversion errors retain field context and a stable
typed refusal.

#### L1: host composition service

Start by extending the existing operator-extension host only if it can retain a narrow
contract. Mint a separate `operator-task-pack-service` crate only when independent
lifecycle, testing, or a second consumer creates contract pressure. Do not create a
crate merely to move files.

The host layer obtains snapshots and delegates effects through consumer-side ports:

```rust
pub trait TaskCatalogPort: Send + Sync {
    fn request_publish(
        &self,
        request: PublishOfferRequest,
    ) -> Result<DeferredOperationRef, TaskHostError>;

    fn request_withdraw(
        &self,
        request: WithdrawOfferRequest,
    ) -> Result<DeferredOperationRef, TaskHostError>;
}

pub trait TaskEnvironmentPort: Send + Sync {
    fn inventory(&self, request: EnvironmentInventoryRequest)
        -> Result<EnvironmentInventory, TaskHostError>;

    fn request_prepare(
        &self,
        request: PrepareEnvironmentRequest,
    ) -> Result<DeferredOperationRef, TaskHostError>;
}

pub trait TaskExperimentPort: Send + Sync {
    fn submit_validated_plan(
        &self,
        plan: ValidatedExperimentPlan,
    ) -> Result<TaskRunRef, TaskHostError>;
}

pub trait TaskAuditPort: Send + Sync {
    fn append_fact(&self, fact: TaskAuditFact) -> Result<(), TaskHostError>;
}
```

These ports are deliberately task-oriented but not domain-authoritative. Catalog,
Workbench, Agent, and Interface implementations still validate their own contracts.
The task host cannot reach their stores directly or infer success from transport
completion.

Avoid a god orchestrator. The host builds an immutable plan, submits typed operations to
owners, and links returned refs. It does not interpret qmail, execute shell, sign offers,
or mutate another domain's projection.

#### L2: daemon composition and HTTP

The daemon maps layered configuration into local-binding sources, constructs handles,
registers routes, and owns lifecycle start/stop. HTTP routes perform authentication,
body/query parsing, Schema Gate admission, and one host call. Domain logic does not move
back into route handlers or `EndpointRuntimeContext`.

Candidate operator surfaces:

```text
GET  /v1/operator/task-packs
GET  /v1/operator/task-packs/{profile_ref}
POST /v1/operator/task-bindings
GET  /v1/operator/task-bindings/{binding_ref}/readiness
GET  /v1/operator/task-bindings/{binding_ref}/profile-change
POST /v1/operator/task-bindings/{binding_ref}/accept-profile
POST /v1/operator/task-bindings/{binding_ref}/state
POST /v1/operator/task-bindings/{binding_ref}/offer-draft
POST /v1/operator/task-bindings/{binding_ref}/publish
POST /v1/operator/task-bindings/{binding_ref}/withdraw
POST /v1/operator/task-bindings/{binding_ref}/runs
GET  /v1/operator/task-runs/{run_ref}
```

Operational routes are keyed by binding, not by profile. One profile may have several
bindings, for example two Workbench environments, and readiness, offers, and runs belong
to exactly one of them. `POST /task-bindings` creates a binding with safe defaults and
host-filled digests; `profile-change` returns the per-axis ceiling diff between the
accepted and current profile digest; `accept-profile` records the new digest;
`state` switches between `enabled` and `paused`.

These names remain candidates until their schemas and authorization are reviewed. Read
surfaces expose metadata, refs, digests, stage states, and bounded refusals only.

### Reuse of host primitives

- **Schema Gate** validates every contract family member before semantic use.
- **P085 lifecycle** owns package install, activation generation, operator binding,
  revocation, rollback, conformance, and refusal corpus.
- **Host-Owned Module Store** may retain bounded local-binding projections, cursors, and
  operation refs. It must not become a second copy of domain event logs.
- **Bounded Deferred Operations** execute image preparation, offer publication,
  withdrawal, and similarly slow host-owned operations.
- **Replay Scheduler** reconciles interrupted publication, withdrawal, provisioning, and
  stale-readiness work with bounded retries and visible terminal states.
- **Artifact Delivery and P088 acquisition** move large immutable images, fixture sets,
  support scripts, and refusal corpora by digest.
- **Temporal Storage Convention** applies if the task host introduces new durable facts.
  Current projection tables are rebuildable; write paths append facts and update
  projections transactionally.
- **Shared HTTP runtime** supplies timeout, byte, concurrency, redirect, and TLS bounds.
  No task-pack-specific unbounded client is added.

### Configuration shape

P091 should expose one explainable collection of local bindings. A candidate JSON shape
is:

```json
{
  "operator_task_packs": {
    "enabled": true,
    "bindings": [
      {
        "source": {
          "type": "file",
          "path": "operator-task-packs/qmail-on-workbench-a.json"
        }
      }
    ]
  }
}
```

The configuration names sources only; the binding ref comes from the source content, so
it is stated once. The path is local configuration, not portable package data. P091
source provenance must remain visible in inspection. A duplicate binding ref with unequal
content is `local-binding/conflict`, not last-writer-wins.

Binding-mutating routes (`create`, `accept-profile`, `state`) write through P091 only to
a host-writable source. For an operator-owned read-only file they return the exact
updated canonical binding and do not take effect until that file changes. Either way
there is no hidden second copy.

### Authoring and binding tooling

Most cross-reference burden is mechanical and should never reach a human:

- **One derivation, two callers.** A pure `derive_pack_facts(assets) -> PackFacts`
  computes every profile digest, the profile `required-capability/ids` by looking up
  each admitted `(owner, kind, operation)` in the versioned owner-owned
  `sensorium-action-semantics.v1` map recorded by the conformance report, the manifest
  superset, and refusal-corpus coverage of registered codes. Author tooling
  writes its output into the package; conformance recomputes it and refuses any
  difference. The two can therefore not drift.
- **Bind fills, operator chooses.** `POST /task-bindings` starts from safe defaults,
  fills `task-profile/digest`, and asks only for choices without a safe default.
- **Profile change as a diff.** When a package upgrade changes the profile digest, the
  binding blocks with `local-binding/profile-changed`, and `profile-change` shows only
  axes and refs that differ, marking each as narrowing, widening, or substitution. Accept
  is one action; the operator does not edit digests.

### Persistence and causal linkage

Prefer links over copies. If a task composition journal is needed, its facts should be
small and causal:

```text
task-binding-accepted
task-offer-publication-requested
task-offer-publication-committed
task-offer-withdrawal-requested
task-offer-withdrawal-committed
task-run-admitted
task-run-terminalized
```

Readiness evaluations are not journaled: readiness is recomputed on read, and a loss of
readiness that matters is recorded where it has a consequence, as the cause carried by
`task-offer-withdrawal-requested` or by a run's terminal refusal. Pausing, resuming, and
accepting a changed profile are binding changes and appear as `task-binding-accepted`
with the new binding digest.

Each fact carries the task profile and local binding digests, activation generation,
causation/correlation ids, and refs to owner-domain evidence. It does not duplicate
prompts, VM output, offer bodies, grants, or Workbench results. If such a journal is
introduced, replay-equivalence and as-of-retention behaviour follow Solution 028.

### Concurrency, retries, and cancellation

- Admission atomically reserves profile, operator, capacity, and aggregate resource
  budgets before starting an effect.
- Per-profile and per-binding concurrency ceilings are explicit positive integers.
- Idempotency keys bind exact request digests.
- Retryability is data separate from error text.
- Cancellation is monotone and checked between steps; it does not claim to undo an
  already admitted effect.
- Timeout after the durable start point produces `unknown` until reconciled.
- Revocation closes new admission synchronously and requests bounded termination or
  draining according to owner policy.
- Background loops are bounded, power-policy aware where appropriate, restart-safe, and
  expose prompt-free status.

### Security and privacy review checklist

- Authorize before every effect, not only before plan creation.
- Treat absent authority as denial and unknown enum members as invalid.
- Never infer identity or authority from task labels, thematic topics, file names, or
  model prose.
- Revalidate canonical paths inside the owning environment boundary.
- Keep network `none` by default and make any wider mode independently visible.
- Keep secrets in host-owned secret providers; task profiles carry only refs.
- Redact command output and verifier details before operator or federated projection.
- Never export chain-of-thought as task evidence.
- Ensure diagnostics cannot enumerate private package assets or local absolute paths.
- Test revocation, changed replay, stale generation, lost operator binding, verifier
  substitution, image substitution, and lease loss before testing the happy path.

### Testing strategy

The implementation should begin with executable contracts and refusal-first tests:

1. schema fixtures for every proposed contract;
2. pure property tests proving ceiling intersection is monotone, commutative where
   applicable, idempotent, and never widens authority;
3. table tests for every readiness stage and refusal code, plus a drift check between the
   refusal table in this proposal, the schema enum, and `TaskPackRefusalCode::spec`;
4. candidate-to-plan tests proving that effect class and HIL requirement are unaffected
   by any candidate content, and that a wider local value refuses on each narrowing
   axis;
5. changed-replay and concurrent-revocation tests;
6. lifecycle replay tests across restart, including pause and resume;
7. Workbench tests proving unknown commands and out-of-policy patches refuse;
8. Interface tests proving lost grants or leases refuse at use;
9. verifier tests proving missing checks and mutation attempts refuse success;
10. crash-after-admission tests proving an `unknown` step recreates the environment and
    is never repeated;
11. publication tests proving activation does not publish and revocation or pause
    refuses locally before asynchronous withdrawal completes;
12. end-to-end qmail acceptance from clean package install through teardown and revoke.

No test may satisfy an authority assertion merely by inspecting source markers. It must
reach the owning boundary and observe the admitted or refused result.

## Failure Modes and Required Behaviour

| Failure | Required behaviour |
| :--- | :--- |
| Package installs but task-profile semantic entry is unknown | Installation may remain inert; conformance/activation for the task profile refuses. |
| Local binding names a runtime outside the package ceiling | Terminal binding refusal; no fallback runtime. |
| Prepared image is unavailable | Readiness reports blocked; optional acquisition is an explicit deferred operation. |
| Model returns a shell command | Plan parsing or action containment refuses it unless it resolves to an exact admitted command profile. |
| Operator revokes package during a run | New steps refuse; current owner applies its bounded cancellation/draining policy; offer withdrawal is scheduled. |
| Catalog withdrawal fails temporarily | Local admission remains closed; status shows withdrawal pending and retries remain bounded. |
| Verifier times out | Task cannot succeed yet; bounded retry only for an observation-mode verifier in the unchanged instance, then terminalize, destroy, and start a new run. |
| Verifier mutates state unexpectedly | Refuse verification, record policy violation, and execute rollback policy if admitted. |
| Sensorium Interface lease expires between planning and actuation | Actuation refuses at use; no transparent lease renewal. |
| Same idempotency key carries changed plan bytes | Terminal `plan/changed-replay`. |
| Host restarts after an effect starts | Recover from owner-domain facts; never infer safe retry from missing response. |
| Task profile is compatible but local HIL is stricter | Stricter local HIL wins. |
| Offer remains cached by a peer after revocation | Provider refuses locally; signed offer validity and normal catalog reconciliation bound remote staleness. |
| Candidate names a ref outside the resolved plan or claims its own effect class | Terminal `plan/outside-profile`, or schema refusal for the unrepresentable field; nothing executes. |
| Operator denies or lets a HIL request expire | That step does not run; the run terminalizes with `hil/denied` or `hil/expired` and the instance is destroyed. |
| Package upgrade changes the task-profile digest | Binding blocks with `local-binding/profile-changed`; runs and publication refuse until the operator accepts the diff; the old offer is withdrawn. |
| Operator pauses a binding during a run | The run stops at the next step boundary, its instance is destroyed, and offer withdrawal is requested; resume needs no reactivation. |
| Step outcome is `unknown` after a crash in Version 1 | The run enters `rollback-pending`; the host issues idempotent `environment.destroy`; the run terminalizes only after owner-confirmed destruction; the step is never repeated. |
| Environment destruction cannot be confirmed | `rollback` stage blocks with `rollback/destroy-unconfirmed`; the binding admits no new run; restart recovery keeps re-issuing the disposer. |
| Binding selects `isolated` network for a mutating profile | `environment/not-contained`; no mutation is admitted in Version 1. |
| Command profile lacks an owner-enforced effect mode | Readiness blocks statically with `workbench/effect-mode-missing` or `verifier/effect-mode-missing` where observation is required; other steps derive `mutation` with `effect/source: missing-source-default`. |
| Action-semantics map revised by its owner | Conformance report stops being current; readiness shows `package/conformance-missing` until conformance reruns. |

## Operator Experience

The primary view should answer four questions without requiring the operator to inspect
every underlying subsystem:

1. What problem class does this pack claim to support?
2. Which portable and local facts make that claim concrete?
3. What is currently blocking publication or execution?
4. Which action would widen effects, network, cost, or retention?

The initial screen is one row per binding: lifecycle projection, the decisive blocker
with its next action, and any effective value that differs from the binding's request.
Drill-down uses stable refs into package activation, thematic profile, Workbench
profiles, environment, verifier, rollback, and publication. It must not flatten all
domain state into one giant status object.

Load-reducing rules:

- **One blocker first.** Dependent stages report `not-evaluated`, so one cause yields
  one blocker and one next action.
- **Effective values with their decider.** Each narrowing axis shows the effective value
  and the layer that set it, for example "network `none` – package ceiling", so the
  operator knows which layer to change or that no local change helps.
- **Widening is separate.** Raising HIL laxity, network, concurrency, or limits and
  enabling publication are distinct confirmations naming the axis, never side effects
  of saving a binding.
- **Change review is a diff.** A package upgrade presents only changed axes and refs,
  classified as narrowing, widening, or substitution.
- **HIL requests carry decision material.** Each request shows the step, its derived
  effect class with its source, the exact target set or patch diff, and the rollback that would apply;
  model prose is at most secondary context. Delivery passes a separate attention gate:
  the P085 `operator-attention-budget.v1` may deliver, group, defer, or deny a question
  but never approves, and it does not change the effective HIL mode. In
  `each-mutation` mode, distinct mutations are never merged into one approval.
- **Pause before revoke.** The reversible stop is one action; revoke is presented as
  terminal.

The CLI and UI edit the same P091-backed local binding. Neither stores a hidden second
configuration. Human-readable explanations are projections of structured refusal and
provenance data, not separately authored truth.

## Documentation Plan

After implementation and acceptance, add a bilingual operator HOWTO that walks through:

1. inspecting an installed task pack;
2. reviewing its refusal corpus and portable ceilings;
3. creating a local binding from safe defaults and reviewing a profile-change diff;
4. preparing the Sensorium environment;
5. validating readiness;
6. creating and signing an offer;
7. admitting one qmail request;
8. approving bounded mutations;
9. reading verification and rollback evidence;
10. pausing, resuming, withdrawing, and finally revoking the pack.

Until those paths exist, this proposal is the canonical design record. A HOWTO must not
document candidate commands as if they were implemented.

## Implementation Tracker

Status values: `todo`, `in-progress`, `partial`, `done`, `deferred`.

Work is sliced so that each milestone is useful on its own and the widest cross-domain
change comes last:

- **M1 – inspect and dry-run.** `P094-002` to `P094-006` and the read surfaces of
  `P094-012`. An operator installs a pack, creates a binding from safe defaults, reads
  readiness with its decisive blocker, and validates candidate plans with the pure core.
  Nothing executes.
- **M2 – local runs.** `P094-018`, `P094-019`, `P094-008` to `P094-011`, `P094-013`,
  and the run surfaces of `P094-012`. The operator is the requester; runs execute in the pinned VM
  under the Version 1 recovery scope. Nothing is published.
- **M3 – federated offer.** `P094-007`, `P094-016`, and the publication surfaces of
  `P094-012`. A remote requester selects the offer.
- **M4 – promotion.** `P094-014` and `P094-015`.

`P094-018` and `P094-019` are owner work on the M2 critical path that does not depend on
the P094 core; they should start during M1. Until `P094-019` lands, M1 readiness already
shows the qmail pack as blocked with `workbench/effect-mode-missing`, which is the
intended, explained state rather than a defect.

Publication is last because it is not needed to prove the authority boundary and adds
asynchronous reconciliation that would otherwise slow every earlier test cycle.

| ID | Work item | Depends on | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- | :--- |
| `P094-001` | Freeze ownership, portable/local/current-use separation, lifecycle, and authority invariants | – | `done` | This proposal records the resolved design, prohibited portable fields, owner matrix, no-prose-authority rule, no-free-form-shell rule, current-use fence, narrowing axes, derived effect semantics, Version 1 recovery scope, pause/revoke split, publication separation, verifier boundary, rollback preference, and qmail-first acceptance target. This is design completion only, not runtime implementation. |
| `P094-002` | Freeze the qmail reference story and acceptance contract | `001` | `done` | An accepted story names requester, solver, reviewer, thematic profile, prepared environment, bounded actions, mandatory HIL, verifier checks, rollback, refusal cases, and retained evidence without adding qmail branches to shared code. Evidence: [Story 013](../30-stories/story-013-qmail-task-pack.md), accepted on 2026-09-25, names the requester, solver, reviewer, and provider operator; the pinned qmail prepared system and its two-part misconfiguration; the admitted command and patch profiles; per-mutation HIL; seven verifier checks including the open-relay trap; destroy-and-recreate rollback; thirteen refusal cases; retained evidence; the substrate gates; and the local (`P094-013`) and federated (`P094-016`) profiles. |
| `P094-003` | Register the P094 schema family, coordinate owner contracts, and add positive/negative fixtures | `001` | `todo` | Schema Gate covers task profile, local binding, readiness, offer draft, experiment candidate, experiment plan and result, and conformance report. The refusal enum matches the refusal table. Workbench and Interfaces owners register `sensorium-patch-policy.v1` and `sensorium-action-semantics.v1`; the command-profile effect mode is tracked by `P094-019`. Negative fixtures cover arbitrary shell, absolute portable paths, hidden egress, unknown actions, Interface operations outside `access/modes` or `manage` in a candidate, candidate-supplied digests/capabilities/effect classes/HIL flags, binding fields restating portable facts, changed replay, missing digests, and verifier mutation. |
| `P094-004` | Implement the pure task-pack core | `003` | `todo` | A daemon-free crate provides DTOs, semantic validation, exact cross-reference checks, `meet_layers`/`member`/`bounded_by_impact_max` with provenance and no derived-`Ord` dependence, readiness derivation with stage dependencies and decisive blocker, candidate-to-plan derivation of capability, step class, and HIL requirement from owner sources with `mutation` as the missing-source default, the exhaustive refusal spec, `derive_pack_facts` over the action-semantics map, property tests, and no filesystem/network/runtime effects. |
| `P094-005` | Integrate task profiles with P085 semantic entries and lifecycle | `004` | `todo` | Task profiles install inertly through the existing P085 package, inherit the package operational class, recheck operator/package/revocation state and activation generation on use, recompute pack facts at conformance, survive durable restart where applicable, and introduce no second activation store. |
| `P094-006` | Implement P091-backed local binding, readiness, and inspection | `004`, `005` | `todo` | Bindings are created from safe defaults with host-filled profile digests and no generation; `local-binding/incomplete` names missing choices; profile changes block with a per-axis diff and one-step acceptance; pause and resume work without reactivation; readiness is computed on read with one decisive blocker; local absolute paths and secrets remain absent from portable and remote views. |
| `P094-007` | Implement offer draft, signing, publication, and withdrawal reconciliation | `006` | `todo` | Activation never publishes. An authenticated operator approves an exact draft; ordinary Service Offer signing/publication commits it; exact task-profile identity is standardized; revocation or pause closes local admission immediately and BDO/Replay Scheduler reconcile withdrawal. |
| `P094-008` | Resolve prepared systems, Workbench profiles, Interfaces, containment, and immutable assets | `005`, `018`, `019` | `todo` | Exact image variant/prepared system, command/patch profiles, descriptor refs, scripts, fixtures, and acquisition refs resolve without fallback. The Workbench enforces patch policies and the `observation` effect mode. The containment predicate is checked at admission and before each step. Substitution, unavailable inventory, wider runtime network, lost containment, or an environment impact class above `impact-class/max` refuses. |
| `P094-009` | Implement the closed experiment-plan compiler and HIL boundary | `004`, `008` | `todo` | Prose/model output can only produce schema-valid candidates contained by the resolved plan. The host stamps digests, effect classes, and HIL requirements; every mutation reaches current HIL through the attention budget and owner authorization; arbitrary command strings, paths, endpoints, capability claims, HIL bypass, and classes outside the Version 1 scope refuse. |
| `P094-010` | Implement verifier, rollback, refusal corpus, and Version 1 uncertain-outcome handling | `008`, `009` | `todo` | Verifier output is observation consumed by a host evaluator; missing checks and mutation refuse success; bounded verifier retry applies only in observation mode and the unchanged instance; destroy-and-recreate works after success, refusal, HIL denial, pause, and crash; an `unknown` step enters `rollback-pending`, terminalizes only after owner-confirmed destruction, is re-driven after restart, and is never repeated; refusal coverage reaches every registered code. |
| `P094-011` | Build the qmail task pack assets and local profile | `003`, `004` | `todo` | A signed package binds thematic profile, reusable inference flow, pinned image/prepared system, exact command/patch profiles, fixtures, verifier, rollback, resource ceiling, and refusal corpus, with every digest and capability list produced by `derive_pack_facts`; no secrets or machine-local authority are portable. |
| `P094-012` | Add bounded operator API, CLI, and UI | `006`; runs `010`; publication `007` | `todo` | Authenticated binding-keyed surfaces inspect packs, bindings, readiness, profile changes, drafts, publication, runs, withdrawal, and evidence refs. They share one source of configuration, lead with the decisive blocker and next action, show effective values with their deciding layer, confirm widening separately, redact sensitive values, and expose no raw internal stores. |
| `P094-013` | Run local acceptance | `010`, `011`, `012` | `todo` | Evidence covers clean install, conformance, activation, binding from defaults, operator-initiated deliberation, observation-first experiment, HIL mutation and denial, qmail verification, rollback, restart, pause/resume, profile-change blocking, and revocation. The acceptance contract is [Story 013](../30-stories/story-013-qmail-task-pack.md)'s local profile. |
| `P094-014` | Publish operator HOWTO and troubleshooting guidance | `013`, `016` | `todo` | English and Polish HOWTOs describe only implemented commands and routes, teach qmail pack preparation and use, explain refusal/recovery states through the refusal table's next actions, and distinguish package provenance, local trust, and current execution authority. |
| `P094-015` | Review, ledger, solution, and readiness synchronization | `014` | `todo` | Code review finds no parallel authority or unbounded executor; Node implementation ledger, generated view, relevant solutions, capability/status matrices, and readiness snapshot distinguish implemented evidence from remaining proposal scope. Promotion decision is recorded explicitly. |
| `P094-016` | Run multi-node publication acceptance | `007`, `013` | `todo` | Evidence covers offer publication, requester discovery, remote deliberation, exact profile-digest admission by the provider, stale-offer refusal after revocation, and committed withdrawal. The acceptance contract is [Story 013](../30-stories/story-013-qmail-task-pack.md)'s federated profile. |
| `P094-017` | Admit effects outside a contained environment | `015` | `deferred` | Uncontained steps, including Interface actuation, are mapped to P080 classes (`transactional-withheld`, `compensatable`, `irreversible-external`) through owner sources and admitted only with the P080 recovery contract, P093 outcome and reconciliation semantics, and crash tests at every admission point. |
| `P094-019` | Enforce the Workbench command-profile effect mode | `001` | `todo` | The Workbench owner ships `sensorium-command-profile.v2` with `effect/mode: observation \| mutation`, absent meaning `mutation`, and enforces `observation` inside the guest rather than trusting it. Host-side read-only sharing does not suffice, because it protects the host, not the guest disk. The owner chooses the mechanism, for example running on a discarded copy-on-write fork of the instance, or comparing digests of declared roots before and after with violation leading to refusal and instance destruction. A refusal fixture proves that a write attempt under `observation` does not take effect or is detected and refused. Mirrored as a Phase 6 item in the P071 tracker. |
| `P094-018` | Extend P080 with the isolated-environment resource kind | `001` | `todo` | A versioned P080 contract change adds `resource/kind: isolated-environment` with `dispose/operation: environment.destroy` under `ephemeral-revertible` and `host-local` scope; Sensorium Virt implements the disposer idempotently with durable destruction confirmation; the P080 recovery-class table and `middleware-component-contract` schema agree; restart re-drives unconfirmed destruction. |

## Acceptance Criteria

P094 may be promoted only when:

- P085 remains the sole package lifecycle and activation authority;
- one package installs and activates without publishing or executing anything;
- a local binding resolves to one immutable plan with no ambient alternatives;
- an operator reaches a runnable binding by supplying only choices without a safe
  default, and never types a digest or activation generation;
- reactivation or P085 rollback of the same profile leaves the binding valid, while a
  changed profile digest blocks it until the operator accepts the diff;
- ordinary Service Offer publication binds the exact task profile and can be withdrawn;
- a remote requester can select the offer and create a Corpus deliberation using prose;
- no prose or model output becomes executable without a closed action profile, and no
  candidate content influences a step's effect class or HIL requirement;
- the qmail scenario performs read-only inspection before mutation;
- every mutation requires the configured HIL and current owner authorization;
- the verifier proves local delivery and rejected relay under its exact contract;
- VM teardown/recreation succeeds, and a crash after an effect admission point ends only
  after owner-confirmed destruction;
- step capabilities and effect classes come only from owner-owned contracts, and a
  missing owner source yields the more restrictive derivation;
- package revocation synchronously closes local admission and eventually withdraws the
  offer;
- every refusal code has a stage, retry class, and next action, and readiness reports
  one decisive blocker per root cause;
- restart, pause during a run, crash with an `unknown` step, changed replay, stale
  generation, substituted image/profile/verifier, lost grant/lease, HIL denial,
  exhausted budget, and unavailable rollback have reaching tests;
- inspection and retained evidence contain no secret, raw prompt, chain-of-thought,
  private payload, or machine-local path leakage;
- documentation describes only implemented surfaces and the implementation ledger
  identifies the evidence.

## Open Questions

1. **Service Offer binding.** Should the exact task-profile identity become an explicit
   Service Offer field or a closed namespaced policy annotation? `P094-007` must resolve
   this before implementation; an ad-hoc field is not acceptable.
2. **Prepared-system schema.** Should the existing acceptance fixture shape be promoted
   as `sensorium-virt-prepared-system.v1`, or should P094 bind only an image manifest and
   separately typed fixture refs? `P094-008` owns the reuse audit and decision.
3. **Local-binding attestation.** Version 1 treats the binding as a host-owned,
   source-aware projection protected by operator configuration and current-use checks.
   A later federated or transferable binding may require a signed artifact, but it must
   not be added merely for symmetry.
4. **Multiple profiles per pack.** The package format can carry multiple semantic
   entries. Acceptance must determine whether independent task profiles may share one
   environment and refusal corpus without obscuring their exact readiness.

## Consequences

### Positive

- Operators configure a coherent product instead of manually preserving a graph of
  loosely related refs.
- Corpus remains domain-general while task-specific semantics stay in package assets and
  owning contracts.
- Natural-language deliberation remains useful without crossing the authority boundary.
- Readiness and refusal become explainable before publication or execution, with one
  decisive blocker and a tabled next action instead of free-form diagnosis.
- Operators author only choices without a safe default; digests, generations, and
  capability lists are derived, so upgrades and reactivations do not create manual
  re-binding work.
- The Version 1 recovery scope removes per-step domain reconciliation from the first
  slice: an uncertain outcome costs one owner-confirmed environment destruction.
- Reuse of P085, Workbench, Interfaces, BDO, Replay Scheduler, and temporal stores avoids
  a second control plane.
- The qmail exemplar exercises non-programming operational work and exposes hidden
  assumptions in the current Story-012-centric composition.

### Costs

- Cross-domain conformance requires exact version and digest management.
- Operators still make local decisions about environments, runtimes, price, HIL, and
  network; the pack organizes those decisions rather than eliminating them.
- Publication and withdrawal add asynchronous reconciliation states.
- Version 1 covers only tasks whose effects stay inside a contained environment; tasks
  that must change durable or external state, or use Interface actuation, wait for
  `P094-017`.
- Workbench and P080 owners must first land four contract changes: patch policy,
  command-profile effect mode, the action-semantics map, and the isolated-environment
  resource kind.
- A useful refusal corpus is substantial and must evolve with every new action kind.
- Strict no-fallback behaviour may feel less convenient than ambient local tooling, but
  it keeps authority and evidence understandable.

### Deferred extensions

- package-defined callable behaviours through P093;
- effects outside a contained environment, including Interface actuation (`P094-017`);
- proving that an `isolated` network is contained;
- plan-level HIL approval as a third, less restrictive HIL mode;
- automatic acceptance of profile revisions that narrow every axis and substitute
  nothing;
- externally networked task environments;
- signed portable local-binding templates;
- transferable prepared-system attestations across heterogeneous hypervisors;
- task-pack composition from multiple signing authorities;
- automated reputation projection for task-pack providers;
- task classes requiring physical actuators beyond the first P083 integration.
