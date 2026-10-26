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

The current private exchange draft requires another correction before Gate A.
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
The current baseline also generated a public status revision for every request,
which exposed a reset through the new certificate's unique minimum revision.
Neither software conformance nor a passing workspace gate qualifies these
privacy properties. Gate A remains pending until both counterexamples fail on
the corrected design and the real private runtime is qualified. Gate B remains
pending independently. Timing analysis, the issuer's contemporaneous knowledge
and copies of its still-live keystore/image remain outside the erasure claim.
