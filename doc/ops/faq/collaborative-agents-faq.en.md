# Collaborative Agents FAQ

## Which components make up agent collaboration?

Corpus organizes the question, provider selection, bids, settlement, and answer. Room
maintains membership, policy, and the ephemeral deliberation channel. Agent runs a
bounded execution session under host authority, while Inquirium normalizes inference
operations against a concrete model runtime. Sensorium Interfaces can attach an
attested view of a live environment. None of these components replaces the others.

The operational sequence is described in the [Collaborative Agents
HOWTO](../howto/collaborative-agents-howto.en.md).

## How does Room differ from Corpus?

Room answers: "who may participate, under which policy, and through which current
carrier epoch?" Corpus answers: "which problem are we solving, who bid, who was
selected, which roles apply, and which answer was accepted?" Room is not an order or
answer ledger, and Corpus does not implement a separate live transport.

## How does Agent differ from Inquirium?

Agent has a node-local lifecycle, budget, binding, working memory, trace, and effect
proposals. Inquirium performs one semantic inference operation through a selected model
adapter. An adapter or model does not become an Agent; it owns no Corpus session, Room
membership, publication authority, or effect authority.

## Do agents deliberate through a structured protocol or natural language?

Both layers are necessary. Turn content can be bounded `text/plain`, while its envelope
is structured: it identifies the query, Room, participant, assignment, `turn/no`,
classification, digest, expiry, and idempotency key. Roles, instruction overlays,
evidence refs, the answer, and its signature are separate contracts. Natural language
carries the argument; the protocol carries authority, order, provenance, and bounds.

## Who manages deliberation?

The requester can appoint its own bounded Agent as chair delegate. The chair organizes
questions, assigns roles, proposes instructions, synthesizes turns, and creates an
answer draft. It cannot accept that draft as the domain answer or widen its own grants.
Corpus authority and local policy retain the final decision.

## Can the chair assign roles and prompts to participants?

It can propose roles and bounded instruction overlays, but a proposal remains inactive
until accepted by local policy or the participant. Overlay source text is not a direct
adapter prompt. The host deterministically renders the accepted instruction and adds it
through host prompt policy immediately before invoking Inquirium.

## Who publishes the final answer?

Agent produces only an inert, content-addressed outcome or answer draft. Corpus checks
the binding, Room evidence, selected bid, policy digest, content digest,
classification, and signature. A separate authorized transition publishes
`corpus-reasoning-answer.v1`. Model output is never equivalent to publication.

## Does Room membership grant access to a live feed?

No. A recipient must simultaneously hold current Room membership and an exact Sensorium
Interface grant. The projection revalidates both authority sets on emission. Revoking
either closes access, while the relay remains only a carrier.

## Does a read-only terminal let an agent execute commands?

No. `latest-state` can expose a bounded terminal viewport but grants no actuation
authority. In the Story-012 profile, only local control on node A mutates the
environment. Remote control requires a separate grant, current control lease,
generation fencing, and schema-gated P083 operations.

P083 is the
[Sensorium Interactive Interfaces proposal](../../project/40-proposals/083-sensorium-interactive-interfaces.md):
it defines the actuation half that complements the read/subscribe surface promoted
as [Solution 046](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).

## What is durable and what is ephemeral?

Query, bid, selection, policy, membership, assignment, overlay, Agent lifecycle, turn
digests, draft, and published-answer facts are durable. Live Room content and terminal
viewports are ephemeral by default and bounded by a buffer. Restart recovers authority
and cursors; it does not pretend to recover unpersisted content.

## Does collaboration work over a network?

Room has a relocatable WSS/TLS relay with epochs, failover, and membership attestation.
Participants can use outbound-only connections to one reachable endpoint for the active
epoch. Story-011 and Story-012, however, are multi-address single-host acceptance
profiles: they test real process and TCP/WSS boundaries, but not public reachability,
independent hosts, or NAT traversal.

## Does Room require Matrix or hole punching?

No. The baseline carrier is a WSS/TLS relay; STUN/ICE, UDP, and hole punching are not
liveness requirements. Matrix remains an optional bridge profile for future
integration, not a second Room semantic model. Direct peer can optimize control
latency, but gains no authority and is not required for deliberation.

## What happens when the relay fails?

A new signed `room-relay-endpoint.v1` establishes a new epoch. Ephemeral buffers are
not merged across epochs. Clients revalidate membership, authority, and the current
endpoint, then refresh from durable facts and current source views. Carrier failure
reduces liveness; it does not remove Room as a fact set.

## How does the requester stop work after receiving an answer?

The requester can mark a round `requester-satisfied`. This explicit domain transition
stops further work collection for that round. Completion must not be inferred from
channel silence or an arbitrary model decision.

## Which acceptance profiles best demonstrate the mechanism?

Story-011 verifies three nodes, provider discovery, bids, Room, Agent turns, chairing,
Inquirium, answer publication, and `requester-satisfied`. Story-012 extends that path
with a read-only Workbench terminal through Sensorium Interfaces, independent B/C
grants, revocation, restart, and a locally executed repair.
