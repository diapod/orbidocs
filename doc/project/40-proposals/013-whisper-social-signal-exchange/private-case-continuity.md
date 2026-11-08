# Private Case Continuity {#private-case-continuity}

Decision date: 2026-11-06. Status: accepted execution contract; implementation
and runtime qualification pending. Owners: P013-PEX-001, P013-LLR-001/008/007
and the S023-001 route profile. No completion claim follows from this decision.

## Executive Summary

A named recipient receives protected Whisper material through AD/INAC. An author
explicitly opens a case anchored to an admitted signal, then continues that case
under a current nym when an action requires it. Private delivery, historical
admission, accepted case history and current authorization are independent facts.

Gate A qualifies private exchange independently. Gate B qualifies opening and
succession on both SQLite and Synapse, including restart and replay. A Synapse
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

The current Matrix relay has a SQLite local store but no admission-store adapter.
The current authoring path also confuses case retention with issuer identifying
data retention. Both gaps require implementation, not a different success claim.

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

The case anchor is the digest of exact signed author bytes admitted with
`agora-admission-receipt.v1`; the protected PEX signal is a separate case artifact.
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
wrapper around origin_server_ts. Runtime publication time retains the declared
`authenticated-admitted-homeserver-v1` policy; full PDU verification is acceptance
work. Missing evidence, nonfinal admission or changed bytes gives anchor-unresolved.
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

Gate B requires ordinary certification and host signing, preview/prepare/bind,
portable receipt and opening on SQLite and Synapse; real sync, exact bytes and full
PDUs; missing-receipt refusal; expired original certificate and current successor;
A-to-B-to-C; concurrent succession/closure/retry; exact lost-response readback;
stale/missing/rollback/equivocating status; unbound keys/abandonment/erasure/recovery;
restart and replay without sending, signing or performing commands again. Keep
Node and homeserver gates separate. Controlled-clock tests are not long observation.

Conformance includes quota boundaries, clock rollback, retention guarantees,
pre/post-CAS crashes, unchanged-head status refresh and both ADC race orders.
Runtime cases have their own process/HTTP observations; conformance has no invented
HTTP success. Real v1 issuance is mandatory; synthetic v2 does not close Gate B.

Retain one campaign through P035-011 with XZ dictionary 128 MiB: complete set
16 MiB, refusal capsule 1 MiB, campaign/profile refusals 4 MiB and current aggregate
limits. New Git controls total at most 64 KiB. Measure headroom before runtime.
Loose, safely extracted and freshly retrieved qualifications from both adopted
stores must agree. Read current retention/retirement contracts before capture;
record owner, classification, inventory, dependencies, minimum retention and
restore/replica facts; unknown remains unknown. No keys or recovery bundles.

## Open Questions

No owner-policy decision is deferred to implementation. Discovering incompatible
existing wire contracts requires an explicit correction here before changing the
claimed scope. A failed gate preserves its real result and leaves its task open.

## Next Actions

Baseline/test collection, contracts/schema mirrors/refusal fixtures, PEX/S023-001,
Gate A, case owner/Matrix admission, ordinary UI/succession/P072, Gate B, then
convergence and status reconciliation. After each substantial stage: review,
repair, recheck and commit. Runtime uses clean committed revisions. Compile without
incremental. Preserve feature worktrees; no integration or push is authorized.

Before closure compare result stores with issuer decisions, AD idempotency and
P091 CommitHost; folds/cursors, PEX/P015 offers and SQLite/Matrix admission.
Every candidate is consolidated, intentionally separate or assigned a concrete
owned follow-up. Reconcile P013/S011/S023, schemas/Schema Gate, P072 PL/EN,
COVERAGE, Node ledger/MVP and the existing MVP readiness snapshot. Gate A can close
PEX/S023-001 alone; the full slice requires both A and B.

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
