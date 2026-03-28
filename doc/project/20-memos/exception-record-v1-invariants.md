# exception-record.v1 invariants

`exception-record.v1` is the smallest machine-readable seed for the full
exception record required by `EXCEPTION-POLICY`.

## Invariants

1. `policy/id` MUST equal `DIA-EXC-001`.
2. `exception/type ∈ { ordinary, emergency, injunction }`.
3. `risk/level ∈ { low, medium, high, critical }`.
4. `status ∈ { proposed, active, suspended, expired, rolled_back }`.
5. `owner/kind = node        → owner/id MUST be node:did:key:...`.
6. `owner/kind = participant → owner/id MUST be participant:did:key:...`.
7. `owner/kind = org         → owner/id MUST be org:did:key:...`.
8. `owner/kind = council     → owner/id MUST be council:did:key:...`.
9. `requester/kind = node|participant|org|council|system` constrains `requester/id` to the corresponding canonical form.
10. `approver/kind = node|participant|org|council|system` constrains `approver/id` to the corresponding canonical form.
11. `risk/level ∈ { high, critical } → approvals, monitoring/metrics, and rollback/conditions MUST all be non-empty`.
12. `expires/at > created/at` and `monitoring/review-at >= created/at` SHOULD be enforced by consumers at ingest time.

## Scope note

This base record intentionally does not include the emergency-specific activation
extension fields from `EMERGENCY-ACTIVATION-CRITERIA` such as `trigger_class`,
`credibility`, `activation_path`, or `ttl_expires_at`. Those belong in a later
`emergency-activation.v1` artifact layered on top of the same exception record.
