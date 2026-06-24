# Topic Taxonomy v1

Source schema: [`doc/schemas/topic-taxonomy.v1.schema.json`](../../schemas/topic-taxonomy.v1.schema.json)

Signed, versioned taxonomy material used by Corpus topic resolution and topic-scoped service-offer indexing. The taxonomy is protocol mechanics, not federation-local preference text.

## Governing Basis

- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`taxonomy/id`](#field-taxonomy-id) | `yes` | string |  |
| [`federation/id`](#field-federation-id) | `yes` | string |  |
| [`version`](#field-version) | `yes` | string |  |
| [`versioning/scheme`](#field-versioning-scheme) | `yes` | enum: `calver`, `semver`, `sequence` |  |
| [`digest`](#field-digest) | `yes` | ref: `#/$defs/sha256_digest` |  |
| [`issuer/nym`](#field-issuer-nym) | `yes` | string |  |
| [`issuer/public-key-ref`](#field-issuer-public-key-ref) | `no` | string |  |
| [`valid/from`](#field-valid-from) | `yes` | string |  |
| [`valid/until`](#field-valid-until) | `yes` | string |  |
| [`supersedes`](#field-supersedes) | `no` | ref: `#/$defs/sha256_digest` |  |
| [`supersession/proof`](#field-supersession-proof) | `no` | ref: `#/$defs/signature` |  |
| [`extension/policy`](#field-extension-policy) | `no` | object |  |
| [`nodes`](#field-nodes) | `yes` | array |  |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`extensions`](#field-extensions) | `no` | ref: `#/$defs/extensions` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`sha256_digest`](#def-sha256-digest) | string |  |
| [`topic_term`](#def-topic-term) | string |  |
| [`topic_node`](#def-topic-node) | object |  |
| [`signature`](#def-signature) | object |  |
| [`extensions`](#def-extensions) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-taxonomy-id"></a>
## `taxonomy/id`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

<a id="field-version"></a>
## `version`

- Required: `yes`
- Shape: string

<a id="field-versioning-scheme"></a>
## `versioning/scheme`

- Required: `yes`
- Shape: enum: `calver`, `semver`, `sequence`

<a id="field-digest"></a>
## `digest`

- Required: `yes`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-issuer-nym"></a>
## `issuer/nym`

- Required: `yes`
- Shape: string

<a id="field-issuer-public-key-ref"></a>
## `issuer/public-key-ref`

- Required: `no`
- Shape: string

<a id="field-valid-from"></a>
## `valid/from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid/until`

- Required: `yes`
- Shape: string

<a id="field-supersedes"></a>
## `supersedes`

- Required: `no`
- Shape: ref: `#/$defs/sha256_digest`

<a id="field-supersession-proof"></a>
## `supersession/proof`

- Required: `no`
- Shape: ref: `#/$defs/signature`

<a id="field-extension-policy"></a>
## `extension/policy`

- Required: `no`
- Shape: object

<a id="field-nodes"></a>
## `nodes`

- Required: `yes`
- Shape: array

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `#/$defs/extensions`

## Definition Semantics

<a id="def-sha256-digest"></a>
## `$defs.sha256_digest`

- Shape: string

<a id="def-topic-term"></a>
## `$defs.topic_term`

- Shape: string

<a id="def-topic-node"></a>
## `$defs.topic_node`

- Shape: object

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-extensions"></a>
## `$defs.extensions`

- Shape: object
