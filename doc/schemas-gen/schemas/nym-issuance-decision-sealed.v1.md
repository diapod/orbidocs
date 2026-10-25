# Nym-issuance-decision-sealed.v1

Source schema: [`doc/schemas/nym-issuance-decision-sealed.v1.schema.json`](../../schemas/nym-issuance-decision-sealed.v1.schema.json)

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
  "$ref": "nym-exchange-sealed.v1.schema.json"
}
```

### Rule 2

Constraint:

```json
{
  "properties": {
    "schema": {
      "const": "nym-issuance-decision-sealed.v1"
    },
    "payload/schema": {
      "const": "nym-issuance-decision.v1"
    }
  }
}
```

## Field Semantics
