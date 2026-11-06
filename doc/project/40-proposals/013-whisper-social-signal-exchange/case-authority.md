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
authority and authenticated return ingress are explicit fixtures. Registration and
succession still accept already signed controls. Native status-read and audience
adoption are described below; complete host signing, active control adapters and
the full retained gates remain pending. No tracker closure follows from these probes.

The native `prepare-status-read` adapter now composes the existing S026 owned-nym
port. It freezes the reader, sorted audience hint and unsigned preimage before
key use; Vault owns key possession and observed-time fencing. Membership remains
an independent authority decision, not a consequence of the supplied hint or a
publication certificate. Saved preparation replays without another nym lease,
signature or seal. The actual Vault-mint/native-sign/AD-enqueue component vector
uses explicit synthetic council discovery and makes no private status-response
transport claim. Registration and succession signing composition remain open.

Prepared request handoff also rechecks the current named circuit against the
owner's frozen domain recipient and forward family/direction. Another currently
allowed route to the original authority cannot authorize a saved circuit that
has been remapped elsewhere. This is an in-memory dispatch binding over existing
saved metadata, without a wire change, new sealing operation or retry owner.
AD independently retains current transport-policy enforcement.

The source workflow now persists an encrypted per-case head/negative view in the
same transaction as the authenticated result and requester-key retirement. It
shares the pure status fold and head comparator, not authority or recipient
lifecycle. A bounded per-revision index retains signed acceptance contradictions
after head advance. A later request cannot extend the original horizon or weaken
the fixed skew basis. Old active results cannot override known closure/conflict;
future signed knowledge is retained without earlier permission. Late terminal
proofs independently block source effects without classifying ordinary old
status replay as equivocation. Historical exact
result reads remain available. Existing rows without this new projection do not
synthesize current permission. This is source-owner component coverage, including
restart and an injected failed commit, not private audience handoff or cold Gate C.
Disclosure, audience membership and final effect authorization remain separate.
Convergence review also found and fixed the recipient counterpart: a late signed
terminal proof is held independently of its high-water head and blocks later
positive decisions across restart. The first negative hold uses reserved capacity;
a status beyond admitted future skew cannot create it. The original stale refusal
and conflict taxonomy stay unchanged. No older head replaces the newer one.
The convergence disposition retains the distinct source view within the existing
S026 owner/store; no new persistence engine, PEX retry or case-history authority
is introduced. Full provider/composition work accounting remains Gate E.

The S026 source now also owns a separate one-way audience lifecycle in its
existing bounded SQLite/fence store. An exact opaque presentation token binds
canonical bytes, reader, admitted policy and evaluation time before sealing.
Its signed acceptance/status facts and source head commit together; preparation
failure resumes the frozen basis, and exact committed packet replay never
reseals. Current policy and a finite lease from the material-disclosure owner
bound each handoff. A shortened lease or advanced source head refuses older
prepared output. Closed evidence remains deliverable without granting a current
effect. No reply key, return grant, PEX store or transport retry is introduced.

Component composition uses actual P035/P037/PEX and the recipient owner for
full/detached × carried/referenced × node/nym audience. It covers restart, lost
preparation/final commit, current policy/lease changes, a later head, terminal
history and expired current successor permission. Authority/transport ingress
remain explicit fixtures. Native source-audience API and the real material-owner
egress lease are not yet adopted; private AD delivery and cold Gate C/D remain
pending. Indexed source controls reuse this owner's prior authenticated/fenced
fact without repeating signature work or exposing a deserialized verified-token
constructor. This does not close any tracker or qualify the full work budget.

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
a still-decryptable carrier cannot replay an expired permission. Source audience workflow, actual AD audience handoff and cold isolated
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
fixtures. Source/audience workflows and actual host
signing, cold isolation and retained A–F qualification remain open. The current
one-role incarnation configuration is an implementation limit, not a prohibition
on participants acting in several roles. No tracker closes from this checkpoint.

The native recipient can now explicitly select protected S026 nym custody.
Omission preserves the owned-node configuration/paths. A named custody profile,
certification id and nym principal only locate a key: the current active local
Vault must independently prove possession. Framing precedes provider access;
AEAD/structure is followed by another custody check and a final owned-time check
using the existing fenced watermark. Missing/retired keys do not remint or fall
back to node identity. Read membership remains independent of publication rights.
The temporary agreement uses the nym principal's Ed25519 public conversion, not
P015's separate exchange-reply key. No raw DH/signing/export operation or root
recovery slot is introduced. The custody profile neither admits a source
certificate nor relaxes the strict case-context law.

