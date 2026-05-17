# Solution 042: Inter-Node Artifact Channel (INAC) — Implementation Guidelines

Proposal: `doc/project/40-proposals/042-inter-node-artifact-channel.md`

Related impl notes:
- `doc/project/60-solutions/008-agora/008-agora-topic-addressed-relay-impl.md` (sister surface — topic-addressed publication)
- `doc/project/60-solutions/011-whisper/011-whisper-impl.md` (first named consumer)

## Purpose of this document

Implementation entry point for INAC — the peer-to-peer,
capability-gated, three-operation channel for exchanging
byte-identical artefacts between two Orbiplex nodes.

This note does **not**:
- duplicate the proposal (proposal 042 is authoritative on
  semantics),
- enumerate every consumer's wiring (consumer-side impl lives in
  the respective consumer's `60-solutions/NNN-*-impl.md`),
- track fine-grained tasks (that lives in the sibling `node`
  repository alongside the transport and peer-dispatch notes).

It exists to:

- map proposal 042's decisions to layers and crates,
- fix the invariants that cross layers (envelope byte-identity,
  authorization sources, attestation-gate reuse, open kind
  registry),
- track current status per layer,
- enumerate open decisions that block coherent implementation,
- give a stable commit order.

## Architectural posture

INAC is a **peer-level artefact exchange protocol**, layered above
the WSS peer transport (proposal 002) and parallel to the peer
message dispatch pipeline (proposal 027). In the component-facing
architecture it is a private/direct transport adapter under
`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`.
It is not a general component send API, not a new identity system, and not a
new authorization authority.

Three operations — `offer`, `request`, `push` — travel as peer
messages with a dedicated `msg` kind `inac.v1`. Large payloads
travel as session-scoped stream chunks on the same WSS session.
Authorization flows through the attestation-gate (proposal 041) using one of four
sources: general capability passport, custody passport, invitation
passport, or attestation alone.

Artifact-kind admission is owned by Artifact Delivery, not by a middleware
chain. INAC receives or transfers byte-identical artifacts and then feeds the
host-owned inbound admission path. That path has a single authoritative
acceptor per artifact schema/content-type class. Additional artifact kinds plug
in as explicit inbound acceptors, not as fan-out chains.

The first remote WSS implementation is deliberately fail-closed: authenticated
peer session establishment is not sufficient authority to send AD-bound INAC
frames. The receiver applies a host-owned allowlist
(`artifact_delivery_adapters.inac_peer_transport.inbound_allowed_peers`) before
answering `offer` or accepting `push`. An empty list means deny-all. This is a
minimal production guard until the full invitation/passport/revocation freshness
gate is wired.

Matrix mailbox remains a later transport adapter, not an INAC authority system.
The accepted default is to use it as the first asynchronous store-and-forward
fallback for private delivery. A mailbox event must carry the same
envelope/INAC authorization proof that WSS would require. Plaintext/JSON
payloads should be sealed before posting as `artifact-mailbox-sealed.v1`
encrypted to the recipient key; already domain-encrypted or opaque custody
payloads may remain byte-identical. The receiver unseals, then validates the
original descriptor (`size/bytes`, `sha256:*`, schema, content type) before the
ordinary Artifact Delivery inbound admission path.

## Invariants that cross layers

1. **Envelope byte-identity.** Whatever an INAC peer receives and
   accepts, it stores byte-identically. The envelope's signature
   and `record/id` (for `agora-record.v1`) or `blob/id` (for
   `memarium-blob.v1`) remain valid without re-signing or
   canonicalization differences across distribution surfaces.

2. **One attestation-gate, shared with Agora.** INAC does not run
   a parallel verifier. It consumes the same attestation-gate
   primitive (proposal 041 §9) and shares the
   `PassportResolutionCache`. Any divergence means the security
   properties drift.

3. **One passport format.** All three authorization-bearing paths
   (general capability, custody, invitation) are
   `capability-passport.v1` instances distinguished by
   `capability_id`. No parallel credential class.

4. **Control plane is cheap; payload is separate.** Control
   messages (`offer`, `request`, `push`, responses) stay small
   and auditable. Payloads above the configured inline ceiling
   travel as binary frames, content-addressed through a
   `sha256:…` reference. The control plane is not where bytes
   accumulate.

