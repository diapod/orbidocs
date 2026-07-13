# Inquirium Adapter Response v1

Source schema: [`doc/schemas/inquirium.adapter.response.v1.schema.json`](../../schemas/inquirium.adapter.response.v1.schema.json)

Neutral text-generation response emitted by middleware-hosted Inquirium adapters.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inquirium.adapter.response.v1` |  |
| [`provider`](#field-provider) | `yes` | string |  |
| [`provider_request_id`](#field-provider-request-id) | `no` | string \| null |  |
| [`model`](#field-model) | `no` | string \| null |  |
| [`output`](#field-output) | `yes` | array |  |
| [`epistemic`](#field-epistemic) | `no` | ref: `#/$defs/epistemicFrame` |  |
| [`params`](#field-params) | `no` | object |  |
| [`control`](#field-control) | `no` | array |  |
| [`stop_reason`](#field-stop-reason) | `no` | string \| null |  |
| [`usage`](#field-usage) | `yes` | object |  |
| [`diagnostics`](#field-diagnostics) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`outputChunk`](#def-outputchunk) | unspecified |  |
| [`textOutputChunk`](#def-textoutputchunk) | object |  |
| [`structuredOutputChunk`](#def-structuredoutputchunk) | object |  |
| [`epistemicFrame`](#def-epistemicframe) | object |  |
| [`controlItem`](#def-controlitem) | unspecified |  |
| [`recallSchemaControlItem`](#def-recallschemacontrolitem) | object |  |
| [`recallGlossaryControlItem`](#def-recallglossarycontrolitem) | object |  |
| [`toolCallControlItem`](#def-toolcallcontrolitem) | object |  |
| [`operatorQuestionControlItem`](#def-operatorquestioncontrolitem) | object |  |
| [`reviseOutputControlItem`](#def-reviseoutputcontrolitem) | object |  |
| [`crisisCandidateControlItem`](#def-crisiscandidatecontrolitem) | object |  |
| [`degradedControlItem`](#def-degradedcontrolitem) | object |  |
| [`refusalControlItem`](#def-refusalcontrolitem) | object |  |
| [`recallControlPayload`](#def-recallcontrolpayload) | object |  |
| [`toolCallPayload`](#def-toolcallpayload) | object |  |
| [`reviseOutputPayload`](#def-reviseoutputpayload) | object |  |
| [`controlReasonPayload`](#def-controlreasonpayload) | object |  |
| [`operatorQuestionPayload`](#def-operatorquestionpayload) | object |  |
| [`crisisCandidatePayload`](#def-crisiscandidatepayload) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inquirium.adapter.response.v1`

<a id="field-provider"></a>
## `provider`

- Required: `yes`
- Shape: string

<a id="field-provider-request-id"></a>
## `provider_request_id`

- Required: `no`
- Shape: string | null

<a id="field-model"></a>
## `model`

- Required: `no`
- Shape: string | null

<a id="field-output"></a>
## `output`

- Required: `yes`
- Shape: array

<a id="field-epistemic"></a>
## `epistemic`

- Required: `no`
- Shape: ref: `#/$defs/epistemicFrame`

<a id="field-params"></a>
## `params`

- Required: `no`
- Shape: object

<a id="field-control"></a>
## `control`

- Required: `no`
- Shape: array

<a id="field-stop-reason"></a>
## `stop_reason`

- Required: `no`
- Shape: string | null

<a id="field-usage"></a>
## `usage`

- Required: `yes`
- Shape: object

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-outputchunk"></a>
## `$defs.outputChunk`

- Shape: unspecified

<a id="def-textoutputchunk"></a>
## `$defs.textOutputChunk`

- Shape: object

<a id="def-structuredoutputchunk"></a>
## `$defs.structuredOutputChunk`

- Shape: object

<a id="def-epistemicframe"></a>
## `$defs.epistemicFrame`

- Shape: object

<a id="def-controlitem"></a>
## `$defs.controlItem`

- Shape: unspecified

<a id="def-recallschemacontrolitem"></a>
## `$defs.recallSchemaControlItem`

- Shape: object

<a id="def-recallglossarycontrolitem"></a>
## `$defs.recallGlossaryControlItem`

- Shape: object

<a id="def-toolcallcontrolitem"></a>
## `$defs.toolCallControlItem`

- Shape: object

<a id="def-operatorquestioncontrolitem"></a>
## `$defs.operatorQuestionControlItem`

- Shape: object

<a id="def-reviseoutputcontrolitem"></a>
## `$defs.reviseOutputControlItem`

- Shape: object

<a id="def-crisiscandidatecontrolitem"></a>
## `$defs.crisisCandidateControlItem`

- Shape: object

<a id="def-degradedcontrolitem"></a>
## `$defs.degradedControlItem`

- Shape: object

<a id="def-refusalcontrolitem"></a>
## `$defs.refusalControlItem`

- Shape: object

<a id="def-recallcontrolpayload"></a>
## `$defs.recallControlPayload`

- Shape: object

<a id="def-toolcallpayload"></a>
## `$defs.toolCallPayload`

- Shape: object

<a id="def-reviseoutputpayload"></a>
## `$defs.reviseOutputPayload`

- Shape: object

<a id="def-controlreasonpayload"></a>
## `$defs.controlReasonPayload`

- Shape: object

<a id="def-operatorquestionpayload"></a>
## `$defs.operatorQuestionPayload`

- Shape: object

<a id="def-crisiscandidatepayload"></a>
## `$defs.crisisCandidatePayload`

- Shape: object
