# Key Delegation v1

Source schema: [`doc/schemas/key-delegation.v1.schema.json`](../../schemas/key-delegation.v1.schema.json)

Registration and management artifact for a scoped delegation of capability-passport signing authority from a participant's sovereign key to a separate proxy key. The participant signs this artifact once to authorise the proxy key; all subsequent operational signing uses the proxy key and carries a compact `DelegationProof` extracted from this artifact (see `capability-passport.v1` `issuer_delegation`). The signature payload is the canonical JSON of the COMPACT proof contract (`delegation_id`, `proxy_key`, `principal_key`, `grants`, `expires_at`), NOT the full artifact. The full artifact is the Seed Directory registration and audit envelope that carries this payload alongside management metadata (`schema`, `issued_at`, `issuer/node_id`, `max_chain_depth`, `parent_delegation_id`).

## Governing Basis

- [`doc/project/40-proposals/032-key-delegation-passports.md`](../../project/40-proposals/032-key-delegation-passports.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/project/40-proposals/030-identity-recovery-service.md`](../../project/40-proposals/030-identity-recovery-service.md)
- [`doc/project/40-proposals/031-participant-key-passphrase-lock.md`](../../project/40-proposals/031-participant-key-passphrase-lock.md)
- [`doc/project/60-solutions/032-key-delegation-passports-impl.md`](../../project/60-solutions/032-key-delegation-passports-impl.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `key-delegation.v1` | Schema discriminator. MUST be exactly `key-delegation.v1`. |
| [`delegation_id`](#field-delegation-id) | `yes` | string | Stable unique identifier for this delegation. MUST use the `delegation:key:` prefix followed by a non-empty suffix. The recommended construction is `delegation:key:<unix-nanos>:<random-hex>` so that ordering and uniqueness are self-evident; schema does not enforce the internal shape beyond the prefix. |
| [`proxy_key`](#field-proxy-key) | `yes` | string | Delegated Ed25519 public key in DID Key form. This is the key that will sign capability passports and revocations on behalf of `issuer/participant_id` for the lifetime of this delegation. The private counterpart is held by the proxy key store and MUST NOT appear anywhere in this artifact. |
| [`grants`](#field-grants) | `yes` | object | Open grant map from grant type to non-empty list of target identifiers. MVP recognizes `signing/capability` whose targets are capability IDs (e.g. `network-ledger`, `escrow`) and `signing/agora-record` whose targets are Agora record-signing scopes (for example topic-scoped targets or the wildcard `"*"`). Additional grant types (`signing/org`, `signing/proxy`, ...) are reserved for future proposals and MUST be ignored by verifiers that do not recognise them (open-world extension semantics). The wildcard `"*"` is operationally convenient but semantically equivalent to full authority for the grant type; operators SHOULD prefer explicit targets. |
| [`max_chain_depth`](#field-max-chain-depth) | `yes` | integer | Maximum number of additional delegation hops the proxy key is authorised to create. `0` means the proxy key MUST NOT issue further `key-delegation.v1` artifacts. Values greater than `0` remain schema-valid (so the artifact can travel through storage layers that pre-date sub-delegation) but MVP runtime implementations MUST reject any delegation with `max_chain_depth > 0` until sub-delegation is formally specified. |
| [`parent_delegation_id`](#field-parent-delegation-id) | `no` | string | Optional reference to the parent delegation from which this one was derived. Absent at the root of the chain (where the issuer is a direct participant key). Present on sub-delegations (`max_chain_depth > 0` in an ancestor). Reserved for post-MVP sub-delegation; MVP MUST reject artifacts that set this field. |
| [`issued_at`](#field-issued-at) | `yes` | string | RFC 3339 timestamp at which the participant issued this delegation. Informational: the signature payload does not include this field. MUST be in the past relative to local wall clock at verification time (subject to clock-skew tolerance). |
| [`expires_at`](#field-expires-at) | `yes` | string | RFC 3339 timestamp after which this delegation MUST be treated as expired. MANDATORY: implementations MUST reject delegation artifacts lacking this field. Part of the signed compact proof payload. Recommended maximum TTL is 365 days; issuance UI SHOULD warn for values exceeding that. |
| [`issuer/participant_id`](#field-issuer-participant-id) | `yes` | string | Canonical `participant:did:key:z...` identifier of the issuing participant. Its embedded public key is the `principal_key` that MUST verify the `signature` field (after canonicalization of the compact proof payload). Verifiers derive `participant:did:key:...` from the `principal_key` carried in a `DelegationProof` and require byte-equality with this value. |
| [`issuer/node_id`](#field-issuer-node-id) | `yes` | string | Node on which the issuing participant's private key resided at the moment of signing. Informational: the signature payload does not include this field. Used for audit and for correlating a delegation artifact to the node that issued it. |
| [`signature`](#field-signature) | `yes` | ref: `#/$defs/ed25519Signature` | Ed25519 signature by the private key of `issuer/participant_id` (the `principal_key`) over the canonical JSON representation of the COMPACT delegation proof contract: `{delegation_id, proxy_key, principal_key, grants, expires_at}`, with `principal_key` being the raw `did:key` bytes of `issuer/participant_id`. The signature explicitly does NOT cover the management metadata (`schema`, `issued_at`, `issuer/node_id`, `max_chain_depth`, `parent_delegation_id`). This keeps the same signed bytes verifiable both from the full artifact and from an inline `DelegationProof` copied into a downstream signed artifact (`capability-passport.v1` `issuer_delegation`). |
| [`co_signatures`](#field-co-signatures) | `no` | array | Reserved for post-MVP M-of-N multisig issuance. When absent, a single primary `signature` authorises the delegation. When present, each entry is an additional signature over the same compact proof payload by a co-issuer key authorised by an out-of-band multisig policy. MVP verifiers MUST ignore this field; MVP issuers MUST NOT emit it. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ed25519Signature`](#def-ed25519signature) | object | Ed25519 signature over the canonical JSON encoding of the compact delegation proof payload (`delegation_id`, `proxy_key`, `principal_key`, `grants`, `expires_at`). Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order. The canonical payload is identical to the one carried in a `DelegationProof` embedded in downstream signed artifacts. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `key-delegation.v1`

Schema discriminator. MUST be exactly `key-delegation.v1`.

<a id="field-delegation-id"></a>
## `delegation_id`

- Required: `yes`
- Shape: string

Stable unique identifier for this delegation. MUST use the `delegation:key:` prefix followed by a non-empty suffix. The recommended construction is `delegation:key:<unix-nanos>:<random-hex>` so that ordering and uniqueness are self-evident; schema does not enforce the internal shape beyond the prefix.

<a id="field-proxy-key"></a>
## `proxy_key`

- Required: `yes`
- Shape: string

Delegated Ed25519 public key in DID Key form. This is the key that will sign capability passports and revocations on behalf of `issuer/participant_id` for the lifetime of this delegation. The private counterpart is held by the proxy key store and MUST NOT appear anywhere in this artifact.

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: object

Open grant map from grant type to non-empty list of target identifiers. MVP recognizes `signing/capability` whose targets are capability IDs (e.g. `network-ledger`, `escrow`) and `signing/agora-record` whose targets are Agora record-signing scopes (for example topic-scoped targets or the wildcard `"*"`). Additional grant types (`signing/org`, `signing/proxy`, ...) are reserved for future proposals and MUST be ignored by verifiers that do not recognise them (open-world extension semantics). The wildcard `"*"` is operationally convenient but semantically equivalent to full authority for the grant type; operators SHOULD prefer explicit targets.

<a id="field-max-chain-depth"></a>
## `max_chain_depth`

- Required: `yes`
- Shape: integer

Maximum number of additional delegation hops the proxy key is authorised to create. `0` means the proxy key MUST NOT issue further `key-delegation.v1` artifacts. Values greater than `0` remain schema-valid (so the artifact can travel through storage layers that pre-date sub-delegation) but MVP runtime implementations MUST reject any delegation with `max_chain_depth > 0` until sub-delegation is formally specified.

<a id="field-parent-delegation-id"></a>
## `parent_delegation_id`

- Required: `no`
- Shape: string

Optional reference to the parent delegation from which this one was derived. Absent at the root of the chain (where the issuer is a direct participant key). Present on sub-delegations (`max_chain_depth > 0` in an ancestor). Reserved for post-MVP sub-delegation; MVP MUST reject artifacts that set this field.

<a id="field-issued-at"></a>
## `issued_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp at which the participant issued this delegation. Informational: the signature payload does not include this field. MUST be in the past relative to local wall clock at verification time (subject to clock-skew tolerance).

<a id="field-expires-at"></a>
## `expires_at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp after which this delegation MUST be treated as expired. MANDATORY: implementations MUST reject delegation artifacts lacking this field. Part of the signed compact proof payload. Recommended maximum TTL is 365 days; issuance UI SHOULD warn for values exceeding that.

<a id="field-issuer-participant-id"></a>
## `issuer/participant_id`

- Required: `yes`
- Shape: string

Canonical `participant:did:key:z...` identifier of the issuing participant. Its embedded public key is the `principal_key` that MUST verify the `signature` field (after canonicalization of the compact proof payload). Verifiers derive `participant:did:key:...` from the `principal_key` carried in a `DelegationProof` and require byte-equality with this value.

<a id="field-issuer-node-id"></a>
## `issuer/node_id`

- Required: `yes`
- Shape: string

Node on which the issuing participant's private key resided at the moment of signing. Informational: the signature payload does not include this field. Used for audit and for correlating a delegation artifact to the node that issued it.

<a id="field-signature"></a>
## `signature`

- Required: `yes`
- Shape: ref: `#/$defs/ed25519Signature`

Ed25519 signature by the private key of `issuer/participant_id` (the `principal_key`) over the canonical JSON representation of the COMPACT delegation proof contract: `{delegation_id, proxy_key, principal_key, grants, expires_at}`, with `principal_key` being the raw `did:key` bytes of `issuer/participant_id`. The signature explicitly does NOT cover the management metadata (`schema`, `issued_at`, `issuer/node_id`, `max_chain_depth`, `parent_delegation_id`). This keeps the same signed bytes verifiable both from the full artifact and from an inline `DelegationProof` copied into a downstream signed artifact (`capability-passport.v1` `issuer_delegation`).

<a id="field-co-signatures"></a>
## `co_signatures`

- Required: `no`
- Shape: array

Reserved for post-MVP M-of-N multisig issuance. When absent, a single primary `signature` authorises the delegation. When present, each entry is an additional signature over the same compact proof payload by a co-issuer key authorised by an out-of-band multisig policy. MVP verifiers MUST ignore this field; MVP issuers MUST NOT emit it.

## Definition Semantics

<a id="def-ed25519signature"></a>
## `$defs.ed25519Signature`

- Shape: object

Ed25519 signature over the canonical JSON encoding of the compact delegation proof payload (`delegation_id`, `proxy_key`, `principal_key`, `grants`, `expires_at`). Object keys are sorted lexicographically; no insignificant whitespace; arrays left in original order. The canonical payload is identical to the one carried in a `DelegationProof` embedded in downstream signed artifacts.
