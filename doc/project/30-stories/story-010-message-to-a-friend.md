# Story 010: Message to a Friend

## Summary

As a recent Orbiplex user, Daniel wants to send a private message to Marcin by
typing the email address he already knows: `marcin@example.org`.

Marcin does not want to create a full friend-to-friend relationship with every
person who may contact him. Instead, he has opted into a narrower messaging
path: his node publishes contactability claims to a Contact Catalog, receives
control attestations for the public handles he lists, and later grants Daniel a
messaging-specific passport after reviewing Daniel's contact request.

The result is a layered flow:

```text
known email address
  -> contact catalog lookup
  -> route candidate
  -> contact request over AD/INAC
  -> local consent on Marcin's node
  -> messaging passport
  -> queued outbound message delivery
```

The email address is a bootstrap handle, not the durable authority. Durable
authorization is carried by a signed passport and checked by Marcin's node
before the message reaches the messaging middleware.

## Current Baseline Used by This Story

This story is grounded in:

- **Proposal 058** (Contact Catalog and Private Contact Discovery), especially
  the separation between Seed Directory infrastructure discovery and Contact
  Catalog contact-route discovery;
- **Proposal 024** (Capability Passports and Network Ledger Delegation) for the
  reusable `capability-passport.v1` artifact;
- **Proposal 025** (Seed Directory as Capability Catalog) for discovering
  catalog providers and other capability-backed infrastructure;
- **Proposal 042** and **Solution 017** (Inter-Node Artifact Channel) for direct
  node-to-node artifact exchange;
- **Solution 023** (Artifact Delivery) for host-owned delivery, recipient
  resolution, and inbound admission dispatch;
- **Proposal 057** (User and Operator Notifications) for turning contact
  requests into durable, actionable UI notifications.

The story also reuses these existing mechanism documents:

- **Solution 006** (Orbiplex Capability Binding) for passport-aware
  authorization, revocation freshness, and auditable host-side decisions;
- **Solution 007** (Capability Advertisement) and the Capability Registry for
  advertising that a node currently accepts a protocol or application
  capability such as a future messaging receive surface;
- **Proposal 032** and **Solution 014** (Key Delegation Passports) for
  `key-delegation.v1`, inline `DelegationProof`, `PassportCache`, and
  `DelegationCache`;
- **Proposal 056** and **Solution 024** (TLS Trust Policy) for endpoint
  certificate evidence and peer-dial enforcement before private/direct
  delivery;
- **Proposal 059** (Participant, Nym, and Routing-Subject Key-Role
  Derivation) plus `pseudonym-vault.v1` and `routing-subject-binding.v1` for
  participant-backed nym continuity, routing subjects, and private vault
  recovery;
- **Proposal 036** and **Solution 002** (Memarium) for local semantic/audit
  facts, with **Proposal 047** (Classification Label Propagation) for
  classification facts that touch Memarium-managed state;
- **Solution 019** (Middleware) for supervised middleware attachment patterns
  and host-owned component boundaries used by a future messaging acceptor.

MVP contract note: Proposal 058 now freezes the concrete messaging authorization
capability id as `messaging-receive`, expressed through
`capability-passport.v1`. The first profile is intentionally narrow: it grants
one accepted sender subject authority to deliver messages to one accepted route.

## Cast and Scene

- **Marcin**, long-time Orbiplex user, runs a node on a GNU/Linux PC.
- **Daniel**, recent Orbiplex user, has a node and a messaging middleware
  client.
- **Seed Directory**, used to discover infrastructure capabilities and to issue
  or broker selected contact-control attestations.
- **Contact Catalog**, a domain catalog that accepts opt-in contact claims and
  returns route candidates rather than raw identity records.
- **Messaging middleware**, a node-attached component that owns message compose,
  outbound queues, inbound message storage, and mailbox UI integration.

Marcin can expose himself to communication in two broad ways:

1. establish a friend-to-friend relationship with another node; local policy may
   then allow all participants or nyms in the `friends` relationship class to
   use selected communication capabilities, such as messaging or bounded backup
   space;
2. avoid a general friend relationship and add the accepted sender to the
   dedicated `contacts` relationship class, whose default local policy is
   exactly "may send messages to me"; the binding is preferably done in a way
   that survives nym regeneration without forcing the user to repeat the whole
   ceremony.

This story uses the second path. Daniel is not made a general F2F friend of
Marcin's node. He is added to Marcin's `contacts` and receives only the
authority needed to send messages under Marcin's local messaging policy.

`contacts` is intentionally narrower than `friends`: where `friends` may
unlock several capabilities at once (messaging, bounded backup space, shared
spaces), `contacts` defaults to inbound messaging only. Local policy may
further refine what a `contacts` member is allowed to do, but adding a sender
to `contacts` should never silently grant friend-class capabilities.

## Sequence of Steps

### Step 1: Marcin Opens a Public Contact Path

Marcin decides that people should be able to reach him through Orbiplex even if
they only know his ordinary contact handles.

In the Node UI, he opens the contactability settings for the messaging
middleware and enters:

- one or more email addresses, including `marcin@example.org`;
- his phone number;
- the Orbiplex identities that may be contacted through these handles, such as
  a participant id, one or more messaging nyms, or a routing subject delegated
  for contact.

The UI explains the operational distinction:

- a contact handle proves reachability or control of an external channel;
- it is not a durable Orbiplex identity by itself;
- inbound messages still require local consent and a valid messaging passport.

### Step 2: Marcin's Node Collects Contact-Control Attestations

Every handle Marcin submits must be attested before the Contact Catalog admits
the claim. Each attestation is a `capability-passport.v1` issued by an
attestation service under a dedicated capability id:

- `phone-control` for a verified phone number;
- `email-control` for a verified email address.

These capability ids name the same kind of artifact and are intentionally
symmetric with what Daniel will later attach to his contact request in Step 6;
the same passport shape proves "this holder controls this handle" regardless
of which side presents it.

For the phone number, Marcin already holds a `phone-control` passport. His
node can present this proof in a way that does not reveal Marcin's root
`participant:did:key` to the catalog unless the selected disclosure mode
requires it. The proof is used only to show that the holder may bind the phone
number to a contact route.

For the email addresses, Marcin does not yet have fresh attestations. His node
discovers an attestation service the same way it discovers any other role
through Seed Directory — by a capability id such as `email-attestation` paired
with endpoint evidence and a service passport. Seed Directory's job stays
limited to infrastructure discovery; the attestation service owns the
verification flow.

The request to the attestation service includes:

- the normalized email address to be attested;
- the Orbiplex identities or routing subjects that Marcin wants to associate
  with the contact path;
- proof material showing that those Orbiplex identities are controlled by
  Marcin's node;
- the requested purpose, here `contact` and `messaging`.

The attestation service sends each address a message containing:

- a confirmation link;
- a one-time code;
- an expiry, here one day from issuance.

After Marcin clicks the link or enters the one-time code, his node retrieves
the resulting `email-control` passport by presenting:

