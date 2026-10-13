# Messaging Send Authorization Observation v1

Source schema: [`doc/schemas/messaging-send-authorize.local.v1.schema.json`](../../schemas/messaging-send-authorize.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`participant_id`](#field-participant-id) | `no` | string \| null |  |
| [`sender/provenance`](#field-sender-provenance) | `no` | object \| null |  |
| [`intent/digest`](#field-intent-digest) | `no` | string \| null |  |
| [`body/digest`](#field-body-digest) | `no` | string \| null |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "sender/provenance"
  ],
  "properties": {
    "sender/provenance": {
      "type": "object"
    }
  }
}
```

Then:

```json
{
  "required": [
    "body/digest"
  ],
  "properties": {
    "body/digest": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

## Field Semantics

<a id="field-participant-id"></a>
## `participant_id`

- Required: `no`
- Shape: string | null

<a id="field-sender-provenance"></a>
## `sender/provenance`

- Required: `no`
- Shape: object | null

<a id="field-intent-digest"></a>
## `intent/digest`

- Required: `no`
- Shape: string | null

<a id="field-body-digest"></a>
## `body/digest`

- Required: `no`
- Shape: string | null
