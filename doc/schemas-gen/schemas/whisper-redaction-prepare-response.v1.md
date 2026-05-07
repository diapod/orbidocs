# Whisper Redaction Prepare Response v1

Source schema: [`doc/schemas/whisper-redaction-prepare-response.v1.schema.json`](../../schemas/whisper-redaction-prepare-response.v1.schema.json)

Host-capability response carrying a local redaction draft for Whisper intake. The response is private workflow data; it does not approve publication and is not an Agora record.

## Governing Basis

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/055-bounded-deferred-operation-contract.md`](../../project/40-proposals/055-bounded-deferred-operation-contract.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Stories

- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-redaction-prepare-response.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | enum: `draft-ready`, `needs-human-review`, `unsafe-output`, `policy-denied`, `model-unavailable`, `retryable-timeout`, `failed` |  |
| [`redaction/draft`](#field-redaction-draft) | `no` | object \| array \| string \| number \| boolean \| null | Provider-produced draft. Required when status is `draft-ready` or `needs-human-review`. The draft is local review material, not a publishable Agora record by itself. |
| [`diagnostics`](#field-diagnostics) | `no` | array |  |
| [`confidence`](#field-confidence) | `no` | number |  |
| [`provider/id`](#field-provider-id) | `no` | string |  |
| [`provider/runtime-id`](#field-provider-runtime-id) | `no` | string |  |
| [`profile/id`](#field-profile-id) | `no` | string |  |
| [`retryable`](#field-retryable) | `no` | boolean |  |
| [`reason`](#field-reason) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "enum": [
        "draft-ready",
        "needs-human-review"
      ]
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "redaction/draft"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-redaction-prepare-response.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `draft-ready`, `needs-human-review`, `unsafe-output`, `policy-denied`, `model-unavailable`, `retryable-timeout`, `failed`

<a id="field-redaction-draft"></a>
## `redaction/draft`

- Required: `no`
- Shape: object | array | string | number | boolean | null

Provider-produced draft. Required when status is `draft-ready` or `needs-human-review`. The draft is local review material, not a publishable Agora record by itself.

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: array

<a id="field-confidence"></a>
## `confidence`

- Required: `no`
- Shape: number

<a id="field-provider-id"></a>
## `provider/id`

- Required: `no`
- Shape: string

<a id="field-provider-runtime-id"></a>
## `provider/runtime-id`

- Required: `no`
- Shape: string

<a id="field-profile-id"></a>
## `profile/id`

- Required: `no`
- Shape: string

<a id="field-retryable"></a>
## `retryable`

- Required: `no`
- Shape: boolean

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string
