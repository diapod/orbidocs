# Story 012: Remote Agents Solve a Problem Through a Shared Chair Terminal

Status: Implemented; baseline, vfkit manifest-repair, and additive
PowerDNS/Bielik single-host acceptance pass

Related:

- [Story 011: Corpus answers the fish-water question](story-011-corpus-fish.md)
- [Proposal 069: Corpus](../40-proposals/069-corpus.md)
- [Proposal 073: Agent Orchestration Organ](../40-proposals/073-agent-orchestration-organ.md)
- [Proposal 082: Sensorium Interfaces](../40-proposals/082-sensorium-interfaces.md)
- [Solution 036: Room](../60-solutions/036-room/036-room.md)
- [Solution 038: Corpus](../60-solutions/038-corpus/038-corpus.md)
- [Solution 042: Sensorium Workbench](../60-solutions/042-sensorium-workbench/042-sensorium-workbench.md)
- [Solution 046: Sensorium Interfaces](../60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md)
- [Solution 047: Agent](../60-solutions/047-agent/047-agent.md)

## Summary

As a node operator, I want three model-backed participants on separate Orbiplex
nodes to deliberate through a shared Room while the chair exposes a bounded,
read-only view of its Workbench terminal. The participants should use the same
current terminal state as evidence, propose a solution, and leave terminal
actuation under the chair node's local authority.

This story composes existing contracts rather than introducing a second agent,
terminal, or collaboration runtime:

- Corpus supplies the deliberation policy, roles, and inert answer draft;
- Agent supplies one bounded controller on each participating node;
- Inquirium supplies model inference to each Agent;
- Room supplies membership and the network collaboration carrier;
- Sensorium Workbench owns the chair-side PTY and command execution;
- Sensorium Interfaces publishes its bounded visible viewport;
- the destination daemon resolves a generic Agent observation need through
  Interaction Broker and the Room/Sensorium adapter.

The active execution profile is the VFKit-backed variant from the shared Story 012
vertical: a digest-pinned full-system guest is started and observed as the chair
terminal source, with additive vfkit/profile wiring from the Story 012 acceptance
trackers (including the critique-gated extension). In practice, this story is
implemented and validated as the same deliberation/repair loop over a Workbench
runtime backed by that VM environment, with direct control remaining local to the
chair node.

The profile is executable. Its process runner reuses the extracted Story 011
three-node federation/bootstrap layer, then composes the Workbench, Sensorium
Interface, Room observation, Agent, and story fixture layers without creating a
second trust bootstrap or collaboration runtime.

The three node processes use distinct loopback addresses on one host. This is
explicitly multi-address single-host acceptance: it strengthens HTTP/WSS process
and TLS-identity evidence, but does not claim multi-host deployment, public relay
reachability, NAT traversal, or independent host failure domains. Those remain
owned by the P070 deployment profiles.

An explicit `single-address-single-host` fallback allows unattended execution
without privileged loopback aliases. It preserves process and port isolation
but is intentionally weaker than the default address-distinct profile and is
reported as such.

## Concrete Problem

The chair node owns a small fixture whose deterministic manifest test fails
because input paths are emitted in filesystem iteration order rather than in
canonical lexical order.

The expected collaboration is:

1. the chair-side operator runs the failing test in a Workbench terminal;
2. the remote implementer Agent observes the bounded visible viewport and
   proposes canonical ordering before digest calculation;
3. the remote reviewer Agent asks for a regression case proving that different
   input enumeration orders yield the same manifest;
4. the chair Agent synthesizes the proposals into an inert action plan;
5. the local operator applies the change and reruns the test;
6. all admitted Agents observe the passing terminal state; and
7. Corpus accepts the chair Agent's terminal outcome as an unpublished answer
   draft with evidence references.

The exact fixture may change without changing the story contract. It must remain
small, local, deterministic, network-independent, and incapable of accessing
credentials or the operator's ordinary working tree.

## Actors

- **Node A / chair node** owns the Corpus query, Room authority, chair Agent,
  isolated Workbench workspace, terminal session, and Sensorium Interface
  publication. Its local operator remains the only terminal actuator in the
  first profile.
- **Node B / implementer node** runs a Room-attested Corpus participant Agent. It
  may deliberate and observe the shared terminal only after receiving both Room
  membership and an exact Sensorium Interface observation grant.
- **Node C / reviewer node** runs a separately admitted participant Agent under
  the same dual-authority rule. It reviews the diagnosis and the proposed
  regression evidence but receives no terminal-control authority.

Agents remain node-local. The story federates observations and deliberation; it
does not migrate an Agent runtime or its private memory between nodes.

## Architectural Profile

```text
Node A Workbench PTY
  -> bounded visible-screen projection
  -> Sensorium Interface resource
  -> exact participant-scoped observe grants
  -> active Room relay epoch over WSS
  -> Node B / Node C Room recipients
  -> host-owned observation admission
  -> bounded Agent passage context
  -> Inquirium
  -> inert Corpus reasoning turns
  -> Node A chair Agent
  -> unpublished Corpus answer draft
```

The terminal screen is not a Room message and is not appended to the Corpus
transcript. Room carries a cursor-free, coalesced
`sensorium-interface-read-result.v1` containing one inline `latest-state`
snapshot. The source cursor, PTY handle, source credentials, and Workbench lease
remain local to node A.

