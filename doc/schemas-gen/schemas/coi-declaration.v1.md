# COI Declaration v1

Source schema: [`doc/schemas/coi-declaration.v1.schema.json`](../../schemas/coi-declaration.v1.schema.json)

Machine-readable schema for a signed conflict-of-interest declaration used by panel selection. The signed surface uses the same family as the rest of the protocol stack: `orbiplex-coi-declaration-v1\x00 || deterministic_cbor(payload_without_signature)`.

## Governing Basis

- [`doc/normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md`](../../normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md)
- [`doc/normative/50-constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md`](../../normative/50-constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`case/hash`](#field-case-hash) | `yes` | string | Blinded or otherwise minimally disclosing challenge hash of the case for which the declaration is made. |
| [`participant/id`](#field-participant-id) | `yes` | string | Stable participant identity serving in the governance pipeline. Nym identities are not valid here. |
| [`declaration`](#field-declaration) | `yes` | enum: `no-conflict`, `conflict` | Conflict-of-interest declaration outcome. |
| [`ts`](#field-ts) | `yes` | string | Timestamp of the declaration. |
| [`nonce`](#field-nonce) | `yes` | string | Fresh nonce preventing replay of the declaration artifact. |
| [`conflict/category`](#field-conflict-category) | `no` | string | Optional coarse category when `declaration = conflict`. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` | Participant signature over the declaration payload. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "declaration": {
      "const": "conflict"
    }
  },
  "required": [
    "declaration"
  ]
}
```

Then:

```json
{
  "required": [
    "conflict/category"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "declaration": {
      "const": "no-conflict"
    }
  },
  "required": [
    "declaration"
  ]
}
```

Then:

```json
{
  "not": {
    "required": [
      "conflict/category"
    ]
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-case-hash"></a>
## `case/hash`

- Required: `yes`
- Shape: string

Blinded or otherwise minimally disclosing challenge hash of the case for which the declaration is made.

<a id="field-participant-id"></a>
## `participant/id`

- Required: `yes`
- Shape: string

Stable participant identity serving in the governance pipeline. Nym identities are not valid here.

<a id="field-declaration"></a>
## `declaration`

- Required: `yes`
- Shape: enum: `no-conflict`, `conflict`

Conflict-of-interest declaration outcome.

<a id="field-ts"></a>
## `ts`

- Required: `yes`
- Shape: string

Timestamp of the declaration.

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

Fresh nonce preventing replay of the declaration artifact.

<a id="field-conflict-category"></a>
## `conflict/category`

- Required: `no`
- Shape: string

Optional coarse category when `declaration = conflict`.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

Participant signature over the declaration payload.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
