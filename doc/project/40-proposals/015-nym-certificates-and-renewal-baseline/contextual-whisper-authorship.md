# Contextual Whisper authorship

Status: accepted design; implementation and both runtime gates remain pending.
Date: 2026-10-25.
Based on: [P015](../015-nym-certificates-and-renewal-baseline.md),
[P013](../013-whisper-social-signal-exchange.md), P081-021, S017 and S023.

## Executive summary

Phase 1 counts council-admitted participant sources within one rumor context and
epoch. Multiple nyms, certificates or transport nodes do not increase one source's
contribution. This profile supersedes the node-counting M4 rule only for the new
v2 artifacts. Historical M4 evidence retains its original scope.

Gate A qualifies private certification and erasure independently of Matrix.
Gate B qualifies real host/Vault authorship and contextual thresholds on SQLite
and unmodified Synapse. Neither gate proves unique humans, an honest council,
anonymous transport, federation, or complete Whisper readiness.

## Context and problem

The existing certificate verifier and historical acceptance nym signer do not
provide an ordinary participant's issuance, signing and renewal path. Transport
admission, certification policy, permission to sign and eligibility to count are
four different decisions. The optional issuer service owns policy and decisions;
the host owns private nym keys; AD owns delivery of already encrypted bytes.

The host bounds each AD submission by the adopted profile's request TTL. This
is a transport lifetime covering discovery, exact invitation consent and retry,
not the duration of one scheduler pass. AD preserves the first submission's
bytes, plan and expiry on retry. This budget neither extends the signed request
or certificate nor grants late issuance; the original domain and consent
validity checks remain decisive. A retained result uses its separately bounded
readback/consent contract.

Knowledge minimization and participant agency require bounded private mappings,
explicit renewal consent and no public reset linkage. Reproducibility requires
immutable admission decisions and a separate current eligibility projection.

## Decisions

### Source profile and ordering

`whisper-source-profile.v1` is content addressed using JCS, with NFC required
before signing. The context is the JCS digest of federation, exact profile digest,
council identity, topic class and similarity key. The digest is not a secret.
A public certificate carries its opaque source reference, profile/context,
epoch, signed `activation/not-before` and stable `status/min-revision = 1`.
The profile requires `source/activation-policy = post-reset-collection-drain-v1`,
so adopting this correction changes its content digest. It carries no participant, source node,
request/reply reference or private predecessor.

Production epochs are half-open seven-day intervals anchored at
`1970-01-05T00:00:00Z`. Certificates last at most 24 hours and end no later than
the epoch. Every certificate uses a fresh context-confined nym key. Routine
renewal retains the source; private reset changes it and revokes the previous
source without publishing a successor. Distinct epochs never combine.

The council knows which participant requested each rumor context and when.
Public similarity keys can reveal the meaning of a context digest. Phase 1
trusts its uniqueness policy and accepts this participation/timing disclosure.
The council is a dependency for a first context and for certificate renewal;
an already usable certificate does not need a fresh issuance round trip.
Acceptance records the complete request-to-decision latency, not just AD ACK.

### Notice and embargo manifest scope extension

Planned post-MVP (2026-10-28), owned by
[P015-005](../015-nym-certificates-and-renewal-baseline.md#embargo-authorship-scope-tracker).
The current signal-only profile does not authorize correlation notices or
separately signed embargo manifests. Its replacement/extension must bind exact
`(record/kind, schema, topic, disclosure/scope)` tuples; independent kind, schema
and topic arrays must never produce an implicit Cartesian product of grants.
Issuance and receiving-side verification both enforce the tuple and the issuer's
admitted profile. Unsupported profiles refuse instead of silently downgrading.

The manifest is a separately domain-bound auxiliary signing use, explicitly
listed by this profile, with the same certified key/context and authenticated
admission-time bounds. It does not grant a new publication kind. The full
protected signal references its digest; the admission receipt binds the two.
The recipient verifies the manifest and receipt without retrieving that signal.
This does not let a detached signature stand in for the full envelope signature.
P015-005 owns positive and cross-kind/cross-scope refusal fixtures; ADC-001/007
own application use. None of this expands the existing narrow signal-only
profile or qualifies Gate B.

### Unpublished Matrix preparation

Ordinary v2 publication first checks current contextual authorship/status and
freezes an exact transport intent. `202 publication-requested` and a later
forwarding ACK are not admitted domain records. The intent creates no source,
publication-time fact or receiving nonce. Authenticated reception independently
supplies the admitted homeserver observation and commits admission. Status and
retry remain available by their topic-authorized links before the record exists.

A first intent must be prepared before its signed proof deadline. Retry preserves
the original bytes and transaction identity; it never extends validity or promises
that a late event will pass admission. Historical readback needs no new status
lease. Frozen intent/carrier/mode/transaction conflicts refuse. Explicit legacy
v1 has no contextual publisher fallback. This owner composition is software
implementation, not completed ordinary UI, Synapse or Gate B qualification.

### Publication time and status freshness

Certificate, request and presentation validity are checked at an authenticated
publication time, with five seconds of skew. `authored/at` is never that proof.
The receiving relay must first admit the record strictly before epoch end; skew
does not extend an epoch. A publication time after local receipt plus skew is
refused. A valid certificate can therefore expire before history reaches C.

The immutable profile binds `publication/matrix-time-policy =
authenticated-admitted-homeserver-v1` and `publication/sqlite-time-policy =
signed-admitted-relay-receipt-v1`; changing either policy changes the profile
digest. This draft refinement invalidates no released certificate or Gate A/B
result, because those runtime gates are not yet qualified.

For Matrix, the phase-1 policy explicitly trusts `origin_server_ts` supplied
by the configured, independently admitted homeserver over an authenticated
Client-Server connection. The trusted network adapter binds that observation to
the account, room, event, sender and exact author bytes; a timestamp inside the
carrier or author document cannot supply it. Persist this backend observation
with admission for restart/replay. No author timestamp, unsigned relay stamp or
unadmitted server is a fallback clock authority.

This is authenticated homeserver-time evidence, not runtime verification of a
server-signed full PDU. Full-PDU hashes/signatures/size remain independent
acceptance evidence. Matrix supports federation-format events through a `/sync`
filter, but this policy does not require that optional runtime verifier or a
Server-Server API identity. Neither TLS authentication nor an event signature
establishes an objective clock or an honest homeserver. The operator accepts the
named server's clock for this phase; the fixture's explicit isolated loopback
HTTP channel is a fixture-only trust profile, never a production TLS substitute.

Phase-1 reaffirmation (2026-10-28): the observation is a local replayable fact,
not a portable time attestation for another node. A later runtime PDU verifier
is a separate explicit profile behind the existing publication-evidence port.
Its missing or invalid PDU must not silently select this observation policy.
The required time policies and `source/activation-policy =
post-reset-collection-drain-v1` remain part of the profile identity; no default
or schema omission may erase those decisions.

For SQLite use an allowlisted relay's signed durable admission receipt binding
record digest, exact author-byte digest, relay identity and acceptance time.
Receipt verification precedes construction of publication-time evidence.

A signed, scope-bound status snapshot is usable for collecting a signal for at
most 3600 seconds. A status older than 300 seconds marks the current basis as
`freshness=unknown` and cannot authorize the first threshold/proposal emission.
The two limits are explicit profile fields, never added to clock tolerance.
Missing/stale status is `deferred`, not a permanent rejection. Revocations are
cumulative within the epoch; signed rollback and same-revision equivocation
refuse. Every change to a signed status payload, including refreshed timestamps, uses
a new revision. Durable high-water marks survive restart and rebuild. Public
certificates use the profile/epoch's stable status floor, not a per-request or
per-reset revision that would identify a revoked predecessor. The private
issuance decision binds the actual minimum publication revision. Eligibility
and the emission latch commit under the same status-revision CAS. Imported
claims cannot replace local eligibility or first-emission facts.

On 2026-10-26 the operator accepted an activation quarantine for private reset.
The replacement source cannot be used while any status from before the reset
could still be admitted under the collection lease. The binding retains this
activation boundary through renewal, restart and another node's request. The
certificate's earliest tolerated publication time must be no earlier than that
boundary; subtracting the five-second certificate tolerance must not create an
overlap. A reset too late to leave a nonempty certificate interval before epoch
end refuses explicitly. It does not silently activate, carry the contribution
to another epoch or fall back to the predecessor. The fixture uses its own
short collection lease; this proves the same boundary, not a one-hour runtime
observation. This replaces the earlier per-reset public-revision barrier.

Let `U` be the greatest collection expiry of every published status before the
reset. Choose the replacement certificate's `not-before >= U + 5 seconds`.
Both its trusted publication anchor and actual local reception must satisfy
that lower validity bound with at most the same five-second tolerance. Testing
only the publication anchor would apply the future-publication allowance a
second time and permit an early local admission. At the earliest permitted
local receipt `r = U`, the old collection lease (`r < U`) has already ended.
Public validity timestamps still permit temporal inference; this profile does
not claim timing anonymity or hide the council's contemporaneous knowledge.

A deferred live admission preserves its first-receipt time but evaluates current
status, revocations and epoch closure at the actual decision time. It cannot
borrow the receipt's older clock to refresh status or admit after epoch end.
Retained facts distinguish publication, first receipt and admission; clock
rollback refuses. This is separate from replaying an already committed decision.

Previously accepted contributions survive natural certificate expiry, but cease
to count after source revocation or epoch end. Historical admission facts do not
change during replay; replay verifies their stored proof and policy identity,
not today's clock. The current view uses the current verified status separately.

The narrow P081 bridge keeps request audience `agora-ingest` and a one-shot
presentation bound to the exact unsigned Agora candidate. Its certificate has
the fixed `whisper-contextual-authorship` audience and rumor-context digest.
Only the concrete verified `whisper-signal.v2` profile bridges these contexts;
this is not a generic audience rewrite. Outer and presentation certificates must
be byte-equivalent under JCS and identify the same certified nym/source.

The presentation's `revocation/evidence-ref` is a stable scope locator:
`nym-source-status-scope:` followed by base64url SHA-256 of the JCS object with
`schema = nym-source-status-scope.v1`, `profile/digest`, `issuer/id`,
`context/digest` and `epoch`. It is not a snapshot or freshness lease. The owner
fetches and verifies the current signed scope status independently. No complete
revocation inventory is copied into each author envelope. P081 possession and
certificate validity use the independently trusted publication anchor; nonce
reservation uses actual local reception and remains through epoch end. Signal
preview/signing uses the collection lease, while the separate first aggregate
emission requires the stricter emission lease.

### Renewal, preview and first emission

Renewal is lazy by default, when the participant next publishes in the context.
Optional `stay-ready` consent covers exactly one context until epoch end, is
revocable and permits at most seven renewals. The scheduler chooses and persists
a random time in 75–95 percent of the current validity interval. It does nothing
when the next certificate cannot extend validity within the epoch. Unlock and
current recovery-bundle requirements remain in force; there is no autoexport.
The host reserves a bounded renewal-operation slot and persists its exact time
and operation id before effects. Re-reading that plan does not redraw time or
spend another slot; uncertain/aborted effects do not silently refund allowance.
Revocation fences future effects while retaining an already reserved operation
for factual decision reconciliation. Late completion cannot revive consent or
count across an epoch boundary. A replacement consent needs a separate explicit
approval; the host enforces one active consent per participant/context/epoch.
All updates retain source authority and CAS.

Operation IDs make nym preparation and preview idempotent. A 423 retains the
exact document; an expired preview requires a new explicit preview.

The first crossing freezes authority, descriptor, inputs, time and signing bytes
under `(profile, context, epoch, kind, authority)`. Later revocation/reset changes
the current basis and a proposal's read-model annotation (`eligible`,
`below-threshold`, `freshness-unknown`, `epoch-ended`). It neither edits a signed
proposal nor emits another first-crossing event. This is an authority-qualified
current annotation, not a globally distributed retraction artifact.

### Private exchange and authority

