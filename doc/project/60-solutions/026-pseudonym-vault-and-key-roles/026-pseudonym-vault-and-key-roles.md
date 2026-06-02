# Pseudonym Vault and Key Roles

`Pseudonym Vault and Key Roles` is the solution-level identity component that
turns Proposal 059 into runtime responsibilities for participant role derivation,
private nym continuity, cryptographic routing-subject continuity, and
role-aware recovery.

Status: `hard-mvp-done`

Date: `2026-05-17`

## Executive Summary

This component owns one narrow identity-storage boundary:

```text
participant mnemonic / recovery root
  -> stable participant signing identity
  -> participant role derivation
  -> participant/recovery-wrap
  -> recovery/import-only vault unwrap

operational-secret-root
  -> participant-signing-key-wrap
  -> proxy-key-wrap
  -> participant/vault-wrap operational profile
  -> ciphertext-only pseudonym-vault.v1 snapshots
  -> private nym and routing-subject seed recovery

sealer-master
  -> separate Argon2id envelope tier, optionally step-up protected
```

The MVP profile is intentionally conservative:

- keep `orbiplex-participant-seed-v1` stable;
- keep the participant root implicit behind recovery, genesis, and import flows
  rather than the normal pseudonym hot path;
- derive `participant/dh` and `participant/recovery-wrap` without changing the
  public participant id, while `participant/vault-wrap` names the operational
  vault-key scope rather than a mnemonic-root hot-path key;
- keep `participant/dh` local-only and never publish it as a standing discovery
  artifact;
- store nym and `routing:did:key:...` seeds inside a private encrypted vault;
- use `operational-vault-key` as the default local write profile so creating
  nyms or routing subjects does not require the mnemonic/recovery root;
- use one random `operational-secret-root` as the local domain-wrap root for
  participant signing, proxy signing, and pseudonym-vault operational wraps;
- keep `sealer-master` outside that root as a stronger tier, while coordinating
  standard and step-up passphrase rotation through the participant
  `set-passphrase` flow;
- reject seed-derived vault wrap profiles (`root-only` and
  `root+local-passphrase`) in greenfield local storage; recovery uses sealed
  bundles instead of mnemonic-only pseudonym derivation;
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
  identity; in the hard-MVP implementation, local writes are wrapped by an
  operational vault secret rather than by repeatedly deriving from the recovery
  root;
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
- fail closed when only raw signing-key material is available and a recovery,
  import, genesis, or legacy-migration operation requires mnemonic or
  recovery-root material.

Status:

- `done` — Node derives the Proposal 059 role purposes while preserving the
  existing participant signing identity path. Pseudonym-vault and recovery
  bundle operations fail closed for raw signing-key-only participants when
  recovery-root material is actually required.

### Ciphertext-Only Pseudonym Vault

