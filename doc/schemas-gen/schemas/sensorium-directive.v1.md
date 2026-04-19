# Sensorium Directive v1

Source schema: [`doc/schemas/sensorium-directive.v1.schema.json`](../../schemas/sensorium-directive.v1.schema.json)

Request envelope addressed to sensorium-core by a consumer module (e.g. Arca, Dator, local agent) invoking an intentional action through a Sensorium connector. Consumers address actions by a public action_id; sensorium-core resolves the action_id through the operator-signed allowlist to a specific connector.

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
| [`schema`](#field-schema) | `yes` | const: `sensorium-directive.v1` | Schema tag for the v1 Sensorium contract. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`directive/id`](#field-directive-id) | `yes` | string | Opaque identifier assigned by the issuer; recommended to be ULID. Used to correlate the request, its outcome record, and any emitted observations. |
| [`directive/issued_at`](#field-directive-issued-at) | `yes` | string | RFC 3339 timestamp at which the issuer produced this directive. |
| [`issuer`](#field-issuer) | `yes` | object | Identity of the invoking party. participant/did:key is the sovereign identity axis; module_id identifies the local module when applicable. At least one of participant/did:key or module_id MUST be present. |
| [`idempotency/key`](#field-idempotency-key) | `no` | string | Optional caller-provided idempotency key. sensorium-core SHOULD use it together with issuer and action_id to make retries of async or retryable directives safe. |
| [`action_id`](#field-action-id) | `yes` | string | Public, operator-allowlisted identifier of the action to perform (dotted notation recommended, e.g. os.process.spawn-read-only). Consumers MUST NOT select connector_id; action_id is the only public addressing handle. |
| [`parameters`](#field-parameters) | `yes` | object | Typed parameters for this action_id. Validated by sensorium-core against the parameter schema held in the allowlist entry for this action_id. MUST NOT carry raw shell strings, raw script bodies, or raw SQL; interpretive surfaces are expressed as script_id references to signed stored artifacts. |
| [`evidence/inputs`](#field-evidence-inputs) | `no` | array | Optional input artifacts, passed by reference rather than inline, using the minimal artifact-lane contract from proposal 045. |
| [`timing`](#field-timing) | `yes` | object | Directive-level timing policy. timing.timeout_ms is the end-to-end deadline enforced by sensorium-core from directive admission through connector dispatch and execution to final outcome recording. |
| [`deadline_at`](#field-deadline-at) | `no` | string | Optional absolute RFC 3339 deadline propagated by the caller. When present, sensorium-core and the connector MUST enforce the smaller of timing.timeout_ms/max_timeout_ms and the remaining time until deadline_at. This keeps role-module HTTP timeouts, Sensorium outcomes, and connector execution telemetry aligned. |
| [`correlation/id`](#field-correlation-id) | `no` | string | Optional opaque string threading this directive through a higher-level plan (e.g. an Arca workflow run step, a Dator task dispatch). Preserved in the outcome and in any linked observations. |
| [`issuer_delegation`](#field-issuer-delegation) | `no` | ref: `#/$defs/delegationProof` | Optional proposal-032 DelegationProof authorising a proxy key to sign this directive. If present, signature MUST be produced by issuer_delegation.proxy_key and issuer_delegation.principal_key MUST derive to issuer.participant/did:key. Sensorium v1 accepts only max_chain_depth=0. |
| [`signature`](#field-signature) | `no` | ref: `#/$defs/ed25519Signature` |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifactRef`](#def-artifactref) | object | Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference. |
| [`delegationProof`](#def-delegationproof) | object | Compact DelegationProof from proposal 032. In Sensorium v1 the proof may be present, but sub-delegation chains are not supported; max_chain_depth, when present, MUST be 0. Additional fields are tolerated for open-world forward compatibility; the canonical proof payload verified by implementations is limited to the proposal-032 compact proof fields. |
| [`ed25519Signature`](#def-ed25519signature) | object | Ed25519 signature over the canonical directive payload. issuer_delegation is excluded from the surrounding directive payload and has its own principal_signature. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-directive.v1`

Schema tag for the v1 Sensorium contract.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-directive-id"></a>
## `directive/id`

- Required: `yes`
- Shape: string

Opaque identifier assigned by the issuer; recommended to be ULID. Used to correlate the request, its outcome record, and any emitted observations.

<a id="field-directive-issued-at"></a>
## `directive/issued_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which the issuer produced this directive.

<a id="field-issuer"></a>
## `issuer`

- Required: `yes`
- Shape: object

Identity of the invoking party. participant/did:key is the sovereign identity axis; module_id identifies the local module when applicable. At least one of participant/did:key or module_id MUST be present.

<a id="field-idempotency-key"></a>
## `idempotency/key`

- Required: `no`
- Shape: string

Optional caller-provided idempotency key. sensorium-core SHOULD use it together with issuer and action_id to make retries of async or retryable directives safe.

<a id="field-action-id"></a>
## `action_id`

- Required: `yes`
- Shape: string

Public, operator-allowlisted identifier of the action to perform (dotted notation recommended, e.g. os.process.spawn-read-only). Consumers MUST NOT select connector_id; action_id is the only public addressing handle.

<a id="field-parameters"></a>
## `parameters`

- Required: `yes`
- Shape: object

Typed parameters for this action_id. Validated by sensorium-core against the parameter schema held in the allowlist entry for this action_id. MUST NOT carry raw shell strings, raw script bodies, or raw SQL; interpretive surfaces are expressed as script_id references to signed stored artifacts.

<a id="field-evidence-inputs"></a>
## `evidence/inputs`

- Required: `no`
- Shape: array

Optional input artifacts, passed by reference rather than inline, using the minimal artifact-lane contract from proposal 045.

<a id="field-timing"></a>
## `timing`

- Required: `yes`
- Shape: object

Directive-level timing policy. timing.timeout_ms is the end-to-end deadline enforced by sensorium-core from directive admission through connector dispatch and execution to final outcome recording.

<a id="field-deadline-at"></a>
## `deadline_at`

- Required: `no`
- Shape: string

Optional absolute RFC 3339 deadline propagated by the caller. When present, sensorium-core and the connector MUST enforce the smaller of timing.timeout_ms/max_timeout_ms and the remaining time until deadline_at. This keeps role-module HTTP timeouts, Sensorium outcomes, and connector execution telemetry aligned.

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

Optional opaque string threading this directive through a higher-level plan (e.g. an Arca workflow run step, a Dator task dispatch). Preserved in the outcome and in any linked observations.

<a id="field-issuer-delegation"></a>
## `issuer_delegation`

- Required: `no`
- Shape: ref: `#/$defs/delegationProof`

Optional proposal-032 DelegationProof authorising a proxy key to sign this directive. If present, signature MUST be produced by issuer_delegation.proxy_key and issuer_delegation.principal_key MUST derive to issuer.participant/did:key. Sensorium v1 accepts only max_chain_depth=0.

<a id="field-signature"></a>
## `signature`

- Required: `no`
- Shape: ref: `#/$defs/ed25519Signature`

## Definition Semantics

<a id="def-artifactref"></a>
## `$defs.artifactRef`

- Shape: object

Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference.

<a id="def-delegationproof"></a>
## `$defs.delegationProof`

- Shape: object

Compact DelegationProof from proposal 032. In Sensorium v1 the proof may be present, but sub-delegation chains are not supported; max_chain_depth, when present, MUST be 0. Additional fields are tolerated for open-world forward compatibility; the canonical proof payload verified by implementations is limited to the proposal-032 compact proof fields.

<a id="def-ed25519signature"></a>
## `$defs.ed25519Signature`

- Shape: object

Ed25519 signature over the canonical directive payload. issuer_delegation is excluded from the surrounding directive payload and has its own principal_signature.
