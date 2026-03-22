# Retrieval Response v1

Source schema: [`doc/schemas/retrieval-response.v1.schema.json`](../../schemas/retrieval-response.v1.schema.json)

Machine-readable schema for archivist or vault responses to retrieval requests.

## Governing Basis

- [`doc/project/30-stories/story-003.md`](../../project/30-stories/story-003.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)
- [`doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`](../../project/40-proposals/012-learning-outcomes-and-archival-contracts.md)

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
| [`request/id`](#field-request-id) | `yes` | string | Retrieval request identifier being answered. |
| [`responded-at`](#field-responded-at) | `yes` | string | Response timestamp. |
| [`responder/node-id`](#field-responder-node-id) | `yes` | string | Archivist or gateway node that answered the retrieval request. |
| [`status`](#field-status) | `yes` | enum: `found`, `denied`, `unavailable`, `tombstoned` | Top-level retrieval result. |
| [`package/id`](#field-package-id) | `no` | string | Archival package identifier returned on successful retrieval. |
| [`artifact/id`](#field-artifact-id) | `no` | string | Artifact identifier returned on successful retrieval. |
| [`publication/scope`](#field-publication-scope) | `no` | enum: `private-retained`, `federation-vault`, `public-vault` | Scope under which the returned artifact is exposed. |
| [`payload/ref`](#field-payload-ref) | `no` | string | Stable content or blob reference returned to the requester. |
| [`integrity/proof`](#field-integrity-proof) | `no` | ref: `#/$defs/integrityProof` |  |
| [`reason/code`](#field-reason-code) | `no` | string | Short machine-readable reason for non-successful retrieval. |
| [`reason/text`](#field-reason-text) | `no` | string | Optional human-readable explanation of denial or unavailability. |
| [`expires-at`](#field-expires-at) | `no` | string | Optional expiry timestamp of the returned retrieval grant or link. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core retrieval semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`integrityProof`](#def-integrityproof) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "found"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "package/id",
    "artifact/id",
    "publication/scope",
    "payload/ref",
    "integrity/proof"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "denied",
        "unavailable",
        "tombstoned"
      ]
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "reason/code"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

Retrieval request identifier being answered.

<a id="field-responded-at"></a>
## `responded-at`

- Required: `yes`
- Shape: string

Response timestamp.

<a id="field-responder-node-id"></a>
## `responder/node-id`

- Required: `yes`
- Shape: string

Archivist or gateway node that answered the retrieval request.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `found`, `denied`, `unavailable`, `tombstoned`

Top-level retrieval result.

<a id="field-package-id"></a>
## `package/id`

- Required: `no`
- Shape: string

Archival package identifier returned on successful retrieval.

<a id="field-artifact-id"></a>
## `artifact/id`

- Required: `no`
- Shape: string

Artifact identifier returned on successful retrieval.

<a id="field-publication-scope"></a>
## `publication/scope`

- Required: `no`
- Shape: enum: `private-retained`, `federation-vault`, `public-vault`

Scope under which the returned artifact is exposed.

<a id="field-payload-ref"></a>
## `payload/ref`

- Required: `no`
- Shape: string

Stable content or blob reference returned to the requester.

<a id="field-integrity-proof"></a>
## `integrity/proof`

- Required: `no`
- Shape: ref: `#/$defs/integrityProof`

<a id="field-reason-code"></a>
## `reason/code`

- Required: `no`
- Shape: string

Short machine-readable reason for non-successful retrieval.

<a id="field-reason-text"></a>
## `reason/text`

- Required: `no`
- Shape: string

Optional human-readable explanation of denial or unavailability.

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

Optional expiry timestamp of the returned retrieval grant or link.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core retrieval semantics.

## Definition Semantics

<a id="def-integrityproof"></a>
## `$defs.integrityProof`

- Shape: object
