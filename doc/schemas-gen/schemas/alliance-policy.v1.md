# Alliance Policy v1

Source schema: [`doc/schemas/alliance-policy.v1.schema.json`](../../schemas/alliance-policy.v1.schema.json)

Unilateral cross-federation alliance declaration. A cooperation relationship is operationally active only when all member federations hold fresh matching halves; the effective scope is the intersection of allowed_scopes minus any denied_scopes. Member root digests are evidence only, not validity pins. Runtime verification must re-check issuer and member subjects against active federation roots before use.

## Governing Basis

- [`doc/project/40-proposals/079-cross-federation-alliance.md`](../../project/40-proposals/079-cross-federation-alliance.md)
- [`doc/project/40-proposals/076-federation-identity-and-network-selector.md`](../../project/40-proposals/076-federation-identity-and-network-selector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fixtures

### Valid Fixtures

- [`doc/schemas/examples/orbiplex-main-research-eu.alliance-policy.json`](../../schemas/examples/orbiplex-main-research-eu.alliance-policy.json)

### Invalid Fixtures

- [`doc/schemas/examples/invalid/duplicate-signature.alliance-policy.json`](../../schemas/examples/invalid/duplicate-signature.alliance-policy.json)
- [`doc/schemas/examples/invalid/unknown-scope.alliance-policy.json`](../../schemas/examples/invalid/unknown-scope.alliance-policy.json)
- [`doc/schemas/examples/invalid/non-goals-field.alliance-policy.json`](../../schemas/examples/invalid/non-goals-field.alliance-policy.json)
- [`doc/schemas/examples/invalid/root-digest-as-required-pin.alliance-policy.json`](../../schemas/examples/invalid/root-digest-as-required-pin.alliance-policy.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `alliance-policy.v1` | Schema discriminator. MUST be exactly `alliance-policy.v1`. |
| [`alliance_id`](#field-alliance-id) | `yes` | string | Deterministic alliance id derived from the sorted member federation ids and the alliance-policy v1 domain label. |
| [`issuer_federation_id`](#field-issuer-federation-id) | `yes` | string | Federation that authored this unilateral policy half. MUST be one of `members[].federation_id`; runtime enforces the cross-field invariant. |
| [`issuer_subject_ref`](#field-issuer-subject-ref) | `yes` | ref: `#/$defs/SovereignSubjectRef` | Sovereign subject in the issuer federation's active root whose custody policy authorizes this declaration. Runtime MUST verify that this subject matches the `members[]` entry for `issuer_federation_id`. |
| [`sequence_no`](#field-sequence-no) | `yes` | integer | Monotonic sequence number per `(issuer_federation_id, alliance_id)`. Older sequence numbers are rollback candidates. |
| [`members`](#field-members) | `yes` | array | Federations participating in the alliance. Runtime treats the member set as unordered and requires every active half to name the same set. |
| [`allowed_scopes`](#field-allowed-scopes) | `yes` | array | Scopes this issuer allows. Active alliance scope is the intersection across all matching halves. |
| [`denied_scopes`](#field-denied-scopes) | `no` | array | Scopes this issuer explicitly denies. Deny overrides allow across all matching halves. |
| [`publication`](#field-publication) | `yes` | ref: `#/$defs/Publication` | Where this policy half may be stored or advertised. Publication surface never substitutes for signature/root verification. |
| [`issued_at`](#field-issued-at) | `yes` | string | RFC 3339 issuance timestamp. Diagnostic and replay context; sequence/expiry/revocation govern replacement. |
| [`expires_at`](#field-expires-at) | `yes` | string | RFC 3339 expiry timestamp. Verifiers MUST reject the half at or after this time. Runtime MUST also enforce `expires_at > issued_at` because portable JSON Schema does not support cross-field date comparison. |
| [`policy_ref`](#field-policy-ref) | `no` | string | Optional local or governance policy reference explaining why this declaration was authorized. |
| [`revocation_ref`](#field-revocation-ref) | `no` | string | Optional revocation feed or local revocation view reference. Runtime profile decides how it is resolved. |
| [`signatures`](#field-signatures) | `yes` | array | One or more Ed25519 signatures over the canonical payload with `signatures` omitted. `uniqueItems` rejects exact duplicate signature objects; runtime still enforces issuer subject custody semantics and unique signing keys. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`SovereignSubjectRef`](#def-sovereignsubjectref) | string |  |
| [`Sha256Digest`](#def-sha256digest) | string |  |
| [`Member`](#def-member) | object |  |
| [`AllianceScope`](#def-alliancescope) | enum: `room/cross-federation`, `whisper/cross-federation`, `corpus/cross-federation`, `artifact-delivery/cross-federation`, `inac/cross-federation`, `agora/topic-bridge` | Closed v1 scope registry. Unknown scopes fail closed. |
| [`Publication`](#def-publication) | object |  |
| [`Signature`](#def-signature) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `alliance-policy.v1`

Schema discriminator. MUST be exactly `alliance-policy.v1`.

<a id="field-alliance-id"></a>
## `alliance_id`

- Required: `yes`
- Shape: string

Deterministic alliance id derived from the sorted member federation ids and the alliance-policy v1 domain label.

<a id="field-issuer-federation-id"></a>
## `issuer_federation_id`

- Required: `yes`
- Shape: string

Federation that authored this unilateral policy half. MUST be one of `members[].federation_id`; runtime enforces the cross-field invariant.

<a id="field-issuer-subject-ref"></a>
## `issuer_subject_ref`

- Required: `yes`
- Shape: ref: `#/$defs/SovereignSubjectRef`

Sovereign subject in the issuer federation's active root whose custody policy authorizes this declaration. Runtime MUST verify that this subject matches the `members[]` entry for `issuer_federation_id`.

<a id="field-sequence-no"></a>
## `sequence_no`

- Required: `yes`
- Shape: integer

Monotonic sequence number per `(issuer_federation_id, alliance_id)`. Older sequence numbers are rollback candidates.

<a id="field-members"></a>
## `members`

- Required: `yes`
- Shape: array

Federations participating in the alliance. Runtime treats the member set as unordered and requires every active half to name the same set.

<a id="field-allowed-scopes"></a>
## `allowed_scopes`

- Required: `yes`
- Shape: array

Scopes this issuer allows. Active alliance scope is the intersection across all matching halves.

<a id="field-denied-scopes"></a>
## `denied_scopes`

- Required: `no`
- Shape: array

Scopes this issuer explicitly denies. Deny overrides allow across all matching halves.

<a id="field-publication"></a>
## `publication`

- Required: `yes`
- Shape: ref: `#/$defs/Publication`

Where this policy half may be stored or advertised. Publication surface never substitutes for signature/root verification.

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

RFC 3339 issuance timestamp. Diagnostic and replay context; sequence/expiry/revocation govern replacement.

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

RFC 3339 expiry timestamp. Verifiers MUST reject the half at or after this time. Runtime MUST also enforce `expires_at > issued_at` because portable JSON Schema does not support cross-field date comparison.

<a id="field-policy-ref"></a>
## `policy_ref`

- Required: `no`
- Shape: string

Optional local or governance policy reference explaining why this declaration was authorized.

<a id="field-revocation-ref"></a>
## `revocation_ref`

- Required: `no`
- Shape: string

Optional revocation feed or local revocation view reference. Runtime profile decides how it is resolved.

<a id="field-signatures"></a>
## `signatures`

- Required: `yes`
- Shape: array

One or more Ed25519 signatures over the canonical payload with `signatures` omitted. `uniqueItems` rejects exact duplicate signature objects; runtime still enforces issuer subject custody semantics and unique signing keys.

## Definition Semantics

<a id="def-sovereignsubjectref"></a>
## `$defs.SovereignSubjectRef`

- Shape: string

<a id="def-sha256digest"></a>
## `$defs.Sha256Digest`

- Shape: string

<a id="def-member"></a>
## `$defs.Member`

- Shape: object

<a id="def-alliancescope"></a>
## `$defs.AllianceScope`

- Shape: enum: `room/cross-federation`, `whisper/cross-federation`, `corpus/cross-federation`, `artifact-delivery/cross-federation`, `inac/cross-federation`, `agora/topic-bridge`

Closed v1 scope registry. Unknown scopes fail closed.

<a id="def-publication"></a>
## `$defs.Publication`

- Shape: object

<a id="def-signature"></a>
## `$defs.Signature`

- Shape: object
