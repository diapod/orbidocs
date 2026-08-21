# Capability Passport Publication Desired State

Source schema: [`doc/schemas/capability-passport-publication-desired-state.v1.schema.json`](../../schemas/capability-passport-publication-desired-state.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema_version`](#field-schema-version) | `yes` | const: `v1` |  |
| [`capability_id`](#field-capability-id) | `yes` | const: `capability_passport_reconcile` |  |
| [`issued_for_module_id`](#field-issued-for-module-id) | `yes` | string |  |
| [`requested_capability_id`](#field-requested-capability-id) | `yes` | string |  |
| [`scope`](#field-scope) | `yes` | object |  |
| [`capability_profile`](#field-capability-profile) | `no` | object |  |
| [`expires_in_sec`](#field-expires-in-sec) | `no` | integer |  |
| [`publication`](#field-publication) | `no` | object |  |
## Field Semantics

<a id="field-schema-version"></a>
## `schema_version`

- Required: `yes`
- Shape: const: `v1`

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: const: `capability_passport_reconcile`

<a id="field-issued-for-module-id"></a>
## `issued_for_module_id`

- Required: `yes`
- Shape: string

<a id="field-requested-capability-id"></a>
## `requested_capability_id`

- Required: `yes`
- Shape: string

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

<a id="field-capability-profile"></a>
## `capability_profile`

- Required: `no`
- Shape: object

<a id="field-expires-in-sec"></a>
## `expires_in_sec`

- Required: `no`
- Shape: integer

<a id="field-publication"></a>
## `publication`

- Required: `no`
- Shape: object
