# Public-gossip-promotion.local.v2

Source schema: [`doc/schemas/public-gossip-promotion.local.v2.schema.json`](../../schemas/public-gossip-promotion.local.v2.schema.json)

Operator request for a versioned promotion draft. The owner resolves origin from already admitted records; the caller cannot replace it. No signature or publication is created.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `public-gossip-promotion.local.v2` |  |
| [`lineage_refs`](#field-lineage-refs) | `yes` | array |  |
| [`approval_policy_ref`](#field-approval-policy-ref) | `yes` | string |  |
| [`redaction_review_ref`](#field-redaction-review-ref) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `public-gossip-promotion.local.v2`

<a id="field-lineage-refs"></a>
## `lineage_refs`

- Required: `yes`
- Shape: array

<a id="field-approval-policy-ref"></a>
## `approval_policy_ref`

- Required: `yes`
- Shape: string

<a id="field-redaction-review-ref"></a>
## `redaction_review_ref`

- Required: `yes`
- Shape: string
