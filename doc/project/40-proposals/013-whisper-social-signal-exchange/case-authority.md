# Ordered case authority and private exchange

Date: 2026-11-04. Status: owner-adopted implementation contract; runtime qualification pending.

## Executive summary

LLR-008 owns ordered acceptance; LLR-007 is its first consumer. PEX-001 and the
single-relay S010 profile have independent transport/privacy gates. Historical
anchor validity, AuthenticSuccession, authority acceptance and current permission
are separate results. None merges source identities or grants publication rights.

## Context and decision

The implementation has three layers: pure `whisper-core::case`, an autonomous
`whisper-case-service` SQLite owner, and stateless PEX family adapters in
`whisper-intake`. The consumer owns a separate CaseKnowledge store and uses the
same pure head-comparison/fold laws. Authority persistence uses temporal-event-log,
exclusive writer locking, synchronous=FULL and external custody-fence time/revision
heads; it does not use a second JSONL or checkpoint journal.

Only node:did:key authorities are enabled. Producer preparation refuses other
principal kinds before exposing a commitment. The committed authority and local
trust admit a key; a carried key never admits itself. Key rotation leaves old
acceptances verifiable but cannot sign new acceptances for the old principal.

### Registration and historical basis

Revision zero is an explicit continuity-key-signed registration and signed
acceptance. It binds exact anchor evidence, authority, audience, original horizon
and one basis: after, none-observed-closed, or none-observed-fresh. Reuse the pure
P041 completeness predicate with use-specific trust. Fresh means an open epoch,
a usable Collection status in the exact scope/minimum revision, and issued/at at
least committed/at plus profile skew. Before refuses permanently; incomplete
knowledge requires new evidence. Snapshot-relative LLR-002 history is unchanged.

A detached registration supplies the manifest certificate and status/closure roles
separately from P035's unchanged detached material. P035 already binds the author
and manifest certificate before and after commit. The verifier relies on the
admitted witness for invisible body checks and never fetches that body. Disclosure
of certificates and revocation lists needs current audience policy permission.

Registration is evaluated once. Later requests use its saved basis and head.
Later verified Before evidence suspends effects immediately and causes terminal
anchor-invalidated closure. Persist negative evidence even when the signer is
unavailable; never mint fresh active status during suspension. Replay preserves
old accepted facts. The consumer states whether it checked the basis independently
or relies on an admitted authority's signed registration.

### Order, replay and conflict

All operations have a table entry: register, succession, amendment, withdrawal,
confirmation, closure, release-commit, abandonment and anchor-invalidated. ADC
preconditions stay with their actual adapters; absent adapters refuse rather than
supply permissive stubs. First succession requires AnchorAuthor; later succession
CASes predecessor against the effective successor. Stale predecessor is retryable
only after evidence changes, with a new request id. Other operations do not change
the successor. Withdrawal after release does not undo an irreversible release.

Under the sole-writer lock: read head, evaluate, persist only unsigned preparation,
sign, prepare reply in memory, atomically commit event/head/result/sealed reply,
then expose. No signature-bearing candidate is persisted or logged before commit.
Recovery resigns identical unsigned bytes only with unchanged head and valid TTL;
a committed result is replayed byte-for-byte without signing or sealing again.
Unauthenticated traffic reserves no request id. The outcome key is
(case/anchor, request/id), bound to the exact request digest.

Conflicted requires signed contradictions: two events at one revision, two head
identities at one status revision, or a lower revision issued later than a known
higher revision by more than skew. An older/earlier presentation is stale-status,
not conflict. A refreshed timestamp at an unchanged head is not equivocation.
Local database rollback is a local integrity error. CaseKnowledge persists negative
knowledge with the consumer decision; restart cannot restore old permission.

The recipient records whether registration relies on the admitted authority's
basis or on an independently verified P035/completeness evaluation. If local policy
withdraws authority-only reliance, current use refuses until explicit independent
evidence strengthens that basis. This update preserves the existing head,
negative knowledge and original horizon. A locally verified later `Before` proof
commits its refusal and exact proof holds without an authority callback. It does
not forge an authority-signed closure or alter the observed authority head.
If verified `Before` evidence causes registration refusal, that refusal still
commits the negative observation and its proofs, including at first admission.
Later presentation of older positive material cannot undo this knowledge.

### Saved results and audience reads

The closed `whisper-case-result.v1` reports one accepted signed acceptance or a
stable typed refusal, its retry class, exact request id/digest and decision time.
A refusal is diagnostic, never portable negative evidence or authority. Positive
claims rely on the embedded signed acceptance. The exact sealed result is stored
with its outcome; replay neither reevaluates the request nor reseals the reply.
Expired request/certificate material does not revoke the retained exact-request
replay right. Delivery of its stored ciphertext remains limited by the separately
committed handoff deadline; expiry does not trigger resealing or reevaluation. A changed authenticated request under the same scoped id conflicts;
invalid traffic is rejected before it can reserve an id or reveal a saved result.

