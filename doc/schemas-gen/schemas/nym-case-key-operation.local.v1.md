# Nym-case-key-operation.local.v1

Source schema: [`doc/schemas/nym-case-key-operation.local.v1.schema.json`](../../schemas/nym-case-key-operation.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md`](../../project/40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`operation`](#field-operation) | `yes` | enum: `read`, `erase`, `recovery-consent`, `provider-inspect`, `provider-replace`, `list-exposed`, `abandon` |  |
| [`continuity/key-digest`](#field-continuity-key-digest) | `no` | string |  |
| [`enabled`](#field-enabled) | `no` | boolean |  |
| [`expected/provider`](#field-expected-provider) | `no` | string |  |
| [`page/after`](#field-page-after) | `no` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "operation": {
      "enum": [
        "read",
        "erase",
        "recovery-consent",
        "abandon"
      ]
    }
  }
}
```

Then:

```json
{
  "required": [
    "continuity/key-digest"
  ],
  "not": {
    "required": [
      "expected/provider"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "operation": {
      "const": "recovery-consent"
    }
  }
}
```

Then:

```json
{
  "required": [
    "enabled"
  ]
}
```

### Rule 3

When:

```json
{
  "properties": {
    "operation": {
      "const": "provider-replace"
    }
  }
}
```

Then:

```json
{
  "required": [
    "expected/provider"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "operation": {
      "const": "list-exposed"
    }
  }
}
```

## Field Semantics

<a id="field-operation"></a>
## `operation`

- Required: `yes`
- Shape: enum: `read`, `erase`, `recovery-consent`, `provider-inspect`, `provider-replace`, `list-exposed`, `abandon`

<a id="field-continuity-key-digest"></a>
## `continuity/key-digest`

- Required: `no`
- Shape: string

<a id="field-enabled"></a>
## `enabled`

- Required: `no`
- Shape: boolean

<a id="field-expected-provider"></a>
## `expected/provider`

- Required: `no`
- Shape: string

<a id="field-page-after"></a>
## `page/after`

- Required: `no`
- Shape: string