- the one-time code;
- the attested email address;
- the Orbiplex identities or routing subjects being associated;
- proof that those identities belong to the requester.

The service returns one or more signed `email-control` passports proving
control of the email handles for the requested purpose. The one-time code
itself is not published as network evidence.

### Step 3: Marcin Publishes Contact Claims

Marcin's node publishes contact claims to the Contact Catalog.

The user-facing action may be described as "publish my email and phone as ways
to contact me", but the catalog should not expose a public raw map such as:

```text
marcin@example.org -> participant:did:key:...
```

Instead, the catalog admission path checks the passports and stores an admitted
projection that can support lookup while preserving the contact-discovery
boundary:

```text
contact handle proof
  -> normalized or blinded lookup index
  -> route candidate
  -> routing subject / contact nym / invitation-required result
```

The stored claim includes the accepted purposes, such as `messaging`, and the
route Marcin's node wants contacted. It may include a routing subject or contact
nym rather than a root participant id. If Marcin later removes an email address
or rotates a contact nym, the catalog record must expire or be revoked rather
than silently remaining valid.

### Step 4: Daniel Composes a Message by Email Address

Daniel opens the Orbiplex client and starts the messaging middleware. The
compose window has ordinary message fields:

- recipient;
- subject or short title, if the middleware exposes one;
- message body;
- optional greeting or contact-request note.

Daniel types:

```text
marcin@example.org
```

As soon as the address is recognized as an external contact handle rather than a
known local Orbiplex contact, the UI shows a warning indicator next to the
recipient. The indicator means:

```text
additional contact setup is required before this message can be delivered
```

Daniel writes the message:

```text
Hi Marcin,

I have started using Orbiplex. Also: tea from brodziuszka, as promised.
```

He clicks **Send**. The message is written to the local outbound message queue.
It is not dropped merely because contact setup is incomplete.

### Step 5: Daniel's Middleware Resolves the Contact Route

The messaging middleware inspects the queued message and sees that Daniel does
not have a passport authorizing messages to the contact route behind
`marcin@example.org`.

Daniel's node discovers a suitable Contact Catalog through Seed Directory.
The lookup itself is performed through the Artifact Delivery resolver
registry, the same plug-in surface that already serves `artifact-store:`,
`memarium-public-entry:`, and `agora-record:`. The lookup is expressed as a
resolver scheme such as:

```text
contact-lookup:email:<normalized-digest>
```

Going through the resolver registry gives the lookup the existing
size/`sha256` verification, per-scheme enablement, and operator-visible
routing for free; the catalog stays a domain authority rather than a parallel
transport.

The query mode may be authenticated exact lookup, invitation-only lookup, or
a future blinded/private lookup profile. This story only requires that the
catalog does not return a naked root participant identity as the normal
result.

The resolver returns a `contact-lookup-result.v1`-like artifact containing a
route candidate for Marcin's node, for example:

- a routing subject;
- a contact nym;
- a node candidate with endpoint evidence;
- a flag saying that contact permission is required.

Daniel's outbound message now moves to:

```text
waiting-for-contact-permission
```

### Step 6: Daniel Sends a Contact Request

Daniel's node contacts Marcin's route over INAC through Artifact Delivery. The
delivery is marked `privacy = private-direct`, so Artifact Delivery may use
only adapters explicitly reviewed as private-safe; today that is
`inac-direct`. The request itself is a small `contact-request.v1` artifact,
not the full private message.

By default, Daniel's node includes:

- Daniel's display name;
- Daniel's sender handle, such as an email address or phone number;
- a passport attesting that Daniel controls that sender handle — the same
  `phone-control` or `email-control` `capability-passport.v1` shape Marcin
  collected in Step 2;
- an optional greeting, limited to 255 characters;
- a reply nym, routing subject, or participant id;
- the delivery material Marcin's node needs to answer the request.

The contact request is evaluated by Marcin's node before it reaches any
user-facing inbox. The transport session authenticates the node path, while
the attached passports and policy determine whether this request can create a
messaging relationship.

### Step 7: Marcin Reviews the Request

Marcin's node receives the request and creates a durable notification through
the existing user/operator notification queue. This step intentionally reuses
the same notification-action-issues-passport pattern already used by INAC
invitations (`inac.invitation.accept` / `inac.invitation.reject`): an inbound
artifact that needs human consent creates a notification with action refs,
and accepting one of those refs is what mints the narrow authorizing
passport. Messaging contact is the second concrete consumer of that pattern,
not a parallel mechanism.

The notification is shaped as a normal `notification.v1` record with at
least:

- `notification/kind = "messaging.contact-request"`;
- `subject/ref = contact-request:<id>`;
- `correlation/id` derived from the pair `(Daniel sender subject, Marcin
  route)`, so repeated requests from the same Daniel about the same route do
  not pile up as separate items;
- `collapse/key` set so that a retransmitted contact request updates the
  pending item idempotently instead of creating a duplicate;
- `actions = [{ ref: "messaging.contact.accept", … },
              { ref: "messaging.contact.reject", … }]`.

In the Node UI notification area, Marcin sees that Daniel is asking for
permission to send messages. The notification body is short and policy-shaped,
for example:

```text
Daniel Kowalski asks to send you Orbiplex messages.
Verified sender handle: daniel@example.net
Requested route: marcin@example.org
```

The UI gives Marcin at least two actions:

- accept messaging contact;
- reject the request.

Accepting does not turn Daniel into a general friend. It adds Daniel's
selected sender subject (participant, nym, or routing subject) to Marcin's
local `contacts` relationship class and issues a passport that authorizes
that subject to send messages to the Marcin route named in the request. The
default `contacts` policy is "may send messages to me"; nothing else is
implicitly granted. Rejecting records the local decision without minting any
authority, exactly as `inac.invitation.reject` does today.

Marcin accepts the communication channel.

### Step 8: Marcin's Node Issues a Messaging Passport

Marcin's node answers Daniel over INAC through Artifact Delivery, also marked
`privacy = private-direct`.

The response contains a `capability-passport.v1` under the
`messaging-receive` profile. Its scope covers at least:

- `scope.receiver` — Marcin's receiver-side Orbiplex contact route as a
  `routing:did:key:...` (per `routing-subject-binding.v1`) or a pairwise
  `contact_nym` (per Proposal 058); never the raw `participant:did:key`,
  consistent with the wire-privacy invariant in Proposal 059;
- `scope.public_handle` — the handle Daniel used to reach Marcin, here
  `marcin@example.org`;
- `scope.sender` — Daniel's authorized sender participant, nym, or routing
  subject;
- the permitted operation, here message delivery;
- expiry and revocation references;
- any local limits Marcin's policy attaches to `contacts`-class messaging.

The passport intentionally carries both kinds of meaning:

- protocol authority: Daniel may present it when sending messages;
- user-facing continuity: the permission corresponds to the Marcin contact
  handle Daniel selected and to Daniel's membership in Marcin's `contacts`
  set.

