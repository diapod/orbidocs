# Node Identity Layering and Upgrade Path

This memo captures one architectural direction for Orbiplex Node identity:

- use a `did:key`-compatible fingerprint as the atomic Node identity anchor,
- keep that atomic anchor stable and simple,
- and reserve a later optional upgrade path to a richer mutable identity method.

The goal is to avoid over-designing identity before the first networking slice is
working, while still preserving a clean path toward key rotation, mutable
capability binding, and reputation continuity.

## Atomic Node identity first

For the baseline networking layer, the most useful identity is the smallest one:

- one public-key-derived Node anchor,
- one stable `node-id`,
- and one auditable relation between that anchor and signed network artifacts.

This is why the current Node baseline uses a `node:did:key:...`-shaped identifier.
The important property is not "full DID support". The important property is that
the fingerprint is:

- deterministic,
- portable,
- self-certifying,
- and cheap to verify across runtimes.

That atomic anchor is enough for:

- advertisements,
- handshake validation,
- keepalive and reconnect,
- and the first reputation-adjacent traces.

## Why not start with mutable identity

If we start the networking seed with a mutable registry-backed identity, we
complect:

- key material,
- key rotation,
- reputation state,
- capability attachment,
- and policy/governance semantics.

That is too much for the first interoperable Node.

The atomic key anchor should therefore stay small and local. It is closer to a
cryptographic fact than to a socially rich identity object.

## Upgrade path: richer method later

Later, Orbiplex may introduce a richer method such as:

- `did:orb`

This would not replace the usefulness of the atomic key anchor. It would layer
above it.

The natural role of such a method would be:

- key rotation,
- continuity across key changes,
- mutable binding of capabilities,
- mutable reputation state,
- federation-aware trust or policy metadata,
- and possibly explicit revocation or deactivation semantics.

In that design, the key itself does not have to change often. What needs to be
mutable is the binding between:

- one or more keys,
- capability claims,
- reputation state,
- and continuity metadata.

## Practical interpretation

The architecture should therefore distinguish at least two strata:

### 1. Atomic Node anchor

- key-derived,
- self-certifying,
- cheap to validate,
- narrow enough for networking MVP.

Examples:

- `node:did:key:...`
- or a future directly carried `did:key:...` form if Orbiplex ever chooses that.

### 2. Mutable continuity and reputation layer

- may refer to one or more atomic anchors,
- may survive key rotation,
- may bind capabilities and reputation,
- may carry federation-level or policy-level semantics.

This higher layer is the natural place for:

- "this rotated key still belongs to the same Node continuity line",
- "this Node currently has these recognized capabilities",
- "this Node currently has this trust or reputation standing".

## Relation to CORE-VALUES

If Orbiplex later defines a richer identity method, its registry semantics should
be inspired by the project values already expressed in `CORE-VALUES`:

- auditability over hidden authority,
- explicit provenance,
- federated rather than monolithic trust,
- and minimal irreversible centralization.

This does **not** imply one global reputation ledger. It implies that if a richer
identity layer exists, its mutability should remain:

- explicit,
- inspectable,
- policy-bounded,
- and compatible with federation-local interpretation.

## Guidance for current implementation work

For current Node development, this memo suggests:

1. keep the atomic `node-id` narrow and self-certifying,
2. avoid pushing reputation and rich capability semantics into the key-derived
   identifier itself,
3. treat mutable capability/reputation binding as a later layer,
4. leave room for a future method such as `did:orb` without making it a
   prerequisite for networking MVP.

## Promote when ready

Promote this memo to a proposal or requirements document when Orbiplex is ready
to freeze:

- key rotation semantics,
- continuity across key changes,
- mutable capability attachment,
- reputation binding,
- and the governance model of a richer identity method.
