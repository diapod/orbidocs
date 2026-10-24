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
- The current acquisition path reuses a fresh cached status or fetches it over the
  grant's exact endpoint, verifying it against the grant's exact status key.
  [P076-036](#p076-036-bounded-status-presentation-and-offline-acceptance)
  adds an attached-status input to the same verifier, not a second trust path.
  Network errors, bad signature/context and stale status fail closed.
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
  failed acceptance or automatic later approval (Q-02). Only an explicit operator
  decision exercises a delegated consent template; reciprocal, startup or repair
  acceptance falls back to that visible decision. One durable delegated child exists per
  decision; a lapsed unused INAC invitation needs a new durable decision
  generation. Its notification and issuance keys bind that generation; earlier
  notifications cannot authorize or reject it.
- A delegated single-use INAC invitation never becomes a standing transport
  contact. Later pushes carry their own current consent, so a parent or child
  withdrawal cannot be bypassed by an earlier approval. Withdrawal of a child
  is signed by the bound Node, immediate locally and published to the status
  authority; it does not withdraw the parent.
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

## P076-036: Bounded status presentation and offline acceptance

**Status: marker-free carrier passed bounded local host acceptance (2026-10-24).** The first receiver of a
V2 Messaging passport should be able to verify it without fetching status when
the presentation carries a usable, existing `issuance-revocation-status.v1` and
the receiver already has an independently admitted active root. This applies
[P032's bounded verification-material rule](032-key-delegation-passports.md#bounded-verification-material-across-artifact-families)
to the [P024 presentation boundary](024-capability-passports-and-network-ledger-delegation.md#implementation-notes)
and the [P060 consent handoff](060-messaging-middleware.md#3-message-envelopev1-artifact).

The slice extends the existing `capability-passport-present` contract and actual
Messaging receive-consent handoff, not every advertisement or message envelope.
The passport already carries its signed issuance delegation and status-authority
binding. The missing portable input is its short-lived signed status. Attaching
it changes neither the child's signed preimage nor the authority of any key.
It does not import a root, grant membership, create consent or install a local
issuance delegate. It does not make Messaging transport itself work offline.

### Frozen carrier and bounded acquisition (2026-10-24)

The existing `capability-passport-present.v1` remains the discriminator. For a
`capability-passport.v2` with `capability_id = messaging-receive`, it may contain
one optional, typed top-level field:

- `issuance/status`: the complete, unchanged `issuance-revocation-status.v1`
  signed object, interpreted only against the child's embedded delegation and
  the receiver's independently admitted local root.

Absence of `issuance/status` leaves the existing local-evidence or online
acquisition policy in force. The producer records its precise omission reason
locally; the receiver records `status/carrier: attached | absent` and the
verifier class in its presentation fact. No unsigned omission label crosses the
wire or contributes authority.

V1 presentations carry no issuance field. External consumers that do not understand
the optional V2 extension may continue their old online verification path, but
may not claim offline acceptance from a field they ignored. The built-in peer
importer refuses a portable carrier it cannot handle. The new host refuses
unknown `issuance/*` carriers instead of silently stripping them. The complete
presentation is limited to 128 KiB, the attached status to 64 KiB, and its
revoked-child list to 128 items, below the existing 256 KiB peer frame. These
values explicitly supersede the earlier planning bound of 64 KiB for the whole
presentation: 64 KiB now bounds only the signed status. The 128-item list limit
defends the receiving implementation; the local producer attaches only an empty
list under its private disclosure policy. These limits apply before signature
work; the AD raw admission remains capped at its
transport budget. The private consent handoff attaches a status only when its
signed revoked-child list is empty. Otherwise it records a local omission reason;
it never trims, redacts or re-signs the list. The network-disabled acceptance
adapter refuses missing usable evidence without calling the status endpoint;
the installed peer host uses the online policy, but a usable attachment prevents
its fetch. Normal online consumption retains the existing bounded fetch when no
exact usable local or
attached status exists, including when an authentic attachment has expired or
exceeds the child's stricter profile freshness. Both sources enter the same
durable revision and known-withdrawal merge. At equal revision a status replaces
the stored one only with a later signed `as_of`; all authenticated withdrawals
are accumulated even from older views. No receipt timestamp renews the signed
lease.
The verifier keeps distinct local refusal classes for missing evidence,
context mismatch (federation/grant/digest), status-authority key mismatch,
invalid status signature, revision rollback, revoked authority, expired lease
and narrower-profile stale observation. The outer Messaging readiness response may coarsen malformed
proofs, while the retained presentation fact records the verifier class.

### Implementation recommendations and reuse

1. **Contract before plumbing.** The optional typed attachment of the existing
   status artifact to the presentation is `issuance/status`.
   Freeze the exact schema/version and unsupported-consumer behavior through
   Schema Gate before implementation. Keep V1 passport semantics and the
   existing no-attachment online path. Never advertise successful offline
   verification when a consumer ignored or stripped the attachment.
2. **Reuse the pure verifier.** Extend the carrier in
   `node:capability/src/present.rs`; reuse status types in
   `node:capability/src/issuance.rs` and `verify_issued_passport` /
   `authorize_issued_consent` in `node:capability-binding/src/issuance.rs`.
   Supply explicit time, the current locally admitted root, persisted minimum
   revision and known withdrawals. Check exact federation, grant id/digest,
   bound status key, signature, parent/child constraints and status validity.
   The 300-second maximum lease and any stricter receive-profile limit remain
   unchanged; presentation receipt time never refreshes a signed observation.
3. **Reuse host ownership and transport.** The builder in
   `node:daemon/src/notifications_host.rs` obtains the existing owner's signed
   status snapshot and carries it through the existing peer-message handoff.
   The consumer in
   `node:daemon/src/endpoint_routes/federation_endorsements.rs` passes it through
   `node:daemon/src/identity_host/messaging_port.rs` to the existing observation
   path in `node:daemon/src/identity_host/messaging_issuance.rs`. Preserve peer
   binding, current-root checks and the durable observation store. An observed
   remote grant remains an observation, not a local delegate registration.
   No new generic proof bundle, crypto crate, status service or transport.
4. **One status state, two acquisition policies.** Attached and fetched evidence
   pass the same checks and durable revision/withdrawal merge. A valid attachment
   must not trigger a redundant fetch. In explicitly network-disabled
   inspection/acceptance, missing usable local or attached evidence is a named
   refusal, never a hidden fetch. Normal online acquisition retains its exact
   endpoint, timeout and response bounds. Invalid attached evidence must produce
   a diagnostic rather than a success attributed to that evidence; any allowed
   online recovery is separately reported. Revalidate current authority and
   freshness at consumption; a successful handoff is not a lasting authority
   cache. Preserve restart/replay and concurrent withdrawal protections.
5. **Bound and minimize disclosure.** Freeze byte and item limits within the
   existing presentation/transport admission budgets, before parsing unbounded
   input or verifying signatures. The status's revoked-child list can disclose
   associations: attach only when the handoff's disclosure policy permits the
   complete signed object. Never truncate, redact or re-sign it to fit. If it
   exceeds the budget or disclosure is disallowed, report the omitted-proof
   dependency explicitly and retain the ordinary online path; offline refuses
   unless usable exact evidence is already local. Do not publish private
   contact-nym bindings or generalize this to broadcast advertisements.

### Offline acceptance gate

Use existing issuance, capability-binding and Messaging handoff/replay fixtures,
with a network-denying status-fetch adapter and a call counter. Retain both pure
verification cases and a test of the real host presentation builder/consumer;
a synthetic verifier alone does not close the task. No models, browser campaign
or full two-node qualification are required for this bounded gate.

| Case | Required evidence |
|---|---|
| Cold status cache, independently admitted root, valid attached status | Real handoff consumer accepts the bounded observation with zero status-fetch calls; expected consent authorization succeeds only under its normal profile. |
| Missing proof without usable cache, revoked/expired/stale status, wrong grant/federation/key, or invalid signature | Distinguishable refusals with zero status-fetch calls in network-disabled mode; no successful consent admission. |
| Status within its lease but beyond a stricter receive-profile freshness limit | Refuse authorization; neither attachment nor a new receipt timestamp refreshes the evidence. |
| Revision rollback or known parent/child withdrawal, including after restart | Attachment cannot lower the high-water mark, clear withdrawal or resurrect consent; concurrent withdrawal is preserved. |
| Root/custody changes between build, observation and use | Current local authority wins; neither attached root material nor a historical successful observation bypasses it. |
| Byte/item overflow, prohibited disclosure, unsupported carrier | Bounded refusal or explicit omission/dependency; no silent stripping, partial signed object or offline-success claim. |
| V1 and no-attachment online regressions | Existing presentation and bounded endpoint acquisition remain usable without widening authority or freshness. |

Retain source-pinned inputs, explicit evaluation times, outcomes and fetch counts
using the existing limited-Messaging evidence/qualification conventions. Update
the Node ledger and MVP only for the measured presentation path. Passing this
gate proves bounded offline verification with pre-existing trust, not long-term
offline authorization, delivery availability or release readiness.

Dependencies are the existing V2 delegation/status verifier, durable observation
owner and scoped receive-consent handoff from P076-029–031. P076-034's full
mixed candidate is not a prerequisite; its qualification is neither reopened nor
claimed by this slice. Sequence implementation after contract freeze and owner
review to avoid concurrent rewrites of the same handoff. S007 and S027 link here
instead of duplicating a tracker or introducing another implementation owner.

## Implementation Tracker

Work is vertical, with review and qualification at the end of each slice. A schema
or unit test alone never closes a runtime gate.

| Task | Slice | Scope | Status | Completion gate |
|---|---|---|---|---|
| P076-028 | A | Decision, status authority/channel, V2 separation | done | Adopted decisions including F-01/F-07 and Q-01..03 |
| P076-029 | A | Participant issuer, status service, local send and ceremony | done | Clean Node `3e9507a9` / Orbidocs `5869853`: actual delegated send; beneficiary/delegate absent from root |
| P076-030 | A | Status outage/revocation, retry/restart and first qualification | done | Same binary set: real 300-second status outage, explicit retry, durable withdrawal and strict sovereign Story-010 |
| P076-031 | B | Scoped receive and explicit single-use INAC consent | done | Bidirectional delivery with two independent consents; passport-derived membership cannot outlive its authority |
| P076-032 | B | UI, new MSG-ONB-007/008 delegated cases and qualification | done | 2026-10-18 clean-source candidate: 1308 conformance/capsule executions, 34 strict Story-010 phases, 32/41 browser cases; signed public proofs requalified before/after extraction |
| P076-033 | C | Explicit org issuance/revocation custody purposes | done | 2026-10-23 focused gate: clean Node `16c39fa1` / Orbidocs `f7509ea6`, 1423 conformance plus 123 capsule executions, 34 strict sovereign phases and 42 browser cases; threshold issuance and separate one-custodian withdrawal, public proofs identical before/after extraction |
| P076-034 | final | Mixed/sovereign regressions and documentation | done | Clean Node `f38b821c6259b8c4a321025f650aced21e1dd963` / Orbidocs `afe06116c6172e19398a50977577baf72975c7cd`, `1559 conformance plus 188 original capsule executions`, strict sovereign Story-010 and the complete ten-scenario runtime on six unchanged binaries; signed proofs qualify identically before/after extraction. Local qualification only |
| P076-035 | UI follow-up | Child-consent inventory and individual withdrawal | done | 2026-10-21: 38/38 focused actual-browser cases on clean Node `baaef9d8` / Orbidocs `a889d11c`, six unchanged binaries and identical signed-public-proof qualification before/after extraction. Explicit idempotent child withdrawal preserves parent/siblings; no automatic authority or full-candidate/release claim |
| P076-036 | Portable-proof follow-up | Bounded signed issuance status in the existing V2 Messaging passport presentation | done | Marker-free clean-source local host gate at Node `2ce1eebd` / Orbidocs `007d47e9`: `node:docs/evidence/limited-messaging/2026-10-24-portable-status-marker-free/README.md` retains source/fixture hashes, evaluation times, results, 0 status fetches on attached peer handoff, 1 online fallback fetch and refusal/restart checks. The older marker-bearing and first incomplete diagnostics remain historical. No offline delivery or full runtime/release claim |

The first vertical gate retains 1025 conformance/capsule test executions, 23 real browser cases, strict sovereign Story-010 and signed public proof requalification at `node:docs/evidence/limited-messaging/2026-10-16-participant-local-send/README.md`. No model or VM ran. This completed slice A only; receive/INAC and later gates were outside that measurement, as recorded in the subsequent checkpoints below.

The 2026-10-17 continuation repaired the runtime integration found by its review
and by a two-ordinary-participant development scenario, recorded in
`node:docs/audits/P076-RECEIVE-INAC-RUNTIME-REVIEW-2026-10-17.md`. Development runs
use dirty sources and do not close the clean-source gate.

Work was paused at the user's request on 2026-10-17 after the receive-basis
implementation and its local tests. At that checkpoint P076-031 remained in progress. The locally committed implementation
checkpoint is recorded in
`node:docs/audits/P076-RECEIVE-AUTHORITY-CHECKPOINT-2026-10-17.md`; it does not
replace the clean-source slice-A evidence or close the delegated runtime gates.

The subsequent 2026-10-18 clean-source gate closes P076-031 at Node `f54f884c`
and Orbidocs `c6c3b0d2`: 1285 test executions, 34 strict sovereign Story-010 phases
and 24 HTML/API runtime cases between two ordinary participants outside root.
Signed public root/request/grant/child/status/withdrawal documents requalify before
and after archive extraction. See
`node:docs/evidence/limited-messaging/2026-10-17-receive-inac/README.md`.
This does not close P076-032, org custody or the final mixed candidate. The earlier
paused checkpoint and development measurements retain their historical scope.

The first P076-032 fragment adds participant-session, CSRF-protected public
request, grant import, delegate unlock and own-use withdrawal forms, plus a typed
pending-notification unlock path. The wizard labels usable issuance authority
separately from sovereign membership. Local UI tests do not close MSG-ONB-007/008;
at that first fragment, bidirectional real-browser and recovery qualification remained open. The first browser probe
passed the request/import/unlock forms and then exposed a user contact-search
writer missing the explicit local membership basis. The repair preserves host
authority eligibility; contact existence alone is no longer counted as successful
rail addition. The repeat at clean Node `739c32c9` / Orbidocs `93b07a9`
passes 27 focused browser cases (forms, actual send/open and parent-status recovery).
`node:docs/evidence/limited-messaging/2026-10-18-grant-ui-probe/README.md` preserves
the expected full-qualifier refusal of runtime-only input. It does not close
MSG-ONB-007/008.

MSG-ONB-005/006 remain closed with their original sovereign scope. Their reserved
`issuer-path` argument is reused by new MSG-ONB-007/008, not used to rewrite the
closed evidence. The delegated INAC template requires explicit `single_use=true`,
one peer and one nonempty artifact id; omitted/default values are refused.

## Next Actions

P076-034 closes the local full mixed/provider candidate. P076-036's first
focused diagnostics at
`node:docs/evidence/limited-messaging/2026-10-24-portable-status/README.md`
do not close the actual peer-import offline gate. The corrected path's earlier
clean-source local acceptance is retained at
`node:docs/evidence/limited-messaging/2026-10-24-portable-status-peer-route/README.md`.
Its former omission marker was removed before release. The final carrier's
clean-source local host acceptance is retained at
`node:docs/evidence/limited-messaging/2026-10-24-portable-status-marker-free/README.md`.
Track remote-withdrawal outbox behavior
and the separate lifecycle suite's ambient model-root isolation. Real email/SMS,
remote self-service catalog publication, production root activation and release
qualification remain separate. Review each substantial slice and preserve the
historical focused/refused measurements and their declared scope.

## P076-032 browser implementation checkpoint (2026-10-18)

Dedicated MSG-ONB-007/008 scenarios now drive both ordinary participants through
real grant forms, explicit INAC/contact consent and chat compose/open/read.
The separate `p076-browser` candidate pins one source/binary/capsule set for
conformance, strict sovereign Story-010 and delegated recovery. Short child and
parent TTLs use existing APIs and an explicit new offline grant ceremony; no
clock injection or automatic authority/resume is introduced. At this checkpoint
the gates remained in progress pending clean-source runtime and public archive requalification.

## P076-032 qualified checkpoint (2026-10-18)

`node:docs/evidence/limited-messaging/2026-10-18-delegated-browser/README.md`
closes MSG-ONB-007/008: clean Node `399ec846` / Orbidocs `26d5386`, six unchanged
binaries, 1308 conformance/capsule executions (1266 conformance + 42 capsule), 34 strict sovereign Story-010 phases and
32/41 real-browser cases. Both ordinary participants remain outside root;
independent explicit receive/INAC consents support correlated bidirectional
compose/open/read. Child and parent expiry, locked delegates, restart, stale
remote status and concurrent setup/single/bulk retry with a lost response deliver
once without implicit resume. Parent withdrawal cascades to receive and INAC.
Public signed proofs qualify identically before/after extraction. A verifier-only
follow-up at Node `92282400` normalizes observed remote grants; original reports
and its initial refusal remain intact. 53 offline tests pass. No model/VM ran.
P076-033 organization custody and P076-034 final mixed qualification remain open;
local qualification does not establish release readiness.


## Post-qualification review boundaries (2026-10-18)

P076-032's measured UI supports whole-grant withdrawal; listing children and
withdrawing one child are API-only. Q-02 was adopted on 2026-10-18: preserve this measured P076-032 scope;
P076-035 separately tracks child inventory and individual withdrawal in UI.
The original 007 unlock identifier came from the harness's issuance-status read;
it was not an independent observation from rendered HTML. A follow-up renders
the typed host response identifier and retains other pending notifications, but
requires a new runtime measurement beyond the historical source/binary pins.

The existing 007 fixture authors local address-book choices. Accepted-only contact
history after withdrawal is not measured there. Q-01 was adopted on 2026-10-18 in S032: retain withdrawn passport history;
only the latest independent local block overrides canonical fact order. The
follow-up browser case removes the receiver address-book membership fixture.
These display choices grant no receive authority; the historical 007 evidence
retains its original scope.

For P076-034, a separate sovereign attestation provider with ordinary participant
nodes is the recommended, still proposed contactability case (Q-03). Messaging
grants do not confer attestation-provider authority. 008 currently measures sender
issuance-authority recovery on new routes, with new explicit receiver consents;
it does not measure reuse of an expired receive consent (Q-04).

Next steps also track remote-withdrawal propagation and sender retries: the older
P076-031 child-withdrawal report records `ready-for-delivery`, whereas 007/008
record `waiting-for-contact-permission`. Also track isolation of ambient
`ORBIPLEX_MODEL_ROOT` in the separate `daemon_lifecycle` suite. These are observed
boundaries, not defects or measured parts of the historical 1308 executions
(1266 conformance plus 42 capsule). Historical evidence retains its date and scope.


The adopted Q-01 correction has a separate focused qualification:
`node:docs/evidence/limited-messaging/2026-10-18-contact-history/README.md`.
Clean Node `0af46d86` / Orbidocs `f4f57d4`, six unchanged binaries and 34/34 browser
cases cover accepted-only receiver history without fixture memberships and history
after parent withdrawal followed by explicit deferral. Signed public receive
proofs and message/digest/consent correlation requalify before/after extraction.
Historical reports and failed attempts remain unchanged. This focused gate does
not qualify the full P076-034 candidate, org custody or release readiness.
P076-035 remains the separate child-inventory/individual-withdrawal UI follow-up.

## P076-035 child-consent UI implementation checkpoint (2026-10-21)

Historical implementation status: `in-progress`, before the subsequent qualified
checkpoint below. The implementation and reviewed contract were accepted before
the focused browser gate was measured. Its retained evidence is now at
`node:docs/evidence/limited-messaging/2026-10-21-child-consent-ui/`. P076-032's
2026-10-18 API-only individual-consent scope remains a historical measurement;
P076-035 supplies a new UI gate without rewriting it.

`GET /v1/identity/messaging-issuance/grants` extends
`messaging-issuance-status.local.v1` with `grants[].passports[]`. Each row is an
exact locally issued child of the imported grant, bound to the current participant
and Node. Peer-observed grants and children are excluded. A row includes public
capability/profile, exact signed scope, validity, typed current-authority reasons,
local withdrawal, its stable public identifier and host-owned `allowed_actions`.
The existing 1024-child persistence bound is unchanged. GET uses one immutable
state/root/time observation; it does not refresh remote status, issue, withdraw or
retry anything. UI pages show at most 25 child rows.

Current authority and publication remain different facts. Displayed `ready` is
an observation, not reusable execution permission. Expiry, stale parent status or
a locked delegate do not by themselves prohibit withdrawal; the host controls
action eligibility, and the existing mutation endpoint checks authority again.
The publication vocabulary is closed:

| Publication | Meaning |
|---|---|
| `not-requested` | No durable local child withdrawal exists. |
| `pending` | Local refusal is effective, without an authenticated publication acknowledgement. |
| `confirmed` | An authenticated signed status explicitly lists this child as revoked. |
| `covered-by-parent` | An authenticated signed status revokes the parent and covers the local child withdrawal without a separate child acknowledgement. |

Status origin, grant binding and monotonic revision are verified before either
acknowledgement is reported. A correctly signed expired lease can still establish
known revocation; it cannot restore current authority. Explicit child
acknowledgement takes precedence over parent coverage. This distinction repairs
the review case where parent revocation stops separate child publication and an
already withdrawn child would otherwise appear permanently pending.

The native participant-session form posts to
`/app/welcome/messaging/issuance/consents/withdraw`, requires CSRF and explicit
confirmation, and binds the exact grant/child selection before forwarding the
immutable passport id to the existing host endpoint. Repeating a known withdrawal
reuses its stored signed artifact and id. It neither renews a child nor changes
the parent or siblings. Local refusal is durable before publication; unavailable
publication is visible and can be retried explicitly. GET, navigation, import,
unlock and restart do not approve pending requests, resume blocked messages or
grant sovereign authority.

The pending browser gate must correlate the rendered child scope and selected id
with the exact signed public proof; exercise confirmation/CSRF refusal, concurrent
submissions, lost response and known-withdrawal replay; preserve the active parent
and sibling consents; and show refused delivery for the withdrawn child. It uses
a synthetic federation without model/VM. P076-033, P076-034 and release readiness
remain separate.

## P076-035 qualified checkpoint (2026-10-21)

P076-035 is `done` within its focused UI scope. The normal `delegated-consent-ui`
attempt 09 passes **38/38 actual-browser cases** on clean Node `baaef9d8` /
Orbidocs `a889d11c`, with six unchanged binary digests and browser pin
`cfb30057edabf240d33882d1300390489804912fc8e57f7ba1e069e39a7b636f`.
`node:docs/evidence/limited-messaging/2026-10-21-child-consent-ui/README.md`
retains the report, signed public proofs, source/profile/binary pins, failed
attempt history and identical `qualified` results before/after archive extraction.

Two synthetic ordinary participants remain outside the sovereign root. The run
correlates the rendered exact child scope and native selection with signed proofs;
measures foreign-target, confirmation and CSRF refusals; and proves one durable
withdrawal across concurrent tabs, response loss and later explicit replay. The
first signed directory event, local receipt and public withdrawal agree. The
parent stays active and sibling public facts are unchanged. Reverse-direction
delivery still works, and the withdrawn receive permission refuses subsequent delivery while
contact history remains accessible without a receiver address-book fixture.

The Python browser pack passes 119/119 tests, including 17 actual-proof cases.
Previously passed unchanged-product checks remain separate: 7 daemon regressions,
368 UI unit plus 2 UI integration tests, 27 protocol, 6 CSRF-client and 22 ledger
tests. These counts do not represent a new full conformance/sovereign campaign.
No model or VM ran. Historical P076-032/007/008 evidence retains its API-only
individual-withdrawal scope. P076-033 and P076-034 remain `todo`; the retained
qualification explicitly reports `full_candidate_qualified=false` and
`release_ready=false`.

### Child inventory read refinement (2026-10-23)

The UI requests a host-selected global `consent_page` window, ordered by grant
and child id, with at most 25 projected children. Selection precedes proof
assessment and scope serialization; `consent_window` and `passport_total` describe
the full local inventory without its off-window scopes. Local storage is bounded
to 1024 children across grants. Exact `delegation_id`/`passport_id` selection
supports bounded single-child withdrawal preflight on the same GET; it cannot
substitute a sibling, peer observation or another owner.

The form and refresh link preserve the validated page. Only this GET ignores
unrelated navigation parameters; invalid/duplicate known selectors and unknown
mutation fields are refused. Human labels explain authority and publication,
while technical details retain exact codes. No execution authority or historical
qualification changes; Node records this local regression checkpoint separately
from the 2026-10-21 browser measurement.

## P076-033 implementation checkpoint (2026-10-23)

The active signed root carries one `federation-root` rule and an optional paired
`capability-issuance` threshold / `capability-revocation` any-authorized policy.
Purposes are unique and closed; pack signatures bind every rule. The root rule's
mode/quorum is independent of the other purposes. Missing, duplicate, unpaired,
wrong-mode and unachievable policies are refused. Key aliases count once.

Node composes these exact policies into its existing issuance-proof verifier.
Custodian refs authorize signatures for the org; they do not admit those
participants, beneficiaries or delegates to sovereign authority. Grant templates,
expiry, signed revocation status and current-root execution guards are unchanged.
Root-draft tooling adds the pair only when explicitly requested, without signing
or activating the result. Local conformance and review are recorded at
`node:docs/audits/P076-ORG-CUSTODY-REVIEW-2026-10-23.md`.

At this implementation/conformance checkpoint P076-033 was `in-progress`;
the subsequent focused qualification is recorded below. P076-034 and release
readiness remain separate.

The P076-033 runtime gate is now defined as `candidate.py --scope p076-org`:
closed conformance, strict sovereign Story-010, and the pinned-browser
`delegated-org-custody` scenario from one clean source/binary set. It measures
partial/duplicate/wrong-purpose signatures and custodian self-issuance refusals,
full exchange with separate contact/INAC decisions, and one authorized custodian's
parent withdrawal while fresh child consents are active. Bound-node self-withdrawal
is a separate earlier phase. The offline qualifier rechecks public signed
artifacts and the measured custody roles; it cannot claim the final mixed gate.
The grant helper adds explicit offline authority-withdrawal draft/sign/verify
commands. Publication is a separate operator action, never an implicit UI GET.

### Organization gate boundary review (2026-10-23)

The focused custody gate withdraws A's active parent immediately after a second
B-to-A delivery on its independent receive consent. B's earlier child withdrawal
applies only to the opposite direction. This proves issuer cascade without adding
a separate parent-renewal ceremony or mistaking an already-withdrawn consent for
an active one. The external issuer document is distinct from bound-node own-use
withdrawal; local relationship history need not invent a local revocation event.
Current host assessment, rather than the historical projection, denies receipt.

The additional A2 renewed-sender cohort in diagnostic attempts 01–03 did not
complete contact exchange. Attempt 03 had a new outgoing canonical request ID but
still timed out; its cause remains unqualified. P076-034 must investigate this
cohort before the full mixed candidate. It is not closed by the focused custody
gate or by source-level inference.

## P076-033 focused custody qualification (2026-10-23)

The [retained Node gate](https://github.com/diapod/node/blob/master/docs/evidence/limited-messaging/2026-10-23-org-custody/README.md)
qualifies slice C only: clean Node `16c39fa1` / Orbidocs `f7509ea6`, one unchanged
six-binary set, 1423 conformance plus 123 capsule executions, 34 strict sovereign
Story-010 phases and 42/42 actual-browser cases. Two keys issue each org grant;
the third authorized custodian withdraws A's active parent after the independent
reverse consent delivered. All children deny, compose returns actual HTTP 403
without a new outbox ID, and B cannot deliver on that previously working consent.
No custodian, ordinary beneficiary or delegate becomes sovereign.

Fourteen public proof files requalify identically before/after extraction. The
final offline pack is 131/131 without skips; its eight retained-proof tests were
not counted as passing in the original 123-execution capsule step. Three failed
attempts remain failed. Their extra A2 cohort is not qualified by this gate;
P076-034 carries diagnosis and the full mixed/provider candidate. Historical
007/008/035 scopes are unchanged. No model or VM ran; full-candidate and release
readiness remain false.


## P076-034 candidate contract and A2 diagnosis (2026-10-23)

A2's additional diagnostic reproduced selection of an older A1 INAC notification
by peer/schema while the new request's offer remained pending. The acceptance
repair matches the current outbox request and generation to the exact locally
observed offer, and chooses a UI local-contact projection rather than its
participant alias. This corrects evidence collection, not runtime authority.
Earlier failed P076-033 attempts retain their original result and scope.

The final gate freezes one clean Node/Orbidocs source set and six binaries after
conformance, then runs strict sovereign Story-010 and ten focused scenarios:
sovereign onboarding/recovery, S027-008 fact recovery, HTML delegated receive,
MSG-ONB-007/008, organization custody/child UI, explicit A2 renewal, mixed exchange
and two ordinary participants using a third sovereign contact provider. Each
scenario pins its profiles and public transport certificates. Signed public facts
are requalified identically before/after archive extraction. A focused success or
a development probe cannot substitute for this complete sequence.

Q-03's separate-provider acceptance is included in this gate. Its synthetic
provider has its own daemon, participant, node and leaf keys. The common transport
CA only permits TLS verification of node-address advertisements; it is not a
sovereign grant. Both Messaging beneficiaries stay outside root. OTP delivery uses
the existing dev mailbox with `always-accepted` disabled. Grants still confer no
contact-control attestation or Contact Catalog provider authority.

The gate remains in progress until retained clean-source measurements exist.
Local final-candidate qualification and release readiness remain distinct.
Implementation review: `node:docs/audits/P076-A2-AND-FINAL-CANDIDATE-REVIEW-2026-10-23.md`.

The separate-provider diagnostic reached verified host discovery but challenge
creation returned 401 because the service expected its local client token. The
operator adopted P061's explicit public challenge/redeem opt-in on 2026-10-23;
status/debug and lifecycle remain protected, default access remains closed, and
public replies carry no dev code. The provider token stays local. Synthetic
acceptance substitutes only OTP delivery through protected operator status.
P076-034 remains in progress until this complete path is measured.

The Q-03 topology also distinguishes local publication from provider admission.
The ordinary node signs and publishes its contact claim locally. The separate
catalog operator admits that exact claim and the provider-issued control passport
through its existing authenticated API. Public lookup and native contact addition
then use that admitted route. This gate does not claim remote self-service claim
publication; neither token distribution nor ordinary catalog-provider authority
is introduced. The retained proof binds claim and control signatures to the
operator admission.

The HTML/API regression scenarios explicitly negotiate P095's current protected
HTML representation, retaining session, CSRF, Origin and presentation-context
checks. This is a server-side contract measurement, not JavaScript execution or
browser-restoration evidence. Only the separately pinned Chromium scenarios
establish the browser claims; no representation header grants authority.

The retained final attempt10 measured A2 renewal54 on clean sources after the
wrong-offer observer repair. It then refused mixed setup at component enabling,
so this is an A2 runtime result inside an unsuccessful complete candidate, not
P076-034 completion. The original first-ten attempt capsules preserve their
results. The offline final gate is being strengthened to require the same closed
case inventory as the runner and bind receive decisions to exact typed child
consents and message/INAC observations; signatures alone do not establish the
purpose of a child passport.


## P076-034 local final qualification (2026-10-24)

Clean Node `f38b821c6259b8c4a321025f650aced21e1dd963` / Orbidocs `afe06116c6172e19398a50977577baf72975c7cd`, one unchanged six-binary set,
`1559 conformance plus 188 original capsule executions`, strict sovereign Story-010 and all ten runtime scenarios.
Exact signed public proofs qualify identically before/after archive extraction.
`full_candidate_qualified=true`, `release_ready=false`; synthetic federation, no model/VM.
See `node:docs/evidence/limited-messaging/2026-10-24-final-candidate/README.md`.

Explicit contact and INAC decisions remain independent. Delegated beneficiaries,
delegates and custodians receive no sovereign authority. The separate
provider substitutes protected dev-mailbox OTP delivery and explicitly
admits the participant-signed claim through its operator API. Actual
email/SMS delivery and remote self-service publication are not qualified.
Historical focused/refused runs retain their original source pins and
results. At that P076-034 checkpoint, P076-036 remained planned; production root activation and release
readiness remain separate gates.
The earlier 54-action focus remains a report-contract refusal. This fresh
complete candidate does not retrospectively repair its reserved-field error
or promote any earlier refused attempt or focused diagnostic.
