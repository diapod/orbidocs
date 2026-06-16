# Messaging Middleware Implementation Notes

Date: `2026-05-17`

## Runtime Boundaries

`messaging-core` is the pure domain layer. It owns typed envelope validation,
queue-state names, refusal classes, mailbox-resolution DTOs, and
`messaging-receive@v1` scope matching.

`messaging-service` is the supervised middleware. It owns Maildir bodies,
SQLite indexes, outbound queue transitions, pending facts, and service status.
It consumes Local Relationship point capabilities for `contacts` membership
checks/appends; it does not own a canonical contacts table. It calls host
capabilities for authority decisions and side effects outside the messaging
domain.

`daemon` is the host and authority layer. It owns signing, Capability Binding,
revocation view checks, Artifact Delivery, notification dispatch, local
participant-handle evidence, Memarium, and Pseudonym Vault recovery mirroring.

`node-ui` is a thin operator surface. It renders daemon-proxied messaging
state and forwards compose/action requests.

## Disabled-by-Default Service

The bundled messaging service remains disabled by default. Enabling it starts a
loopback supervised HTTP service and injects the standard host capability
environment variables into the child process.

In user-mode desktop profiles, the welcome wizard has a messaging setup step
after participant identity and operator binding. That step may enable the
service, verify the Local Relationship owner/ref and storage readiness, check
the local `messaging-send` readiness gate, issue a missing local
`messaging-send` passport when it is listed by the daemon's local-readiness
requirements, create or reuse a messaging routing-subject, and store either a
`pseudonymous-only` contactability marker or an optional public-handle draft.
The wizard-issued passport uses a bounded bootstrap lifetime and the wizard is
intentionally not an attestation or Contact Catalog publication flow.

## Local Data

The service stores data under its module data directory:

```text
storage/messaging/
  index.sqlite
  maildir/
    <mailbox-id>/{tmp,new,cur}
    outbox/body/{tmp,new,cur}
  projections/maildir-eml/
    .orbiplex-projection
    <mailbox-id>/{tmp,new,cur}
```

Outbound compose writes a native Orbiplex EML profile v1 file under
`maildir/outbox/body/` before queueing the Layer 2 row. SQLite stores the
digest, size, routing metadata, state, host delivery ids, retry diagnostics,
and EML path. The body digest and size remain computed over the EML body
bytes, not over the full RFC 5322 container.

Inbound accepted `message-envelope.v1` artifacts remain canonical signed JSON
under `<mailbox-id>/new/*.json`. The service also writes a regenerable EML
sidecar projection under `projections/maildir-eml/` for MUA/import tooling;
deleting that projection loses no authority state because `reindex` rebuilds
it from the canonical Maildir JSON.

## Contact Conversation Read Model

The Node UI contact chat modal is a read model over existing service surfaces,
not a message store. The backend derives a local contact identity-key set from
handle, routing-subject, contact-nym, participant, and node references already
present on the local contact record. It then lists bounded inbound mailbox rows
and outbound outbox rows, normalizes their asymmetric shapes, filters by exact
canonical route-key intersection, sorts by `(sent/at, envelope/id)`, and
hydrates only the bounded rendered window.

Body hydration uses the local body endpoints for mailbox and outbox rows. Those
endpoints verify size and digest before returning text and never return
filesystem paths. Non-text, oversized, missing, or digest-mismatched bodies are
reported as placeholders or typed error rows in the UI.

The modal is effect-free on read. Mark-as-read is a separate CSRF-protected
command that recomputes the conversation, intersects submitted ids with visible
unread inbound rows, and writes `messaging.flag.v1` facts idempotently. Live
refresh uses id-only `messaging-mailbox-changed` SSE as an invalidation signal
plus notification/polling fallbacks; message content is read only through the
authenticated HTTP surfaces.

