# Ledger Account v1

Source schema: [`doc/schemas/ledger-account.v1.schema.json`](../../schemas/ledger-account.v1.schema.json)

Machine-readable schema for one supervised prepaid ledger account used by the host-ledger settlement rail.

## Governing Basis

- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`](../../project/40-proposals/007-pod-identity-and-tenancy-model.md)
- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`account/id`](#field-account-id) | `yes` | string | Stable identifier of the supervised ledger account. |
| [`account/purpose`](#field-account-purpose) | `yes` | enum: `participant-settlement`, `pod-user-settlement`, `org-settlement`, `community-pool` | Operational purpose of the account within the host-ledger rail. |
| [`owner/kind`](#field-owner-kind) | `yes` | enum: `participant`, `pod-user`, `org` | Identity layer that owns the account. |
| [`owner/id`](#field-owner-id) | `yes` | string | Canonical identifier of the account owner. The allowed format depends on `owner/kind`. |
| [`federation/id`](#field-federation-id) | `yes` | string | Authoritative federation ledger scope for this account. |
| [`unit`](#field-unit) | `yes` | const: `ORC` | Internal settlement unit carried by this account in MVP. `ORC` uses fixed decimal scale `2`; protocol-visible integer balances therefore carry ORC minor units. |
| [`status`](#field-status) | `yes` | enum: `active`, `suspended`, `closed` | Administrative state of the account on the supervised ledger. |
| [`available/balance`](#field-available-balance) | `no` | integer | Optional exported read-model snapshot of immediately spendable balance in ORC minor units with fixed scale `2`. The append-only transfer and hold facts remain the source of truth. |
| [`held/balance`](#field-held-balance) | `no` | integer | Optional exported read-model snapshot of funds currently reserved by active holds in ORC minor units with fixed scale `2`. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the account was opened. |
| [`closed-at`](#field-closed-at) | `no` | string | Timestamp when the account was closed, if applicable. |
| [`gateway/ref`](#field-gateway-ref) | `no` | string | Optional reference to the gateway or onboarding policy under which the account was provisioned. |
| [`disbursement/controller-kind`](#field-disbursement-controller-kind) | `no` | enum: `owner`, `council` | Who is allowed to authorize outbound disbursement from this account. |
| [`disbursement/controller-id`](#field-disbursement-controller-id) | `no` | string | Canonical identifier of the disbursement controller when it differs from the owner. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "account/purpose": {
      "const": "community-pool"
    }
  },
  "required": [
    "account/purpose"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/kind": {
      "const": "org"
    },
    "disbursement/controller-kind": {
      "const": "council"
    },
    "disbursement/controller-id": {
      "pattern": "^council:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  },
  "required": [
    "disbursement/controller-kind",
    "disbursement/controller-id"
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "participant"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^participant:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "pod-user"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^pod-user:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 4

When:

```json
{
  "properties": {
    "owner/kind": {
      "const": "org"
    }
  },
  "required": [
    "owner/kind"
  ]
}
```

Then:

```json
{
  "properties": {
    "owner/id": {
      "pattern": "^org:did:key:z[1-9A-HJ-NP-Za-km-z]+$"
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "status": {
      "const": "closed"
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
    "closed-at"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-account-id"></a>
## `account/id`

- Required: `yes`
- Shape: string

Stable identifier of the supervised ledger account.

<a id="field-account-purpose"></a>
## `account/purpose`

- Required: `yes`
- Shape: enum: `participant-settlement`, `pod-user-settlement`, `org-settlement`, `community-pool`

Operational purpose of the account within the host-ledger rail.

<a id="field-owner-kind"></a>
## `owner/kind`

- Required: `yes`
- Shape: enum: `participant`, `pod-user`, `org`

Identity layer that owns the account.

<a id="field-owner-id"></a>
## `owner/id`

- Required: `yes`
- Shape: string

Canonical identifier of the account owner. The allowed format depends on `owner/kind`.

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

Authoritative federation ledger scope for this account.

<a id="field-unit"></a>
## `unit`

- Required: `yes`
- Shape: const: `ORC`

Internal settlement unit carried by this account in MVP. `ORC` uses fixed decimal scale `2`; protocol-visible integer balances therefore carry ORC minor units.

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: enum: `active`, `suspended`, `closed`

Administrative state of the account on the supervised ledger.

<a id="field-available-balance"></a>
## `available/balance`

- Required: `no`
- Shape: integer

Optional exported read-model snapshot of immediately spendable balance in ORC minor units with fixed scale `2`. The append-only transfer and hold facts remain the source of truth.

<a id="field-held-balance"></a>
## `held/balance`

- Required: `no`
- Shape: integer

Optional exported read-model snapshot of funds currently reserved by active holds in ORC minor units with fixed scale `2`.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the account was opened.

<a id="field-closed-at"></a>
## `closed-at`

- Required: `no`
- Shape: string

Timestamp when the account was closed, if applicable.

<a id="field-gateway-ref"></a>
## `gateway/ref`

- Required: `no`
- Shape: string

Optional reference to the gateway or onboarding policy under which the account was provisioned.

<a id="field-disbursement-controller-kind"></a>
## `disbursement/controller-kind`

- Required: `no`
- Shape: enum: `owner`, `council`

Who is allowed to authorize outbound disbursement from this account.

<a id="field-disbursement-controller-id"></a>
## `disbursement/controller-id`

- Required: `no`
- Shape: string

Canonical identifier of the disbursement controller when it differs from the owner.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
