# Inquirium Assistant Channel

Based on:

- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/60-solutions/044-inquirium/044-inquirium.md`
- `doc/project/60-solutions/018-classification/018-classification.md`
- `doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`
- `doc/project/60-solutions/039-notifications/039-notifications.md`
- `doc/normative/50-constitutional-ops/en/UNIVERSAL-BASIC-COMPUTE.en.md`

Related schemas:

- `inquirium.assistant.turn.request.v1`
- `inquirium.assistant.turn.response.v1`
- `inquirium.assistant.transcript.fact.v1`
- `inquirium.assistant.transcript.bundle.v1`
- `inquirium.context-assembly.request.v1`
- `inquirium.context-grant.issue.request.v1`
- `inquirium.context-grant.revoke.request.v1`
- `inquirium.operator-question.request.v1`
- `inquirium.operator-question.transition.request.v1`
- `inquirium.inquiry-feedback.v1`
- `inquirium.training-grant.issue.request.v1`
- `inquirium.training-grant.revoke.request.v1`
- `inquirium.crisis-candidate.v1`

## Status

Implemented MVP solution.

The advise-first Assistant Channel, local baseline profile, classified context
grants, transcript lifecycle, operator questions, notification projection,
feedback, training grants, observability feed, and non-dopamine UI affordance are
implemented. Agentic effects remain a separately governed Agent integration.

## Date

2026-07-13

## Executive Summary

The Inquirium Assistant Channel is the human-facing interaction surface for
local model inquiry. It may look conversation-like in Node UI, but it is not a
contact, nym, messaging peer, or INAC route.

```text
operator or participant
  -> Assistant Channel turn
  -> Inquirium bounded inquiry
  -> classified response and transcript facts