5. **Signing domains are per-envelope.** `agora-record.v1` is
   signed in `agora.record.v1`; `memarium-blob.v1` is signed in
   `memarium.blob.v1`. INAC itself has no signing domain; its
   control messages ride the peer session's authentication.

6. **No public observability.** INAC has no topic index, no
   public enumeration, no per-topic digest. The only observability
   is each endpoint's Memarium. Tombstones (proposal 040) do not
   apply — there is no shared substrate to "forget on behalf of".

7. **Open kind registry with a safety floor.** Unknown kinds MUST
   be refused with `kind-not-supported`. `memarium-blob.v1` is the
   explicit exception: opaque blobs are allowed because the blob
   envelope is itself the contract.

## Layer 0 — JSON Schemas

| Schema | Role | State |
|---|---|---|
| `memarium-blob.v1` | generic Memarium-native artefact envelope (content-addressed `blob/id`, domain `memarium.blob.v1`) | ✅ schema exists and is synchronized into node schema-gate |
| `inac-control.v1` | control-message envelope for `offer`/`request`/`push` operations + response frames | ✅ schema exists; local runtime scaffold validates it; `push` requires exactly one payload location |
| `agora-record.v1` | reused from proposal 035 | ✅ exists |
| `capability-passport.v1` (`inac.invitation`, generic `inac-push@v1`, and `memarium.custody`) | authorization artifact for invitation, general push, and custody push | ✅ receiver-side WSS `push` verifies all three passport paths through the shared capability-binding gate |

## Layer 1 — Peer-message kind registration

INAC operations are peer messages under the `PeerMessageChain`
(proposal 027).

| Item | State |
|---|---|
| Register `inac.v1` as a `msg` kind in the reference peer-message registry | ✅ implemented for WSS peer sessions |
| Document the message envelope under `peer-message-invoke.v1` forwarding rules | ❌ not started |
| Feed received artifacts into Artifact Delivery inbound admission | ✅ implemented for WSS `push` frames |
| Project middleware and in-process component acceptor declarations into the Artifact Delivery route table | 🟡 partial — daemon config supports supervised HTTP, in-process, and pure JSON-e Flow Artifact Delivery acceptors; projection from module reports remains later |

## Layer 2 — Control protocol

Three operations + response frames.

### Operations

| Operation | Request fields | Response variants |
|---|---|---|
| `offer` | `op`, `artifact/schema`, `artifact/id`, `artifact/content-type?`, `artifact/size-bytes`, `reason?`, `invitation-ref?` | `accept`, `decline { reason }`, `defer { retry-after-secs }` |
| `request` | `op`, `artifact/id` **or** `filter`, `max-artifacts?`, `max-bytes?`, `capability-passport-ref?` | `push` (payload), `decline { reason }`, `partial { reason }` |
| `push` | `op`, `artifact` (full envelope), `authorization` (`custody-passport` \| `invitation-token` \| `own-artifact` \| `attestation-only`), `correlation-ref?` | `ingested`, `already-present`, `refused { reason }` |

### Refusal-code vocabulary

Shared with proposal 041 §6 refusal table, extended with INAC-specific
codes:

- `kind-not-supported`, `encryption-mismatch`, `content-type-blocked`,
  `storage-full`,
- `invitation-unknown`, `invitation-expired`, `invitation-revoked`,
  `invitation-scope-mismatch`,
- plus all proposal 041 §6 codes (`attestation-insufficient`,
  `passport-expired`, `passport-revoked`, `nym-certificate-*`, etc.).

Registration of these codes in proposal 041 §6 is 042 Follow-Up #12.

### Status

| Component | State |
|---|---|
| Control-message schemas (`inac-control.v1` envelopes for each op + response frame) | ✅ implemented for the local MVP scaffold |
| Refusal-code vocabulary extension in proposal 041 §6 | ❌ not started |
| Query/filter grammar for `request` (reuse of proposal 035 §8 selectors where possible) | ❌ not started |

Response metadata is intentionally not a cross-node round-trip contract in the
current implementation. The WSS peer handler terminates inbound `meta` at the
node boundary and emits response frames without copying caller-provided metadata.
Middleware-visible semantics must not depend on implicit `meta` propagation.

## Layer 3 — Streamed payload transfer

