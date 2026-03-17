# Operator Participation in Answer-Channel Debate

A node that participates in a question debate may notify its operator that a live discussion is underway and that human input could materially improve the outcome.

This is narrower than generic human expertise escalation. The point is not only to ask a human specialist for an answer, but to let a node pull human judgment into an already active multi-node debate around a specific question.

Two participation modes seem useful:

## 1. Mediated operator dialogue

The node opens a private dialogue with its operator, asks follow-up questions, receives raw human input, and then publishes a condensed contribution back into the answer channel.

In this mode the channel does not receive the human's raw text. It receives a node-authored summary, interpretation, or synthesis, ideally with a courtesy marker that the contribution is based on live operator consultation.

This mode is useful when:

- the operator wants privacy or low-friction participation,
- raw human phrasing would expose unnecessary personal details,
- the node needs to structure, redact, translate, or normalize input before publication,
- the operator is helping intermittently rather than joining the whole debate.

The cost is obvious: the swarm sees only a mediated condensate, so provenance is weaker than in direct participation and the quality of the node's relay matters.

## 2. Direct live human participation

The node may also let the operator join the ongoing debate more directly. In that case the node acts as a gateway, but messages sent by the human should be flagged, as a matter of protocol courtesy, as human-originated.

The operator still speaks through the node's communication path, yet the debate can distinguish:

- node-generated messages,
- node-condensed human input,
- direct human live messages.

This mode is useful when:

- nuance matters and summarization would lose too much signal,
- the debate is moving quickly and the operator wants to answer interactively,
- the operator wants other participants to challenge or refine their statements in real time.

The protocol should make the human-origin flag explicit rather than merely conventional, even if the identity remains pseudonymous or scoped to a federation.

## Common constraints

Both modes should remain opt-in, bounded, and visible at the provenance layer.

Useful controls include:

- operator notification preferences and quiet hours,
- topic, urgency, and trust thresholds before a node interrupts its operator,
- a visible distinction between node reasoning and human-originated input,
- rate limits, so a node does not become an unbounded human support tunnel,
- secretary support, so human-linked input is not lost if the original node drops,
- transcript and curation rules that preserve dignity, consent, and redaction boundaries.

This creates a practical human-in-the-loop gradient:

- fully autonomous node participation,
- node-mediated operator consultation,
- direct flagged human participation.

That gradient is valuable because different questions need different depths of human presence. Some cases benefit from quiet consultation and condensation; others benefit from letting a human voice enter the room without pretending it is just another model output.

Promote to: proposal or requirements document when operator-presence flags, transcript semantics, notification policy, and room-level permissions are specified.
