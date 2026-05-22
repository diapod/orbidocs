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
> During Solution 032 Phase 2 bridge, messaging continues to write to
> the legacy `contacts_membership` table as compatibility cache and
> continues to emit `contacts.membership-changed.v1` as legacy
> projection. The canonical fact is now
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
queue state, the legacy `contacts_membership` cache (transitional during
Solution 032 Phase 2), and the bounded Layer 3 messaging-fact stream.

After Solution 032 Phase 2 completes, `contacts` membership read/write goes
through the local host capability layer; messaging no longer owns the
relationship concept end-to-end.

## Scope

This solution implements the MVP+ personal messaging path:

- inbound `message-envelope.v1` admission through Artifact Delivery;
- outbound compose, route lookup, contact permission waiting, and private-direct
  delivery through host capabilities;
- the canonical `messaging-receive@v1` passport profile;
- the local contactability draft surface used by Story-010 before Contact
  Catalog publication is fully automated;
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
  contact_nym_id
  purposes
  max_revocation_staleness_seconds
  limits?
```

The messaging acceptor applies three messaging-specific checks after Capability
Binding has verified the passport signature and freshness:

- the sender subject in the envelope must match `sender_subjects`;
- the receiver route must match `recipient_routes` and `contact_nym_id` when
  the envelope carries one;
- the purpose must include `messaging`.

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

## Storage Model

Layer 1 is Maildir. It stores message bodies and serialized accepted envelopes
under the node data directory. Bodies are retained until explicit user/operator
delete or archive.

Layer 2 is SQLite. It stores mailbox indexes, outbound queue state, contacts
membership, pending Layer 3 facts, and recovery replay cursors. It is
rebuildable from Layer 1 plus Layer 3 and vault recovery records.

Layer 3 is Memarium. It receives separate fact schemas, not a generic
`messaging.fact.v1` artifact:

- `contacts.membership-changed.v1`;
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
`pseudonym-vault.v1`; import/root-only startup replay preserves terminal
pairwise mapping states and explicit passphrase replay covers
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
receive-consent state remains the messaging service's `contacts` membership plus
the corresponding `messaging-receive@v1` passport.

`mailbox.open` is a host-owned notification action target. It opens
`/admin/messaging/messages/{message_id}` and may mark the notification handled
or the local read UX state; it does not mutate messaging-domain consent or
delivery state.

## Implementation Tracker

| ID | Feature | Status | Evidence |
|---|---|---|---|
| S027-001 | Canonical `messaging-receive@v1` profile enforcement | done | Node `capability` rejects non-canonical `messaging-receive` profile discriminators and defaults missing `max_revocation_staleness_seconds` to 300 seconds. |
| S027-002 | Messaging service runtime | done | `messaging-service` covers inbound accept, outbox, contact-lookup-result promotion, sender-side lookup against a shared remote Contact Catalog provider, receive-passport handoff, private-direct delivery, Maildir/SQLite storage, temporal outbox transaction/event/attempt tables with `outbox` as the public projection, redacted outbox event snapshots that omit raw recipient handles and subjects, replay-equivalence tests, operator temporal diagnostics endpoints for status/redacted events/correlation/replay-check via daemon proxy, recorded-message lineage enforcement, best-effort Agora Vault storage diagnostics and retryable vault-job replay, kind-specific Layer 3 fact artifacts, pending Memarium replay, recovery mirroring, receiver-side revocation snapshot checks for inline `messaging-receive@v1` passports, fail-closed no-host behavior for passport-based first contact, revocation-triggered `messaging.passport-revoked.v1`, read/unread sync through `messaging.flag.v1`, reindex with remote Memarium replay + local Layer 3 replay + Maildir + FTS5 rebuild, and strict Story-010 cross-node delivery smoke coverage. Mock-host coverage covers inline revocation, outbound passport lookup, signer, `artifact.delivery.send`, `agora.vault.put`, redacted failure classes, and remote replay. |
| S027-003 | Contactability and local contacts | done | Daemon exposes contactability draft/options/attest/publish endpoints, requires contact-control passport evidence at publish time, binds the published owner participant to the draft route or attestation passport subject, signs canonical route-set `contact-claim.v1`, admits it to the supervised Contact Catalog, validates `local-contact.v1` import/export, stores local contact labels/metadata, tracks pairwise mapping lifecycle, and exposes `/v1/local-contacts/resolve`. Local contact and messaging recovery bundles seal into `pseudonym-vault.v1`, replay on import/root-only startup, preserve terminal pairwise mapping states, and explicit operator passphrase replay covers `root+local-passphrase` local-contact recovery snapshots. |
| S027-004 | Contact attestation service dependency | done | Node adds `attestation-core`, supervised opt-in `attestation-service`, contact attestation schemas/examples, schema-gate validators, `email-attestation` / `phone-attestation` capability ids, local/dev delivery, SMTP email delivery, SMS webhook delivery, attempt limits, challenge TTL, quotas, and delivery audit. Daemon contactability options discover trusted/fresh `role/email-attestation` / `role/phone-attestation` providers through Seed Directory, expose provider status in Node UI, and start/redeem challenges through daemon contactability endpoints. Story-010 now uses that runtime path for e-mail-control acquisition. |
| S027-005 | Node UI messaging surface | done | Node UI renders `/admin/messaging` with contactability draft controls, provider challenge/redeem controls, compose, local-contact based unknown-recipient warning, inbox, read/unread actions, outbox, diagnostics, and message detail. |
| S027-006 | Story-010 acceptance pack | done | `node/tools/acceptance/story-010-operator/` provides two-node profile generation, launchers, UI helpers, `story-smoke`, and self-contained `ad-smoke`. Strict `ad-smoke` now defaults to the no-scaffold path: INAC transport is approved through the receiver's operator notification before contact-request AD admission. It also covers Attestation Service challenge/redeem, daemon contactability publish, supervised Contact Catalog admission, shared remote lookup, contact request delivery, operator accept, `messaging-receive@v1` passport handoff, private-direct `message-envelope.v1` delivery, delivered inbox/outbox state, `messaging.flag.v1` read/unread replay, and a second recorded message stored as an encrypted generic artifact in Node B's Agora Vault. The old peer allowlist/preissued transport passport path is retained only as an explicit acceptance debug flag. |

## References

- `doc/project/40-proposals/060-messaging-middleware.md`
- `doc/project/40-proposals/061-contact-attestation-service.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/025-contact-catalog/025-contact-catalog.md`
- `doc/project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md`
