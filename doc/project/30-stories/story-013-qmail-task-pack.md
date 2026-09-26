# Story 013: An Operator Task Pack Repairs qmail Local Delivery in a Disposable VM

Status: Accepted reference story for Proposal 094; not implemented

Related:

- [Proposal 094: Operator Task Packs for Bounded Problem Solving](../40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
- [Proposal 085: Operator-Sovereign Extensibility and Experiment Packages](../40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)
- [Proposal 071: Sensorium Workbench](../40-proposals/071-sensorium-workbench.md)
- [Proposal 069: Corpus](../40-proposals/069-corpus.md)
- [Proposal 073: Agent](../40-proposals/073-agent-orchestration-organ.md)
- [Story 011: Corpus answers the fish-water question](story-011-corpus-fish.md)
- [Story 012: Remote Agents Solve a Problem Through a Shared Chair Terminal](story-012-agents-share-chair-terminal.md)

## Summary

As a node operator, I want to install one reviewed task pack for local qmail
administration, bind it to my own lab environment with a few local choices, and
let a model-backed solver repair a qmail configuration problem inside a
disposable VM. Every change must pass a closed plan, my approval, and an exact
verifier; afterwards the VM is destroyed and recreated, and the result is a
verified recipe rather than a change to anyone's real mail server.

The story is the acceptance contract for P094's qmail reference pack. It proves
the domain-general task-pack composition on a non-programming operational task.
qmail meaning lives only in package assets: the thematic profile, command and
patch profiles, fixtures, and verifier. The shared P094 code contains no qmail
branch.

Two execution profiles share one story:

- **Local profile (`P094-013`).** The provider's own operator is the requester.
  Nothing is published.
- **Federated profile (`P094-016`).** A remote requester finds the provider's
  ordinary Service Offer, admits the exact task-profile digest, and receives the
  verified recipe through Corpus.

## Concrete Problem

The pinned prepared system is a qmail installation whose baseline is wrong in
two ways that are common in real deployments:

1. mail for the local domain `example.test` is refused, because the domain is
   absent from `control/locals` and `control/rcpthosts`; and
2. the tempting "fix" of accepting any recipient domain, or granting `RELAY` to
   every client, would turn the host into an open relay.

The requester states the goal in prose: "Accept local mail for `example.test`
from the local host, and make sure the server is not an open relay." The
expected outcome is a diagnosis, the smallest bounded change to the admitted
control files, and verifier evidence that local delivery works while relay
outside the admitted policy is refused.

The fixture must stay small, deterministic, and network-independent. The exact
misconfiguration may change without changing the story contract, provided the
verifier still distinguishes a correct repair from an open-relay "repair".

## Actors

- **Requester.** States the problem in prose and receives the answer. In the
  local profile this is the provider's own operator; in the federated profile a
  remote node that selected the offer. The requester never gains access to the
  provider's VM, files, or terminal.
- **Provider node.** Holds the installed and activated task pack, the local
  binding, the Workbench VM backend, the Corpus Room, and the resulting evidence.
- **Solver Agent.** A node-local Agent on the provider node that deliberates
  under the pack's reusable inference flow and emits candidate plans. It never
  names digests, effect classes, HIL flags, or shell text.
- **Reviewer Agent.** A second Corpus participant that checks the diagnosis and
  the candidate plan against the requester's goal, in particular the open-relay
  trap. In the local profile it runs on the provider node; the federated profile
  may place it on a third node under Story 011 membership rules.
- **Provider operator.** Installs, binds, and, if the federated profile is used,
  publishes the pack. Answers every HIL request for a mutation. Can pause the
  binding or revoke the package at any time.

## Task Pack Contents

The signed P085 package carries one `operator-task-profile.v1` semantic entry.
Its portable facts, all digest-pinned and produced by the pack build rather than
typed by hand:

| Element | Value |
| :--- | :--- |
| Thematic profile | `corpus-profile:qmail-administration`, roles `requester`, `solver`, `reviewer` |
| Reusable inference flow | package-owned deliberation flow with bounded passages, experiments, and wall time |
| Image variants | at least one pinned Debian image manifest with build provenance and guest-agent identity |
| Prepared system | qmail installed per the manifest, the baseline control files above, fixture mailboxes, and absence claims for unexpected listeners |
| Runtime network ceiling | `none` |
| Impact-class maximum | `test` |
| Command profiles | `qmail-showctl` and `qmail-qread` in Workbench-enforced `observation` mode; service status in `observation` mode; local SMTP injection against the instance; exact service restart |
| Patch policy | `sensorium-patch-policy.v1` admitting only `control/locals`, `control/rcpthosts`, and `control/defaultdomain`, with size, owner, mode, and line-shape constraints |
| Verifier | observation-mode command profile plus result schema; checks listed below |
| Rollback | `recreate-prepared-system` |
| HIL mode | `each-mutation` |
| First step class | `observation` |
| Refusal corpus | one fixture per refusal case below |

The local binding supplies only the choices without a safe default: workspace
root, VM backend, and the model/runtime when the flow admits more than one. It
keeps the safe defaults: runtime network `none`, HIL `each-mutation`, one
concurrent run, publication disabled until the operator enables it.

## Flow

1. The operator installs the package. P085 verifies it and stores it inertly;
   conformance recomputes the pack facts and runs the refusal corpus.
2. The operator activates the package and creates a binding from safe defaults.
   Readiness shows one decisive blocker until the prepared system exists, then
   `runnable`.
3. The requester states the goal in prose. Corpus opens a Room under the qmail
   thematic profile with solver and reviewer.
4. The host creates a fresh contained VM instance from the pinned image and
   prepared system.
5. The solver's first candidate plan observes the baseline with `qmail-showctl`,
   `qmail-qread`, and service status. The host stamps each step as
   `observation`; no HIL request is needed.
6. The solver diagnoses the missing local domain and proposes a candidate with a
   patch to `control/locals` and `control/rcpthosts` plus a service restart. The
   reviewer checks that no wildcard, relay grant, or unrelated file appears.
7. The host validates the whole candidate against the resolved plan, stamps each
   step as `contained-mutation`, and asks the operator once per mutation. Each
   HIL request shows the step, its derived class and source, the exact diff or
   target, and the rollback that would apply.
8. After approval, the host applies one mutation at a time, rechecking the
   current-use fence before each step.
9. The solver observes service and queue state and injects a local test message.
10. The exact verifier runs in `observation` mode. The host evaluator decides pass
    or fail from its bounded observations.
11. The run result links the Corpus deliberation, the stamped plan, the step
    outcomes, the HIL decisions, and the verifier evidence. Corpus turns the
    solver's outcome into an answer draft containing the diagnosis and the
    verified patch as a recipe.
12. The host destroys the instance and records the owner's destruction
    confirmation.

In the federated profile, steps 3 and 11 cross the network: the requester
reaches the provider through its signed offer, the provider admits the request
only for the exact task-profile digest, and the answer returns through the
ordinary Corpus publication path.

## Verifier Checks

The run succeeds only if all checks pass under the exact verifier contract:

- the qmail service is healthy under the prepared service manager;
- a local test message to a mailbox in `example.test` is accepted and reaches the
  expected mailbox or queue state;
- the listener scope matches the profile;
- a relay attempt to a domain outside the admitted policy is refused;
- no control file outside the patch policy changed;
- runtime network stayed within the `none` ceiling;
- the verifier performed no mutation outside its observation profile.

A repair that accepts every domain passes the delivery check and fails the relay
check. That is the intended trap: the verifier, not the solver's prose, decides.

## Authority Contract

- Prose, the requester's goal, and model output are inert. Only a schema-valid
  candidate made of closed action kinds and refs from the resolved plan can
  become executable, and only after host stamping.
- The solver never obtains Workbench, terminal, patch, or network authority of
  its own. Every effect passes P094's current-use fence and the owning Workbench
  boundary.
- Every mutation needs the operator's HIL answer. The P085 attention budget may
  group, defer, or deny delivery of a question, but never approves.
- Observation is enforced by the Workbench, never declared. A command profile
  without an enforced effect mode is a mutation, and readiness blocks the pack
  with `workbench/effect-mode-missing` until the owner contract exists.
- The requester's real systems are never touched. The pack runs only inside the
  provider's contained instance and exports a recipe, not an effect.
- Publication is a separate operator action. Activation, binding, or a passing
  run never advertises anything.

## Refusal Cases

Each case has a refusal-corpus fixture and must be reached at the owning
boundary, not asserted from source markers:

| Case | Expected outcome |
| :--- | :--- |
| The model returns a shell command or `sed -i` text | refused as not representable or `plan/outside-profile`; nothing executes |
| The candidate claims its own effect class, digest, or HIL flag | schema refusal of the unrepresentable field |
| The first step is a mutation | `plan/first-step-not-observation` |
| A patch touches `/etc/tcp.smtp`, adds a wildcard, or writes outside the policy | `workbench/patch-outside-policy` |
| The operator denies a mutation, or the HIL request expires | `hil/denied` or `hil/expired`; the run ends and the instance is destroyed |
| The binding selects `isolated` network | `environment/not-contained`; no mutation is admitted |
| The image or prepared system is substituted | `environment/image-mismatch` |
| The verifier misses a check, times out repeatedly, or mutates | `verifier/check-missing`, `verifier/timeout` after bounded retries, or `verifier/mutation-not-admitted` |
| The host crashes after a patch is admitted | the step stays `unknown`, the run is `rollback-pending` until destruction is confirmed, and the step is never repeated |
| The operator pauses the binding mid-run | the run stops at the next step boundary and the instance is destroyed; resume needs no reactivation |
| The package is revoked or reactivated mid-run | `package/generation-stale` for further steps; offer withdrawal is requested |
| A package upgrade changes the profile digest | `local-binding/profile-changed` until the operator accepts the diff |
| A remote request carries another profile digest (federated profile) | refused at offer admission before any deliberation |

## Retained Evidence

The run retains links, not copies: the task-profile, binding, activation
generation, and plan digests; Corpus deliberation and Agent passage refs;
Workbench directive and result refs; HIL decision refs; verifier observations and
the host evaluation; the rollback outcome and destruction confirmation; bounded
timings and resource accounting; and typed refusals.

It does not retain prompts, model chain-of-thought, raw VM files, unredacted
command output, secrets, or machine-local absolute paths. The recipe returned to
the requester contains the diagnosis, the exact admitted patch, and the verifier
result, disclosed according to the result's disclosure metadata.

## Substrate Gates

| Gate | Owner | Needed for |
| :--- | :--- | :--- |
| Task-profile schemas, candidate and plan contracts, refusal table | P094 (`P094-003`, `P094-004`) | all runs |
| Package semantic entry and lifecycle | P085 through `P094-005a` (admission, done) and `P094-005b` (conformance recompute) | all runs |
| Binding, readiness, and inspection | `P094-006` | all runs |
| `sensorium-patch-policy.v1` and `sensorium-action-semantics.v1` | Workbench, mirrored in P071 Phase 6 | effects |
| Enforced command-profile effect mode | Workbench, `P094-019a` (contract, done) and `P094-019b` (enforcement) | observation steps and verifier |
| `isolated-environment` recovery class with `environment.destroy` | P080 and Sensorium Virt, `P094-018` | contained mutations and uncertain outcomes |
| Offer draft, publication, and withdrawal | `P094-007` | federated profile only |

The acceptance runner must refuse to start while a required gate is missing and
must say which one.

## Non-Goals

- Changing the requester's real mail server, DNS, TLS certificates, or firewall.
- Internet-facing deployment, spam filtering, or arbitrary package installation.
- Giving the solver or the requester terminal or file-write authority.
- Automatic publication, automatic HIL approval, or plan-level approval.
- qmail-specific code in shared Node crates.

## Open Questions

- **First acceptance architecture.** P094 names one Debian amd64 image manifest.
  Running the local profile on macOS with vfkit needs an arm64 variant, which the
  profile's `image-variants` list can carry. The first acceptance host decides
  which variant is built first; the story contract does not change.

## Done When

- [ ] The pack builds reproducibly: `derive_pack_facts` produces every digest and
  capability list, and conformance recomputes them.
- [ ] A clean install, activation, and binding from safe defaults reach `runnable`
  with no hand-typed digest.
- [ ] The local profile repairs the fixture through observation-first
  deliberation, one HIL approval per mutation, and a passing verifier, then
  destroys the instance with confirmation (`P094-013`).
- [ ] An open-relay "repair" is refused by the verifier in a retained negative
  run.
- [ ] Every refusal case above is reached at its owning boundary.
- [ ] Restart, pause/resume, crash with an `unknown` step, and revocation behave
  as specified.
- [ ] The federated profile delivers the recipe to a remote requester that
  admitted the exact profile digest, and a stale offer is refused after
  revocation (`P094-016`).
- [ ] A structural check shows that shared P094 crates contain no qmail-specific
  branch.
