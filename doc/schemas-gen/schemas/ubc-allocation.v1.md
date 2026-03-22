# UBC Allocation v1

Source schema: [`doc/schemas/ubc-allocation.v1.schema.json`](../../schemas/ubc-allocation.v1.schema.json)

Machine-readable schema for Universal Basic Compute allocations, including guaranteed access modes and recognition through federation or FIP bridge paths.

## Governing Basis

- [`doc/normative/40-constitution/pl/CONSTITUTION.pl.md`](../../normative/40-constitution/pl/CONSTITUTION.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](../../normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md`](../../normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`allocation_id`](#field-allocation-id) | `yes` | string | Stable identifier of this allocation record. |
| [`subject_ref`](#field-subject-ref) | `yes` | string | Stable anonymous handle of the person receiving the compute floor. |
| [`federation_id`](#field-federation-id) | `yes` | string |  |
| [`attestation_ref`](#field-attestation-ref) | `yes` | string | Reference to the Proof-of-Personhood attestation that justifies the allocation. |
| [`recognition_source`](#field-recognition-source) | `yes` | enum: `federation_local`, `federation_cross_recognition`, `fip_bridge` | Which recognition path made this allocation valid in the current federation. |
| [`recognition_ref`](#field-recognition-ref) | `yes` | string | Reference to the recognizing federation or the FIP bridge. |
| [`measurement_period`](#field-measurement-period) | `yes` | string | Named accounting window used to measure and settle the allocation. |
| [`valid_from`](#field-valid-from) | `yes` | string |  |
| [`valid_until`](#field-valid-until) | `no` | string |  |
| [`compute_unit`](#field-compute-unit) | `yes` | string | Declared unit of account for the allocated compute floor. |
| [`portability_scope`](#field-portability-scope) | `yes` | enum: `local`, `trans_federation_limited`, `trans_federation_extended` | How far this concrete allocation may travel beyond the issuing federation. |
| [`guaranteed_modes`](#field-guaranteed-modes) | `yes` | ref: `#/$defs/guaranteedModes` | Guaranteed access contract for emergency, communication, and care paths. |
| [`funding_policy_ref`](#field-funding-policy-ref) | `yes` | string | Reference to the policy defining who funds the allocation floor. |
| [`limit_policy_ref`](#field-limit-policy-ref) | `yes` | string | Reference to the profile that defines communication and care limits. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |
| [`created_at`](#field-created-at) | `yes` | string |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`modeAccess`](#def-modeaccess) | object |  |
| [`guaranteedModes`](#def-guaranteedmodes) | object |  |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "properties": {
    "guaranteed_modes": {
      "properties": {
        "emergency": {
          "properties": {
            "access": {
              "const": true
            },
            "limit_profile": {
              "const": "unlimited"
            }
          }
        },
        "communication": {
          "properties": {
            "access": {
              "const": true
            }
          }
        },
        "care": {
          "properties": {
            "access": {
              "const": true
            }
          }
        }
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "recognition_source": {
      "const": "fip_bridge"
    }
  },
  "required": [
    "recognition_source"
  ]
}
```

Then:

```json
{
  "properties": {
    "portability_scope": {
      "const": "trans_federation_limited"
    },
    "guaranteed_modes": {
      "properties": {
        "communication": {
          "properties": {
            "limit_profile": {
              "const": "limited"
            }
          },
          "required": [
            "limit_ref"
          ]
        },
        "care": {
          "properties": {
            "limit_profile": {
              "const": "limited"
            }
          },
          "required": [
            "limit_ref"
          ]
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
    "portability_scope": {
      "const": "trans_federation_extended"
    }
  },
  "required": [
    "portability_scope"
  ]
}
```

Then:

```json
{
  "properties": {
    "guaranteed_modes": {
      "properties": {
        "communication": {
          "required": [
            "limit_ref"
          ]
        },
        "care": {
          "required": [
            "limit_ref"
          ]
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

<a id="field-allocation-id"></a>
## `allocation_id`

- Required: `yes`
- Shape: string

Stable identifier of this allocation record.

<a id="field-subject-ref"></a>
## `subject_ref`

- Required: `yes`
- Shape: string

Stable anonymous handle of the person receiving the compute floor.

<a id="field-federation-id"></a>
## `federation_id`

- Required: `yes`
- Shape: string

<a id="field-attestation-ref"></a>
## `attestation_ref`

- Required: `yes`
- Shape: string

Reference to the Proof-of-Personhood attestation that justifies the allocation.

<a id="field-recognition-source"></a>
## `recognition_source`

- Required: `yes`
- Shape: enum: `federation_local`, `federation_cross_recognition`, `fip_bridge`

Which recognition path made this allocation valid in the current federation.

<a id="field-recognition-ref"></a>
## `recognition_ref`

- Required: `yes`
- Shape: string

Reference to the recognizing federation or the FIP bridge.

<a id="field-measurement-period"></a>
## `measurement_period`

- Required: `yes`
- Shape: string

Named accounting window used to measure and settle the allocation.

<a id="field-valid-from"></a>
## `valid_from`

- Required: `yes`
- Shape: string

<a id="field-valid-until"></a>
## `valid_until`

- Required: `no`
- Shape: string

<a id="field-compute-unit"></a>
## `compute_unit`

- Required: `yes`
- Shape: string

Declared unit of account for the allocated compute floor.

<a id="field-portability-scope"></a>
## `portability_scope`

- Required: `yes`
- Shape: enum: `local`, `trans_federation_limited`, `trans_federation_extended`

How far this concrete allocation may travel beyond the issuing federation.

<a id="field-guaranteed-modes"></a>
## `guaranteed_modes`

- Required: `yes`
- Shape: ref: `#/$defs/guaranteedModes`

Guaranteed access contract for emergency, communication, and care paths.

Governing basis:
- [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](../../normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md)
- [`doc/normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md`](../../normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md)

<a id="field-funding-policy-ref"></a>
## `funding_policy_ref`

- Required: `yes`
- Shape: string

Reference to the policy defining who funds the allocation floor.

<a id="field-limit-policy-ref"></a>
## `limit_policy_ref`

- Required: `yes`
- Shape: string

Reference to the profile that defines communication and care limits.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

<a id="field-created-at"></a>
## `created_at`

- Required: `yes`
- Shape: string

## Definition Semantics

<a id="def-modeaccess"></a>
## `$defs.modeAccess`

- Shape: object

<a id="def-guaranteedmodes"></a>
## `$defs.guaranteedModes`

- Shape: object
