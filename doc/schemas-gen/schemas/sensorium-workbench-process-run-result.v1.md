# Sensorium Workbench Process Run Result v1

Source schema: [`doc/schemas/sensorium-workbench-process-run-result.v1.schema.json`](../../schemas/sensorium-workbench-process-run-result.v1.schema.json)

Outcome of one structured command run in a microVM workspace under the command profile it was pinned to (P094-021b). `completed` carries the exit code and bounded output, and for a declared observation the guest's enforcement evidence; `refused` proves that nothing ran, except for a detected observation effect or a proven quiesced observation timeout; `unknown` proves nothing. The result is kept under its idempotency key, so a replay within the retention window does not run it twice.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

### Requirements

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-workbench-process-run-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`result/ref`](#field-result-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`address`](#field-address) | `yes` | ref: `#/$defs/address` |  |
| [`command.profile/ref`](#field-command-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`command-profile/digest`](#field-command-profile-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`effect/mode`](#field-effect-mode) | `yes` | enum: `observation`, `mutation` |  |
| [`outcome`](#field-outcome) | `yes` | enum: `completed`, `refused`, `unknown` |  |
| [`exit/code`](#field-exit-code) | `no` | integer \| null | Null when a signal ended the process. |
| [`stdout/base64`](#field-stdout-base64) | `no` | string |  |
| [`stderr/base64`](#field-stderr-base64) | `no` | string |  |
| [`output/truncated`](#field-output-truncated) | `no` | boolean |  |
| [`effect/enforcement`](#field-effect-enforcement) | `no` | object | The guest's evidence that it enforced the observation; present exactly for a completed observation. |
| [`error/code`](#field-error-code) | `no` | ref: `#/$defs/code` |  |
| [`evidence/class`](#field-evidence-class) | `no` | enum: `guest-admission`, `guest-execution`, `none` |  |
| [`observation/timeout`](#field-observation-timeout) | `no` | object |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`relativePath`](#def-relativepath) | string |  |
| [`address`](#def-address) | object |  |
| [`code`](#def-code) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "error/code"
  ],
  "properties": {
    "error/code": {
      "const": "observation-timeout-quiesced"
    }
  }
}
```

Then:

```json
{
  "required": [
    "observation/timeout",
    "evidence/class"
  ],
  "properties": {
    "effect/mode": {
      "const": "observation"
    },
    "outcome": {
      "const": "refused"
    },
    "evidence/class": {
      "const": "guest-execution"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "outcome": {
      "const": "completed"
    }
  }
}
```

Then:

```json
{
  "required": [
    "exit/code",
    "stdout/base64",
    "stderr/base64",
    "output/truncated"
  ],
  "not": {
    "required": [
      "error/code"
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "outcome": {
      "const": "completed"
    },
    "effect/mode": {
      "const": "observation"
    }
  },
  "required": [
    "outcome",
    "effect/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "effect/enforcement"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "effect/mode": {
      "const": "mutation"
    }
  },
  "required": [
    "effect/mode"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "effect/enforcement"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-workbench-process-run-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-result-ref"></a>
## `result/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-address"></a>
## `address`

- Required: `yes`
- Shape: ref: `#/$defs/address`

<a id="field-command-profile-ref"></a>
## `command.profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-command-profile-digest"></a>
## `command-profile/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-effect-mode"></a>
## `effect/mode`

- Required: `yes`
- Shape: enum: `observation`, `mutation`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `completed`, `refused`, `unknown`

<a id="field-exit-code"></a>
## `exit/code`

- Required: `no`
- Shape: integer | null

Null when a signal ended the process.

<a id="field-stdout-base64"></a>
## `stdout/base64`

- Required: `no`
- Shape: string

<a id="field-stderr-base64"></a>
## `stderr/base64`

- Required: `no`
- Shape: string

<a id="field-output-truncated"></a>
## `output/truncated`

- Required: `no`
- Shape: boolean

<a id="field-effect-enforcement"></a>
## `effect/enforcement`

- Required: `no`
- Shape: object

The guest's evidence that it enforced the observation; present exactly for a completed observation.

<a id="field-error-code"></a>
## `error/code`

- Required: `no`
- Shape: ref: `#/$defs/code`

<a id="field-evidence-class"></a>
## `evidence/class`

- Required: `no`
- Shape: enum: `guest-admission`, `guest-execution`, `none`

<a id="field-observation-timeout"></a>
## `observation/timeout`

- Required: `no`
- Shape: object

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string

<a id="def-address"></a>
## `$defs.address`

- Shape: object

<a id="def-code"></a>
## `$defs.code`

- Shape: string
