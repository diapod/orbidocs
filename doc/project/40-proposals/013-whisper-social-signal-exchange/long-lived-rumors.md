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
  that the revealed public key matches the commitment in the `case/anchor`
  record, that this record verifies historically (`P013-LLR-002`), and that
  B's certificate is valid now. It also checks the scope, purpose, audience and
  `not-after`. The successor's signature counts only as proof of possession in
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

## Open Questions {#open-questions}

- Cross-epoch source equivalence without durable participant linkage remains
  deferred to LLR-005; a case succession is not its substitute.
- Availability/transfer of the case status authority beyond the single-authority
  v1 contract needs a separately reviewed design; outage currently defers.
- An independently authorized recovery/compromise process would change the trust
  model and is outside v1. No authority is invented when a key is lost.

## Long-Lived Rumor Tracker {#long-lived-rumor-tracker}

All rows remain planned or deferred. These gates qualify implementation; the
design and its review do not supply that evidence.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P013-LLR-000 | Controlled-clock twin acceptance | todo | P013-LLR-001–004, P013-LLR-006–008; P035-019; P041-001; P078-014; P015-004 | A rumor admitted at T with a receipt; after its certificate expires, redelivery at T + 1 year is accepted by a historical-mode relay and refused by a strict relay with `nym_certificate_expired`. A twin at T + 1 year is matched on the author's node, and the author reaffirms in the current epoch with a case-bound succession proof delivered only to the chosen audience. Succession signed by the expired nym key outside its grace window refuses. The old rumor is not counted toward the current threshold, and disclosure conditions are unaffected. |
| P013-LLR-001 | Four-period contract | todo | P015; P036-004 | Each period has a named field or policy and an owner; the consistency rules are fixed; an audit of existing contracts finds and corrects conflations, such as counting horizons longer than retention. |
| P013-LLR-002 | Historical verifier | todo | P035-019; P015 | One library for relays, custodians and counting authorities with separate historical-validity and current-status outputs. Golden vectors cover revocation before and after admission, skew and unknown time authorities. |
| P013-LLR-003 | Admission evidence in Memarium | todo | P035-019; P036 | Receipts are stored beside envelope bytes under the same retention; redelivery carries them beside, never inside, the signed bytes. |
| P013-LLR-004 | Re-contact for authored rumors | todo | P078-014; P013-DFR-004; P057-015; P013-LLR-007 | A notice when a new rumor matches an old authored one; a new related signal that is unlinked by default; an optional, warned `reaffirms` relation backed by a case-bound succession proof. |
| P013-LLR-005 | Long-horizon distinct-source counting | deferred | P013-ADC-004; cryptographic review | Case-scoped distinctness or continuity across epochs without a public stable identifier, with explicit consent duration. Candidates include a source-equivalence attestation by the issuer while both bindings are still retained, which would also allow exact author exclusion in later epochs. A proposal-grade review comes before any runtime work. |
| P013-LLR-006 | Case continuity key | todo | P015 v2 signal; S026 Pseudonym Vault | Single owner of the case key commitment, Phase 1 suite, lifetime and uses. Generate one key per case in the Vault; commit case/continuity-key-digest and case/status-authority in the first signed signal, independently of whether ADC is used. One key for amendments, confirmations and succession; bounded lifetime, deletion erasure fact and explicit opt-in recovery. Fixtures cover missing key, wrong commitment, deletion/recovery exclusion and independent cases. ADC-001 consumes this contract; no execution dependency points back to ADC. |
| P013-LLR-007 | Case-bound succession | todo | P015-004; P013-LLR-002; P013-LLR-006; P013-LLR-008 | Whisper use of `nym-succession.v2` with scope `case`: two signatures over one preimage, the commitment check, historical verification of the anchor, a current successor certificate used only as proof of possession, membership of the succession in the accepted case history and a fresh case status naming it as `case/current-succession`, private delivery to the declared audience, effects limited to `continue-case` with no source merging, closure handling, and refusal for each predecessor state in the table above. |
| P013-LLR-008 | Case state and currency | todo | P013-LLR-006; P013-PEX-001 | Case requests with `case/anchor` and `request/id`, and `whisper-case-acceptance.v1` assigning revision and previous digest; the `case/status-authority` commitment; a signed `whisper-case-status.v1` with head, state and `case/current-succession`; one durable transaction per acceptance that checks the head, evaluates the request, appends the event and stores the outcome by `request/id`; a durable high-water mark refusing rollback; `conflicted` only for contradictory accepted histories; a 300-second freshness bound that defers effects. Fixtures cover a missed withdrawal, competing requests that are not conflicts, a lost commit response followed by a withdrawal, rollback, an authority equivocation, a missing status, an amendment after a succession that leaves the successor authorized, a succession from B to C that ends B's authority, and a withdrawal racing a release commit on both orders. |
