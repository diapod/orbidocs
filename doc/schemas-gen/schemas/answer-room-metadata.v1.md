# AnswerRoomMetadata v1

Source schema: [`doc/schemas/answer-room-metadata.v1.schema.json`](../../schemas/answer-room-metadata.v1.schema.json)

Machine-readable schema for answer-channel room metadata, including operator participation policy profile and provenance-preservation expectations.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`room/id`](#field-room-id) | `yes` | string |  |
| [`question/id`](#field-question-id) | `yes` | string |  |
| [`delivery/scope`](#field-delivery-scope) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`room-policy/profile`](#field-room-policy-profile) | `yes` | enum: `none`, `mediated-only`, `direct-live-allowed` |  |
| [`operator-consultation/allowed`](#field-operator-consultation-allowed) | `yes` | boolean |  |
| [`operator-direct-live/allowed`](#field-operator-direct-live-allowed) | `yes` | boolean |  |
| [`human-live/origin-flag-required`](#field-human-live-origin-flag-required) | `no` | boolean |  |
| [`summary/human-provenance-required`](#field-summary-human-provenance-required) | `yes` | boolean |  |
| [`transcript/human-origin-preserved`](#field-transcript-human-origin-preserved) | `yes` | boolean |  |
| [`room-policy/effective-at`](#field-room-policy-effective-at) | `no` | string |  |
| [`room-policy/changed-by`](#field-room-policy-changed-by) | `no` | string |  |
| [`moderation/approval-required`](#field-moderation-approval-required) | `no` | boolean |  |
| [`secretary/required-for-direct-live`](#field-secretary-required-for-direct-live) | `no` | boolean |  |
| [`retention/profile`](#field-retention-profile) | `no` | string |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "room-policy/profile": {
      "const": "none"
    }
  },
  "required": [
    "room-policy/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "operator-consultation/allowed": {
      "const": false
    },
    "operator-direct-live/allowed": {
      "const": false
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "room-policy/profile": {
      "const": "mediated-only"
    }
  },
  "required": [
    "room-policy/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "operator-consultation/allowed": {
      "const": true
    },
    "operator-direct-live/allowed": {
      "const": false
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "room-policy/profile": {
      "const": "direct-live-allowed"
    }
  },
  "required": [
    "room-policy/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "operator-consultation/allowed": {
      "const": true
    },
    "operator-direct-live/allowed": {
      "const": true
    },
    "human-live/origin-flag-required": {
      "const": true
    }
  },
  "required": [
    "human-live/origin-flag-required"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "delivery/scope": {
      "const": "global"
    }
  },
  "required": [
    "delivery/scope"
  ]
}
```

Then:

```json
{
  "properties": {
    "room-policy/profile": {
      "not": {
        "const": "direct-live-allowed"
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: string

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

<a id="field-delivery-scope"></a>
## `delivery/scope`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-room-policy-profile"></a>
## `room-policy/profile`

- Required: `yes`
- Shape: enum: `none`, `mediated-only`, `direct-live-allowed`

<a id="field-operator-consultation-allowed"></a>
## `operator-consultation/allowed`

- Required: `yes`
- Shape: boolean

<a id="field-operator-direct-live-allowed"></a>
## `operator-direct-live/allowed`

- Required: `yes`
- Shape: boolean

<a id="field-human-live-origin-flag-required"></a>
## `human-live/origin-flag-required`

- Required: `no`
- Shape: boolean

<a id="field-summary-human-provenance-required"></a>
## `summary/human-provenance-required`

- Required: `yes`
- Shape: boolean

<a id="field-transcript-human-origin-preserved"></a>
## `transcript/human-origin-preserved`

- Required: `yes`
- Shape: boolean

<a id="field-room-policy-effective-at"></a>
## `room-policy/effective-at`

- Required: `no`
- Shape: string

<a id="field-room-policy-changed-by"></a>
## `room-policy/changed-by`

- Required: `no`
- Shape: string

<a id="field-moderation-approval-required"></a>
## `moderation/approval-required`

- Required: `no`
- Shape: boolean

<a id="field-secretary-required-for-direct-live"></a>
## `secretary/required-for-direct-live`

- Required: `no`
- Shape: boolean

<a id="field-retention-profile"></a>
## `retention/profile`

- Required: `no`
- Shape: string

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