Use `nym-issuance-request.v1` and `nym-issuance-decision.v1`. The exact signed
request digest identifies the idempotent domain decision inside erasable
custody. A separately random `ExchangeHandle` (`exchange:` plus canonical
base64url of 32 random bytes) identifies transport; it is not derived from that
digest, a participant, nym, nonce, context or source. Bind applicant proof,
proof of the new nym key, an independent ephemeral bootstrap proof, council,
permitted reply recipient, operation, nonce and deadline. Requests expire within 15 minutes and before epoch end.
Persist the decision and prepared reply before AD sends it. Readback by request
reference never repeats issuance. Duplicate delivery returns the retained result.

Council admission is an explicit P015 policy. A federation root does not grant
council certification authority. A separate root-admitted capability-issuance
key can authorize exact, bounded request/reply INAC invitations for ordinary
participants. This P076 bootstrap profile grants neither Messaging permissions,
sovereignty nor onward delegation. AD receipt is not a council decision.

P015 plaintext is encrypted to the authorized recipient before entering AD;
AD stores ciphertext and opaque references only. No general AD custody hook is
introduced. The issuer's recipient key for identifying exchange material must
be erasable with that exchange/binding. Encrypting archived requests to a
permanent council key would defeat erasure and is forbidden for this profile.
Signed recipient-key offers and invitations bind the exchange, recipient, key
and deadline. Applicant reply custody remains with that applicant. Reset-linking
request/reply material uses a separate disposable transition key, not the new
binding's surviving key. Existing X25519/HKDF and XChaCha20-Poly1305 primitives
are reused with explicit purpose and AAD; no new cryptographic construction.

### Erasure and keystore

`application-keystore-v1` stores one independently random secret per key file,
outside DB/WAL, application backups, logs and retained evidence. Each context/epoch permits at most 2048 issued certificates, including renewals
and replacements. Reserve this quota before effects, including the capacity to
revoke all issued certificates/sources. Cumulative status arrays allow 4096
entries each; retirement does not replenish issuance quota. Their public signed
status has a separate 512 KiB canonical-JSON byte ceiling, sufficient for both
full inventories. This does not raise the private P015 plaintext (64 KiB), sealed
exchange (96 KiB), Agora envelope or Matrix PDU budgets. The active plus
retiring key cap is separately 4096; capacity refusal precedes minting or issuance effects.
The provider pins its instance and encrypted volume. Missing mount is a typed
refusal, never directory creation on an underlying unencrypted filesystem.
Keys are not derivable from a retained master, epoch seed or mnemonic.

The local encrypted-image custody default requires backup exclusions. The owner
subsequently permits an explicit acceptance-fixture adoption
`custody.image_backup_policy = "allow-encrypted-image-backups"`. An encrypted
sparseimage/sparsebundle on unexcluded backing storage may then pass preflight,
including when macOS automatically reports its mounted contents excluded. Preserve
both actual OS values; for this test backup exposure follows the backing image,
not the automatic mount flag. This choice does not change OS exclusions and does
not silently replace an earlier refusal with success. Production profiles retain
the strict default; null/unknown local policy refuses before custody effects.

A backup of the image is a copy of the keystore and lies outside crypto-erasure
assurance, alongside copied keydirs or whole-host images. It can preserve keys
removed from the active store. The explicit fixture adoption does not broaden
that assurance or change source identity, signatures, retention deadlines,
encryption, host FileVault, mount/instance binding, or missing-mount refusal.
This local media choice is not a new public source-identity parameter: the signed
profile already excludes copies of the keystore/image from its erasure guarantee.
A new observed positive preflight under the named policy is required separately
from the preserved strict negative case.

`source/ref` is HMAC-SHA256 under an independent binding key over a framed
participant/context/epoch tuple. Normal renewal keeps that key; reset creates a
new one. Old binding and all reset-linking ciphertext keys retire after signed
revocation publication/readback plus 300 seconds. The active replacement map
has no predecessor. Other identifying data retires 24 hours after the maximum
of epoch end, last certificate/request expiry and revocation publication ACK.
Duplicate requests never extend that deadline. Nonidentifying digest-to-digest
tombstones and aggregate counters can remain seven days. Each decision includes a fresh, uniformly random 256-bit
`decision/nonce`, covered by its signature and held only in the encrypted private
payload. The council must never retain that nonce in tombstones or logs. Without
it, the public certificate, known applicant/request digest and retained council
signing key could reconstruct a candidate decision and test its tombstone digest,
undoing erasure. A duplicate reuses the frozen nonce and exact ciphertext; it
never generates a new decision. The applicant keeps its own authorized copy.
The result link is limited to request digest → digest of the full signed,
nonce-bearing decision. A certificate digest, source/nym reference or digest
of a nonce-free decision projection is not an allowed replacement tombstone.
Request nonces also remain private. The issuer draws decision entropy
independently of public nonces, timestamps and key references.

Key use and key retention have different deadlines. Fixed request-recipient
keys retain their fixed expiry. A binding or transition awaiting a required
revocation publication must instead carry provider-local `awaiting-publication`
state, the exact committed scope/snapshot and its retention rule. An acknowledged
signed status plus matching readback fixes the first ACK time and resulting
destruction deadline; duplicate ACKs cannot replace it with a later time. This
never extends issuance beyond the context epoch. Pending-publication keys count
toward the same capacity ceiling and require bounded reconciliation and visible
operator attention. If ACK never arrives, this rule supplies no absolute calendar
destruction deadline; the implementation must expose that limitation, not invent
an infinite timestamp or silently use epoch-end plus retention. Publication-link
metadata is held with the erasable key, not in retained destruction receipts.
The optional issuer implements this lifecycle with provider fences and bounded
S020 reconciliation. It still needs real Gate A qualification.

### Opaque private snapshots and factual publication readback (2026-10-26)

The stable context/epoch key fences the opaque journal. It must not encrypt
identifying maps or expose stable participant lookup deltas next to public reset
revocation deltas. Each full private current-state snapshot instead uses a fresh,
independently random erasable snapshot key. The outer checkpoint contains only
opaque key/chunk references, ciphertext, public signed status and nonidentifying
nonce-bearing decision commitments/prepared encrypted replies. Identifying lookup
maps remain inside that snapshot; the current map has no predecessor/reset link.
This uses the existing bounded checkpoint, not an unbounded historical map cache.

A reset's publication ACK retires every prior private snapshot key that could
recover the old map, the old binding key and all issuer-side request/bootstrap/
transition keys that retain the reset link, within the profile reset buffer.
The current independent snapshot remains readable. Retaining the epoch fencing
key or restoring an old DB/WAL must not recover those old maps. Obsolete key
references may remain opaque for bounded reconciliation; permanent destruction
receipts contain no participant, source or publication-link metadata. This
protects controlled retained bytes, not outside timing inference or the council's
prior knowledge. Pending keys count toward the same provider capacity ceiling.

Key creation enters awaiting-publication before a domain snapshot references it.
The exact committed head is then attached by provider CAS before exposing an
output. Finalization stops future use without inventing a destruction timestamp;
normal minimum end-of-use remains the epoch boundary, while reset finalization
uses the accepted shorter reset rule. A duplicate operation cannot choose new
keys, deadlines or bytes after a crash.

Publication ACK is a durable historical fact, not a collection/emission lease.
The owner selects the exact prepared signed status and committed head; its trusted
publisher adapter reads that publication back. The verifier checks signature,
canonical exact bytes, scope, minimum revision and required revocations, with an
observed time no earlier than status issuance. Status expiry or epoch end does
not invalidate factual readback completed later. It does not renew status
freshness for admission or emission.
The verified readback time and its exact signed status are committed under a
provider-fenced Ready head before cleanup. Reopening that head must finish key
acknowledgements locally even when the publisher is now offline; it cannot
repeat network I/O as a prerequisite for the already acknowledged retirement.
The frozen time cannot move forward on a restart.
 Equality/crypto conformance alone proves no
backend I/O; real publication/readback remains a runtime Gate A obligation.

Destruction durably retires a key, fences and drains operations, removes the key
file, fsyncs its directory and persists a receipt. Provider-local lifecycle
metadata prevents old DB restore from undoing retirement. Startup finishes due
destruction before decrypting private state. A missing key never invokes
get-or-create or mints a replacement counting source.

Normal epoch closure is an explicit owner transition even when no later request
arrives. It fences a complete opaque key-handle set, verifies factual readback,
commits Closed state and acknowledges the current map/bindings before the epoch
fence key. Closing does not mint a post-epoch key or renew eligibility. The outer
journal never exposes a cumulative epoch-keyed nym-tag history: such tags belong
inside erasable full snapshots, because their deltas can reveal a reset successor.

After the profile's finite replay-retention window, a bounded owner sweep removes
closed-scope request/result markers and ciphertext caches. A provider-local
metadata-only retirement revision fences the purge, so restoring an older database
cannot revive lookup results. It does not reactivate a key. A lookup with no retained
result means `not-found-or-expired`; it is never permission to reissue. Bootstrap
exchanges that never reached a context decision need the same bounded sweep using
their immutable verified epoch/deadline and expired recipient-key state.

The guarantee covers logical unreadability of controlled database, WAL and app
backup copies. It does not cover raw SSD/APFS blocks, snapshots or images that
copied the keydir, host images, or memory captured before destruction. The
participants' own Vault/recovery material has its separate custody policy.

### Exact encoding and signature preimages

All new P015 exchange plaintexts use UTF-8 JCS (`JcsV1`), without BOM or trailing
bytes. Require NFC for all names and string values before signing. Reject a
received private request unless its bytes equal its parsed JCS serialization;
this also rejects duplicate decoded object keys and ambiguous serializations.
This is a new-family rule; historical certificate and Agora bytes are untouched.
Every digest below is SHA-256, unpadded canonical base64url, prefixed `sha256:`.

The context preimage is exactly the JCS object with keys `domain` (constant
`orbiplex.whisper.context.v1`), `federation/id`, `profile/digest`, `issuer/id`,
`topic/class`, `signal/similarity-key`. The profile digest hashes the complete
profile's JCS. The binding MAC preimage is the JCS array
`["orbiplex.whisper.source-binding.v1", participant, contextDigest, epoch]`.
`source/ref` is `source:` followed by canonical base64url of that MAC.

All new-profile Ed25519 verification is strict and refuses weak public keys,
including new-nym proof of possession. This is an explicit profile rule, not a
retroactive change to every historical v1 signature verifier.

Signing preimages use a literal ASCII domain followed by one NUL byte and JCS:

| Signature | Domain | Removed top-level fields |
|---|---|---|
| New nym proof of possession | `orbiplex.nym-issuance-proof.v1` | `nym/proof`, `signature`, `bootstrap/proof` |
| Participant request | `orbiplex.nym-issuance-request.v1` | `signature`, `bootstrap/proof` (includes the nym proof) |
| Full request bootstrap possession | `orbiplex.nym-issuance-bootstrap-proof.v1` | `bootstrap/proof` (includes both prior signatures) |
| Issuer decision | `orbiplex.nym-issuance-decision.v1` | `signature` |
| Source status | `orbiplex.nym-source-status.v1` | `signature` |
| Issuer exchange-key offer | `orbiplex.nym-exchange-key-offer.v1` | `signature` |

The certificate preserves v1: JCS of the certificate minus `signature`, **no
prefix**. Requiring NFC makes both existing certificate canonicalizers agree.
Verify the new nym PoP, then the participant signature, then the ephemeral
bootstrap proof before any issuance effect. The request digest hashes the
complete canonical signed request, including all three proofs. The private
request and decision bind `exchange/handle`; outer ciphertexts and AD artifact
IDs carry that handle, never the real signed-request digest. The private issued
decision carries its actual `status/min-revision`; the public certificate's
constant floor cannot substitute for it. Decision recipient and issuer must
equal the request's exact bindings. The certified nym/profile/context,
epoch and route must equal that request. A fresh nym may not reuse the applicant's
primary public key. A certificate must carry mandatory compatible Agora scope
restrictions: exact topic key, federation, record kind `whisper-signal`, content
schema `whisper-signal.v2`, and its supported disclosure scopes. The contextual
profile cannot be accepted through the generic verifier as an unrestricted nym.

