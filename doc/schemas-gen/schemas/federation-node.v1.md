# Federation Node v1

Source schema: [`doc/schemas/federation-node.v1.schema.json`](../../schemas/federation-node.v1.schema.json)

Redacted per-slot node entry retained in a federation acceptance run manifest.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `federation-node.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/id`](#field-run-id) | `yes` | ref: `#/$defs/runId` |  |
| [`node/ref`](#field-node-ref) | `yes` | ref: `#/$defs/token` |  |
| [`node/id`](#field-node-id) | `no` | string |  |
| [`data-dir/ref`](#field-data-dir-ref) | `yes` | string |  |
| [`product/endpoints`](#field-product-endpoints) | `yes` | array |  |
| [`services`](#field-services) | `yes` | ref: `#/$defs/tokenList` |  |
| [`capabilities`](#field-capabilities) | `yes` | ref: `#/$defs/tokenList` |  |
| [`model/binding`](#field-model-binding) | `no` | ref: `#/$defs/modelBindingEvidence` |  |
| [`model/revalidation`](#field-model-revalidation) | `no` | ref: `#/$defs/revalidationEvidence` |  |
| [`vfkit/preparation`](#field-vfkit-preparation) | `no` | ref: `#/$defs/vfkitPreparationEvidence` |  |
| [`vfkit/cleanup`](#field-vfkit-cleanup) | `no` | ref: `#/$defs/vfkitCleanupEvidence` |  |
| [`storage/policies`](#field-storage-policies) | `no` | array |  |
| [`storage/revalidation`](#field-storage-revalidation) | `no` | ref: `#/$defs/revalidationEvidence` |  |
| [`status`](#field-status) | `yes` | enum: `planned`, `running`, `passed`, `failed`, `refused`, `unavailable` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`runId`](#def-runid) | string |  |
| [`token`](#def-token) | string |  |
| [`tokenList`](#def-tokenlist) | array |  |
| [`digest`](#def-digest) | string |  |
| [`rawDigest`](#def-rawdigest) | string |  |
| [`revalidationEvidence`](#def-revalidationevidence) | object |  |
| [`modelBindingEvidence`](#def-modelbindingevidence) | object |  |
| [`vfkitPreparationEvidence`](#def-vfkitpreparationevidence) | object |  |
| [`vfkitCleanupEvidence`](#def-vfkitcleanupevidence) | object |  |
| [`storagePolicyEvidence`](#def-storagepolicyevidence) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federation-node.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-id"></a>
## `run/id`

- Required: `yes`
- Shape: ref: `#/$defs/runId`

<a id="field-node-ref"></a>
## `node/ref`

- Required: `yes`
- Shape: ref: `#/$defs/token`

<a id="field-node-id"></a>
## `node/id`

- Required: `no`
- Shape: string

<a id="field-data-dir-ref"></a>
## `data-dir/ref`

- Required: `yes`
- Shape: string

<a id="field-product-endpoints"></a>
## `product/endpoints`

- Required: `yes`
- Shape: array

<a id="field-services"></a>
## `services`

- Required: `yes`
- Shape: ref: `#/$defs/tokenList`

<a id="field-capabilities"></a>
## `capabilities`

- Required: `yes`
- Shape: ref: `#/$defs/tokenList`

<a id="field-model-binding"></a>
## `model/binding`

- Required: `no`
- Shape: ref: `#/$defs/modelBindingEvidence`

<a id="field-model-revalidation"></a>
## `model/revalidation`

- Required: `no`
- Shape: ref: `#/$defs/revalidationEvidence`

<a id="field-vfkit-preparation"></a>
## `vfkit/preparation`

- Required: `no`
- Shape: ref: `#/$defs/vfkitPreparationEvidence`

<a id="field-vfkit-cleanup"></a>
## `vfkit/cleanup`

- Required: `no`
- Shape: ref: `#/$defs/vfkitCleanupEvidence`

<a id="field-storage-policies"></a>
## `storage/policies`

- Required: `no`
- Shape: array

<a id="field-storage-revalidation"></a>
## `storage/revalidation`

- Required: `no`
- Shape: ref: `#/$defs/revalidationEvidence`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `planned`, `running`, `passed`, `failed`, `refused`, `unavailable`

## Definition Semantics

<a id="def-runid"></a>
## `$defs.runId`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-tokenlist"></a>
## `$defs.tokenList`

- Shape: array

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-rawdigest"></a>
## `$defs.rawDigest`

- Shape: string

<a id="def-revalidationevidence"></a>
## `$defs.revalidationEvidence`

- Shape: object

<a id="def-modelbindingevidence"></a>
## `$defs.modelBindingEvidence`

- Shape: object

<a id="def-vfkitpreparationevidence"></a>
## `$defs.vfkitPreparationEvidence`

- Shape: object

<a id="def-vfkitcleanupevidence"></a>
## `$defs.vfkitCleanupEvidence`

- Shape: object

<a id="def-storagepolicyevidence"></a>
## `$defs.storagePolicyEvidence`

- Shape: object
