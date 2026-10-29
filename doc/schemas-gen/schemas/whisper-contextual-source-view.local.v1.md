# Whisper-contextual-source-view.local.v1

Source schema: [`doc/schemas/whisper-contextual-source-view.local.v1.schema.json`](../../schemas/whisper-contextual-source-view.local.v1.schema.json)

Authority-qualified local current annotation, separate from immutable signed claims. Freshness uses the emission lease and the unchanged complete source revision. Last evaluation is historical when freshness is unknown. Epoch closure makes the current contribution zero without rewriting claims. This read model grants no admission, signing or delivery authority.

## Governing Basis

- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline/contextual-whisper-authorship.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-contextual-source-view.local.v1` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | string |  |
| [`context/digest`](#field-context-digest) | `yes` | string |  |
| [`epoch`](#field-epoch) | `yes` | integer |  |
| [`authority`](#field-authority) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `eligible`, `below-threshold`, `freshness-unknown`, `epoch-ended` |  |
| [`freshness`](#field-freshness) | `yes` | enum: `fresh`, `unknown` |  |
| [`current/sources`](#field-current-sources) | `yes` | unspecified |  |
| [`last-evaluation`](#field-last-evaluation) | `yes` | unspecified |  |
| [`first-emission`](#field-first-emission) | `yes` | unspecified |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "state": {
      "const": "eligible"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "freshness": {
      "const": "fresh"
    },
    "current/sources": {
      "type": "integer",
      "minimum": 2,
      "maximum": 4096
    },
    "last-evaluation": {
      "type": "object"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "state": {
      "const": "below-threshold"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "freshness": {
      "const": "fresh"
    },
    "current/sources": {
      "type": "integer",
      "minimum": 0,
      "maximum": 1
    },
    "last-evaluation": {
      "type": "object"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "state": {
      "const": "freshness-unknown"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "freshness": {
      "const": "unknown"
    },
    "current/sources": {
      "type": "null"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "state": {
      "const": "epoch-ended"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "freshness": {
      "const": "unknown"
    },
    "current/sources": {
      "const": 0
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-contextual-source-view.local.v1`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: string

<a id="field-context-digest"></a>
## `context/digest`

- Required: `yes`
- Shape: string

<a id="field-epoch"></a>
## `epoch`

- Required: `yes`
- Shape: integer

<a id="field-authority"></a>
## `authority`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `eligible`, `below-threshold`, `freshness-unknown`, `epoch-ended`

<a id="field-freshness"></a>
## `freshness`

- Required: `yes`
- Shape: enum: `fresh`, `unknown`

<a id="field-current-sources"></a>
## `current/sources`

- Required: `yes`
- Shape: unspecified

<a id="field-last-evaluation"></a>
## `last-evaluation`

- Required: `yes`
- Shape: unspecified

<a id="field-first-emission"></a>
## `first-emission`

- Required: `yes`
- Shape: unspecified
