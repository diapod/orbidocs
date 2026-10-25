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
A public certificate carries only its opaque source reference, profile/context,
epoch and minimum status revision. It carries no participant, source node,
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

For Matrix the evidence is a full PDU with verified content hash, event reference
hash and server signature, bound to room, event, sender and exact author bytes.
The configured server/key is an explicit time authority for this profile.
Verification of a signature alone does not establish an objective clock. The
runtime must request federation-format events; a Client-Server timestamp without
verified PDU evidence is insufficient. The qualified Synapse profile supports
federation-format `/sync` and `/messages`; unsupported adapters defer rather than
substituting the author's timestamp. Full PDU exports used by an acceptance
qualifier do not constitute runtime verification.

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
a new revision. Durable high-water marks survive restart and rebuild. A certificate's
minimum revision prevents reset from counting old and replacement sources at
once. Eligibility and the emission latch commit under the same status-revision
CAS. Imported claims cannot replace local eligibility or first-emission facts.

Previously accepted contributions survive natural certificate expiry, but cease
to count after source revocation or epoch end. Historical admission facts do not
change during replay; replay verifies their stored proof and policy identity,
not today's clock. The current view uses the current verified status separately.

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
request digest identifies the exchange and idempotent decision. Bind applicant
proof, proof of the new nym key, council, permitted reply recipient, operation,
nonce and deadline. Requests expire within 15 minutes and before epoch end.
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
entries each; retirement does not replenish issuance quota. The active plus
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
tombstones and aggregate counters can remain seven days.

Destruction durably retires a key, fences and drains operations, removes the key
file, fsyncs its directory and persists a receipt. Provider-local lifecycle
metadata prevents old DB restore from undoing retirement. Startup finishes due
destruction before decrypting private state. A missing key never invokes
get-or-create or mints a replacement counting source.

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
| New nym proof of possession | `orbiplex.nym-issuance-proof.v1` | `nym/proof`, `signature` |
| Participant request | `orbiplex.nym-issuance-request.v1` | `signature` (includes the nym proof) |
| Issuer decision | `orbiplex.nym-issuance-decision.v1` | `signature` |
| Source status | `orbiplex.nym-source-status.v1` | `signature` |
| Issuer exchange-key offer | `orbiplex.nym-exchange-key-offer.v1` | `signature` |

The certificate preserves v1: JCS of the certificate minus `signature`, **no
prefix**. Requiring NFC makes both existing certificate canonicalizers agree.
Verify the new nym PoP before the participant signature; verify both before any
issuance effect. The request digest hashes the complete canonical signed request
bytes, including both signatures. `exchange/digest` equals this request digest;
there is no independently chosen exchange identifier. Decision recipient and
issuer must equal the request's exact bindings. The certified nym/profile/context,
epoch and route must equal that request. A fresh nym may not reuse the applicant's
primary public key. A certificate must carry mandatory compatible Agora scope
restrictions: exact topic key, federation, record kind `whisper-signal`, content
schema `whisper-signal.v2`, and its supported disclosure scopes. The contextual
profile cannot be accepted through the generic verifier as an unrestricted nym.

D supplies a signed `nym-exchange-key-offer.v1` for a prepared request digest,
requesting participant, recipient D, public X25519 key/ref and expiry. Preparing
an offer does not decide issuance. The request already exists before the offer;
the offer is outside its signed bytes, avoiding a digest cycle. Key ref hashes
the 32 raw public-key bytes. Replies use the applicant's signed `reply/key` from
the accepted request. No unbound reply address or key is accepted.

The offer bootstrap is a separate private exchange, not a plaintext AD reply.
A prepares the complete signed issuance request first. A then signs the narrow
`nym-exchange-key-request.v1`: applicant, approved profile/issuer, exact issuance
request digest, signed reply key/recipient, issue time and expiry. It contains no
nym, context, source, predecessor or certificate. Its signature preimage is
`orbiplex.nym-exchange-key-request.v1` + NUL + JCS minus `signature`.

A uses an independently adopted `nym-bootstrap-recipient.v1`, signed by the
profile's council, binding its separate X25519 bootstrap key/ref, exact profile,
peer node, purpose and validity (at most 24 hours). Its signature preimage is
`orbiplex.nym-bootstrap-recipient.v1` + NUL + JCS minus `signature`. Council
signature verifies the descriptor, but grants no AD/INAC authority. Root-admitted,
exact peer/family/artifact request and reply invitations remain mandatory.

D opens only the key-request metadata with that bootstrap-purpose key. It
verifies the applicant signature and deadline before preparing one per-exchange
recipient key. D durably reserves the exact signed applicant/reply/deadline tuple before
creating any recipient key. Its keystore pins that input identity and immutable
deadline independently of application DB restore. Saved bootstrap metadata binds
the exact recipient handle and role through AEAD AAD. D stores the exact sealed
offer with its companion references in one SQL transaction, then fences its
output digest in the keystore before returning bytes for AD. Startup/retry can
finish the same committed result; an old DB missing a committed result refuses
new encryption. Domain clock observations use the provider's durable high-water,
not an application-DB-restorable clock floor. Same digest with changed tuple is a conflict;
duplicates recover the original offer/key. The offer itself is encrypted to the
signed applicant reply key. The eventual full issuance request must match that
frozen tuple. Bootstrap metadata may expose private peer activity to D, but never
carries the participant-to-context/nym mapping. A bootstrap-purpose key cannot
open issuance requests, offers or decisions, even with otherwise valid ciphertext.

Each encrypted payload has its own outer AD family: `nym-key-request-sealed.v1`,
`nym-key-offer-sealed.v1`, `nym-issuance-request-sealed.v1`, and
`nym-issuance-decision-sealed.v1`. The common `nym-exchange-sealed.v1` schema
checks their closed outer/inner pairing; it is not a grant for every direction.
Before AD submission, each phase durably freezes its exact canonical sealed
envelope, including ephemeral public key, nonce and ciphertext. Retransmission
reuses those bytes; it never re-encrypts even identical plaintext under the same
artifact/idempotency id. AD alone owns transport retries.

An invitation names one exact family and deterministic artifact id derived from
request digest and the exact phase/family (direction alone collides between
bootstrap and issuance). Both artifact id and AD idempotency key are exactly
`urn:orbiplex:nym-exchange:<outer-family>:<unprefixed-request-digest>`.
Malformed family pairing never tries another key
purpose, decryptor or admission policy. This refines an unqualified, prerelease
codec; it makes no claim about deployed-state compatibility.

For `nym-exchange-sealed.v1`, the header is the complete envelope minus
`ciphertext`. All base64url strings are canonical, unpadded. The ephemeral sender
key and 24-byte nonce are random and never reused. HKDF-SHA256 uses the existing
X25519 primitive, UTF-8 `exchange/digest` as salt, and the bytes
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
