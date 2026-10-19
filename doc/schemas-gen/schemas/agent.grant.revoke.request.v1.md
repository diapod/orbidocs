# Agent Single Grant Revoke Request v1

Source schema: [`doc/schemas/agent.grant.revoke.request.v1.schema.json`](../../schemas/agent.grant.revoke.request.v1.schema.json)

Owner-authorized, monotone withdrawal of one exact Agent capability grant.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.grant.revoke.request.v1` |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.grant.revoke.request.v1`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string
