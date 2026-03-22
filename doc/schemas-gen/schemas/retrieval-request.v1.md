# Retrieval Request v1

Source schema: [`doc/schemas/retrieval-request.v1.schema.json`](../../schemas/retrieval-request.v1.schema.json)

Machine-readable schema for scope-aware retrieval of archived artifacts.

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
| [`request/id`](#field-request-id) | `yes` | string | Stable retrieval request identifier. |
| [`requested-at`](#field-requested-at) | `yes` | string | Timestamp of the retrieval attempt. |
| [`requester/node-id`](#field-requester-node-id) | `yes` | string | Node or gateway actor requesting access. |
| [`package/id`](#field-package-id) | `no` | string | Requested archival package identifier. |
| [`artifact/id`](#field-artifact-id) | `no` | string | Requested artifact identifier when package id is not known. |
| [`access/scope`](#field-access-scope) | `yes` | enum: `private-retained`, `federation-vault`, `public-vault` | Scope under which the requester expects the retrieval to be authorized. |
| [`authorization/basis`](#field-authorization-basis) | `yes` | enum: `local-owner`, `federation-policy`, `public-access`, `curator-review`, `audit` | Reason why the requester believes access is allowed. |
| [`retrieval/purpose`](#field-retrieval-purpose) | `yes` | enum: `local-recovery`, `serving`, `curation`, `training`, `audit`, `replay` | Declared purpose of retrieval. |
| [`proof/context-ref`](#field-proof-context-ref) | `no` | string | Optional external proof or audit context reference. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core retrieval semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "access/scope": {
      "const": "private-retained"
    }
  },
  "required": [
    "access/scope"
  ]
}
```

Then:

```json
{
  "properties": {
    "authorization/basis": {
      "enum": [
        "local-owner",
        "curator-review",
        "audit"
      ]
    }
  }
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

Stable retrieval request identifier.

<a id="field-requested-at"></a>
## `requested-at`

- Required: `yes`
- Shape: string

Timestamp of the retrieval attempt.

<a id="field-requester-node-id"></a>
## `requester/node-id`

- Required: `yes`
- Shape: string

Node or gateway actor requesting access.

<a id="field-package-id"></a>
## `package/id`

- Required: `no`
- Shape: string

Requested archival package identifier.

<a id="field-artifact-id"></a>
## `artifact/id`

- Required: `no`
- Shape: string

Requested artifact identifier when package id is not known.

<a id="field-access-scope"></a>
## `access/scope`

- Required: `yes`
- Shape: enum: `private-retained`, `federation-vault`, `public-vault`

Scope under which the requester expects the retrieval to be authorized.

<a id="field-authorization-basis"></a>
## `authorization/basis`

- Required: `yes`
- Shape: enum: `local-owner`, `federation-policy`, `public-access`, `curator-review`, `audit`

Reason why the requester believes access is allowed.

<a id="field-retrieval-purpose"></a>
## `retrieval/purpose`

- Required: `yes`
- Shape: enum: `local-recovery`, `serving`, `curation`, `training`, `audit`, `replay`

Declared purpose of retrieval.

<a id="field-proof-context-ref"></a>
## `proof/context-ref`

- Required: `no`
- Shape: string

Optional external proof or audit context reference.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core retrieval semantics.