The hardening path is now explicit in code: route-key extraction lives in the
pure `local-relationship-core::route_key` module shared by
send/add-contact/history filtering, the chat surface uses the service-side
conversation query instead of UI-side global filtering, the redacted
`trace-delivery --envelope-id` diagnostic correlates outbox, AD,
INAC/passport, and route-key decisions, and authority read paths revalidate
stored passports before treating a cached row as usable.

Accepted contact requests materialize a local-contact projection for UX and
conversation continuity. The `contact-request:<id>` remains source/audit
correlation, not a usable reply handle. The local-contact record uses the
sender reply route when one is disclosed, otherwise the sender subject, and
the chat composer ignores technical `handle/kind = other` values when a real
route is present.

The compose path keeps transport reachability and pairwise relationship identity
separate. A local contact recipient may carry both a transport route, such as
`routing-subject/id`, and an authorization context, such as `contact-nym/id`.
The outbox stores both values as one recipient route context. Artifact Delivery
targets the transport route, while the signed `message-envelope.v1` receiver
route uses the `contact-nym/id` when the resolved `messaging-receive@v1`
passport profile is contact-nym scoped. This is a guardrail against split-brain
contacts: sending to an accepted contact must reuse the pairwise nym established
by contact acceptance instead of silently falling back to a different
source/receiver route.

The sender-local pairwise nym is never a passport lookup requirement for a
transport receiver. For a queued `routing-subject/id`, `node/id`, or
`participant/id` route, the lookup asks for that transport receiver only; a
returned passport may then contribute the receiver-issued `contact-nym/id`.
Only a queued `contact-nym:*` receiver asks lookup to match `contact-nym/id`
directly.

Contact consent remains directional because each side issues its own narrow
`messaging-receive@v1` passport. For usability, a reciprocal
`contact-request.v1` from a sender that already matches an active local
contact may be auto-accepted by the daemon. Auto-accept still uses the normal
acceptance path: it materializes the local contact projection, writes the
Local Relationship membership and pairwise nym binding, signs a scoped
`messaging-receive@v1` passport, and hands the passport back to the source
peer. It skips only the redundant operator notification.

When a contact request is accepted, the daemon first tries to match the request
against existing active local contacts through the shared canonical
`route_key` set. A match updates that contact in place with the pairwise
`contact-nym` and any missing remote subject data instead of creating a second
route-only contact. This keeps the user-visible contact, conversation history,
and passport authorization context aligned.

The sender-side outbox MUST NOT treat a completed Artifact Delivery transport
record for `contact-request.v1` as proof that contact permission exists. The
proof is the later `messaging-receive@v1` passport lookup. If that passport
does not appear after the contact-request delivery marker becomes stale, the
outbox reissues the same logical contact request instead of waiting forever.

## MUA Profile

Operators may inspect local message history with a standard MUA through the
Orbiplex EML profile. Point the MUA at the disposable
`storage/messaging/projections/maildir-eml/` tree for inbound mailboxes and at
`storage/messaging/maildir/outbox/body/` for outbox body records. The inbound
projection may be deleted and rebuilt by `reindex`; the canonical inbound
authority is still the signed JSON Maildir under `storage/messaging/maildir`.
Outbox `.eml` files are durable local records and carry enough
`X-Orbiplex-*` headers to reconstruct outbox rows when SQLite is absent.
Reindex reports `outbox/recovered` ids and `outbox/errors` per-file failures;
malformed outbox EML does not abort the whole rebuild. A recovered outbox file
with no recipient route and no recipient handle is fail-closed as
`failed-terminal` with `last_error = "recovered without addressing"`.

## Outbound Processor

`POST /v1/messaging/outbox/process` runs a bounded deterministic batch. The
daemon may call the same endpoint from a small service loop. The endpoint is
idempotent: it advances only rows whose state and retry time allow progress.

Host capability failures are classified as retryable unless the host returns a
schema, conflict, or scope refusal. Retryable rows keep `last_error` and
`next_attempt_at`.

