# Story 012: Remote Agents Solve a Problem Through a Shared Chair Terminal

Status: Profile defined; execution blocked by substrate gates

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
- Interaction Broker admits the received view as an Agent observation source.

The profile is intentionally not executable yet. It must remain fail-closed until
the host can bind an admitted Room-delivered Sensorium Interface frame to one
specific Agent passage without turning Room membership into interface authority
or persisting terminal content as Agent memory by accident.

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
transcript. Room carries a cursor-free, coalesced `latest-state` projection. The
source cursor, PTY handle, source credentials, and Workbench lease remain local
to node A.

## Flow

1. Node A creates the Corpus query and opens a bounded Room under the same policy
   and invite model used by Story 011.
2. Nodes B and C accept signed Room invitations and create narrowed
   `corpus-participant` Agent bindings. Node A creates the corresponding chair
   binding.
3. Node A creates an isolated Workbench terminal session under an allowlisted
   story workspace and starts the deterministic failing fixture.
4. Node A publishes only the visible terminal-screen representation as a
   `latest-state` Sensorium Interface. Ordered terminal-event replay is refused.
5. The host issues exact, expiring `subscribe` grants for that interface to the
   admitted B and C participant subjects. Room membership by itself does not
   satisfy this step. The first profile does not add an independent one-shot
   `read` grant.
6. The active Room relay projects the view only to recipients in the intersection
   of current Room observation rights and current Sensorium Interface grantees.
7. Each recipient host validates the interface frame, room, relay epoch,
   participant, Agent binding, classification ceiling, byte cap, and freshness
   before producing an ephemeral Agent observation input.
8. The Agent controller uses the accepted latest state in one bounded passage.
   The durable step trace contains only schema, refs, classification, policy
   digest, and content digest; it contains no terminal bytes or prompt text.
9. B and C publish inert Corpus reasoning turns through the existing
   `corpus.room.turn` effect and human-in-loop policy. They do not invoke the
   terminal.
10. The chair Agent proposes a bounded next action. In the first profile, only
    local control on node A may enact terminal input, command execution, resize,
    signal, patch, or file mutation through Workbench.
11. After the local operator applies the accepted change and reruns the fixture,
    the latest-state projection shows the passing result to all still-authorized
    participants.
12. Corpus accepts the chair's `agent.outcome.v1` as an inert answer draft.
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

Before this profile may run, the host must provide one explicit admission path
from a received Sensorium Interface frame to an Agent controller passage. That
path must:

- bind the frame to the exact interface, Room, relay epoch, recipient subject,
  Agent, and Agent binding;
- recheck both Room and interface authority at admission time;
- admit only the declared terminal-screen snapshot schema and `latest-state`
  delivery profile;
- enforce classification, age, item-count, and byte ceilings before prompt
  assembly;
- coalesce superseded snapshots rather than replay terminal history;
- expose the accepted observation as inert context, never as an effect request;
- record only prompt-free metadata and a host-keyed content digest in durable
  Agent trace; and
- discard terminal bytes after the bounded passage unless local control performs
  a separate classified Workbench capture.

Responsibility for summarizing terminal content belongs to a separately
authorized component. The Agent context bridge may select and bound an existing
snapshot, but it must not silently become a transcript store or summarizer.

## Substrate Gates

| Gate | Current state | Required evidence before execution |
|---|---|---|
| Story 011 Corpus/Agent deliberation | available | selected participant and chair Agents deliberate over Room with restart-safe bindings and inert final draft |
| Room Phase 6A relay | available | three-node member-visible WSS relay carries bounded Room and Sensorium Interface payloads with epoch fencing |
| Workbench terminal source | available | isolated PTY, bounded visible-screen snapshot, local actuation authority, and classified explicit capture |
| Sensorium Interface Room projection | available | exact grants, `latest-state`, recipient intersection, revocation, restart recovery, and no terminal control |
| Agent observation admission | **missing** | one host-owned, dual-authority, classification-aware frame-to-passage adapter with prompt-free trace |
| Story 012 process runner | **missing** | a composed three-node runner extending the Story 011 topology without copying its trust/bootstrap logic |

The acceptance pack must refuse execution while any gate is missing. Marking a
documentation row complete is not sufficient evidence; the runner must probe the
corresponding runtime surface or execute its refusal vector.

## Acceptance Profile

The planned operator-facing pack lives in:

```text
node/tools/acceptance/story-012-shared-chair-terminal/
```

Its checked-in profile plan is non-executable. It records topology, authority,
delivery mode, missing gates, and required assertions. A future runner should
reuse Story 011's profile rendering and federation-root bootstrap as a lower
stratum, then add only the Workbench, Sensorium Interface, Agent-observation, and
story-specific fixture layers.

The eventual process smoke must prove:

- three distinct daemon identities and node-local Agents;
- signed Room invite and membership admission for B and C;
- no terminal view before the exact interface grant exists;
- no view from Room membership alone or from an interface grant alone;
- cursor-free bounded latest-state delivery over the active Room relay epoch;
- exact frame-to-Agent binding and classification checks;
- B and C can deliberate from the shared view but cannot invoke or manage it;
- revocation stops one observer while the Room and other observer remain active;
- restart restores durable Agent, Room, interface, and grant projections, while
  stale relay or subscription state fails closed and refreshes from current
  latest state;
- terminal bytes do not enter Room messages, Memarium Agent facts, status,
  notifications, or prompt-free traces;
- the passing result is observed after local chair-side actuation; and
- the chair outcome remains an unpublished Corpus answer draft.

## Failure Modes and Mitigations

| Failure mode | Risk | Mitigation |
|---|---|---|
| Room membership is treated as terminal authority | unauthorized observation | require the exact current interface grant independently on every delivery and Agent admission |
| Remote Agent receives an actuation grant | participant controls the chair terminal | close the observer capability set to `read` and `subscribe`; refuse `invoke` and `manage` in profile validation |
| Old screen snapshots are replayed as a transcript | stale or excessive context | use cursor-free coalesced `latest-state`; reject ordered-event interfaces |
| Terminal bytes enter durable Agent memory | credential or source leakage | retain only refs, classification, policy digest, and host-keyed content digest |
| Revocation closes the Room | collaboration state is lost with one view | close only the projection/subscription and preserve the durable Room |
| Restart silently widens authority | stale grants or relay epochs revive | rebuild from durable facts, recheck revocation, and require a fresh current-state delivery |
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

- The story document and non-executable acceptance profile agree on topology,
  authority, data lifetime, and refusal behavior.
- P069 and P073 track the missing Agent observation bridge and the eventual
  process smoke explicitly.
- The profile validator rejects terminal actuation grants, membership-as-authority,
  ordered-event delivery, durable terminal content, and premature execution.
- Every substrate gate has executable evidence and is marked available.
- Only then, a composed three-node smoke completes the concrete problem from
  failing test through shared observation, deliberation, local repair, passing
  test, and unpublished answer draft.
