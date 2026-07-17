# Sensorium Interface LED Set v1

Source schema: [`doc/schemas/sensorium-interface-led-set.v1.schema.json`](../../schemas/sensorium-interface-led-set.v1.schema.json)

Convergent target-state payload used by the bounded P083 shared LED fixture.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-led-set.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`on`](#field-on) | `yes` | boolean |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-led-set.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-on"></a>
## `on`

- Required: `yes`
- Shape: boolean
