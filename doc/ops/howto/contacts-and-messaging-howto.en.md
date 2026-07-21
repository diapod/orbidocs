# Contacts and Messaging HOWTO

This document follows the complete path from contact-channel attestation, through
route publication and relationship acceptance, to private message delivery. The
conceptual answers and responsibility boundaries are in the
[Contacts and Messaging FAQ](../faq/contacts-and-messaging-faq.en.md).

## Separate the sources of truth

| Layer | Responsibility | Not authoritative for |
|---|---|---|
| Contact Attestation | control of an email address or phone at a particular time | civil identity and relationships |
| Contact Catalog | attested claims and lookup-safe invitation routes | the local address book |
| Local contacts | labels and an owner-scoped UX projection | capability authority |
| Local Relationship Layer | owner classes, memberships, predicates, and groups | transport and passports |
| Pseudonym Vault | routing subject, pairwise nym, and recovery material | a public directory of people |
| Messaging | outbox, inbox, content, flags, and temporal delivery trail | provider discovery |
| AD + INAC | private artifact transport and admission | relationship consent |

## Check configuration and readiness

Run daemon `check-config` first, then inspect each layer separately:

```http
GET /v1/contact-catalog/status
GET /v1/messaging/status
GET /v1/local-relationships/status
GET /v1/messaging/contactability/options
```

One component reporting `ready` does not imply readiness of the whole path.
Contactability options should expose a local participant and a discovered, trusted,
fresh attestation provider. Remote contact additionally needs a working AD/INAC path.

## Prepare a participant and routing subject

Contactability is published for a particular local participant, but the catalog must
not expose that participant's root identity. Create or import the participant, unlock
their signing key, and create a separate routing subject. Preserve this separation:

```text
participant/id       -> local authority and signature
routing-subject/id   -> public invitation route
pairwise nym         -> relationship after contact-request acceptance
```

## Save a contactability draft

The draft declares handles and the route purpose. It does not publish a claim yet:

```http
POST /v1/messaging/contactability/draft
Content-Type: application/json
```

```json
{
  "handles": [
    {"handle/kind": "email", "handle/value": "marcin@example.org"}
  ],
  "routes": [
    {"participant/id": "participant:LOCAL", "purpose": "messaging"}
  ]
}
```

The handle value is transient operator input. The durable catalog index should be
lookup-safe; do not copy a raw email address into public diagnostics or audit.

## Obtain contact attestation

Start a challenge through the daemon bridge, then redeem it using the provider's
delivery adapter:

```http
POST /v1/messaging/contactability/attestation/challenges
POST /v1/messaging/contactability/attestation/challenges/{challenge_id}/redeem
```

The `contact-attestation-request.v1` request specifies `contact/kind`,
`contact/value`, subject, requested profile, and validity period. The result is a
channel-control passport. Story-010 profiles may use an explicit development
`always_accept` shortcut; never carry that setting into a production profile.

## Bind the attestation and publish a claim

Bind the passport to the draft handle first, then publish the signed claim:

```http
POST /v1/messaging/contactability/attest
POST /v1/messaging/contactability/publish
```

```json
{
  "handle/kind": "email",
  "handle/value": "marcin@example.org",
  "passport": {"schema": "capability-passport.v1"}
}
```

The `passport` value above abbreviates the complete passport returned by `redeem`;
the shown object is not a valid standalone passport.

Publication passes through the supervised Contact Catalog. A claim with invalid
attestation, an expired passport, or a mismatched subject should be refused.

## Verify lookup without disclosing identity

The Contact Catalog provider accepts `POST /v1/contact-catalog/lookups`. A production
client should use a provider discovered through Seed Directory rather than a hard-coded
endpoint. The minimum request semantics are:

```json
{
  "schema": "contact-lookup-request.local.v1",
  "contact_index_value": "sha256:LOOKUP_SAFE_VALUE",
  "purpose": "messaging",
  "lookup_mode": "invitation-only"
}
```

The expected `contact-lookup-result.v1` has `match/class = invitation-available` and
`result/routes`. It must not contain the root `participant/id` or raw handle.

## Send the first message

The sender may provide an external handle. Messaging records the message in its outbox,
but does not send content to an unknown recipient before completing the contact request:

```http
POST /v1/messaging/outbound
Content-Type: application/json
```