## Flow

1. Node A creates the Corpus query and opens a bounded Room under the same policy
   and invite model used by Story 011.
2. Nodes B and C accept signed Room invitations and create narrowed
   `collaborative-participant` Agent bindings. Node A creates the corresponding
   `collaborative-chair` binding.
3. Node A creates an isolated Workbench terminal session under an allowlisted
   story workspace, pins `sensorium-operational-context.v1` with
   `impact/class = test` to that exact environment, and starts the deterministic
   failing fixture.
4. Node A publishes only the visible terminal-screen representation as a
   `latest-state` Sensorium Interface. Ordered terminal-event replay is refused.
5. The host issues exact, expiring `subscribe` grants for that interface to the
   admitted B and C participant subjects. Room membership by itself does not
   satisfy this step. The first profile does not add an independent one-shot
   `read` grant.
6. The active Room relay projects the view only to recipients in the intersection
   of current Room observation rights and current Sensorium Interface grantees.
7. Each Agent binding fixes a generic need, opaque source ref, payload schema,
   freshness, and byte bound. The recipient daemon resolves that need through its
   Room/Sensorium adapter and validates the read result, inline interface frame,
   Room, relay epoch, Room membership source sequence, recipient, Agent binding,
   classification ceiling, byte cap, exact source generation, operational context,
   effective publication, and freshness before producing ephemeral inert context.
8. The Agent controller uses the accepted latest state in one bounded passage.
   The durable step trace contains only schema, refs, classification, policy
   digest, and content digest; it contains no terminal bytes or prompt text.
9. B and C publish inert Corpus reasoning turns through the existing
   `corpus.room.turn` effect and human-in-loop policy. They do not invoke the
   terminal.
10. The chair Agent proposes a bounded next action. In the first profile, only
    local control on node A may enact terminal input, command execution, resize,
    signal, patch, or file mutation through Workbench.
11. The host revokes C's exact interface grant and waits until the source-side
    projection reports the reduced recipient set. C is refused before any repaired
    terminal state exists.
12. Node B is dirty-restarted to prove durable Agent and invitation recovery without
    retaining terminal content in the recipient process.
13. After the local operator applies the accepted change and reruns the fixture,
    the latest-state projection shows the passing result to all still-authorized
    participants. B observes the new source version; C remains refused.
14. Corpus accepts the chair's `agent.outcome.v1` as an inert answer draft.
    Rendering, publication, settlement, and durable terminal capture remain
    separate transitions.

## Authority Contract

The story requires two independent authorities for every remote observer:

1. current Room membership with the relevant observation right; and
2. a current exact-resource Sensorium Interface `subscribe` grant.

Neither authority implies the other. In particular:

- Room membership does not grant access to the terminal view;
- an interface grant does not admit its holder to the Room;
- terminal subscription does not grant `sensorium.interface.read`,
  `sensorium.interface.invoke`, or
  `sensorium.interface.manage`;
- a participant Agent cannot use terminal input, resize, signal, command, patch,
  or file-write operations;
- the chair Agent does not gain ambient Workbench authority merely because its
  operator owns the terminal; and
- revoking either authority stops future delivery without closing the durable
  Room.

## Observation-To-Agent Boundary

The Agent contract is horizontal. `agent-core` carries only a bounded
`AgentObservationNeed`, a durable `AgentObservationBinding`, and prompt-free
resolution evidence. Their source refs are opaque; the core neither imports nor
interprets Sensorium, Workbench, Room, or provider types.

Operator-authored JSON-e Flow configuration may predeclare a bounded mapping from
`need/ref` to `source/ref`, payload schema, freshness, and byte limits, together
with separate grant requests. The configuration is schema-validated and
digest-pinned. Rendered flow data may select or narrow a predeclared mapping but
must not construct or widen one, and Agent/model/observation data never
interpolates an authority-significant wiring field.

The destination daemon is the composition root. For this story it selects the
Room/Sensorium resolver, which:

- binds the read result and its single inline snapshot to the exact interface,
  Room, relay epoch, Room membership source sequence, recipient subject, Agent,
  durable Agent binding, and generic observation need;
- rejects unbound, dynamically selected, changed-schema, or widened-bound needs
  before source I/O;
- rechecks both Room and interface authority before and after the broker read;
- admits only the declared terminal-screen snapshot schema and `latest-state`
  delivery profile;
- enforces classification, age, item-count, and byte ceilings before prompt
  assembly;
- coalesces superseded snapshots rather than replaying terminal history;
- exposes the accepted observation as inert context, never as an effect request;
- records only prompt-free generic metadata, the validated source
  `causal/context`, source-version/ref, resolution/ref, policy evidence, and a
  host-keyed content digest in durable Agent trace; and
- discards terminal bytes after the bounded passage unless local control performs
  a separate classified Workbench capture.

Responsibility for summarizing terminal content belongs to a separately
authorized component. The Agent context bridge may select and bound an existing
snapshot, but it must not silently become a transcript store or summarizer.

## Substrate Gates

