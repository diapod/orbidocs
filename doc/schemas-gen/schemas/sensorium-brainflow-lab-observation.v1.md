# Sensorium Brain Flow Lab Observation v1

Source schema: [`doc/schemas/sensorium-brainflow-lab-observation.v1.schema.json`](../../schemas/sensorium-brainflow-lab-observation.v1.schema.json)

Bounded metadata-only self-wearer laboratory evidence, never product qualification or acquisition authority. Firmware and TCC attribution are sourced operator observations, not inferred from parent PIDs. Every launch context is explicit, including SSH. Monotonic observation and first-data times measure the local native drain. Counter discontinuities ignore repeated 16-bit packets and count wraps separately; they are diagnostic and do not prove exact sample loss. Nonconstant row flags compare finite samples across the full observation, revealing activity but no values. Raw values, selectors, paths and native labels are excluded.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-lab-observation.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`evidence/class`](#field-evidence-class) | `yes` | const: `lab-observation` |  |
| [`acquisition/mode`](#field-acquisition-mode) | `yes` | enum: `p21`, `p51` |  |
| [`identity/assurance`](#field-identity-assurance) | `yes` | const: `operator-confirmed-selector` |  |
| [`consent`](#field-consent) | `yes` | object |  |
| [`permissions`](#field-permissions) | `yes` | object |  |
| [`firmware`](#field-firmware) | `yes` | unspecified |  |
| [`scope/exclusions`](#field-scope-exclusions) | `yes` | const: `['product-acquisition', 'qualification', 'radio-concurrency', 'contact-quality']` |  |
| [`observation`](#field-observation) | `yes` | object |  |
| [`runtime`](#field-runtime) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`descriptor`](#def-descriptor) | object |  |
| [`stream`](#def-stream) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "acquisition/mode": {
      "const": "p21"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "consent": {
      "properties": {
        "signals/acquired": {
          "const": [
            "eeg",
            "accelerometer",
            "gyroscope"
          ]
        }
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "acquisition/mode": {
      "const": "p51"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "consent": {
      "properties": {
        "signals/acquired": {
          "const": [
            "eeg",
            "accelerometer",
            "gyroscope",
            "ppg"
          ]
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
- Shape: const: `sensorium-brainflow-lab-observation.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-evidence-class"></a>
## `evidence/class`

- Required: `yes`
- Shape: const: `lab-observation`

<a id="field-acquisition-mode"></a>
## `acquisition/mode`

- Required: `yes`
- Shape: enum: `p21`, `p51`

<a id="field-identity-assurance"></a>
## `identity/assurance`

- Required: `yes`
- Shape: const: `operator-confirmed-selector`

<a id="field-consent"></a>
## `consent`

- Required: `yes`
- Shape: object

<a id="field-permissions"></a>
## `permissions`

- Required: `yes`
- Shape: object

<a id="field-firmware"></a>
## `firmware`

- Required: `yes`
- Shape: unspecified

<a id="field-scope-exclusions"></a>
## `scope/exclusions`

- Required: `yes`
- Shape: const: `['product-acquisition', 'qualification', 'radio-concurrency', 'contact-quality']`

<a id="field-observation"></a>
## `observation`

- Required: `yes`
- Shape: object

<a id="field-runtime"></a>
## `runtime`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-descriptor"></a>
## `$defs.descriptor`

- Shape: object

<a id="def-stream"></a>
## `$defs.stream`

- Shape: object
