# Public Gossip v1

Source schema: [`doc/schemas/public-gossip.v1.schema.json`](../../schemas/public-gossip.v1.schema.json)

Machine-readable schema for the content body of an Agora record carrying a public, bounded gossip item: a rumor, weak signal, or low-resolution observation that is intentionally not evidence. The enclosing `agora-record.v1` envelope carries identity, authorship, topic routing, `record/about`, parent/supersedes links, and signature. This payload carries only the public epistemic claim and its local context.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/60-solutions/008-agora/008-agora-dir-simplify-impl.md`](../../project/60-solutions/008-agora/008-agora-dir-simplify-impl.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `public-gossip.v1` | Content-level discriminator for consumers that inspect the payload outside its Agora envelope. |
| [`gossip/text`](#field-gossip-text) | `yes` | string | Human-readable public gossip text. Renderers MUST treat it as untrusted input. This text is not evidence; it is a public claim requiring independent corroboration. |
| [`gossip/lang`](#field-gossip-lang) | `no` | string | Optional BCP 47 language tag for `gossip/text`. |
| [`epistemic/class`](#field-epistemic-class) | `yes` | enum: `rumor`, `weak-signal`, `observation` | Epistemic posture. `rumor` is unverified social information; `weak-signal` is an early pattern hint; `observation` is a low-resolution public observation that still must not be treated as verified evidence by this schema alone. |
| [`topic/class`](#field-topic-class) | `yes` | string | Normalized semantic class used for topic grouping and local correlation. This is not the Agora `topic/key`; it is payload-level meaning. |
| [`context/facets`](#field-context-facets) | `no` | array | Optional low-resolution facets that help readers and indexers understand the context without forcing raw disclosure. |
| [`confidence`](#field-confidence) | `yes` | number | Author-local confidence in the relevance or signal value. Consumers MUST NOT treat this as proof or reputation weight without an explicit policy mapping. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | const: `public` | Public gossip is intentionally public. Private or federation-scoped rumor exchange belongs to `whisper-signal.v1` or another non-public transport policy. |
| [`gossip/source-kind`](#field-gossip-source-kind) | `no` | enum: `first-hand`, `second-hand`, `pattern-observed`, `machine-assisted`, `unspecified` | Optional coarse source posture. It is a disclosure aid, not an evidentiary proof. |
| [`gossip/tags`](#field-gossip-tags) | `no` | array | Optional loose tags. Tags are not a closed taxonomy. |
| [`gossip/expires-at`](#field-gossip-expires-at) | `no` | string | Optional author-suggested expiration time for the effective gossip view. Projection policy MAY clamp this value and MUST keep the historical Agora record immutable. |
| [`gossip/decay-half-life-seconds`](#field-gossip-decay-half-life-seconds) | `no` | integer | Optional author-suggested half-life for local effective-weight decay. Projection policy MAY clamp this value. |
| [`gossip/min-effective-weight`](#field-gossip-min-effective-weight) | `no` | number | Optional author-suggested minimum effective weight below which the local projection may treat the gossip as below-threshold. Projection policy MAY clamp this value. |
| [`gossip/see-also`](#field-gossip-see-also) | `no` | array | Optional related public resources or records. |
| [`policy/notes`](#field-policy-notes) | `no` | string | Optional policy or moderation note shown to readers. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `public-gossip.v1`

Content-level discriminator for consumers that inspect the payload outside its Agora envelope.

<a id="field-gossip-text"></a>
## `gossip/text`

- Required: `yes`
- Shape: string

Human-readable public gossip text. Renderers MUST treat it as untrusted input. This text is not evidence; it is a public claim requiring independent corroboration.

<a id="field-gossip-lang"></a>
## `gossip/lang`

- Required: `no`
- Shape: string

Optional BCP 47 language tag for `gossip/text`.

<a id="field-epistemic-class"></a>
## `epistemic/class`

- Required: `yes`
- Shape: enum: `rumor`, `weak-signal`, `observation`

Epistemic posture. `rumor` is unverified social information; `weak-signal` is an early pattern hint; `observation` is a low-resolution public observation that still must not be treated as verified evidence by this schema alone.

<a id="field-topic-class"></a>
## `topic/class`

- Required: `yes`
- Shape: string

Normalized semantic class used for topic grouping and local correlation. This is not the Agora `topic/key`; it is payload-level meaning.

<a id="field-context-facets"></a>
## `context/facets`

- Required: `no`
- Shape: array

Optional low-resolution facets that help readers and indexers understand the context without forcing raw disclosure.

<a id="field-confidence"></a>
## `confidence`

- Required: `yes`
- Shape: number

Author-local confidence in the relevance or signal value. Consumers MUST NOT treat this as proof or reputation weight without an explicit policy mapping.

<a id="field-disclosure-scope"></a>
## `disclosure/scope`

- Required: `yes`
- Shape: const: `public`

Public gossip is intentionally public. Private or federation-scoped rumor exchange belongs to `whisper-signal.v1` or another non-public transport policy.

<a id="field-gossip-source-kind"></a>
## `gossip/source-kind`

- Required: `no`
- Shape: enum: `first-hand`, `second-hand`, `pattern-observed`, `machine-assisted`, `unspecified`

Optional coarse source posture. It is a disclosure aid, not an evidentiary proof.

<a id="field-gossip-tags"></a>
## `gossip/tags`

- Required: `no`
- Shape: array

Optional loose tags. Tags are not a closed taxonomy.

<a id="field-gossip-expires-at"></a>
## `gossip/expires-at`

- Required: `no`
- Shape: string

Optional author-suggested expiration time for the effective gossip view. Projection policy MAY clamp this value and MUST keep the historical Agora record immutable.

<a id="field-gossip-decay-half-life-seconds"></a>
## `gossip/decay-half-life-seconds`

- Required: `no`
- Shape: integer

Optional author-suggested half-life for local effective-weight decay. Projection policy MAY clamp this value.

<a id="field-gossip-min-effective-weight"></a>
## `gossip/min-effective-weight`

- Required: `no`
- Shape: number

Optional author-suggested minimum effective weight below which the local projection may treat the gossip as below-threshold. Projection policy MAY clamp this value.

<a id="field-gossip-see-also"></a>
## `gossip/see-also`

- Required: `no`
- Shape: array

Optional related public resources or records.

<a id="field-policy-notes"></a>
## `policy/notes`

- Required: `no`
- Shape: string

Optional policy or moderation note shown to readers.