| Gate | Current state | Required evidence before execution |
|---|---|---|
| Story 011 Corpus/Agent deliberation | available | selected participant and chair Agents deliberate over Room with restart-safe bindings and inert final draft |
| Room Phase 6A relay | available | three-node member-visible WSS relay carries bounded Room and Sensorium Interface payloads with epoch fencing |
| Workbench terminal source | available | isolated PTY, bounded visible-screen snapshot, exact environment generation/context, local actuation authority, and classified explicit capture |
| Sensorium Interface Room projection | available | exact grants, complete context-bearing `latest-state`, recipient intersection, host-only terminal status, supersession, revocation, recipient-side restart recovery, and no terminal control; the source-host pump remains process-local and must be recreated after a source-host restart |
| Agent observation admission | available | substrate-neutral need/binding/evidence in `agent-core`, bounded neutral context qualifiers, preserved P081 source causality, static fail-closed JSON-e wiring, daemon-owned Room/Sensorium resolution, process-local revocable latest-state inbox, resource-bound Interaction Broker source, host-owned pre-inference caution, prompt-free trace, and restart/retention refusal tests |
| Story 012 process runner | available | the baseline runner extends the shared Story 011 topology; the additive vfkit v2 profile runs the pinned guest fixture and full collaboration through one Workbench runtime without copying trust/bootstrap logic |

The acceptance pack must refuse execution while any gate is missing. Marking a
documentation row complete is not sufficient evidence; the runner must probe the
corresponding runtime surface or execute its refusal vector.

## Acceptance Profile

The operator-facing pack lives in:

```text
node/tools/acceptance/story-012-shared-chair-terminal/
```

Its checked-in profile is executable through `profile_plan.py smoke`. The shared
`three_node_federation.py` layer owns profile rendering, federation-root
bootstrap, process lifecycle, and dirty restart for both Stories 011 and 012.
The Story 012 runner adds only Workbench, Sensorium Interface,
Agent-observation, Room-deliberation, and deterministic fixture behavior.

The smoke activates the local relay epoch through a reserved `.invalid`
endpoint because it is proving composed authority and lifecycle behavior, not
network deployment. P070's separate multi-process host-TLS acceptance remains
the deployment evidence for the external relay boundary.

The composed profile binds every required refusal to named executable evidence.
The process smoke directly proves:

- three distinct daemon identities and node-local Agents;
- signed Room invite and membership admission for B and C;
- no terminal view before the exact interface grant exists;
- no view from Room membership alone or from an interface grant alone;
- cursor-free bounded latest-state delivery over the active Room relay epoch;
- exact generic need/binding plus refusal of a binding belonging to another Agent;
- refusal of unbound, dynamically interpolated, changed-schema, or widened source
  mappings before source I/O;
- B and C can deliberate from the shared view but cannot invoke or manage it;
- B and C receive the same source-owned `test` operational-context qualifier before
  their first feed-dependent turn, while publisher summary text remains unprivileged;
- C's revocation converges before repair, stops both the current read and the new
  passing-state read, and leaves the Room plus B active;
- dirty restart of recipient B restores its durable Agent and Room invitation while
  its process-local observation inbox starts empty and refreshes from current state;
- terminal bytes do not enter Room messages, Memarium Agent facts, status,
  notifications, or prompt-free traces;
- A raises the effective context to `production` through an immutable replacement;
  B's old statically bound Agent refuses the superseded publication and a new exact
  binding admits the replacement, while C remains refused;
- the passing result is observed after local chair-side actuation; and
- the chair outcome remains an unpublished Corpus answer draft.

Lower-stratum suites named in `profile.json` prove wrong Room, interface and
participant binding, conflicting relay-position digests, stale relay epochs,
classification ceilings, ordered-event refusal, and remote actuation refusal. This
keeps protocol conformance in P070/P082/P083 while making the Story-level evidence
ownership closed and machine-validated instead of implying that one process runner
duplicates every lower-layer test.

The post-MVP operational-context extension tracked by P082, P064, P069, P071, and
P073 is implemented. The composed smoke proves that B and C receive the same source
context qualifier before their first feed-dependent Inquirium call, that publisher
summary text is not retained as privileged instruction evidence, and that a monotone
`test -> production` host floor is published only through immutable replacement. The
old Agent binding refuses the superseded `interface/id`; the replacement requires a
new exact binding and current grant. Missing, malformed, oversized, stripped,
downgraded, generation-mismatched, or superseded context fails the collaborative
observation passage closed before terminal bytes reach a model, with lower-stratum
P064/P071/P082 tests owning the vectors that the composed story does not duplicate.
P082 owns this freshness predicate; Story 012 adds no TTL.

The additive `profile-vfkit-full-system.json` keeps the completed baseline
unchanged while proving the stronger vertical in one Workbench runtime. Version 2
boots the pinned full-system guest, verifies the digest-pinned in-guest repair
fixture, projects failing and passing PTY state through P082, fences repair through
P083, and runs the same three-node collaboration, revoke, dirty restart, export,
and inert Corpus-draft lifecycle. Its schema-gated report names the evidence
boundary `single-runtime-vertical`; it does not infer that claim from independent
harness results.

