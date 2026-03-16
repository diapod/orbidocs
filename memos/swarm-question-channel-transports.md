# Swarm Question Channel Transports

Question envelopes and answer-channel conversation likely should not be forced onto one
transport. The protocol shape naturally splits into two concerns:

- broadcast and discovery of the signed question envelope,
- many-participant conversation on the channel identified by the question id.

For the conversation layer, the strongest candidates are protocols that already know
how to run large rooms, survive partial outages, and replicate across multiple servers.

## Candidate classes

- `IRC / IRC-like server networks`
  - Strong fit for large shared channels and simple multi-server topology.
  - Good when low ceremony, lightweight clients, and ad-hoc channels matter.
  - Weak on structured metadata, durable history, signatures-as-first-class fields, and
    modern permission / moderation semantics.

- `Matrix rooms`
  - Strong fit for federated rooms, replicated history, many participants, and durable
    multi-server presence.
  - Better than IRC when the channel must carry structured events, recover after node
    reconnects, and preserve room state across time.
  - Heavier operationally; room state and federation behavior need careful limits if
    rooms become very large or highly active.

- `XMPP MUC`
  - Good fit for room chat with federation and mature messaging semantics.
  - Simpler and leaner than Matrix in some deployments.
  - Weaker ecosystem fit for swarm-style structured event modeling and less natural for
    append-only, signed protocol envelopes.

- `NATS / JetStream`
  - Excellent for broadcast, fan-out, replay, queues, and redundant server clusters.
  - Very good as the bus for question envelopes and machine-readable event streams.
  - Not a natural human/group conversation protocol by itself; room semantics, presence,
    moderation, and threaded discussion would need to be built above it.

- `libp2p pubsub / GossipSub`
  - Attractive for wide reach and reduced dependence on a fixed server operator.
  - Useful when public dissemination and resilience against single-host failure matter.
  - Harder for durable history, moderation, room membership semantics, and predictable
    large-group conversation UX.

## Working recommendation

If the goal is easy group conversation among dozens or hundreds of participants with
redundant servers, the default choice should be `Matrix` or an `IRC-like federated room
system`, not a raw message bus.

If the goal is protocol transport for the signed question object itself, `NATS /
JetStream` is a stronger primitive than chat protocols.

That suggests a split architecture:

- a signed question envelope is published on a durable event bus,
- the envelope declares a conversation channel id,
- the actual multi-party discussion happens in a room protocol optimized for group
  conversation,
- summaries and final outputs are written back onto the durable bus as signed events.

## Bias for first implementation

If the system wants the shortest path to something IRC-like but more structurally
capable, `Matrix` is the best starting point.

If the system wants the smallest operational surface and accepts weaker structured
semantics, `IRC` remains a valid prototype transport.

If the system wants the cleanest systems architecture, use a hybrid:

- `NATS / JetStream` for envelopes, replay, and machine-readable event propagation,
- `Matrix` for the live answer channel,
- optional bridges for IRC-style clients where lightweight access matters.

Promote to: proposal or requirements document when the project decides whether question
broadcast and answer-channel conversation are one protocol or two.
