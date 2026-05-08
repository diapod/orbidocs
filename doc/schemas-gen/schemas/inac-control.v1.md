# INAC Control Frame

Source schema: [`doc/schemas/inac-control.v1.schema.json`](../../schemas/inac-control.v1.schema.json)

Control-plane frame for Inter-Node Artifact Channel offer/request/push/response exchanges. The frame is transport-neutral; concrete transports must preserve the byte identity of inline artifact bytes.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inac-control.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `offer`, `request`, `push`, `accept`, `decline`, `defer`, `ingested`, `already-present`, `refused`, `partial` |  |
| [`correlation/id`](#field-correlation-id) | `no` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string |  |
| [`artifact`](#field-artifact) | `no` | ref: `#/$defs/artifact` |  |
| [`request`](#field-request) | `no` | ref: `#/$defs/request` |  |
| [`transfer`](#field-transfer) | `no` | ref: `#/$defs/transfer` |  |
| [`response`](#field-response) | `no` | ref: `#/$defs/response` |  |
| [`meta`](#field-meta) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifact`](#def-artifact) | object |  |
| [`request`](#def-request) | object |  |
| [`transfer`](#def-transfer) | object |  |
| [`response`](#def-response) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "operation": {
      "const": "offer"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "required": [
    "artifact"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "operation": {
      "const": "push"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "required": [
    "artifact"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "operation": {
      "const": "request"
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "required": [
    "request"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "operation": {
      "enum": [
        "accept",
        "decline",
        "defer",
        "ingested",
        "already-present",
        "refused",
        "partial"
      ]
    }
  },
  "required": [
    "operation"
  ]
}
```

Then:

```json
{
  "required": [
    "response"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `inac-control.v1`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `offer`, `request`, `push`, `accept`, `decline`, `defer`, `ingested`, `already-present`, `refused`, `partial`

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: string

<a id="field-artifact"></a>
## `artifact`

- Required: `no`
- Shape: ref: `#/$defs/artifact`

<a id="field-request"></a>
## `request`

- Required: `no`
- Shape: ref: `#/$defs/request`

<a id="field-transfer"></a>
## `transfer`

- Required: `no`
- Shape: ref: `#/$defs/transfer`

<a id="field-response"></a>
## `response`

- Required: `no`
- Shape: ref: `#/$defs/response`

<a id="field-meta"></a>
## `meta`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-artifact"></a>
## `$defs.artifact`

- Shape: object

<a id="def-request"></a>
## `$defs.request`

- Shape: object

<a id="def-transfer"></a>
## `$defs.transfer`

- Shape: object

<a id="def-response"></a>
## `$defs.response`

- Shape: object
