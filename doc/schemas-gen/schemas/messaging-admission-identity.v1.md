# Messaging Admission Identity Support

Source schema: [`doc/schemas/messaging-admission-identity.v1.schema.json`](../../schemas/messaging-admission-identity.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`profile`](#field-profile) | `yes` | const: `messaging-admission-identity.v1` |  |
| [`contract/digest`](#field-contract-digest) | `yes` | string |  |
| [`store/epoch`](#field-store-epoch) | `yes` | string |  |
| [`coverage/from`](#field-coverage-from) | `yes` | string |  |
| [`guaranteed/until`](#field-guaranteed-until) | `yes` | string |  |
## Field Semantics

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: const: `messaging-admission-identity.v1`

<a id="field-contract-digest"></a>
## `contract/digest`

- Required: `yes`
- Shape: string

<a id="field-store-epoch"></a>
## `store/epoch`

- Required: `yes`
- Shape: string

<a id="field-coverage-from"></a>
## `coverage/from`

- Required: `yes`
- Shape: string

<a id="field-guaranteed-until"></a>
## `guaranteed/until`

- Required: `yes`
- Shape: string