Each nym scopes its own CaseKnowledge store and fence. Selecting another audience
does not erase old state or reset its horizon; inactive-scope retention still
requires qualification. Actual Vault framing/clock vectors and a native nym-domain
composition reach real P035/authority/CaseKnowledge with controlled time and an
explicit delivered-frame fixture. Full source audience/control composition,
private transport, cold isolation and retained A–F remain open. This checkpoint
closes no tracker and does not broaden hard-MVP or P015-005 claims.

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


Memarium now exposes a separate host-local finite disclosure lease for a concrete
node/nym audience. It checks current private classification and the original
material/profile horizons around provider work. Full-record requires the retained
payload; detached leases only public proof material, never its private author
bytes. Local case-knowledge inspection is not an egress decision. Real custody
component vectors cover erasure, distinct horizons, exact expiry and a policy
change during owner work. Native source-gate/API adoption now consumes this real
port as described below; cold/transport gates and all tracker closures remain open.


Native source configuration now separately admits a closed optional audience
policy: independently selected receipt trust, authority/profile sets and explicit
end-recipient-to-one-way-circuit mappings. A nym principal is not its transport
node. The declaration has finite cardinalities; duplicate recipient/family
choices, missing mappings, return budgets and unsupported kinds refuse. Legacy
source serialization is unchanged when omitted. This is an unreleased local
configuration extension, without changing signed artifacts. It does not itself
grant disclosure or outbound authority. The native audience API now separately
adopts the real S026 one-way owner and current Memarium disclosure lease.

The authenticated operator workflow offers audience-begin/prepare/handoff/read.
Preparation accepts direct nested presentation JSON, rejects duplicate fields and
excess depth before Vault access, and binds exact bytes to independently admitted
reader policy. Saved preparation resumes its committed evidence basis without
new resolution, signature work or resealing. Each handoff checks current retained
material/profile horizons, classification, source head and concrete recipient/
family/circuit mapping. Historical custody metadata is not a disclosure lease.
Full payload erasure stops new full-record handoff; retained detached public proof
has a separate horizon and never discloses private author bytes.

These additive unreleased local-workflow v1 extensions preserve legacy branches,
signed artifacts and historical schema pins. Native component composition covers
full/detached, carried/referenced and node/nym recipients using actual Vault,
Memarium, P035/P037, AD enqueue and a durable receiver decision. Authority and
relay ingress plus recipient key agreement remain explicit fixtures. Native host
signing, private transport, cold-process A-F and independent tracker closure
remain pending; transport custody alone proves no domain delivery.

A presentation's current successor assessment now folds all signature-checked
anchor statuses from the exact same cumulative P015 scope, including holder-local
custody observations. Different epochs remain separate. Weaker current-role
attachments cannot hide that high-water or a later revocation. The recipient
commits the effective source proof with its refusal and preserves it across
restart, while historical succession authenticity and the shared signature budget
remain unchanged. A refused cursor advance preserves the prior revocation proof,
including when a larger revision omits cumulative revocations. This has
full/detached and carried/referenced component coverage; independent native
transport/cold gates remain open.

Native authority adoption now permits an explicit owned-node recipient attachment
with independently admitted knowledge policy, witness trust and material source.
The roles share one transport incarnation under its original finite combined
route/config/AD budget, while retaining separate SQLite/FULL stores, fences and
zero-queue workers. Closed PEX end-family selection dispatches to exactly one
owner; refusal does not fall through. The existing strict presence parser keeps
omission distinct from invalid null, and legacy declarations serialize unchanged.
Standalone nym recipients remain supported. Source/recipient co-adoption is
independently described below; authority/source co-adoption is not enabled. Component vectors cover admission, both real owner lifecycles and
real authority registration while both are active. Actual private delivery to
the authority audience, inactive-role retention and independent A-F remain open.


A source can now explicitly adopt an independent recipient through the same
closed paired-role mechanism used by an authority. Its recipient declaration
chooses owned-node or owned-nym custody, independent receipt trust, knowledge
policy and local material source. Source responses and audience presentations
route by the existing PEX end-family role, with no fallback, new queue or shared
domain fold. Source and CaseKnowledge keep separate stores, fences and workers;
combined transport routes and custody retain the existing finite budget. Missing
adoption preserves the legacy profile; explicit null refuses. The actual-daemon
dual-store vector and real protected nym recipient through the paired sink are
component evidence with explicit authority/relay-ingress fixtures. They do not
qualify private audience delivery, cold Gate C or PEX/LLR closure. Authority/source
co-adoption remains unsupported.


