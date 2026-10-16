# Decision: Limited Messaging Grants under P076

Status: `proposed` — no new issuance or delegation authority is adopted.

Date: `2026-10-16`

Based on [P076](076-federation-identity-and-network-selector.md#open-questions)
and [P097](097-fresh-identity-onboarding-and-messaging-readiness.md).

## Executive Summary

Recommend one explicitly authorized delegation level for narrowly scoped Messaging
preparation by an ordinary participant, anchored in a sovereign issuer admitted by
the active federation root. Creating an identity, unlocking its key or completing
onboarding never grants this authority. This decision remains proposed; the current
runtime continues to support only the locally qualified sovereign-operator path.

## Context and Problem Statement

P097 separates truthful readiness, operator root admission and enforced execution.
Its current local-send selector requires issuer/participant equality. It cannot be
relaxed merely because a passport carries `issuer_delegation`: the existing proof
delegates a signing key acting as its principal and retains that principal as the
issuer. Its grant map does not itself express all participant/node/caller/profile
constraints needed for ordinary-participant issuance.

## Options Considered

1. Admit every ordinary participant as sovereign. Rejected: it widens authority
   to solve local preparation and hides the governance decision in onboarding.
2. Let an admitted issuer issue each constrained passport directly. Viable, but
   requires issuer availability for each renewal and is not delegated issuance.
3. Authorize one bounded issuance delegate under an admitted issuer. Recommended:
   reuse signature verification, active-root lookup and target revocation while
   defining the missing signed issuance constraints explicitly.

## Proposed Decision

- Separate the beneficiary participant, actual signer/delegate and root authority
  anchor. The participant is not added to sovereign subjects as a side effect.
- Require a signed restriction to one participant, node, authenticated caller and
  `messaging-local-send@v1` profile, with explicit expiry. No wildcard or onward
  delegation is implied. Recipient receive consent and INAC consent remain separate.
- Effective scope is the intersection of the delegation and passport scopes;
  passport validity cannot exceed delegation validity. A proof of signing authority
  alone is insufficient to authorize constrained issuance.
- Verify every signature and constraint, delegation expiry and `revoked_targets`,
  and resolve the authority anchor against the **active** root. Staged roots do not
  change authority. Cache evidence must include the delegation and root revisions.
- A later implementation must replace the relevant self-issuer selection rule with
  this complete verifier, rather than remove equality/admission checks piecemeal.
- Retain versioned canonical signing semantics: adding unsigned constraints to an
  old proof is not a valid extension. Artifact/version selection requires adoption
  of this decision and a separate schema/implementation review.

## Trade-offs

Delegation permits bounded renewal without continuously exposing the sovereign
signing key, but adds a revocable authority edge and additional proof validation.
Direct issuance remains a useful alternative if that complexity is unnecessary.
Multiple delegation levels and ordinary-participant receiver-side issuance policy
are outside this first proposed decision.

## Failure Modes and Mitigations

| Failure | Required behavior |
|---|---|
| Delegate changes beneficiary, node, caller or profile | Refuse before issuance or execution effects. |
| Delegation is expired or revoked | Refuse even if the derived passport has not expired. |
| Authority anchor is removed by active-root rotation | Refuse historical passports; staging alone has no effect. |
| Legacy signing proof lacks signed issuance constraints | Do not infer constrained issuance authority. |
| Harness requests delegated path before implementation | Return `unsupported-issuer-path`; never fall back to sovereign. |

## Open Questions

Adoption must settle the canonical issuance-delegation artifact/version, the
actor/custody ceremony and the ordinary-participant receive/preparation policy.
These are design gates, not implementation defaults. P076's original question
remains open until the policy is adopted and its intended scope is explicit.

## Next Actions

Review and adopt or revise this record first. Only then create the implementation
tracker and delegated acceptance profile. MSG-ONB-005/006 reserve `issuer-path`
now but do not implement this authority path. Keep the ordinary self-issued
sovereign conformance and qualification independently reproducible.
