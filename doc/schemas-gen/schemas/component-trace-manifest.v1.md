# Component Trace Manifest V1

Source schema: [`doc/schemas/component-trace-manifest.v1.schema.json`](../../schemas/component-trace-manifest.v1.schema.json)

Rebuildable bounded inventory and completeness projection for an offline trace session.

## Governing Basis

- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `component-trace-manifest.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`recording/ref`](#field-recording-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`capture/session-ref`](#field-capture-session-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`node/ref`](#field-node-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`observation/generation`](#field-observation-generation) | `yes` | ref: `#/$defs/ref` |  |
| [`start/cursor`](#field-start-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`durable/cursor`](#field-durable-cursor) | `yes` | ref: `#/$defs/cursor` |  |
| [`final/cursor`](#field-final-cursor) | `no` | ref: `#/$defs/cursor` |  |
| [`started/at`](#field-started-at) | `yes` | ref: `#/$defs/timestamp` |  |
| [`ended/at`](#field-ended-at) | `no` | ref: `#/$defs/timestamp` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`policy/digest`](#field-policy-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`redaction/digests`](#field-redaction-digests) | `yes` | array |  |
| [`segments`](#field-segments) | `yes` | ref: `#/$defs/inventory` |  |
| [`schemas`](#field-schemas) | `yes` | ref: `#/$defs/inventory` |  |
| [`contexts`](#field-contexts) | `yes` | ref: `#/$defs/inventory` |  |
| [`artifacts`](#field-artifacts) | `yes` | ref: `#/$defs/inventory` |  |
| [`boundary/coverage`](#field-boundary-coverage) | `yes` | array |  |
| [`boundary/exclusions`](#field-boundary-exclusions) | `yes` | array |  |
| [`counters`](#field-counters) | `yes` | ref: `#/$defs/counters` |  |
| [`completeness`](#field-completeness) | `yes` | enum: `complete`, `incomplete`, `aborted` |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
| [`recorder/version`](#field-recorder-version) | `yes` | ref: `#/$defs/ref` |  |
| [`format/profile`](#field-format-profile) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`timestamp`](#def-timestamp) | string |  |
| [`cursor`](#def-cursor) | integer |  |
| [`inventory-item`](#def-inventory-item) | object |  |
| [`inventory`](#def-inventory) | array |  |
| [`counters`](#def-counters) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "completeness": {
      "const": "complete"
    }
  },
  "required": [
    "completeness"
  ]
}
```

Then:

```json
{
  "required": [
    "final/cursor",
    "ended/at"
  ],
  "properties": {
    "counters": {
      "properties": {
        "drops": {
          "const": 0
        },
        "gaps": {
          "const": 0
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
- Shape: const: `component-trace-manifest.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-recording-ref"></a>
## `recording/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-capture-session-ref"></a>
## `capture/session-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-observation-generation"></a>
## `observation/generation`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-start-cursor"></a>
## `start/cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-durable-cursor"></a>
## `durable/cursor`

- Required: `yes`
- Shape: ref: `#/$defs/cursor`

<a id="field-final-cursor"></a>
## `final/cursor`

- Required: `no`
- Shape: ref: `#/$defs/cursor`

<a id="field-started-at"></a>
## `started/at`

- Required: `yes`
- Shape: ref: `#/$defs/timestamp`

<a id="field-ended-at"></a>
## `ended/at`

- Required: `no`
- Shape: ref: `#/$defs/timestamp`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-redaction-digests"></a>
## `redaction/digests`

- Required: `yes`
- Shape: array

<a id="field-segments"></a>
## `segments`

- Required: `yes`
- Shape: ref: `#/$defs/inventory`

<a id="field-schemas"></a>
## `schemas`

- Required: `yes`
- Shape: ref: `#/$defs/inventory`

<a id="field-contexts"></a>
## `contexts`

- Required: `yes`
- Shape: ref: `#/$defs/inventory`

<a id="field-artifacts"></a>
## `artifacts`

- Required: `yes`
- Shape: ref: `#/$defs/inventory`

<a id="field-boundary-coverage"></a>
## `boundary/coverage`

- Required: `yes`
- Shape: array

<a id="field-boundary-exclusions"></a>
## `boundary/exclusions`

- Required: `yes`
- Shape: array

<a id="field-counters"></a>
## `counters`

- Required: `yes`
- Shape: ref: `#/$defs/counters`

<a id="field-completeness"></a>
## `completeness`

- Required: `yes`
- Shape: enum: `complete`, `incomplete`, `aborted`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

<a id="field-recorder-version"></a>
## `recorder/version`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-format-profile"></a>
## `format/profile`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-timestamp"></a>
## `$defs.timestamp`

- Shape: string

<a id="def-cursor"></a>
## `$defs.cursor`

- Shape: integer

<a id="def-inventory-item"></a>
## `$defs.inventory-item`

- Shape: object

<a id="def-inventory"></a>
## `$defs.inventory`

- Shape: array

<a id="def-counters"></a>
## `$defs.counters`

- Shape: object
