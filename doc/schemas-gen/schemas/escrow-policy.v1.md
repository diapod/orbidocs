# Escrow Policy v1

Source schema: [`doc/schemas/escrow-policy.v1.schema.json`](../../schemas/escrow-policy.v1.schema.json)

Machine-readable schema for one trusted escrow policy binding a supervisory settlement node to an accountable organization in the host-ledger rail.

## Governing Basis

- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`policy/id`](#field-policy-id) | `yes` | string | Stable identifier of the escrow policy. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the escrow policy became auditable. |
| [`federation/id`](#field-federation-id) | `yes` | string | Federation scope in which the escrow policy applies. |
| [`escrow/node-id`](#field-escrow-node-id) | `yes` | string | Node currently serving the escrow supervisor role under this policy. |
| [`operator/org-ref`](#field-operator-org-ref) | `yes` | string | Accountable organization operating the escrow policy. |
| [`settlement/unit`](#field-settlement-unit) | `yes` | const: `ORC` | Internal settlement unit governed by this escrow policy in MVP. |
| [`confirmation/modes`](#field-confirmation-modes) | `yes` | array | Confirmation modes admitted by the escrow policy. |
| [`dispute/default-window-sec`](#field-dispute-default-window-sec) | `yes` | integer | Default dispute window applied when a contract does not override it. |
| [`auto-release/default-sec`](#field-auto-release-default-sec) | `yes` | integer | Default auto-release delay applied after the relevant acceptance stage when a contract does not override it. |
| [`partial-release/allowed`](#field-partial-release-allowed) | `yes` | boolean | Whether partial release is permitted under this escrow policy. |
| [`arbiter/required-above-risk`](#field-arbiter-required-above-risk) | `no` | enum: `none`, `medium`, `high`, `critical` | Minimum risk tier above which arbiter confirmation becomes mandatory under local policy. |
| [`status`](#field-status) | `yes` | enum: `active`, `suspended`, `retired` | Administrative lifecycle state of the escrow policy. |
| [`suspended-at`](#field-suspended-at) | `no` | string | Timestamp when the escrow policy was suspended, if applicable. |
| [`retired-at`](#field-retired-at) | `no` | string | Timestamp when the escrow policy was retired, if applicable. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "status": {
      "const": "suspended"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "suspended-at"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "status": {
      "const": "retired"
    }
  },
  "required": [
    "status"
  ]
}
```

Then:

```json
{
  "required": [
    "retired-at"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

Stable identifier of the escrow policy.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the escrow policy became auditable.

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

Federation scope in which the escrow policy applies.

<a id="field-escrow-node-id"></a>
## `escrow/node-id`

- Required: `yes`
- Shape: string

Node currently serving the escrow supervisor role under this policy.

<a id="field-operator-org-ref"></a>
## `operator/org-ref`

- Required: `yes`
- Shape: string

Accountable organization operating the escrow policy.

<a id="field-settlement-unit"></a>
## `settlement/unit`

- Required: `yes`
- Shape: const: `ORC`

Internal settlement unit governed by this escrow policy in MVP.

<a id="field-confirmation-modes"></a>
## `confirmation/modes`

- Required: `yes`
- Shape: array

Confirmation modes admitted by the escrow policy.

<a id="field-dispute-default-window-sec"></a>
## `dispute/default-window-sec`

- Required: `yes`
- Shape: integer

Default dispute window applied when a contract does not override it.

<a id="field-auto-release-default-sec"></a>
## `auto-release/default-sec`

- Required: `yes`
- Shape: integer

Default auto-release delay applied after the relevant acceptance stage when a contract does not override it.

<a id="field-partial-release-allowed"></a>
## `partial-release/allowed`

- Required: `yes`
- Shape: boolean

Whether partial release is permitted under this escrow policy.

<a id="field-arbiter-required-above-risk"></a>
## `arbiter/required-above-risk`

- Required: `no`
- Shape: enum: `none`, `medium`, `high`, `critical`

Minimum risk tier above which arbiter confirmation becomes mandatory under local policy.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `active`, `suspended`, `retired`

Administrative lifecycle state of the escrow policy.

<a id="field-suspended-at"></a>
## `suspended-at`

- Required: `no`
- Shape: string

Timestamp when the escrow policy was suspended, if applicable.

<a id="field-retired-at"></a>
## `retired-at`

- Required: `no`
- Shape: string

Timestamp when the escrow policy was retired, if applicable.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
