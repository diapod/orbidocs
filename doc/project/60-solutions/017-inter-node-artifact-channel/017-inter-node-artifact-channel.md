# Inter-Node Artifact Channel (INAC)

INAC is the planned peer-to-peer artifact exchange surface for moving
byte-identical Orbiplex artifacts between nodes without publishing them through
a public substrate.

It is layered above authenticated peer sessions and parallel to Agora:

- Agora is topic-addressed public or semi-public relay.
- INAC is direct node-to-node artifact transfer.
- Memarium remains the local custody store.

The current solution status is **planned**. Proposal 042 defines the semantic
contract; the implementation guideline in this directory decomposes the work
into schemas, peer-message registration, authorization, binary streaming, and
storage integration.

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
- Route accepted artifacts to Agora, Memarium, or a registered middleware
  handler depending on artifact kind.
- Keep large payload bytes out of the JSON control plane by using
  content-addressed binary-frame streams.

## Status

Planned. The solution has an implementation outline and baseline artifact
contracts, but the peer-message kind, control schemas, binary stream handling,
and authorization gate are not implemented as a complete runtime slice yet.

## Related Schemas

- `agora-record.v1`
- `memarium-blob.v1`
- future `inac-control.v1`
- `capability-passport.v1`

