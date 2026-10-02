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
    dated, additive amendment of `middleware-component-contract.v1` adding resource kind
    `isolated-environment` with the typed disposer `environment.destroy` (`P094-018`;
    clarified on `2026-09-27`: the amendment extends closed enums without changing any
    existing declaration, so it needs no new schema version). Any other effect, including every
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
    mutation would bypass HIL. Until the owner enforcement exists (`P094-019b`), the
    affected profiles are blocked in readiness, not weakened.

Recorded on `2026-09-27`, resolving review question Q-01 of `P094-006a`:

22. **Binding changes need current operator authority, through a lighter contract.** A
    binding is configuration, not execution authority, yet its environment, profile and
    limits shape every later run. Who may change it and whether it may be used now are
    therefore separate questions: the second stays with P085 and the current-use fence.
    Creating a binding, resuming it, accepting a changed profile, changing its
    parameters, and an ordinary pause each name an exact `node-operator-binding`, which
    the host verifies as current with the P085 operator-authority check, the same one
    that gates P085 activation and session activation. No second local trust vocabulary
    exists. The change does not repeat the P085 activation ceremony: it carries no
    detached signature and no plan digest. Authority and the expected binding revision
    are checked when the change is committed, not only when a diff or preview was
    computed. Every committed change is recorded as `operator-task-binding-change.v1`
    with the verified actor, the operator binding, and the binding revision before and
    after it. Readiness, inspection and a profile-change review need only read access.
    Preparing a binding document offline is allowed and grants nothing by itself.
23. **Emergency pause is a separate host-local channel, not a fallback.** Losing or
    revoking the operator binding must not take from the node owner the ability to
    restrict the node. An explicit, authenticated host-local route accepts
    `operator-task-binding-emergency-pause.v1`, which can only pause, needs no operator
    binding and no expected revision, and is recorded with the host-local actor. An
    ordinary request that fails authorization is refused; the host never retries it as
    an emergency pause.
24. **Changing configuration never transfers activation.** A new legitimate operator
    may change a binding, but does not thereby take over a package activation issued
    under a predecessor's operator binding. Readiness keeps reporting
    `operator/binding-lost` for that activation until it is reissued under current
    authority.
25. **A binding revision fences mutation history, not just its current value.**
    Accepted during the `P094-006c` review on `2026-09-27`: the host stores
    `binding/revision`, starting at 1 and incrementing on every effective change,
    including emergency pause. It is part of `local-binding/digest`. A pause/resume/
    pause cycle therefore cannot make an old resume request current again (ABA).
    The counter is never caller-supplied; no-op retries do not advance it. Legacy
    records without it retain their digest until their first change assigns 1.
    This supersedes the earlier exclusion of all binding revision counters, not the
    exclusion of package activation generation or duplicated portable facts.

26. **Portable roots are explicitly mapped by the local binding.**
    `workspace/root/ref` selects the local Workbench root; optional
    `workspace/profile/root-ref` names the portable root used by the pack's
    command profiles and patch policy. Absence means identity mapping, not
    discovery or a wildcard. The mapping participates in the binding digest,
    is retained by the run instance across restart, and cannot be changed by
    replaying allocation. One binding maps one root; multi-root mappings are
    outside V1. Owner admission still checks the original portable profile and
    its digest, never a rewritten profile. P094-011 should use the explicit
    mapping for `workspace-root:qmail-lab` to `guest-root:qmail`.

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

### Registered schema family

The contracts below are registered as draft schemas in `doc/schemas/`
(`operator-task-common.v1` plus one thin schema per contract) with positive and
negative vectors, and Node's Schema Gate validates them (`P094-003a`); the host
evidence contract `operator-task-pack-facts-evidence.v1` joined them with `P094-005b`, and
the operator route contracts (`operator-task-pack-conformance-run.v1` and its result,
`operator-task-binding-create.v1`, `operator-task-binding-state.v1`,
`operator-task-profile-change.v1` and its result, and `operator-task-refusal.v1`) with
`P094-006a`. `P094-006c` added current operator authority and the expected revision
to the change requests, `operator-task-binding-emergency-pause.v1`, and the audit fact
`operator-task-binding-change.v1`. `P094-012` added the operator read projections
`operator-task-binding-list.v1` and `operator-task-binding-inspection.v1`. The JSON
examples in this section are illustrative; the schemas are authoritative for the exact
shape. The refusal table later in this proposal is the source of truth for the
refusal vocabulary, and a drift check keeps the schema enum equal to it.

### `operator-task-profile.v1`

The profile is a portable, immutable composition contract. It contains identifiers and
digests, not the referenced large content.

