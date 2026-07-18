# Classification v1

Source schema: [`doc/schemas/classification.v1.schema.json`](../../schemas/classification.v1.schema.json)

Machine-readable schema for the Memarium classification label that travels with data across component boundaries. The label distinguishes the immutable `source_tier` (stamped once at first ingress or write) from the derived `effective_tier`. A context-free read uses `source_tier`; a concrete egress boundary may derive a lower tier only from active `DeclassifyFact` values matching its surface and topic class under a current revocation view. Declassification never rewrites `source_tier`; it appends policy facts. The lattice is intentionally small (Personal > Community > Public) with most-restrictive-wins semantics on merge.

## Governing Basis

- [`doc/project/40-proposals/047-classification-label-propagation.md`](../../project/40-proposals/047-classification-label-propagation.md)
- [`doc/project/40-proposals/036-memarium.md`](../../project/40-proposals/036-memarium.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/032-key-delegation-passports.md`](../../project/40-proposals/032-key-delegation-passports.md)
- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/042-inter-node-artifact-channel.md`](../../project/40-proposals/042-inter-node-artifact-channel.md)

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

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `classification.v1` | Content-level discriminator for consumers that inspect the label outside its enclosing envelope. |
| [`source_tier`](#field-source-tier) | `yes` | ref: `#/$defs/Tier` | Immutable classification assigned at first stamping (write into Memarium, ingress from outside, or operator acceptance out of quarantine). Never rewritten. A request that attempts to change `source_tier` MUST be rejected with `reason: source_tier_immutable`. |
| [`effective_tier`](#field-effective-tier) | `yes` | ref: `#/$defs/Tier` | Derived tier used by a concrete egress guard. Context-free Memarium reads set it to `source_tier`. A boundary may lower it only when a `DeclassifyFact` is active for the exact surface/topic/time, has a non-empty unrevoked anchor, and has not been consumed for one-shot mode. Consumers MUST treat a carried lower value as a cache, not authority, and recompute it with their boundary context. It MUST NOT exceed `source_tier` in the lattice order (i.e. it is never more restrictive than the source). |
| [`provenance`](#field-provenance) | `yes` | ref: `#/$defs/SpaceOrigin` | Where the data first entered the system. For locally written facts: the target Memarium space. For ingress from a peer or import: the ingress origin. For derivations: a two-parent reference summarizing the joined inputs. |
| [`bound_subjects`](#field-bound-subjects) | `yes` | ref: `#/$defs/BoundSubjects` | Tier-dependent projection of the subjects whose dignity interests attach to the fact. Egress to Public surfaces MUST carry only `public_projection` and MUST NOT carry `personal_or_community`. Violation is rejected with `reason: bound_subjects_not_public`. |
| [`declassify_trail`](#field-declassify-trail) | `yes` | array | Append-only, time-ordered history of declassification acts. Possibly empty. Context-free readers retain `source_tier`; concrete boundaries compute their projection from this trail plus exact surface/topic/time and revocation context. They MUST NOT infer authority from the trail alone. Transformation facts may be referenced as evidence, but they do not lower classification by themselves in v1. |
| [`quarantine`](#field-quarantine) | `no` | ref: `#/$defs/QuarantineMarker` | Present iff the fact is currently in ingress quarantine (no operator acceptance yet). Guarded reads of a quarantined fact MUST be rejected with `reason: quarantined`. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`Tier`](#def-tier) | enum: `Personal`, `Community`, `Public` | Small boring lattice. `Personal` is top (most restrictive), `Public` is bottom (least restrictive), `Community` strictly between. Sub-tiers (Internal/Secret/Restricted) are intentionally NOT part of v1 — added only when a concrete edge guard would enforce them. Crisis is orthogonal and carried as a flag on the bearer, not a tier. |
| [`SpaceOrigin`](#def-spaceorigin) | unspecified | Origin of the data. Either a local Memarium space, an external ingress point, or a derivation over parent origins. |
| [`BoundSubjects`](#def-boundsubjects) | object | Tier-dependent projection. Exactly one branch is populated; the choice MUST match `effective_tier`. Carrying the wrong branch at egress is rejected with `reason: bound_subjects_not_public` (for Public egress) or `classification_mismatch` otherwise. |
| [`SubjectRef`](#def-subjectref) | object | Reference to a subject whose dignity interests attach to the fact. |
| [`PublicProjection`](#def-publicprojection) | object |  |
| [`DeclassifyFact`](#def-declassifyfact) | object |  |
| [`TransformationKind`](#def-transformationkind) | enum: `k-anonymization`, `histogram`, `summary`, `embedding`, `redaction`, `other` | Evidence-only transformation class. In v1, a TransformationFact is provenance for a DeclassifyFact, not an authorization to lower effective_tier. |
| [`TransformationFact`](#def-transformationfact) | object | Append-only provenance fact for aggregation, redaction, embedding, or summarization. It can be referenced from DeclassifyFact.evidence_ref, but never changes effective_tier on its own. |
| [`QuarantineMarker`](#def-quarantinemarker) | object | Marker indicating that the fact has not yet been accepted by the operator out of the ingress quarantine. While present, guarded reads/publishes MUST be rejected with `reason: quarantined`. |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "source_tier": {
      "const": "Public"
    }
  },
  "required": [
    "source_tier"
  ]
}
```

Then:

```json
{
  "properties": {
    "effective_tier": {
      "const": "Public"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "source_tier": {
      "const": "Community"
    }
  },
  "required": [
    "source_tier"
  ]
}
```

Then:

```json
{
  "properties": {
    "effective_tier": {
      "enum": [
        "Community",
        "Public"
      ]
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "effective_tier": {
      "const": "Public"
    }
  },
  "required": [
    "effective_tier"
  ]
}
```

Then:

```json
{
  "properties": {
    "bound_subjects": {
      "required": [
        "public_projection"
      ],
      "not": {
        "required": [
          "personal_or_community"
        ]
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `classification.v1`

Content-level discriminator for consumers that inspect the label outside its enclosing envelope.

<a id="field-source-tier"></a>
## `source_tier`

- Required: `yes`
- Shape: ref: `#/$defs/Tier`

Immutable classification assigned at first stamping (write into Memarium, ingress from outside, or operator acceptance out of quarantine). Never rewritten. A request that attempts to change `source_tier` MUST be rejected with `reason: source_tier_immutable`.

<a id="field-effective-tier"></a>
## `effective_tier`

- Required: `yes`
- Shape: ref: `#/$defs/Tier`

Derived tier used by a concrete egress guard. Context-free Memarium reads set it to `source_tier`. A boundary may lower it only when a `DeclassifyFact` is active for the exact surface/topic/time, has a non-empty unrevoked anchor, and has not been consumed for one-shot mode. Consumers MUST treat a carried lower value as a cache, not authority, and recompute it with their boundary context. It MUST NOT exceed `source_tier` in the lattice order (i.e. it is never more restrictive than the source).

<a id="field-provenance"></a>
## `provenance`

- Required: `yes`
- Shape: ref: `#/$defs/SpaceOrigin`

Where the data first entered the system. For locally written facts: the target Memarium space. For ingress from a peer or import: the ingress origin. For derivations: a two-parent reference summarizing the joined inputs.

<a id="field-bound-subjects"></a>
## `bound_subjects`

- Required: `yes`
- Shape: ref: `#/$defs/BoundSubjects`

Tier-dependent projection of the subjects whose dignity interests attach to the fact. Egress to Public surfaces MUST carry only `public_projection` and MUST NOT carry `personal_or_community`. Violation is rejected with `reason: bound_subjects_not_public`.

<a id="field-declassify-trail"></a>
## `declassify_trail`

- Required: `yes`
- Shape: array

Append-only, time-ordered history of declassification acts. Possibly empty. Context-free readers retain `source_tier`; concrete boundaries compute their projection from this trail plus exact surface/topic/time and revocation context. They MUST NOT infer authority from the trail alone. Transformation facts may be referenced as evidence, but they do not lower classification by themselves in v1.

<a id="field-quarantine"></a>
## `quarantine`

- Required: `no`
- Shape: ref: `#/$defs/QuarantineMarker`

Present iff the fact is currently in ingress quarantine (no operator acceptance yet). Guarded reads of a quarantined fact MUST be rejected with `reason: quarantined`.

## Definition Semantics

<a id="def-tier"></a>
## `$defs.Tier`

- Shape: enum: `Personal`, `Community`, `Public`

Small boring lattice. `Personal` is top (most restrictive), `Public` is bottom (least restrictive), `Community` strictly between. Sub-tiers (Internal/Secret/Restricted) are intentionally NOT part of v1 — added only when a concrete edge guard would enforce them. Crisis is orthogonal and carried as a flag on the bearer, not a tier.

<a id="def-spaceorigin"></a>
## `$defs.SpaceOrigin`

- Shape: unspecified

Origin of the data. Either a local Memarium space, an external ingress point, or a derivation over parent origins.

<a id="def-boundsubjects"></a>
## `$defs.BoundSubjects`

- Shape: object

Tier-dependent projection. Exactly one branch is populated; the choice MUST match `effective_tier`. Carrying the wrong branch at egress is rejected with `reason: bound_subjects_not_public` (for Public egress) or `classification_mismatch` otherwise.

<a id="def-subjectref"></a>
## `$defs.SubjectRef`

- Shape: object

Reference to a subject whose dignity interests attach to the fact.

<a id="def-publicprojection"></a>
## `$defs.PublicProjection`

- Shape: object

<a id="def-declassifyfact"></a>
## `$defs.DeclassifyFact`

- Shape: object

<a id="def-transformationkind"></a>
## `$defs.TransformationKind`

- Shape: enum: `k-anonymization`, `histogram`, `summary`, `embedding`, `redaction`, `other`

Evidence-only transformation class. In v1, a TransformationFact is provenance for a DeclassifyFact, not an authorization to lower effective_tier.

<a id="def-transformationfact"></a>
## `$defs.TransformationFact`

- Shape: object

Append-only provenance fact for aggregation, redaction, embedding, or summarization. It can be referenced from DeclassifyFact.evidence_ref, but never changes effective_tier on its own.

<a id="def-quarantinemarker"></a>
## `$defs.QuarantineMarker`

- Shape: object

Marker indicating that the fact has not yet been accepted by the operator out of the ingress quarantine. While present, guarded reads/publishes MUST be rejected with `reason: quarantined`.
