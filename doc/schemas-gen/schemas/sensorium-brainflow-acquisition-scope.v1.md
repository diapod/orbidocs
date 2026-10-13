# Sensorium-brainflow-acquisition-scope.v1

Source schema: [`doc/schemas/sensorium-brainflow-acquisition-scope.v1.schema.json`](../../schemas/sensorium-brainflow-acquisition-scope.v1.schema.json)

Payload inside existing host consent/grant authority envelopes. Only acquisition is granted here; read, capture, publish and discover require separate authority. All unavoidable incidental signals must be covered. Expiry, revoke and wearer protected stop are checked at the host, with Personal classification preserved.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-acquisition-scope.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`scope/ref`](#field-scope-ref) | `yes` | object |  |
| [`instance/ref`](#field-instance-ref) | `yes` | object |  |
| [`profile/ref`](#field-profile-ref) | `yes` | object |  |
| [`mode/id`](#field-mode-id) | `yes` | enum: `p21`, `p51` |  |
| [`signals/acquired`](#field-signals-acquired) | `yes` | array |  |
| [`wearer/ref`](#field-wearer-ref) | `yes` | string |  |
| [`operator/ref`](#field-operator-ref) | `yes` | string |  |
| [`operator-is-wearer`](#field-operator-is-wearer) | `yes` | boolean |  |
| [`confirmed/at-unix-s`](#field-confirmed-at-unix-s) | `yes` | integer |  |
| [`expires/at-unix-s`](#field-expires-at-unix-s) | `yes` | integer |  |
| [`session/epoch`](#field-session-epoch) | `yes` | string |  |
| [`source/generation`](#field-source-generation) | `yes` | integer |  |
| [`authorities`](#field-authorities) | `yes` | const: `['acquire']` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "mode/id": {
      "const": "p21"
    }
  }
}
```

Then:

```json
{
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
```

### Rule 2

When:

```json
{
  "properties": {
    "mode/id": {
      "const": "p51"
    }
  }
}
```

Then:

```json
{
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
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-acquisition-scope.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-scope-ref"></a>
## `scope/ref`

- Required: `yes`
- Shape: object

<a id="field-instance-ref"></a>
## `instance/ref`

- Required: `yes`
- Shape: object

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: object

<a id="field-mode-id"></a>
## `mode/id`

- Required: `yes`
- Shape: enum: `p21`, `p51`

<a id="field-signals-acquired"></a>
## `signals/acquired`

- Required: `yes`
- Shape: array

<a id="field-wearer-ref"></a>
## `wearer/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-ref"></a>
## `operator/ref`

- Required: `yes`
- Shape: string

<a id="field-operator-is-wearer"></a>
## `operator-is-wearer`

- Required: `yes`
- Shape: boolean

<a id="field-confirmed-at-unix-s"></a>
## `confirmed/at-unix-s`

- Required: `yes`
- Shape: integer

<a id="field-expires-at-unix-s"></a>
## `expires/at-unix-s`

- Required: `yes`
- Shape: integer

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: string

<a id="field-source-generation"></a>
## `source/generation`

- Required: `yes`
- Shape: integer

<a id="field-authorities"></a>
## `authorities`

- Required: `yes`
- Shape: const: `['acquire']`
