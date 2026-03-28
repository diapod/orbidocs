# Emergency Activation v1

Source schema: [`doc/schemas/emergency-activation.v1.schema.json`](../../schemas/emergency-activation.v1.schema.json)

Machine-readable schema for one emergency activation decision layered over an existing `exception-record.v1`. This artifact carries trigger selection, credibility, activation path, TTL ceilings, agent elevation, deactivation, and post-crisis review state.

## Governing Basis

- [`doc/normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md`](../../normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md)
- [`doc/normative/50-constitutional-ops/en/EXCEPTION-POLICY.en.md`](../../normative/50-constitutional-ops/en/EXCEPTION-POLICY.en.md)
- [`doc/project/20-memos/emergency-activation-v1-invariants.md`](../../project/20-memos/emergency-activation-v1-invariants.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`exception/id`](#field-exception-id) | `yes` | string | Identifier of the already-created `exception-record.v1` associated with this activation cycle. |
| [`exception/type`](#field-exception-type) | `yes` | const: `emergency` | Emergency activations always extend an emergency exception. |
| [`trigger/class`](#field-trigger-class) | `yes` | enum: `TC1`, `TC2`, `TC3`, `TC4`, `TC5` | Trigger class that justified activation. |
| [`trigger/signal-refs`](#field-trigger-signal-refs) | `yes` | array | Emergency signal ids that justified the activation. |
| [`credibility/class`](#field-credibility-class) | `yes` | enum: `C0`, `C1`, `C2`, `C3`, `C4` | Credibility class used at the moment of activation. |
| [`activation/path`](#field-activation-path) | `yes` | enum: `automatic`, `manual`, `escalation_auto` | How the activation entered force. |
| [`activated-by/kind`](#field-activated-by-kind) | `yes` | enum: `node`, `system` | Activator identity class. |
| [`activated-by/id`](#field-activated-by-id) | `yes` | string | Activator identifier. `node` uses canonical `node:did:key:...`; `system` uses literal `system`. |
| [`activated/at`](#field-activated-at) | `yes` | string | Timestamp when the activation entered force. |
| [`ttl/expires-at`](#field-ttl-expires-at) | `yes` | string | Current TTL deadline of the activation. Consumers SHOULD enforce `ttl/expires-at > activated/at`. |
| [`max-extension/until`](#field-max-extension-until) | `yes` | string | Absolute extension ceiling for the activation. Consumers SHOULD enforce `max-extension/until >= ttl/expires-at`. |
| [`extensions`](#field-extensions) | `yes` | array | Recorded TTL extensions for this activation cycle. |
| [`agents/elevated`](#field-agents-elevated) | `yes` | array | Identifiers of agents elevated to A3 or equivalent emergency mode. TC5 may keep this empty. |
| [`scope/summary`](#field-scope-summary) | `yes` | string | Operational scope covered by this activation. |
| [`fail-closed/target`](#field-fail-closed-target) | `yes` | string | Return state after TTL expiry or manual deactivation. |
| [`deactivated/at`](#field-deactivated-at) | `no` | string | Timestamp when the activation was deactivated. |
| [`deactivation/reason`](#field-deactivation-reason) | `no` | enum: `ttl_expired`, `operator_deactivated`, `threat_resolved`, `superseded` | Reason why the activation stopped being active. |
| [`review/due-at`](#field-review-due-at) | `no` | string | Mandatory post-crisis review deadline. Consumers SHOULD enforce `review/due-at >= deactivated/at` when deactivation exists. |
| [`review/status`](#field-review-status) | `yes` | enum: `pending`, `in_progress`, `completed` | Status of the post-crisis review. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`extension`](#def-extension) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "activated-by/kind": {
      "const": "node"
    }
  },
  "required": [
    "activated-by/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "activated-by/id": {
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
    "activated-by/kind": {
      "const": "system"
    }
  },
  "required": [
    "activated-by/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "activated-by/id": {
      "const": "system"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "trigger/class": {
      "enum": [
        "TC1",
        "TC2",
        "TC3",
        "TC4"
      ]
    }
  },
  "required": [
    "trigger/class"
  ]
}
```

Then:

```json
{
  "properties": {
    "agents/elevated": {
      "minItems": 1
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "trigger/class": {
      "const": "TC5"
    }
  },
  "required": [
    "trigger/class"
  ]
}
```

Then:

```json
{
  "properties": {
    "agents/elevated": {
      "maxItems": 0
    }
  }
}
```

### Rule 5

When:

```json
{
  "required": [
    "deactivated/at"
  ]
}
```

Then:

```json
{
  "required": [
    "deactivation/reason",
    "review/due-at"
  ],
  "properties": {
    "review/status": {
      "enum": [
        "pending",
        "in_progress",
        "completed"
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

<a id="field-exception-id"></a>
## `exception/id`

- Required: `yes`
- Shape: string

Identifier of the already-created `exception-record.v1` associated with this activation cycle.

<a id="field-exception-type"></a>
## `exception/type`

- Required: `yes`
- Shape: const: `emergency`

Emergency activations always extend an emergency exception.

<a id="field-trigger-class"></a>
## `trigger/class`

- Required: `yes`
- Shape: enum: `TC1`, `TC2`, `TC3`, `TC4`, `TC5`

Trigger class that justified activation.

<a id="field-trigger-signal-refs"></a>
## `trigger/signal-refs`

- Required: `yes`
- Shape: array

Emergency signal ids that justified the activation.

<a id="field-credibility-class"></a>
## `credibility/class`

- Required: `yes`
- Shape: enum: `C0`, `C1`, `C2`, `C3`, `C4`

Credibility class used at the moment of activation.

<a id="field-activation-path"></a>
## `activation/path`

- Required: `yes`
- Shape: enum: `automatic`, `manual`, `escalation_auto`

How the activation entered force.

<a id="field-activated-by-kind"></a>
## `activated-by/kind`

- Required: `yes`
- Shape: enum: `node`, `system`

Activator identity class.

<a id="field-activated-by-id"></a>
## `activated-by/id`

- Required: `yes`
- Shape: string

Activator identifier. `node` uses canonical `node:did:key:...`; `system` uses literal `system`.

<a id="field-activated-at"></a>
## `activated/at`

- Required: `yes`
- Shape: string

Timestamp when the activation entered force.

<a id="field-ttl-expires-at"></a>
## `ttl/expires-at`

- Required: `yes`
- Shape: string

Current TTL deadline of the activation. Consumers SHOULD enforce `ttl/expires-at > activated/at`.

<a id="field-max-extension-until"></a>
## `max-extension/until`

- Required: `yes`
- Shape: string

Absolute extension ceiling for the activation. Consumers SHOULD enforce `max-extension/until >= ttl/expires-at`.

<a id="field-extensions"></a>
## `extensions`

- Required: `yes`
- Shape: array

Recorded TTL extensions for this activation cycle.

<a id="field-agents-elevated"></a>
## `agents/elevated`

- Required: `yes`
- Shape: array

Identifiers of agents elevated to A3 or equivalent emergency mode. TC5 may keep this empty.

<a id="field-scope-summary"></a>
## `scope/summary`

- Required: `yes`
- Shape: string

Operational scope covered by this activation.

<a id="field-fail-closed-target"></a>
## `fail-closed/target`

- Required: `yes`
- Shape: string

Return state after TTL expiry or manual deactivation.

<a id="field-deactivated-at"></a>
## `deactivated/at`

- Required: `no`
- Shape: string

Timestamp when the activation was deactivated.

<a id="field-deactivation-reason"></a>
## `deactivation/reason`

- Required: `no`
- Shape: enum: `ttl_expired`, `operator_deactivated`, `threat_resolved`, `superseded`

Reason why the activation stopped being active.

<a id="field-review-due-at"></a>
## `review/due-at`

- Required: `no`
- Shape: string

Mandatory post-crisis review deadline. Consumers SHOULD enforce `review/due-at >= deactivated/at` when deactivation exists.

<a id="field-review-status"></a>
## `review/status`

- Required: `yes`
- Shape: enum: `pending`, `in_progress`, `completed`

Status of the post-crisis review.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

## Definition Semantics

<a id="def-extension"></a>
## `$defs.extension`

- Shape: object
