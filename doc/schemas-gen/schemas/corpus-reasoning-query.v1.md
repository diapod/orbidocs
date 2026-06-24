# Corpus Reasoning Query v1

Source schema: [`doc/schemas/corpus-reasoning-query.v1.schema.json`](../../schemas/corpus-reasoning-query.v1.schema.json)

MVP Corpus procurement query. It decorates an existing question-envelope.v1 with a resolved topic, buyer price bracket, reply target, and fan-out bounds.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`correlation/id`](#field-correlation-id) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`requester/node-id`](#field-requester-node-id) | `yes` | string |  |
| [`requester/participant-id`](#field-requester-participant-id) | `yes` | string |  |
| [`topic/term`](#field-topic-term) | `yes` | ref: `#/$defs/topic_term` |  |
| [`corpus/taxonomy-digest`](#field-corpus-taxonomy-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`query/keywords`](#field-query-keywords) | `yes` | array |  |
| [`question`](#field-question) | `yes` | ref: `question-envelope.v1.schema.json` |  |
| [`pricing/min-amount`](#field-pricing-min-amount) | `yes` | integer | Minimum acceptable buyer price in minor units. |
| [`pricing/max-amount`](#field-pricing-max-amount) | `yes` | integer | Maximum acceptable buyer price in minor units. |
| [`pricing/currency`](#field-pricing-currency) | `yes` | string |  |
| [`max/candidates`](#field-max-candidates) | `yes` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`deadline-at`](#field-deadline-at) | `yes` | string |  |
| [`reply/target`](#field-reply-target) | `yes` | ref: `#/$defs/reply_target` |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256_digest`](#def-sha256-digest) | string |  |
| [`topic_term`](#def-topic-term) | string |  |
| [`reply_target`](#def-reply-target) | object |  |
| [`extensions`](#def-extensions) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-requester-node-id"></a>
## `requester/node-id`

- Required: `yes`
- Shape: string

<a id="field-requester-participant-id"></a>
## `requester/participant-id`

- Required: `yes`
- Shape: string

<a id="field-topic-term"></a>
## `topic/term`

- Required: `yes`
- Shape: ref: `#/$defs/topic_term`

<a id="field-corpus-taxonomy-digest"></a>
## `corpus/taxonomy-digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-query-keywords"></a>
## `query/keywords`

- Required: `yes`
- Shape: array

<a id="field-question"></a>
## `question`

- Required: `yes`
- Shape: ref: `question-envelope.v1.schema.json`

<a id="field-pricing-min-amount"></a>
## `pricing/min-amount`

- Required: `yes`
- Shape: integer

Minimum acceptable buyer price in minor units.

<a id="field-pricing-max-amount"></a>
## `pricing/max-amount`

- Required: `yes`
- Shape: integer

Maximum acceptable buyer price in minor units.

<a id="field-pricing-currency"></a>
## `pricing/currency`

- Required: `yes`
- Shape: string

<a id="field-max-candidates"></a>
## `max/candidates`

- Required: `yes`
- Shape: integer

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-deadline-at"></a>
## `deadline-at`

- Required: `yes`
- Shape: string

<a id="field-reply-target"></a>
## `reply/target`

- Required: `yes`
- Shape: ref: `#/$defs/reply_target`

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

<a id="def-reply-target"></a>
## `$defs.reply_target`

- Shape: object

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
