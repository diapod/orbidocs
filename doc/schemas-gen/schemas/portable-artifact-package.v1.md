# Portable Artifact Package v1

Source schema: [`doc/schemas/portable-artifact-package.v1.schema.json`](../../schemas/portable-artifact-package.v1.schema.json)

Content-neutral framing for one inline artifact or one bounded manifest of inline files. The package carries no artifact schema, authority, classification, provenance, admission, retention, or publication semantics.

## Governing Basis

- [`doc/project/40-proposals/088-pull-based-artifact-acquisition.md`](../../project/40-proposals/088-pull-based-artifact-acquisition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `portable-artifact-package.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`package/layout`](#field-package-layout) | `yes` | enum: `inline`, `manifest` |  |
| [`content/encoding`](#field-content-encoding) | `no` | const: `base64url` |  |
| [`content/digest`](#field-content-digest) | `no` | ref: `#/$defs/digest` |  |
| [`content/size`](#field-content-size) | `no` | ref: `#/$defs/size` |  |
| [`content/inline`](#field-content-inline) | `no` | ref: `#/$defs/encoded` |  |
| [`manifest/root`](#field-manifest-root) | `no` | ref: `#/$defs/relativePath` |  |
| [`manifest/digest`](#field-manifest-digest) | `no` | ref: `#/$defs/digest` |  |
| [`manifest/size`](#field-manifest-size) | `no` | integer |  |
| [`manifest/entries`](#field-manifest-entries) | `no` | array |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`size`](#def-size) | integer |  |
| [`encoded`](#def-encoded) | string |  |
| [`relativePath`](#def-relativepath) | string |  |
| [`entry`](#def-entry) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "package/layout": {
      "const": "inline"
    }
  }
}
```

Then:

```json
{
  "required": [
    "content/encoding",
    "content/digest",
    "content/size",
    "content/inline"
  ],
  "not": {
    "anyOf": [
      {
        "required": [
          "manifest/root"
        ]
      },
      {
        "required": [
          "manifest/digest"
        ]
      },
      {
        "required": [
          "manifest/size"
        ]
      },
      {
        "required": [
          "manifest/entries"
        ]
      }
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `portable-artifact-package.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-package-layout"></a>
## `package/layout`

- Required: `yes`
- Shape: enum: `inline`, `manifest`

<a id="field-content-encoding"></a>
## `content/encoding`

- Required: `no`
- Shape: const: `base64url`

<a id="field-content-digest"></a>
## `content/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-content-size"></a>
## `content/size`

- Required: `no`
- Shape: ref: `#/$defs/size`

<a id="field-content-inline"></a>
## `content/inline`

- Required: `no`
- Shape: ref: `#/$defs/encoded`

<a id="field-manifest-root"></a>
## `manifest/root`

- Required: `no`
- Shape: ref: `#/$defs/relativePath`

<a id="field-manifest-digest"></a>
## `manifest/digest`

- Required: `no`
- Shape: ref: `#/$defs/digest`

<a id="field-manifest-size"></a>
## `manifest/size`

- Required: `no`
- Shape: integer

<a id="field-manifest-entries"></a>
## `manifest/entries`

- Required: `no`
- Shape: array

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-size"></a>
## `$defs.size`

- Shape: integer

<a id="def-encoded"></a>
## `$defs.encoded`

- Shape: string

<a id="def-relativepath"></a>
## `$defs.relativePath`

- Shape: string

<a id="def-entry"></a>
## `$defs.entry`

- Shape: object
