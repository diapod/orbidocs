# Pseudonym Vault and Key Roles

`Pseudonym Vault and Key Roles` is the solution-level identity component that
turns Proposal 059 into runtime responsibilities for participant role derivation,
private nym continuity, cryptographic routing-subject continuity, and
role-aware recovery.

Status: `partial`

Date: `2026-05-17`

## Executive Summary

This component owns one narrow identity-storage boundary:

```text
participant mnemonic / recovery root
  -> stable participant signing identity
  -> participant role derivation
  -> participant/vault-wrap
  -> participant/recovery-wrap
  -> ciphertext-only pseudonym-vault.v1 snapshots
  -> private nym and routing-subject seed recovery
```

The MVP profile is intentionally conservative:

- keep `orbiplex-participant-seed-v1` stable;
- keep the participant root implicit behind recovery flows;
- derive `participant/dh`, `participant/vault-wrap`, and
  `participant/recovery-wrap` without changing the public participant id;
- keep `participant/dh` local-only and never publish it as a standing discovery
  artifact;
- store nym and `routing:did:key:...` seeds inside a private encrypted vault;
- support `root-only` vault wrapping by default and optional
  `root+local-passphrase` wrapping when the operator wants a second local
  factor;
- synchronize only opaque `pseudonym-vault.v1` snapshots;
- accept only single-writer linear vault updates;
- reject participant recovery-recipient leakage in pseudonymous or routing
  metadata.

## Context and Problem Statement

Proposal 059 closes the gap between stable participant signing and recoverable
pseudonymous operation. Before this component, Orbiplex had a stable participant
seed path and public nym / routing-subject artifacts, but no coherent runtime
owner for private nym seed storage, routing-subject seed storage, encrypted
vault sync, or role-aware participant recovery.

The solution must preserve four boundaries:

- participant signing identity remains backward compatible;
- `participant/vault-wrap` is private storage material, not a public wire
  identity;
- `route:...` stays an advisory routing identifier, while
  `routing:did:key:...` is a cryptographic routing subject;
- public envelopes must not reveal `nym -> participant` or
  `routing-subject -> participant` linkage through recovery metadata.

## Must Implement

### Stable Participant Role Derivation

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/20-memos/participant-seed-contract-v1.md`

Related schemas:

- `participant-key-envelope.v1`

Responsibilities:

- preserve the current `orbiplex-participant-seed-v1` signing path and known
  participant id vectors;
- derive role-specific material through versioned, domain-separated labels;
- expose `participant/signing`, `participant/dh`, and
  `participant/vault-wrap` as distinct purposes;
- keep `participant/dh` local-only: derivable on demand for controlled
  direct/sealed protocols, but not discoverable;
- expose `participant/recovery-wrap` as an internal-wrap purpose for local
  sealed recovery bundles;
- fail closed when only raw signing-key material is available and a role-root
  operation requires mnemonic or recovery-root material.

Status:

- `done` — Node derives the Proposal 059 role purposes while preserving the
  existing participant signing identity path. Pseudonym-vault and recovery
  bundle operations fail closed for raw signing-key-only participants.

### Ciphertext-Only Pseudonym Vault

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- validate `pseudonym-vault.v1` only at import/export boundaries;
- keep the outer artifact ciphertext-only and free of participant, nym, and
  routing-subject public identifiers;
- enforce runtime crypto semantics that JSON Schema cannot fully express, such
  as valid salt, nonce length, non-empty ciphertext, AEAD integrity, and stable
  AAD profile;
- store snapshots with `vault/version` and `supersedes` lineage;
- reject rollback imports and concurrent higher-version conflicts.

Status:

- `done` — Node mirrors the schema, gates import/export, stores sealed
  snapshots under the identity storage boundary, and enforces single-writer
  latest semantics with rollback and conflict rejection.

### Local Nym and Routing-Subject Creation

Based on:

- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `nym-certificate.v1`
- `routing-subject-binding.v1`
- `pseudonym-vault.v1`

Responsibilities:

- create nyms from random per-nym local seeds stored inside the encrypted vault;
- create cryptographic routing subjects from random per-subject local seeds
  stored inside the encrypted vault;
- derive each nym and routing subject into separate signing and DH roles;
- keep advisory `route:...` identifiers out of the vault recovery model unless
  a future proposal explicitly elevates them to cryptographic subjects;
- reseal the vault after local pseudonym mutation.

Status:

- `done` — Node exposes local nym and `routing-subject` creation through the
  host identity control plane and persists the resulting private seeds only
  inside sealed vault snapshots.

### Role-Aware Participant Recovery Bundle

Based on:

- `doc/project/40-proposals/030-identity-recovery-service.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- export enough mnemonic/recovery-root material to restore participant role
  derivation where policy allows export;
