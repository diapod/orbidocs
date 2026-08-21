# Capability Passport Publication Status

Source schema: [`doc/schemas/capability-passport-publication-status.v1.schema.json`](../../schemas/capability-passport-publication-status.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema_version`](#field-schema-version) | `yes` | const: `v1` |  |
| [`capability_id`](#field-capability-id) | `yes` | const: `capability_passport_reconcile` |  |
| [`declaration_id`](#field-declaration-id) | `yes` | string |  |
| [`issued_for_module_id`](#field-issued-for-module-id) | `yes` | string |  |
| [`caller_principal`](#field-caller-principal) | `yes` | string |  |
| [`requested_capability_id`](#field-requested-capability-id) | `yes` | string |  |
| [`publication`](#field-publication) | `yes` | object |  |
| [`observed`](#field-observed) | `yes` | object |  |
## Field Semantics

<a id="field-schema-version"></a>
## `schema_version`

- Required: `yes`
- Shape: const: `v1`

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: const: `capability_passport_reconcile`

<a id="field-declaration-id"></a>
## `declaration_id`

- Required: `yes`
- Shape: string

<a id="field-issued-for-module-id"></a>
## `issued_for_module_id`

- Required: `yes`
- Shape: string

<a id="field-caller-principal"></a>
## `caller_principal`

- Required: `yes`
- Shape: string

<a id="field-requested-capability-id"></a>
## `requested_capability_id`

- Required: `yes`
- Shape: string

<a id="field-publication"></a>
## `publication`

- Required: `yes`
- Shape: object

<a id="field-observed"></a>
## `observed`

- Required: `yes`
- Shape: object
