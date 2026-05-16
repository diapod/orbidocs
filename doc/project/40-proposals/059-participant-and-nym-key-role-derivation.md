# Proposal 059: Participant, Nym, and Routing-Subject Key-Role Derivation

Based on:
- `doc/project/20-memos/participant-seed-contract-v1.md`
- `doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/030-identity-recovery-service.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/037-generic-signing-service.md`
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
- `doc/schemas/pseudonym-vault.v1.schema.json`

## Status

Draft

## Date

2026-05-16

## Executive Summary

Orbiplex already has one concrete role split in the Node networking layer:
Ed25519 signs long-lived identity artifacts while a static X25519 key-agreement
surface is deterministically derived for session establishment. Participant,
nym, and routing-subject handling, however, still mostly speaks in terms of one
signing key and does not yet define a coherent model for encryption, local
secret storage, or private recovery without publicly exposing `participant-id`.

This proposal extends the same layered discipline to participant, nym, and
routing-subject material.

Key decisions:

1. The current `orbiplex-participant-seed-v1` signing derivation remains stable
   and backward compatible; existing `mnemonic -> participant:did:key:...`
   mapping must not change.
2. New key roles are added through deterministic, versioned derivation from a
   participant root seed, not by ad-hoc chaining from one private key into the
   next.
3. `participant/vault-wrap` is a local symmetric wrapping purpose for encrypted
   vault storage, not a public wire identity.
4. Nyms SHOULD use random per-nym local seeds stored inside an encrypted
   participant-owned vault rather than being fully deterministically derived
   from the participant root.
5. Routing subjects (`routing:did:key:...`) SHOULD follow the same private
   vault discipline as nyms, but with delivery/contact semantics rather than
   authorship semantics.
6. `pseudonym-vault.v1` is the first schema seed for this private vault. It MAY
   be synchronised to external storage, but only
   as an opaque, encrypted, versioned blob with no public `participant-id`
   disclosure.
7. Public envelopes and encrypted payload metadata MUST NOT expose participant
   recovery recipients or otherwise reveal `nym -> participant` or
   `routing-subject -> participant` linkage.

## Context and Problem Statement

Orbiplex currently freezes the following relevant pieces:

- `orbiplex-participant-seed-v1` defines participant creation/import from a
  BIP39 mnemonic and yields one stable Ed25519 participant signing identity.
- `participant-key-envelope.v1` protects participant signing material at rest
  with a local passphrase-controlled envelope.
- Node transport already uses a deterministic Ed25519-to-X25519 split for
  static key agreement in the peer-session handshake.
- `nym-certificate.v1` defines pseudonymous authorship and certification, but
  does not yet define how nym private material is recovered, rotated, or stored
  without leaking participant linkage.
- `routing-subject-binding.v1` already defines a public
  `routing:did:key:...` delivery/contact surface with an Ed25519 signature plus
  a separate `encryption/key/public`, but it does not yet define how that
  routing-subject material is privately derived, stored, or recovered.

This leaves several gaps:

1. There is no stable participant-facing model for key roles beyond signing.
2. There is no private, syncable vault model for nym or routing-subject secret
   material.
3. A naive multi-recipient encryption envelope that includes a participant
   recovery key on the wire would leak participant linkage in public metadata.
4. A naive design that derives every nym or routing subject deterministically
   from one participant secret would maximize blast radius and reduce privacy
   isolation.

Orbiplex needs a design that preserves:

- stable participant identity derivation,
- pseudonymous nym publication,
- privacy-preserving routing-subject delivery/contact surfaces,
- no public `participant-id` leakage in recovery paths,
- deterministic recovery where it helps,
- and layered separation between signing, transport DH, and local sealed
  storage.

## Existing Facts

1. `requirements-006-node-networking-mvp.md` already permits deterministic
   static X25519 derivation from the Ed25519 node identity for MVP transport.
2. `participant-seed-contract-v1.md` freezes the participant signing path as
   BIP39 -> PBKDF2-SHA512 -> SLIP-0010 Ed25519 -> `m/44'/2268'/0'`.
3. `participant-key-passphrase-lock.md` protects a participant signing key at
   rest, but still treats the protected payload as one signing secret rather
   than a role-partitioned vault.
