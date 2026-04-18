# Sensorium Directive Result v1

Source schema: [`doc/schemas/sensorium-directive-result.v1.schema.json`](../../schemas/sensorium-directive-result.v1.schema.json)

Response envelope returned by sensorium-core to the consumer that submitted a sensorium-directive.v1. Always carries outcome/id (audit record reference) and observation/ids (empty when the directive produced no world-fact observations).

## Governing Basis

- [`doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`](../../project/40-proposals/045-sensorium-local-enaction-stratum.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-directive-result.v1` | Schema tag for the v1 Sensorium contract. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`directive/id`](#field-directive-id) | `yes` | string | Echo of the directive/id from the originating sensorium-directive.v1. |
| [`correlation/id`](#field-correlation-id) | `no` | string | Optional echo of the correlation/id from the directive, when present, so callers can confirm the response belongs to the expected workflow/thread without fetching the outcome record. |
| [`status`](#field-status) | `yes` | enum: `admitted`, `completed`, `failed`, `timed_out`, `rejected` | Final status for sync mode; initial status for async mode (typically admitted). rejected indicates the directive was refused at admission (policy, allowlist, or schema validation); in that case outcome/id is present and observation/ids is empty. |
| [`result`](#field-result) | `no` | unspecified | Typed per action_id. Shape defined by the allowlist entry's result_schema. Absent or null for rejected responses and admitted/async responses. |
| [`outcome/id`](#field-outcome-id) | `yes` | string | Identifier of the sensorium-directive-outcome.v1 audit record. Always present. Outcome records are audit-only and are NOT published to the local Agora bus; they are reachable only through host-owned audit capabilities. |
| [`observation/ids`](#field-observation-ids) | `yes` | array | List of linked sensorium-observation.v1 ids. Empty list means the directive produced no world-fact observations or has not completed yet in async mode. The outcome record is authoritative for the full list. |
| [`artifacts`](#field-artifacts) | `no` | array | References to artifacts produced by the directive (e.g. stdout, stderr, generated files) using the minimal artifact-lane contract from proposal 045. |
| [`diagnostics`](#field-diagnostics) | `no` | array | Optional diagnostic entries from the connector (warnings, soft errors). Not a replacement for the outcome record; these are hints to the caller. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifactRef`](#def-artifactref) | object | Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "status"
  ],
  "properties": {
    "status": {
      "enum": [
        "rejected",
        "admitted"
      ]
    }
  }
}
```

Then:

```json
{
  "properties": {
    "result": {
      "type": "null"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-directive-result.v1`

Schema tag for the v1 Sensorium contract.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-directive-id"></a>
## `directive/id`

- Required: `yes`
- Shape: string

Echo of the directive/id from the originating sensorium-directive.v1.

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

Optional echo of the correlation/id from the directive, when present, so callers can confirm the response belongs to the expected workflow/thread without fetching the outcome record.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `admitted`, `completed`, `failed`, `timed_out`, `rejected`

Final status for sync mode; initial status for async mode (typically admitted). rejected indicates the directive was refused at admission (policy, allowlist, or schema validation); in that case outcome/id is present and observation/ids is empty.

<a id="field-result"></a>
## `result`

- Required: `no`
- Shape: unspecified

Typed per action_id. Shape defined by the allowlist entry's result_schema. Absent or null for rejected responses and admitted/async responses.

<a id="field-outcome-id"></a>
## `outcome/id`

- Required: `yes`
- Shape: string

Identifier of the sensorium-directive-outcome.v1 audit record. Always present. Outcome records are audit-only and are NOT published to the local Agora bus; they are reachable only through host-owned audit capabilities.

<a id="field-observation-ids"></a>
## `observation/ids`

- Required: `yes`
- Shape: array

List of linked sensorium-observation.v1 ids. Empty list means the directive produced no world-fact observations or has not completed yet in async mode. The outcome record is authoritative for the full list.

<a id="field-artifacts"></a>
## `artifacts`

- Required: `no`
- Shape: array

References to artifacts produced by the directive (e.g. stdout, stderr, generated files) using the minimal artifact-lane contract from proposal 045.

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: array

Optional diagnostic entries from the connector (warnings, soft errors). Not a replacement for the outcome record; these are hints to the caller.

## Definition Semantics

<a id="def-artifactref"></a>
## `$defs.artifactRef`

- Shape: object

Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference.
