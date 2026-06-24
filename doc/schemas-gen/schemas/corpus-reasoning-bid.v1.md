# Corpus Reasoning Bid v1

Source schema: [`doc/schemas/corpus-reasoning-bid.v1.schema.json`](../../schemas/corpus-reasoning-bid.v1.schema.json)

Provider response envelope for one Corpus reasoning query. Accepted and counter bids embed an ordinary procurement-offer.v1 instead of defining a parallel pricing contract.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`bid/id`](#field-bid-id) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `yes` | string |  |
| [`bidder/node-id`](#field-bidder-node-id) | `yes` | string |  |
| [`decision`](#field-decision) | `yes` | enum: `accept`, `decline`, `counter` |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`bid/valid-until`](#field-bid-valid-until) | `yes` | string |  |
| [`policy/digest`](#field-policy-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`procurement-offer`](#field-procurement-offer) | `no` | ref: `procurement-offer.v1.schema.json` |  |
| [`decline/reason`](#field-decline-reason) | `no` | enum: `no-capacity`, `out-of-policy`, `topic-mismatch`, `price-too-low`, `unavailable`, `other` |  |
| [`diagnostic/ref`](#field-diagnostic-ref) | `no` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256_digest`](#def-sha256-digest) | string |  |
| [`signature`](#def-signature) | object |  |
| [`extensions`](#def-extensions) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "decision": {
      "enum": [
        "accept",
        "counter"
      ]
    }
  },
  "required": [
    "decision"
  ]
}
```

Then:

```json
{
  "required": [
    "procurement-offer"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "decision": {
      "const": "decline"
    }
  },
  "required": [
    "decision"
  ]
}
```

Then:

```json
{
  "required": [
    "decline/reason"
  ],
  "not": {
    "required": [
      "procurement-offer"
    ]
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-bid-id"></a>
## `bid/id`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `yes`
- Shape: string

<a id="field-bidder-node-id"></a>
## `bidder/node-id`

- Required: `yes`
- Shape: string

<a id="field-decision"></a>
## `decision`

- Required: `yes`
- Shape: enum: `accept`, `decline`, `counter`

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-bid-valid-until"></a>
## `bid/valid-until`

- Required: `yes`
- Shape: string

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-procurement-offer"></a>
## `procurement-offer`

- Required: `no`
- Shape: ref: `procurement-offer.v1.schema.json`

<a id="field-decline-reason"></a>
## `decline/reason`

- Required: `no`
- Shape: enum: `no-capacity`, `out-of-policy`, `topic-mismatch`, `price-too-low`, `unavailable`, `other`

<a id="field-diagnostic-ref"></a>
## `diagnostic/ref`

- Required: `no`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `#/$defs/extensions`

## Definition Semantics

<a id="def-sha256-digest"></a>
## `$defs.sha256_digest`

- Shape: string

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
