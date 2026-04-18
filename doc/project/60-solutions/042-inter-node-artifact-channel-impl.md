# Solution 042: Inter-Node Artifact Channel (INAC) — Implementation Guidelines

Proposal: `doc/project/40-proposals/042-inter-node-artifact-channel.md`

Related impl notes:
- `doc/project/60-solutions/035-agora-topic-addressed-relay-impl.md` (sister surface — topic-addressed publication)
- `doc/project/60-solutions/013-whisper-social-signal-exchange-impl.md` (first named consumer)

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
message dispatch pipeline (proposal 027). It is not a new transport,
not a new identity system, and not a new authorization authority.

Three operations — `offer`, `request`, `push` — travel as peer
messages with a dedicated `msg` kind `inac.v1`. Large payloads
travel as binary frames on the same WSS session. Authorization flows
through the attestation-gate (proposal 041) using one of four
sources: general capability passport, custody passport, invitation
passport, or attestation alone.

The kind registry is **open**: baseline artefact shapes are
`agora-record.v1` and `memarium-blob.v1`; additional kinds plug in
through the same `middleware-module-report` extension idiom as
peer-message kinds.

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
| `memarium-blob.v1` | generic Memarium-native artefact envelope (content-addressed `blob/id`, domain `memarium.blob.v1`) | ❌ not started — described in proposal 042 §2.2 in prose; schema file to write |
| `inac-control.v1` (tentative name) | control-message envelope for `offer`/`request`/`push` operations + response frames | ❌ not started |
| `agora-record.v1` | reused from proposal 035 | ✅ exists |
| `capability-passport.v1` (with `capability_id = "inac.invitation"` variant) | authorization artifact for invitation-based push | 🟡 base format exists; `inac.invitation` scope grammar and single-use rule to document in proposal 024 (042 Follow-Up #5) |

## Layer 1 — Peer-message kind registration

INAC operations are peer messages under the `PeerMessageChain`
(proposal 027).

| Item | State |
|---|---|
| Register `inac.v1` as a `msg` kind in the reference peer-message registry | ❌ not started |
| Document the message envelope under `peer-message-invoke.v1` forwarding rules | ❌ not started |
| Add `handles_artifact_kinds` field to `middleware-module-report` (mirrors `handles_peer_message_types`) | ❌ not started |
| Document registration semantics for kind claims (precedence, conflict detection, startup warning on shadowing) | ❌ not started |

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
| Control-message schemas (`inac-control.v1` envelopes for each op + response frame) | ❌ not started |
| Refusal-code vocabulary extension in proposal 041 §6 | ❌ not started |
| Query/filter grammar for `request` (reuse of proposal 035 §8 selectors where possible) | ❌ not started |

## Layer 3 — Binary-frame streaming

Large payloads travel on the same WSS session as binary frames,
tagged with a session-scoped `stream-id`. Proposal 042 §3.4 is the
contract.

### Rules

- control message carries `blob/payload = { ref: "sha256:…",
  size-bytes, stream-id }`,
- chunks carry the `stream-id` in their frame header,
- receiver reassembles → recomputes `sha256` → MUST refuse with
  `content-hash-mismatch` on mismatch,
- abort control frame cancels mid-stream without invalidating the
  authorizing passport,
- inline base64 allowed only below the configured ceiling
  (proposed default 64 KiB, per-node / per-peer / per-kind
  configurable).

### Placement

The binary-frame discipline is a **transport concern** and belongs
in proposal 002, not in INAC proper (042 Follow-Up #6). INAC is a
consumer of this framing, not its author.

### Status

| Component | State |
|---|---|
| WSS binary-frame discipline documented in proposal 002 | ❌ not started (042 Follow-Up #6) |
| Sender-side stream serializer | ❌ not started |
| Receiver-side reassembler + hash verifier | ❌ not started |
| Abort frame handling | ❌ not started |
| Per-peer / per-kind inline-ceiling configuration surface | ❌ not started |

## Layer 4 — Authorization (attestation-gate consumer)

Every inbound INAC operation passes through the attestation-gate
(proposal 041 §9). Four authorization sources map to gate predicates
as described in proposal 042 §5.

### Status

| Component | State |
|---|---|
| Attestation-gate crate (shared with Agora) | ❌ not started |
| `PassportResolutionCache` (shared with Agora) | ❌ not started |
| General-capability-passport verifier path | ❌ not started |
| Custody-passport verifier path (enforces `max_bytes`, `max_records`, `duration` from scope) | ❌ not started |
| Invitation-passport verifier path (expiry, single-use consumption log, scope match) | ❌ not started |
| Attestation-only fallback (for `offer` and for per-kind policies that allow unsolicited accept) | ❌ not started |
| Per-peer rate budgets (for `offer` vs `push`) | ❌ not started |

## Layer 5 — Kind dispatch and storage targets

Once authorization passes, dispatch routes the artefact to the
registered handler for its `schema`.

### Baseline handlers

| Schema | Handler | Storage target | State |
|---|---|---|---|
| `agora-record.v1` | Agora-relay subsystem when present (re-ingest through the relay); otherwise Memarium opaque store | Agora SQLite + subject index, **or** Memarium | 🟡 Agora ingest exists; Memarium opaque-envelope storage for records not present on local Agora not started |
| `memarium-blob.v1` | Memarium directly | Memarium | ❌ not started (schema and storage path) |

### Open-kind handlers

A module registers `handles_artifact_kinds` in its
`middleware-module-report`; INAC looks up the handler per operation.
Safety floor (§Invariant 7) applies: unknown registered kind with no
handler → `kind-not-supported`.

### Status

| Component | State |
|---|---|
| `handles_artifact_kinds` registry + lookup | ❌ not started |
| Precedence rule on shadowed kinds (proposal 042 Open Question #4; proposed default: first loaded wins + startup warning) | ❌ decision pending |
| Safety-floor refusal for unknown kinds | ❌ not started |
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
| `inac.invitation` scope grammar documented in proposal 024 (042 Follow-Up #5) | ❌ not started |
| Issuer-side: passport builder for invitations | ❌ not started |
| Receiver-side: single-use consumption log in Memarium | ❌ not started |
| Revocation channel (reuse of proposal 024 passport revocation) | 🟡 generic passport revocation exists; invitation-specific rate-limit/lifecycle interplay not designed |

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
| `node-address-attestation.v1` kind | ❌ deferred (042 Open Question #6) |

## Layer 8 — Middleware integration

INAC lives inside the daemon's peer plane, so its wiring is analogous
to proposal 027's peer-message dispatch.

| Component | State |
|---|---|
| `inac.v1` peer-message handler registered in the `PeerMessageChain` | ❌ not started |
| Sidecar-registration path (so Python/other-language modules can claim kinds via `handles_artifact_kinds`) | ❌ not started |
| Daemon supervisor readiness: kind registry is resolved at init, not at first request | ❌ not started |

## Open decisions blocking implementation

1. **Inline-ceiling defaults and configurability surface.**
   Proposed 64 KiB default; operators configure per-node,
   per-peer, per-kind. Decision: where in config schema
   (daemon-level? per-middleware-module? per-kind registration?).

2. **Single-use consumption semantics for invitation passports.**
   Is single-use the default, or is it an opt-in scope field? What
   is the consumption granularity — per-peer, per-artifact-id,
   per-schema? Decision lives in proposal 024 scope grammar
   extension.

3. **Kind-shadowing precedence (042 Open Question #4).**
   Proposed default: first-loaded wins with operator warning.
   Alternative: explicit ordering in config. Decision informs
   Layer 5 dispatch.

4. **Offer-without-intent policy default (042 Open Question #3).**
   Proposed default: allowed but rate-limited per source node id.
   Decision informs Layer 4 per-peer rate budgets.

5. **Opaque-envelope storage for `agora-record.v1` on nodes without
   a local Agora-relay subsystem.** If a node receives an
   `agora-record.v1` via INAC but runs no Agora relay, does it
   store the envelope in Memarium (allowing later re-ship per
   proposal 040) or refuse? Proposal 042 §5 implies allow;
   confirm and specify Memarium storage shape.

6. **Streaming abort semantics.** After abort, does the passport
   remain usable for a retry of the same artefact, or does abort
   count as consumption? Affects invitation passport lifecycle
   (Layer 6).

## MVP boundaries

- inline-only payloads in v1 (no binary-frame streaming). Artefacts
  above the ceiling → `push` refused with `storage-full` until
  Layer 3 lands. This lets Layer 2 (control protocol) ship before
  Layer 3 (streaming);
- two baseline kinds only (`agora-record.v1`, `memarium-blob.v1`);
  `handles_artifact_kinds` registry lands after baseline works;
- no session-level kind handshake in v1 (authoritative routing
  per-operation is sufficient);
- no `node-address-attestation.v1` kind (042 Open Question #6 is
  explicitly deferred);
- single-custodian flows in v1 (multi-custody is allowed per
  proposal 040 §3 but the INAC protocol does not coordinate
  custodians — each operates independently);
- no automatic INAC-to-Agora promotion (cross-surface migration is
  a consumer's concern, e.g. whisper durable promotion; INAC
  itself does not migrate).

## Recommended commit order

Each step leaves the tree compiling.

1. **Resolve open decisions 2 (invitation single-use semantics),
   3 (shadowing precedence), 4 (offer rate default).** Cheap;
   unblocks schemas and gate.
2. **Layer 0 — schemas.** `memarium-blob.v1` first, then
   `inac-control.v1` control-message envelopes.
3. **Attestation-gate (proposal 041).** Shared primitive; blocks
   Layer 4.
4. **`inac.invitation` scope grammar documented in proposal 024.**
   Blocks Layer 6.
5. **Layer 4 — authorization.** Verifier paths for all four sources.
6. **Layer 5 — baseline kind dispatch.** `agora-record.v1` +
   `memarium-blob.v1` handlers only; `handles_artifact_kinds`
   registry omitted.
7. **Layer 2 — control protocol.** `offer` / `request` / `push` +
   responses, inline-only payloads.
8. **Layer 1 — peer-message registration.** Register `inac.v1`
   with the `PeerMessageChain`.
9. **Layer 6 — invitation lifecycle.** Issuer + receiver +
   consumption log.
10. **Layer 8 — middleware integration.** Daemon wiring of the
    INAC handler.
11. **MVP ships here.** Consumers (whisper direct, custody
    transfer, crisis fan-out, passport handoff) start depending
    on INAC.
12. **Layer 3 — binary-frame streaming.** After proposal 002
    documents the transport-level framing.
13. **Layer 5 — `handles_artifact_kinds` open registry.** Unlocks
    third-party middleware kind extensions.
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
- **Streaming hash-mismatch test** (post-MVP Layer 3): an
  intentional byte-flip in a chunk MUST trigger
  `content-hash-mismatch` refusal; no partial-commit residue on
  the receiver.
