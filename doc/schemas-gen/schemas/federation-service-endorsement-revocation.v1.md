# Federation Service Endorsement Revocation v1

Source schema: [`doc/schemas/federation-service-endorsement-revocation.v1.schema.json`](../../schemas/federation-service-endorsement-revocation.v1.schema.json)

Signed federation-level withdrawal of one `federation-service-endorsement.v1` artifact. The revocation targets one endorsement id and repeats its federation, node, and capability coordinates so verifiers can refuse cross-scope revocation attempts before signature evaluation.

## Governing Basis

- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/076-federation-identity-and-network-selector.md`](../../project/40-proposals/076-federation-identity-and-network-selector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `federation-service-endorsement-revocation.v1` | Schema discriminator. MUST be exactly `federation-service-endorsement-revocation.v1`. |
| [`revocation_id`](#field-revocation-id) | `yes` | string | Stable id for this revocation fact. |
| [`endorsement_id`](#field-endorsement-id) | `yes` | string | The exact endorsement artifact being withdrawn. |
| [`federation_id`](#field-federation-id) | `yes` | string | Federation whose active sovereign subjects authorize this withdrawal. |
| [`node_id`](#field-node-id) | `yes` | string | Service node named by the revoked endorsement. |
| [`capability_id`](#field-capability-id) | `yes` | string | Capability named by the revoked endorsement. |
| [`revoker_subject_ref`](#field-revoker-subject-ref) | `yes` | string | Sovereign participant or org subject authorized by the active federation root to withdraw the endorsement. |
| [`revoked_at`](#field-revoked-at) | `yes` | string | RFC 3339 timestamp when the revoker issued this withdrawal. |
| [`reason`](#field-reason) | `no` | string | Optional operator-facing reason reference or terse reason code. |
| [`signatures`](#field-signatures) | `yes` | array | One or more Ed25519 signatures over `federation-service-endorsement-revocation.v1\x00 \|\| canonical_json(payload_without_signatures)`. Org revocation is fail-safe: one authorized custodian may withdraw official status. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`Signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federation-service-endorsement-revocation.v1`

Schema discriminator. MUST be exactly `federation-service-endorsement-revocation.v1`.

<a id="field-revocation-id"></a>
## `revocation_id`

- Required: `yes`
- Shape: string

Stable id for this revocation fact.

<a id="field-endorsement-id"></a>
## `endorsement_id`

- Required: `yes`
- Shape: string

The exact endorsement artifact being withdrawn.

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

Federation whose active sovereign subjects authorize this withdrawal.

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

Service node named by the revoked endorsement.

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: string

Capability named by the revoked endorsement.

<a id="field-revoker-subject-ref"></a>
## `revoker_subject_ref`

- Required: `yes`
- Shape: string

Sovereign participant or org subject authorized by the active federation root to withdraw the endorsement.

<a id="field-revoked-at"></a>
## `revoked_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp when the revoker issued this withdrawal.

<a id="field-reason"></a>
## `reason`

- Required: `no`
- Shape: string

Optional operator-facing reason reference or terse reason code.

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

One or more Ed25519 signatures over `federation-service-endorsement-revocation.v1\x00 || canonical_json(payload_without_signatures)`. Org revocation is fail-safe: one authorized custodian may withdraw official status.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.Signature`

- Shape: object
