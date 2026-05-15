# Inter-Node Artifact Channel (INAC)

INAC is the planned peer-to-peer artifact exchange surface for moving
byte-identical Orbiplex artifacts between nodes without publishing them through
a public substrate.

It is layered above authenticated peer sessions and parallel to Agora, but the
component-facing delivery abstraction belongs to Artifact Delivery:

- Agora is topic-addressed public or semi-public relay.
- Artifact Delivery is the host-owned delivery and admission plane.
- INAC is the private/direct node-to-node transport adapter under that plane.
- Memarium remains the local custody store.

The current solution status is **partial / MVP scaffold**. Proposal 042 defines
the semantic contract; the implementation guideline in this directory
decomposes the work into schemas, peer-message registration, authorization,
binary streaming, and storage integration.

Implemented now:

- `inac-control.v1` as the transport-neutral control frame for `offer`,
  `request`, `push`, and response/refusal operations.
- `memarium-blob.v1` synchronized into the node schema gate as a transferable
  signed artifact envelope.
- `node/inac-core` for pure DTOs, operation validation, refusal vocabulary,
  inline payload ceiling, and byte identity checks.
- `node/inac-runtime` for an explicit artifact handler registry and fail-closed
  dispatch semantics.
  Local outbound allows are deny-by-default: empty `operations` or `schemas`
  sets do not mean wildcard authority.
- `node/inac-handlers` as the daemon composition point for future concrete
  handlers (`agora-record.v1`, `memarium-blob.v1`, middleware-owned kinds).
- Daemon host/operator surface:
  `POST /v1/host/capabilities/inac.offer`,
  `POST /v1/host/capabilities/inac.request`,
  `POST /v1/host/capabilities/inac.push`, and `GET /v1/inac/status`.
- `msg = "inac.v1"` registered in the daemon peer-message chain for WSS
  sessions. Artifact Delivery remote `inac-direct` targets use this path, and
  received `push` frames feed the shared Artifact Delivery inbound admission
  registry instead of a parallel INAC-specific dispatch table.
- Node endpoint dials enforce endpoint certificate evidence when discovery has
  it. Seed Directory node resolution can fetch `node-address-attestation.v1`,
  copy the selected `endpoint/certificate` fingerprint into the daemon's peer
  endpoint evidence companion, and the peer supervisor then carries that
  fingerprint into the concrete dial candidate. Static seed pins remain a
  bootstrap shortcut; attested endpoint evidence wins when both are present.
  Stale or expired attestations are ignored before they can become dial pins.
- The daemon exposes peer supervisor endpoint-evidence diagnostics for operator
  inspection. Fresh evidence can feed direct INAC delivery; usable/stale/dead
  evidence remains a discovery or troubleshooting hint and does not become a
  direct delivery target without fresh verification.
- Story-005 private/direct Whisper is wired as the first concrete vertical
  consumer of `AD -> inac-direct`: the sender produces a signed private
  `agora-record.v1` artifact, Artifact Delivery routes it to the configured
  peer, and the receiver feeds the push into the shared AD admission path.

## Based On

- [Proposal 042: Inter-Node Artifact Channel](../../40-proposals/042-inter-node-artifact-channel.md)
- [INAC implementation guidelines](./017-inter-node-artifact-channel-impl.md)
- [Agora relay implementation notes](../008-agora/008-agora-topic-addressed-relay-impl.md)
- [Whisper solution](../011-whisper/011-whisper.md)

## Responsibilities

- Exchange artifact offers, requests, pushes, and refusals over authenticated
  peer sessions.
- Keep artifact envelopes byte-identical across transfer and storage.
- Reuse existing authority surfaces such as capability passports,
  invitation/custody passports, and attestation-gate style verification.
- Feed received artifacts into the host-owned Artifact Delivery inbound
  admission path, which dispatches to exactly one authoritative acceptor.
- Keep large payload bytes out of the JSON control plane by using
  content-addressed binary-frame streams.

## Status

Partial / MVP scaffold.

The schema-gated control plane, local runtime skeleton, and WSS peer-message
transport are implemented. The runtime intentionally fails closed when no
authoritative handler is registered for an artifact kind. `push` requires
exactly one payload location (`bytes/base64url`, `artifact/ref`, or
`artifact/href`). The first remote path is inline-first over WSS peer messages;
referenced payloads can be resolved before admission through Artifact Delivery's
resolver registry, with `artifact-store:` as the first production resolver.
Direct component calls to `inac.*` host capabilities are governed by INAC
outbound allowlists; Artifact Delivery routes that happen to use `inac-direct`
are governed by Artifact Delivery outbound allowlists. Matrix mailbox transport
and binary-frame streaming remain outside the MVP scaffold. Receiver-side WSS
`push` authorization now has a first production gate: without an explicit
profile allowlist the frame must carry an inline `capability-passport.v1` under
`authorization`. Invitation passports (`capability_id = "inac.invitation"`),
general INAC push passports (`inac-push@v1`), and Memarium custody passports
(`capability_id = "memarium.custody"`, profile `memarium-custody@v1`) all pass
through the shared capability-binding authorization path before Artifact Delivery
admission. Rejected transfers are written to a local INAC transfer ledger before
Artifact Delivery admission. Passport authorization fails closed when the
receiver has no current revocation view source; the WSS peer identity still
authenticates the transport session, while the passport only authorizes that
verified peer to present a specific artifact push.

Baseline Artifact Delivery acceptors are now present for the two INAC baseline
artifact kinds. `agora-record.v1` is verified and re-ingested through the local
Agora service when available; absence of local Agora is an explicit handler
unavailable condition, not an implicit Memarium fallback. `memarium-blob.v1` is
verified as a Memarium blob envelope and stored through Memarium as an accepted
custody fact. The baseline acceptor requires an explicit
`signature.key/public`, rejects delegated blob signatures for now, and accepts
only encrypted/opaque custody envelopes. Plaintext/private blob custody remains
fail-closed unless a future explicit policy enables it. MVP custody facts are
written to the local public Memarium space; configurable target spaces are a
later custody-policy layer.

Inbound INAC budgets are receiver-side policy: they match remote node id,
operation, artifact schema, and optional content type, then refuse before
Artifact Delivery admission or notification creation. Refusals such as
`payload-too-large`, `rate-limited`, and `quota-exceeded` are local transfer
decisions, not public protocol judgments. A per-minute limit of zero is an
explicit `policy-denied` deny rule. Active pending offers are also bounded per
remote node before notification creation, so unsolicited `offer` cannot be used
as an unbounded local queue.

Invitation delivery and acceptance now uses the generic user/operator
notification queue. An unsolicited `offer` that passes schema, size, and budget
checks creates a local pending offer plus an operator notification with
host-owned `inac.invitation.accept` and `inac.invitation.reject` action refs.
Accepting issues a narrow `inac.invitation` passport and returns it on the next
matching `offer`; rejecting records the local decision without minting
authority. This notification flow is a local UX that issues a passport; it is
not a second INAC authority system and does not replace Artifact Delivery
admission. The receiver-issued invitation passport TTL is daemon policy
(`artifact_delivery_adapters.inac_peer_transport.invitation_passport_ttl_seconds`,
default 3600 seconds). Repeating `Accept` after the offer is already accepted
is idempotent and does not issue a replacement passport.

## Related Schemas

- `agora-record.v1`
- `memarium-blob.v1`
- `inac-control.v1`
- `capability-passport.v1`
- `node-address-attestation.v1`

## Related Solutions

- [Artifact Delivery](../023-artifact-delivery/023-artifact-delivery.md)