Large payloads travel on the same WSS session, tagged with a
session-scoped `stream-id`. The current implementation uses peer-message
frames with `msg = "inac.stream.chunk.v1"` carried by the existing WSS binary
envelope. Senders prefer the `inac.stream.chunk.binary.v1` payload shape, which
adds offset, size, final flag, artifact ref, and per-chunk `sha256`; the older
JSON/base64url chunk shape remains a compatibility fallback. In the current
runtime this is still an application-frame JSON payload with `bytes/base64url`;
`binary` names the byte-level validation contract, not a raw WebSocket frame.
A future lower level zero-copy WebSocket split can replace only the carrier
plumbing, not the INAC/AD contract.

### Rules

- the final `push` carries `transfer.mode = "stream"` and
  `artifact/ref = "inac-stream:<stream-id>"`,
- chunks carry `stream/id`, `chunk/index`, final flag, descriptor snapshot,
  artifact ref, chunk size, chunk offset, optional per-chunk digest, and chunk
  bytes,
- receiver reassembles → recomputes `sha256` → MUST refuse with
  `digest-mismatch` on mismatch,
- interrupted or malformed streams do not invoke Artifact Delivery admission
  or any domain acceptor,
- inline base64 allowed only below the configured ceiling
  (proposed default 64 KiB, per-node / per-peer / per-kind
  configurable).

### Placement

The stream chunk discipline is a **transport concern**. INAC consumes it and
Artifact Delivery decides when to use it for `inac-direct`; domain acceptors
only see a byte-identical artifact after size/digest verification.

### Status

| Component | State |
|---|---|
| WSS peer-message stream carrier | ✅ implemented as `inac.stream.chunk.v1` |
| Preferred binary chunk payload shape | ✅ implemented as `inac.stream.chunk.binary.v1` with JSON/base64url fallback |
| Sender-side stream serializer | ✅ implemented for AD `inac-direct` |
| Receiver-side reassembler + hash verifier | ✅ implemented under `<data-dir>/storage/artifact-delivery/streams/` |
| Abort frame handling | ❌ not started; malformed/interrupted streams fail closed and are cleaned at startup |
| Per-peer / per-kind inline-ceiling configuration surface | ❌ not started |

`artifact/ref` and `artifact/href` are valid control-plane payload locations,
but they are not enough by themselves. A production route must also define a
resolver/fetch or binary-frame streaming contract that turns the reference into
byte-identical artifact bytes before domain admission.

## Layer 4 — Authorization (attestation-gate consumer)

Every inbound INAC operation passes through the attestation-gate
(proposal 041 §9). Four authorization sources map to gate predicates
as described in proposal 042 §5.

### Status

| Component | State |
|---|---|
| Attestation-gate crate (shared with Agora) | ❌ not started |
| `PassportResolutionCache` (shared with Agora) | ❌ not started |
| General-capability-passport verifier path | ✅ implemented for receiver-side WSS `push` through `capability-binding::authorize`, `OperationRequest::InacPush`, and the built-in `inac-push@v1` evaluator |
| Custody-passport verifier path (enforces `max_bytes`, `max_records`, `duration` from scope) | ✅ implemented for receiver-side WSS `push` through `capability-binding::authorize`, the built-in `memarium-custody@v1` evaluator, byte-limit enforcement, and durable `max_records` consumption in the INAC ledger |
| Invitation-passport verifier path (expiry, revocation freshness, single-use consumption log, scope match) | ✅ implemented for receiver-side WSS `push` before Artifact Delivery admission; missing revocation source is a fail-closed `not-authorized` condition |
| Attestation-only fallback (for `offer` and for per-kind policies that allow unsolicited accept) | ❌ not started |
| Per-peer/per-kind budgets (for `offer` vs `push`, schema, content type, size, and per-minute rate) | ✅ implemented as receiver-side `artifact_delivery_adapters.inac_peer_transport.inbound_budgets`; budget refusals are recorded before AD admission and before invitation notifications; `max_per_minute = 0` is an explicit `policy-denied` deny rule, not a transient quota state |

## Layer 5 — Kind dispatch and storage targets

Once authorization passes, dispatch routes the artefact to the
registered handler for its `schema`.

### Baseline handlers

