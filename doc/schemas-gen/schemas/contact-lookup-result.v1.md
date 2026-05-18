# Contact Lookup Result v1

Source schema: [`doc/schemas/contact-lookup-result.v1.schema.json`](../../schemas/contact-lookup-result.v1.schema.json)

Route-set result of a Contact Catalog lookup. A positive result is a lookup-safe route candidate, not identity assurance and not proof that a relationship exists.

## Governing Basis

- [`doc/project/40-proposals/058-contact-catalog.md`](../../project/40-proposals/058-contact-catalog.md)
- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)
- [`doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-010-message-to-a-friend.md`](../../project/30-stories/story-010-message-to-a-friend.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `contact-lookup-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`lookup/id`](#field-lookup-id) | `yes` | string |  |
| [`catalog/id`](#field-catalog-id) | `no` | string |  |
| [`lookup/mode`](#field-lookup-mode) | `yes` | enum: `invitation-only`, `blinded-digest`, `psi` |  |
| [`match/class`](#field-match-class) | `yes` | enum: `invitation-available`, `ambiguous`, `no-match`, `policy-denied`, `rate-limited` |  |
| [`result/routes`](#field-result-routes) | `yes` | array |  |
| [`selected/route`](#field-selected-route) | `no` | ref: `#/$defs/route` |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`policy/ref`](#field-policy-ref) | `no` | string |  |
| [`issued/at`](#field-issued-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`route`](#def-route) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "match/class": {
      "const": "invitation-available"
    }
  },
  "required": [
    "match/class"
  ]
}
```

Then:

```json
{
  "required": [
    "selected/route"
  ],
  "properties": {
    "result/routes": {
      "minItems": 1
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `contact-lookup-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-lookup-id"></a>
## `lookup/id`

- Required: `yes`
- Shape: string

<a id="field-catalog-id"></a>
## `catalog/id`

- Required: `no`
- Shape: string

<a id="field-lookup-mode"></a>
## `lookup/mode`

- Required: `yes`
- Shape: enum: `invitation-only`, `blinded-digest`, `psi`

<a id="field-match-class"></a>
## `match/class`

- Required: `yes`
- Shape: enum: `invitation-available`, `ambiguous`, `no-match`, `policy-denied`, `rate-limited`

<a id="field-result-routes"></a>
## `result/routes`

- Required: `yes`
- Shape: array

<a id="field-selected-route"></a>
## `selected/route`

- Required: `no`
- Shape: ref: `#/$defs/route`

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `no`
- Shape: string

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-route"></a>
## `$defs.route`

- Shape: object