```json
{
  "schema": "operator-task-profile.v1",
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
    "inference-flow/ref": "qmail-task-pack-steps",
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
    "prepared-system/ref": "prepared-system:qmail-v1",
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

`deliberation.inference-flow/ref` is the id of an `orbiplex.json_e_flow.v1` Flow
in its owner's grammar (`flowId`: lowercase ASCII letters and digits with
single `.`, `_` or `-` separators, 1–128 bytes), not a `prefix:name` ref. One
identifier names the Flow document, its configuration, its P085 registration and
an Agent's binding to it; an actor ref derived from it never becomes another Flow
id, and a prefixed value is refused, never stripped. Its digest is the delivered
Flow document's (JCS v1 of the JSON object), which the host compares with the
Flow it loaded. The contracts that name an asset as its profile slot does
(conformance requests, pack-facts evidence, readiness evidence) accept a ref or
that Flow id.

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
publish, or execute the profile. The profile bytes are an immutable package asset that
the package does not store. Following the P085 pattern for package-owned content, the
caller supplies the profile, and the host admits it only when the registration's
`entry/digest` equals SHA-256 over the supplied profile's JCS v1 canonical JSON and a
current activation authorizes the entry (`P085-045`); the admitted profile inherits the
package's operational class. The tuple is not a substitute for carrying or validating
the referenced payload.

The containing P085 manifest must list a superset of every profile
`required-capability/ids` value in its own `required-capability/ids`, and must bind
every package-owned reusable inference flow used by the profile. Mismatch is package
conformance failure, not a reason to infer or copy the missing declaration. The
profile's `resource-envelope/ref` names the **task resource envelope**, a package asset
that the profile pins by ref and digest and conformance checks like every other asset.
It is not an **operator Inquirium envelope**: the manifest's `resource-envelope/refs`
name only operator-signed `operator-resource-envelope.v1` envelopes the package
declares a dependency on, which activation requires to be current under the activating
operator, and the task resource envelope is never copied into that list.

### `operator-task-local-binding.v1`

The local binding is host-owned and source-aware. It is a P091-resolved projection, not
a portable package asset and not authority by itself.

```json
{
  "schema": "operator-task-local-binding.v1",
  "schema/v": 1,
  "binding/ref": "operator-task-local-binding:qmail-on-workbench-a",
  "binding/state": "enabled",
  "package/ref": "extension-package:qmail-operator-pack",
  "task-profile/ref": "operator-task-profile:qmail-local-administration",
  "task-profile/digest": "sha256:PROFILE_DIGEST",
  "workspace": {
    "root/ref": "workspace-root:qmail-lab",
    "backend/ref": "sensorium-virt-backend:cloud-hypervisor-system.v1"
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
- **Host-filled on mutation:** `binding/revision`, a monotone JSON-safe counter
  included in the binding digest, per Resolved Decision 25.
- **Absent by design:** activation generation and the local binding digest itself.
  The generation is read at resolution and recorded in the resolved plan and run
  facts; the binding digest is computed from the canonical resolved binding,
  including its mutation revision.

The stored binding may use stable logical roots such as `workspace-root:qmail-lab`.
`workspace/backend/ref` names the Sensorium Virt backend by its capability descriptor's
id, `sensorium-virt-backend:<backend/id>`, and the Workbench root named by
`workspace/root/ref` must use that backend as its executor (`P094-008a`).
Decision 26 maps the portable pack root through `workspace/profile/root-ref`;
this is a local operator choice, not authority supplied by a candidate plan.
Resolution to an absolute local path happens inside the owning Workbench or environment
provider and is omitted from portable inspection and remote status.

### Binding changes and their authority

Resolved Decisions 22 to 24 separate who may change a binding from whether it may be used
now. The gate depends on the operation:

| Operation | Gate |
| :--- | :--- |
| Create a binding (it starts `enabled`) | a current, exactly verified operator binding |
| Resume, accept a changed profile, change parameters | the same |
| Pause | the same; additionally the host-local emergency channel |
| Readiness, inspection, profile-change review | read access; no operator binding |
| Prepare a binding document offline | allowed; grants nothing and starts nothing |

A change request names `operator/binding-ref`; the state and profile-acceptance requests
also name `local-binding/expected-digest`, the revision they were prepared against, as
readiness or the review reported it; tooling copies it from that read, so the operator
still never types a digest (Resolved Decision 19). Creation expects no binding under the ref, and an
exact replay returns the stored binding. The host commits a change in this order, under
one mutation guard shared with operator-binding revocation, supersession and deletion:

1. validate the request against its contract;
2. read the stored binding and compute the changed one;
3. if the outcome already holds, return the stored binding and record nothing;
4. verify the operator binding as current through the P085 authority check, else refuse
   with `operator/binding-lost`;
5. compare the stored revision with the expected one, else refuse with
   `local-binding/revision-stale`;
6. advance the host mutation revision (refuse exhaustion before writing), append
   `operator-task-binding-change.v1`, then write the binding.

A fact whose write fails leaves the binding unchanged. A fact whose binding write then
fails is only an authorized attempt; it does not prove a committed transition and
never authorizes automatic replay. The binding file is the current-state commit
point, not a historical receipt. The provisional file store cannot establish which
older attempts committed from the latest digest alone; transactional historical
receipts and recovery belong to `P094-006b`.

The emergency pause skips steps 4 and 5 and records `actor/kind: host-local`. It is
reached only through its own route and contract; nothing in an ordinary request selects
it.

Scenario: an operator reviews a changed profile, the review reports the current
`local-binding/digest`, and the operator accepts with that digest. Meanwhile a second
operator session pauses the binding. The acceptance refuses with
`local-binding/revision-stale`; the operator reviews again, now against the paused
revision, and accepts. When the operator binding is later revoked, the node owner can
still stop the binding with an emergency pause, while resuming it waits for a current
operator binding and readiness keeps showing `operator/binding-lost` for the old
activation.

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
recorded but does not refuse unless the result is empty, which refuses with
`run/budget-exhausted`.

The P085 operator attention budget is not an axis. The effective HIL mode decides
whether a step needs a question; a separate attention gate then decides whether that
question is delivered, grouped, deferred, or denied, and only the operator's answer
approves. When no question can currently be delivered, readiness reports the `effects`
stage as `degraded` with `hil/attention-unavailable`.

### `operator-task-readiness.v1`

Readiness is an explainable projection of one local binding, not a grant:

```json
{
  "schema": "operator-task-readiness.v1",
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
- `not-applicable` means the binding does not use the stage; in Version 1 only
  `publication` can be not applicable, when `publication.enabled` is `false`, and
  any other stage assessed as not applicable is a contradiction that refuses;
- `not-evaluated` means a stage it depends on is blocked. `package` precedes `binding`;
  both precede the five execution stages; all precede `publication`. One root cause
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
  `enabled`; a paused binding blocks the `binding` stage with `local-binding/paused`,
  unless that stage is already blocked for another reason, which stays the root
  cause;
- `deliberation` is `ready` when a deliberation can start now: the package registers
  exactly the profile's Flow and agent policy, the P085 fence admits the Flow's use,
  and the runtime the binding selects is routable (`P094-020`);
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
  "schema": "operator-task-experiment-candidate.v1",
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
  "schema": "operator-task-experiment-plan.v1",
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
recovery scope (`plan/recovery-class-not-admitted`). A triple without an
action-semantics row is `plan/unknown-action-kind`, and an observation of an
owner-declared mutation is `plan/outside-profile`. A missing owner source refuses with
the owner's code: `workbench/command-profile-missing` for a command profile or patch
policy without an exact owner source, `interface/grant-missing` for a descriptor without
one, since no grant can name an absent descriptor, and `workbench/effect-mode-missing`
for an observation whose Workbench enforcement is not attested.
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

The run `outcome` is `verified`, `verification-failed`, `refused`, `cancelled`, or
`unknown`; a refused run names its refusal code, and a verified or failed run links the
verifier result and host evaluation. Each step is `completed`, `refused`, `unknown`, or
`not-run`. The rollback outcome is `destroyed`, which requires the owner's destruction
confirmation, or `rollback-pending` while that confirmation is outstanding.

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

Each result is `passed`, `failed`, or `not-run`; only the environment acceptance may
remain `not-run` in a passing report.

Only a current fully passing report may satisfy activation or publication policy where
the profile marks conformance as required.

### `operator-task-pack-facts-evidence.v1`

The cross-reference part of conformance is host evidence, not an author's claim. For
every task profile a package binds, the host recomputes the pack facts from the asset
bytes supplied with the conformance request and from owner-published sources, and records
`operator-task-pack-facts-evidence.v1`. It binds the P085 package ref and digest (the
package's lowercase-hex artifact digest), the profile ref, revision and digest, and the
host's action-semantics map ref, revision and digest; it lists every recomputed asset
digest with the rule that produced it (`owner` or `jcs-v1`), the admitted triples and the
derived capability list, and each mismatch against the authored profile and manifest. It
carries no asset bytes, secrets or local paths. P085 stores it as domain conformance
evidence (`P085-046`): the package's conformance report cannot be recorded, and its
activation authorizes no use, until the evidence for every bound profile passes. Task
admission additionally requires the evidence to be current under the host's map, so a
revised map makes it stale. P085 rechecks the evidence byte ceiling and canonical
digest on read, including after restart and before activation use; a corrupt
retained document fails closed.

Digest rules are owner rules where an owner publishes one: the Workbench command profile
(the validated whole document, so fields its typed view lacks, such as `network`, stay
addressed), the Workbench patch policy, and the registry's semantic-entry header for the
thematic profile. Every other slot uses SHA-256 over JCS v1 canonical JSON until its owner
publishes a rule. Command profiles pass the full owner JSON Schema at the import
boundary before typed validation and digesting: binding omitted fields into a
digest alone does not establish that their values are valid. Interface descriptors
have no owner adapter on the host yet, so a profile naming one refuses conformance
rather than guess. The map is the owners'
published default, and capabilities no row yields come from the Workbench's published
VM-environment requirements (`sensorium.virt.host`, `sensorium.workbench.file`), never
from the author.

### Owner-side contracts this proposal requires

P094 consumes, but does not own, several contracts that do not exist yet. Each belongs to
its domain owner and is registered through that owner's review, not as a P094 sidecar:

| Contract | Owner | Purpose | Tracker |
| :--- | :--- | :--- | :--- |
| `sensorium-patch-policy.v1` (new) | Sensorium Workbench | Closed path set, file size, ownership, mode, and accepted content shape for patch admission. Today only patch artifacts and stage/apply results exist. Mirrored in the P071 tracker. | `P094-003b`, `P094-008` |
| `sensorium-command-profile.v1` effect mode (optional field, amended in place) | Sensorium Workbench | `effect/mode: observation \| mutation`. `observation` is enforced by the Workbench, not trusted as a label. Absent means `mutation`. The contract is done; enforcement is `P094-019b`. Mirrored in the P071 tracker. | `P094-019a`, `P094-019b` |
| `sensorium-action-semantics.v1` (new) | Sensorium Workbench and Interfaces | Versioned map from `(owner, kind, operation)` to a registered capability id and to the effect-class rule: fixed, from the command profile's effect mode, or from the descriptor. Mirrored in the P071 tracker; Interface rows co-owned with P083. | `P094-003b`, `P094-008` |
| `sensorium-virt-image-manifest.v1` `guest/effect-modes` (optional field, additive) | Sensorium Virt | The effect modes the image's guest agent enforces, written by the image builder; absent means mutation only. Readiness reads it to decide whether observation is enforceable (`P094-008a`). | `P094-008a` |
| `sensorium-virt-prepared-system.v1` (promoted) and `sensorium-virt-image-manifest.v1` `prepared-system/digest` (optional field, additive) | Sensorium Virt | The closed prepared-system shape the image builder already read (files pinned by content digest and mode, absent paths, bounded claims, `prepared-system:` ref), promoted unchanged so existing manifests keep their digests; its content address is SHA-256 over JCS v1. The image manifest binds it, and conformance requires every admitted image to bind exactly the profile's prepared system (`P094-008c`). | `P094-008c` |
| P080 `isolated-environment` resource kind (extension) | P080 with Sensorium Virt as implementer | `ephemeral-revertible` host-local resource with typed idempotent disposer `environment.destroy` and durable destruction confirmation. | `P094-018` |
| Typed experiment proposal (revision of `corpus-reasoning-experiment-proposal.v1`) | Corpus (P069) | A proposal envelope that names its candidate artifact's type as well as its ref and digest, and the target it is meant for: for a task pack, the exact task profile and local binding. The current envelope promises `inquirium.candidate-plan.v1`, so a task-pack candidate may not ride in it. | `P094-022a` |
| Task-pack review and execution records | Corpus (P069) | A review verdict over exactly the proposed candidate's bytes (approve, reject, or request a correction that yields a new candidate), and the record through which an executed run's result is published back to the Room. | `P094-022a` |

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
| `local-binding/revision-stale` | binding | after-operator-action | `edit-binding` |
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
terminalizes, the instance is destroyed, and the operator starts a new run. `local-binding/revision-stale` arises only when a binding change is committed against
an older revision and is never a readiness blocker. `publication/disabled` is reported only when a publication
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

### Corpus experiment execution

When a task is deliberated in a Corpus Room, the task pack is the executor of the
Room's admitted experiment, not a path beside it. Authority stays with its owners:

| Owner | Decides |
| :--- | :--- |
| Corpus (P069) | the proposal, the review, the chair decision, provenance, and publication of the result |
| P094 | candidate validation, deterministic compilation, run admission and the run lifecycle |
| Workbench and Sensorium Virt | enforcement of each concrete effect and of isolation |

A chair decision admits an experiment; it grants no effect. Package activation, a
current operator binding and HIL remain required. When the operator is also the chair,
the two decisions stay separate facts.

- **Executor selection.** Corpus's `deterministic-host-compiler` executor mode does not
  mean P094 by itself. The daemon selects an implementation from the admitted artifact
  type and the executor's binding; the first implementation is the task pack. Any other
  combination is refused; nothing falls back to the P083 control path.
- **Exact bytes.** The typed proposal binds the candidate's type, ref and digest and the
  target task profile and binding. Review and chair decision cover exactly those bytes.
  A correction produces a new candidate that needs its own review; an earlier approval
  never carries over to it.
- **Provenance is a verified relation.** The executor adapter checks that query, Room,
  proposal, candidate, roles and passages belong together before it compiles. A
  candidate is published from a committed Agent product, never from client bytes: the
  product's passage has a current Corpus inference-Flow binding naming exactly the
  author's turn (query, Room, participant, role assignment, turn number), no wider in
  class, and the candidate is the canonical form of the product's kept bytes. The
  record keeps the passage ref. A client
  cannot attach deliberation refs to an operator-supplied plan and obtain the status
  "admitted by Corpus". The operator's manual path stays legal, without that attribution
  and without counting as deliberation evidence.
- **Publication.** The result is a host-signed Corpus fact bound to the exact Room,
  query, proposal, plan and run and to the digests of its result and evidence. It is
  not an utterance: the host publishes it without becoming a Room participant, and no
  Room event kind carries it, since Corpus owns its meaning. Corpus serves the record,
  and the artifacts it names, to a reader with the current right to read the Room:
  a current member holding `observe` in an unexpired Room. The host's signature proves
  origin; it grants no reader access. Publication has a durable, idempotent identity.
  `Published` means available to entitled readers, not read by every participant; a
  live notification may follow as a signal, never as the only carrier of the evidence.
- **Durable handoff.** The relation admitted proposal → plan → run → result → publication
  in the Room is recorded. A retry of the same proposal finds the existing run instead of
  starting another. A crash after execution but before publication retries the
  publication, never the effect. Changed content under the same identity is a conflict.
  Recovering an existing run, its record or its publication needs no new authority;
  compiling or admitting a run needs a current authorization of the chain. A run
  admitted just before a crash is found by its ref, known from the plan and the run key,
  and is never admitted twice.
- **Observation lifecycle.** Plans stay immutable, and each run's instance is destroyed
  when it concludes. Observation is its own run; the repair is a later run on a fresh
  instance from the same pinned image and prepared system. Evidence names its instance,
  so observations of an earlier instance are never presented as the current state of the
  next, and the repair plan checks its own preconditions again. An observation run that
  does not pass the target verifier is the expected outcome of that experiment, not an
  integration failure.

### Evidence, envelopes and the experiment loop

Three things stay apart: what an Agent saw, what it proposed, and what was allowed.

**Evidence is explicit input.** The requester's Flow names the exact records and
artifacts the next passage needs, by ref and digest. The host reads them as the Agent's
Room subject: current membership with `observe`, classification, and whether the
selected runtime may receive them. Inquirium materializes the content through the local
prompt-assembly policy (`content/ref` layers resolved by the host), within byte and
token limits. Before inference the host fixes an immutable evidence manifest: the
execution and result refs, the chosen artifacts, the source instance of each, and the
identifier and revision of the projection applied. Its digest binds the passage to that
evidence through the passage's `input/digest`, and its ref stays in the passage lineage;
if the passage input needs a field for it, that is an explicit revision of the Agent
contract. `latest` may select evidence but is never left unresolved in an input.

| Passage | Receives |
| :--- | :--- |
| solver | the verifier result, the relevant observations, and the history of earlier proposals and refusals |
| reviewer | the exact candidate under review and the same base evidence |

No private chain of thought is passed on. Terminal output is untrusted data, never an
instruction. A missing required artifact, a digest mismatch or an exceeded limit blocks
the passage; an optional artifact left out is named as left out, and evidence is never
cut silently.

**Adapters produce the envelopes.** The model produces a candidate or a verdict; a
Corpus adapter of the host produces the signed fact.

| Fact | Content from | Built and signed by |
| :--- | :--- | :--- |
| proposal v2 | the solver's committed product | the Corpus adapter of the solver's node |
| review v4 | the reviewer's committed product | the Corpus adapter of the reviewer's node |
| Chair decision v2 | the explicit decision of the entitled Chair | the Corpus adapter of the Chair's node |
| execution record | the P094 run result | the host that ran it |

The adapter checks the product, its passage, the Flow binding, the role and the exact
turn. The model chooses no author, signing node, authority or generation: the host
derives them from admitted facts and narrows expiry to the current authority. A node's
signature says that this node attests this participant's decision; no model holds a
node key, and a requester never signs for a remote solver or reviewer. An operator who
is also the Chair performs two acts: the Corpus decision admitting exactly the reviewed
experiment, and the HIL approval of each mutation of the run. The first never creates the
second. A changed candidate needs a new review and a new decision, never a repackaged
signature.

**The pack's Flow acts in an authorized context.** It executes steps in the authorized
context of a participant or of the round's coordinator; it grants no role, opens no turn
and creates no turn binding. Turn scheduling stays Corpus and Room mechanics. A
participant step runs in one exact turn, with that participant's Agent and current
inference-Flow binding: the solver's passage, the candidate's publication and the
proposal in the Implementer's turn; the reviewer's passage and the review in the
Reviewer's. A coordinator step runs for the round: admission of a closed
proposal → review → Chair decision chain, and authorized reads of positions and results.
One Flow document may serve both, with typed inputs and separate grants; solver and
reviewer keep their own Agents, roles, bindings, products and prompt overlays. A position
read routes the next step and authorizes nothing: every mutation checks its facts and
authority again, and a call outside the caller's role is refused by the host.

**The loop belongs to the requester.** The requester's durable Corpus Flow drives the
deliberation; P094 runs one admitted experiment at a time and never decides on its own
to try again. Story 013 runs:

```text
unsafe candidate → reviewer rejects → no run
observation → review → Chair → run on VM₁ → verification-failed → evidence
repair candidate → review → Chair → HIL → run on VM₂ → verification passes
```

VM₂ comes from the same pinned image and prepared system but is a new instance; VM₁'s
evidence describes a historical state, and the repair checks its preconditions again.

The loop keeps separate counters for proposal-review cycles, passages per role and
admitted runs. A rejected proposal consumes inference but no VM; an exact replay takes no
new slot. Effective limits are the meet of package, binding and the owners' remaining
budgets (see Narrowing axes). The deadline covers the whole process, human waiting
included; waiting for HIL consumes no active inference time. Expired authority needs an
explicit renewal, never an automatic TTL extension. The loop stops on success, an
exhausted budget, cancellation or a terminal safety refusal. `unknown` is not a failed
hypothesis and never starts another effect by itself.

Proposed limits for the deterministic profile, not yet measured:

| Counter | Limit |
| :--- | :--- |
| proposal-review cycles | 4 |
| admitted runs | 2 (observation and repair) |
| solver passages | 4, regenerations included |
| reviewer passages | 4, regenerations included |

The portable `deliberation.limits` bound passages (`max/passages`), admitted runs
(`max/experiments`) and wall time. Revision `P094-023c` adds `max/cycles`,
`max/solver-passages` and `max/reviewer-passages`, all optional and narrowed by `min`
like the others. When a pack leaves a role counter unstated, it equals `max/passages`;
unstated cycles equal the solver's passages, since every proposal needs one.

The host keeps the loop as an append-only Corpus log on the node that owns the round
(`corpus-task-pack-loop.v1`). An operator opens it for one binding; the host fixes its
limits (package, binding and host caps) and its deadline (one wall time from the
opening). The host charges the loop at the natural transitions, each under one key:

- a claimed passage, by its participant's role;
- a signed proposal, which opens its cycle;
- an admitted experiment, which spends its run and requires the loop.

A new step of an admitted run needs the loop neither stopped nor past its deadline. A
published run concludes in the loop. Only an operator renews a deadline, by at most one
wall time, or cancels the loop.

Participant steps that publish a candidate or author a review consume only a committed
product of the exact Agent inference-Flow binding named by their current Corpus context,
not merely a product of the same Agent and turn.
Participant contexts also revalidate their Agent's packaged Flow through the P085 use
fence and package-owned Corpus role/overlay ceilings; a current task binding's package
does not revive an Agent Flow binding from an earlier activation generation.
The position projection coalesces repeated evidence refs before its 32-item bound;
requiredness takes precedence and a kind or digest conflict refuses. More than 32
distinct required items refuse the projection. Only optional items may be omitted,
and deduplication is not an omission.

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
POST /v1/operator/task-bindings/{binding_ref}/emergency-pause
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
`state` switches between `enabled` and `paused`; `emergency-pause` is the host-local
channel of [Binding changes and their authority](#binding-changes-and-their-authority).

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

Until P091 backs this collection (`P094-006b`), the daemon keeps bindings as
host-writable canonical files behind the same store port (`P094-006a`).
The provisional store validates schemas on read and write, rechecks existing
profile snapshots, and uses bounded descriptor-relative I/O below the data-dir
without following links or opening special files. Read-only previews and
rejected requests do not create storage. Profile-change review includes full
thematic and image identities, service type and rollback mode; acceptance
rechecks every retained local deliberation ceiling. Readiness preserves a
conformance failure of an existing activation as `package/conformance-missing`
so its next action is conformance, not another activation attempt.

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
  difference. The two can therefore not drift. The pure core computes no digest: each
  owner computes the content address of its asset, for example `PatchPolicy::digest`,
  and derivation fills and compares digests from that inventory. The admitted triples
  follow from the profile's content: command profiles admit `observe`, `process` and
  `service-control`, the verifier admits `observe`, a patch policy admits `patch`, and
  each descriptor admits its access modes. A capability no row yields, such as the
  host capability of a prepared system, comes from an owner's capability declaration
  naming a source the profile references, never from P094 code. Author tooling and
  conformance share `derive_bundle_facts`: both digest the same asset bytes under the
  same rules, so conformance can reproduce the facts without trusting the profile's
  declarations, and records `operator-task-pack-facts-evidence.v1` with P085.
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
`task-offer-withdrawal-requested` or by a run's terminal refusal. Creating, pausing,
resuming, and accepting a changed profile are binding changes. Until `P094-006b` binds
audit history to committed revisions transactionally, the daemon records each authorized
attempt as `operator-task-binding-change.v1` – the change kind, the verified actor and
operator binding, or the host-local actor of an emergency pause, and the binding digest
before and after – ahead of the binding write. Such a fact is not by itself
`task-binding-accepted`: the change committed only if the stored binding reached its
digest.

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
- Authorize binding changes and compare their expected revision when committing them,
  not when previewing them; never fall back from a refused change to the emergency pause.
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
| A binding change names a revoked, stale, or non-local operator binding | `operator/binding-lost`; nothing is recorded or written, and the request is not retried as an emergency pause. |
| Two operator sessions change one binding concurrently | The later commit refuses with `local-binding/revision-stale`; the operator reviews the current revision and repeats the change. |
| The operator binding is lost while a binding must be stopped | The host-local emergency pause stops it without operator authority; resuming waits for a current operator binding. |
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

- **M1 – inspect and dry-run.** `P094-002`, `P094-003a`, `P094-004a`, `P094-004b`, `P094-005a`, `P094-005b`, `P094-006a`, `P094-006b`, `P094-006c`, and the read surfaces of
  `P094-012`. An operator installs a pack, creates a binding from safe defaults, reads
  readiness with its decisive blocker, and validates candidate plans with the pure core.
  Nothing executes.
- **M2 – local runs.** `P094-018`, `P094-019b`, `P094-008` to `P094-011`, `P094-021`, `P094-013`,
  and the run surfaces of `P094-012`. The operator is the requester; runs execute in the pinned VM
  under the Version 1 recovery scope. Nothing is published.
- **M3 – federated offer.** `P094-007`, `P094-016`, and the publication surfaces of
  `P094-012`. A remote requester selects the offer.
- **M4 – promotion.** `P094-014` and `P094-015`.

`P094-018` and `P094-019b` are owner work on the M2 critical path that does not depend on
the P094 core; both were done during M1 (2026-09-27 and 2026-09-28). `P094-008` now
reads the owner's enforcement evidence for the bound environment. Readiness still
blocks with `workbench/effect-mode-missing` when that evidence is unavailable or
an observation-first profile has no admitted observation command; a verifier
alone does not supply the first step. Real-backend readiness qualification stays
in `P094-013`, and per-step containment revalidation stays in `P094-012`.

The 2026-09-28 follow-up review pins these distinctions with regressions, rejects
a single empty patch line when its policy forbids it, aligns default-context
validation with Workbench, and binds builder/owner digests with a shared UTF-16
key-order golden vector. Builder identity and path checks also match the owner.
These are contract and readiness corrections, not a new VM acceptance result.

Publication is last because it is not needed to prove the authority boundary and adds
asynchronous reconciliation that would otherwise slow every earlier test cycle.

| ID | Work item | Depends on | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- | :--- |
| `P094-001` | Freeze ownership, portable/local/current-use separation, lifecycle, and authority invariants | – | `done` | This proposal records the resolved design, prohibited portable fields, owner matrix, no-prose-authority rule, no-free-form-shell rule, current-use fence, narrowing axes, derived effect semantics, Version 1 recovery scope, pause/revoke split, publication separation, verifier boundary, rollback preference, and qmail-first acceptance target. This is design completion only, not runtime implementation. |
| `P094-002` | Freeze the qmail reference story and acceptance contract | `001` | `done` | An accepted story names requester, solver, reviewer, thematic profile, prepared environment, bounded actions, mandatory HIL, verifier checks, rollback, refusal cases, and retained evidence without adding qmail branches to shared code. Evidence: [Story 013](../30-stories/story-013-qmail-task-pack.md), accepted on 2026-09-25, names the requester, solver, reviewer, and provider operator; the pinned qmail prepared system and its two-part misconfiguration; the admitted command and patch profiles; per-mutation HIL; seven verifier checks including the open-relay trap; destroy-and-recreate rollback; thirteen refusal cases; retained evidence; the substrate gates; and the local (`P094-013`) and federated (`P094-016`) profiles. |
| `P094-003a` | Register the P094-owned schema family with positive and negative fixtures | `001` | `done` | 2026-09-26: `operator-task-common.v1` holds the shared definitions, including the closed refusal-code, stage, retry-class and next-action vocabularies; eight thin schemas cover the task profile, local binding, readiness, offer draft, experiment candidate, experiment plan, experiment result and conformance report. Positive qmail vectors from Story 013 and 34 negative vectors cover arbitrary shell, absolute POSIX and Windows portable paths, hidden egress, unknown actions, `manage` in a candidate, candidate-supplied digests, capabilities, effect classes, HIL flags and binding identity, restated portable facts and activation generation in a binding, missing digests, embedded secrets, a mutation claimed as observation, an observation from a missing owner source, a mutation without HIL, an uncontained class, readiness without a refusal code or a stage, derived readiness fields contradicting their stages, an unknown refusal code, an unconfirmed or contradictory destruction, a verified run whose verifier failed, a refusal code on success or missing on a refused step, a raw transcript, a signed draft, and a conformance report without the action-semantics digest. Node's Schema Gate registers the eight families, and `scripts/test_operator_task_refusal_codes.py` keeps the refusal table and the schema enum equal. Changed replay and actual verifier mutation are semantic refusals owned by `P094-004`, `P094-009` and `P094-010`. |
| `P094-003b` | Register the owner contracts P094 consumes | `001` | `done` | 2026-09-26: `sensorium-patch-policy.v1` (line-oriented content shape per logical root and relative path) and `sensorium-action-semantics.v1` (the default map for the seven admitted triples) are registered with qmail vectors, schema-negative and semantic-negative vectors, mirrored in P071 Phase 6. `sensorium-actuation-core` owns their types: `PatchPolicy::validate` and `ActionSemanticsMap::validate` mirror the schema grammar and refuse what the schemas cannot express, such as a patch declared as a fixed observation, a repeated triple, or a line pattern with a backreference or lookaround; `PatchPolicy::digest` and `ActionSemanticsMap::digest` give the content addresses that plans and conformance reports record (SHA-256 over JCS v1, only for a valid document). Enforcement of the patch policy before staging is `P094-008`; registry admission of map capability ids belongs to the host that loads the map. |
| `P094-004a` | Implement the pure task-pack core without owner-dependent derivations | `003a` | `done` | 2026-09-26: the daemon-free `operator-task-pack-core` crate provides DTOs for the eight contracts that round-trip the Story 013 vectors and re-serialize through Schema Gate; the refusal vocabulary generated from one table, tested equal to the schema enum; `meet_layers`, `member` and `bounded_by_impact_max` with explicit ranks and deciding layer, tested exhaustively over their domains; and `derive_readiness` with dependency order, `not-evaluated` propagation, one blocker per root cause, pause precedence and the closed `runnable`/`publishable` rules, whose outputs pass Schema Gate and reproduce the readiness vector. A dependency guard keeps the crate free of runtime, storage and effect crates. |
| `P094-004b` | Derive plans and pack facts from owner sources | `004a`, `003b`, `019a` | `done` | 2026-09-26: `derive_plan` in `operator-task-pack-core` stamps capability, step class, effect source and HIL requirement on every candidate step from `OwnerSources`, the host's mapping of the action-semantics map, command-profile effects, the patch policy and Interface descriptors, with `mutation` as the missing-source default; the effective HIL mode is met with the profile's again, so a host can only make HIL stricter, and an ambiguous owner source resolves to none; it reproduces the Story 013 plan and reaches every plan refusal of the candidate table for its own reason. `derive_pack_facts` fills every profile digest from the owners' inventory, refusing one that is not a `sha256:` content address, derives `required-capability/ids` from the rows of the triples the profile admits plus owner capability declarations, states the P085 manifest requirements and reports refusal-corpus coverage; `PackFacts::check` names every digest, capability, manifest and structural difference, and reproduces the Story 013 profile. The core stays free of owner crates and computes no digest. Binding package-owned inference flows is checked with the P085 package facts in `P094-005a`. Follow-up audit, 2026-09-26: pack-fact derivation additionally requires exact command-profile, verifier-profile and patch-policy owner bindings before deriving capabilities; paused readiness validates the supplied stage evidence before applying the pause overlay. These are core-boundary repairs, not runtime completion. |
| `P094-005a` | Admit supplied task profiles from P085 packages | `004a` | `done` | 2026-09-26: P085 resolves asset-pinned semantic entries (`P085-045`); `admit_task_profile` in `operator-task-pack-core` admits a supplied profile only when its package is installed and currently activated at the manifest's package digest, binds the profile's ref, revision and digest, the activation's operator binding is the current authority, the caller's generation is current, and the manifest lists the profile's capabilities and binds any package-owned inference flow at the same digest (2026-10-02: the task resource envelope is no longer required in the manifest's operator-envelope list; see the manifest rule above); it refuses with `package/not-active`, `package/profile-digest-mismatch`, `operator/binding-lost`, `package/generation-stale` or `package/conformance-missing`, and inherits the package's operational class. The new `operator-task-pack-service` crate composes Schema Gate, the JCS v1 profile digest, the P085 adapter and an operator-authority port, with no store of its own. Activation, rollback, revocation and restart are exercised at the P085 owner. |
| `P094-005b` | Recompute pack facts at package conformance | `004b`, `005a` | `done` | 2026-09-27: `run_task_pack_conformance` in `operator-task-pack-service` takes each bound profile from a supplied asset bundle, requires its JCS v1 digest to be the pinned registration digest, digests every named asset itself (Workbench command profiles as whole validated documents, the patch policy and the thematic semantic-entry header by owner rules, other slots by JCS v1; Interface descriptors refuse as unsupported), takes the map and the Workbench VM-environment capabilities from their owners, and runs `derive_pack_facts` and `PackFacts::check`. A missing or malformed asset refuses without evidence; a mismatch records failing `operator-task-pack-facts-evidence.v1`. P085 domain conformance (`P085-046`) refuses the package's conformance report and every use of its activation until that evidence passes, and admission requires it to be current under the host map. Tests cover a correct pack, declared and omitted capabilities, a swapped policy, profile and command profile, a missing source, a missing map row, an unsupported descriptor and a later failing run. The daemon requires the domain; its P085 conformance route alone still refuses such packages, and `/v1/operator/extensions/task-packs/conformance` (`P094-006a`) carries the bundle end to end. Review regression coverage also rejects invalid schema/version/network and unknown command-profile fields before derivation; the full owner Schema Gate runs before the incomplete typed view. |
| `P094-006a` | Implement local binding, readiness, and inspection behind a store port | `004a`, `005a` | `done` | 2026-09-27: `create_binding` fills the most restrictive safety defaults, publication off and the host profile digest, names missing choices (`local-binding/incomplete` with `missing/fields`), refuses a choice wider than the profile's ceiling, and treats an unequal binding under an existing ref as `local-binding/conflict`; pause and resume change only the state; `review_profile_change` returns a per-axis diff classified as narrowing, widening or substitution and accepts it in one step only when the binding still fits the new ceilings. Readiness is computed on read from the P085 entry, current pack-facts evidence under the host map, the operator authority and the binding, with one decisive blocker per root cause; execution stages whose owner adapters do not exist yet report the tabled blocker for that missing owner fact. Bindings and the verified copy of each accepted profile live behind `BindingStorePort`, implemented by the daemon as host-writable canonical files. The daemon exposes `/v1/operator/extensions/task-packs/bindings`, `…/bindings/state`, `…/bindings/profile-change` and `…/bindings/readiness`, and `…/conformance`, which reads the asset bundle from a host-admitted P085 import root without following links and runs the P085 runner only after the pack facts pass; every request and answer passes its `operator-task-*` contract, and refusals are `operator-task-refusal.v1`.  Review regressions cover no-follow bounded storage and stored-schema checks, read-only previews, full identity/mode diffs, local deliberation ceiling acceptance, legacy-route refusal after passing conformance, and conformance-specific readiness blockers. |
| `P094-006b` | Back local bindings with P091 | `006a`, P091 `003`/`004` | `todo` | The P091 collection of binding sources replaces the daemon file store behind the same port, with visible source provenance, `local-binding/conflict` for unequal duplicates, and writes only to host-writable sources; an operator-owned read-only source returns the canonical binding without taking effect. Preserve the host mutation revision and atomically bind audit history to committed revisions; pending/failed attempts must remain distinguishable after restart. |
| `P094-006c` | Commit binding changes under current operator authority | `006a` | `done` | 2026-09-27, resolving review question Q-01 of `P094-006a` through Resolved Decisions 22 to 24. `operator-task-binding-create.v1`, `operator-task-binding-state.v1`, and an accepting `operator-task-profile-change.v1` name `operator/binding-ref`; the state and acceptance requests also name `local-binding/expected-digest`, and a review names neither and reports the current revision in its result. The service commits every change in one order – outcome check, P085 operator-binding verification through `ChangeAuthorityPort` (`operator/binding-lost`), revision comparison (`local-binding/revision-stale`), `operator-task-binding-change.v1` fact, binding write – and a change whose fact is not recorded does not take effect. The daemon verifies the operator binding with the same `exact_active_operator_binding_authority` check that gates P085 activation, under the process-wide mutation guard, and stores each fact as a content-addressed file beside the binding. `operator-task-binding-emergency-pause.v1` on `/v1/operator/extensions/task-packs/bindings/emergency-pause`, behind the safe-mode route capability, pauses without operator authority and is recorded with the host-local actor. Tests cover recorded actors and revision chains, a lost operator binding that refuses every ordinary change while the emergency pause still stops the binding, a stale acceptance after a concurrent pause, a successor operator who configures without taking over the predecessor's activation, and a failed fact write; a daemon test drives the routes with a real operator binding before and after its revocation. The profile-change review still shares its route, and so its lifecycle capability, with acceptance; `P094-012` owns separating it. Review closeout: Decision 25 adds a host mutation revision to fence ABA, with legacy digest preservation, no-op and exhaustion tests. The mutation guard now also serializes operator-binding revocation, supersession and deletion; a concurrent-revocation regression pins that boundary. Failed binding writes retain only an attempt, never replay authority; transactional history remains P094-006b. |
| `P094-007` | Implement offer draft, signing, publication, and withdrawal reconciliation | `006a` | `todo` | Activation never publishes. An authenticated operator approves an exact draft; ordinary Service Offer signing/publication commits it; exact task-profile identity is standardized; revocation or pause closes local admission immediately and BDO/Replay Scheduler reconcile withdrawal. |
| `P094-008` | Resolve prepared systems, Workbench profiles, Interfaces, containment, and immutable assets | `003b`, `005a`, `018`, `019b` | `done` | 2026-09-28: `P094-008a` to `P094-008d` are done; readiness checks the containment predicate at admission, and the per-step recheck with the same exported predicate belongs to the step fence of `P094-012`. Split into `P094-008a` to `P094-008d`, each useful alone. Together: exact image variant/prepared system, command/patch profiles, descriptor refs, scripts, fixtures, and acquisition refs resolve without fallback; the Workbench enforces patch policies and the `observation` effect mode; the containment predicate is checked at admission and before each step; substitution, unavailable inventory, wider runtime network, lost containment, or an environment impact class above `impact-class/max` refuses. |
| `P094-008a` | Keep verified assets and read Workbench and Sensorium Virt owner facts into readiness | `005b`, `018`, `019b` | `done` | 2026-09-28. After a profile passes pack-fact conformance, the host keeps the verified document of every asset it names behind `TaskAssetPort`, compactly and content-addressed by slot and digest, before recording the passing evidence; readiness and runs resolve an asset only by exact slot digest and re-verify it with the same owner rule (`slot_digest`) on every read, and a missing asset is never substituted. `TaskEnvironmentPort` resolves `workspace/root/ref` and `workspace/backend/ref` (`sensorium-virt-backend:<backend/id>`) to the admitted backend's capability descriptor and image manifest: exactly one Workbench microVM root with that executor, and an enabled backend profile; nothing starts. `sensorium-virt-image-manifest.v1` gains the additive `guest/effect-modes`, which the image builder writes; absent means mutation only. Readiness now reads owner facts for four stages: environment (the admitted manifest is exactly the selected variant under the slot rule, else `environment/image-mismatch`; no environment, `environment/prepared-system-unavailable`; an `isolated` binding, `environment/not-contained`), effects (every command profile kept, else `workbench/command-profile-missing`; an observation-first profile or observation command needs a hardware-VM guest that enforces observation, else `workbench/effect-mode-missing`), verification (the verifier profile kept and an enforced observation, else `verifier/unavailable` or `verifier/effect-mode-missing`), and rollback (a hardware-VM backend with the `environment.destroy` disposer, else `rollback/unavailable`). Tests cover asset keeping and re-verification, six owner-fact scenarios with contract-valid evidence, Workbench root resolution, and the manifest field. Prepared-system binding, containment, network and impact class follow in `P094-008c`. |
| `P094-008b` | Enforce patch policies before staging | `008a` | `done` | 2026-09-28. `PatchPolicy::admit_content` admits the complete resulting file of one staged write: the exact root and path must be a target admitting create or modify, the bytes UTF-8 within the target and policy byte bounds and the target line bound, and every line a full match of the target's anchored pattern (a final newline ends the last line); `admit_delete` admits a deletion. The Rust actuation companion exposes it as the bridge operation `patch-policy.admit`, answering the policy digest, the owner, group and mode the policy assigns, and the admitted operations. A Workbench `patch.stage` request may attach the policy pinned by `patch-policy/digest`; the Workbench admits the bytes before any reach the guest and refuses with `patch-outside-policy` or `patch-policy-invalid`; the guest's `target/existed` then selects `modify` or `create`, which the policy must admit; the receipt (`sensorium-workbench-patch-stage-result.v1`, additive fields) carries the digest and `patch/target`, and the digest joins the idempotent request. Readiness keeps effects blocked with `workbench/command-profile-missing` when the profile binds a patch policy the host does not keep, or names one without its digest. Tests cover target shape admission in the core, the bridge answer, five Workbench refusals before staging, the create/modify selection, idempotent conflict on a changed policy, and the readiness scenarios. No operation applies staged guest bytes yet; that apply must re-admit against the pinned policy and set exactly the assigned owner, group and mode. |
| `P094-008c` | Bind the prepared system and check containment | `008a` | `done` | 2026-09-28. `sensorium-virt-prepared-system.v1` is registered as a Sensorium Virt owner contract (orbidocs schema, Schema Gate family, `PreparedSystem` with `validate_prepared_system` in `sensorium-virt-core`), keeping the exact shape the image builder already read and its `prepared-system:` refs; the builder's digest is exactly the Rust owner digest (SHA-256 over JCS v1), pinned by the same constant on both sides. `sensorium-virt-image-manifest.v1` gains the additive `prepared-system/digest`, which the image builder writes. Conformance digests the image-manifest and prepared-system slots by owner rules: the complete owner schema, then typed validation (a prepared system must name the slot ref), then the owner content address in the task-pack encoding; every image variant must bind exactly the profile's prepared system. The profile examples use `prepared-system:qmail-v1`. Readiness adds to the environment stage: the kept prepared system bound by the admitted manifest (else `environment/prepared-system-unavailable` or `environment/image-mismatch`), the Workbench root's operational impact class within `impact-class/max` (else `environment/impact-class-exceeded`), and the pure containment predicate `contained` (hardware VM, no writable host share, no credential injection, effective runtime network `none` offered by the backend, no Interface actuation, the `environment.destroy` disposer), else `environment/not-contained` with a `containment-breach:<name>` evidence ref. The predicate is exported for the step fence; run exclusivity stays with `P094-012`. Tests cover the owner type, the shared digest constant, builder path normalization, the manifest binding, conformance refusals (another or no prepared system, a foreign ref, a bad mode, a non-manifest, an explicit null), and every readiness blocker with contract-valid evidence. |
| `P094-008d` | Resolve Interface descriptors | `008a` | `done` | 2026-09-28. Conformance digests Interface descriptors by owner rules instead of refusing them: an observation descriptor passes the complete `sensorium-interface-descriptor.v1` schema and `SensoriumInterfaceDescriptor::validate` under the host limits the Interface runtime uses, an actuation descriptor the `sensorium-interface-actuation-descriptor.v1` schema and its typed validation; each must carry the exact `interface/id` the profile names, is digested as SHA-256 over JCS v1 of the typed value, and contributes its access modes (`read`, `subscribe`, or `invoke`) as the owner source derivation reads. A passing profile keeps them like every other asset. Readiness blocks effects with `interface/grant-missing` for any observation descriptor until a grant adapter exists, and an actuation descriptor blocks the environment with `environment/not-contained` (`containment-breach:interface-actuation`, `P094-008c`). The conformance refusal `UnsupportedSource` is gone because no slot lacks an owner rule. A positive actuation-descriptor vector is added. Tests cover a passing profile with both descriptor kinds, both blockers, an observation-only profile, a foreign `interface/id` and a non-descriptor document. |
| `P094-009` | Implement the closed experiment-plan compiler and HIL boundary | `004b`, `008` | `done` | 2026-09-28: `P094-009a` to `P094-009d` are done; the step fence that consumes approvals is `P094-012`, and the deliberation readiness adapter is `P094-020`. Prose/model output can only produce schema-valid candidates contained by the resolved plan. The host stamps digests, effect classes, and HIL requirements; every mutation reaches current HIL through the attention budget and owner authorization; arbitrary command strings, paths, endpoints, capability claims, HIL bypass, and classes outside the Version 1 scope refuse. |
| `P094-009a` | Compile candidates into immutable plans | `004b`, `008` | `done` | 2026-09-28. `compile_plan` admits an untrusted candidate under the checked-in candidate contract and, in conjunction, the candidate schema the profile pins. That schema is compiled offline from the kept package asset: it may refer only to embedded contracts, and its patterns use the linear `regex` engine. Conformance now refuses a candidate schema that does not compile. Compilation requires every readiness stage a plan depends on except deliberation, which produces candidates, and publication. It rebuilds owner sources from kept assets. A declared observation counts as enforced only on a guest that enforces it. `derive_plan` stamps the plan under the effective HIL mode and the containment predicate. The plan ref is the content address of the candidate, profile and binding digests and the activation generation. Plans are inserted create-only, atomically; a different plan under the same ref is `plan/changed-replay`. |
| `P094-009b` | Admit patch artifacts before any question | `009a` | `done` | 2026-09-28. `operator-task-patch.v1` is a closed patch written for exactly one patch policy: each file is either written as its complete resulting content or deleted. It is stored as `artifact:sha256:<base64url>`, bounded to 1 MiB of content in total. Compilation requires every patch a `patch` step names to be held and written for the step's policy. It admits every file with the Workbench owner's `PatchPolicy` rules and the policy's `patch/max-bytes` over the whole patch, else `workbench/patch-outside-policy`. The fixture candidate names the fixture patch by its real address. |
| `P094-009c` | Issue HIL requests and record operator decisions | `009a` | `done` | 2026-09-28. Every plan step that requires HIL gets one immutable `operator-task-hil-request.v1`. It carries the decision material: the stamped step, the patch files with content digests, and the rollback mode. It is issued only for the binding revision the plan was compiled for, while that binding is enabled. The immutable request is stored before delivery through the P085 attention gate under `operator-task-step`, with its own grouping key. A create-only delivery receipt prevents repeated completed delivery; interrupted delivery retries the winning request with its original deadline and idempotent notification, including a grouped attention admission. Completed deferred/denied receipts are not retried automatically. `operator-task-hil-answer.v1` decides a request once, and only under a current operator binding. An expired request refuses with `hil/expired`, and a different second answer with `plan/changed-replay`. `step_approval` verifies the exact request/plan/generation/step and decision lineage, then gives the step fence `not-required`, `approved`, `pending`, `denied` or `expired`. Readiness degrades effects with `hil/attention-unavailable` when a covering budget is outside its window; a plan still compiles. Amended by `P094-010b` (2026-09-28): a request belongs to one admitted run. It carries `run/ref`, its ref is the content address of the run and the step, it derives plan and binding from the run's admission, and a concluded run issues no new request. `operator-task-hil-issue.v1` therefore names only `run/ref`, and `operator-task-hil-status.v1` reports it. |
| `P094-009d` | Store plans and expose plan and HIL routes | `009b`, `009c` | `done` | 2026-09-28. The daemon file store keeps plans, patches, HIL requests, delivery receipts and decisions immutable. It files each under a hash of its ref and writes it create-only by linking a synced temporary file into place. Reads verify the contract and ref, and a patch must still hash to its address. Routes below `/v1/operator/extensions/task-packs/`: `POST patches`, `POST plans` (`operator-task-plan-compile.v1`), `GET plans?plan=`, `POST plans/hil` (`operator-task-hil-issue.v1` to `operator-task-hil-status.v1`), and `POST plans/hil/answer`. A shown HIL request becomes one high-priority operator notification keyed by its ref. The operator answers through the answer route; answering a P066 question directly is not wired yet. |
| `P094-010` | Implement verifier, rollback, refusal corpus, and Version 1 uncertain-outcome handling | `008`, `009` | `done` | 2026-09-28: `P094-010a` to `P094-010e` are done in the task-pack service behind ports; the daemon adapter is `P094-021`. Verifier output is observation consumed by a host evaluator; missing checks and mutation refuse success; bounded verifier retry applies only in observation mode and the unchanged instance; destroy-and-recreate works after success, refusal, HIL denial, pause, and crash; an `unknown` step enters `rollback-pending`, terminalizes only after owner-confirmed destruction, is re-driven after restart, and is never repeated; refusal coverage of every registered code is recorded in the evidence, and every executable corpus case must refuse with its own code. |
| `P094-010a` | Record runs as append-only facts and admit them | `009` | `done` | 2026-09-28. `operator-task-run-fact.v1` is one fact of one run at one sequence: `admitted`, `environment-allocated`, `step-started`, `step-outcome`, `verifier-evaluated`, `cancel-requested`, `concluded`, `destruction-confirmed`. `RunState` replays and admits each fact, so the store (`RunStorePort`, create-only per sequence) never holds a sequence the projection refuses; phases are `running`, `rollback-pending` and `terminal`. `admit_run` admits a stored plan only for the binding's current revision (`local-binding/revision-stale`) and activation generation (`package/generation-stale`) while the binding is ready for a run, and within `max/concurrent-runs` open runs (`run/budget-exhausted`); the run ref is the content address of the plan ref and a caller run key, so admission is idempotent. `request_cancel` is monotone. Follow-up review binds admission replay to the original binding and exact plan digest; an occupied transition sequence never grants execution ownership, even for identical bytes. |
| `P094-010b` | Drive runs one transition at a time behind a fence | `010a` | `done` | 2026-09-28. `advance_run` performs at most one transition. Before any effect it rechecks the run gate (readiness except deliberation and publication, revision, generation) and the environment stage of the run's own instance; it allocates through `RunEnvironmentPort`, records `step-started` as the durable admission point before `StepExecutorPort` runs a step, and consults `step_approval` for HIL. A step in flight after a crash is recorded `unknown`, never repeated, and the run concludes `unknown`. HIL requests became run-bound (see `P094-009c`). The core refuses further work after a negative outcome or cancellation and refuses late step outcomes after conclusion. |
| `P094-010c` | Evaluate verifier observations on the host | `010b` | `done` | 2026-09-28. `operator-task-verifier.v1` declares the checks a verifier must report, its time bound and `retry/max`; `operator-task-verifier-result.v1` is what one run observed, admitted in conjunction with the checked-in contract, the package's kept `verifier/result-schema` and the verifier ref. `judge_checks` requires every declared check exactly once (else `verifier/check-missing`); a timeout is retried up to `retry/max` (then `verifier/timeout`), a detected mutation refuses with `verifier/mutation-not-admitted` without retry, and no answer is `verifier/unavailable`. Each `operator-task-verifier-evaluation.v1` is stored create-only under its content address, and only a passed evaluation concludes a run `verified`. Conformance digests the verifier as a named contract. Recovery revalidates the evaluation schema and content address and binds it to the exact run, pinned verifier and stored result links. |
| `P094-010d` | Roll back by destruction and recover after restart | `010b` | `done` | 2026-09-28. Every conclusion asks the environment owner to destroy the run's instance; a run is terminal only on owner confirmation (`destruction-confirmed`). `recover_runs` settles each interrupted run of a binding on its own from its facts alone: a step in flight concludes `unknown`, an unconfirmed destruction is requested again, and a failure is reported per run. A destruction unconfirmed for `DESTRUCTION_CONFIRMATION_BOUND` (ten minutes) blocks the rollback stage with `rollback/destroy-unconfirmed`, naming the run, so no further run is admitted and the fence stops runs in progress. Follow-up regression tests also cover a crash between recording a negative step outcome and its conclusion, and pending cancellation: both settle before plan lookup without further execution. |
| `P094-010e` | Run the refusal corpus in conformance | `010c` | `done` | 2026-09-28. `operator-task-refusal-corpus.v1` lists up to 512 cases, each with a tabled code; a case with a candidate is executable. Conformance compiles each executable case under the most permissive host (contained, declared observations enforced) through the package candidate schema and derivation; a case refused with another code, or not refused, adds a `refusal-case` mismatch naming the case and fails the evidence. Cases without a candidate name refusals later layers prove. The evidence records `refusal-coverage {covered, uncovered}`, which never decides the result. A repeated case id refuses the corpus. |
| `P094-011` | Build the qmail task pack assets and local profile | `003a`, `003b`, `004b` | `done` | 2026-09-29: `P094-011a` to `P094-011d` are done; the built image and its qualification in the guest are `P094-011e`. The pack lives in `node/tools/acceptance/story-013-qmail-task-pack/`. An author types no digest: `orbiplex-task-pack-author` derives every asset digest and capability list with `derive_bundle_facts` (the function conformance uses), the task-profile semantic entry, the inference-Flow registration and the P085 package, and writes a self-contained import root reproducibly. The pack ships the wrong qmail baseline and six command profiles with declared effect modes; observations include the verifier and its status mode, and mutations are the probe injection and `service qmail restart`. It also ships a patch policy for `locals`, `rcpthosts` and `defaultdomain`, a verifier with seven checks and a narrowed result schema, and a refusal corpus with the 13 Story 013 cases. The verifier is designed to judge relay with `qmail-smtpd` over stdin; host tests use a stand-in and reject both open-relay repairs. Independent review also rejects RCPT-only repairs and unrelated Maildir files, retains registered Flow documents in the export and validates the exported conformance request. The checked-in pack passes host conformance with its executable corpus cases. `tools/check-task-pack-domain-neutrality.py` shows the shared task-pack code names no domain. Signing is the operator's import signature (`P094-013`). |
| `P094-011e` | Build the qmail image and qualify the pack in the guest | `011`, `019b`, `021g` | `done` | 2026-09-29, on Linux x86_64 with Cloud Hypervisor. Debian 13 ships no qmail, so `image/build_packages.py` in the pack builds notqmail 1.09 reproducibly and without root from the release tarball, pinned by digest and checked against a signature by the pinned signer, laid out as Debian's qmail was (`/var/lib/qmail`, `/etc/qmail`, `qmail-*` in `/usr/sbin`, `qmail.service`), next to the Debian `acl` package pinned by digest. The Cloud Hypervisor builder gains domain-neutral offline packages, a prepared system bound by the image manifest, a provision script and `guest/effect-modes`. The pack provisions the probe Maildir owned by the alias user with a default ACL, because qmail-local writes with umask 077, and declares only the `x86_64` Cloud Hypervisor variant. Probe injection is one SMTP session to the loopback listener, since the guest agent's no-new-privileges keeps `qmail-queue` from its setuid queue user. The domain-neutral `cloud_hypervisor_declared_guest_steps` test runs declared steps in one real guest and reports verbatim; the pack's `qualify_image.py` judges the report. The verifier fails the baseline and both open-relay states, and after the repair a fresh probe reaches the empty Maildir, all seven checks pass, systemd reports qmail live and the listener greets; every observation ran under the enforced sandbox. The author tool binds the built manifest. The passing summary is retained in the pack's `reports/`. The run engine path is `P094-013`. Independent follow-up tightens the qualifier's step-digest and ordered-result admission, rejects failed Maildir reads and duplicate verifier checks, and validates absent paths after provisioning. After these fixes the image was rebuilt with the corrected builder (manifest `sha256:19fc725a…`) and the revised qualifier passed all 20 steps in a real KVM guest (steps `sha256:06dac2c7…`, report `sha256:50e6c0c2…`); the retained summary records that run. |
| `P094-011f` | Build the vfkit arm64 image variant | `011e` | `todo` | Build the qmail image for vfkit on macOS arm64 and add it as a second variant of the profile, qualified in the guest as `P094-011e` qualified `x86_64`. |
| `P094-012` | Add bounded operator API, CLI, and UI | `006a`, `006c`; runs `010` | `done` | 2026-09-29, without publication (`P094-012b`). Read surfaces: `operator-task-binding-list.v1` (one row per binding with its decisive blocker and next action) and `operator-task-binding-inspection.v1` (each narrowing axis with its effective value and the layer that decided it, drill-down refs, the latest runs), projected in the pure core from the binding, its accepted profile, readiness and run facts and admitted by Schema Gate; `GET .../task-packs/bindings`, `.../bindings/inspection` and a read of a run's issued HIL requests with their decision material that issues and delivers nothing (`GET .../plans/hil`). The CLI `orbiplex-node-task-packs` is a thin client of these routes through the node's shared HTTP surface: it checks every request against its contract before sending, reads the revision before a pause, resume or profile acceptance and sends it, asks a separate `--confirm-widening AXIS` for each widened axis of a new binding, offers the emergency pause as its own command, renders refusals as their code and next action, and keeps no configuration. Node UI adds `/operator/task-packs`: the list, the drill-down with effective values and their deciders, pause and resume at the read revision, the emergency stop as a separate action, and a run page whose questions show step, effect class, patch targets and digests and rollback, each answered on its own. Every view projects the structured answer; no raw store is exposed. Review fixes (2026-09-30): the UI sends the revision the page showed, never a fresh read, so a binding changed or stopped after display refuses the change; UI and CLI show each question's exact action (profile and digest, quoted arguments, service action, operation, patch). |
| `P094-012b` | Complete the operator surfaces | `012`, `007` | `todo` | Binding creation and profile-change acceptance in Node UI, with each widening confirmed separately; draft, publication and withdrawal inspection once `P094-007` exists. |
| `P094-013` | Run local acceptance | `010`, `011`, `011e`, `012`, `021g`, `022b`, `023d3` | `todo` | Evidence covers clean install, conformance, activation, binding from defaults, operator-initiated deliberation, observation-first experiment, HIL mutation and denial, qmail verification, rollback, restart, pause/resume, profile-change blocking, and revocation. Also qualify the PID-namespace supervisor on Linux: a detached descendant dies on timeout, a command exit 124 is not timeout proof, and bounded verifier retry succeeds without recreating the VM. The acceptance contract is [Story 013](../30-stories/story-013-qmail-task-pack.md)'s local profile. Inference is deterministic and execution real ([Story 013 inference classes](../30-stories/story-013-qmail-task-pack.md#inference-classes)): the pack ships executable Flow and prompt documents, and a fixture answers only at the inference boundary; Corpus, Agent and Inquirium are real, with Room roles, bindings, passages, budgets and candidate provenance on the production path; the fixture proposes the observation first and the repair only after receiving its result, and refuses missing or unexpected input; the VM and every effect are real, and the harness never repairs qmail by a side path; the reviewer has its own passages and rejects an unsafe open-relay proposal in at least one run, which is a separate proof from an independent negative run in which the verifier detects an open-relay state; the report names its evidence class (deterministic inference, real execution) and claims integration and policy enforcement, not autonomous discovery. |
| `P094-013b` | Run the local profile with a real model | `013` | `todo` | The same flow and boundaries as `P094-013` with a local model runtime answering the solver and the reviewer. Its report names the real-model evidence class and is judged by the same verifier and refusals. Failure to find the repair does not invalidate deterministic mechanism acceptance. Attribute it to model capability only after excluding runtime, evidence-delivery, orchestration and budget failures; otherwise retain the corresponding failure classification. |
| `P094-014` | Publish operator HOWTO and troubleshooting guidance | `013`, `016` | `todo` | English and Polish HOWTOs describe only implemented commands and routes, teach qmail pack preparation and use, explain refusal/recovery states through the refusal table's next actions, and distinguish package provenance, local trust, and current execution authority. |
| `P094-015` | Review, ledger, solution, and readiness synchronization | `014` | `todo` | Code review finds no parallel authority or unbounded executor; Node implementation ledger, generated view, relevant solutions, capability/status matrices, and readiness snapshot distinguish implemented evidence from remaining proposal scope. Promotion decision is recorded explicitly. |
| `P094-016` | Run multi-node publication acceptance | `007`, `013` | `todo` | Evidence covers offer publication, requester discovery, remote deliberation, exact profile-digest admission by the provider, stale-offer refusal after revocation, and committed withdrawal. The acceptance contract is [Story 013](../30-stories/story-013-qmail-task-pack.md)'s federated profile. |
| `P094-017` | Admit effects outside a contained environment | `015` | `deferred` | Uncontained steps, including Interface actuation, are mapped to P080 classes (`transactional-withheld`, `compensatable`, `irreversible-external`) through owner sources and admitted only with the P080 recovery contract, P093 outcome and reconciliation semantics, and crash tests at every admission point. |
| `P094-019a` | Add the command-profile effect mode to the Workbench contract | `001` | `done` | 2026-09-26: `sensorium-command-profile.v1` gained an optional `effect/mode: observation \| mutation` in place (v1 was an unreleased draft), absent meaning `mutation`; `CommandProfile::declared_effect_mode` reads it, with a qmail observation vector and a negative vector. The declaration alone never makes a step an observation. Mirrored in P071 Phase 6. |
| `P094-019b` | Enforce the Workbench command-profile effect mode | `019a` | `done` | 2026-09-28. The Workbench guest enforces a declared observation in two layers instead of trusting it. `spawn-process` carries `effect/mode: observation` with 1 to 8 workspace-relative `observation/roots` (`sensorium-virt.host.request.v1`); `orbiplex-workbench-guest` re-executes itself as a sandbox helper that enters new mount, IPC, network and UTS namespaces, remounts every mount read-only, adds private scratch and an empty read-only `/run`, sets `no_new_privs` and drops to uid and gid 65534 before `exec`, and it digests the declared roots before and after the step. A change refuses the step as `observation-effect-detected` with guest-execution evidence, taints the guest, and makes the host destroy the environment through `environment.destroy` (`P094-018`); a non-Linux guest refuses observation as `effect-mode-unenforceable` and a failed sandbox step as `observation-sandbox-failed`, both before anything runs. The refusal fixture is the real-vfkit deployment check `observation-enforced` (18 of 18 passed): on the pinned GNU/Linux guest an observation runs as uid 65534 with an empty `/run`, a write into a world-writable directory fails with `Read-only file system`, and the file never exists. Unit tests cover detection, taint, metadata and link handling, the refusal off Linux, and the host's destruction decision. `open-pty` stays a mutation, and reading this evidence into readiness belongs to `P094-008`. |
| `P094-020` | Read deliberation owner facts into readiness | `009` | `done` | 2026-09-29. The deliberation stage is ready when a deliberation can start now; no Agent needs to exist, since Agent inference-Flow bindings belong to the session an operator starts. The pure `deliberation_readiness` requires the binding's package to register exactly the profile's Flow with exactly its agent policy, the P085 use fence to admit the Flow now (safe mode, package digest, activation generation, current operator binding, compatibility) and the effective runtime to be routable, and cites the Flow and the agent policy. An inference choice the registration does not admit is the binding's own `local-binding/incomplete` or `local-binding/outside-package-ceiling`, so it also blocks runs; an unusable Flow blocks only deliberation, and plan compilation still does not depend on it. `DeliberationOwnerPort` reads the owners; the daemon's `HostDeliberation` uses the same registration fence as an Agent's packaged Flow binding, now factored out of `ensure_inference_flow_use_at`, and the model runtime host's routable runtimes. Model quality and the remaining Agent and Inquirium budgets stay use-time facts. |
| `P094-021` | Adapt the run engine in the daemon | `010`, `019b` | `done` | 2026-09-28: `P094-021a` to `P094-021f` are done. The owner operations come first, then the daemon. Runs execute through the Workbench in their own microVM instance, a background worker drives them off the request path, and restart recovery waits for older workers through a store lock. A concurrent test proves that recovery never reads a live step as interrupted. The end-to-end run on a real VM with the qmail image is acceptance evidence for `P094-013`. Decision 26 introduces digest-bound `workspace/profile/root-ref`, retained and fenced by the Workbench instance. The verifier retries only `observation-timeout-quiesced` with private helper proof, reaped PID namespace and unchanged roots; missing proof remains unknown. Linux/VM qualification of the newer supervisor remains P094-013. |
| `P094-021a` | Apply staged patches in the guest | `008b` | `done` | 2026-09-28. The Sensorium Virt guest operation `patch-apply` (`sensorium-virt.host.request.v1`) takes 1 to 64 entries: a write of staged bytes with the owner, group and mode its policy assigns, or a deletion. It admits every entry before the first change: the stage of exactly that path, digest and length, a contained target, an existing owner and group, and a mode without special bits. It then installs each write through a synced temporary file and a rename, resolving each target again just before it changes. A refusal changed nothing; a failure after a change is `patch-apply-partial`, and the environment must be destroyed. |
| `P094-021b` | Run structured commands and install patches through the Workbench | `021a` | `done` | 2026-09-28. The actuation companion's `command-profile.admit` admits an argv against a command profile pinned by digest and answers the owner's effect mode, timeout and output bound. The Workbench's `process/run` runs it through the guest `spawn-process` operation. A declared observation runs as a guest-enforced observation of the workspace with a plain grant; a mutation needs an operator-confirmed grant; a timeout that does not fit the host channel is refused. `patch/install` turns stages admitted under the pinned policy into one `patch-apply`. Answers are `completed`/`applied`, `refused` or `unknown` (`sensorium-workbench-process-run-result.v1`, `sensorium-workbench-patch-install-result.v1`) and are replayed under their idempotency key. |
| `P094-021c` | Allocate one Workbench instance per run | `021b` | `done` | 2026-09-28. `environment/allocate` builds the microVM instance of one run from a configured root, keyed by instance key; its root ref is a content address, so a Workbench restart re-binds the live VM through the host's idempotent allocation. The store records an instance as `allocating` before its VM starts, so a failed start can still be torn down; one a restart cannot re-bind is `unbound`. A closed instance is never allocated again under its key. `environment/instance-status` describes an instance by key alone (`sensorium-workbench-instance.v1`). |
| `P094-021d` | Serialize run operations and drive runs in the background | `010` | `done` | 2026-09-28. `RunLocks` in the service gives one lock per run and one per binding. `recover_runs` reads and settles each run under its lock, so it never sees a live step in flight; a concurrent test with real recovery proves it, and it fails without the lock. The daemon's `RunWorker` holds an exclusive `flock` on the run store for its lifetime and recovers every binding first, retrying until that succeeds. It then drives each woken run until the run waits: HIL is rechecked for expiry, rollback and errors are retried after a delay, and a run has at most one pending look. |
| `P094-021e` | Implement the run ports over the Workbench | `021b`, `021c`, `021d` | `done` | 2026-09-28. `WorkbenchRuns` implements the environment, step executor and verifier ports over the Workbench channel. Every answer is admitted by its Schema Gate family. Commands run `[executable, fixed_args..., arguments...]` of their kept profile, and service control appends its action. Patches are staged per file and installed once. Workbench refusals map to tabled codes through a data table; answered unknowns, detected observation effects and lost channels stay unknown. Destruction of an instance never allocated is confirmed. The daemon store keeps verifier evaluations create-only under their content address. |
| `P094-021f` | Expose run routes and start the worker with the daemon | `021e` | `done` | 2026-09-28. `POST runs` (`operator-task-run-admit.v1`), `POST runs/cancel` (`operator-task-run-cancel.v1`) and `GET runs?run=` answer `operator-task-run-status.v1`. Admission holds the binding's lock and cancellation the run's; both wake the worker, and an answered HIL request wakes its run. No route advances a run, and without a worker no run is admitted. The daemon starts the worker with its host owners; when a step waits, the worker issues its HIL request. A route test shows a cancelled run concluded by the worker and left rollback-pending while no Workbench can destroy its instance. |
| `P094-022a` | Register the Corpus contracts of task-pack experiments | `009`, P069 | `done` | 2026-09-30. Canonical `corpus-reasoning-experiment-proposal.v2`, `corpus-reasoning-experiment-review.v4`, `corpus-reasoning-chair-experiment-decision.v2` and `corpus-experiment-task-pack-execution.v1`, synced and registered in Schema Gate, with typed DTOs in `corpus-core`. The pure `resolve_corpus_typed_experiment_gate` admits exactly the reviewed candidate with its target, and `validate_task_pack_execution_relation` requires a record to execute exactly the admitted proposal, review and decision. Each negative vector goes through the gate that owns it: the schema rejects a candidate of another type, a missing target, another executor, a replacement and outcomes without their facts (16 vectors); the record's own validation rejects evidence of another instance; the relation gate blocks a review of other bytes, an approval carried over to a corrected candidate and a decision over another review, each of which is sound alone. Fixtures are signed by a generator test and verified against it. |
| `P094-022b` | Execute admitted Corpus experiments as task-pack runs | `022a`, `010`, `021` | `done` | 2026-09-30. A candidate is published into the Room from an Agent passage of its author's retained turn (`POST /v1/corpus/task-pack-candidates`). Admission (`POST /v1/corpus/rounds/{query}/task-pack-experiments`) selects the executor by artifact type and mode through host ceilings, with no fallback to P083. It checks the proposal against a current Implementer turn and the review against a current Reviewer turn, with current membership and invite-bound origins; the Chair is the Room's. The typed gate must admit exactly the reviewed candidate, which the proposal's own turn published. The chain and the first handoff fact are stored in one transaction. The handoff (`TaskPackHandoff` in `corpus-core`) records plan, run, execution record and publication at fixed positions. A retry compiles nothing already compiled and admits nothing already admitted: one run key per proposal. A P094 refusal before the run records nothing and resumes. A running run is only awaited; an `unknown` conclusion is recorded as unknown and never run again; after the record, only the publication is retried. The run worker's observer takes a terminal run on to its record, and after recovery it resumes only handoffs whose run exists. Step evidence is the Workbench's own answer, kept by content; the result carries its `deliberation` links and is kept by content. The host-signed `corpus-experiment-task-pack-execution.v1` is a Room fact readable by current members with `observe` (`GET .../task-pack-executions`, `.../task-pack-artifacts`). The contract now requires `result/digest` for every recorded run and a code only for `refused`. Small tests cover every interruption point, the negative verdict, the preserved failure codes and a changed target. Review fixes (2026-09-30): the candidate comes from a committed Agent product verified through its Corpus inference-Flow binding; recovery reconciles a run admitted before a crash and needs no authority, while new execution steps need a current one; historical records use the admission's chain validator; candidate bytes and their publication commit together within per-turn, per-query and byte limits, with retention for unreferenced publications; the HTTP envelopes are contracts (`corpus-task-pack-*`) and appear in the API inventory. |
| `P094-023a` | Bind explicit evidence input to passages | `022b`, P069, P071 | `done` | 2026-09-30. `POST /v1/corpus/rounds/{query}/passage-evidence` fixes a `corpus-passage-evidence-manifest.v1`: items by exact ref and digest (`latest` is refused by the contract), each published in the query or named by a published record, read as the Corpus inference-Flow binding's participant (current membership with `observe`), no wider in class than the binding allows, rendered by projection `corpus-task-pack-evidence` revision 1 (framed as untrusted data, `*/base64` output shown as text, nothing cut: a required item over the limit refuses, an optional one is named as left out), and kept by content address together with the manifest. The passage request names the manifest in `metadata["corpus/evidence-manifest"]`, which `input/digest` covers; only a manifest this host made for exactly the passage's current binding, query, Room and reader resolves. At invocation the host re-checks the reader, requires the passage input and the actual request to be at least as restrictive as the evidence (the rule layer selection uses), verifies the kept content against the manifest, and adds the content as a required prompt layer in the user role with an exact role binding, never promoted to an instruction role. Only after the actor and passage are admitted does it record `corpus-passage-evidence-binding.v1`, before the model runs; a replay must find the same binding and a second manifest for the passage is a conflict. Decoded output never replaces a field of the same name. Manifests are bounded per query and overall, and unbound ones are pruned after retention. `GET /v1/corpus/passage-evidence?passage=` shows the binding and manifest. Proposal and review history become evidence items with `023b`. |
| `P094-023e` | Carry a neutral passage input manifest in the Agent contract | `023a` | `todo` | Later, when passages outside Corpus need evidence input: a revision of the Agent passage contract with a general input manifest, without Room or task-pack semantics. The Agent then keeps the canonical passage-to-manifest binding and Corpus keeps its domain relations and points to it; the same input is never declared twice. The passage contract owns this revision; P071 and P083 consume it. |
| `P094-023b` | Build Corpus envelopes from committed products | `022a`, `022b`, P069 | `done` | 2026-09-30. Three host adapters build, sign and record Room facts on the participant's own node. `POST .../task-pack-proposals` builds a proposal v2 from the solver's candidate publication (this node is the author's; a current Implementer role on the retained turn; the publication's Corpus inference-Flow binding is current). `POST .../task-pack-reviews` builds a review v4 from the reviewer's committed product, whose content is a `corpus-task-pack-review-verdict.v1`: the passage belongs to the named reviewer turn, the Reviewer role is current, and the passage was bound before inference to a review target (the proposal's ref and digest and the candidate's digest, fixed in its evidence manifest, with the candidate a required item), which must be exactly the proposal under review; the manifest digest becomes `evidence-state/digest`. `POST .../task-pack-chair-decisions` builds a decision v2 from an explicit decision of a current local operator binding on the node that owns the round and holds the Room's Chair; the decision closes the chain and grants no HIL. The host derives author, reviewer, Chair, signer, candidate, class and idempotency from admitted facts, and expiry narrows to the earliest current authority (Flow binding, role, Room policy, answered document). Each fact is recorded under an identity key, and a retry answers the recorded fact only for the same query, provenance and intent, compared in the write transaction, so a racing writer with another intent gets a conflict; a Chair decides once per review, and the operator authority gate spans the check and the commit. Evidence items gain `candidate`, `proposal`, `review` and `decision`, which gives the solver the history of proposals and refusals. Adapters run on the node that holds the round; remote participants wait for the cross-node Room relay. |
| `P094-023c` | Drive the bounded experiment loop from the requester's Flow | `023a`, `023b` | `done` | 2026-09-30. The loop the requester's Flow drives is an append-only Corpus log per query on the node that owns the round (`task_pack_loop` in `corpus-core`, contract `corpus-task-pack-loop.v1`): opening, charged passages, opened cycles, admitted runs, conclusions, renewals and cancellation. The host enforces it at the natural transitions, each charge under one key so a replay spends nothing: a claimed passage, named by its Agent and passage ref, spends `max/passages` and its role's counter (implementer → solver, reviewer → reviewer; the role comes from the binding's role assignment), and a retry must be the same charge; a signed proposal is recorded together with its cycle in one transaction, so a proposal the loop refuses is never kept; admission spends the run (and a cycle signed elsewhere) and requires the loop, which must still be current even on a retry. Each new handoff step (compiling, admitting a run) checks the loop again and holds a fence against cancellation until its fact is recorded. Renewals are bounded (64), so a loop holds at most 1366 facts. Every loop transaction first concludes admitted runs whose execution is published. Limits are the meet of the profile's `deliberation.limits`, the binding's and the host caps, runs also capped by experiments per round; `deliberation.limits` is revised with optional `max/cycles`, `max/solver-passages` and `max/reviewer-passages`. The deadline is one wall time from the opening, covers human waiting, and moves only by an operator's renewal of at most one wall time. `verified`, `unknown` and the terminal safety refusals stop the loop; `verification-failed`, `cancelled`, `hil/denied` and other refusals do not; an exhausted counter or a passed deadline refuses the next step. Routes open, renew, cancel and read the loop, each as a current local operator binding under the authority guard. The executable Flow that drives it and the qmail pack's per-role limits are `023d`. |
| `P094-023d` | Ship executable deliberation documents and the deterministic inference fixture | `011`, `020`, `023c` | `todo` | Split into `023d1` to `023d3`. Runtime feasibility was shown first: one Flow identity binds and claims passages for two separate Agents; this is not yet a live host-dispatch or inference proof. A Flow-computed `input/digest` equals the host's for a request rendered in the form the host serializes. |
| `P094-023d1` | Expose Corpus task-pack steps to the pack's Flow | `023c` | `done` | 2026-10-01. Host capabilities `corpus.task-pack.*`: position read, evidence preparation, candidate publication, proposal and review authoring (participant steps, bound to the caller's exact turn, Agent and binding) and experiment admission (a coordinator step for a closed chain; it grants no HIL and no Workbench access). A new grant family bounds a Flow to its pack's task profile; each call additionally checks the package's current activation and generation, the profile digest and the local binding, the query, Room, participant and binding, and the role the operation requires. The Chair decision and opening, renewing and cancelling the loop stay operator acts. The position projection names the phase with exact fact refs, counters, deadline and the reason for waiting or blocking, and tells waiting (for the Chair or a run), blocked (exhausted counters or an elapsed deadline; renewal moves only the deadline and replenishes no counter) and stopped apart; it carries no prompt or artifact content. JSON-e helper `sha256_jcs_b64u` (the shared JCS v1 primitive; `sha256_json` unchanged). Built: six registered capabilities and the `corpus_task_pack_grants` family; the step envelope `corpus-task-pack-step.request.v1` with a typed participant or coordinator context; `corpus-task-pack-chain.admit.request.v1`, by which the host assembles a recorded, closed chain from its own documents; and `corpus-task-pack-position.v1`, whose evidence selections are bounded to one preparation, keeping every required item and counting the optional ones left out. Each call checks, in order: the envelope, the static pairing of operation and context, the operator's loop, the P094 gate (current activation and generation, unblocked package and binding stages, the profile the grant names), the participant's binding, turn, Agent and role and that the Flow bound the Agent, and that the operation's request names exactly that context; then the Corpus route runs. |
| `P094-023d2` | Ship the pack's executable documents | `023d1` | `done` | One step Flow (`orbiplex.json_e_flow.v1`) registered as the pack's P085 inference Flow, with typed participant and coordinator inputs; each invocation makes at most one passage or one transition, and waiting for the Chair, HIL or a run returns a wait instead of polling. Restart recovers the position from facts, and a retry reuses the stable operation identity and an existing product instead of inferring again. Requests are rendered in the host's normalized form. The prompt policy with role overlays, the candidate and verdict output schemas and the agent policy; limits 4 cycles, 2 runs, 4 solver and 4 reviewer passages, with an explicit `max/passages` checked against the Agents' Flow bindings. One local runtime serves both Agents, a managed `http_local` adapter (`inquirium.generate` routes no `command_stdio` runtime); separate runtimes per role need a contract change, without weakening the one-runtime gate. Part 1 done (2026-10-01): `deliberation.inference-flow/ref` is a `flowId` in the JSON-e Flow owner's grammar, so the profile, Flow document, configuration, registration and Agent binding share one identifier; slot-ref contracts accept a ref or that Flow id; every loaded Flow carries the digest of its delivered source object (JCS v1, before defaults), and a packaged binding and each passage are admitted only while the Flow loaded under the id carries exactly the registered digest. Part 2 is the pack's step Flow and documents. Part 2 done (2026-10-01): the qmail pack's `inference-flow.json` is the executable step Flow `qmail-task-pack-steps`. `bind` makes the turn's own Agent Flow binding with one passage on a fresh Agent, so the passage number is always 1 and an identical retry replays. The scheduler spawns and consumer-binds that Agent before opening the turn, keeps the exact Agent and inputs through publication retries, then stops it at turn closure; Room participants and roles remain stable, and Corpus loop counters stay query-wide. Recovery reuses retained turn identities, never a replacement Agent. A second binding on a long-lived Agent is refused; the singleton rule, fresh turn Agents and recovery are pinned by runtime tests. Live scheduler integration remains `023d3`. `act` reads the position and routes by status and role to one step: propose (evidence if any, one solver passage, candidate, proposal), review (evidence bound to the target, one reviewer passage, review) or admit (the closed chain by refs); any other position answers `no-step`, never polling. Requests are rendered in the host's normalized form (passage `input/digest` and binding digest equal the host's). JSON-e helper `ref_digest`. Passages run under the Corpus overlay prompt policy; both Agents answer `inquirium.generate.response.v1`, with content checked by the Corpus adapters; limits are 4 cycles, 2 runs, 4 solver, 4 reviewer and 8 passages. |
| `P094-023d3` | Prove the step Flow with the deterministic fixture | `023d2` | `todo` | A fixture, run by the node as a managed `http_local` runtime, answers only at the Inquirium boundary and reacts to evidence, not call counts: it proposes the repair only after recognizing the real observation record in its manifest, the reviewer rejects the exact bytes of the open-relay candidate, and missing, foreign or inconsistent evidence refuses. qmail knowledge stays in the pack and the fixture. A process test drives the Flow through a live local Room, real Agent passages and the signed Corpus adapters, including the turn scheduler's fresh-Agent lifecycle (spawn before turn opening, exact replay identities, stop after publication, query-wide counters): the rejected open relay creates no run, and the corrected candidate needs a new review. The VM and execution evidence are `P094-013`. Part 1 done (2026-10-01): the fixture (`fixture-inference/` of the pack) keeps its candidates and patches as data, decides only from the task text and the evidence layer, and refuses with HTTP 422 otherwise; its parser reads samples rendered by the host's own `project_task_pack_evidence`, a parity test failing when they go stale; the pack's patch policy admits every patch, the open-relay trap included, so only the review stops it; the daemon starts the fixture as a managed runtime and `inquirium.generate` reaches it with evidence intact. Part 2 is the live process test. |
| `P094-023d3a` | Prove the deterministic inference fixture and managed transport | `023d2` | `done` | 2026-10-01. One managed `http_local` runtime serves solver and reviewer. Host-projection samples pin the parser; fixture transitions check exact proposal/candidate relations and a failed observation's named successful step output, including its source instance. Evidence never selects the task role. Malformed, ambiguous, oversized or inconsistent requests receive bounded, non-retryable HTTP 422 refusals. Signature and CAS verification remain the host's responsibility; sample documents are synthetic, not signed acceptance evidence. Pack admission and daemon transport tests cover all three solver candidates and reviewer rejection, without a live Room or passage claim. |
| `P094-023d3b` | Prove the live Room step sequence | `023d3a` | `todo` | Real turn scheduling and fresh-Agent lifecycle, passage claim and actual P064 instruction hash, signed Corpus proposal/review adapters and rejection-before-run proof. VM execution remains `P094-013`. |
| `P094-018` | Extend P080 with the isolated-environment resource kind | `001` | `done` | 2026-09-27. `middleware-component-contract.v1` admits `resource/kind: isolated-environment` with `dispose/operation: environment.destroy` under `ephemeral-revertible` and `host-local` scope, as a dated additive amendment (P080-046); the P080 recovery section, the schema and `middleware-runtime` validation agree and refuse a mismatched operation, kind or scope. Sensorium Virt implements the disposer as `environment.teardown` over a new `destroying` state of `sensorium-virt-recovery-record.v1`: every backend (`fixture-copy.v1`, `vfkit-system.v1`, `cloud-hypervisor-system.v1`) records it durably before the first destructive step, only `destroying` reaches `closed`, a completed destruction replays as confirmed, and start, recover, drain and allocation replay refuse a `destroying` record instead of quarantining it. Startup reconciliation completes every recorded destruction and reports `records/destroyed`; a record that can no longer prove its resource identity is quarantined, never returned to a live state. Tests cover the transition table, a removal interrupted mid-way on `fixture-copy`, and a destruction interrupted with a live VMM on the fake-vfkit and fake Cloud Hypervisor process harnesses. Real-VM deployment runs were not repeated.  Review regressions also cover destruction interrupted during unrecorded-launch cleanup, refusal of unbound resource paths before teardown, record-only quarantine of an invalid destruction, and drained VMM identity validation. |

### P094-021 Follow-Up

| ID | Task | Depends on | Status | Acceptance |
| :--- | :--- | :--- | :--- | :--- |
| `P094-021g` | Fence patch targets and operation kind at installation | `021a`, `021b` | `done` | 2026-09-28; reviewed 2026-09-29. A patch write carries the operation its policy admitted at staging (`create` or `modify`, from `target/existed`), recorded by the Workbench with the stage and required by `sensorium-virt.host.request.v1`. The guest reaches each target's parent from the pinned workspace root one component at a time with `openat` and `O_NOFOLLOW`, pins it by descriptor and identity, and admits the target in the state the operation names. It commits only while walking the path again still reaches the pinned parent, and only through descriptor-relative atomic operations: `create` renames with `NOREPLACE`, `modify` exchanges with the target (`EXCHANGE`) and swaps back anything that is not a regular file, and a delete renames the file aside, checks its type and unlinks or restores it. A walk after the commit that no longer reaches the parent makes the result `patch-apply-partial`. New bytes and displaced objects use agent-owned `0700` scratch pinned by descriptor. Unsupported renames refuse with `patch-apply-unsupported` only before a target change; later failures, including restored replacements and unconfirmed cleanup, are `patch-apply-partial`. Adversarial tests replace a parent with a link or another directory, create a target before a `create`, delete a target or replace it with a link before a `modify`, and replace a deleted file with a directory; pre-rename conflicts refuse; conflicts detected after a rename require destruction even when restoration succeeds. Deterministic checkpoints cover post-rename metadata errors, scratch substitution and post-commit parent displacement. Parent checks do not prove absence of transient move-away-and-back races or protect against guest root. |

The original P094-021a-f implementation is complete, and the independent-review
hardening P094-021g is done (2026-09-28, reviewed 2026-09-29). New bytes and
displaced objects now use an agent-owned, descriptor-pinned `0700` scratch
directory on the target filesystem. Errors after the first target rename,
even with successful restoration, and unconfirmed scratch cleanup require
destruction. Unsupported renames are clean refusals only before any target
change. The parent check detects displacement still visible at the check,
not every transient move away and back; it does not claim protection against
guest root. Deterministic test checkpoints cover metadata failure after
displacement, scratch-name substitution and parent movement after commit.
The qmail VM run remains P094-013.

### P094-019b Review Qualification

The implementation now uses a private close-on-exec helper-status channel instead
of trusting command stderr, bounds output draining by the process deadline,
bounds tree traversal before allocation, and retains pending-observation taint
across guest-agent restart. An unconfirmed timeout or unknown helper status fails closed with
`observation-outcome-unknown`; the host also destroys on recovered taint, including
inspection after a lost original response. Unit and process-conformance tests
cover these paths. The original real-vfkit 18-check proof predates these fixes.

- [x] Rebuild the Linux helper/image and repeat the real-vfkit deployment for the
  reviewed revision before treating that binary as deployment-qualified. On 2026-09-28 the revised helper was compiled, linted and unit-tested on Linux in the pinned builder image, which caught and fixed an ambiguous `by_ref` that only the Linux build sees, and a rebuilt image passed a fresh real-vfkit deployment with 18 of 18 checks, including `observation-enforced`.

P094-021 review adds a PID-namespace supervisor. Only an enforced observation
whose process tree was killed/reaped and whose root digest is unchanged can
return `observation-timeout-quiesced`; Workbench preserves this proof and the
verifier adapter maps it to bounded `retry/max`. Transport loss, missing proof,
or changed roots never qualify. The extra 1 s is cleanup grace, not command
budget. This newer supervisor is not covered by the earlier vfkit report;
Linux execution and the qmail VM run remain qualification work for P094-013.

## Acceptance Criteria

P094 may be promoted only when:

- P085 remains the sole package lifecycle and activation authority;
- one package installs and activates without publishing or executing anything;
- a local binding resolves to one immutable plan with no ambient alternatives;
- an operator reaches a runnable binding by supplying only choices without a safe
  default, and never types a digest or activation generation;
- every binding change except the host-local emergency pause is committed under a
  current operator binding and the expected revision, and is recorded with its actor;
- reactivation or P085 rollback of the same profile leaves the binding valid, while a
  changed profile digest blocks it until the operator accepts the diff;
- ordinary Service Offer publication binds the exact task profile and can be withdrawn;
- a remote requester can select the offer and create a Corpus deliberation using prose;
- no prose or model output becomes executable without a closed action profile, and no
  candidate content influences a step's effect class or HIL requirement;
- the qmail scenario performs read-only inspection before mutation, deliberated in a
  real Corpus Room with a reviewer that can reject an unsafe proposal, and its report
  names the evidence class of its inference;
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
2. **Prepared-system schema.** Resolved by `P094-008c` (2026-09-28): the existing
   acceptance fixture shape is promoted unchanged as `sensorium-virt-prepared-system.v1`,
   a Sensorium Virt owner contract, and the image manifest binds its digest.
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
