# Messaging Middleware

`Messaging Middleware` is the node-attached application messaging component
that turns Proposal 060 into runtime responsibilities for personal message
admission, outbound contact permission, mailbox indexing, and recovery metadata.

Status: `hard-mvp-done`

Date: `2026-05-17`

Updated: `2026-10-16` — bounded fact recovery and scoped mailbox reconstruction.

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

| ID | Feature | Status | Evidence |
|---|---|---|---|
| S027-001 | Canonical `messaging-receive@v1` profile enforcement | done | Node `capability` rejects non-canonical `messaging-receive` profile discriminators, defaults missing `max_revocation_staleness_seconds` to 300 seconds, accepts route-only profiles without `contact_nym_id`, and rejects malformed `contact_nym_id` values that do not use the `contact-nym:*` namespace. |
| S027-002 | Messaging service runtime | done | `messaging-service` covers inbound accept, outbox, contact-lookup-result promotion, sender-side lookup against a shared remote Contact Catalog provider, receive-passport handoff, private-direct delivery, native EML outbox body storage, canonical inbound JSON Maildir storage with disposable EML sidecar projection, SQLite storage, bounded body-read endpoints for inbound mailbox rows and outbound outbox rows, temporal outbox transaction/event/attempt tables with `outbox` as the public projection, redacted outbox event snapshots that omit raw recipient handles and subjects, replay-equivalence tests, operator temporal diagnostics endpoints for status/redacted events/correlation/replay-check via daemon proxy, recorded-message lineage enforcement, best-effort Agora Vault storage diagnostics and retryable vault-job replay, kind-specific Layer 3 fact artifacts, pending Memarium replay, recovery mirroring, receiver-side revocation snapshot checks for inline `messaging-receive@v1` passports, fail-closed no-host behavior for passport-based first contact, revocation-triggered `messaging.passport-revoked.v1`, read/unread sync through `messaging.flag.v1`, reindex with remote Memarium replay + local Layer 3 replay + native EML outbox recovery + canonical inbound Maildir JSON + disposable EML sidecar rebuild + FTS5 rebuild, and strict Story-010 cross-node delivery smoke coverage. Mock-host coverage covers inline revocation, outbound passport lookup, signer, `artifact.delivery.send`, `agora.vault.put`, redacted failure classes, and remote replay. |
| S027-003 | Contactability and local contacts | done | Daemon exposes contactability draft/options/attest/publish endpoints, requires contact-control passport evidence at publish time, binds the published owner participant to the draft route or attestation passport subject, signs canonical route-set `contact-claim.v1`, admits it to the supervised Contact Catalog, validates `local-contact.v1` import/export, stores local contact labels/metadata, tracks pairwise mapping lifecycle, and exposes `/v1/local-contacts/resolve`. Local contact and messaging recovery bundles seal into `pseudonym-vault.v1`, replay on import and operational-vault-key startup, preserve terminal pairwise mapping states, treat root-only as recovery/migration-only, and explicit operator passphrase replay covers `root+local-passphrase` local-contact recovery snapshots. |
| S027-004 | Contact attestation service dependency | done | Node adds `attestation-core`, supervised opt-in `attestation-service`, contact attestation schemas/examples, schema-gate validators, `email-attestation` / `phone-attestation` capability ids, local/dev delivery, SMTP email delivery, SMS webhook delivery, attempt limits, challenge TTL, quotas, delivery audit, and a default-disabled `always_accept` provider policy for local acceptance profiles. Daemon contactability options discover trusted/fresh `role/email-attestation` / `role/phone-attestation` providers through Seed Directory, expose provider status in Node UI, start challenges through daemon contactability endpoints, import immediate `always_accept` passport results when returned, and retain challenge redeem for non-local profiles. Story-010 now uses that runtime path for e-mail-control acquisition without manual OTP handling in local profiles. |
| S027-005 | Node UI messaging surface | done | Node UI renders `/admin/messaging` with contactability draft controls, provider challenge/redeem controls, compose, local-contact based unknown-recipient warning, inbox, read/unread actions, outbox, diagnostics, and message detail. User UI also renders a contact chat modal as a bounded read-model over the messaging-service mailbox/outbox stores: it hydrates text bodies through bounded body endpoints, merges inbound and outbound rows through the shared `local-relationship-core::route_key` canonicalizer, refreshes history through `messaging-mailbox-changed` SSE plus polling fallback, and marks rendered unread inbound rows through an explicit mailbox-scoped flag mutation. Relationship/conversation subject precedence is separated from delivery-route precedence so `participant/id` is not hidden by a transport route, and active local-contact route-key matching preserves schema-safe pairwise contact nyms while excluding blocked contacts. |
| S027-006 | Story-010 acceptance pack | done | `node/tools/acceptance/story-010-operator/` provides two-node profile generation, launchers, UI helpers, `story-smoke`, and self-contained `ad-smoke`. Strict `ad-smoke` now defaults to the no-scaffold path: `contact-request.v1` is admitted through the schema-scoped INAC preflight/policy gate, then the receiver sees the contact-request notification and explicitly accepts the relationship before any `message-envelope.v1` delivery authority exists. It also covers local `always_accept` Attestation Service acquisition through daemon contactability endpoints, daemon contactability publish, supervised Contact Catalog admission, shared remote lookup, contact request delivery, operator accept, `messaging-receive@v1` passport handoff, private-direct `message-envelope.v1` delivery, delivered inbox/outbox state, `messaging.flag.v1` read/unread replay, and a second recorded message stored as an encrypted generic artifact in Node B's Agora Vault. The old peer allowlist/preissued transport passport path and explicit INAC operator-approval path are retained only as acceptance debug/policy variants. |
| S027-007 | User-mode messaging readiness wizard | done | Node UI has five welcome steps: participant identity, key unlock phrase, operator binding, Messaging issuance authority (sovereign or bounded grant) and Messaging. The latter two can be durably deferred to enter `/app` with visible status. The step can enable `messaging-service`, checks Local Relationship owner/storage readiness and `messaging-send` readiness, creates/reuses a Pseudonym Vault routing subject, and saves either explicit `pseudonymous-only` contactability or a `public-handle-draft`. It does not mint a global messaging nym; pairwise contact nyms remain acceptance-time relationship facts. |

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