The additive `profile-powerdns-bielik-vfkit.json` is the first full-system
service-configuration specialization. The image builder pins
`pdns-server=4.8.3-4build3`, `pdns-backend-bind=4.8.3-4build3`, the closed
PowerDNS fixture, and the final image digest. Build-time vfkit NAT exists only
while obtaining those exact Ubuntu packages; runtime vfkit still has no NIC,
host share, or SSH service.

Nodes B and C each supervise a separate direct local `llama-server` over HTTP
and select the same stable Bielik alias through their own Inquirium runtime
candidate. The acceptance consumer verifies the actual Agent product in the
daemon object store by digest and uses its bounded text as an inert Corpus turn.
No model output is interpreted as a command. After the existing HIL gate, node A
alone may apply bounded host-owned experiments and the checked-in deterministic
configuration through P083 exclusive leases. Success requires PowerDNS to listen
only on `127.0.0.1:53`, answer
authoritatively for `localdomain`, and return exactly `a -> 127.0.0.1`,
`b -> 127.0.0.2`, and `c -> 127.0.0.3`. The report consumes the guest's
structured PASS evidence and retains the observed transaction ids, expected and
actual addresses, and localhost peer rather than reconstructing a declarative
success list.

The current additive runner strengthens the deliberation without widening that
effect boundary. The requester query is the opening contribution; accepted
Corpus instruction overlays frame B as `solver` and C as `reviewer`. A controlled
Chair Agent maps Corpus `baton` to Room `round-robin`, producing the ordered cycle
`requester context -> solver -> reviewer`. The soft deadline is five minutes,
the structural guard is 64 cycles, and at least two cycles are required. After
the first solver/reviewer pair, node A applies one bounded deliberately incorrect
CandidatePlan through a short-lived P083 lease; the DNS verifier rejects it and
the failure becomes fresh read-only terminal evidence for the second cycle. That
cycle observes the newer terminal state before node A submits a distinct corrected
CandidatePlan through a fresh Agent decision, HIL decision, and P083 lease. Both
plans are currently constructed by host-owned acceptance code and bound to solver
turns; their commands are not derived from the model text. The profile therefore
proves feedback and control mechanics, not causal authorship of the plans by the
deliberating Agents. Natural-language output is never compiled into terminal input.
The checked-in fixture is permitted only after the deadline as explicit diagnostic
recovery; a run that needs it cannot emit the promoted 17-check report.

This bounded executor keeps the acceptance effective even when node A has no
local model or terminal-capable Agent: it can execute only the host-owned
experiment catalog and fixture. It does not solve the general transfer of
deliberation intent into actuation. That later path must carry a typed inert
`inquirium.candidate-plan.v1` or experiment proposal from the deliberation,
attribute it to the requester-selected executor, join node A's admission, and
compile through the ordinary Sensorium boundary. The requester may select a
local host compiler, a local Chair Agent, or a remote Chair/designated participant
Agent. The first implemented vertical enables only the local Agent; the other modes
fail daemon admission until their passage adapters have evidence. Room role and
membership never imply terminal authority: remote execution
uses the P083 / Solution 046 Sensorium Interactive Interfaces
claim/control/invoke path and still requires a separate resource-scoped Sensorium
grant, current generation, bounded lease, review policy, and local refusal path.
Free-form Room text is never an executable fallback.

### Critique-gated technical deliberation successor

The additive `ready` profile
`node:tools/acceptance/story-012-shared-chair-terminal/profile-powerdns-bielik-critique-gated-vfkit.json`
closes that causal gap without turning Room prose into terminal input. Its Room
policy permits bounded shell fragments, file paths, configuration fragments,
diagnostic and verification commands, and rollback instructions as inert technical
evidence. It rejects credentials, binary payloads, unbounded scripts, ambient
authority claims, and direct terminal input. The profile narrows the ordinary
64 KiB Room message ceiling to 16 KiB per technical contribution.

The baton becomes
`requester opening -> solver -> reviewer -> Chair`. A solver contribution must
state a hypothesis, evidence refs, proposed changes, verification, and rollback,
and must publish a content-addressed inert CandidatePlan. The reviewer emits an
exactly bound `accept|revise|reject` judgment over the proposal digest and fresh
terminal-state digest. `revise` must identify a replacement CandidatePlan rather
than silently changing prose. The Chair defaults to `block` and may emit only
`block`, `request-revision`, or `admit-reviewed-candidate`, bound to the exact
review and reviewed plan digest.

Chair admission still does not execute anything. Node A validates the selected
artifact, compiles a pending InquiryFlow, rechecks current grants, classification,
budget, generation, idempotency, and Room authority, obtains HIL for the exact
effect, and invokes Workbench only through P083 `claim -> invoke -> release`. A
missing review, stale terminal-state binding, digest mismatch, rejected proposal,
or unavailable Chair resolves to no effect. No control lease spans inference.

The typed Corpus review and Chair-decision contracts, Agent-product-bound
CandidatePlan publication path, durable host admission, critique-gated runner, and
closed 26-check report revision are implemented. A retained 2026-07-25 macOS arm64
run passes all 26 checks with two real Bielik runtimes and no deadline fixture.
The deterministic fixture cannot satisfy that evidence claim.

### Model-authored discovery successor

