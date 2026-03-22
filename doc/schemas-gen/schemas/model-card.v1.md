# Model Card v1

Source schema: [`doc/schemas/model-card.v1.schema.json`](../../schemas/model-card.v1.schema.json)

Machine-readable schema for deployment-facing manifests describing intended use, exclusions, risks, and provenance of specialized adapters.

## Governing Basis

- [`doc/project/50-requirements/requirements-004.md`](../../project/50-requirements/requirements-004.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-002.md`](../../project/50-requirements/requirements-002.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)
- [`doc/project/50-requirements/requirements-004.md`](../../project/50-requirements/requirements-004.md)
- [`doc/project/50-requirements/requirements-005.md`](../../project/50-requirements/requirements-005.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-002.md`](../../project/30-stories/story-002.md)
- [`doc/project/30-stories/story-003.md`](../../project/30-stories/story-003.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`model-card/id`](#field-model-card-id) | `yes` | string | Stable identifier of the model card. |
| [`adapter/id`](#field-adapter-id) | `yes` | string | Adapter artifact described by this model card. |
| [`base-model/ref`](#field-base-model-ref) | `yes` | string | Immutable base model on top of which the adapter operates. |
| [`created-at`](#field-created-at) | `yes` | string | Creation timestamp of the model card. |
| [`deployment/scope`](#field-deployment-scope) | `yes` | enum: `private`, `federation-local`, `public` | Deployment visibility for which this card is valid. |
| [`intended-use`](#field-intended-use) | `yes` | string | Intended use domain or task family. |
| [`out-of-scope`](#field-out-of-scope) | `yes` | string | Use classes that are explicitly out of scope. |
| [`limitations`](#field-limitations) | `yes` | string | Known operational or epistemic limitations. |
| [`excluded-data-classes`](#field-excluded-data-classes) | `yes` | array | Data classes explicitly excluded from the training corpus or deployment use. |
| [`known-risks`](#field-known-risks) | `yes` | array | Known risks that operators and federations should keep visible. |
| [`evaluation/ref`](#field-evaluation-ref) | `yes` | string | Reference to the evaluation report that justifies publication or deployment. |
| [`provenance/refs`](#field-provenance-refs) | `yes` | array | References to source corpora, jobs, or governance decisions that justify the adapter. |
| [`maintainer/refs`](#field-maintainer-refs) | `no` | array | Maintainers or governors responsible for ongoing publication and revocation handling. |
| [`policy/profile`](#field-policy-profile) | `no` | string | Deployment or governance profile associated with the model card. |
| [`status`](#field-status) | `no` | enum: `draft`, `validated`, `published`, `deprecated` | Lifecycle state of the model card. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core model-card semantics. |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-model-card-id"></a>
## `model-card/id`

- Required: `yes`
- Shape: string

Stable identifier of the model card.

<a id="field-adapter-id"></a>
## `adapter/id`

- Required: `yes`
- Shape: string

Adapter artifact described by this model card.

<a id="field-base-model-ref"></a>
## `base-model/ref`

- Required: `yes`
- Shape: string

Immutable base model on top of which the adapter operates.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Creation timestamp of the model card.

<a id="field-deployment-scope"></a>
## `deployment/scope`

- Required: `yes`
- Shape: enum: `private`, `federation-local`, `public`

Deployment visibility for which this card is valid.

<a id="field-intended-use"></a>
## `intended-use`

- Required: `yes`
- Shape: string

Intended use domain or task family.

<a id="field-out-of-scope"></a>
## `out-of-scope`

- Required: `yes`
- Shape: string

Use classes that are explicitly out of scope.

<a id="field-limitations"></a>
## `limitations`

- Required: `yes`
- Shape: string

Known operational or epistemic limitations.

<a id="field-excluded-data-classes"></a>
## `excluded-data-classes`

- Required: `yes`
- Shape: array

Data classes explicitly excluded from the training corpus or deployment use.

<a id="field-known-risks"></a>
## `known-risks`

- Required: `yes`
- Shape: array

Known risks that operators and federations should keep visible.

<a id="field-evaluation-ref"></a>
## `evaluation/ref`

- Required: `yes`
- Shape: string

Reference to the evaluation report that justifies publication or deployment.

<a id="field-provenance-refs"></a>
## `provenance/refs`

- Required: `yes`
- Shape: array

References to source corpora, jobs, or governance decisions that justify the adapter.

<a id="field-maintainer-refs"></a>
## `maintainer/refs`

- Required: `no`
- Shape: array

Maintainers or governors responsible for ongoing publication and revocation handling.

<a id="field-policy-profile"></a>
## `policy/profile`

- Required: `no`
- Shape: string

Deployment or governance profile associated with the model card.

<a id="field-status"></a>
## `status`

- Required: `no`
- Shape: enum: `draft`, `validated`, `published`, `deprecated`

Lifecycle state of the model card.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core model-card semantics.
