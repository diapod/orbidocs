# Implementation Guidelines 032 — Three Concrete Decisions

Supplement to `032-key-delegation-passports-impl.md`.

Each section records one concrete decision that materially shapes the
implementation.

## Decision 1 — revocations target either passports or delegations

### Context

`CapabilityPassportRevocation.passport_id` used to be a mandatory capability
passport identifier. That shape is too narrow once the same revocation artifact
must also revoke `key-delegation.v1` entries.

### Decision

Generalize the target model:

```rust
pub passport_id: Option<String>,
pub target_id: Option<String>,
```

Rules:

- exactly one of them must be present,
- `passport_id` means capability-passport revocation,
- `target_id` means delegation revocation.

### Why this is better

- backward-compatible for existing passport revocations,
- no need for a second revocation artifact just for delegations,
- one feed shape can drive invalidation for both passport cache and delegation
  cache.

### Edge rules

- `target_id` must validate against `delegation:key:`,
- `effective_target_id()` becomes the stable helper for consumers,
- `is_delegation_revocation()` remains a convenience, not the primary contract.

### Seed Directory impact

The `revocations` table gains `target_id`, and feed serialization should expose
both `passport_id` and `target_id`. Consumers then decide which cache to
invalidate.

## Decision 2 — reuse existing multibase helpers instead of inventing new key formatting

### Context

Proxy keys are represented as `did:key:...`, while the crypto helper surface
already knows how to derive public multibase values from Ed25519 verifying keys.

### Decision

Use the existing helper:

```rust
orbiplex_node_crypto::public_key_multibase_from_verifying_key(...)
```

and derive:

```text
did:key:<multibase>
key:did:key:<multibase>
```

from it.

### Why this is better

- one canonical `did:key` encoding path,
- no duplicate formatting logic inside daemon code,
- verification and generation use the same representation family.

### Practical implication

When verifying a proxy-signed capability passport:

- strip `did:key:` from `issuer/signing_key`,
- pass the raw multibase part to `verify_message_base64url(...)`.

Do not invent a second representation just for delegated signing.

## Decision 3 — reuse the existing key-unlock cache model for proxy keys

### Context

Proxy keys and participant keys differ semantically, but their unlock behavior
is very similar:

- optional encrypted-at-rest envelope,
- optional explicit unlock,
- temporary residence in memory for signing operations,
- TTL-driven eviction.

### Decision

Reuse the same cache mechanics for proxy keys rather than building a separate
unlock subsystem from scratch.

This does not mean proxy keys and participant keys become the same abstraction.
It only means they can share:

- unlock TTL behavior,
- in-memory zeroizable storage,
- `touch-and-copy` style access,
- eviction mechanics.

### Why this is better

- lower implementation surface,
- fewer subtly different lock/unlock flows,
- easier operator mental model.

### Constraint

Keep the semantic split explicit:

- participant keys remain sovereign identity keys,
- proxy keys remain scoped operational keys.

Reuse mechanics, not identity meaning.

## Consequence for the daemon surface

The daemon should expose:

- proxy key generate/import/list/unlock/delete flows,
- delegation issue/publish/revoke flows,
- capability passport issuance with an optional `proxy_key_id`.

All of them remain layered on top of:

- `CapabilityPassport`,
- `KeyDelegationPassport`,
- the generalized revocation target model.

That keeps the implementation stratified instead of encoding delegation logic as
special cases in unrelated surfaces.
