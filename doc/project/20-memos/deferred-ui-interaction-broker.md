# Deferred UI Interaction Broker

This memo captures one likely missing local contract for Orbiplex Node: a node-attached middleware module or other attached role may need user interaction without blocking the whole node communication path.

The current intuition is that this should be modeled as a host-owned interaction broker rather than as direct `middleware <-> GUI` coupling.

Related notes:

- `orbidocs:doc/project/20-memos/pod-backed-thin-clients.md`
- `orbidocs:doc/project/20-memos/node-middleware-init-and-capability-reporting.md`

## Problem

Some local middleware flows are not purely automatic. A module may need to:

- display a message to the user,
- ask a yes/no or multiple-choice question,
- request free-form text input,
- or resume only after a human response exists.

The important constraint is that waiting for the human should not stall unrelated node activity.

If the local GUI or client is offline, the request should remain pending until a user-facing client reconnects and fetches queued interaction work.

## Proposed model

Treat this as one host-owned local interaction plane.

The main actors are:

- attached middleware or another node-attached role,
- local node daemon,
- local GUI, launcher, or thin client,
- human user.

The node should own:

- stable `interaction/id`,
- durable storage of pending requests,
- notification emission,
- response intake,
- and resume delivery back to the waiting module.

The middleware should not talk to GUI directly as its primary protocol path. It should talk to the node.

## Proposed flow

1. A middleware module receives one normal host call.
2. The module determines that human input is required.
3. The module calls one host capability such as `interaction.request`, passing a
   typed interaction request payload. The host capability returns an
   `interaction/id` immediately.
4. The module returns a `suspended` outcome referencing that `interaction/id`.
   The module does not block waiting for user input.
5. The node persists:
   - the interaction request,
   - the suspended execution context record,
   - and a causality link to the originating invoke or message.
6. The node emits a local notification so GUI clients can learn that pending
   interaction work exists.
7. A GUI client either receives that notification live or later fetches queued
   pending interactions.
8. The user answers.
9. The GUI sends the answer back to the node through a local control-plane
   endpoint.
10. The node persists the response and delivers an explicit resume message to
    the middleware — as a new POST to the module's resume endpoint, not as a
    replay of the original call.
11. The middleware continues from that resume point and returns a normal outcome.

Step 3 uses a host capability call rather than a special return type so that the
interaction contract stays symmetric with the rest of the middleware capability
surface. The `suspended` return in step 4 is a typed outcome, not an error.

## Why this shape

This keeps the layers clean:

- GUI remains a local client of the node control plane,
- middleware remains a local extension of node behavior,
- the node remains the causal and durable coordinator.

This also avoids turning "waiting for user input" into a global stall in the
middleware host or daemon loop.

The `suspended` outcome is execution-scoped on the node side. For
`http_local_json` middleware, "suspended" means the node does not advance the
execution to the next step until the interaction is resolved. The middleware
process itself does not block or hold a thread; it simply returns and is later
called again at the resume point.

## Contract intuition

The semantic core probably needs three local contract objects:

- `interaction_request`
- `interaction_response`
- `interaction_suspension`

### Interaction request

The request should describe:

- `interaction/id` — stable, host-assigned URN,
- `prompt/kind` — one of `confirm`, `choice`, `text_input`, `inform`,
- `prompt/text` — human-readable prompt,
- `prompt/choices` — ordered list of labeled options when `kind = choice`,
- `response/constraints` — allowed shape for the user answer,
- `origin/invoke_ref` — causality link to the triggering middleware invoke,
- `origin/execution_ref` — optional procurement or workflow execution reference,
- `expires_at` — optional hard deadline after which the node times out the
  interaction.

`prompt/kind` should be a closed enum at this layer. Free-form rendering hints
may be added as optional presentation metadata but must not be required for
correct behavior.

### Interaction response

The response should describe:

- `interaction/id` — the answered request,
- `payload` — user-selected or user-authored answer, validated against
  `response/constraints`,
- `responded_at` — timestamp,
- `responder_ref` — optional local client context.

On hard MVP, `responder_ref` may be omitted. Local control-plane access is
already gated by the operator authtok. Multi-user local identity is post-MVP.

### Interaction suspension record

The suspension record is a node-internal durable artifact. It should describe:

- `interaction/id`,
- `middleware_module_id` — which module requested the interaction,
- `resume_endpoint` — how the node delivers the resume message to the module,
- `origin/invoke_ref` — the originating call,
- `suspended_at` — timestamp.

This record is not a wire contract. It is a node-local persistence artifact used
to survive daemon restarts and to support reconciliation on open.

## Important semantic boundary

This should not overload an existing generic `defer` meaning.

`defer` is usually too weak semantically. It can mean "host fallback" or "not
decided here", while this case is more specific:

- a human-facing interaction was requested,
- a local execution context was suspended,
- and a later resume is expected.

That suggests one explicit suspend-or-await-user contract rather than one
ambiguous reuse of generic deferral.

## Resume semantics

The resume path should not blindly replay the original middleware invoke as if
nothing happened.

That would risk duplicated side effects or accidental re-interpretation of the
call as a fresh event.

The safer shape is one explicit resume message carrying at least:

- `interaction/id`,
- `origin/invoke_ref` — causality reference to the original call,
- `original_input` — optional snapshot of the original call payload, carried as
  context only, not re-executed,
- `user_response` — the resolved interaction response payload,
- `resumed_at` — timestamp.

The node delivers this as a new POST to the module's resume endpoint, distinct
from the original capability call path.

## Failure and edge cases

These must be frozen before this matures into a proposal.

### Timeout

When `expires_at` elapses and no response has been received, the node resumes
the middleware with a typed `timed_out` outcome rather than dropping the
interaction silently. The middleware decides how to proceed — cancel, use a
default, or escalate.

### Duplicate response

A second response submission for the same `interaction/id` should be treated as
idempotent if the payload matches, or rejected with a classified error if it
conflicts. The node must not apply two responses to one interaction.

### Cancellation

When the originating execution is cancelled, the node should void all pending
interactions associated with it and emit a `cancelled` resume to any waiting
module. This prevents suspended modules from holding stale references to
cancelled executions.

### Daemon restart

On daemon open, the node should replay the suspension record log and re-register
all pending interactions that were not yet resolved. Interactions without a
matching live execution record should be voided rather than silently dropped.

### Concurrent interactions per execution

Whether one execution may hold more than one pending interaction simultaneously
should be decided before implementation. The simplest hard-MVP policy is one
pending interaction per execution at a time, with a second request returning an
error until the first is resolved.

## Delivery

The node should support two complementary local client patterns:

- **push**: notification through a local event stream such as
  `GET /v1/interactions/events` (SSE or equivalent),
- **pull**: `GET /v1/interactions/pending` listing unresolved interaction
  requests with optional filters by module, execution, or kind.

Response submission goes through a dedicated write endpoint:
`POST /v1/interactions/{interaction_id}/respond`.

That combination tolerates GUI disconnects while still supporting a live
operator experience.

## Actionable next step

When this matures, promote it to a proposal and freeze at least:

- one local interaction object model with explicit `prompt/kind` enum,
- one suspend/resume sequence showing the exact capability call and resume POST
  shapes,
- one local control-plane surface for pending requests and responses,
- one failure policy covering timeout, cancellation, abandonment, duplicate
  response, and daemon-restart reconciliation,
- and the concurrent-interactions-per-execution cardinality rule.

Promote to: proposal when the interaction object model, control-plane surface,
and resume semantics are stable enough to freeze as one Node-side local contract.
