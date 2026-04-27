# Capability Schema v1

Source schema: [`doc/schemas/capability-schema.v1.schema.json`](../../schemas/capability-schema.v1.schema.json)

Portable, content-addressed machine-readable schema artifact for one capability profile. Nodes may serve this artifact over the authenticated peer-message channel so receivers can validate capability scope, inputs, outputs, error profiles, and retry semantics without depending on an external URL.

## Governing Basis

- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/027-middleware-peer-message-dispatch.md`](../../project/40-proposals/027-middleware-peer-message-dispatch.md)
- [`doc/project/60-solutions/capability-advertisement.md`](../../project/60-solutions/capability-advertisement.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-schema.v1` | Schema discriminator. MUST be exactly `capability-schema.v1`. |
| [`schema/id`](#field-schema-id) | `yes` | string | Stable logical identifier of the capability schema contract. This identifies what contract the content describes, not where it is hosted. |
| [`schema/ref`](#field-schema-ref) | `yes` | string | Content-addressed reference to the canonical schema content. Receivers MUST verify that `content` hashes to this reference before using the schema. |
| [`schema/media-type`](#field-schema-media-type) | `yes` | string | Media type of `content`, for example `application/schema+json`, `application/vnd.malli+edn`, or another profile-accepted machine-readable schema format. |
| [`capability/id`](#field-capability-id) | `no` | string | Optional capability id this schema describes. Formal profiles may use a bare id; sovereign or private profiles may use an identity-anchored id. |
| [`compatible_with`](#field-compatible-with) | `no` | string | Optional formal capability id whose public contract this schema claims to implement. Omit for purely custom `~...@...` protocols. |
| [`wire/name`](#field-wire-name) | `no` | string | Optional wire-visible projection associated with the capability id. |
| [`display/name`](#field-display-name) | `no` | string | Short human-readable capability name for UI display. |
| [`description`](#field-description) | `no` | string | Human-readable capability explanation. |
| [`lang`](#field-lang) | `no` | string | BCP 47-style language tag for human-readable fields. |
| [`doc/ref`](#field-doc-ref) | `no` | string | Optional content-addressed reference to human-readable documentation. |
| [`doc/url`](#field-doc-url) | `no` | string | Optional convenience URL for human-readable documentation. This is a mirror or hint, not a protocol dependency. |
| [`content`](#field-content) | `yes` | unspecified | Machine-readable schema content. The interpretation is selected by `schema/media-type`. |
| [`published-at`](#field-published-at) | `yes` | string | Timestamp when this schema artifact was published. |
| [`author/node-id`](#field-author-node-id) | `yes` | string | Node identity that publishes this schema artifact. |
| [`author/participant-id`](#field-author-participant-id) | `no` | string | Optional participant identity responsible for authoring or approving this schema artifact. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation-local annotations that do not change core schema semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object | Signature over the deterministic canonical form of this artifact with the top-level `signature` field omitted. The `schema/ref` still addresses only the canonical `content` value. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-schema.v1`

Schema discriminator. MUST be exactly `capability-schema.v1`.

<a id="field-schema-id"></a>
## `schema/id`

- Required: `yes`
- Shape: string

Stable logical identifier of the capability schema contract. This identifies what contract the content describes, not where it is hosted.

<a id="field-schema-ref"></a>
## `schema/ref`

- Required: `yes`
- Shape: string

Content-addressed reference to the canonical schema content. Receivers MUST verify that `content` hashes to this reference before using the schema.

<a id="field-schema-media-type"></a>
## `schema/media-type`

- Required: `yes`
- Shape: string

Media type of `content`, for example `application/schema+json`, `application/vnd.malli+edn`, or another profile-accepted machine-readable schema format.

<a id="field-capability-id"></a>
## `capability/id`

- Required: `no`
- Shape: string

Optional capability id this schema describes. Formal profiles may use a bare id; sovereign or private profiles may use an identity-anchored id.

<a id="field-compatible-with"></a>
## `compatible_with`

- Required: `no`
- Shape: string

Optional formal capability id whose public contract this schema claims to implement. Omit for purely custom `~...@...` protocols.

<a id="field-wire-name"></a>
## `wire/name`

- Required: `no`
- Shape: string

Optional wire-visible projection associated with the capability id.

<a id="field-display-name"></a>
## `display/name`

- Required: `no`
- Shape: string

Short human-readable capability name for UI display.

<a id="field-description"></a>
## `description`

- Required: `no`
- Shape: string

Human-readable capability explanation.

<a id="field-lang"></a>
## `lang`

- Required: `no`
- Shape: string

BCP 47-style language tag for human-readable fields.

<a id="field-doc-ref"></a>
## `doc/ref`

- Required: `no`
- Shape: string

Optional content-addressed reference to human-readable documentation.

<a id="field-doc-url"></a>
## `doc/url`

- Required: `no`
- Shape: string

Optional convenience URL for human-readable documentation. This is a mirror or hint, not a protocol dependency.

<a id="field-content"></a>
## `content`

- Required: `yes`
- Shape: unspecified

Machine-readable schema content. The interpretation is selected by `schema/media-type`.

<a id="field-published-at"></a>
## `published-at`

- Required: `yes`
- Shape: string

Timestamp when this schema artifact was published.

<a id="field-author-node-id"></a>
## `author/node-id`

- Required: `yes`
- Shape: string

Node identity that publishes this schema artifact.

<a id="field-author-participant-id"></a>
## `author/participant-id`

- Required: `no`
- Shape: string

Optional participant identity responsible for authoring or approving this schema artifact.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation-local annotations that do not change core schema semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

Signature over the deterministic canonical form of this artifact with the top-level `signature` field omitted. The `schema/ref` still addresses only the canonical `content` value.
