# Decision: Limited Messaging Grants under P076

Status: `accepted` — design adopted on 2026-10-16; runtime qualification is tracked separately.

Date: `2026-10-16`

Based on [P076](076-federation-identity-and-network-selector.md#open-questions)
and [P097](097-fresh-identity-onboarding-and-messaging-readiness.md).

## Executive Summary

Adopt one explicitly authorized delegation level for narrowly scoped Messaging
preparation by an ordinary participant, anchored in a sovereign issuer admitted by
the active federation root. Creating an identity, unlocking its key or completing
onboarding never grants this authority. Design adoption does not qualify the delegated runtime. Existing sovereign evidence retains its original scope.

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

## Decision

- Separate the beneficiary participant, actual signer/delegate and root authority
  anchor. The participant is not added to sovereign subjects as a side effect.
- The beneficiary is the ordinary primary operator of one Node. A separate encrypted
  local delegate key receives no sovereign standing and no general signing grant.
- `capability-issuance-delegation.v1` signs federation, grant id, sovereign subject,
  participant, node, delegate key, issuance callers, closed Messaging templates,
  validity and per-template maximum child TTL. Wildcards and onward delegation are
  forbidden. The templates are local send, request-specific receive consent and
  single-use INAC consent for `contact-request.v1` or `message-envelope.v1`.
- The issuance caller is host-authenticated and distinct from the child's allowed
  caller. The host proves route ownership and requires a durable explicit consent
  before issuing receive or INAC consent. Setup prepares the receiving role; it
  does not issue an any-sender passport for this path.
- `capability-passport.v2` carries the complete signed parent as
  `issuance_authority.delegation`; its beneficiary is explicit, while
  the parent explicitly names the sovereign anchor and delegate signer. V2 is a separate typed artifact with `beneficiary_participant_id`, `beneficiary_node_id`, `authority_subject_ref` and `signer_key`; the V1 struct and selectors remain V1-only. Its
  domain-separated signature covers the entire parent and scope. V1 retains its
  signing semantics. Unknown V2 must fail closed, with no proof stripping/downgrade.
- The grant request proves participant, node and delegate key possession, binds `federation_id`, the active root digest/version, includes
  a 256-bit nonce and expires within 15 minutes. Grant approval is an offline
  signing ceremony, never an onboarding side effect. Import does not change the
  federation root or its anti-rollback state.
- Both participant and org sovereign subjects may approve a grant. An org must meet
  a new explicit `capability-issuance` custody purpose with its authorized keys and threshold; withdrawal uses the separately adopted `capability-revocation` purpose with `any-authorized` policy;
  grant signing has its own domain and does not reuse a root-pack signature.
- Effective scope is the intersection of parent and child. Child validity cannot
  exceed parent validity or its per-template maximum TTL. The verifier checks
  signatures, all constraints, known revocations and the anchor/custody in the
  active root. Staged roots have no effect. No empty-roster authority fallback.
- **Revocation status source (F-01, adopted before runtime integration):** the
  offline issuer explicitly binds an online status key and endpoint in each signed
  grant. The service has authority to attest status only, never to issue grants,
  renew them or manufacture revocations. Seed Directory hosts this bounded status
  surface; official-service endorsement does not by itself grant status authority.
  An offline issuer need not sign a fresh status every five minutes.
- `issuance-revocation-status.v1` signs federation, grant id/full-artifact digest,
  monotonic revision, `as_of`, `valid_until`, active/revoked state and revoked child
  ids. Maximum observation validity is 300 seconds. A wall-clock fetch timestamp
  and an absent revocation record are never proof of non-revocation. Unknown or
  unregistered grants yield unavailable, never active. Initial registration and
  verified withdrawals are durable and serialized before a status can be signed.
  Re-registration cannot clear withdrawals. Clients persist revision high-water
  marks and known withdrawals; stale status cannot erase them.
- Status is fetched over the grant's exact endpoint and verified against its exact
  status key. Network errors, bad signature/context and stale status fail closed.
  Local child withdrawals remain immediate. For an honest service, already minted
  active observations can remain usable for at most their 300-second lease after
  a withdrawal commits. The online status key is an explicit trust assumption:
  compromise can forge fresh negative observations until parent expiry or another
  locally known refusal, and can deny service with false withdrawal assertions.
  It cannot sign a new grant or a sovereign/node withdrawal artifact. Known
  withdrawals cannot be erased by a later status. The service retains terminal
  grant withdrawal until after grant expiry and the observation window.
- `capability-passport-revocation.v2` supports parent/child withdrawal. Withdrawal
  of a parent, by its sovereign authority or the bound Node, cascades to all its
  receive passports and INAC invitations. It does not merely disable new issuance.
  Child expiry is bounded by parent expiry and per-template TTL, independently of
  the 300-second status observation window (Q-01).
- Locked delegate key: acceptance remains visibly pending and offers unlock;
  acceptance is committed only after its scoped child can be issued. No silent
  failed acceptance or automatic later approval (Q-02).
- Receive consent is evaluated by the host for every message against current
  authority in the active root. A receive passport requires its complete current
  proof, including parent status. An independently authored local `contacts`
  consent is eligible only while its receiver is itself a sovereign subject in
  that root. A delegated receiver's local facts may restrict, but cannot grant,
  authority beyond its grant. Root activation can therefore remove membership
  eligibility without rewriting relationship history.
- A membership projected from an accepted passport retains that passport's id
  and is never silently promoted to independent consent. Expiry or withdrawal
  invalidates that basis on both issuer paths. An independent local consent is a
  separate explicit action; revoking a passport does not change that separate
  decision. Admission records the chosen basis (`passport` or `local-membership`)
  and the host's eligibility evidence. An unusable delegated passport cannot
  fall back to its derived relationship projection.
- Readiness V2 has the same meaning on both paths: `receive/role-prepared` is local
  preparation; `receive/open-consent` separately reports the existing sovereign
  wizard passport if present. The delegated path never creates open consent.
  Send authorization does not depend on either receive facet (F-04).
- Empty sovereign rosters confer no authority on any path. Existing fallback checks
  are removed, and conformance/runtime fixtures use a nonempty explicit root that
  excludes ordinary beneficiaries and delegates (F-05).
- Parent renewal requires a new explicitly approved grant. Setup may renew children
  within a current parent using the shared idempotent coordinator. Historical keys
  retain historical results within the bounded receipt window (30 days after
  proof expiry). Expired requests/proofs then release local snapshot capacity;
  an expired parent cannot be reimported as current authority. Import, GET,
  restart, unlock and auto-ready do not
  resurrect authority-blocked intents or withdrawn consent.
- Readiness/decision/audit V2 distinguish sovereign membership from usable bounded
  issuance authority. The existing evaluator and execution guards remain the
  enforcement boundaries. Runtime proofs and release readiness remain separate.

Before the first release, read contracts and consumers switch together to V2.
No migration, downgrade adapter or version negotiation is introduced. Separate
passport types preserve the distinction between two authority proofs.

## Trade-offs

Delegation permits bounded renewal without continuously exposing the sovereign
signing key, but adds a revocable authority edge and additional proof validation.
Direct issuance remains a useful alternative if that complexity is unnecessary.
Multiple delegation levels, hosted multi-participant Nodes and grants for non-Messaging capabilities remain outside this decision.

## Failure Modes and Mitigations

| Failure | Required behavior |
|---|---|
| Delegate changes beneficiary, node, caller or profile | Refuse before issuance or execution effects. |
| Delegation is expired or revoked | Refuse even if the derived passport has not expired. |
| Authority anchor is removed by active-root rotation | Refuse historical passports; staging alone has no effect. |
| Legacy signing proof lacks signed issuance constraints | Do not infer constrained issuance authority. |
| Harness requests delegated path before implementation | Return `unsupported-issuer-path`; never fall back to sovereign. |

## Open Questions

Multi-user Nodes, deeper delegation and longer offline revocation leases require
separate decisions. None is a fallback
for this bounded first implementation.

## Implementation Tracker

Work is vertical, with review and qualification at the end of each slice. A schema
or unit test alone never closes a runtime gate.

| Task | Slice | Scope | Status | Completion gate |
|---|---|---|---|---|
| P076-028 | A | Decision, status authority/channel, V2 separation | done | Adopted decisions including F-01/F-07 and Q-01..03 |
| P076-029 | A | Participant issuer, status service, local send and ceremony | done | Clean Node `3e9507a9` / Orbidocs `5869853`: actual delegated send; beneficiary/delegate absent from root |
| P076-030 | A | Status outage/revocation, retry/restart and first qualification | done | Same binary set: real 300-second status outage, explicit retry, durable withdrawal and strict sovereign Story-010 |
| P076-031 | B | Scoped receive and explicit single-use INAC consent | in-progress | Bidirectional delivery with two independent consents; passport-derived membership cannot outlive its authority |
| P076-032 | B | UI, new MSG-ONB-007/008 delegated cases and qualification | todo | Two-tab recovery and parent withdrawal cascades |
| P076-033 | C | Explicit org issuance/revocation custody purposes | todo | Threshold issuance, any-authorized withdrawal and org qualification |
| P076-034 | final | Mixed/sovereign regressions and documentation | todo | One clean-source, profile/binary-pinned candidate |

The first vertical gate retains 1025 conformance/capsule test executions, 23 real browser cases, strict sovereign Story-010 and signed public proof requalification at `node:docs/evidence/limited-messaging/2026-10-16-participant-local-send/README.md`. No model or VM ran. This completes slice A only; receive/INAC, organization custody and the final mixed candidate remain open.

Work is paused at the user's request on 2026-10-17 after the current receive-basis
implementation and its local tests. P076-031 remains in progress. The locally committed implementation
checkpoint is recorded in
`node:docs/audits/P076-RECEIVE-AUTHORITY-CHECKPOINT-2026-10-17.md`; it does not
replace the clean-source slice-A evidence or close the delegated runtime gates.

MSG-ONB-005/006 remain closed with their original sovereign scope. Their reserved
`issuer-path` argument is reused by new MSG-ONB-007/008, not used to rewrite the
closed evidence. The delegated INAC template requires explicit `single_use=true`,
one peer and one nonempty artifact id; omitted/default values are refused.

## Next Actions

Implement and qualify slice A before B, and B before org custody C. Review after
each substantial slice, including the online authority's durable negative-proof
semantics and replay. Synchronize P032, P097, S027, INAC, schemas/mirrors, API
registry, Node ledger and MVP. No model or VM is required; historical qualifications
and release readiness remain distinct.
