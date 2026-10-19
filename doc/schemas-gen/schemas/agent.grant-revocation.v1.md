# Agent Grant Revocation Fact v1

Source schema: [`doc/schemas/agent.grant-revocation.v1.schema.json`](../../schemas/agent.grant-revocation.v1.schema.json)

Single durable authority-reduction fact; the prior session and binding facts remain unchanged.

## Governing Basis

- [`doc/project/40-proposals/073-agent-orchestration-organ.md`](../../project/40-proposals/073-agent-orchestration-organ.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agent.grant-revocation.v1` |  |
| [`agent/id`](#field-agent-id) | `yes` | string | At most 1024 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound. |
| [`capability/id`](#field-capability-id) | `yes` | string | At most 256 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound. |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string | At most 256 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound. |
| [`request/digest`](#field-request-digest) | `yes` | string |  |
| [`result/state`](#field-result-state) | `yes` | enum: `running`, `suspended` |  |
| [`changed`](#field-changed) | `yes` | boolean |  |
| [`reason/code`](#field-reason-code) | `yes` | string | At most 256 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound. |
| [`at`](#field-at) | `yes` | string |  |
| [`by`](#field-by) | `yes` | string | Authenticated local-control or module id, at most 256 UTF-8 bytes; the host enforces the byte bound. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agent.grant-revocation.v1`

<a id="field-agent-id"></a>
## `agent/id`

- Required: `yes`
- Shape: string

At most 1024 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound.

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: string

At most 256 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound.

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

At most 256 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound.

<a id="field-request-digest"></a>
## `request/digest`

- Required: `yes`
- Shape: string

<a id="field-result-state"></a>
## `result/state`

- Required: `yes`
- Shape: enum: `running`, `suspended`

<a id="field-changed"></a>
## `changed`

- Required: `yes`
- Shape: boolean

<a id="field-reason-code"></a>
## `reason/code`

- Required: `yes`
- Shape: string

At most 256 UTF-8 bytes; JSON Schema maxLength counts code points and the host enforces the byte bound.

<a id="field-at"></a>
## `at`

- Required: `yes`
- Shape: string

<a id="field-by"></a>
## `by`

- Required: `yes`
- Shape: string

Authenticated local-control or module id, at most 256 UTF-8 bytes; the host enforces the byte bound.
