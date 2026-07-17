# Sensorium Interface Control Request v1

Source schema: [`doc/schemas/sensorium-interface-control-request.v1.schema.json`](../../schemas/sensorium-interface-control-request.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-control-request.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`action`](#field-action) | `yes` | enum: `claim`, `cancel`, `renew`, `release`, `handoff` |  |
| [`interface/id`](#field-interface-id) | `yes` | ref: `#/$defs/interface_ref` |  |
| [`caller/ref`](#field-caller-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`grant/id`](#field-grant-id) | `yes` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`claim/id`](#field-claim-id) | `no` | ref: `#/$defs/claim_ref` |  |
| [`handoff/accept`](#field-handoff-accept) | `no` | boolean |  |
| [`target/claim-id`](#field-target-claim-id) | `no` | ref: `#/$defs/claim_ref` |  |
| [`lease/id`](#field-lease-id) | `no` | ref: `#/$defs/lease_ref` |  |
| [`lease/epoch`](#field-lease-epoch) | `no` | integer |  |
| [`lease/requested-ms`](#field-lease-requested-ms) | `no` | integer |  |
| [`deadline/at`](#field-deadline-at) | `yes` | string |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`interface_ref`](#def-interface-ref) | string |  |
| [`claim_ref`](#def-claim-ref) | string |  |
| [`lease_ref`](#def-lease-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "action": {
      "const": "claim"
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "required": [
    "claim/id",
    "handoff/accept",
    "lease/requested-ms"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "target/claim-id"
        ]
      },
      {
        "required": [
          "lease/id"
        ]
      },
      {
        "required": [
          "lease/epoch"
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
    "action": {
      "const": "cancel"
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "required": [
    "claim/id"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "target/claim-id"
        ]
      },
      {
        "required": [
          "lease/id"
        ]
      },
      {
        "required": [
          "lease/epoch"
        ]
      },
      {
        "required": [
          "lease/requested-ms"
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
    "action": {
      "enum": [
        "renew",
        "release",
        "handoff"
      ]
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "required": [
    "lease/id",
    "lease/epoch"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "action": {
      "const": "renew"
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "required": [
    "lease/requested-ms"
  ]
}
```

### Rule 5

When:

```json
{
  "properties": {
    "action": {
      "const": "handoff"
    }
  },
  "required": [
    "action"
  ]
}
```

Then:

```json
{
  "required": [
    "target/claim-id"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-control-request.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-action"></a>
## `action`

- Required: `yes`
- Shape: enum: `claim`, `cancel`, `renew`, `release`, `handoff`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-caller-ref"></a>
## `caller/ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-grant-id"></a>
## `grant/id`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-claim-id"></a>
## `claim/id`

- Required: `no`
- Shape: ref: `#/$defs/claim_ref`

<a id="field-handoff-accept"></a>
## `handoff/accept`

- Required: `no`
- Shape: boolean

<a id="field-target-claim-id"></a>
## `target/claim-id`

- Required: `no`
- Shape: ref: `#/$defs/claim_ref`

<a id="field-lease-id"></a>
## `lease/id`

- Required: `no`
- Shape: ref: `#/$defs/lease_ref`

<a id="field-lease-epoch"></a>
## `lease/epoch`

- Required: `no`
- Shape: integer

<a id="field-lease-requested-ms"></a>
## `lease/requested-ms`

- Required: `no`
- Shape: integer

<a id="field-deadline-at"></a>
## `deadline/at`

- Required: `yes`
- Shape: string

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-interface-ref"></a>
## `$defs.interface_ref`

- Shape: string

<a id="def-claim-ref"></a>
## `$defs.claim_ref`

- Shape: string

<a id="def-lease-ref"></a>
## `$defs.lease_ref`

- Shape: string