If Daniel later regenerates a nym, the preferred user experience is
transparent continuity. The concrete mechanism is `key-delegation.v1`: the
`messaging-receive` passport is rooted in Daniel's participant authority
(or another stable subject Marcin accepted), and new nyms sign messages as
delegated proxies. Marcin's node verifies the inbound message through the
existing inline `DelegationProof` path already implemented by the Key
Delegation Passports solution, so no extra round-trip is needed to confirm
that a freshly rotated nym still belongs to the accepted Daniel.

The user-level invariant is that Marcin should not have to re-approve the
same person only because Daniel rotated an application nym. The
implementation invariant is that this is realised by a single, already
existing delegation mechanism rather than by a new bespoke renewal flow.

### Step 9: Daniel's Node Attaches the Passport to Queued Messages

Daniel's node receives the passport, verifies it, and stores it in the
existing daemon passport state — the same `PassportCache` and
`DelegationCache` (with background sync) that today serves capability
passports and key delegations. There is no new "messaging passport store";
the messaging middleware reuses these primitives.

The messaging middleware scans the outbound queue for messages that were
waiting on this authority. It asks the host for a usable passport through a
`capability.passport.lookup`-style host capability call (the symmetric
counterpart to the existing `capability-passport-issue-request`), then
attaches the passport reference or inline passport to each matching outgoing
message.

The queued message to `marcin@example.org` can now leave
`waiting-for-contact-permission` and move to:

```text
ready-for-delivery
```

This step matters for recovery. On Marcin's side, the
`contacts`-class membership and the corresponding issued
`messaging-receive` passports live inside the participant-owned encrypted
vault defined by `pseudonym-vault.v1` (per Proposal 059), so reinstalling
Marcin's node from his mnemonic restores the policy state — not only keys —
and the same class of passport can still explain why Daniel's message should
be admitted.

### Step 10: Daniel Sends the Message

Daniel's node sends the message over INAC through Artifact Delivery, again
marked `privacy = private-direct`. The payload is a `message-envelope.v1`
artifact containing:

- the message body;
- sender and receiver references;
- the messaging passport or passport reference;
- any message id, threading id, timestamps, and content digest required by
  the messaging middleware.

Authorization is checked in two layers, matching the existing host-owned
admission contract:

Already enforced by the host and shared infrastructure (no messaging-specific
code needed):

- the passport signature is valid — Capability Binding's
  passport-aware verification pipeline;
- the passport has not expired or been revoked — Capability Binding plus
  the Seed Directory revocation feed, fail-closed when no current revocation
  view is available;
- the transport session is authenticated and pinned to attested endpoint
  certificate evidence — TLS Trust Policy peer-dial enforcement;
- size, rate, and idempotency limits hold — Artifact Delivery route policy
  and INAC receiver-side budgets.

Enforced by the messaging inbound acceptor itself:

- the sender participant or nym matches the passport `scope.sender` (and, if
  the sender presents a delegated nym, the inline `DelegationProof` resolves
  to the accepted subject);
- the receiver route matches the Marcin route in the passport
  `scope.receiver`;
- the public contact handle, if present, matches the route Daniel used and
  `scope.public_handle`;
- the `contacts`-class policy still admits this sender (membership not
  revoked, no local limits exhausted).

The acceptor itself is registered through one of the existing Artifact
Delivery acceptor surfaces (`artifact_delivery_acceptors.supervised_http`,
`in_process`, or `json_e_flow`) and is the single authoritative owner of the
`message-envelope.v1` artifact kind. If any of these checks fail, the node
may refuse the INAC transfer or stop admission before the messaging
middleware sees the content. The middleware should not be the first line of
authority for a malformed or unauthorized message.

### Step 11: Marcin's Middleware Stores the Message

The host-owned Artifact Delivery admission path dispatches the accepted
artifact to exactly one authoritative acceptor: the messaging middleware.

Storage is intentionally stratified across three layers, each holding a
different *class* of data with its own write rate and lifecycle:

```text
incoming message envelope
  -> Maildir body file                 (Layer 1: immutable per-message bytes)
  -> messaging-middleware SQLite index (Layer 2: rebuildable operational state)
  -> Memarium messaging facts          (Layer 3: bounded semantic/audit facts)
  -> inbox projection                  (read model fed by Layers 1+2)
```

**Layer 1 — Maildir bodies.** The durable per-message body is written as a
Maildir file under the messaging middleware's data directory. Bodies are
immutable for the life of the message and are not part of Memarium custody by
default; the file system is the right primitive for opaque per-message blobs.

**Layer 2 — Messaging-middleware-owned SQLite index.** The middleware owns a
local SQLite database (for example at `<data-dir>/messaging/index.sqlite`)
that holds operational mailbox state: per-message rows (id, from, to, date,
subject, threading id, flags, size, Maildir path), optional FTS5 search,
thread joins, read/unread, snooze, and starring. These fields are *hot* —
flipping `read` is a write — and they are fully rebuildable from Layer 1
bodies plus the Layer 3 fact stream. The index is therefore allowed to be
vacuumed, sharded, or fully rebuilt without coordinating with any other
module.

**Layer 3 — Memarium messaging facts.** Only the entries that carry real
semantic or audit weight are written into Memarium, so that the Memarium fact
volume stays bounded by *user and policy decisions* rather than by raw
message traffic. The story-relevant Layer 3 facts are:

- `contacts`-class membership changes (added, removed, sender subject
  rotated);
- issuance and revocation of `messaging-receive` passports, joined with
  the existing revocation feed;
- per-conversation or per-message classification decisions
  (`classification.v1` already lives in Memarium);
- retention decisions (deletion reason, archival export pointer);
- explicit crisis-space marks the user applies to a thread or message.

Per-message header rows and read flags **do not** belong to Layer 3.

The bounding rule, in one line:

> If the field is rewritten more often than once per message lifetime
> (read/unread flips, sort keys, thread membership), it stays in Layer 2.
> If it is a user-or-policy decision with non-zero audit weight, it goes to
> Layer 3. Bodies stay in Layer 1.

After storage succeeds, the middleware creates a notification through the
same notification queue used in Step 7. When Marcin clicks it, the UI opens
the mailbox view owned by the mailbox access middleware, focused on Daniel's
new message.

## Implementation Guidance Carried by This Story

- Contact handles are bootstrap claims, not durable identities.
- Contact Catalog may receive raw handles during attestation or lookup, but
  its default durable publication should be a privacy-preserving route
  projection (see Proposal 058 §2 for the Seed Directory / Contact Catalog
  boundary).
- Pairwise contact nyms are the preferred privacy posture for one-to-one
  communication (Proposal 058 §6). `messaging-receive` passport scope
  should accordingly name a `routing:did:key:...` or a pairwise `contact_nym`
  on the receiver side, never a bare `participant:did:key`.
- Messaging contact acceptance is narrower than F2F friendship. It should be
  represented as `contacts`-class membership plus a scoped passport, not as
  a global relationship-class upgrade.