| Schema | Handler | Storage target | State |
|---|---|---|---|
| `agora-record.v1` | Artifact Delivery in-process acceptor that verifies the envelope and re-ingests through local `agora-service` when available | Agora relay/store | ✅ implemented; absence of local Agora is an explicit handler-unavailable refusal/transient failure, with no implicit Memarium fallback |
| `memarium-blob.v1` | Artifact Delivery in-process acceptor that validates schema, recomputes `blob/id`, verifies the envelope signature, and writes an accepted custody fact through Memarium | Memarium | ✅ implemented for encrypted/opaque custody; plaintext/private custody remains fail-closed unless a future explicit policy enables it |

The baseline `memarium-blob.v1` acceptor is intentionally stricter than the
portable schema. It requires `signature.key/public` so verification does not
infer a signing key from `author/participant-id`; delegated blob signatures are
future work. It also requires a non-plaintext encryption descriptor object and
rejects both `blob/encryption = "none"` and descriptors with
`algorithm = "none"`. Accepted custody envelopes are recorded as local
Memarium facts in the public space for the MVP; configurable target spaces and
sealed/private custody storage remain future work.

### Open-kind handlers

Open artifact kinds are registered as Artifact Delivery inbound acceptors.
INAC does not own this registry and does not fan out to middleware chains. It
feeds the received artifact into Artifact Delivery; the host-owned admission
table selects exactly one authoritative acceptor. Safety floor (§Invariant 7)
applies: unknown registered kind with no acceptor → `kind-not-supported`.

### Status

| Component | State |
|---|---|
| Artifact Delivery inbound acceptor registry + lookup | ✅ implemented for in-process MVP acceptors, supervised HTTP acceptors, JSON-e Flow acceptors, and WSS `inac.v1` push admission |
| Conflict rule on shadowed kinds: duplicate exact authoritative acceptors fail readiness; exact content-type handlers may coexist with one wildcard fallback | ✅ implemented in Artifact Delivery |
| Safety-floor refusal for unknown kinds | ✅ implemented in local INAC runtime as fail-closed `kind-not-supported` |
| Session-level kind handshake (advisory enumeration, authoritative routing per-op) | ❌ not started |

## Layer 6 — Invitation-passport lifecycle

Invitation passports (`capability_id = "inac.invitation"`) are
short-lived narrow-scope instances of `capability-passport.v1`.
Distinctive traits expressed through scope fields:

- short expiry,
- optional single-use consumption,
- directed at a specific peer node id,
- bound to a specific `artifact/id` or `artifact/schema`.

### Status

| Component | State |
|---|---|
| `inac.invitation` scope grammar | ✅ implemented as `inac-invitation@v1` with `inac/push`, `peer_node_ids`, `artifact_schemas`, optional `artifact_ids`, optional `content_types`, and `single_use` defaulting to `true` |
| Issuer-side: passport builder for invitations | ✅ generic `capability.passport.sign` exists; Story-005 bootstrap can install A↔B invitation passports, and receiver-side notification Accept can issue a narrow `inac.invitation` passport for a pending offer; receiver-issued notification passports use `artifact_delivery_adapters.inac_peer_transport.invitation_passport_ttl_seconds` (default 3600 seconds) |
| Receiver-side: single-use consumption log | ✅ implemented in the local INAC SQLite ledger under `<data-dir>/storage/inac.sqlite`; repeated use of the same single-use passport for a different transfer is refused before AD admission |
| Receiver-side authorization core | ✅ implemented through the shared `capability-binding::authorize` path using `OperationRequest::InacPush`, a synthetic remote-node caller binding, the built-in `inac-invitation@v1` evaluator, and the receiver revocation view |
| Revocation channel (reuse of proposal 024 passport revocation) | ✅ receiver gate requires a revocation view source, checks the current revocation view and freshness budget, and fails closed when the view is missing or stale; invitation-specific rate-limit policy remains a later policy layer |

Invitation UX is built on the generic notification queue rather than inside the
INAC transport. A pending `offer` creates an operator notification with
host-owned `inac.invitation.accept` and `inac.invitation.reject` action refs.
Accepting issues the narrow `inac.invitation` passport; rejecting records a
local refusal. Accept is idempotent for an already accepted offer and does not
issue another passport on a repeated action. Active pending offers are capped
per remote node before another notification is created. Accept also creates a
durable local contact projection in the INAC SQLite ledger when
`artifact_delivery_adapters.inac_peer_transport.contact_creation_after_accept`
is enabled. That contact is an operator-visible local relationship read model;
it does not grant authority, publish to Seed Directory or Agora, or replace the
future Contact Catalog.