The stronger additive `story-012-powerdns-bielik-discovery-vfkit` profile removes
the ready PowerDNS solution wrapper from the guest and from every model-facing prompt. The
solver emits closed structured process or file-write intents; the Agent compiles
the exact values into a content-addressed CandidatePlan; the reviewer may publish
a replacement through the same requester-owned policy; and the Chair can select
only the exact reviewed publication. HIL and P083 remain the only actuation path.
The legacy fixture is isolated outside discovery mode and cannot satisfy the
discovery report.

The requester also owns a staged admission policy. After the read-only bootstrap,
each passage may mutate exactly one path already present in active terminal
configuration. A later stage may follow a file path authored by an earlier model
plan only after that path appears in the active configuration. The stage selector
encodes solution-aware listener, declaration, and zone-data sequencing, and its
selected scope is disclosed to solver and reviewer. It does not author bytes or
decide whether the DNS goal is met. The model authors review findings and an
optional replacement, while host policy constrains the admissible verdict for a
phase; this profile does not claim an epistemically independent reviewer verdict.
Full CandidatePlan digests, terminal completion markers, host-derived bounded and
non-truncated effect projection, retained provisioning inventory, reviewer
replacement, and restart-safe append-only facts remain checked.

The diagnostic ladder is intentionally cheaper than the deployment story. Pure
contract tests run first; deterministic replay exercises policy, review, Chair,
and inert-effect transitions over recorded values; a real-model bench measures
one planning stage without daemons, Room, or VM; only then may the vfkit profile
run as deployment evidence. Every real-model sample records prompt, evidence,
response, usage, duration, verdict, and a digest of all policy/model/runtime inputs.

The original 2026-07-29 Bielik calibration did not justify deployment smoke. Its
path-aware active-directive oracle accepted two of five retained scoped
zone-declaration samples, while both measured zone-data stages produced no
goal-ready correction. That result remains useful negative evidence rather than a
passing profile claim.

The bounded 2026-07-30 role matrix then compared pinned local candidates over 130
samples without daemons, Room, or VM. Qwen2.5-Coder 7B produced 26 goal-ready and
46 policy-admitted plans from 50 solver attempts, including 9/10 ready plans on
the failed-plan correction case. Qwen3.5 4B produced 2 ready and 30 admitted plans
from 50 attempts and no ready correction. Qwen2.5-Coder 7B therefore remains the
solver default. None of the reviewer candidates crossed the deployment gate:
Qwen2.5-Coder 3B, Qwen2.5-Coder 7B, and Phi-4 Mini had 0/10, 1/10, and 2/10
contract-admitted replacements respectively, and all had 0/10 ready replacements.
The matrix records no reviewer deployment selection; Phi-4 Mini is only the best
observed next challenger. The current-profile model-only four-pair p95 sum is
528,400 ms, but a full authority budget still requires measured HIL,
P083, terminal, and verifier latency.

The selected deployment profile now carries both guest-attested challenge
descriptors. Its passing retained run selects
`powerdns-bind-missing-zone-data.v1`: PowerDNS already has a valid loopback
listener, BIND backend, and authoritative declaration, but the referenced
zone-data file is absent and no final `localdomain` records exist in the image.
The prepared-system manifest, completion record, fixture digest, and image digest
bind that initial state before vfkit starts. This proves the second variant only;
it does not turn one retained run into a general claim over all prepared systems.

The role boundary now has an additive v2 correction path. A reviewer can emit one
bounded `request-regeneration` correction without plan bytes; the daemon binds it
to the source proposal and shared correction-state digest, the solver authors a
fresh proposal, and a fresh review must bind that successor before Chair admission.
The join is append-only, restart-safe, and inert until the existing host, HIL, and
P083 gates run. A 2026-08-01 ten-pair Qwen2.5-Coder 7B calibration produced ten
valid requests but only one domain-ready staged successor. The mechanism is
therefore implemented, while model deployment readiness remains explicitly open.

The stronger `story-012-powerdns-qwen25-coder-discovery-vfkit` profile has one
retained passing macOS arm64 full-system run. Two separately supervised
Qwen2.5-Coder 7B runtimes completed two round-robin cycles against the second
challenge. The first model-authored plan was admitted through HIL and P083 but did
not satisfy the verifier; after fresh terminal evidence, a different model-authored
plan reached the exact DNS goal. The closed report passes 30 checks, records
16,577 prompt-plus-completion tokens, 516,110 ms of model time, 544,637 ms of
deliberation, and 794,192 ms end to end, and reports the host-owned structural
`umask 022` framing separately from unchanged CandidatePlan bytes. It uses no
deadline fixture and derives no effect directly from Room prose. This is one
deployment proof, not yet repeatability evidence and not evidence that the
critique-to-regeneration v2 path has crossed its separate `0.6` promotion gate.

For reproducibility, the story policy supplies a closed allowlisted command-plan
template to the solver. The real model must carry the exact CandidatePlan marker in
its verified Agent product, and the acceptance runner publishes those retained
bytes with the product ref and digest; there is no prose fallback. This proves
typed product provenance and critique authority, not unconstrained plan synthesis.

The host bounds approval pressure independently from the story fixture: it
admits two distinct experiment proposals per round by default, permits an
operator override only up to eight, and does not charge exact proposal or
idempotency replay as a new proposal. Each plan remains independently limited to
one effect proposal by default and eight at the hard ceiling.