`whisper-case-status-request.v1` is an audience-member signature over the exact
case/authority, request id, short owner-checked interval and response-key digest.
It uses `orbiplex.whisper-case-status-request.v1\0` and canonical unsigned JCS.
The key digest is SHA-256 of the raw exchange-scoped X25519 response public key.
The current audience, independently committed authority and response recipient
are checked before a cache hit or new signature. All did:key principal kinds in
the admitted audience prove their own Ed25519 key; they are not authority signers.
No transport peer becomes a reader by implication. New status and response
preparation are budgeted; response encryption is preparation only, with no I/O.

Commands and audience reads share the scoped request-id namespace. Ordinary
status signature work has a finite window budget and cache per current head.
One signature and one prepared response for a terminal head may use reserved
capacity; additional fresh read ids cannot consume the terminal storage reserve.
Recovery of an unsigned command preserves signature-budget observations made by
intervening reads. Saved refusals remain refusals after a budget window changes;
a new authenticated request id is required for a new decision.

The authority's accepted-operation limit is derived from the finite case horizon,
operation-window length and permitted operations per window, plus registration.
Admission also reserves objects, events and bytes for negative knowledge for each
admitted case. The byte reserve covers the complete bounded resolved negative-evidence token,
including additional local status history, plus bounded snapshots/facts, control
documents and one prepared response. The recipient reserves that complete token
and its local refusal independently; carried role counts alone do not size it.
Global physical-storage failures remain dependency failures, not a persistence
guarantee from a logical reservation.

### Presentation profiles and budgets

LLR-007 freezes whisper-case-succession-presentation.v1; LLR-009 qualifies that
frozen schema later. Carried supplies required proof bytes. Referenced carries
succession, registration, both acceptances and case status and resolves other roles
only by exact digest in an explicitly supplied local store. Missing is unresolved;
bad carried evidence cannot be hidden by good cached evidence. No network resolver.

The role table in the presentation schema is normative. Anchor statuses have three
slots in one scope. Successor status at acceptance and current successor status
have separate slots/scopes, deduplicated if identical. One shared profile, two
certificates, one receipt (including delegation), at most two anchor closures,
one full anchor or manifest, one succession and four bounded control documents
have a decoded maximum of 2,805,760 bytes (2740 KiB), including 32 KiB metadata.
The second closure is conflict evidence, not a second successful closure.

Carried JSON is bounded by 4 MiB; referenced JSON by 64 KiB. The sealed PEX artifact
is independently bounded by 5 MiB and must pass an encoded-maximum test. Each
control document is at most 4096 canonical UTF-8 bytes. Total signature work is
at most 32, including local resolution. Role maxima and sums are compile-time
assertions. Oversize, foreign scope, cycles, substitutions and unknown uses refuse;
never trim a signed status. P035 retains its own 2/4 MiB bounds and P015's private
exchange codec remains unchanged. Large artifacts use AD streaming.

### Privacy and owners

Every new case family requires relayed delivery without downgrade. The bounded
S010 profile uses one relay with independently admitted per-hop INAC authority;
only the final recipient opens the end artifact. Neither origin metadata nor a
stable origin transport id reaches destination domain facts, logs, trace or metrics.
Return handles bind recipient, family, deadline and byte budget. Retry rechecks
privacy. Missing relay/onion provider refuses before transmission. The relay knows
its neighbors and timing; collusion/global observation/onion guarantees are outside
this profile. Gate D uses three loopback-only local processes.

#### PEX binary sealed profile

`whisper-private-exchange-header.v1` is the closed JCS header of a binary artifact:
`"orbiplex.pex.v1\0" || u32be(header-length) || header || ciphertext-with-tag`.
The NUL is one zero byte. Header length is at most 464 canonical UTF-8 bytes.
Ciphertext is binary, with one 16-byte XChaCha20-Poly1305 tag; it is not wrapped in
another whole-artifact base64 layer. The maximum is 4,194,803 bytes, below 5 MiB.
The structural header maximum does not imply that every combination satisfies the
stricter family/time laws. All owners retain their narrower domain deadlines.

| Family | Recipient role | Plaintext maximum | Transport TTL ceiling |
|---|---|---:|---:|
| case-registration | authority | 4 MiB | 900 s |
| case-request | authority | 4 MiB | 900 s |
| case-result | requester | 16 KiB | 900 s |
| case-status-request | authority | 4 KiB | 900 s |
| case-status-response | requester | 4 KiB | 300 s |
| case-presentation-carried | audience | 4 MiB | 900 s |
| case-presentation-referenced | audience | 64 KiB | 900 s |

Every family requires single-relay hard-fail privacy. These TTLs bound transport
custody, not domain authority or status leases. KDF info binds the codec domain,
family domain and exact header; HKDF salt is the bounded opaque exchange handle.
Use existing X25519/HKDF-SHA256 and XChaCha20-Poly1305 primitives. The header binds
recipient-key digest, fresh ephemeral key/nonce, family, handle, issue/expiry and
plaintext size. It contains no source node, peer identity, case/record id or public
plaintext digest. Low-order keys, noncanonical bytes and mismatched independently
expected family/handle/role/recipient refuse before plaintext release.