4. `nym-certificate-and-renewal-baseline.md` models nym authorship and
   certification, but not nym encryption-key recovery or vault synchronisation.
5. `routing-subject-binding.v1` already treats `routing:did:key:...` as a
   signed public routing subject and carries a separate
   `encryption/key/public` for delivery/contact use.

## Goals

- Preserve the existing stable participant signing identity path.
- Introduce a participant-facing key-role derivation model that is compatible
  with the current signer and recovery-seed baseline.
- Provide a clean private-storage model for nym and routing-subject secret
  material without public participant linkage.
- Make encrypted backup and cross-device sync of nym and routing-subject
  material possible.
- Keep wire protocols and recovery storage stratified.

## Non-Goals

- This proposal does not replace `orbiplex-participant-seed-v1`.
- This proposal does not define a public nym-to-participant recovery service
  API.
- This proposal does not add a public recovery recipient to message envelopes.
- This proposal does not define social recovery, threshold custody, or HSM-only
  operation.
- This proposal does not require all nyms or routing subjects to be
  deterministically derived from one root.

## Options Considered

### Option A: Fully deterministic pseudonym derivation from the participant root

Benefits:

- minimal local state,
- easy regeneration of all nym and routing-subject keys from one seed.

Risks:

- one participant-root compromise compromises all pseudonyms,
- weaker isolation between nyms and routing subjects,
- difficult partial retirement and migration,
- stronger pressure toward metadata linkage mistakes.

### Option B: Public multi-recipient envelopes with participant recovery key

Benefits:

- conventional hybrid-encryption recovery pattern,
- participant can decrypt any nym-targeted or routing-targeted payload.

Risks:

- envelope metadata risks exposing a stable participant recovery recipient,
- public wire artifacts become a linkage oracle,
- directly conflicts with the requirement to avoid public `participant-id`
  exposure.

### Option C: Deterministic participant role roots plus encrypted private pseudonym vault

Benefits:

- preserves stable participant signing identity,
- adds explicit role split,
- keeps participant linkage off the wire,
- allows cross-device sync via ciphertext-only blobs,
- gives better per-pseudonym isolation than full deterministic derivation.

Costs:

- requires a private vault format and local sync lifecycle,
- requires a recovery/export story stronger than raw signing-key export.

## Decision

Orbiplex adopts **Option C**.

### 1. Stable participant signing path remains unchanged

`orbiplex-participant-seed-v1` remains the canonical signing identity path for
`participant:did:key:...`.

The current mapping:

```text
BIP39 mnemonic
-> PBKDF2-SHA512 seed
-> SLIP-0010 Ed25519
-> m/44'/2268'/0'
-> participant signing key
-> participant:did:key:...
```

MUST remain backward compatible.

New key-role derivation MUST be additive. It must not silently remap existing
mnemonics to different participant identifiers.

### 2. Participant key roles are derived from a root-seed layer, not chained from ad-hoc private keys

The model introduces a conceptual participant root-seed layer.

For mnemonic-backed participants this is the mnemonic-derived seed material
before the final signing-key projection. Future implementations MAY materialise
that layer explicitly; current implementations MAY keep it implicit as long as
compatibility is preserved.

Role-specific derivation must be deterministic, versioned, and domain-separated.
Representative labels:

```text
orbiplex/v1/participant/signing
orbiplex/v1/participant/dh
orbiplex/v1/participant/vault-wrap
orbiplex/v1/participant/recovery-wrap
```

The core invariant is:

- one root material,
- multiple role-specific derivation contexts,
- no informal “private key A becomes private key B” chaining.

### 3. Participant roles

The minimum role model is:

1. `participant/signing`
   - algorithm: Ed25519,
   - public role: authorship, consent, capability issuance, governance-bound
     participant actions,
   - stable public identifier anchor.

2. `participant/dh`
   - algorithm: X25519 or later equivalent,
   - private role: direct key agreement, sealed-session or recipient-side
     private communication where a participant-scoped DH surface is needed,
   - not required to be publicly advertised in MVP.

3. `participant/vault-wrap`
   - algorithm class: symmetric AEAD wrapping key derived from the participant
     root,
   - private role: encrypting participant-owned vault snapshots and local secret
     stores,
   - never a public wire identity.