Its evidence boundary is deliberately `single-host-full-system`: the three Node
processes, two local model processes, and one full-system VM cross real
HTTP/WSS, PTY, and vsock boundaries on one macOS host. This is not evidence for
separate host failure domains. Structural validation is complete; a `passed`
report was retained from the 2026-07-24 expensive run with real `llama-server`,
Bielik GGUF bytes, and the prepared PowerDNS image. The run completed in
155,637 ms, including 45,496 ms of deliberation, and records distinct
host-issued inference refs for B and C. Equal product digests remain valid for
deterministic responses and are not used as execution identity.
The profile therefore proves two separately supervised invocations whose
returned bytes converged; it does not claim epistemically independent first
judgments. Such a stronger claim would require an explicit isolation and
diversity policy rather than an output-digest inequality check.
The duration is an observed wall-clock measurement, not a cold-cache benchmark:
model and operating-system cache state was not controlled by this profile.
The retained report also proves the role-aware multi-cycle extension: distinct
solver and reviewer roles, two round-robin cycles, a verifier-rejected first
experiment followed by a host-submitted corrected CandidatePlan after fresh
terminal feedback, Agent `propose` decisions, admitted HIL, and separate P083
`claim -> invoke -> release` lifecycles. Its closed evidence records zero effects
derived directly from Room prose; it does not claim that either plan was derived
from that prose.
The retained report is
`node:tools/acceptance/story-012-shared-chair-terminal/reports/2026-07-24.story-012-powerdns-full-system.macos-arm64.json`
with file digest
`sha256:706e1c78f069a2277cb86dde79919880e6450a1505d2aa8df08d26ab0a739de4`.
This additive post-MVP profile is manual or dedicated-runner evidence and does
not replace, reopen, or gate the completed baseline Story 012 acceptance.
The report is registered in Schema Gate with positive and fail-closed duplicate-
check fixtures; structural schema passage still does not substitute for a real run.

The Story consumer validates `bytes/base64`, `bytes/count`, and `bytes/sha256`
before interpreting a terminal marker. Chair admission also uses the current Room
membership high-water sequence rather than a creation-time or fixture constant.

## Failure Modes and Mitigations

| Failure mode | Risk | Mitigation |
|---|---|---|
| Room membership is treated as terminal authority | unauthorized observation | require the exact current interface grant independently on every delivery and Agent admission |
| Remote Agent receives an actuation grant | participant controls the chair terminal | close the observer capability set to `read` and `subscribe`; refuse `invoke` and `manage` in profile validation |
| Old screen snapshots are replayed as a transcript | stale or excessive context | use cursor-free coalesced `latest-state`; reject ordered-event interfaces |
| Terminal bytes enter durable Agent memory | credential or source leakage | retain only refs, classification, policy digest, and host-keyed content digest |
| A technical Room fragment is treated as executable input | prompt injection crosses into Workbench | keep prose inert; require a content-addressed CandidatePlan, bound review, Chair decision, host admission, HIL, and P083 |
| Chair admits a plan other than the one reviewed | critique is bypassed after approval | bind Chair decision to review ref and reviewed plan digest; mismatch resolves to `block` |
| Revocation closes the Room | collaboration state is lost with one view | close only the projection/subscription and preserve the durable Room |
| Restart silently widens authority | stale grants or relay epochs revive | rebuild from durable facts, recheck revocation, and require a fresh current-state delivery |
| Agent or observed data changes source wiring | confused deputy selects an authority-bearing source | accept only operator-authored, digest-pinned static mappings; rendered flow data may select or narrow but never create or widen them |
| Story runner duplicates Story 011 trust logic | two drifting federation bootstraps | compose or extract the existing topology/bootstrap helper before implementing the runner |
| Chair Agent becomes terminal operator by implication | observation and effect authority are complected | keep first-profile actuation local-control-only and require a later explicit effect profile for Agent-driven commands |

## Non-Goals

- Giving every participant interactive terminal control.
- Sending raw PTY input or ordered terminal events as ordinary Room messages.
- Persisting a full terminal transcript automatically.
- Migrating Agent state between nodes.
- Requiring a non-member federation relay or a public Matrix homeserver.
- Treating terminal observation as evidence that a proposed diagnosis is true.
- Letting an Agent publish the final Corpus answer or enact changes by itself.

## Done When

- [x] The story document and executable acceptance profile agree on topology,
  authority, data lifetime, and refusal behavior.
- [x] P069 and P073 track the substrate-neutral Agent observation port,
  daemon-owned Room/Sensorium resolver, and composed process evidence.
- [x] The profile validator rejects terminal actuation grants,
  membership-as-authority, ordered-event delivery, and durable terminal content.
- [x] Every substrate gate has executable evidence and is marked available.
- [x] The composed three-node smoke completes the concrete problem from failing
  test through independent B/C deliberation, C revocation, dirty B restart, local
  repair, passing-state observation by B plus continued refusal for C, and an
  unpublished answer draft.
- [x] The additive vfkit v2 profile proves full-system, interface/fencing, and
  collaborative behavior through one Workbench runtime without weakening or
  relabeling the completed baseline.
- [x] Terminal marker checks consume verified byte evidence and Chair authority
  binds the current Room membership high-water sequence.
