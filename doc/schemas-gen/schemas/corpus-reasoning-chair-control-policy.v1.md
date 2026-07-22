# Corpus Reasoning Chair Control Policy v1

Source schema: [`doc/schemas/corpus-reasoning-chair-control-policy.v1.schema.json`](../../schemas/corpus-reasoning-chair-control-policy.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/070-room-primitive.md`](../../project/40-proposals/070-room-primitive.md)
- [`doc/project/60-solutions/047-agent/047-agent.md`](../../project/60-solutions/047-agent/047-agent.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-reasoning-chair-control-policy.v1` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`round/id`](#field-round-id) | `yes` | string |  |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`chair/subject`](#field-chair-subject) | `yes` | string |  |
| [`chair/agent-ref`](#field-chair-agent-ref) | `no` | string |  |
| [`policy/generation`](#field-policy-generation) | `yes` | integer |  |
| [`requested`](#field-requested) | `yes` | ref: `#/$defs/control-values` |  |
| [`effective`](#field-effective) | `yes` | ref: `#/$defs/control-values` |  |
| [`issued-at`](#field-issued-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`control-values`](#def-control-values) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-reasoning-chair-control-policy.v1`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-round-id"></a>
## `round/id`

- Required: `yes`
- Shape: string

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-chair-subject"></a>
## `chair/subject`

- Required: `yes`
- Shape: string

<a id="field-chair-agent-ref"></a>
## `chair/agent-ref`

- Required: `no`
- Shape: string

<a id="field-policy-generation"></a>
## `policy/generation`

- Required: `yes`
- Shape: integer

<a id="field-requested"></a>
## `requested`

- Required: `yes`
- Shape: ref: `#/$defs/control-values`

<a id="field-effective"></a>
## `effective`

- Required: `yes`
- Shape: ref: `#/$defs/control-values`

<a id="field-issued-at"></a>
## `issued-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-control-values"></a>
## `$defs.control-values`

- Shape: object