## Inbound Policy

Inbound admission validates `message-envelope.v1`, validates any inline passport
against the message, verifies `passport-ref` through `capability.passport.lookup`
when host capabilities are configured, asks the daemon to resolve the local
mailbox, and then applies the `contacts` policy gate. A first valid receive
passport tied to an accepted contact request may project membership. Otherwise a
missing active membership is refused as `contacts-policy-denied`.

The refusal response is intentionally generic. It must not reveal whether a
public handle exists locally or which participant owns it.

Current receiver-side revocation coverage is fail-closed for `passport-ref`
admission through `capability.passport.lookup`, which uses the daemon
revocation view and a 300 second freshness budget. Inline presented passports
are scope-checked at the messaging boundary; full inline revocation verification
requires a host verifier that can evaluate the presented passport against the
revocation view without requiring it to exist in the local passport cache.

## Facts and Recovery

Layer 3 fact writes go through `memarium.write`. On failure, the fact is stored
in `pending_facts` and service status becomes `degraded`. Replay is explicit and
idempotent through `POST /v1/messaging/pending-facts/replay`.

Recovery mirroring is host-owned. The service requests
`identity.messaging-recovery.mirror` for membership and receive-passport
reference records. The daemon persists those records in a durable local
recovery mirror table and seals/replays local recovery bundles through
`pseudonym-vault.v1`. Operational-vault-key startup replay is the normal
unattended path; root-only remains recovery/migration-only, and
`root+local-passphrase` replay requires explicit operator passphrase input. The
messaging service can accept replayed records through its recovery endpoint or
startup replay path.

## Verification

The MVP+ acceptance set is:

- schema-gate validates message envelopes, fact schemas, and host capability
  DTOs;
- service tests cover inbound idempotency, outbox processing, pending facts,
  and reindex;
- daemon tests cover passport lookup, participant handle ownership,
  mailbox-resolution fallback, and `mailbox.open`;
- UI smoke loads `/admin/messaging`, queues compose, lists inbox/outbox, and
  opens a message detail through a notification action.

Additional hardening now covered by focused tests:

- `capability` rejects alternate `messaging-receive` passport profile shapes
  and defaults missing receive-profile revocation freshness to 300 seconds;
- `messaging-service` promotes valid `contact-lookup-result.v1` route
  candidates and terminally fails `no-match` results;
- daemon proxying includes the outbox contact-lookup-result promotion endpoint;
- `messaging-service` checks receiver-side revocation snapshots for inline
  `messaging-receive@v1` passports before Maildir/SQLite persistence;
- `messaging-service` reindex attempts remote Memarium replay before local
  Layer 3 projection replay, Maildir walk, and FTS5 rebuild, with degraded
  diagnostics when Memarium is unavailable;
- the daemon local contact store can export/replay local contact, pairwise
  mapping, and messaging recovery mirror records without reactivating revoked
  or archived pairwise mappings;
- `schema-gate` validates `local-contact.v1`,
  `contact-attestation-request.v1`, and `contact-attestation-result.v1` at the
  intended local import/export and ingress/egress boundaries;
- Story-010 has a two-node profile and launcher scaffold under
  `node/tools/acceptance/story-010-operator/`; strict `ad-smoke` now covers
  Seed Directory discovery of attestation providers, attestation,
  contactability publish, shared Contact Catalog lookup, receiver-side INAC
  transport invitation approval through operator notifications, contact
  request acceptance, `messaging-receive@v1` passport handoff, private-direct
  message delivery, and delivered inbox/outbox state. The preauthorized
  peer-allowlist scaffold remains available only through an explicit acceptance
  debug flag.
- Node UI user-mode wizard tests cover the new messaging setup step selection
  and pseudonymous-only contactability marker parsing; daemon tests cover saving
  a pseudonymous-only contactability draft with no public handle and a messaging
  routing subject.
