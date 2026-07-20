# Sensorium Operational Context v1

Source schema: [`doc/schemas/sensorium-operational-context.v1.schema.json`](../../schemas/sensorium-operational-context.v1.schema.json)

Bounded, non-authoritative operational impact metadata for an enacted Sensorium resource.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-operational-context.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`impact/class`](#field-impact-class) | `yes` | enum: `research`, `experimental`, `test`, `production`, `critical` |  |
| [`context/summary`](#field-context-summary) | `no` | string | Untrusted operator-facing context. Implementations additionally enforce a 512 UTF-8 byte cap and reject non-whitespace control characters. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-operational-context.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-impact-class"></a>
## `impact/class`

- Required: `yes`
- Shape: enum: `research`, `experimental`, `test`, `production`, `critical`

<a id="field-context-summary"></a>
## `context/summary`

- Required: `no`
- Shape: string

Untrusted operator-facing context. Implementations additionally enforce a 512 UTF-8 byte cap and reject non-whitespace control characters.
