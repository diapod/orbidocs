# Topic Resolution v1

Source schema: [`doc/schemas/topic-resolution.v1.schema.json`](../../schemas/topic-resolution.v1.schema.json)

Signed deterministic resolver output over one pinned topic taxonomy. Ambiguous and unresolved are first-class states, not malformed outputs.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`resolution/id`](#field-resolution-id) | `yes` | string |  |
| [`taxonomy/digest`](#field-taxonomy-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`resolver/version`](#field-resolver-version) | `yes` | string |  |
| [`epsilon`](#field-epsilon) | `yes` | number |  |
| [`query/keywords`](#field-query-keywords) | `yes` | array |  |
| [`result`](#field-result) | `yes` | enum: `resolved`, `ambiguous`, `unresolved` |  |
| [`topic/term`](#field-topic-term) | `no` | ref: `#/$defs/topic_term` |  |
| [`score`](#field-score) | `no` | number |  |
| [`matched/labels`](#field-matched-labels) | `yes` | array |  |
| [`candidates`](#field-candidates) | `yes` | array |  |
| [`ambiguous/reason`](#field-ambiguous-reason) | `no` | string \| null |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`resolver/node-id`](#field-resolver-node-id) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256_digest`](#def-sha256-digest) | string |  |
| [`topic_term`](#def-topic-term) | string |  |
| [`matched_label`](#def-matched-label) | object |  |
| [`candidate`](#def-candidate) | object |  |
| [`signature`](#def-signature) | object |  |
| [`extensions`](#def-extensions) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "result": {
      "const": "resolved"
    }
  },
  "required": [
    "result"
  ]
}
```

Then:

```json
{
  "required": [
    "topic/term",
    "score"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "result": {
      "const": "ambiguous"
    }
  },
  "required": [
    "result"
  ]
}
```

Then:

```json
{
  "required": [
    "ambiguous/reason"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-resolution-id"></a>
## `resolution/id`

- Required: `yes`
- Shape: string

<a id="field-taxonomy-digest"></a>
## `taxonomy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-resolver-version"></a>
## `resolver/version`

- Required: `yes`
- Shape: string

<a id="field-epsilon"></a>
## `epsilon`

- Required: `yes`
- Shape: number

<a id="field-query-keywords"></a>
## `query/keywords`

- Required: `yes`
- Shape: array

<a id="field-result"></a>
## `result`

- Required: `yes`
- Shape: enum: `resolved`, `ambiguous`, `unresolved`

<a id="field-topic-term"></a>
## `topic/term`

- Required: `no`
- Shape: ref: `#/$defs/topic_term`

<a id="field-score"></a>
## `score`

- Required: `no`
- Shape: number

<a id="field-matched-labels"></a>
## `matched/labels`

- Required: `yes`
- Shape: array

<a id="field-candidates"></a>
## `candidates`

- Required: `yes`
- Shape: array

<a id="field-ambiguous-reason"></a>
## `ambiguous/reason`

- Required: `no`
- Shape: string | null

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-resolver-node-id"></a>
## `resolver/node-id`

- Required: `yes`
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

<a id="def-topic-term"></a>
## `$defs.topic_term`

- Shape: string

<a id="def-matched-label"></a>
## `$defs.matched_label`

- Shape: object

<a id="def-candidate"></a>
## `$defs.candidate`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
