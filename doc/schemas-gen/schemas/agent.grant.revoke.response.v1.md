# Agent Single Grant Revoke Response v1

Source schema: [`doc/schemas/agent.grant.revoke.response.v1.schema.json`](../../schemas/agent.grant.revoke.response.v1.schema.json)

Retained decision at the withdrawal boundary; state is the state when the fact was written.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.grant.revoke.response.v1` |  |
| [`agent/id`](#field-agent-id) | `yes` | string |  |
| [`capability/id`](#field-capability-id) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `running`, `suspended` |  |
| [`changed`](#field-changed) | `yes` | boolean |  |
| [`replayed`](#field-replayed) | `yes` | boolean |  |
| [`reason/code`](#field-reason-code) | `yes` | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.grant.revoke.response.v1`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `running`, `suspended`

<a id="field-changed"></a>
## `changed`

- Required: `yes`
- Shape: boolean

<a id="field-replayed"></a>
## `replayed`

- Required: `yes`
- Shape: boolean

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string
