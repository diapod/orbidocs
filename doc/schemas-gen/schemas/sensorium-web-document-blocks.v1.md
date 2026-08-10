# Sensorium Web Document Blocks v1

Source schema: [`doc/schemas/sensorium-web-document-blocks.v1.schema.json`](../../schemas/sensorium-web-document-blocks.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-document-blocks.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`media/type`](#field-media-type) | `yes` | enum: `text/html`, `application/xhtml+xml`, `text/plain` |  |
| [`selected/charset`](#field-selected-charset) | `yes` | const: `utf-8` |  |
| [`title`](#field-title) | `no` | unspecified |  |
| [`byline`](#field-byline) | `no` | unspecified |  |
| [`language/claim`](#field-language-claim) | `no` | unspecified |  |
| [`blocks`](#field-blocks) | `yes` | array |  |
| [`links`](#field-links) | `yes` | array |  |
| [`text/characters`](#field-text-characters) | `yes` | integer |  |
| [`truncated`](#field-truncated) | `yes` | boolean |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |
| [`safeText`](#def-safetext) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-document-blocks.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-media-type"></a>
## `media/type`

- Required: `yes`
- Shape: enum: `text/html`, `application/xhtml+xml`, `text/plain`

<a id="field-selected-charset"></a>
## `selected/charset`

- Required: `yes`
- Shape: const: `utf-8`

<a id="field-title"></a>
## `title`

- Required: `no`
- Shape: unspecified

<a id="field-byline"></a>
## `byline`

- Required: `no`
- Shape: unspecified

<a id="field-language-claim"></a>
## `language/claim`

- Required: `no`
- Shape: unspecified

<a id="field-blocks"></a>
## `blocks`

- Required: `yes`
- Shape: array

<a id="field-links"></a>
## `links`

- Required: `yes`
- Shape: array

<a id="field-text-characters"></a>
## `text/characters`

- Required: `yes`
- Shape: integer

<a id="field-truncated"></a>
## `truncated`

- Required: `yes`
- Shape: boolean

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string

<a id="def-safetext"></a>
## `$defs.safeText`

- Shape: string
