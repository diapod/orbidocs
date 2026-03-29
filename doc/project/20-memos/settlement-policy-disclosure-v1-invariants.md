# settlement-policy-disclosure.v1 invariants

`settlement-policy-disclosure.v1` is the smallest append-only audit artifact for
operator-facing disclosure events affecting settlement policies in the
`host-ledger` rail.

## Invariants

1. `policy/ref` MUST be either `gateway-policy:...` or `escrow-policy:...`.
2. `operator/org-ref` MUST be canonical `org:did:key:...`.
3. `serving/node-id` MUST be canonical `node:did:key:...`.
4. `event/type` is an append-only event label, not a mutable policy state.
5. `disclosure/scope` defines how widely the event may be exposed, not whether the
   underlying policy exists.
6. `impact/mode` defines the practical operator impact of the disclosure and MUST
   stay separate from `event/type`.
7. `manual-review-only` and `blocked` impacts MUST declare `decision/basis` so
   bounded refusal remains distinguishable from opaque operator grace.
8. `decision/basis = case-bounded` MUST carry `case/ref`.
9. `decision/basis = exception-bounded` MUST carry `exception/ref`.
10. `incident/access-condition-violation` is the canonical event family for
    dignity-unsafe or arbitrarily discretionary settlement gating.
11. `effective/from <= effective/until` SHOULD be enforced by consumers when
    `effective/until` is present.
12. `incident/*` events MUST carry at least one formal anchor:
    `case/ref`, `exception/ref`, or non-empty `basis/refs`.
13. This artifact MAY snapshot `operator/org-ref` and `serving/node-id` even though
    those can be derived from the referenced policy, because audit must preserve the
    accountable organization and serving node as observed at event time.
14. `settlement-policy-disclosure.v1` does not replace `exception-record.v1`; it
    stays a smaller settlement-facing fact record and may optionally point at a
    fuller exception or case pipeline.
