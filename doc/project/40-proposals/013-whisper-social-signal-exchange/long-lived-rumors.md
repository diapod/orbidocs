# Long-Lived Rumors and Historical Authorship {#long-lived-rumors-and-historical-authorship}

Created: 2026-10-27. Revised: 2026-10-28.

Based on: [P013 domain map](../013-whisper-social-signal-exchange.md).

Status: proposed post-MVP clarification and feature; no runtime claim.

## Summary {#summary}

Nym certificates live at most 24 hours, yet a rumor may need to meet its twin a
year later. A short certificate need not mean a short-lived statement. The
design separates historical authorship, current admission, the counting window
and the author's consent. Certificates are not lengthened to make rumors live
longer.

## Context and Problem {#context-and-problem}

- **Fact.** P035 requires a currently valid `nym-authorship-proof.v1` at
  ingest. The proof is part of the signed canonical bytes, while
  `relay/received-at` is relay metadata outside the author's signature.
- **Fact.** P041 refuses `nym_certificate_expired`, and redelivery ships a
  byte-identical envelope that is evaluated against the current policy.
- **Fact.** This proposal stores the signed envelope byte-identically in
  Memarium with its lifecycle trace and privacy policy. No rule deletes it
  because its author's certificate expired.
- **Fact.** P015 keeps contributions after natural certificate expiry at the
  counting authority, and proves publication time with verified Matrix PDUs or
  an allowlisted relay's signed admission receipt.
- **Inference.** A gate that demands current validity refuses an old envelope,
  redelivery included. Replacing `author/nym-proof` would change the signed
  bytes and the `record/id`, so renewing the author's authority and preserving
  the original publication are separate operations.
- **Fact.** Story 014's 10-minute epochs and 2-minute certificates are fixture
  parameters, not production lifetimes, and that story tests a dormant fact
  followed by a rumor, not two rumors a year apart.

## Four Periods {#four-periods}

| Period | Question it answers | Owner |
|---|---|---|
| Nym certificate validity | May this nym perform a new operation now? | P015 |
| Retention of the rumor and its verification material | How long do we keep this historical statement and the means to check its origin? | Memarium (P036) and the local rumor store |
| Correlation and counting horizon | How far apart in time may reports be linked and counted toward one threshold? | This proposal (pull windows, disclosure-condition windows) |
| Consent validity | Does the author still permit disclosure, contact or association? | Conditions, interests and room consents |

No period is derived from another. A counting horizon may not exceed the
retention of the evidence it counts, and recognizing a link between two rumors
is not the same as counting them as two qualified sources in one epoch.

## Historical Admission Evidence {#historical-admission-evidence}

