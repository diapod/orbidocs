# Federation Scenario v1

Source schema: [`doc/schemas/federation-scenario.v1.schema.json`](../../schemas/federation-scenario.v1.schema.json)

Story-owned declarative duties, services, and dependency-ordered steps over reusable acceptance slots.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `federation-scenario.v1` |  |
| [`scenario/ref`](#field-scenario-ref) | `yes` | string |  |
| [`owner/slot`](#field-owner-slot) | `yes` | ref: `#/$defs/token64` |  |
| [`port/base`](#field-port-base) | `yes` | integer |  |
| [`evidence/claim-ref`](#field-evidence-claim-ref) | `no` | string |  |
| [`nodes`](#field-nodes) | `yes` | object |  |
| [`services`](#field-services) | `yes` | array |  |
| [`steps`](#field-steps) | `yes` | array |  |
| [`assertions`](#field-assertions) | `yes` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`token64`](#def-token64) | string |  |
| [`token128`](#def-token128) | string |  |
| [`tokenList`](#def-tokenlist) | array |  |
| [`node`](#def-node) | object |  |
| [`service`](#def-service) | object |  |
| [`step`](#def-step) | object |  |
| [`assertion`](#def-assertion) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federation-scenario.v1`

<a id="field-scenario-ref"></a>
## `scenario/ref`

- Required: `yes`
- Shape: string

<a id="field-owner-slot"></a>
## `owner/slot`

- Required: `yes`
- Shape: ref: `#/$defs/token64`

<a id="field-port-base"></a>
## `port/base`

- Required: `yes`
- Shape: integer

<a id="field-evidence-claim-ref"></a>
## `evidence/claim-ref`

- Required: `no`
- Shape: string

<a id="field-nodes"></a>
## `nodes`

- Required: `yes`
- Shape: object

<a id="field-services"></a>
## `services`

- Required: `yes`
- Shape: array

<a id="field-steps"></a>
## `steps`

- Required: `yes`
- Shape: array

<a id="field-assertions"></a>
## `assertions`

- Required: `yes`
- Shape: array

## Definition Semantics

<a id="def-token64"></a>
## `$defs.token64`

- Shape: string

<a id="def-token128"></a>
## `$defs.token128`

- Shape: string

<a id="def-tokenlist"></a>
## `$defs.tokenList`

- Shape: array

<a id="def-node"></a>
## `$defs.node`

- Shape: object

<a id="def-service"></a>
## `$defs.service`

- Shape: object

<a id="def-step"></a>
## `$defs.step`

- Shape: object

<a id="def-assertion"></a>
## `$defs.assertion`

- Shape: object