D supplies a signed `nym-exchange-key-offer.v1` for the anonymous first leg:
exact handle, ephemeral bootstrap public key, signed reply public key, digest
of that first-leg request, recipient X25519 key/ref and expiry. Preparing an
offer does not decide issuance. It does not contain the participant, actual
nym, context or real signed-request digest. The offer is outside the full
request's signed bytes, avoiding a digest cycle. Its private verifier pins the
actual full request in memory before sealing it. Key ref hashes the 32 raw
public-key bytes. No unbound reply address or key is accepted.

A freezes one random handle and operation nonce before minting. Inside the
Vault, a separate HKDF domain and that nonce derive an ephemeral Ed25519
bootstrap key E from protected nym material. E differs from the primary and
actual nym public keys. The narrow `nym-exchange-key-request.v1` contains only
handle, approved profile/issuer, E public key, reply X25519 public key and validity;
it is signed by E. It carries no applicant, actual nym, context, predecessor,
certificate, reply participant or real signed-request digest. Its preimage is
`orbiplex.nym-exchange-key-request.v1` + NUL + JCS minus `signature`.
The full private request includes the same handle, E key and reply key, with
the third E proof binding the already participant/nym-signed candidate.

A uses an independently adopted `nym-bootstrap-recipient.v1`, signed by the
profile's council, binding its separate X25519 bootstrap key/ref, exact profile,
peer node, purpose and validity (at most 24 hours). Its signature preimage is
`orbiplex.nym-bootstrap-recipient.v1` + NUL + JCS minus `signature`. Council
signature verifies the descriptor, but grants no AD/INAC authority. Root-admitted,
exact peer/family/artifact request and reply invitations remain mandatory.

D opens only anonymous first-leg metadata with the global bootstrap-purpose
key. It verifies E possession and validity before preparing one per-handle
recipient key. The real participant and nym proofs are checked only after
opening the full private request under that recipient. Exact encrypted-input
identities, handle and finite deadline are reserved before effects. Random
per-purpose allocation identifiers remain inside a separate erasable sealed
payload; retained provider operation bindings do not carry the real request
digest. A restored database missing frozen output refuses reconciliation rather
than encrypting a replacement under the same artifact ID.

The independent provider response fence binds handle, closed phase, exact
input-ciphertext digest, output-ciphertext digest and immutable replay deadline.
KeyOffer and Decision have distinct slots; an internal sealed allocation slot
is not a new wire phase or delivery queue. A preexisting reservation may finish
its frozen output commitment after recipient-key destruction, without new key
use. Global SQL ciphertext rows are retained replay source, not disposable
context projections. Their lookup needs no surviving private map or scan of
context membership. Private maps hold real request-digest/reply membership and
quota; outer checkpoints do not expose those joins. Expired provider markers
retain only opaque identity/deadline and cannot reopen an old exchange.

Domain clocks use the provider's durable high-water, not an application-DB-
restorable clock floor. A changed ciphertext under the same handle/phase
conflicts; duplicates reuse exact frozen bytes. Bootstrap metadata still exposes
peer activity to its authorized receivers, but not a participant-to-nym/context
mapping. The global bootstrap key cannot open full requests, offers or decisions.
A fresh operator-approved Decision reply invitation can retrieve an already
prepared historical result within its finite retention horizon after request
expiry. It cannot authorize a new expired issuance or extend key/record validity.
KeyOffer consent retains the original request deadline.

The earlier unqualified candidate used the signed-request digest as the transport
identifier and a primary-signed metadata first leg. This decision was superseded
on 2026-10-26 after the exact reset-link counterexample; its source-specific
findings remain in Node's certification component audit. Neither candidate is
promoted to Gate A by schema or software conformance alone.

Each encrypted payload has its own outer AD family: `nym-key-request-sealed.v1`,
`nym-key-offer-sealed.v1`, `nym-issuance-request-sealed.v1`, and
`nym-issuance-decision-sealed.v1`. The common `nym-exchange-sealed.v1` schema
checks their closed outer/inner pairing; it is not a grant for every direction.
Before AD submission, each phase durably freezes its exact canonical sealed
envelope, including ephemeral public key, nonce and ciphertext. Retransmission
reuses those bytes; it never re-encrypts even identical plaintext under the same
artifact/idempotency id. AD alone owns transport retries.

An invitation names one exact family and deterministic artifact id derived from
the random exchange handle H and exact phase/family (direction alone collides
between bootstrap and issuance). Both artifact id and AD idempotency key are
exactly `urn:orbiplex:nym-exchange:<outer-family>:<unprefixed-exchange-handle>`.
No signed-request digest appears in that public transport identity.
Malformed family pairing never tries another key
purpose, decryptor or admission policy. This refines an unqualified, prerelease
codec; it makes no claim about deployed-state compatibility.

For `nym-exchange-sealed.v1`, the header is the complete envelope minus
`ciphertext`. All base64url strings are canonical, unpadded. The ephemeral sender
key and 24-byte nonce are random and never reused. HKDF-SHA256 uses the existing
X25519 primitive, UTF-8 `exchange/handle` as salt, and the bytes
`orbiplex.nym-exchange-sealed.v1` + NUL + header JCS as info. Reject the all-zero
shared secret. XChaCha20-Poly1305 uses that derived 32-byte key, header JCS as AAD,
and the exact canonical plaintext. Decryption checks expected exchange, payload
family and recipient key before exposing plaintext; maximum plaintext is 64 KiB.
The sender's ephemeral private key is not persisted. Provider leases fence the
recipient key throughout decryption. A replayed ciphertext cannot revive a
retired exchange or bypass request idempotency.

## Trade-offs and failure modes

A named publication-time authority improves late delivery but adds explicit trust
in that authority's clock. Unknown evidence, missing issuer status, unavailable
keys or a failed policy check cannot silently select another profile. Transient
failures defer. Permanent refusals carry typed field/reason diagnostics.
A one-hour collection lease trades revocation reaction latency for availability;
first emission still requires a five-minute status. A lone council remains an
availability and metadata-concentration limitation of Phase 1.

## Open questions

No policy question blocks the accepted profile. Runtime adapter support, maximum
key population, issue latency and evidence size remain measured implementation
gates, not assumptions of completion.

## Next actions and acceptance

1. Freeze schema/DTO parity, negative fixtures and shared JCS golden vectors.
2. Qualify Gate A: issue, lazy renew, reject, private reset, readback, duplicates,
   lost replies, restart, wrong authority/recipient/digest/PoP, status rollback,
   equivocation, cryptographic destruction/crash/DB restore and mount refusals.
3. Qualify Gate B on SQLite and pinned unmodified Synapse: real UI/host nym
   signing, confidence 0.5, two participant sources, one threshold/proposal,
   same participant across nodes/nyms, expiry/revocation/reset, late first
   receipt after certificate expiry but before epoch end, restart and replay.
4. Scan public records, full PDUs, UI/API/SSE/notifications, logs and durable AD
   copies under their declared access class for identity/key canaries. Private
   authorized recipient payloads are distinct from public leakage surfaces.
5. Remove the environment acceptance signer before final Gate B. Use four roles
   A/B (ordinary applicants), C (sole projection authority) and D (council plus
   separate bootstrap authority). A read-only observer never publishes.
6. Retain both gates in campaign P015-003/profile whisper-contextual-authorship,
   with <=16 MiB combined positives, XZ 128 MiB, <=1/4 MiB refusal budgets and
   <=64 KiB new Git metadata. Preserve equal loose/extracted/two-store results.
   The fixture's 10-minute epoch and 2-minute certificate prove mechanics;
   controlled-clock conformance proves production seven-day/24-hour bounds.


### Local issuer state recovery

The issuer's temporal store appends encrypted transaction/event facts and derives
its current context projection, following S028. Each exact profile, issuer,
context and epoch has an independent lookup key and provider-local revision
commitment. State revisions are local recovery counters, distinct from signed
source-status revisions. A checkpoint contains public facts and opaque keyed
lookups/handles/ciphertexts only. Independently erasable binding and transition
keys protect identifying payloads; an epoch-wide key cannot preserve a private
reset's predecessor link.

Commit the exact event, opaque payload and projection in SQL, then CAS the
provider's previous revision/digest to the new revision/digest before exposing
output. Interrupted recovery may finish that exact saved successor. A database
behind the provider refuses; it cannot regenerate decisions or resurrect sources.
Rebuilding a projection replays immutable ciphertext facts without re-signing,
opening erased payloads or applying today's issuance policy. No provider, media,
signing or network work runs inside the SQL write transaction. The reference
implementation bounds an opaque context checkpoint at 32 MiB and its local event
history at 65,536 entries; each key seal/open keeps its own 64 KiB budget. These
are local capacity refusals, not an increase in public status or artifact limits.
This foundation alone does not qualify either runtime gate.


### Narrow bootstrap delegation and local consent

The root-admitted capability-issuance authority approves separate, beneficiary-
bound nym-only delegations for ordinary A/B and D's receiver. The existing V2
beneficiary equality is unchanged: a delegate issues only for its own participant
and Node. D cannot issue consent on behalf of A/B. Council certification, root
transport authority and local recipient consent remain independent.

`nym-bootstrap-consent` is a singleton issuance template; it cannot share a grant
with Messaging templates. Its host-resolved caller is `host:nym-bootstrap.accept`.
It can issue only an `inac-invitation@v1` child, single-use, for exactly one peer,
one P015 sealed family, one phase-qualified artifact ID, `application/json`, and
a TTL no greater than 900 seconds or the parent's remaining validity. The exact
INAC offer key (including the ciphertext digest) remains the consent reference.
The four families are `nym-key-request-sealed.v1`, `nym-key-offer-sealed.v1`,
`nym-issuance-request-sealed.v1` and `nym-issuance-decision-sealed.v1`.

An active parent delegation is not local consent. A/B's host must bind incoming
replies to a durable, approved local exchange intent, expected D peer, phase and
digest. D's host uses its separately installed issuer-receive policy to approve
the exact offered peer/phase/artifact; certificate admission is decided later.
A module cannot assert the host caller or impersonate an explicit operator.
Until these host adapters are implemented, the pure template alone cannot cause
an invitation. No sovereign fallback exists on the nym path. Grant status retains
its existing 300-second budget, independent of nym source-status freshness.
Nym-only grants do not make Messaging issuance/readiness ready and cannot issue
Messaging send or receive passports. This is the narrow P015 exception to P076's
original Messaging-only decision, not an expansion of its historical evidence.

### Qualification blockers found during implementation review (2026-10-26)

The reviewed private exchange draft required another correction before Gate A.
A still-live global bootstrap recipient can open historical first-leg metadata;
that metadata must not contain the participant, actual nym, context or real
signed-request digest. Use an independently random exchange handle and an
unlinked ephemeral proof key for that anonymous first leg. The full request
still carries the participant signature and actual nym proof inside its
per-exchange encrypted recipient.

Durable global replay binds the opaque handle and phase to the exact sealed
input digest, exact sealed output, artifact identity and finite deadline. It
must not retain a request-to-context/status/checkpoint join. Identifying reply
membership, decision material and quota belong in independently erasable
private snapshots; a phase-qualified provider fence preserves the same replay
bytes without reopening an erased map. Domain idempotency still uses the real
signed-request digest inside that private boundary. No pool of random handles
or transport receipt grants council authority.

A positive software attack probe reproduced the old bootstrap/checkpoint join.
The reviewed baseline also generated a public status revision for every request,
which exposed a reset through the new certificate's unique minimum revision.
Neither software conformance nor a passing workspace gate qualifies these
privacy properties. Gate A remains pending until both counterexamples fail on
the corrected design and the real private runtime is qualified. Gate B remains
pending independently. Timing analysis, the issuer's contemporaneous knowledge
and copies of its still-live keystore/image remain outside the erasure claim.


### Reference-owner status capacity and lifecycle

Status freshness requires schedulable work, not only a bounded number of rows.
The reference owner refreshes by due time before its ordinary maintenance
rotation and yields new issuance to runnable overdue status work. Its local
configuration capacity is derived from the profile freshness age, cadence,
cooperative work-slot budget and a reserved in-flight slot. Unsupported capacity
refuses before key-provider initialization. No new lease follows from a queue,
a retry or a budget overrun. These execution limits are not protocol namespace
limits; larger capacity needs separate throughput qualification.