- Middleware using INAC should expose configurable criteria for relationship
  classes such as `friends`, `contacts`, and local custom groups. `contacts`
  is the default class for "accepted message sender" and carries the
  built-in policy "may send messages to the owner"; richer per-class policies
  are local refinements.
- Nodes that accept messaging should publish that fact through
  `capability-advertisement.v1`, e.g. as a `messaging.accept` capability tied
  to the `messaging-receive` profile. Capability Advertisement is already
  the done discovery surface for "this peer currently speaks this baseline
  protocol surface" and is the natural place for Contact Catalog and lookup
  consumers to distinguish messaging-capable nodes.
- Authorization is checked at the host/Artifact Delivery admission boundary
  before the messaging middleware persists message content; the seven
  story-level checks split into shared infrastructure checks (passport sig,
  expiry/revocation, TLS evidence, size/rate) and messaging-specific
  acceptor checks (sender/receiver scope, public-handle match,
  `contacts` policy).
- The messaging middleware owns mailbox semantics; Artifact Delivery owns
  transport, recipient resolution, and single-owner inbound admission
  dispatch.
- Recovery of messaging-contact state belongs in the participant-owned
  encrypted vault (`pseudonym-vault.v1`), so restoring a node from its
  mnemonic restores `contacts` membership and issued
  `messaging-receive` passports — not only signing keys.
- Incoming message storage is stratified across three layers with disjoint
  lifecycle: Maildir for immutable bodies, a messaging-middleware-owned
  SQLite index for hot operational state (rebuildable from the other two
  layers), and Memarium for bounded semantic/audit facts only. Per-message
  header rows and `read/unread` flags **must not** end up in Memarium; the
  operational index must stay private to the messaging middleware so it can
  vacuum, shard, or rebuild without coordinating with Memarium's retention
  and classification policy.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| Someone tries to bind another person's email to their Orbiplex route | Catalog admission requires fresh contact-control attestation and proof that the named Orbiplex route belongs to the requester. |
| Contact Catalog becomes a public deanonymization index | Store privacy-preserving lookup projections and return route candidates or invitation-required results, not root participants by default. |
| Daniel sends the full message before consent exists | The message remains in Daniel's local outbound queue until a valid messaging passport is available. |
| Marcin accepts Daniel as a messenger but not as a friend | Use a scoped messaging passport and add Daniel to the dedicated `contacts` relationship class, kept distinct from `friends`. |
| Daniel rotates a nym and loses contact continuity | Root the `messaging-receive` passport in Daniel's participant (or another stable accepted subject); new nyms sign as delegated proxies under `key-delegation.v1` and are verified through the existing inline `DelegationProof` path. |
| Marcin reinstalls his node | `contacts` membership and issued `messaging-receive` passports live in `pseudonym-vault.v1`; mnemonic-based restore brings back both signing material and policy state, so Daniel's authority is re-evaluable without re-approval. |
| Passport scope and message envelope disagree | Marcin's node rejects before the messaging middleware stores the message. |
| Contact handle is reassigned by an email or phone provider | Use expiry, re-attestation windows, and revocation; do not treat contact-control proof as strong identity assurance. |
| Operational mailbox index grows to hundreds of MB on long-lived nodes | Keep the SQLite index private to the messaging middleware (Layer 2); allow it to be vacuumed, sharded, or fully rebuilt from Maildir bodies plus Memarium messaging facts without coordinating with Memarium retention or archival policy. |

## Open Continuation

- Implement the concrete `messaging-receive` passport profile, including the
  `scope.receiver` / `scope.sender` / `scope.public_handle` field shapes.
- Define the `message-envelope.v1` artifact.
- Define the attestation-service capability id used in Step 2 and the concrete
  OTP/link request and return contracts.
- Formalise the `contact-lookup:` resolver scheme for the frozen MVP
  invitation-only lookup profile.
- Specify the host-capability surface for "look up a usable passport for this
  outbound message" (`capability.passport.lookup`-style), since today the
  middleware host bridge exposes issue but not best-match lookup.
- Define Layer 2 (operational SQLite index) repair rules so the index can be
  fully rebuilt from Layer 1 Maildir bodies plus the Layer 3 Memarium
  messaging-fact stream, with no dependency on prior index state.
- Enumerate the concrete Layer 3 messaging-fact kinds (membership change,
  passport issuance/revocation, classification decision, retention
  decision, crisis-space mark) and register them with Memarium's fact
  surface.

## Implementation Coverage

Status legend: `[todo]` not started, `[in-progress]` partially implemented or
infrastructure exists but the story-specific surface is missing, `[done]`
implementation covers the story step. Each entry names the closest existing
artifact and what is still missing.

### Per-Step Coverage

- **Step 1 — Marcin opens a public contact path (contactability UI):** `[todo]`
  - Closest artifacts: Proposal 058 (Contact Catalog, Draft) sketches the local
    contact store / catalog split; Node UI (`Orbiplex Node UI`, status
    `partial`) has no contactability settings panel for messaging.
  - Missing: messaging-component contactability form, local contact store
    schema, and the participant/nym/routing-subject picker for outbound contact
    routes.

- **Step 2 — Marcin's node collects contact-control attestations:** `[todo]`
  - Closest artifacts: `capability-passport.v1` issuance via Capability Binding
    (`done`) and Key Delegation Passports (`done`) give the passport machinery;
    Seed Directory has discovery/`/key` endpoints (`done` / `partial`).
  - Newly frozen contracts: `phone-control` and `email-control` capability
    ids are registered as contact-control proof capabilities.
  - Missing: their concrete passport profiles, the attestation-service role
    (whether hosted on Seed Directory or a separate capability), OTP/link
    verification flow, and the request/return schemas referenced by
    `contact/attestation-ref` in Proposal 058.

- **Step 3 — Marcin publishes contact claims to the Contact Catalog:** `[in-progress]`
  - Closest artifacts: the catalog mechanics that Contact Catalog needs
    already exist in the `orbiplex-node-catalog` crate (`CatalogRecord`,
    `CatalogStore<T>`, `SqliteCatalog<T>`, `ObservedCatalogStore<T>`,
    `CatalogResolver`, `CatalogPredicate`, `TrustedProviderStore`, Agora
    bridge). Dator is the existing concrete instance of the Catalog
    Provider Role for the offer domain; Contact Catalog is the next named
    instance, now documented in Proposal 058 §11 and §12 with a Rust
    supervised-middleware reuse path. Solution 019 (`Orbiplex Middleware`,
    `done`) provides the hosting plane.
  - Newly frozen contracts: `contact-claim.v1`, the `contact-catalog`
    capability id, and Solution 025 define the first implementation target.
  - Missing: the Contact Catalog Rust middleware crate that parameterises `node/catalog` with
    `ContactClaimRecord` (P058-017), `catalog_kind: contact` registration
    (P058-004), admission policy enforcing attestation freshness
    (P058-005), revocation / expiry pipeline (P058-011), and generalisation
    of the `CatalogAdapter` trait over `T: CatalogRecord` if remote fetch
    is in scope (P058-018).

