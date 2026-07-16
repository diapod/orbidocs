# Sensorium Interface Frame v1

Source schema: [`doc/schemas/sensorium-interface-frame.v1.schema.json`](../../schemas/sensorium-interface-frame.v1.schema.json)

One bounded classified value or lifecycle marker inside a Sensorium Interface result batch.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-frame.v1` | Contract discriminator. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Contract version. |
| [`frame/kind`](#field-frame-kind) | `yes` | enum: `snapshot`, `event`, `gap`, `end` | Data or lifecycle shape of this frame. |
| [`observed/at`](#field-observed-at) | `yes` | string | Time represented by the source value or marker. |
| [`emitted/at`](#field-emitted-at) | `yes` | string | Time the interface adapter emitted this frame. |
| [`payload/schema-ref`](#field-payload-schema-ref) | `no` | string | Schema of an inline or artifact-backed data payload; must equal the descriptor output schema. |
| [`payload`](#field-payload) | `no` | unspecified | Inline data value for a snapshot or event. |
| [`artifact/ref`](#field-artifact-ref) | `no` | string | Reference to an independently admitted Artifact Delivery value when data is not inline. |
| [`gap/from-cursor`](#field-gap-from-cursor) | `no` | string | First cursor position in a lost or unavailable ordered-event interval. |
| [`gap/to-cursor`](#field-gap-to-cursor) | `no` | string | Resume boundary after a lost or unavailable ordered-event interval. |
| [`terminal/reason`](#field-terminal-reason) | `no` | string | Typed reason carried only by the final end frame. |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` | Effective classification enforced for this emitted frame, including gap and terminal metadata. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "frame/kind": {
      "enum": [
        "snapshot",
        "event"
      ]
    }
  },
  "required": [
    "frame/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "payload/schema-ref"
  ],
  "oneOf": [
    {
      "required": [
        "payload"
      ],
      "not": {
        "required": [
          "artifact/ref"
        ]
      }
    },
    {
      "required": [
        "artifact/ref"
      ],
      "not": {
        "required": [
          "payload"
        ]
      }
    }
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "gap/from-cursor"
        ]
      },
      {
        "required": [
          "gap/to-cursor"
        ]
      },
      {
        "required": [
          "terminal/reason"
        ]
      }
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "frame/kind": {
      "const": "gap"
    }
  },
  "required": [
    "frame/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "gap/from-cursor",
    "gap/to-cursor"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "payload/schema-ref"
        ]
      },
      {
        "required": [
          "payload"
        ]
      },
      {
        "required": [
          "artifact/ref"
        ]
      },
      {
        "required": [
          "terminal/reason"
        ]
      }
    ]
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "frame/kind": {
      "const": "end"
    }
  },
  "required": [
    "frame/kind"
  ]
}
```

Then:

```json
{
  "required": [
    "terminal/reason"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "payload/schema-ref"
        ]
      },
      {
        "required": [
          "payload"
        ]
      },
      {
        "required": [
          "artifact/ref"
        ]
      },
      {
        "required": [
          "gap/from-cursor"
        ]
      },
      {
        "required": [
          "gap/to-cursor"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-frame.v1`

Contract discriminator.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Contract version.

<a id="field-frame-kind"></a>
## `frame/kind`

- Required: `yes`
- Shape: enum: `snapshot`, `event`, `gap`, `end`

Data or lifecycle shape of this frame.

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

Time represented by the source value or marker.

<a id="field-emitted-at"></a>
## `emitted/at`

- Required: `yes`
- Shape: string

Time the interface adapter emitted this frame.

<a id="field-payload-schema-ref"></a>
## `payload/schema-ref`

- Required: `no`
- Shape: string

Schema of an inline or artifact-backed data payload; must equal the descriptor output schema.

<a id="field-payload"></a>
## `payload`

- Required: `no`
- Shape: unspecified

Inline data value for a snapshot or event.

<a id="field-artifact-ref"></a>
## `artifact/ref`

- Required: `no`
- Shape: string

Reference to an independently admitted Artifact Delivery value when data is not inline.

<a id="field-gap-from-cursor"></a>
## `gap/from-cursor`

- Required: `no`
- Shape: string

First cursor position in a lost or unavailable ordered-event interval.

<a id="field-gap-to-cursor"></a>
## `gap/to-cursor`

- Required: `no`
- Shape: string

Resume boundary after a lost or unavailable ordered-event interval.

<a id="field-terminal-reason"></a>
## `terminal/reason`

- Required: `no`
- Shape: string

Typed reason carried only by the final end frame.

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

Effective classification enforced for this emitted frame, including gap and terminal metadata.
