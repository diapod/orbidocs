# Authenticated Assessment Exposure Request v1

Source schema: [`doc/schemas/assessment-exposure-command.v1.schema.json`](../../schemas/assessment-exposure-command.v1.schema.json)

Viewer is bound by the host caller resolver, never supplied by the caller. Read rejects transition fields; transition requires event and idempotency/key. Own judgment is checked against an admitted signed record.

## Governing Basis

- [`doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`](../../project/40-proposals/026-resource-opinions-and-discussion-surfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`subject`](#field-subject) | `yes` | object |  |
| [`event`](#field-event) | `no` | enum: `encounter`, `explicit-skip`, `own-first-judgment` |  |
| [`idempotency/key`](#field-idempotency-key) | `no` | string |  |
| [`cause/record-id`](#field-cause-record-id) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "event"
  ]
}
```

Then:

```json
{
  "required": [
    "idempotency/key"
  ]
}
```

### Rule 2

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

<a id="field-subject"></a>
## `subject`

- Required: `yes`
- Shape: object

<a id="field-event"></a>
## `event`

- Required: `no`
- Shape: enum: `encounter`, `explicit-skip`, `own-first-judgment`

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: string

<a id="field-cause-record-id"></a>
## `cause/record-id`

- Required: `no`
- Shape: string
