# Exact Local Artifact Delivery Reconciliation Result

Source schema: [`doc/schemas/artifact-delivery-reconciliation.local.v1.schema.json`](../../schemas/artifact-delivery-reconciliation.local.v1.schema.json)

## Governing Basis

- [`doc/project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery`](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md#consent-loss-recovery)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-delivery-reconciliation.local.v1` |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`submission/digest`](#field-submission-digest) | `yes` | string |  |
| [`delivery/id`](#field-delivery-id) | `no` | string |  |
| [`observation`](#field-observation) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "observation": {
      "properties": {
        "kind": {
          "const": "historical"
        }
      }
    }
  }
}
```

Then:

```json
{
  "required": [
    "delivery/id"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-delivery-reconciliation.local.v1`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-submission-digest"></a>
## `submission/digest`

- Required: `yes`
- Shape: string

<a id="field-delivery-id"></a>
## `delivery/id`

- Required: `no`
- Shape: string

<a id="field-observation"></a>
## `observation`

- Required: `yes`
- Shape: unspecified
