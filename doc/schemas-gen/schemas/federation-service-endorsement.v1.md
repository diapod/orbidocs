# Federation Service Endorsement v1

Source schema: [`doc/schemas/federation-service-endorsement.v1.schema.json`](../../schemas/federation-service-endorsement.v1.schema.json)

Signed federation-level vouch that a service node is official for one capability in one federation. This artifact is the official-status proof; `capability-passport.v1` remains the scope/advertisement artifact. The endorsement names the sovereign subject explicitly through `endorser_subject_ref` so verifiers know which active federation-root subject and custody policy to evaluate. Runtime verification checks signatures, active `identity.sovereign_subject_refs[]`, participant/org custody semantics, expiry, revocation, and local endorsement-multiplicity policy.

## Governing Basis

- [`doc/project/40-proposals/076-federation-identity-and-network-selector.md`](../../project/40-proposals/076-federation-identity-and-network-selector.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)

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
| [`schema`](#field-schema) | `yes` | const: `federation-service-endorsement.v1` | Schema discriminator. MUST be exactly `federation-service-endorsement.v1`. |
| [`endorsement_id`](#field-endorsement-id) | `yes` | string | Stable identifier for this endorsement. Revocation records target this value. |
| [`federation_id`](#field-federation-id) | `yes` | string | Federation selector whose active federation-root is used to resolve `endorser_subject_ref`. |
| [`node_id`](#field-node-id) | `yes` | string | Service node being endorsed. MUST match the capability registration / service being consumed. |
| [`capability_id`](#field-capability-id) | `yes` | string | Capability for which this node is federation-official, e.g. `seed-directory`, `offer-catalog`, or `network-ledger`. |
| [`endorser_subject_ref`](#field-endorser-subject-ref) | `yes` | string | Sovereign subject from the active federation root that vouches for the service. Participant subjects require their own key as the sole signer; org subjects require the signer set to satisfy that org's federation-root custody policy. |
| [`issued_at`](#field-issued-at) | `yes` | string | RFC 3339 issuance timestamp. Diagnostic; expiry and revocation determine validity. |
| [`expires_at`](#field-expires-at) | `yes` | string | RFC 3339 expiry timestamp. Verifiers MUST reject endorsements at or after this time. |
| [`policy_ref`](#field-policy-ref) | `no` | string | Optional policy document governing this endorsement. Informational unless a local verifier policy binds it. |
| [`revocation_ref`](#field-revocation-ref) | `no` | string | Optional revocation feed reference where endorsement revocations are expected to appear. |
| [`signatures`](#field-signatures) | `yes` | array | One or more Ed25519 signatures over the canonical endorsement payload with `signatures` omitted. Runtime verification enforces unique signing keys and participant/org custody thresholds. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`Signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `federation-service-endorsement.v1`

Schema discriminator. MUST be exactly `federation-service-endorsement.v1`.

<a id="field-endorsement-id"></a>
## `endorsement_id`

- Required: `yes`
- Shape: string

Stable identifier for this endorsement. Revocation records target this value.

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

Federation selector whose active federation-root is used to resolve `endorser_subject_ref`.

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

Service node being endorsed. MUST match the capability registration / service being consumed.

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: string

Capability for which this node is federation-official, e.g. `seed-directory`, `offer-catalog`, or `network-ledger`.

<a id="field-endorser-subject-ref"></a>
## `endorser_subject_ref`

- Required: `yes`
- Shape: string

Sovereign subject from the active federation root that vouches for the service. Participant subjects require their own key as the sole signer; org subjects require the signer set to satisfy that org's federation-root custody policy.

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

RFC 3339 issuance timestamp. Diagnostic; expiry and revocation determine validity.

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

RFC 3339 expiry timestamp. Verifiers MUST reject endorsements at or after this time.

<a id="field-policy-ref"></a>
## `policy_ref`

- Required: `no`
- Shape: string

Optional policy document governing this endorsement. Informational unless a local verifier policy binds it.

<a id="field-revocation-ref"></a>
## `revocation_ref`

- Required: `no`
- Shape: string

Optional revocation feed reference where endorsement revocations are expected to appear.

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

One or more Ed25519 signatures over the canonical endorsement payload with `signatures` omitted. Runtime verification enforces unique signing keys and participant/org custody thresholds.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.Signature`

- Shape: object
