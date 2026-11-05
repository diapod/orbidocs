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

### Recipient continuation decision

The recipient supplies its own saved exact source-status proof to presentation
verification. It commits high-water knowledge, scoped source conflicts, proof holds
and the final continue-case decision together. The local closed projection
`whisper-case-continuation-decision.local.v1` keeps case and source currency as
separate axes; an allowed result requires both. This point-in-time decision grants
no publication right and never merges source identities or counting units.

Original independently admitted registration completeness is not renewed on each
use. Current policy still applies; later Before evidence remains terminal. A pair
of incompatible signed revision-zero events is durable authority conflict. P015
source equivocation instead stays scoped to that status stream and retains its
exact proof pair; it does not manufacture a conflict of the case authority.

A future signed source status can establish high-water knowledge, but no positive
source result exists before its issued/at. The recipient checks its owned time and
fence after persistence and withholds an expired positive decision. The effective
case deadline includes any already known shorter same-issue lease. An effect owner
rechecks time/fencing at execution; stored positive decisions are not permission
caches. First source revocation/conflict has reserved negative-write capacity. A later
negative-proof capacity failure records a bounded local suspension; subsequent use
requires retaining the exact pending evidence. This is a dependency failure, not
an authority or issuer assertion, and older input cannot clear it.

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

### Accepted material identity

Succession acceptance binds the exact historical successor certificate, profile
and status used for its decision. Let `H` be SHA-256 encoded as `sha256:` plus
unpadded base64url and let every array below use JCS v1. Their order is fixed:

- `anchor-identity = H(JCS([author-nym, author/bytes-digest,
  continuity-key-digest, status-authority, canonical-case-not-after, federation,
  context-digest, profile-digest, receipt-digest, detached-witness-or-null]))`;
- `certificate-evidence = H(JCS([certificate-digest, profile-digest,
  status-at-acceptance-digest]))`;
- succession acceptance `inputs/digest = H(JCS([anchor-identity,
  succession-digest, certificate-evidence]))`.

All element digests address exact signed bytes. The registration acceptance's
`inputs/digest` equals the original signed registration request's `inputs/digest`;
its request digest addresses those exact request bytes. Another valid receipt
cannot silently replace the receipt or witness admitted at registration.

The receiver verifies the original control at the signed registration acceptance
time and the succession at its own exactly bound acceptance time, never at the
artifact's self-declared issue time. Succession acceptance cannot predate
registration, and a case status cannot predate the succession it names. These
three timestamps share one authority's clock. Across the P035 witness/authority
boundary, registration cannot precede the receipt's commit time by more than the
profile's admitted clock skew; no new constant or lease extension is introduced.
Current successor status remains a separate role and cannot replace the bound
historical snapshot. Conversely, the authenticated historical snapshot is already
known evidence: an explicitly older current role cannot roll it back. Historical
and local observations are folded by the existing P015 scope/revision/negative
knowledge laws before current source use. Exact status/certificate signatures
are reused across roles, without caching a positive time-dependent permission.
An expired current certificate or later revocation does not rewrite successful
historical succession authentication.

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


#### Portable registration input binding

Registration request and revision-zero acceptance `inputs/digest` equal the
immutable anchor-identity defined above. The exact P035 receipt commits author,
certificate, profile and admission-snapshot bindings. This input identity excludes
evaluator trust, first-seen/provenance and later completeness observations; source,
authority and recipient may independently admit different trust inventories.

The authority separately retains its basis-evaluation digest and exact proof
references, which include the actual local completeness, trust and observations
used for its decision. Signed AnchorBasis remains the admitted authority's claim;
a consumer choosing independent evaluation applies its own evidence and trust.
Later valid Before evidence remains terminal regardless of unchanged portable
anchor identity. This correction affects the unreleased LLR foundation only;
frozen P035/P015 evidence and earlier source pins are not rewritten.

#### Authority command carrier

