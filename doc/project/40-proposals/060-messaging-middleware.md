# Proposal 060: Messaging Middleware and Personal Message Delivery

Based on:

- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/60-solutions/002-memarium/002-memarium.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`
- `doc/project/60-solutions/014-key-delegation-passports/014-key-delegation-passports.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/025-contact-catalog/025-contact-catalog.md`
- `doc/schemas/capability-passport.v1.schema.json`
- `doc/schemas/contact-request.v1.schema.json`

## Status

Draft

## Date

2026-05-17

## Executive Summary

Story-010 (Message to a Friend) walks through the end-to-end UX of sending a
private Orbiplex message by typing an external contact handle. Most of the
plumbing needed for that flow is already specified and partially landed:
Contact Catalog (Solution 025) handles discovery, admission, and contact
requests; Artifact Delivery (Solution 023) handles transport; Capability
Binding handles passport authority; INAC handles private/direct transport;
P057 handles notifications.

What is still missing is the **messaging middleware** — the
application-level domain module that owns:

- composing messages,
- the local outbound message queue with its state machine,
- inbound message storage stratified across Maildir bodies, a
  middleware-owned SQLite operational index, and bounded Memarium
  semantic / audit facts,
- the `messaging-receive@v1` passport profile freeze and the
  `message-envelope.v1` artifact contract,
- the inbound acceptor that performs the three messaging-specific scope
  checks plus the `contacts`-class policy gate before persisting any
  message body,
- the `contacts` relationship class model with default policy
  "may send messages to me",
- the mailbox view, inbox projection, and the "open in mailbox view"
  notification target,
- the bridge to participant-owned vault recovery for `contacts`
  membership and issued passports.

This proposal freezes those contracts, names the component, and stratifies
its responsibilities against the daemon and the existing supervised
middleware host. It deliberately reuses every piece of existing
infrastructure rather than reinventing transport, admission, or passport
verification.

The single biggest decision is that **messaging middleware is the
authoritative acceptor for `message-envelope.v1` registered through one
of the existing `artifact_delivery_acceptors.*` surfaces**, not a parallel
transport plane. AD does generic admission (signature, expiry, revocation,
TLS evidence, size, rate); the messaging acceptor does the three
messaging-specific scope checks and the `contacts`-class policy gate
before invoking persistence.

The first implementation slice should be deliberately narrow: one-to-one
text messages, `private-direct` delivery, Contact Catalog lookup by route
candidate, inline or `artifact-store:` body payloads, one local node UI
mailbox, and no cross-device synchronization. That slice is already enough
to exercise the real seams without asking the messaging module to become
its own transport, identity system, contact catalog, or long-term archive.

## Context and Problem Statement

Orbiplex today has every primitive needed to deliver a private message
between two nodes, but no application-level domain module that ties them
together into a user-facing inbox + outbox experience:

- Artifact Delivery moves any signed artifact between authenticated peers
  with single-owner inbound admission and the existing privacy invariant
  (`privacy = private-direct` → `inac-direct`).
- INAC carries inline-passport-gated peer pushes over WSS.
- Capability Binding verifies passport signatures, expiry, revocation
  freshness, and audits authorization decisions.
- Key Delegation Passports supports proxy-signed artifacts with inline
  `DelegationProof`.
- Contact Catalog (Solution 025) admits contact claims, exposes
  invitation-only lookup, registers the `contact.request` acceptor,
  creates `contact-request.received` notifications with accept / reject
  actions, and issues `messaging-receive@v1` capability passports on
  acceptance.
- The Capability Registry already has `messaging-receive` as an
  application-consent capability id (`app/messaging-receive`).
- Solution 019 Middleware provides the supervised-HTTP / in-process /
  JSON-e-Flow extension-host plane.
- Memarium exposes a host capability surface for semantic facts with
  policy and classification.
- `core/messaging` is the protocol-native peer-session baseline; it is not
  an application middleware.

What no document yet specifies is *how* a node-attached domain module
turns those primitives into a personal mailbox: which acceptor it
registers, what schema it consumes, how its outbound queue interacts with
passport issuance, where message bodies live, how operational state is
kept separate from semantic facts, and what consent class governs
sender-side acceptance.

Story-010 §11 already sketched the stratified storage model (Maildir +
middleware-owned SQLite + bounded Memarium facts) and the
`contacts`-class membership idea. This proposal lifts those story-level
sketches into a proposal-level contract and freezes the artifact +
passport profile required to implement them.

## Goals

- Define the messaging middleware as a node-attached domain module with
  one named role and explicit responsibilities.
- Freeze the `message-envelope.v1` artifact schema.
- Freeze the `messaging-receive@v1` passport profile, including its
  `scope.*` field shapes.
- Define the local outbound message queue state machine.
- Define the inbound acceptor contract and enumerate the three
  messaging-specific scope checks + `contacts`-class policy gate.
- Define the storage stratification across Layer 1 (Maildir),
  Layer 2 (middleware-owned SQLite operational index), and
  Layer 3 (bounded Memarium semantic / audit facts).
- Define the `contacts` relationship class as a local set with default
  policy "may send messages to me" and a bi-directional projection
  against issued `messaging-receive@v1` passports.
- Specify the recovery story for `contacts` membership and issued
  passports against `pseudonym-vault.v1` (P059).
- Specify the `key-delegation.v1` grant label for delegated messaging
  signing, so Daniel's nym rotation does not break Marcin's acceptance.
- Stratify the role into a small daemon-side host/authority layer and a
  separate messaging service, following the precedent set by Contact
  Catalog (P058 §11 Catalog Provider Role and the daemon-vs-service split
  documented for Solution 025).

## Non-Goals

- This proposal does not specify a compose UI design beyond saying that
  compose is a Node UI surface that calls into the messaging service.
- This proposal does not bridge to standard email or to any external IM
  network. Messaging is Orbiplex-only.
- This proposal does not define a search query language. Layer 2 may
  expose FTS5 over message bodies, but the query surface is implementation
  detail.
- This proposal does not define a cross-device sync protocol for read /
  unread / flag state. Single-device MVP is enough for story-010; sync
  is post-MVP.
- This proposal does not own the contact-request flow. That flow lives in
  Solution 025 Contact Request Admission; the messaging middleware
  consumes the resulting `messaging-receive@v1` passports.
- This proposal does not own the local contact store. That store is
  owned by the daemon under Solution 025 Local Contact Store; the
  messaging middleware reads / writes through host capability calls.
- This proposal does not own attestation acquisition for `phone-control`
  / `email-control`. That is a separate proposal slot (see story-010
  Cross-Cutting block).
- This proposal does not define end-to-end message-body encryption. It may
  be added as a later body profile without changing the transport,
  consent, or storage boundaries frozen here.

## Proposed Model

### 1. Component Boundary

The messaging middleware is a node-attached domain module with two
co-located but distinct subsystems, mirroring the Contact Catalog split:

- **Node daemon** owns the small host / authority layer:
  - supervisor lifecycle for the messaging service binary;
  - in-process or supervised-HTTP routing of the `message-envelope.v1`
    Artifact Delivery acceptor to the messaging service;
  - host capability bridge for `capability.passport.lookup`,
    `capability.passport.issue`, `memarium.write`, `notification.create`,
    `local-contacts.*`, and `local-recipient-mailbox.resolve`;
  - policy evaluation for which supervised service may call each host
    capability, using the existing Capability Binding and middleware
    caller-binding machinery;
  - the `/admin/messaging` operator UI surface;
  - the `/v1/messaging/status` proxy reading service state.

- **Messaging service** (Rust supervised HTTP middleware, recommended) owns
  the domain:
  - Layer 1 Maildir body store under
    `<node-data-dir>/storage/messaging/maildir/...`;
  - Layer 2 middleware-owned SQLite operational index at
    `<node-data-dir>/storage/messaging/index.sqlite`, with rows for
    mailbox id, message id, from, to, date, subject, threading id,
    flags, size, Maildir path, plus optional FTS5;
  - the inbound acceptor that runs the three messaging-specific scope
    checks plus the `contacts`-class policy gate and local recipient
    mailbox resolution;
  - the outbound message queue with its state machine, queue scanner,
    and passport attachment;
  - the inbox projection feeding the mailbox view;
  - construction of AD delivery envelopes using either
    `selector/kind = "contact-lookup"` (preferred) or a normal
    `routing-subject` / `node` selector after a middleware-side direct
    lookup;
  - writing the bounded Layer 3 messaging-fact stream through the
    Memarium host capability;
  - calling `notification.create` for arrival notifications with a
    `mailbox/open` action target.

Compose UI is a Node UI surface that calls into the messaging service.
The middleware does not embed its own browser stack.

The host boundary is intentionally thin. The daemon does not parse message
threads, flags, mailbox search, or contact relationship semantics beyond
the authority decisions it already owns. Conversely, the messaging service
does not fetch peer endpoints, verify TLS evidence, maintain revocation
freshness, or issue arbitrary passports on its own. It asks the host for
those things through explicit capabilities.

### 2. Stratified Storage

Inbound and outbound message state is stratified across three layers,
each holding a different class of data with its own write rate and
lifecycle. The layering was sketched in story-010 §11; this proposal
freezes it.

```text
incoming message envelope
  -> Maildir body file                          (Layer 1: immutable per-message bytes)
  -> messaging-service SQLite operational index (Layer 2: rebuildable hot state)
  -> Memarium messaging facts                   (Layer 3: bounded semantic / audit facts)
  -> inbox projection                           (read model fed by Layers 1+2)
