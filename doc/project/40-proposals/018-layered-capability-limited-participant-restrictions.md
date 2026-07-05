# Proposal 018: Layered `capability_limited` Participant Restrictions

## Status

`promoted`

Promoted to: `doc/project/60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md`

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

The MVP rollout also persists imported restriction records in the daemon commit
log, replays them into the local read model after restart, exposes local
operator import/list/detail/clear control surfaces, and records clear operations
as daemon-local tombstones with optional `reason/ref`. The daemon keeps a
monotonic `last_cleared_at` read model so imports with `recorded-at` at or before
the latest clear tombstone cannot resurrect stale sanctions, including after
commit-log replay. Import rejects already-dead hard blocks where
`hard.expires-at <= recorded-at` or where `hard.expires-at` has already passed at
import time, rejects stale `recorded-at` overwrites of a newer local record, and
applies Rust-side defense-in-depth validation for participant id shape,
`reason/ref` bounds, and soft factors in `(0.0, 1.0]`. List/detail export paths
validate each emitted record through the same schema-gate family before returning
operator JSON, while import/clear bodies are bounded to a small local control
payload size. Import and clear also emit a metadata-only
`participant-capability-limits-changed` SSE event so operator surfaces can
refresh without scraping the commit log. Discovery visibility, broader operation
coverage, maximum hard-block renewal policy, and richer graduated governor
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

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-05:

1. The first cooldown grain remains `(participant, operation)`. A later
   `(participant, operation, question)` grain may be introduced only when
   multi-contract concurrency requires it.
2. Later review history belongs to a separate review/case family. The
   restriction record remains the active restriction fact rather than the full
   procedural history.
3. Organization restrictions use the same artifact family with `subject/kind`.
   This keeps the evaluator and read model shared across participant and
   organization subjects.
4. The first operation ids to elevate into a formal registry are messaging,
   broadcast, marketplace, governance, and public-publish operations.

## Implementation Status

| ID | Feature | Status | Notes |
|---|---|---|---|
| P018-01 | Canonical `participant-capability-limits.v1` schema and Node contract mirror | done | The schema is synchronized into Node protocol contracts and closed at the top-level security gate. |
| P018-02 | Schema-gated daemon import | done | Invalid JSON, oversized local bodies, invalid restriction records, already-dead or already-expired hard blocks, stale `recorded-at` overwrites, stale imports behind a clear tombstone, invalid participant ids, unsafe `reason/ref` values, and out-of-range soft factors are rejected before mutating runtime state. |
| P018-03 | Hard-block enforcement for first privileged operation set | done | Procurement and response operations fail closed when an active hard block matches the operation. |
| P018-04 | Protected-floor enforcement | done | `core/messaging`, `keepalive`, `dispute/file`, `ubc/claim`, and `signal-marker/send` are rejected at schema level as hard-block targets; runtime keeps `signal-marker/send` and participant-side `dispute/file` admissible. |
| P018-05 | Soft `priority-factor` ranking penalty | done | Procurement offer scoring consumes the imported participant restriction state deterministically. |
| P018-06 | Soft `rate-limit-factor` cooldown hook | done | The daemon applies per-participant operation cooldowns for the current admitted operation set. |
| P018-07 | Durable daemon replay | done | Imports and clear tombstones are appended to the daemon commit log; replay preserves monotonic `recorded-at` and `last_cleared_at` read models. |
| P018-08 | Operator control-plane surface | done | Local HTTP exposes import, schema-gated list/detail export, and clear operations; clear accepts optional bounded `reason/ref`, and import/clear emit metadata-only SSE refresh events. |
| P018-09 | Participant-scoped lifecycle controls stay separate from operator execution actions | done | Participant accept/dispute/reject surfaces remain distinct from infrastructure-operator execution controls. |
| P018-10 | `subject/kind = org` support using the same artifact family | deferred | Organization restrictions share evaluator and read-model semantics with participant restrictions; trigger this after P017 organization subject invariants are frozen. |
| P018-11 | Review/case history moves to a separate artifact family | deferred | The active restriction record remains the authoritative restriction fact; procedural review history must not bloat this artifact. |
