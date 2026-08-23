# Bounded HTTP Fetch Result v1

Source schema: [`doc/schemas/bounded-http-fetch-result.v1.schema.json`](../../schemas/bounded-http-fetch-result.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `bounded-http-fetch-result.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`request/id`](#field-request-id) | `yes` | string |  |
| [`outcome`](#field-outcome) | `yes` | enum: `completed`, `refused`, `failed`, `unknown` |  |
| [`requested-url/digest`](#field-requested-url-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`final-url/digest`](#field-final-url-digest) | `no` | ref: `#/$defs/sha256Digest` |  |
| [`response/status`](#field-response-status) | `no` | integer |  |
| [`media/type`](#field-media-type) | `no` | string |  |
| [`declared/charset`](#field-declared-charset) | `no` | string |  |
| [`response/etag`](#field-response-etag) | `no` | string |  |
| [`response/last-modified`](#field-response-last-modified) | `no` | string |  |
| [`content/encoding`](#field-content-encoding) | `no` | enum: `identity`, `gzip` |  |
| [`compressed-bytes`](#field-compressed-bytes) | `no` | integer |  |
| [`decompressed-bytes`](#field-decompressed-bytes) | `no` | integer |  |
| [`body/digest`](#field-body-digest) | `no` | ref: `#/$defs/sha256Digest` |  |
| [`body`](#field-body) | `no` | unspecified |  |
| [`redirects/followed`](#field-redirects-followed) | `yes` | integer |  |
| [`failure`](#field-failure) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "outcome": {
      "const": "completed"
    }
  },
  "required": [
    "outcome"
  ]
}
```

Then:

```json
{
  "required": [
    "final-url/digest",
    "response/status",
    "compressed-bytes",
    "decompressed-bytes"
  ],
  "not": {
    "required": [
      "failure"
    ]
  },
  "allOf": [
    {
      "if": {
        "properties": {
          "response/status": {
            "const": 304
          }
        },
        "required": [
          "response/status"
        ]
      },
      "then": {
        "not": {
          "anyOf": [
            {
              "required": [
                "body"
              ]
            },
            {
              "required": [
                "body/digest"
              ]
            }
          ]
        }
      },
      "else": {
        "required": [
          "body/digest",
          "body"
        ]
      }
    }
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `bounded-http-fetch-result.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

<a id="field-outcome"></a>
## `outcome`

- Required: `yes`
- Shape: enum: `completed`, `refused`, `failed`, `unknown`

<a id="field-requested-url-digest"></a>
## `requested-url/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-final-url-digest"></a>
## `final-url/digest`

- Required: `no`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-response-status"></a>
## `response/status`

- Required: `no`
- Shape: integer

<a id="field-media-type"></a>
## `media/type`

- Required: `no`
- Shape: string

<a id="field-declared-charset"></a>
## `declared/charset`

- Required: `no`
- Shape: string

<a id="field-response-etag"></a>
## `response/etag`

- Required: `no`
- Shape: string

<a id="field-response-last-modified"></a>
## `response/last-modified`

- Required: `no`
- Shape: string

<a id="field-content-encoding"></a>
## `content/encoding`

- Required: `no`
- Shape: enum: `identity`, `gzip`

<a id="field-compressed-bytes"></a>
## `compressed-bytes`

- Required: `no`
- Shape: integer

<a id="field-decompressed-bytes"></a>
## `decompressed-bytes`

- Required: `no`
- Shape: integer

<a id="field-body-digest"></a>
## `body/digest`

- Required: `no`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-body"></a>
## `body`

- Required: `no`
- Shape: unspecified

<a id="field-redirects-followed"></a>
## `redirects/followed`

- Required: `yes`
- Shape: integer

<a id="field-failure"></a>
## `failure`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
