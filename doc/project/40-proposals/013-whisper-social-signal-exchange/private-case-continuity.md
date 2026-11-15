# Private Case Continuity {#private-case-continuity}

Decision date: 2026-11-06. Scope corrected 2026-11-14 after evidence review:
direct Gate A is qualified; Gate B has a qualified bounded subset. LLR-008
is **partial** pending the independent replacement Gate B campaign (LLR-012).
Owners: P013-PEX-001, P013-LLR-001/008/007/012
and the S023-001 route profile. The decision alone is not runtime evidence.

Current evidence: `node:docs/evidence/private-case-continuity/2026-11-14-ordinary-gate-b/README.md`.
Loose, pooled, extracted and fresh both-store qualification agree for the
measured subset, not every original Gate B requirement. See the
[scope correction](#gate-b-scope-correction-2026-11-14). Historical
checkpoints below retain their original observation-only scope. Production v2
issuance, detached ordinary anchors, LLR-009/010/011, S023-002 and global readiness
remain separate.

## Executive Summary

A named recipient receives protected Whisper material through AD/INAC. An author
explicitly opens a case anchored to an admitted signal, then continues that case
under a current nym when an action requires it. Private delivery, historical
admission, accepted case history and current authorization are independent facts.

Gate A qualifies private exchange independently. The observed Gate B subset
qualifies opening and succession on SQLite and Synapse, with restart and replay.
The remaining acceptance obligations below keep the complete gate open. A Synapse
anchor-unresolved refusal does not substitute for its positive path.

Based on the [P013 domain map](../013-whisper-social-signal-exchange.md),
[LLR owner](long-lived-rumors.md), [P015 contextual authorship](../015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md),
[S023 Artifact Delivery](../../60-solutions/023-artifact-delivery/023-artifact-delivery.md)
and S026 case-key custody. Voluntary disclosure, privacy and accountable authority
are preserved as concrete recipient/scope checks, explicit consent and replayable
outcomes; transport success confers no domain permission.

## Context and Problem

Existing host authoring already prepares an exposed case commitment before
preview and binds exact signed bytes before returning them. Custody qualification
used a disclosed synthetic v2 certificate; it does not establish real case
succession. The ordinary v1 issuance path and P015-004's WhisperV1 verifier must
compose in Gate B without fixture-only signing authority.

At decision time the Matrix relay had no portable admission-store adapter, and
authoring coupled case retention to issuer identifying-data retention. The scoped
A/B implementation below resolves these gaps without changing historical claims.

## Adopted Model

### Four independent periods and opening

Certificate validity belongs to P015. Record/proof retention belongs to the
respective P036/local custody owners. Counting belongs to Whisper. Consent belongs
to its particular operation owner. No period extends another. Counting cannot
outlive its evidence. Succession does not renew consent or counting eligibility.

The authority publishes a signed policy declaring scope, maximum case horizon,
history limits, status freshness and supported operations. P091
`whisper/case-authorities` admits exact authority identity and policy digest;
policy updates do not rewrite existing commitments. Missing admission refuses.

Opening is an explicit new-case intent. The reviewed not-after is the minimum of
the requested deadline, authority guarantee, record custody guarantee, proof
custody guarantee and key horizon. Missing guarantees refuse before key exposure;
issuer identifying-data retention is not a custody guarantee.

The host durably prepares Exposed, includes the complete case tuple in preview,
stores the exact signed author bytes, binds their digest and only then releases
them for admission. Preview expiry does not erase an exposed key. UI lists exposed
unbound keys and offers explicit abandonment. Repeated operation IDs cannot mint
another key. Original signed records cannot acquire commitments retroactively.

Exact author bytes may use any representation admitted by their Agora carrier.
Custody and case verification must not require JCS on that buffer or reserialize
it to read case fields. Strict bounded JSON, record signature/identity and receipt
byte bindings still apply; signed metadata keeps its own canonical contract.
Full PDU source buffers keep the independent Matrix verification rules.

The case anchor is the digest of exact signed author bytes admitted with
`agora-admission-receipt.v2` for current source adapters (v1 remains a historical
reader contract); the protected PEX signal is a separate case artifact.
A local time-only receipt or Matrix timestamp is insufficient for LLR-002.
Opening needs a positive historical admission result and acceptance by the
committed, independently admitted authority. Revision zero is the original anchor.

### Private exchange and recipient keys

Reuse P015's cryptographic key-offer mechanism beneath closed family adapters.
Do not reinterpret council-bound `nym-exchange-key-offer.v1` as a generic recipient
offer. PEX has a recipient-signed adapter binding purpose `whisper-pex`, family,
exchange identity, recipient/reply keys and expiry (at most fifteen minutes and
no later than exchange expiry). P091 admits exact recipient identity and role.
Labels never derive recipient keys. Keep P015 wire bytes and signing domains.

The source commits its random exchange and reply key before requesting the offer.
It then binds the exact canonical signed offer in its existing encrypted workflow
metadata. A changed valid offer is a conflicting preparation, not a retry. A
prepared unoffered exchange cannot switch profiles. Restart and lost response
preserve the original reply key, offer identity and prepared ciphertext. The
shorter of offer, native-control and original request deadlines governs effects;
no layer extends another's lease. Direct and historical relay preparation are
explicit alternatives without fallback. A retained signed result remains a
historical read after the exchange lease, under current disclosure policy.

Direct source adoption names the exact recipient/family and configured AD route;
it cannot overlap the historical relay posture for that same pair. Handoff binds
an absolute transport lease and exact target inside AD's existing idempotent
owner, independent from domain admission. Recovery cannot turn it into a fresh
relative timeout or redirect it under a remapped named route. Active custody
retains the encrypted original input; terminal compaction removes the lease with
that input. Previously transferred custody obeys current AD route/outbound/egress
grants; withdrawing only the source role cannot rewrite that separate fact.
The direct response receiver binds the authenticated peer to the saved recipient
and offered exchange before opening the original reply key. Relay and direct
responses cannot be substituted. Neither transport custody nor a protected frame
claims a processed command, open case or current permission.

Encrypt before any AD custody. Outer transport correlation is independent random
data; private anchors, nyms and request digests stay inside ciphertext. AD alone
owns transport retry. Domain outcomes are durable before reply handover; readback
never repeats a mutation. Exact request identity binds saved bytes. Authenticate
before exposing an outcome or reserving an idempotency key.

S023-001 is an explicit route property: inac-direct only, inline only, at most
65536 bytes for the complete sealed artifact, no peer artifact cache or generic
object-store payload. After acceptor decision, AD retains reduced delivery/admission
outcome metadata without domain correlation. Active retry retains the necessary
ciphertext. Logs, notifications and observers contain neither body nor nym links.
Large evidence is independently available verified local material; PEX never
silently fetches it or bypasses the inline limit.

Gate A has two production consumers: protected-signal custody and a domain inbox
that persists exact case-request bytes and returns transport-accepted/owner-pending.
Gate B attaches the authority to that inbox without changing delivery semantics.
Authorized domain custody is distinct from AD's reduced transport ledger.

The first protected-signal payload profile is exact signed `agora-record.v1`
author bytes with private-correlation/direct `whisper-signal.v1` content, not an
additional JSON wrapper. Its offer label is `whisper-protected-signal.v1`; its
closed PEX family is `protected-signal`, custodian role and 48-KiB plaintext
ceiling. It is one-way and acquires no response key or authority-command role.
The complete frame remains within 64 KiB and never enters the historical relay
resolver. Existing contextual v2 content excludes private-correlation and is not
silently widened. Its public anchor remains a separate admitted artifact.

Memarium may preserve the original encrypted frame and signed offer in its
reserved Personal fact journal, with independent current peer/record admission,
original finite local read deadline and exact storage idempotency. No plaintext
record store or second retry queue is permitted. Such custody grants no portable
admission, guaranteed future key access or additional opening horizon. Recovering
author bytes still requires the authorized original recipient key; loss refuses.
Local read expiry does not claim purge of filesystem copies or retained keys.
Native offer/current-policy adoption and actual transport must qualify together;
standalone journal tests do not complete Gate A.

S023-002 purge is separate. The recipient sees the INAC sender node; metadata and
timing correlation remain possible. No anonymity or forensic-erasure claim follows.

### Admission on SQLite and Synapse

Compose the existing portable admission producer and local indexing for both
backends. Matrix admission binds exact author bytes, the actual local admission
decision, its policy/evidence and the observed Matrix source. A receipt is not a
wrapper around origin_server_ts. The original Matrix time policy remains
`authenticated-admitted-homeserver-v1`; the explicitly admitted portable witness
now verifies and retains its original full PDU/key/admission material. Acceptance
also checks the separate server export. The witness adds portability, not an
independent guarantee of the homeserver clock. Missing evidence, nonfinal
admission or changed bytes gives anchor-unresolved.
Replay preserves the original decision/material and never invents historical time.

### One case authority

The existing `whisper-core::case` owns pure typed transitions, opening horizons
and history-page verification; `whisper-case-service` owns durable acceptance,
the AD acceptor and S020 maintenance. These concrete owners replace the initial
planned whisper-case-core/whisper-case-authority-service package names after
integration on 2026-11-07. Daemon only composes. Reuse S028 and storage::owner_checkpoint, issuer
prepared-result laws and the authenticated-head comparison beneath StatusCursor;
do not import issuer-specific custody or create a parallel ADC state store.

A request names anchor and request ID, not a client-assigned history revision.
Acceptance binds its digest, assigned revision, previous accepted digest and
explicit evaluation inputs. Authenticate first. In one durable transaction append
the accepted event, update head/projection and save the exact result. An exact
duplicate returns that result even after later withdrawal; changed bytes conflict.

Evaluate/sign outside the write transaction, then recheck head and evidence with
CAS before commit and exposure. Signer audits cannot expose signed losing
candidates. Losing CAS discards the candidate and reevaluates. A contradictory
signed acceptance observed by a recipient cannot be excused as an internal draft.
A Clock port with durable high-water and independent rollback witness governs time;
restoring the same database alone must not restore authority. No ambient now_utc.

Status is fresh for 300 seconds. Refresh at an unchanged accepted head is not
equivocation. Missing/stale status defers effects. Known closure or a newer
succession wins over an older still-fresh status. Incomplete chains are unavailable,
not empty active cases; conflicted is reserved for contradictory accepted history.

The fold has typed amendment, withdrawal, confirmation, closure, succession,
release-commit and abandonment transitions. ADC operations have no production
route/capability in this slice. Exercise both withdrawal/release orders against
the actual transactional owner as conformance, not runtime disclosure evidence.

### Lazy succession

Use P015-004 and S026 keys, not another signature verifier. Both roles sign one
validated preimage. Successor stays in the original context/profile. The first
predecessor is anchor-author; later requests name the effective successor. In
concurrent A-to-B and A-to-C, the first accepted wins and the other receives
stale-predecessor, not conflicted. Ordinary amendments preserve the successor.

There is no periodic succession. Prepare it only for an explicit action when the
current successor lacks a valid certificate. Allow at most 64 accepted successions
per case and four in the rolling previous 24 hours (the left boundary is excluded).
Duplicates consume no quota; quota exhaustion cannot prevent closure or readback.
Certificate expiry emits no case event: status still names that successor while
current action authorization fails. UI says successor-without-current-certificate.

UI is usable without JavaScript, uses POST/CSRF, preserves the exact document on
423 and requires another review after expiry. Show audience, accumulated disclosed
links, status freshness, delivery and acceptance separately. A private succession
links nyms to its audience; it grants continue-case only, never source merging,
reputation, additional threshold contribution or human-identity proof.

### Initial wire boundary

The canonical additions are whisper-pex-key-offer.v1 and
whisper-case-authority-policy.v1. PEX reuses the existing authenticated binary
whisper-private-exchange-header.v2. The unused JSON whisper-pex-sealed.v1 draft
was superseded before any runtime consumer; its original Git bytes remain historical. Their examples are shape fixtures, not valid
cryptographic exchange or usable recipient keys. Runtime verifies canonical
base64url, key digest, X25519 non-low-order keys, independent admission, signature,
exact offer/envelope binding and time. Key offers live at most 900 seconds.
The offer signature uses `orbiplex.whisper-pex-key-offer.v1` followed by NUL and
JCS of the document without signature.
For the direct offered profile, derive a 32-byte HKDF-SHA256 intermediate from raw
X25519 agreement, with salt equal to the UTF-8 exchange handle and info equal to
`orbiplex.whisper-pex-offered-key.v1`, NUL and the UTF-8 `sha256:<base64url>` digest
of exact canonical signed offer bytes. Apply the existing binary PEX family/header
key schedule to that intermediate. The verified offer must already be exact JCS.
This binds independently admitted peers, purpose, reply key and original lease
cryptographically; another valid offer with the same key/exchange/time is not
interchangeable. Historical unoffered traffic keeps its original schedule.
There is no offered-to-unoffered decryption fallback.
 The policy domain is
`orbiplex.whisper-case-authority-policy.v1` followed by NUL and JCS without signature.

Offer role binds case-authority, protected-signal-custodian or case-applicant;
reply delivery requires its own admitted recipient offer. PEX family names are
closed. Runtime must reject role/family mismatch, same-key unsafe constructions
and use outside the named exchange. No body or private case correlation is an
outer field. Ciphertext string validation does not establish the 65536-byte
complete framed-artifact limit; runtime checks the complete bytes before
AD handover and before accepting/decrypting.

The authority policy binds a federation and exact source profile, not one private
anchor. Initial host/service support is open/succession/closure only; ADC remains
without a route. Max history is 4096 accepted events, max active cases 1024;
a policy may lower either bound (history at least 65 to accommodate 64 successions
and closure). Succession and freshness constants cannot be relaxed by policy.
Durable owner storage must reserve closure capacity before accepting operations;
full capacity cannot prevent closure or readback. Policy duration uses checked
arithmetic; JSON number validity alone proves no feasible custody horizon.

## Trade-offs and Exclusions

Named recipients learn sender-node identity. Admission and case authority are
separately trusted roles. Private-only anchors from a new case time authority,
S023-002 purge, LLR-009 portable presentations, LLR-010 context transitions,
automatic recontact, Anon and ADC execution remain outside this contract. Key loss
has no invented authority recovery; explicit existing opt-in custody recovery is
separate. New unlinked cases remain possible. Global Whisper/Agora stay partial.

## Failure Modes and Qualification

Gate A requires real two-node AD/INAC signal and request/reply, both acceptors,
wrong recipient/key/purpose/signature/scope, expiry, duplicates, changed bytes,
lost replies, restart/replay and non-inline/oversize refusals. Inspect DB/WAL,
cache, object stores, logs, SSE and notifications by access class. Separate private
domain custody from prohibited transport plaintext. No public fallback is allowed.

The original Gate B contract required the full matrix below. Review found that
its 2026-11-14 report proved a smaller subset. The following correction is adopted
**now**, after that run; it does not claim prior approval or reclassify the frozen
observations. LLR-001 and LLR-007 retain their bounded completed scope; the full
case-state milestone LLR-008 remains partial until LLR-012 is qualified.

### Gate B scope correction 2026-11-14

| Original obligation | Evidence class and current disposition | Reason / owner |
| --- | --- | --- |
| Ordinary certification, preview/prepare/bind, positive anchor, A-to-B-to-C, restart/replay | Observed runtime on SQLite and one stock Synapse homeserver | Original full-record records, exact author bytes and source-bound receipts are retained; real sync and full PDU verification remain mandatory for Matrix, with separate Node/homeserver gates. |
| Expired predecessor | Observed runtime: SQLite B before C; Matrix A before B | These are distinct measured transitions, not both expiry positions on both backends. |
| Competing A-to-B/A-to-C; closure versus succession/retry | Transactional-owner conformance; no live concurrency claim | Deterministic ordering/fencing tests are the reliable race witness. LLR-012 must identify both orders by named tests. |
| Lost commit reply after later state change | LLR-012 runtime follow-up | Cached restart reads alone do not prove this scenario. |
| Missing/stale status, older head, bad attachment, case horizon | Native historical readback for SQLite only | Controlled evaluations are not new HTTP refusals. Matrix equivalents belong to LLR-012. |
| Status rollback, equivocation, missed closure, unchanged-head refresh | Owner/recipient conformance | Preserve exact named tests and test counts. No inferred live status coverage. |
| Unbound exposed-key inventory and explicit abandon | LLR-012 runtime follow-up through POST/CSRF | Preparation conformance does not prove the operator flow. |
| Key loss, erasure and recovery opt-in | Custody conformance; LLR-012 coverage audit | No physical erasure claim; missing named witnesses stay open, never inferred from an export. |
| Missing Synapse receipt, anchor unresolved | LLR-012 runtime follow-up | A positive receipt does not prove absence refuses without timestamp fallback. |
| Closure / sticky terminal knowledge | Observed SQLite closure plus native cold readback only | Matrix closure remains LLR-012 runtime follow-up. |
| Live SSE privacy | LLR-012 runtime follow-up | Gate A remains historical; capture fresh B-prime streams. Source comparison cannot replace them. |
| Amendment preserves succession | Pure-fold conformance; durable path LLR-011 | No enabled ADC route or runtime amendment claim. |
| Complete clean-source capture producer | LLR-012 provenance requirement | Product commits were clean; the private capture programs were not in those commits. |

Real v1 issuance and host signing remain mandatory; synthetic v2 cannot close B.
Restart/replay must not resend, re-sign or perform commands again. The correction
changes evidence classes only where stated; it does not weaken domain invariants.
Runtime cases retain their own process/HTTP observations. Conformance has no
invented HTTP success. Quota edges, clock rollback, pre/post-CAS interruption and
ADC race laws remain conformance; ADC production routes remain LLR-011. A
controlled-clock evaluation is not a long-duration observation.

The Node review,
`node:docs/audits/PRIVATE-CASE-GATE-B-SCOPE-2026-11-14.md`, provides the backend
matrix, recovered capture provenance and exact limits.
Frozen reports and external references are unchanged. A qualifier's `qualified`
result attests its predicates, never completeness of this entire contract.

### LLR-012 independent Gate B campaign {#llr-012-independent-gate-b-campaign}

**Adopted 2026-11-14; implementation and qualification pending.** Campaign
`P013-LLR-012` is the independent basis for closing Gate B and LLR-008. It
repeats ordinary certification, authoring, registration and case continuity; it
does not combine new observations with the historical bounded subset to fill
missing witnesses. Gate A, the old subset and its private-source capsule retain
their exact historical bytes, tool pins and limitations. Durable ADC remains
LLR-011. A passing LLR-012 closes LLR-008; it does not close future ADC
operations.

Freeze a versioned requirement inventory before capture: requirement, backend,
phase, result owner, evidence class, source observations and qualifier
predicate. Runtime, native historical readback, conformance and named
follow-ups remain separate. The qualifier computes coverage from bound
witnesses, not backend names or a producer's claim. No missing witness may be
supplied by prose.

SQLite and stock Synapse use independent runs with fresh actors and separate
issuer, authority, Vault, AD and projection state. Within one run, roles may
share a process only with separately retained key identities and adopted
policies. Actual v1 certification and host signing remain mandatory. Fixture
confidence is 0.5, recorded in the pinned scenario rather than imposed on
product authoring.

#### Scenario order and result ownership

Registration creates head 0; A-to-B creates head 1; B-to-C creates head 2. Each
backend records that sequence and independently observes heads `[1,2]` for cold
readback. Source/key/audience identities come from the actual actors.

1. Certify A, explicitly preview a new case, then prepare, sign, bind, admit,
   obtain the portable receipt and register the case.
2. Accept A-to-B and discard the local author-workflow response body. SQLite
   also waits for A's certificate to expire before that succession.
3. On both backends, wait for B's certificate to expire, then accept B-to-C
   under C's valid current certificate.
4. Read/retry the original author operation: exact A-to-B result, without a new
   PEX/AD handoff. Changed input under its ID refuses. Include the original
   result in exact post-restart readbacks.
5. Submit new A-to-C under a new ID: `stale-predecessor` with
   `retry` equal to `evidence-change`; head, current succession and accepted-succession count
   remain unchanged, with no acceptance event. The vertical development run
   establishes whether ordinary API preparation or authority acceptance owns
   that refusal, then freezes the exact path before the campaign. Do not bypass
   the API to force authority execution. If authority owns it, retain exact
   refusal readback too. New A-to-B after B expiry is not this control: its
   successor-certificate check would fail before predecessor evaluation.
6. Refuse abandonment of the bound case key, restart/replay without new
   signatures, sends or command effects, then perform closure as the last case
   mutation. Only reads and recipient restarts follow; older Active material
   cannot undo sticky terminal knowledge.

`http_loss` discards the body returned by local `AuthorWorkflow`, not a
transport packet or an authority command. Resuming its sealed operation reads
the original result. The AD ledger must show no new handoff to authority.
Authority `replay_request` is a separate conformance/previous Gate A law, not a
claim made by this fault injection.

Use a separate Synapse anchor while the coordinator explicitly withholds its
witness step. Before and after restart, the same author preparation refuses for
missing proof. `anchor-unresolved` names the scenario, not a new wire enum or a
persisted authority decision; the inventory pins the existing typed refusal. A
malformed request is not a missing-proof witness. Check no new signature/nonce,
PEX/AD handoff, case/history entry, acceptance SSE event, key exposure or P036
reservation. Matrix time cannot replace the absent receipt. Run the witness and
open the same anchor under a new ID as positive control; document existing
old-ID semantics without adding durable refusal. Existing S026/P036 lifecycles
remain.

After the main public opening and before main registration, use original A
for the separate controls. They must not publicly expose a private successor B
or C. A separate exposed, unbound preview on each backend survives restart and
appears in inventory. UI POST without CSRF refuses without S026/P036/inventory
effects. A valid POST abandons it: S026 erase fact, P036 opening-release fact
and absence from active exposed inventory. These are two owner effects, not one
transaction; empty inventory alone does not prove release. Bound-key
abandonment refuses without erasure or release. Named conformance covers
interruption between owner effects and safe retry. No physical block-erasure
guarantee is inferred.

Scenario data declares phases, dependencies and each credential's last use.
Compound preflight includes expiry waits, issuance/status, requests, restart,
replay and closure, while intentionally expired predecessor certificates need
cover only their legitimate uses. Build/setup precedes short credential
windows. Preflight neither extends credentials nor replaces owner
authorization. Full-phase budgets include all certification work. A separate
measured post-issue response tail starts at the actual issue time and is checked
after every issue/renewal; it never extends the original certificate. Two
separate backend processes each receive 256 MiB of the existing 512 MiB combined
live-SSE allowance.

#### Shared abstractions before the capture producer

Follow Node's reusable-data-abstraction and convergence rules. Start with the
curated reuse index, inspect concrete callers and compare operations, laws,
effects, errors, identity, authority, lifecycle, cost and dependency direction.
Two uses warrant consideration, not automatic extraction. Prefer an existing
owner, a small function or an explicit representation adapter.

Review and implement suitable sharing for version-bound workflow reads/body
loss, SSE inspection separate from Gate A topology, per-backend privacy-surface
inventories, named Cargo/Python test outcomes and phase/deadline calculations
using existing preflight. Migrate real consumers and preserve their
contract-law regressions; do not leave unused generic APIs or build a universal
scheduler. Keep author results, authority decisions and AD idempotency
separate. Share value scanning beneath logical snapshots and raw files, not
their completeness laws.

Keep the full status observation journal separate from a bounded owner proof
snapshot. The existing EvidenceBundle and carried-presentation limit is three
attached statuses; the native completeness evaluator's merged limit of seven
includes local facts and does not increase the wire limit. A new snapshot must
retain every receipt/closure-pinned whole status and its explicitly acquired
current status, or refuse for missing dependencies/capacity. No signed document
is truncated and no acquisition fact is deleted to fit that snapshot.

The journal preserves original current-acquisition outcomes and their order for
one local verifier, separately from historical proof dependencies and another
owner's observations. Qualification binds those outcomes to retained API facts
and applies the existing nym StatusCursor laws to all supplied signed current
claims, including unselected claims. This grants neither a fresh lease nor a
completeness claim by itself; the qualifier must independently establish journal
coverage. Historical embedded statuses are not new acquisitions. These are
representation boundaries within LLR-012, not a new status or receipt policy.

Each material candidate ends in implemented consolidation, documented
intentional separation or an owned follow-up with a revisit condition. Update
the reuse index only for inspectable existing constructs. Repeat this review at
closeout and check that sharing reduced coupling and preserved diagnostic
clarity.

#### Privacy, conformance and clean capture

Freeze canary source roles and access classes before runtime, not unknown
future random nym values. The closed LLR-012 profile derives eight actual
canaries per backend after capture: main anchor, public nym A, private nyms B/C,
A's primary participant and node, its primary did:key public-key fingerprint,
and the public signal text. Bind every value to the exact source evidence;
unrelated literals or empty minimum scan sets refuse. Preserve all sixteen
semantic bindings when values coincide; deduplicate scanner patterns only.

Public HTTP, fresh browser SSE and both original/export PDU buffers forbid main
anchors, private B/C nyms and primary identity values across both runs. The
separate Matrix control anchor is an additional source-derived scan pattern. Public A
and the public signal text remain permitted on those public surfaces. Opaque
transport custody and operational logs also forbid A and that text. The private
owner's legitimate knowledge has a separate access class, not a public-privacy
claim. This does not renew the historical Gate A protected-text PEX evidence.
The selection declares the fixed policy; it cannot supply replacement values
or weaker access rights. Runtime-derived values are re-bound independently by
the offline qualifier before native work.

##### SSE exposure correction, 2026-11-15

Before the new FULL campaign, distinguish the daemon's operator control stream
from the actual Node UI browser projection. `/v1/events` uses the daemon control
credential and contains whole health/component snapshots and peer diagnostics.
The local operator may see primary participant and node identities there.
Preserve the complete raw streams as operational evidence; main/control
anchors, nyms A/B/C and the public signal text remain forbidden. An ordinary
module credential gives no authority to read this stream, including when it
accompanies an operator credential. The HTTP owner must enforce that boundary.

`/app/events` is a separate, participant-session-protected Node UI projection.
Its server consumes the control stream and forwards a closed wake-up event
vocabulary with empty JSON data. Capture that actual browser endpoint with
its own readiness, restart, real-event, phase and completion witnesses; scan
its original bytes under the public canary minimum. Reconstructing a safe
projection from archived control frames does not supply this witness. Empty
streams and raw control activity cannot replace real browser activity.

Process readiness and participant-session readiness are distinct. Retain every
owner generation. The raw subscription starts at process readiness; the browser
records an actual locked response and activates only after an observed ordinary
unlock, before the next signing or case action. The observer does not unlock
the participant or turn authentication, dependency or transport failures into
readiness. A generation stopped before its successful browser barrier remains
incomplete. Preserve the original locked-sign refusal, then use the normal UI
unlock and CSRF boundary before the browser barrier and signing retry. Exact
readiness attempts and the unlock fact bind that transition to its generation.

This is a correction before fresh capture, not a retrospective relabeling of
historical evidence or removal of a privacy requirement. Raw operator and
browser streams retain distinct fixed classes, both are scanned completely,
and archive metadata cannot weaken their rights or omit a generation. Work
budget exhaustion remains a refusal and leaves the corresponding row open.

Both backends retain complete
logical AD/INAC/notification tables, including history, outbox and tombstones,
and passive schema through `ordinary_ledger.observe` read-only WAL snapshots.
Views, virtual tables and unknown schemas refuse. Scan all non-database data,
cache and log files after stopping actors, including rotated logs, public HTTP,
full PDU evidence and fresh SSE. Each file is scanned or explicitly inventoried
as omitted; keys/recovery bundles are excluded with class and reason. Physical
DB/WAL pages remain S023-002, not an unrecorded exception to this gate.

Scan raw values and declared base64/base64url, hex, JSON-escape and
canary-digest representations, charging every occurrence. Retain the exact
scanned material through P035-011. Measure work/time/bytes in the development
vertical; freeze limits with margin before full capture. Exhaustion preserves
refusal and leaves the row open, without sampling or later scope removal.
Authorized recipient knowledge and public disclosure remain distinct
access-class predicates.

Fresh SSE has readiness barriers before effects and after restart, expected
real events, continuity and completion/truncation checks. An empty stream does
not prove privacy. Capture all other required process, request and response
witnesses per case; controlled faults are labeled as such.

Conformance rows identify concrete commands and test names. Each must appear as
executed `ok` in captured output: ignored, skipped, filtered or missing tests
give no credit. Preserve both race orders, authority replay, status rollback
and equivocation, missed closure, unchanged-head refresh, limits, clock
rollback, CAS interruptions, custody/erasure/recovery and pure-fold amendment
coverage. Native reads with selected evaluation times do not become runtime
HTTP refusals.

The configurable producer, scenario, dependencies, binaries and offline
qualifier are pinned to clean committed sources before campaign execution.
Private config is closed data with secret handles, no executable logic; its
retained semantic digest excludes secrets and private paths. Map every
private-source step to a committed/reused step or justified omission. Vertical
outputs are development material only. Preserve ordinary
signing/unlock/recovery guards. Dispose only owned processes; export and retain
Synapse PDU before tearing down its container.

A qualifier change after capture requires reason/diff review and renewed loose,
extracted and both-store fresh qualification. Changed runtime or unavailable
observations require a fresh corresponding capture. Never relax an assertion to
make an observed candidate pass.

#### Retention decision and closure

This decision explicitly replaces the old area's 64 KiB history allowance with
128 KiB. First publication adds at most 56 KiB of unique Git blobs; the
campaign's entire new control history, including replaced versions, stays at
most 64 KiB. Count history and staged blobs, including README/index changes,
not just the final tree. Intermediate controls stay in private campaign
scratch; publish final controls once after qualification/review. The
policy-control-history allowance remains 500000 bytes. Re-measure all aggregate
margins before runtime/publication.

One combined positive set for both backends uses P035-011 with XZ dictionary
128 MiB and stays within 16 MiB. Each refusal capsule stays within 1 MiB;
refusals stay within 4 MiB per campaign and profile, including previous
campaigns of that profile. A new campaign ID does not reset the profile budget.
Measure current refusal use and the vertical's forecast before full runtime. No
sampling, campaign splitting or silent budget increase follows an overrun.

Loose qualification, safe extraction and fresh retrieval/qualification from
both adopted stores must agree. Retain exactly the qualified material, without
keys, recovery bundles or physical owner databases. Read current
retention/retirement contracts; record owner, classification, inventory/hashes,
dependencies/holds, minimum retention and restoration/replica facts. Unknown
remains unknown.

Owner decision, 2026-11-14: the necessary exact logs, cache artifacts and
observations containing private filesystem paths may use an operator-only
LLR-012 retention scope in both adopted private stores. Content audit must
exclude keystores, keys, tokens, passwords, recovery bundles and full physical
owner databases. Git contains only path-free metadata and digests. This is no
public-disclosure permission, budget increase or qualification waiver; the
ordinary completeness, privacy and fresh-retrieval gates remain mandatory.
The operational projection is owned by `node:docs/evidence/RETENTION.md`.

After review, repairs and full repository/workspace gates, LLR-012 and LLR-008
become done; durable ADC remains LLR-011. Reconcile LLR-001/007
dependency/evidence notes, S011 Private Case Continuity, Node
ledger/MVP/readiness and P035-019a/b, with a new actual-date acceptance
decision. Point the old scope audit to this independent replacement basis
without changing frozen observations. Until every required row, retention step
and check passes, both the new gate and LLR-008 remain open. No global
Whisper/Agora readiness follows from this bounded gate.

## Open Questions

No owner-policy decision is deferred to implementation. Discovering incompatible
existing wire contracts requires an explicit correction here before changing the
claimed scope. A failed gate preserves its real result and leaves its task open.

## Next Actions

- LLR-012: implement and qualify the independent Gate B campaign above;
  preserve historical data/results and link the new standalone proof.
- P015-005: ordinary scoped v2 issuance and detached anchors.
- LLR-009/010/011: portable presentation qualification, context transition and
  separately authorized durable ADC operations.
- PEX-002 and S023-002: load/scale and trace-purge qualification.
- Keep the completed convergence dispositions in the Node integration map;
  review changed abstractions again before closing LLR-012.

After each substantial stage: review, repair, recheck and commit. Runtime uses
clean committed revisions. Compile without incremental. Preserve feature
worktrees; no integration or push is authorized. Reconcile S011, Node ledger/MVP
and readiness views; global Whisper/Agora and release readiness remain partial.

### Offer-control composition checkpoint

The receiving implementation now shares exact public-offer reservation/signing
law between separately fenced case-command and protected-signal owners. The
protected-signal port composes actual P037 agreement and Memarium Personal-journal
custody under independent current gates. Exact committed custody acknowledgement
can be recovered before live-offer lookup after a crash, even after offer expiry
or cleanup; this neither renews admission nor extends record read authority.
Component regressions cover cross-offer substitution, actual owner restart and
expired-result recovery. Native direct adoption is composed below; real two-node
Gate A and ordinary-v1 SQLite/Synapse Gate B remain open.

The optional native custodian now installs the offer/P037/Memarium composition
with a finite, separately adopted peer/record-custody policy. A standalone role
does not require case authority; an explicitly paired authority keeps separate
owners and trust. Exact admitted record-author keys authorize storage only, not
source eligibility or certificate issuance. The closed operator operation
`prepare-protected-signal-offer` selects this recipient purpose, while the existing
command-offer operation remains distinct. Both direct consumers share bounded
AD/INAC framing controls. Their authority/offer maintenance runs through S020;
disabled offer owners use the existing bounded retention catalog. Native seam
conformance is not the real two-node Gate A. Native direct source/response adapters
are installed; separately adopted owner progression is described below and both
runtime gates remain open.

### Original pending-command lease

The domain inbox preserves the exact authenticated PEX ceiling as part of its
immutable input binding, independently of the signed offer and inner control.
Its effective deadline is their minimum. Retry or restart cannot extend that
ceiling, and a shorter replacement is also changed input. Later owner processing
and response preparation inherit the original ceiling; delivery custody is not
permission to create another exchange lease. Missing historical lease material
refuses rather than being reconstructed from a longer date. This contract is not
an additional runtime-qualification claim.

### Separately adopted owner progression

Native direct command custody remains `transport-accepted-owner-unprocessed`.
An independently adopted processing profile attaches the existing authority via
S020; it visits at most one bounded inbox row per run and rechecks current
peer/key/role and command-family admission. Tightening the current family adoption
after restart also applies to already retained pending commands. Native command
validation is independent of transport.
No second transport retry or native decision queue is introduced.

Committed native output is immutable across lost handoff acknowledgement, newer
heads and restart. Status-response references are retained atomically with the
native output until the original inbox horizon, without extending status or
network validity. Expired output cannot be replaced with a newly signed status
under the same exchange. A separate owner fact records durable AD custody; AD
alone subsequently forwards or retries the original ciphertext. Current gates,
exact target and absolute original deadline still apply. Component evidence does
not replace either runtime gate.

### Scoped direct-consumer evidence, 2026-11-08

The [Node observation](../../../../../node/docs/audits/WHISPER-DIRECT-CONSUMERS-2026-11-08.md)
records actual two-endpoint AD/INAC command/result and protected-signal custody,
transport-only pending inbox before optional S020 processing, host offer refusals,
terminal AD completion independent of domain acceptance, restart and exact replay.
Its certificate/media/topology boundaries and original refused observer runs
remain explicit. These are implementation observations, not complete Gate A.
A subsequent clean-source, explicitly fault-injected run discarded one actual
peer admission ACK; the existing AD retry returned the identical saved admission,
with exact custody bytes after reopen. The stopped observer also checks selected
AD/INAC, network/log and notification surfaces plus default cache/store contents.
A later clean run also captured all twelve role/phase-bound live SSE streams and
checked exact command/reply/protected ciphertext canaries. Logical AD payload
retention is distinguished from physical SQLite pages; S023-002 is not claimed.
The original stale-terminal-snapshot refusal remains separate from the corrected
fresh run. These are scoped canary observations, not complete privacy
qualification. A separate native readback oracle now verifies the captured
registration control and authority signatures against separately supplied
controller trust, including exact request/input bindings and explicit mutation
refusals. It proves neither anchor admission nor the complete runtime build chain.
A fresh native run also discarded the first successful HTTP result body at the
controller boundary, then recovered the exact result through normal readback
and restart. Complete bounded logical AD/INAC views are prepared for the capsule;
no owner images or keys are included. This is not wire loss or proof of a lost
AD domain reply before source commit. Independent full direct Gate A
loose/archive/two-store qualification remains open. Ordinary-v1 positive SQLite and
Synapse Gate B, independent horizons and ordinary UI/succession are still required;
no tracker is promoted from these scoped observations.


## Independent direct Gate A qualification — 2026-11-08

The bounded direct profile is now qualified independently: actual two-endpoint
AD/INAC, production P037 offers, protected Memarium custody and exact pending
case inbox before separately adopted S020 processing. Eight actual offer refusals,
three native AD refusals, real ACK-return loss, client HTTP-body-return loss,
exact retry/restart and complete selected logical/SSE access classes are checked.
Ten actual-data semantic mutations refuse. Loose, extracted and fresh primary and
secondary qualification outcomes are identical; the complete set is 131,533 B
with XZ128MiB. Evidence and original refusals:
`node:docs/evidence/private-case-continuity/2026-11-08-direct-gate-a/README.md`.

This completes this profile's PEX/S023-001 Gate A, not ordinary-v1 Gate B.
Synthetic-v2 case credentials and fixture-signed private v1 signals remain explicit.
Minimal AD outcomes contain no private domain link or payload; authorized local
INAC decisions retain authenticated peer identity, opaque transport handle,
ciphertext digest and times. Empty constructor directories are not cache payload
entries. No transport anonymity, physical purge, universal-encoding privacy,
new media topology or release readiness is established.

The earlier dated checkpoints above preserve their observation-only status.
Ordinary-v1 issuance/host/Vault opening, independent horizons, positive portable
Matrix receipt and SQLite/Synapse continuity remain required before full closure.


## Open ordinary-v1 admission-policy clarification — 2026-11-08

Implementation review found a contract gap, not an absent store getter. The
ordinary P015 decision-v1 path issues WhisperV1 under
`signed-admitted-relay-receipt-v1`; the existing portable P035 producer/evaluator
requires `witnessed-admission-receipt-v1` and v2 witness-window fields. Lifecycle
support for v2 does not authorize its production issuance. Synthetic v2 or
relabeling the v1 profile cannot satisfy the required ordinary-v1 Gate B.

An explicit, independently admitted versioned admission policy over real v1
credentials is proposed; the owner decision remains pending. Existing signed
profiles, receipt meanings and historical evidence are unchanged. Matrix time-only
observations remain insufficient. Source/receipt composition and positive
SQLite/Synapse continuity are still required after that clarification.

## Signed-policy and quota component foundation

The case owner now prepares `whisper-case-authority-policy.v1` through its
existing protected P037 control and fenced Store. It freezes the adopted owner
configuration and exact source profile under a canonical random operation ID;
restart and response-loss retry keep the original bytes and issue time. Readback
cannot resume an unsigned signature operation. Current profile withdrawal,
changed input, final-commit refusal and expired leases remain refusals. This
library composition does not install the independent P091 authority setting or
a host publication route.

The owner reuses its complete retained accepted-result chain for 64/case and
four/rolling-24h succession accounting, without a second counter or schema
migration. Component tests exercise fifth refusal after restart, unchanged replay
and emergency closure; pure conformance exercises 64/65 and the exact rolling-day
edge. Full long-lived owner and ordinary-v1 SQLite/Synapse Gate B remain open.
See `node:whisper-case-service/README.md` for the owner contract and convergence
boundaries. This does not broaden the source-pinned direct Gate A result.

## Local policy adoption boundary

The P091 `/whisper/case-authorities` value is the closed local
`whisper-case-authorities.local.v1` list of exact `{authority/id, policy/digest}`
pairs, with an empty deny-all default and at most 64 entries. Policy bytes are
separate input material: new-case preview carries the canonical signed policy as
unpadded base64url in `case.authority/policy`. Supplied bytes cannot establish
local trust or change the selected certificate profile/federation.

Host preparation and first signing reacquire current P091 sources and verify
that same frozen document; a bad later source cannot reuse cached authority.
Original preview time fixes the authority ceiling. Retained document/result
readback does not grant another signature. This boundary does not yet supply
the three independent custody guarantees or close ordinary-v1 Gate B.


The producer is available to an independently adopted native case authority's
local operator through `prepare-authority-policy` and `read-authority-policy` on
the existing identity workflow route. Requests select an exact owner-adopted
source profile and canonical random operation ID; only preparation specifies a
finite deadline. Readback cannot resume signing. The result distinguishes
`not-published` from committed exact `policy/bytes` and `policy/digest`. P072
admits only these local operator uses; no generic middleware or public fetch
alias follows. Recipient adoption remains a separate P091 decision. Native
signer/store/reopen conformance does not renew Gate A or close ordinary-v1 B.


### P036 preflight and actual custody

The local P036 owner can expose finite policy horizons and a change witness from
its existing provider, at the original reviewed creation observation. The host
requires current enabled policy and independently admitted issuer/profile before
owner access, then resolves the complete policy again. Provider loss, source
failure, changed values, clock regression or expired horizons refuse. This is a
nonserializable local composition port, not a new public receipt or capability.

Such preflight is neither a capacity reservation nor proof of captured material.
A positive actual anchor and its retained record/proof guarantees remain mandatory
before opening; a later policy, origin or holder cannot extend original custody.
Its component/reopen tests do not complete LLR-001 or ordinary-v1 Gate B, and the
old issuer-retention coupling cannot be removed using this preflight alone. See
`node:memarium-runtime/README.md#prospective-case-custody-preflight`.


### Exposed preparation operator projection

The ordinary operator `case-key` command lists current exposed, unbound
preparations in digest order, at most 64 per page. The cursor is exclusive and
live, not a snapshot; lifecycle changes require a fresh scan. The response carries
only the operation reference, commitment digest and original horizon, together
with owner revision and continuation. It does not verify secret availability.

Explicit `abandon` checks the absence of an author binding inside the same S026
owner that commits erase intent and completion. A stale inventory selection must
refuse after bind. Existing unbound erase intent/completion remains idempotent
through restart; there is no implicit replacement key. Bound-key erasure and case
closure remain separate operations. This is exposed through the existing
operator-session route and protected Whisper UI, using POST/CSRF and P095's
private template catalogue. No module capability or new access route follows.
Component owner/schema/UI tests do not qualify ordinary-v1 Gate B.


### Explicit creation UI and authoritative review

The protected Whisper form selects `signal` or `new-case` explicitly. Only the
preview request can carry the existing creation intent (authority, requested
absolute horizon and exact signed policy material); neither sign nor readback
re-submits changed creation fields. The host's independent P091 admission and
provider rules remain mandatory. An ordinary preview cannot silently introduce
`case/*`, and a requested case response must preserve its authority and may only
shorten its horizon.

The review projects commitment, authority and absolute deadline from the actual
retained document, separately from editable request inputs. A lock keeps the
same operation and document; stale CAS refuses before replacing the projection.
The view calls it an exposed preparation or signed anchor candidate, not an open
case. Component UI/request-binding tests do not establish actual custody,
portable admission or ordinary-v1 SQLite/Synapse Gate B.


### Opening custody commitment and portable bridges (2026-11-12)

The missing guarantee before key exposure is a P036 owner obligation, not another
policy preflight. Reserve a bounded entry in the same exclusive provider/journal
and capacity as actual material. Freeze original operation identity, provider,
policy and finite payload/proof deadlines before S026 exposes a key. Unknown or
failed reservation refuses. Retry cannot extend an origin, change the promise or
silently adopt a replacement provider. This promises managed retention/capacity;
it is neither proof of capture nor physical disk preallocation or immunity to
provider loss and explicit erasure.

Persist exact signed bytes before binding both S026 and the reservation; return
new publication material only after both bindings complete. Interrupted bindings
resume that exact result without new keys or signatures. Successful actual
portable capture atomically consumes the reservation into the retained entry,
keeping the original deadlines. A changed capture policy cannot renew or silently
shorten an existing promise. Full-record capture reads the case ceiling from the
already verified signed body; only detached receipt profiles repeat case fields.
A reservation, policy or signed body alone cannot open the case: the actual
retained record/proof and positive historical anchor verifier remain mandatory.

Preview expiry never abandons an exposed key. Explicit unbound abandonment
retires the key before releasing its reservation. Bound reservations expire at
the original case ceiling or are consumed by actual capture. Maintenance rotates
through bounded reservation batches in the same owner; it creates no new queue.
Combined material/reservation capacity remains bounded. Exhaustion must still
permit abandonment and expiry cleanup. Source loss, clock/fencing failure and
unresolved commit outcome refuse before a new exposure.

The portable bridges are owned by
[P035-019a/019b](../035-agora-topic-addressed-record-relay.md#witness-source-adapters-for-ordinary-case-anchors-2026-11-12).
They keep the existing source-profile and certificate digests, require separate
exact policy/use admission and never select a fallback. The SQLite v1 bridge
uses the original local receipt; it does not produce Matrix anchors. Synapse
requires the separately adopted full-PDU observation witness. P015-005 is not
substituted for either bridge, and current ordinary-v1 Gate B remains open.

Source-bound case evidence has explicit `whisper-case-command.v2` and
`whisper-case-succession-presentation.v2` carriers. They add the opaque
`anchor-source` role: at most eight exact buffers, 64 KiB each and 256 KiB in
total, charged inside the existing command/presentation decoded budgets. The
wire limit remains 4 MiB; the referenced profile remains 64 KiB. Each occurrence
counts in v2's byte budget, including a buffer reused under another role.
Registration and presentations require the source role. V1 schemas, signatures,
pins and unique-buffer accounting remain unchanged and refuse that role.

Ordinary source-bound operations use the operator-only
`POST /v2/identity/whisper-case-workflow`, with closed
`whisper-case-workflow-request.local.v2` and result v2. The path selects the
carrier explicitly; v1 bodies do not pass the v2 path, and v2 bodies do not pass
the old path. Begin freezes carriage v2 in the existing sealed operation before
requester-key exposure. Subsequent source-command mutations and readback check that saved
version; an operation cannot switch versions under one ID. V2 command preparation uses only the
explicit offered direct profile. Audience presentations have an independent
explicit schema and frozen exact-byte binding under their separately adopted
audience route; a command offer grants no audience authority. It does not enable protected-signal offers or
add a module/public capability. The old v1 endpoint and its contracts remain
unchanged. Business intent, certificate/profile version and original admission
time policy are independent from this carrier choice.

Source commands use `whisper-pex-key-offer.v2`, whose closed payload is
`whisper-case-command.v2` and whose recipient role remains `case-authority`.
Its protected signing domain is `whisper.exchange-key.offer.v2`, with preimage
prefix `orbiplex.whisper-pex-key-offer.v2` followed by NUL. The v1 offer remains
unchanged. A version-1 offer never authorizes a version-2 command. The shared
recipient-key, interval and exact exchange laws apply without a second key
schedule, transport queue or authority grant.

The explicit carrier version selects admission material v3. One shared structural
projection feeds both registration and recipient verification; P035 still owns
source verification and independent policy/use adoption. A bad carried buffer
cannot fall back to a good local copy. References resolve only through the
explicit local exact-byte port, with no acquisition operation.

The relay route's `record/id` is distinct from the case anchor's exact signed
author-byte digest. They are not interchangeable even though both use SHA-256.
Verification dependencies retain only the required, checked metadata objects.
A full Matrix PDU remains payload; its digest is a separate dependency reference,
not a non-payload hold or custody promise. Unused carried objects do not become
verification metadata. Source payload custody and ordinary host/private transport
composition retain their own Gate B obligations; declaring these carriers does
not qualify that runtime.