```

**Layer 1 — Maildir bodies.** Immutable for the life of the message.
Owned by the messaging service. Not part of Memarium custody by default;
the file system is the right primitive for opaque per-message blobs.

**Layer 2 — Messaging-service-owned SQLite operational index.** Hot
operational state: per-message rows, `mailbox/id`, optional FTS5,
thread joins, read / unread, snooze, starring. Fully rebuildable from
Layer 1 bodies plus the Layer 3 fact stream. The service is allowed to
vacuum, shard, or fully rebuild Layer 2 without coordinating with any
other module.

**Layer 3 — Memarium messaging facts.** Bounded by user and policy
decisions, not by message traffic. The enumerated fact kinds are:

- `contacts.membership-changed.v1` — sender subject added, removed, or
  rotated within `contacts`;
- `messaging.passport-issued.v1` and `messaging.passport-revoked.v1` —
  joined with the existing revocation feed;
- `messaging.classification-decided.v1` — per-conversation or
  per-message classification (`classification.v1` already lives in
  Memarium);
- `messaging.retention-decided.v1` — deletion reason, archival export
  pointer;
- `messaging.crisis-marked.v1` — explicit crisis-space mark the user
  applies to a thread or message.

Layer 3 uses separate fact schemas for these domain events. MVP MUST NOT
introduce a catch-all `messaging.fact.v1` wire artifact with a generic
`fact/kind` switch.

Per-message header rows and `read / unread` flags **must not** end up
in Layer 3.

The bounding rule, in one line:

> If the field is rewritten more often than once per message lifetime
> (read / unread flips, sort keys, thread membership), it stays in
> Layer 2. If it is a user-or-policy decision with non-zero audit
> weight, it goes to Layer 3. Bodies stay in Layer 1.

### 3. `message-envelope.v1` Artifact

The wire envelope carrying a personal message between nodes:

```text
message-envelope.v1
  schema                    # "message-envelope.v1"
  schema/v                  # "1"
  envelope/id               # ULID-like stable id
  message/id                # opaque per-message id (= envelope/id in MVP)
  thread/id?                # optional threading group id
  sender/subject            # participant | nym | routing-subject (matches passport scope.sender)
  receiver/route            # node:did:key:..., routing:did:key:..., or contact-nym:... (matches passport scope.receiver)
  receiver/public-handle?   # external searchable handle used for discovery, e.g. marcin@example.org
  authorization
    passport-ref?           # canonical ref to a cached capability-passport.v1
    passport?               # inline capability-passport.v1 (preferred for first contact)
    delegation-proof?       # inline DelegationProof when sender uses a delegated nym
  body
    content-type            # text/plain | text/markdown | application/json (MVP set)
    encoding                # "utf-8" | "base64" (latter for opaque payloads)
    size/bytes
    sha256                  # required, byte-identity over body content
    inline?                 # body bytes for small messages
    ref?                    # artifact-store: or similar for larger bodies
  meta
    sent/at                 # ISO-8601
    content/digest          # canonical digest covering id + sender + receiver + body sha256
    classification?         # optional classification.v1 hint
  signature
    key/public              # sender subject signing key
    value                   # signature over the canonical payload
```

The MVP profile requires only `schema`, `schema/v`, `envelope/id`,
`sender/subject`, `receiver/route`, `authorization`, `body`,
`meta.sent/at`, `meta.content/digest`, and `signature`. All other fields
are optional.

The body MAY be inline for short messages or referenced via an existing
AD resolver scheme (`artifact-store:` for local pre-staged blobs) for
larger payloads. End-to-end encryption of the body is out of scope for
MVP; the private-direct INAC transport already provides
sender-authenticated transport confidentiality on the wire.

`receiver/public-handle` is deliberately receiver-side. It records the
external searchable handle the sender used to discover the route, such
as `marcin@example.org` or a phone number digest/presentation accepted
by the Contact Catalog profile. It is not Daniel's email address.
Daniel's own display or sender handle belongs to the contact-request /
local address book layer and should not be copied into every message
unless a later profile explicitly needs it.

`receiver/public-handle` is not a participant/nym correlation oracle. If
the receiver is addressed by a participant-bound route, the route remains
authoritative for mailbox delivery; the public handle can be mapped,
verified, or marked suspicious locally, but it must not be used to prove
or disprove the receiver route to the sender.

### 4. `messaging-receive@v1` Passport Profile

The passport profile minted by Solution 025 Contact Request Admission on
acceptance, and the same profile consumed by the messaging acceptor on
inbound. Frozen here:

```text
capability_id     = "messaging-receive"
profile/v         = "1"
scope
  receiver        # node:did:key:..., routing:did:key:..., or contact-nym:... (MVP excludes participant:did:key)
  sender          # participant | nym | routing-subject of the accepted sender
  public_handle?  # the contact handle Daniel used to reach Marcin, when known
  contact-request # contact-request.v1/id that motivated this passport
  purpose         # "messaging" (MVP fixed value)
expires/at        # required
revocation/ref    # required; canonical ref into the daemon revocation feed
limits?
  rate/per-day?   # per-class messaging rate limit (default: unbounded for MVP)
  body/max-bytes? # per-class body size limit (default: 1 MiB for MVP)
