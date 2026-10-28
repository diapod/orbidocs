# Private Assessment Exposure Fact v1

Source schema: [`doc/schemas/assessment-exposure-fact.v1.schema.json`](../../schemas/assessment-exposure-fact.v1.schema.json)

Host-accepted private facts. Never an assertion of psychological independence. Round events are reserved and not admitted by the local store.

## Governing Basis

- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `assessment-exposure-fact.v1` |  |
| [`viewer/ref`](#field-viewer-ref) | `yes` | string |  |
| [`subject/key`](#field-subject-key) | `yes` | string |  |
| [`event`](#field-event) | `yes` | enum: `subject-first-seen`, `own-first-judgment`, `explicit-skip`, `subject-window-elapsed`, `view-released`, `barrier-released` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`recorded/at`](#field-recorded-at) | `yes` | string |  |
| [`idempotency/key`](#field-idempotency-key) | `yes` | string |  |
| [`cause/record-id`](#field-cause-record-id) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "event"
  ],
  "properties": {
    "event": {
      "const": "own-first-judgment"
    }
  }
}
```

Then:

```json
{
  "required": [
    "cause/record-id"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `assessment-exposure-fact.v1`

<a id="field-viewer-ref"></a>
## `viewer/ref`

- Required: `yes`
- Shape: string

<a id="field-subject-key"></a>
## `subject/key`

- Required: `yes`
- Shape: string

<a id="field-event"></a>
## `event`

- Required: `yes`
- Shape: enum: `subject-first-seen`, `own-first-judgment`, `explicit-skip`, `subject-window-elapsed`, `view-released`, `barrier-released`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-recorded-at"></a>
## `recorded/at`

- Required: `yes`
- Shape: string

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `yes`
- Shape: string

<a id="field-cause-record-id"></a>
## `cause/record-id`

- Required: `no`
- Shape: string
