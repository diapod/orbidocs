# Assessment-agent-run-result.v2

Source schema: [`doc/schemas/assessment-agent-run-result.v2.schema.json`](../../schemas/assessment-agent-run-result.v2.schema.json)

P026-012b-r1 successor. Historical versions are unchanged; private commitments have explicit HMAC labels.

## Governing Basis

- [`doc/project/40-proposals/026-assessment-agent-consumer-r1.md`](../../project/40-proposals/026-assessment-agent-consumer-r1.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `assessment-agent-run-result.v2` |  |
| [`status`](#field-status) | `yes` | const: `completed` |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`outcome`](#field-outcome) | `yes` | ref: `agent.outcome.v4.schema.json` |  |
| [`manifest`](#field-manifest) | `yes` | ref: `agent.supplied-input-manifest.v3.schema.json` |  |
| [`step`](#field-step) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "replayed": {
      "const": false
    }
  }
}
```

Then:

```json
{
  "required": [
    "step"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `assessment-agent-run-result.v2`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `completed`

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: ref: `agent.outcome.v4.schema.json`

<a id="field-manifest"></a>
## `manifest`

- Required: `yes`
- Shape: ref: `agent.supplied-input-manifest.v3.schema.json`

<a id="field-step"></a>
## `step`

- Required: `no`
- Shape: object
