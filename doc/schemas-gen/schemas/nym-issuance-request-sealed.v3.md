# Nym-issuance-request-sealed.v3

Source schema: [`doc/schemas/nym-issuance-request-sealed.v3.schema.json`](../../schemas/nym-issuance-request-sealed.v3.schema.json)

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "$ref": "nym-exchange-sealed.v3.schema.json"
}
```

### Rule 2

Constraint:

```json
{
  "properties": {
    "schema": {
      "const": "nym-issuance-request-sealed.v3"
    },
    "payload/schema": {
      "const": "nym-issuance-request.v3"
    }
  }
}
```

## Field Semantics