```

The channel is advise-first and operator-initiated. It cannot mutate
relationships, publish to the swarm, or execute tools. Context requires explicit
host grants, response provenance remains visible, and any blocking operator
question uses registered notification widgets rather than model-defined UI.

## Context and Problem Statement

A conversational assistant can easily be mistaken for a relationship actor.
That would introduce fake identities, special Messaging routes, and confusing
retention semantics. The assistant is instead a projection over a local
Inquirium capability and its participant-scoped inquiry history.

This separation preserves the meaning of contacts and messages while still
allowing a rich interaction surface. It also keeps local baseline assistance
available without making remote inference a precondition or silently exporting
protected context.

## Proposed Model / Decision

### Channel, Not Counterparty

The Assistant Channel belongs to the Node interaction surface. Local
Relationship and Messaging remain uninvolved. A UI may render it beside
conversation-like surfaces, but it must not mint a peer identity, contact
record, delivery route, or relationship state.

### Advise First, Effects Elsewhere

Assistant responses carry content, epistemic posture, and admitted inert control
proposals. The channel may project a host-owned operator question or crisis
candidate, but it cannot declare a crisis, answer its own question, or execute a
proposed effect. Durable agentic control belongs to the Agent organ and the
relevant Sensorium or Artifact Delivery authority boundary.

### Local Baseline, Explicit Remote Extension

A conforming `profile/baseline-assistant` local runtime is a non-withdrawable
minimum. Remote candidates are additive and require explicit model acceptance,
classification-compatible egress policy, and acknowledgement of the concrete
context release. They are never a silent fallback for the local baseline.

## Must Implement

### Assistant Turn Boundary

Responsibilities:

- expose typed, bounded, idempotent assistant turns through Inquirium;
- bind principal and participant scope from authenticated host context rather
  than trusting request-body identity;
- preserve valid caller turn ids and assign host ids when missing;
- cap completed output before transcript persistence;
- keep response epistemic posture visible and non-authoritative.

Status: `done`.

### Baseline Runtime And Conformance

Responsibilities:

- require a local-only, strict-local, offline-capable baseline runtime profile;
- gate routing on a fresh profile- and host-class-scoped conformance report;
- expose readiness and remediation paths to the operator;
- keep remote inference additive rather than a prerequisite for assistance.

Status: `done`.

### Transcript And Session Projection

Responsibilities:

- store inquiry turns and results as participant-scoped facts through a
  Memarium-first transcript port with a local non-federating fallback;
- keep large content behind object-store refs and redact before persistence;
- preserve idempotent replay without duplicating transcript facts;
- support search, tags, rebuild, export/import, retention, and audit-preserving
  excision markers;
- project bounded working memory while assigning summary production to another
  configured component or workflow.

Status: `done`.

### Granted Context And Classification

Responsibilities:

- require durable participant/session/source-bound grants for Relationship,
  Memarium, query, Messaging, artifact, and dataset context;
- carry classification and provenance for every accepted context element;
- fail closed when a source cannot be resolved or policy requires rejection;
- archive terminal grants before pruning active authority;
- require explicit acceptance and egress acknowledgement for remote protected
  context.

Status: `done`.

### Operator Questions And Escalation

Responsibilities:

- create questions from host-owned registered widget kinds only;
- persist pending, answered, timed-out, cancelled, and superseded transitions;
- validate answers server-side and reject late or conflicting transitions;
- project questions into durable Notifications without storing arbitrary model
  UI payloads;
- treat crisis output as a classified candidate for host review, never as a
  self-authorizing diagnosis.

Status: `done`.

### Feedback And Training Admission

Responsibilities:

- record verified, refuted, and amended feedback as append-only classified
  facts;
- require a separate live participant- and feedback-bound training grant before
  feedback becomes a training candidate;
- keep dataset construction and model adaptation behind Inquirium's bounded
  manifest, lease, deferred-operation, evaluation, and publication gates.

Status: `done`.

### Observability And UI

Responsibilities:

- provide a local read-only activity feed over metadata-only assistant traces;
- retain one-way trace refs without prompt or response content in trace storage;
- render the assistant as an explicit inquiry affordance, not as a contact;
- avoid streaks, nudges, leaderboards, attention scores, or autonomous
  engagement loops.

Status: `done`.

## May Implement

### Agentic Effect Integration

An operator may explicitly bind the Assistant Channel to a bounded Agent. The
Agent owns lifecycle, controller steps, grants, budgets, and effect proposals.
Relationship, governance, publication, and external actuation still require the
owning capability gate and human-in-loop policy.

Status: `deferred`; tracked by Proposal 073.

## Trade-offs

The channel is less socially seamless than pretending the assistant is another
contact, and explicit grants add interaction steps. In return, identity,
retention, egress, and effect authority remain truthful. The local baseline may
be weaker than remote models, but it preserves a minimum assistance capability
without dependency on a provider or network path.

## Failure Modes And Mitigations

- **Assistant is treated as a contact:** keep all relationship and Messaging
  mutations outside the channel contract.
- **Caller spoofs participant scope:** derive scope from authenticated host
  identity.
- **Remote model receives undeclared context:** require source grants,
  classification admission, model acceptance, and egress acknowledgement.
- **Model injects an operator widget:** accept only registered host-shaped
  question kinds and validate answers server-side.
- **Transcript persistence fails:** preserve typed degraded behavior and the
  local fallback without publishing transcript data to the swarm.
- **Repeated or late interaction mutates state twice:** use idempotency,
  terminal transition facts, expiry checks, and conflict rejection.
- **Assistant claims authority or crisis certainty:** constrain epistemic posture
  and route only a metadata-safe candidate to host-owned review.

## Open Questions

No unresolved question blocks the implemented MVP solution. Agentic effects are
not an open Assistant Channel decision; they are a deferred integration with the
Agent organ and the relevant effect-owning components.

## Next Actions

1. Preserve the local baseline and no-contact invariants as UI surfaces evolve.
2. Productize local runtime installation and diagnosis for distributors and
   operators.
3. Add Agent integration only after Proposal 073 supplies durable lifecycle,
   effect admission, and human-in-loop outcomes.

## Out Of Scope

- representing the assistant as a contact, nym, peer, or Messaging route;
- autonomous initiation or engagement optimization;
- direct relationship, governance, publication, filesystem, or network effects;
- using transcript or trace storage as a covert swarm publication path;
- letting a model define executable widgets, grants, or effect authority.

## Consumes

- authenticated participant/operator context;
- `inquirium.assistant.turn.request.v1`;
- classified context grants and source projections;
- baseline and selected runtime conformance state;
- notification and transcript storage ports.

## Produces

- `inquirium.assistant.turn.response.v1`;
- participant-scoped transcript facts and bundles;
- metadata-only activity and trace projections;
- registered operator questions and notification actions;
- classified feedback, crisis candidates, and training-candidate admissions.

## Related Capability Data

- `045-inquirium-assistant-channel-caps.edn`

## Implementation Recommendations

The shared implementation invariants and extension rules remain in
`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`.
Those recommendations serve both Inquirium and this channel without defining a
third component.
