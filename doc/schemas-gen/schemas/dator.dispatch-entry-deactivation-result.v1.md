# Dator Dispatch Entry Deactivation Result v1

Source schema: [`doc/schemas/dator.dispatch-entry-deactivation-result.v1.schema.json`](../../schemas/dator.dispatch-entry-deactivation-result.v1.schema.json)

Exact idempotent result of synchronously deactivating one Dator dispatch entry.

## Governing Basis

- [`doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`](../../project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `dator.dispatch-entry-deactivation-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`event/ref`](#field-event-ref) | `yes` | string |  |
| [`entry/ref`](#field-entry-ref) | `yes` | string |  |
| [`entry/revision`](#field-entry-revision) | `yes` | integer |  |
| [`entry/digest`](#field-entry-digest) | `yes` | string |  |
| [`activation/generation`](#field-activation-generation) | `yes` | integer |  |
| [`status`](#field-status) | `yes` | const: `deactivated` |  |
| [`recorded-at`](#field-recorded-at) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `dator.dispatch-entry-deactivation-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-event-ref"></a>
## `event/ref`

- Required: `yes`
- Shape: string

<a id="field-entry-ref"></a>
## `entry/ref`

- Required: `yes`
- Shape: string

<a id="field-entry-revision"></a>
## `entry/revision`

- Required: `yes`
- Shape: integer

<a id="field-entry-digest"></a>
## `entry/digest`

- Required: `yes`
- Shape: string

<a id="field-activation-generation"></a>
## `activation/generation`

- Required: `yes`
- Shape: integer

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `deactivated`

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string
