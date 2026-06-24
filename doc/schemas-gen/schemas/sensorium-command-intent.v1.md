# Sensorium Command Intent v1

Source schema: [`doc/schemas/sensorium-command-intent.v1.schema.json`](../../schemas/sensorium-command-intent.v1.schema.json)

Caller-supplied command intent after host policy/model merge. The intent carries argv as data, never a raw shell string.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-command-intent.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`command/id`](#field-command-id) | `no` | ref: `#/$defs/ref` | Optional command identity. The host assigns it when missing and preserves it when present and valid, so terminal-command records keep correlation identity. |
| [`command.profile/ref`](#field-command-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`argv`](#field-argv) | `yes` | array |  |
| [`cwd`](#field-cwd) | `yes` | ref: `sensorium-relative-path-address.v1.schema.json` |  |
| [`env`](#field-env) | `no` | object |  |
| [`timeout_ms`](#field-timeout-ms) | `no` | integer |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`argvAtom`](#def-argvatom) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-command-intent.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-command-id"></a>
## `command/id`

- Required: `no`
- Shape: ref: `#/$defs/ref`

Optional command identity. The host assigns it when missing and preserves it when present and valid, so terminal-command records keep correlation identity.

<a id="field-command-profile-ref"></a>
## `command.profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-argv"></a>
## `argv`

- Required: `yes`
- Shape: array

<a id="field-cwd"></a>
## `cwd`

- Required: `yes`
- Shape: ref: `sensorium-relative-path-address.v1.schema.json`

<a id="field-env"></a>
## `env`

- Required: `no`
- Shape: object

<a id="field-timeout-ms"></a>
## `timeout_ms`

- Required: `no`
- Shape: integer

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-argvatom"></a>
## `$defs.argvAtom`

- Shape: string
