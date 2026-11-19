# Author Disclosure Conditions {#author-disclosure-conditions}

Created: 2026-10-27. Revised: 2026-10-28.

Based on: [P013 domain map](../013-whisper-social-signal-exchange.md).

Status: proposed post-MVP feature; no runtime claim. This section owns the
feature and its tracker. The acceptance scenario is the
[author disclosure condition variant of Story 014](../../30-stories/story-014-dormant-contest-entry.md#variant-author-disclosure-condition).

## Summary {#summary}

An author may make wider disclosure of a rumor conditional: "do not show this
content beyond the correlators and counting authority I chose until at least N other qualified sources
report the same matter". The condition is part of the author's consent. It is
bound by a separately nym-signed release manifest and referenced by the protected
rumor. It binds every admitted holder; it is not a hint to a server.

Four separations carry the design:

1. **Same matter is a context.** Reports count together only when they share a
   `topic/class` and a `signal/similarity-key` derived by a versioned grouping
   rule from a correlation descriptor that the author approved. The counter
   compares identifiers; it does not interpret meaning.
2. **Sources, not copies.** Counting uses P015 contextual sources per epoch.
   Copies, forwards and republications by one source count once.
3. **Release is verifiable.** A release publishes a payload that was redacted
   for the release audience when the rumor was authored. It requires a release
   commit accepted by the admitted counting authority, which orders it against
   withdrawal and counts sources at that point, and, by default, the author's
   final confirmation.
4. **Disclosure is not coordination.** The disclosure condition answers "when
   may this content be shown?". The coordination threshold of section 5
   answers "when should joint action be proposed?". The two never imply each
   other.

## Context and Problem {#context-and-problem}

- **Fact.** Section 5 defines a coordination threshold that leads to an
  association-room proposal, and section 6 an explicit consent gate. Neither
  lets an author define when content may reach wider audiences.
- **Fact.** [Whisper implementation Layer 7](../../60-solutions/011-whisper/011-whisper-impl.md#layer-7-threshold-detection-and-durable-promotion) resolved that `whisper-durable.v1` carries aggregates
  and a content-addressed reference, and that text redacted under one scope is
  never re-published under another.
- **Fact.** P015 counts council-admitted participant sources per context and
  epoch. `source/ref` is derived per participant, context and epoch, so
  distinctness is defined only within one epoch, and contributions stop
  counting after revocation or epoch end.
- **Inference.** A number alone is not a condition. Without an exact criterion
  of which reports count together, a node could reach the threshold by
  widening the matter. If a semantic similarity score could move a report into
  a group, it would change when a consent executes, not only how well search
  works.

## Roles and Payloads {#roles-and-payloads}

| Role | Holds before release | May | Must not |
|---|---|---|---|
| Author node | Protected signal, release payload, control key (the case continuity key) | Narrow or withdraw the condition, confirm or decline a release | — |
| Correlator (custodian) | Correlation payload; the release payload only in held custody | Match locally, propose context joins, pass the descriptor to the counting authority | Disclose protected material outside the correlation scope |
| Counting authority | Protected signal and condition; signals of the context | Count sources, attest, and order case events including release commits, as the case status authority | Count anything other than the condition's context, or accept a commit out of order |
| Recipient | Released record | Verify the release offline | Treat the count as evidence of truth |

The material is split into two payloads and an independently verifiable manifest:

- **Correlation payload.** The protected v2 signal with `disclosure/scope =
  private-correlation`, the correlation descriptor and the manifest digest.
  Authorized holders are exactly the author-named correlators **union** the
  named counting authority, including when these are different nodes. Each
  holder has a role-specific use, delivery grant and retention obligation.
  Hop/forwarding budgets bound transport; they never grant recipient authority.
- **Release payload.** `whisper-release-payload.v1`, redacted through Story 005
  for the declared release audience at authoring. It has no signature of its
  own; its digest is committed in the manifest. Custody is `withheld` (author
  node) or `held-under-obligation` (a named custodian). This honours S011's
  prohibition on reusing text under a different disclosure scope.
- **Release manifest.** `whisper-embargo-manifest.v1` carries the original
  `whisper-embargo-condition.v1`, the release-payload digest, the case continuity
  public-key commitment, `case/not-after`, the counting/status authority and the
  approved public metadata policy (count/proof required, rendered criterion
  optional). A nym signature covers its domain-separated canonical bytes.
  Its auxiliary signing use must be explicitly permitted by
  the P015-005 profile; possession of a nym key alone does not permit it.

The manifest is created first. It includes neither the protected signal's body
nor its record id: the signal then commits the signed manifest's digest, and
P035-019's detached admission receipt binds the digest of the exact **signed**
author bytes and the manifest digest after verifying the complete private
publication. The private `record/id` excludes the signature and is forbidden in
the public receipt, URLs, logs, metric labels and traces: it would allow a
dictionary to confirm guessed low-entropy content.
There is no reverse manifest-to-signal hash dependency and no field-stripping
from a signed Agora envelope. The receiver can verify the author's manifest
and the authority's claim about admission without seeing the protected body;
it cannot independently verify that hidden body's signature or semantics.
The construction order is acyclic:

```mermaid
flowchart LR
    Payload[Release payload] --> Manifest[Nym-signed manifest]
    Manifest --> Signal[Protected signal]
    Manifest --> Admission[Admission receipt]
    Signal --> Admission
    Manifest --> Intent[Immutable release intent]
    Admission --> Intent
    Intent --> Commit[Authority commit receipt]
    Intent --> Envelope[Final release envelope]
    Commit --> Envelope
    Envelope --> AD[AD hand-over]
```

Arrows mean "must exist before constructing", not permission to disclose. The
protected signal is absent from the recipient package. The final envelope does
not influence the commit receipt's preimage.

The public form of the condition must itself be safe for the consented audience:
private facets stay in the correlation payload, with only authorized opaque
commitments and a redacted criterion in the manifest. A plain hash of a
low-entropy private descriptor is not confidentiality; it must not be exported
as a supposed redaction. ADC-001 must freeze the bounded public proof fields
and their privacy review before runtime work.

The control key is the
[case continuity key](long-lived-rumors.md#case-continuity-key-and-case-bound-succession), owned by
P013-LLR-006 and stored by S026. One fresh key per case signs amendments,
withdrawal, confirmations and case-bound succession. The anchor and manifest
must commit the same key, authority and case lifetime. P035-019's admission
profile verifies that equality before attesting the binding; a receipt over
two digests alone must not imply that an unchecked case binding was verified.
The manifest and that receipt can then serve as the detached anchor proof in
[LLR's portable succession profile](long-lived-rumors.md#portable-case-succession-verification),
when their disclosure is permitted to that audience. This reuses existing ADC
material; it neither requires an embargo for every case nor exposes the private
signal. The key does not identify the participant;
its uses can link actions inside the case. All such actions follow the
[case state](long-lived-rumors.md#case-state-and-currency) contract.

In v1 one case anchor has **zero or one original embargo condition**. If present,
the anchor binds it at creation and its counting authority is the case status
authority. Narrowing amendments keep the original condition digest and its
release slots. A wider condition needs a new protected anchor and a new case,
with new consent and no automatic public link; it neither withdraws the old
condition nor inherits its permissions. Adding an embargo to a previously
unconditioned case likewise requires a new anchor. The editor shows both cases
and offers a separate withdrawal of the old one.

## Same Matter: Descriptor, Grouping Rule and Key {#same-matter-descriptor-grouping-rule-and-key}

The author approves a `whisper-correlation-descriptor.v1`: a grouping rule
plus typed, normalized fields, rendered as a sentence the author can judge.
An illustrative descriptor, not a frozen field list:

| Field | Value |
|---|---|
| Grouping rule | `contest-assessment/v1` |
| Organizer | Organizer O, identified by its website domain |
| Event | Contest K, identified by its canonical page URL |
| Edition | `2026` |
| Issue kind | `assessment-integrity-doubt` |
| Rendering | "Doubts about how entries were assessed in the 2026 edition of contest K organized by O." |

Grouping rules live in the decorrelation vocabulary document beside its terms
([P013-DFR-001](../013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27)) and reach nodes the same
way: a factory JSON source with local P091 layers. Each rule has an id, a
version, applicable terms, a closed field list with admissible identifier types
(domain, canonical URL, registry id, normalized text, closed enums), the
canonicalization and a rendering template. A local rule produces keys that
other nodes do not derive, and the UI says so.

The similarity key is the domain-separated digest of the normalized
descriptor:

```text
signal/similarity-key = "gk1:" || base64url(sha256(JCS([
  "orbiplex.whisper.grouping.v1", rule-id, rule-version, normalized-fields
])))
```

Changing a rule's normalization or field set requires a new version. The
condition binds the rule id, version and digest, so no node can substitute a
broader rule.

Breadth is the author's decision. `contest/v1` counts any report about the
contest; `contest-assessment/v1` counts only doubts about assessment, and
excludes, for example, payout or form problems. The key is the outcome of
agreeing on meaning, not a mechanism that discovers it: two different
descriptors remain different after hashing.

## Ambiguous Reports: Proposals, Not Merges {#ambiguous-reports-proposals-not-merges}

People describe one event differently: an official name, a colloquial name, or
no name at all. Correlators may look for such candidates, and a model may help,
but its output is a proposal:

1. When the condition's join policy is `keyed-and-confirmed-joins`, a
   correlator may send a content-free `whisper-context-join-proposal.v1` to the
   candidate's author through that signal's reply path. It shows only the
   rendered target descriptor, never other rumors.
2. The candidate's author accepts by authoring a related signal in the target
   context (P013-DFR-004). The keyed counting rule then counts it.

No node merges contexts on its own, and no similarity score opens an embargo.
Under the default join policy `keyed-only`, only reports that derive the same
key count.

## Counting Rule {#counting-rule}

For each epoch `e` of the window, the counting authority computes the number of
distinct `source/ref` values among admitted signals that:

- carry the condition's context digest and were admitted in epoch `e`;
- had certificates valid at their authenticated publication time (P015);
- belong to sources that are not revoked under a status no older than
  300 seconds.

Copies, forwards and republications of one source count once. Counts of
different epochs are never summed.

- **N means other sources.** In the protected signal's epoch, the author's
  `source/ref` is known from the protected signal's certificate and is
  excluded exactly; the requirement is N. In each later epoch of the window the
  author's source cannot be excluded reliably, so the requirement is N + 1
  **even if the author never publishes in that epoch**. This conservative rule
  can therefore require one extra genuinely other source. The UI shows both N
  and this effective threshold. Succession does not change the counter: it
  proves consent of key holders, not participant-source equivalence. A possible
  handover of the case is a separate reason not to infer that equivalence from
  succession, not the reason for the N + 1 bound. Exact exclusion would need a
  source-equivalence attestation from the issuer, which remains open
  (`P013-LLR-005`).
- **Window.** `count/window-epochs` whole epochs starting with the protected
  signal's epoch. The proposed bound is 13 epochs, about 91 days under the
  production seven-day profile.
- **Limitation.** Reports that trickle in across epochs do not satisfy the
  condition unless one epoch alone reaches the requirement. Longer counting
  needs a longer-epoch profile (the issuer then retains bindings longer) or a
  cryptographic cross-epoch linkage.
- **Meaning.** Distinct sources are a consent trigger. They do not show that
  the reports are true.

## Attestation and Verification {#attestation-and-verification}

The condition names exactly one counting authority in v1: the projection
authority that federation policy admits for the contextual profile and context
(the P015 role C). Committees with quorum proofs may follow, as section 5
already anticipates.

`whisper-embargo-attestation.v1` is a private threshold proposal from the
pinned authority to an authenticated eligible executor. It binds the case,
original commitment, exact single-audience manifest, release ID, executor,
effective mode, epoch and counting basis (`author-epoch-exact` or
`later-epoch-conservative`). It carries `threshold-met`, the finite signed
observation window, effective release deadline and an opaque trigger tied to the complete
admitted membership. The owner retains exact counts, status revisions and
inventory evidence separately from the proposal and public commit statement.

Verification has two entry paths sharing the same bounded verifier library:

1. A protected holder verifies the complete signal, nym signature, contextual
   certificate and publication/admission proof, including the signal-to-manifest
   binding. A recipient instead verifies the separately signed manifest, its
   explicit P015 scope and the admitted authority's receipt binding it to the
   protected publication. No retrieval of the protected signal is required.
2. Both verify the original condition, key commitment and any accepted narrowing
   amendments needed to establish consent at the commit point. Requests and
   acceptances included in the public package use closed, content-free bodies;
   private status/contact data cannot be smuggled into this proof chain.
3. The triggering attestation binds the condition/context, authority and an epoch
   inside the window. It may prompt the author while no older than
   `attestation/max-age-seconds` (proposed at most 900), but never authorizes
   publication alone.
4. In confirm mode, the accepted author's confirmation binds the exact audience,
   original condition and triggering attestation and was unexpired at commit.
5. The signed commit receipt binds the immutable release-intent digest, logical
   release id, canonical audience digest, executor, hand-over deadline, commit
   revision, observed count and source-status revision. It attests that consent
   and the count passed at that point.
6. The intent's payload matches the manifest commitment; its audience is an
   explicitly consented descriptor, no wider than the current condition. The
   final Agora envelope verifies normally, including its content-addressed id.

Recipients need no current case status to verify an already committed release.
This proves a historical authorization at commit, not current authority or the
truth of the rumors. Missing required proof prevents successful verification rather
than fetching private text as a fallback. Certificates and proof references must
be supplied inline or in the authorized offline package within declared limits.

Freshness and consent are measured at one named point, the commit point: the
case authority's acceptance of the release commit. The authority counts at that
moment under a source status no older than 300 seconds, so the source basis of
a release is at most 300 seconds old at its commit point, not counting the
five-second skew tolerance of P015. A revocation that has not yet reached that
status may not stop the release, and the acceptance claims are bounded
accordingly. The bound concerns the commit point only. When the bytes later
reach AD the basis may be older; the hand-over deadline limits that gap without
a recount, and a withdrawal accepted after the commit does not cancel the
committed release.

The ADC counter parses the verified issuer's RFC 3339 times as instants
without reformatting the status. The signed status digest continues to anchor
the inventory pin. The fixed-width time format applies to the locally
persisted evaluation.

Evidence that recipients can re-verify without trusting the counting authority
remains to be designed in `P013-ADC-004`.

## Release {#release}

The case authority commits one logical act of disclosure. Artifact Delivery
carries out its delivery and never decides domain consent/counts again. The
commit is not an INAC capability: AD still enforces its recipient, transport
authority, expiry and budget contracts. A delivery refusal neither cancels the
accepted commit nor frees its slot.

- **Modes.** `confirm` is the default. The author node retrieves the
  attestation by condition id through the private exchange path it used to
  submit the protected signal, so the authority stores no route to the author.
  The author sees a prompt and signs `whisper-embargo-confirmation.v1` with
  the control key, or declines. The confirmation is a case event that binds
  the condition, the audience, the triggering attestation and a short
  `confirmation/not-after`. In `pre-authorized` mode there is no prompt: the
  condition itself authorizes commits until `release/not-after`, and the author
  is notified afterwards.
- **Commit point.** The executor, which is the releasing party, prepares the
  immutable `whisper-embargo-release-intent.v1` and submits a
  `whisper-release-commit.v1` request with a fresh
  `request/id` to the case authority. For a case with a disclosure condition
  that authority must be the counting authority. The request binds:
  - the release-intent digest, covering the exact payload and recipient proof
    package prepared so far, **excluding** the future commit receipt and final
    Agora envelope/signature;
  - the canonical audience descriptor and its digest, not only its class;
  - the executor's identity and frozen delivery route;
  - `commit/hand-over-by`, a short deadline for the first hand-over to AD
    (proposed at most 15 minutes and never after `release/not-after`).

  The authority accepts the request in one durable transaction only if the
  case and condition are active, no earlier commit holds the slot for
  `(original condition digest, canonical audience descriptor digest)`, the
  confirmation is accepted and unexpired (in confirm mode), neither the counting
  window nor `release/not-after` has ended, and its own count under a source
  status no older than 300 seconds meets the requirement. Its acceptance is the
  commit receipt. Refusal never reactivates a withdrawn or expired condition.
  A retryable refusal leaves an otherwise active condition active; confirm mode
  needs a new confirmation for a later triggering attestation.
- **Withdrawal versus release.** The order of durable acceptance by the case
  authority decides. A withdrawal accepted before a commit refuses that
  commit. A withdrawal accepted after a commit does not cancel the committed
  release for its audience, even while its bytes have not yet been handed to
  AD; otherwise consent would have to be checked again between commit and
  hand-over. It ends every other and every later release. A withdrawal takes
  effect when the authority accepts it, not when it is signed, and the author's
  editor shows that point.
- **Record.** `whisper-embargo-release.v1` contains the immutable intent and
  commit receipt, with the releasing node's normal Agora signature. The receipt
  commits the intent, not the final receipt-bearing envelope, avoiding a hash
  cycle. Its `release/id` is a domain-separated digest of the original condition
  digest and canonical audience digest; it is distinct from Agora's
  content-addressed `record/id`. The executor freezes and journals the final
  envelope bytes before the first AD submission and reuses them on every retry.
  All final-envelope metadata except the receipt is fixed in the intent; its
  construction from the stored intent and receipt is deterministic in Phase 1.
  A crash before journal completion cannot choose a fresh timestamp/nonce or
  different payload when recovering that envelope.
- **Audiences.** Closed classes are `association-room` (P070),
  `federation-scoped` and `cross-federation`. The canonical descriptor names the
  concrete room plus consented history-access policy revision, or exact
  federation/topic/access scope. It excludes delivery routes. Two routes to the
  same room consume one slot; two rooms have separate slots **only if consent
  permits both descriptors**. Executor and route are frozen separately in the
  intent. Membership alone cannot widen the audience or historical access.
  Agora audiences require registering the record kind and content schema.
- **Releasing party.** The author node in withheld custody, the custodian in
  held custody. A counting authority that is also the custodian concentrates
  trust; confirm mode keeps the author's final word.
- **Irreversibility.** A release cannot be recalled. Revocations after a
  release change the current annotation, as P015 does for first emissions, but
  not the released record.

The executor journals each execution phase, including the intent and the
deterministic AD delivery id before submission, as P035-001 requires. Recovery
after a crash depends on the phase reached:

| Phase | Recovery |
|---|---|
| Commit requested, outcome unknown | Read the outcome by `request/id` or resubmit the same request. An accepted commit is recovered unchanged, even if a withdrawal was accepted after it; the authority neither counts again nor reserves a second slot. A refused request may be followed by a new request with a new id |
| Commit accepted | Hand the committed bytes to AD with the frozen delivery id before `commit/hand-over-by`, without a new domain-consent/count decision or different bytes; ordinary AD admission still applies. If the deadline passes and AD confirms that no submission exists, request `release-abandoned`; the slot stays consumed, and a later disclosure to that audience needs a new condition |
| Released for delivery, outcome unknown | Keep the bytes and the delivery id, and reconcile the same operation through AD status and readback as in P035-001; never prepare an alternative publication |
| Delivery confirmed | Retries only repeat the same, already executed operation |

Release for delivery is the moment from which AD may start sending on its own,
that is, AD's durable acceptance of the submission. It is a conservative
boundary of control over the disclosure, not proof that any recipient has read
the content. Execution therefore keeps three states: commit accepted, released
for delivery and delivery confirmed. The local journal is
`transactional-withheld`; the commit is `irreversible-external` toward the case
authority, because it fixes consent and the release slot; release for delivery
is `irreversible-external` toward the audience. A recipient that sees two
different intents or final envelopes for one logical `release/id` treats them as
equivocation: it keeps the first
and flags the conflict. Under the one-slot rule this indicates a faulty or
malicious executor.

The closed release surface is the approved pre-redacted payload, the explicitly
approved criterion/count metadata and the minimal verification package described
above. Participant identity, private facets, source lists, original attachments and
contact routes are excluded. Proof metadata can still link a nym or case, so the
editor previews that disclosure too. Every additional field needs explicit
consent and a contract-level privacy review; an evidence digest is not a license
to publish its private preimage.

## Amendments and Withdrawal {#amendments-and-withdrawal}

`whisper-embargo-amendment.v1` is signed with the control key and can only
narrow the condition: raise N, shorten the window, narrow the audience, switch
`pre-authorized` to `confirm`, or withdraw. A wider condition requires a new
condition on a new anchor and a new case under the one-anchor rule above.
It does not implicitly withdraw the old condition. Amendments and withdrawal are case
requests, and the case authority's acceptance gives them their place in the
order ([case state](long-lived-rumors.md#case-state-and-currency)). A withdrawal takes effect when
the authority durably accepts it and is ordered against release commits as
described under Release; it erases unused held payload copies. Already committed
execution bytes remain subject to their bounded journal/AD recovery obligations.

The private ADC proposal exchange can carry an owner-signed
`adc-withdrawn` result in the
`orbiplex.whisper.case.unused-custody-withdrawal.v1` domain. The owner emits
this proof only for a named held executor and a release with no committed
slot, after durable withdrawal. The exact signed request binds the case,
release, executor and reply key. The recipient journals the verified result
with the selected held transfer digest before retiring its key and
ciphertext. Committed slots and ordinary refusal diagnostics are separate
from this proof. This path requires a current request by the holder.

For a holder without a current request, the owner can sign a separate
`whisper-held-custody-withdrawal.v1` with the same durable withdrawal and
unused-slot preconditions. This private statement binds one named holder,
release, selected manifest, original case authority and horizon. On
admission the custodian fences exactly that scope. A verified later
statement can retire the bound key and ciphertext without opening the
payload. The original receipt keeps its deadline. Prior AD handoff and
foreign or absent local custody refuse.

The optional one-way withdrawal uses the `held-custody-withdrawal` PEX
family and a short offer signed by the named custodian. Separate local
adoptions bind the sending case authority, the receiving custodian and the
private direct route. The authority's fenced owner retains only the exact
encrypted frame for replay through the offer lease and its exchange binding
through the case horizon. The owner's existing bounded cleanup retires the
encrypted frame's storage references. AD owns retry. The receiver requires the authenticated
sender to match the signature and checks the stored scope and exchange
time before erasure. Beyond the offer lease, a fresh exchange consumes a
new offer. The original custody and case deadlines continue to bound
offline copies and their receipts.

## Custody Obligations {#custody-obligations}

Every protected holder, including a separate counting authority, advertises the
custody profile `whisper-embargo-custody:v1`. The author selects all protected
holders from that admitted set.

The counting authority signs its adopted custody profile and absolute
deadline as `adc/custody` in `whisper-case-authority-policy.v1`. Publication
uses the existing restricted case-control signing operation. The publication
lease is bounded by the custody deadline. The author uses the existing
independent P091 authority, policy-digest and source-profile pins before
checking that custody covers the reviewed case. The owner checks its own
adopted deadline on fresh registration. Exact committed replies retain
their original leases.

For held custody the author supplies exact, sender-bound
`whisper-pex-key-offer.v1` advertisements for `whisper-embargo-custody-transfer.v1`
in the private `case.disclosure` input. `custody/offers` is keyed by the public
keys in `custody.holder/keys`. The source independently pins each selected
`{holder/id, offer/digest}` in the P091 `whisper/case-authorities` setting.
Holder pins and counting-authority pins are independently typed. Each offer
must be current at selection and before the first signature and its advertised
obligation must cover the case deadline. The advertisements remain private.
Selection reserves no PEX exchange or custody at the remote holder. A later
transfer independently checks its own current offer, route and recipient policy.
Both SQLite development paths passed with this gate. The held actor supplies an
advertisement signed by its synthetic holder identity before source authoring.

A custodian:

- labels protected material through `classification.v1`, so the existing
  egress guards refuse it;
- never includes it in Agora records, topic or subject query responses,
  aggregate notices, holder availability beacons, redistribution offers, room
  frames, notification previews, exports, logs or remote model egress;
- uses it only for its admitted role: correlators match and propose joins; the
  counting authority admits and counts. AD/INAC checks the named holder set as
  well as transport budgets, including a separate correlator/authority fixture;
- erases unused custody copies at release, withdrawal, expiry or
  `release/not-after`. Bytes already committed for execution are retained only
  until bounded hand-over/reconciliation completes; they cannot feed a new slot.

These are policy obligations backed by audit, not cryptography.

Agora public record carriers refuse recognizable private custody objects,
including source and audience manifests, private attestations, custody
transfers, executable material and private ADC controls. The carrier checks
declared content schema, nested documents in the content object, and complete
JSON in its text fields. The author and delegation verifiers own their signed
scope declarations. Open extensions in threshold notices and other public
records therefore cannot carry a recognized private document. Matrix keeps
the source event identity and refusal code for checkpointing and omits the
carrier bytes, author bytes and private record identifier. A queued Matrix
publication with private custody content ends in a permanent refusal before
contacting a room.

The dedicated release carrier permits the audience manifest discriminator in
the exact `proof/package → audience/manifest` slot of the declared release
contract. Signing tuples in that proof retain their schema declarations.
Copies elsewhere and private documents inside the manifest still cause
refusal. The publisher and receiver independently verify the release
receipt, proof and audience before public admission.

Room uses the same private schema discriminators for live sends, projections
and relay payloads. A private Room `content/type` or recognizable private
document in a JSON object carried by `content` returns
`private-custody-carrier-required` before
advancing the live or relay sequence. The sealed profile applies the check
where plaintext is available, before sealing and after authenticated opening.
The check identifies structured custody documents. Opaque and unlabelled
copies remain subject to the holder's egress obligation above.

Artifact Delivery refuses recognizable custody plaintext at outbound plan
preparation and again before the adapter effect, including on recovery. The
same schema checks cover inline and resolved reference bodies, including
nested objects and complete JSON in text fields. The reserved ADC release
preserves the same exact audience manifest slot as Agora. Existing
protected-signal and held-custody exchanges carry
inline opaque PEX bytes on an adopted direct `minimal-trace-v1` INAC route.
That carriage leaves the holder, recipient and proof checks with their owners.

Application backup selection cannot read the separate held provider by release
identity. A recognized private ADC document in an ordinary Memarium entry or
fact also returns `private-custody-carrier-required` before serialization into
the backup. This includes private retained backups. The operation reveals no
protected content in the refusal.

Model HTTP adapters check the final provider body after binding and mapping.
Recognized private ADC documents, including serialized JSON text parts, return
`private-custody-carrier-required` before egress observation or dispatch to a
remote or loopback endpoint. The host applies the same check to the effective
middleware invocation body and to merged subprocess input before spawn. These
ports do not admit custody holders. The holder's obligation still applies to
material without a recognizable schema.

Notification creation refuses recognizable custody documents before computing
request and body digests, reserving idempotency or writing the queue or audit.
This covers previews that contain a complete serialized JSON document and
structured request fields such as action input. The create and legacy emit
routes return `private-custody-carrier-required`.

The P086 broker refuses live observations with a private custody schema or
recognizable inline custody content before applying capture interest, and
refuses such context snapshots before interning them. Middleware reports
reject this content before projection can retain a digest. Channel and host
capability observations use their private metadata projection before
measurement. The channel checks the encoded JSON body of its typed HTTP
carriers and protects replies scoped to a recognized private request.

The held-release handover carries one selected audience inside a separate
private `whisper-embargo-custody-transfer.v1` exchange. The signed private
registration acceptance contains the keys named in both the original holder
list and executor list for `held-under-obligation`. The source verifies the
original selection and independently authorizes the intended peer. The
holder's private key offer signs its `whisper-embargo-custody:v1` profile and
its custody horizon. The source checks that horizon against the retained case
before sealing the transfer. The short exchange lease continues to bound
the offered key and ciphertext. The recipient rechecks the signed and
locally adopted obligations against the verified case before writing the
copy. These offer fields carry the holder's obligation without case, audience
or source material.

The recipient verifies its owned node, the authority signature and the selected
manifest under local witness trust. The complete original and its opening
stay with the source. The acceptance and its holder projection stay outside
the public release.

Component verification covers the handover material and its binding to the
named holder and audience. The receiving host still needs to establish the
local custody obligation under the adopted storage and egress policy before
the executor can use the material.

## Coordination Independence {#coordination-independence}

- Disclosure conditions and coordination thresholds have separate state and
  separate artifacts. `coordination/participation` defaults to `excluded`: a
  protected signal then feeds no public threshold or proposal record. With
  `allowed`, a room proposal can form while the content stays embargoed for
  wider audiences, as in the Story 014 variant.
- A room is a release audience only when the condition names it. Room
  membership alone grants nothing.
- The author can always disclose their own material by a new, explicit act.
  The condition binds custodians and automation, not the author.

## Optional Public Notice {#optional-public-notice}

With `descriptor/visibility = public-notice`, the author node publishes a
content-free `whisper-correlation-notice.v1`, signed by the author's nym, in
the vocabulary bucket of its `topic/class`. A notice is a publication of its
own kind, so P015-005 must authorize its exact publication tuple explicitly
([signature uses](long-lived-rumors.md#signature-uses-and-certificate-scope)). It carries the rendered descriptor,
the grouping rule, the similarity key, N and an expiry. Dormant-fact readers
can then find the matter, and their authors can join by keyed derivation. The
notice has a public `record/id`. Related authoring targets that id with
`target/kind = whisper-correlation-notice`, never the hidden signal id. Matching
uses the grouping key; no public reverse pointer to the protected signal is
required or synthesized. The notice is itself a disclosure that the matter exists, and the author's editor
says so. The default is `correlators-only`.

## Confidentiality from Correlators {#confidentiality-from-correlators}

In the basic variant a correlator can read what it holds and is obliged not to
disclose it. Withheld custody keeps the release payload at the author node
until release, but needs that node at release time. A variant in which no node
can read the protected material before N sources exist, for example threshold
or escrow-style encryption, is a separate cryptographic mechanism
(`P013-ADC-009`). Disclosure policy alone cannot provide it.

## Condition, Proposal and Execution States {#condition-proposal-and-execution-states}

These are three different projections, not one persistent case enum. The
condition is `active`, `withdrawn` or `expired`; the case status additionally
handles closure/conflict under LLR. `satisfied` is a **derived, temporary
attestation predicate**, not a stored `whisper-case-status.v1` state or a reserved
slot. A declined proposal ends only that prompt. The condition stays active,
but the same proposal is durably suppressed across restart; another prompt
requires an explicit author retry or a consented re-prompt policy with a new
attestation and a bounded cooldown. Without that policy, no automatic re-prompt.

The diagram shows the proposal evaluation and one audience's execution. Before
commit, withdrawal or expiry applies from every waiting state, also in
pre-authorized mode. After commit, condition changes do not undo that slot.

```mermaid
stateDiagram-v2
    [*] --> active
    active --> satisfied: usable attestation (derived predicate)
    satisfied --> awaiting_confirmation: confirm mode
    satisfied --> committed: pre-authorized and authority accepts
    satisfied --> active: stale attestation or retryable refusal
    satisfied --> withdrawn: withdrawal accepted before commit
    satisfied --> expired: counting window or release deadline ends
    awaiting_confirmation --> committed: valid confirmation and authority accepts
    awaiting_confirmation --> active: stale confirmation or retryable refusal
    awaiting_confirmation --> declined: decline this proposal
    declined --> active: prompt suppressed; condition still active
    active --> withdrawn: withdrawal accepted
    active --> expired: counting window or release deadline ends
    awaiting_confirmation --> withdrawn: withdrawal accepted before commit
    awaiting_confirmation --> expired: counting window or release deadline ends
    committed --> released_for_delivery: AD accepts frozen bytes by hand-over deadline
    released_for_delivery --> delivery_confirmed: delivery confirmed
    committed --> abandoned: deadline passed and AD proves no submission
```

## Invariants {#invariants}

1. Before release, protected material leaves the author node only toward the
   named correlators and the counting authority.
2. No correlator discloses protected material through any surface listed under
   custody obligations.
3. Group membership follows the context digest only. No semantic score
   changes it.
4. One source counts once per epoch; epochs are never summed.
5. A release requires a commit accepted by the case authority, which counts
   at the commit point, and, in confirm mode, the author's confirmation. AD
   carries out the delivery of a committed release and never decides consent
   again.
6. A release exposes only the pre-redacted payload, approved criterion/count
   metadata and minimal public verification package to its consented audience;
   neither correlation text nor private facets/source lists/contact routes leak.
7. Amendments only narrow.
8. Disclosure conditions and coordination thresholds are independent.
9. Release records state that distinct sources are not evidence of truth.

## Trade-offs {#trade-offs}

- Per-epoch counting is exact and unlinkable, but misses reports that trickle
  in over several epochs. Later epochs require N + 1 even without the author;
  this deliberately trades recall for not accidentally counting the author.
- Confirm mode preserves the author's agency, but an absent author blocks the
  release. Pre-authorized mode releases in the author's absence, but trusts
  custodians and the authority more.
- Withheld custody exposes less, but needs the author node at release.
- A single counting authority is a trust concentration. Evidence commitments,
  confirm mode and later committees reduce it.
- Keyed-only counting avoids false merges, but reaches N more slowly than
  confirmed joins.
- A public notice speeds discovery, but reveals that the matter exists.

## Failure Modes and Mitigations {#failure-modes-and-mitigations}

| Failure | Effect | Mitigation |
|---|---|---|
| A correlator leaks protected material | Disclosure without consent | Custody profile, classification guards, audit; withheld custody; sealed variant later |
| A node widens the matter to reach N | Early release | Rule id, version and digest bound in the condition; joins need the candidate author's act |
| One source republishes or is forwarded | Inflated count | Distinct `source/ref` per epoch |
| The author republishes in a later epoch | Self-triggered release | N + 1 outside the author's epoch |
| Coordinated fake sources | Release triggered by a group | Council admission of sources (P015), an author-chosen N, confirm mode |
| The authority attests a false count | Release on a false basis | Evidence commitment and entries for the author and custodian; confirm mode; committees later |
| Release on an outdated count | Release after revocations | The authority counts at the commit point under a source status no older than 300 seconds; the residual staleness is stated |
| Withdrawal and release race | Release against current consent | The order of durable acceptance by the case authority decides; a later withdrawal does not cancel a committed release |
| Competing valid requests | A valid case frozen as conflicted | Requests are ordered by durable acceptance; only contradictory accepted histories are conflicts |
| The author is unreachable | Release blocked | Expiry; pre-authorized mode as an explicit choice |
| Crash, lost response or retry during release | A second, stale or re-decided publication | One commit slot per original condition and canonical audience digest; outcomes stored by `request/id`; recovery by phase: the same commit after a lost response, the same bytes and delivery id after the commit, reconciliation after release for delivery |
| A protected signal feeds a public threshold | The matter is exposed | `coordination/participation` defaults to `excluded` |

## Open Questions {#open-questions}

1. Multi-epoch accumulation: a longer-epoch profile with longer issuer
   retention, or a cryptographic cross-epoch linkage.
2. Evidence that recipients can re-verify without trusting the counting
   authority, and committee attestation.
3. Defaults and bounds: maximum N, window length, attestation age and the
   pre-authorized horizon.
4. Bounded size and custody of the public verification package. In this v1
   design the signed attestation/count and its fixed-size evidence commitment
   are required public proof; evidence entries remain private. A count-hiding
   proof would be a different, separately reviewed profile.
5. How a confirm-mode author stays reachable without exposing a route to the
   counting authority, beyond pulling over the private exchange path.

## Implementation Recommendations {#implementation-recommendations}

Follow the [shared-mechanism dispositions](../013-whisper-social-signal-exchange.md#implementation-reuse).
The following are internal value shapes, not new wire schemas or completed APIs:

```text
ContextEpoch = (profile_digest, issuer, context_digest, epoch)
Contribution = (context_epoch, source_ref, record_id,
                certificate_digest, admission_proof_digest)
CountBasis = (context_epoch, source_status_revision, source_status_digest,
              evaluated_at, eligible_sources, evidence_commitment)
ReleaseSlot = (original_condition_digest, canonical_audience_digest)
PreparedRelease = (release_id, intent_digest, commit_receipt_digest,
                   envelope_bytes, envelope_digest, delivery_id, hand_over_by)
```

Keep `eligible_sources` and its evidence private. One bounded map from
`source_ref` to eligible contributions serves both contextual coordination and
disclosure counting, within one `ContextEpoch`. Never count map entries from
different epochs or issuers together. Evaluate admission evidence and the P015
current-source rules before deduplicating; repeated copies add no source, and
natural certificate expiry does not erase a contribution admitted while valid.
If one source has several eligible records, choose a deterministic representative
for its evidence entry by canonical record-id ordering, without discarding the
other retained evidence. A revoked or otherwise ineligible record cannot replace
an eligible representative. Rebuild and incremental updates must agree.

`evaluate_epoch_sources` yields either a complete, revision-bound basis over its
pinned locally admitted view or an explicit unavailable/incomplete result, never
a guessed zero. Completeness here does not claim knowledge of all reports in the
federation. Coordination uses
its own participation filter and emission latch. `evaluate_disclosure_condition`
uses the same source evaluator over the condition's admitted holder view, then
excludes the exact author source in the original epoch, or compares the full
later-epoch set against checked `N + 1`. The count supplies no publication right.
The authority re-evaluates it at release commit under the same source-status
revision fence as eligibility; the triggering attestation is not a cached permit.

Use two typed proof inputs: `FullPrivateAnchor` and `DetachedManifestAdmission`.
They have different trust claims and meet only after their own signature, scope
and binding checks. The shared tail checks the condition, accepted narrowing,
confirmation if required, intent, commit receipt, audience and payload binding.
The public path consumes only the bounded offline proof package and never calls
a private-body loader. P035 owns the receipt carrier and verification adapter;
ADC adds its manifest-binding profile rather than a second receipt format.

Release execution uses the [LLR case owner](long-lived-rumors.md#implementation-recommendations):
one acceptance reserves `ReleaseSlot` and binds the evaluated source basis and
intent. The executor then freezes the final envelope and its delivery identity
before AD hand-over. Recovery reads the saved phase: recover an unknown commit
outcome by request id, finish the committed envelope once, or resubmit the saved
bytes to AD. It never recounts to replace an accepted commit or reuses its slot.
No cryptography, key-provider call or network I/O belongs inside the SQL write
transaction; signature preparation and result exposure must preserve the atomic
acceptance boundary and be covered by crash fixtures.

ADC-004/005 must exercise duplicate/forwarded records, representative replacement,
source revocation, natural certificate expiry, missing status, both epoch bases,
two consented rooms, one room over two routes, and commit/withdrawal in both
orders. A permutation/replay fixture must produce the same eligible-source set
and evidence commitment from the same admitted inputs. Historical M4 counting
and ids stay unchanged.

The local ADC-004 component now exercises all six admission orders for three
contributions on the same witnessed original. Two contributions from one source
count once. Exact replay preserves the eligible evidence commitment, trigger and
count. This covers the SQLite admission and evaluator path. ADC-004 remains todo.

The local ADC-005 owner check now commits two independently confirmed
audiences with the real detached original and counter. A competing signed
intent for a second route of the first audience cannot allocate another slot.
The original reply still replays after the other audience commits and the
owner reopens. Native Agora delivery is measured separately.

## Lean Release Model Before Durable ADC Enablement {#lean-release-model}

**Model gate qualified, 2026-11-16; ADC-005 remains `todo`.** LLR-011 now has
an implemented [owner component](long-lived-rumors.md#long-lived-rumor-tracker)
with separately qualified source-pinned offline owner tests. The
[Node report](https://github.com/diapod/node/blob/master/docs/audits/P013-ADC-011-LEAN-RELEASE-2026-11-16.md)
pins 73 checked theorems, 35 executable vectors, 4,096 generated model steps and
18 existing Rust case-law tests. It uses the reviewed
[S027-009-06 discipline](../../60-solutions/027-messaging-middleware/027-messaging-middleware.md#lean-delivery-pilot)
while preserving separate domain laws. The subsequent LLR-011 gate qualifies
its implemented owner-decision subset and fenced writes; complete executor/AD
composition, comparison and submission/readback remain ADC-005.

ADC-001/004's freeze for this model covers current authority/count/confirmation,
canonical audience and exact request/head/intent identities, permitted narrowing
and half-open deadlines. It does not close their schemas or runtime rows.
The model's request capacity of 64 is a finite proof/test profile. Its capacity
law covers retained results plus one reserve per committed audience, and the
full-budget vector exercises settlement. Historical qualifications, alpha
scope and public readiness are unchanged.

### Model and implementation boundary

Reuse the existing `whisper-core::case` transitions and `ReleaseOrder` as
implementation references, and the LLR-008 owner/outcome store as the target
integration seam. Model the full relevant composition, not only the two release
flags: accepted head, original condition and permitted narrowing, confirmation,
per-audience slots, immutable intents, exact request outcomes and the phase of
AD hand-over. `satisfied` remains derived; condition, prompt and execution are
separate state axes. Time, current source basis and authenticated commands are
explicit inputs. No new wire schema, store, authority or delivery loop is implied.

The model must distinguish durable acceptance, lost reply, recovery and an
unknown AD outcome. Define atomic acceptance and exact retained outcomes as
explicit owner obligations, not claims that Lean has verified SQLite or the
network. Counts consume ADC-004's scope-bound eligible-source contract; they
do not prove source independence, truth or cryptographic security. Keep finite
capacity, deadline and revision refusals visible. Persisted negative knowledge
and terminal states cannot be replaced with an empty active case on recovery.

### Required claims and acceptance

| Claim | Required proof or witness |
|---|---|
| Consent is checked at acceptance | A fresh commit requires the currently applicable condition, count basis, authority, audience and timely confirmation when required. An earlier `satisfied` observation alone is insufficient. |
| Withdrawal has one order | Accepted withdrawal before a fresh commit prevents that commit. Withdrawal after a commit preserves that exact accepted slot/outcome while preventing new releases. Both orders have reachable witnesses, including a lost commit reply. |
| Narrowing cannot widen consent | Accepted amendments shrink the set of permitted fresh releases while preserving original condition identity and accepted slots. Raising N, shortening windows, narrowing audiences and switching to confirm are covered. |
| Slots belong to concrete audiences | At most one intent is accepted per original-condition/canonical-audience pair. Two routes to one room share a slot; distinct consented rooms can have distinct slots; an unconsented room refuses. |
| Recovery preserves identity | Matching request replay returns the same outcome without recounting or a second reservation; changed bytes under that request key refuse. Restart/response loss cannot choose another payload, envelope or delivery identity. |
| Handoff cannot manufacture a second disclosure | A first hand-over requires a committed exact intent within its deadline and ordinary AD admission. Unknown outcome is not absence. Abandonment requires the specified evidence and leaves the slot consumed; retries preserve the accepted delivery identity. |
| Unrelated control does not replace the successor | Amendment, withdrawal and release operations preserve the current successor; terminal/conflicted case state never silently returns to active. |

P013-ADC-011 closes on checked claims over reachable histories, executable
positive/refusal witnesses, explicit assumptions and a source/symbol/fixture map
using the S027 pilot discipline. Cover confirm and pre-authorized modes, expiry
between attestation and acceptance, both commit/withdrawal orders, two rooms/two
routes, changed request bytes, lost responses and restart before AD hand-over.
Use concrete counterexamples or distinguishing executable traces for removed
audience, withdrawal and replay guards; proof-search failure alone is inconclusive.
Do not force noncommuting operations into permutation-invariant laws.

Reuse existing Rust vectors for already implemented shared laws. Comparison
with new Rust was outside this original model gate. LLR-011 subsequently
qualified its fresh owner-decision subset and real fenced writes; ADC-005
execution/handoff comparison remains open. Their acceptance must compare the pinned model and Rust
on bounded generated traces and inject crashes at the actual owner boundaries:
before/after acceptance, before reply exposure and around AD submission/readback.
All effect authorization and privacy gates remain in force. Neither proof of the
model nor matching vectors qualify signature checks, storage atomicity, real
delivery, metadata non-disclosure or social independence.

Freeze ADC-001/004 preconditions with this model before enabling durable control
operations. LLR-011 then implements owner transitions; ADC-005 composes release
execution and closes only after that owner integration. The formal gate depends
on contract freezes, not completion of those downstream runtime tasks. This
avoids an ADC-005/LLR-011 implementation cycle. S027-009-06 is a prior method
review, not a new authority dependency. If the pilot cannot establish a useful
bounded method, record a scoped decision before changing this sequence; never
silently waive a proof gate or expand it to the whole protocol.

## ADC-005 accepted continuation (2026-11-17) {#adc-execution-continuation}

Accepted design; implementation is in progress and ADC-005 remains `todo`.
This continuation supersedes the earlier recipient-manifest, public commit
receipt, AD delivery-id and abandonment descriptions where they conflict. The
dated ADC-011/LLR-011 qualifications remain evidence for their pinned contracts,
not qualification of these revised semantics.

### Private origin, audience proof and public commit

The private manifest M retains all original audiences. Each audience A gets a
separate author-signed M_A containing only its exact P070 descriptor, condition
projection, admitted executors, continuity key, fixed counting authority and case
horizon. M contains a secret random 256-bit nonce; its domain-separated hiding
commitment C_M is the common original identity. Registration verifies a bijection
between M's audience set and the prepared M_A set. S026 freezes all or none; the
protected signal does not distribute M_A to every correlator.

One approved release payload has one separately salted commitment C_P, common to
all audiences of this condition. The author or admitted custodian retains its
opening until release. Different payloads require a new case. The public package
opens C_P but not C_M. It carries neither other audiences nor their count,
dictionary-testable aliases, private source identifiers or protected body.

The public intent binds C_M, C_P, M_A, the audience, executor, handover deadline,
safe package digest and public envelope metadata. A hiding commitment binds the
private execution descriptor (component, idempotency key, route and exact plan).
`Intent.proof` must not be an ordinary digest of low-entropy count facts. Release
identity is H(release-domain, C_M, canonical-audience-descriptor), independent of
route and distinct from the final content-addressed Agora record id.

ADC-004 owns a separate public commit statement and signer domain. It binds the
public intent and effective audience restrictions, reports satisfied and its
time, and carries no case/source revision, exact observed count, private
Acceptance or input digest. Private outcome and exact public bytes commit
together; no candidate signature is disclosed before fence completion. The
recipient verifies author consent for A directly, trusting the admitted counter
for count, freshness, ordering and effective narrowing. Full history is not a
portable completeness proof. Cross-room correlation through C_M and timing is
an explicit residual disclosure.

M_A's counting authority equals the registered authority and commit signer for
the complete case. A different configured signer is dependency loss, not a new
domain decision. Ordinary key retirement must honor the case hold. Loss of the
key prevents new signed decisions; it does not revoke historical commitments.
Author/nym succession does not change this authority. Authority rotation or
delegation is a separate proposal, outside ADC-005. Offline receivers cannot
discover omitted revocations and assume uncompromised pinned-key custody.

### Time, settlement and owner resources

Freeze 60 s minimum handoff, 60 s reply margin, 900 s settlement window, 5 s
preparation budget and three stale cycles in the admitted case policy. Registration
requires request TTL 125..900 s and release_end + 900 <= case/not-after. The
executor selects min(request/not-after - 60, release_end); the prepared reply
must survive handoverBy + 60. Static shortage is Never; a shorter available
transport/preparer lease is dependency unavailability. Recheck owner time after
guard acquisition. The core still requires now < handoverBy: the 60 s host
policy only narrows admitted commits. Neither value guarantees delivery.

Each accepted commit reserves one further command result and finite physical
resources for that slot's accepted abandonment, independently of ordinary quota
and the first-withdrawal reserve. Bad claims cannot consume that reserve.
The executor separately reserves its final-envelope and settlement journal space.

The source fence is a non-writing BEGIN IMMEDIATE guard implemented by the relay
schema owner. Acquire within 250 ms, reread time, validate the exact pin and
deadlines, commit the case through its final fence, then release. Pin scope is
the admitted local index even for Synapse; ingestion delay consumes the signed
300 s freshness budget. A pin includes installation/file identity, scope,
revision, its transactionally assigned generation and status digest. Replacing
the file requires readmission. Restoring an older snapshot in place and
revisiting a revision through different writes requires a fresh evaluation.
No source acquisition, signing or sealing runs under this guard.
If the case owner panics under the guard, it lets the unwind stop before
dropping the relay reservation. It marks the case store as requiring verified
reopen and resumes the panic. The relay remains usable when its rollback and
busy-handler restoration succeed.

EvaluationStale is a transport deferral, not a case result. Durably invalidate
the undisclosed candidate before reevaluating identical bytes. A bounded record
retains request id/digest conflict binding and stale count across restart until
request expiry plus replay margin. Stale cycles charge a separate per-case
window with the same configured interval and bound as the operation window.
Fresh request IDs share that stale budget. Exhaustion defers release-commit
evaluation and leaves author controls and slot settlement available. The
per-request counter still stops after the third stale cycle. Neither counter
charges max_commands_per_case or changes a committed result.

### Executor and accountable abandonment

`whisper-case-service::executor::ReleaseExecutor` owns the local commit journal,
using the existing fenced Store in role adc-executor and projections keyed by
adc-execution:release-id. Prepared bytes use existing case object/event/blob
mechanics and protected custody, not a second authority or transport retry loop.
Owner slots become Committed or Abandoned; unknown, released, delivered and
tombstoned are executor observations. Terminal executor outcomes include commit
rejected, commit-outcome-lost and unresolved-at-closure. If the exact response
lease is lost, do not mint another reply or guess the slot receipt.

A durable release-commit refusal carries the case owner's private signature
over the exact `whisper-case-result.v1` in the dedicated
`orbiplex.whisper.case.release-commit-refusal.v1` domain. The executor checks
the existing exchange, expected authority, exact request and live reply
lease before recording `commit-rejected`. Unsigned diagnostics leave
commit outcome unknown. The signed result and its replay remain private to
the case workflow.

Abandonment repeats the exact journaled exchange while its request is live.
After expiry a fresh private exchange can identify the same AD tombstone and
slot. The owner authenticates the executor and returns the original signed
acceptance with outcome `settled`. Its signed inputs digest binds the exact
tombstone claim. The read uses the status budget and a short reply lease, with
no new head or command charge. Exact replay of the new read within its lease
returns the stored response without charging the status budget again. A dedicated
abandonment-refusal signature lets the executor retain a permanent refusal
across restart. An unsigned diagnostic remains pending. Neither terminal result
can resume handoff.

The implemented commit stages bind one assessed `M_A` to the historical
source anchor and the executor's signed request. The existing fenced Store
holds the exact request, independently expiring response key and prepared PEX
packet. The first commit handoff fences `CommitUnknown` and stores the local
AD reservation before exposing any bytes. Replay returns the frozen packet
through the reply lease. Verification of both owner signatures precedes
recording an accepted result. An unsigned refusal remains diagnostic. An
unrecovered reply becomes `CommitOutcomeLost` at expiry. Final release-envelope
construction, AD handover and subsequent settlement still require native
composition. These commit stages do not qualify a runtime matrix cell.

AD assigns its delivery id only at admission. Freeze (component, idempotency key)
before commit. Before the deadline, exact KnownAbsent allows the same prepared
bytes to be submitted; Unknown/Unavailable do not. At/after the deadline, one
complete-history AD transaction serializes exact absence, deadline and tombstone
against admission. Tombstones cannot be GC'd merely after deadline+skew: without
a durable anti-rollback premise that would reopen the identity. Bounded capacity
blocks new work; namespace retirement must continue refusing old submissions.

**Enablement gate.** The current ledger caps ADC at 4096 reservation identities
over its lifetime, including admitted, abandoned and unresolved operations.
Before enabling ADC on a long-lived node, qualify durable identity-namespace
retirement and renewal, with stale submissions still refused after retirement,
restart and rollback. The bounded diagnostic matrix uses synthetic ledgers.

The AD component now reserves the local `adc-executor` identity with the exact
intent digest and deadline in the complete SQLite ledger before domain commit.
The executor retains the reservation with its prepared operation. AD serializes
first admission and settlement and pins the reservation to the admitted file.
The executor verifies domain acceptance and binds the exact release envelope.
Component tests exercise restart, both writer orders, the expiry boundary,
rollback and missing history. The native executor and runtime cells remain open.
See `node:artifact-delivery/README.md` for custody and capacity limits.

Abandonment changes the owner core, not only host policy. An accepted claim
requires Active, the slot's executor signature, exact intent/receipt/submission
binding, owner time at/after handoverBy and a Committed slot. The owner trusts the
executor's report after its local tombstone; it does not query the remote AD or
counter. Extend the existing abandonment command/domain with those bindings,
tombstone time and coverage marker. Journal its signed bytes before transmission.
The claim promises no execution and reports local absence; it is not proof that
nobody obtained the content. Slot consumption is irreversible.

Authentication, saved replay and id-conflict checks precede independent binding
and phase checks. Only a sole early-time failure yields NotYetValid/retry-at,
without signed case result or prepare entry. Bind the slot receipt, not current
head: unrelated amendment and withdrawal preserve it. Closure freezes owner
slots and new abandonment becomes Terminal/Never; local AD history can still
resolve transport facts without reopening the case. Expired request bytes do
not revive. While the claim is live, a tombstone plus unknown settlement
replays the recorded bytes. After expiry a new private exchange can recover
the original signed settlement for the same bound claim. Neither action hands
the payload to AD.

The pre-enable request now carries only the accepted revision and event digest
as the private slot receipt identity. The executor verifies the pinned owner's
signature on the private acceptance and binds it to the exact prepared commit
bytes before deriving that identity. The event binds the owner's evaluation
commitment. Exact count and source observation time stay in the owner record.
The public commit statement exposes neither the private receipt nor those facts.
An owner regression derives the claim from the actual result and exercises
settlement across both a withdrawal and an amendment.

### Dependency and qualification ownership

P015-011 supplies finite prepared-output retention. A scoped child of P015-005
must qualify the required publication/manifest tuples and actual issuance, not
silently close its whole parent. ADC-001 owns M/M_A, registration bijection and
intent contracts; ADC-004 owns actual counting, attestation and public commit;
ADC-003 owns holder obligations and every egress canary. ADC-005 consumes those
gates, P070 descriptors, P035 admission and the revised ADC-011/LLR-011 model and
owner. A schema or arithmetic helper alone closes none of these parents.

First complete a diagnostic end-to-end path, then a fresh pinned qualification.
Retain separate evidence for model laws, real owners and the 2x2 matrix (Agora
SQLite/Synapse by withheld/held-under-obligation). Compare model to actual Rust,
with independent specification vectors, mutation witnesses and axiom audit.
Measure commit-to-AD from the durable case fence through first exact AD
admission, including release of the writer reservation. Measure settlement,
guard hold and stale incidence separately. Distinguish ordinary publication,
publication after withdrawal, accepted abandonment and closure in the samples.
Model results prove neither cryptography nor filesystem crash recovery.
No inference/VM, installation or pull. Unavailable native Synapse means
not-run and ADC-005 todo.
full_candidate_qualified=false and release_ready=false throughout this slice.

The opt-in SQLite development check on macOS passes the exact WSS/INAC release
to a separate cold verifier with OS networking denied. A reachable loopback
listener supplies the positive control and a typed OS refusal inside the verifier.
The verifier uses the carried package, independent local trust and a fresh
SQLite index. Its digest binds the result to the original publication.

The local detached-fixture size check exercises real M/M_A, proof preparation,
the ordered commit and final signature for SQLite and both Matrix carriers.
Each carrier's boundary case verifies at the recipient. The next payload byte
is refused during planning, before requesting a commit.

The native Synapse developer check distinguishes local Agora admission from
durable forwarding and independent reception. The publisher's forwarding
record must name the exact Matrix event read back by the independent account.
The independent Agora relay must also return the original signed author bytes.
Neither local AD admission nor a publisher-local readback closes a runtime cell.
Each future Synapse qualification binds the structured native preflight emitted
by the same fixture launch to the candidate. It records the native Linux check,
local Unix engine, Compose version and both image digests. The launch also
records the resolved Compose image set and refuses startup if it differs from
the locally verified pins or cannot be resolved. The earlier developer
runs have no independently retained preflight record. A later development
run at Node `985127e69`, with an issued certificate, passed both custody
modes and tore down the owned fixture. Its launch printed a successful native
preflight with both pinned images. The later early-erasure path was exercised
by the SQLite held probe. These observations cover their respective sources.
Both SQLite publication modes passed a subsequent development run with signed
counting-authority custody and a fixture budget that includes AD hop retries.

The executor records `adc-release-admitted` for the exact retained AD run.
It advances to `adc-release-delivered` after an authenticated read from the
adopted Agora publication owner confirms matching signed bytes and carrier
completion. SQLite confirms audience-store admission. Matrix requires the
durable acknowledgement of the selected room and event. The journal fences
this observation with the original AD ID and a reserved write. Independent
recipient verification remains part of each runtime qualification cell.

## ADC-001 protected source preparation checkpoint (2026-11-17)

The existing Node authoring owner now accepts explicit private `case.disclosure`
input on its ordinary operator preview. It checks the exact M_A use in both
profile and certificate, canonical payload/Room descriptors/nonweak keys and the
default settlement horizon before case-key exposure. The finite encrypted
authoring checkpoint reserves independent random origin/payload/audience
openings before preview exposure. Case preparation binds C_M into that same
source preview without replacing its original source nonce/time.

Explicit Sign prepares the entire signed M_A set and exact signed source in
one checkpoint/fence before response. Replay retains bytes and openings; a
partial signature failure produces no partial returned set. The public source
readback contains neither M, payload/openings nor other audiences. An arbitrary
caller-supplied C_M cannot substitute for complete source consent.

This is source-owner implementation/component coverage, not a new qualification.
The disclosed component certificate is synthetic; actual issuance/native custody
and the full runtime remain separate gates. The finite source checkpoint is not
a promised full case-horizon hold or proof of transfer to S026. Complete-consent
handoff, source/payload/key holds, public owner publication, executor and all four
runtime cells remain open; ADC-001/003/004/005 remain todo. See the
[Node source contract](https://github.com/diapod/node/blob/master/daemon/docs/CONTEXTUAL-NYM-CERTIFICATION.md#protected-adc-source-preparation-2026-11-17).
Historical qualification sources, bytes and scope are unchanged.

## ADC-001 exact public-consent retention checkpoint (2026-11-17)

The existing Node original port now supplies the exact authenticated single-audience
manifest set as well as its compact basis. Actual full/detached P035 admission and
the complete M/M_A/certificate-use verifier precede freezing those bytes. The
registration owner rechecks signature and basis consistency, then retains the
canonical manifests and release-id/digest map in its existing fenced prepare/final
blob graph. Raw signed manifests are not independent certificate/profile authority.
Unsupported original adapters refuse before reserving a registration candidate.

Recovery uses the saved set without source acquisition or certificate renewal;
exact replay and first withdrawal preserve it with live ports disabled. Private
M, payload and secret openings are not copied into this public-consent storage.
Owner inspection remains privileged, not a public inventory of other audiences.
The experimental record marker changes to `public-consent.v1`; incompatible
pre-enable records refuse rather than acquiring an invented legacy meaning.

This is development component coverage, not clean-source/runtime qualification.
Public intent admission, protected execution openings, atomic retention/exposure
of the public statement with the private result, source/key/payload holds, actual
issuance, executor/cold receiver and all four runtime cells remain open.
ADC-001/004/005 and global/public readiness are unchanged. See the
[Node owner contract](https://github.com/diapod/node/blob/master/whisper-case-service/ADC.md#exact-public-consent-in-owner-registration-2026-11-17).
Historical qualification bytes and scope remain unchanged.

## ADC-004 public statement contract checkpoint (2026-11-17)

`whisper-release-commit-statement.v1` is now the bounded single-audience public
contract, with its own reserved signer domain and prepared authority-control
selector. It binds the public intent and effective restrictions; it does not
export private Acceptance, source/owner revisions, exact counts or private proof
identities. The same scalar narrowing law and independent audience binding
preserve the author's restrictions. Canonical signed fixtures and actual host
signer checks refuse changed authority, public/private field substitution,
generic signing and external callers. No authority rotation or default grant
is introduced.

See `node:whisper-core/DISCLOSURE.md` and `node:whisper-case-service/ADC.md`.
These are contract/crypto/signing component checks. Frozen public input admission,
atomic public/private result retention and post-fence exposure/replay remain open;
a signed candidate alone proves no owner commit, author admission or count truth.
The existing prototype intent/receipt must not be exported. ADC-004/005 stay todo,
with custody, release executor/AD closure, cold receiver and all four runtime cells
still unqualified. Historical model/runtime evidence is unchanged.

## ADC-004 local source-count component checkpoint (2026-11-17)

The explicitly adopted `node:whisper-intake::adc::LocalAdcCounter` now composes
actual contextual SQLite admission/complete inventory with the existing shared
contribution evaluator and real case-owner source barrier. It excludes the exact
original source only in its original epoch, applies the existing conservative
N+1 decision later, and retains historical certificate admission. Missing/future/
stale evidence never becomes a guessed zero or a new freshness clock.

The owner now also has a trusted-host proposal port using this same count. It
checks current case scope, eligible executor, withdrawal, slot and time before
signing a separate private `whisper-embargo-attestation.v1` under the restricted
signer domain. Source preparation checks it against retained consent and owned
executor. The source retrieves a proposal over relayed PEX v1 or offered direct PEX v2 using
`whisper-adc-proposal-request.v1`, which signs the exact exchange and reply key.
The signed attestation binds the request digest and returns in a private
`whisper-case-result.v1` with outcome `proposed`. Read budget, bounded exact
reply replay and the case fence are shared with existing owners. The proposal
leaves the case head and slot unchanged. A component history uses the private
PEX reply in release commit, with an independent explicit confirmation.
Direct preparation requires the already persisted v2 exchange and its live
authority-signed offer. The authority processes the exact carried query through
its ordered inbox. The source accepts the result from the authenticated
authority on the same exchange and carrier.

The canonical private `whisper-adc-source-evaluation.local.v1` descriptor freezes
exact request/facts, evidence, scope/epoch, finite validity and installed source
pin. It is bounded to 4096 bytes and passes Schema Gate; it is neither a public
count proof nor a portable authority token. Recovered owner candidates revalidate
that pin without recounting. Actual full/detached component histories cover
publication races, saved preparation/reopen and unchanged final replay.

See `node:whisper-intake/ADC.md` for ownership, boundaries and refusal cases.
These are development checks under synthetic credential/clock policy, not a
clean-source campaign or full ADC-004 qualification. Actual auxiliary issuance,
source/key/payload holds and runtime egress, public count/commit statement, AD
closure, executor/cold receiver and all four runtime cells remain open. ADC-004
and ADC-005 stay todo; historical evidence and readiness are unchanged.

### Counter recovery from committed registration

The ordered owner can reconstitute the original counting identity from the
fenced registration and its exact retained profile, certificate, basis and
M_A set. A composing host selects the admitted local relay. Authenticated
release continuation can recover its counter without private M or a new original
admission. A prepared candidate still uses its saved pin, and fresh evaluations
still require current source evidence. Completed replay and author controls do
not depend on counter recovery. Full/detached development tests cover this
boundary, including missing retained material and recovery without recounting.
Native adoption, finite custody and the four runtime cells remain open.

## ADC atomic public commit component (2026-11-18)

Development component, not full runtime qualification. Executor-signed private
release requests now carry the public intent and its private execution opening;
these bind the exact retained M_A before a source count is evaluated. The existing
owner candidate fixes public statement inputs and effective restrictions. Restricted
P037 signing, private result, public bytes, head/slot and settlement hold use one
final Store/fence commit. No signed candidate is exposed; failure/reopen preserves
the same public preimage, and completed replay does not sign or seal. An accepted
release result requires its separate public statement; old private-only outcomes
are not upgraded by a default. Controls and abandonment cannot attach the opening.

The control cap remains 4096 B; the derived result cap becomes 11414 B, below the
existing 16-KiB CaseResult PEX profile. No Synapse limit is increased. The component
reuses exact manifests, the actual local counter/guard and existing owner persistence,
not another journal or receipt protocol. Complete safe-public proof production,
authority/source/payload holds, executor/AD closure, cold receiver and all four
runtime cells remain open. ADC-004/005 stay todo. See `node:whisper-core/DISCLOSURE.md`
and `node:whisper-case-service/ADC.md`; historical qualifications remain unchanged.

## ADC private registration carrier component (2026-11-18)

The private command v1/v2 carries original M and the complete signed M_A set in
closed `adc/consent`, with its canonical digest bound by the continuity-signed
registration. Other command families refuse it. Payload and opening remain in
the protected source hold and are not registration material. This extends the
pre-enable contract in place; ordinary registrations omit both optional fields
and retain their bytes. Existing control and transport budgets are unchanged.

The source uses its existing encrypted S026 hold and exact PEX preparation.
The ordered service requires explicit composition adoption, independently
verifies P035 evidence/source certificate/complete consent and freezes the
existing per-case basis, manifests and policy. It does not replace a global
original provider. Completed exact replay and first withdrawal remain available
without live count/original ports after reopen. Signature budgets include both
manifest checks and reconstruction of the scoped certificate.

Development packet/dispatcher tests cover actual encryption/opening, exact
binding, default refusal, missing/changed material, bad child signature, no
partial case/signature, reopen and immutable handoff. This does not install the
native daemon adoption, finite authority/source/payload holds, per-case counter,
executor or cold receiver. ADC-001/004/005 and the four runtime cells retain
their open status; historical evidence and readiness claims are unchanged.
Implementation details: `node:whisper-case-service/ADC.md`.

## ADC source author-control workflow component (2026-11-18)

Implementation component; ADC-005 remains todo. The existing S026 author workflow
now freezes and prepares amendment, withdrawal and confirmation with its original
finite request interval, exact packet replay and ordered result verification.
The operator v1/v2 `prepare-adc-author-control` action resolves the actual bound
case key/anchor/authority/horizon and rechecks custody at handoff. It does not
renew a nym certificate, consult a live count, sign an executor command or create
another queue. Remote acceptance remains with the case authority; AD custody is
not a result. The local v1/v2 read contract admits the previously retained
signed amendment, withdrawal or confirmation as request material with empty
evidence. The projection stays within the authenticated source operator
boundary and refuses executor claims. Development checks pass all 292 service
tests (one existing exporter ignored),
11 local Schema Gate tests and a native three-control V1/V2 history. V2 requires
independent direct adoption plus a signed recipient offer; missing adoption is
measured as a refusal. Minimal-trace inspection remains redacted, and synthetic
anchor/registration inputs are explicit. These component tests do not close authority-key holds,
public/private commit publication, the release executor/AD closure, cold receiver
or any full SQLite/Synapse by custody runtime cell. See
`node:whisper-case-service/ADC.md` and `node:daemon/docs/RELAY-DELIVERY.md`.

## ADC author continuity signing component (2026-11-18)

Implementation component; ADC-005 remains todo. S026's existing case-key owner
now accepts only a closed prepared author amendment, withdrawal or confirmation.
It checks the bound author-byte anchor, actual case public key, original horizon,
clock, erasure and fence before returning a signature, independently of a live
source certificate or count. Release-commit and abandonment remain executor
operations. The ordered case owner still determines effective consent and accepts
or refuses the control. No host route, authority-key hold, release execution,
runtime cell or historical qualification is established by this component.
See `node:case-key-service/README.md` for tests and convergence boundaries.

## ADC explicit source transfer component (2026-11-18)

The existing operator case workflow adds `retain-adc-consent` with only adopted
source profile, certification and authoring-operation references. The host
resolves protected source material and local verified status independently; it
transfers exact complete consent and approved payload/opening into the existing
S026 fenced owner, without a private-material JSON export, fetch or signature.
The saved encrypted source-operation binding governs exact retry even when the
source's shorter preparation is unavailable. Current actor/root/disclosure and
adopted-profile checks remain required; acknowledgement creates no release right.

The source checkpoint and target have separate durability owners. Retained target
state resolves a lost response and must never be recreated from current source
labels. Actual native key holds, complete egress composition, public statement
publication, executor/AD closure and all runtime cells remain open. Development
component tests do not promote ADC-001/003/004/005 or historical qualification.

## ADC approved-payload retention component (2026-11-17)

The existing S026 consent blob now retains the exact approved release payload and
its independent C_P opening together with M/M_A. The pure original verifier
checks exact bytes, bounded size and distinct opening before retention and after
decode. The source read gate and scoped protection key still control access;
these private exports are not a counter projection or permission to release.
Replay preserves the first ciphertext and horizon. Missing pre-enable fields
refuse instead of synthesizing material. Requester expiry does not erase the
longer existing consent hold; the case/replay horizon does not renew itself.

This component does not establish actual protected-source transfer, native
payload/key holds, public commit publication, executor/AD closure or runtime
qualification. ADC-001/003/004/005 remain todo. Historical evidence is unchanged.

## ADC source-owner consent retention checkpoint (2026-11-17)

The existing S026 AuthorWorkflow now retains complete M/M_A consent in one
bounded, purpose-separated encrypted blob and one fenced owner update. The
operation checks the actual source signature/certificate/scope, original binding,
case authority/horizon and complete audience bijection. Exact retry preserves
first bytes and original time; historical read grants no current release right.
Blob references survive actual PEX registration preparation and short requester
expiry. Wrong scope/gate, changed consent, failed writes and missing material
refuse without substituting a new set. No source body or public hold receipt is
introduced. See `node:whisper-case-service/ADC.md` for the component contract.

These are development component checks, not a new retained campaign. Actual
vault/operational leases, protected source/payload holds, atomic source signing,
runtime egress composition, real P015 issuance, ADC-004 count/public statement,
AD closure, executor and all four runtime cells remain open. ADC-001/003/004/005
stay todo; no historical qualification or public readiness is renewed.

## ADC-001/005 private/public contract development checkpoint (2026-11-17)

The new `whisper-embargo-original.v1` contains private M; the separate signed
`whisper-embargo-audience-manifest.v1` carries one M_A. These do not change the
qualified P035/LLR `whisper-embargo-manifest.v1` contract or signing preimage.
Closed `whisper-release-execution.v1` and `whisper-release-intent.v1` separate
private execution identity/route/plan from public release evidence. P070 owns
`room-release-audience.v1`: room identity plus an exact history-policy digest,
without routes. The nested consumers share its schema and Rust descriptor.

Domain-separated commitments bind private origin, exact payload and execution
using independent 256-bit openings; public intent has no unsalted private proof
alias. M_A has its own nonce and signature domain. Complete registration checks
require every consented audience exactly once, exact common/header/condition
bindings, actual signatures and P015 scope. Current revocations, original-anchor
verification, protected preparation and durable registration remain separate.
The wrappers do not make those missing facts true by parsing.

A new exact auxiliary use must occur in both profile and certificate:
`(whisper-release, whisper-embargo-audience-manifest.v1, exact topic/key,
single-audience, embargo-audience-manifest)`. No default gains that tuple. The
actual authoring function checks current signing window, fresh status, revocations
and signer before signing, then verifies the returned signature. Old manifest
and publication grants cannot substitute. The macOS developer diagnostic now
exercises the exact auxiliary issuance and registration on encrypted APFS
media. P015-005-ADC retains the full native issuer composition and
qualification gate.

Canonical schemas/mirrors and refusal fixtures cover private-field injection,
unknown routes, scope, signature/domain, nonce, bijection and identity bindings.
See `node:whisper-core/DISCLOSURE.md` for exact preimages, caps and reproduction.
This component does not replace the current owner's private prototype intent,
install a real ADC-004 evaluator, freeze an atomic S026 output, or qualify public
commit attestation, custody, AD closure, executor/cold receiver or any runtime
matrix cell. ADC-001/004/005 remain todo; historical evidence is unchanged.

## ADC-004/005 real relay barrier development checkpoint (2026-11-17)

The file-backed SQLite relay provides explicit host source adoption, a durable
private inventory pin and an RAII IMMEDIATE writer barrier. The pin binds the
adopted instance/installation, actual file, scope revision and status digest.
It shares the complete inventory and existing revision check; it grants neither
count authority, inventory completeness nor a renewed signed status lease.
The one acquisition budget (at most 250 ms) covers mutex and SQLite waiting,
with current-pin checks afterwards. The composing case owner samples its final
time only after acquisition and retains the token through commit/fence.

Relay schema 7 preserves one installation identity and refuses missing/corrupt
metadata rather than reminting it. Verified reopen requires fresh explicit host
adoption; unchanged files can retain their pin. Copy/restore or maintenance by
file/directory replacement requires readmission. This local mechanism assumes
cooperating maintenance, not protection from privileged in-place full DB rollback.
It fences the local index for both Agora carriers, not the Synapse homeserver.

Development signed-source tests pass 69 contextual SQLite cases, with one
controlled child helper ignored by the ordinary runner; external writers, WAL
readers, timeout/cleanup, replacement, restart and process death are covered.
Relay migration/descriptor suites and all-target Clippy pass. Owner ADC fixtures
still use a synthetic evaluator. Actual ADC-004 count/original composition,
M/M_A, custody, public proofs, AD atomic closure, executor and all four runtime
cells remain open. ADC-004/005 stay todo. No formal campaign, model/VM or new
runtime qualification was performed; historical evidence is unchanged.

## ADC-001/005 actual original-port checkpoint (2026-11-17)

The Node `AdmittedAdcOriginal` now verifies the actual proven P035 registration
observation, M/M_A bijection and exact original source certificate before
freezing the existing ordered-owner basis. Canonical audience descriptors derive
route-independent release IDs. The bounded private
`whisper-adc-original-basis.local.v1` descriptor binds the exact admission/original
and complete manifest set through Schema Gate; it is neither a custody hold nor
the public recipient proof.

Actual full/detached owner fixtures register through this port, reopen without
live original/count adapters, replay the exact original registration and accept
the first withdrawal from frozen state. Missing/changed/forged consent, foreign
anchors and unavailable timing/completeness refuse. These component checks do
not install the daemon's ADC execution path or qualify private source retention.

S026 atomic source preparation/holds, real P015 issuance, ADC-004 count/public
statement, AD close, executor and all four runtime cells remain open. Parent
ADC-001/004/005 statuses and historical qualifications are unchanged.

## ADC-001/005 signed original-source binding checkpoint (2026-11-17)

The optional `disclosure/original` field carries C_M in signed protected signal
v2/v3 and the separate detached anchor manifest. Both require the complete case
commitment. P035 checks their exact equality before detached admission; the
existing receipt commits the signed objects without adding a manifest list or
private opening. An ordinary source without C_M cannot acquire ADC retrospectively.

The independently verified historical anchor carries C_M, the original source
certificate digest/epoch and receipt acceptance time. The registered owner retains
these claims; ordinary snapshot/input preimages remain unchanged. The original
verifier binds that source to M and the complete exact M_A bijection. Historical
publication-time validity is separate from current permission to sign or count.

Actual full/detached producer-to-anchor tests and snapshot refusal/roundtrip checks
exercise this component. Source custody, S026 atomic preparation, real scoped
issuance, installed original/count adapters, public commit, AD closure, executor
and all four runtime cells remain open. ADC-001/004/005 stay `todo`; this checkpoint
does not replace historical ADC-011/LLR-011 qualification or promote readiness.

## ADC-005 bounded public release package

`whisper-release-proof-package.v1` carries just the signed single-audience
manifest, the detached P035 anchor and witnessed receipt, the receipt profile,
and the approved payload with its independent opening. The receiver selects
its own audience and locally admitted trust. The package contains no original
protected signal, homeserver PDU, private acceptance, count, or private route.
The public intent binds the exact package digest before commit.

`whisper-embargo-release.v1` carries that package, the exact public intent and
separately signed public commit statement in the executor-signed Agora record.
Preflight checks the selected carrier with the upper bound on late statement
and signature bytes. The journal fences the final bytes before handoff and
retains them across restart. Carrier checks cover the stamped 49,152-byte
SQLite envelope, the Matrix v1 49,152-byte author budget with stamped envelope
limit, and the Matrix v2 36,864-byte author budget. Matrix carrier tests do not
exercise admission by Synapse.

The development history uses a detached SQLite anchor and actual ordered
owner. It verifies the released payload without acquiring the protected
original or trusting a witness selected by the sender. Destination admission,
native custody, AD handover and the four runtime cells remain open.

## ADC-005 reserved AD handoff component

The private execution descriptor binds the host-resolved Agora route plan
before commit. AD reserves that binding with the intent and handover deadline.
A changed plan cannot admit the old intent. An already admitted execution
retains its first plan and AD ID independently of later route resolution.

The journal fences the unknown outcome before submission. A lookup that
proves absence before the deadline permits the exact same persisted artifact.
A retained admission or durable tombstone fences the corresponding local
phase. The adapter owns transport retry after admission. The in-process
component histories cover a pre-admission write failure, replay after restart,
and a lost response to a successful admission. Confirmation of delivery, daemon custody and the runtime matrix remain open.

## ADC-005 signed abandonment component

The journal derives the executor claim from the retained private commit
acceptance and local AD tombstone. It fences the exact signed operation,
separate exchange and expiring reply key before preparing the private packet.
A live packet replays byte for byte. After the request expires, a new
private exchange can report the same tombstone and receipt. It can recover
the original signed acceptance through a settlement read even after the
earlier reply lease expires. The owner checks the executor and exact slot
binding and charges the read budget. This exchange cannot submit the release.

The in-process history couples the real SQLite AD settlement and ordered
case authority through PEX with controlled time. It rejects a foreign
executor key, restarts at the control and packet boundaries, renews the
expired claim and records an owner-signed acceptance after exact reply
replay.

The operator workflow exposes prepare, handoff and read actions for the
exact release ID. Preparation requires the retained AD tombstone.
The relayed carrier uses the adopted CaseRequest circuit. The direct
carrier binds an authority offer to the settlement exchange and saves it
with the exact packet before AD admission. The result is routed by its
durable exchange locator. The local projection distinguishes private
transport custody, pending settlement, verified abandonment and unresolved
execution at closure. Only a terminal refusal for the bound executor and
committed slot can carry the owner's original signed closure acceptance.
The executor verifies the closure against its pinned authority and earlier
signed commit and fences the exact result. An authenticated permanent refusal
for the matching abandonment is retained as `abandonment-refused`. An unsigned
or retryable refusal leaves settlement pending.
Separate custodian handover and runtime matrix qualification remain open.

The relayed v1 development probe exercises the operator actions through
HTTP and the actual WSS/INAC courier. It confirms early refusal, a real
deadline and AD tombstone, the same delivery ID on handoff replay, and
signed response readback. The source AD inventory contains no release job
after settlement. Direct v2 offer retention and replay were tested in the
component fixture.

A companion relayed v1 development probe closes the case through the same
operator and WSS/INAC path after an accepted commit. The executor waits for the
handover deadline, retains its AD tombstone and reads `adc-unresolved-at-closure`
from the verified terminal reply. The slot remains committed in the component
history, and the runtime probe observes no public release job.

## ADC-005 source-barrier and stale-recovery development checkpoint (2026-11-17)

The case owner now separates publication predicates from acquisition of an
RAII source barrier. Missing adapter support refuses. Signing/reply preparation
are outside it; final time, retained pin and lease checks follow acquisition.
The token lives through Store commit and its final fence. Full evaluation is
not rerun under the barrier or when recovering a pending candidate. The owner
supplies a 250 ms acquisition budget; real relay enforcement and durable
instance/installation/file/scope/revision pins remain ADC-004 work.

Stale publication atomically deletes its candidate, records a bounded technical
cycle/digest binding and charges the dedicated stale-attempt window. It changes no
accepted head or signed outcome and cannot use settlement reserves. Restart
preserves the three-cycle limit and cross-operation request-ID conflict checks.
Cleanup failure blocks the owner until verified reopen. The same bytes can
be reevaluated only after durable invalidation; the fourth stale-cycle attempt
does not evaluate. Saved final results retain exact replay. Technical history
uses existing finite Store limits and the case/replay horizon.

Typed local workflow responses and relay diagnostics distinguish transient
`evaluation-stale` from terminal `evaluation-stale-exhausted`; neither is a
signed case result. Five new component histories cover acquisition delay,
fence lifetime, missing guard, cycles/restart/conflicts/budgets and cleanup
failure. Their source pin/lock is synthetic, not real relay qualification.
The inspected signer audit receives no signature or raw control. ADC-004
adapters, privacy proofs and actual execution remain open; ADC-005 stays todo.

The private snapshot now requires a guarded-publication contract marker. Older
strict readers refuse the new shape; new readers do not upgrade old prototypes
by default. Diagnostic regression passed 17,699 model/Rust comparisons, twelve
independent histories and 330 scoped Rust tests, including 35 signed ADC owner
histories (one existing exporter ignored). The marker-bearing owner suite
passed again directly, 35/35; two focused daemon adapter tests passed. Schemas
and source mirrors include positive local errors and negative case-result
fixtures. No full runtime, new retained campaign or readiness claim is made.

## ADC-005 frozen-registration development checkpoint (2026-11-17)

The existing case owner now has an explicit host composition entry,
`register_adc`, which freezes the independently verified original, finite
release policy and empty projection with registration. Ordinary registration
does not authorize a later ADC retrofit. Pending registration recovers its
exact policy/proof; restart or configuration changes do not renew it. The
private pre-enable snapshot requires the policy, with no guessed migration.
Default settlement/TTL checks run before preparation or signing. The current
short-clock component fixtures explicitly choose a shorter test profile; they
are not evidence for the default 60/60/900-second runtime profile.

Static handoff/reply shortfalls are retained permanent refusals; a shorter
actual response lease is unavailable, not a consent refusal. A fresh final
time and the actual sealed lease are checked before publication, using the
registered TTL/horizon. First withdrawal needs no live count/original adapter.
This shares the existing owner/candidate/Store/fence machinery. It does not
qualify M/M_A admission, remote policy disclosure, the relay guard, real
ADC-004 adapters, stale-cycle recovery or release execution. ADC-005 remains
todo and all historical qualification scope remains unchanged.

Diagnostic checks passed 17,699 model/Rust comparisons, twelve independent
specification histories and 324 scoped Rust tests, including 30 named ADC
fixtures. One existing exporter remains ignored; the new strict policy
roundtrip test passed separately. The runner requires the exact reviewed
execution-name inventory, with missing/duplicate/substituted/ignored controls.
Core/owner all-target Clippy and global retention checks pass. No new formal
campaign, retained qualification or release-readiness claim is introduced.

## ADC-005 executor-claim development checkpoint (2026-11-17)

The current pre-enable v1 request replaces remote-AD evaluation for abandonment
with the executor's signed exact intent/receipt/submission claim, tombstone time
and coverage binding. The owner authenticates an admitted actor independently
of the supplied slot fields, then applies the revised active/committed/deadline
law. It trusts the executor report; a coverage digest is not independent proof
of AD absence. Owner phases are only committed/abandoned. Current private intent
fields are not yet the recipient-safe public intent required by ADC-001.

Valid early claims return a typed time deferral without candidate, result or
operation charge, even at full ordinary quota. Bad binding is a retained refusal
before that deferral. Expired bytes do not revive and future issue time is
included in retry-at. The original slot receipt survives author withdrawal or
amendment; closure freezes new claims and exact saved results remain replayable.
The local operator workflow schemas v1/v2 preserve an explicit retry-at, without
minting a signed case result. Full executor/remote deferral handling remains an
execution integration obligation.

The model separates owner settlement from executor closure. Exact absent AD
history proposes closure; only an exact completed closure establishes a local
tombstone. Settlement and tombstone stickiness lift to finite histories, and
concrete guard mutations cover receipt, authenticated actor and tombstone.
Development checks cover 102 audited theorems, 53 named vectors and 4096 trace
steps; actual axiom union is propext/Quot.sound. The actual Rust decision adapter
covers 17,699 comparisons and twelve independent expected histories. The scoped
Rust entry passes 318 tests including 24 signed ADC fixtures, with one existing
exporter ignored; the daemon retry-at projection test passes for both local
workflow versions. All-target core/owner and daemon-library Clippy pass. These are
current worktree checks, not a new clean-source retained qualification or proof
of crypto, AD closure, custody or filesystem recovery. Historical ADC-011/LLR-011
evidence retains its pins/scope; ADC-005 remains todo.

## ADC-005 native environment checkpoint (2026-11-17) {#adc-native-environment}

The resumed implementation uses integrated Node `d13029149` / Orbidocs
`871068e3` as its base. P015-011's finite-authoring retention gate is now done
in its separately qualified scope; ADC consumes that contract rather than
reimplementing it. ADC's own source-custody use still needs qualification.

An initial pure host-policy implementation lives in
`node:whisper-core/src/case/adc_policy.rs`, with eight offline contract tests.
Defaults are 60 s minimum handoff, 60 s reply margin, 900 s settlement window,
5 s preparation budget and three stale cycles. Registration arithmetic requires
TTL 125..900 s and `release_end + settlement_window <= case/not-after`.
The executor chooses handover no later than request expiry minus reply margin.
Static handoff/reply shortage is Never; shortening only by the available reply
preparer is dependency unavailability. Canonical result schema and Node mirror
carry `adc-handoff-window-short` and `adc-reply-window-short`; transport
`evaluation-stale` is not a case-result reason.

The host-policy helpers are not yet installed in the owner. Policy snapshots,
revalidation after guard acquisition, durable stale
accounting, revised owner/executor models and actual release composition remain
open. This checkpoint does not promote ADC-001/004/005 or supersede the qualified
historical LLR-011 behavior. Time arithmetic is not a promise of delivery.

The owner component correction reserves one command result for each
committed slot and checks that capacity before preparing a new commit. Ordinary
commands cannot spend it; valid settlement survives a full command/operation
budget and restart without accumulating preparations on signer failures. The
owner's admitted principal is retained independently of its replaceable signer:
fresh mismatched-signer decisions are unavailable, while exact history remains
readable. Three added actual-owner fixtures cover these boundaries. At that checkpoint the synthetic abandonment port and old model were still in
use. The executor-claim component above supersedes those boundaries; the full
runtime remains open.
The diagnostic comparison entry passes 15,636 model/Rust comparisons, eight
independent specification histories and 304 scoped component tests, including
18 ADC owner fixtures. No new clean-source qualification or formal evidence
campaign is claimed; previous qualifiers and proofs retain their scope.

The storage-quota extension adds a finite fenced hold per accepted slot,
consumed only by its settlement or released by closure. Even terminal writes
preserve other holds. Object/event/byte quota, exact pending-basis readback,
rollback and process-kill boundaries are tested in the existing Store. Format
two preserves verified no-hold v1 facts/head preimages during a metadata-only
upgrade; active holds use a distinct root domain and predecessors refuse them.
This is quota protection, not disk preallocation or a claim against physical
I/O failure. It does not install registration policy, revise abandonment/model
laws or qualify execution. The diagnostic entry passes 15,636 model/Rust steps,
eight independent specification histories and 312 scoped Rust tests, including
19 ADC fixtures; one existing exporter remains ignored. The ordinary-path
read-only observer recognizes both store formats, with 37 scoped Python tests.
Historical qualifiers retain their source pins and bytes. See the current
[Node checkpoint](https://github.com/diapod/node/blob/master/whisper-case-service/ADC.md).

Implementation checkpoint, not release execution qualification. The current
Node launcher has an explicit `--native-only` gate and a read-only JSON preflight
in `tools/matrix-fixture/synapse/native_preflight.py`. ADC qualification requires
bare-metal Linux, a local Unix-socket Docker engine with Compose and both exact
profile images already installed. Missing Compose returns
`not-run/compose-unavailable` before fixture-state writes. macOS refuses before
Docker or fixture-state writes; missing
virtualization detection, containers and uncertain observations fail closed.
The launcher and Compose services prohibit automatic pulls. Missing software or
images need a separate operator decision.

The measured macOS result is `not-run/virtualized-runtime`. Seven new gate tests
and 23 existing fixture-setup tests pass offline without a service. This closes
only the environment-gate implementation fragment. It does not qualify Synapse,
payload custody, public proofs, owner revisions or release execution. The matrix
axes remain Agora carrier (SQLite/Synapse) and custody (withheld/held-under-obligation).
ADC-005 stays `todo` while required Synapse runtime cells are `not-run`; historical
P035 evidence is not a substitute. The preceding stage-0 evidence is unchanged.

## Pre-executor stage-0 corrections (2026-11-16) {#pre-executor-stage0}

Before ADC-005 enablement, correct the model/owner/AD prerequisites. The current
model permits exact authoritative AD absence to restore unknown to committed
strictly before handover expiry. Only the same accepted intent and execution
identity may then be handed over. At/after expiry absence permits abandonment;
unknown/unavailable never implies absence, and admission cannot be undone.
Confirmations are stored per canonical audience and admitted only in confirm
mode. Narrowing pre-authorized to confirm therefore requires fresh confirmation.
Permanent withdrawn, occupied-slot and expired refusal codes have retry Never.
Original retained registration verification is independent of live evaluation;
a first withdrawal cannot require the current counter or AD service.

AD reuses its existing exact input/first-plan bindings for the release schema,
refusing changed bytes under the same component/idempotency key. Volatile history
cannot establish absence; ADC enablement requires complete durable SQLite.
Missing historical binding or incomplete recovery is unavailable, not permission
for another execution. Deadline/admission/absence serialization remains an ADC-005
integration gate, not a theorem about the pure model.

Independent specification vectors cover recovery-table obligations and explicit
state edges in addition to model/Rust equality. Model-only executor witnesses do
not qualify the absent runtime executor. Historical ADC-011 and LLR-011 reports
retain their exact bytes and original scope; see
`node:docs/audits/P013-ADC-STAGE0-2026-11-16.md` for corrections and current tests.
ADC-005 remains todo until real ADC-004, source custody and executor acceptance.

## ADC-005 live counter adoption checkpoint

The daemon can now select the local ADC counter for an already admitted case
registration through explicit adoption of the live Agora SQLite index. The
relay retains ingestion, migration and recovery. The companion reads the exact
inventory and holds the existing short writer barrier through the case commit.
The adoption binds the installation, file and named local instance. Replacing
the index requires readmission. An in-place restore that returns to an older
scope revision can otherwise replay the numeric revision with different
inventory. Each revision now carries a random generation from the same SQLite
transaction. A changed generation invalidates the candidate and requires a
fresh evaluation. For Synapse the pin covers the local ingested index. Remote
freshness and homeserver completeness remain separate checks.

A focused owner test exercises real retained admissions, a frozen candidate,
restart recovery without recounting and exact replay. ADC-004 and ADC-005
remain `todo` pending native registration and custody adoption, executed release
and cold verification, and the runtime matrix.

## ADC-005 native registration and key hold checkpoint

The native authority profile can explicitly adopt ADC registration alongside
the adopted counter. The ordered owner authenticates the request and verifies
the original source and exact per-audience consent. Before a candidate is
written, the identity owner durably holds that exact signing key through the
case horizon. Its bounded record keeps the greatest horizon for the current key.
An interrupted attempt can conservatively leave a finite hold. Ordinary rotation
preparation and identity bootstrap use the same lock, including when the case
role is disabled. A caller's prepared time cannot end the hold. No entry stores
private key material.

Fresh ADC decisions check the configured provider against the pinned authority
before changing case state. Exact historical replay is independent of current
signing and renewal of the hold. Component tests exercise the registration
failure before candidate creation, same-byte replay, native rotation refusal,
loss/reopen and monotone recovery.

The native registration probe also completes PEX/AD ingress and opens the
authority's signed reply for FullRecord and DetachedManifest. Both use actual
signed P035 receipts in a synthetic federation and the default ADC policy with
the 900-second settlement window. The daemon saves the original binding, both
audience manifest digests, the owner policy and the key hold. The hold still
applies after shutdown. The relay provenance is a fixture at the native ingress
boundary. Source/payload custody, native execution and cold verification, and
the four runtime cells remain open. ADC-004 and ADC-005 stay `todo`.

## ADC-003/005 source custody at executor preparation {#adc-source-custody}

S026 source review can explicitly select the detached form with
`case.disclosure["source/detached"]`. Its review digest binds the selection
before any signature. The author needs the exact P015 detached and audience
manifest tuples. The explicit signing operation fences the auxiliary and the
protected signal with the private manifest set. The signal binds the exact
signed auxiliary digest; both bind the same hiding commitment and case.
P035 still owns witnessed admission and detached projection. Local readback
of the signed auxiliary does not grant custody, register the case or count as
a qualified runtime cell.

The P036 owner pins the receipt profile on opening reservation. The witnessed
detached capture keeps the original horizon and can store the public proof
without the protected signal. S026 can then prepare an exact encrypted
registration with the already bound continuity key and protected consent.
Authority-side admission and delivery across independent processes remain part
of the runtime gate.

The ADC component also prepares and reopens this encrypted registration using
the exact certificate from the real P015 V2 applicant and issuer exchange.
The issuer publishes a fresh signed status after the witnessed admission to
establish the P041 basis. Omitting the requested manifest use produces a
certificate that cannot authorize protected authoring. This check uses fixture
media attestation and reply delivery for issuance. The issued certificate now
also goes through S026 registration, real WSS/INAC execution and independent
SQLite publication readback in both custody modes. The earlier Synapse pair
used a fixture certificate. Both modes later passed with an issued certificate
at Node `985127e69`, as described in the native preflight checkpoint above.
The formal matrix is open.

A focused native check now passes the exact S026 detached registration packet
to a separate authority daemon. Its AD ingress accepts the packet, the ordered
owner returns a signed result, and the source verifies, retains and recovers
that result after reopening. The authority signing key remains held through
the case horizon. Authenticated relay provenance is supplied at the fixture
boundary. This check establishes independent owner composition, not WSS
delivery, release execution, cold reception or a runtime matrix cell.

The component scenario continues through two verified contextual admissions
in the authority's adopted SQLite index. The authority returns a private
signed threshold proposal bound to one audience and its named executor. The
source verifies the result and signs an explicit confirmation of that trigger
using the retained continuity key. The ordered authority accepts it at
revision one. The same fixture relay and synthetic identities bound this
development result.

The same withheld component scenario then reopens the accepted registration
with current Memarium custody. The executor fences its preparation, commits
through the native authority's AD ingress and consumes the sealed result. It
hands the exact signed Agora envelope to its local AD ledger, and replay returns
the same delivery ID. The cold SQLite-backed verifier uses independent local
trust and checks the carried proof without the protected original. The relay
ingress is still supplied by the fixture. A separate development probe uses
the normal AD Agora adapter to publish the same bytes to a stock SQLite Agora
process with independently adopted trust and audience. The authenticated HTTP
readback preserves the exact signed author bytes and the relay supplies its own
unsigned metadata. A second development probe sends registration, proposal,
author confirmation and commit over authenticated WSS/INAC through the AD
source, courier and authority roles. The four exchanges correlate sixteen
exact AD deliveries, and the courier preserves their opaque PEX bodies. The
source verifies the retained results and publishes to the independent SQLite
receiver. Source workflow actions enter through the operator HTTP route.
The fixture checks missing-token and missing-binding refusals before parsing
the body, then establishes its local binding through the identity API. It
supplies the initial retained author consent, synthetic trust and signed
contextual admissions. Separate custodian handover, authenticated closure
readback and the runtime matrix remain outstanding.

The S026 source owner constructs the protected package for one retained audience
under independently adopted P035 trust. The source custody port must observe the
owned author node in `withheld` mode or the named custodian's finite obligation
in `held-under-obligation` mode. The source checks the signed holder and executor
lists and requires coverage through the case horizon. It keeps the complete
private original and other audiences at the source.

The executor first-write boundary checks and preserves the exact custody
binding in its encrypted journal and rechecks the lease before commit to disk.
Earlier component tests connect both custody modes with a fixture custody port.
The held package uses the one-way `held-custody-transfer` PEX family and the
signed `held-custody-recipient` key-offer role. Its named destination must
match the independently admitted offer at sealing and opening. The distinct
key derivation domain and typed key ports keep held execution material out of
ordinary protected-signal and case-command flows. The 57,856-byte plaintext
budget fits the 64 KiB AD minimal-trace frame. Opening establishes which
private package was carried. Admission and durable custody at the destination
require the host's current peer policy, independent local witness trust and
finite custody obligation. Component tests cover exact round-trip and role
separation. The recipient's bounded offer journal uses its own SQLite scope
and external fence. It recovers exact signed bytes after restart under current
peer authorization. Before a held recipient is installed, AD refuses detailed
admission of both the binary `whisper-held-custody-pex.v1` carriage and its
inner JSON schema. The local Memarium payload owner records both the
signed release deadline and the case deadline in a separate journal and
uses an erasable DEK for each retained payload. The release deadline closes
reads and triggers managed key and ciphertext removal on maintenance or
restart. A fenced AD admission can retire the exact held copy sooner. The
executor replays the idempotent retirement using its originally bound delivery
identity. The journal keeps the exact transport receipt until the case
deadline. The committed executor has a separate journal for settlement.
Component tests cover restart between committed retirement and file
removal, plus exact receipt replay after erasure. The host receiving
adapter now checks the exact offer, protected recipient, audience and witness
policy, and a local obligation through the signed case deadline. It can
recover an exact committed receipt after offer expiry using digests and
current peer authorization. Executor readback has a separate live gate.
An explicit native source profile can now adopt held reception for bounded
peers, audiences, witness trust and deadlines. The operator prepares the offer
through the existing local case workflow. The dedicated binary AD carriage
uses the authenticated direct minimal-trace path. The local provider stays
outside application backup selection and S020 can expire records after role
withdrawal when the journal is available. ADC-003/005 remain `todo` and
runtime qualification remains open.

The author crosses the same direct AD boundary using the authenticated local
`handoff-held-adc-transfer` operation and an explicit route to the named
custodian. The source verifies the retained registration, one selected
manifest, the holder binding and its current private disclosure policy. S026
fences the exact offered ciphertext before AD and binds the exchange to the
offer and route through the case horizon. Ciphertext retention in this journal
ends at the original offer deadline. Tests reopen the author journal
and check exact replay, changed-route refusal and expiry. AD owns transport
execution and retries, and the recipient observes custody independently.

The held executor reads that recipient's Memarium under the independently
adopted Room policy. Operator proposal and commit preparation select the held
release ID and audience. The existing journal distinguishes author registration
from held custody and rechecks the exact package and registration acceptance
before commit handoff. It can complete an accepted commit from its own frozen
proof with the held role's local witness policy. The component test exercises
the held provider, restart, refusal when the held copy is unavailable and AD
publication. A separate development run delivers the package from the author
to the custodian through direct WSS and minimal-trace AD. Before custody,
the custodian cannot prepare a proposal. After custody, the proposal and
commit travel from the custodian through the courier, and the author signs
confirmation from the original source. The custodian publishes to the
independent SQLite receiver. Readback matches the signed custodian bytes
and the cold verifier recovers the approved payload. The Synapse runs and
formal qualification remain open.

### Signed registration policy

The private ADC registration acceptance carries a signed `adc/registration`
snapshot with the original commitment, the frozen release policy and the
effective request TTL. The snapshot comes from the same fenced registration
candidate as the case row. Recovery and exact replay preserve the original
policy. Ordinary registration and subsequent acceptances omit the snapshot.

Before preparing an execution, the executor verifies the acceptance for the
case authority, checks the case and original against its release proof and
intent, and uses the snapshot for the handoff window. It pins the acceptance
digest in its encrypted journal. Recipients of the public release receive the
separate commit statement and the authorized release proof. The policy snapshot
does not attest custody or complete any cell of the runtime matrix.

### Source-local withheld preparation

The source role adopts explicit ADC execution routes by canonical audience and
uses the independently adopted registration trust. The local operator
can invoke `prepare-adc-execution` with a stable request ID, route, signed
private proposal and the retained registration and manifest references. The daemon checks the
local executor identity, verified registration, live finite Memarium proof
lease and exact local route. It transfers the single approved payload and
opening internally from the S026 owner to the fenced executor journal.
The executor selects the handoff window from the signed policy and constructs
the public intent and salted private descriptor. Only the internal P037 node
operation signs the commit, within its reserved signing domain. The journal
pins the exact signed bytes before an acknowledgment identifies the release
and local phase. Exact replay returns the same exchange without signing.

The source-local `withheld` path now includes an explicit `handoff-adc-commit`
for relayed PEX v1 and offered direct PEX v2. The journal fences the exact control
packet and local AD reservation before enqueuing transport. Its exchange locator routes the private
case result back to the executor. The response's transport custody is distinct
from the signed owner commitment and the later release submission. Reply lease
exhaustion records a lost outcome independently of current egress permission.
For direct v2 the journal retains the exact recipient offer with the packet.
The authenticated reply must come from the named case authority and match
the durable direct exchange. After the accepted reply, `handoff-adc-release`
reobtains the frozen audience, route and carrier from the executor journal.
The host signs the verified Agora envelope with the admitted executor's node
key. The journal fences the signed bytes before submitting the existing AD
reservation. Retained admission returns the original AD run; established
absence before the deadline permits submitting the same bytes. At or after
the deadline the local ledger can persist a tombstone. The operation returns
only its local phase and, when admitted, the AD identifier.
Agora verifies the complete carried proof before SQLite HTTP admission or
Matrix reception. It resolves the expected audience and history policy from
local adoption, including the observed Matrix room on that carrier. The
Matrix receiver registers the exact rooms from its local audience policy in
the durable account receiver before advancing the sync cursor. The
receiver reads only local observations concerning the carried receipt. The
Matrix origin verifies the carried proof before atomically storing the
publication with its adopted physical room, carrier and author bytes. Retry
uses that room and never resolves an alias; an unpinned historical release
request cannot be forwarded. Both SQLite custody modes have development
runs. The Synapse modes and the four formal runtime matrix cells remain open.
ADC-005 remains `todo`.

## Optional Confidential Affiliation Review {#confidential-affiliation-review}

Proposed post-MVP addition (2026-11-04), independently tracked as P013-ADC-010.
The [P015 profile](../015-nym-certificates-and-renewal-baseline.md#confidential-affiliation-attestation)
owns the proof and privacy contract. Whisper consumes a scoped finding, not the
author-to-participant mapping. This profile is optional for each signal author;
it is not a prerequisite for ADC-000 or existing alpha/MVP gates.

During `confirm`, the releasing author may inspect other signals or affiliation
results only within their separately authorized view. Being asked to confirm a
release grants no access to other authors' protected bodies, root identities or
assessment inputs. The subject author of each checked signal must consent before
assessment and separately authorize who may see which result fields. The
releasing author's request for context cannot supply that consent on their behalf.

The purpose is to support a human decision about this payload and audience, not
to certify absence of bait. Display `relationship-confirmed`,
`not-found-in-scope`, `indeterminate` and the local `not-assessed` state with their
P015 meanings and coverage/time limits. No badge means no conclusion, not
independence; declining assessment carries no penalty. No finding automatically
changes eligibility, source counts, rankings or publication rights. Any future
counting policy would need its own explicit proposal and acceptance, not a UI rule.

For example, a confirmed employment relationship to the institution may describe
both an interested spokesperson and a whistleblower with direct knowledge. The
interface must not label either as deceptive. It may help the releasing author
decide to proceed or decline under the existing confirmation contract. Absence
of affiliation evidence does not make a coordinated trap safe.

Reuse ADC-008's editor/view, P015-007/008's verifier and result semantics, existing
classification/redaction and authorization owners, and P013-PEX-001 for private
exchange. Host-side read admission precedes projection; UI, Agent, exports,
notifications and other clients must consume the same authorized projection.
Do not add an Agora-indexed affiliation record or public proof field to the
embargo manifest/release. The assessment result has its own narrower recipients;
consent to release the rumor never widens access to that result.

Public labels are excluded from this first profile: even a minimal flag can
identify the sole employee in a small group. Show only authorized granularity;
otherwise withhold the result without exposing a sensitive reason. Respect
P015 expiry, accepted withdrawal and correction through the existing lifecycle
owners. An old signed finding is historical evidence, not a permanent live badge;
already disclosed information cannot be made unseen. Never revive an erased
issuer mapping to refresh a result.

The main trade-off is useful context versus an additional disclosure and trust
concentration. The initial supported relationship/evidence scope and assessor
recusal policy remain P015-007 open decisions. This profile does not introduce
cryptographic protection against the assessor itself, nor does it resolve
collusion or psychological intent. Safe context review remains possible without
affiliation assessment, using material already shared with the deciding author.

## Author Disclosure Condition Tracker {#author-disclosure-condition-tracker}

P035-019 freezes the minimum `whisper-embargo-manifest.v1` proof input before
this runtime: exact authorized publication-use tuple, certified nym key, profile
and certificate digests, case continuity-key digest, canonical public authority
principal and bounded `case/not-after`. P015-005 owns issuance authorization;
LLR-006 owns the case key. The manifest precedes the signal, whose private fields
must match; the receipt attests those checks. This prerequisite does not close
ADC-001's condition/release/amendment contracts or any ADC execution gate.
P035-019 qualified that synthetic detached producer and cold OS-isolated
inspection on 2026-10-29. The witness attestation remains distinct from an
independent hidden-body check; see
`node:docs/audits/ACCEPTANCE-P035-019-2026-10-29.md` for the bounded claim.

All rows are post-MVP `todo` unless marked otherwise. The grouping row closes
only on the composed Story 014 variant run.

ADC-001/005 also freeze and qualify the embargo row of the
[portable verification matrix](../013-whisper-social-signal-exchange.md#portable-verification-profiles):
minimum public proof, exact bindings, numerical byte/item/depth/work limits and
disclosure policy. ADC-005's completion requires a producer/consumer test with
all allowed proof bytes carried, independently admitted local trust and a
network-denying resolver whose fetch counter remains zero. Reuse P032's common
law fixtures and compare evidence-access/accounting helpers with LLR-009 at
whichever implementation lands second. That is a convergence checkpoint, not
an execution dependency of ADC-005 on LLR-009.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| P013-ADC-000 | Story 014 disclosure-condition variant acceptance | todo | P013-ADC-001–008; P057-017; P015 Gates A and B; P015-005; P013-PEX-001; P013-DFR-001–004; P013-DFR-006 | One retained run of the [variant](../../30-stories/story-014-dormant-contest-entry.md#variant-author-disclosure-condition) proves S014-A12–A21 and its assertion-to-task matrix. Canary scans cover queries, Agora, AD copies, notifications and logs. Required cases include receiver verification without private-body retrieval, separate correlator and counting authority, two rooms versus two routes, later-epoch author present/absent, both commit/withdrawal orders, pre-authorized expiry, declined-prompt suppression, lost commit response and restart before AD hand-over. |
| P013-ADC-001 | Freeze embargo manifest and condition contracts | todo | P015 v2 signal; P015-005; P013-LLR-006; P035-019 | Private and single-audience manifest contracts, `whisper-embargo-condition.v1`, `whisper-release-payload.v1` and amendment through `whisper-case-adc-request.v1`; apply the [accepted continuation](#adc-execution-continuation), including hiding commitments and registration bijection; acyclic manifest -> protected signal -> admission receipt construction, one anchor/at most one original condition, identical key/authority/case-lifetime commitments and closed public proof fields. P035 admission verifies their equality, supporting LLR-009's detached anchor proof without a new signature carrier. Preserve original condition identity through narrowing; widening creates a new case without silently withdrawing the old. Explicit authorized holder set; role-bound custody; per-descriptor consent. Golden and refusal fixtures cover offline verification without protected text, forbidden proof fields, substituted manifest/payload/authority/case lifetime, widening, unknown fields and expiry. LLR-006 owns the key contract; this row consumes it. Development component: [reference-only source transfer](#adc-explicit-source-transfer-component-2026-11-18) now binds complete protected consent/payload to the existing S026 owner. [Explicit detached source preparation](#adc-source-custody) binds the signed P035 auxiliary to the same reviewed original. The P036 profile-bound capture and S026 encrypted registration are checked together at the component boundary. Independent-process custody and clean-source runtime qualification remain required. |
| P013-ADC-002 | Grouping rules, descriptors and similarity keys | todo | P013-DFR-001 | Grouping rules in the vocabulary document with typed fields, canonicalization and rendering templates; `whisper-correlation-descriptor.v1`; the domain-separated key derivation with golden vectors; a version bump on every normalization change; warnings for local rules; the breadth choice rendered for the author. Reuse one vocabulary-bound normalization/key function for authoring, notice creation and holder validation; display rendering never feeds the hash, and semantic-model suggestions never bypass author approval. |
| P013-ADC-003 | Correlator custody obligations | todo | P013-ADC-001; S018 | The `whisper-embargo-custody:v1` profile and its advertisement; classification-based refusal on every listed egress surface; bounded custody retention; a canary test for each surface. The native holder gates offers, work admission and local lookup on the current custody deadline independently of maintenance. Component tests cover managed erasure at the signed release deadline and exact receipt replay through the case horizon. Development canaries cover generic Memarium lookup, queries, index projections and backup selection. An exact fenced AD handoff now retires the held copy under its original delivery identity. A holder can recover a signed unused-slot withdrawal through its private proposal query and retire the exact copy. SQLite WSS development probes verified erasure before commit and preservation through handoff after commit. The private held-transfer offer now advertises a signed custody profile and horizon checked by both endpoints. A portable owner statement uses a separately adopted one-way PEX offer and fenced AD delivery to the named custodian. Updated SQLite WSS diagnostics passed both the one-way erasure and the occupied-slot refusal with subsequent exact readback. The counting authority advertises its custody profile and deadline in its signed authority policy. The author checks that policy before preparing keys, and the owner checks its own adopted coverage before holding a key on new registration. Component tests cover the horizon, exact replay and native publication, author preparation and registration. Held authoring also selects each custodian using a sender-bound signed advertisement and a distinct local pin before key preparation and first signing. Component tests cover missing and mismatched selection, insufficient horizons and removal of a pin before signing. Public Agora canaries cover refusal before record, topic and subject readback, SQLite live subscriptions, and Matrix v1/v2 checkpointing without private carrier bytes or record IDs, including nested custody content under open extensions. Component canaries also cover Room, nested custody in outbound Artifact Delivery, Memarium application backup, ordinary model adapters, notification creation and live P086 observation/report boundaries. Full egress qualification remains open. |
| P013-ADC-004 | Counting and attestation | todo | P013-ADC-001; P015 Gate B; P013-PEX-001 | Per-epoch counting with exact original-epoch exclusion and conservative N + 1 thereafter, with author-present and author-absent fixtures and UI effective-threshold explanation. `whisper-embargo-attestation.v1` for proposal evidence, separate `whisper-release-commit-statement.v1` and restricted signer domain for the public committed result, status freshness, publication receipt and counting at commit. The private proposal contract, restricted signing, real owner count and local source verification are implemented alongside the separate public statement and atomic owner publication. The [detached source component](#adc-source-custody) exercises native relayed proposal retrieval and explicit author confirmation against the adopted SQLite counter. Direct source retrieval and source/custody/executor/cold-receiver runtime qualification remain required. Share bounded primitives between full-private and detached-public verifier paths; recipient verification never fetches protected text and explicitly trusts the admitted counter. Independently verifiable counts remain a separate open design. Reuse the contextual contribution evaluator with separate coordination/disclosure policies; qualify permutation/replay parity, duplicate sources and evidence-representative replacement without altering M4. |
| P013-ADC-005-00 | Model, owner and AD prerequisite corrections | done | P013-ADC-011; P013-LLR-011 | Repair exact-absence recovery, audience confirmations, terminal refusal classes, independent retained-original verification and exact AD submission identity; independently specified expected outcomes, axiom audit, actual owner and AD concurrency/restart tests. See [stage-0 scope](#pre-executor-stage0). 80 audited model theorems, 40 vectors, 15636 comparisons including eight independent expected histories, 293 core/owner and 176 AD tests. Executor and full ADC-005 acceptance remain open. |
| P013-ADC-005 | Release execution | todo | P013-ADC-003–004; P013-ADC-011; P013-LLR-011; P070 | Apply the [accepted continuation](#adc-execution-continuation): confirmation/commit/abandonment use `whisper-case-adc-request.v1`, with separate public intent, public commit statement and release contracts. Revise ADC-011/LLR-011 semantics and requalify; historical gates do not transfer. Public statement binds pre-commit intent, not its own final envelope or private owner revision. Qualify all four runtime cells, reserves, exact reply loss and bounded stale recovery. Before long-lived enablement, qualify AD identity-namespace retirement and renewal under the 4096-reservation lifetime cap. Slot/logical release id binds original condition and canonical audience digests; Agora record/id remains content-addressed. Same room/two routes uses one slot; two consented rooms use two; unauthorized room refuses. Atomic count/consent/slot acceptance, both commit/withdrawal orders, pre-authorized withdrawal/expiry after attestation, per-request outcomes, exact-byte replay, lost reply and crash before AD hand-over; AD unknown never means absent. Abandonment leaves the slot consumed. Offline recipient package verifies without the protected signal; closure evidence follows Story 014. Use LLR-008's acceptance owner; P013-LLR-011 owns durable enablement of these control operations and the shared prepared-output recovery laws; no parallel embargo case database or AD retry loop. After the ADC-011 model gate, compare new Rust behavior against the pinned model and qualify actual owner/AD crash boundaries; model proof alone does not close this row. The explicit source-to-S026 transfer, role-closed S026 author-control signing, atomic public/private owner publication, private slot receipt recovery, and fenced preparation of the commit and release envelope are implemented as local components. The detached package verifies under independent local trust in the cold component test. The reserved AD handoff, exact outcome recovery and signed abandonment run in the local component fixture. Settlement uses the dedicated P037 node signer and an exact journal locator fenced with the signed claim and reply key. Renewal replaces the locator atomically and authenticated replies remain bound to the current exchange. Native registration retains the authority key and now supplies the [signed registration policy](#signed-registration-policy) required by the executor. The [local withheld preparation and relayed PEX v1 commit handoff](#source-local-withheld-preparation) compose the source, executor journal, private relay and owner result. The native release operation fences the signed Agora envelope before exact local AD admission. The independent SQLite HTTP and Matrix receiver gates resolve locally adopted audience, destination and witness policy before accepting the carried proof. The Matrix origin durably pins the approved physical room and exact carrier before dispatch. Direct PEX v2 proposal retrieval uses the same retained offer and ordered inbox as other case controls. Direct commit handoff retains the signed offer in the executor journal and uses the bound peer reply path. The native withheld component composes Memarium, source and executor journals, an independent authority commit, exact local AD admission and cold SQLite-backed proof verification at fixture relay ingress. The SQLite HTTP development probe publishes the retained bytes through the real AD Agora adapter and verifies an authenticated readback from an independent SQLite receiver. A second development probe sends registration, proposal, author confirmation and commit through a stock WSS/INAC courier and verifies publication and readback at the independent SQLite receiver. The source enters through the authenticated operator HTTP route and checks the token and binding refusals. The relayed v1 settlement probe confirms early refusal, AD tombstone, exact handoff replay and authenticated operator readback over WSS/INAC. Direct v2 offer replay is tested at the component boundary. The executor also retains authenticated closure for the exact abandonment exchange and projects unresolved-at-closure without a new release handoff. The held handover component prepares and verifies the private registration acceptance and selected audience for a named custodian. The held PEX codec now transports those exact bytes under a separate purpose in component tests. The recipient recovers the exact signed held offer from its separately fenced store. AD guards the binary and inner labels while the recipient is disabled. Memarium has an owner-local held payload store with separate fencing, exact recovery and managed key erasure. The held receiving adapter commits the exact verified PEX package under current local obligation and recovers its receipt without an unexpired offer. The daemon adopts the held receiver explicitly, prepares offers locally and checks the authenticated minimal-trace carrier. The separate-node held WSS development run exercises actual AD handover, custodian proposal and execution, author confirmation and exact publication readback at independent SQLite Agora. Native developer runs for both Synapse custody modes verified forwarding and exact independent Agora readback. The shutdown trace exposed an HTTP sync worker race. Both SQLite WSS/INAC custody runs verified durable delivered readback, the carried release-envelope privacy checks and authenticated process shutdown. Agora cancels long polls and retry waits before joining its Matrix workers. The intermediate native Synapse run completed delivered readback and authenticated shutdown in both custody modes using a shortened sync timeout. An isolated WSS/INAC actor now samples local durable commit, exact AD admission, tombstone and retained settlement on one monotonic clock. Both SQLite publication scenarios passed with separate timings for the pending fence, SQLite commit and committed fence. A subsequent development run on native Linux passed both Synapse custody modes with the ordinary 30 s sync timeout, independent delivered readback and authenticated exit. Both SQLite custody modes passed again after the held payload deadline change. Formal latency sampling and the remaining ADC-003 egress surfaces are open. All four formal matrix cells remain open. |
| P013-ADC-006 | Context-join proposals | todo | P013-ADC-002; P013-DFR-004 | Content-free `whisper-context-join-proposal.v1` from correlators to candidate authors, only under `keyed-and-confirmed-joins`; acceptance authors a related signal in the target context; model output stays advisory. A fixture proves that no context merges without the candidate author's act. |
| P013-ADC-007 | Optional public correlation notice | todo | P013-ADC-002; P013-DFR-002; P015-005 | `whisper-correlation-notice.v1` is signed under an explicitly admitted publication tuple, content-free, expiring and discoverable through the term bucket. The editor warns about disclosure of the matter. Related signals point to the public notice record/id with a closed target kind; no hidden signal id is required or leaked. Tests refuse wrong kind/schema/topic/scope tuples and verify a notice-only reader can author a related signal. |
| P013-ADC-008 | Author condition editor and status | todo | P013-ADC-001–002; P013-DFR-003; P057-017 | Render N and its effective epoch threshold, public criterion and proof disclosure, window, concrete audiences, mode, authorized holders, notice and coordination participation. Keep condition, proposal and per-slot execution states separate. Declining suppresses that proposal across restart; no renewed prompt without an explicit retry or consented bounded policy. Show widening as a new independent case and withdrawal as effective only after authority acceptance. |
| P013-ADC-009 | Sealed pre-threshold confidentiality | deferred | P013-ADC-004; cryptographic review | A mechanism in which no correlator can read protected material before N sources exist, for example threshold or escrow-style encryption. It needs a separate, proposal-grade review. |
| P013-ADC-010 | Optional private affiliation context at disclosure confirmation | todo | P015-007–008; P013-ADC-008; P013-PEX-001 | Reuse the bounded result verifier and one host-authorized projection for UI/Agent and other consumers. Acceptance includes separate consent by the checked author, no-consent/unavailable paths with no penalty, no access to protected peer bodies, employee-as-whistleblower and employee-as-interested-party cases without an intent verdict, limited coverage/expiry, swapped-result refusal, small-group identification risk and no leakage through Agora, release proof, exports, logs or notifications. Existing counts and release authority stay identical with the feature absent, refused or unavailable; authorized context informs only the human confirmation decision. Offline synthetic fixtures qualify semantics without claiming live affiliation verification; private delivery composes the separately qualified P015-008 path. |
| P013-ADC-011 | Lean release-ordering model before ADC-005/LLR-011 / Whisper domain owner | done | S027-009-06 pilot review; P013-ADC-001/004 contract freezes; P013-LLR-008 contract | Meet the [model gate](#lean-release-model): reviewed executable state/assumption map, checked reachable-history proofs for consent/order/narrowing/slots/replay/handoff/successor preservation, positive witnesses and guard-mutation counterexamples. Reuse S027 proof discipline and existing case laws without sharing domain authority. Pin contracts, model/toolchain and existing Rust fixtures; the subsequent LLR-011 owner comparison/qualification is separate, and ADC-005 executor/AD qualification remains open. No dependency on their completed runtime, no alpha expansion and no change to historical qualification. |
