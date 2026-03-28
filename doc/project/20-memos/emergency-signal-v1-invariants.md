# emergency-signal.v1 invariants

`emergency-signal.v1` is the smallest machine-readable seed for one signal
entering the emergency evaluation pipeline.

## Invariants

1. `source/node-id` MUST be `node:did:key:...`.
2. `source/type ∈ { sensorium, operator, peer_report, oracle }`.
3. `trigger/class ∈ { TC1, TC2, TC3, TC4, TC5 }`.
4. `confidence/class ∈ { C0, C1, C2, C3, C4 }`.
5. `metadata/affected-scope ∈ { node, federation, inter-federation }`.
6. `metadata/urgency ∈ { immediate, hours, days }`.
7. `trigger/class = TC5 → tc5/active MUST be true`.
8. `tc5/active = true → trigger/class MUST be TC5`.
9. `corroborating/signal-refs` SHOULD contain no duplicates.
10. Confidence-to-corroboration thresholds remain runtime policy, not schema logic.

## Scope note

This record models only the **input signal**. It intentionally does not include
activation-decision fields such as `activation_path`, `activated_at`,
`ttl_expires_at`, or `review_due_at`. Those belong in a later
`emergency-activation.v1` artifact layered over the same emergency pipeline.
