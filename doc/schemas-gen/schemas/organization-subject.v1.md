# Organization Subject v1

Source schema: [`doc/schemas/organization-subject.v1.schema.json`](../../schemas/organization-subject.v1.schema.json)

Machine-readable schema for a canonical organization-scoped accountability subject and its MVP custody anchor.

## Governing Basis

- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`org/id`](#field-org-id) | `yes` | string | Canonical organization subject identifier. |
| [`created-at`](#field-created-at) | `yes` | string | Timestamp when the organization subject was first provisioned. |
| [`org/status`](#field-org-status) | `yes` | enum: `active`, `suspended`, `retired` | Administrative status of the organization subject. |
| [`org/display-name`](#field-org-display-name) | `no` | string | Optional human-facing display name. |
| [`org/legal-name`](#field-org-legal-name) | `no` | string | Optional legal or registry name when the federation tracks it. |
| [`org/key/alg`](#field-org-key-alg) | `yes` | enum: `ed25519` | Verification algorithm backing the canonical organization identifier. |
| [`org/key/public`](#field-org-key-public) | `yes` | string | Canonical did:key fingerprint payload for the organization subject without the `org:did:key:` prefix. |
| [`org/custodian-ref`](#field-org-custodian-ref) | `yes` | string | MVP human-side custodian responsible for administering this organization subject. |
| [`org/custody-mode`](#field-org-custody-mode) | `no` | enum: `single-custodian` | Custody mode of the organization subject. MVP freezes `single-custodian` only. |
| [`suspended-at`](#field-suspended-at) | `no` | string | Timestamp when the organization subject was suspended, if applicable. |
| [`retired-at`](#field-retired-at) | `no` | string | Timestamp when the organization subject was retired, if applicable. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "org/custody-mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "org/custody-mode": {
      "const": "single-custodian"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "org/status": {
      "const": "suspended"
    }
  },
  "required": [
    "org/status"
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

### Rule 3

When:

```json
{
  "properties": {
    "org/status": {
      "const": "retired"
    }
  },
  "required": [
    "org/status"
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

<a id="field-org-id"></a>
## `org/id`

- Required: `yes`
- Shape: string

Canonical organization subject identifier.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Timestamp when the organization subject was first provisioned.

<a id="field-org-status"></a>
## `org/status`

- Required: `yes`
- Shape: enum: `active`, `suspended`, `retired`

Administrative status of the organization subject.

<a id="field-org-display-name"></a>
## `org/display-name`

- Required: `no`
- Shape: string

Optional human-facing display name.

<a id="field-org-legal-name"></a>
## `org/legal-name`

- Required: `no`
- Shape: string

Optional legal or registry name when the federation tracks it.

<a id="field-org-key-alg"></a>
## `org/key/alg`

- Required: `yes`
- Shape: enum: `ed25519`

Verification algorithm backing the canonical organization identifier.

<a id="field-org-key-public"></a>
## `org/key/public`

- Required: `yes`
- Shape: string

Canonical did:key fingerprint payload for the organization subject without the `org:did:key:` prefix.

<a id="field-org-custodian-ref"></a>
## `org/custodian-ref`

- Required: `yes`
- Shape: string

MVP human-side custodian responsible for administering this organization subject.

<a id="field-org-custody-mode"></a>
## `org/custody-mode`

- Required: `no`
- Shape: enum: `single-custodian`

Custody mode of the organization subject. MVP freezes `single-custodian` only.

<a id="field-suspended-at"></a>
## `suspended-at`

- Required: `no`
- Shape: string

Timestamp when the organization subject was suspended, if applicable.

<a id="field-retired-at"></a>
## `retired-at`

- Required: `no`
- Shape: string

Timestamp when the organization subject was retired, if applicable.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