issuer
  participant     # Marcin's participant id (issuer of the receive consent)
  delegation?     # optional issuer DelegationProof when minted via a proxy key
signature
  key/public      # matches issuer.participant (or issuer.delegation proxy)
  value
```

Three properties of this profile matter:

1. MVP `scope.receiver` is never the raw `participant:did:key`. It is a
   `node:did:key:...` for node-level direct delivery, a
   `routing:did:key:...` (per `routing-subject-binding.v1`), or a
   pairwise `contact-nym` (per P058). Participant-specific delivery
   should prefer routing subjects or contact nyms; node-id delivery is
   treated as node-level unless local recipient mailbox resolution below
   can bind it to a participant-controlled public handle. If a later
   participant-direct profile admits `participant:did:key` as a receiver,
   it follows the same participant-bound mailbox rule as `contact-nym`.
2. `scope.sender` may be a participant (most stable) or a nym
   (privacy-preserving). Nym rotation is supported through the
   `key-delegation.v1` grant label defined below.
3. `contact-request` ties the consent to the specific request, so revoking
   the contact request also unambiguously revokes the messaging consent.

### 5. `key-delegation.v1` Grant Label for Delegated Messaging Signing

Daniel's nym-rotation continuity uses the existing inline
`DelegationProof` path. This proposal adds one grant label to the Key
Delegation Passports grant vocabulary:

```text
signing/messaging-send
```

Semantics: a participant authorizes a proxy key to sign
`message-envelope.v1` artifacts on its behalf. When Daniel rotates a
messaging nym, the new nym presents an inline `DelegationProof` rooted in
the participant that Marcin accepted. The messaging acceptor verifies
the proof and treats the message as sent by the accepted participant.
No re-approval ceremony is needed.

### 6. Inbound Acceptor and the Messaging-Specific Checks

The messaging acceptor registers exactly one acceptor target for the
`message-envelope.v1` artifact kind through one of the existing
`artifact_delivery_acceptors.*` surfaces:

- `artifact_delivery_acceptors.supervised_http` (recommended for the
  Rust messaging service);
- `artifact_delivery_acceptors.in_process` (for the MVP fallback that
  runs entirely inside the daemon);
- `artifact_delivery_acceptors.json_e_flow` (for compositional
  experimentation, not the production path).

Generic AD admission already enforces:

- the passport signature is valid (Capability Binding);
- the passport has not expired or been revoked (Capability Binding +
  Seed Directory revocation feed);
- the transport session is authenticated and pinned to attested endpoint
  certificate evidence (TLS Trust Policy);
- size, rate, and idempotency limits hold (AD route policy + INAC
  receiver-side budgets).

The messaging acceptor adds **three messaging-specific scope checks plus
one policy gate**:

1. `sender ↔ scope.sender`: the `sender/subject` field in the envelope
   matches the `scope.sender` field in the presented passport. When the
   sender presents a delegated nym, the inline `DelegationProof` must
   resolve to a subject equal to `scope.sender`.
2. `receiver ↔ scope.receiver`: the `receiver/route` field matches the
   `scope.receiver` field in the passport.
3. `receiver/public-handle ↔ scope.public_handle`: when the envelope
   carries `receiver/public-handle`, it matches `scope.public_handle`.
   When absent on either side, the check is skipped.
4. **`contacts`-class policy gate**: the resolved `sender/subject`
   must still be a member of the local `contacts` set (no revocation
   on Marcin's side) and the per-class limits (`limits.*` in the
   passport) must not be exhausted.

If any check fails, the acceptor refuses admission before invoking
persistence. Refusal classes are first-class operator-visible audit
events.

#### Recipient Mailbox Resolution

After the acceptor has passed AD, passport, scope, and `contacts`
policy checks, the messaging service resolves the local mailbox that
will receive the message. This is a local projection decision; it does
not grant authority and it must not weaken the admission checks above.

For an inbound message addressed to a node-level or non-participant-bound
receiver (`node:did:key:...` or a routing subject that does not locally
resolve to exactly one participant mailbox):

- if the envelope does not carry `receiver/public-handle`, the message
  goes to the node operator mailbox;
- if the envelope carries `receiver/public-handle`, the service asks the
  host to resolve that handle against local, attested, participant-owned
  public identity mappings;
- if the host returns exactly one local participant mailbox whose
  mapping is still backed by a valid `email-control@v1` /
  `phone-control@v1` passport or equivalent Contact Catalog admission
  evidence, the message goes to that participant mailbox;
- if the host cannot resolve the handle, the evidence is stale or
  revoked, or the mapping is ambiguous, the message goes to the node
  operator mailbox with an operator-visible reason.

The service MUST NOT infer a participant mailbox merely because the
receiver route is locally known. A bare node id or routing subject is a
network delivery target, not a mailbox owner. `receiver/public-handle`
is the intentional user-facing selector for participant mailbox routing
for these routes.

For an inbound message addressed to a participant-bound route, such as a
pairwise `contact-nym` or a future explicit `participant:did:key`
direct-addressing profile, the resolved participant is authoritative for
mailbox delivery. If the envelope also carries `receiver/public-handle`,
the host may verify whether that handle is locally attested for the same
participant and return a local `public-handle/status`, but the messaging
service MUST NOT reject with a sender-visible `user unknown` solely
because the public handle is absent, stale, unknown, or not attested for
that participant. Otherwise a sender could probe whether a nym belongs
to a known email address or phone number.

Pairwise `contact-nym` receivers resolve through the local `contacts`
membership projection. If that projection is absent or ambiguous, the
same operator-mailbox fallback applies.

The local mapping is owned by the daemon / Contact Catalog authority
layer, not by the messaging service. It may be backed by canonical route-set
`contact-claim.v1` records, the local contact store, `PassportCache`,
and participant vault records, but the messaging service sees only the
bounded host-capability response.

The acceptor MUST treat `envelope/id` as the idempotency key for
receiver-side persistence. Replaying the same accepted envelope may repair
Layer 2 / Layer 3 side effects, but it must not create a second Maildir
message. If a replay presents the same `envelope/id` with different body
digest, sender, receiver, or authorization material, the acceptor refuses it
as an identity conflict.

### 7. Outbound Queue State Machine

The outbound message queue is owned by the messaging service. The
canonical state machine:

```text
composed
  -> waiting-for-route       # recipient is an external contact handle, no route yet
  -> waiting-for-contact-permission
  -> ready-for-delivery
  -> in-flight
  -> delivered
  -> failed-terminal
