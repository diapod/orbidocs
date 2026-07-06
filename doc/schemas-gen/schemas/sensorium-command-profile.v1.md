# Sensorium Command Profile v1

Source schema: [`doc/schemas/sensorium-command-profile.v1.schema.json`](../../schemas/sensorium-command-profile.v1.schema.json)

Declarative command profile for local Sensorium actuation. The profile describes argv-as-data admission, cwd roots, env policy, and bounded output/timeout limits; it does not execute commands.

## Governing Basis

- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)
- [`doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`](../../project/40-proposals/048-sensorium-os-connector-action-classes.md)

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-command-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`command.profile/ref`](#field-command-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`executable`](#field-executable) | `yes` | ref: `#/$defs/argvAtom` |  |
| [`fixed_args`](#field-fixed-args) | `no` | array |  |
| [`allowed_arg_prefixes`](#field-allowed-arg-prefixes) | `no` | array | Allowed prefixes for variable argv atoms after executable and fixed_args. An empty list means no variable argv atoms are allowed. |
| [`allowed_workspace_roots`](#field-allowed-workspace-roots) | `yes` | array | Explicit allowlist of workspace root refs. The list is required to be non-empty; filesystem authority is default-deny. |
| [`env`](#field-env) | `yes` | ref: `#/$defs/envPolicy` |  |
| [`network`](#field-network) | `no` | ref: `#/$defs/networkPolicy` | Profile-level network policy. The Workbench hard-MVP contract admits only no-egress/local-only policy values; any future egress grant must use a separate capability contract. |
| [`limits`](#field-limits) | `yes` | ref: `#/$defs/commandLimits` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`argvAtom`](#def-argvatom) | string |  |
| [`envKey`](#def-envkey) | string |  |
| [`envPolicy`](#def-envpolicy) | unspecified |  |
| [`commandLimits`](#def-commandlimits) | object |  |
| [`networkPolicy`](#def-networkpolicy) | unspecified |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-command-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-command-profile-ref"></a>
## `command.profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-executable"></a>
## `executable`

- Required: `yes`
- Shape: ref: `#/$defs/argvAtom`

<a id="field-fixed-args"></a>
## `fixed_args`

- Required: `no`
- Shape: array

<a id="field-allowed-arg-prefixes"></a>
## `allowed_arg_prefixes`

- Required: `no`
- Shape: array

Allowed prefixes for variable argv atoms after executable and fixed_args. An empty list means no variable argv atoms are allowed.

<a id="field-allowed-workspace-roots"></a>
## `allowed_workspace_roots`

- Required: `yes`
- Shape: array

Explicit allowlist of workspace root refs. The list is required to be non-empty; filesystem authority is default-deny.

<a id="field-env"></a>
## `env`

- Required: `yes`
- Shape: ref: `#/$defs/envPolicy`

<a id="field-network"></a>
## `network`

- Required: `no`
- Shape: ref: `#/$defs/networkPolicy`

Profile-level network policy. The Workbench hard-MVP contract admits only no-egress/local-only policy values; any future egress grant must use a separate capability contract.

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `#/$defs/commandLimits`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-argvatom"></a>
## `$defs.argvAtom`

- Shape: string

<a id="def-envkey"></a>
## `$defs.envKey`

- Shape: string

<a id="def-envpolicy"></a>
## `$defs.envPolicy`

- Shape: unspecified

<a id="def-commandlimits"></a>
## `$defs.commandLimits`

- Shape: object

<a id="def-networkpolicy"></a>
## `$defs.networkPolicy`

- Shape: unspecified