The source owner now also stages unsigned registration before its dedicated
continuity-key signer port. Exact carried roles, audience, original observed time,
continuity commitment and independently admitted receipt-policy digest are frozen
in that owner's encrypted metadata. The P035 token carries the actual policy
identity; full author bytes or detached manifest and all non-payload roles must
match that verified evidence. The shared signature budget includes finish's
returned-signature check. Failure at custody or packet preparation resumes the
same unsigned bytes; prepared replay performs neither anchor verification nor
signing use. A policy change refuses replay rather than silently adopting new
trust. Current disclosure and time remain separate gates.

Source and authority adapters share the historical registration projection, with
independent adopted trust and local observations. Carried registration roles can
be checked before the signed control exists, reserving its maximum size without
a placeholder signature. This projection performs no I/O or trust admission;
current key custody, disclosure and private transport remain separate host gates.

Public raw-control preparation cannot replace a frozen native registration or
status-read attempt, including with a valid external control. Only the native
owner operation enters the shared private commit boundary after its core finish
verified the signature; binding checks there do not repeat cryptography. Full
and detached component vectors compose actual P035, SQLite, PEX preparation and
independent authority admission, with explicit policy/continuity-signer fixture
ports. The native operator adapter now also composes actual S026 continuity
custody, the shared P035 projection and current finite Memarium disclosure.
It requires independent optional `registration/trust`; it accepts only public
commitment, sorted audience and carried roles, without secrets, caller times,
trust or signed controls. The provider owner remains held through preparation
and AD enqueue. Saved native handoff checks key erasure/provider availability,
original anchor/authority/horizon, policy identity and current disclosure; replay
signs and seals nothing again. Contention remains retryable. Missing full/detached
profile in an older encrypted native row is unknown and refuses this adapter.
The unreleased local request schema is extended in place with exact mirrors;
there is no signed-carrier change. Full/detached native vectors use actual random
case keys, P035, Vault, Memarium and AD enqueue with synthetic v2 credentials and
fixture authority opening. Successor signing, complete later source-local negative
basis handling, private transport and cold gates remain open. No tracker closes.

The owned successor PoP port now checks compact bindings from the opaque prepared
intent against the actual Vault nym's profile, context, epoch and known private
status floor. It samples its own observed clock and retains the current managed
recovery requirement. It does not require a decision-v1 publication grant for an
independently admitted certificate, and publication keeps its strict separate
issuer-decision guard. The real two-owner/P035 component vector uses a synthetic
v2 certificate/discovery, checks both signatures, and refuses clock rollback or
stale recovery. No wire/preimage changes, v2 issuer completion or native source
succession-workflow/private/cold qualification follows from this internal port.

The source-owner succession preparation now persists only unsigned candidate bytes
before its two narrow signing roles. Original owner time, predecessor, audience,
anchor-policy identity and exact successor roles survive failures and restart.
The checked certificate/status deadline also bounds prepared output and handoff;
replay neither resigns nor reseals. Full/detached component vectors use the actual
P035 producer, source SQLite and L2 PEX against the authority's A→B→C CAS, with
explicit custody/policy fixtures and synthetic v2 certificates/statuses. Native
source command adoption and the independent cold/private gates remain open; this
foundation changes no signed wire artifact, case-authority claim or MVP status.


The native source now adopts two-owner succession preparation. It uses independent
source `CaseAnchor` trust, current finite Memarium disclosure, actual S026 continuity
custody and an owned successor nym with current managed recovery. The source freezes
the exact anchor-input and custody-selector bindings before signatures; the key
provider independently enforces its original profile/context/authority/horizon.
Full/detached native component vectors produce exact prepared PEX bytes and cover
replay, altered inputs, key erasure and raw-control refusal. The successor certificate
and council discovery remain explicitly synthetic; P015-005 is not implemented by
these vectors. Succession transport/authority roundtrip, source-local later negative
basis, retained signed material for audience assembly, inactive-scope maintenance
and the independent cold/private A-F gates remain open. No tracker closes.


