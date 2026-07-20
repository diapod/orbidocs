# Sensorium Interface Resource v1

Source schema: [`doc/schemas/sensorium-interface-resource.v1.schema.json`](../../schemas/sensorium-interface-resource.v1.schema.json)

Direction-neutral identity, ownership, classification, source generation, operational context, and lifetime fields shared by observation and actuation descriptors.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-interface-resource.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`interface/id`](#field-interface-id) | `yes` | ref: `#/$defs/interface_ref` |  |
| [`interface/kind`](#field-interface-kind) | `yes` | enum: `observation`, `actuation` |  |
| [`interface/name`](#field-interface-name) | `yes` | string |  |
| [`publisher/node-ref`](#field-publisher-node-ref) | `yes` | string |  |
| [`classification/max-tier`](#field-classification-max-tier) | `yes` | enum: `Public`, `Community`, `Personal` |  |
| [`classification/topic-class`](#field-classification-topic-class) | `yes` | string |  |
| [`redaction/profile-ref`](#field-redaction-profile-ref) | `no` | ref: `#/$defs/ref` |  |
| [`source/generation-ref`](#field-source-generation-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`operational/context`](#field-operational-context) | `yes` | ref: `sensorium-operational-context.v1.schema.json` |  |
| [`supersedes/interface-id`](#field-supersedes-interface-id) | `no` | ref: `#/$defs/interface_ref` |  |
| [`published/at`](#field-published-at) | `yes` | string |  |
| [`expires/at`](#field-expires-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`interface_ref`](#def-interface-ref) | string |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-interface-resource.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-interface-id"></a>
## `interface/id`

- Required: `yes`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-interface-kind"></a>
## `interface/kind`

- Required: `yes`
- Shape: enum: `observation`, `actuation`

<a id="field-interface-name"></a>
## `interface/name`

- Required: `yes`
- Shape: string

<a id="field-publisher-node-ref"></a>
## `publisher/node-ref`

- Required: `yes`
- Shape: string

<a id="field-classification-max-tier"></a>
## `classification/max-tier`

- Required: `yes`
- Shape: enum: `Public`, `Community`, `Personal`

<a id="field-classification-topic-class"></a>
## `classification/topic-class`

- Required: `yes`
- Shape: string

<a id="field-redaction-profile-ref"></a>
## `redaction/profile-ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-source-generation-ref"></a>
## `source/generation-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-operational-context"></a>
## `operational/context`

- Required: `yes`
- Shape: ref: `sensorium-operational-context.v1.schema.json`

<a id="field-supersedes-interface-id"></a>
## `supersedes/interface-id`

- Required: `no`
- Shape: ref: `#/$defs/interface_ref`

<a id="field-published-at"></a>
## `published/at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires/at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-interface-ref"></a>
## `$defs.interface_ref`

- Shape: string
