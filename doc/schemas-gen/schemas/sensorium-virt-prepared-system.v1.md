# Sensorium Virt Prepared System v1

Source schema: [`doc/schemas/sensorium-virt-prepared-system.v1.schema.json`](../../schemas/sensorium-virt-prepared-system.v1.schema.json)

Closed, content-bound state an image builder writes into a guest beyond its base image: files pinned by the digest of their bytes, paths that must be absent, and bounded claims for verifiers. Its content address is the SHA-256 over JCS v1 of the whole document, which an image manifest binds as `prepared-system/digest`. The shape is the one builder tooling already reads, so it carries no `schema/v`.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-virt-prepared-system.v1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | string |  |
| [`files`](#field-files) | `yes` | array |  |
| [`absent/paths`](#field-absent-paths) | `yes` | array |  |
| [`claims`](#field-claims) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`guestPath`](#def-guestpath) | string | Absolute, normalized guest path: no empty, `.` or `..` component. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-virt-prepared-system.v1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: string

<a id="field-files"></a>
## `files`

- Required: `yes`
- Shape: array

<a id="field-absent-paths"></a>
## `absent/paths`

- Required: `yes`
- Shape: array

<a id="field-claims"></a>
## `claims`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-guestpath"></a>
## `$defs.guestPath`

- Shape: string

Absolute, normalized guest path: no empty, `.` or `..` component.
