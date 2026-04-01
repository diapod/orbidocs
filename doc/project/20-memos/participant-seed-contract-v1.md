# Participant Seed Contract v1

Based on:

- `doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/20-memos/console-participant-identity-create-and-import.md`

This memo freezes the local recovery-seed contract used for explicit participant
identity creation and import in Orbiplex Node MVP.

## Contract

- Contract name: `orbiplex-participant-seed-v1`
- Wordlist: BIP39 English
- Word count: 12 words for MVP, with 24 words accepted by the derivation path
- Seed KDF: BIP39 standard `PBKDF2-SHA512`, `2048` iterations, empty passphrase
- Derivation: `SLIP-0010 Ed25519`
- Path: `m/44'/2268'/0'`
- Key algorithm: Ed25519
- Accountable id encoding:
  - public key -> multicodec `0xed01`
  - multibase `base58btc`
  - final form `participant:did:key:z...`

## Scope

This contract applies only to **participant** recovery material.

It does **not** change:

- `node-identity.v1`
- the automatic creation of one local `node-id`
- org identity generation in MVP

`node-identity.v1` remains infrastructure identity for the node as a network
actor. Participant identity remains an explicit operator action.

## Create flow

`Create Participant` means:

1. generate a fresh BIP39 English mnemonic,
2. derive a deterministic Ed25519 participant signing key via
   `orbiplex-participant-seed-v1`,
3. derive canonical `participant:did:key:...`,
4. persist the signing key locally,
5. optionally persist the recovery phrase in local secret storage,
6. show the mnemonic phrase to the operator exactly once.

The mnemonic phrase is never appended to the fact stream.

## Import flow

`Import Participant` means:

1. accept a mnemonic phrase from the operator,
2. derive the participant signing key through the same contract,
3. derive canonical `participant:did:key:...`,
4. persist the local signing key binding,
5. optionally persist the recovery phrase in local secret storage.

Because create and import share the same contract, one mnemonic phrase always
maps to one stable `participant-id`.

## Local secret storage

If the operator explicitly asks the node to keep the recovery phrase, it is
stored in local secret storage outside the append-only fact streams.

The local record is:

- mutable,
- deleteable,
- operator-local,
- and never replayed as a public fact.

The presence of stored recovery material may be surfaced through an operator
read model such as `recovery_seed_stored = true`.

## Export

Existing participants may be exported only through an explicit recovery export
operation.

Preferred export:

- stored mnemonic phrase, if available

Fallback export:

- private key material, if mnemonic was not stored locally

This operation is intentionally named as recovery export rather than generic
identity export, because it yields high-sensitivity recovery material.
