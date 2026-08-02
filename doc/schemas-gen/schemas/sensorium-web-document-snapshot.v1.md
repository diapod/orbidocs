# Sensorium Web Document Snapshot v1

Source schema: [`doc/schemas/sensorium-web-document-snapshot.v1.schema.json`](../../schemas/sensorium-web-document-snapshot.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-web-document-snapshot.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`snapshot/id`](#field-snapshot-id) | `yes` | string |  |
| [`source/ref`](#field-source-ref) | `yes` | string |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | string |  |
| [`requested-url/display`](#field-requested-url-display) | `no` | string |  |
| [`requested-url/digest`](#field-requested-url-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`final-url/display`](#field-final-url-display) | `no` | string |  |
| [`final-url/digest`](#field-final-url-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`fetched/at`](#field-fetched-at) | `yes` | string |  |
| [`response/status`](#field-response-status) | `yes` | integer |  |
| [`media/type`](#field-media-type) | `yes` | enum: `text/html`, `application/xhtml+xml`, `text/plain` |  |
| [`declared/charset`](#field-declared-charset) | `no` | string |  |
| [`selected/charset`](#field-selected-charset) | `no` | string |  |
| [`body/bytes`](#field-body-bytes) | `no` | integer |  |
| [`body/digest`](#field-body-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`body/artifact-ref`](#field-body-artifact-ref) | `no` | string |  |
| [`fetch/result-digest`](#field-fetch-result-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`extraction/profile-ref`](#field-extraction-profile-ref) | `yes` | string |  |
| [`extraction/profile-digest`](#field-extraction-profile-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`representation/digest`](#field-representation-digest) | `yes` | ref: `#/$defs/sha256Digest` |  |
| [`representation/artifact-ref`](#field-representation-artifact-ref) | `no` | string |  |
| [`title`](#field-title) | `no` | string |  |
| [`byline`](#field-byline) | `no` | string |  |
| [`language/claim`](#field-language-claim) | `no` | string |  |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |
| [`classification`](#field-classification) | `yes` | ref: `classification.v1.schema.json` |  |
| [`causal/context`](#field-causal-context) | `yes` | ref: `causal-context.v1.schema.json` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256Digest`](#def-sha256digest) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-web-document-snapshot.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-snapshot-id"></a>
## `snapshot/id`

- Required: `yes`
- Shape: string

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: string

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: string

<a id="field-requested-url-display"></a>
## `requested-url/display`

- Required: `no`
- Shape: string

<a id="field-requested-url-digest"></a>
## `requested-url/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-final-url-display"></a>
## `final-url/display`

- Required: `no`
- Shape: string

<a id="field-final-url-digest"></a>
## `final-url/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-fetched-at"></a>
## `fetched/at`

- Required: `yes`
- Shape: string

<a id="field-response-status"></a>
## `response/status`

- Required: `yes`
- Shape: integer

<a id="field-media-type"></a>
## `media/type`

- Required: `yes`
- Shape: enum: `text/html`, `application/xhtml+xml`, `text/plain`

<a id="field-declared-charset"></a>
## `declared/charset`

- Required: `no`
- Shape: string

<a id="field-selected-charset"></a>
## `selected/charset`

- Required: `no`
- Shape: string

<a id="field-body-bytes"></a>
## `body/bytes`

- Required: `no`
- Shape: integer

<a id="field-body-digest"></a>
## `body/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-body-artifact-ref"></a>
## `body/artifact-ref`

- Required: `no`
- Shape: string

<a id="field-fetch-result-digest"></a>
## `fetch/result-digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-extraction-profile-ref"></a>
## `extraction/profile-ref`

- Required: `yes`
- Shape: string

<a id="field-extraction-profile-digest"></a>
## `extraction/profile-digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-representation-digest"></a>
## `representation/digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256Digest`

<a id="field-representation-artifact-ref"></a>
## `representation/artifact-ref`

- Required: `no`
- Shape: string

<a id="field-title"></a>
## `title`

- Required: `no`
- Shape: string

<a id="field-byline"></a>
## `byline`

- Required: `no`
- Shape: string

<a id="field-language-claim"></a>
## `language/claim`

- Required: `no`
- Shape: string

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

<a id="field-classification"></a>
## `classification`

- Required: `yes`
- Shape: ref: `classification.v1.schema.json`

<a id="field-causal-context"></a>
## `causal/context`

- Required: `yes`
- Shape: ref: `causal-context.v1.schema.json`

## Definition Semantics

<a id="def-sha256digest"></a>
## `$defs.sha256Digest`

- Shape: string
