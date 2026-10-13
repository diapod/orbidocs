# Inquirium Model Package Chat Template Proof v1

Source schema: [`doc/schemas/inquirium.model-package.chat-template-proof.v1.schema.json`](../../schemas/inquirium.model-package.chat-template-proof.v1.schema.json)

Host-produced offline rendering evidence bound to the exact package, runtime and model. Preserved sentinel text proves rendering, not trained understanding. Supplied JSON cannot grant template-verified status. Twenty ordered probes cover first, after-user, repeated, Corpus preamble and postamble layouts. Global roles require preservation of every message in order in all five layouts; this is not arbitrary-sequence or training evidence.

## Governing Basis

- [`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`](../../project/40-proposals/064-inquirium-implementation-recommendations.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.model-package.chat-template-proof.v1` |  |
| [`manifest/digest`](#field-manifest-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`runtime/digest`](#field-runtime-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`model/digest`](#field-model-digest) | `yes` | ref: `#/$defs/digest` | Digest of the manifest's primary model asset, which may be config.json rather than weights. manifest/digest commits every asset and the runtime arguments. |
| [`chat-template/digest`](#field-chat-template-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`roles/probes`](#field-roles-probes) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`probe`](#def-probe) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.model-package.chat-template-proof.v1`

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-runtime-digest"></a>
## `runtime/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-model-digest"></a>
## `model/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

Digest of the manifest's primary model asset, which may be config.json rather than weights. manifest/digest commits every asset and the runtime arguments.

<a id="field-chat-template-digest"></a>
## `chat-template/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-roles-probes"></a>
## `roles/probes`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-probe"></a>
## `$defs.probe`

- Shape: object
