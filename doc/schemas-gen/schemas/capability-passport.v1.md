# Capability Passport v1

Source schema: [`doc/schemas/capability-passport.v1.schema.json`](../../schemas/capability-passport.v1.schema.json)

Signed capability or consent artifact naming a capability profile for a target Node. Direct signatures are verified against the public key embedded in `issuer/participant_id`. Delegated signatures are verified against `issuer_delegation.proxy_key` after the inline delegation proof verifies against the same issuer. The signed payload is the deterministic canonical JSON of the artifact with `signature` and `issuer_delegation` omitted. Trust derives from profile-specific local policy, not from the passport alone: infrastructure profiles such as `network-ledger` may require a sovereign operator issuer, while consent profiles such as `node-primary-operator` may require a matching Node acceptance artifact.

## Governing Basis

- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/20-memos/participant-assurance-levels.md`](../../project/20-memos/participant-assurance-levels.md)
- [`doc/project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md`](../../project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md)
- [`doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`](../../project/40-proposals/038-key-roles-and-key-use-taxonomy.md)
- [`doc/project/60-solutions/capability-binding.md`](../../project/60-solutions/capability-binding.md)
- [`doc/project/60-solutions/sealer.md`](../../project/60-solutions/sealer.md)

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

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `capability-passport.v1` | Schema discriminator. MUST be exactly `capability-passport.v1`. |
| [`passport_id`](#field-passport-id) | `yes` | string | Stable unique identifier for this passport. MUST use the `passport:capability:` prefix. |
| [`node_id`](#field-node-id) | `yes` | string | Target Node receiving the delegated capability. MUST match the `node:did:key:z...` canonical format. |
| [`capability_id`](#field-capability-id) | `yes` | string | Capability identifier. Formal global profiles use bare kebab-case identifiers such as `network-ledger`, `seed-directory`, `escrow`, or `node-primary-operator`. Sovereign/private profiles may add an identity anchor, e.g. `audio-transcription@participant:did:key:z...`, with an optional leading `~` for informal profiles. See Proposal 024 and Proposal 025 for naming and advertisement projection. |
| [`capability_profile`](#field-capability-profile) | `no` | ref: `#/$defs/capabilityProfile` | Optional human and machine description of the capability profile. This is signed with the passport when present, but it is metadata: trust still derives from passport verification and local policy. |
| [`scope`](#field-scope) | `yes` | object | Capability-specific parameters constraining the delegation. MAY be empty (`{}`). Receivers MUST tolerate unknown keys. Non-key-use passports (e.g. `network-ledger`, `node-primary-operator`) MAY continue to use free-form scope fields such as `federation/id`. Key-use passports (Sealer, Memarium space, community key) SHOULD populate the typed `allowed_callers[]` and `profiles[]` fields defined below; this schema validates their shape when present, but does not require them at the envelope level. Key-use verifiers (`capability-binding`) semantically require both a matching `allowed_callers[]` entry and at least one authorizing recognized profile in `profiles[]` before emitting `AuthorizationDecision::Authorized`. See proposal 038 §Tightened `capability-passport.v1` Scope for Key-Use Authorization. |
| [`issued_at`](#field-issued-at) | `yes` | string | RFC 3339 timestamp at which this passport was issued. |
| [`expires_at`](#field-expires-at) | `no` | string \| null | RFC 3339 timestamp after which this passport MUST be treated as expired. `null` means no explicit expiry; receivers SHOULD apply a locally configured maximum TTL. |
| [`issuer/participant_id`](#field-issuer-participant-id) | `yes` | string | Canonical `participant:did:key:z...` identifier of the issuing participant. The required authority level is determined by the capability profile. Infrastructure profiles such as `network-ledger` and `seed-directory` usually require a software-pinned sovereign operator; the `node-primary-operator` consent profile requires this participant to match the operator named by the binding policy and to be accepted by the target Node. |
| [`issuer/node_id`](#field-issuer-node-id) | `yes` | string | Node on which the issuing participant acted when signing this passport. |
| [`revocation_ref`](#field-revocation-ref) | `yes` | string \| null | Optional reference to an out-of-band revocation endpoint or log for this passport. `null` if no external revocation surface is provided; consumers SHOULD still poll the Seed Directory revocation log. |
| [`issuer_delegation`](#field-issuer-delegation) | `no` | ref: `#/$defs/delegationProof` | Optional compact inline proof authorising a proxy key to sign this artifact for `issuer/participant_id`. Verifiers MUST verify this proof before checking the artifact signature with `proxy_key`; it is excluded from the artifact signature payload. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/ed25519Signature` |  |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional informational annotations. MUST NOT alter core passport semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`capabilityProfile`](#def-capabilityprofile) | object |  |
| [`delegationProof`](#def-delegationproof) | object | Compact bearer credential copied out of a `key-delegation.v1` registration artifact and embedded beside a proxy-key signature. Its own principal signature covers only the compact proof payload. |
| [`ed25519Signature`](#def-ed25519signature) | object | Ed25519 signature over the deterministic canonical JSON of the passport with the `signature` and `issuer_delegation` fields omitted entirely from the signed payload. Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order. |
| [`allowedCaller`](#def-allowedcaller) | object | One caller entry recognized by a key-use passport. Verifier matches entries against a resolved `CallerBinding` produced by the `caller-binding` crate: `subject_key` MUST overlap `CallerBinding.subject_keys`; `label` MUST match `CallerBinding.caller_label` when present; `kind` MUST match `CallerBinding.subject_kind` when present. Only public-key material appears here; binding entries MUST NOT embed secrets. |
| [`scopeProfileV1`](#def-scopeprofilev1) | object | One key-use profile entry in `scope.profiles[]`. The `profile` field is the discriminator. Recognized discriminators (`sealer-access@v1`, `memarium-space-access@v1`, `memarium-declassify@v1`, `community-key-access@v1`) trigger profile-specific shape validation below. Unknown discriminators are tolerated by the schema but MUST NOT grant access at the verifier. |
| [`sealerAccessProfileV1`](#def-sealeraccessprofilev1) | object | Authorizes Sealer AEAD operations on bounded semantic key identifiers as known to the operator. `key_ref_prefixes` and grant targets match values such as `key:community:...`; signer-layer wrapping such as `proxy:` is not part of the authorization tag. The dispatch layer is responsible for translating concrete signer `KeyRef` values before evaluation. See proposal 038 §Profile `sealer-access@v1`. |
| [`memariumSpaceAccessProfileV1`](#def-memariumspaceaccessprofilev1) | object | Authorizes Memarium space-level operations at a layer above Sealer. See proposal 038 §Profile `memarium-space-access@v1`. |
| [`memariumDeclassifyProfileV1`](#def-memariumdeclassifyprofilev1) | object | Authorizes append-only Memarium declassification policy facts. This profile is deliberately separate from `memarium-space-access@v1`: declassification binds not only to a space, but also to surface, topic class, mode, and tier transition. |
| [`communityKeyAccessProfileV1`](#def-communitykeyaccessprofilev1) | object | Authorizes community key material reception, rotation, and distribution decisions at a layer above Sealer. See proposal 038 §Profile `community-key-access@v1`. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "passport_id"
  ]
}
```

Then:

```json
{
  "properties": {
    "passport_id": {
      "pattern": "^passport:capability:"
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `capability-passport.v1`

Schema discriminator. MUST be exactly `capability-passport.v1`.

<a id="field-passport-id"></a>
## `passport_id`

- Required: `yes`
- Shape: string

Stable unique identifier for this passport. MUST use the `passport:capability:` prefix.

<a id="field-node-id"></a>
## `node_id`

- Required: `yes`
- Shape: string

Target Node receiving the delegated capability. MUST match the `node:did:key:z...` canonical format.

<a id="field-capability-id"></a>
## `capability_id`

- Required: `yes`
- Shape: string

Capability identifier. Formal global profiles use bare kebab-case identifiers such as `network-ledger`, `seed-directory`, `escrow`, or `node-primary-operator`. Sovereign/private profiles may add an identity anchor, e.g. `audio-transcription@participant:did:key:z...`, with an optional leading `~` for informal profiles. See Proposal 024 and Proposal 025 for naming and advertisement projection.

<a id="field-capability-profile"></a>
## `capability_profile`

- Required: `no`
- Shape: ref: `#/$defs/capabilityProfile`

Optional human and machine description of the capability profile. This is signed with the passport when present, but it is metadata: trust still derives from passport verification and local policy.

<a id="field-scope"></a>
## `scope`

- Required: `yes`
- Shape: object

Capability-specific parameters constraining the delegation. MAY be empty (`{}`). Receivers MUST tolerate unknown keys. Non-key-use passports (e.g. `network-ledger`, `node-primary-operator`) MAY continue to use free-form scope fields such as `federation/id`. Key-use passports (Sealer, Memarium space, community key) SHOULD populate the typed `allowed_callers[]` and `profiles[]` fields defined below; this schema validates their shape when present, but does not require them at the envelope level. Key-use verifiers (`capability-binding`) semantically require both a matching `allowed_callers[]` entry and at least one authorizing recognized profile in `profiles[]` before emitting `AuthorizationDecision::Authorized`. See proposal 038 §Tightened `capability-passport.v1` Scope for Key-Use Authorization.

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which this passport was issued.

<a id="field-expires-at"></a>
## `expires_at`

- Required: `no`
- Shape: string | null

RFC 3339 timestamp after which this passport MUST be treated as expired. `null` means no explicit expiry; receivers SHOULD apply a locally configured maximum TTL.

<a id="field-issuer-participant-id"></a>
## `issuer/participant_id`

- Required: `yes`
- Shape: string

Canonical `participant:did:key:z...` identifier of the issuing participant. The required authority level is determined by the capability profile. Infrastructure profiles such as `network-ledger` and `seed-directory` usually require a software-pinned sovereign operator; the `node-primary-operator` consent profile requires this participant to match the operator named by the binding policy and to be accepted by the target Node.

<a id="field-issuer-node-id"></a>
## `issuer/node_id`

- Required: `yes`
- Shape: string

Node on which the issuing participant acted when signing this passport.

<a id="field-revocation-ref"></a>
## `revocation_ref`

- Required: `yes`
- Shape: string | null

Optional reference to an out-of-band revocation endpoint or log for this passport. `null` if no external revocation surface is provided; consumers SHOULD still poll the Seed Directory revocation log.

<a id="field-issuer-delegation"></a>
## `issuer_delegation`

- Required: `no`
- Shape: ref: `#/$defs/delegationProof`

Optional compact inline proof authorising a proxy key to sign this artifact for `issuer/participant_id`. Verifiers MUST verify this proof before checking the artifact signature with `proxy_key`; it is excluded from the artifact signature payload.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/ed25519Signature`

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional informational annotations. MUST NOT alter core passport semantics.

## Definition Semantics

<a id="def-capabilityprofile"></a>
## `$defs.capabilityProfile`

- Shape: object

<a id="def-delegationproof"></a>
## `$defs.delegationProof`

- Shape: object

Compact bearer credential copied out of a `key-delegation.v1` registration artifact and embedded beside a proxy-key signature. Its own principal signature covers only the compact proof payload.

<a id="def-ed25519signature"></a>
## `$defs.ed25519Signature`

- Shape: object

Ed25519 signature over the deterministic canonical JSON of the passport with the `signature` and `issuer_delegation` fields omitted entirely from the signed payload. Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order.

<a id="def-allowedcaller"></a>
## `$defs.allowedCaller`

- Shape: object

One caller entry recognized by a key-use passport. Verifier matches entries against a resolved `CallerBinding` produced by the `caller-binding` crate: `subject_key` MUST overlap `CallerBinding.subject_keys`; `label` MUST match `CallerBinding.caller_label` when present; `kind` MUST match `CallerBinding.subject_kind` when present. Only public-key material appears here; binding entries MUST NOT embed secrets.

<a id="def-scopeprofilev1"></a>
## `$defs.scopeProfileV1`

- Shape: object

One key-use profile entry in `scope.profiles[]`. The `profile` field is the discriminator. Recognized discriminators (`sealer-access@v1`, `memarium-space-access@v1`, `memarium-declassify@v1`, `community-key-access@v1`) trigger profile-specific shape validation below. Unknown discriminators are tolerated by the schema but MUST NOT grant access at the verifier.

<a id="def-sealeraccessprofilev1"></a>
## `$defs.sealerAccessProfileV1`

- Shape: object

Authorizes Sealer AEAD operations on bounded semantic key identifiers as known to the operator. `key_ref_prefixes` and grant targets match values such as `key:community:...`; signer-layer wrapping such as `proxy:` is not part of the authorization tag. The dispatch layer is responsible for translating concrete signer `KeyRef` values before evaluation. See proposal 038 §Profile `sealer-access@v1`.

<a id="def-memariumspaceaccessprofilev1"></a>
## `$defs.memariumSpaceAccessProfileV1`

- Shape: object

Authorizes Memarium space-level operations at a layer above Sealer. See proposal 038 §Profile `memarium-space-access@v1`.

<a id="def-memariumdeclassifyprofilev1"></a>
## `$defs.memariumDeclassifyProfileV1`

- Shape: object

Authorizes append-only Memarium declassification policy facts. This profile is deliberately separate from `memarium-space-access@v1`: declassification binds not only to a space, but also to surface, topic class, mode, and tier transition.

<a id="def-communitykeyaccessprofilev1"></a>
## `$defs.communityKeyAccessProfileV1`

- Shape: object

Authorizes community key material reception, rotation, and distribution decisions at a layer above Sealer. See proposal 038 §Profile `community-key-access@v1`.
