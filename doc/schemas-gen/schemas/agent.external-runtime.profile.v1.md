# Agent External Runtime Profile v1

Source schema: [`doc/schemas/agent.external-runtime.profile.v1.schema.json`](../../schemas/agent.external-runtime.profile.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.external-runtime.profile.v1` |  |
| [`profile/ref`](#field-profile-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`profile/generation`](#field-profile-generation) | `yes` | ref: `#/$defs/positive-safe-integer` |  |
| [`driver/variant`](#field-driver-variant) | `yes` | ref: `#/$defs/ref` |  |
| [`driver/version`](#field-driver-version) | `yes` | ref: `#/$defs/ref` |  |
| [`transport/class`](#field-transport-class) | `yes` | enum: `in-process`, `supervised-process`, `local-socket`, `remote` |  |
| [`auth/class`](#field-auth-class) | `yes` | enum: `none`, `operator-session`, `api-credential`, `workload-identity` |  |
| [`principal/snapshot-ref`](#field-principal-snapshot-ref) | `no` | ref: `#/$defs/ref` |  |
| [`session/scope`](#field-session-scope) | `yes` | const: `agent-runtime-binding` |  |
| [`session/persistence`](#field-session-persistence) | `yes` | enum: `ephemeral`, `adapter-restart`, `remote` |  |
| [`retention/class`](#field-retention-class) | `yes` | enum: `none`, `operator-policy`, `provider-policy` |  |
| [`egress/classes`](#field-egress-classes) | `yes` | array |  |
| [`tool/mode`](#field-tool-mode) | `yes` | enum: `deny-all`, `mediated` |  |
| [`usage/fidelity`](#field-usage-fidelity) | `yes` | enum: `authoritative`, `host-measured`, `estimated`, `unavailable` |  |
| [`event/ordering`](#field-event-ordering) | `yes` | const: `strict-sequence` |  |
| [`supports`](#field-supports) | `yes` | object |  |
| [`limits`](#field-limits) | `yes` | object |  |
| [`created/at`](#field-created-at) | `yes` | string |  |
| [`created/by`](#field-created-by) | `yes` | ref: `#/$defs/ref` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`positive-safe-integer`](#def-positive-safe-integer) | integer |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.external-runtime.profile.v1`

<a id="field-profile-ref"></a>
## `profile/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-profile-generation"></a>
## `profile/generation`

- Required: `yes`
- Shape: ref: `#/$defs/positive-safe-integer`

<a id="field-driver-variant"></a>
## `driver/variant`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-driver-version"></a>
## `driver/version`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-transport-class"></a>
## `transport/class`

- Required: `yes`
- Shape: enum: `in-process`, `supervised-process`, `local-socket`, `remote`

<a id="field-auth-class"></a>
## `auth/class`

- Required: `yes`
- Shape: enum: `none`, `operator-session`, `api-credential`, `workload-identity`

<a id="field-principal-snapshot-ref"></a>
## `principal/snapshot-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-session-scope"></a>
## `session/scope`

- Required: `yes`
- Shape: const: `agent-runtime-binding`

<a id="field-session-persistence"></a>
## `session/persistence`

- Required: `yes`
- Shape: enum: `ephemeral`, `adapter-restart`, `remote`

<a id="field-retention-class"></a>
## `retention/class`

- Required: `yes`
- Shape: enum: `none`, `operator-policy`, `provider-policy`

<a id="field-egress-classes"></a>
## `egress/classes`

- Required: `yes`
- Shape: array

<a id="field-tool-mode"></a>
## `tool/mode`

- Required: `yes`
- Shape: enum: `deny-all`, `mediated`

<a id="field-usage-fidelity"></a>
## `usage/fidelity`

- Required: `yes`
- Shape: enum: `authoritative`, `host-measured`, `estimated`, `unavailable`

<a id="field-event-ordering"></a>
## `event/ordering`

- Required: `yes`
- Shape: const: `strict-sequence`

<a id="field-supports"></a>
## `supports`

- Required: `yes`
- Shape: object

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: object

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: string

<a id="field-created-by"></a>
## `created/by`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-positive-safe-integer"></a>
## `$defs.positive-safe-integer`

- Shape: integer