A public lease refresh must not require re-encrypting an unchanged private
participant map or allocating new identifying-custody keys. It retains its own
recoverable publication/readback boundary and the last private-effects fence.
Reset eligibility drains the latest signed collection lease even if the private
map's cached lease predates that refresh. Key retirement, source rollback
protection and exact prepared decision replay remain unchanged. Local readers
must explicitly distinguish checkpoint semantics; no old reader may silently
use the cached private timestamp as the latest public lease.

The current-status consumer may checkpoint a verified cumulative signed head
and its exact high-water cursor, then atomically remove superseded cache facts
and bytes. Historical admission evidence is owned separately and is not pruned
by this cache lifecycle. A monotone per-profile retired-epoch floor frees ended
scope watches while refusing their reactivation after restart, rebuild or clock
rollback. The latest cumulative revocations and live-scope HWM are preserved;
retired floors cannot be reset to regain capacity. Local cache capacity is a
simultaneous-use limit, not a lifetime limit on valid status revisions or epochs.

### Uncommitted key allocation recovery

Publication-bound key records are also the durable inventory of unfinished
preparations. The single issuer writer must reconcile the complete committed
source with the provider high-water mark before destroying an allocation without
a publication boundary. A missing projection or an SQL error alone is not proof
that the candidate failed to commit. A committed candidate finishes its existing
fences and exact prepared output; an unused candidate is retired with a durable
no-recreation marker. Ambiguous, corrupt or restored old source refuses cleanup.
An unused epoch root survives until epoch end and is destroyed only after its
verified empty scope has no remaining candidate allocations. Startup and bounded
S020 maintenance resume this reconciliation without a publication ACK for a
candidate that was never published. No new permanent request-to-source join is
introduced for cleanup.

### Current implementation checkpoint (2026-10-28)

The dated 2026-10-26 counterexamples above remain historical review findings.
The Node foundation now has software regressions for anonymous first-leg
metadata, independent erasable reply membership, and the post-reset collection
lease drain. They are not substitutes for the complete runtime privacy gate.

A clean-source private diagnostic has exercised issue, renewal with a new nym
and the same contextual source, ordinary protected host signing, and exact
certificate/authoring readback after applicant and issuer restart. The following
private reset expired during processing and remains an original refusal. No
request window was extended and no complete Gate A/B result is claimed.

The implementation now authenticates a sealed request and binds its custody from
one immutable allocation, removing repeated metadata decryption and provider
inspection. Controlled-media conformance measures 16 versus 8 attestations for
that input path. Actual key leases, media checks and request/signing/commit
expiry rules remain intact; the measurement does not promise a latency bound.
A new clean-candidate reset probe and the full two-gate qualification are still
required. See `node:nym-issuer-service/README.md` and the Node implementation
ledger for repository-local implementation status.

The 2026-10-28 status/ownership review is implemented at Node `d69a5fec`:
118 issuer and 58 host tests pass, including pre/post-commit allocation recovery,
deadline priority/backpressure, cumulative-checkpoint rollback, atomic cleanup
refusal, and capacity reuse after a full 1024-watch epoch. Strict all-target
Clippy and documentation checks pass. At that source revision, full/light
workspace gates refused on the independently owned Sensorium evidence-history
budget. This is software
conformance, not the runtime qualification of either Gate A or Gate B; the
P015-001–003 tracker and the aggregate authorship slice remain incomplete.

## Consumer: author disclosure conditions (2026-10-27)