- [x] One-runtime vfkit Story 012 evidence uses a digest-pinned guest fixture
  rather than a host-path copy and emits the closed
  `story-012-vfkit-full-system-report.v1` artifact.
- [x] Retain one passing `story-012-powerdns-full-system-report.v1` from the
  additive post-MVP single-host profile using two real local Bielik runtimes and the
  exact PowerDNS guest image. The profile, runner, digest-verified Agent-product
  bridge, deterministic host-owned actuation fixture, localhost/DNS assertions,
  structural tests, and schema-gated closed report validator are implemented.
  The 2026-07-24 retained report proves the real run independently of those
  structural gates.
- [x] Implement the additive role-aware PowerDNS deliberation runner: requester
  opening, solver/reviewer overlays, Corpus `baton` to Room `round-robin`, two
  required and at most 64 cycles under a five-minute deadline, one bounded
  verifier-rejected guest experiment, a separately admitted corrected CandidatePlan
  from fresh terminal evidence, append-only proposal/flow/operation/receipt
  execution projections, restart quarantine without blind retry, and fresh P083
  leases. Fixture fallback is forbidden before the deadline and cannot produce a
  passing 17-check report.
- [x] Run the expensive role-aware profile with real Bielik runtimes and vfkit,
  and replace the retained report only after its closed `deliberation` evidence
  passes the exact 17-check profile validator and Schema Gate. The retained
  2026-07-24 report proves separate roles, two round-robin cycles, failed and
  corrected experiments, Agent `propose`, HIL, P083 lease release, and no effect
  derived directly from Room prose.
- [x] Add the first adaptive follow-up profile in which a typed inert
  `inquirium.candidate-plan.v1` or experiment proposal crosses from Corpus
  deliberation to the requester-selected local Chair Agent. The portable policy
  also names deterministic local compiler, remote Chair Agent, and designated
  participant Agent modes, but daemon admission rejects those modes until their
  passage adapters have executable evidence. Every plan remains inert until node A verifies
  attribution and a separate
  resource-scoped Sensorium grant, review, classification, generation, lease,
  budget, and idempotency policy. The implemented local vertical binds the signed
  proposal to a retained solver turn and the author's Room invite, compiles a
  pending `InquiryFlowV1`, prepares fresh latest-state evidence, performs an Agent
  passage, verifies the content-addressed Inquirium product under a closed
  `propose|no-effect` decision contract, and prevents `no-effect` from claiming or
  invoking. For `propose`, node A rechecks the exact flow node, interface, grant,
  generation, operational context, method, input schema, payload digest,
  classification, lease ceiling, and proposal expiry, requires an admitted
  operator-question decision, and lets
  P083 acquire and release the lease only around invoke. Execute future admitted
  remote control through P083 / Solution 046 rather than a Story-local proxy;
  the remote executor carrier remains additive work and is not claimed by this
  local evidence. Free-form prose is rejected as effect authority.
- [x] Define the additive critique-gated technical deliberation profile with
  bounded shell/configuration guidance as inert Room evidence, ordered
  `solver -> reviewer -> Chair` control, fail-closed Chair decisions, exact digest
  lineage, and unchanged HIL/P083 effect authority. The checked-in profile is
  structurally validated and marked `ready`.
- [x] Freeze typed `corpus-reasoning-experiment-review.v1` and
  `corpus-reasoning-chair-experiment-decision.v1` contracts, plus positive and
  fail-closed fixtures for missing review, stale terminal evidence, unbound
  replacement plans, digest substitution, and Chair bypass.
- [x] Implement the critique-gated runner and Agent-authored CandidatePlan
  publication path. It must prove an unsafe technical proposal is blocked with no
  lease or effect, then prove a reviewer-accepted or reviewer-revised exact plan
  crosses host admission. Host-constructed fixtures cannot satisfy this gate.
- [x] Add a closed 26-check report revision proving technical proposal lineage,
  reviewer verdict, Chair decision, exact admitted plan digest, HIL, P083 lifecycle,
  and zero direct effects from Room prose.
- [x] Retain one real vfkit/Bielik run that passes the closed critique-gated report
  validator without using the deadline-only deterministic fixture. The retained
  2026-07-25 macOS arm64 run passes all 26 checks with two round-robin cycles, one
  failed experiment, one reviewed correction, HIL, and P083 lease release.
- [x] Implement the model-authored discovery contracts, solution-free guest
  fixture, structured intent compiler, reviewer replacement, full-plan terminal
  digest binding, staged active-configuration-derived mutation scope, real-model
  bench, deterministic replay, append-only calibration ledger, closed report
  schema, and fail-closed profile validator.
- [x] Measure the pinned Bielik 4.5B Q8 planning ceiling before deployment smoke.
  The scoped declaration stage reaches two ready plans in five re-evaluated
  samples; both measured zone-data stages reach zero ready plans in five samples.
- [x] Complete the discovery correction loop with a bounded three-attempt
  causal lineage and terminal-delta projection. Preserve exact plans host-side,
  expose normalized process calls and digest-only historical file-write identity
  to the models, carry bounded reviewer findings and verifier outcomes, and
  exclude historical payload bytes and hidden reasoning from prompts. A file value
  later observed in the active configuration remains fresh terminal evidence.
  Solver and reviewer now receive the same closed
  `story-012.powerdns-correction-state.v1` value.
