# Nym Issue Request v1

Source schema: [`doc/schemas/nym-issue-request.v1.schema.json`](../../schemas/nym-issue-request.v1.schema.json)

Machine-readable schema for a participant-signed request to issue a fresh application-layer pseudonym certificate.

## Governing Basis

- [`doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`](../../project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`request/id`](#field-request-id) | `yes` | string | Stable identifier of this nym issuance request. |
| [`request/type`](#field-request-type) | `yes` | const: `nym/issue` | Application-level request discriminator. |
| [`participant/id`](#field-participant-id) | `yes` | string | Participant identity asking the council to issue the pseudonym. |
| [`nym/id`](#field-nym-id) | `yes` | string | Fresh requested pseudonym identity. In Phase 1 this remains an application-layer identity and MUST NOT leak into the transport boundary. |
| [`requested-ttl-seconds`](#field-requested-ttl-seconds) | `yes` | integer | Requested validity window in seconds. The issuer may clamp this value according to local policy. |
| [`created-at`](#field-created-at) | `yes` | string | Creation timestamp of the issuance request. |
| [`nonce`](#field-nonce) | `yes` | string | Fresh base64url-encoded 32-byte nonce used to reduce replay risk on the request path. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

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

<a id="field-request-id"></a>
## `request/id`

- Required: `yes`
- Shape: string

Stable identifier of this nym issuance request.

<a id="field-request-type"></a>
## `request/type`

- Required: `yes`
- Shape: const: `nym/issue`

Application-level request discriminator.

<a id="field-participant-id"></a>
## `participant/id`

- Required: `yes`
- Shape: string

Participant identity asking the council to issue the pseudonym.

<a id="field-nym-id"></a>
## `nym/id`

- Required: `yes`
- Shape: string

Fresh requested pseudonym identity. In Phase 1 this remains an application-layer identity and MUST NOT leak into the transport boundary.

<a id="field-requested-ttl-seconds"></a>
## `requested-ttl-seconds`

- Required: `yes`
- Shape: integer

Requested validity window in seconds. The issuer may clamp this value according to local policy.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Creation timestamp of the issuance request.

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string

Fresh base64url-encoded 32-byte nonce used to reduce replay risk on the request path.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