- support a legacy full-root export profile for compatibility;
- support a sealed-local profile whose payload is wrapped by
  `participant/recovery-wrap` and whose import requires the mnemonic/recovery
  root supplied separately;
- include latest sealed pseudonym-vault snapshots as opaque ciphertext blobs;
- restore the role tree and sealed vault snapshots without exposing participant
  linkage in public artifacts;
- make raw signing-key-only export explicit as legacy-minimum recovery, not full
  role recovery.

Status:

- `done` — Node has a role-aware participant recovery bundle import/export path
  that restores mnemonic-backed role derivation and latest sealed vault
  snapshots, supports legacy full-root and sealed-local profiles, and
  fail-closes when only raw signing-key material is present.

### Pseudonymous and Routing Metadata Privacy Guard

Based on:

- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/008-agora/008-agora.md`

Related schemas:

- `artifact-delivery-envelope.v1`
- `agora-record.v1`
- `pseudonym-vault.v1`

Responsibilities:

- reject public or federated pseudonymous/routing envelopes that expose a
  participant recovery recipient;
- apply the same invariant to Artifact Delivery and Agora admission/signing
  paths;
- keep `participant:did:key:...` recovery recipients legal only in explicitly
  non-pseudonymous participant-scoped contexts;
- preserve diagnostic trace without logging vault plaintext or secret material.

Status:

- `done` — Node rejects participant recovery-recipient leakage for
  pseudonymous/routing Artifact Delivery and Agora paths and carries a negative
  vault leak fixture.

## May Implement

### Participant DH Local-Only Role

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- none yet

Responsibilities:

- derive `participant/dh` from the implicit participant root when controlled
  direct/sealed protocols need it;
- keep `participant/dh` out of Seed Directory records, node advertisements,
  capability advertisements, vault outer metadata, and recovery bundle
  metadata;
- expose only role-purpose catalog metadata that says the role exists and is
  local-only.

Status:

- `done` — Node exposes `participant/dh` only as a local role-purpose catalog
  row and derives the key on demand from mnemonic/recovery-root material.

### Recovery-Wrap Profile

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- none yet

Responsibilities:

- define `participant/recovery-wrap` separately from `participant/vault-wrap`;
- use it for local sealed recovery-bundle payloads;
- require mnemonic/recovery-root material separately when importing a
  sealed-local bundle;
- keep escrow, social recovery, and hardware custody out of this profile until
  separate procedures are designed.

Status:

- `done` — MVP implements `participant/recovery-wrap` as a local internal-wrap
  role for sealed recovery bundles, not as social recovery or escrow.

### Stronger Vault-Wrap Profiles

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- add an optional second local factor or hardware-backed wrapping mode;
- preserve root-only `participant/vault-wrap` as the MVP compatibility profile;
- make profile selection explicit in the vault metadata and import policy.

Status:

- `partial` — Node implements the opt-in `root+local-passphrase` profile in
  `pseudonym-vault.v1` metadata and runtime import/export; hardware-backed
  wrapping remains deferred.

### Multi-Device Vault Merge

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- replace single-writer latest snapshots with a conflict-resolving or
  operation-based model only after the merge semantics are designed;
- preserve rollback detection and AEAD integrity under any future merge model;
- avoid leaking plaintext item identifiers to the sync backend.

Status:

- `deferred`

## Out of Scope

- changing the stable `orbiplex-participant-seed-v1` participant signing path;
- deriving every nym or routing subject deterministically from the participant
  root;
- publishing `nym -> participant` or `routing-subject -> participant` linkage;
- treating advisory `route:...` identifiers as cryptographic subjects;
- publishing a standing participant DH discovery artifact;
- defining social recovery, threshold custody, or HSM-only operation;
- storing vault plaintext in network-visible artifacts.

## Consumes

- `orbiplex-participant-seed-v1` mnemonic/recovery material
- `participant-key-envelope.v1`
- `pseudonym-vault.v1` import snapshots
- local nym and routing-subject creation requests
- Artifact Delivery and Agora envelopes at privacy-guard boundaries

## Produces

- stable `participant:did:key:...` signing identities
- local `participant/dh` role material
- local `participant/vault-wrap` AEAD wrapping material
- local `participant/recovery-wrap` AEAD wrapping material
- local `nym:did:key:...` signing and DH material
- local `routing:did:key:...` signing and DH material
- sealed `pseudonym-vault.v1` snapshots
- role-aware participant recovery bundles
- privacy rejection facts for participant recovery-recipient leakage

## Related Capability Data

- `026-pseudonym-vault-and-key-roles-caps.edn`

## Notes

This component is intentionally local-first. The public contracts expose
pseudonymous authorship and routing subjects; the private vault preserves the
secret continuity needed to operate those surfaces without making participant
linkage part of the wire protocol.
