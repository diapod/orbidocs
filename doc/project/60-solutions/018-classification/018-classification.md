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
- Keep declassification explicit and append-only: transformation evidence may
  justify an act but never lowers a tier by itself.
- Derive lowered tiers only for an exact surface/topic/time under an explicit
  revocation view, and persist one-shot consumption before the effect.
- Allow future public, pseudonymous, private, and peer-forwarding paths to share
  one label vocabulary without forcing one global policy engine.

## Status

Implemented hard-MVP. The accepted `classification.v1` schema and
`orbiplex-node-classification` crate provide the shared label vocabulary,
contextual effective-tier derivation, projection-aware bound subjects,
quarantine markers, stable denial codes, and common egress helpers used by
Memarium, Agora, Whisper, INAC/private Artifact Delivery, local archival
export, and adjacent host boundaries. Context-free reads retain the immutable
source tier and policy trail. `evaluate_egress` accepts an explicit revocation
predicate and returns append-only one-shot use claims; the simpler
`authorize_egress` fails closed when no authority store is available.

One-shot use is represented by a `classification-declassify-consumed` Memarium
policy fact. Read projections fold that fact into `mode.consumed_at` without
mutating the original `DeclassifyFact`. Persistent exceptions verify both their
TTL and exact expiry, and an absent revocation anchor makes an exception inert.

Post-MVP work remains deliberately outside this solution slice: whole-program
information-flow control, per-field labels, complete historical backfill,
richer quarantine/operator UI, a pooled/batched SQLite projection read path,
and future downstream forwarding surfaces that need stronger product
affordances. An open-world Agora schema that is not declared Memarium-derived
may remain unlabelled; known Memarium-native content schemas fail closed when a
label is stripped.

## Related Schemas

- `classification.v1`
- `memarium-host-api.v1`
- `archival-package.v1`
- `artifact-delivery-envelope.v1`
