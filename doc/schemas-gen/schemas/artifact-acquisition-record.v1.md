# Artifact Acquisition Record v1

Source schema: [`doc/schemas/artifact-acquisition-record.v1.schema.json`](../../schemas/artifact-acquisition-record.v1.schema.json)

Closed append-only record family for acquisition attempts, stable receipts, extraction facts, and object transitions.

## Governing Basis

- [`doc/project/40-proposals/088-pull-based-artifact-acquisition.md`](../../project/40-proposals/088-pull-based-artifact-acquisition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`ref`](#def-ref) | string |  |
| [`refusal`](#def-refusal) | object |  |
| [`attempt`](#def-attempt) | object |  |
| [`receipt`](#def-receipt) | object |  |
| [`extraction`](#def-extraction) | object |  |
| [`contentEvidence`](#def-contentevidence) | object |  |
| [`objectTransition`](#def-objecttransition) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-refusal"></a>
## `$defs.refusal`

- Shape: object

<a id="def-attempt"></a>
## `$defs.attempt`

- Shape: object

<a id="def-receipt"></a>
## `$defs.receipt`

- Shape: object

<a id="def-extraction"></a>
## `$defs.extraction`

- Shape: object

<a id="def-contentevidence"></a>
## `$defs.contentEvidence`

- Shape: object

<a id="def-objecttransition"></a>
## `$defs.objectTransition`

- Shape: object
