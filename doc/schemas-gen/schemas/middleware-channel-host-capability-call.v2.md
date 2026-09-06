# Middleware Channel Host Capability Call v2

Source schema: [`doc/schemas/middleware-channel-host-capability-call.v2.schema.json`](../../schemas/middleware-channel-host-capability-call.v2.schema.json)

Module-authored request body for invoking one host-authorized capability or reading its host-owned routing view through an authenticated channel session.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-host-capability-call.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`capability/id`](#field-capability-id) | `yes` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/capability~1id` |  |
| [`operation`](#field-operation) | `no` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/operation` |  |
| [`request/schema`](#field-request-schema) | `yes` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/request~1schema` |  |
| [`request`](#field-request) | `yes` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/request` |  |
| [`completion/mode`](#field-completion-mode) | `no` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/completion~1mode` |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/idempotency~1key` |  |
| [`response/schema`](#field-response-schema) | `no` | ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/request~1schema` | Optional exact successful response representation. Unsupported selection refuses before capability I/O; no automatic downgrade. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "operation"
  ],
  "properties": {
    "operation": {
      "const": "lookup"
    }
  }
}
```

Then:

```json
{
  "not": {
    "required": [
      "response/schema"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-host-capability-call.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-capability-id"></a>
## `capability/id`

- Required: `yes`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/capability~1id`

<a id="field-operation"></a>
## `operation`

- Required: `no`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/operation`

<a id="field-request-schema"></a>
## `request/schema`

- Required: `yes`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/request~1schema`

<a id="field-request"></a>
## `request`

- Required: `yes`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/request`

<a id="field-completion-mode"></a>
## `completion/mode`

- Required: `no`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/completion~1mode`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/idempotency~1key`

<a id="field-response-schema"></a>
## `response/schema`

- Required: `no`
- Shape: ref: `middleware-channel-host-capability-call.v1.schema.json#/properties/request~1schema`

Optional exact successful response representation. Unsupported selection refuses before capability I/O; no automatic downgrade.
