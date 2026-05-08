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

The schema-gated control plane and local runtime skeleton are implemented. The
runtime intentionally fails closed when no authoritative handler is registered
for an artifact kind. `push` requires exactly one payload location
(`bytes/base64url`, `artifact/ref`, or `artifact/href`). The local MVP scaffold
is operationally inline-first: referenced payload locations are schema-valid,
but require a future resolver/fetch or binary streaming contract before
production peer transfer can accept them. Direct component calls to `inac.*`
host capabilities are governed by INAC outbound allowlists; Artifact Delivery
routes that happen to use `inac-direct` are governed by Artifact Delivery
outbound allowlists. Full WSS peer-message wiring, binary-frame streaming,
passport/invitation authorization, and concrete Agora/Memarium handlers remain
outside the MVP scaffold.

## Related Schemas

- `agora-record.v1`
- `memarium-blob.v1`
- `inac-control.v1`
- `capability-passport.v1`

## Related Solutions

- [Artifact Delivery](../023-artifact-delivery/023-artifact-delivery.md)
