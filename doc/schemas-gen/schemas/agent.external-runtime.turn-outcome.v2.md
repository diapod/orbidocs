# External Agent Runtime Turn Outcome V2

Source schema: [`doc/schemas/agent.external-runtime.turn-outcome.v2.schema.json`](../../schemas/agent.external-runtime.turn-outcome.v2.schema.json)

Compatible successor binding every V1 terminal external-runtime outcome to provider-neutral realized inference execution provenance.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.external-runtime.turn-outcome.v2` |  |
| [`outcome`](#field-outcome) | `yes` | ref: `agent.external-runtime.turn-outcome.v1.schema.json` |  |
| [`execution/provenance`](#field-execution-provenance) | `yes` | ref: `inference-execution-provenance.v1.schema.json` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.external-runtime.turn-outcome.v2`

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: ref: `agent.external-runtime.turn-outcome.v1.schema.json`

<a id="field-execution-provenance"></a>
## `execution/provenance`

- Required: `yes`
- Shape: ref: `inference-execution-provenance.v1.schema.json`
