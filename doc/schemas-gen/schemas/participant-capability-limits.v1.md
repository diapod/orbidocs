# Participant Capability Limits v1

Source schema: [`doc/schemas/participant-capability-limits.v1.schema.json`](../../schemas/participant-capability-limits.v1.schema.json)

Machine-readable schema for a participant-scoped layered restriction state. The record freezes always-on soft degradation knobs and optional hard blocked operations without collapsing the participant into transport-layer peer quality or permanent exclusion.

## Governing Basis

- [`doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`](../../project/40-proposals/018-layered-capability-limited-participant-restrictions.md)
- [`doc/project/50-requirements/requirements-009.md`](../../project/50-requirements/requirements-009.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-009.md`](../../project/50-requirements/requirements-009.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`participant/id`](#field-participant-id) | `yes` | string | Canonical participant subject to which the restriction state applies. |
| [`recorded-at`](#field-recorded-at) | `yes` | string | Timestamp when this restriction state was recorded. |
| [`status`](#field-status) | `yes` | const: `capability_limited` | Frozen MVP state label for layered degraded participation. |
| [`soft`](#field-soft) | `yes` | ref: `#/$defs/soft` |  |
| [`hard`](#field-hard) | `no` | ref: `#/$defs/hard` |  |
| [`notes`](#field-notes) | `no` | string | Optional human-readable explanation. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`soft`](#def-soft) | object |  |
| [`hard`](#def-hard) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-participant-id"></a>
## `participant/id`

- Required: `yes`
- Shape: string

Canonical participant subject to which the restriction state applies.

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

Timestamp when this restriction state was recorded.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `capability_limited`

Frozen MVP state label for layered degraded participation.

<a id="field-soft"></a>
## `soft`

- Required: `yes`
- Shape: ref: `#/$defs/soft`

<a id="field-hard"></a>
## `hard`

- Required: `no`
- Shape: ref: `#/$defs/hard`

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable explanation.

## Definition Semantics

<a id="def-soft"></a>
## `$defs.soft`

- Shape: object

<a id="def-hard"></a>
## `$defs.hard`

- Shape: object
