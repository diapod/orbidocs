# Issuer-admission-request.v1

Source schema: [`doc/schemas/issuer-admission-request.v1.schema.json`](../../schemas/issuer-admission-request.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md`](../../project/40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`key_public`](#field-key-public) | `yes` | string |  |
| [`node_id`](#field-node-id) | `yes` | string |  |
| [`federation_id`](#field-federation-id) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | string |  |
| [`root_digest`](#field-root-digest) | `yes` | string |  |
| [`signature`](#field-signature) | `yes` | string |  |
| [`schema`](#field-schema) | `yes` | const: `orbiplex.federation.issuer-admission-request.v1` |  |
| [`requested_role`](#field-requested-role) | `yes` | const: `sovereign-passport-issuer` |  |
| [`purpose`](#field-purpose) | `yes` | const: `federation-passport-issuance` |  |
| [`root_version`](#field-root-version) | `yes` | integer |  |
| [`issued_at`](#field-issued-at) | `yes` | string |  |
| [`expires_at`](#field-expires-at) | `yes` | string |  |
| [`nonce`](#field-nonce) | `yes` | string |  |
## Field Semantics

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-key-public"></a>
## `key_public`

- Required: `yes`
- Shape: string

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: string

<a id="field-root-digest"></a>
## `root_digest`

- Required: `yes`
- Shape: string

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: string

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `orbiplex.federation.issuer-admission-request.v1`

<a id="field-requested-role"></a>
## `requested_role`

- Required: `yes`
- Shape: const: `sovereign-passport-issuer`

<a id="field-purpose"></a>
## `purpose`

- Required: `yes`
- Shape: const: `federation-passport-issuance`

<a id="field-root-version"></a>
## `root_version`

- Required: `yes`
- Shape: integer

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

<a id="field-nonce"></a>
## `nonce`

- Required: `yes`
- Shape: string
