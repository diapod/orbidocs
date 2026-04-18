# Sensorium Directive Outcome v1

Source schema: [`doc/schemas/sensorium-directive-outcome.v1.schema.json`](../../schemas/sensorium-directive-outcome.v1.schema.json)

Audit-only outcome record for a sensorium-directive.v1. Exactly one outcome record exists for every directive, including rejected, failed, timed_out, and completed directives. Outcome records are not published to local Agora observation topics and are reachable only through host-owned audit capabilities.

## Governing Basis

- [`doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`](../../project/40-proposals/045-sensorium-local-enaction-stratum.md)
- [`doc/project/40-proposals/032-key-delegation-passports.md`](../../project/40-proposals/032-key-delegation-passports.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-directive-outcome.v1` | Schema tag for the v1 Sensorium contract. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`outcome/id`](#field-outcome-id) | `yes` | string | Opaque audit outcome id assigned by sensorium-core; recommended to be ULID-prefixed. |
| [`directive/id`](#field-directive-id) | `yes` | string | Identifier of the originating sensorium-directive.v1. |
| [`correlation/id`](#field-correlation-id) | `no` | string | Optional opaque id threading this directive outcome through a higher-level plan or workflow. |
| [`outcome/status`](#field-outcome-status) | `yes` | enum: `admitted`, `completed`, `failed`, `timed_out`, `rejected` | Directive outcome status. admitted is used for async acceptance before final execution result is known. |
| [`outcome/recorded_at`](#field-outcome-recorded-at) | `yes` | string | RFC 3339 timestamp at which sensorium-core wrote the outcome record. |
| [`directive/issued_at`](#field-directive-issued-at) | `no` | string | RFC 3339 timestamp copied from the directive when available. |
| [`started_at`](#field-started-at) | `no` | string | Connector-reported execution start timestamp, when available. This is connector telemetry, not the source/instrument event time; facts observed in the world belong in linked sensorium-observation.v1 records. |
| [`completed_at`](#field-completed-at) | `no` | string | Connector-reported execution completion timestamp, when available. sensorium-core receipt of the connector response is recorded separately as connector/responded_at. |
| [`duration_ms`](#field-duration-ms) | `no` | integer | Connector-reported or sensorium-core-measured execution duration when available. Implementations SHOULD document which clock pair was used when precision matters. |
| [`issuer`](#field-issuer) | `yes` | object | Identity of the invoking party copied from the directive. participant/did:key is the sovereign identity axis; module_id identifies the local module when applicable. |
| [`action_id`](#field-action-id) | `yes` | string | Public action id invoked by the consumer. |
| [`connector/id`](#field-connector-id) | `no` | string | Connector module id selected by sensorium-core after allowlist resolution. Absent for directives rejected before connector selection. |
| [`connector/kind`](#field-connector-kind) | `no` | string | Connector kind/class label, e.g. OS. |
| [`allowlist/ref`](#field-allowlist-ref) | `no` | object | Reference to the operator-signed allowlist entry used for admission. |
| [`policy/decision`](#field-policy-decision) | `no` | object | Sensorium policy decision summary for admission, rejection, timeout, or failure. |
| [`retry/attempts`](#field-retry-attempts) | `no` | integer | Number of execution attempts made for this directive outcome. Zero is valid for rejection before execution. |
| [`result/summary`](#field-result-summary) | `no` | unspecified | Optional compact result summary. Full typed results remain action-specific and may be returned through sensorium-directive-result.v1 or artifact references. |
| [`observation/ids`](#field-observation-ids) | `no` | array | Ids of sensorium-observation.v1 records emitted because the directive produced facts about the world. Empty or absent when no world-fact observation was produced. |
| [`artifacts`](#field-artifacts) | `no` | array | References to artifacts produced by the directive, such as stdout, stderr, generated files, or raw signal captures, using the minimal artifact-lane contract from proposal 045. |
| [`diagnostics`](#field-diagnostics) | `no` | array | Structured diagnostics from sensorium-core or the connector. These are audit hints, not observation records. |
| [`issuer_delegation`](#field-issuer-delegation) | `no` | ref: `#/$defs/delegationProof` | Optional proposal-032 DelegationProof copied from the originating directive when the directive was signed by a proxy key. Outcome verification policy treats this as part of the directive audit chain; Sensorium v1 accepts only max_chain_depth=0. |
| [`audit/store`](#field-audit-store) | `no` | object | Optional host-owned audit sink reference. Directive outcomes are written to the Node-owned module store behind restricted sensorium.audit.* capabilities, not to local Agora observation topics. |
| [`connector/dispatched_at`](#field-connector-dispatched-at) | `no` | string | RFC 3339 timestamp when sensorium-core dispatched the admitted directive to the selected connector. Absent when the directive was rejected before connector selection. |
| [`connector/responded_at`](#field-connector-responded-at) | `no` | string | RFC 3339 timestamp when sensorium-core received the terminal connector response. Absent when the connector did not respond before timing.timeout_ms expired. |
| [`directive/signature_digest`](#field-directive-signature-digest) | `no` | string | Optional sha256 digest of the originating directive signature bytes, using the canonical signature value exactly as verified by sensorium-core. Preserves audit linkage without duplicating the full signature in the outcome record. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifactRef`](#def-artifactref) | object | Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference. |
| [`delegationProof`](#def-delegationproof) | object | Compact DelegationProof from proposal 032. In Sensorium v1 the proof may be present, but sub-delegation chains are not supported; max_chain_depth, when present, MUST be 0. Additional fields are tolerated for open-world forward compatibility; the canonical proof payload verified by implementations is limited to the proposal-032 compact proof fields. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-directive-outcome.v1`

Schema tag for the v1 Sensorium contract.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-outcome-id"></a>
## `outcome/id`

- Required: `yes`
- Shape: string

Opaque audit outcome id assigned by sensorium-core; recommended to be ULID-prefixed.

<a id="field-directive-id"></a>
## `directive/id`

- Required: `yes`
- Shape: string

Identifier of the originating sensorium-directive.v1.

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

Optional opaque id threading this directive outcome through a higher-level plan or workflow.

<a id="field-outcome-status"></a>
## `outcome/status`

- Required: `yes`
- Shape: enum: `admitted`, `completed`, `failed`, `timed_out`, `rejected`

Directive outcome status. admitted is used for async acceptance before final execution result is known.

<a id="field-outcome-recorded-at"></a>
## `outcome/recorded_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which sensorium-core wrote the outcome record.

<a id="field-directive-issued-at"></a>
## `directive/issued_at`

- Required: `no`
- Shape: string

RFC 3339 timestamp copied from the directive when available.

<a id="field-started-at"></a>
## `started_at`

- Required: `no`
- Shape: string

Connector-reported execution start timestamp, when available. This is connector telemetry, not the source/instrument event time; facts observed in the world belong in linked sensorium-observation.v1 records.

<a id="field-completed-at"></a>
## `completed_at`

- Required: `no`
- Shape: string

Connector-reported execution completion timestamp, when available. sensorium-core receipt of the connector response is recorded separately as connector/responded_at.

<a id="field-duration-ms"></a>
## `duration_ms`

- Required: `no`
- Shape: integer

Connector-reported or sensorium-core-measured execution duration when available. Implementations SHOULD document which clock pair was used when precision matters.

<a id="field-issuer"></a>
## `issuer`

- Required: `yes`
- Shape: object

Identity of the invoking party copied from the directive. participant/did:key is the sovereign identity axis; module_id identifies the local module when applicable.

<a id="field-action-id"></a>
## `action_id`

- Required: `yes`
- Shape: string

Public action id invoked by the consumer.

<a id="field-connector-id"></a>
## `connector/id`

- Required: `no`
- Shape: string

Connector module id selected by sensorium-core after allowlist resolution. Absent for directives rejected before connector selection.

<a id="field-connector-kind"></a>
## `connector/kind`

- Required: `no`
- Shape: string

Connector kind/class label, e.g. OS.

<a id="field-allowlist-ref"></a>
## `allowlist/ref`

- Required: `no`
- Shape: object

Reference to the operator-signed allowlist entry used for admission.

<a id="field-policy-decision"></a>
## `policy/decision`

- Required: `no`
- Shape: object

Sensorium policy decision summary for admission, rejection, timeout, or failure.

<a id="field-retry-attempts"></a>
## `retry/attempts`

- Required: `no`
- Shape: integer

Number of execution attempts made for this directive outcome. Zero is valid for rejection before execution.

<a id="field-result-summary"></a>
## `result/summary`

- Required: `no`
- Shape: unspecified

Optional compact result summary. Full typed results remain action-specific and may be returned through sensorium-directive-result.v1 or artifact references.

<a id="field-observation-ids"></a>
## `observation/ids`

- Required: `no`
- Shape: array

Ids of sensorium-observation.v1 records emitted because the directive produced facts about the world. Empty or absent when no world-fact observation was produced.

<a id="field-artifacts"></a>
## `artifacts`

- Required: `no`
- Shape: array

References to artifacts produced by the directive, such as stdout, stderr, generated files, or raw signal captures, using the minimal artifact-lane contract from proposal 045.

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: array

Structured diagnostics from sensorium-core or the connector. These are audit hints, not observation records.

<a id="field-issuer-delegation"></a>
## `issuer_delegation`

- Required: `no`
- Shape: ref: `#/$defs/delegationProof`

Optional proposal-032 DelegationProof copied from the originating directive when the directive was signed by a proxy key. Outcome verification policy treats this as part of the directive audit chain; Sensorium v1 accepts only max_chain_depth=0.

<a id="field-audit-store"></a>
## `audit/store`

- Required: `no`
- Shape: object

Optional host-owned audit sink reference. Directive outcomes are written to the Node-owned module store behind restricted sensorium.audit.* capabilities, not to local Agora observation topics.

<a id="field-connector-dispatched-at"></a>
## `connector/dispatched_at`

- Required: `no`
- Shape: string

RFC 3339 timestamp when sensorium-core dispatched the admitted directive to the selected connector. Absent when the directive was rejected before connector selection.

<a id="field-connector-responded-at"></a>
## `connector/responded_at`

- Required: `no`
- Shape: string

RFC 3339 timestamp when sensorium-core received the terminal connector response. Absent when the connector did not respond before timing.timeout_ms expired.

<a id="field-directive-signature-digest"></a>
## `directive/signature_digest`

- Required: `no`
- Shape: string

Optional sha256 digest of the originating directive signature bytes, using the canonical signature value exactly as verified by sensorium-core. Preserves audit linkage without duplicating the full signature in the outcome record.

## Definition Semantics

<a id="def-artifactref"></a>
## `$defs.artifactRef`

- Shape: object

Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference.

<a id="def-delegationproof"></a>
## `$defs.delegationProof`

- Shape: object

Compact DelegationProof from proposal 032. In Sensorium v1 the proof may be present, but sub-delegation chains are not supported; max_chain_depth, when present, MUST be 0. Additional fields are tolerated for open-world forward compatibility; the canonical proof payload verified by implementations is limited to the proposal-032 compact proof fields.
