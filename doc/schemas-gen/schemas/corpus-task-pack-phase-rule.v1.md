# Corpus Task Pack Phase Rule v1

Source schema: [`doc/schemas/corpus-task-pack-phase-rule.v1.schema.json`](../../schemas/corpus-task-pack-phase-rule.v1.schema.json)

Package-owned observation and verifier requirements. The host validates profile membership and exact observation effect modes. This rule grants no effects.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-phase-rule.v1` |  |
| [`rule/ref`](#field-rule-ref) | `yes` | string |  |
| [`observation/profile-refs`](#field-observation-profile-refs) | `yes` | array |  |
| [`verifier/ref`](#field-verifier-ref) | `yes` | string |  |
| [`repair/observation-only`](#field-repair-observation-only) | `yes` | const: `refuse` | Explicit policy for this bounded rule: no further observation-only candidate once repair is eligible, even after a failed repair. Additional diagnosis needs a separately designed host-gap policy, not a model exception. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-phase-rule.v1`

<a id="field-rule-ref"></a>
## `rule/ref`

- Required: `yes`
- Shape: string

<a id="field-observation-profile-refs"></a>
## `observation/profile-refs`

- Required: `yes`
- Shape: array

<a id="field-verifier-ref"></a>
## `verifier/ref`

- Required: `yes`
- Shape: string

<a id="field-repair-observation-only"></a>
## `repair/observation-only`

- Required: `yes`
- Shape: const: `refuse`

Explicit policy for this bounded rule: no further observation-only candidate once repair is eligible, even after a failed repair. Additional diagnosis needs a separately designed host-gap policy, not a model exception.
