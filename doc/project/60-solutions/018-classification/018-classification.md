# Classification

Classification is the shared label and propagation layer used to carry
privacy, disclosure, and egress constraints across Memarium, Agora, archival
exports, and future peer-forwarding paths.

The solution is intentionally small: it does not decide social policy by
itself. It gives other components a common data contract for saying what a
payload may be used for, where it may flow, and whether a later transformation
or declassification fact changed the effective tier.

## Based On

- [Proposal 047: Classification Label Propagation](../../40-proposals/047-classification-label-propagation.md)
- [Classification schema](../../../schemas/classification.v1.schema.json)
- [Memarium solution](../002-memarium/002-memarium.md)
- [Agora solution](../008-agora/008-agora.md)

## Responsibilities

- Represent classification labels as data, not as hidden runtime state.
- Preserve labels through Memarium entry/fact storage and archival export.
- Provide edge guards for public and private egress surfaces such as Agora,
  Whisper, INAC/private Artifact Delivery, and archival export.
- Keep declassification explicit and append-only through transformation or
  declassification evidence.
- Allow future public, pseudonymous, private, and peer-forwarding paths to share
  one label vocabulary without forcing one global policy engine.

## Status

Draft / partial. The `classification.v1` schema and core propagation concepts
exist, and Memarium, Agora, Whisper, INAC/private Artifact Delivery, and local
archival export now consume the shared egress helper. Richer operator UI,
production schema freeze, and future downstream forwarding surfaces remain
implementation work.

## Related Schemas

- `classification.v1`
- `memarium-host-api.v1`
- `archival-package.v1`
- `artifact-delivery-envelope.v1`