Requester reply keys must be scoped to an exchange and admitted from the protected
request/workflow; an origin node key is not a private reply route. AEAD encryption
authenticates bytes for a recipient, not sender authority. Domain owners still
verify signatures, access and payload schemas. The codec owns no durable state
and performs no handoff; an owner persists its exact prepared ciphertext before AD.
Its component tests do not qualify a concrete relay, host admission or Gate D.


#### AD single-relay packet profile

The AD transport owner carries the end-sealed PEX artifact in a binary packet:
`"orbiplex.ad-relay.v1\0" || u32be(header-length) || JCS(header) || opaque-body`.
The closed `artifact-delivery-relay-header.v1` binds direction, random 32-byte
base64url return handle, family, issue/absolute expiry and body size. Only `forward`
may name a configured circuit; `return` and `delivered` forbid it. The canonical
header maximum is 443 bytes, within the 1024-byte framing allocation. The whole
packet ceiling is 5 MiB. No origin identity, endpoint, origin grant or causal trace
is copied into the delivered packet. Circuit/neighbor knowledge remains private
to the origin and relay; the destination config admits only a relay and families.

A configured circuit binds independently admitted hop targets and grants, separate
forward/response size limits and a finite TTL. The relay atomically commits the
capability with exact onward custody in the existing AD ledger. It binds the
response to the authenticated destination, allowed family, original expiry and one
exact body. Same-byte retry recovers that plan; changed bytes conflict. The domain
owner persists its exact prepared packet before enqueue, without regenerating its
header/ciphertext on retry. The AD owner is the only transport retry owner.

Capacity accounts for live capabilities and reserved logical ciphertext bytes,
including one bounded response. This is not physical database allocation. The
explicit local classification of opaque transport bytes passes existing INAC
egress policy at admission and retry; it never authorizes inner plaintext
release. Receiver domain authentication/disclosure remains separate.

Maintenance logically expires prepared transport copies and return capabilities
at the original deadline, without discarding domain history. Active transfers are
withheld from sweeping. HTTP clients may not impersonate the authenticated INAC
source adapter. First-hop acceptance is durable relay custody; success still
requires the final domain's receipt. The maximum-size component composition uses
an injected session boundary. A separate source probe (2026-11-05) uses production
WSS/TLS/3DH in three independent loopback processes with real AD/INAC and explicit
fixture-domain receipts. It covers source restart with exact prepared bytes,
a lost post-custody push acknowledgement and bounded raw-store/trace privacy
scans. These source probes do not close PEX-001/S010 or the full retained Gate D;
admitted daemon policy, the real domain adapter and the remaining family, route
policy, expiry and negative vectors remain pending.

Memarium is the sole protected-record store. S026 workflow owns exact prepared
requests; LLR-008 owns exact accepted results and sealed replies; CaseKnowledge owns
consumer decisions; AD owns transport custody and retry. PEX owns no durable state.

## Trade-offs and failure modes

A status lease is at most 300 seconds, shortened by policy, and never refreshed by
receipt time. Missing/current-future/stale material cannot authorize. Authority
acceptance implements the existing AcceptanceTimeVerifier for historical evaluation;
current certificates/status and fences are checked separately at use. Same-context
succession does not implement authority or context transition.

All dependencies are explicit: signer, store, AD/INAC and privacy provider. Missing
dependency refuses new effects; saved results remain readable under access checks.
Result reads require exact authenticated request bytes; status reads require signed
audience proof bound to the response recipient. Other callers cannot discover case
existence. Case authorization never depends on the transport peer identity.

## Retention and effects

Acceptance is transactional-withheld; replay is an idempotent read; status issuance
and AD handoff are irreversible-external. Exact output and audit precede handoff.
Original case/not-after bounds all operations. Import/replay does not renew it.
Finite policy budgets cover live cases, bytes, events, replies, work and replay.
Reserve closure/invalidation/conflict capacity before registration. Expired replay
returns expiry, not reevaluation. Ciphertext handoff retention and proof/history
retention have separate horizons. Proof holds never prolong private payload life.

## Open boundaries

P015-005, ADC runtime, LLR-009 full qualification, LLR-010 context/authority
transition, onion routing and global/physical privacy remain separate. Synthetic
v2 certificates in acceptance do not qualify production issuance. No power-loss,
whole-machine rollback or global copy-erasure claim follows.

## Next actions and gates

Implement contracts -> pure core and PEX/S010 -> durable owners -> LLR-007 ->
independent A-F acceptance. Review, fix and commit each stage on the feature branch;
no merge or push. Gate C requires cold OS-network-denied consumers plus counting
adapters. Gate D permits loopback only and proves actual admission rather than queue
success. Qualifiers test mutations and extracted evidence. Before retaining evidence,
apply current retention/retirement/external-retention policy and record owner,
classification, inventory/hashes, holds, retention, recovery/replicas; unknown remains
unknown. Source and evidence commits are separate. Done requires each owner's gate.
