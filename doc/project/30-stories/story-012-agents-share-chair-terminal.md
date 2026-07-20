# Story 012: Remote Agents Solve a Problem Through a Shared Chair Terminal

Status: Implemented; composed three-node acceptance passes

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

The profile is executable. Its process runner reuses the extracted Story 011
three-node federation/bootstrap layer, then composes the Workbench, Sensorium
Interface, Room observation, Agent, and story fixture layers without creating a
second trust bootstrap or collaboration runtime.

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
| Story 012 process runner | available | a composed three-node runner extends the shared Story 011 topology without copying its trust/bootstrap logic |

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

## Failure Modes and Mitigations

| Failure mode | Risk | Mitigation |
|---|---|---|
| Room membership is treated as terminal authority | unauthorized observation | require the exact current interface grant independently on every delivery and Agent admission |
| Remote Agent receives an actuation grant | participant controls the chair terminal | close the observer capability set to `read` and `subscribe`; refuse `invoke` and `manage` in profile validation |
| Old screen snapshots are replayed as a transcript | stale or excessive context | use cursor-free coalesced `latest-state`; reject ordered-event interfaces |
| Terminal bytes enter durable Agent memory | credential or source leakage | retain only refs, classification, policy digest, and host-keyed content digest |
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