```

`draft` is not part of this protocol state machine. Draft editing may live
in Node UI local state or in a future draft store. The queue begins at
`composed`, after the user has asked the service to send.

State transitions:

- `composed → waiting-for-route` when the recipient is an external
  contact handle that does not yet resolve to a local known contact.
- `waiting-for-route → waiting-for-contact-permission` after the
  Contact Catalog lookup returns a route candidate but no
  `messaging-receive@v1` passport for that sender↔receiver pair is yet
  cached.
- `waiting-for-route → ready-for-delivery` shortcut when the recipient
  is a known local contact and a usable passport is already cached.
- `waiting-for-contact-permission → ready-for-delivery` when a usable
  passport arrives via `capability.passport.lookup` (queue scanner
  attaches it).
- `ready-for-delivery → in-flight` when the AD delivery envelope is
  accepted by the host (typically returns a `delivery/id` for tracking).
- `in-flight → delivered` on successful AD admission on the receiver
  side (tracked via AD `deferred-operation` or recovery worker).
- `in-flight → failed-terminal` on AD recovery exhaustion.

The queue scanner runs whenever a new passport is added to
`PassportCache`. It looks up messages in `waiting-for-contact-permission`
that match the freshly arrived passport's `scope.sender ↔ scope.receiver`
pair and promotes them to `ready-for-delivery`.

The first implementation may support only a single recipient per envelope.
Group messaging, CC/BCC-like fan-out, and shared conversation state are
post-MVP because they require different consent and key-management rules.

### 8. `contacts` Relationship Class

The messaging service owns the local `contacts` relationship-class set,
with the following invariants:

- Membership is keyed by the accepted sender subject (participant, nym,
  or routing subject), not by handle.
- Default policy is "may send messages to me". No other capability is
  implicitly granted.
- Membership is bi-directionally projected with issued
  `messaging-receive@v1` passports: issuing a passport adds (or
  refreshes) membership; revoking the passport removes membership and
  emits a `contacts.membership-changed.v1` fact into Layer 3.
- Per-class limits (`rate/per-day`, `body/max-bytes`, sender allow /
  deny overrides) are local policy that the messaging acceptor enforces
  alongside the passport's own `limits.*`.
- Membership state is mirrored into `pseudonym-vault.v1` (P059) so it
  survives node reinstall from the participant mnemonic.

`contacts` is intentionally narrower than `friends`. Adding a sender to
`contacts` never silently grants friend-class capabilities. The class
distinction is documented for INAC middleware configuration generally,
not only for messaging.

`contacts` membership is not the same row as a human address-book entry.
The messaging service owns the canonical relationship for receive consent.
The daemon-owned local contact store may hold labels, raw handles, pairwise
nym mappings, and an optional UX projection of the relationship, but it is
not the source of truth for messaging consent.

### 9. Recovery and Vault Integration

Three classes of state need recovery treatment:

- **Maildir bodies (Layer 1)** are backed up like any file storage. Loss
  causes user data loss but does not break the protocol. A future
  archivist handoff (P012) MAY package Maildir bodies as
  `memarium-blob.v1` bundles; this is optional.
- **SQLite operational index (Layer 2)** is **not** backed up. It is
  fully rebuildable from Layer 1 plus the Layer 3 fact stream. This is
  the point of stratification.
- **Layer 3 Memarium facts** are backed up through the existing Memarium
  archival path.
- **`contacts` membership + issued `messaging-receive@v1` passports**
  live inside `pseudonym-vault.v1` (P059), so mnemonic-based restore
  brings back both signing material and policy state. The messaging
  service queries the vault on startup to reconstruct its `contacts`
  set and reissue / re-validate passports.

The recovery story for the SQLite operational index is: on first
startup after restore, replay Layer 3 messaging facts to recreate
`contacts` membership and known passports; walk the Maildir tree to
populate per-message rows; rebuild the FTS5 index; surface a
"reindexing" status through `/v1/messaging/status` until done.

MVP retention default is keep-local / no automatic purge:

- Layer 1 Maildir bodies stay until an explicit user or operator delete /
  archive action.
- Layer 2 rows live while the corresponding Maildir body exists; they are
  derived state and may be removed, vacuumed, or rebuilt at any time.
- Layer 3 facts follow Memarium retention and classification policy. A
  concrete removal / archival choice is recorded as
  `messaging.retention-decided.v1`.

## Daemon vs Service Boundary

This proposal explicitly stratifies the messaging middleware between
two co-located subsystems, following the precedent established for
Contact Catalog (P058 §11 Catalog Provider Role).

**Node daemon** owns the small host / authority layer:

- supervisor lifecycle for the messaging-service binary;
- `message-envelope.v1` Artifact Delivery acceptor routing (either
  in-process to the service or supervised-HTTP proxy);
- host capability bridge: `capability.passport.lookup`,
  `capability.passport.issue`, `memarium.write`, `notification.create`,
  `local-contacts.read`, `local-recipient-mailbox.resolve` (per
  Solution 025 daemon-owned contact and claim state);
- `/admin/messaging` operator UI surface;
- `/v1/messaging/status` proxy.

**messaging-service** (separate process / supervised middleware) owns
the domain:

- Layer 1 Maildir body store under
  `<node-data-dir>/storage/messaging/maildir/...`;
- Layer 2 middleware-owned SQLite operational index;
- the inbound acceptor running the three scope checks +
  `contacts`-class policy gate and recipient mailbox resolution;
- the outbound queue + state machine + scanner + passport attachment;
- the inbox projection feeding the mailbox view;
- AD delivery envelope construction;
- writing Layer 3 messaging facts through Memarium host capability;
- arrival notifications via `notification.create` with a `mailbox/open`
  action target.

This split is what the user pays for in stratification: daemon stays a
small host / authority that does not learn messaging-domain semantics;
the service owns the domain and may be evolved independently. Compose
UI is a Node UI surface that calls into the service through host
capability and operator HTTP routes.

## Host Capability Contracts Needed by Messaging

The messaging service should use existing host capability patterns wherever
possible. The MVP host bridge needs these calls:

| Capability | Owner | Used for |
| :--- | :--- | :--- |
| `artifact.delivery.send` | daemon / Artifact Delivery | Submit `message-envelope.v1` for `private-direct` delivery. |
| `capability.passport.lookup` | daemon / Capability Binding | Find a usable `messaging-receive` passport for an outbound queue item. |
| `capability.passport.issue` | daemon / Capability Binding | Issue or refresh local passports only through already authorized action paths; ordinary outbound sending should not call this. |
| `memarium.write` | daemon / Memarium | Append Layer 3 messaging facts. |
| `notification.create` | daemon / Notifications | Create inbound-message and delivery-status notifications. |
| `local-contacts.read` | daemon / Contact Catalog local store | Resolve local contact labels and route hints. |
| `local-contacts.write` | daemon / Contact Catalog local store | Optional MVP write path for adding a newly accepted contact projection. |
| `local-recipient-mailbox.resolve` | daemon / Contact Catalog local claim store + Capability Binding | Resolve an accepted inbound receiver route to the node operator mailbox or a participant mailbox without turning public handles into sender-visible correlation tests. |
| `pseudonym-vault.read` / `pseudonym-vault.write` | daemon / Solution 026 | Restore and persist `contacts` membership and issued passport references. |

`capability.passport.lookup` is the only new host capability that blocks the
outbound queue from being clean. Its MVP request shape can be small:

```text
capability.passport.lookup
  capability_id = "messaging-receive"
  required_scope
    sender
    receiver
    public_handle?
    purpose = "messaging"
  freshness
    require_revocation_fresh = true
  now
```

The response is either:

```text
usable-passport
  passport-ref
  passport?
  expires/at
  revocation/ref
```

or a refusal such as `not-found`, `expired`, `revoked`,
`revocation-view-stale`, or `scope-mismatch`. The lookup capability does not
mint authority; it only selects an already valid passport under the host's
current revocation view.

`local-recipient-mailbox.resolve` is the inbound counterpart for mailbox
routing, not for admission:

```text
local-recipient-mailbox.resolve
  receiver_route            # node:did:key:..., routing:did:key:..., contact-nym:..., or future participant-direct receiver
  public_handle?            # from receiver/public-handle
  purpose = "messaging"
  freshness
    require_control_passport_fresh = true
    require_revocation_fresh = true
