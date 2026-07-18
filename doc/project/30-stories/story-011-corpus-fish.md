# Story 011: Corpus answers the fish-water question

Status: Hard-MVP blocker

## Summary

As a node operator, I want one node to ask a bounded biological question and two
other nodes to contribute through a bounded reasoning market and, in the
post-MVP profile, let selected model-backed participants deliberate through a
shared Room so the requester can stop the process once the answer is satisfactory.

The concrete question is:

> Do fish drink water?

Node A is the requester. Node B and node C are Corpus-capable providers. Node B
also hosts the Seed Directory and an offer-catalog profile with a biology
taxonomy. The story uses Corpus as the topic-routed reasoning layer over the
existing question, service-offer, procurement, and room primitives.

## Actors

- **Node A** asks the question, creates the Corpus query, aggregates bids, selects
  a provider, and may close the round as `requester-satisfied`. In the Agent
  profile it also runs the Room-attested chair Agent.
- **Node B** publishes a `corpus.provider` offer for the biology taxonomy, runs
  the Seed Directory role in the profile, and is selected as the expert. In the
  Agent profile it participates through a Room-attested participant Agent.
- **Node C** publishes a second `corpus.provider` offer for the same taxonomy and
  remains a competing bidder; selection does not ambiently enroll it in the
  A↔B deliberation.

## Flow

1. Node B exposes a remote offer catalog and Seed Directory profile.
2. Node B and node C publish `corpus.provider` offers with the same
   `corpus/taxonomy-digest` and `corpus/topics`.
3. Node A creates a `corpus-reasoning-query.v1` around a `question-envelope.v1`
   whose text is `Do fish drink water?`.
4. The query carries a Room collaboration reference; the acceptance pack uses
   the daemon-owned bounded WSS carrier and retains the Matrix room id only as
   future transport intent.
5. Node B and node C produce `corpus-reasoning-bid.v1` responses.
6. Node A builds a requester-owned bid-state read model and selects the cheapest
   valid accepted bid.
7. In the Agent profile, B's admitted participant Agent invokes Inquirium and
   proposes an inert, content-addressed reasoning turn through the explicit
   `corpus.room.turn` effect and human-in-loop gate.
8. A consumes the Room event through Interaction Broker, runs its admitted chair
   Agent, and accepts the terminal product as an unpublished Corpus answer draft.
9. Once the answer is satisfactory, node A can stop the round by marking it
   `requester-satisfied`; publication remains a separate Corpus-owned transition.

The intended answer distinguishes freshwater and saltwater fish: freshwater fish
gain water osmotically and mostly do not need to drink, while many marine fish
drink seawater and excrete salts.

## MVP Boundary

This story is part of the hard-MVP story set and blocks MVP readiness until the
local acceptance pack can complete the documented three-node Corpus
query/bid/select/close path. The MVP blocker is the bounded Corpus procurement
round itself; a real Matrix homeserver-backed live collaboration transport is a
post-MVP extension as long as the query and answer path preserve the Matrix room
id as protocol intent.

[Story 012](story-012-agents-share-chair-terminal.md) is the gated follow-on
profile that composes this Agent-deliberation topology with a chair-owned,
read-only Workbench terminal view. It is not part of Story 011 completion and
must remain non-executable until its Agent observation-admission gate exists.

## Acceptance Pack

The initial operator-facing pack lives in:

```text
node/tools/acceptance/story-011-corpus-fish/
```

It renders three local daemon profiles, imports Corpus-capable offers for B and
C, creates the A-side query, asks B and C for provider bids, registers those bids
on A, selects the cheapest valid bid, and verifies that A can stop the round as
`requester-satisfied`.

The managed smoke uses the same federation-root trust seam as runtime
consumers: after first boot it reads real node IDs, creates B/C provider
participants, rewrites the signed runtime `federation-root.v1` with Node B's
official Seed Directory endorsement and B/C participant attestation roots,
restarts all daemons, asserts Node A's active `/v1/seed-directory` trust view,
and only then issues/publishes provider capability passports.

The pack does not start a real Matrix homeserver. It exercises the bounded WSS
Room carrier. Its Agent-deliberation profile proves a selected B participant
Agent, an A chair Agent, a host-owned `room-event` Interaction Broker watch,
human-approved turn dispatch, metadata-only durable watch replay, restart-safe
Agent bindings, mismatched participant refusal, stale cursor refusal after
Room-source restart, exact accepted-draft replay after restart, and absence of
ambient answer publication. A homeserver-backed transport fixture can be layered
onto the same Room contract later.

## Done When

- The local three-node acceptance pack initializes all profiles with valid daemon
  configuration.
- The managed smoke starts A, B, and C and completes the Corpus query/bid/select
  path.
- The managed smoke refreshes the signed runtime federation root after first
  boot and proves that Node A sees Node B as an active `federation-endorsed`
  Seed Directory source before provider passport discovery.
- B is selected when it offers the lower valid price.
- A closes the round with `round/status = requester-satisfied`.
- The query and answer path preserve the Room and future Matrix transport intent,
  while the exercised carrier is stated explicitly.
- The Agent profile admits only signed, fresh, exact Room evidence; B's turn is
  inert until human-approved effect dispatch, and A observes it through the
  host-owned broker.
- B is the selected expert, C remains a competing bidder, and neither raw model
  adapters nor unselected providers gain Room authority.
- Restart recovers the A/B Agent bindings and completed chair outcome; stale Room
  cursors fail closed and exact effect replay does not duplicate publication.
- Agent output remains an inert draft until a separate Corpus-owned acceptance or
  publication transition.