4. `participant/recovery-wrap` (deferred but reserved)
   - private role: future escrow or recovery-bundle sealing distinct from both
     signing and ordinary vault wrap.

### 4. Nym and routing-subject private material live in an encrypted vault

Nyms SHOULD NOT be fully and publicly predictably derived from the participant
signing identity.

Instead, each nym SHOULD have its own local seed material:

```text
nym-seed -> nym/signing
nym-seed -> nym/dh
```

The `nym-seed` SHOULD be random and per-nym.

This material is stored inside an encrypted participant-owned vault protected by
`participant/vault-wrap`.

This gives:

- stronger separation between nyms,
- easier retirement of one nym without touching the others,
- no public participant recovery recipient on the wire,
- local recoverability after node loss.

Routing subjects SHOULD use the same storage pattern:

```text
routing-subject-seed -> routing-subject/signing
routing-subject-seed -> routing-subject/dh
```

Important boundary:

- `routing:did:key:...` is not merely an opaque route label;
- it is a delegated/public routing subject anchored in a signing key;
- `routing-subject-binding.v1` additionally carries a separate
  `encryption/key/public` for reply/contact delivery.

This makes `routing-subject` closer to a delivery/contact pseudonym than to a
plain advisory route label.

### 5. Private vault sync model

The first schema seed for this model is:

- `doc/schemas/pseudonym-vault.v1.schema.json`

The vault MAY be synchronised across devices or to external storage, but only as
an opaque ciphertext blob.

The remote store must see only technical metadata needed for retrieval and
rollback detection, for example:

```json
{
  "schema": "pseudonym-vault.v1",
  "vault/id": "pseudonym-vault:01JV...",
  "vault/version": 17,
  "vault/profile": "participant-private-pseudonyms",
  "contents/kinds": ["nym", "routing-subject"],
  "crypto/kdf": "hkdf-sha256",
  "crypto/aead": "xchacha20-poly1305",
  "crypto/wrap-purpose": "participant/vault-wrap",
  "salt": "...",
  "nonce": "...",
  "ciphertext": "...",
  "supersedes": "pseudonym-vault:01JU..."
}
```

The store SHOULD NOT learn:

- `participant-id`,
- nym public identifiers as explicit metadata,
- routing-subject public identifiers as explicit metadata,
- plaintext nym handles,
- vault contents.

A synchronised vault is therefore:

- encrypted,
- versioned,
- mutable as local secret state,
- but not a public append-only fact stream.

### 6. Advisory route ids are a separate class from routing subjects

Orbiplex currently has two route-like surfaces that must not be conflated:

1. `route:...`
   - an advisory route id, for example in TLS certificate CN extraction and
     endpoint consistency checks,
   - may be an opaque operational label,
   - does not by itself imply a private keypair.

2. `routing:did:key:...`
   - a delegated/public routing subject,
   - anchored in an Ed25519 signing identity,
   - usually paired with a separate encryption public key for contact/delivery.

This proposal concerns the second class. Opaque advisory `route:` labels do not
need vault recovery semantics unless a future proposal explicitly elevates them
into cryptographic subjects.

### 7. Wire privacy invariant

Public or federated payloads MUST NOT expose a participant recovery recipient as
an ordinary encryption recipient when the intention is pseudonymous delivery.

If a payload is addressed to a nym or routing subject, the public artifact may
reveal:

- the nym or routing-subject public identity,
- the relevant signature,
- attached or inline proof material.

It MUST NOT reveal:

- a public `participant-id` recovery recipient,
- a stable recipient handle that trivially maps back to the participant,
- explicit `nym -> participant` or `routing-subject -> participant`
  correlation metadata.

### 8. Recovery and export consequence

The current fallback export path that yields only raw participant private-key
material is not sufficient for full future role recovery.

If Orbiplex wants recoverable participant DH roles and private vault
restoration, then operators SHOULD preserve one of:

- the participant mnemonic / root recovery material,
- or a role-aware encrypted recovery bundle that includes enough material to
  restore the role tree and the private vault.

Raw signing-key-only export is therefore a legacy-compatible minimum, not a
future-complete recovery shape.

## Proposed Model / Sequence

### Scenario: restore after node loss

