# Plain Comment v1

Source schema: [`doc/schemas/plain-comment.v1.schema.json`](../../schemas/plain-comment.v1.schema.json)

Machine-readable schema for the simplest Agora content payload: a plain-text comment. Used as the inner `content` of an `agora-record.v1` envelope when `content/schema = plain-comment.v1`. The envelope is the sole source of truth for schema identity: this object does NOT carry a `schema` discriminator, because the envelope's `content/schema` field already names the contract.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`body`](#field-body) | `yes` | string | The textual body of the comment. Plain, unformatted text by default. Renderers MUST treat the content as untrusted input and escape appropriately before display. |
| [`body/format`](#field-body-format) | `no` | enum: `text/plain`, `text/markdown` | Optional content type hint for rendering. `text/plain` is the default. `text/markdown` requests CommonMark rendering. Renderers MUST NOT execute embedded scripts or interpret active content regardless of format. |
| [`lang`](#field-lang) | `no` | string | Optional BCP 47 language tag for the comment body. Duplicates the envelope `record/lang` when both are present; when they disagree, the inner value takes precedence for rendering. |
## Field Semantics

<a id="field-body"></a>
## `body`

- Required: `yes`
- Shape: string

The textual body of the comment. Plain, unformatted text by default. Renderers MUST treat the content as untrusted input and escape appropriately before display.

<a id="field-body-format"></a>
## `body/format`

- Required: `no`
- Shape: enum: `text/plain`, `text/markdown`

Optional content type hint for rendering. `text/plain` is the default. `text/markdown` requests CommonMark rendering. Renderers MUST NOT execute embedded scripts or interpret active content regardless of format.

<a id="field-lang"></a>
## `lang`

- Required: `no`
- Shape: string

Optional BCP 47 language tag for the comment body. Duplicates the envelope `record/lang` when both are present; when they disagree, the inner value takes precedence for rendering.