The source now retains native signed controls in a bounded scoped encrypted blob,
committed atomically with its exact packet. Registration retains no anchor roles;
succession retains only the three non-payload successor roles. Original case/replay
holds outlive packet and reply-key expiry, and current-classification local result
read exposes the optional assembly inputs without resigning, resealing or fetching.
Protected record/manifest bytes remain solely in Memarium. Prototype/raw rows without
this material remain explicitly incomplete. This is source workflow composition,
not an independent presentation/private/cold qualification or a new permission.


The source's explicit later-anchor observation now has a separate local refutation
fact, without inventing authority revision/closure. It retains encrypted exact
non-payload proof dependencies under the original case/replay horizon. The evidence
must match the source's frozen native receipt/time identity and adopted policy;
another or unknown basis is unproven. New control effects and active audience
presentation consult the local refusal; historical result reads and status reads
remain separate. Finite source reservations include the full negative-token bound,
so insufficient explicit prototype policies refuse rather than auto-expanding.
Inactive-scope maintenance, ordinary-process cold/private acceptance and independent
closure remain open. This source-owner mechanism changes no historical LLR-002 verdict and issues
no signed authority statement.


Cached native source controls and audience effects now freeze a scoped Memarium
exact-evidence witness with their original inputs. The witness covers this entry's
proof sets per role, local first-seen facts and accepted cursor identity, without
reading blobs/private text or verifying signatures. Duplicate/reordered references
and unrelated journal, payload-read or time-fence activity do not invalidate it.
A newly admitted proof or cursor identity makes cached prepare/handoff refuse
`anchor-unproven` and requires a new bounded request ID. Missing prototype witnesses
also refuse effects. Explicit later-anchor observation never renews an existing
packet, witness or deadline. Historical local reads do not demand a disclosure
witness; current custody, classification, trust, independent successor floors and
original finite horizons remain separate. Public P035 detached material is unchanged.
This is a local input-change guard, not a global knowledge epoch or current permission.


### Co-held audience delivery decision, 2026-11-06

Adopted contract; runtime qualification remains pending. An audience nym held by
this exact S026 participant owner receives the exact presentation through a verified
local delivery. An external recipient uses the declared PEX relayed posture. The
route follows actual private-key possession and the derived nym principal, never a
configured label. A different local participant is a distinct owner and receives
`cross-owner-local-delivery-not-supported`, without network traffic or a shortcut
across participant boundaries. A locked or unavailable possession provider is not
evidence that a recipient is external.

Both paths use the same closed presentation-family admission, limits, verifier,
independently adopted recipient policy and CaseKnowledge mechanism. Local delivery
has no synthetic AD header or peer identity. The local ownership proof is an opaque
host value, not a caller-supplied flag. Route selection is a pure function of the
verified ownership classification. A frozen local route never retries over PEX;
a refused external relay never falls back to direct or local delivery.

The recipient commits a `local-coheld` receipt with the exact presentation digest,
recipient nym, participant-owner scope and observed decision time in the transaction
that records the verified recipient decision. Receipt replay is idempotent after
restart and does not roll back newer knowledge. A refused continuation can still
have a verified receipt: delivery is not current permission. Invalid presentation
bytes produce the same refusal on local and remote paths and no receipt. The
sender records `delivered-local` separately from `delivered-ad`. Existing AD queue
or first-hop custody remains `transport-custody`; it is not end-recipient delivery.
Local reception is a transactional-withheld effect; AD handoff remains an
irreversible-external effect. Temporary source bytes retain their original handoff
horizon; no new PEX store, retry owner or payload archive is introduced.

LLR-007 private audience delivery includes this verified local case. PEX-001's
external delivery and privacy gate is unchanged. Acceptance must prove actual key
possession, zero AD/network activity for local delivery, local/remote verifier and
knowledge parity, other-owner refusal, exact-byte replay after restart, and no
fallback. It must separately observe domain reception for an external recipient.

Whether the author's own node may be the case authority is a separate policy
question. This decision creates no local authority fallback and no independent
ordering claim for an authority controlled by that author. The suggested editor
default requiring explicit consent for a self-owned authority remains unimplemented.

The recipient may already hold the exact presentation from an earlier admitted
operation. Its immutable local receipt retains that earlier time; a later source
operation can account for that fact without making it a new receipt. Sender route
freezing applies per operation. A recipient may separately retain local and AD
reception facts for identical bytes and reader, sharing one knowledge head.

