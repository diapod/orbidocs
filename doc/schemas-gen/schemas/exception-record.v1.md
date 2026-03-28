# Exception Record v1

Source schema: [`doc/schemas/exception-record.v1.schema.json`](../../schemas/exception-record.v1.schema.json)

Machine-readable schema for a first-class audit record describing one bounded operational or constitutional exception. This contract follows the minimum exception data model from `EXCEPTION-POLICY` and stays general enough for ordinary, emergency, and injunction cases. Emergency-specific activation fields belong in a later extension artifact rather than in this base record.

## Governing Basis

- [`doc/normative/50-constitutional-ops/en/EXCEPTION-POLICY.en.md`](../../normative/50-constitutional-ops/en/EXCEPTION-POLICY.en.md)
- [`doc/normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md`](../../normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md)
- [`doc/project/20-memos/exception-record-v1-invariants.md`](../../project/20-memos/exception-record-v1-invariants.md)
- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`policy/id`](#field-policy-id) | `yes` | const: `DIA-EXC-001` | Normative policy anchor for this exception record family. |
| [`exception/id`](#field-exception-id) | `yes` | string | Stable exception identifier, e.g. `EXC-[federation]-[timestamp]-[nonce]`. |
| [`exception/type`](#field-exception-type) | `yes` | enum: `ordinary`, `emergency`, `injunction` | Exception family as defined by `EXCEPTION-POLICY`. |
| [`owner/kind`](#field-owner-kind) | `yes` | enum: `node`, `participant`, `org`, `council`, `panel`, `system`, `role` | Actor class that owns responsibility for the exception effects. |
| [`owner/id`](#field-owner-id) | `yes` | string | Identifier of the responsible owner. Canonical DID forms are used where available. |
| [`requester/kind`](#field-requester-kind) | `yes` | enum: `node`, `participant`, `org`, `council`, `panel`, `system`, `role` | Actor class that requested or initiated the exception. |
| [`requester/id`](#field-requester-id) | `yes` | string | Identifier of the initiator. Canonical DID forms are used where available. |
| [`scope/summary`](#field-scope-summary) | `yes` | string | What roles, resources, procedures, or data are covered by the exception. |
| [`reason/summary`](#field-reason-summary) | `yes` | string | Business, ethical, safety, or constitutional rationale for the exception. |
| [`risk/level`](#field-risk-level) | `yes` | enum: `low`, `medium`, `high`, `critical` | Risk class of the exception. High and critical records require non-empty approvals, monitoring metrics, and rollback conditions. |
| [`constitutional/basis`](#field-constitutional-basis) | `yes` | array | References to constitutional or normative clauses justifying the exception. |
| [`created/at`](#field-created-at) | `yes` | string | Timestamp when the exception record was created. |
| [`expires/at`](#field-expires-at) | `yes` | string | Expiry timestamp. Consumers SHOULD enforce `expires/at > created/at`. |
| [`fail-closed/target`](#field-fail-closed-target) | `yes` | string | Return state the system must enter when the exception ends or is revoked. |
| [`trigger/refs`](#field-trigger-refs) | `no` | array | Optional references to triggering signals, incidents, or cases that caused the exception to be opened. |
| [`approvals`](#field-approvals) | `yes` | array | Approval entries for the exception. High and critical records require at least one approval entry. |
| [`monitoring/metrics`](#field-monitoring-metrics) | `yes` | array | Side-effect indicators or health metrics to watch while the exception remains active. |
| [`monitoring/review-at`](#field-monitoring-review-at) | `yes` | string | Next mandatory review checkpoint. Consumers SHOULD enforce `monitoring/review-at >= created/at`. |
| [`rollback/conditions`](#field-rollback-conditions) | `yes` | array | Conditions under which the exception must be suspended or rolled back. |
| [`status`](#field-status) | `yes` | enum: `proposed`, `active`, `suspended`, `expired`, `rolled_back` | Lifecycle state of the exception record. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`approval`](#def-approval) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "node"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^node:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "participant"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^participant:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "org"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^org:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "council"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^council:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "system"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "const": "system"
    }
  }
}
```

### Rule 6

When:

```json
{
  "properties": {
    "requester/kind": {
      "const": "node"
    }
  },
  "required": [
    "requester/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "requester/id": {
      "pattern": "^node:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 7

When:

```json
{
  "properties": {
    "requester/kind": {
      "const": "participant"
    }
  },
  "required": [
    "requester/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "requester/id": {
      "pattern": "^participant:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 8

When:

```json
{
  "properties": {
    "requester/kind": {
      "const": "org"
    }
  },
  "required": [
    "requester/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "requester/id": {
      "pattern": "^org:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 9

When:

```json
{
  "properties": {
    "requester/kind": {
      "const": "council"
    }
  },
  "required": [
    "requester/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "requester/id": {
      "pattern": "^council:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 10

When:

```json
{
  "properties": {
    "requester/kind": {
      "const": "system"
    }
  },
  "required": [
    "requester/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "requester/id": {
      "const": "system"
    }
  }
}
```

### Rule 11

When:

```json
{
  "properties": {
    "risk/level": {
      "enum": [
        "high",
        "critical"
      ]
    }
  },
  "required": [
    "risk/level"
  ]
}
```

Then:

```json
{
  "properties": {
    "approvals": {
      "minItems": 1
    },
    "monitoring/metrics": {
      "minItems": 1
    },
    "rollback/conditions": {
      "minItems": 1
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

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: const: `DIA-EXC-001`

Normative policy anchor for this exception record family.

<a id="field-exception-id"></a>
## `exception/id`

- Required: `yes`
- Shape: string

Stable exception identifier, e.g. `EXC-[federation]-[timestamp]-[nonce]`.

<a id="field-exception-type"></a>
## `exception/type`

- Required: `yes`
- Shape: enum: `ordinary`, `emergency`, `injunction`

Exception family as defined by `EXCEPTION-POLICY`.

<a id="field-owner-kind"></a>
## `owner/kind`

- Required: `yes`
- Shape: enum: `node`, `participant`, `org`, `council`, `panel`, `system`, `role`

Actor class that owns responsibility for the exception effects.

<a id="field-owner-id"></a>
## `owner/id`

- Required: `yes`
- Shape: string

Identifier of the responsible owner. Canonical DID forms are used where available.

<a id="field-requester-kind"></a>
## `requester/kind`

- Required: `yes`
- Shape: enum: `node`, `participant`, `org`, `council`, `panel`, `system`, `role`

Actor class that requested or initiated the exception.

<a id="field-requester-id"></a>
## `requester/id`

- Required: `yes`
- Shape: string

Identifier of the initiator. Canonical DID forms are used where available.

<a id="field-scope-summary"></a>
## `scope/summary`

- Required: `yes`
- Shape: string

What roles, resources, procedures, or data are covered by the exception.

<a id="field-reason-summary"></a>
## `reason/summary`

- Required: `yes`
- Shape: string

Business, ethical, safety, or constitutional rationale for the exception.

<a id="field-risk-level"></a>
## `risk/level`

- Required: `yes`
- Shape: enum: `low`, `medium`, `high`, `critical`

Risk class of the exception. High and critical records require non-empty approvals, monitoring metrics, and rollback conditions.

<a id="field-constitutional-basis"></a>
## `constitutional/basis`

- Required: `yes`
- Shape: array

References to constitutional or normative clauses justifying the exception.

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

Timestamp when the exception record was created.

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

Expiry timestamp. Consumers SHOULD enforce `expires/at > created/at`.

<a id="field-fail-closed-target"></a>
## `fail-closed/target`

- Required: `yes`
- Shape: string

Return state the system must enter when the exception ends or is revoked.

<a id="field-trigger-refs"></a>
## `trigger/refs`

- Required: `no`
- Shape: array

Optional references to triggering signals, incidents, or cases that caused the exception to be opened.

<a id="field-approvals"></a>
## `approvals`

- Required: `yes`
- Shape: array

Approval entries for the exception. High and critical records require at least one approval entry.

<a id="field-monitoring-metrics"></a>
## `monitoring/metrics`

- Required: `yes`
- Shape: array

Side-effect indicators or health metrics to watch while the exception remains active.

<a id="field-monitoring-review-at"></a>
## `monitoring/review-at`

- Required: `yes`
- Shape: string

Next mandatory review checkpoint. Consumers SHOULD enforce `monitoring/review-at >= created/at`.

<a id="field-rollback-conditions"></a>
## `rollback/conditions`

- Required: `yes`
- Shape: array

Conditions under which the exception must be suspended or rolled back.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `proposed`, `active`, `suspended`, `expired`, `rolled_back`

Lifecycle state of the exception record.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

## Definition Semantics

<a id="def-approval"></a>
## `$defs.approval`

- Shape: object
