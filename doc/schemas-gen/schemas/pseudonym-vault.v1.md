# Pseudonym Vault v1

Source schema: [`doc/schemas/pseudonym-vault.v1.schema.json`](../../schemas/pseudonym-vault.v1.schema.json)

Opaque encrypted local vault snapshot for nym and routing-subject private material. The outer artifact carries only technical sync and crypto metadata; plaintext pseudonym identifiers and participant linkage belong inside the ciphertext.

## Governing Basis

- [`doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`](../../project/40-proposals/059-participant-and-nym-key-role-derivation.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `pseudonym-vault.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`vault/id`](#field-vault-id) | `yes` | string | Opaque vault snapshot identifier. It must not encode participant, nym, or routing-subject ids. |
| [`vault/version`](#field-vault-version) | `yes` | integer | Monotonic local version of this sealed vault snapshot. |
| [`vault/profile`](#field-vault-profile) | `yes` | enum: `participant-private-pseudonyms` | Declares the plaintext family without exposing plaintext subjects. |
| [`contents/kinds`](#field-contents-kinds) | `yes` | array | Coarse encrypted content class. Known kinds include `nym`, `routing-subject`, `local-contact-recovery`, and `local-relationship`. Readers MAY ignore unknown kinds, but importers and resealers MUST preserve unknown plaintext entries verbatim unless an unknown entry is marked critical. |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`sealed-at`](#field-sealed-at) | `yes` | string |  |
| [`supersedes`](#field-supersedes) | `no` | string | Optional previous vault snapshot id for rollback detection and sync lineage. |
| [`crypto/kdf`](#field-crypto-kdf) | `yes` | enum: `hkdf-sha256` | KDF used to derive the vault wrapping key from participant root material and the stored salt. |
| [`crypto/aead`](#field-crypto-aead) | `yes` | enum: `xchacha20-poly1305`, `aes-256-gcm` |  |
| [`crypto/wrap-purpose`](#field-crypto-wrap-purpose) | `yes` | const: `participant/vault-wrap` | Private role purpose used to derive the wrapping key. This is a role label, not a public participant identifier. |
| [`crypto/wrap-profile`](#field-crypto-wrap-profile) | `no` | enum: `root-only`, `root+local-passphrase`, `operational-vault-key` | Local wrap-strength profile. `root-only` preserves the Proposal 059 recovery compatibility profile; `root+local-passphrase` additionally requires a local passphrase at open/import time; `operational-vault-key` is the non-mnemonic hot-path profile. |
| [`crypto/passphrase-kdf`](#field-crypto-passphrase-kdf) | `no` | object | Metadata for the optional local passphrase factor. The passphrase itself is never serialized. |
| [`crypto/aad-profile`](#field-crypto-aad-profile) | `no` | enum: `pseudonym-vault.outer-metadata.v1` |  |
| [`salt`](#field-salt) | `yes` | ref: `#/$defs/base64url` |  |
| [`nonce`](#field-nonce) | `yes` | ref: `#/$defs/base64url` |  |
| [`ciphertext`](#field-ciphertext) | `yes` | ref: `#/$defs/base64url` |  |
| [`ciphertext/digest`](#field-ciphertext-digest) | `no` | string | Optional digest of the ciphertext for object-store deduplication and sync verification. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`base64url`](#def-base64url) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "crypto/wrap-profile": {
      "const": "root+local-passphrase"
    }
  },
  "required": [
    "crypto/wrap-profile"
  ]
}
```

Then:

```json
{
  "required": [
    "crypto/passphrase-kdf"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "crypto/wrap-profile": {
      "const": "root-only"
    }
  },
  "required": [
    "crypto/wrap-profile"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "crypto/passphrase-kdf"
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "crypto/wrap-profile": {
      "const": "operational-vault-key"
    }
  },
  "required": [
    "crypto/wrap-profile"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "crypto/passphrase-kdf"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `pseudonym-vault.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-vault-id"></a>
## `vault/id`

- Required: `yes`
- Shape: string

Opaque vault snapshot identifier. It must not encode participant, nym, or routing-subject ids.

<a id="field-vault-version"></a>
## `vault/version`

- Required: `yes`
- Shape: integer

Monotonic local version of this sealed vault snapshot.

<a id="field-vault-profile"></a>
## `vault/profile`

- Required: `yes`
- Shape: enum: `participant-private-pseudonyms`

Declares the plaintext family without exposing plaintext subjects.

<a id="field-contents-kinds"></a>
## `contents/kinds`

- Required: `yes`
- Shape: array

Coarse encrypted content class. Known kinds include `nym`, `routing-subject`, `local-contact-recovery`, and `local-relationship`. Readers MAY ignore unknown kinds, but importers and resealers MUST preserve unknown plaintext entries verbatim unless an unknown entry is marked critical.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-sealed-at"></a>
## `sealed-at`

- Required: `yes`
- Shape: string

<a id="field-supersedes"></a>
## `supersedes`

- Required: `no`
- Shape: string

Optional previous vault snapshot id for rollback detection and sync lineage.

<a id="field-crypto-kdf"></a>
## `crypto/kdf`

- Required: `yes`
- Shape: enum: `hkdf-sha256`

KDF used to derive the vault wrapping key from participant root material and the stored salt.

<a id="field-crypto-aead"></a>
## `crypto/aead`

- Required: `yes`
- Shape: enum: `xchacha20-poly1305`, `aes-256-gcm`

<a id="field-crypto-wrap-purpose"></a>
## `crypto/wrap-purpose`

- Required: `yes`
- Shape: const: `participant/vault-wrap`

Private role purpose used to derive the wrapping key. This is a role label, not a public participant identifier.

<a id="field-crypto-wrap-profile"></a>
## `crypto/wrap-profile`

- Required: `no`
- Shape: enum: `root-only`, `root+local-passphrase`, `operational-vault-key`

Local wrap-strength profile. `root-only` preserves the Proposal 059 recovery compatibility profile; `root+local-passphrase` additionally requires a local passphrase at open/import time; `operational-vault-key` is the non-mnemonic hot-path profile.

<a id="field-crypto-passphrase-kdf"></a>
## `crypto/passphrase-kdf`

- Required: `no`
- Shape: object

Metadata for the optional local passphrase factor. The passphrase itself is never serialized.

<a id="field-crypto-aad-profile"></a>
## `crypto/aad-profile`

- Required: `no`
- Shape: enum: `pseudonym-vault.outer-metadata.v1`

<a id="field-salt"></a>
## `salt`

- Required: `yes`
- Shape: ref: `#/$defs/base64url`

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: ref: `#/$defs/base64url`

<a id="field-ciphertext"></a>
## `ciphertext`

- Required: `yes`
- Shape: ref: `#/$defs/base64url`

<a id="field-ciphertext-digest"></a>
## `ciphertext/digest`

- Required: `no`
- Shape: string

Optional digest of the ciphertext for object-store deduplication and sync verification.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-base64url"></a>
## `$defs.base64url`

- Shape: string
