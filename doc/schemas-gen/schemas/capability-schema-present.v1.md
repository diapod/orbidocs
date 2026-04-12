# Capability Schema Present v1

Source schema: [`doc/schemas/capability-schema-present.v1.schema.json`](../../schemas/capability-schema-present.v1.schema.json)

Peer-message response payload used to present one `capability-schema.v1` artifact over an authenticated Node-to-Node session. It mirrors the thin `capability-passport-present.v1` pattern while allowing explicit error responses for unavailable schemas.

## Governing Basis

- [`doc/project/40-proposals/027-middleware-peer-message-dispatch.md`](../../project/40-proposals/027-middleware-peer-message-dispatch.md)
- [`doc/project/60-solutions/capability-advertisement.md`](../../project/60-solutions/capability-advertisement.md)
- [`doc/schemas/capability-schema.v1.schema.json`](../../schemas/capability-schema.v1.schema.json)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-schema-present.v1` | Schema discriminator. MUST be exactly `capability-schema-present.v1`. |
| [`status`](#field-status) | `yes` | enum: `ok`, `error` | Whether the requested schema artifact is present in this response. |
| [`artifact`](#field-artifact) | `no` | object | Returned `capability-schema.v1` artifact. Required when `status = "ok"`. |
| [`error`](#field-error) | `no` | object | Machine-readable error object. Required when `status = "error"`. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "ok"
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
    "artifact"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "error"
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
    "error"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-schema-present.v1`

Schema discriminator. MUST be exactly `capability-schema-present.v1`.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `ok`, `error`

Whether the requested schema artifact is present in this response.

<a id="field-artifact"></a>
## `artifact`

- Required: `no`
- Shape: object

Returned `capability-schema.v1` artifact. Required when `status = "ok"`.

<a id="field-error"></a>
## `error`

- Required: `no`
- Shape: object

Machine-readable error object. Required when `status = "error"`.
