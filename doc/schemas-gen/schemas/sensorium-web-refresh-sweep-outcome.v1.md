# Sensorium Web Refresh Sweep Outcome v1

Source schema: [`doc/schemas/sensorium-web-refresh-sweep-outcome.v1.schema.json`](../../schemas/sensorium-web-refresh-sweep-outcome.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-refresh-sweep-outcome.v1` |  |
| [`records_seen`](#field-records-seen) | `yes` | integer |  |
| [`records_applied`](#field-records-applied) | `yes` | integer |  |
| [`records_skipped`](#field-records-skipped) | `yes` | integer |  |
| [`records_rejected`](#field-records-rejected) | `yes` | const: `0` |  |
| [`cursor`](#field-cursor) | `yes` | null |  |
| [`details`](#field-details) | `yes` | ref: `sensorium-web-refresh-sweep.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-refresh-sweep-outcome.v1`

<a id="field-records-seen"></a>
## `records_seen`

- Required: `yes`
- Shape: integer

<a id="field-records-applied"></a>
## `records_applied`

- Required: `yes`
- Shape: integer

<a id="field-records-skipped"></a>
## `records_skipped`

- Required: `yes`
- Shape: integer

<a id="field-records-rejected"></a>
## `records_rejected`

- Required: `yes`
- Shape: const: `0`

<a id="field-cursor"></a>
## `cursor`

- Required: `yes`
- Shape: null

<a id="field-details"></a>
## `details`

- Required: `yes`
- Shape: ref: `sensorium-web-refresh-sweep.v1.schema.json`