> **Cross-reference to Solution 032:** Solution 032 (Local Relationship
> Layer) extends `pseudonym-vault.v1` additively with `local-relationship`
> as an accepted plaintext inner-entry kind. The outer artifact remains
> ciphertext-only per this section. The forward-compat contract for
> unknown inner-entry kinds is: readers MAY ignore unknown kinds;
> importers/resealers MUST preserve unknown entries verbatim;
> `critical = true` entries fail closed on unknown kind; integrity
> violations always fail closed regardless of `critical` flag.
>
> This makes the vault the canonical home for sealed relationship state
> (classes, membership facts, pairwise nym bindings, predicate decisions
> audit). Recovery bundle (this solution §Role-Aware Participant Recovery
> Bundle) automatically includes relationship state with no further
> change to recovery semantics.

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`

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
- reject rollback imports and concurrent higher-version conflicts;
- accept `local-relationship` inner-entry kind additively; preserve unknown
  inner-entry kinds verbatim on reseal (Solution 032 forward-compat rule).

Status:

- `done` — Node mirrors the schema, gates import/export, stores sealed
  snapshots under the identity storage boundary, seals new local writes with
  `operational-vault-key`, rejects legacy seed-derived wrap profiles, and
  enforces single-writer latest semantics with rollback and conflict rejection.
- `done for Solution 032 M1` — additive `local-relationship` inner-entry
  kind and forward-compat unknown-kind preservation rule are schema-gated and
  implemented in the Node pseudonym-vault crate. Daemon-owned relationship
  event-log storage remains Solution 032 M3 work.

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
- write sealed accountability metadata for each private nym/routing subject:
  `custodian/ref` points to the local `node:id`, and `disclosure/class`
  defaults to `unsealing-only` unless a higher layer intentionally marks a
  routine-disclosable nym;
- keep advisory `route:...` identifiers out of the vault recovery model unless
  a future proposal explicitly elevates them to cryptographic subjects;
- reseal the vault after local pseudonym mutation.

Status:

- `done` — Node exposes local nym and `routing-subject` creation through the
  host identity control plane and persists the resulting private seeds only
  inside sealed vault snapshots. New writes use `operational-vault-key` by
  default, so the user wizard and messaging setup can create routing subjects
  without requiring the mnemonic after participant identity exists. Minting a
  second local nym/routing subject is gated on `recovery-bundle/current` so the
  latest vault-random snapshot is covered before further pseudonym expansion.

### Operational Unlock Root and Sealer Tiering

Based on:

- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/037-generic-signing-service.md`
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`

Related schemas:

- `participant-key-envelope.v1`
- `pseudonym-vault.v1`

Responsibilities:

- maintain a random local `operational-secret-root` that is not the participant
  mnemonic or BIP39 root material;
- protect the root with a passphrase slot and a recovery slot so passphrase
  rotation re-wraps the root rather than every domain secret;
- derive named domain wrap keys from the root for participant signing,
  proxy/signer keys and pseudonym-vault operational wrapping;
- keep the sealer master key as a deliberately separate Argon2id envelope tier,
  optionally protected by an additional step-up secret;
- enforce the normative invariant: `sealer-master` MUST be randomly generated
  and MUST NOT be derived from participant mnemonic. It MAY be recoverable
  through a sealed recovery envelope bound to `participant/recovery-wrap`,
  optionally requiring `recovery_aux` or step-up policy;
- coordinate participant/root/sealer passphrase rotation atomically, requiring
  `sealer_current_passphrase` and `sealer_step_up_secret` when the active sealer
  envelope is step-up protected.

Status:

- `done` — Node uses `operational-secret-root.v1`
  for participant signing, proxy/signer and pseudonym-vault operational wraps;
  `session.unlock` populates the corresponding caches from one passphrase;
  `set-passphrase` re-wraps the operational root and also re-wraps an active
  sealer master envelope in the same file transaction. Step-up sealer envelopes
  keep their additional factor during passphrase rotation when the operator
  supplies `sealer_current_passphrase` and `sealer_step_up_secret`. Recovery
  bundle export includes the random sealer master as a
  `sealer-master-recovery.local.v1` record inside the sealed participant
  recovery payload; import re-wraps it under the target host's local passphrase
  and optional `sealer_step_up_secret`.

### Role-Aware Participant Recovery Bundle

Based on:

- `doc/project/40-proposals/030-identity-recovery-service.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- export enough recovery material to restore participant role derivation and
  latest vault snapshots where policy allows export;
- support a sealed-local profile whose payload is wrapped by
  `participant/recovery-wrap` and whose import requires the mnemonic/recovery
  root supplied separately;
- include latest pseudonym-vault snapshots as recovery-export ciphertext blobs:
  export opens the source operational-vault snapshot through its recovery slot,
  re-seals the snapshot under a mnemonic-root-derived recovery-export secret,
  and import re-seals it again under the target host's operational-secret-root;
- include the active random `sealer-master` in the same sealed payload when it
  exists and is unlocked, so sealer recovery follows the same export freshness
  contract as vault-random nyms without deriving the master from mnemonic;
- restore the role tree and sealed vault snapshots without exposing participant
  linkage in public artifacts;
- support the seed+aux hardening profile as an optional recovery unwrap factor.

Status:

- `done` — Node has a role-aware participant recovery bundle import/export path
  that restores mnemonic-backed role derivation and latest sealed vault
  snapshots, supports sealed-local and sealed-local-seed-aux profiles, uses a
  recovery-export snapshot secret rather than carrying the source
  operational-secret-root, includes sealer-master recovery material as a
  sealed-payload-local record when an active master exists and is unlocked,
  requires a target local passphrase before importing vault snapshots or sealer
  recovery material on a fresh host, and fail-closes before mutating local
  identity when that target passphrase is missing.

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
  row. It remains non-discoverable and outside vault outer metadata; operations
  that require role-root material still fail closed when only raw signing-key
  recovery is available.

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

- keep `operational-vault-key` as the default local write profile;
- reject `root-only` and `root+local-passphrase` local write/import requests as
  obsolete seed-derived wrap profiles;
- add future hardware-backed wrapping modes without changing the
  `pseudonym-vault.v1` outer contract;
- make profile selection explicit in the vault metadata and import policy.

Status:

- `done for hard-MVP` — Node implements `operational-vault-key` for default
  local writes and rejects seed-derived wrap profiles. The hard-MVP daemon
  stores the headless/file operational secret as a sealed local node-AEAD
  record; hardware-backed
  wrapping and platform keychain-backed operational secret providers remain
  deferred hardening.

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
- sealed local operational vault secret
- `participant-key-envelope.v1`
- `pseudonym-vault.v1` import snapshots
- local nym and routing-subject creation requests
- Artifact Delivery and Agora envelopes at privacy-guard boundaries

## Produces

- stable `participant:did:key:...` signing identities
- local `participant/dh` role material
- local `participant/vault-wrap` AEAD wrapping material backed by the
  operational vault secret for normal writes
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
