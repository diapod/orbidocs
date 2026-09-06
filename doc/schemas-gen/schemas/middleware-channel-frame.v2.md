# Middleware Channel Frame v2

Source schema: [`doc/schemas/middleware-channel-frame.v2.schema.json`](../../schemas/middleware-channel-frame.v2.schema.json)

Strict outer application frame for one accepted middleware channel session.

## Governing Basis

- [`doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`](../../project/40-proposals/080-multiplexed-middleware-channel-executor.md)
- [`doc/project/40-proposals/086-component-communication-observation-and-trace-sessions.md`](../../project/40-proposals/086-component-communication-observation-and-trace-sessions.md)
- [`doc/project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md`](../../project/40-proposals/090-inference-execution-provenance-and-non-local-disclosure.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `middleware-channel-frame.v2` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `2` |  |
| [`session/id`](#field-session-id) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/session~1id` |  |
| [`session/epoch`](#field-session-epoch) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/session~1epoch` |  |
| [`frame/seq`](#field-frame-seq) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/frame~1seq` |  |
| [`message/kind`](#field-message-kind) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/message~1kind` |  |
| [`operation`](#field-operation) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/operation` |  |
| [`request/id`](#field-request-id) | `no` | ref: `middleware-channel-frame.v1.schema.json#/properties/request~1id` |  |
| [`reply/to`](#field-reply-to) | `no` | ref: `middleware-channel-frame.v1.schema.json#/properties/reply~1to` |  |
| [`deadline/at`](#field-deadline-at) | `no` | ref: `middleware-channel-frame.v1.schema.json#/properties/deadline~1at` |  |
| [`trace/correlation-id`](#field-trace-correlation-id) | `no` | ref: `middleware-channel-frame.v1.schema.json#/properties/trace~1correlation-id` |  |
| [`payload/schema`](#field-payload-schema) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/payload~1schema` |  |
| [`payload`](#field-payload) | `yes` | ref: `middleware-channel-frame.v1.schema.json#/properties/payload` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`id`](#def-id) | ref: `middleware-channel-frame.v1.schema.json#/$defs/id` |  |
| [`schemaName`](#def-schemaname) | ref: `middleware-channel-frame.v1.schema.json#/$defs/schemaName` |  |

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
      "enum": [
        "middleware.observe",
        "middleware.trace.report"
      ]
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
      "const": "event"
    },
    "operation": {
      "const": "middleware.trace.report"
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
      "const": "component-communication-report.v1"
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

### Rule 6

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
      "const": "middleware-channel-host-capability-call.v2"
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

### Rule 8

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

### Rule 9

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

### Rule 10

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

### Rule 11

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

### Rule 12

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
- Shape: const: `middleware-channel-frame.v2`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `2`

<a id="field-session-id"></a>
## `session/id`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/session~1id`

<a id="field-session-epoch"></a>
## `session/epoch`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/session~1epoch`

<a id="field-frame-seq"></a>
## `frame/seq`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/frame~1seq`

<a id="field-message-kind"></a>
## `message/kind`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/message~1kind`

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/operation`

<a id="field-request-id"></a>
## `request/id`

- Required: `no`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/request~1id`

<a id="field-reply-to"></a>
## `reply/to`

- Required: `no`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/reply~1to`

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `no`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/deadline~1at`

<a id="field-trace-correlation-id"></a>
## `trace/correlation-id`

- Required: `no`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/trace~1correlation-id`

<a id="field-payload-schema"></a>
## `payload/schema`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/payload~1schema`

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: ref: `middleware-channel-frame.v1.schema.json#/properties/payload`

## Definition Semantics

<a id="def-id"></a>
## `$defs.id`

- Shape: ref: `middleware-channel-frame.v1.schema.json#/$defs/id`

<a id="def-schemaname"></a>
## `$defs.schemaName`

- Shape: ref: `middleware-channel-frame.v1.schema.json#/$defs/schemaName`
