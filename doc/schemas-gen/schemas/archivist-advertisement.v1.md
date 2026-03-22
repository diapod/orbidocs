# Archivist Advertisement v1

Source schema: [`doc/schemas/archivist-advertisement.v1.schema.json`](../../schemas/archivist-advertisement.v1.schema.json)

Machine-readable schema for archivist capability advertisements covering archival scope, retention posture, and optional settlement requirements.

## Governing Basis

- [`doc/project/30-stories/story-003.md`](../../project/30-stories/story-003.md)
- [`doc/project/50-requirements/requirements-003.md`](../../project/50-requirements/requirements-003.md)
- [`doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`](../../project/40-proposals/008-transcription-monitors-and-public-vaults.md)
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
| [`advertisement/id`](#field-advertisement-id) | `yes` | string | Stable identifier of the archivist capability advertisement. |
| [`created-at`](#field-created-at) | `yes` | string | Advertisement publication timestamp. |
| [`archivist/node-id`](#field-archivist-node-id) | `yes` | string | Archivist node or durable storage actor. |
| [`accepted/scopes`](#field-accepted-scopes) | `yes` | array | Publication scopes this archivist is willing to accept. |
| [`accepted/artifact-types`](#field-accepted-artifact-types) | `yes` | array | Artifact classes this archivist accepts. |
| [`retrieval/mode`](#field-retrieval-mode) | `yes` | enum: `direct-only`, `federation-discovery`, `public-discovery` | Primary discovery or retrieval mode exposed by the archivist. |
| [`retention/default-max-duration-sec`](#field-retention-default-max-duration-sec) | `no` | integer | Default maximum storage duration when no explicit contract overrides it. |
| [`retention/default-max-idle-ttl-sec`](#field-retention-default-max-idle-ttl-sec) | `no` | integer | Default maximum idle TTL when no explicit contract overrides it. |
| [`replication/max-copies`](#field-replication-max-copies) | `no` | integer | Maximum replication copies this archivist is willing to coordinate. |
| [`publication/timing-profiles`](#field-publication-timing-profiles) | `no` | array | Publication timing profiles the archivist supports. |
| [`settlement/required`](#field-settlement-required) | `yes` | boolean | Whether this archivist requires explicit negotiated settlement for storage. |
| [`settlement/rail-hints`](#field-settlement-rail-hints) | `no` | array | Optional settlement rail hints when negotiated storage is required. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional implementation-local annotations that do not change the core advertisement semantics. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "settlement/required": {
      "const": true
    }
  },
  "required": [
    "settlement/required"
  ]
}
```

Then:

```json
{
  "required": [
    "settlement/rail-hints"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-advertisement-id"></a>
## `advertisement/id`

- Required: `yes`
- Shape: string

Stable identifier of the archivist capability advertisement.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Advertisement publication timestamp.

<a id="field-archivist-node-id"></a>
## `archivist/node-id`

- Required: `yes`
- Shape: string

Archivist node or durable storage actor.

<a id="field-accepted-scopes"></a>
## `accepted/scopes`

- Required: `yes`
- Shape: array

Publication scopes this archivist is willing to accept.

<a id="field-accepted-artifact-types"></a>
## `accepted/artifact-types`

- Required: `yes`
- Shape: array

Artifact classes this archivist accepts.

<a id="field-retrieval-mode"></a>
## `retrieval/mode`

- Required: `yes`
- Shape: enum: `direct-only`, `federation-discovery`, `public-discovery`

Primary discovery or retrieval mode exposed by the archivist.

<a id="field-retention-default-max-duration-sec"></a>
## `retention/default-max-duration-sec`

- Required: `no`
- Shape: integer

Default maximum storage duration when no explicit contract overrides it.

<a id="field-retention-default-max-idle-ttl-sec"></a>
## `retention/default-max-idle-ttl-sec`

- Required: `no`
- Shape: integer

Default maximum idle TTL when no explicit contract overrides it.

<a id="field-replication-max-copies"></a>
## `replication/max-copies`

- Required: `no`
- Shape: integer

Maximum replication copies this archivist is willing to coordinate.

<a id="field-publication-timing-profiles"></a>
## `publication/timing-profiles`

- Required: `no`
- Shape: array

Publication timing profiles the archivist supports.

<a id="field-settlement-required"></a>
## `settlement/required`

- Required: `yes`
- Shape: boolean

Whether this archivist requires explicit negotiated settlement for storage.

<a id="field-settlement-rail-hints"></a>
## `settlement/rail-hints`

- Required: `no`
- Shape: array

Optional settlement rail hints when negotiated storage is required.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional implementation-local annotations that do not change the core advertisement semantics.
