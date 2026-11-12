# Nym-bootstrap-authority-request.local.v1

Source schema: [`doc/schemas/nym-bootstrap-authority-request.local.v1.schema.json`](../../schemas/nym-bootstrap-authority-request.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`idempotency_key`](#field-idempotency-key) | `yes` | string |  |
| [`passphrase`](#field-passphrase) | `no` | string |  |
| [`exchange/revision`](#field-exchange-revision) | `no` | enum: `v1`, `v2` | Explicit transport revision. Absence retains the original v1 singleton request. |
## Field Semantics

<a id="field-idempotency-key"></a>
## `idempotency_key`

- Required: `yes`
- Shape: string

<a id="field-passphrase"></a>
## `passphrase`

- Required: `no`
- Shape: string

<a id="field-exchange-revision"></a>
## `exchange/revision`

- Required: `no`
- Shape: enum: `v1`, `v2`

Explicit transport revision. Absence retains the original v1 singleton request.