1. The operator creates a participant from `orbiplex-participant-seed-v1`.
2. The node derives the stable participant signing identity.
3. The node derives `participant/vault-wrap` from the same participant root.
4. The node creates one or more nyms and routing subjects with random local
   seeds.
5. The node stores those seeds and local metadata inside a private encrypted
   vault.
6. The vault is encrypted locally and synchronised as ciphertext to one or more
   storage targets.
7. The node fails or the device is lost.
8. The operator imports the participant mnemonic or equivalent root recovery
   material on a new node.
9. The new node recreates the same participant signing identity and
   `participant/vault-wrap` material.
10. The new node downloads the latest encrypted vault snapshot, decrypts it,
    and restores the nym and routing-subject seeds.
11. The restored seeds recreate the nym and routing-subject signing and DH
    roles without any public disclosure of the participant recovery path.

## Trade-offs

### Benefits

- Preserves backward compatibility for participant identity.
- Reuses the same conceptual split already accepted for node networking.
- Keeps pseudonymous linkage off the wire.
- Supports private backup and cross-device sync.
- Covers both public-authorship pseudonyms and delivery/contact pseudonyms.
- Keeps signing, DH, and local sealed-storage semantics separate.

### Risks and Constraints

- Introduces a new local-state artifact that must be versioned and audited
  carefully.
- Makes raw signing-key-only recovery increasingly insufficient.
- Requires care in KDF label stability and migration.
- Requires explicit operator UX for vault sync, restore, and conflict handling.

## Failure Modes and Mitigations

| Failure mode | Impact | Mitigation |
|---|---|---|
| Participant root or mnemonic is compromised | All participant-scoped derived roles are compromised | Encourage passphrase lock, optional extra local secret factor, and explicit recovery hygiene. |
| One nym or routing-subject key is compromised | One pseudonymous surface is compromised, but others should remain isolated | Keep per-nym and per-routing-subject random seeds; do not derive every public pseudonymous surface directly from one public derivation path. |
| Vault ciphertext is tampered with or rolled back | Stale or corrupted nym/routing state | Use AEAD integrity, version counters, and `supersedes` / rollback detection. |
| Only raw signing-key export survives | Participant id can be restored but extended roles or private vault contents cannot | Mark raw signing-key export as legacy-minimum recovery only; add role-aware recovery bundle later. |
| Public envelope accidentally includes participant recovery recipient | Pseudonymous linkage leak | Make this a schema and policy violation at the envelope boundary. |
| `route:` and `routing:did:key:` are conflated in implementation | Wrong recovery model or false key assumptions | Keep advisory `route:` handling separate from cryptographic `routing-subject` handling. |

## Open Questions

1. Should the participant root-seed layer be made explicit as a stable local
   artifact, or remain implicit behind recovery flows?
2. Should `participant/dh` ever be publicly discoverable, or remain a local
   capability surfaced only through controlled direct protocols?
3. What is the minimal vault shape that supports sync, restore, rollback
   detection, and future partial rotation for both nyms and routing subjects?
4. Should vault wrapping be derived only from participant root material, or from
   root material plus a second local factor by default?
5. How should multiple concurrently edited vault snapshots merge across devices?

## Consequences

### Short-term

- No existing participant identifiers change.
- Node and docs gain a clean target for participant/nym/routing-subject
  recovery work.
- Future pseudonym privacy work stops relying on public participant recovery
  recipients.

### Long-term

- Role-aware participant recovery can replace signing-key-only export.
- Nym and routing-subject key rotation, vault sync, and cross-device restore
  gain one coherent foundation.
- Public protocol artifacts stay stratified: pseudonymous authorship and
  contact/delivery remain on the envelope/discovery boundary, while recovery and
  local secret storage remain private.

## Next Actions

1. Promote `pseudonym-vault.v1` from first schema seed to runtime import/export
   support in Node.
2. Define a role-aware participant recovery bundle that supersedes raw
   signing-key-only fallback export.
3. Add explicit signer and/or sealer purpose labels for
   `participant/signing`, `participant/dh`, and `participant/vault-wrap`.
4. Decide whether `participant/dh` needs any protocol-visible projection in MVP
   follow-up work, or should remain fully local.
5. Add negative tests and schema-gate policy for accidental participant
   recovery-recipient leakage in pseudonymous envelopes.