- **Step 4 — Daniel composes a message by email address (compose UI + outbound
  queue):** `[todo]`
  - Closest artifacts: the `core/messaging` capability in the Capability
    Registry is the baseline encrypted peer-session surface, **not** an
    application-level messaging middleware; INAC (`partial`) and Artifact
    Delivery (`partial`) own transport, not message UX; Solution 019
    (`Orbiplex Middleware`, `done`) provides the supervised-middleware
    plumbing on which a future messaging-middleware module would attach
    (claimed routes, host capability bridge, lifecycle, module reporting).
  - Missing: messaging middleware module (compose form, recipient parsing,
    local outbound queue with `waiting-for-contact-permission` /
    `ready-for-delivery` states), and the "unknown recipient" warning
    indicator.

- **Step 5 — Daniel's middleware resolves the contact route:** `[todo]`
  - Closest artifacts: Artifact Delivery resolver registry (`partial`,
    production: `artifact-store:`, plus opt-in `memarium-*` and
    `agora-record:`) is the plug-in point named by the story as
    `contact-lookup:`; Seed Directory capability discovery is in place.
  - Newly frozen contracts: `contact-lookup-result.v1` and MVP
    invitation-only lookup.
  - Missing: the `contact-lookup:` resolver scheme and its Contact Catalog
    client, and the queue state transition driven by the lookup result.

- **Step 6 — Daniel sends a contact request over INAC/AD:** `[in-progress]`
  - Closest artifacts: the exact transport shape this step needs —
    `AD -> inac-direct` push with inline `capability-passport.v1`
    authorization and `privacy = private-direct` — is already live as
    Story-005's private/direct Whisper path; INAC `inac.push` + Artifact
    Delivery single-owner inbound admission (`partial`) carry the inline
    passport gate, including the `inac.invitation` passport precedent;
    `participant-bind.v1` / `routing-subject-binding.v1` cover sender
    identifiers.
  - Newly frozen contract: `contact-request.v1`.
  - Missing: an authoritative acceptor registered for it, and a sender-handle
    attestation reference compatible with Step 2.

- **Step 7 — Marcin reviews the request (notification + accept/reject):**
  `[in-progress]`
  - Closest artifacts: Proposal 057 notifications are largely landed —
    `notification.create` host capability, durable store, operator UI inbox,
    rate limiting (`done`); INAC invitation flow already issues passports
    through `inac.invitation.accept` / `inac.invitation.reject` actions on the
    shared notification queue and is the direct precedent for the messaging
    contact-request flow.
  - Missing: a messaging-specific `notification/kind`, the contact-request
    detail view, and accept/reject actions wired to `messaging-receive`
    issuance instead of `inac.invitation`. P057-009 (inline action execution)
    is itself `partial`.

- **Step 8 — Marcin's node issues a messaging passport:** `[in-progress]`
  - Closest artifacts: `capability-passport.v1`, Capability Binding (`done`),
    Key Delegation Passports incl. inline `DelegationProof` (`done`) — the
    chosen mechanism for nym-rotation continuity is the existing delegation
    path; INAC + Artifact Delivery can carry the response (`partial`).
  - Newly frozen contract: `messaging-receive` capability id.
  - Missing: passport profile implementation (scope fields `receiver` as
    `routing:did:key:...` or `contact_nym`, `sender`, `public_handle`,
    permitted op, expiry, revocation refs, `contacts`-class limits), and a
    `key-delegation.v1`
    grant label scoping delegated messaging signing.

- **Step 9 — Daniel's node attaches the passport to queued messages:** `[todo]`
  - Closest artifacts: the daemon already has `PassportCache` and
    `DelegationCache` with background sync (`done`); INAC/AD already accept
    inline passports under `authorization`; `pseudonym-vault.v1` is the named
    recovery container on Marcin's side (P059, schema seed present, runtime
    not implemented).
  - Missing: messaging middleware outbound-queue scanner, a host capability
    surface for best-match passport lookup
    (`capability.passport.lookup`-style — the middleware bridge currently
    exposes issue but not lookup), attach-and-rescan on passport arrival,
    queue state transition to `ready-for-delivery`, and the vault-backed
    persistence of `contacts` membership.

- **Step 10 — Daniel sends the message; Marcin's node verifies before
  middleware:** `[in-progress]`
  - Closest artifacts: four of the seven story-level checks are already
    enforced by shared infrastructure — Capability Binding passport
    sig/expiry/revocation pipeline (`done`), TLS Trust Policy peer-dial
    evidence (`mvp-ready`), and AD/INAC route policy + receiver-side
    budgets (`partial`); only sender/receiver/public-handle scope match and
    the `contacts`-class policy belong to the messaging acceptor itself.
    AD single-owner inbound admission (`partial`) is the dispatch surface
    the acceptor will register through.
  - Missing: `message-envelope.v1` artifact schema, the messaging acceptor
    registered via `artifact_delivery_acceptors.supervised_http` /
    `in_process` / `json_e_flow`, and the three messaging-specific scope
    checks plus the `contacts`-policy gate inside it.

- **Step 11 — Marcin's middleware stores the message:** `[todo]`
  - Closest artifacts: AD single-owner acceptor dispatch (`partial`) is the
    intended hand-off point; notification infrastructure (P057) can announce
    arrival; Memarium owns the Layer 3 fact surface
    (`Memarium Host Capability API` — `partial`,
    `Classification Policy Facts` — `partial`); two of the five planned
    Layer 3 fact kinds already have frozen contracts on the Memarium side —
    `classification.v1` (Classification Label Contract — `done`) and
    crisis-space marks (Memarium Crisis Space Loop — `done`).
  - Missing: messaging middleware itself, Layer 1 Maildir body store, Layer
    2 middleware-owned SQLite operational index with a documented
    rebuild-from-Layer-1+Layer-3 procedure, the three remaining Layer 3
    messaging-fact kinds (membership change, passport
    issuance/revocation, retention decision) registered with Memarium, the
    inbox projection, and the "open in mailbox view" notification target.

### Cross-Cutting Building Blocks

- **Capability passports (issue, embed, verify, cache, revoke):** `[done]` —
  Capability Binding, Key Delegation Passports, and Capability Advertisement
  cover issuance, inline `DelegationProof` verification, background sync, and
  revocation feed plumbing.
- **Middleware extension-host plumbing for the future messaging middleware
  (Solution 019):** `[done]` — supervised local HTTP middleware, in-process
  middleware, claimed local routes, host capability bridge, middleware
  init/reporting, trace, and component path are all `done`; the messaging
  middleware module attaches through these primitives without inventing a
  new lifecycle. What's still messaging-specific is the module itself, not
  the hosting plane.
