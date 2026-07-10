# Middleware Channel Frame v1

Source schema: [`doc/schemas/middleware-channel-frame.v1.schema.json`](../../schemas/middleware-channel-frame.v1.schema.json)

Strict outer application frame for one accepted middleware channel session.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-frame.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`session/id`](#field-session-id) | `yes` | ref: `#/$defs/id` |  |
| [`session/epoch`](#field-session-epoch) | `yes` | integer |  |
| [`frame/seq`](#field-frame-seq) | `yes` | integer |  |
| [`message/kind`](#field-message-kind) | `yes` | enum: `request`, `response`, `event`, `control` |  |
| [`operation`](#field-operation) | `yes` | enum: `middleware.init`, `middleware.invoke`, `middleware.observe`, `module-http.invoke`, `request.cancel`, `host-capability.invoke`, `heartbeat`, `session.shutdown` |  |
| [`request/id`](#field-request-id) | `no` | ref: `#/$defs/id` |  |
| [`reply/to`](#field-reply-to) | `no` | ref: `#/$defs/id` |  |
| [`deadline/at`](#field-deadline-at) | `no` | string |  |
| [`trace/correlation-id`](#field-trace-correlation-id) | `no` | ref: `#/$defs/id` |  |
| [`payload/schema`](#field-payload-schema) | `yes` | ref: `#/$defs/schemaName` |  |
| [`payload`](#field-payload) | `yes` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | string |  |
| [`schemaName`](#def-schemaname) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "request"
    }
  },
  "required": [
    "message/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "request/id",
    "deadline/at"
  ],
  "not": {
    "required": [
      "reply/to"
    ]
  },
  "properties": {
    "operation": {
      "enum": [
        "middleware.init",
        "middleware.invoke",
        "module-http.invoke",
        "host-capability.invoke"
      ]
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "response"
    }
  },
  "required": [
    "message/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "reply/to"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "request/id"
        ]
      },
      {
        "required": [
          "deadline/at"
        ]
      }
    ]
  },
  "properties": {
    "operation": {
      "enum": [
        "middleware.init",
        "middleware.invoke",
        "module-http.invoke",
        "host-capability.invoke"
      ]
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "event"
    }
  },
  "required": [
    "message/kind"
  ]
}
```

Then:

```json
{
  "not": {
    "anyOf": [
      {
        "required": [
          "request/id"
        ]
      },
      {
        "required": [
          "reply/to"
        ]
      },
      {
        "required": [
          "deadline/at"
        ]
      }
    ]
  },
  "properties": {
    "operation": {
      "const": "middleware.observe"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "control"
    }
  },
  "required": [
    "message/kind"
  ]
}
```

Then:

```json
{
  "not": {
    "anyOf": [
      {
        "required": [
          "request/id"
        ]
      },
      {
        "required": [
          "reply/to"
        ]
      },
      {
        "required": [
          "deadline/at"
        ]
      }
    ]
  },
  "properties": {
    "operation": {
      "enum": [
        "request.cancel",
        "heartbeat",
        "session.shutdown"
      ]
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "request"
    },
    "operation": {
      "const": "host-capability.invoke"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-channel-host-capability-call.v1"
    }
  }
}
```

### Rule 6

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "response"
    },
    "operation": {
      "const": "host-capability.invoke"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-channel-call-result.v1"
    }
  }
}
```

### Rule 7

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "request"
    },
    "operation": {
      "const": "module-http.invoke"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-module-http-request.v1"
    }
  }
}
```

### Rule 8

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "response"
    },
    "operation": {
      "const": "module-http.invoke"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-module-http-response.v1"
    }
  }
}
```

### Rule 9

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "control"
    },
    "operation": {
      "const": "request.cancel"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-channel-request-cancel.v1"
    }
  }
}
```

### Rule 10

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "control"
    },
    "operation": {
      "const": "heartbeat"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-channel-heartbeat.v1"
    }
  }
}
```

### Rule 11

When:

```json
{
  "properties": {
    "message/kind": {
      "const": "control"
    },
    "operation": {
      "const": "session.shutdown"
    }
  },
  "required": [
    "message/kind",
    "operation"
  ]
}
```

Then:

```json
{
  "properties": {
    "payload/schema": {
      "const": "middleware-channel-session-shutdown.v1"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `middleware-channel-frame.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-session-id"></a>
## `session/id`

- Required: `yes`
- Shape: ref: `#/$defs/id`

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: integer

<a id="field-frame-seq"></a>
## `frame/seq`

- Required: `yes`
- Shape: integer

<a id="field-message-kind"></a>
## `message/kind`

- Required: `yes`
- Shape: enum: `request`, `response`, `event`, `control`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `middleware.init`, `middleware.invoke`, `middleware.observe`, `module-http.invoke`, `request.cancel`, `host-capability.invoke`, `heartbeat`, `session.shutdown`

<a id="field-request-id"></a>
## `request/id`

- Required: `no`
- Shape: ref: `#/$defs/id`

<a id="field-reply-to"></a>
## `reply/to`

- Required: `no`
- Shape: ref: `#/$defs/id`

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `no`
- Shape: string

<a id="field-trace-correlation-id"></a>
## `trace/correlation-id`

- Required: `no`
- Shape: ref: `#/$defs/id`

<a id="field-payload-schema"></a>
## `payload/schema`

- Required: `yes`
- Shape: ref: `#/$defs/schemaName`

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: object

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: string

<a id="def-schemaname"></a>
## `$defs.schemaName`

- Shape: string
