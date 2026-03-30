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
3. Instead of returning a normal final decision, it returns an interaction request.
4. The node persists:
   - the interaction request,
   - the suspended execution context,
   - and a causality link to the originating message or invoke.
5. The node emits a local notification so GUI clients can learn that pending interaction work exists.
6. A GUI client either receives that notification live or later fetches queued pending interactions.
7. The user answers.
8. The GUI sends the answer back to the node.
9. The node persists the response and resumes the suspended middleware context through an explicit resume message.
10. The middleware continues from that resume point and returns a normal outcome.

## Why this shape

This keeps the layers clean:

- GUI remains a local client of the node control plane,
- middleware remains a local extension of node behavior,
- the node remains the causal and durable coordinator.

This also avoids turning "waiting for user input" into a global stall in the middleware host or daemon loop.

## Contract intuition

The semantic core probably needs three local contract objects:

- `interaction_request`
- `interaction_response`
- `interaction_suspension`

The request should describe:

- prompt kind,
- presentation hints,
- allowed response shape,
- origin references,
- and expiry or timeout policy when needed.

The response should describe:

- the answered `interaction/id`,
- user-selected or user-authored payload,
- responder identity or local client context when relevant,
- and response timestamp.

The suspension record should describe:

- which middleware or attached role is waiting,
- how the node resumes it,
- and which originating invoke or message caused the wait.

## Important semantic boundary

This should probably not overload an existing generic `defer` meaning.

`defer` is usually too weak semantically. It can mean "host fallback" or "not decided here", while this case is more specific:

- a human-facing interaction was requested,
- a local execution context was suspended,
- and a later resume is expected.

That suggests one explicit suspend-or-await-user contract rather than one ambiguous reuse of generic deferral.

## Resume semantics

The resume path should not blindly replay the original middleware invoke as if nothing happened.

That would risk duplicated side effects or accidental re-interpretation of the call as a fresh event.

The safer shape is one explicit resume message carrying at least:

- `interaction/id`,
- `origin/message_ref` or equivalent causality reference,
- optional original input snapshot,
- user response payload,
- and resume timestamp.

The node may still include the original triggering payload for context, but it should be carried as context for resume, not as a silent retry.

## Delivery intuition

The node can support two complementary local client patterns:

- push notification through a local event stream,
- pull of queued pending interaction requests through a local control API.

That combination tolerates GUI disconnects while still supporting live operator experience.

## Actionable next step

When this matures, promote it to a proposal and freeze at least:

- one local interaction object model,
- one suspend/resume sequence,
- one local control-plane surface for pending requests and responses,
- and one failure policy for timeout, cancellation, abandonment, and duplicate response submission.

Promote to: proposal when the interaction object model, control-plane surface, and resume semantics are stable enough to freeze as one Node-side local contract.