- [x] Add a deterministic novelty gate and structured reviewer findings. The
  implemented first slice rejects an exact failed read-only experiment, or a
  subset of the same failed probes plus service activation, emits a typed inert
  refusal, and requires any reviewer replacement to pass the same gate. Replay
  records the redundant original decision and novel selected decision separately.
- [x] Add a relevant-precondition digest and extend deterministic novelty rejection
  to exact failed file mutations only while challenge, VM generation, resolved
  admission scope, literal configuration, normalized service state, and verifier
  state remain unchanged. The projection consumes only the last complete
  nonce-marked, host-owned read-only snapshot from the cumulative PTY feed; a
  changed digest keeps the retry novel. The gate checks all three retained
  experiments rather than only the immediately preceding attempt.
- [x] Benchmark solver and reviewer candidates independently with at least ten
  samples per discovery stage. Compare the pinned Qwen2.5-Coder 7B solver baseline
  with a runtime-conformant Qwen3.5 4B challenger, and evaluate
  Qwen2.5-Coder 3B plus Phi-4-mini for the lower-latency reviewer role. Select by
  domain correction success and measured latency, not a general leaderboard. The
  130-sample matrix retains Qwen2.5-Coder 7B as solver and deliberately leaves the
  reviewer deployment default unset because none of the candidates produced a
  ready replacement.
- [x] Replace accumulated experiment prose with one bounded state capsule carrying
  at most three exact host-side lineages, prompt-safe effect summaries, learned
  facts, refuted assumptions, next tests, terminal delta, and effective scope.
  Process summaries include canonical argv digests. The closed acceptance report
  retains bounded review analysis, the relevant-precondition digest, and original
  plus selected typed novelty decisions, while leaving raw precondition state and
  historical file bytes in runtime/replay evidence rather than retained metadata.
- [x] Add an additive critique-to-regeneration path in which the reviewer may emit
  bounded typed findings without authoring a replacement CandidatePlan, the solver
  regenerates a candidate from those findings and the shared correction-state
  capsule, and the regenerated candidate receives a fresh review before the Chair
  may select it. Bind every transition to the original proposal, terminal evidence,
  correction-state digest, and regenerated plan digest; apply the same novelty,
  policy, budget, and host-admission gates as for any other candidate. Keep the
  current reviewer-authored `revise` replacement contract valid as a compatibility
  path. The v2 review and regeneration schemas, negative fixtures, signature golden
  vectors, append-only daemon join, restart recovery, requester-owned API, live
  baton integration, strict role grammars, host-side current-role and
  effective-membership checks for exact `implementer` and `reviewer` assignments,
  and prompt-free replay are implemented.
- [ ] Promote critique-to-regeneration from opt-in mechanism to a deployment-ready
  Story 012 model path only after a role-specific bench of at least ten correction
  pairs reaches the declared thresholds without policy relaxation. The pinned
  Qwen2.5-Coder 7B run on 2026-08-01 produced 10/10 typed requests but only 1/10
  domain-ready solver successors in the staged zone-declaration case, below the
  `0.6` ready-rate threshold. This measured model-capability gap does not reopen the
  completed baseline Story 012 acceptance.
- [ ] Derive budgets from the append-only run ledger. Fit at least four complete
  feedback cycles inside one authority epoch or renew authority between cycles without
  widening an individual grant or holding a P083 lease during inference. The
  matrix yields a provisional model-only envelope of 720,000 ms and 24,576 tokens
  after a 25 percent margin. The retained full-system run adds four model turns,
  16,577 total tokens, 516,110 ms of model time, 544,637 ms of deliberation, and a
  164,161 ms maximum turn. Keep this task open for explicit between-cycle authority
  renewal: four cycles at the measured effect-feedback cost do not fit safely under
  one canonical Room authority ceiling.
- [ ] Require deterministic replay before vfkit and retain repeatable seeded E2E
  evidence with prompt-free per-role latency, token, cycle, rejection, experiment,
  and correction measurements. One closed 30-check deployment run now passes;
  another fresh seeded success is still required before claiming repeatability.
- [x] Add the resolved guest-attested
  `powerdns-bind-missing-zone-data.v1` prepared-system challenge: valid loopback
  listener, BIND backend, and authoritative declaration referencing an absent
  zone-data file, without final `localdomain` records. Select `challenge/id` and
  verifier contract ref/digest from pinned guest/image evidence rather than a
  runner literal. The exact prepared-system source, manifest, image completion
  record, and retained deployment report now bind the selected second variant.
- [x] Retain a passing `story-012-powerdns-discovery-full-system-report.v1` from a
  real vfkit, `llama-server`, and pinned local-model run that reaches the exact DNS
  goal through model-authored trial and error without a solution fixture. Do not
  promote a report until the staged bench demonstrates a plausible correction
  path and the closed validator accepts the exact deployment bytes. The retained
  2026-08-01 Qwen2.5-Coder 7B run passes 30 checks after one nonpassing and one
  successful admitted experiment, with fresh terminal feedback, HIL, P083 lease
  release, reported host structural framing, and zero direct Room-prose effects.
