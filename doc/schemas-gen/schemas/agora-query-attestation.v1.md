# Agora Query Attestation v1

Source schema: [`doc/schemas/agora-query-attestation.v1.schema.json`](../../schemas/agora-query-attestation.v1.schema.json)

Machine-readable attestation for one Agora historical query response. It binds the query scope, normalized filter, returned record ids, pagination/pruning metadata, and a deterministic digest of the response page. A signature is optional in v1 so local relays can emit unsigned attestations before relay signing is wired; signed deployments should sign the canonical JSON of this object with `signature` omitted.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/60-solutions/008-agora/008-agora-dir-simplify-impl.md`](../../project/60-solutions/008-agora/008-agora-dir-simplify-impl.md)
- [`doc/project/60-solutions/021-agora-authority/021-agora-authority.md`](../../project/60-solutions/021-agora-authority/021-agora-authority.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-008-org-subject-rollout.md`](../../project/50-requirements/requirements-008-org-subject-rollout.md)
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

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `agora-query-attestation.v1` | Schema discriminator. MUST be exactly `agora-query-attestation.v1`. |
| [`attestation/id`](#field-attestation-id) | `yes` | string | Stable identifier for this attested response page. The reference implementation derives it from the response digest. |
| [`attested/at`](#field-attested-at) | `yes` | string | UTC time when the relay assembled the attestation. |
| [`relay/id`](#field-relay-id) | `no` | string | Optional relay identifier that assembled the page. |
| [`query/mode`](#field-query-mode) | `yes` | enum: `topic-records`, `subject-records` | Query family this attestation describes. |
| [`query/topic-key`](#field-query-topic-key) | `no` | string | Topic key for a topic-records query. |
| [`query/resource`](#field-query-resource) | `no` | ref: `#/$defs/resourceRef` | Subject resource for a subject-records query. |
| [`query/filter`](#field-query-filter) | `yes` | object | Normalized filter used by the relay after URL decoding and limit defaults. |
| [`result/record-ids`](#field-result-record-ids) | `yes` | array | Record ids returned in page order. |
| [`result/count`](#field-result-count) | `yes` | integer | Number of returned records. MUST equal the length of `result/record-ids`. |
| [`result/next-cursor`](#field-result-next-cursor) | `no` | string | Opaque cursor for the next page, if present in the response. |
| [`result/cursor-pruned`](#field-result-cursor-pruned) | `no` | object | Explicit discontinuity notice when retention pruned records below the caller's cursor. |
| [`result/digest`](#field-result-digest) | `yes` | string | Digest of the canonical query-attestation material: query mode, scope, normalized filter, returned record ids, next cursor, and cursor-pruned notice. |
| [`result/digest-alg`](#field-result-digest-alg) | `yes` | const: `jcs-nfc-sha256-base64url` | Digest algorithm used for `result/digest`. |
| [`signature`](#field-signature) | `no` | object | Optional relay signature over the canonical attestation with `signature` omitted. Unsigned v1 attestations still provide deterministic digest evidence but not relay accountability. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`resourceRef`](#def-resourceref) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "query/mode": {
      "const": "topic-records"
    }
  },
  "required": [
    "query/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "query/topic-key"
  ],
  "not": {
    "required": [
      "query/resource"
    ]
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "query/mode": {
      "const": "subject-records"
    }
  },
  "required": [
    "query/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "query/resource"
  ],
  "not": {
    "required": [
      "query/topic-key"
    ]
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-query-attestation.v1`

Schema discriminator. MUST be exactly `agora-query-attestation.v1`.

<a id="field-attestation-id"></a>
## `attestation/id`

- Required: `yes`
- Shape: string

Stable identifier for this attested response page. The reference implementation derives it from the response digest.

<a id="field-attested-at"></a>
## `attested/at`

- Required: `yes`
- Shape: string

UTC time when the relay assembled the attestation.

<a id="field-relay-id"></a>
## `relay/id`

- Required: `no`
- Shape: string

Optional relay identifier that assembled the page.

<a id="field-query-mode"></a>
## `query/mode`

- Required: `yes`
- Shape: enum: `topic-records`, `subject-records`

Query family this attestation describes.

<a id="field-query-topic-key"></a>
## `query/topic-key`

- Required: `no`
- Shape: string

Topic key for a topic-records query.

<a id="field-query-resource"></a>
## `query/resource`

- Required: `no`
- Shape: ref: `#/$defs/resourceRef`

Subject resource for a subject-records query.

<a id="field-query-filter"></a>
## `query/filter`

- Required: `yes`
- Shape: object

Normalized filter used by the relay after URL decoding and limit defaults.

<a id="field-result-record-ids"></a>
## `result/record-ids`

- Required: `yes`
- Shape: array

Record ids returned in page order.

<a id="field-result-count"></a>
## `result/count`

- Required: `yes`
- Shape: integer

Number of returned records. MUST equal the length of `result/record-ids`.

<a id="field-result-next-cursor"></a>
## `result/next-cursor`

- Required: `no`
- Shape: string

Opaque cursor for the next page, if present in the response.

<a id="field-result-cursor-pruned"></a>
## `result/cursor-pruned`

- Required: `no`
- Shape: object

Explicit discontinuity notice when retention pruned records below the caller's cursor.

<a id="field-result-digest"></a>
## `result/digest`

- Required: `yes`
- Shape: string

Digest of the canonical query-attestation material: query mode, scope, normalized filter, returned record ids, next cursor, and cursor-pruned notice.

<a id="field-result-digest-alg"></a>
## `result/digest-alg`

- Required: `yes`
- Shape: const: `jcs-nfc-sha256-base64url`

Digest algorithm used for `result/digest`.

<a id="field-signature"></a>
## `signature`

- Required: `no`
- Shape: object

Optional relay signature over the canonical attestation with `signature` omitted. Unsigned v1 attestations still provide deterministic digest evidence but not relay accountability.

## Definition Semantics

<a id="def-resourceref"></a>
## `$defs.resourceRef`

- Shape: object
