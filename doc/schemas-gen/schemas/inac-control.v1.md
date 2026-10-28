# INAC Control Frame

Source schema: [`doc/schemas/inac-control.v1.schema.json`](../../schemas/inac-control.v1.schema.json)

Control-plane frame for Inter-Node Artifact Channel offer/request/push/response exchanges. The frame is transport-neutral; concrete transports must preserve the byte identity of inline artifact bytes.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `inac-control.v1` |  |
| [`operation`](#field-operation) | `yes` | enum: `offer`, `request`, `push`, `accept`, `decline`, `defer`, `ingested`, `already-present`, `refused`, `partial`, `admission-status`, `admission-status-result` |  |
| [`correlation/id`](#field-correlation-id) | `no` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string |  |
| [`artifact`](#field-artifact) | `no` | ref: `#/$defs/artifact` |  |
| [`request`](#field-request) | `no` | ref: `#/$defs/request` |  |
| [`transfer`](#field-transfer) | `no` | ref: `#/$defs/transfer` |  |
| [`authorization`](#field-authorization) | `no` | ref: `#/$defs/authorization` |  |
| [`response`](#field-response) | `no` | ref: `#/$defs/response` |  |
| [`meta`](#field-meta) | `no` | object |  |
| [`admission/status`](#field-admission-status) | `no` | unspecified |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifact`](#def-artifact) | object |  |
| [`request`](#def-request) | object |  |
| [`transfer`](#def-transfer) | object |  |
| [`authorization`](#def-authorization) | object |  |
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
  ],
  "properties": {
    "artifact": {
      "oneOf": [
        {
          "required": [
            "bytes/base64url"
          ],
          "not": {
            "anyOf": [
              {
                "required": [
                  "artifact/ref"
                ]
              },
              {
                "required": [
                  "artifact/href"
                ]
              }
            ]
          }
        },
        {
          "required": [
            "artifact/ref"
          ],
          "not": {
            "anyOf": [
              {
                "required": [
                  "bytes/base64url"
                ]
              },
              {
                "required": [
                  "artifact/href"
                ]
              }
            ]
          }
        },
        {
          "required": [
            "artifact/href"
          ],
          "not": {
            "anyOf": [
              {
                "required": [
                  "bytes/base64url"
                ]
              },
              {
                "required": [
                  "artifact/ref"
                ]
              }
            ]
          }
        }
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

### Rule 5

When:

```json
{
  "properties": {
    "operation": {
      "const": "admission-status"
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
    "correlation/id",
    "admission/status"
  ],
  "properties": {
    "admission/status": {
      "properties": {
        "kind": {
          "const": "query"
        }
      }
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "artifact"
        ]
      },
      {
        "required": [
          "request"
        ]
      },
      {
        "required": [
          "authorization"
        ]
      },
      {
        "required": [
          "transfer"
        ]
      },
      {
        "required": [
          "response"
        ]
      },
      {
        "required": [
          "meta"
        ]
      }
    ]
  }
}
```

### Rule 6

When:

```json
{
  "properties": {
    "operation": {
      "const": "admission-status-result"
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
    "correlation/id",
    "admission/status"
  ],
  "properties": {
    "admission/status": {
      "properties": {
        "kind": {
          "const": "result"
        }
      }
    }
  },
  "not": {
    "anyOf": [
      {
        "required": [
          "artifact"
        ]
      },
      {
        "required": [
          "request"
        ]
      },
      {
        "required": [
          "authorization"
        ]
      },
      {
        "required": [
          "transfer"
        ]
      },
      {
        "required": [
          "response"
        ]
      },
      {
        "required": [
          "meta"
        ]
      }
    ]
  }
}
```

### Rule 7

When:

```json
{
  "required": [
    "admission/status"
  ]
}
```

Then:

```json
{
  "properties": {
    "operation": {
      "enum": [
        "admission-status",
        "admission-status-result"
      ]
    }
  }
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
- Shape: enum: `offer`, `request`, `push`, `accept`, `decline`, `defer`, `ingested`, `already-present`, `refused`, `partial`, `admission-status`, `admission-status-result`

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

<a id="field-authorization"></a>
## `authorization`

- Required: `no`
- Shape: ref: `#/$defs/authorization`

<a id="field-response"></a>
## `response`

- Required: `no`
- Shape: ref: `#/$defs/response`

<a id="field-meta"></a>
## `meta`

- Required: `no`
- Shape: object

<a id="field-admission-status"></a>
## `admission/status`

- Required: `no`
- Shape: unspecified

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

<a id="def-authorization"></a>
## `$defs.authorization`

- Shape: object

<a id="def-response"></a>
## `$defs.response`

- Shape: object
