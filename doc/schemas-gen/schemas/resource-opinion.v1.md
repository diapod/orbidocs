# Resource Opinion v1

Source schema: [`doc/schemas/resource-opinion.v1.schema.json`](../../schemas/resource-opinion.v1.schema.json)

Machine-readable schema for the content body of an Agora record expressing a participant's opinion about a resource. The enclosing `agora-record.v1` envelope carries identity, authorship, topic routing, and the canonical `record/about` subject reference; this schema validates only the content body.

## Governing Basis

- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)
- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/50-requirements/requirements-014.md`](../../project/50-requirements/requirements-014.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)
- [`doc/project/50-requirements/requirements-014.md`](../../project/50-requirements/requirements-014.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `resource-opinion.v1` | Content-level discriminator for consumers that inspect the payload outside its Agora envelope. |
| [`opinion/text`](#field-opinion-text) | `yes` | string | Human-authored opinion text. Renderers MUST treat this value as untrusted input and escape appropriately before display. |
| [`opinion/rating`](#field-opinion-rating) | `no` | enum: `-1`, `0`, `1` | Optional ternary rating: negative (-1), neutral (0), or positive (1). Absence means no rating was supplied. |
| [`opinion/tags`](#field-opinion-tags) | `no` | array | Optional loose tags. Tags are not a closed taxonomy. |
| [`opinion/lang`](#field-opinion-lang) | `no` | string | Optional BCP 47 language tag for `opinion/text`. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `resource-opinion.v1`

Content-level discriminator for consumers that inspect the payload outside its Agora envelope.

<a id="field-opinion-text"></a>
## `opinion/text`

- Required: `yes`
- Shape: string

Human-authored opinion text. Renderers MUST treat this value as untrusted input and escape appropriately before display.

<a id="field-opinion-rating"></a>
## `opinion/rating`

- Required: `no`
- Shape: enum: `-1`, `0`, `1`

Optional ternary rating: negative (-1), neutral (0), or positive (1). Absence means no rating was supplied.

<a id="field-opinion-tags"></a>
## `opinion/tags`

- Required: `no`
- Shape: array

Optional loose tags. Tags are not a closed taxonomy.

<a id="field-opinion-lang"></a>
## `opinion/lang`

- Required: `no`
- Shape: string

Optional BCP 47 language tag for `opinion/text`.
