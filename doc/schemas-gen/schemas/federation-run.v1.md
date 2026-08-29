# Federation Run v1

Source schema: [`doc/schemas/federation-run.v1.schema.json`](../../schemas/federation-run.v1.schema.json)

Redacted aggregate manifest for one leased federation acceptance run.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `federation-run.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`run/id`](#field-run-id) | `yes` | string |  |
| [`scenario/ref`](#field-scenario-ref) | `yes` | string |  |
| [`topology/digest`](#field-topology-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | ref: `#/$defs/digest` |  |
| [`owner/slot`](#field-owner-slot) | `yes` | string |  |
| [`nodes`](#field-nodes) | `yes` | array |  |
| [`story/evidence`](#field-story-evidence) | `no` | ref: `#/$defs/storyEvidence` |  |
| [`assertions`](#field-assertions) | `no` | array |  |
| [`started/at`](#field-started-at) | `yes` | string |  |
| [`ended/at`](#field-ended-at) | `no` | string |  |
| [`status`](#field-status) | `yes` | enum: `planned`, `running`, `passed`, `failed`, `refused` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`digest`](#def-digest) | string |  |
| [`rawDigest`](#def-rawdigest) | string |  |
| [`token`](#def-token) | string |  |
| [`storyEvidence`](#def-storyevidence) | object |  |
| [`assertionResult`](#def-assertionresult) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federation-run.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-run-id"></a>
## `run/id`

- Required: `yes`
- Shape: string

<a id="field-scenario-ref"></a>
## `scenario/ref`

- Required: `yes`
- Shape: string

<a id="field-topology-digest"></a>
## `topology/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: ref: `#/$defs/digest`

<a id="field-owner-slot"></a>
## `owner/slot`

- Required: `yes`
- Shape: string

<a id="field-nodes"></a>
## `nodes`

- Required: `yes`
- Shape: array

<a id="field-story-evidence"></a>
## `story/evidence`

- Required: `no`
- Shape: ref: `#/$defs/storyEvidence`

<a id="field-assertions"></a>
## `assertions`

- Required: `no`
- Shape: array

<a id="field-started-at"></a>
## `started/at`

- Required: `yes`
- Shape: string

<a id="field-ended-at"></a>
## `ended/at`

- Required: `no`
- Shape: string

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `planned`, `running`, `passed`, `failed`, `refused`

## Definition Semantics

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-rawdigest"></a>
## `$defs.rawDigest`

- Shape: string

<a id="def-token"></a>
## `$defs.token`

- Shape: string

<a id="def-storyevidence"></a>
## `$defs.storyEvidence`

- Shape: object

<a id="def-assertionresult"></a>
## `$defs.assertionResult`

- Shape: object
