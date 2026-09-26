# Sensorium Patch Policy v1

Source schema: [`doc/schemas/sensorium-patch-policy.v1.schema.json`](../../schemas/sensorium-patch-policy.v1.schema.json)

Closed, content-addressable admission policy for Workbench patches. It names every admitted target by a logical root and a relative path, the admitted change operations, and a line-oriented content shape. It does not apply patches; the Workbench enforces it before staging.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md`](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-patch-policy.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`patch-policy/ref`](#field-patch-policy-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`targets`](#field-targets) | `yes` | array |  |
| [`patch/max-bytes`](#field-patch-max-bytes) | `yes` | integer |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`relativePath`](#def-relativepath) | string | Relative path below the logical root: components of `[A-Za-z0-9._-]` separated by single slashes, with no leading slash and no `.` or `..` component. A leading dot is admitted (for example `alias/.qmail-root`); globs, backslashes and whitespace are not. |
| [`target`](#def-target) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-patch-policy.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-patch-policy-ref"></a>
## `patch-policy/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-targets"></a>
## `targets`

- Required: `yes`
- Shape: array

<a id="field-patch-max-bytes"></a>
## `patch/max-bytes`

- Required: `yes`
- Shape: integer

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string

Relative path below the logical root: components of `[A-Za-z0-9._-]` separated by single slashes, with no leading slash and no `.` or `..` component. A leading dot is admitted (for example `alias/.qmail-root`); globs, backslashes and whitespace are not.

<a id="def-target"></a>
## `$defs.target`

- Shape: object