## Layer 7 — Peer transport and node-identity

INAC reuses, does not replace:

- node-to-node WSS session from proposal 002,
- Ed25519 node identity and security profiles (`CORP_COMPLIANT`,
  `E2E_PREFERRED`, `E2E_REQUIRED`) from proposal 002,
- discovery and reachability from proposal 014.

Open Question #6 in proposal 042 proposes a future
`node-address-attestation.v1` kind for gossip-level address
distribution with multi-sig trust scoring and reflected-DDoS
resistance. That kind would itself be an INAC-carried
`memarium-blob.v1` — i.e. INAC transports the very artefact that
helps peers find each other — but this is deferred.

### Status

| Component | State |
|---|---|
| WSS transport + identity (proposal 002) | 🟡 transport proposal accepted; implementation state lives in node repo |
| Discovery (proposal 014) | 🟡 same as above |
| `node-address-attestation.v1` endpoint evidence | ✅ implemented as discovery/TLS trust evidence in Seed Directory and peer supervisor integration; carrying it as an INAC artefact for peer-relayed discovery remains deferred |

## Layer 8 — Middleware integration

INAC lives inside the daemon's peer plane, so its wiring is analogous
to proposal 027's peer-message dispatch.

| Component | State |
|---|---|
| `inac.v1` peer-message handler registered in the `PeerMessageChain` | ✅ implemented for daemon in-process WSS handling |
| Sidecar-registration path (so Python/other-language modules can declare Artifact Delivery inbound acceptors) | 🟡 partial — supervised HTTP acceptors can be wired through explicit daemon config; module-report-driven self-registration remains later |
| Daemon supervisor readiness: Artifact Delivery route table is resolved at init, not at first request | ✅ implemented for the current config/runtime validation surface; module-report acceptor projection remains later |

The direct INAC host capability surface and the Artifact Delivery route surface
remain separate authorization boundaries:

- `inac.offer`, `inac.request`, and `inac.push` use INAC outbound allowlists;
- `artifact.delivery.send` uses Artifact Delivery outbound allowlists, even
  when a route resolves to the local `inac-direct` adapter.
- Story-005 private/direct Whisper uses the Artifact Delivery route surface:
  `private-whisper-default` resolves to `inac-direct` and uses the same
  receiver-side INAC passport gate as other remote WSS `push` frames.

This avoids treating permission to use one component-facing surface as implicit
permission to use the other.

## Remaining follow-ups and settled implementation decisions

1. **Inline ceiling and streaming.** The implementation now has a bounded inline
   ceiling plus `inac.stream.chunk.v1` over the existing WSS peer-message
   session for larger payloads. A lower-level raw WebSocket binary carrier is a
   future performance optimization, not a semantic requirement.

2. **Per-peer and per-kind budget configurability.** Receiver-side
   `offer`/`push` budgets exist, but finer per-kind inline-ceiling and stream
   budget surfaces remain future hardening.

3. **Single-use invitation passports.** `inac-invitation@v1` defaults
   `single_use` to `true`. Reuse is checked by the receiver-side INAC ledger
   before AD admission.

4. **Kind-shadowing precedence.** Artifact Delivery owns the authoritative
   acceptor table. Duplicate exact authoritative acceptors are conflicts;
   exact content-type handlers may coexist with one wildcard fallback.

5. **Offer-without-intent policy.** Unsolicited `offer` intake is controlled by
   receiver-side peer budgets and invitation notification policy. It must never
   imply authority to `push`.

6. **Opaque-envelope storage for `agora-record.v1` on nodes without a local
   Agora-relay subsystem.** The baseline acceptor refuses explicitly when local
   Agora is unavailable. INAC/AD do not silently store Agora records in Memarium;
   a future custody path can add that behavior only through an explicit
   acceptor/configuration.

7. **Streaming abort semantics.** Abort frames and whether an aborted transfer
   consumes a single-use invitation remain future work. Interrupted or malformed
   streams fail closed and do not invoke AD admission.

## Current production-MVP boundaries

- Payload transfer supports inline artefacts and session-scoped stream chunks
  over the existing WSS peer-message session. A raw lower-level WebSocket binary
  carrier remains a profiling-led optimization.
