# Proposal 042: Inter-Node Artifact Channel (F2F Memarium Exchange)

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/036-memarium.md`
- `doc/project/40-proposals/039-crisis-space-seed-v1.md`
- `doc/project/40-proposals/040-custodial-redelivery-and-tombstones.md`
- `doc/project/40-proposals/041-agora-ingest-attestation.md`

## Status

Draft

## Date

2026-04-17

## Executive Summary

Several existing proposals describe **direct node-to-node exchange** of
signed artefacts, each from its own angle:

- proposal 013 §Distribution names direct exchange as the second
  distribution surface for whispers,
- proposal 040 §3 defines a custody handshake whose final step is a
  `Transfer` addressed either to an Agora ingest surface **or to a
  memarium-to-memarium transfer endpoint**,
- proposal 036 Next Action #12 promises such an endpoint,
- proposal 039 (crisis seed) and proposal 025 (seed directory) both
  imply situations in which two nodes would benefit from passing an
  artifact without going through a public relay.

None of these individually defines the channel. This proposal
consolidates them into a single first-class, reusable surface: the
**Inter-Node Artifact Channel (INAC)** — a peer-to-peer,
capability-gated, three-operation protocol for exchanging byte-identical
artefacts between two Orbiplex nodes.

The channel is **orthogonal to Agora**: Agora is a topic-addressed
publication substrate with public observability; INAC is a direct
addressed exchange with no substrate and no public index. Both carry the
same byte-identical envelopes, so an artefact may move from one to the
other without re-signing.

The channel is **generic**. Its baseline carries two artefact shapes —
`agora-record.v1` (for records that already live, or could live, on
Agora) and `memarium-blob.v1` (for generic Memarium-native custody
payloads) — but the kind registry is **open**: additional kinds are
registered by middleware modules through the same
`middleware-module-report` mechanism that already lets modules claim
peer message types in proposal 027.

## Context and Problem Statement

### What is scattered today

1. **Transport exists** (proposal 002: WSS over 443, Ed25519 identity,
   profiles `CORP_COMPLIANT`, `E2E_PREFERRED`, `E2E_REQUIRED`).
2. **Peer dispatch exists** (proposal 027: `PeerMessageChain` pipeline
   with in-process handlers and supervised sidecars, registration via
   `input_chains` in `middleware-module-report`).
3. **A canonical wire format exists** (proposal 035: `agora-record.v1`
   envelope, JCS-canonicalized, `record/id = sha256(canonical_bytes)`,
   signed in the `agora.record.v1` domain).
4. **Authorization primitives exist** (proposal 024: capability
   passports; proposal 041: attestation-gate as reusable ingress
   authorization primitive).
5. **Local authoritative storage exists** (proposal 036: Memarium, with
   default indefinite self-custody per proposal 040 §4).

What does **not** exist as a first-class artifact:

- a named contract for the wire operations that move artefacts between
  two nodes without a public relay,
- a unified position on which authorization source applies in which
  situation (passport vs invitation vs whitelist vs attestation),
- a single definition of how `memarium-blob.v1` relates to
  `agora-record.v1` on the wire,
- an extensibility model answering the question: *should the channel
  accept only a closed set of known artefact kinds, or any kind that
  both nodes understand?*

### Five motivating use cases

This proposal must serve all of the following without requiring a
separate transport for each:

1. **F2F distribution of opinions and whispers** — alternative to Agora
   when `disclosure/scope = "private-correlation"`, when no Agora relay
   satisfies the requested anonymity posture, or when the participants
   prefer a decentralized non-public path.
2. **Crisis notification** — rapid fan-out of
   `crisis-space-seed-v1` artefacts (proposal 039) to a pre-arranged
   neighbour set without waiting for a public relay round-trip.
3. **Custody assistance** — realizing the Transfer step of proposal
   040 §3 for memarium-native blobs (the endpoint that §3 step 3
   references).
4. **Instant participant-to-participant direct exchange** — low-latency
   carrying of signed artefacts between two participants who share a
   trust relationship (F2F), without placing a copy on any substrate.
5. **Passport exchange as an alternative to Seed Directory** — handing a
   `capability-passport.v1` directly, especially for narrow-scope
   passports or for passports not yet ready for catalog publication
   (proposal 025).

## Decision

### 1. Scope and position in the stack

INAC is a **peer-level artefact exchange protocol**, layered **above**
the peer transport (002) and **parallel** to the peer message dispatch
pipeline (027). It is **not** a new transport. It reuses:

- node-to-node WSS session and node identity from proposal 002,
- the `PeerMessageChain` / supervised-sidecar dispatch model from
  proposal 027 (INAC operations are peer messages with a dedicated
  `msg` kind),
- the attestation-gate reusable primitive from proposal 041 for
  ingress authorization decisions,
- the capability-passport format from proposal 024 as the baseline
  authorization artifact.

INAC is **not** a publication surface. There is no topic index, no
public enumeration, no per-topic digest; observability belongs to each
endpoint's Memarium, not to a shared substrate.

### 2. Artefact shapes

Two baseline shapes are recognized. Both are signed, content-addressed,
and byte-identical across distribution surfaces.

#### 2.1 `agora-record.v1`

Defined in proposal 035. Carried **unchanged**. The receiver can:

- verify the envelope locally (JCS + `record/id` recompute + signature
  check in `agora.record.v1` domain),
- store it in Memarium byte-identically,
- later re-ship it to Agora under the redelivery flow (proposal 040),
  because the signature and `record/id` remain valid.

Use this shape whenever the artefact is one that lives, or could live,
on Agora (opinions, whispers, service offers, workflow templates, etc.).

#### 2.2 `memarium-blob.v1`

A new generic envelope for Memarium-native artefacts that are not
structured as Agora records — e.g. action-trace archives, raw
attachments, encrypted personal notes, backup bundles, signed passports
being handed over out-of-band, crisis seed payloads that are not yet
promoted to an Agora record kind.

Minimum required fields (draft; details deferred to the schema file):

- `schema`: constant `"memarium-blob.v1"`.
- `blob/id`: `sha256` of `canonical_bytes(envelope_without_signature)`
  (JCS canonicalization identical to `agora-record.v1`).
- `blob/content-type`: IANA-style media type or Orbiplex-registered
  kind label; receiver uses this to dispatch to a handler.
- `blob/payload`: either inline (base64, only for small payloads under
  a declared size ceiling) or a content-addressed reference
  `sha256:…` to a side-loaded **binary-frame stream** on the same WSS
  session (see §3.4). Inline is reserved for tiny control-plane
  payloads (e.g. a passport handoff); any payload above the ceiling
  MUST use the binary-frame path.
- `blob/encryption`: `none` | `{algorithm, key-ref}`. If not `none`,
  the custodian rule from proposal 040 §3 applies: byte custodian, not
  reader.
- `author/participant-id`: same grammar as `agora-record.v1`, accepting
  `participant:did:key:…` and `nym:did:key:…` (proposal 015).
- `authored-at`: RFC-3339.
- `signature`: Ed25519 over canonical bytes, signing domain
  `memarium.blob.v1`.
- optional `author/attestation-ref` (proposal 041),
  `author/nym-certificate-ref` (proposal 015),
  `author/passport-ref` (proposal 024).

Rationale for a separate schema rather than reusing
`agora-record.v1`:

- `agora-record.v1` couples the envelope to Agora's topic/subject
  model (`topic/key`, `subject/kind`, `subject/id`), which is
  meaningless for most Memarium-native blobs,
- a separate signing domain (`memarium.blob.v1`) prevents
  cross-domain signature replay,
- the two can still live inside the same INAC control message by
  polymorphism on `schema`.

### 3. Three operations

INAC is a three-operation protocol. Each operation travels as a peer
message through the `PeerMessageChain` (proposal 027) with a new `msg`
kind `inac.v1`.

#### 3.1 `offer`

Unsolicited or negotiated advertisement: *"I have this artefact, do you
want it?"*

Request carries:

- `op`: `"offer"`,
- `artifact/schema` (e.g. `agora-record.v1`),
- `artifact/id` (`record/id` or `blob/id`),
- `artifact/content-type` (for blobs),
- `artifact/size-bytes`,
- optional `reason`: free-form tag from a small vocabulary
  (`custody`, `redelivery`, `crisis`, `whisper-direct`,
  `passport-handoff`, `gossip`, `other`),
- optional `invitation-ref`: opaque token received out-of-band from
  the recipient authorizing this offer.

Response is one of:

- `accept` — the receiver wants the artefact; a follow-up `push` or
  `request` is expected,
- `decline` — not now; optional structured `reason` from a shared
  vocabulary (`already-have`, `kind-not-supported`, `policy-refuse`,
  `quota-exceeded`, `rate-limited`, `unauthenticated`,
  `attestation-insufficient`, `content-type-blocked`,
  `encryption-mismatch`, `other`),
- `defer` — try again later with a `retry-after-secs` hint.

`offer` is the least privileged operation: it reveals *existence* and
*size* only, never payload. It MAY be throttled but SHOULD NOT require
full authentication; the attestation-gate applies with an `offer` budget
distinct from the `push` budget.

#### 3.2 `request`

Pull from the other side: *"please send me the artefact with this
id"* or *"please send me artefacts matching this filter from your
own archives"*.

Request carries:

- `op`: `"request"`,
- either `artifact/id` (exact pull) **or** `filter` (bounded
  selector: author-scoped, topic-scoped, kind-scoped, time-range;
  grammar reuses the selectors from proposal 035 §8 where they
  already exist),
- optional `max-artifacts`, `max-bytes`,
- optional `capability-passport-ref` authorizing the filter-scoped
  read (required for any filter that reaches beyond the requester's
  own authored set).

Response is one of:

- `push` with the payload (inline `memarium-blob.v1` or
  `agora-record.v1`),
- `decline` with a reason from the shared vocabulary,
- `partial` with a hint about why the response is truncated
  (`quota-exceeded`, `attestation-insufficient-for-some`, etc.).

`request` MUST be authorized. Default: only the artefact's own author
MAY `request` by `artifact/id` without further capability. Any other
requester MUST present a capability passport (proposal 024) whose
scope covers the requested artefact. Custody-passport-bearing
requesters MAY pull within their custody scope.

#### 3.3 `push`

Delivery: *"here is the artefact, as authorized"*.

Request carries:

- `op`: `"push"`,
- `artifact`: the full envelope (`agora-record.v1` or
  `memarium-blob.v1` or other registered kind),
- `authorization`: one of:
  - `custody-passport`: a `capability-passport.v1` with
    `capability_id = "memarium.custody"` whose scope authorizes this
    push (the proposal 040 §3 custody flow),
  - `invitation-token`: a short-lived token previously issued by
    the receiver (for crisis fan-out, whisper direct exchange,
    pre-arranged peer sets),
  - `own-artifact`: the pushing node is the author of the
    artefact; receiver policy decides whether own-artifact pushes
    are accepted (typically yes for known peers, no for
    strangers),
  - `attestation-only`: no passport; relies entirely on the
    receiver's attestation-gate (proposal 041) to decide.
- optional `correlation-ref` to a prior `offer` or `request` in the
  same session.

Response is one of:

- `ingested`: artefact is in receiver's Memarium (or their chosen
  storage target),
- `already-present`: content-addressed dedup (`record/id` or
  `blob/id`) shows the receiver already has it; treated as success
  for the pusher's bookkeeping,
- `refused`: with a reason from the shared vocabulary (the same set
  as proposal 041 §6 refusal codes, extended with
  `encryption-mismatch`, `content-type-blocked`, `storage-full`).

#### 3.4 Large payloads: binary-frame streaming

For any artefact whose serialized size exceeds the inline ceiling
(proposed default: 64 KiB; configurable per node, per peer, per kind),
the payload travels as a **separate binary-frame stream on the same
WSS session** rather than inline inside the control message.

Mechanism:

- the control message (`push` or `response-to-request`) carries the
  artefact envelope with `blob/payload = { ref: "sha256:…",
  size-bytes, stream-id }`,
- the `stream-id` is a short integer scoped to the WSS session;
  binary frames carrying chunks of the payload are tagged with this
  `stream-id` in their frame header,
- the receiver reassembles the stream, recomputes `sha256` over the
  concatenated bytes, and MUST refuse the artefact with
  `content-hash-mismatch` if the recomputed digest does not match
  the `ref`,
- the `agora-record.v1` envelope's own signature still covers the
  canonical bytes of the envelope; the binary-framed payload is
  content-addressed separately through the `blob/payload.ref`,
- an authorized peer MAY cancel a stream mid-flight with an abort
  control frame; this does not invalidate the authorizing passport
  or invitation.

Why binary frames rather than inline base64:

- avoids the ~33% base64 overhead on hot paths like custody transfer
  and crisis payload fan-out,
- avoids buffering the entire payload in a single JSON control
  message (memory pressure, head-of-line blocking on the control
  plane),
- keeps the control plane cheap to audit and log (control messages
  stay small even when payloads are large),
- reuses the WSS session that the peer has already authenticated,
  without opening a parallel HTTPS range-read endpoint.

Why not a separate HTTPS range-read endpoint: it would require its
own authentication surface, its own proxy-compatibility story
(proposal 002), and a separate connection; keeping streaming on the
established WSS session avoids all three.

### 4. Extensibility: open kind registry, capability-gated per peer

This was an explicit open question when the proposal was commissioned.
The answer: **open registry, not a closed enumeration**.

Rationale (stratified design from CLAUDE.md):

- a closed set couples the channel to today's artefact vocabulary and
  forces every new kind into a core-proposal amendment,
- Orbiplex already has an open extension mechanism for peer message
  types (proposal 027: `handles_peer_message_types` on
  `middleware-module-report`); mirroring it keeps one extension idiom
  across the whole peer plane,
- the channel itself does not need to understand every kind — it only
  needs to **route** a kind to a handler that claims it and to let
  the attestation-gate apply per-kind policy.

Model:

1. **Baseline kinds** are defined normatively in this proposal:
   - `agora-record.v1` (handled by the daemon's Agora-relay subsystem
     when present, otherwise stored as an opaque envelope in
     Memarium),
   - `memarium-blob.v1` (handled by Memarium directly).
2. **Additional kinds** are registered by middleware modules through
   a new field on `middleware-module-report`:
   `handles_artifact_kinds: [{ schema, content_types?,
   authorization_modes_allowed, storage_target }]`. The registration
   says *"I understand this kind, here is my policy for accepting
   it, here is where it lands."*
3. **Kind discovery at the peer level** happens inside `offer` and
   the optional INAC session handshake: an `offer` with a
   `schema` the receiver does not handle yields
   `decline { reason: kind-not-supported }`. A session-level
   handshake MAY enumerate supported kinds up front as an
   optimization, but enumeration is advisory; authoritative routing
   always happens per-operation.
4. **Safety floor for unknown kinds.** A receiver confronted with a
   registered kind that has no local handler MUST refuse with
   `kind-not-supported` rather than storing opaque content; silent
   opaque storage would let pushers exploit the channel as a generic
   dead-drop. (Opaque storage of `memarium-blob.v1` is explicitly
   **allowed** because the blob envelope is itself the contract.)

This design makes INAC the peer counterpart to what Agora's kind
registry is for topic-addressed records: a shared extensible surface
where new artefact domains plug in without forking the protocol.

### 5. Authorization: one gate, four sources

Every inbound INAC operation passes through the
**attestation-gate** primitive (proposal 041 §9). The gate decides
accept/refuse based on which of four authorization sources applies.
All three passport-based sources share the `capability-passport.v1`
format (proposal 024); they differ only in the `capability_id` and
in the scope fields the gate is required to enforce:

| Source | `capability_id` | Who uses it | Gate behaviour |
|---|---|---|---|
| **General capability passport** (024) | domain-specific (e.g. `memarium.read`, `whisper.receive`) | `request` with filter, `push` where the receiver's policy accepts a matching general passport | Verify passport signature, check scope covers the operation, check revocation. |
| **Custody passport** (040 §3) | `memarium.custody` | `push` for custody transfer | Same as general passport plus: enforce `max_bytes`, `max_records`, `duration` from the scope. |
| **Invitation passport** (this proposal) | `inac.invitation` | `push` / `request` with `invitation-ref`, crisis fan-out, whisper direct exchange, passport handoff | Verify passport signature and issuer (the inviter is the receiver, who signs a short-lived narrow-scope passport directed at a specific peer node id); check expiry, single-use consumption, scope match (`artifact/id` or `artifact/schema`). |
| **Attestation alone** (041 modes `passport` / `passport_scoped` / `layered` / `allowlist` / `open`) | — | `offer`, or `push` where the receiver's local policy permits unsolicited accept | Apply the receiver's per-kind ingest policy; budgets and rate limits are per-peer, not per-channel. |

All three passport variants flow through the **same**
`PassportResolutionCache` described in proposal 041 §9; INAC is a
consumer, not a separate authority. Unifying the invitation token as
a passport variant means:

- one verification path for signature, expiry, revocation,
- one cache for resolution,
- one lifecycle vocabulary in refusal codes (`…_unknown`,
  `…_expired`, `…_revoked`, `…_scope_mismatch`),
- one operator mental model ("everything that authorizes inbound
  operations is a passport with a `capability_id`").

The invitation variant's distinctive traits — short expiry, optional
single-use consumption, directed at a specific peer — are expressed
through the passport's scope fields, not through a separate
credential class.

### 6. Privacy and observability differences from Agora

INAC is **not** a publication surface. Consequently:

- no per-topic digest and no per-author digest on the channel (those
  are Agora concerns, proposals 035 and 040),
- no public enumeration endpoints,
- the fact that an artefact passed between two nodes is only
  observable to those two nodes (plus any lawful intercept mandated
  on the transport, which is a property of proposal 002, not of
  INAC),
- tombstones (proposal 040) do **not** apply to INAC; the channel
  has no shared substrate to "forget on behalf of". A node that
  refuses a `push` simply refuses; a node that later deletes from
  Memarium just deletes.

What INAC **does** give for observability:

- every accepted `push` produces a Memarium fact on the receiver
  side (proposal 036 §Facts),
- every sent `push` produces a Memarium fact on the sender side,
- every refusal emits a structured reason code; operators see their
  own refusal history but not the counterparty's acceptance history,
- the channel carries **no public digest**; an operator who wants to
  prove they received a particular `artifact/id` from a particular
  peer can produce their own Memarium-level audit trail.

### 7. Retention: receiver's Memarium policy

Once an INAC `push` is accepted, the artefact is **the receiver's
Memarium content**, subject entirely to the receiver's retention
policy (proposal 036):

- for custody-tagged artefacts, the passport's `duration` applies,
- for own-artefact artefacts, the default indefinite self-custody
  rule from proposal 040 §4 applies,
- for invitation-tokened artefacts (whispers, crisis notifications,
  passport handovers), the receiver's default space policy applies
  unless the token itself bounds retention,
- there is no inter-node retention convergence; two receivers of the
  same `push` MAY legitimately diverge on when they delete,
- the sender retains no claim over the receiver's copy beyond what
  was encoded in the authorizing artefact (passport or invitation
  token); there is no "right to be forgotten" channel primitive in
  INAC (that belongs to higher layers and policy, not to the wire).

### 8. How the five use cases map

| Use case | Operation(s) | Authorization | Artefact shape |
|---|---|---|---|
| F2F opinion / whisper distribution | `offer` → `accept` → `push`, or direct `push` on invitation | `invitation-token` or attestation-only | `agora-record.v1` (opinions, whispers) |
| Crisis notification | `push` to each member of the pre-arranged neighbour set | `invitation-token` issued when the neighbour set was formed | `agora-record.v1` (if crisis-space-seed has an Agora kind) or `memarium-blob.v1` |
| Custody assistance | `push` (the Transfer step of proposal 040 §3) | `custody-passport` (040 §3) | `agora-record.v1` for Agora-native records, `memarium-blob.v1` for native blobs |
| Instant direct F2F exchange | `offer` → `push`, or `request` → `push` | `invitation-token` or `own-artifact` | both |
| Passport exchange (alternative to Seed Directory) | `offer` → `push`, or direct `push` on invitation | `invitation-token` or attestation-only; **the pushed artefact is itself the passport** | `memarium-blob.v1` wrapping the `capability-passport.v1` |

For use case 5 specifically: unlike Seed Directory (025), which is a
catalog with enumeration and listing semantics, INAC hands a passport
**to one recipient** without publishing it. This is appropriate when
the passport's scope is narrow, the relationship is pre-existing, or
the holder does not want the passport to appear in any public catalog
before it has been used.

## Non-Goals

- INAC is **not** a replacement for Agora. Any artefact with a public
  audience and a persistent topic SHOULD prefer Agora (035); INAC is
  for directly-addressed exchange.
- INAC does **not** define NAT traversal, hole-punching, or
  discovery; those belong to proposals 002 and 014.
- INAC does **not** define how invitation passports are delivered
  out-of-band to the inviter's peer; it only defines their
  verification on arrival. Delivery may itself happen through INAC
  (passport handoff is one of the five use cases in §8) or through
  any other channel the inviter and invitee have already
  established.
- INAC does **not** define Memarium storage semantics; it defines
  wire operations that write into Memarium via its existing host
  capabilities (proposal 036).
- INAC does **not** run its own signing domain for the envelope; it
  reuses `agora.record.v1` and `memarium.blob.v1`. INAC's own
  control messages (offer / request / push / response codes) are
  peer messages under 027's dispatch rules and carry no extra
  signature beyond what the peer session provides.

## Consequences

### Positive

- One named first-class channel instead of scattered references in
  013, 036, 039, 040.
- Reuses all existing primitives (passports, attestation-gate,
  peer message chain, WSS transport).
- Enables F2F use cases that Agora cannot serve (hard anonymity,
  pre-publication passports, instant direct exchange).
- Natural carrier for the custody Transfer step that proposal 040
  left to a future endpoint.
- Open kind registry keeps the channel forward-compatible.

### Negative / watch items

- Two envelope schemas (`agora-record.v1`, `memarium-blob.v1`)
  increase the surface that the attestation-gate must recognize; the
  shared `schema` discriminator and identical JCS rules keep this
  cost bounded.
- Invitation passports (`capability_id = "inac.invitation"`) are
  short-lived narrow-scope instances of `capability-passport.v1`
  (proposal 024); they reuse the existing passport lifecycle
  (issuance, revocation, expiry, cache) but add a single-use
  consumption rule that the receiver's gate enforces. No new
  credential class is introduced.
- Because there is no shared substrate, redelivery semantics from
  proposal 040 do not apply on INAC; recovery from loss is the
  sender's problem and happens via re-`push`, not via tombstone-gated
  refusal.
- Open kind registry means a malicious middleware module could claim
  a legitimate kind label and mis-handle it; per-kind registration
  MUST be subject to the same trust review as any other middleware
  module (proposal 027).

## Resolved Open Questions

1. ~~**Invitation token format.**~~ **Resolved (§5):** invitation
   tokens are a `capability-passport.v1` variant with
   `capability_id = "inac.invitation"`, narrow scope, short expiry,
   and optional single-use consumption expressed through scope
   fields. No separate credential class.
2. ~~**Streaming large blobs.**~~ **Resolved (§3.4):** large payloads
   travel as binary frames on the same WSS session, tagged with a
   session-scoped `stream-id` and content-addressed through a
   `sha256:…` reference inside `blob/payload`. No parallel HTTPS
   range-read endpoint.
3. ~~**Offer-without-intent.**~~ **Resolved:** unsolicited `offer`
   from an unknown peer is refused by default. A receiver MAY enable
   open intake per artefact kind, but that mode MUST be explicit,
   rate-limited, and evaluated by the attestation-gate before any
   persistent local fact is written. The default allow conditions are:
   known peer, Seed Directory acquaintance, valid `inac.invitation`,
   response to a previous `request`, or an operator-enabled public
   intake profile.
4. ~~**Kind shadowing.**~~ **Resolved:** duplicate authoritative
   registrations for the same `(schema, content-type?)` MUST NOT be
   resolved by load order. Baseline kinds (`agora-record.v1` and
   `memarium-blob.v1`) are daemon-reserved. For middleware-owned kinds,
   the daemon MUST either use an explicit operator route override or
   mark the kind as conflicted and refuse it with `kind-conflict` /
   `kind-not-supported`. Multiple observer/audit modules MAY watch the
   same kind, but only one authoritative ingest/storage handler may own
   it.
5. ~~**Cross-surface migration of invitation-based artefacts.**~~
   **Resolved:** an `inac.invitation` authorizes direct transfer, not
   future publication. It is not part of the signed artefact, does not
   change `record/id`, and does not grant the receiver a right to
   republish to Agora. Later Agora publication is a separate author or
   relay decision evaluated by Agora ingest policy and the
   attestation-gate. A non-author receiver MUST NOT republish an
   invitation-delivered private/direct artefact unless the artefact or
   a separate passport explicitly grants republication.
6. ~~**Redundant distributed node-address attestation.**~~
   **Resolved:** keep the full contract out of INAC and define it in
   a separate proposal as `node-address-attestation.v1`. Seed Directory
   remains the trusted primary source, operated by network/organization
   operators; the new artefact is a fallback evidence packet for the
   case where Seed Directory is unavailable and a node asks already
   trusted peers for the last known address of another node. INAC may
   carry that artefact as an ordinary registered kind, but it does not
   own the schema, trust policy, or anti-reflection rules. See proposal
   043.

## Follow-Up / Next Actions

1. Write the `memarium-blob.v1` JSON Schema under `doc/schemas/`
   following the content-addressed, signed pattern of
   `agora-record.v1`.
2. Register the `inac.v1` peer-message `msg` kind in the
   reference-implementation peer message registry (proposal 027).
3. Add a new `handles_artifact_kinds` field to
   `middleware-module-report` and document its registration
   semantics alongside `handles_peer_message_types`.
4. Specify the INAC control-message schemas for `offer`, `request`,
   `push` and their response envelopes.
5. Document the `inac.invitation` `capability_id` in proposal 024
   (scope grammar, single-use consumption rule, recommended expiry
   bounds) so it lives alongside the other passport variants.
6. Document the WSS binary-frame stream discipline
   (`stream-id` scoping, chunk framing, abort control frame,
   digest-verify-then-commit rule) as a section in proposal 002, so
   the transport-level framing lives where the transport is
   defined.
7. Update proposal 013 Next Action #9 to reference this proposal as
   the direct-exchange contract.
8. Update proposal 036 Next Action #12 to reference this proposal as
   the memarium-to-memarium transfer endpoint.
9. Update proposal 040 §3 step 3 to name INAC `push` with
   `custody-passport` authorization as the canonical Transfer
   channel.
10. Update proposal 039 (crisis) to reference INAC as the low-latency
    fan-out channel for crisis seeds.
11. Update proposal 025 (seed directory) to note INAC passport
    handoff as the complementary path for narrow-scope or
    pre-publication passports, and proposal 043 as a fallback
    node-address evidence path when Seed Directory is temporarily
    unavailable.
12. Extend proposal 041 §6 refusal code table with INAC-specific
    codes (`kind-not-supported`, `encryption-mismatch`,
    `content-type-blocked`, `storage-full`, `invitation-unknown`,
    `invitation-expired`, `invitation-revoked`,
    `invitation-scope-mismatch`).
13. Add requirements mapping in `doc/project/50-requirements/` for
    the INAC contract (operations, authorization sources, Memarium
    write behaviour, refusal codes).
14. **Done:** `node-address-attestation.v1` is now a separate schema
    and proposal 043 owns its verification and anti-reflection policy.
    INAC only carries the artefact as a registered kind.
