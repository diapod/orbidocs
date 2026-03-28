# Question Envelope and Answer-Channel Transport for Orbiplex Swarm

Based on:
- `doc/project/20-memos/swarm-broadcast-assistance.md`
- `doc/project/20-memos/swarm-question-channel-transports.md`
- `doc/project/20-memos/model-requests.md`

## Status

Proposed (Draft)

## Date

2026-03-17

## Executive Summary

This proposal separates two concerns that should not be forced onto one transport:

1. durable publication and discovery of signed question envelopes,
2. live many-participant discussion on the answer channel identified by the question id.

The recommended baseline is a hybrid model:

- `NATS / JetStream` for signed question envelopes, summaries, closure events, replay, and machine-readable dissemination,
- `Matrix` for live answer-channel conversation among dozens or hundreds of participants,
- optional IRC-style bridges for lightweight observer or operator access where needed.

## Context and Problem Statement

Orbiplex needs a swarm-native way for one node to ask the wider federation or global
swarm for help with a question that may require many responders and iterative
discussion.

The mechanism must support:

- signed, replayable question publication,
- scoped dissemination (`federation-local`, `cross-federation`, `global`),
- responder filtering (models, reputation, tags, language, other policy constraints),
- TTL semantics,
- shared answer channels for many participants,
- redundant server infrastructure,
- graceful handling of partial absence of the asking node.

The project also wants the communication shape to remain IRC-like where useful:
question id opens a room-like channel, many nodes join, discuss, and converge.

## Options Considered

### Option A: One room/chat protocol for both envelopes and discussion

Use `Matrix`, `IRC`, or `XMPP MUC` as both the publication bus and the live answer
channel.

- Pros:
  - Simple conceptual model.
  - Fewer moving parts.
  - Fast prototype path.
- Cons:
  - Weak fit for durable replayable protocol envelopes and machine-readable event flow.
  - Harder to express delivery guarantees, structured fan-out, and retention policy as protocol primitives.
  - Pushes envelope semantics into room messages instead of a transport that understands event persistence.

### Option B: Event bus only

Use `NATS / JetStream` or another durable event bus for both envelopes and the full
multi-party discussion.

- Pros:
  - Strong replay, clustering, and dissemination model.
  - Clean event architecture.
  - Strong machine-node integration.
- Cons:
  - Weak human conversation ergonomics by default.
  - Presence, room semantics, moderation, and large-group discussion UX must be built from scratch.
  - Poor fit for ad-hoc operator participation compared to room/chat systems.

### Option C: Split architecture with event bus plus room protocol

Publish envelopes and lifecycle events on a durable event bus, but run the live
question discussion in a federated room transport.

- Pros:
  - Best fit for both machine-readable protocol flow and large-group conversation.
  - Redundant servers on both layers.
  - Clear separation between durable state and live discussion.
  - Easier later substitution of either layer.
- Cons:
  - More operational complexity than a single transport.
  - Need channel binding rules between the two layers.
  - Need bridge logic for summaries, closure, and late joiners.

## Decision

Adopt **Option C (Split Architecture)** as the baseline.

The system should treat question publication and answer-channel discussion as distinct
but linked layers:

1. `NATS / JetStream` is the default protocol substrate for question envelopes and
   durable lifecycle events.
2. `Matrix` is the default protocol substrate for live answer-channel discussion.
3. The answer channel id MUST equal the published question id unless a federation
   profile explicitly wraps it in another namespace.
4. The asking node chooses channel scope (`federation-local`, `cross-federation`,
   `global`) and whether live follow-up discussion is allowed.
5. IRC-like access MAY exist through bridges, but IRC is not the normative baseline for
   durable protocol events.

For authored identity at the envelope layer:

- routing remains node-scoped through `sender/node-id`,
- the ordinary authored path may remain `sender/participant-id`,
- but some question publications may instead use an application-layer pseudonymous
  authored path through `author/nym`, attached `nym-certificate`, and `nym`
  signature.

This pseudonymous path remains above the transport boundary and does not change
the node-scoped session model.

## Proposed Model

### 1. Layer split

#### Envelope/event layer

Purpose:
- publish signed questions,
- discover active questions,
- replay late-joining state,
- persist summaries and closure outcomes.

Required properties:
- append-only event retention,
- clustering / redundant servers,
- filtered subscription,
- explicit TTL-aware consumers,
- machine-readable events.

#### Conversation layer

Purpose:
- allow many nodes to collaborate on the question in real time,
- carry partial answers, clarifications, objections, and synthesis attempts,
- support operator presence and delegation.

Required properties:
- room/channel model,
- many participants,
- replicated servers,
- presence and history,
- moderation / access control hooks.

### 2. Minimal event contracts

#### `swarm/question`

Published once to announce the question and open the answer channel.

