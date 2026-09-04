# Inference Provenance Common Definitions v1

Source schema: [`doc/schemas/inference-provenance-common.v1.schema.json`](../../schemas/inference-provenance-common.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`provider-ref`](#def-provider-ref) | string |  |
| [`provider-disclosure`](#def-provider-disclosure) | enum: `complete`, `partial`, `withheld`, `unknown` |  |
| [`evidence-basis`](#def-evidence-basis) | unspecified |  |
| [`evidence-requirement`](#def-evidence-requirement) | unspecified |  |
| [`extensions`](#def-extensions) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-provider-ref"></a>
## `$defs.provider-ref`

- Shape: string

<a id="def-provider-disclosure"></a>
## `$defs.provider-disclosure`

- Shape: enum: `complete`, `partial`, `withheld`, `unknown`

<a id="def-evidence-basis"></a>
## `$defs.evidence-basis`

- Shape: unspecified

<a id="def-evidence-requirement"></a>
## `$defs.evidence-requirement`

- Shape: unspecified

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