- **Receipt at first admission.** The admitting relay, or the counting
  authority for private carriage, issues an
  [`agora-admission-receipt.v1`](../035-agora-topic-addressed-record-relay.md#portable-admission-receipts-2026-10-27).
  It binds the record id, the author-byte digest, the nym certificate digest
  and issuing council, the verification outcome, the gate policy, the relay
  identity and the acceptance time, and the relay signs it as an explicitly
  admitted time authority. A verified Matrix PDU is an equivalent proof under
  P015. This generalizes the P015 publication-time evidence rather than adding
  a second format.
- **Storage.** Nodes keep receipts beside the envelope bytes in Memarium, under
  the same retention.
- **Historical verification.** "Was authorized then" means: verify the
  signature; verify the nym proof against the certificate validity window at
  the receipt's acceptance time, within five seconds of skew; verify that the
  receipt signer is an admitted time authority; and evaluate revocation by its
  effective time. The verifier returns two separate facts: historical validity
  and current status. Neither `authored/at` nor a bare `relay/received-at`
  suffices. RFC 3161 timestamping is a comparable general technique; it is not
  an Orbiplex feature.
- **Admission after expiry.** A gate may enable historical admission for
  archival or redelivery topics
  ([P041-001](../041-agora-ingest-attestation.md#historical-nym-admission-2026-10-27)).
  The default remains refusal.
- **No automatic recount.** Historical admission makes an old rumor verifiable
  and storable; it does not make it count again. Counting follows its own
  horizon.

## Meeting a Twin After a Year {#meeting-a-twin-after-a-year}

**Variant 1: re-contact (proposed default).**

- The author's own node treats its authored rumors as dormant records in
  dormant-fact matching ([P078-014](../078-weak-signal-harvester.md#implementation-tracker)).
  A new rumor that matches an old one produces a notice to the author.
- The author may author a new related signal under a fresh nym in the current
  epoch. By default it is not linked to the old record. An explicit `reaffirms`
  relation, which discloses an authorized continuation of the case, is a
  separate, warned choice backed by a
  [case-bound succession proof](#case-continuity-key-and-case-bound-succession)
  delivered only to the chosen audience.
- A third-party holder of the old rumor can reach its author only through a
  `contact/ref` the rumor carries; otherwise the match stays local.
- The cost is explicit: an unavailable author yields no current confirmation.

**Variant 2: cumulative long-horizon counting (deferred research).** Counting
across many epochs needs case-scoped distinctness or continuity that prevents
one person under successive nyms from counting as several sources, without a
public stable identifier. Candidates are issuer-retained case bindings for the
case horizon, which lengthen issuer retention, or rate-limited blind tokens per
participant and case. Consent must cover the whole horizon explicitly. This is
the same gap as the first open question of
[author disclosure conditions](author-disclosure-conditions.md#author-disclosure-conditions).

## Case Continuity Key and Case-Bound Succession {#case-continuity-key-and-case-bound-succession}

A later nym B may need to show that it continues a matter started by an earlier
nym A: to reaffirm the old rumor, to amend its disclosure condition, or to be
recognized as the authorized successor in this case. Signing with A's key a
year later would require
keeping A's private key that long. That contradicts the fresh key per
certificate and the erasure rules of P015, lets a seized device prove
authorship of old rumors, and turns the compromise of an expired key into a
takeover path.

The design anchors a case-scoped authority to continue in advance. The idea
comes from pre-rotation in KERI, where a controller commits to its next keys
and a sequenced key event log records each rotation (background:
[KERI specification](https://trustoverip.github.io/kswg-keri-specification/)).
Orbiplex takes a narrower pattern: one key committed at the start of a case
and then used repeatedly, without a rotation chain for that key and without a
key event log of its own. KERI's properties therefore do not carry over
automatically. Compromise of the old nym key alone cannot take over a case,
but compromise of the continuity key is critical and terminal for the case.
Case events get a small ordering contract instead
([case state](#case-state-and-currency)).

- **Case continuity key.** When the author publishes the first signal of a
  case, the Pseudonym Vault generates a fresh key pair for that case
  (Ed25519 in the explicitly closed Phase 1 suite),
  and the signal commits to it through `case/continuity-key-digest` inside the
  nym-signed bytes. The public key is revealed only when it is first used. The
  case is identified by the original record's digest. P013-LLR-006 owns this
  commitment independently of ADC; ADC consumes it. The first signal may bind
  at most one original embargo condition with the same status/counting authority.
- **One key per case.** The same key is the control key of an author
  disclosure condition: it signs amendments, withdrawal, release confirmations
  and succession. There is no second per-condition key.
- **Lifetime.** The key lives until `case/not-after`, which may not exceed the
  retention of the original record. The author may delete it earlier, which
  ends the ability to continue or amend the case; the deletion is recorded as
  an erasure fact. The key enters the recovery bundle only if the author opts
  in, trading survival against seizure risk.
- **Succession artifact.** Case-bound succession uses
  [`nym-succession.v2`](../015-nym-certificates-and-renewal-baseline.md#succession-after-expiry-and-the-narrow-successor-2026-10-27)
  (`P015-004`) with scope `case` and authorization mode `continuity-key`. The
  continuity key and nym B sign the same domain-separated bytes, which bind the
  purpose, the `case/anchor` record, B's current certificate, the audience and a
  short validity window.
- **Verification.** The verifier checks both signatures over one preimage,
  that the revealed public key matches the verified original `case/anchor`
  commitment, its historical admission (`P013-LLR-002`), and that B's certificate
  is valid now. The [portable profile](#portable-case-succession-verification)
  distinguishes a full-anchor check from reliance on an admitted detached proof.
  It also checks the case lifetime, scope, purpose, audience and `not-after`.
  The successor's signature counts only as proof of possession in
  this protocol ([signature uses](#signature-uses-and-certificate-scope)).
- **Authenticity versus authority.** These checks show that the succession
  document is authentic. Whether B is still the authorized successor is a
  separate question answered by the case status: the succession must belong
  to the accepted case history, and a fresh status of an active case must
  still name it as the effective succession. The authority's acceptance places
  the succession in the history, and later acts of B do not require it to
  remain the head. An ordinary amendment therefore leaves B authorized, while a
  later accepted succession from B to C ends B's authority.

Effects stay inside the case. `continue-case` lets B act for the matter, for
example by reaffirming it. Succession never carries reputation outside the
case, never renews a certificate, never adds a counted source and never merges
two sources. A counting authority that receives a succession proof keeps
counting `source/ref` values as before, because the proof establishes consent
of key holders, not that A and B belong to one participant. Succession also
does not stop a dishonest author from hiding continuity in order to count
twice. Both gaps belong to `P013-LLR-005`.

| Predecessor state | Treatment |
|---|---|
| Certificate expired, continuity key retained | Succession signed by the continuity key and B |
| Continuity key lost or deleted | No succession. The council keeps no participant mapping after its retention, so there is no recovery path; the author can only open a new, unlinked case |
| Nym key A compromised or revoked | A's key never authorizes case succession, and the separate continuity key is still required. A compromised continuity key is terminal for the case: the author closes it with that key if possible, and verifiers refuse succession after a closure |

The proof shows that the key holders consented to the transition, not that one
person holds both keys. Every recipient learns the link between A and B, and
the scope limits the permitted effects, not that knowledge. Case-bound
successions therefore travel only to their audience through the private
exchange path, and the author's editor names who will learn the link.

## Portable Case-Succession Verification {#portable-case-succession-verification}

**Proposed profile, 2026-10-28; post-MVP, P013-LLR-009.** Apply
[P032's shared verification contract](../032-key-delegation-passports.md#shared-verification-operations)
to Whisper's own evidence, alongside the other
[Whisper family profiles](../013-whisper-social-signal-exchange.md#portable-verification-profiles).
Reuse exact-evidence access, verification mechanics and acceptance laws.
P076 provides a qualified consumer example, not the common contract or a carrier
for Whisper. Its grant status and authority resolver cannot establish case
currency; P076-038 gains no Whisper scope. P015-004 remains the narrow pure MVP
verifier; this presentation and its host path belong to the LLR continuation.

The proposed closed `whisper-case-succession-presentation.v1` carries the
following roles. Each signed artifact keeps its existing schema, domain and
exact signed bytes; the carrier is not a new signature or a source of trust.

| Role | Minimum material and binding |
|---|---|
| `succession` | The exact `nym-succession.v2` with scope `case`, both signatures, the revealed continuity public key and the declared audience. |
| `proof/anchor` | One of the two anchor-proof variants below, binding `case/anchor`, the original continuity-key digest, `case/status-authority` and `case/not-after`. |
| `proof/certificates` | The original and successor nym certificates and the bounded public council/profile evidence their existing verifiers require. Expected roots and permitted profiles come from the receiver. Deduplicate identical evidence; a bare public key is not a certificate. |
| `proof/acceptance` | The authority-signed `whisper-case-acceptance.v1` for these exact succession bytes; together they identify the accepted succession event. |
| `proof/case-status` | A signed `whisper-case-status.v1` from the committed, locally admitted case authority, naming that event as the effective succession of an active case. |
| `proof/source-status` | The signed nym/source status evidence required by P015 for the successor's current use, and any historical evidence required by the anchor verifier. Source status and case status cannot replace one another. |

The **full-anchor** variant carries the complete original signed signal and its
P035 receipt or profile-permitted verified Matrix PDU. It is available only to
an audience authorized to see that signal. The **detached-manifest** variant,
for a case that already has ADC, carries its separately nym-signed
`whisper-embargo-manifest.v1` and P035's signed manifest/admission binding. That
receipt attests that the manifest's case key, authority and lifetime match the
private anchor. The verifier checks the manifest and the admitted receipt
signer; it does not claim to verify the unseen signal's signature independently.
The manifest contains no anchor id; the later receipt binds it to the anchor,
preserving the acyclic construction.

No embargo is required merely to have a case. A non-ADC case without an
authorized full anchor or exact retained local proof yields **missing anchor
evidence** for that receiver; v1 invents no detachable proof by deleting fields
from a signed signal. A reference to an unavailable private body is not a
self-contained presentation. Even the detached variant discloses case/nyms,
condition metadata and timing: the builder checks the declared audience and
disclosure policy for every included artifact before delivery. If the manifest
is unsuitable for that audience, report unavailable rather than exporting it.
Private keys, participant bindings and correlation text do not enter a public
proof package. Use PEX-001's protected delivery for audience-limited packages.

### Bounds and Representation

Initial v1 budgets to freeze and qualify in LLR-009: at most **65,536 encoded
carrier bytes**, **65,536 total unique decoded proof bytes**, **16 evidence
items**, **8 levels of JSON nesting**, and **32 signature checks** including
certificate/authority verification. Count nested and locally resolved evidence
toward the same budgets; deduplication must not multiply work. These are proposed
Whisper limits, not a consequence of P076's similarly sized carrier. Check size
and nesting before expensive parsing/cryptography, and preflight the work budget.
Oversize or unsupported evidence refuses explicitly, without truncating a
certificate, authority proof or signed status to make it fit. Fixtures must
demonstrate that the supported Phase 1 council profile fits these bounds.

Use role-specific closed fields and existing signed-artifact encodings. A small
evidence table may share an exact artifact between roles; its byte digest is
distinct from an Agora `record/id`. References resolve only inside the bounded
presentation or an explicitly supplied local exact-byte store. Reject cycles,
conflicting copies, wrong artifact families and unknown signing uses. No URL,
mutable `latest` reference, network discovery or attacker-selected fetch is part
of verification. Acquisition, when separately authorized, belongs to the existing
owner and must produce a new explicit verification input. A locally complete
view and a fully carried presentation have different evidence claims.

Preserve raw signed subdocuments when building and parsing; typed round-tripping
must not insert defaults, discard extensions or reorder signed arrays. Reuse
`canonical-json`, `nym-core`'s per-use byte checks, P035's publication-evidence
adapters and P015-004's two-signature verifier. Add only a Whisper presentation
adapter and a verified anchor-binding value recording which proof variant was
used; do not turn a detached receipt into `SignalBinding` for a body never seen.

### Verification Order and Results

The verifier receives the expected case, operation and audience, independently
admitted trust/profile inputs, explicit evaluation time and durable local
status knowledge. Then:

1. Bound and validate the presentation, resolve its exact local evidence and
   check all role bindings. Missing required material is `unresolved`; malformed,
   substituted or contradictory supplied material is `refused`. A valid cached
   alternative must not conceal bad evidence supplied in this presentation.
2. Verify the original anchor binding historically at its **admitted publication
   time**, using the appropriate full or detached P035/P015 adapter. A sender's
   timestamp does not establish that time. A carried root or authority cannot
   admit itself; today's certificate check cannot replace historical admission.
3. Verify the successor's current certificate/source status and call P015-004
   with the verified key commitment, case lifetime, audience and current time.
   The two signatures establish `AuthenticSuccession`, not continuing authority.
4. Verify the exact authority acceptance and fresh case status, including the
   same case/authority, active state, acceptance revision no later than the
   status head and `case/current-succession` equal to this accepted event.
   Compare against the receiver's retained head and negative knowledge before
   accepting any effect. A newer local closure, conflict or different successor
   cannot be replaced by an older attached `active` status.
5. Return separate historical-anchor, succession-authenticity and current-case
   results, bound to the evaluated evidence and time. The effect owner rechecks
   the applicable time/status fences at its admission boundary; a saved positive
   result is not a timeless permission.

Case freshness remains LLR-008's **300-second** bound, including its clock and
rollback rules. P015's source-status policy remains separate. Share only the
authenticated-head comparison described below: P076's union of revocation ids
is not a case-history merge algorithm. Do not synthesize a signed status from
several snapshots. Missing or stale currency defers current effects even when
historical authenticity is established. An offline result cannot detect an
unseen later revocation or an unreported key compromise.

For example, a package received at T can establish the old anchor's historical
authorship and B's current case authority. Rechecking it after the status exceeds
its freshness bound can still establish the historical result, but must defer
the current effect. If the receiver already knows of a newer closure, even a
still-fresh older `active` status cannot authorize B.

This current-succession check does not retroactively gate an ADC release already
committed by its authority. That receiver verifies the historical release commit
and its approved public proof package under ADC-005; it does not fetch a current
case status to undo the commit.

### Offline Acceptance

LLR-009 supplies a counting, network-denying resolver and an explicit local trust
snapshot. Both full-anchor and detached-manifest cases must verify with **zero
fetches**, with all positive proof bytes carried. In the detached case the
private signal is absent and its retrieval is denied. This qualifies a verifier
and its consumer adapter, not offline transport or unconditional authorization.

Negative fixtures cover missing anchor/receipt/certificate/acceptance/status;
changed continuity key or case lifetime; wrong case, audience, signer or profile;
unsupported signature use; expired successor; stale or future-dated status;
substituted succession bytes; unknown self-supplied root; known revocation;
newer local closure/successor; rollback/equivocation across restart; all resource
bounds; and privacy-forbidden evidence. Missing local-reference evidence stays
unresolved without a fetch. A valid cache plus an invalid carried artifact still
refuses. A refreshed status at the same accepted head must retain LLR-008's
non-equivocation behavior. Historical authorship can remain established while
current authority is deferred or refused.

## Case State and Currency {#case-state-and-currency}

Signatures verified offline prove authenticity, not that no newer withdrawal or
closure exists. Every act of the continuity key is therefore a case event in a
small ordered contract. This is not a full key event log.

- **Requests and accepted events.** The continuity key signs case requests:
  condition amendments and withdrawal, release confirmations, case closure and
  `case`-scope successions. Executors sign release commit and abandonment
  requests. Each request carries `case/anchor` (the original record digest) and
  a durable `request/id`, but no revision. The authority gives a request its
  place in the order by accepting it: its signed `whisper-case-acceptance.v1`
  binds the request digest, `case/revision` (a monotonic integer; the anchor is
  revision 0), `case/previous` (the digest of the previous accepted event, or
  of the anchor) and the evaluation inputs it used. An accepted event is the
  pair of request and acceptance. Only these header fields are shared across
  event kinds; each request keeps its own body and authority, following the
  reusable-data-abstraction rule of `node:DEV-GUIDELINES.md`.
- **One transaction per acceptance.** For each request the authority, in one
  durable transaction, checks the current head and state, evaluates the
  request against them (for a release commit it counts under a recorded source
  status revision and reserves the slot), appends the accepted event and
  records the outcome under `request/id`. The order of durable acceptance
  decides between competing requests, not the time of signing, a click or
  arrival.
- **Status authority.** The first signal of a case commits to
  `case/status-authority` beside the continuity-key digest. For a case with an
  author disclosure condition it must be the condition's counting authority,
  so counting and ordering happen in one place;
  otherwise the editor proposes the profile's projection authority, and the
  choice is always committed explicitly. The author node submits each event to
  it through the private exchange path. The authority serves a signed
  `whisper-case-status.v1` with the head revision and digest, the state
  (`active`, `closed` or `conflicted`), the effective succession as
  `case/current-succession` (the digest of its event, with the successor nym),
  if any, and the issue time.
- **Freshness.** An effect that depends on the case being current, such as an
  act of a successor or a reaffirmation, needs a case status no older than 300
  seconds, the same bound as P015 source status. A missing or stale status
  defers the effect and never implies that the case is active. A release does
  not rely on a fetched status: its commit is itself a case event that the
  authority orders against withdrawal.
- **Competing requests are not conflicts.** When requests race, the
  authority accepts one and evaluates the next against the changed state; it
  then accepts it at the following revision or refuses it. A withdrawal
  accepted after a commit is a valid, later event.
- **Lost responses.** An outcome is durable and readable by `request/id`.
  Resubmitting the same request id returns that stored outcome without
  re-evaluation, so an executor whose commit response was lost recovers the
  same accepted commit, even if a withdrawal was accepted after it. Reusing an
  id with different request bytes refuses as an idempotency conflict. A new
  `request/id` is a new request.
- **Conflicts.** `conflicted` means contradictory accepted histories: two
  acceptances by the authority with the same revision but different events, or
  a status that rolls back below a durable high-water mark. Relying parties
  that hold such evidence refuse both histories and treat the authority as
  faulty. The state is terminal for the case.
- **One current successor.** The effective succession is the latest accepted
  succession event. Other case events, such as amendments, confirmations or
  release commits, never change it, and a later accepted succession replaces
  it. v1 supports no co-successors.
- **Disclosure.** The status authority learns the timing of case events and the
  successor nym, so it necessarily belongs to the audience of every succession.

## Signature Uses and Certificate Scope {#signature-uses-and-certificate-scope}

The contextual certificate restricts nym publications to its exact topic key,
record kind `whisper-signal` and schema `whisper-signal.v2` (P015). The
artifacts of this proposal must not widen that scope implicitly. Each signature
has one declared use:

| Signature | Signer | Use | Requirement |
|---|---|---|---|
| Protected or related `whisper-signal.v2` | Nym | Publication | The existing contextual scope |
| Commitments inside a signal: signed manifest digest, `case/continuity-key-digest`, `case/status-authority` | Nym, as part of the signal | Part of that publication | The existing scope; no separate signature |
| Release manifest | Nym | Domain-separated auxiliary authorization of the original condition and release payload | Explicit P015-005 manifest-use profile; never interchangeable with a publication signature |
| Release payload | None | Authenticated by the digest committed in the signed manifest | None |
| Correlation notice | Nym | A publication of its own kind | Exact bound kind/schema/topic/disclosure-scope tuple admitted by P015-005 |
| Successor acceptance in `nym-succession.v2` | Successor nym | Proof of possession in a domain-separated auxiliary protocol | A currently valid certificate, checked only by the succession verifier; never accepted by a publication verifier |
| Case events | Continuity key | Case control | None beyond the anchor commitment |
| Disclosure attestations and case status | Counting or status authority | Authority claims | Admission of that authority |
| Release record | Releasing node | The release act | Node identity |
| Cover request | None | Authenticated by the peer session | None |

## Invariants {#invariants}

1. Succession proves authorization by key holders, never identity of sources;
   it changes neither source counts nor reputation outside the case.
2. Historical validity, current authority, retention and consent have separate
   inputs. Offline authenticity cannot assert that a case is still active.
3. No missing/deleted continuity key triggers council recovery or silent key
   substitution. Recovery inclusion is an explicit, separately warned opt-in.
4. One case has one anchor, one committed status authority and at most one
   original embargo condition. Requests have one ordering owner and a durable
   outcome; contradictory accepted histories fail closed.
5. Continuity-key compromise is terminal for that case. Without an independent
   recovery authority, a holder of the compromised key cannot prove which user
   is legitimate; closure requires reaching the status authority. An offline
   verifier cannot detect an unreported compromise.
6. Two semantic authorizations remain distinct from the Phase 1 Ed25519 suite.
   P081's suite-neutral adapter does not silently upgrade this wire format.
7. Portable proof cannot bootstrap trust, replace case currency with Messaging
   grant status, or disclose a private anchor to obtain self-containment.

## Trade-offs {#trade-offs}

- A case key allows continuation after nym expiry but retains takeover power
  longer. Separate custody and opt-in recovery trade availability against seizure.
- A status authority simplifies atomic ordering but is an availability and
  trust dependency. Its outage defers current effects; historical verification
  can still work from retained proof.
- Recipients learn a case's nym linkage. Scope limits use, not knowledge; no
  public chain or participant identity should be inferred from it.
- Receipts and keys cost retention. Erasure can make a later historical check
  impossible; the result is missing evidence, not invalidity or fresh authority.
- A bounded presentation reduces lookups but duplicates some evidence and can
  expire in transit. Detached proof adds reliance on the admitted receipt signer;
  an unavailable safe proof is preferable to revealing the private anchor.

## Failure Modes and Mitigations {#failure-modes-and-mitigations}

| Failure | Effect | Mitigation / qualifying task |
|---|---|---|
| Lost/deleted key | Continuation unavailable | Explicit refusal, no hidden recovery; new unlinked case (LLR-006) |
| Compromised continuity key | Case takeover risk | Terminal closure when possible; no automatic successor recovery; show limitation (LLR-006/008) |
| Missing/stale authority status | Current authorization unknown | Defer effects; do not reinterpret historical proof as permission (LLR-008) |
| Contradictory accepted histories or rollback | Authority untrustworthy | Retained high-water mark and conflict refusal (LLR-008) |
| Receipts purged before retained bytes | Authorship cannot be rechecked | Co-retain verification bundle and bytes; diagnose incomplete evidence (LLR-003) |
| Lost response or restart | Duplicate/re-decided event | Durable request digest/outcome; reject id reuse with changed bytes (LLR-008) |
| Succession sent to wrong audience | Unwanted nym linkage | Recipient-bound AD/INAC; no public fallback (PEX-001/LLR-007) |
| Incomplete/oversize presentation or forbidden anchor disclosure | No safe portable verification | Typed unresolved/refused result; no silent fetch, truncation or trust import (LLR-009) |

## Open Questions {#open-questions}

- Cross-epoch source equivalence without durable participant linkage remains
  deferred to LLR-005; a case succession is not its substitute.
- Availability/transfer of the case status authority beyond the single-authority
  v1 contract needs a separately reviewed design; outage currently defers.
- An independently authorized recovery/compromise process would change the trust
  model and is outside v1. No authority is invented when a key is lost.

## Implementation Recommendations {#implementation-recommendations}

Use the [shared-mechanism dispositions](../013-whisper-social-signal-exchange.md#implementation-reuse).
One pure case fold and one transactional case owner serve every operation below;
do not add separate current-state stores for succession and embargo. Suggested
internal values retain the existing wire contracts:

```text
CaseHead = (case_anchor, authority, revision, accepted_event_digest)
CaseRequest = { case_anchor, request_id, body: typed operation }
AcceptedCaseEvent = (request, acceptance)
StoredOutcome = (case_anchor, request_id, request_digest, exact_result)
```

The closed operation variants are amendment, withdrawal, confirmation, closure,
succession, release commit and abandonment. Their signatures and preconditions
stay operation-specific. `fold_case_event(state, accepted_event)` checks the
chain and derives the next immutable state without I/O. In particular, an
amendment does not replace the current successor and a withdrawal does not free
an already committed release slot. A corrupt or incomplete chain is unavailable,
never a newly active empty case.

The acceptance owner first authenticates the caller and exact request binding.
Within its durable acceptance boundary it retrieves any saved outcome, refuses
changed bytes under the same `(case_anchor, request_id)`, or checks the current
head and evaluates the new operation with explicit current time and evidence.
It appends the accepted event, advances the projection, reserves any release
slot and records the outcome together. A duplicate returns its stored result;
it is not evaluated against today's state. Serialize competing requests or use
an expected-head CAS; after a conflict, re-evaluate against the new head.
Unauthenticated traffic must not reserve ids or read private saved outcomes.

Reuse S028 facts/projections and the recovery laws demonstrated by
`node:nym-issuer-service/src/revision_store.rs`, without importing its
issuer-specific database/key-provider coupling. Keep signing, media probes and
network calls outside SQL write transactions. Prepared signatures/results may
be exposed only after their exact input/head checks and durable acceptance;
a failed CAS discards the candidate, not an already accepted event. LLR-008 owns
fixtures for this seam, including a crash before result exposure.

Extract only the shared head comparison from `nym-core::StatusCursor` when
implementing the case cursor: a verified scope plus revision and identity digest
compares as initial, unchanged, advanced, rollback, equivocation or wrong scope.
Scope includes the artifact family and admitted authority as well as the domain's
context/epoch or case anchor; equal numeric revisions across scopes are unrelated.
The **identity digest differs by domain**: source status uses its signed payload;
case status compares the accepted-history head. Refreshing a case status's issue
time without changing that head is not equivocation. Each adapter separately
checks its timestamp, authority and semantic claims. P015 keeps cumulative
revocations; LLR keeps chain validity and terminal conflict behavior. Persist
the accepted high-water mark with the decision that relies on it; a pure
comparison alone does not protect a restored database.

LLR-002 must return historical admission and current eligibility as separate
results, using the P035/P015 publication-evidence port. Do not call the existing
live `Certificate::admit` with an old clock value to simulate historical
verification. LLR-007 calls P015-004's pure succession verifier, then checks
accepted membership and fresh case currency; it does not implement another
two-signature verifier. Shared law fixtures cover wrong scope, same head with a
refreshed status, rollback, same revision/different accepted head and restart;
domain fixtures retain missed withdrawal, conflicting history and key loss.

## Long-Lived Rumor Tracker {#long-lived-rumor-tracker}

All rows remain planned or deferred. These gates qualify implementation; the
design and its review do not supply that evidence.

LLR-009 includes P032's common verification-law fixtures and a convergence
review with ADC-005's evidence-access/accounting path. Share the mechanisms
when their contracts match, or retain a concrete reason for separation. Do not
make either proof-package consumer wait for the other's runtime merely to
extract a generic library; the later implementation owns that comparison.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P013-LLR-000 | Controlled-clock twin acceptance | todo | P013-LLR-001–004, P013-LLR-006–009; P035-019; P041-001; P078-014; P015-004 | A rumor admitted at T with a receipt; after its certificate expires, redelivery at T + 1 year is accepted by a historical-mode relay and refused by a strict relay with `nym_certificate_expired`. A twin at T + 1 year is matched on the author's node, and the author reaffirms in the current epoch with a case-bound succession proof delivered only to the chosen audience. Its LLR-009 presentation verifies with no proof fetch and keeps authenticity separate from current authority. Succession signed by the expired nym key outside its grace window refuses. The old rumor is not counted toward the current threshold, and disclosure conditions are unaffected. |
| P013-LLR-001 | Four-period contract | todo | P015; P036-004 | Each period has a named field or policy and an owner; the consistency rules are fixed; an audit of existing contracts finds and corrects conflations, such as counting horizons longer than retention. |
| P013-LLR-002 | Historical verifier | todo | P035-019; P015 | One library for relays, custodians and counting authorities with separate historical-validity and current-status outputs. Golden vectors cover revocation before and after admission, skew and unknown time authorities. Reuse P035's publication-evidence adapters and binding-law fixtures; a local admission row is not a signed proof. |
| P013-LLR-003 | Admission evidence in Memarium | todo | P035-019; P036 | Receipts are stored beside envelope bytes under the same retention; redelivery carries them beside, never inside, the signed bytes. |
| P013-LLR-004 | Re-contact for authored rumors | todo | P078-014; P013-DFR-004; P057-015; P013-LLR-007 | A notice when a new rumor matches an old authored one; a new related signal that is unlinked by default; an optional, warned `reaffirms` relation backed by a case-bound succession proof. |
| P013-LLR-005 | Long-horizon distinct-source counting | deferred | P013-ADC-004; cryptographic review | Case-scoped distinctness or continuity across epochs without a public stable identifier, with explicit consent duration. Candidates include a source-equivalence attestation by the issuer while both bindings are still retained, which would also allow exact author exclusion in later epochs. A proposal-grade review comes before any runtime work. |
| P013-LLR-006 | Case continuity key | todo | P015 v2 signal; S026 Pseudonym Vault | Single owner of the case key commitment, Phase 1 suite, lifetime and uses. Generate one key per case in the Vault; commit case/continuity-key-digest and case/status-authority in the first signed signal, independently of whether ADC is used. One key for amendments, confirmations and succession; bounded lifetime, deletion erasure fact and explicit opt-in recovery. Fixtures cover missing key, wrong commitment, deletion/recovery exclusion and independent cases. ADC-001 consumes this contract; no execution dependency points back to ADC. |
| P013-LLR-007 | Case-bound succession | todo | P015-004; P013-LLR-002; P013-LLR-006; P013-LLR-008 | Whisper use of `nym-succession.v2` with scope `case`: two signatures over one preimage, the commitment check, historical verification of the anchor, a current successor certificate used only as proof of possession, membership of the succession in the accepted case history and a fresh case status naming it as `case/current-succession`, private delivery to the declared audience, effects limited to `continue-case` with no source merging, closure handling, and refusal for each predecessor state in the table above. Call the P015-004 verifier; do not duplicate its cryptographic or mode/scope logic. |
| P013-LLR-008 | Case state and currency | todo | P013-LLR-006; P013-PEX-001 | Case requests with `case/anchor` and `request/id`, and `whisper-case-acceptance.v1` assigning revision and previous digest; the `case/status-authority` commitment; a signed `whisper-case-status.v1` with head, state and `case/current-succession`; one durable transaction per acceptance that checks the head, evaluates the request, appends the event and stores the outcome by `request/id`; a durable high-water mark refusing rollback; `conflicted` only for contradictory accepted histories; a 300-second freshness bound that defers effects. Fixtures cover a missed withdrawal, competing requests that are not conflicts, a lost commit response followed by a withdrawal, rollback, an authority equivocation, a missing status, an amendment after a succession that leaves the successor authorized, a succession from B to C that ends B's authority, and a withdrawal racing a release commit on both orders. One fold/store serves all typed case operations. Share only authenticated-head comparison with P015; test refreshed case-status timestamps at an unchanged history head, source-status regression parity and crashes before signed result exposure. |
| P013-LLR-009 | Bounded portable succession verification | todo | P013-LLR-002; P013-LLR-006–008; P013-ADC-001; P015-004; P035-019 | Freeze `whisper-case-succession-presentation.v1` and qualify the [portable profile](#portable-case-succession-verification): exact signed subdocuments, both authorized anchor-proof variants, certificate/source evidence, accepted succession and current case status; explicit size/item/depth/work bounds and typed missing-proof refusal to authorize. Reuse P015-004, P035 adapters and LLR-008's case cursor. Retain zero-fetch evidence for full and detached variants with independent local trust; all negative/privacy/cache-conflict/restart cases listed above pass. No protected-body fetch, generic certificate carrier, source merge, or P076-038/MVP scope expansion. |