- **INAC + Artifact Delivery transport plane:** `[in-progress]` — control
  plane, single-owner inbound admission, WSS peer transport, endpoint
  evidence, passport gates, and recovery worker are landed (`partial`);
  Matrix mailbox transport, broader production hardening, and any
  messaging-specific acceptors remain to do.
- **User/operator notifications (P057):** `[in-progress]` — store, operator
  inbox, host capability, and per-sender/kind rate limits are `done`; inline
  action execution is `partial` and user-facing inboxes are MVP operator-only.
- **Capability Advertisement of messaging support:** `[todo]` —
  `capability-advertisement.v1` plumbing is `done`; a concrete
  `messaging.accept` advertisement entry tied to the `messaging-receive`
  profile is not yet defined or published.
- **Contact Catalog as a domain catalog (P058):** `[in-progress]` —
  `contact-claim.v1`, `contact-lookup-result.v1`, `contact-request.v1`,
  Solution 025, and the `contact-catalog` capability id are now frozen for
  MVP; module implementation and Seed Directory advertisement remain to do.
- **Contact-handle attestation (phone / email) as a capability surface:**
  `[todo]` — `phone-control` and `email-control` ids are registered; the
  attestation-service role and OTP/link verification flow remain to do.
- **Messaging middleware with stratified storage (compose, outbound queue,
  Layer 1 Maildir bodies, Layer 2 middleware-owned SQLite index, Layer 3
  Memarium messaging facts, mailbox view):** `[todo]` — the only existing
  "messaging" identifier is the `core/messaging` transport-baseline
  capability, which is not an application middleware; Memarium provides the
  fact surface for Layer 3 (`Memarium Host Capability API` is `partial`)
  but the messaging fact kinds are not yet enumerated.
- **Local contact store (raw address book, labels, pairwise nym mappings):**
  `[todo]` — Proposal 058 names it; nothing implemented.
- **"Nym factory" with role-separated derived keys (signing, DH, sealing) and
  routing-subject vault:** `[todo]` — Proposal 059 is Draft;
  `pseudonym-vault.v1` exists as a first schema seed and `nym-certificate.v1`
  / `routing-subject-binding.v1` define the public surfaces, but participant
  key-role derivation (`participant/signing`, `participant/dh`,
  `participant/vault-wrap`), per-nym random seed storage, and vault
  sync/restore runtime are not implemented.
- **`contacts` relationship class (default policy: "may send messages to me")
  kept distinct from `friends`:** `[todo]` — no relationship-class model
  exists yet at the middleware admission boundary; the messaging middleware
  needs a local `contacts` set whose membership is what the
  `messaging-receive` passport effectively encodes for the receiver side.

## Outstanding Features per Subsystem (Path to `[done]`)

For each `[todo]` and `[in-progress]` entry in Implementation Coverage above,
this section lists the concrete features that still need to land. Each
feature points to the closest existing tracker document; when no tracker
exists yet, that is called out explicitly so the gap is visible.

### Step 1 — outstanding features

- contactability settings UI panel inside the messaging middleware client (no
  dedicated tracker; awaiting messaging middleware solution doc)
- local contact store schema covering raw handles, labels, and pairwise nym
  mappings (see: [Proposal 058 Tracking row P058-008](../40-proposals/058-contact-catalog.md))
- participant / nym / routing-subject picker for outbound contact routes
  (see: [Proposal 058 Tracking row P058-001](../40-proposals/058-contact-catalog.md),
  [Solution 001 Node UI](../60-solutions/001-node-ui/001-node-ui.md))
- UI wording distinguishing contact-control proof from identity assurance
  (see: [Proposal 058 Tracking row P058-012](../40-proposals/058-contact-catalog.md))

### Step 2 — outstanding features

- `phone-control` capability id registration (see:
  [Capability Registry](../60-solutions/CAPABILITY-REGISTRY.en.md))
- `email-control` capability id registration (see:
  [Capability Registry](../60-solutions/CAPABILITY-REGISTRY.en.md))
- attestation-service role discoverable through Seed Directory under a
  capability id such as `email-attestation` (see:
  [Proposal 025](../40-proposals/025-seed-directory-as-capability-catalog.md);
  no dedicated attestation-service solution doc yet)
- OTP/link verification flow specification (no dedicated tracker; needs new
  proposal)
- request/return schemas referenced by `contact/attestation-ref` (see:
  [Proposal 058 Tracking row P058-001](../40-proposals/058-contact-catalog.md))

### Step 3 — outstanding features

- `contact-claim.v1` schema definition (see:
  [Proposal 058 Tracking row P058-001](../40-proposals/058-contact-catalog.md))
- Contact Catalog module/service implementation as a Rust supervised HTTP
  middleware reusing `orbiplex-node-catalog` (see:
  [Proposal 058 Tracking row P058-014](../40-proposals/058-contact-catalog.md),
  [Proposal 058 Tracking row P058-016](../40-proposals/058-contact-catalog.md),
  [Proposal 058 Tracking row P058-017](../40-proposals/058-contact-catalog.md),
  [Proposal 058 Tracking row P058-018](../40-proposals/058-contact-catalog.md))
- `catalog_kind: contact` registration via existing `catalog_endpoints`
  abstraction (see:
  [Proposal 058 Tracking row P058-004](../40-proposals/058-contact-catalog.md))
- admission policy enforcing attestation freshness (see:
  [Proposal 058 Tracking row P058-005](../40-proposals/058-contact-catalog.md))
- revocation / expiry pipeline for rotated contact handles (see:
  [Proposal 058 Tracking row P058-011](../40-proposals/058-contact-catalog.md))

### Step 4 — outstanding features

- messaging middleware module with compose form, recipient parser, and local
  outbound queue (no dedicated tracker; hosted on
  [Solution 019 Middleware](../60-solutions/019-middleware/019-middleware.md))
- outbound queue state machine including
  `waiting-for-contact-permission` and `ready-for-delivery` (no dedicated
  tracker)
- "unknown recipient" warning indicator in compose UI (see:
  [Solution 001 Node UI](../60-solutions/001-node-ui/001-node-ui.md))

### Step 5 — outstanding features

- `contact-lookup:` resolver scheme registration in the Artifact Delivery
  resolver registry (see:
  [Solution 023](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))
- Contact Catalog lookup client behind that resolver (no dedicated tracker;
  covered by Contact Catalog module work in
  [Proposal 058 Tracking row P058-014](../40-proposals/058-contact-catalog.md))
- queue state transition wiring driven by the lookup result (depends on Step
  4 messaging middleware)

### Step 6 — outstanding features

- authoritative inbound acceptor for `contact-request.v1` registered with
  Artifact Delivery (see:
  [Solution 023 §Single-Owner Inbound Admission](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))
- sender-handle attestation reference compatible with the Step 2 passport
  shape (see:
  [Proposal 058 Tracking row P058-005](../40-proposals/058-contact-catalog.md))
- route policy default with `privacy = private-direct` for the
  contact-request route (see:
  [Solution 023 privacy invariant](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))

### Step 7 — outstanding features