- Referenced payload locations (`artifact/ref`, `artifact/href`) are valid
  control-plane slots only when a configured resolver/fetch or stream contract
  can turn the reference into byte-identical bytes before domain admission.
- Baseline handlers cover `agora-record.v1` and `memarium-blob.v1`. Open
  middleware acceptors are represented through Artifact Delivery acceptor
  declarations rather than by making INAC a middleware chain.
- No session-level kind handshake in v1; authoritative routing remains
  per-operation and per-admission.
- `node-address-attestation.v1` is implemented as discovery/TLS endpoint
  evidence, but peer-relaying address attestations as INAC-carried artefacts is
  deferred.
- Single-custodian flows are the operational baseline. Multi-custody is allowed
  by higher-level custody policy, but the INAC protocol does not coordinate
  custodians; each custodian operates independently.
- No automatic INAC-to-Agora promotion. Cross-surface migration is a consumer's
  concern, such as a future Whisper durable-promotion workflow; INAC itself does
  not migrate artefacts between substrates.

## Recommended commit order

Each step leaves the tree compiling.

1. **Resolve open decisions 2 (invitation single-use semantics),
   3 (shadowing precedence), 4 (offer rate default).** Cheap;
   unblocks schemas and gate.
2. **Layer 0 — schemas.** `memarium-blob.v1` first, then
   `inac-control.v1` control-message envelopes. **Done for the MVP
   scaffold.**
3. **Attestation-gate (proposal 041).** Shared primitive; blocks
   Layer 4.
4. **`inac.invitation` scope grammar documented in proposal 024.**
   Blocks Layer 6.
5. **Layer 4 — authorization.** Verifier paths for invitation, general
   INAC push, and Memarium custody passports are implemented through the
   shared capability-binding gate. Attestation-only remains future work.
6. **Layer 5 — baseline kind dispatch.** Runtime registry exists and
   fails closed. Concrete `agora-record.v1` and `memarium-blob.v1`
   acceptors are wired through Artifact Delivery in-process acceptors.
7. **Layer 2 — control protocol.** `offer` / `request` / `push` +
   responses, inline-only payloads. **Done locally and over WSS peer-message
   push.**
8. **Layer 1 — peer-message registration.** Register `inac.v1`
   with the `PeerMessageChain`. **Done for WSS.**
9. **Layer 6 — invitation lifecycle.** Issuer + receiver +
   consumption log.
10. **Layer 8 — middleware integration.** Daemon wiring of the
    INAC handler.
11. **MVP ships here.** Consumers (whisper direct, custody
    transfer, crisis fan-out, passport handoff) start depending
    on INAC.
12. **Layer 3 — lower-level zero-copy WebSocket split.** Optional profiling-led
    optimization beyond the authenticated stream chunk carrier.
13. **Layer 5 — Artifact Delivery open acceptor registry.** Unlocks
    third-party middleware kind extensions without making INAC a chain.
14. **042 Open Question #6 — `node-address-attestation.v1`.**
    Deferred; gated on the Seed Directory federation decision.

## Testing posture

- **Golden vectors** for control messages (`offer`, `request`,
  `push` and all response variants) in `inac-core/tests/`.
  Federation-level contract; bumps require version increment.
- **Authorization-path tests**: for each authorization source,
  produce acceptance and refusal cases; refusal codes must match
  the shared vocabulary exactly (regression guard against silent
  code drift).
- **Envelope byte-identity tests**: a record received via INAC
  must hash (`record/id`) identical to the same record ingested
  via Agora. Cross-surface equality is the invariant; this test
  is the enforcement.
- **Safety-floor test**: an `offer` or `push` for an unknown
  `schema` (with no registered handler) MUST refuse with
  `kind-not-supported`; no opaque storage path taken.
- **Invitation single-use test**: a passport marked single-use
  consumed once MUST refuse a second use with
  `invitation-revoked` (or the chosen single-use refusal code).
- **Shared-cache test**: a passport resolved on the Agora path
  is immediately available on the INAC path and vice versa (same
  `PassportResolutionCache`).
- **Streaming hash-mismatch test**: an
  intentional byte-flip in a chunk MUST trigger
  `digest-mismatch` refusal; no partial-commit residue on
  the receiver.
