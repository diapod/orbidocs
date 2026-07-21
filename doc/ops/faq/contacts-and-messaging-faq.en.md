# Contacts and Messaging FAQ

## Where does a user keep their address book?

The address book is a local, owner-scoped node read model. `local-contact.v1`
records keep labels and metadata needed by the UI, while canonical consent to receive
messages follows from active membership in the `contacts` relationship class. Contact
Catalog does not replace this layer.

The practical path from contactability publication to a local contact is described in
the [Contacts and Messaging HOWTO](../howto/contacts-and-messaging-howto.en.md).

## How does Contact Catalog differ from local contacts?

Contact Catalog answers: "does an attested invitation route exist for this lookup-safe
index?" A local contact instead answers: "how does this node owner classify this
relationship, and have they consented to receive messages through it?" The first layer
supports discovery; the second supports local policy and UX.

The catalog must not disclose a raw email address, phone number, or root
`participant/id`. A lookup result carries an invitation route, not a global directory
of people.

## What does contact attestation prove?

`email-control@v1` or `phone-control@v1` proves that a subject controlled the given
channel during the attestation procedure. It does not prove a legal name, civil
identity, or indefinite future control of the channel. Attestation can therefore open
contactability and anti-spam gates, but not high-trust roles.

## Why does a published route not point directly to a participant?

A public catalog result leads to a `routing-subject/id` or another bounded routable
target. Pseudonym Vault then binds local and pairwise nyms to the route needed by a
particular relationship. A public handle consequently does not become a universal
identifier correlating all participant activity.

## Why does the first message start with a contact request?

An unknown sender does not immediately receive authority to send content. Messaging
first resolves the handle through Contact Catalog and delivers `contact-request.v1`.
Only the recipient's decision creates the local `contacts` relationship, pairwise
mapping, and narrow `messaging-receive@v1` passport. Refusal is not a transport error;
it is a valid recipient-policy outcome.

## Why can the operator see two consent questions?

The first question can concern admitting the remote node through INAC for a particular
artifact class. The second concerns the user's contact request itself. These are
different exercises of authority: transport authorization does not create a
relationship, and a relationship must not silently open arbitrary transport.

## Does a relationship class grant a capability?

No. `contacts`, `friends`, or another LRL class is a local policy input and group
selector. Assigning a class does not issue a passport or bypass host authorization.
A capability exists only through an explicit issuance mechanism and remains bounded by
profile, subject, route, time, and revocation view.

## Where is a message stored?

Messaging maintains a durable outbox and inbox, a conversation index, and a temporal
trail of attempts and state changes. Native outbound bodies are stored as EML, while
canonical inbound records use JSON Maildir with a reproducible EML projection.
`messaging.flag.v1` records read/unread state as facts instead of silently overwriting
the view.

## Does message content enter Contact Catalog or Seed Directory?

No. The catalog and Seed Directory discover trusted providers and routes; they do not
store message content. The message itself travels privately through Artifact Delivery
and INAC. Public or retained copies require a separate explicit contract, such as a
recorded-message policy and Agora Vault.

## How is a relationship blocked or revoked?

The operator or owner changes the LRL membership state, revokes the relevant passport,
and updates the local contact. Each operation has a distinct effect: LRL changes local
selection, revocation stops authority, and the contact record updates UX. One hidden
`blocked` field must not replace these three explicit changes.

## Does Messaging support groups?

LRL can deterministically resolve a class such as `friends` into an owner-scoped local
candidate list. This is a usable selection primitive, but not a complete multi-party
conversation protocol. Persistent group communication and shared history belong to
Room/Corpus, not to a simulated loop of private messages.

## What is the shortest end-to-end test?

Story-010 starts two local nodes, Seed Directory, Attestation Service, Contact Catalog,
and two Messaging services. It publishes attested contactability, performs lookup,
handles INAC consent, accepts a contact request, and verifies private delivery plus
inbox/outbox state. It is a multi-node single-host acceptance, not evidence of public
Internet reachability.

