# Contact Lookup Result v1

Source schema: [`doc/schemas/contact-lookup-result.v1.schema.json`](../../schemas/contact-lookup-result.v1.schema.json)

Result of a Contact Catalog lookup. A positive result is a route candidate or invitation path, not a durable identity assertion and not proof that a relationship exists.

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
| [`catalog/id`](#field-catalog-id) | `yes` | string |  |
| [`lookup/mode`](#field-lookup-mode) | `no` | enum: `invitation-only`, `authenticated-exact`, `keyed-digest`, `blinded-digest`, `psi` |  |
| [`match/class`](#field-match-class) | `yes` | enum: `exact-control-proof`, `invitation-available`, `ambiguous`, `no-match`, `policy-denied`, `rate-limited` | MVP public or semi-public catalogs SHOULD prefer `invitation-available`, `policy-denied`, or `no-match` over identity-revealing exact-owner answers. |
| [`result/route`](#field-result-route) | `no` | ref: `#/$defs/route` |  |
| [`result/presentation-required`](#field-result-presentation-required) | `no` | boolean |  |
| [`result/invitation-required`](#field-result-invitation-required) | `no` | boolean |  |
| [`result/retry-after`](#field-result-retry-after) | `no` | string |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`audit/ref`](#field-audit-ref) | `no` | string | Optional audit reference. No-match audit references must avoid leaking raw address-book contents. |
| [`issued/at`](#field-issued-at) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `no` | string |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`route`](#def-route) | object |  |
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

- Required: `yes`
- Shape: string

<a id="field-lookup-mode"></a>
## `lookup/mode`

- Required: `no`
- Shape: enum: `invitation-only`, `authenticated-exact`, `keyed-digest`, `blinded-digest`, `psi`

<a id="field-match-class"></a>
## `match/class`

- Required: `yes`
- Shape: enum: `exact-control-proof`, `invitation-available`, `ambiguous`, `no-match`, `policy-denied`, `rate-limited`

MVP public or semi-public catalogs SHOULD prefer `invitation-available`, `policy-denied`, or `no-match` over identity-revealing exact-owner answers.

<a id="field-result-route"></a>
## `result/route`

- Required: `no`
- Shape: ref: `#/$defs/route`

<a id="field-result-presentation-required"></a>
## `result/presentation-required`

- Required: `no`
- Shape: boolean

<a id="field-result-invitation-required"></a>
## `result/invitation-required`

- Required: `no`
- Shape: boolean

<a id="field-result-retry-after"></a>
## `result/retry-after`

- Required: `no`
- Shape: string

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-audit-ref"></a>
## `audit/ref`

- Required: `no`
- Shape: string

Optional audit reference. No-match audit references must avoid leaking raw address-book contents.

<a id="field-issued-at"></a>
## `issued/at`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `no`
- Shape: string

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-route"></a>
## `$defs.route`

- Shape: object