```json
{
  "recipient/handle": {"kind": "email", "value": "marcin@example.org"},
  "subject": "Contact attempt",
  "body": "Hello, can we talk?",
  "content-type": "text/plain"
}
```

Run the queue processor:

```http
POST /v1/messaging/outbox/process

{"batch/limit": 10}
```

## Handle transport consent and the contact request

If the nodes do not yet have a transport relationship, the recipient sees an
`inac/invitation-request` notification. Accept it and process the sender outbox again.
A separate `contact-request/received` notification then appears:

```http
GET /v1/operator/notifications?limit=50
POST /v1/operator/notifications/{notification_id}/actions/accept

{"version": 1}
```

Use the version returned by that notification; `1` is not a constant. Contact-request
acceptance creates or updates the local contact, `contacts` membership, pairwise
mapping, and narrow receive passport. Process the sender outbox again after the
decision.

## Inspect the outbox, inbox, and body

The read surfaces are deliberately separated:

```http
GET /v1/messaging/outbox
GET /v1/messaging/outbox/{envelope_id}/body
GET /v1/messaging/mailboxes
GET /v1/messaging/mailboxes/{mailbox_id}/messages
GET /v1/messaging/mailboxes/{mailbox_id}/messages/{envelope_id}/body
GET /v1/messaging/messages/{message_id}
```

Body endpoints are separate bounded surfaces. A message list must not accidentally
carry full content or diagnostic secrets.

## Change flags as facts

Write read/unread and related flags through the message flag endpoint. The runtime
records `messaging.flag.v1`, and the read model derives current state:

```http
POST /v1/messaging/messages/{message_id}/flags
```

Do not edit SQLite or Maildir files manually. When a projection needs rebuilding, use
`POST /v1/messaging/reindex`; for pending facts use
`POST /v1/messaging/pending-facts/replay`.

## Classify contacts without granting authority

LRL can append a membership and resolve a group:

```http
POST /v1/local-relationships/memberships
POST /v1/local-relationships/group.resolve
```

```json
{
  "owner/ref": "participant:LOCAL",
  "contact/ref": "contact:EXAMPLE",
  "class/id": "friends",
  "status": "active",
  "actor/ref": "participant:LOCAL",
  "reason/code": "operator-classification"
}
```

Group resolution is owner-scoped and respects blocks. Its result is a routing
candidate set, not a passport and not consent to broadcast.

## Withdraw a contact or capability

When a relationship ends, perform the relevant operations explicitly: change or
delete the local contact, set LRL membership to `blocked` or inactive, and revoke the
receive passport. Then inspect the revocation view and rerun reindex if the operator
repaired a projection. Do not delete historical facts merely to "clean" the view.

## Run Story-010

From the `node/` workspace, prepare profiles and run the complete self-contained smoke:

```sh
python3 tools/acceptance/story-010-operator/story-010-local-profiles.py init
python3 tools/acceptance/story-010-operator/story-010-local-profiles.py \
  ad-smoke --strict
```

Run the LRL gate with:

```sh
python3 tools/acceptance/story-010-operator/story-010-relationship-acceptance.py
```

The acceptance uses two node profiles on one host. It verifies contracts, restarts,
provider discovery, private delivery, and owner scope, but does not replace a public
network test or a production OTP delivery adapter.

## Diagnose the boundary that refused the operation

| Symptom | Check first |
|---|---|
| no attestation provider | Seed Directory trust, freshness, and capability profile |
| claim publication refused | passport, subject, expiry, and claim signature |
| lookup returns `no-match` | lookup-safe canonicalization, purpose, and active claim state |
| outbox waits for permission | INAC notification, contact request, and retry schedule |
| contact exists but message is refused | `contacts` membership, receive passport, and revocation view |
| inbox has a record without body | bounded body surface, Maildir, and projection diagnostics |
| group differs between operators | `owner/ref`, membership status, and local predicates |

Repair the lowest unsatisfied boundary. Manually inserting records into a later layer
hides the cause and creates state that cannot be reproduced.

## Source documents

- [Solution 025: Contact Catalog](../../project/60-solutions/025-contact-catalog/025-contact-catalog.md)
- [Solution 026: Pseudonym Vault and Key Roles](../../project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md)
- [Solution 027: Messaging Middleware](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md)
- [Solution 032: Local Relationship Layer](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)
- [Story-010](../../project/30-stories/story-010-message-to-a-friend.md)
