# emergency-activation.v1 invariants

`emergency-activation.v1` is the smallest machine-readable seed for the
activation decision layered over an existing `exception-record.v1`.

## Invariants

1. `exception/type` MUST equal `emergency`.
2. `trigger/class ∈ { TC1, TC2, TC3, TC4, TC5 }`.
3. `credibility/class ∈ { C0, C1, C2, C3, C4 }`.
4. `activation/path ∈ { automatic, manual, escalation_auto }`.
5. `activated-by/kind = node   → activated-by/id MUST be node:did:key:...`.
6. `activated-by/kind = system → activated-by/id MUST equal system`.
7. `trigger/class ∈ { TC1, TC2, TC3, TC4 } → agents/elevated MUST be non-empty`.
8. `trigger/class = TC5 → agents/elevated MUST be empty`.
9. `deactivated/at` present → `deactivation/reason` and `review/due-at` MUST also be present.
10. `ttl/expires-at > activated/at`, `max-extension/until >= ttl/expires-at`, and `review/due-at >= deactivated/at` SHOULD be enforced by consumers at ingest time.

## Scope note

This record is the **decision layer**, not the input signal and not the full
exception base record. It assumes that:

- `emergency-signal.v1` already captured the observed inputs,
- `exception-record.v1` already exists as the audit root,
- this artifact only adds activation, extension, deactivation, and review state.
