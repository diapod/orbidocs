# Sensorium-biosignal-sample-block.v1

Source schema: [`doc/schemas/sensorium-biosignal-sample-block.v1.schema.json`](../../schemas/sensorium-biosignal-sample-block.v1.schema.json)

Closed sample-block contract. buffer is the nested sensorium-biosignal-buffer.v1 signal tensor; source-time and package-num are separate 1 by N tensors. All shapes and stream mappings require semantic validation. Host binds metadata to current admitted identity, epoch, generation, profile and classification before hashing; a worker metadata assertion grants no authority. Host digest is carried by the enclosing interface frame. Preimage: UTF-8 domain orbiplex.sensorium.sample-block.v1 followed by NUL; seven independently u64BE length-prefixed segments: JCS metadata with derived tensor descriptors, signal values, signal mask, source-time values, source-time mask, package-num values, package-num mask. Real and real-derived playback data enter as Personal, sensitive-personal/health-wearable.

## Governing Basis

- [`doc/project/40-proposals/096-sensorium-brainflow-connector.md`](../../project/40-proposals/096-sensorium-brainflow-connector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)
- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-biosignal-sample-block.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`metadata`](#field-metadata) | `yes` | object |  |
| [`buffer`](#field-buffer) | `yes` | ref: `sensorium-biosignal-buffer.v1.schema.json` |  |
| [`source-time`](#field-source-time) | `yes` | ref: `sensorium-biosignal-buffer.v1.schema.json` |  |
| [`package-num`](#field-package-num) | `yes` | ref: `sensorium-biosignal-buffer.v1.schema.json` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "metadata": {
      "properties": {
        "evidence/class": {
          "enum": [
            "real-device",
            "playback"
          ]
        }
      }
    }
  }
}
```

Then:

```json
{
  "properties": {
    "metadata": {
      "properties": {
        "classification": {
          "properties": {
            "source_tier": {
              "const": "Personal"
            },
            "effective_tier": {
              "const": "Personal"
            }
          }
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-biosignal-sample-block.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-metadata"></a>
## `metadata`

- Required: `yes`
- Shape: object

<a id="field-buffer"></a>
## `buffer`

- Required: `yes`
- Shape: ref: `sensorium-biosignal-buffer.v1.schema.json`

<a id="field-source-time"></a>
## `source-time`

- Required: `yes`
- Shape: ref: `sensorium-biosignal-buffer.v1.schema.json`

<a id="field-package-num"></a>
## `package-num`

- Required: `yes`
- Shape: ref: `sensorium-biosignal-buffer.v1.schema.json`
