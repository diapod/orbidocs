# Messaging Middleware

`Messaging Middleware` is the node-attached application messaging component
that turns Proposal 060 into runtime responsibilities for personal message
admission, outbound contact permission, mailbox indexing, and recovery metadata.

Status: `hard-mvp-done`

Date: `2026-05-17`

Updated: `2026-10-16` — bounded fact recovery and scoped mailbox reconstruction.

Continuation registered: `2026-10-28` — [S027-009](#consent-loss-recovery)
is planned; the status above describes the qualified baseline, not this continuation.

## Executive Summary

> **Cross-reference to Solution 032 (Local Relationship Layer):** With
> Solution 032, the **canonical owner of the `contacts` concept**
> (relationship classes, membership facts, pairwise nym continuity)
> moves out of this solution. Messaging becomes a *consumer* of the
> Local Relationship Layer: it asks the host to evaluate the current authority
> of receive consent, including independent `contacts` decisions, and triggers
> passport-derived relationship projection through the local
> host capability `local-relationship.membership.append` on
> `contact-request.accept`. Explicit acceptance issues a scoped
> `messaging-receive@v1` profile under its current sovereign or delegated proof.
>
> Because the system is still before first release, the Solution 032
> compatibility bridge was removed instead of retained. Messaging no
> longer writes a `contacts_membership` cache and no longer emits
> `contacts.membership-changed.v1`; the canonical fact is
> `relationship-membership-fact.v1` (Solution 032).
>
> Messaging may declare relationship-derived `trust_requirements` in its
> package manifest for autonomous decisions outside the operator loop
> (e.g. accepting a contact-request from a peer whose operator is
> already in `friends` of the local operator, under bounded scope).
> Middleware never reads sealed relationship state; it receives
> `relationship-policy-decision.v1` shapes from the host policy
> evaluator.

The solution is deliberately stratified:

```text
message-envelope.v1 / contact-request.v1
  -> messaging-core domain invariants
  -> messaging-service Maildir + SQLite domain runtime
  -> daemon host capabilities and authority checks
  -> Node UI mailbox and compose surface
```

The daemon remains the host and authority layer. It owns signing, Capability
Binding, revocation freshness, local participant-handle evidence, notification
actions, Artifact Delivery, Memarium, Pseudonym Vault access, and (via
Solution 032) the canonical Local Relationship Layer. The `messaging-service`
owns messaging-domain state: Maildir bodies, the hot SQLite index, outbound
queue state, and the bounded Layer 3 messaging-fact stream. `contacts`
membership read/write goes through the Local Relationship host capability
layer; messaging no longer owns the relationship concept end-to-end.

## Scope

This solution implements the MVP+ personal messaging path:

- inbound `message-envelope.v1` admission through Artifact Delivery;
- outbound compose, route lookup, contact permission waiting, and private-direct
  delivery through host capabilities;
- the canonical `messaging-receive@v1` passport profile;
- the local contactability draft surface used by Story-010 before Contact
  Catalog publication is fully automated;
- user-mode readiness wiring: after participant identity and operator binding,
  the user wizard prepares messaging by enabling `messaging-service`, checking
  Local Relationship ownership/storage readiness, and saving either a
  pseudonymous-only contactability route or an optional public-handle draft;
- local participant mailbox resolution through a daemon-owned authority store;
- Layer 1 Maildir bodies, Layer 2 SQLite indexes, and Layer 3 Memarium facts;
- degraded operation when Memarium or host capabilities are temporarily
  unavailable;
- recovery mirroring for contact membership and receive-passport references;
- a thin Node UI for compose, inbox, outbox, status, and diagnostics.

Out of scope for this hard-MVP are body encryption, HTML rendering, group
messaging, CC/BCC, live multi-device mailbox-state push, and full
multi-device vault merge. Read/unread sync is in scope as replayable
`messaging.flag.v1` Layer 3 facts.

## Local preparation and onboarding

[P097](../../40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)
separates issuer authority, preparation and actual send execution. Stage B accepts
only `messaging-local-send@v1`; profile-less/legacy artifacts are unsupported.
INAC push consent and signer delegation remain distinct. A shared evaluator checks
current root, signature, revocation, participant/caller/bindings and owned route.
Host-owned local issuer revocation does not depend on directory freshness; remote
verified observations have a 300-second budget. The bounded 1024-entry proof cache
never skips current time/key/revision checks.

Compose admission belongs to the daemon, before EML/outbox/signing/contact effects.
It records immutable local sender provenance, referenced by Messaging, AD and peer
queues. AD statically protects message envelopes and outgoing contact requests and
fails closed without its host guard. Admission, retries, indirect adapters and each
protected peer frame recheck current authority. Refusal ends an AD attempt as
`OutboundDenied` and pauses the Messaging intent as `authority-blocked`; restart,
unlock and replay do not resume it. Generated INAC chunks retain artifact identity
and provenance, so even an already-started stream stops at the next protected emission
after refusal. Emitted bytes cannot be recalled. Fetching an already-shared object
pointer uses its own expiring, one-use fetch grant; send revocation does not revoke
that independent grant or reclaim bytes the recipient already holds.

Host-owned immutable artifact snapshots publish digests and revisions at writes;
execution reads snapshots and bounded provenance caches instead of rereading artifact
files for every frame. The actual authenticated request binding supplies the caller.
Recipient-push passports are excluded from local-send diagnostics; actual passport
issuer membership determines `issuer-not-admitted` under the unchanged issuer policy.

Single and participant bulk retry are explicit and generation/idempotency protected.
Retention bounds paused intents to 256 per participant, 1024 per node and 30 days,
terminating oldest entries as `expired-unsent` before transport-copy deletion.
One host provenance reference owns one outbox row, protected by a unique index
and replay receipts without EML rewrites. Module lifecycle reconciliation adopts
committed rows and reports terminal states. Unadopted operational proofs expire
in 60 minutes; terminal proofs and artifacts expire 30 days after delivered,
expired or discarded outcomes. Completed bulk retry receipts retain a 30-day
idempotency window, while incomplete operations remain recoverable.
Audit metadata and separate recordings survive. Unattributed entries can be
explicitly discarded or resent with new IDs, never attributed to today's operator.
Read-only authorization and a paginated operator audit expose the same reason and
evidence contract without granting authority.

The UI permits durable explicit deferral into `/app` with truthful status. Signed
admission requests remain non-authoritative. Root admission is an explicit P076
operator action; setup/auto-ready/retry grant no sovereign authority or withdrawn
binding consent. Explicit new setup keys can renew expired/unsupported preparation;
old keys remain tied to historical results. There is one always-enforced policy,
with no migration, observation or cutover mode. Lack of pre-release backward
compatibility is deliberate; post-release migration needs separate design.

The accepted P076 limited-grant decision separates root membership from bounded
issuance authority. Current V2 readiness reports `issuance_authority_status` and
`issuance_authority_kind`; receive readiness has distinct `receive/role-prepared`
and `receive/open-consent` facets on both paths. Setup needs the local role, not
open contact consent. A delegated setup never creates an any-sender passport.
Participant-issuer local send and scoped receive/INAC have separate clean-source
qualifications. The receive gate at Node `f54f884c` / Orbidocs `c6c3b0d2` retains
1285 tests, 34 strict sovereign phases, 24 HTML/API runtime cases and independently
rechecked signed public proofs at
`node:docs/evidence/limited-messaging/2026-10-17-receive-inac/README.md`.
MSG-ONB-007/008 are qualified by the subsequent P076-032 checkpoint below; org custody and the
final mixed candidate remain open. Completed MSG-ONB-005/006 evidence remains
sovereign-only.

The first P076-032 UI fragment offers explicit limited-grant request, import,
unlock and own-use withdrawal under the local participant session and CSRF guard.
Typed pending decisions link to delegate unlock, then require explicit retry.
The wizard's issuance-authority step does not claim sovereign membership; the
host keeps these facts separate. At this first UI-fragment checkpoint MSG-ONB-007/008 remained unqualified. User
contact-search addition explicitly records the local membership basis before it
reports success; this does not grant delegated receive authority. The
focused probe (`node:docs/evidence/limited-messaging/2026-10-18-grant-ui-probe/README.md`)
at Node `739c32c9` / Orbidocs `93b07a9` passes 27 browser cases and retains its
incomplete candidate qualification. It does not close MSG-ONB-007/008.

Canonical [readiness](../../../schemas/messaging-readiness.local.v2.schema.json),
[authorization request](../../../schemas/messaging-send-authorize.local.v1.schema.json),
[decision](../../../schemas/messaging-send-decision.local.v2.schema.json) and
[audit](../../../schemas/messaging-send-audit.local.v2.schema.json) schemas define
these local surfaces. Node retains the dated Stage A report separately from Stage B
conformance, fresh-identity runtime and strict Story-010 qualification at
`node:docs/evidence/messaging-onboarding/README.md`. Original Stage B local measurements
dated `2026-10-13` retain 804 conformance tests plus native gates, 24 fresh-UI
cases, seven narrow-profile cases and 31 strict Story-010 phases, pinned to
sources, profiles and unchanged executables. Neither this extension nor local
qualification establishes release
readiness or broader ordinary-participant authority policy.

The separate `2026-10-13` review closeout qualifies bounded provenance and completed
retry history, unique outbox adoption, immutable host observations, actual caller
and issuer checks, required content digests and the protected chunk/fetch boundary.
Its pinned candidate passes 810 conformance tests with additional native gates,
25 fresh-identity cases, seven narrow cases and 31 strict phases; delivery after
323 seconds of directory isolation still uses local issuer authority. See
`node:docs/evidence/messaging-onboarding/2026-10-13-review/README.md`.

A scoped browser follow-up on the same date fixes fresh-draft Messaging rendering
and measures actual guided-profile chat submission, explicit INAC/contact approvals
and one correlated delivered/read message. It reuses previously approved UI-created
identities with clean contact/transport histories; it is not a new fresh-creation
or strict Story-010 run. See
`node:docs/evidence/messaging-onboarding/2026-10-13-browser/README.md`.

## Portable Verification Material

Apply [P032's bounded inline-evidence guidance](../../40-proposals/032-key-delegation-passports.md#bounded-verification-material-across-artifact-families)
through the existing [P060 envelope binding](../../40-proposals/060-messaging-middleware.md#3-message-envelopev1-artifact).
Reuse `signature.key/public`, inline receive-consent passports and applicable
delegation proofs; reference-only envelopes require exact local evidence or an
explicit acquisition step. This is not a second credential format. Protect
contact-nym correlations, retain all receive-authority/freshness checks, and
distinguish offline signature inspection from authorization and delivery. Existing
runtime checkpoints do not qualify every offline variant; add bounded
network-disabled verifier/replay evidence when adopting a profile.

[P076-036](../../40-proposals/076-limited-messaging-grants-decision.md#p076-036-bounded-status-presentation-and-offline-acceptance)
owns the first planned slice: a bounded existing signed issuance status attached
to the V2 consent-passport handoff. Reuse the notification builder, peer-message
consumer, capability-binding verifier and durable issuance observation store.
Require a cold-cache host-path test with zero status fetches plus stale-proof,
rollback, withdrawal and restart refusals. Neither this attachment nor its
acceptance creates local issuance authority, admits roots, lengthens freshness
or qualifies offline message delivery. Disclosure and wire budgets govern
attachment; exact signed status is never trimmed. P060 and S007 reference the
same P076 tracker; existing runtime checkpoints retain their original scope.

## Passport Profile

`messaging-receive@v1` is the canonical receive-consent passport profile. The
solution does not introduce a second shape; it documents the
`MessagingReceiveProfileV1` profile already used by `node/capability`.

```text
capability_id = "messaging-receive"
grant         = "messaging/receive"
revocation freshness default = 300 seconds

scope profile:
  request/id
  sender_subjects
  recipient_routes
  contact_nym_id?              # optional; when present, MUST be contact-nym:*
  purposes
  max_revocation_staleness_seconds
  limits?
```

The messaging acceptor applies three messaging-specific checks after Capability
Binding has verified the passport signature and freshness:

- the sender subject in the envelope must match `sender_subjects`;
- the receiver route must match `recipient_routes`;
- `contact_nym_id`, when present in the profile, is an additional pairwise
  contact constraint and must match a `contact-nym:*` receiver context; route-only
  profiles for a `routing:did:key:...` receiver intentionally omit it;
- the purpose must include `messaging`.

For this solution, a routing subject is a routable pseudonymous subject rather
than a full participant nym. It can act as a routing nym for delivery and reply
routes, but it does not automatically carry pairwise contact-nym, relationship,
reputation, or recovery semantics. Those semantics are added only by an
explicit binding/profile or by Local Relationship state.

The preferred private post-accept receiver subject is the pairwise
`contact-nym` created for the accepted messaging relationship. Its transport
reachability is resolved through a private binding or projection to node or
routing-subject delivery targets, without exposing a root participant id. A
dedicated per-contact routing subject is only the fallback receive-route
profile when `contact-nym` delivery is not available.

Messaging keeps two precedence orders explicit. Relationship/conversation
subject selection prefers `contact-nym/id`, then `participant/id`, before
falling back to transport fields. Delivery target selection keeps the transport
order: `routing-subject/id`, `node/id`, then `participant/id`. This prevents a
routable subject from silently hiding a participant identity in relationship
matching while preserving the existing delivery path for AD/INAC targets.

Sender-side passport lookup keeps those two axes separate. When the queued
recipient route is a transport subject such as `routing:did:key:...`,
`capability.passport.lookup` requires that transport receiver and must not
send the sender-local `contact-nym/id` as an additional scope requirement. If
the returned `messaging-receive@v1` passport is pairwise-nym scoped, the
sender records that receiver-issued `contact-nym/id` in the effective route
context before delivery. Passport route context may refresh the pairwise
`contact-nym/id`, but it must not overwrite the current queued transport route;
transport fields from the passport only fill missing address fields.

The passport may be presented inline or by reference, but the service never
owns private keys and never mints the passport directly.

The host evaluates receive authority for every message from the active root and
the actual receiver/route. A passport is one basis, with its current complete
proof and parent status. An independent local `contacts` consent is another basis
only while its author/receiver currently has sovereign authority. A delegated
participant's local facts can restrict consent but cannot grant beyond its parent.
An empty roster gives no authority. Root activation can remove independent
membership eligibility without rewriting facts. A receiver-issued pairwise
`contact-nym` route is local only for an active contact of the
signature-authenticated sender, and it satisfies a consent only as that
consent's exact `contact_nym_id`; a wildcard or route-list entry cannot replace
that binding. Every local issuance path publishes its receipt into the current
authority observation before handoff. Only an explicit operator decision may issue
delegated consent; automatic reciprocity or repair falls back to that decision.

Membership projected from a passport carries `basis.kind=passport` and
`basis.passport/id`. It remains relationship/UI data; expiry or withdrawal of
the passport cannot be bypassed through that projection. Independent local
decisions (`basis.kind=local`) have a separate reduction of their history, so
projections cannot erase an explicit block or create an independent consent.
An independent consent is changed by a separate explicit local action. Each
accepted message retains the host decision, selected basis and eligibility
evidence alongside the signed envelope, without changing that envelope.

Verifier boundary rule: when `capability_id = "messaging-receive"`, the
capability layer rejects passports that do not contain at least one canonical
`messaging-receive@v1` scope profile, and it rejects alternate profile
discriminators such as bare `messaging-receive`. If
`max_revocation_staleness_seconds` is omitted by an older producer, the typed
profile defaults it to 300 seconds before evaluation.

## Host Capabilities

The messaging service consumes host capabilities through the standard supervised
module environment:

- `ORBIPLEX_HOST_CAPABILITY_BASE_URL`;
- `ORBIPLEX_HOST_CAPABILITY_AUTH_HEADER`;
- `ORBIPLEX_HOST_CAPABILITY_AUTHTOK_FILE`.

The following capabilities are part of the solution boundary:

| Capability | Owner | Messaging use |
| --- | --- | --- |
| `capability.passport.lookup` | Daemon / Capability Binding | Select or verify a usable `messaging-receive` passport for outbound queue promotion and inbound `passport-ref` admission. |
| `local-recipient-mailbox.resolve` | Daemon / local participant authority | Resolve an inbound receiver route and optional public handle to an operator or participant mailbox. |
| `artifact.delivery.send` | Daemon / Artifact Delivery | Send signed `contact-request.v1` via contact lookup and signed `message-envelope.v1` via `private-direct`; outbound envelopes carry `classification.v1` so INAC/private routes pass the shared classification egress guard. |
| `signer.sign` | Daemon / signer | Sign outbound contact requests and message envelopes under the `contact-request.v1` and `message-envelope.v1` domains granted to `messaging-service`. |
| `memarium.write` | Daemon / Memarium | Append bounded Layer 3 messaging facts. |
| `notification.create` | Daemon / notification center | Notify the operator about newly stored inbound messages. |
| `identity.routing-subject.create` | Daemon / Pseudonym Vault | Create a private reply route for outbound contact requests. |
| `identity.messaging-recovery.mirror` | Daemon / Pseudonym Vault | Persist private recovery mirror records for membership and receive-passport references. |
| `agora.vault.put/list/get/delete` | Agora service / daemon host bridge | Store and recover encrypted generic vault artifacts for recorded messages without exposing message metadata as Agora topic records. |

## User-Mode Readiness

The user desktop wizard treats messaging readiness as an application-level
requirement after participant identity and operator binding. This gate is for
the user-mode app and messaging surface; operator/headless nodes may keep
messaging disabled and report it as a degraded or unavailable capability
without blocking the whole node.

The MVP wizard has one messaging setup screen. It checks or prepares:

- Local Relationship Store readiness and owner/ref configuration;
- `messaging-service` enabled/running status;
- the local `messaging-send` readiness/passport gate, issuing the missing local
  passport with a bounded bootstrap lifetime when the daemon exposes it as a
  pending local-readiness requirement;
- Maildir/SQLite/Temporal storage paths reported by the service;
- a contactability draft with a messaging routing subject.

Public e-mail or SMS is optional at this stage. The default mode is
`pseudonymous-only`: the daemon creates or reuses a Pseudonym Vault
`routing-subject` for messaging contactability and stores an explicit draft
marker with no public handles. The alternate `public-handle-draft` mode stores
an e-mail/SMS draft routed through the same routing subject; attestation and
Contact Catalog publication remain in the full messaging surface.

This setup does not create a global "messaging nym". Contactability names a
local routing subject, and pairwise contact nyms are created only when a
contact request or relationship is accepted.

## Storage Model

Layer 1 is Maildir. Outbound local bodies are stored as native Orbiplex EML
profile v1 files under `maildir/outbox/body/`, so the outbox can be
reconstructed without SQLite. Inbound accepted `message-envelope.v1` artifacts
remain byte-identical signed JSON under `<mailbox-id>/new/*.json`; an EML
Maildir sidecar under `projections/maildir-eml/` is only a regenerable MUA
projection marked by `.orbiplex-projection`. Bodies are retained until
explicit user/operator delete or archive.

Layer 2 is SQLite. It stores mailbox indexes, outbound queue state, pending
Layer 3 facts, and recovery replay cursors. It is
rebuildable from Layer 1 plus Layer 3 and vault recovery records.

Layer 3 is Memarium. It receives separate fact schemas, not a generic
`messaging.fact.v1` artifact:

- `messaging.passport-issued.v1`;
- `messaging.passport-revoked.v1`;
- `messaging.retention-decided.v1`;
- `messaging.crisis-marked.v1`.

If Memarium is unavailable, the service stores facts in `pending_facts`, reports
`degraded`, and replays them idempotently when requested.

Recorded messages add a side path, not a fourth messaging storage layer.
`message-envelope.v1.recording` states that a signed envelope is intended for
encrypted preservation. The messaging service keeps delivery authoritative in
the ordinary outbox/mailbox state and then attempts a best-effort
`agora.vault.put` of an `agora-vault-entry.v1` artifact. Vault failures update
the message's `vault.*` diagnostics and remain retryable; they do not roll back
message delivery. Replies or forwards to a locally known recorded parent must
carry `recording.required = true`; otherwise inbound admission refuses before
Maildir write with `recording-lineage-required`.

## Mailbox Resolution

Inbound messaging always calls `local-recipient-mailbox.resolve`; it never
infers a mailbox from `contact-nym/id` alone.

The daemon owns local public-handle evidence in a store separate from remote
address-book contacts. `verified` means a fresh evidence reference to a
contact-control passport exists. A local UX projection without that evidence is
only `mapped`. Node-id or routing-subject delivery without a known public
handle or local participant-handle evidence falls back to the operator mailbox.

When the receiver is a nym or participant id, that identity is the primary
routing authority. A public handle supplied with the message may narrow the
route only when local evidence proves that the handle belongs to the same
participant; otherwise the daemon refuses without giving the sender a
user-unknown oracle.

## Outbound Flow

The outbound queue is deterministic and retryable:

1. `waiting-for-route` sends a signed `contact-request.v1` through
   `artifact.delivery.send` with `selector/kind = contact-lookup`,
   `lookup/mode = invitation-only`, and
   `selector/purpose = contact-request/messaging`. The request uses the
   signer-derived participant id and a fresh routing-subject reply route from
   the Pseudonym Vault. If Contact Catalog lookup is the only known recipient
   address, `recipient/route` is omitted; the receiving daemon binds the
   request to its local node id instead of trusting a sender-invented route.
   The `artifact-delivery-envelope.v1` wrapper is labelled
   `classification.v1` with `effective_tier = Community`, matching the
   hard-MVP INAC/private route budget.
   When a `contact-lookup-result.v1` arrives for an outbox item, the service
   promotes only concrete route candidates whose `selected/route.purposes`
   contains `messaging`; `no-match`, `policy-denied`, and `ambiguous` are
   terminal failures, while stale or rate-limited results stay retryable.
2. `waiting-for-contact-permission` calls `capability.passport.lookup` for a
   usable `messaging-receive` passport. Repeated equivalent contact requests
   use a logical local-state id derived from sender, recipient route, requested
   capability and purposes, so retries collapse the visible pending prompt while
   preserving the original wire `request/id` in the stored request JSON.
3. `ready-for-delivery` builds and signs `message-envelope.v1`, attaches the
   passport reference or inline passport, and sends it through
   `artifact.delivery.send` as `private-direct`. The AD envelope carries the
   same `Community` classification label before leaving the service boundary;
   message-body privacy and future per-conversation policy remain separate
   messaging-domain layers.
4. `in-flight` becomes `delivered` after a successful host capability call.
5. Retryable transport/host failures set `next_attempt_at`; terminal schema,
   conflict, or scope failures become `failed-terminal`.

The service never sends unsigned artifacts. If `signer.sign` is unavailable,
the queued row remains retryable and the service reports degraded state.

## Recovery

The recovery boundary is private and host-owned. The messaging service mirrors:

- `contacts` membership records;
- `messaging-receive` passport references needed to recover receive consent.

The daemon persists these records through
`identity.messaging-recovery.mirror` in a durable local recovery mirror table.
Local contact and messaging recovery bundles are sealed into
`pseudonym-vault.v1`; import and operational-vault-key startup replay preserve
terminal pairwise mapping states. Legacy root-only snapshots are handled as
recovery/migration inputs, while explicit passphrase replay covers
`root+local-passphrase` local-contact recovery snapshots. A separate
`POST /v1/messaging/reindex` rebuilds SQLite mailbox indexes from Maildir and
Layer 3 facts and exposes `reindexing` through service status.

## UI Boundary

Node UI owns `/middleware/messaging`; `/admin/messaging` redirects there. It
renders status, contactability draft
settings, provider challenge/redeem controls, compose, inbox, mailbox lists,
read/unread controls, outbox, message detail, pending-facts diagnostics, and
recovery/reindex actions by calling `/v1/messaging/*` daemon proxies. It does
not duplicate messaging policy logic.

Fresh pseudonymous drafts may omit attestation objects. The panel renders a
`draft` status and blank provider/challenge fields for absent/null optional
parents; rendering does not establish attestation or change readiness.

The contactability panel is draft-first. Editing public handles and route
bindings never mutates Contact Catalog state until the user invokes `Publish`.
`Publish` now requires contact-control evidence from the attestation flow and
submits a signed `contact-claim.v1` admission to the supervised Contact Catalog.

Local contacts are a daemon-owned UX and continuity projection. They may carry
labels, local metadata, and the active pairwise `contact-nym` mapping used for
operator-facing continuity, but they are not network evidence. The canonical
receive-consent state is Local Relationship `contacts` membership plus the
corresponding `messaging-receive@v1` passport.

`mailbox.open` is a host-owned notification action target. It opens
`/admin/messaging/messages/{message_id}` and may mark the notification handled
or the local read UX state; it does not mutate messaging-domain consent or
delivery state.

The user contact chat modal is a narrow read-model over the same mailbox and
outbox stores. It derives route keys from the selected local contact, normalizes
inbound and outbound rows before matching, and only matches exact canonical
keys. Human labels and display names are presentation data, not identity
evidence. The modal fetches at most a bounded recent window, hydrates text
bodies through the bounded body endpoints, and renders non-text, oversized,
missing, or digest-mismatched bodies as placeholders or typed error rows.
Opening or refreshing the modal has no write effects. Read state changes only
through the explicit mark-read command, which recomputes conversation
membership and writes `messaging.flag.v1` facts for visible unread inbound
messages. `messaging-mailbox-changed` SSE carries only id-like invalidation
data; the UI then re-reads through authenticated HTTP and preserves the composer
while swapping the history fragment.

The local contact route-key index is active-contact only. `handle.kind =
"other"` remains a display/local-continuity handle, not a Contact Catalog lookup
handle; when its value is itself a typed route subject (`routing:*`,
`participant:*`, `node:*`, `contact-nym:*`), the index records the corresponding
typed route key so contact-request repair and conversation matching can reuse
the existing contact. The index is rebuildable: opening an upgraded local
contact store backfills missing route-key index rows from stored contact records
before matching uses it. `state = blocked` contacts are excluded from active
matching, and existing schema-safe `pairwise/contact-nym-id` values are
preserved during contact-request repair instead of being replaced by fallback
nyms. If a repair replaces a legacy non-schema-safe nym, the daemon emits a
typed audit trace with an explicit `legacy-contact-nym-not-schema-safe` reason.
The user contact rail excludes local receive `routing-subject` keys from its
dedupe set but keeps participant and `contact-nym` keys, so route rotation does
not hide a distinct contact while stable pairwise identity still collapses
duplicates.

For operator/MUA tooling, inbound signed JSON envelopes remain the authority.
The `projections/maildir-eml/` tree is a disposable Maildir projection marked
with `.orbiplex-projection`; a MUA may rename files or set Maildir flags there
without mutating canonical messaging state. Outbox bodies are native Orbiplex
EML profile v1 files and can be used for outbox recovery during `reindex`.

## Implementation Tracker

Completed rows retain their measured scope. S027-009 is a separate continuation
with five implementation gates; registering it does not reopen or extend the
historical S027-001–008 qualifications.

| ID | Feature | Status | Evidence |
|---|---|---|---|
| S027-001 | Canonical `messaging-receive@v1` profile enforcement | done | Node `capability` rejects non-canonical `messaging-receive` profile discriminators, defaults missing `max_revocation_staleness_seconds` to 300 seconds, accepts route-only profiles without `contact_nym_id`, and rejects malformed `contact_nym_id` values that do not use the `contact-nym:*` namespace. |
| S027-002 | Messaging service runtime | done | `messaging-service` covers inbound accept, outbox, contact-lookup-result promotion, sender-side lookup against a shared remote Contact Catalog provider, receive-passport handoff, private-direct delivery, native EML outbox body storage, canonical inbound JSON Maildir storage with disposable EML sidecar projection, SQLite storage, bounded body-read endpoints for inbound mailbox rows and outbound outbox rows, temporal outbox transaction/event/attempt tables with `outbox` as the public projection, redacted outbox event snapshots that omit raw recipient handles and subjects, replay-equivalence tests, operator temporal diagnostics endpoints for status/redacted events/correlation/replay-check via daemon proxy, recorded-message lineage enforcement, best-effort Agora Vault storage diagnostics and retryable vault-job replay, kind-specific Layer 3 fact artifacts, pending Memarium replay, recovery mirroring, receiver-side revocation snapshot checks for inline `messaging-receive@v1` passports, fail-closed no-host behavior for passport-based first contact, revocation-triggered `messaging.passport-revoked.v1`, read/unread sync through `messaging.flag.v1`, reindex with remote Memarium replay + local Layer 3 replay + native EML outbox recovery + canonical inbound Maildir JSON + disposable EML sidecar rebuild + FTS5 rebuild, and strict Story-010 cross-node delivery smoke coverage. Mock-host coverage covers inline revocation, outbound passport lookup, signer, `artifact.delivery.send`, `agora.vault.put`, redacted failure classes, and remote replay. |
| S027-003 | Contactability and local contacts | done | Daemon exposes contactability draft/options/attest/publish endpoints, requires contact-control passport evidence at publish time, binds the published owner participant to the draft route or attestation passport subject, signs canonical route-set `contact-claim.v1`, admits it to the supervised Contact Catalog, validates `local-contact.v1` import/export, stores local contact labels/metadata, tracks pairwise mapping lifecycle, and exposes `/v1/local-contacts/resolve`. Local contact and messaging recovery bundles seal into `pseudonym-vault.v1`, replay on import and operational-vault-key startup, preserve terminal pairwise mapping states, treat root-only as recovery/migration-only, and explicit operator passphrase replay covers `root+local-passphrase` local-contact recovery snapshots. |
| S027-004 | Contact attestation service dependency | done | Node adds `attestation-core`, supervised opt-in `attestation-service`, contact attestation schemas/examples, schema-gate validators, `email-attestation` / `phone-attestation` capability ids, local/dev delivery, SMTP email delivery, SMS webhook delivery, attempt limits, challenge TTL, quotas, delivery audit, and a default-disabled `always_accept` provider policy for local acceptance profiles. Daemon contactability options discover trusted/fresh `role/email-attestation` / `role/phone-attestation` providers through Seed Directory, expose provider status in Node UI, start challenges through daemon contactability endpoints, import immediate `always_accept` passport results when returned, and retain challenge redeem for non-local profiles. Story-010 now uses that runtime path for e-mail-control acquisition without manual OTP handling in local profiles. |
| S027-005 | Node UI messaging surface | done | Node UI renders `/admin/messaging` with contactability draft controls, provider challenge/redeem controls, compose, local-contact based unknown-recipient warning, inbox, read/unread actions, outbox, diagnostics, and message detail. User UI also renders a contact chat modal as a bounded read-model over the messaging-service mailbox/outbox stores: it hydrates text bodies through bounded body endpoints, merges inbound and outbound rows through the shared `local-relationship-core::route_key` canonicalizer, refreshes history through `messaging-mailbox-changed` SSE plus polling fallback, and marks rendered unread inbound rows through an explicit mailbox-scoped flag mutation. Relationship/conversation subject precedence is separated from delivery-route precedence so `participant/id` is not hidden by a transport route, and active local-contact route-key matching preserves schema-safe pairwise contact nyms while excluding blocked contacts. |
| S027-006 | Story-010 acceptance pack | done | `node/tools/acceptance/story-010-operator/` provides two-node profile generation, launchers, UI helpers, `story-smoke`, and self-contained `ad-smoke`. Strict `ad-smoke` now defaults to the no-scaffold path: `contact-request.v1` is admitted through the schema-scoped INAC preflight/policy gate, then the receiver sees the contact-request notification and explicitly accepts the relationship before any `message-envelope.v1` delivery authority exists. It also covers local `always_accept` Attestation Service acquisition through daemon contactability endpoints, daemon contactability publish, supervised Contact Catalog admission, shared remote lookup, contact request delivery, operator accept, `messaging-receive@v1` passport handoff, private-direct `message-envelope.v1` delivery, delivered inbox/outbox state, `messaging.flag.v1` read/unread replay, and a second recorded message stored as an encrypted generic artifact in Node B's Agora Vault. The old peer allowlist/preissued transport passport path and explicit INAC operator-approval path are retained only as acceptance debug/policy variants. |
| S027-007 | User-mode messaging readiness wizard | done | Node UI has five welcome steps: participant identity, key unlock phrase, operator binding, Messaging issuance authority (sovereign or bounded grant) and Messaging. The latter two can be durably deferred to enter `/app` with visible status. The step can enable `messaging-service`, checks Local Relationship owner/storage readiness and `messaging-send` readiness, creates/reuses a Pseudonym Vault routing subject, and saves either explicit `pseudonymous-only` contactability or a `public-handle-draft`. It does not mint a global messaging nym; pairwise contact nyms remain acceptance-time relationship facts. |
| S027-009 | Recipient-consent loss and duplicate-safe delivery recovery | todo | Development foundations exist; the [single-source tracker](#consent-loss-recovery-tracker) still requires complete contracts, insert-once admission, historical INAC reconciliation, explicit retry/UI and retained qualification. |

### Bounded Memarium Recovery (S027-008)

Logical mailbox IDs are preserved by Layer 1 `mailbox.json`, using
`messaging-mailbox-storage.local.v1`. Filesystem slugs are physical locators, not
mailbox IDs. Reindex verifies all descriptors before clearing the index; old
pre-release directories can acquire a descriptor from retained exact mailbox IDs
or flag facts. Missing/ambiguous historical identity fails explicitly and never
infers ownership from the current operator. Colliding slugs refuse admission.

The service reserves each unconfirmed fact durably before publication. Read flag
changes and receive-passport promotion commit their local projections, temporal
events and fact in the same SQLite transaction. An immediate transaction serializes
capacity checks across connections. The default budget is 1024 records and 16 MiB of
serialized UTF-8 fact JSON. Full capacity refuses a new local change with HTTP 503
`reason/code=pending-facts-capacity-exhausted`; it does not become an authority denial.
Unconfirmed facts have no expiry/drop policy. Initial publication and replay use the
same stable fact ID, payload and idempotency key. Only a matching semantic Memarium
confirmation frees a slot; transport success alone does not.

Explicit pending replay is bounded to 100 records. Remote reconstruction pages
through the existing Memarium offset/upper-time query contract with a fixed snapshot
boundary and a 100-page work budget; exhaustion reports degradation and retains known
flags. Reindex merges read `set`/`cleared` facts without clearing known state on a
partial/unavailable read. No starred/marked flag is introduced. Paused and terminal
outbox states preserve their independent authority/retention semantics.

The independent `S027-008` runtime fixture uses real host Memarium. It disables and
restores `memarium.enabled` through profile configuration plus daemon reload, rather
than killing a Memarium process. Explicit Personal-space grants, fixture budgets of
4 records/8192 bytes, count/byte refusal before mutation, restart, repeated replay,
read/unread flags and a fault after remote write but before pending-copy cleanup are
separate measured gates. It must retain `authority-blocked` and terminal outbox
results. Runtime measurements are required in addition to storage/conformance tests.

| Task | Scope | Status | Completion gate |
|---|---|---|---|
| S027-008 | Bounded durable facts and actual Memarium outage/recovery | done | Atomic capacity refusal; real component controls; stable ID/payload through unknown results, restart/replay/reindex; one remote fact per intent; read set/cleared and paused/terminal outbox preservation. |

The `2026-10-16` clean-source candidate passes 23 independent real-Memarium cases,
with 132 service conformance tests and the separately measured P097 browser/strict
Story-010 gates. Runtime measurement exposed and corrected two additional defects:
missing daemon `discard` forwarding/SSE invalidation, and lossy mailbox-directory
names used as logical IDs during reindex. The retained manifest pins clean sources,
profile inputs, six unchanged binaries and the offline browser. Review and reports:
`node:docs/evidence/messaging-onboarding/2026-10-16/README.md`. This scoped local
qualification does not establish release readiness or ordinary delegated authority.

## Recipient-Consent Loss and Delivery Recovery {#consent-loss-recovery}

**Decision registered 2026-10-28; implementation `todo`.** Close the loop from
recipient-consent loss to a truthful sender state, renewed explicit consent and
safe resumption of the same message. This is the owner of S027-009; the linked
consumer documents do not maintain parallel completion trackers.

### Ownership and Implementation Recommendations

Reuse `messaging-core` for message identity and the pure transition function
`(state, event, verified facts) -> (state, effects, allowed_actions)`;
`messaging-service` for domain admission, Maildir/SQLite and the temporal outbox;
the existing INAC ledger for attempt reservations and historical outcomes; and
AD for transient transport retries. Preserve S027-008's durable pending facts
and Memarium recovery. UI renders owner-produced actions, not a second state machine.

The upstream contracts remain [P060](../../40-proposals/060-messaging-middleware.md#consent-loss-recovery),
[P032's shared verification operations](../../40-proposals/032-key-delegation-passports.md#shared-verification-operations),
[P076-036/037](../../40-proposals/076-limited-messaging-grants-decision.md#messaging-consent-loss-recovery),
[P097](../../40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md#recipient-consent-recovery-acceptance),
[S017](../017-inter-node-artifact-channel/017-inter-node-artifact-channel.md#messaging-admission-reconciliation),
[S023](../023-artifact-delivery/023-artifact-delivery.md#messaging-delivery-recovery) and
[S028](../028-temporal-storage-convention/028-temporal-storage-convention.md#messaging-recovery-retention).

1. **Freeze two identities.** The message commitment covers the validated original
   JSON except top-level `authorization` and `signature`, preserving extensions,
   sender, route, body, metadata, thread/parent and recording. Verify the sender's
   authenticated binding separately. The attempt digest covers the complete signed
   envelope. Freeze `sent/at` and message content at first construction; changed
   content requires a new ID. Persist exact attempt bytes, carried-proof binding,
   generation and idempotency key before AD submission; bind AD's returned ID once
   known. Lost responses recover that submission, not a rebuilt envelope or new
   generation. Changed transmitted proof/envelope requires a new generation;
   refreshed local verification context need not change the envelope.
2. **Insert once at the domain owner.** The same ID, authenticated sender and
   message commitment yield `AlreadyPresent`; conflicting identity yields
   `identity-conflict`. Preserve the first envelope, Maildir path, mailbox,
   recording and read state, without duplicate files, notifications or recording.
   Serialize reservations across connections and use atomic no-overwrite file
   publication. Distinguish reservation, durable domain admission and confirmed
   ledger outcome; reconcile crashes from exact durable evidence, leaving gaps
   unknown. Reindex must not replace the first envelope or manufacture admission.
3. **Require the ledger before effects.** Reservation failure prevents acceptor
   execution and single-use consent consumption; mailbox reads remain available.
   Bind attempts to authenticated peer, generation idempotency key and envelope
   digest, rather than a globally trusted raw transfer ID. The ledger records the
   domain owner's outcome; transport success cannot create it. A finalization
   failure after domain commit remains reconcilable, not a negative admission.
4. **Separate current permission from history.** Every body push rechecks current
   local authority and recipient consent. Reuse P032/P076 bounded proof verification,
   independently admitted trust and retained revocation knowledge, with acquisition
   as a separate authorized effect. Preserve all three P076-037 acquisition modes,
   presenter renewal/disclosure and budgets. Missing/stale material,
   `AcquisitionDisabled` and source outage are not confirmed consent refusal.
   Historical admission is a fact, not permission for another push. Whisper's
   prepared-byte/reconciliation laws are useful comparisons, but its accepted-release
   authority and pending ADC/LLR implementation are not Messaging dependencies.
5. **Read an exact historical result.** Proposed INAC `admission-status` /
   `admission-status-result` and host `artifact.delivery.reconcile` query a bound
   attempt without body, acceptor invocation or consent consumption. Authenticate
   and scope the caller before disclosure; current receive consent is not required
   to read its own attempt. Return a known outcome, `unknown`, or read unavailability;
   absent record, foreign peer and wrong digest share the same `unknown` shape/code.
   Limit replies to 4 KiB under INAC budgets. Authenticated support for
   `messaging-admission-identity.v1` must cover the retry's deduplication horizon;
   an untrusted label or unsupported receiver cannot enable uncertain retry. This
   session-bound read is not a portable signed/time receipt; add no new keys or
   receipt family. Freeze these proposed contracts through Schema Gate before exposure.
6. **Preserve typed causes and causal order.** Carry existing `RefusalCode`,
   `retryable` and `retry_after_ms` through AD and its durable status. Map private
   recipient-consent reasons to `recipient-consent-required` before the wire, without
   implying global passport revocation. Local AD `404` means
   `delivery-outcome-unknown`, never automatic retry; read failure preserves the
   current state/delivery ID with a separate unavailable observation. Confirmed
   admission or `AlreadyPresent` makes delivery terminal. A late matching success
   may confirm it; an old refusal cannot downgrade it or block a newer generation.
7. **One retry owner.** AD gets at most five actual pushes within 15 minutes per
   generation, subject to stricter host policy, with durable counters/deadlines.
   Messaging creates no competing delivery or transport loop. Single/bulk retry
   share one transaction and operation/item idempotency. Ordinary retry requires
   resolved prior attempts; any still-unknown effect requires a distinct confirmed
   uncertain retry, current authority/consent and applicable receiver deduplication.
   Preserve `waiting-for-contact-permission` for the original intent;
   `authority-blocked` and `recipient-consent-blocked` require explicit recovery.
   New grants, GET, unlock, refresh, restart and reindex do not resume a blocked send.
   Extend existing retry APIs and add participant-scoped
   `POST /v1/messaging/outbox/{id}/reconcile`, with owner checks and CSRF in UI.

### Exact-attempt reconciliation contract

Contract checkpoint for S027-009-01. The delivery owner freezes the message ID,
generation key, message commitment, signed-envelope digest, receiver and original
`resume/until` with the prepared submission. Direct INAC and Matrix mailbox use
the same stored key and the envelope ID as `artifact/id`. The transport verifies
the final artifact against the prepared envelope. An object pointer has its own
digest. AD publishes its local execution ID separately from the prepared binding.

Historical reads use an established authenticated WSS session to the original
receiver for either push route. Each operation has a five-second total deadline
and at most one query with a 4 KiB response. Work is shared per message generation
and limited to one active query per peer. A missing session or unsupported route
produces `unavailable`. A receiver with a working ledger emits the same public
`unknown` for an absent, foreign or mismatching record. Budget and correlation are
per authenticated peer. An authorized owner can repeat the POST after a retained
success and receive the current `delivered` view without network work.

| Verified observation | Sender transition | Current execution fact |
|---|---|---|
| Accepted or already present for a retained current generation | `DomainAccepted`, then `delivered` | Resolve this execution |
| Accepted or already present for a retained older generation | `DomainAccepted`, then `delivered` | Preserve the newer execution fact |
| Current consent refusal with all effects resolved | `RecipientConsentDenied`, then `recipient-consent-blocked` | Resolve this execution. Explicit recovery checks current consent |
| Other current refusal with all effects resolved | `RemoteDeliveryRejected`, then `failed-terminal` | Resolve this execution. Evaluate the retained retry flag and deadline for command admission and allowed actions |
| Older refusal, a refusal during running AD, or remaining uncertainty | Retain the observation for its attempt | Preserve current execution and retry restrictions |
| Unknown | Observe, preserving the message state | Preserve current execution and retry restrictions |
| Unavailable | `ObservationUnavailable` | Preserve current execution and retry restrictions |
| Missing current local AD result | `LocalDeliveryMissing` for an unresolved message | Unknown. The retained exact binding can still identify the execution |

The delivery owner must establish completion and exclude all outstanding effects
before a rejection can resolve an execution. Signature, query correlation and
generation matching alone do not establish completion. Epoch-pinned receiver
deduplication protects a separately confirmed retry while uncertainty remains.

INAC reserves the attempt, its result budget and any single-use consumption in
one transaction. It gives the acceptor an opaque reservation token. Messaging
records the token with the domain result of that push. A repeated generation can
record `AlreadyPresent` while preserving the first admission and envelope.
Withdrawal after INAC commits but before domain admission retains consumption
and produces `recipient-consent-required`. Startup repair proceeds from exact
Messaging facts into INAC after owner recovery. A bare reservation stays unknown.

The push-result journal has its own 10,000-record and 32 MiB logical byte limits.
Reserve capacity before domain admission. An unacknowledged repair fact remains
held through restart and GC. After durable finalization, INAC keeps the result
until Messaging has durably recorded confirmation and acknowledged it. Both
owners then apply the later of the resume horizon and 31 days from completion.
Messaging persists the floor returned by INAC before sending its acknowledgement.
If the acknowledgement reply is lost and INAC retires the token, a later read of
its absence can complete the acknowledgement only after the saved floor and only
with that existing local finalization receipt. Unresolved INAC reservations
and empty Messaging placeholders expire 31 days after the original resume
deadline. INAC admits at most 256 unresolved generations per authenticated
peer inside the shared budget. If a pending domain fact outlives both floors,
only confirmed absence of its exact token permits retiring the repair as
unresolved. Until settlement or expiry, a committed repair fact protects
its first admission from deletion. The two ledgers may reach capacity independently.

Implementation checkpoint, 2026-11-22. Node carries the prepared commitment,
envelope digest and original deadline through AD and INAC. The runtime gives
the commitment, signed-envelope digest, final artifact-bytes digest and AD
submission digest distinct types. The two adapters and the receive bridge
use the same digest relation for the final artifact. Their wire fields and
canonical preimages retain their existing encoding. The receive bridge
requires an exact ledger reservation before the acceptor, atomically consumes
any single-use invitation, and serves peer-scoped historical point reads.
The direct AD adapter preserves typed remote refusals. The local
`artifact.delivery.reconcile` host contract and owner-scoped outbox POST use
the frozen binding and established INAC session. Messaging persists a verified
positive observation and a recovered execution ID atomically with the outbox
state. A remote refusal without complete execution evidence preserves the
prior uncertainty. The receive path carries an opaque push token through AD.
Messaging checks the token against the INAC reservation through the local
[`messaging.delivery.push.check` contract](../../../schemas/messaging-push-check.local.v1.schema.json)
and commits the exact per-push fact with the admission journal transition.
INAC finalizes positive results from this fact. A bounded background pass after
journal initialization replays exact committed facts through the local
[`messaging.delivery.push.settle` contract](../../../schemas/messaging-push-settle.local.v1.schema.json).
It persists the [retention receipt](../../../schemas/messaging-push-settlement.local.v1.schema.json)
before acknowledgement. A component test drives both SQLite collectors at
the retention floor. It loses the reply after INAC records a duplicate result
and then loses the acknowledgement. Each GC order preserves the pending
repair until the corresponding durable receipt allows release.

The complete Messaging journal owns the epoch and
[admission support declaration](../../../schemas/messaging-admission-identity.v1.schema.json).
Its contract digest is SHA-256 of the exact canonical schema file. The epoch is an
opaque, canonical base64url value encoding 32 bytes. INAC can accompany a
historical result with this declaration independently of the identity examined.
The sender's AD owner makes one bounded observation over the already established
authenticated session and seals it in the exact binding before its first body
effect. Current sender authority also gates this observation because it
discloses identifiers of the new attempt. A missing or insufficient observation
seals a missing pin. A later observation cannot backfill it. The pin binds the receiver, the
original query and resume horizon, the contract digest, and the complete
store's epoch and coverage. A current observation must confirm continuity with
those bounds before an uncertain retransmission could use the pin. Exact
positive historical readback needs no pin.

The 2026-11-22 development run delivered strict Story-010 with explicit INAC
approval over WSS. Inspection after shutdown matched the sealed sender pin to
the receiver journal's epoch. A separate cold readback on those synthetic profiles
removed the AD run and its Messaging-side handle and injected the sender's
`delivery-outcome-unknown` state. The real outbox command restored `delivered`
and the original handle with no new generation, push or change to the first
receiver admission. The injection exercises readback after loss of the local
record. A subsequent active-delivery fixture removed the terminal AD run before
the sender's poll. A real AD `404` paused the outbox, and the WSS read confirmed
the original admission with no new generation or push. This case also exposed
missing vault scheduling for a recovered recorded message. The owner now
enqueues the vault job in the same transaction as the confirmation and uses the
confirmed signed envelope for the job. A development rerun repeated the pause
and recovery and reached `vault.stored`.

A loopback transport fault discarded receiver-to-sender traffic during a second
real admission. The receiver committed one push while the sender had no success
result. After sender restart and loss of the local AD run, polling produced `404`
and the receiver revoked the original passport. The established WSS session then
returned the exact historical admission. Reconciliation preserved the prepared
envelope, generation and first receiver admission. The strict Story-010
runner observes the matching receiver response on the native WSS session
before continuing and checks zero new pushes, generations and acceptor calls. A
separate daemon integration regression uses two independently signed client
sessions and a seeded receiver ledger. It compares absent, foreign and
mismatched results, checks that reading leaves the ledger unchanged, and observes
`unavailable` for a damaged own record without disclosing it to the foreign peer.

A repeat with the return-traffic fault exposed an ordering error at sender
startup. Outbox processing sampled the send guard before its host capability
channel was ready and recorded `authority-blocked` before polling the retained
AD handle. It now observes an existing message execution first. A status
transport failure preserves its state and handle, and a real 404 records
`delivery-outcome-unknown`. Envelope construction and a new submission still
require current send authority. The development repeat recovered the same
first admission after consent withdrawal and completed recorded-message vault
storage.

The development crash diagnostic stopped a live receiver on both sides of the
domain commit. Before the commit, the exact reservation survived and WSS readback
returned `unknown`, with no first admission or extra push. After the commit,
Messaging's exact push fact survived while the INAC reservation remained open.
After cleaning up the test's orphaned sidecars, startup replay finalized the
same `Accepted` token and released the owner hold. The sender recovered
`delivered` over WSS with the original admission, mailbox record, Maildir bytes,
generation and single receiver push intact. Both cases are reproducible with
the strict Story-010 recovery runner.

The duplicate variant used a newly issued passport and a different signed
envelope with the same message commitment. At that checkpoint the isolated
sender fixture staged the next generation. After a receiver crash, replay finalized the distinct
`AlreadyPresent` admission for the second generation. The WSS read used
that admission and preserved the original envelope, Maildir file set,
recording and read flag.

The sender-side crash diagnostic on 2026-11-22 fenced the Messaging write
before the new AD handle could be recorded and stopped the live Messaging
subprocess after AD committed the exact binding. The original AD run still
reached the receiver's admission. After shutdown, the fixture removed that
run and retained the binding. Following restart, the locally missing run
returned 404, and the WSS read recovered the handle, confirmed `delivered`,
and completed the recorded-message vault job. The prepared envelope,
generation, first receiver admission and single push survived the diagnostic.
The runtime was built from Node `38dc001a9`. The runner is
`node:tools/acceptance/story-010-operator/s027-ad-handle-diagnostic.py`.
The same fixture held the receiver while the first reconciliation queued
its historical query and issued a second POST for the same generation. Both
requests shared the same admission response and one WSS query. A subsequent
POST returned the delivered state without another query.

The late-success variant held the response while the fixture staged a newer
paused generation. A read for that generation returned busy without issuing
another peer query. The matching older result confirmed delivery, recovered the
original preparation's handle and left the newer generation's handle empty.
The read caused no additional push.

The rerouted-peer variant moved the same receiver identity to a new WSS
endpoint. The previous listener refused a connection. The established
session at the new endpoint returned the original admission without a push
or a generation change.

The local AD response now carries `execution/resolved` when a single direct
attempt's typed terminal refusal agrees with the authenticated historical
rejection and AD has the complete original run. Multiple attempts, uncertainty
or a missing run leave the marker absent. Messaging applies the exact current
generation's pause and stores the observation atomically. Subsequent owner
reads can return that saved result.

In a separate WSS diagnostic, the recipient withdrew the receive passport
after the exact INAC reservation became durable and before Messaging
committed an admission. The original reservation finalized with
`recipient-consent-required` and no first admission. After restart the
sender's historical read carried `execution/resolved` and persisted
`recipient-consent-blocked`. The same generation retained one push token
throughout the diagnostic.

The missing-ledger variant parked the receiver's SQLite file while the node
was running. The WSS read returned `unavailable` and preserved the outbox state
and generation. The existing mailbox message could still be read. Neither
read recreated the ledger. A separate development run parked the original
database across a receiver restart while retaining the local continuity marker.
The database stayed absent, the existing inbox stayed readable, and the
history response remained `unavailable`. Replacing the original database
restored the exact admission and left the original push count intact.
The continuity check identifies the enrolled database. Its coverage includes
loss and replacement while the marker is retained.

The Matrix-only development run enabled the mailbox adapter against a loopback
join and polling fixture and disabled both WSS listeners and dialers. The read
returned `unavailable`, preserved the sender state and generation, and emitted
zero Matrix events. Restoring the WSS route recovered the original admission.
A separate run disabled WSS without a mailbox route. Readback reported
`unavailable` without dialing or sending an INAC frame.

The focused WSS campaign qualified on 2026-11-22 from clean Node `6fc10c4b`
and Orbidocs `bf3d508a`. It passed 13 runtime cases, 558 component tests
and 57,997 Lean–Rust comparisons with 13 named reconciliation vectors. The
[retained campaign](https://github.com/diapod/node/tree/master/docs/evidence/limited-messaging/2026-11-22-s027-exact-history)
binds the exact sources, executable digests and observed results. Loose
and extracted qualification agree. The interrupted pre-merge attempt has
its own retained record and contributes no counts to this campaign.

The lost-WSS-response case correlates the original message and generation,
its AD submission, the exact receiver result and the retained admission.
After a real local AD `404` and consent withdrawal it confirms `delivered`
with zero new pushes, generations or acceptor calls. The three-peer test
measures authenticated read isolation. The receiver commit cuts and
duplicate case measure recovery without changing the first admission,
mailbox or read state. The fixture stages the newer generations used in
the duplicate and delayed-success cases. The 2026-11-23 S027-009-04/05
qualification separately generates the retry through actual user choices.

The shared exact-submission registry and checked digest relation cover
both adapters. INAC's historical ledger currently has one registered
consumer, Messaging. INAC and AD should extract common ledger policy
registration when a second family needs an exact historical read.

The November 22 follow-up review adds component regressions for reservation
expiry, pre-effect refusals, transient support probes and durable retry facts.
A receiver reports typed consent, identity, lineage or quota refusals from
its acceptor. Ambiguous failures preserve uncertainty. Before first exposure,
a busy or timed-out support read keeps the pin pending. The pre-push probe uses
at most three seconds within its enclosing execution deadline. AD records when this
probe stopped an attempt before any adapter received the body. Such a record
can exclude that attempt from possible remote effects when the owner verifies
a later refusal. Missing evidence keeps the earlier attempt uncertain. Both sender views use
the stored execution state and an absolute retry deadline. On an explicit
command the sender may check a saved running handle with its local AD owner
within the five-second deadline. Only an ended or missing local run allows
that command to proceed to peer history. Historical reads
use the AD digest frozen when preparing the generation. The follow-up WSS
diagnostic withdrew consent after reservation, restarted the sender and
observed `recipient-consent-blocked` without another push or generation. A
second WSS diagnostic repaired `AlreadyPresent` after receiver process loss,
preserving the first admission, Maildir copy and read state. The independently
pinned campaign above records the earlier revision.

### Retry Facts Across Generations

The message owner evaluates all generations that could affect the message. The
execution state joins their facts in the order `Resolved < Unknown < Running`.
Missing required history contributes uncovered uncertainty. Ordinary retry
requires resolved execution. An active execution prevents either retry.

The retry restriction and any absolute deadline come from the current
generation's resolved result. Earlier restrictions remain historical even if
the current generation has no result. A current deadline has elapsed when the
evaluation time reaches it.

Initial contact discovery may learn a pairwise receiver route from a consent
that lists the discovered transport route. An execution or retry lookup uses
`receiver/exact: true` and the receiver carried by the signed envelope.
The lookup, capability evaluation and Messaging admission share the same
pairwise constraint. A consent that requires a contact nym cannot authorize
retry on a prepared envelope carrying only a transport subject.

Confirmed uncertain retry requires deduplication coverage for every unresolved
possible emission. Each such generation needs a retained pin established
before its first possible emission. An authenticated current observation must
match the pinned receiver, contract and storage epoch, cover the emission
time and guarantee deduplication through the original recovery horizon.
The sender can still reconcile or explicitly close an uncertainty that lacks
this evidence. Exact positive historical admission can confirm delivery even
when the retry prerequisites fail.

New Messaging preparations request up to five possible emissions in one
15-minute window. Artifact Delivery owns the shared debit for all adapters on
that generation. A stricter host retry cap and the earlier of the persisted
delivery deadline and the original resume deadline still apply. An interrupted
handoff can leave a debit without an observed push.

### Explicit Retry Operation {#explicit-retry-operation}

The local daemon binds the operator when accepting
`POST /v1/messaging/outbox/retry-operations`.
[messaging-retry-command.local.v1](../../../schemas/messaging-retry-command.local.v1.schema.json)
accepts an ordinary selection, a preview selection, or confirmation of a
previously saved digest. The body contains no owner field.
`GET /v1/messaging/outbox/retry-operations/{operation_id}` returns the
[operation and durable item receipts](../../../schemas/messaging-retry-operation.local.v1.schema.json)
without executing work. Only initial preview creation provides its token.
An earlier journal receipt is available at `/v1/messaging/outbox/retry-operations/legacy/{key}`.

`GET /v1/messaging/outbox/recovery?page=N` returns a page of up to 25 entries
from the authenticated operator's outbox, with adjacent pages and unresolved
slot usage. The daemon derives the owner locally and the service filters by
owner before paging. Preview context comes from the exact selected generation
in the owner store even when that message is outside the operator overview.
The former implicit single and bulk endpoints no longer schedule retry.

Node UI uses these same operations for an explicit single selection or a
selection from the visible page. The preview with its one-time credential is
a private response. After a lost POST reply, the UI reads the saved operation
at its existing ID. A scheduled receipt confirms local preparation work;
historical admission confirms delivery. A local outbox read uses retained
generation facts and offers checks. The worker establishes live authority and
coverage before allocating the next generation.

When a new receive consent is needed on the existing route, the receiver's
[contact admission](../025-contact-catalog/025-contact-catalog.md#contact-request-admission)
can create a new explicitly actionable request after confirmed consent loss.
The previous decision remains readable. Approving the new request changes
current receive permission and leaves the sender's paused generations in place.

An explicit historical read can check an exact unresolved earlier attempt.
A complete rejection resolves the queried attempt's execution. Only a
rejection of the current generation changes the message's pause and retry
restriction. An exact earlier admission can confirm delivery. View and action
use the same folded execution facts.

The daemon binds both the historical read and
`POST /v1/messaging/outbox/{id}/close-unresolved` to its current operator.
Closure accepts `{"expected/generation": n}` and checks the original generation
and current execution in one write transaction. A repeated closure returns the
existing state. A still-running attempt or a stale generation cannot be closed
by this command. The worker also reports this terminal lifecycle fact to the
host provenance store for operational retention. The stored outcome remains
`closed-unresolved` unless exact
admission confirms delivery. The receipt reason `authority-proof-unavailable`
distinguishes an unavailable verification from a proved denial or missing
consent. None of these refusals allocates a generation.


Single and bulk recovery use the same participant-owned journal. A command
names one to 25 envelope IDs and their expected generations. The operation ID
and the canonical selection bind a replay to its retained decision.

An uncertain preview also binds the prepared recipient route and message
commitment for every item. The credential expires after 300 seconds.
Confirmation checks ownership and the exact selection and consumes the
credential in one transaction. The operation remains readable by its owner
after response loss or restart. Confirmed selections give the worker immutable
input. Worker admission still uses the current authority, consent, execution
and deduplication evidence. Retained receipts from the earlier journal remain
readable until their retention deadline.

The retry decision applies to paused or failed delivery. The initial wait for
contact permission continues the original intent. The owner reloads the
selected generation and folds retained executions when deciding whether to
reserve another generation. Only the current generation's terminal refusal
contributes a retry restriction. A legacy history gap does not resolve execution.

The generation compare-and-set, reservation for preparation, durable work
and per-item receipt share a transaction. Publishing the exact preparation
replaces the reservation with the bytes retained by the owner. A failed write
rolls back the complete reservation; loss of the response leaves a readable
receipt for the original result.
The sender worker takes one confirmed position per tick from the durable
journal. Restart resumes confirmed items with no receipt; previews without
confirmation do not enter the work queue. Receipt reads remain local.

Before allocating an uncertain retry, Messaging asks the local AD owner for
current coverage of each unresolved exact attempt. AD checks the original
sealed pin and the first durable emission debit against the receiver's current
support on WSS. The coverage checks must agree on receiver, contract and store
epoch. Messaging checks the original resume horizon again under the writer and
retains the agreed receiver coverage with the generation reservation.
The exact prepared submission carries the required receiver, contract and
epoch together with the earlier generation and digest pairs. The outbox marks
that it needs the policy, so losing the preparation work cannot publish a plain
retry. The AD owner uses the same binding after restart and rechecks coverage
before every adapter invocation. A changed node, active predecessor or changed
receiver coverage prevents a new emission debit.

After a message execution ends, the sender worker makes one bounded point
read through the same exact AD binding used by explicit reconciliation.
Accepted or AlreadyPresent confirms delivery. A bound terminal refusal
supplies the typed pause. Completion without usable evidence pauses as
unknown and leaves the generation and prepared submission available for
reconciliation. A first contact-request result still follows the contact
permission flow. Legacy state repair must recheck the absence of an exact
positive admission when changing a projection.

### Retention and Failure Boundaries

These are planned Messaging-profile bounds, not a change to every INAC family.
Policy is configuration through existing P091 mechanisms; consumed budgets,
reservations, generations and results are durable facts.

| Data | Required bound |
|---|---|
| Unresolved messages / resume window | 30 days from original message creation. At initial admission each nonterminal outbox row reserves one slot, including a message waiting for a route or contact consent. Defaults are 256 per participant and 1024 per node. Retry/import/restart cannot extend the window. |
| Prepared copies and reservations | At most eight generations, including the first. Defaults are 64 MiB of logical prepared bytes per message and 256 MiB per node. Check the first generation reservation before publishing EML. A later generation replaces the superseded reservation. Publication atomically exchanges the active reservation for the exact byte count. Only nonterminal messages charge this pool. Terminal prepared history follows its own recording and retention holds. |
| INAC results, AD records and generation keys | Through the resume window and at least 31 days after attempt completion. |
| Receiver deduplication | For the message lifetime; after body deletion, a body-free tombstone for at least 31 days after last admission/recognized duplicate, preventing resurrection. |
| Bulk results | At least 31 days after every item has a durable terminal result. |
| Messaging attempt-result capacity | 10,000 attempts and 32 MiB of serialized records, including at most 256 unresolved reservations per peer. Refuse admission when the applicable budget is full. Reads do not extend retention. |

The outbox retains exact prepared bytes for active recovery and unfinished
recording work. Terminal preparations may retire only after the original
resume window and result-retention floor. A receiver tombstone continues to
fence reindex until its body is absent and all associated push holds are
released. Tombstone GC does not delete a mailbox body.

Align startup cleanup and GC with these guarantees; the existing INAC 30-day
cleanup cannot silently erase a required 31-day result. Protect active/unknown
attempts from deletion that could authorize resend. Explicitly closing an unknown
outcome records `closed-unresolved`. Expiry has the same outcome when prior
submission cannot be ruled out. Only an entry proved never submitted becomes
`expired-unsent`. The terminal fact precedes any file cleanup and blocks EML
recovery from restarting delivery. Bound late admission can confirm a closed
outcome. No receiver guarantee
for the relevant window means no uncertain retry. Do not run network acquisition
or signing inside SQLite transactions or assume atomic commit across all stores.

Full outbox capacity refuses new admissions. Accepted rows still record
delivery observations. An exact enqueue replay keeps its original result
at capacity. Retained rows above the limit after migration or a tighter
configuration keep their slots until their normal terminal transition.

The cost is bounded retained state and possible admission refusal under storage
pressure. Unknown results and unavailable proof stay visible rather than becoming
optimistic progress. Exact schema fields, migration handling for legacy attempts
without complete identity, and authenticated support negotiation must be frozen
in S027-009-01; missing legacy evidence cannot be synthesized as authority.

### Bounded Lean Pilot {#lean-delivery-pilot}

**Bounded pilot qualified, 2026-11-16; runtime qualification remains separate.**
The [Node report](https://github.com/diapod/node/blob/master/docs/audits/S027-009-06-LEAN-PILOT-2026-11-16.md)
records checked safety, 57,984 correspondence cases, 33 core tests and the exact
source/tool pins. Owner authentication, storage, push and public readiness remain unverified.
S027-009-06 first qualifies a small executable model of delivery recovery in
Lean. P013 then applies the reviewed method to
[ADC-005/LLR-011 release ordering](../../40-proposals/013-whisper-social-signal-exchange/author-disclosure-conditions.md#lean-release-model).
This sequence limits rework; Messaging does not depend on Whisper. The pilot
does not replace S027-009-01–05 or make formalization of the whole federation a
release prerequisite. Existing runtime work may proceed in parallel.

#### Scope and reuse

Start from the owning contract above and inspect
`node:messaging-core/src/delivery.rs`: `DeliveryFacts`, `DeliveryEvent`,
`DeliveryEffect`, `transition`, `require_retry` and `allowed_actions`. Reuse its
identity, generation, refusal and explicit-recovery vocabulary; do not create a
second production state machine, retry owner or verification carrier. Inventory
the existing transition tests and prepared-attempt/admission fixtures before
adding cases. The specification remains upstream of both implementations: a
disagreement with Rust requires investigation, not copying its behavior into a
weaker theorem.

Model one message, its generations and already authenticated, exactly correlated
observations. Keep message identity distinct from signed-attempt identity and
historical admission distinct from current send permission. Make time/window,
authority, prior execution and receiver-deduplication facts explicit inputs.
State bounds and their correspondence to Rust counters and checked arithmetic;
an unbounded mathematical integer must not silently stand for a bounded counter.
Cryptography, acquisition, storage, UI and network effects remain outside this
first model. In particular, emitting `PrepareNextGeneration` does not itself
prove insert-once admission, a durable reservation or permission at actual push.

#### Required claims

| Claim | Required model property |
|---|---|
| Delivered remains terminal | No admitted event sequence regresses confirmed delivery into a retryable state or emits a new preparation from it. |
| Retry preserves authority | Every preparation requires current sender authority, recipient consent, an open resume window and no running prior attempt. Unknown prior execution additionally requires explicit uncertain-retry confirmation and current receiver deduplication. |
| Unknown is not permission | Missing/unavailable observations alone neither prepare a generation nor count as confirmed consent refusal; local AD absence does not authorize ordinary retry. |
| Generations preserve causal scope | An old refusal cannot pause a newer generation; an exactly correlated older success may confirm delivery. Foreign or future observations cannot be admitted as matching history. |
| Read and command contracts agree | For each offered recovery action, the corresponding command has the same admission predicate under the same facts. The correspondence is explicit for actions outside the pure transition function; no proof of an absent handler is claimed. |

Prove the applicable invariant inductively over reachable states and admissible
histories, rather than only evaluating a finite list of examples. Include legal
positive witnesses: ordinary retry, confirmed uncertain retry and delayed success.
A model that denies every action cannot satisfy the intended contract. This
pilot proves safety properties, not eventual delivery under arbitrary outages.

#### Acceptance and evidence boundary

1. Before proof work, freeze a bounded claim/assumption map linking each claim
   to this contract, its Lean declaration, Rust symbols and existing/new fixtures.
   Review event admission and abstractions independently of the proof script.
   Explicit assumptions may describe trusted inputs or environmental guarantees;
   they must not assume the transition property being proved.
2. Pin Lean and any libraries; compile every claimed theorem without `sorry`,
   `admit` or unchecked custom axioms. Inspect transitive axiom dependencies;
   the pilot accepts only the declared standard logical basis. Native-evaluation
   axioms or other additions to the trusted base require a separate decision.
3. Retain executable positive/refusal vectors and compare the model with the
   pinned Rust core over bounded generated event sequences, including stale and
   future generations, expiry, missing results and all authority combinations.
   Name the corpus and bounds. These comparisons test correspondence; they do
   not prove the Rust implementation refines Lean for every input.
4. Deliberately weaken guards for delivered-state retry, unknown-outcome retry
   and stale refusal. Retain concrete counterexamples or distinguishing executable
   traces; a failed tactic or timeout alone is inconclusive. Reject vacuous or
   unreachable-only claims. Keep these mutations out of the production
   implementation. Reuse existing counterexamples where sufficient.
5. Produce one source-bound report separating checked model claims, assumptions,
   Rust comparison results and untested owner/runtime boundaries. Reuse the
   S027-009 evidence owner and retention conventions. Pin specification/model/
   Rust revisions and toolchain; invalidate correspondence when their relevant
   contracts drift. No inference models, live nodes, browser, network or full
   campaign are required for this offline pilot once its toolchain is provisioned.

The main cost is maintaining correspondence between model and code. Bound the
pilot to these claims; if tooling or representation dominates the work, retain
the findings and request a scoped redesign rather than weaken the claims or
launch an unbounded verification project. Aeneas-based Rust extraction may be
evaluated later; it is not a prerequisite. Storage atomicity, execution-time
authorization, crash/restart, inter-node interoperability and public readiness
still require S027-009's actual-owner tests. No completed baseline is reopened.

The pilot closeout records which laws/fixtures can be reused by P013 and which
must remain Messaging-specific. In particular, every Messaging body push needs
current consent; a previously accepted Whisper disclosure commit has its own
irreversibility contract. No shared proof may erase that difference.

### Implementation Tracker {#consent-loss-recovery-tracker}

The 2026-11-22 exact-history campaign closes S027-009-01–03. The 2026-11-23
[delivery recovery qualification](node:docs/evidence/limited-messaging/2026-11-23-s027-delivery-recovery/README.md)
closes S027-009-04/05. Dependencies below are closure prerequisites.
The pure-kernel freeze required by S027-009-06 is a bounded part of S027-009-01,
and the Lean pilot retains its separate proof scope.
P076-036/037 and S027-008 supply regression baselines. MSG-ONB-009/010
are evidence cases owned by S027-009-04.

P091 resolves the node-local `/messaging/recovery/capacity` setting for new
allocations. The authenticated Messaging module reads the current values via
[the capacity contract](../../../schemas/messaging-recovery-capacity.local.v1.schema.json).
Reduced limits can expose existing usage above capacity. They block further
allocation of that resource and preserve existing reservations, terminal
observations and their original deadlines. Publication spends a previously
reserved charge. Resolution failure preserves access to local history and
reconciliation.

Pre-qualification diagnostics exercised both sovereign cases on Chromium with real
WSS/INAC. The sender recovered consent on the same route through overlapping
single and bulk actions. A lost acknowledgement reconciled without retransmission,
and a separate deadline led to a confirmed retransmission from two tabs. The
recipient reported `AlreadyPresent` with the original mailbox and read state
preserved. The formal campaign below covers the role, failure and limits matrix.
Additional developer runs passed overlapping ordinary bulk and distinct
uncertain confirmations. Delegated child expiry recovered on the original
pairwise route. A later request had reused the prior handled contact decision.
The contact acceptor now opens a distinct explicit approval after confirmed
consent loss. Component tests cover retention of the prior decision, exact
replay and competing successors. The 2026-11-23 delegated browser diagnostic
passed 41 assertions. It paused on child expiry, parent expiry and stale parent
status, obtained new consent on the original pairwise route, and delivered once
after explicit recovery. Revoking the receiving parent rejected a later push.
The default preparation byte pool is tested at exhaustion and after expiry
releases the original unsent reservation.
The ordinary-traffic diagnostic exposed a gap in the AD budget split. A
receiver had committed an admission while the sender's historical read
reported a transport failure. The first support probe had used the historical
operation. Initial and repeat support probes now use the receiver's
support-only budget, preserving a separate budget for exact historical outcomes.
The S027-008 development rerun passed on the same binaries after the fixture
waited for the new daemon runtime at each reload. It checked pending-fact
capacity, idempotent Memarium replay and preservation of paused and terminal
outbox entries.
The mixed sovereign/delegated development scenario also delivered in both
directions through explicit contact and INAC approvals. Its initial consent
flow uses ordinary outbox processing on the original generation.

| Task | Scope / owner | Depends on | Status | Completion gate |
|---|---|---|---|---|
| S027-009-01 | Contracts and pure transition table / Messaging with INAC and AD owners | P032; P060; current P076-036/037 and P097 contracts | done | Inventory reusable seams; freeze both commitments, prepared-attempt binding, peer-scoped read/support contracts, closed reasons/privacy mapping, allowed actions, migration refusals and profile retention. Update canonical schemas, Node mirrors and API registries at implementation time; retain refusal/replay fixtures, including acquisition-disabled versus consent-refused. |
| S027-009-02 | Insert-once admission and immutable attempts / Messaging | S027-009-01 | done | Durable reservations before effects; exact prepared bytes/idempotency across lost submission replies; concurrent first admissions and retries preserve first envelope/path/mailbox/recording/read state. Crash between reservation, Maildir, index and outcome remains reconcilable or explicitly unknown; historical bytes stay unchanged. |
| S027-009-03 | Historical read and typed delivery outcome / INAC and AD | S027-009-02 | done | Required ledger, peer/key/digest binding, bounded body-free reconciliation and authenticated deduplication support. Foreign/absent/mismatched lookups agree; AD preserves refusal/retry fields; local 404 creates zero new generations; failed outcome finalization cannot erase admission. Retain first actual WSS/INAC evidence. |
| S027-009-04 | Explicit single/bulk recovery and UI / Messaging and Node UI | S027-009-03 | done | One durable AD retry budget; distinct confirmed uncertain retry; no duplicate generation from concurrent tabs/bulk; current authority and consent before every push. UI shows stage/reason/observation/actions, keeps composer and owner/CSRF checks. Qualified [MSG-ONB-009/010](../../40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md#recipient-consent-recovery-acceptance) on the same relationship/route. Late failures cannot downgrade delivered. |
| S027-009-05 | Retained qualification and convergence closeout / S027 owner | S027-009-04; S027-008; P076-036/037 regression | done | Separate conformance, host/browser and regression evidence covers retention/startup GC/capacity/tombstones, Memarium outage and restart/replay/reindex, sovereign/delegated/mixed, strict Story-010 and P076-036/037. Clean sources and binaries are pinned. The original verdict is retained and the reviewed qualification agrees before and after retrieval and extraction via `$PRIMARY_EVIDENCE_STORE`. |
| S027-009-06 | Bounded Lean delivery-recovery pilot / Messaging core owner | S027-009-01 pure-kernel contract freeze only; existing Rust transition/fixture baseline | done | Meet the [pilot gate](#lean-delivery-pilot): reviewed claim/assumption map, pinned checked proofs over reachable histories, positive witnesses and guard-mutation controls; bounded differential traces against the existing Rust core; source-bound report separating proof, correspondence tests and runtime obligations. Record reusable laws and intentional domain differences for P013-ADC-011. No full S027-009 runtime, browser or public-release qualification follows. |

The retained 2026-11-23 campaign ran on Node `d6024c1f1` and Orbidocs
`3e9a8e71`. It records 789 component tests, 208 host/browser cases, 34
strict Story-010 phases and 67,845 Lean–Rust comparisons. The synthetic
federation used two browser tabs in one sender session, a separate receiver
session and explicit contact and INAC approval. Evidence correlates message
identity, generation, signed envelope and frozen AD submission digests,
operation receipt, AD ID, outbox, admission and mailbox. A body-free read
caused zero new pushes, generations or acceptor calls. Explicit uncertain
retransmission returned `AlreadyPresent` with the first mailbox content
and flags intact. The 100-message ordinary workload used one participant,
one established route and the native outbox worker with one message in
flight. Clock-driven component tests cover 30/31-day boundary behavior.

The first qualifier conflated a distinct submission with distinct signed
envelope bytes. The original refusal and all original reports remain in
the bundle. The corrected qualifier distinguishes a new authorization from
resubmission of the same signed bytes and qualifies the unchanged runtime
results. Fresh retrieval reproduces that result. Scope flags are
`full_candidate_qualified=false` and `release_ready=false`. The
P076-036 zero-fetch proof concerns local evidence verification. Continued
offline delivery, longer leases, body encryption and a full release
candidate are outside this campaign.

Premerge review found that terminal history still charged the active preparation
pool in the qualified runtime. The reviewed implementation releases live charge
and preparation work at terminal transition and retains the exact confirmation
inputs. Per-owner operation capacity is 1,024 out of 4,096 node-wide. Retry
checks run separately from outbox emission. Three failed checks return
`recovery-check-unavailable` for that position. The 256 MiB default remains
an engineering limit. Sizing under concurrent participants and a sustained
wave of paused messages remains open. The original single-participant
run and three correlated losses do not measure that workload.

Convergence review reused checked capacity arithmetic between P091 and
Messaging, exact submission binding in AD across Messaging and Whisper,
and owner-bound receipt, TTL and budget laws in the tests. Messaging keeps
its durable confirmation beside its generation allocation. Its preparation
history supplies exact original bytes, including extensions. The bounded
owner journal also keeps the authority requirement for each future push.
Whisper's accepted disclosure commit keeps its separate law. The INAC/AD
owners revisit shared ledger policy registration when a second profile
needs historical reads. P091 and Messaging keep their respective budget
units, transaction boundaries and refusal semantics.

Implementation checkpoint (2026-10-28): the first contract fragment adds the
original-JSON message commitment, distinct attempt digest, pure transition/retry
predicate and closed INAC exact-attempt query/result grammar in Node. Canonical
schemas are `inac-admission-status.query.v1`, `inac-admission-status.result.v1`
and `messaging-admission-identity.v1`; their Node mirrors and Schema Gate boundary
fixtures are registered together. A known wire operation is not authenticated
support for the identity profile. Host reconciliation and support negotiation
remain unexposed until the runtime gates below are met. These development checks
do not close any row, change a historical qualification or establish release
readiness. Node's [core contract](node:messaging-core/README.md#delivery-identity-and-recovery)
records repository-local responsibilities without a second tracker.

The subsequent owner-store fragment reserves and freezes exact prepared attempts,
fences first admission and retains an explicit body-free tombstone variant. Local
AD 404 pauses without creating a generation. A separately bound positive observation
checks the persisted attempt key, generation, envelope digest and AD ID before
confirming through that pause; generic refresh remains unable to resume it.
`rejected` requires preserved typed refusal evidence in both schema and Rust.
These focused tests do not yet prove authenticated own/foreign/missing INAC reads,
mandatory transport reservation, retention/deletion writers or browser recovery.
Those five runtime tracker rows were `todo` at this checkpoint. The later
Lean pilot has its own evidence gate.

AD now atomically binds Messaging component/key/input digest to the first resolved
plan, recovering it without another route resolution after a lost reply or restart.
Missing or inconsistent retained bindings fail closed. A separate INAC owner-store
fragment adds body-free peer/key/digest reservations, fenced finalization, bounded
exact reads and protected terminal retention. Component tests exercise actual
SQLite own/foreign/missing queries; they do not qualify authenticated network
reads. The INAC push/query handlers still need these operations installed before
exposure, together with current-permission checks, typed AD outcomes and negotiated
deduplication continuity. No runtime or browser gate is claimed by this checkpoint.

## References

- `doc/project/40-proposals/060-messaging-middleware.md`
- `doc/project/40-proposals/061-contact-attestation-service.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/025-contact-catalog/025-contact-catalog.md`
- `doc/project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md`

### Delegated browser gate implementation (2026-10-18)

P076-032 now has separate `delegated-onboarding` and
`delegated-authority-recovery` scenarios using two ordinary participants outside
root, real native consent/chat forms and the offline browser capsule. The
`p076-browser` candidate and public proof qualifier preserve the historical
HTML receive/INAC and sovereign gates. Short child/parent TTLs, signed status
expiry and competing native retry are required before MSG-ONB-007/008 closure;
no org custody or release readiness is inferred.

The contact rail uses the explicit Local Relationship `view=contact-display`
read: an independent local choice takes precedence over a derived projection for
display, including local blocks. The default membership list remains the raw
projection. Withdrawing a passport cannot hide an explicit address-book choice;
neither view grants receive authority. Per-message host evaluation is unchanged.

### Qualified delegated browser checkpoint (2026-10-18)

P076-032 / MSG-ONB-007/008 is locally qualified:
`node:docs/evidence/limited-messaging/2026-10-18-delegated-browser/README.md`
pins clean sources/binaries, 1308 conformance/capsule executions
(1266 conformance + 42 capsule), 34 strict Story-010 phases and 32/41 actual browser cases. Two ordinary operators outside root use
independent explicit INAC/receive consent and correlated send/open/read. Real
child/parent expiry, locked delegate, restart, stale status and competing retry
recover once only after explicit action; parent withdrawal cascades. Public
proof qualification is identical before/after extraction. The independent
contact-display view confers no receive authority. Org custody, the final mixed
candidate and release readiness remain separate. Historical evidence is unchanged.

### Child-consent UI implementation checkpoint (P076-035, 2026-10-21)

The [P076 child-consent contract](../../40-proposals/076-limited-messaging-grants-decision.md#p076-035-child-consent-ui-implementation-checkpoint-2026-10-21)
was implemented and reviewed before the focused actual-browser measurement.
This historical checkpoint was `in-progress`; the subsequent qualified checkpoint
below closes P076-035 with retained evidence at
`node:docs/evidence/limited-messaging/2026-10-21-child-consent-ui/`. The historical
P076-032 evidence measured whole-grant UI withdrawal and API-only individual
withdrawal. Its date, sources, binaries and scope are preserved.

The UI lists exact locally issued child passports of the participant's own
Node-bound imported grants, with signed public scope and current typed authority
observation. Peer observations are not actionable inventory. The read-only status
projection and host-owned `allowed_actions` do not grant authority; execution
continues to evaluate the current proof. Expiry or a locked delegate does not by
itself prevent an explicit withdrawal.

A participant-session, CSRF-protected confirmed form withdraws only the selected
immutable child. Known withdrawal repetition reuses its durable signed artifact
and identifier, preserving the active parent and siblings. Local refusal applies
before publication. `confirmed` requires an authenticated child acknowledgement;
`covered-by-parent` separately reports an authenticated revoked parent covering
that child. `pending` is not silently converted to success, and an authentic
expired observation can retain a known acknowledgement. The pending browser gate
must measure exact scope/selection, concurrency and lost-response repetition,
sibling preservation and delivery refusal. GET, navigation, import, unlock and
restart cause no implicit retry or sovereign admission. This synthetic-federation
gate requires no model/VM and does not qualify the final mixed candidate or release.

### Qualified child-consent UI checkpoint (P076-035, 2026-10-21)

P076-035 is `done` in its focused scope: normal attempt 09 passes 38/38
actual-browser cases on clean Node `baaef9d8` / Orbidocs `a889d11c`, six unchanged
binaries and the pinned browser.
`node:docs/evidence/limited-messaging/2026-10-21-child-consent-ui/README.md`
retains the signed public proof set and identical loose/extracted `qualified`
results. The Python pack passes 119/119 tests, including 17 actual-proof cases.

Two ordinary participants outside the synthetic root exercise exact rendered
child selection and foreign-target/confirmation/CSRF refusal. Concurrent tabs,
response loss and later explicit replay preserve one immutable signed withdrawal
matching the first accepted directory event. The parent stays active and sibling
public facts stay unchanged. Reverse-direction delivery succeeds; the withdrawn child's later delivery is
refused and accepted-only history remains visible. No model or VM ran.

This is a separate measurement from historical P076-032/007/008, whose individual
withdrawal was API-only. P076-033 and P076-034 remain open; the focused result
reports `full_candidate_qualified=false` and `release_ready=false`.


### Final limited-Messaging qualification (2026-10-24)

P076-034 locally qualifies the complete ten-scenario mixed/provider candidate.
See [the implementation checkpoint](027-messaging-middleware-impl.md#p076-034-local-final-qualification-2026-10-24)
and `node:docs/evidence/limited-messaging/2026-10-24-final-candidate/README.md` for exact sources, binaries, counts, public proofs and provider
substitutions. Historical focused runs keep scope; P076-036 and production/release
readiness remain separate gates.

### P076-036 status observation

The direct receive-consent handoff preserves the complete V2 presentation. Its
optional signed status uses owner-local per-grant disclosure policy, default
omit, and at least a 60-second remaining usable lease at build. The receiver
shares one bounded acquisition/monotonic observation owner with import and
refresh; stale/absent evidence permits exactly one online acquisition attempt.
At the P076-036 checkpoint there was no product NoFetch setting. Actual peer identity, locally admitted root,
current custody and exact consent scope are still required. A status attachment
does not create membership/consent, elevate assurance or resume blocked messages.
The scoped acceptance capsule excludes browser, model, VM and full-candidate
reruns; historical evidence and release readiness retain their separate scope.

The [P076-036 bounded capsule](https://github.com/diapod/node/blob/master/docs/evidence/limited-messaging/2026-10-24-portable-status/README.md)
qualifies the actual cold-cache handoff and zero source acquisitions on clean
Node `9b0a613e` / Orbidocs `8523cf2b`, with 264 conformance/regression and 12
host capsule tests. Signature/correlation qualification matches after extraction.
Its scope, controlled time and live global-retention baseline blocker are explicit;
it does not replace S027 delivery evidence or P076-034's historical candidate.

### P076-037 acquisition and peer renewal

The local P091 `/messaging/issuance/status-acquisition` setting selects `online`,
`scheduled-only` or `no-observed-grant-query` per acquisition. Only S020 can
query observed grants in `scheduled-only`; neither presentation nor S020 can do
so in `no-observed-grant-query`. Local delegates and explicit verified imports
retain their source access. A stale receive-consent send may request one exact
V2 presentation from its authenticated contact and then repeat the pure lookup.
The presenter may fetch its own grant once only in the last mode. The response
needs 15 seconds of usable status, and the contact must have enabled
`full-status`. An unavailable contact keeps the send pending. Signed withdrawal
publication retries independently of S020; pausing status refresh is visible
without invalidating a still-current lease. This is not message delivery offline.
See [P076-037](../../40-proposals/076-limited-messaging-grants-decision.md#p076-037-status-acquisition-policy-and-contact-renewal).

P076-038 separates signed-time verification, owner-local deferred observation,
send retry scheduling and physical transport. A status up to five seconds ahead
of the local clock is retained as negative knowledge but cannot authorize use
until `as_of`; the next local retry rechecks active trust and uses no new fetch.
The v3 readiness/send views expose `status-not-yet-valid` while old v2 views
project it to `revocation-view-stale`. The P074 profile must prove receiver-side
receipt and distinct holder/presenter authority-query counts. See
[P076-038](../../40-proposals/076-limited-messaging-grants-decision.md#p076-038-two-physical-host-consent-renewal-qualification).

The subsequent review adds owner-confirmed disclosure controls on the existing
grant page and bounded actor/time/old/new policy history. Normal windows expose
one latest change per grant; exact-grant windows expose at most 64. Repeated
assignment adds no event, and no action unlocks a delegate, resumes a message or
changes a signed document. Presentation warnings/facts and host-lifetime counters
separate observed, deferred and refused from transport success. Local capacity
uses `issuance-observation-capacity-exhausted` (unknown/503).

The historical retention-header blocker above is repaired in the live checker by
verifying qualifier blobs at the adoption proof's recorded source commit. Prior
proof bytes and source pins remain unchanged. This maintenance has focused local
regressions; it does not rerun the historical full candidate or browser gate.

### P076-038 qualification checkpoint — 2026-10-28

The P076-038 physical gate passed five policy/role windows, exact receiver
observations and eight term/kill role restarts after child/parent withdrawal.
Private holders made zero observed-grant HTTP queries; independent owner/network
witnesses agreed. Runtime and trusted qualifier sources are pinned separately in
P076-038 and `node:docs/audits/ACCEPTANCE-P076-038-2026-10-28.md`. This bounded
qualification does not establish offline message delivery or release readiness.