`whisper-case-command.v1` is the closed authority-input carrier for
case-registration, case-request (succession), and case-status-request. It binds
the family, signed-byte case anchor, random exchange handle, raw canonical
base64url X25519 response public key, one exact base64url native control and
carried digest-addressed evidence roles. It contains no route, peer, sender-node
identity, URL or acquisition reference. The destination independently admits its
own authority/trust policy; neither encryption nor a carried key grants authority.
The native status-read signature also binds the exact raw response-key digest.

The evidence roles reuse the presentation's exact-byte role limits and resolution
mechanics, with separate command completeness: registration needs full record or
manifest, receipt, anchor certificate, profile and status. Succession carries only
the profile, successor certificate and acceptance-time status; the authority uses
its originally admitted fenced anchor claims, without reevaluating registration.
Closures are optional registration conflict/completeness evidence. A status read carries no evidence. All supplied
items are checked; a bad attachment is never hidden by another copy. Command
resolution has no local-store or network fallback. Detached supplements remain
separate LLR roles, without widening frozen P035 detached material.

The maximum decoded command is 1684 KiB, derived from shared role maxima plus
8 KiB control and 32 KiB metadata. The carrier ceiling remains 4 MiB (status reads
retain their 4 KiB family ceiling); the shared complete-evaluation limit remains
2740 KiB/32 signatures, including independent local observations. Base64 and
packet/seal framing retain their own bounds. These are structural ceilings, not a
claim that contradictory closures or incomplete evidence are admissible.

A previously committed result may replay from possession of the exact native
request control before expired proofs are resolved. A new command without complete
material refuses without reserving an id. Saved replay never repeats historical
verification, signing or sealing. Initial admission and current local negative
knowledge remain separate owner decisions.

The destination adapter binds the admitted delivered AD header to the PEX family,
random handle, exact interval and recipient before dispatching native command
bytes. It receives no origin peer identity. Request/response associations are one
closed profile table used by both source and destination. The deterministic return
packet is prepared only from the authority owner's committed token: result bodies
bind the exact native control digest; status bodies bind the case. Its lease is
bounded by the stored inner ciphertext and original request, without resealing or
extending either. AD treats the forward deadline as the return-capability
ceiling; the response packet may expire sooner. Packet expiry removes its transport
copy while the consumed-response identity remains until that original ceiling.
Cleanup cannot restore the right to choose another response. Header framing establishes no native authorization or current
AD policy by itself. Authenticated host installation and retained qualification
remain separate from this source component composition.

#### Source workflow and requester-key lifetime

The S026 workflow commits an exchange-scoped random requester key and independent
random handle before returning public preparation. Repeating the same immutable
intent returns those values, never a replacement key. The native signed control,
exact evidence and admitted response recipient are frozen before packet
preparation. Current disclosure/privacy and owned time are checked both before
commit and immediately before handoff; AD alone retries the exact saved packet.
Transport custody is an independent fact and cannot regress a received result.

Short request keys/packets and historical result metadata have separate original
horizons. Request expiry never extends the case horizon. A completed exact result
may be read during the case/replay window without the requester key; this is
historical information, not a cached current permission. The source verifies the
native authority signature, exact request/case/operation, accepted time and
registration-input binding after AEAD decryption. An unsigned refusal remains a
bounded diagnostic and cannot preempt a later signed acceptance or establish
negative case knowledge.

A private audience read uses the owned nym key, not the originating node key. Its
closed signing intent binds the case, committed authority, reader, short original
deadline and exchange-scoped response public key. The source first persists the
unsigned request and observed time in its encrypted workflow. Signer or packet
preparation failure resumes the same preimage; completed preparation replays the
exact packet without signing or sealing again. The authority rechecks current
audience membership even when its status cache hits. This separate read right
neither requires nor revives publication authority. The protected host nym lease
reuses the owned clock/fence and rejects rollback or expiry around signing.

