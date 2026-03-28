# Emergency Signal v1

Source schema: [`doc/schemas/emergency-signal.v1.schema.json`](../../schemas/emergency-signal.v1.schema.json)

Machine-readable schema for one emergency-ingest fact entering the crisis evaluation pipeline. This contract models a reporting signal, not an activation decision. It stays below `emergency-activation.v1` and above raw connector telemetry.

## Governing Basis

- [`doc/normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md`](../../normative/50-constitutional-ops/en/EMERGENCY-ACTIVATION-CRITERIA.en.md)
- [`doc/project/20-memos/emergency-signal-v1-invariants.md`](../../project/20-memos/emergency-signal-v1-invariants.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`signal/id`](#field-signal-id) | `yes` | string | Stable identifier of the emergency signal. |
| [`source/node-id`](#field-source-node-id) | `yes` | string | Canonical identity of the reporting node. |
| [`source/type`](#field-source-type) | `yes` | enum: `sensorium`, `operator`, `peer_report`, `oracle` | Source class of the emergency signal. |
| [`observed/at`](#field-observed-at) | `yes` | string | Timestamp when the signal was observed or emitted. |
| [`trigger/class`](#field-trigger-class) | `yes` | enum: `TC1`, `TC2`, `TC3`, `TC4`, `TC5` | Emergency trigger class from `EMERGENCY-ACTIVATION-CRITERIA`. |
| [`description`](#field-description) | `yes` | string | Human-readable summary of the observed condition. |
| [`evidence/ref`](#field-evidence-ref) | `yes` | string | Reference to auditable evidence backing the signal. |
| [`confidence/class`](#field-confidence-class) | `yes` | enum: `C0`, `C1`, `C2`, `C3`, `C4` | Credibility class of the observed signal. |
| [`corroborating/signal-refs`](#field-corroborating-signal-refs) | `yes` | array | References to other signals that corroborate the current one. |
| [`tc5/active`](#field-tc5-active) | `yes` | boolean | Whether degraded-trust mode is active for this signal. |
| [`metadata/geo-hint`](#field-metadata-geo-hint) | `no` | string | Optional coarse location hint. |
| [`metadata/affected-scope`](#field-metadata-affected-scope) | `yes` | enum: `node`, `federation`, `inter-federation` | Operational scope affected by the reported condition. |
| [`metadata/urgency`](#field-metadata-urgency) | `yes` | enum: `immediate`, `hours`, `days` | Expected time pressure of the condition. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |

## Conditional Rules

### Rule 1

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
    "tc5/active": {
      "const": true
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "tc5/active": {
      "const": true
    }
  },
  "required": [
    "tc5/active"
  ]
}
```

Then:

```json
{
  "properties": {
    "trigger/class": {
      "const": "TC5"
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

<a id="field-signal-id"></a>
## `signal/id`

- Required: `yes`
- Shape: string

Stable identifier of the emergency signal.

<a id="field-source-node-id"></a>
## `source/node-id`

- Required: `yes`
- Shape: string

Canonical identity of the reporting node.

<a id="field-source-type"></a>
## `source/type`

- Required: `yes`
- Shape: enum: `sensorium`, `operator`, `peer_report`, `oracle`

Source class of the emergency signal.

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

Timestamp when the signal was observed or emitted.

<a id="field-trigger-class"></a>
## `trigger/class`

- Required: `yes`
- Shape: enum: `TC1`, `TC2`, `TC3`, `TC4`, `TC5`

Emergency trigger class from `EMERGENCY-ACTIVATION-CRITERIA`.

<a id="field-description"></a>
## `description`

- Required: `yes`
- Shape: string

Human-readable summary of the observed condition.

<a id="field-evidence-ref"></a>
## `evidence/ref`

- Required: `yes`
- Shape: string

Reference to auditable evidence backing the signal.

<a id="field-confidence-class"></a>
## `confidence/class`

- Required: `yes`
- Shape: enum: `C0`, `C1`, `C2`, `C3`, `C4`

Credibility class of the observed signal.

<a id="field-corroborating-signal-refs"></a>
## `corroborating/signal-refs`

- Required: `yes`
- Shape: array

References to other signals that corroborate the current one.

<a id="field-tc5-active"></a>
## `tc5/active`

- Required: `yes`
- Shape: boolean

Whether degraded-trust mode is active for this signal.

<a id="field-metadata-geo-hint"></a>
## `metadata/geo-hint`

- Required: `no`
- Shape: string

Optional coarse location hint.

<a id="field-metadata-affected-scope"></a>
## `metadata/affected-scope`

- Required: `yes`
- Shape: enum: `node`, `federation`, `inter-federation`

Operational scope affected by the reported condition.

<a id="field-metadata-urgency"></a>
## `metadata/urgency`

- Required: `yes`
- Shape: enum: `immediate`, `hours`, `days`

Expected time pressure of the condition.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.