```json
{
  "type": "swarm/question",
  "id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "sender": {
    "node/id": "node:pl-wro-7f3c",
    "federation/id": "fed:orbiplex-pl",
    "pubkey": "ed25519:9f2e5b5c4d..."
  },
  "created-at": "2026-03-17T18:42:11Z",
  "ttl-sec": 1800,
  "question": {
    "text": "What is the safest way to rotate a federation-wide trust root without breaking older nodes?",
    "tags": ["trust", "rotation", "backward-compatibility", "federation"],
    "urgency": "normal"
  },
  "delivery": {
    "scope": "federation-local",
    "response-channel/id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
    "response-channel/mode": "federation",
    "follow-ups?": true
  },
  "filters": {
    "models/require": ["model:claude-sonnet-4.5", "model:gpt-5"],
    "models/exclude": ["model:legacy-router-v1"],
    "responder/min-reputation": 0.78,
    "languages": ["en", "pl"]
  },
  "reward": {
    "kind": "tbd",
    "amount": null
  },
  "signature": {
    "alg": "ed25519",
    "value": "base64url:MEYCIQDf..."
  }
}
```

#### `swarm/question-summary`

Published one or more times as the live channel converges.

```json
{
  "type": "swarm/question-summary",
  "question/id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "summary/id": "summary:01JNY7C6D57CVS4CC0W4A3W6XQ",
  "created-at": "2026-03-17T18:58:02Z",
  "author": {
    "node/id": "node:pl-wro-secretary-2",
    "role": "secretary"
  },
  "status": "intermediate",
  "content": {
    "facts": ["Older nodes pin the previous root.", "A two-root overlap window is possible."],
    "hypotheses": ["A staged trust set may avoid partition."],
    "recommendations": ["Keep both roots active for one epoch before final removal."],
    "uncertainty": 0.23
  },
  "signature": {
    "alg": "ed25519",
    "value": "base64url:MGQCM..."
  }
}
```

#### `swarm/question-close`

Published when the asking node, or an authorized secretary under defined policy,
declares the question closed, expired, or handed off.

```json
{
  "type": "swarm/question-close",
  "question/id": "question:01JNY6M2X6Y8M1G5R4Z3K7Q2P9",
  "created-at": "2026-03-17T19:11:40Z",
  "closed-by": {
    "node/id": "node:pl-wro-7f3c",
    "role": "asker"
  },
  "resolution": "accepted-answer",
  "accepted-summary/id": "summary:01JNY7C6D57CVS4CC0W4A3W6XQ",
  "signature": {
    "alg": "ed25519",
    "value": "base64url:MEUCIF..."
  }
}
```

### 3. Conversation-layer contract

The `response-channel/id` declared in `swarm/question` opens a room on the conversation
layer.

Rules:

1. The asking node SHOULD remain present on the room, because it owns clarification and
   acceptance responsibility.
2. Another node MAY act as `secretary`:
   - when the asking node is absent,
   - when the asking node explicitly delegates,
   - or as backup while the asking node remains present.
3. Room scope MUST match the declared `delivery.scope`.
4. Room history SHOULD be retained long enough to support summary writing and post-hoc
   audit, but the durable source of truth remains the event layer summaries and closure
   events.
5. The conversation layer MAY contain many noisy or speculative messages; only signed
   event-layer summaries and closures count as durable protocol outputs.

### 4. Transport bindings

#### Event layer binding

Recommended baseline:
- `NATS / JetStream`

Reason:
- clustering and redundant servers,
- replay,
- filtered subscriptions,
- simple machine-node integration.

Suggested subject families:
- `swarm.question.publish.<scope>`
- `swarm.question.summary.<scope>`
- `swarm.question.close.<scope>`

This naming is illustrative, not yet normative.

#### Conversation layer binding

Recommended baseline:
- `Matrix`

Reason:
- federated rooms,
- replicated history,
- many-participant conversation,
- mature clients and bridges,
- good enough semantics for live room collaboration.

Suggested room mapping:
- room alias or room id derived from `question/id`,
- federation profile decides whether room creation is local-only, federated, or global.

### 5. Role semantics

#### Asking node

- publishes the signed question,
- chooses scope and filters,
- stays present if possible,
- accepts, rejects, or ignores answers until TTL expiry,
- normally closes the question.

#### Secretary node

- maintains continuity when the asking node is absent or unstable,
- publishes summaries,
- may close only under separately defined delegated or timeout rules.

#### Participant nodes

- join the answer room if filters and local policy allow,
- contribute analyses, follow-up questions, and synthesis,
- may publish candidate summaries if policy permits.

## Consequences

### Short-term

1. Need transport adapters for at least one event bus and one room protocol.
2. Need canonical signing rules for `swarm/question`, `swarm/question-summary`, and
   `swarm/question-close`.
3. Need secretary role policy and timeout semantics.
4. Need federation policy for room creation, retention, and bridge exposure.

### Long-term

1. Cleaner separation between durable swarm memory and live discussion.
2. Easier scaling to hundreds of participants without turning the event substrate into a
   chat protocol.
3. Better resilience: loss of one server should not destroy question visibility or room
   continuity.
4. Stronger room to evolve one layer without replacing the other.

## Implementation Notes

1. Start with one `JetStream` subject family and one `Matrix` room namespace.
2. Keep `question/id == response-channel/id` in the first implementation.
3. Treat IRC bridging as optional observer/access compatibility, not as normative state.
4. Add explicit limits for:
   - room size,
   - history retention,
   - summary publication frequency,
   - secretary takeover timing,
   - TTL expiry behavior.
5. Define whether model filters use model ids, hashes, or both; current baseline permits
   ids, while `model-requests.md` still argues for checksums where available.