A scoped operational-root lease may protect private source-workflow metadata and
short requester seeds. It must not derive or recover the independent case
continuity key. No private requester seed is serialized into domain JSON or
exported by a generic signing API. Expiry and reference collection prove local
application reachability only; they do not revoke filesystem copies or constitute
forensic erasure. Explicit source-role adoption now installs that root lease and finite owner in
the daemon. Its protected operator API accepts already signed controls. Complete
host signing composition, recipient/audience adoption and retained PEX/LLR
qualification remain separate work.

#### AD single-relay packet profile

The AD transport owner carries the end-sealed PEX artifact in a binary packet:
`"orbiplex.ad-relay.v1\0" || u32be(header-length) || JCS(header) || opaque-body`.
Local AD circuits and receive routes distinguish `exchange/mode`:
`request-response` (the omitted legacy default) and explicit `one-way`. The latter
requires an empty response family and zero response-byte budget, creates no return
capability and reserves only its forward packet. Its opaque handle is an
idempotency identity, not a response grant. The persisted mode/circuit digest
prevents later policy changes from upgrading an existing one-way binding. Unknown
or non-string mode values and contradictory fields refuse. This local policy
extension leaves packet/header bytes, PEX profiles and existing request/response
serialization unchanged. Audience presentations use the one-way profile; native
authority requests retain scoped request/response. Destination admission returns
no reply route for one-way, and source/relay/ledger checks refuse returns.

The closed `artifact-delivery-relay-header.v1` binds direction, random 32-byte
base64url return handle, family, issue/absolute expiry and body size. Only `forward`
may name a configured circuit; `return` and `delivered` forbid it. The canonical
header maximum is 443 bytes, within the 1024-byte framing allocation. The whole
packet ceiling is 5 MiB. No origin identity, endpoint, origin grant or causal trace
is copied into the delivered packet. Circuit/neighbor knowledge remains private
to the origin and relay; the destination config admits only a relay and families.

A configured circuit binds independently admitted hop targets and grants, separate
forward/response size limits and a finite TTL. The relay atomically commits the
exchange mode and exact onward custody in the existing AD ledger. For
request/response it also binds one response to the authenticated destination,
allowed family, original expiry and exact body; one-way has no such right.
Same-byte retry recovers that plan; changed bytes conflict. The domain
owner persists its exact prepared packet before enqueue, without regenerating its
header/ciphertext on retry. The AD owner is the only transport retry owner.

Capacity accounts for live transport bindings and reserved logical ciphertext
bytes, including one bounded response only for request/response. This is not physical database allocation. The
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
the real domain adapter and the remaining family, route policy, expiry and
negative vectors remain pending. An explicit restart-bound daemon courier profile
now binds every relay hop to the owned node, requires finite capacity, installs
the runtime before peer admission, and creates no outbound or domain permission.
Authenticated INAC source provenance cannot be supplied through HTTP, including
under an incorrectly configured source allowlist. This courier adoption is not a
claim of installed authority/source/recipient workflows or completed Gate D.
The L2 authority recipient now calls the existing protected P037 node DH port,
checking its pinned principal/key metadata before and after agreement and its
owned clock/deadline before exposing opened command bytes. The static key stays
with the existing provider; the common crypto transcript is unchanged. Component
coverage uses the real P037 engine with structural command fixtures, including
cached-key rotation, revocation and post-call clock/expiry refusal. This port is
now installed by an explicit restart-bound daemon authority role. Adoption supplies
finite receiving routes, independent CaseAnchor trust and owner policy; it creates
no outbound or implicit INAC permission. One lifecycle-owned native thread opens
commands through P037, executes the actual SQLite/fenced dispatcher and enqueues
the committed exact response into AD. Its rendezvous has no pending queue; a busy
authority returns retryable and AD alone retries. Effect and reply ceilings cannot
exceed the received PEX lease. Signed candidates and ciphertext stay withheld
until the owner commit.

The authority now owns P015 source floors alongside its decisions, instead of
relying on a caller to remember them. Positive knowledge is atomic with the
acceptance using it; a verified issuer contradiction persists independently and
cannot silently be healed by a higher revision. This source-axis refusal is not
case-authority equivocation. Pending unsigned registrations consume case capacity.
Host-triggered, one-case maintenance resumes pending negative closures when the
signer recovers, independently from read traffic. Historical basis and saved exact
replay keep their distinct semantics.

