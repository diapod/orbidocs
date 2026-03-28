# Nym-Authored Payload Verification

## Status

Memo

## Date

2026-03-28

## Purpose

This memo freezes a reusable verification note for application artifacts authored
through a `nym` rather than through a directly disclosed `participant-id`.

It is intentionally small and operational. It does not redefine the nym
certificate lifecycle. It only states how receivers should reason about a
nym-authored payload once the artifact family chooses that embedding pattern.

## Scope

This note applies above the encrypted node-to-node session.

It does not apply to:

- `peer-handshake.v1`,
- `node-advertisement.v1`,
- keepalive or reconnect,
- or any transport-layer rate limit bucket.

## Reusable Verification Sequence

For a nym-authored application payload, the receiving side should verify:

1. **Node-level carrier trust**
   - the artifact arrived over a valid node-scoped session,
   - routing identity remains `node-id`, not `nym`.
2. **Council trust**
   - parse `issuer/id` from the attached `nym-certificate`,
   - require canonical `council:did:key:...`,
   - check whether that council is in the local trusted council list.
3. **Certificate integrity**
   - verify the council signature over the attached `nym-certificate`.
4. **Certificate freshness**
   - require the certificate to be inside its validity window,
   - or, if the artifact family explicitly allows it, inside its narrower
     continuity-only leniency semantics.
5. **Nym binding**
   - require the payload's local nym field to match the `nym/id` certified by the
     attached `nym-certificate`.
6. **Payload signature**
   - verify the payload signature using the public key implied by the certified
     `nym:did:key:...`.

If any of these checks fail, the receiver rejects the payload.

## Architectural Consequence

This keeps the layers clean:

- transport trusts infrastructure,
- the application artifact trusts council attestation plus nym possession,
- and the hidden participant remains behind the issuing side of the boundary.

## Abuse Control

Even for nym-authored payloads:

- transport throttling stays per `node-id`,
- peer degradation remains node-scoped,
- and application-level pseudonym validation does not create a new transport
  identity bucket.

## Promote To

Promote into proposal or requirements when:

- more than one application family depends on the same note,
- or the project wants one shared reusable envelope for nym-authored payloads.