Source local preparation encrypts exact presentation bytes under a separate
workflow purpose, with its original handoff horizon. It does not call a PEX
preparer. After a recipient commit and source-side crash, reconciliation can read
the original opaque recipient fact within the case/replay horizon; it cannot
redisclose an expired packet or restore permission. `delivered-local` requires
bound evidence and has no AD delivery id. This is an explicit additive unreleased
local-result contract change; historical schema pins remain unchanged.

Native recipient adoption may group a bounded set of owned nyms under one
participant's knowledge owner. Configuration supplies only key locators and a
negative owner boundary. Private-key derivation establishes possession. Duplicate
selectors or Ed25519 identities mapping to the same X25519 key refuse adoption.
The local and AD adapters share the same nonqueued owner, exact-byte verifier and
negative knowledge; transport custody remains solely with AD. Earlier per-nym
prototype stores cannot be silently abandoned when adopting a group. Their
presence requires explicit reconciliation. This does not qualify inactive-scope
retention or the clean-source private-delivery gate.


### Explicit external domain reception (2026-11-06)

Legacy `case-presentation-carried` and `case-presentation-referenced` remain
one-way. Their relay ACK establishes onward custody, never `delivered-ad`.
Confirmed delivery uses separate `*-confirmed` families and
`whisper-private-exchange-header.v2`. The presentation itself and its 4 MiB /
64 KiB bounds do not change. A random exchange-scoped response public key is
part of the authenticated header; it is not a source-node route or identity.
Legacy v1 header bytes and schema stay unchanged. The v2 header maximum is
542 canonical bytes; the complete PEX and AD frame remain under the existing
5 MiB ceiling without another payload wrapper or base64 layer.

`whisper-case-reception.v1` is a separate recipient-signed reception fact. It
binds the original exchange, confirmed request family, exact presentation digest,
recipient, response-key digest, received-time observation and original handoff
horizon. Its maximum is 663 canonical bytes, derived from the closed fields.
It carries no participant/owner scope, source node, private record id or permission.
The receiver's node/nym key signs the dedicated reserved reception domain; the
transport peer cannot establish that key. Source verification uses its retained
exact context and expected recipient, never a key selected by the receipt.
`received/at` is sampled by the receiver before its decision commit; it is not a
claim of physical durability by that instant. The fact grants no `continue-case`.

The recipient CaseKnowledge owner must commit its reception/decision and exact
prepared response before revealing the response. It owns that bounded response,
not PEX. Replay returns the retained ciphertext without another sign or seal;
AD alone retries delivery. The response ciphertext expires at the original
handoff horizon without extending the retained knowledge. The source accounts
`delivered-ad` only after verifying this end-recipient receipt. Missing return
routing or a failed domain verification never falls back to one-way success,
direct delivery or local co-held delivery.

Implementation status: schemas, closed family profiles, stateless codec, pure
receipt verifier and restricted protected node/nym signing ports have component
coverage. The node operation fixes its key, closed schema, internal caller and
clock; the S026 operation requires actual nym possession and its key-use fence.
Neither signature grants publication or current case permission. Recipient-owned
atomic prepared-response persistence, original-deadline expiry and exact restart
replay now have real SQLite/PEX component coverage. Failure to prepare/store an
acknowledgement cannot suppress newer negative knowledge; optional output cannot
consume terminal capacity. Native recipient return routing is connected through
opaque committed output, with one-way/confirmed mode admission before key access
and post-commit access, possession, time and stop checks. Source end accounting
and ordinary external-reception qualification remain to be connected.
This protocol foundation closes no PEX/LLR tracker or ordinary transport gate.


The source's optional local intent `delivery/mode` is explicit: `one-way` is the
legacy default and is omitted from its normalized private metadata; `confirmed`
selects the separate confirmed family. Existing operations cannot silently
upgrade. On a frozen external route, confirmed mode requires the matching AD
request/response circuit and one random exchange-scoped response key. The source
retains that key only in a purpose-separated protected row until the original
handoff deadline. A receipt must match the retained packet context and expected
reader before `delivered-ad`; transport custody alone remains insufficient.

Actual custody classification still selects the route before effects. A frozen
co-held route uses the verified local receipt, without a response key or AD
return capability; the external confirmation preference does not force a trip
through a relay or create an AD claim. Neither route falls back to the other.
The additive unreleased local intent/result changes leave historical pins and
legacy one-way wire bytes unchanged. Source mode/key/accounting implementation
and qualification are pending.
