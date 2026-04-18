# Resource Opinion v1

Source schema: [`doc/schemas/resource-opinion.v1.schema.json`](../../schemas/resource-opinion.v1.schema.json)

Machine-readable schema for the content body of an Agora record expressing a participant's opinion about a resource. The enclosing `agora-record.v1` envelope carries identity, authorship, topic routing, and the canonical `record/about` subject reference; this schema validates only the content body. The schema is intentionally open (`additionalProperties: true`); consumers MAY extend it with kind-specific namespaced keys of the form `<kind>/<field>` validated by a separate overlay schema (e.g. `rumor-opinion.overlay.v1`). See proposal 026 §Kind-specific extensions.

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
| [`opinion/text`](#field-opinion-text) | `no` | string | Human-authored opinion text. Renderers MUST treat this value as untrusted input and escape appropriately before display. Optional only when `opinion/rating` is present — every opinion MUST carry at least one of `opinion/text` or `opinion/rating`. Relational fields (`opinion/in-reply-to`, `opinion/see-also`, `opinion/related`) are additive context and do NOT substitute for the opinion's own substance. |
| [`opinion/rating`](#field-opinion-rating) | `no` | integer | Optional rating on a 1..5 scale where 1 is the weakest and 5 is the strongest positive assessment. The value `0` is the explicit 'no rating' marker; absence of the field has the same meaning. Consumers MUST NOT silently translate ratings to a different scale (e.g. a reputation signal) without an explicit mapping. |
| [`opinion/tags`](#field-opinion-tags) | `no` | array | Optional loose tags. Tags are not a closed taxonomy. |
| [`opinion/lang`](#field-opinion-lang) | `no` | string | Optional BCP 47 language tag for `opinion/text`. |
| [`opinion/subject-kind`](#field-opinion-subject-kind) | `no` | string | Optional soft discriminator naming the kind of subject this opinion is about (e.g. `rumor`, `gps-location`, `public-person`, `ean`, `url`). Consumers MAY use this value to select a kind-specific overlay schema and interpret namespaced extension keys (e.g. `rumor/credibility`). It does not replace `record/about` in the enclosing envelope; it is a hint for payload-level routing. |
| [`opinion/in-reply-to`](#field-opinion-in-reply-to) | `no` | string | Optional `record/id` of another opinion to which this opinion is a direct reply. Gives the opinion conversational context; consumers MAY thread replies by following this link. The referenced opinion SHOULD itself be a `resource-opinion.v1` record, but consumers MUST tolerate dangling references (the referent may be unreachable at read time). |
| [`opinion/related`](#field-opinion-related) | `no` | array | Optional list of `record/id` values of other opinions related to this one (for example: prior takes the author has seen, opinions that inspired or corroborate this one, opinions the author is explicitly contrasting with). The relation is intentionally loose; stronger semantics belong in overlay fields or in a dedicated opinion-link schema. |
| [`opinion/see-also`](#field-opinion-see-also) | `no` | array | Optional list of related opinable objects the reader may want to look at alongside this opinion. Each entry is a 2-element vector `[kind, id]`. Unlike `opinion/related`, entries here are NOT restricted to opinions — they point at the underlying objects themselves (a URL, a rumor record, a resource URN, a person identity). |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `resource-opinion.v1`

Content-level discriminator for consumers that inspect the payload outside its Agora envelope.

<a id="field-opinion-text"></a>
## `opinion/text`

- Required: `no`
- Shape: string

Human-authored opinion text. Renderers MUST treat this value as untrusted input and escape appropriately before display. Optional only when `opinion/rating` is present — every opinion MUST carry at least one of `opinion/text` or `opinion/rating`. Relational fields (`opinion/in-reply-to`, `opinion/see-also`, `opinion/related`) are additive context and do NOT substitute for the opinion's own substance.

<a id="field-opinion-rating"></a>
## `opinion/rating`

- Required: `no`
- Shape: integer

Optional rating on a 1..5 scale where 1 is the weakest and 5 is the strongest positive assessment. The value `0` is the explicit 'no rating' marker; absence of the field has the same meaning. Consumers MUST NOT silently translate ratings to a different scale (e.g. a reputation signal) without an explicit mapping.

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

<a id="field-opinion-subject-kind"></a>
## `opinion/subject-kind`

- Required: `no`
- Shape: string

Optional soft discriminator naming the kind of subject this opinion is about (e.g. `rumor`, `gps-location`, `public-person`, `ean`, `url`). Consumers MAY use this value to select a kind-specific overlay schema and interpret namespaced extension keys (e.g. `rumor/credibility`). It does not replace `record/about` in the enclosing envelope; it is a hint for payload-level routing.

<a id="field-opinion-in-reply-to"></a>
## `opinion/in-reply-to`

- Required: `no`
- Shape: string

Optional `record/id` of another opinion to which this opinion is a direct reply. Gives the opinion conversational context; consumers MAY thread replies by following this link. The referenced opinion SHOULD itself be a `resource-opinion.v1` record, but consumers MUST tolerate dangling references (the referent may be unreachable at read time).

<a id="field-opinion-related"></a>
## `opinion/related`

- Required: `no`
- Shape: array

Optional list of `record/id` values of other opinions related to this one (for example: prior takes the author has seen, opinions that inspired or corroborate this one, opinions the author is explicitly contrasting with). The relation is intentionally loose; stronger semantics belong in overlay fields or in a dedicated opinion-link schema.

<a id="field-opinion-see-also"></a>
## `opinion/see-also`

- Required: `no`
- Shape: array

Optional list of related opinable objects the reader may want to look at alongside this opinion. Each entry is a 2-element vector `[kind, id]`. Unlike `opinion/related`, entries here are NOT restricted to opinions — they point at the underlying objects themselves (a URL, a rumor record, a resource URN, a person identity).
