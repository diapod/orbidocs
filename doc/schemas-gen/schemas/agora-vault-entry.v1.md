# Agora Vault Entry v1

Source schema: [`doc/schemas/agora-vault-entry.v1.schema.json`](../../schemas/agora-vault-entry.v1.schema.json)

Generic encrypted Agora Vault artifact entry. The outer shape exposes only opaque artifact identifiers and cryptographic envelope metadata; plaintext artifact payload and domain metadata stay inside ciphertext.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/060-messaging-middleware.md`](../../project/40-proposals/060-messaging-middleware.md)
- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md)

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
| [`schema`](#field-schema) | `yes` | const: `agora-vault-entry.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`vault-entry/id`](#field-vault-entry-id) | `yes` | string |  |
| [`artifact/id`](#field-artifact-id) | `yes` | string |  |
| [`artifact/kind`](#field-artifact-kind) | `yes` | string |  |
| [`encryption`](#field-encryption) | `yes` | object |  |
| [`ciphertext`](#field-ciphertext) | `yes` | ref: `#/$defs/base64url` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`base64url`](#def-base64url) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-vault-entry.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-vault-entry-id"></a>
## `vault-entry/id`

- Required: `yes`
- Shape: string

<a id="field-artifact-id"></a>
## `artifact/id`

- Required: `yes`
- Shape: string

<a id="field-artifact-kind"></a>
## `artifact/kind`

- Required: `yes`
- Shape: string

<a id="field-encryption"></a>
## `encryption`

- Required: `yes`
- Shape: object

<a id="field-ciphertext"></a>
## `ciphertext`

- Required: `yes`
- Shape: ref: `#/$defs/base64url`

## Definition Semantics

<a id="def-base64url"></a>
## `$defs.base64url`

- Shape: string
