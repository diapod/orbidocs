# Messaging Middleware

`Messaging Middleware` is the node-attached application messaging component
that turns Proposal 060 into runtime responsibilities for personal message
admission, outbound contact permission, mailbox indexing, and recovery metadata.

Status: `hard-mvp-done`

Date: `2026-05-17`

## Executive Summary

> **Cross-reference to Solution 032 (Local Relationship Layer):** With
> Solution 032, the **canonical owner of the `contacts` concept**
> (relationship classes, membership facts, pairwise nym continuity)
> moves out of this solution. Messaging becomes a *consumer* of the
> Local Relationship Layer: it reads active `contacts` class membership
> for receive consent, triggers membership append through the local
> host capability `local-relationship.membership.append` on
> `contact-request.accept`, and emits `messaging-receive@v1` based on
> relationship state.
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

The passport may be presented inline or by reference, but the service never
owns private keys and never mints the passport directly.

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
   usable `messaging-receive` passport.
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

Node UI owns `/admin/messaging`. It renders status, contactability draft
settings, provider challenge/redeem controls, compose, inbox, mailbox lists,
read/unread controls, outbox, message detail, pending-facts diagnostics, and
recovery/reindex actions by calling `/v1/messaging/*` daemon proxies. It does
not duplicate messaging policy logic.

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
| S027-005 | Node UI messaging surface | done | Node UI renders `/admin/messaging` with contactability draft controls, provider challenge/redeem controls, compose, local-contact based unknown-recipient warning, inbox, read/unread actions, outbox, diagnostics, and message detail. User UI also renders a contact chat modal as a bounded read-model over the messaging-service mailbox/outbox stores: it hydrates text bodies through bounded body endpoints, merges inbound and outbound rows by normalized contact route keys, refreshes history through `messaging-mailbox-changed` SSE plus polling fallback, and marks rendered unread inbound rows through an explicit mailbox-scoped flag mutation. |
| S027-006 | Story-010 acceptance pack | done | `node/tools/acceptance/story-010-operator/` provides two-node profile generation, launchers, UI helpers, `story-smoke`, and self-contained `ad-smoke`. Strict `ad-smoke` now defaults to the no-scaffold path: INAC transport is approved through the receiver's operator notification before contact-request AD admission. It also covers local `always_accept` Attestation Service acquisition through daemon contactability endpoints, daemon contactability publish, supervised Contact Catalog admission, shared remote lookup, contact request delivery, operator accept, `messaging-receive@v1` passport handoff, private-direct `message-envelope.v1` delivery, delivered inbox/outbox state, `messaging.flag.v1` read/unread replay, and a second recorded message stored as an encrypted generic artifact in Node B's Agora Vault. The old peer allowlist/preissued transport passport path is retained only as an explicit acceptance debug flag. |
| S027-007 | User-mode messaging readiness wizard | done | Node UI adds a third welcome step after participant identity and operator binding. The step can enable `messaging-service`, checks Local Relationship owner/storage readiness and `messaging-send` readiness, creates/reuses a Pseudonym Vault routing subject, and saves either explicit `pseudonymous-only` contactability or a `public-handle-draft`. It does not mint a global messaging nym; pairwise contact nyms remain acceptance-time relationship facts. |

## References

- `doc/project/40-proposals/060-messaging-middleware.md`
- `doc/project/40-proposals/061-contact-attestation-service.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/025-contact-catalog/025-contact-catalog.md`
- `doc/project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md`
