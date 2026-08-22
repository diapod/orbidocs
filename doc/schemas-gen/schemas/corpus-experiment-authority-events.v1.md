# Corpus Experiment Authority Events v1

Source schema: [`doc/schemas/corpus-experiment-authority-events.v1.schema.json`](../../schemas/corpus-experiment-authority-events.v1.schema.json)

Ordered host evidence that one experiment was operator-approved and executed through one fenced P083 control lease.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`authority-events`](#def-authority-events) | array |  |
| [`operator-approval-event`](#def-operator-approval-event) | object |  |
| [`control-claim-event`](#def-control-claim-event) | unspecified |  |
| [`effect-invoke-event`](#def-effect-invoke-event) | unspecified |  |
| [`control-release-event`](#def-control-release-event) | unspecified |  |
| [`lease-authority-event`](#def-lease-authority-event) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-authority-events"></a>
## `$defs.authority-events`

- Shape: array

<a id="def-operator-approval-event"></a>
## `$defs.operator-approval-event`

- Shape: object

<a id="def-control-claim-event"></a>
## `$defs.control-claim-event`

- Shape: unspecified

<a id="def-effect-invoke-event"></a>
## `$defs.effect-invoke-event`

- Shape: unspecified

<a id="def-control-release-event"></a>
## `$defs.control-release-event`

- Shape: unspecified

<a id="def-lease-authority-event"></a>
## `$defs.lease-authority-event`

- Shape: object
