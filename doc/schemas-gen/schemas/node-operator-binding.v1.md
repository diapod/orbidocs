# Node Operator Binding v1

Source schema: [`doc/schemas/node-operator-binding.v1.schema.json`](../../schemas/node-operator-binding.v1.schema.json)

Machine-readable schema for a node-held operator-assurance certificate. The binding is a bundle over `capability-passport.v1`: the operator participant issues a `node-primary-operator` passport to the target node, and the node signs a separate acceptance proving that it accepts that participant as primary operator. Derived node assurance remains an eligibility gate, not reputation.

## Governing Basis

- [`doc/project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md`](../../project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md)
- [`doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`](../../project/40-proposals/024-capability-passports-and-network-ledger-delegation.md)
- [`doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
- [`doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`](../../normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md)
- [`doc/normative/50-constitutional-ops/pl/ROLE-TO-IAL-MATRIX.pl.md`](../../normative/50-constitutional-ops/pl/ROLE-TO-IAL-MATRIX.pl.md)

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
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`binding/id`](#field-binding-id) | `yes` | string | Stable identifier of this node/operator binding bundle. |
| [`binding/status`](#field-binding-status) | `yes` | enum: `active`, `revoked`, `expired`, `superseded` | Lifecycle state of this binding bundle. Passport expiry or revocation should drive this projection. |
| [`passport`](#field-passport) | `yes` | object | Full `capability-passport.v1` artifact issued by the operator participant. In this profile it is the participant-side consent claim: I agree to be primary operator of this target node. |
| [`node_acceptance`](#field-node-acceptance) | `yes` | object | Node-side acceptance proving that the target node accepts the passport issuer as its primary operator. A participant-issued passport without this node acceptance is not a binding. |
| [`published/disclosure-mode`](#field-published-disclosure-mode) | `no` | enum: `local-only`, `present-on-demand`, `seed-directory` | Disclosure posture for this binding. `seed-directory` means the node explicitly chose higher availability for the node/operator relation. |
| [`seed-directory/ref`](#field-seed-directory-ref) | `no` | string | Optional Seed Directory publication reference when disclosure mode is `seed-directory`. |
| [`revocation/ref`](#field-revocation-ref) | `no` | string | Reference to the record that revoked or superseded this binding. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional local or federation policy annotations that do not change the core binding semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`assuranceLevel`](#def-assurancelevel) | enum: `IAL0`, `IAL1`, `IAL2`, `IAL3`, `IAL4` | Identity assurance level recognized by the surrounding policy for participant/operator identity proofing. |
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "binding/status": {
      "const": "revoked"
    }
  },
  "required": [
    "binding/status"
  ]
}
```

Then:

```json
{
  "required": [
    "revocation/ref"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "published/disclosure-mode": {
      "const": "seed-directory"
    }
  },
  "required": [
    "published/disclosure-mode"
  ]
}
```

Then:

```json
{
  "required": [
    "seed-directory/ref"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-binding-id"></a>
## `binding/id`

- Required: `yes`
- Shape: string

Stable identifier of this node/operator binding bundle.

<a id="field-binding-status"></a>
## `binding/status`

- Required: `yes`
- Shape: enum: `active`, `revoked`, `expired`, `superseded`

Lifecycle state of this binding bundle. Passport expiry or revocation should drive this projection.

<a id="field-passport"></a>
## `passport`

- Required: `yes`
- Shape: object

Full `capability-passport.v1` artifact issued by the operator participant. In this profile it is the participant-side consent claim: I agree to be primary operator of this target node.

<a id="field-node-acceptance"></a>
## `node_acceptance`

- Required: `yes`
- Shape: object

Node-side acceptance proving that the target node accepts the passport issuer as its primary operator. A participant-issued passport without this node acceptance is not a binding.

<a id="field-published-disclosure-mode"></a>
## `published/disclosure-mode`

- Required: `no`
- Shape: enum: `local-only`, `present-on-demand`, `seed-directory`

Disclosure posture for this binding. `seed-directory` means the node explicitly chose higher availability for the node/operator relation.

<a id="field-seed-directory-ref"></a>
## `seed-directory/ref`

- Required: `no`
- Shape: string

Optional Seed Directory publication reference when disclosure mode is `seed-directory`.

<a id="field-revocation-ref"></a>
## `revocation/ref`

- Required: `no`
- Shape: string

Reference to the record that revoked or superseded this binding.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional local or federation policy annotations that do not change the core binding semantics.

## Definition Semantics

<a id="def-assurancelevel"></a>
## `$defs.assuranceLevel`

- Shape: enum: `IAL0`, `IAL1`, `IAL2`, `IAL3`, `IAL4`

Identity assurance level recognized by the surrounding policy for participant/operator identity proofing.

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
