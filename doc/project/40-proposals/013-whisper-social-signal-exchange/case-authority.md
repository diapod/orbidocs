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
