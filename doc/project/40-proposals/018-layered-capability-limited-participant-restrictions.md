# Proposal 018: Layered `capability_limited` Participant Restrictions

## Context

The current Node runtime already uses `capability_limited` as a peer-quality
state when a remote peer is missing required transport capabilities. That solves
one narrow networking problem, but it does not yet define how participant-level
sanctions should work above transport.

This leaves an architectural gap:

- soft degradation is underspecified,
- hard operation blocks are ad hoc,
- and the system lacks one auditable artifact binding sanctions to a concrete
  participant subject, author, and expiry.

The gap matters because Orbiplex explicitly rejects both extremes:

- a harmless soft downgrade that leaves every privileged operation effectively
  available,
- and an opaque binary kill switch that collapses all escalation into permanent
  exclusion.

## Goals

- freeze a participant-scoped artifact for layered restriction state,
- keep soft degradation separate from hard blocked operations,
- preserve a non-blockable minimum participation floor,
- define the first minimal Node enforcement hooks without overloading the
  transport governor,
- and keep the blocked-operation namespace open for later growth.

## Non-Goals

- This proposal does not redefine transport-layer capability advertisement.
- This proposal does not make `capability_limited` a permanent exclusion state.
- This proposal does not yet define a global sanction registry or federation-wide
  propagation rail.
- This proposal does not yet standardize graduated time-based soft degradation
  curves.

## Decision

Orbiplex should model participant-scoped limited participation through one
layered artifact:

- `participant-capability-limits.v1`

The artifact represents one participant-level state:

- `status = capability_limited`

That state always carries a soft layer:

- `soft.priority-factor`
- `soft.rate-limit-factor`

and may additionally carry a hard layer:

- `hard.blocked-operations`
- `hard.reason/ref`
- `hard.decision/author`
- `hard.expires-at`

The hard layer is therefore:

- explicit,
- authored,
- bounded in time,
- and narrower than full removal from the network.

## Proposed Model

### 1. Separation of Layers

`capability_limited` is a composite state, not a single switch.

- The `soft` layer adds friction.
- The `hard` layer removes selected operational permissions.

This lets the system degrade participation without collapsing immediately into
ban semantics.

### 2. Scope

The first artifact is participant-scoped:

- `participant/id = participant:did:key:...`

This is deliberate. The participant is the right MVP target for service-facing
restrictions such as `procurement/offer` or `endorsement/emit`.

The proposal does not yet extend the same artifact family to `org` or `pod-user`.

### 3. Soft Layer

The MVP soft layer freezes two factors:

- `priority-factor`
- `rate-limit-factor`

Both are normalized to `(0.0, 1.0]`, where `1.0` means no degradation.

The first Node runtime SHOULD consume `priority-factor` on procurement ranking
and SHOULD consume `rate-limit-factor` through a small deterministic per-participant
operation cooldown hook for the first admitted daemon operations.

### 4. Hard Layer

The MVP hard layer is an open namespace of blocked operations rather than a closed
enum of privilege names.

Examples:

- `procurement/offer`
- `nym/issue`
- `endorsement/emit`
- `relay/serve`
- `arbitration/participate`

This keeps operation semantics above the transport layer and avoids confusing
blocked service permissions with handshake-time advertised capabilities.

### 5. Protected Operations

Some operations remain outside the admissible hard-block set in MVP:

- `core/messaging`
- `keepalive`
- `dispute/file`
- `ubc/claim`
- `signal-marker/send`

These form the minimum floor of continued presence, communication, and appeal.

### 6. Relationship to Existing Peer Governor State

This proposal complements the existing peer-quality downgrade path.

- peer governor state remains transport- and session-facing,
- participant restriction state remains actor- and operation-facing.

The two MAY correlate in later policy, but they are not the same layer and
should not be collapsed into one mutable flag.

## First Runtime Hooks

The first Node runtime rollout should stay small but real:

1. reject `procurement/request` when the asking participant is hard-blocked for
   that operation,
2. reject `procurement/offer` when the responder participant is hard-blocked for
   that operation,
3. reject `response/deliver` when the responding participant is hard-blocked for
   that operation,
4. reject `procurement/contract-accept` when the asking participant is
   hard-blocked for that operation,
5. reject `response/accept` when the asking participant is hard-blocked for that
   operation,
6. reject `response/reject` when the asking participant is hard-blocked for that
   operation,
7. apply `soft.priority-factor` as a deterministic procurement-ranking penalty,
8. apply `soft.rate-limit-factor` as a deterministic per-participant cooldown on
   currently admitted daemon operations such as `procurement/request`,
   `procurement/offer`, `procurement/contract-accept`, `response/deliver`,
   `response/accept`, `response/reject`, and `signal-marker/send`,
9. keep `signal-marker/send` explicitly admissible as a protected-floor operation
   even when the participant is otherwise limited,
10. expose participant-side `response/accept` and `response/reject` through a
    dedicated participant-scoped daemon control contract instead of reusing
    operator action endpoints.

Discovery visibility, broader operation coverage, and richer graduated governor
policies remain deferred to later work.

## Trade-offs

### Benefits

- sanctions become auditable rather than folkloric,
- hard blocks become narrow and time-bounded,
- the project preserves a protected minimum participation floor,
- runtime policy can grow incrementally without redesigning identifiers.

### Costs

- one more artifact family to keep in sync across docs and runtime,
- temporary asymmetry where soft factors are frozen before every soft hook is
  equally mature,
- a new distinction operators must understand between peer downgrade and
  participant restriction.

### Risks

- if the blocked-operation namespace drifts semantically, enforcement becomes
  confusing,
- if protected operations are not frozen early, ad hoc sanctions may overreach,
- if soft factors are not consumed by real runtime hooks, the artifact becomes a
  paper tiger.

## Open Questions

1. When should `rate-limit-factor` become a generic per-operation governor hook
   rather than a stored-but-lightly-used field?
2. Should the first cooldown grain stay at `(participant, operation)`, or move
   later toward `(participant, operation, question)` for multi-contract
   concurrency?
3. Which artifact should carry later review history: this restriction record
   directly, or a separate review/case family?
4. Should `org` eventually use a sibling artifact or the same family with
   `subject/kind`?
5. Which operation ids should be elevated into a more formal registry first?

## Next Actions

1. Add `participant-capability-limits.v1` to the synchronized contract mirror.
2. Add Node-side import validation for that artifact.
3. Wire the first procurement and messaging hooks against the new artifact.
4. Revisit generic rate limiting only after the operation-facing governor layer
   is ready.
5. Keep launcher-facing participant lifecycle decisions on a distinct control
   surface from infrastructure-operator actions.
