# Corpus Reasoning Answer v1

Source schema: [`doc/schemas/corpus-reasoning-answer.v1.schema.json`](../../schemas/corpus-reasoning-answer.v1.schema.json)

Signed final answer artifact for one Corpus reasoning query. This is the post-procurement result fact; live deliberation, if any, remains outside this artifact.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`answer/id`](#field-answer-id) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `yes` | string |  |
| [`responder/node-id`](#field-responder-node-id) | `yes` | string |  |
| [`selected/bid-id`](#field-selected-bid-id) | `no` | string |  |
| [`supersedes`](#field-supersedes) | `no` | string | Optional previous answer revision replaced by this answer in local latest read-models. Federated publication remains append-only: a superseding answer is a new fact, not an overwrite. |
| [`revision/no`](#field-revision-no) | `no` | integer | Optional human-facing revision counter. Ordering authority remains append-only fact order plus supersedes links, not this advisory counter alone. |
| [`room/id`](#field-room-id) | `no` | string |  |
| [`room-event/high-water`](#field-room-event-high-water) | `no` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`answer/text`](#field-answer-text) | `yes` | string |  |
| [`answer/digest`](#field-answer-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`policy/digest`](#field-policy-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`classification`](#field-classification) | `no` | enum: `Public`, `Community`, `Personal` | Optional classification.v1 tier. If omitted by a legacy/admin producer, the AD answer envelope is treated as Public; production providers should set this explicitly. |
| [`contributor/weights`](#field-contributor-weights) | `no` | array |  |
| [`evidence/refs`](#field-evidence-refs) | `no` | array |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256_digest`](#def-sha256-digest) | string |  |
| [`contributor_weight`](#def-contributor-weight) | object |  |
| [`signature`](#def-signature) | object |  |
| [`extensions`](#def-extensions) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-answer-id"></a>
## `answer/id`

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

<a id="field-responder-node-id"></a>
## `responder/node-id`

- Required: `yes`
- Shape: string

<a id="field-selected-bid-id"></a>
## `selected/bid-id`

- Required: `no`
- Shape: string

<a id="field-supersedes"></a>
## `supersedes`

- Required: `no`
- Shape: string

Optional previous answer revision replaced by this answer in local latest read-models. Federated publication remains append-only: a superseding answer is a new fact, not an overwrite.

<a id="field-revision-no"></a>
## `revision/no`

- Required: `no`
- Shape: integer

Optional human-facing revision counter. Ordering authority remains append-only fact order plus supersedes links, not this advisory counter alone.

<a id="field-room-id"></a>
## `room/id`

- Required: `no`
- Shape: string

<a id="field-room-event-high-water"></a>
## `room-event/high-water`

- Required: `no`
- Shape: integer

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-answer-text"></a>
## `answer/text`

- Required: `yes`
- Shape: string

<a id="field-answer-digest"></a>
## `answer/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-policy-digest"></a>
## `policy/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-classification"></a>
## `classification`

- Required: `no`
- Shape: enum: `Public`, `Community`, `Personal`

Optional classification.v1 tier. If omitted by a legacy/admin producer, the AD answer envelope is treated as Public; production providers should set this explicitly.

<a id="field-contributor-weights"></a>
## `contributor/weights`

- Required: `no`
- Shape: array

<a id="field-evidence-refs"></a>
## `evidence/refs`

- Required: `no`
- Shape: array

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

<a id="def-contributor-weight"></a>
## `$defs.contributor_weight`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