```

The response is either:

```text
participant-mailbox
  participant
  mailbox/id
  resolution/source          # contact-nym | participant-direct | public-handle-mapping
  public-handle/status?      # absent | mapped | verified | unverified | mismatch | stale | revoked
  public-handle/ref?
  contact-claim/ref?
  control-passport/ref?
```

or:

```text
operator-mailbox
  mailbox/id = "operator"
  reason = no-public-handle | unknown-public-handle | stale-evidence | revoked | ambiguous | no-recipient-owner
```

The messaging service stores the returned `mailbox/id` in Layer 2. Raw
public handles remain daemon-local except for the optional
`receiver/public-handle` already present in the sender-provided envelope.
`mapped` means a daemon-local contact row selected a mailbox, but the host
has not asserted fresh public-handle control evidence for that row.
For participant-bound routes, `public-handle/status` is local diagnostic
context; it must not become a sender-visible delivery oracle.

## Relationship to Existing Mechanisms

### Artifact Delivery (Solution 023)

The messaging service registers exactly one inbound acceptor for
`message-envelope.v1` through `artifact_delivery_acceptors.*`. Outbound
messages use either the `contact-lookup` recipient selector kind
(P058-019, `done`) or a normal `routing-subject` / `node` selector after
a middleware-side direct catalog lookup. The `privacy = private-direct`
invariant applies; today's private-safe adapter is `inac-direct`.

### INAC (Solution 017)

INAC is the private/direct transport adapter under AD. The messaging
service does not speak INAC directly; AD routes the
`message-envelope.v1` push.

### Capability Binding (Solution 006) and Key Delegation Passports (Solution 014)

Capability Binding verifies passport signature, expiry, and revocation
freshness before the acceptor is invoked. Key Delegation Passports
provides the inline `DelegationProof` path for nym-rotation continuity.
This proposal adds one grant label, `signing/messaging-send`.

### Contact Catalog (Solution 025) and Proposal 058

Contact Catalog owns: contact discovery (Invitation-Only Lookup),
contact-claim admission, the `contact.request` acceptor, durable
`contact-request.received` notifications, and `messaging-receive@v1`
passport issuance. The messaging middleware *consumes* the issued
passports and does not duplicate any of those responsibilities.

The contact-lookup recipient selector kind (P058-019) is the preferred
outbound integration; middleware-side direct HTTP is the alternative.
The same daemon-owned Contact Catalog state is the natural source for
local public-identity mappings used by inbound mailbox resolution. That
projection is local authority state, not a network lookup performed by
the messaging service.

### User and Operator Notifications (P057)

The messaging service uses `notification.create` for:

- inbound message arrival, with a `mailbox/open` action that opens the
  mailbox view focused on the new message;
- delivery confirmations or failures, when the user opted into them.

The contact-request notification flow is owned by Solution 025; this
proposal does not duplicate it.

For MVP, Node UI owns mailbox rendering and handles `mailbox.open`.
The messaging service exposes structured read APIs or supervised HTML
fragments only as an implementation convenience; the durable notification
action target remains a stable action ref, not an embedded UI contract.

### Memarium (Solution 002, Proposal 036) and Classification (Proposal 047)

The messaging service writes the bounded Layer 3 fact stream through
the Memarium host capability. `classification.v1` decisions reuse the
existing Memarium classification path. Memarium does not learn
per-message header semantics; only the enumerated semantic facts cross
the boundary.

### Solution 019 Middleware

The messaging service attaches through the supervised-HTTP / in-process
host capability bridge already provided by Solution 019. No new
extension-host primitive is introduced.

### Proposal 059 (Nym key-role derivation) and Solution 026

`contacts` membership and issued `messaging-receive@v1` passports live
inside `pseudonym-vault.v1`. Proposal 059 is Accepted with Node MVP
runtime implemented; Solution 026 (Pseudonym Vault and Key Roles)
realises the runtime — sealed vault snapshots, role-aware recovery
bundles, single-writer latest with rollback and conflict rejection. The
messaging service writes membership and passport records as private
plaintext entries inside vault snapshots, and replays them on startup.
No degraded-mode fallback is needed.

### `core/messaging` Capability

`core/messaging` is the protocol-native baseline peer messaging /
session capability. It is mandatory for every node, used by the peer
handshake. It is **not** an application messaging middleware. This
proposal adds a separate application capability id.

### New Capability Ids Introduced

- `messaging-send` (`app/messaging-send`) — application capability id
  for sending personal messages. Used by `key-delegation.v1` grant
  `signing/messaging-send`. The capability id and signing grant are
  registered; concrete passport issuance/use is part of the sender-side
  messaging path.
- `messaging.contact-request` `notification/kind` — already registered
  implicitly by Solution 025; this proposal restates the dependency.
- `mailbox.open` `notification/action` — new action target wired by the
  messaging service and dispatched into the Node UI mailbox view.

## MVP Decisions

These decisions answer the open questions for the first implementation
slice. They can be revisited later without changing the stratified
boundary.

| Area | MVP decision | Later extension |
| :--- | :--- | :--- |
| Compose UI ownership | Node UI owns compose and mailbox screens; it calls the messaging service through daemon-proxied HTTP or host capabilities. | Service-rendered fragments may be added later if Node UI wants to delegate rendering. |
| Threading | `thread/id` is optional and opaque. Replies may set it to the root `message/id`; no RFC-style reply graph in MVP. | Rich conversation containers and reply DAGs. |
| Content types | `text/plain` and `text/markdown` are admitted. `application/json` is allowed only for explicitly typed system/test messages. `text/html` is deferred. | Sanitized HTML profile. |
| Body at rest | Maildir bodies are stored as ordinary files under the node data directory. At-rest encryption is delegated to OS/user-disk policy in MVP. | Per-message sealed body profile using participant/vault wrapping. |
| Limits | Messaging acceptor enforces `limits.*`; AD route policy enforces coarse body-size and route budgets before the acceptor. | Shared policy registry if duplication becomes costly. |
| Cross-device sync | Deferred. Layer 2 flags are local operational state. | `messaging.flag.v1` or similar sync artifact. |
| Mailbox view | Node UI renders mailbox views from `/v1/messaging/*`. | Service-owned fragments if useful. |
| Receiver public handle | `receiver/public-handle` is optional for admission. If absent on node-id / non-participant-bound routing-subject delivery, the accepted message is routed to the operator mailbox. Participant-bound routes deliver to the participant resolved from the route; a supplied public handle is mapped, verified, or marked suspicious locally, never used as a sender-visible `nym -> email/phone` test. | Later profiles may require the public handle for selected mailbox policies or derive mailbox ownership from stronger private presentations, but must preserve the anti-oracle property. |
| Layer 3 fact schemas | Messaging-owned Layer 3 events use separate schemas per fact kind: `contacts.membership-changed.v1`, `messaging.passport-issued.v1`, `messaging.passport-revoked.v1`, `messaging.retention-decided.v1`, and `messaging.crisis-marked.v1`. Shared envelope conventions are allowed, but MVP does not introduce `messaging.fact.v1` as a catch-all wire artifact. `classification.v1` remains the reusable classification artifact. | A future aggregation/read-model envelope may summarize these facts without replacing the canonical schemas. |
| Contacts storage boundary | The messaging service owns canonical `contacts` membership for receive consent. The daemon-owned local contact store may hold labels, raw handles, pairwise mappings, and an optional projection; `pseudonym-vault.v1` mirrors the private recovery state. | A future UX may merge address-book and contacts views while preserving the consent source of truth. |
| Retention defaults | MVP uses keep-local / no automatic purge. Maildir bodies stay until explicit delete or archive; Layer 2 rows live while bodies exist and are rebuildable; Layer 3 facts follow Memarium retention plus explicit `messaging.retention-decided.v1`. | User/operator retention profiles, auto-expiry, and archival handoff policy. |
| Inline body threshold | Inline body is allowed up to 64 KiB in MVP; larger bodies use `artifact-store:`. Receiver policy may set a lower limit. | Streaming / attachment-specific profile. |
| Failed-terminal recovery | User may retry, which creates a new delivery attempt for the same `envelope/id` if the content is unchanged; editing creates a new envelope. | Rich retry scheduling and per-recipient partial success. |

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| Sender forges `sender/subject` | The messaging acceptor enforces sender ↔ `scope.sender` match against the presented passport; Capability Binding already verified passport signature and revocation. |
| Sender uses a rotated nym | Inline `DelegationProof` rooted in the accepted participant; the messaging acceptor verifies the proof and treats the message as sent by the accepted subject. |
| Receiver route does not match accepted route | The messaging acceptor enforces receiver ↔ `scope.receiver` match and refuses before persistence. |
| Public handle drift (handle reassigned externally) | The messaging acceptor enforces `receiver/public-handle` ↔ `scope.public_handle` when the envelope carries the receiver handle; absent handles skip the check. Handle reassignment is mitigated upstream by Contact Catalog claim revocation (P058-011). |
| Direct node/routing-subject message cannot be bound to a local participant mailbox | The accepted message goes to the node operator mailbox with a structured reason; the service does not guess mailbox ownership from route familiarity. |
| Public handle used as a nym correlation probe | Participant-bound receiver routes ignore the public handle for sender-visible admission and mailbox ownership. The host may return a local `public-handle/status`, but mismatch or unknown status does not produce a sender-visible `user unknown`. |
| Operational index (Layer 2) corruption | Layer 2 is rebuildable from Layer 1 bodies plus Layer 3 fact stream; the service surfaces a "reindexing" status while it rebuilds. |
| Memarium fact volume bloats with traffic | Layer 3 is bounded to user / policy decisions, not per-message rows. The bounding rule is enforced at write time; rows that fail the rule are refused at the messaging service before reaching the Memarium host capability. |
| Mailbox view opens before reindex completes | `/v1/messaging/status` exposes a `reindexing` flag; Node UI surfaces a banner and may render partial mailbox views from whatever Layer 2 is already populated. |
| Daniel sends before consent | The message remains in the outbound queue at `waiting-for-contact-permission` until a usable passport arrives; AD is never invoked. |
| Daniel sends with a passport but Marcin revoked it mid-flight | The receiver-side Capability Binding revocation check fails closed; the message is refused at AD admission before the messaging acceptor sees it. |
| `messaging-receive@v1` passport scope and envelope disagree | The messaging acceptor refuses; the refusal is operator-visible as an audit event. |
| Service crashes mid-write | Layer 1 Maildir write is the durable commit point; Layer 2 / Layer 3 updates are idempotent on retry, keyed by `envelope/id`. |
| Vault unavailable during startup | Vault runtime is owned by Solution 026 and is `done`; the messaging service treats vault unavailability as a transient daemon condition and waits, surfacing the wait state through `/v1/messaging/status`. New memberships are queued until the vault accepts a snapshot. |
| `contact-request` revoked after acceptance | Revoking the `messaging-receive@v1` passport on Marcin's side propagates through Capability Binding revocation and `contacts.membership-changed.v1` fact in Layer 3. |

## Trade-offs

### Benefits

- One named domain module ties together every existing primitive
  (passports, INAC, AD, Memarium, notifications, Contact Catalog) into a
  story-shaped flow without inventing new transport or admission
  semantics.
- Stratified storage (Layer 1 / Layer 2 / Layer 3) keeps high-volume
  operational state out of Memarium and out of any backup that doesn't
  need it.
- The `contacts` relationship class is local-first and explicitly
  narrower than `friends`, preserving the "scoped acceptance" property
  Marcin wants in story-010.
- Nym-rotation continuity reuses the existing inline `DelegationProof`
  path; no bespoke renewal flow.
- Daemon stays a small host / authority that does not learn
  messaging-domain semantics; the service owns the domain.

### Costs

- New state to maintain: outbound queue, `contacts` set, Layer 2 index,
  Layer 3 fact stream, mailbox projection.
- More moving parts at startup: the service must coordinate with the
  vault, Memarium, the daemon's host capability bridge, AD acceptor
  registration, and Node UI.
- Recovery scenarios multiply: lose-bodies, lose-index, lose-vault each
  produce a different recovery posture.

## Open Questions

No MVP-blocking open questions remain after the decisions above.

## Recommended Implementation Slices

Implementation should proceed in thin vertical slices that preserve the
daemon/service boundary and reuse existing primitives.

### Slice 1: Inbound Local Accept and Store

Goal: prove that `message-envelope.v1` can be admitted and stored without
building compose UI or contact lookup.

Deliverables:

- `message-envelope.v1` schema and positive/negative examples;
- in-process or supervised-HTTP AD acceptor registration for
  `message-envelope.v1`;
- acceptor validation for body digest, signature shape, idempotency, and
  the three scope checks against a supplied `messaging-receive` passport;
- Layer 1 Maildir write;
- minimal Layer 2 SQLite row insert;
- `/v1/messaging/status` exposing ready / degraded / reindexing state.

This slice may use a fixture passport and a direct `node` or
`routing-subject` selector. It should not depend on compose UI, Contact
Catalog lookup, or outbound queue scanning.

### Slice 2: Contacts and Passport Lookup

Goal: make consent local and queryable.

Deliverables:

- `contacts` membership table or store inside the messaging service;
- `capability.passport.lookup` host capability with the MVP request /
  response shape from this proposal;
- `local-recipient-mailbox.resolve` host capability with the MVP request /
  response shape from this proposal;
- `contacts` gate in the inbound acceptor;
- recipient mailbox resolution for operator vs participant mailboxes;
- Layer 3 fact writes for membership changes and passport issuance /
  revocation, using either the final fact schemas or a temporary internal
  event shape clearly marked as non-wire.

This slice turns acceptance from "passport shape matches" into "passport
and current local relationship policy both match".

### Slice 3: Outbound Queue and AD Send

Goal: send a message to an already known route.

Deliverables:

- outbound queue table and state machine;
- queue scanner triggered by passport arrival or explicit retry;
- AD delivery envelope construction with `privacy = private-direct`;
- transition handling for `ready-for-delivery`, `in-flight`,
  `delivered`, and `failed-terminal`;
- arrival notification using `notification.create` and `mailbox.open`.

This slice still does not require external handle lookup. The recipient can
be a known `routing-subject` or `node` target with a cached passport.

### Slice 4: Contact Catalog Integration

Goal: support story-010's "type `marcin@example.org`" path.

Deliverables:

- recipient parser that distinguishes known local contacts from external
  contact handles;
- `waiting-for-route` and `waiting-for-contact-permission` transitions;
- preferred AD `selector/kind = "contact-lookup"` integration, or the
  middleware-side direct `POST /v1/contact-catalog/lookups` fallback;
- contact-request handoff reuse from Solution 025;
- queue promotion when the resulting `messaging-receive` passport appears.

This slice should not duplicate Contact Catalog admission or contact-request
accept/reject semantics. It only consumes the result.

### Slice 5: Mailbox UX and Recovery

Goal: make the feature usable and repairable.

Deliverables:

- Node UI compose, inbox, message detail, and notification target;
- Layer 2 rebuild command / startup path;
- vault integration for `contacts` membership and issued passport refs;
- Memarium-backed Layer 3 facts promoted from temporary event shapes to
  stable schemas if Slice 2 used a temporary shape.

This is the first slice where operator polish matters. Earlier slices should
prefer contract tests and daemon/service boundaries over UI completeness.

## Next Actions

1. Keep `message-envelope.v1` schema examples and Node `schema-gate`
   validators synchronized while service-side admission evolves.
2. Keep the `messaging-send` Capability Registry row synchronized with
   node-side capability constants.
3. Keep the `signing/messaging-send` grant label synchronized with
   Solution 014 Key Delegation Passports and node-side delegation constants.
4. Harden outbound contact-request/message signing fixtures with a full
   mock-host integration test that verifies signer-derived sender identity,
   Pseudonym Vault reply-route creation, and Artifact Delivery payloads.
5. Complete receiver-side revocation-view coverage and supervised cross-node
   acceptor tests for inbound messaging admission.
6. Extend sealed `pseudonym-vault.v1` recovery beyond the current
   local-contact import/root-only startup replay into passphrase-unlock
   startup UX and receive-passport membership restoration.
7. Add remote Memarium replay to the Layer 2 `reindex` rebuild path.
8. Keep MVP decision rows and tracker evidence in sync while hardening the
   remaining runtime and recovery paths.

## Tracking

Status legend: `todo` (no implementation work started), `planned` (design
defined, awaiting implementation), `partial` (partially implemented), `done`
(fully implemented and integrated), `open` (a design decision is still
required before implementation can proceed), `deferred` (explicitly post-MVP
for this proposal). Status values are kept consistent with other tracker
tables in this project (see Proposal 057 §Tracking and Proposal 058
§Tracking for precedent).

| ID | Feature | Status | Evidence |
|---|---|---|---|
| P060-001 | `message-envelope.v1` artifact schema (fields per §3) | done | `doc/schemas/message-envelope.v1.schema.json`, examples, Node protocol mirror, and `schema-gate` validators exist. |
| P060-002 | `messaging-receive@v1` passport profile freeze (scope shape per §4) | done | Solution 027 documents `messaging-receive@v1` as the canonical `MessagingReceiveProfileV1` shape with `request/id`, `sender_subjects`, `recipient_routes`, `contact_nym_id`, `purposes`, revocation freshness default 300 seconds, optional limits, and no second profile shape. Node `capability` rejects alternate `messaging-receive` profile shapes at passport validation time and defaults omitted freshness to 300 seconds. |
| P060-003 | `messaging-send` capability id registration in the Capability Registry | done | Registered in `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md` / `.pl.md` and node `capability` constants as `app/messaging-send`. |
| P060-004 | `signing/messaging-send` grant label added to `key-delegation.v1` grant vocabulary | done | Added to Solution 014 implementation notes/capability sidecar and node `capability` delegation constants. |
| P060-005 | Messaging middleware solution document and capability sidecar | done | `doc/project/60-solutions/027-messaging-middleware/` contains the solution document, implementation notes, and `027-messaging-middleware-caps.edn`; generated capability matrices include the component. |
| P060-006 | Daemon vs service boundary documented (small host/authority layer vs domain service) | done | §1 Component Boundary + Daemon vs Service Boundary section. Mirrors P058 §11 Catalog Provider Role pattern. |
| P060-007 | Stratified storage contract (Layer 1 Maildir, Layer 2 service SQLite, Layer 3 Memarium facts) frozen | done | §2 Stratified Storage with bounding rule; promoted from story-010 §11 sketch. |
| P060-008 | `contacts` relationship class model frozen (local set, default "may send messages to me" policy, bi-directional projection with `messaging-receive@v1` passports) | done | §8 `contacts` Relationship Class. Implementation tracked separately by P060-013. |
| P060-009 | Inbound acceptor: three messaging-specific scope checks + `contacts`-policy gate + recipient mailbox resolution | partial | `messaging-service` exposes `POST /v1/artifact-delivery/accept`, schema/domain validation, digest idempotency, Maildir + SQLite writes, passport scope matching, `contacts` membership projection from presented receive passports, generic `contacts-policy-denied` refusal, host `local-recipient-mailbox.resolve`, and inbound notifications. Passport-ref admission uses `capability.passport.lookup`; inline `messaging-receive@v1` passports now fail closed against the receiver-side revocation snapshot before Maildir/SQLite writes and record `messaging.passport-revoked.v1` on revocation. Missing host capability access refuses passport-based first contact rather than trusting local-only verification. Remaining hardening: broader supervised cross-node acceptor tests. |
| P060-010 | Outbound queue state machine | done | §7 Outbound Queue State Machine; implementation tracked separately by P060-013. |
| P060-011 | Layer 3 messaging-fact kind schemas (`contacts.membership-changed.v1`, `messaging.passport-issued.v1`, `messaging.passport-revoked.v1`, `messaging.retention-decided.v1`, `messaging.crisis-marked.v1`) | done | Schema files, examples where useful, Node protocol mirror, and `schema-gate` export validators exist. Runtime Memarium writes remain tracked by P060-013. |
| P060-012 | `capability.passport.lookup` host capability surface (symmetric counterpart of the existing issue path) | done | Daemon host capability endpoint validates `capability-passport-lookup.v1`, rejects stale revocation views, scans the shared multi-passport `PassportCache`, filters revoked passports, scope-matches typed profiles, and returns usable/refused lookup states. Solution 019 documents it as a stable host capability bridge rather than a messaging-private helper. |
| P060-013 | Messaging service implementation (compose + outbound queue + Layer 1 Maildir + Layer 2 SQLite + inbox projection + acceptor + Layer 3 fact writes) | partial | Node has `messaging-core` and `messaging-service` crates with host capability client, status, inbound accept, outbound enqueue/outbox/retry/process, contact-lookup-result promotion, mailbox/message read endpoints, Maildir message and draft storage, SQLite `PRAGMA user_version` migrations, signer-derived contact-request/message sender identity, Pseudonym Vault reply-route creation, contact-request dispatch through AD, sender-side lookup against a shared remote Contact Catalog provider, passport lookup promotion, `capability.passport.present` receive-passport handoff, signed message-envelope private-direct delivery, kind-specific Layer 3 fact artifacts through `memarium.write`, pending fact replay, retention/crisis fact endpoints, revocation-triggered `messaging.passport-revoked.v1`, reindex, and strict Story-010 two-node delivery smoke coverage. Mock-host coverage now exercises receiver-side revocation snapshot checks and remote Memarium replay. Remaining hardening: fuller outbound signer/AD/notification and failure-class matrices. |
| P060-014 | `mailbox.open` notification action target wired into Node UI mailbox view | done | Messaging inbound notifications include `mailbox.open`; daemon marks the action handled through a host-owned no-domain-mutation target, and Node UI exposes message detail at `/admin/messaging/messages/{message_id}`. |
| P060-015 | `/admin/messaging` operator UI surface and `/v1/messaging/status` daemon proxy | done | Daemon proxies `/v1/messaging/status`, contactability draft/options/attest/publish, outbound, outbox, outbox process, pending-facts replay, reindex, retry, mailbox, and message read/write surfaces; Node UI exposes `/admin/messaging` contactability draft controls, compose, status, inbox, outbox, diagnostics, unknown-recipient warning, and message detail. |
| P060-016 | Recovery: `contacts` membership + issued `messaging-receive@v1` passports persisted in `pseudonym-vault.v1` | partial | `messaging-service` mirrors contacts membership records through the daemon host capability `identity.messaging-recovery.mirror`; the daemon validates accepted record kinds and persists them in a durable local recovery mirror table. The local contact store can now export/replay a recovery bundle covering local contacts, pairwise mappings, and messaging recovery mirror records, and replay refuses to reactivate `revoked` / `archived` pairwise mappings. Sealed vault record persistence and startup replay remain follow-up work. |
| P060-017 | Recovery: Layer 2 SQLite index rebuild procedure (replay Layer 3 → walk Maildir → repopulate rows → rebuild FTS5) | done | `messaging-service` exposes `POST /v1/messaging/reindex` and daemon/UI proxies; the implementation attempts remote Memarium fact replay first via `memarium.read`, records remote replay diagnostics (`stage`, `remote/cursor`, `last/error`), degrades to local sources if Memarium is unavailable, replays locally durable Layer 3 fact projections from `pending_facts`, walks Maildir, repopulates message rows, rebuilds FTS5, and exposes `reindexing`. |
| P060-018 | Compose UI ownership decision (service-embedded HTTP UI vs Node UI surface calling service) | done | MVP Decisions: Node UI owns compose and mailbox screens. |
| P060-019 | Threading model decision (opaque id vs In-Reply-To chain vs richer conversation container) | done | MVP Decisions: optional opaque `thread/id`; replies may use root `message/id`. |
| P060-020 | Body content-type set decision (text/plain + text/markdown + application/json vs adding text/html with sanitization) | done | MVP Decisions: `text/plain`, `text/markdown`, and restricted `application/json`; `text/html` deferred. |
| P060-021 | Body at-rest encryption decision (Maildir bodies plaintext vs sealed by `participant/vault-wrap`) | done | MVP Decisions: ordinary files under node data dir; sealed body profile deferred. |
| P060-022 | Per-class limits enforcement placement (messaging acceptor only vs AD route policy aware) | done | MVP Decisions: coarse AD budgets plus messaging acceptor `limits.*`. |
| P060-023 | Cross-device sync of `read/unread` and other Layer 2 flags | deferred | MVP Decisions: post-MVP; may require `messaging.flag.v1`. |
| P060-024 | Mailbox view rendering ownership (service-rendered fragments vs Node UI server-side render against `/v1/messaging/*`) | done | MVP Decisions: Node UI renders from `/v1/messaging/*`. |
| P060-025 | Attachment handling threshold (inline vs `artifact-store:` ref) | done | MVP Decisions: inline up to 64 KiB; larger bodies use `artifact-store:`. |
| P060-026 | Failed-terminal outbound recovery UX (manual retry vs re-compose) | done | MVP Decisions: unchanged retry keeps `envelope/id`; edits create a new envelope. |
| P060-027 | `receiver/public-handle` policy when passport has `scope.public_handle` or receiver is participant-bound | done | MVP Decisions: optional for admission; absent handle on node-id / non-participant-bound routing-subject delivery routes to the operator mailbox, while participant-bound routes deliver by route ownership and treat public-handle verification as local diagnostic context, not a sender-visible correlation oracle. |
| P060-028 | Layer 3 fact schema shape (generic envelope vs separate schemas) | done | MVP Decisions: separate messaging-owned fact schemas per fact kind; no `messaging.fact.v1` catch-all wire artifact in MVP. |
| P060-029 | `contacts` membership storage boundary vs local-contact row projection | done | MVP Decisions + §8 `contacts` Relationship Class: messaging service owns canonical receive-consent membership; local contacts may project it for UX. |
| P060-030 | Retention defaults for Maildir, Layer 2, and Layer 3 | done | MVP Decisions + §9 Recovery and Vault Integration: keep-local / no automatic purge; Layer 2 remains rebuildable; Layer 3 follows Memarium retention plus `messaging.retention-decided.v1`. |
| P060-031 | Recommended implementation slices | done | **Recommended Implementation Slices** defines five thin slices: inbound local accept/store, contacts + passport lookup, outbound queue + AD send, Contact Catalog integration, mailbox UX + recovery. |
| P060-032 | `local-recipient-mailbox.resolve` host capability and inbound mailbox routing contract | done | Daemon endpoint validates `local-recipient-mailbox-resolve.v1`, uses daemon-owned local participant handle ownership records for public-handle → participant mailbox, reports `verified` only for explicit evidence status, keeps address-book contacts as mapped fallback, and falls back to the operator mailbox without a sender-visible oracle. |
| P060-033 | Local contact and contactability bridge for Story-010 | done | Node adds `local-contact.v1` schema-gate import/export validation, local contact labels and metadata, `/v1/local-contacts/resolve`, daemon contactability draft/options/attest/publish endpoints, a Node UI contactability panel, contact-control passport binding at publish time, owner participant binding from the draft route or passport subject, signed `contact-claim.v1` construction, and supervised Contact Catalog admission. |
| P060-034 | Contact attestation acquisition dependency for email/phone control | partial | Proposal 061 defines the separate attestation role. Node worktree adds `attestation-core`, `attestation-service`, bundled opt-in `attestation-service` middleware config, `contact-attestation-request.v1` / `contact-attestation-result.v1` schemas and examples, schema-gate validators, `email-attestation` / `phone-attestation` capability ids, local/dev delivery, production SMTP email delivery, SMS webhook delivery, challenge attempt limits, TTL, quotas, and delivery audit. The Story-010 acceptance pack now issues and publishes `role/email-attestation` / `role/phone-attestation` provider passports through Seed Directory and discovers them before requesting e-mail control. Remaining hardening: production contactability acquisition should select a discovered/trusted provider instead of relying on a locally configured attestation endpoint. |
| P060-035 | Story-010 two-node acceptance scaffold | done | `node/tools/acceptance/story-010-operator/` contains profile generation, Node A/B daemon launchers, UI launch/stop helpers, a runbook, `story-smoke`, and self-contained `ad-smoke` for the two-node Seed Directory + Attestation Service + Contact Catalog + Messaging topology. Strict `ad-smoke` is also the top-level Contact Catalog E2E gate: it reports provider publish/trust, admission, projection, lookup, provider sync, private lookup mode, and route-set v1 phases while still exercising attestation challenge/redeem, contactability publish with passport-bound signed contact claims and supervised Contact Catalog admission, shared Contact Catalog lookup, contact request delivery, operator accept, `messaging-receive@v1` passport handoff, private-direct `message-envelope.v1` delivery, and delivered inbox/outbox state. |
| P060-036 | `messaging.accept` capability advertisement for messaging-capable nodes | done | Registered in `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md` / `.pl.md` and node `capability` mapping as `app/messaging.accept`. Solution 007 documents it as an application advertisement tied to the canonical `messaging-receive@v1` profile and `privacy = private-direct`; lookup consumers may filter candidates by it, while admission still requires a concrete `messaging-receive` passport and local `contacts` policy. |
