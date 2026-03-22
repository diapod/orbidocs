# ProofOfPersonhoodAttestation v1

Source schema: [`doc/schemas/proof-of-personhood-attestation.v1.schema.json`](../../schemas/proof-of-personhood-attestation.v1.schema.json)

Machine-readable schema for minimal Proof-of-Personhood attestations that support non-withdrawable UBC and limited cross-federation portability, including recognition through the minimal FIP bridge/registry.

## Governing Basis

- [`doc/normative/40-constitution/pl/CONSTITUTION.pl.md`](../../normative/40-constitution/pl/CONSTITUTION.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](../../normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md`](../../normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`attestation_id`](#field-attestation-id) | `yes` | string | Stable identifier of this attestation record. |
| [`subject_ref`](#field-subject-ref) | `yes` | string | Stable anonymous handle for the verified person. |
| [`issuer_scope`](#field-issuer-scope) | `yes` | enum: `federation`, `fip_bridge`, `hybrid` | Which institutional path stands behind recognition of personhood: a federation, the minimal FIP bridge, or both together. |
| [`issuer_ref`](#field-issuer-ref) | `yes` | string | Stable reference to the issuing federation, the FIP bridge, or a hybrid issuing path. |
| [`issuer_federation_id`](#field-issuer-federation-id) | `no` | string | Canonical federation identifier when federation-side recognition participates in issuing the attestation. |
| [`bridge_ref`](#field-bridge-ref) | `no` | string | Optional reference to the FIP bridge/registry that recognizes the attestation cross-federation. |
| [`attestation_method`](#field-attestation-method) | `yes` | enum: `cryptographic_vouching`, `federation_attestation`, `sealed_chambers_recognition`, `fip_bridge_recognition`, `hybrid` | Recognition method used to establish Proof-of-Personhood without making de-anonymization the default path. |
| [`assurance_scope`](#field-assurance-scope) | `yes` | const: `proof_of_personhood` |  |
| [`deanon_not_required`](#field-deanon-not-required) | `yes` | boolean |  |
| [`uniqueness_scope`](#field-uniqueness-scope) | `yes` | enum: `federation`, `trans_federation_limited`, `trans_federation_extended` | How far the attestation's one-person-one-presence guarantees are meant to travel across federation boundaries. |
| [`valid_from`](#field-valid-from) | `yes` | string |  |
| [`valid_until`](#field-valid-until) | `no` | string |  |
| [`recognition_basis_ref`](#field-recognition-basis-ref) | `no` | string |  |
| [`evidence_ref`](#field-evidence-ref) | `no` | string |  |
| [`revocation_ref`](#field-revocation-ref) | `no` | string |  |
| [`revocation_status`](#field-revocation-status) | `no` | enum: `active`, `revoked`, `expired`, `superseded` |  |
| [`portability_profile`](#field-portability-profile) | `yes` | ref: `#/$defs/portabilityProfile` | Declared portability floor and extension capability for emergency, communication, and care access modes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`portabilityModeMap`](#def-portabilitymodemap) | object |  |
| [`portabilityProfile`](#def-portabilityprofile) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "issuer_scope": {
      "const": "federation"
    }
  },
  "required": [
    "issuer_scope"
  ]
}
```

Then:

```json
{
  "required": [
    "issuer_federation_id"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "issuer_scope": {
      "const": "fip_bridge"
    }
  },
  "required": [
    "issuer_scope"
  ]
}
```

Then:

```json
{
  "required": [
    "bridge_ref"
  ],
  "properties": {
    "attestation_method": {
      "enum": [
        "sealed_chambers_recognition",
        "fip_bridge_recognition",
        "hybrid"
      ]
    },
    "portability_profile": {
      "properties": {
        "bridge_minimum_supported": {
          "const": true
        }
      }
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "issuer_scope": {
      "const": "hybrid"
    }
  },
  "required": [
    "issuer_scope"
  ]
}
```

Then:

```json
{
  "required": [
    "issuer_federation_id",
    "bridge_ref"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "uniqueness_scope": {
      "const": "trans_federation_extended"
    }
  },
  "required": [
    "uniqueness_scope"
  ]
}
```

Then:

```json
{
  "properties": {
    "portability_profile": {
      "properties": {
        "extension_profile_refs": {
          "minItems": 1
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-attestation-id"></a>
## `attestation_id`

- Required: `yes`
- Shape: string

Stable identifier of this attestation record.

Governing basis:
- [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](../../normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md)

<a id="field-subject-ref"></a>
## `subject_ref`

- Required: `yes`
- Shape: string

Stable anonymous handle for the verified person.

<a id="field-issuer-scope"></a>
## `issuer_scope`

- Required: `yes`
- Shape: enum: `federation`, `fip_bridge`, `hybrid`

Which institutional path stands behind recognition of personhood: a federation, the minimal FIP bridge, or both together.

Governing basis:
- [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](../../normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md`](../../normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md)

<a id="field-issuer-ref"></a>
## `issuer_ref`

- Required: `yes`
- Shape: string

Stable reference to the issuing federation, the FIP bridge, or a hybrid issuing path.

<a id="field-issuer-federation-id"></a>
## `issuer_federation_id`

- Required: `no`
- Shape: string

Canonical federation identifier when federation-side recognition participates in issuing the attestation.

<a id="field-bridge-ref"></a>
## `bridge_ref`

- Required: `no`
- Shape: string

Optional reference to the FIP bridge/registry that recognizes the attestation cross-federation.

<a id="field-attestation-method"></a>
## `attestation_method`

- Required: `yes`
- Shape: enum: `cryptographic_vouching`, `federation_attestation`, `sealed_chambers_recognition`, `fip_bridge_recognition`, `hybrid`

Recognition method used to establish Proof-of-Personhood without making de-anonymization the default path.

<a id="field-assurance-scope"></a>
## `assurance_scope`

- Required: `yes`
- Shape: const: `proof_of_personhood`

<a id="field-deanon-not-required"></a>
## `deanon_not_required`

- Required: `yes`
- Shape: boolean

<a id="field-uniqueness-scope"></a>
## `uniqueness_scope`

- Required: `yes`
- Shape: enum: `federation`, `trans_federation_limited`, `trans_federation_extended`

How far the attestation's one-person-one-presence guarantees are meant to travel across federation boundaries.

<a id="field-valid-from"></a>
## `valid_from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid_until`

- Required: `no`
- Shape: string

<a id="field-recognition-basis-ref"></a>
## `recognition_basis_ref`

- Required: `no`
- Shape: string

<a id="field-evidence-ref"></a>
## `evidence_ref`

- Required: `no`
- Shape: string

<a id="field-revocation-ref"></a>
## `revocation_ref`

- Required: `no`
- Shape: string

<a id="field-revocation-status"></a>
## `revocation_status`

- Required: `no`
- Shape: enum: `active`, `revoked`, `expired`, `superseded`

<a id="field-portability-profile"></a>
## `portability_profile`

- Required: `yes`
- Shape: ref: `#/$defs/portabilityProfile`

Declared portability floor and extension capability for emergency, communication, and care access modes.

Governing basis:
- [`doc/normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md`](../../normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md)

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-portabilitymodemap"></a>
## `$defs.portabilityModeMap`

- Shape: object

<a id="def-portabilityprofile"></a>
## `$defs.portabilityProfile`

- Shape: object