- `notification/kind = "messaging.contact-request"` registered as a known
  notification kind (see:
  [Proposal 057](../40-proposals/057-user-and-operator-notifications.md))
- contact-request detail view in operator/user UI (see:
  [Solution 001 Node UI](../60-solutions/001-node-ui/001-node-ui.md))
- `messaging.contact.accept` / `messaging.contact.reject` action refs wired
  to `messaging-receive` issuance via the inline action execution
  registry (see:
  [Proposal 057 Tracking row P057-009](../40-proposals/057-user-and-operator-notifications.md))
- promote inline action execution (P057-009) from `partial` to `done` for
  the messaging-action class (see:
  [Proposal 057 Tracking row P057-009](../40-proposals/057-user-and-operator-notifications.md))

### Step 8 — outstanding features

- `messaging-receive` passport profile and scope field shapes (`receiver`,
  `sender`, `public_handle`, op, expiry, revocation, `contacts`-class limits)
  (see:
  [Capability Registry](../60-solutions/CAPABILITY-REGISTRY.en.md); needs a
  new proposal to freeze the profile)
- `key-delegation.v1` grant label for delegated messaging signing (see:
  [Solution 014](../60-solutions/014-key-delegation-passports/014-key-delegation-passports.md),
  [Proposal 032](../40-proposals/032-key-delegation-passports.md))
- INAC/AD outbound carrying the issued passport response under
  `privacy = private-direct` (see:
  [Solution 017](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md),
  [Solution 023](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))

### Step 9 — outstanding features

- messaging middleware outbound-queue scanner (no dedicated tracker)
- `capability.passport.lookup`-style host capability surface for
  best-match passport lookup from middleware — the missing symmetric
  counterpart of the existing issue path (see:
  [Solution 006 Daemon Dispatch Integration](../60-solutions/006-capability-binding/006-capability-binding.md),
  [Solution 019 Host Capability Bridge](../60-solutions/019-middleware/019-middleware.md))
- attach-and-rescan-on-passport-arrival in the middleware (no dedicated
  tracker)
- queue state transition to `ready-for-delivery` (no dedicated tracker)
- vault-backed persistence of `contacts` membership and issued
  `messaging-receive` passports (see:
  [Proposal 059 Tracking row P059-009](../40-proposals/059-participant-and-nym-key-role-derivation.md),
  [Proposal 059 Tracking row P059-010](../40-proposals/059-participant-and-nym-key-role-derivation.md))

### Step 10 — outstanding features

- `message-envelope.v1` artifact schema (no dedicated tracker; needs new
  proposal)
- messaging inbound acceptor registered via one of
  `artifact_delivery_acceptors.supervised_http` / `in_process` /
  `json_e_flow` (see:
  [Solution 023](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))
- messaging-specific sender ↔ `scope.sender` check, with delegated nyms
  resolving through inline `DelegationProof` (see:
  [Solution 014](../60-solutions/014-key-delegation-passports/014-key-delegation-passports.md))
- messaging-specific receiver-route ↔ `scope.receiver` check (no dedicated
  tracker; messaging acceptor responsibility)
- messaging-specific public-handle ↔ `scope.public_handle` check (no
  dedicated tracker; messaging acceptor responsibility)
- `contacts`-class policy gate inside the acceptor (no dedicated tracker;
  depends on Cross-Cutting `contacts` block below)
- route policy default with `privacy = private-direct` for the
  `message-envelope.v1` route (see:
  [Solution 023 privacy invariant](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))

### Step 11 — outstanding features

- messaging middleware module itself (no dedicated tracker; awaiting
  solution doc)
- Layer 1 Maildir body store under the middleware data directory (no
  dedicated tracker)
- Layer 2 middleware-owned SQLite operational index with documented
  rebuild-from-Layer-1 + Layer-3 procedure (see: this story's Open
  Continuation; no separate tracker yet)
- Layer 3 `contacts`-membership-change fact kind registered with Memarium
  (see:
  [Solution 002 Memarium Host Capability API](../60-solutions/002-memarium/002-memarium.md),
  [Proposal 036](../40-proposals/036-memarium.md))
- Layer 3 `messaging-receive` issuance / revocation fact kind registered
  with Memarium (see: same)
- Layer 3 retention-decision fact kind registered with Memarium (see: same)
- inbox projection fed by Layer 1 + Layer 2 (no dedicated tracker)
- "open in mailbox view" notification target wired into the arrival
  notification (see:
  [Proposal 057](../40-proposals/057-user-and-operator-notifications.md),
  [Solution 001 Node UI](../60-solutions/001-node-ui/001-node-ui.md))

### Cross-Cutting Block — INAC + Artifact Delivery transport plane — outstanding features

- Matrix mailbox transport adapter (see:
  [Solution 023](../60-solutions/023-artifact-delivery/023-artifact-delivery.md),
  [Solution 017](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md))
- raw binary frame streaming optimization (see:
  [Solution 017 capability "Binary Frame Streaming"](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md))
- `inac-peer-artifact:` peer-referenced payload fetch (see:
  [Solution 023](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))
- broader production hardening for AD outbound + inbound paths (see:
  [Solution 023](../60-solutions/023-artifact-delivery/023-artifact-delivery.md))
- messaging-specific acceptors (covered by Step 6 and Step 10 above)

### Cross-Cutting Block — User/operator notifications — outstanding features

- promote P057-009 inline action execution from `partial` to `done` for
  the messaging-action class (see:
  [Proposal 057 Tracking](../40-proposals/057-user-and-operator-notifications.md))
- promote P057-011 cross-recipient user inboxes from `partial` to `done`
  so the user (not only operator) sees messaging notifications (see:
  [Proposal 057 Tracking](../40-proposals/057-user-and-operator-notifications.md))
- (deferred: P057-012 OS notifications — not blocking for this story)

### Cross-Cutting Block — Capability Advertisement of messaging support — outstanding features

- `messaging.accept` advertisement entry defined and tied to the
  `messaging-receive` profile (see:
  [Capability Registry](../60-solutions/CAPABILITY-REGISTRY.en.md),
  [Solution 007](../60-solutions/007-capability-advertisement/007-capability-advertisement.md))
- publication of `messaging.accept` by nodes that accept messaging, so
  Contact Catalog and lookup consumers can filter messaging-capable nodes
  (see:
  [Solution 007](../60-solutions/007-capability-advertisement/007-capability-advertisement.md))

### Cross-Cutting Block — Contact Catalog as a domain catalog (P058) — outstanding features

Already frozen for MVP:

- `contact-claim.v1` schema (see:
  [Proposal 058 Tracking row P058-001](../40-proposals/058-contact-catalog.md))
- `contact-lookup-result.v1` schema (see:
  [Proposal 058 Tracking row P058-002](../40-proposals/058-contact-catalog.md))
- `contact-request.v1` schema (see:
  [Solution 025 Contact Catalog](../60-solutions/025-contact-catalog/025-contact-catalog.md))