[P013 author disclosure conditions](../013-whisper-social-signal-exchange/author-disclosure-conditions.md#author-disclosure-conditions)
count this profile's sources without changing the profile. They evaluate one
epoch at a time and never sum epochs. In the protected signal's epoch they
exclude the author's `source/ref` exactly; in later epochs they require one
additional source, because the author cannot be recognized there. They use the
same status freshness, revocation and publication-time rules as first emission.
Implement these consumers over one revision-bound contribution evaluator, with
separate coordination participation/latch and disclosure-consent decisions;
[P013's implementation recommendations](../013-whisper-social-signal-exchange/author-disclosure-conditions.md#implementation-recommendations)
own its count/evidence shape and replay fixtures. The existing M4 node-counting
path is not a contextual-source implementation and keeps its historical ids.
Privately carried v2 signals reach the counting authority without a relay, so
their publication-time evidence must come from that authority's durable
admission receipt. Gate B qualifies Agora carriage only; the private carriage
belongs to `P013-ADC-004`.

## Consumer: long-lived rumors (2026-10-27)

[P013 long-lived rumors](../013-whisper-social-signal-exchange/long-lived-rumors.md#long-lived-rumors-and-historical-authorship)
keep certificates short. The SQLite admission receipt used above as
publication-time evidence becomes an instance of the portable
[`agora-admission-receipt.v1`](../035-agora-topic-addressed-record-relay.md#portable-admission-receipts-2026-10-27),
so other nodes can verify later that a record was admitted while its nym proof
was valid. That historical validity grants no current authority and does not
extend this profile's epoch or counting rules.

Case-bound succession adds no public succession to this profile. Routine
renewal still keeps the source without any succession artifact, and a private
reset still publishes no successor. A participant who wants a later nym to
continue one case uses
[`nym-succession.v2`](../015-nym-certificates-and-renewal-baseline.md#succession-after-expiry-and-the-narrow-successor-2026-10-27)
with scope `case`, authorized by a continuity key committed in the case's first
signal and delivered privately to a named audience
([P013-LLR-007](../013-whisper-social-signal-exchange/long-lived-rumors.md#case-continuity-key-and-case-bound-succession)).
The predecessor nym key is not kept for that purpose.


## Resumed qualification and refresh scheduling (2026-10-28)

The resumed Node `b7f184be` diagnostic observed an issued certificate through
ordinary private AD and a protected host signature with confidence 0.5. Its
renewal expired after repeated `nym-issuer-status-maintenance-due` decisions;
the original refusal is retained and does not qualify Gate A or Gate B.

The implementation separates two local execution deadlines. Early status refresh
is scheduled at 10% of the emission freshness age. Issuance backpressure reserves
one provider work slot before the earlier of actual emission freshness and signed
status expiry. A successful provider call may outlast the early scheduling age;
that alone must not eliminate every issuance window. A failed refresh's backoff
cannot extend the admission boundary. These scheduling rules neither alter the
profile digest and validity limits nor turn a stale status into emission authority.
Full certification lifecycle and contextual relay/aggregate qualification remain
required before closing the two gates.


The subsequent clean `4777ccd5` private repeat reached renewal's full-request
invitation but retained consent-busy refusal. Prepared ciphertext/readback lookup
now uses the existing immutable output/provider/expiry checks without taking the
runtime mutation fence. Channel-gated concurrency conformance and all 123 issuer
cases pass. Neither this owner repair nor either private probe qualifies the
complete lifecycle or contextual relay/aggregate runtime.


The clean `bd825b2e` cycle completed ordinary issue and renewal, with a new nym,
the same source and exact signed readback. Reset retained expiry after repeated
AD retry collisions with maintenance. A bounded, transient ingress hint now
allows a turn between work slots while preserving hard freshness backpressure,
ordinary maintenance attempts and the original signed request deadline. The hint
is neither an admission fact nor a new transport queue. Conformance passes 126
issuer and seven issuer-host cases; actual complete lifecycle and Gate B remain
unqualified.


### Shared consumer boundary (2026-10-29)

Node's `whisper-core` now owns a pure, revision-bound source-contribution
evaluator for coordination and later disclosure consumers. It counts distinct
admitted sources in one complete exact epoch inventory, retains all eligible
records, filters revocations before representative choice and commits the private
evidence basis. It does not create admission facts, nonce reservations, authority,
consent or a first-emission latch. Incomplete inventory and stale status remain
unavailable. The historical node-counting M4 qualification is unchanged.

Seventy-five component conformance cases and strict all-target Clippy pass.
Private `a77105e2` diagnostics observed ordinary AD issue, renewal and reset;
a separate lazy renewal after reset activation preserved exact certificate and
signed-record readbacks across A/D restart. An original pre-reset ciphertext
probe returned `key-destroyed` after pre-existing provider destruction. Those
observations and the retained original harness refusals are not complete Gate A/B
qualification. Both gates remain pending in the tracker and Node ledger.


### Authenticated scope refresh during issuance (2026-10-29)

The issuer's local scheduler must distinguish an anonymous reservation from a
full authenticated request that will publish a fresh status for its own exact
scope. That full decision can perform its own refresh under the same mutation
fence and mandatory publication/readback. Waiting first for a separate refresh
of that same scope can otherwise consume every retry until a valid request
expires. Other due contexts retain their reservation; an anonymous request
cannot choose or infer the excluded scope.

The `fb133aa9` diagnostic's immutable AD attempt history records six such
maintenance-due results followed by original expiry. The repair changes no
profile identity, signed deadline, reset activation drain, status lease or
independent council policy. An end-of-epoch renewal that cannot extend validity
still receives a signed refusal. This is an owner execution correction, with
both full runtime gates still pending after it.


### Local atomic-admission foundation (2026-10-29)

The Node SQLite owner now composes pending contextual verification with its
existing relay ingest. The exact author buffer, signed relay-clock receipt,
nonce/record reservation, admission facts and selected cumulative status
checkpoint commit together. Signature verification precedes SQL; checkpoint CAS,
collection freshness and epoch closure are checked at commit. Repeated delivery
of the completed command preserves its original facts, and a generic historical
record cannot acquire a retroactive admission/time claim.

This storage mechanism implements the earlier atomicity decision; it does not
create issuer trust, authorize publication, replace backend clock policy or emit
an aggregate. Contextual HTTP/Matrix wiring, the host/UI flow, current source
projection and first-emission CAS remain implementation/qualification obligations.
No tracker gate is closed by signed-fixture SQLite tests.

A clean `d7595742` private repeat completed ordinary AD issue, lazy renewal,
private reset, refusal before activation, protected signing after activation and
exact certificate/request/document readback after A/D restart. This is a diagnostic
lifecycle, not the complete Gate A qualifier. The old-ciphertext probe also remains
a limited refusal check: routine snapshot replacement can retire its key, so that
probe alone does not establish reset-caused erasure. Gate A and Gate B remain
pending, with original failed attempts preserved and no readiness promotion.

A successful local contextual mutation now retains a nanosecond clock high-water
checkpoint alongside its status/admission transaction. Reopening cannot accept a
cryptographically valid decision earlier than this owner already observed.
Missing clock state beside contextual history is an explicit refusal, not a new
initialization. Readback and exact completed-command retry keep original facts.
This local restart fence does not claim protection against restoring an entire
older database. The clean Node `c09fa017` / Orbidocs `8e12cae7` full software gate
passed 9,097 tests with zero failures and 127 explicit ignores; that baseline
precedes the separately tested clock correction and does not qualify A or B.


### Source/checkpoint composition and actual private diagnostics (2026-10-29)

The SQLite owner now accepts the same opaque contextual preparation beside a
Matrix source decision. Exact author bytes, independently admitted clock source,
event binding and first local receipt are checked before the transaction; nonce,
status CAS, admission, source, retained time and account/job progress commit
together. Multiple carriers preserve one first locally admitted fact. An existing
rejected event cannot be upgraded or leave an orphan reservation. The pure Matrix
codec/client and wire carrier remain independent of this optional owner policy.
Signed fixture tests cover source/checkpoint and history-job rollback, restart,
status races, duplicate observations and clock/source substitution. They do not
qualify Synapse or the contextual service/UI/projection path.

The `d7595742` runtime also observed ordinary issue53/renewal54/reset55 and a
separate signed council refusal over still-admitted AD transport. A sequential
provider probe verified the same live binding MAC before reset and
`key-destroyed` after the actual reset and retirement buffer; no key or private map
was exported. Its initial concurrent-provider startup refusal remains preserved.
A/D restart preserved the exact certificate, request reference, preview and signed
record without a new signing/issuance command. These remain scoped private
diagnostics pending complete independent case qualification and retention.
No A/B gate, aggregate, disclosure or global readiness status is promoted.


The later probe review removes automatic recovery-bundle downloads. A missing
current recovery bundle stops the canonical runner after stable preparation;
the operator completes protected recovery/export separately, outside retained
evidence/cache, before resuming the same operation/deadline. Older diagnostic
runs that downloaded/discarded the response do not establish recoverable custody.
The public v2 signal boundary now reuses the existing nym/proof/kind and public
disclosure/routing checks; direct routing cannot silently pass as unknown v2
content. This preserves the adopted carrier policy without qualifying contextual
counting, UI, aggregate emission or either full runtime gate.


The later receiver composition carries the same opaque contextual preparation
through decoding to the existing source/checkpoint transaction. A deferred event
preserves its original local receipt while admission evaluates the new status
and epoch clock. Exact signed fixtures cover reopen, event-token substitution
and rollback. Service policy wiring, UI and actual SQLite/Synapse qualification
remain separate pending Gate B obligations; this port does not change the
adopted publication-time authority or promote either gate.


### Host-owned source-status acquisition

`identity.nym.source-status.acquire` accepts the closed
`nym-source-status-acquire.local.v1`: an already adopted profile digest, a
council-signed contextual certificate and explicit `collection` or
`first-emission` purpose. The certificate determines context/epoch. The caller
cannot supply a clock, endpoint, issuer adoption, private minimum revision or
signing authority. Invalid certificates and unknown profiles acquire no watch.

The optional host cache registers that verified live scope idempotently for its
existing bounded S020 refresh job. The request performs no network fetch or Vault
operation. `nym-source-status-result.local.v1` distinguishes an available signed
snapshot from pending/unavailable or stale refresh. Available means status bytes
for that purpose, not certificate eligibility, record admission or permission to
emit. In particular, a revoked certificate can obtain the signed status that
proves its revocation. Callers recheck signatures, scope and time at use.

The authenticated current-operator route and explicitly adopted authenticated
receiver module bindings use the same owner. The receiver role is an exact local
operator selection, independent of package names and signing domains. Node's
startup `identity.nym_status_consumer_modules` policy defaults to the existing
`agora-service` binding; an explicit list replaces it, including an empty disabled
selection. It admits at most 16 distinct canonical module IDs. Null, duplicate,
malformed and reserved local-control selectors refuse; matching never normalizes
or expands aliases. Selection creates neither a credential nor an instance.
Independent receivers additionally present their current signed launch and exact
live channel identity. A registry entry or another module credential grants no
access. Acquisition does not require a certificate to be
unexpired now: the receiving owner separately verifies its trusted publication
time. Ended epochs do not gain a new watch or lease. Existing cumulative status
high-water marks and retirement remain authoritative. Missing refresh or storage
is deferred unavailability, never permission to fall back to the old P081 nonce
cache or to author-provided status/time. Implementation and qualification remain
separate from this contract.

The reference receiving service adopts profiles independently of the host cache.
Its Matrix observation is bound to the authenticated client/account and configured
clock authority. V2 admission has no fallback to the legacy current-certificate
nonce cache. A distinct transport carrier of an already locally admitted record
preserves its first admission and nonce decision; new carrier bytes/provenance
remain separate. This historical read path cannot create missing domain facts or
renew their time/status. Missing original record/author material is corruption,
not a new admission opportunity. Software composition does not qualify Gate B.


### Ordinary SQLite publisher composition (2026-10-29)

The reference local publisher independently adopts a relay clock and a named
protected host proxy. That adoption does not grant the module a signing domain,
unlock a key or derive trust from a certificate. Existing publisher ACL, content,
disclosure, namespace and size checks remain in front of contextual admission.
The host signs only the receipt's exact author-buffer-bound preimage outside SQL.

A newly prepared local receipt is not yet publication. Its record, exact author
bytes, admission facts, nonce and receipt must commit together within the adopted
profile's clock-skew window, checked after acquiring the writer. A separately
durable receipt received late has a different path and preserves its original
publication time. Neither path substitutes authored time or creates a missing
historical fact. Exact completed-command readback uses the first receipt and
repairs its derived index, without a new status acquisition or signature; a valid
alternate JSON spelling remains an alternate buffer. Concurrent identical calls
cannot replace the winning receipt with their later private preparations.

This service composition does not emit the contextual threshold. UI, Matrix
publisher composition, current-source projection and full Gates A/B remain open.
The actual clean candidate19 diagnostic issued and renewed through ordinary AD
and protected host authorship. Its reset attempt retained an invitation-observation
refusal, and an earlier recovery download exceeded the observation tool's bound.
Encrypted authority recovery is retained separately from evidence; no old request
deadline, formal acceptance claim or global readiness status is changed.


### Selected ordinary SQLite observations (2026-10-29)

Node's reviewed `2084117d` owner candidate, with the separately pinned ordinary
`6efe21bd` Agora service, completed independent A/B certification through private
AD, host/Vault signatures at confidence 0.5 and two C SQLite HTTP 201 publications
under one exact profile/context/epoch. C restart/readback preserved the original
author buffers, signed clock receipts and admission facts after certificate expiry.
Receipt signatures and both retained host documents passed separate checks.

A recoverable prepared-status startup refusal was reproduced and repaired without
publishing at open or treating a private candidate as available status. A missing
B fixture transport/allowlist retained its real refusal before explicit narrow
preparation; no transport grant was treated as AD or council authority.

These selected observations do not close P015-001–003 or Gate B. Complete private
lifecycle/failure qualification, certification UI, live contextual counting and
first-emission orchestration, actual Synapse/PDU, replay and both-store retention
remain required. See Node's
[resumption review](https://github.com/diapod/node/blob/master/docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md)
for source-specific outcomes and preserved refusals. Historical node-counting M4,
global Agora and release readiness retain their prior scope.


### Complete local inventory component (2026-10-29)

The optional Node SQLite source owner now reads a complete adopted
profile/context/epoch in bounded pages. Its private cursor and completion seal
remain tied to the exact open owner. Per-scope source transaction revisions fence
concurrent admission, status and retained dependency changes; another scope does
not invalidate the read. A missing signed checkpoint is unknown, not zero, and
a missing empty-scope head cannot reset its retained rollback history. Initial
control installation is atomic and later missing controls refuse.

These are component completeness/concurrency facts. The seal does not grant
admission, first-emission freshness or publication authority. The aggregate owner
still must compose current source evaluation and revalidate the pin inside its
actual durable mutation, with its clock and status policy. Component tests do
not close Gate A/B, P015-001–003 or historical M4. See the Node source-owner README
and resumption review for the bounded software scope.


### Source-owned first-emission draft component (2026-10-29)

The optional Node source owner now composes the complete local inventory with
the shared contextual-source evaluator. Typed retained facts are read after
verifying their byte/hash/record binding; arbitrary decoded facts do not acquire
live admission rights. The private preparation cannot accept a caller count or
substitute a different profile/context/epoch basis.

The first mutation repeats source/status CAS in the source transaction, samples
its clock and requires first-emission freshness. It freezes the selected signer
and both exact v2 drafts once. The proposal binds the threshold content address
before signing. Subsequent revocation changes the current count without
replacing the historical pair, and the frozen basis retains its signed status.
Partial control loss refuses rather than silently rearming first emission.

This is a bounded component implementation, not actual emission or Gate A/B
qualification. Host signing/publication scheduling, certification UI, complete
private failure coverage, Synapse/PDU, replay and both-store retention remain
required. Historical M4 and global readiness retain their existing scope.


The Node owner also retains the first verified host-signed buffers before
publication I/O and acknowledges only an actual durable local relay record.
Threshold submission precedes proposal submission. Local acknowledgement is not
Matrix forwarding or remote admission. Indexed selection is a bounded scheduling
hint, not an eligibility/completeness proof; cooperative interruption creates no
new emission fact. Unreleased local installation changes refuse unknown or old
developer controls rather than silently rearming a latch. These component laws
do not qualify the service scheduler, certification UI or either runtime gate.


The opt-in Node service composition now consumes the existing S020 module-job
contract. Explicit local adoption selects one profile, authority, output topic
and host key reference; incoming source fields cannot grant that authority.
The job shares the collection/first-emission status verifier and the source
owner's transaction fence, then uses ordinary protected host signing. Retained
signed buffers precede local submission; Matrix forwarding remains the existing
journal worker's responsibility. The module starts no private scheduler and
installs no default job. Component conformance does not establish actual
certification UI, source-result annotation or SQLite/Synapse qualification.


### Current source annotation contract (2026-10-30)

`whisper-contextual-source-view.local.v1` separates the current source count from
its last complete evaluation and the immutable first-emission references.
`eligible` and `below-threshold` require an unchanged complete source/status
revision and the emission freshness lease. Otherwise the current count is null
with `freshness-unknown`; the last evaluation remains explicitly historical.
At epoch closure the current count is zero and the state is `epoch-ended`.
A sampled clock earlier than the owner's committed high-water cannot produce
a fresh annotation. Reads neither advance that fence nor extend a status lease. A newer signed status or
source change invalidates the previous current count until reevaluation.

The read model is rebuildable. Deleting it must not erase or recreate the
source-owned first-emission latch. A collection-only update may persist an
annotation without authorizing a new pair. Its display is separate from the
signed proposal and cannot rewrite the historical claim or trigger publication.
A record-bound read retains that record's existing topic ACL and independently
adopted local projection authority; imported claims cannot borrow a local basis.


Node now implements this read model over a rebuildable cache in the complete
source owner's transaction. The record-bound API and UI preserve the topic ACL
and exact frozen local claim binding. Refreshing a frozen pair does not frame or
publish another pair. Component conformance covers revocation/restoration,
freshness, corruption, rollback against the committed fence and cache rebuild.
This does not close the complete certification UI, durable result-change audit,
actual Gate A/B campaigns or retained proof obligations.

### Explicit local certification controls (2026-10-30)

The protected Node UI now projects the existing operator-local applicant API.
Each POST selects one explicit transition: prepare issue/renew/private reset,
prepare a key request, submit one prepared encrypted artifact through AD, inspect
its delivery, bind an exact reply offer, accept its exact INAC notification, or
read the retained result. No transition is inferred from delivery success or the
latest notification. Authority adoption remains an independent host decision.

Preparation keeps its operation identity and protected nym through a lost
response. A form-only JCS digest confirms the exact prepared intent. Changed
scope, operation or predecessor fields refuse before another owner transition;
readback does not confirm edited fields. This digest is not issuance authority.
A changed intent requires a new operation. The separate recovery guard
still applies; these controls never export recovery, approve a peer implicitly,
replace a reviewed authorship document or retry a mutation on transport failure.
A 401 may refresh local authentication only because it precedes owner dispatch.
The returned operation, profile, issuer and reply bindings must match the command.

The two mounted aliases share the authenticated operator proof, P095 private-view
catalogue, CSRF protection, private/no-store responses and passphrase omission.
Delivery, council decision, certificate validity/activation, status freshness and
relay admission stay distinct in UI and API. Component checks do not qualify the
actual private exchange, browser flow, SQLite/Synapse path or either Gate A/B.
The source-result audit and all retained runtime obligations remain open.


### Stable local basis identity and measured positive prefixes (2026-10-30)

The pure source evaluator distinguishes eligible-membership identity from
revision/time-bound evaluation evidence. The local membership preimage binds the
exact profile, context, epoch and sorted eligible source/record/certificate /
original-admission-proof tuples. Refreshing evaluation time or an otherwise
unchanged signed status does not create a membership change. A changed eligible
record or proof does, even when the distinct-source count is unchanged. The
existing evidence commitment and public signed contracts retain their preimages.

A subsequent source-owned result-change journal must preserve the first complete
evaluation and actual membership changes under the same source/status commit CAS.
It must retain the evaluated evidence and original status, remain separate from
the rebuildable latest-view cache, and never rearm first emission. Its installation
boundary cannot claim to reconstruct unrecorded earlier evaluations. The pure
identity primitive does not itself implement that journal.

The private Node continuation has now observed ordinary A/B AD certification,
protected host signing and a SQLite first pair after certificate expiry/restart.
A separate canonical Synapse case observed two admitted sources, one first pair,
exact author bytes through independent sync/durable source/full PDU, four native
signatures and an actual C restart. Its maximum selected full PDU was 9,245 B.
These positive prefixes do not close P015-003 or Gates A/B: full lifecycle,
erasure/refusal, the complete browser/refusal matrix, replay, complete privacy and
both-store retention qualification remain open. The Node ledger and resumption review own
source-specific observations. Historical transport qualifications remain unchanged.


### Source-owned result history component (2026-10-30)

Node now persists the initial complete evaluation and eligible-membership changes
in the source owner's transaction. It keeps the evaluated source/status revision,
original signed status, times and evidence commitments separate from the latest
cache and immutable first pair. Time/status refresh without membership change is
not another result change. Read-derived unknown freshness or epoch closure does
not fabricate a complete evaluation fact. Historical reads do not evaluate the
history against today's clock or grant admission/emission authority.

The local journal uses bounded exact-scope/authority keyset pages and commit order,
without implying chronological Matrix order. Current installation version 3 and
its separate journal marker refuse partial loss; an intact v2 upgrade preserves
the first pair and explicitly declares unknown prior evaluation coverage. Old
writers must be stopped before upgrade, and an old v2 opener refuses v3. Cache
rebuild never resets audit or emission ownership. Local integrity checks are not
portable attestation or whole-database rollback protection.

This is reviewed component implementation. The earlier private SQLite/Synapse
positive prefixes predate the journal. Actual journal/replay qualification and
full Gates A/B remain open; no historical transport or global readiness status
changes follow from this component step.

### Cold-start lock classification review (2026-10-30)

A later private signed-instance cold-copy startup preserved eight accepted records
and two immutable first pairs while installing the source result journal with
`prior-coverage-unknown`. This is an upgrade diagnostic, not fresh membership-change
or replay qualification. The original source database and instance remain intact.

Actual ordinary private AD issuance and the protected authorship UI reached
certificate readback and a retained preview. After restart, signing without an
unlock secret exposed a generic503 caused by loss of the typed protected-Vault
lock condition. The root owner now preserves the existing `KeyLocked` class for
P015423 handling. Missing status, invalid credentials and corruption remain
separate failures; unlock cannot extend certificate or preview validity. Component
tests and this correction do not close the pending fresh UI/runtime verification
or Gates A/B.

### Ordinary UI smoke and fixture-signer retirement (2026-10-30)

After the typed-lock correction, an actual private AD/UI probe completed issue,
certificate readback, retained review, daemon restart,423, explicit unlock and
host signing of the same document with `confidence=0.5`, followed by Matrix202
publication intent. Daemon842ef007 and separately pinned317a87a0 UI/service were
recorded independently. This is a positive narrow path, not receipt, erasure,
complete lifecycle/replay or both-store qualification.

The environment-selected deterministic nym signer is removed from current intake
runtime after that smoke. The current legacy Story-005 renderer no longer installs
its seed/source variables; v1 primary-participant host signing cannot stand in for
the new contextual source profile. Frozen historical tools and evidence retain
their exact bytes. Final Gate B still requires a clean candidate without that
side path and the complete qualification/retention matrix.


### Historical source inspection and delayed collection (2026-10-30)

The verification-only native adapter reuses ordinary source/admission, receipt,
status and aggregation owners at recorded times. It checks complete selected-scope
inventory and rederives both first-emission drafts from their original basis.
It creates no clock, nonce, source, signer or renewed admission authority.

A focused real AD/host signal published through the Matrix Client-Server API
before both certificate and one-shot proof expiry is admitted by C 8.9 seconds
after certificate expiry, within its original epoch. Independent read-only
`/sync`, exact author bytes and the complete signed PDU bind that observation.
Full PDU verification remains acceptance-only under the adopted
`authenticated-admitted-homeserver-v1` runtime policy. This focused case does not
qualify Node's publication path, a new scheduled aggregate lifecycle, homeserver
size enforcement or federation. The original observer failures and the valid
refusal of a different document published after its proof expiry remain distinct.

P015-001–003 and Gates A/B stay partial: the complete shared profile qualifier,
remaining runtime/uniqueness/privacy matrix and qualified two-store retention are
still outstanding. See the Node resumption review for exact source pins and
measured scope. No historical M4 or global readiness claim is promoted.


### Independently inspected ordinary UI paths (2026-11-02)

The subsequent Node continuation independently inspects ordinary private AD and
protected host UI authoring on both SQLite and Matrix. The corrected Matrix
receiver starts without a live subscriber; actual restart and carrier replay
preserve original admission, author bytes and first-emission facts. Exact author
bytes also match an independent read-only sync observer and full stock Synapse
PDU. These are narrow measured cases, not a renewal of all historical transport
claims. The complete software gate passes on Node `925f68a2` / Orbidocs `e767bf32`
with 9,259 passes, zero failures and 127 existing ignores. Subsequent fixture
context/expiry refusals remain refused; no signed deadline is extended.

P015-001–003 and both complete A/B gates remain partial. The outstanding
authority/status/reset/erasure-crash/privacy matrix, final backend campaign and
identical loose/extracted/fresh two-store qualification still govern closure.
Node's current ledger and dated resumption audit own detailed source/capture
pins and individual results. Development retention, original protected evidence
and global Agora/Whisper/release scope remain unchanged.


### Qualification checkpoint (2026-11-02)

The corrected runtime independently verifies ordinary AD issue, lazy renewal
after actual certificate expiry, and private reset on the same protected path.
Fresh signed statuses and the certificate confirm reset activation after the
latest pre-reset collection lease plus the unchanged skew. A concrete old
ciphertext sample from a pre-reset application DB receives `KeyDestroyed` without
copying the keystore. This does not cover the full crash/WAL/export matrix.
An original private controller bookkeeping refusal remains preserved; independent
reinspection repeats no issuance/reset command. The clean Node software gate
passes 9,264/0/127 on `7a75376f` / docs `70b0c2a4`. Neither software checks nor
these selected runtime predicates close Gate A/B. The then-pending duplicate/
lost-reply predicate is advanced by the following checkpoint; authority, status,
erasure/privacy and final backend/retention obligations remain pending.
The Node audit and implementation ledger carry the precise source/proof scope.


### Controlled private response recovery (2026-11-02)

Clean capture `e100b94d` with frozen runtime `bde3272f` completes a real
80.94-second four-process-birth A/D case. The same full request is submitted
twice; an original private response attempt fails while A is stopped. D then
stops and both owners restart. The prepared ciphertext, delivery plan and
expiry, nym, request deadline and owner decision remain exact, and the original
consented AD response reaches A. Explicit protected recovery and cleanup pass.

A fresh read-only predicate independently verifies issue, reference readback,
duplicate-request/reply and lost-response/restart subsets against original
observations, ready bootstrap capabilities and the native certificate verifier.
The default predicate refuses the unchanged `fault-injected-runtime` class.
This is controlled offline delivery failure within original AD expiry, not a
claim of spontaneous ACK loss or late retransport. The capture now separately
waits for issuer admission and initial AD submission, using only readbacks
within the original request window. Original prefix refusals remain intact.

The harness has 137 strict conformance passes and a green light gate. Full
software checks retain their separately pinned earlier revisions. P015-001–003
and both full runtime gates remain `partial`: the remaining authority/status/
erasure/privacy matrix, final SQLite/Synapse campaign and equivalent fresh
qualification from both retained locations still govern closure. The Node
resumption audit and implementation ledger own detailed source/proof bindings.


### Encrypted-provider process interruption subset (2026-11-02)

Node `7da785e9` / docs `206f0acc` now has four controlled native process cuts
and independent read-only predicates for those exact crash obligations. Each
cut uses a fresh provider on the adopted encrypted fixture. Startup after the
durable fence must leave the destroyed receipt and no key entry before a
recovering key API runs; before the fence, explicit replay remains necessary.
Original ciphertext and operation recreation then refuse with `KeyDestroyed`.
The earlier open-plus-state observation is preserved and refuses this stronger
predicate. These are process interruptions, not power-loss qualification.

139 provider and 149 harness conformance cases plus scoped strict Clippy/light
checks pass. The Node resumption audit owns report/binary bindings. Remaining
authority/status/old-database/privacy matrices, final SQLite/Synapse Gate B and
fresh equivalent two-store retention keep P015-001–003 and aggregate A/B partial.


### Fresh software prerequisite and proof inventory (2026-11-02)

Clean Node `16675e10` / docs `5d668ed6` passes the full nonincremental software
gate: 9,267 passed, zero failed, 128 explicit ignores, strict workspace/all-target
Clippy and final paths. The pair remains clean and unchanged throughout.
A fresh independent composition verifies 14/66 obligations, using 13 native
inspections plus the four-cut predicate over exact original inputs.52 still
remain open; the old six-obligation inventory keeps its historical scope.

These are software prerequisites and verified subsets, not complete Gate A/B or
final both-store qualification. Subsequent history-count proofs must independently
derive later bases; stale-database restoration must be tested within the live
epoch so expiry cannot supply a false explanation. The Node ledger and resumption
audit carry exact source/log/remaining-matrix bindings. P015-001–003 stay partial.


### Independent complete-inventory inspection review (2026-11-02)

The Node acceptance verifier now has an explicit complete local inventory-cut
mode, separate from the historical timestamp-selected adapter. It rederives the
last recorded count, membership and evidence commitment with the ordinary owner
evaluator and original signed status/time. Earlier transitions require their
own snapshots. First drafts are verified only when that complete inventory also
matches their original evidence commitment and stricter emission freshness;
a later reset cut instead reports that an earlier cut is required.

Original SQLite/Matrix/uniqueness snapshots and a repaired-hash count mutation
exercise this distinction. These are conformance checks, not a renewed backend
runtime campaign.151 harness/102 package cases and scoped Clippy pass. A separate
real same-live-epoch old-DB restore refuses `issuer-state-rollback`, with original
DB/provider/config preserved and current readback restored. The readback occurs
outside the certificate window and does not prove renewed signing usability.
The Node audit records exact identities and the preserved unsuccessful observer.

P015-001–003 and Gates A/B remain partial: the independently verified inventory
is still14/66, with final authority/status/erasure/privacy/backend and equivalent
both-store qualification required. No production wire/profile/admission semantic
changes or readiness promotion follow from this inspector review.


A subsequent actual same-epoch control on frozen application `bde3272f` and clean
capture `0c435ea0` / docs `e5def2aa` completes ordinary issue/reset, native refusal
of the stopped old DB, exact config restoration, ordinary renewal and host
signing confidence0.5. Fresh read-only inspection performs six native checks of
original AD, certificates and the exact review/signature. It verifies usability
of the current new source after refusal, beyond the earlier late readback.
The Node audit records original identities. The formal composite old-DB predicate,
remaining matrices and final both-store A/B qualification still govern closure;
the independently composed inventory remains14/66 and P015 stays partial.


The subsequent profile-owned composite reader binds that original stopped
snapshot and distinct native refusal to the ordinary AD issue/reset/renewal
predicates and exact restored host review. It can establish only the controlled
`A/old-database-restore` obligation, with fault-injected origin. A clean-source
reinspection must produce its proof; stored success flags and archived procedures
are not authority. Remaining gate and final retention requirements are unchanged.

Fresh clean Node `c0b8e690` / Orbidocs `806b86b9` composition makes19 native
checks over1725 original artifacts and verifies15/66 obligations, including only
the newly added controlled old-database restore.51 remain missing.161 strict
Python cases and light/documentation gates pass; full A/B and both-store
qualification remain open. The Node audit binds the original result digest.


Stay-ready implementation checkpoint: Node now has pure consent/planning values
with bounded slots, immutable CAS transitions, fixed operation/time, exact
representable75–95% bounds and preserved source activation across renewal.
The next Node component checkpoint adds a separately sealed host consent source
and protected approval/readback/CAS-revocation API. It derives the scope from
an accepted owned certification; duplicate approval cannot replace revocation
or replenish an allowance. P072 registers three literal operator-only host
routes, without generic dispatch or passport authority. Their readback explicitly
reports execution as not enabled. The subsequent source checkpoint stores the
exact reserved operation, deadline and certificate and uses separate local
high-water marks to refuse rollback of SQLite/WAL. It can complete only the
original authenticated one-step SQL successor, without resealing or repeating
a command. This guarantee assumes preserved current authority anchors; an old
whole-host snapshot cannot substitute for them. The effect-fenced S020 consumer,
explicit replacement, operator UI and real unlock/recovery continuation remain
required before renewal-consent conformance can be granted. A/B remains
15/66; these component changes add no runtime acceptance.


### Narrow runtime and predicate review — 2026-11-03

The corrected issuer dispatch, current receiver admission/native pins and
fresh-process readiness are exercised by ordinary SQLite and Matrix UI cases.
They preserve the reviewed document through restart/423/unlock and publish
confidence 0.5 with host-held nyms. Independent native checks cover the signed
SQLite receipt, the original two-source Matrix first basis after certificate
expiry, and five complete Node-created v10 PDUs (maximum 9,285 B). A separate
read-only `/sync` client observes exact author buffers. Runtime still trusts the
explicitly adopted authenticated homeserver clock; full PDU verification remains
an acceptance operation. This does not renew transport-wide or federation claims.

The emitting C/D operator continuation is distinct from the earlier UI starts.
Read-only composition must bind its independently adopted capture driver,
actual processes, exact successful S020 receipt, subsequent public records and
original complete native source cut. Missing or substituted lineage refuses;
it is not inferred from a later SQLite snapshot or serialized success flags.
The first software attempt's temporary-path/ancestry refusals remain recorded;
its assertions and shared-volume permissions are preserved for a corrected run.

P015-001–003 and both whole gates remain `partial`. The prior 15/66 composition
retains its original scope; later narrow observations and new component
predicates require their own clean composition. Remaining authority/status/
erasure/privacy/backend/replay matrices and equivalent two-store retention are
still required. See `node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md`.


The acceptance-only Matrix composition additionally requires an independently
adopted standalone read-only client, its original process and ordered `/sync`
observations, exact source author buffers and complete PDU/export rows for the
same explicitly selected complete source cut. Retained aggregate author buffers
are facts separate from their typed signatures; absent buffers remain absent.
Fresh native hash/signature/size verification does not change the runtime clock
policy or establish room authorization/federation. Representative subsets cannot
stand in for full campaign coverage. Both whole gates and retained qualification
remain partial until the remaining obligations are composed.


A projector continuation may use the explicit acceptance protocol
`bounded-launches.v2`: 1–16 ordinary S020 operator launches, each bound to its
own original HTTP payload and indexed typed receipt, followed by the final
public read. The original single-launch format keeps its exact one-step rule.
This accommodates bounded projector work phases without changing launch
permissions, treating a busy 409 as success, or inferring missing execution
facts from the source snapshot. A controlled fixture explicitly disables its
projector's periodic dispatch in configuration before publication, then uses
authorized `run-once`. Process-local pause is not claimed to survive scheduler
registration on restart. The fixture restores periodicity by explicit adoption
afterwards. Both whole authorship gates remain partial.


The controlled SQLite pair at clean Node `591ecf06` / Orbidocs `cd17826c`
now produces one original threshold/proposal pair after both accepted signal
certificates expire beyond skew. Six separately receipted ordinary S020 steps
complete bounded projector phases; fresh native inspection verifies the complete
first basis and both original signed receipts. Explicit fixture periodicity is
restored afterwards. This is a narrow backend result, not complete Gate B or a
change to the last combined15/66 coverage inventory. The separately pinned
Node `0c2e4894` / Orbidocs `2ddb7ef0` full software gate passes9,313/0/128 with
strict Clippy and paths; software prerequisites do not establish either runtime
gate. Qualification review adds pre-read logical-path refusals. Full A/B and
final both-store qualification remain partial; the Node resumption audit owns
the exact observations and failure scope.


A fresh clean Node `f9ec2370` read-only composition now verifies22/66 obligations
through49 native inspections of original inputs. The22 include narrow SQLite and
Matrix first-pair/expiry, SQLite signed receipts and the independent observer/full
PDU cut;44 remain. This is an explicitly heterogeneous prefix inventory, not a
final single-candidate A/B campaign or both-store qualification. Subsequent
ordinary A/A2 UI and a separately receipted sole-source control complete with
restored fixture periodicity; their uniqueness predicate is still pending.
An acceptance-only registration adapter separately adopts the fixture participant
root and reuses existing nym-bootstrap grant verification. It neither enrolls a
council nor grants current transport/revocation authority. Both whole gates and
optional stay-ready execution retain their partial scope.


The next clean Node `2928253c` composition verifies 24/66 obligations through
59 native inspections, including ordinary A/A2 renewal on distinct nodes with
one rooted participant and one evaluated source. Forty-two obligations remain;
these are original heterogeneous runtime prefixes, not final A/B qualification.
A later SQLite cohort observes the reset lifecycle 2/1/2 with an unchanged first
pair. Its independent three-cut predicate additionally verifies the persisted
current read model; membership history cannot substitute for status-only cache
refresh. Clean-source verification and the Matrix counterpart remain pending.
This verification-only tooling does not change the adopted homeserver clock,
certificate policy, admission, signing, renewal authority or global readiness.


Clean Node `3eef910b` subsequently verifies the original SQLite reset lifecycle:
complete before/revoked/replacement cuts, ordinary AD reset, signed old-source
revocation, replacement after the activation drain, unchanged first pair and
exact public current annotations. The full fresh prefix composition advances to
28/66 through71 native inspections;38 obligations remain. The current annotation
is independently checked through its owner and complete recorded basis, without
requiring status-only refresh to be a membership-history event. This scope does
not include the Matrix counterpart, final replay/privacy matrix, stay-ready
execution or loose/extracted/fresh-two-store equivalence. Whole A/B remain open.


Clean Node `9918b048` advances the fresh heterogeneous prefix inventory to 33/66
through 95 native inspections. The original Matrix A/A2 same-participant renewal
remains one source; the later A/A2/B reset has complete 2/1/2 cuts, signed
revocation, drained replacement, unchanged first pair and exact current annotations.
A later clean `4bf8df5a` separate read-only whoami/sync observer and seven native
inspections verify all six original lifecycle PDU, stored export rows and author
buffers (maximum canonical PDU 9,305 bytes). Runtime still uses the explicitly
adopted authenticated-homeserver observation, without a runtime PDU-verifier claim.
Thirty-three obligations, full A/B and final two-store qualification remain open.
The new read-only media-control predicates do not close those gates by themselves.


The original strict media control/refusals at clean Node `91c43334` advance the
heterogeneous prefix composition to35/66 (102 native inspections). The owner's
subsequent local fixture image-backup adoption above requires a new positive
preflight; the inventory now has67 obligations. The original refusal and its
scope remain unchanged, without promoting it to the newly requested success.
Full A/B, effect-fenced optional renewal and final retained-store equivalence
remain open. The Node audit records exact process, tool and runtime provenance.


The owner-approved positive image-backup case is now observed at clean Node
`37be7d02` / Orbidocs `16b1d962`: backing/mounted OS exclusions remain false/true,
the explicitly named effective-view rule derives false, and the read-only native
preflight attests under `allow-encrypted-image-backups`. The strict case still
refuses. No provider/key is created in the empty image. Fresh composition600
verifies36/67, including that new requirement, through102 native inspections;
31 remain. Copies of image/keystore stay outside erasure assurances. This is
heterogeneous prefix verification; final A/B and both-store qualification remain
open. The later exact bb060dd8/92d0fe7b full software repeat passes9315/0/128;
it does not promote that original prefix to a complete runtime gate.


### Explicit conformance composition — 2026-11-03

Clean Node `c6f57910` / Orbidocs `92d0fe7b` freshly composes42/67 obligations:
the prior36 runtime/native prefixes plus six separately classified component
conformance predicates. Exact named assertions, complete per-suite counters,
original source/process receipts and48 independently adopted schema byte pairs
are required. The schema-sync script's unit tests alone do not prove mirror
synchronization. The component tests keep their original `91c43334` / `4b50ef48`
source identity, distinct from the newer predicate and runtime prefixes.

The whole profile remains partial:13 A and12 backend B obligations, optional
stay-ready effects and final single-candidate/retained-store qualification remain.
Conformance neither creates runtime HTTP observations nor closes either gate.
The Node resumption audit and ledger own the exact command, review and result
provenance. No source-profile parameters, authority or historical evidence change.

The later clean Node `b212be6a` prefix composition613 verifies43/67 through103
native calls. `A/post-ack-erasure` now binds the exact complete original explicit
SQL key/ciphertext inventory, signed closing status, owner-local ACK deadline and
metadata observed before recovering provider open. The current v2 snapshot is
not substituted for a compacted historical v1 context. This does not claim
physical-block erasure, backup-keystore destruction or whole-AD/Vault privacy.
Twelve A and12 backend B obligations remain; optional stay-ready execution, final
single-candidate A/B and loose/extracted/fresh two-store qualification remain open.


## Independently verified source replay checkpoint (2026-11-03)

Clean Node `b7b2cf49` composition627 freshly verifies **45/67** obligations through
111 native inspections. Actual Matrix619 and SQLite622 restart after loss of only
the derived contextual cache and perform real owner replay. Original source,
admission, nonce, receipt, first-emission and history tables remain unchanged.
A separate ended-epoch/no-cache verifier checks the actual current readback; it
neither weakens fresh-view assertions nor supplies fresh active-epoch evidence.
Original fresh-only refusal624 remains preserved.

Twelve A authority/status/privacy and five B cases per backend remain. Runtime,
capture and verifier pins differ explicitly. The heterogeneous prefix inventory
does not close final single-candidate A/B or loose/extracted/fresh two-store
qualification. P015-001–003 and complete contextual authorship remain partial.
See `node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#independent-original-backend-replay-qualification-2026-11-03`.


The subsequent original631 controlled AD receiver cases observe rejection of
four encrypted invalid private requests, with no prepared decision or new target
context. Clean Node `e75dd92a` independently reinspects their valid baselines,
council offers and isolated faults in633. The temporary local source adapter is
explicit fault injection and is restored after D stops; it proves no INAC/network
authority. An expired anonymous first leg remains a separate narrower witness.
Process/input/effect qualification and recomposition are still required, so
coverage remains45/67 and both complete gates remain partial.


## Independently qualified private receiver refusal checkpoint (2026-11-03)

Clean Node `f270f62a` composition636 freshly verifies **49/67** obligations through
115 native inspections. Four original631 full-request refusals now have complete
process, exact input, AD receipt, offer/outbox/recipient and no-effect predicates.
No decision is prepared and no new issuer context appears. The temporary local
fault adapter is restored after D stops; this does not prove INAC authority.
The expired anonymous first leg remains separate from full-request expiry.

Eight A and five B cases per backend remain. Capture, runtime, fixture client,
native verifier and profile revisions are independently pinned. Final
single-candidate A/B, privacy and retained two-store equivalence remain open;
P015-001–003 and complete contextual authorship stay partial. Review:
`node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#independent-original-private-ad-refusal-qualification-2026-11-03`.


### Independent original full private-request expiry checkpoint (2026-11-03)

Clean Node `8d590a16` independently qualifies original638: a full, unchanged
private request and signed council key offer were valid when frozen; after the
original 30-second deadline, actual D runtime `103c8fae` permanently rejected
that exact sealed buffer with `expires/at: expired`. No decision or new target
context was created. Owned cleanup and temporary local adapter restoration
completed. Capture, client and native verifier are pinned to clean `153932f9`;
this controlled local AD refusal is distinct from INAC transport authority and
from the earlier narrower expired anonymous first leg.

Fresh composition641 covers **50/67** obligations through 116 native calls.
Seven A authority/status/privacy obligations and five B obligations per backend
remain open. The remaining B scope is late first receipt, collection/emission
freshness, public privacy, retired acceptance environment and UI refusals.
273 Python profile tests, 24 native inspector tests, five negative-client tests
and strict all-target Clippy for both affected crates pass without incremental
compilation. Scoped headers and the light gate pass; a broader header migration
audit separately refuses an existing unrelated Sensorium inventory mismatch,
which this work leaves untouched. Final single-candidate A/B and fresh two-store
retention remain unqualified. P015-001–003, full Whisper and global readiness
retain their partial/bounded scopes; historical runtime evidence is unchanged.

Status-owner checkpoint (2026-11-03): original648 observed actual host S020
progression from signed revision4 to5, refused refresh of an older still-valid
status, and the retained higher HWM after A restart. Frozen native42 from clean
Node `a2ae9913` freshly verifies original signatures/time/cursor in inspection650.
The complete process/proxy/HTTP/source-image predicate is still pending; this
adds no qualified coverage yet (**50/67** remains). The final forward read was
cache-only and does not prove a completed healing fetch. Original647's ordinary
AD certificate and separate protected fixture recovery steps prepare these cases;
its ended fixture epoch is historical input, not new authoring authority. All
owned actors and the proxy stopped, and A's adoption was restored. P015 remains
partial; final A/B and retained two-store qualification remain open.


### Independently qualified status-HWM checkpoint (2026-11-03)

Complete qualification653 at clean Node `bc480a7a` binds original648's actual
A/D processes, S020 proxy response bytes, scoped HTTP reads and immutable source
images. It verifies signed revision4→5 progression, refusal of older still-valid
bytes and the higher retained HWM/API after A restart. Native42 independently
checks original signature/time/cursor semantics. Original652's discriminator
refusal is preserved; the correction requires canonical integer `schema/v = 1`.
The final cached forward read remains distinct from a completed healing fetch.

Fresh composition654 covers **52/67** obligations in 118 native calls. Five A
cases and five B cases per backend remain open, along with final single-candidate
A/B and fresh retention from both adopted stores. Tests: 282 Python profile and
25 native inspector cases, affected all-target Clippy, scoped headers and light
gate pass without incremental compilation. No full historical runtime cohort
is renewed. P015-001–003, full Whisper and global readiness retain partial/bounded
scope. Owned A/D and proxy stopped and original A adoption was restored.


### Independently qualified private-minimum checkpoint (2026-11-03)

At clean Node `9e2c4dcb`, independent665 verifies original664: ordinary renew
retains public floor1 while the local private minimum13 refuses still-valid
signed status12. Actual preview returns the typed status-revision-unavailable
503 and readback has no authoring result. After actual status15 arrives, the same
certificate signs the reviewed confidence0.5 document through the ordinary host;
readback preserves the exact signed record. Four native checks verify certificate,
both statuses and reviewed record. Exact source/process/HTTP/proxy pins, original
time windows and cleanup/restoration bind the controlled runtime. No private
decision plaintext is reconstructed. Earlier producer failures remain unchanged.

Fresh composition666 covers **53/67** obligations in 122 native calls. Four A
cases remain: wrong exchange digest, revoked bootstrap authority, status
equivocation and private AD/tombstone privacy. Five B cases per backend, final
single-candidate A/B and fresh retention from both adopted stores remain open.
All 297 Python profile tests and scoped headers/light gate pass. Runtime source
`103c8fae` is unchanged; no full historical runtime or software gate is renewed.
P015-001–003, full Whisper and global readiness retain partial/bounded scope.
Owned A/D and proxy stopped; original A adoption restored. No merge/push.


### Independently qualified withdrawn-bootstrap checkpoint (2026-11-03)

Clean Node `b8dbfd76` inspection673 independently verifies original669: exact
valid INAC offer, signed active-to-revoked bootstrap authority, unlocked but
blocked issuer, actual403 before and after owned restart and absent issuer
reply/applicant certificate. Two native owner calls preserve the independently
adopted root and original times. The reason-only HTTP projection is retained
exactly and bound to separate captured coarse owner results; it is not expanded
into a claim of raw HTTP preservation. Original668 and672 coordinator failures
retain their original outcomes. Withdrawal is permanent, without reimport or
automatic authority replacement.

Fresh composition674 covers **54/67** obligations in 124 native calls over
8,446 logical reads/322,724,216 bytes; result SHA-256 is
`0319cbfc5bc6d6796bc6540516f3440425ee778d3054ca6fd202367c456c10b7`.
Three A cases remain (wrong exchange digest, status equivocation and private
AD/tombstone privacy), plus five B cases per backend, final single-candidate
qualification and fresh two-store retention. All310 Python profile tests pass;
the28 native and affected strict Clippy/paths evidence retains its stated source.
Native43 uses clean `85b8c9e3`, without incremental; runtime `103c8fae` is unchanged.
This does not renew the complete software/transport qualification or close
P015-001–003, either full gate, Whisper or release readiness. No merge/push.


### Independently qualified status-equivocation checkpoint (2026-11-03)

Clean Node `d14a3c89` inspection682 binds original681 actual host S020, exact
proxy response bodies, owner/control/process identities and four immutable
source images. Two correctly signed statuses have the same revision4 and
different canonical digests. The owner refuses the conflict before and after
A restart, preserving the original status, durable cursor and actual API view.
Three fresh native calls verify the certificate and both original-time conflict
transitions. Fixture-only operator signing and proxy adoption are restored;
no council key is exported. Native44 uses clean `107b436b`, separately from
runtime `103c8fae` and the later inspection source.

Fresh composition683 covers **55/67** obligations in127 native calls over
8,502 logical reads/323,488,096 bytes, with result SHA-256
`bde6f2270965e6f786f96e7e8524fc17b9ec1994d50b296a17f4d156ad06d181`.
The324 profile Python and29 native example tests, affected strict Clippy/paths,
scoped headers and light gate pass. At that checkpoint, two A cases remained
(wrong exchange digest and private AD/tombstone privacy), five B cases per backend, final single-candidate
qualification and fresh two-store retention. P015-001–003 and both full gates
retain their partial scope; no new full transport, software or release claim.

Original680 completes ordinary protected AD issue with two explicit recovery
exports. Original679 expiry and684 missing-decision outcomes remain failures.
For684, the correlated receiver row says `expires/at: expired`, while its AD
admission timestamp is5.274067 seconds before the original deadline. Exact
subsequent owner verification time is unknown. The earlier diagnostic's
arrival-after-expiry assumption is explicitly refused; the corrected source
snapshot/row correlation is retained separately. This does not qualify a
wrong-digest refusal or justify extending the signed deadline. Owned actors
are stopped, protected originals retained, and no merge/push occurs.


### 2026-11-03 private reply-binding implementation checkpoint

The earlier implementation checkpoint retained55/67 independently verified obligations.
Controlled original694 now observes an otherwise valid council-signed coarse reply
with a wrong private request digest being rejected by the actual applicant INAC
acceptor. Decision and certificate remain absent after the owned applicant restart.
Its independent profile closure was pending at that checkpoint; the later
qualified checkpoint below resolves this one obligation, not either full gate.
The current producer repair uses canonical Community ciphertext classification
for both exchange senders. Earlier runtime source pins and failed attempts remain
historical. See the Node resumption audit for exact source, control and verification
boundaries; an acceptance-only signed-pair inspection is not runtime admission.


### Independently qualified private-decision binding (2026-11-03)

Clean Node039b46ec inspection697 now qualifies `A/wrong-exchange-digest` from
original694. The profile binds actual owned A/D processes, authenticated controlled
AD submission, the exact INAC offer/notification/consent and sealed reply, the
stored typed applicant refusal, and unchanged absent decision/certificate after
restart. Later read-only source snapshots696 verify the exact original A/D
admissions without pretending to have been captured at the original admission
time. Native45 (cleanbe2781d6) freshly checks both council signatures, the anonymous
proof at original time and exact sealed public-recipient binding. It never
reconstructs the private request, decrypts, signs or creates admission.

Fresh composition698 verifies **56/67** obligations through128 native calls over
8,635 logical reads/344,823,251 bytes; result SHA-256
`16a18e3144219707ee004bfa0368e7c9599c520f072a012f4537a2da9e33e2a8`.
The339 profile conformance tests include corrupt/missing sources, rebound causes,
foreign owners, nonunique source identities and incomplete INAC/restart witnesses.
One A privacy obligation, five B obligations per backend, final current-candidate
qualification and identical fresh retained-store qualification remain.
P015-001--003 and both full gates stay partial; global Agora, full Whisper and
release readiness are unchanged. Earlier failed attempts and prefix-only claims
remain historical. No merge or push occurs.


### Independently audited private storage (2026-11-04)

Clean Node73dc0288 composition703 now verifies **57/67** obligations, covering
all30 A predicates, through128 fresh native calls and9,204 logical reads/
393,710,364 bytes. Result SHA-256:
`07263819db8740ecae49811dda153aaf18a63a7781daa24d60cda8578cece107`.
A profile-owned bounded audit checks561 later AD/INAC/issuer source entries and
composes the original ordinary issue/reset/renew and post-ACK-erasure predicates.
These later source cuts do not become admission-time observations.

Private INAC authorization passports may name their beneficiary and authorization/
delegation subjects at four exact fields. That permission is confined to private
transport metadata; it does not admit a participant-to-nym mapping, a private
request/decision nonce, successor linkage or primary identity in public artifacts.
The audit checks closed aggregate retention receipts and encrypted exchange
buffers; it does not claim whole-Vault privacy or completeness of historical
logs. No erasure guarantee for physical blocks or copied keystores is added.

351 profile tests and scoped source/light checks pass. The five B predicates per
backend, final clean current-candidate cohort and identical loose/extracted/
two-store qualification remain pending. All full gates and P015-001--003 remain
partial; neither global Agora nor release readiness is promoted. Existing
failed attempts and source-specific software results retain their exact scope.
See `node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#private-adinac-storage-privacy-closure-2026-11-04`.

The final source-boundary review rejects hidden/generated columns and user tables
resembling SQLite internals; fresh703 repeats the full57-predicate closure under
that guard. The earlier702 source-bound result remains historical and unchanged.


### Actual late first SQLite reception (2026-11-04)

Clean Node61b27ba8 composition719 verifies **58/67** obligations (A30/30,
B22/31 and six conformance),132 fresh native calls and9,359 logical reads/
398,848,754 bytes. Result SHA-256:
`d37a49f5ef00b0a160c708dcdd40caf4efb73ae3a19d36ef1483d1add0ac9ae4`.
The separately qualified ordinary UI715 publication and later receiving716 bind
the same exact author bytes and signed SQLite receipt. Publication is within
certificate validity; actual first reception is after expiry plus5s and before
epoch end. The receiving process uses existing SDK owner ports with SystemClock;
it is not an HTTP import, another signer or an invented historical clock.
Later consistent snapshots and original process observations are independently
checked; close/reopen does not replace the separate restart/replay predicate.

361 profile tests and scoped source/light checks pass. The original decoder,
missing-command and expired-delivery refusals retain their original outcomes.
Nine B predicates remain: Matrix late receipt and collection/emission freshness,
public privacy, retired acceptance environment and UI refusals on each backend.
The final current-candidate cohort and identical loose/extracted/fresh two-store
qualification are still required. Optional stay-ready effects remain not-enabled;
P015-001--003 and both full gates remain partial. No full software, transport,
global Whisper or release qualification is renewed. See
`node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#actual-late-first-sqlite-reception-2026-11-04`.


### Actual late Matrix reception (2026-11-04)

Clean Nodebf607f06 composition727 freshly verifies **59/67** obligations
(A30/30, B23/31 and six conformance),137 native calls and9,710 logical reads/
412,471,376 bytes. Result SHA-256:
`f75c33d9ce748abecae8c40458a897dd2ca1871db2c363ad2a1050399473dc15`.
Ordinary AD/protected host721 and confidence0.5 publication reach actual Synapse;
controlled503 sync/history refusal delays first C reception until after real
certificate expiry plus5s, before epoch end. Separate read-only observer723 and
complete9,317B room-v10 PDU724 bind exact author bytes, authenticated publication
time and original source/nonce to independently verified hashes/signature/size.
The controlled fault is not a homeserver failure; this is host/API authoring,
not another UI case. PDU verification is acceptance-only and adds no runtime
PDU verifier, portable time or federation guarantee.

All372 profile conformance tests and scoped source/light checks pass. Eight B
predicates remain: collection/emission freshness, public privacy, retired
acceptance environment and UI refusals on each backend. Final current-candidate
qualification and identical loose/extracted/fresh two-store retention remain
pending. Optional stay-ready effects remain not-enabled. Neither full gate,
P015-001--003, full Whisper/global Agora nor release readiness is promoted.
Original refusals and earlier source/software scopes stay unchanged. See
`node:docs/audits/WHISPER-AUTHORSHIP-RESUMPTION-2026-10-29.md#actual-late-matrix-reception-2026-11-04`.
