# Host Effect Apply With Source Set CAS

Source schema: [`doc/schemas/responsibility-effect-apply.v1.schema.json`](../../schemas/responsibility-effect-apply.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `responsibility-effect-apply.v1` |  |
| [`intent`](#field-intent) | `yes` | ref: `responsibility-common.v1.schema.json#/$defs/EffectIntent` |  |
| [`expected_source_set`](#field-expected-source-set) | `yes` | ref: `responsibility-common.v1.schema.json#/$defs/Binding` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-effect-apply.v1`

<a id="field-intent"></a>
## `intent`

- Required: `yes`
- Shape: ref: `responsibility-common.v1.schema.json#/$defs/EffectIntent`

<a id="field-expected-source-set"></a>
## `expected_source_set`

- Required: `yes`
- Shape: ref: `responsibility-common.v1.schema.json#/$defs/Binding`
