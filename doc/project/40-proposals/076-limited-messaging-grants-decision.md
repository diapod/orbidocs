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
  Qualified [P076-036](#p076-036-bounded-status-presentation-and-offline-acceptance)
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
Multiple delegation levels and hosted multi-participant Nodes remain outside this decision.
Non-Messaging grants remain outside this original decision and its qualification.
The later [P015 contextual bootstrap profile](015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md#narrow-bootstrap-delegation-and-local-consent)
adopts one separate singleton nym-only template. It preserves beneficiary equality
and existing root/status verification, requires independent host-owned local
consent and confers no Messaging readiness, send/receive or sovereignty.

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

**Status: bounded gate qualified (2026-10-24).** The first receiver of a
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

### Frozen presentation contract — 2026-10-24

`capability-passport-present.v2` is a closed carrier containing only a V2
passport and optional `issuance/status` (`issuance-revocation-status.v1`). Signed
documents and preimages are unchanged. V2 rejects signed subdocuments whose
typed decoding would reorder arrays, insert defaults or discard fields; it never
normalizes incoming signed material. V1 input remains open and supports both
passport versions. New delegated Messaging handoffs always use V2, including
when status is omitted, without automatic downgrade. Pre-release deployments
must use receivers implementing that carrier. Mixed older receivers explicitly
refuse it; schema negotiation is outside this stage. The compatibility regression
models the older V1 Schema Gate, not an old running binary.

The canonical carrier budget is 65,536 bytes, checked after the existing bounded
1 MiB frame decode and before cryptography/merge. Check final frame size too.
There is one status and at most 4096 signed revoked-child identifiers. Never
truncate, redact or re-sign the status.

Disclosure is explicit per owned local grant: `status_disclosure = omit |
full-status`, default `omit`, including empty revoked-child lists. The operator
sets it through `POST /v1/identity/messaging-issuance/grants/presentation-policy`;
remote observations cannot grant this action. The existing inventory exposes the
policy and allowed action. This metadata changes neither the signed grant nor
issuance authority. The original qualified capsule excluded UI. Its review
follow-up adds a confirmed owner form to the existing grant page. Policy and
actor/node/time/old/new audit metadata commit atomically; identical assignment
adds no event. Retain 64 changes per grant with explicit dropped-history count.
Normal inventory windows show one latest change; exact-grant inspection combines
`delegation_id` with a bounded `consent_page` and returns the retained history.

The builder reads one owner snapshot without fetching/signing. Attach only a
currently valid full status allowed by policy, fitting the budget, with at least
60 seconds of useful validity after profile and parent/child expiry bounds.
Omission is a local typed diagnostic, not a peer-supplied policy label. It does
not roll back an accepted contact. Policies affect new builds, not copies already
disclosed.
The 60-second margin is fixed. A profile budget of 60 seconds or less normally
cannot supply that useful window; exact local observations or online fallback
remain available. Repeated omissions
under `full-status` receive bounded-frequency info diagnostics.

The entire typed presentation crosses builder/dispatch/authenticated-peer/cache/
issuance boundaries. Host context binds the beneficiary node to the actual peer;
trusted local import is explicit, never inferred from missing peer identity.
Observation results distinguish observed, deferred and refused; a handled frame
or transport receipt is not authority. Generic dispatch, AD/reference/batch and
network-ledger consumers reject the new carrier. Present-request responses stay V1.
Deferred/refused peer imports produce warnings and metadata-only local observation
facts, independently of transport success. Inspection counters state their
host-lifetime scope; neither counters nor diagnostic identifiers confer authority.
Local observation capacity has its own `issuance-observation-capacity-exhausted`
reason (unknown/503), distinct from an unavailable status source.

### Shared observation and online acquisition

All status acquisition uses one bounded `IssuanceStatusSource`: the signed
endpoint, 5 seconds, 1 MiB, no redirects. Import, presentation, pending retries and
manual/periodic refresh share this port and merge. Invalid root/grant registration
never selects a network endpoint.

There is **no product NoFetch mode**. Check an attachment's signature and binding
even if local cache is valid; malformed evidence refuses without fetch or write.
Authentic stale evidence contributes negative knowledge. Use exact current local
or attached evidence when sufficient; otherwise attempt exactly one online fetch,
including when an authentic attachment is stale. Never retry that fetch implicitly.
After acquisition and acquisition of the state writer, obtain one explicit
evaluation time `at` and pass it through
verification and merge; a status minted during fetch must not be evaluated against
the earlier request time. Later authorization remains a separate current check
without hidden I/O.

Merge is monotonic: maximum revision, union of known child withdrawals and
permanent parent withdrawal. Lower revisions do not change state. Within one
revision retain the latest signed `as_of` with deterministic ties; freshness-only
changes are not equivocation. Different withdrawal semantics at equal revision
retain their union and bounded equivocation diagnostics. Keep the signed snapshot
separate from local knowledge; never fabricate a joined signed status. At 4096
known revoked children, overflow persists a local unavailable guard rather than
dropping negative facts. The same capacity-safe merger is used by presentation,
import and refresh. Full positive-receipt admission cannot roll back a verified
negative join. Store overflow records a sticky local unavailable guard; a bounded
unknown-grant admission guard also applies to later imports. These are not issuer
revocations, and refresh cannot clear them. Recheck under the owner's atomic
update and preserve knowledge through restart/replay. Cache only cryptography.

### Bounded host-path acceptance gate

Conformance and real host-path evidence are distinct. Use synthetic federation,
controlled authority time and a counting, network-denying source adapter. Do not
add a daemon configuration test mode. Control the fixture refresh loop separately
from the measured presentation; production refresh continues normally.

| Case | Required evidence |
|---|---|
| Cold status cache, admitted root, usable attached status | Actual builder-to-peer-to-observation handoff and normal consent authorization; zero fetch attempts |
| Exact useful local evidence, no attachment | Accepted from cache; zero fetch attempts |
| Missing or authentic stale evidence | Exactly one attempt; typed unavailable/stale with denied adapter, success with a fresh source response |
| Status signed during fetch | Final evaluation uses time after acquisition and accepts a valid new as_of |
| Invalid attachment, grant, root or peer | Refusal without fetch/store pollution, even with useful cache |
| Known withdrawals, rollback, restart and concurrent merge | No lost negative knowledge or resurrected consent |
| Equal-revision refresh/equivocation and capacity overflow | Deterministic snapshot, union/diagnostics and persistent bounded guard |
| Time/profile/root/custody changes | Current locally admitted authority and original signed lease win at use; staged root changes nothing |
| Disclosure, 60-second margin, byte/item limits and unsupported consumers | Exact boundary cases and typed omission/refusal; no downgrade, stripping or generic authority installation |
| V1/no-attachment online regressions | Existing authority scope and bounded acquisition preserved |

Evidence pins clean sources, test executable, fixtures, evaluation times, digests,
outcomes and fetch counts. Retain exact public documents and compare qualification
before/after extraction. No browser campaign, model, VM or new full P076-034 run.
This proves bounded verification during a signed lease (at most 300 seconds,
potentially shorter by profile), not long-term offline authorization or delivery.
Full-candidate and release flags remain false. Source-query privacy remains open.

Dependencies are the existing V2 delegation/status verifier, durable observation
owner and scoped receive-consent handoff from P076-029–031. P076-034's full
mixed candidate is not a prerequisite; its qualification is neither reopened nor
claimed by this slice. Sequence implementation after contract freeze and owner
review to avoid concurrent rewrites of the same handoff. S007 and S027 link here
instead of duplicating a tracker or introducing another implementation owner.

## P076-037: Status acquisition policy and contact renewal

**Status: decision adopted; focused implementation and host acceptance done.** A local
node-scope P091 setting `/messaging/issuance/status-acquisition` has three closed
values: `online` (default), `scheduled-only`, and
`no-observed-grant-query`. The setting is live and applies at each status-source
call. It changes acquisition timing, never the signed lease, V2 preimage,
verifier, durable high-water mark, locally admitted root, or current-use check.

| Mode | Observed grant at presentation or operator refresh | Observed grant in S020 refresh, including pending retry | Owned `LocalDelegate` refresh | Explicit verified local grant import |
|---|---|---|---|---|
| `online` | allowed | allowed | allowed | allowed |
| `scheduled-only` | refused before I/O | allowed | allowed | allowed |
| `no-observed-grant-query` | refused before I/O | refused before I/O | allowed | allowed |

An owned grant is a durable `LocalDelegate` with its local encrypted key; endpoint
location does not define ownership. An explicit import is bound to the current
operator, grant registration and possession request before it selects the signed
status endpoint. Publication and bounded retry of signed parent/child withdrawals
are independent of this read policy and remain active when S020 is disabled.
Unavailable policy resolution fails closed for observed-grant queries. An
acquisition already admitted before a live setting change may finish and merge;
its diagnostic records the `resolution/id` used at admission. The source returns
a typed `AcquisitionDisabled`, distinct from source outage or stale evidence.
The resolver still reads every bounded node configuration source at a decision;
it reuses a successful parse only for the exact unchanged source bytes. A broken
unrelated source therefore also closes observed-grant queries until repaired.
Operator `refresh` is an on-demand decision and follows the presentation column;
only S020 `refresh-status` may perform the scheduled-only observed query.

When a delegated `messaging-receive` observation becomes too old, Messaging may
make one bounded request to the original authenticated presenting peer before a
send attempt, then re-read and authorize current consent. The existing
`capability.passport.present.request/response` pair gains an explicit typed V2
request for the exact `passport/id` and `cached-only` or `allow-owned-fetch`.
Legacy V1 requests and responses retain their prior meaning; V1 cannot answer a
V2 request. `scheduled-only` requests cached evidence only.
`no-observed-grant-query` may authorize the presenter to make at most one status
fetch for its **own** grant. The presenter must hold the exact local passport,
current root and original authenticated handoff-peer binding, and the local
`full-status` disclosure decision. An old local passport without that binding
requires a new handoff. A requested response uses the unchanged closed V2 carrier
and needs at least 15 seconds of useful signed validity; the original unsolicited
handoff retains its 60-second margin. Missing peer, disclosure, status or time
refuses without manufacturing evidence or widening lease. No raw child-revocation
list or status URL enters policy diagnostics.

The renewal budgets are nested: the presenter's own HTTP status attempt has a
2-second timeout, the holder waits up to 8 seconds for the authenticated peer
response after a peer-session dial capped at 8 seconds, and the local Messaging
preflight waits up to 24 seconds. A lane can wait at most 3 seconds for a
concurrent renewal. These bounds do not extend the signed status lease.
The presenter handles the request synchronously on a peer-session worker, so an
allowed own-grant fetch can occupy that worker for up to 2 seconds. At most four
such fetches run concurrently per host. A failed fetch is suppressed for 5
seconds per bound peer, in a bounded in-memory cache; no status or permission is
cached by that mechanism. An unknown passport and a passport not bound to the
authenticated peer have the same `passport-unavailable` refusal. After a fresh
fetch, known revocation or passport expiry is a definitive refusal, not
`status-too-old`; an exact send waiting on that passport stops retrying.

The direct holder's lack of authority queries is a narrow privacy claim. The
presenter may query the status authority on demand, so that authority may infer
the timing of a peer request. Peer connectivity and owner disclosure remain
prerequisites for renewal; this is not offline message delivery. S020 owns the
60-second status-refresh cadence with a bounded stable jitter and skip-missed
behavior. A distinct durable withdrawal-publication retry worker is independent
of S020. Pausing the status job or disabling the whole scheduler is visible in
readiness but does not invalidate otherwise current signed evidence. Without
another refresh, owned grants also lose fresh presentable status when their
signed evidence passes the profile limit. The S020 worker checks stop and
execution budget between pending observations and four-fetch groups; an
in-flight HTTP attempt has its own five-second bound. The P076-037 close gate required targeted
host-path, policy, peer, scheduler, INAC, AD and send regressions with exact
source-pinned evidence; full-candidate and release flags remain separate.
The 2026-10-25 focused capsule pins clean Node
`c08f3b46adae0cd4d4436e5c376463e1651158cd` and Orbidocs
`e2ab1f27075902bd91748f5c2ea3c72adf0b4dcb`; its public synthetic inputs
and results are in retained capsule `p076-status-acquisition-20261025`, identified by its
`inputs.json` SHA-256 `a27f0a5929f5bcb67191c36bf1547d30b04c5dabfb24916d3f2d55ade7f46919`
and `host-path.json` SHA-256 `98fc0ff97781f3389b1883484d97b97dee04ca243f7cee7cd40af52a6af7f861`.
Actual WSS renewal records zero holder queries and one permitted presenter
query. The same binary passed one short synthetic two-peer probe on each of
two distinct test hosts; this is not cross-machine delivery evidence.

The P091 setting and local readiness/request schemas extend `.local` contracts
within this unmerged slice. They are not signed passport fields or a change to
remote V1 semantics. Their closed local value enums were expanded in place
before a released producer or consumer existed; future released wire changes
require a new contract version.

The corrective review on clean Node
`235c23543245db1644b1cd8949ec3101f3a274f8` and Orbidocs
`d9f91bfc19e5292a7037af1985248e8191a58ffc` is recorded in Node
`docs/audits/REVIEW-P076-037-CORRECTIONS-2026-10-25.md`. Its retained
capsule `p076-status-acquisition-review-repairs-20261025` is identified by
`manifest.json` SHA-256
`ebf0574ca8ee2280b764fa660a80f68287333818c2ed1b0348121d8e7030bd5b`.
The corrected local WSS gate observes 0 holder and 1 presenter status
query. The same corrected binary passed one named WSS test on a second host,
using that host's existing distribution resources. The remote-probe record
has SHA-256
`7aef5bd7347bf73444553ae9af320126489f97b712688ad7d5fe219255a30998`;
it retains setup refusals and confirmation that the temporary binary was
removed. This is not cross-machine message-delivery evidence.

## P076-038: Two physical host consent renewal qualification

**Status: contract adopted; implementation and qualification in progress.** The
claim `acceptance-claim:p076-038-two-physical-host-renewal-v1` requires exactly
two logical nodes on two distinct physical hosts, independent synthetic root
admissions, separate storage and direct product WSS. It qualifies recipient-side
receipt after V2 renewal under all three P091 modes. It does not establish
offline message delivery, production HTTPS status retrieval, or release readiness.
The holder's mode governs whether it queries an observed grant; the presenter
obeys the `cached-only` or `allow-owned-fetch` choice in the request, even when
its own P091 mode is more permissive. An authority may infer when a presenter
makes an allowed own-grant query. A local `status_disclosure=omit` cannot silently
produce an offline-ready consent.

A signed `issuance-revocation-status.v1` with `as_of` in `(now, now+5 s]` can
advance durable revision high-water marks and known revocations. It cannot
authorize before its signed `as_of`. More than five seconds of future offset
is a refusal. The existing 300-second lease, `valid_until`, and narrower child
profile still use the issuer's signed times and are never lengthened by this
tolerance. A pending send receives the typed local `status-not-yet-valid`
reason and signed `retry/at`; at that time the owner rechecks the current root,
custody, revocations and freshness using retained status, without a new peer
request or status HTTP call. The old local readiness/send v2 projections retain
`revocation-view-stale`; new closed v3 read and send decisions expose the new
reason. The v3 host send alias retains the existing Messaging capability
binding. The local renewal preflight uses v2 for a typed activation time;
legacy v1 remains available.

The two independent query witnesses are the daemon's bounded process-epoch
acquisition counters and a loopback-only acceptance forwarder on each host.
Counters record closed role, reason and decision/HTTP stages, plus sent and
handled peer-renewal counts; they contain no grant, peer, endpoint or status
content. The read-only owner route also exposes the current P091 mode and
`resolution/id`, or explicit unavailability. The forwarders use one fixed
upstream on a synthetic authority and count each status request including 503.
The identical loopback endpoint is placed in both grants before signing; the
status signature provides integrity, while this profile makes no TLS or DNS
claim. A discrepancy between owner and network counts is a finding to resolve.

The profile uses the P074 physical harness for SSH control, revision pins,
leases, storage isolation, clock offsets and `federation-run.v1`. Each host
builds ordinary product processes from the same clean source revision via a
private Git bundle; no origin push is required. Mode windows are sequential
because P091 is node-scoped. Owner counter snapshots and `resolution/id`
bound each window to events; S020 stays active and its queries are classified
by reason. Signed short-profile fixtures age naturally. The gate includes
role reversal, receiver-side receipt, restart of each role, durable withdrawal
and signed status-revision rollback. It excludes directory rollback and power
loss. Source and evidence commits remain separate, and the tracker closes only
after the complete two-host gate and evidence-retention checks.

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
| P076-036 | Portable-proof follow-up | Bounded V2 status presentation | done | Clean Node 9b0a613e / Orbidocs 8523cf2b; 264 conformance/regression plus 12 host capsule tests, actual cold-cache WSS handoff with zero status fetches and identical loose/extracted qualification. Scoped gate only; primary global retention baseline blocker disclosed; no full-candidate or release claim |
| P076-037 | Product acquisition policy | Three live P091 modes, bounded peer renewal and S020 status refresh | done | Corrected local WSS host renewal, send preflight, typed no-query refusals, independent withdrawal retry and paused-scheduler diagnostics pass on clean commits; the same corrected binary passed the named second-host probe. No lease extension, cross-machine or offline delivery, full candidate or release claim |
| P076-038 | Physical qualification | Two-host V2 renewal, bounded time skew and independent query witnesses | in progress | Clean, identical revisions on two physical hosts; direct WSS, recipient receipt, mode matrix, restarts/revocation, two counter witnesses and retained P074 claim. No offline delivery or release claim |

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

P076-034 closes the local full mixed/provider candidate; P076-036 closes its
separate bounded status-presentation gate. Continue with the P076-037 acquisition
policy prerequisites, without extending the measured lease or privacy claims.
Track remote-withdrawal outbox behavior and the separate lifecycle suite's ambient
model-root isolation. Real email/SMS,
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
results. P076-036 remains planned; production root activation and release
readiness remain separate gates.
The earlier 54-action focus remains a report-contract refusal. This fresh
complete candidate does not retrospectively repair its reserved-field error
or promote any earlier refused attempt or focused diagnostic.

### P076-036 implementation gates

| Task | Gate | Status |
|---|---|---|
| P076-036-01 | Carrier/schema/policy contract, mirrors and boundary fixtures | done |
| P076-036-02 | Single source, explicit evaluation time and durable monotonic merge | done |
| P076-036-03 | Actual builder/peer/context plumbing and unsupported-consumer refusals | done |
| P076-036-04 | Source-pinned bounded host-path qualification and review | done |
| P076-036-05 | Retention equality, scoped documentation/ledger/MVP closeout | done |

### P076-036 measured closeout — 2026-10-24

The [retained Node capsule](https://github.com/diapod/node/blob/master/docs/evidence/limited-messaging/2026-10-24-portable-status/README.md)
pins clean Node `9b0a613e01a3f66748d306f7fa8b46963daf317a` / Orbidocs
`8523cf2b099643ac792e35a01f2367213d3ec05b` and eight unchanged Rust test
executables. Twelve suites pass 276 tests: 264 conformance/regression and 12 host
capsule tests. One is the actual two-daemon authenticated WSS handoff with cold
status cache, zero acquisition attempts and normal consent authorization within
the controlled signed lease; it refuses at expiry. Public root, complete carrier
and bounded correlation/counters are retained. Loose/extracted qualification is
identical. Eight separate active verifier tests (positive and refusal) pass.

Independent reviews closed typed signed-array normalization, writer-time expiry,
negative-knowledge capacity rollback in every acquisition path, unknown-grant
readmission, current root/custody cache, generic-dispatch and AD/reference/batch
consumer gaps, and qualifier temporal/inventory/correlation gaps. Failed dirty
development probes retain their failure classification and disclosed source
limits; the clean capsule passes on its first attempt.

The live repository-wide retention checker has an earlier Story-008 qualifier
header pin mismatch from Node `34d68537`, also present in the clean pre-retention
baseline. A data-only isolated control restoring the exact already-pinned
historical helper bytes passes all storage/frozen-tree checks including this
new run. The live helpers, policy, frozen evidence and pins are unchanged; the
primary-checkout blocker needs separate replica-policy reconciliation. This
limitation does not become a full-candidate or release claim.

This slice runs no browser, model, VM or full P076-034 candidate. It verifies
bounded handoff/consumption, not delivery or a new grant ceremony, and keeps
`full_candidate_qualified=false`, `release_ready=false`. Continue with the
separate P076-037 policy prerequisites; production periodic queries still occur.

### P076-036 review maintenance — 2026-10-24

The live global retention blocker is closed through the recorded-source qualifier
lookup, without changing any prior proof or pin. The follow-up implements the
owner-confirmed disclosure form and atomic bounded history, typed local capacity
unavailability, warning-level peer outcomes, metadata-only receipts and scoped
counters. It documents the fixed margin, matching-carrier deployment requirement
and shared V1 AD size limit. See
[the Node follow-up review](https://github.com/diapod/node/blob/master/docs/audits/REVIEW-P076-036-FOLLOWUPS-2026-10-24.md).

The separate `codex/self-contained-signatures` branch also retained a physical
`self.local`/`turbo.local` handoff at Node `5a01ee95` / Orbidocs `3f573420`.
Its [source-pinned report](https://github.com/diapod/node/blob/a265d334664e492859dea1932b2b9d4b46c8f451/docs/evidence/limited-messaging/2026-10-24-portable-status-two-host/README.md)
records zero issuance requests in the bounded handoff window. That run measured
the earlier V1 presentation carrier and its disclosure rule. It is historical
evidence of that implementation, not qualification of the closed V2 carrier or
the current owner-confirmed disclosure policy. The clean V2 capsule above remains
the current P076-036 acceptance source.

These changes have focused current-worktree regressions. The 276-test clean-source
capsule above retains its original source, executable and temporal scope; no new
browser/full candidate or release qualification is claimed. P076-037 was todo
at that capsule's source revision; its current scope is tracked above.
