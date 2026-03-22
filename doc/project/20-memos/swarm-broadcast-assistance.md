# Swarm Broadcast Assistance

A node user may open a communication window to the swarm as a whole and broadcast an issue that matters to them, such as a personal problem, a technical blockage, a safety concern, or a request for orientation.

The swarm should treat such a broadcast as a shared assistance request rather than a point-to-point message. It may gather relevant memory, route sub-questions to capable nodes, request clarification, and converge on a helpful response or action plan.

The user should be able to control scope and intensity, for example whether the issue is private, federation-local, or wider; whether follow-up questions are allowed; and how urgent the matter is.

The response does not have to come from one node. It may be synthesized from many partial contributions, with traceable sources, explicit uncertainty, and a clear distinction between facts, hypotheses, and recommendations.

This mode should support both direct problem solving and reflective guidance. In some cases the swarm may help by answering; in others by decomposing the issue, finding the right humans or agents, and maintaining continuity until the matter is resolved or safely handed off.

## Example question envelope

A node that wants swarm help may publish a signed question envelope onto a federation
question bus. The envelope should carry a stable identifier, enough routing metadata to
filter responders, and a TTL after which the asking node no longer promises to accept
late answers.

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

## Response channel semantics

The published question opens a response channel with the same identifier as the
question itself. Nodes that choose to participate join that channel and discuss the
issue, compare hypotheses, and converge on candidate answers.

The asking node should remain present on that channel, because it is responsible for
tracking answers, clarifying intent, and deciding whether the result is sufficient. If
the asking node is absent or unstable, another node may act as secretary; it may also
shadow the asking node as a communication backup even when the asker remains present.

Channel scope should be chosen by the asking node: federation-local, cross-federation,
or global. Dissemination likely needs multiple mechanisms with different reach and cost
profiles. Transport is still an open question, but the problem shape is IRC-like:
shared channels, many participants, partial presence, and synchronized server sets.

Promote to: story, proposal, or requirements document when shared assistance routing and user-facing interaction modes are designed.
