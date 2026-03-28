# Client Instance Recovery v1

Source schema: [`doc/schemas/client-instance-recovery.v1.schema.json`](../../schemas/client-instance-recovery.v1.schema.json)

Machine-readable schema for a pod-layer artifact that recovers client access after a detachment, device loss, migration, or other interruption, while reusing the same participant-over-channel boundary as the attachment and detachment artifacts.

## Governing Basis

- [`doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`](../../project/40-proposals/006-pod-access-layer-for-thin-clients.md)
- [`doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`](../../project/40-proposals/007-pod-identity-and-tenancy-model.md)
- [`doc/schemas/client-instance-attachment.v1.schema.json`](../../schemas/client-instance-attachment.v1.schema.json)
- [`doc/schemas/client-instance-detachment.v1.schema.json`](../../schemas/client-instance-detachment.v1.schema.json)
- [`doc/schemas/participant-bind.v1.schema.json`](../../schemas/participant-bind.v1.schema.json)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`recovery/id`](#field-recovery-id) | `yes` | string | Stable identifier of this client-instance recovery artifact. |
| [`recovered-at`](#field-recovered-at) | `yes` | string | Timestamp when the recovery path was accepted. |
| [`serving-node/id`](#field-serving-node-id) | `yes` | string | Serving node that accepts the recovered client access. |
| [`client-instance/id`](#field-client-instance-id) | `yes` | string | Concrete client, device, or install instance being recovered or re-established. |
| [`recovery/mode`](#field-recovery-mode) | `yes` | enum: `reattach-existing-device`, `replace-device`, `migrate-to-new-host`, `resume-after-suspension` | Coarse recovery mode used for the resumed client path. |
| [`recovery/from-detachment-id`](#field-recovery-from-detachment-id) | `yes` | string | Reference to the detachment artifact or equivalent termination event being recovered from. |
| [`recovery/token-ref`](#field-recovery-token-ref) | `no` | string | Optional reference to a migration bundle, export token, or recovery token used in the process. |
| [`participant-bind`](#field-participant-bind) | `yes` | ref: `participant-bind.v1.schema.json` | Participant-scoped bind proving who is resuming access over the already established channel. |
| [`proof/node-attestation`](#field-proof-node-attestation) | `no` | ref: `#/$defs/signature` | Optional future-facing serving-node attestation over the recovery artifact. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation policy annotations that do not change the core recovery semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-recovery-id"></a>
## `recovery/id`

- Required: `yes`
- Shape: string

Stable identifier of this client-instance recovery artifact.

<a id="field-recovered-at"></a>
## `recovered-at`

- Required: `yes`
- Shape: string

Timestamp when the recovery path was accepted.

<a id="field-serving-node-id"></a>
## `serving-node/id`

- Required: `yes`
- Shape: string

Serving node that accepts the recovered client access.

<a id="field-client-instance-id"></a>
## `client-instance/id`

- Required: `yes`
- Shape: string

Concrete client, device, or install instance being recovered or re-established.

<a id="field-recovery-mode"></a>
## `recovery/mode`

- Required: `yes`
- Shape: enum: `reattach-existing-device`, `replace-device`, `migrate-to-new-host`, `resume-after-suspension`

Coarse recovery mode used for the resumed client path.

<a id="field-recovery-from-detachment-id"></a>
## `recovery/from-detachment-id`

- Required: `yes`
- Shape: string

Reference to the detachment artifact or equivalent termination event being recovered from.

<a id="field-recovery-token-ref"></a>
## `recovery/token-ref`

- Required: `no`
- Shape: string

Optional reference to a migration bundle, export token, or recovery token used in the process.

<a id="field-participant-bind"></a>
## `participant-bind`

- Required: `yes`
- Shape: ref: `participant-bind.v1.schema.json`

Participant-scoped bind proving who is resuming access over the already established channel.

<a id="field-proof-node-attestation"></a>
## `proof/node-attestation`

- Required: `no`
- Shape: ref: `#/$defs/signature`

Optional future-facing serving-node attestation over the recovery artifact.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation policy annotations that do not change the core recovery semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