A source component probe uses the actual daemon, P035 producer, P037 and native
owner for full/detached registration and prepared AD return. Its relay provenance
is an explicit in-process ingress fixture and its v2 nym credentials/statuses are
synthetic. It does not qualify real WSS audience delivery or an OS-denied cold
consumer. The source is now independently adopted through a finite restart-bound
profile, current disclosure/private-route policy and per-call unlocked S026 root
lease. Its closed host-owned operator API checks session and current operator
authority before Schema Gate, protected input or Vault; middleware cannot inspect
or rewrite its namespace. Actual source handoff and signed-result receipt share
the authority executor mechanism, with separate domain owners and AD-only retry.
Component tests compose real Vault/P035/P037 with full/detached anchors; native
authority and authenticated return ingress are explicit fixtures. The API accepts
already signed control documents. Host signing composition, recipient adoption,
private audience, active control adapters and the full retained gates remain
pending. No tracker closure follows from these probes.

The source-adoption convergence review shared the actual zero-queue executor and
closed delivered-frame preflight across authority/source adapters. Stores, trust,
root leases and domain admission remain with their distinct owners. Both consumers
are recorded in the Node re-use index. PEX sealing extraction remains deferred
until a second real ADC-005 adapter exists; this source installation is another
consumer of the existing case adapter, not that second semantic family.

The one-way AD regression covers memory/SQLite/reopen, response-reservation
absence, mode changes at retry and finite expiry. The shared three-process
WSS/3DH/AD/INAC probe separately observes an audience-family fixture at its
recipient, no return output, source restart/exact-byte replay, lost custody ack
and raw privacy scans. Destination control reuses the actual AD `ReceiveRoute`
without origin/circuit fields. This remains fixture-domain component transport,
not installed recipient/private-nym or full Gate D qualification.

The protected node-audience opener now binds the delivered AD family, role,
handle, exact interval and recipient before the P037 key call. After decryption
it checks canonical closed presentation structure and profile/family agreement.
It grants no membership or action. The installed command port and audience port
reuse one protected node-self agreement mechanism with separate principal rules;
local recipient rotation is dependency loss, not case-authority equivocation.
A real P035/P037 component composition reaches durable CaseKnowledge in all four
full/detached × carried/referenced variants. Restart re-evaluates current input;
a still-decryptable carrier cannot replay an expired permission. Protected nym
custody, source audience workflow, actual AD audience handoff and cold isolated
qualification remain pending; no gate closes from this adapter composition.
Native daemon `mode: recipient` now adopts the owned node's protected P037 key,
independent receipt/authority/profile policy and actual `CaseKnowledge`. Only the
two presentation families have admitted one-way routes; no response or outbound
permission follows. The lifecycle-owned zero-queue executor holds the sole writer
directly, with SQLite/FULL and a separate fence. Domain receipt records processing,
including a saved refusal, rather than a reusable permission. The PEX lease is
checked around decision work; no transport peer enters the case facts.

An explicit local source is either absent or existing Memarium custody. The
latter resolves current classification and exact anchor bytes together with the
holder's own first-seen observations. Missing proof remains unresolved; provider,
policy and integrity failure cannot become successful absence. Capture disablement
does not disable existing reads. Payload horizons/erasure and the omission of
private detached text remain Memarium's law; no new payload store, acquisition
operation or exported first-seen authority is introduced. Full/detached ×
carried/referenced native component probes use real daemon/P035/P037/Memarium and
recipient persistence/restart with explicit authenticated-relay and authority-reply
fixtures. Protected nym adoption, combined source/audience workflows, actual host
signing, cold isolation and retained A–F qualification remain open. The current
one-role incarnation configuration is an implementation limit, not a prohibition
on participants acting in several roles. No tracker closes from this checkpoint.

The re-use review retained separate domain owners and deferred sealing extraction
until the already declared second real ADC-005 adapter.

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