- `contact-catalog` capability id and minimal profile (see:
  [Proposal 058 Tracking row P058-003](../40-proposals/058-contact-catalog.md))
- first MVP query mode decision: authenticated invitation-only lookup (see:
  [Proposal 058 Tracking row P058-007](../40-proposals/058-contact-catalog.md))
- Contact Catalog solution doc and capability sidecar (see:
  [Proposal 058 Tracking row P058-014](../40-proposals/058-contact-catalog.md))

Still outstanding:

- `catalog_kind: contact` registration through `catalog_endpoints` (see:
  [Proposal 058 Tracking row P058-004](../40-proposals/058-contact-catalog.md))
- admission policy (attestation freshness, signature, expiry, purpose
  allowlist, TTL) (see:
  [Proposal 058 Tracking row P058-005](../40-proposals/058-contact-catalog.md))
- privacy-preserving lookup index (see:
  [Proposal 058 Tracking row P058-006](../40-proposals/058-contact-catalog.md))
- local contact store model (see:
  [Proposal 058 Tracking row P058-008](../40-proposals/058-contact-catalog.md))
- pairwise contact nym handling (see:
  [Proposal 058 Tracking row P058-009](../40-proposals/058-contact-catalog.md))
- routing-subject / contact-nym as default lookup result with multi-route
  support (see:
  [Proposal 058 Tracking row P058-010](../40-proposals/058-contact-catalog.md))
- contact claim revocation and expiry pipeline (see:
  [Proposal 058 Tracking row P058-011](../40-proposals/058-contact-catalog.md))
- operator / user UI wording (see:
  [Proposal 058 Tracking row P058-012](../40-proposals/058-contact-catalog.md))
- Agora publication policy for catalog records (see:
  [Proposal 058 Tracking row P058-013](../40-proposals/058-contact-catalog.md))
- no-match audit event policy (see:
  [Proposal 058 Tracking row P058-015](../40-proposals/058-contact-catalog.md))
- Catalog Provider Role contract documented (Dator + Contact Catalog as
  named instances of the same role) (see:
  [Proposal 058 Tracking row P058-016](../40-proposals/058-contact-catalog.md))
- Contact Catalog Rust supervised HTTP middleware crate scaffold reusing
  `orbiplex-node-catalog` primitives (see:
  [Proposal 058 Tracking row P058-017](../40-proposals/058-contact-catalog.md))
- generalise `node/catalog` `CatalogAdapter` trait over `T: CatalogRecord`
  so contact and offer providers share one async remote-fetch contract
  (see:
  [Proposal 058 Tracking row P058-018](../40-proposals/058-contact-catalog.md))

### Cross-Cutting Block — Contact-handle attestation as a capability surface — outstanding features

- Already frozen: `phone-control` and `email-control` capability ids are now
  registered in the Capability Registry.
- attestation-service role and Seed Directory discoverability (no dedicated
  tracker; needs new proposal)
- `phone-control` passport profile (see:
  [Capability Registry](../60-solutions/CAPABILITY-REGISTRY.en.md))
- `email-control` passport profile (see:
  [Capability Registry](../60-solutions/CAPABILITY-REGISTRY.en.md))
- OTP/link verification flow (no dedicated tracker)
- request/return schema definitions (see:
  [Proposal 058 Tracking row P058-001](../40-proposals/058-contact-catalog.md))

### Cross-Cutting Block — Messaging middleware with stratified storage — outstanding features

- messaging middleware solution document and capability sidecar (no
  dedicated tracker)
- Layer 1 / Layer 2 / Layer 3 storage stratification per Step 11 (see: Step
  11 above)
- enumeration and registration of Layer 3 messaging-fact kinds with
  Memarium (see:
  [Solution 002](../60-solutions/002-memarium/002-memarium.md), this
  story's Open Continuation)
- mailbox view and inbox projection (no dedicated tracker)
- mailbox-view-targeted notification action (see:
  [Proposal 057](../40-proposals/057-user-and-operator-notifications.md))

### Cross-Cutting Block — Local contact store — outstanding features

- raw address book entry storage (see:
  [Proposal 058 Tracking row P058-008](../40-proposals/058-contact-catalog.md))
- user labels and per-contact metadata (see:
  [Proposal 058 Tracking row P058-008](../40-proposals/058-contact-catalog.md))
- pairwise nym mapping table (see:
  [Proposal 058 Tracking row P058-008](../40-proposals/058-contact-catalog.md),
  [Proposal 058 Tracking row P058-009](../40-proposals/058-contact-catalog.md))
- never-published-by-default policy enforcement (see:
  [Proposal 058 Tracking row P058-008](../40-proposals/058-contact-catalog.md))

### Cross-Cutting Block — "Nym factory" with role-separated derived keys — outstanding features

- participant root-seed derivation layer with versioned, domain-separated
  derivation labels (see:
  [Proposal 059 Tracking row P059-002](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- `participant/dh` role (X25519 key agreement) (see:
  [Proposal 059 Tracking row P059-004](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- `participant/vault-wrap` symmetric AEAD wrap key (see:
  [Proposal 059 Tracking row P059-005](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- per-nym random seed storage inside the encrypted vault (see:
  [Proposal 059 Tracking row P059-007](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- routing-subject seed storage inside the vault (see:
  [Proposal 059 Tracking row P059-008](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- `pseudonym-vault.v1` runtime promotion from schema seed (see:
  [Proposal 059 Tracking row P059-009](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- vault sync / restore runtime in Node (see:
  [Proposal 059 Tracking row P059-010](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- role-aware participant recovery bundle (see:
  [Proposal 059 Tracking row P059-011](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- explicit signer / sealer purpose labels for the new participant roles
  (see:
  [Proposal 059 Tracking row P059-012](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- schema-gate policy preventing accidental participant-recovery-recipient
  leakage in pseudonymous envelopes (see:
  [Proposal 059 Tracking row P059-013](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- explicit `route:` vs `routing:did:key:...` boundary tests (see:
  [Proposal 059 Tracking row P059-014](../40-proposals/059-participant-and-nym-key-role-derivation.md))
- pending design decisions: `participant/dh` projection (P059-015),
  root-seed materialization (P059-016), minimal vault shape (P059-017),
  vault wrap derivation source (P059-018), multi-device vault merge
  (P059-019) (see:
  [Proposal 059 Tracking](../40-proposals/059-participant-and-nym-key-role-derivation.md))

### Cross-Cutting Block — `contacts` relationship class — outstanding features

- local relationship-class model inside the messaging middleware (no
  dedicated tracker)
- `contacts` membership set with default "may send messages to me" policy
  (no dedicated tracker)
- bi-directional projection between `contacts` membership and issued
  `messaging-receive` passports (no dedicated tracker)
- per-class limit configuration surface (rate, size, sender allow/deny) (no
  dedicated tracker)
- vault-backed persistence of membership changes per Step 9 (see:
  [Proposal 059 Tracking row P059-010](../40-proposals/059-participant-and-nym-key-role-derivation.md))
