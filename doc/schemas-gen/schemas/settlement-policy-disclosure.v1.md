# Settlement Policy Disclosure v1

Source schema: [`doc/schemas/settlement-policy-disclosure.v1.schema.json`](../../schemas/settlement-policy-disclosure.v1.schema.json)

Machine-readable schema for one append-only disclosure or audit event affecting a trusted gateway or escrow policy in the host-ledger settlement rail.

## Governing Basis

- [`doc/project/20-memos/settlement-policy-disclosure-v1-invariants.md`](../../project/20-memos/settlement-policy-disclosure-v1-invariants.md)
- [`doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [`doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`](../../project/40-proposals/017-organization-subjects-and-org-did-key.md)
- [`doc/project/50-requirements/requirements-007.md`](../../project/50-requirements/requirements-007.md)
- [`doc/project/50-requirements/requirements-008.md`](../../project/50-requirements/requirements-008.md)
- [`doc/normative/50-constitutional-ops/pl/ABUSE-DISCLOSURE-PROTOCOL.pl.md`](../../normative/50-constitutional-ops/pl/ABUSE-DISCLOSURE-PROTOCOL.pl.md)

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
| [`disclosure/id`](#field-disclosure-id) | `yes` | string | Stable identifier of this settlement policy disclosure event. |
| [`recorded-at`](#field-recorded-at) | `yes` | string | Timestamp when the disclosure event was committed as an auditable fact. |
| [`effective/from`](#field-effective-from) | `yes` | string | Timestamp from which the disclosed impact becomes effective. |
| [`effective/until`](#field-effective-until) | `no` | string | Optional timestamp until which the disclosed impact remains effective. |
| [`federation/id`](#field-federation-id) | `yes` | string | Federation scope in which the disclosed settlement policy event applies. |
| [`policy/ref`](#field-policy-ref) | `yes` | string | Referenced settlement policy affected by this disclosure event. |
| [`operator/org-ref`](#field-operator-org-ref) | `yes` | string | Accountable organization operating the affected settlement policy at event time. |
| [`serving/node-id`](#field-serving-node-id) | `yes` | string | Serving node observed under the affected settlement policy at event time. |
| [`event/type`](#field-event-type) | `yes` | string | Open event namespace for settlement-policy disclosures. Example families: `lifecycle/suspended`, `limits/tightened`, `incident/opened`. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | enum: `internal-only`, `federation-redacted`, `federation-scoped`, `public-redacted` | Maximum disclosure scope admitted for this event. |
| [`impact/mode`](#field-impact-mode) | `yes` | enum: `informational`, `degraded`, `blocked`, `manual-review-only` | Practical operator impact implied by the disclosed event. |
| [`reason/summary`](#field-reason-summary) | `yes` | string | Short human-readable summary explaining why the disclosure event exists. |
| [`changed/fields`](#field-changed-fields) | `no` | array | Optional policy fields or operational dimensions materially affected by this disclosure event. |
| [`case/ref`](#field-case-ref) | `no` | string | Optional review or incident case reference. |
| [`exception/ref`](#field-exception-ref) | `no` | string | Optional bounded exception record authorizing or constraining the disclosed event. |
| [`basis/refs`](#field-basis-refs) | `no` | array | Optional references to receipts, holds, incident materials, or other audit artifacts that justify the disclosure event. |
| [`supersedes/ref`](#field-supersedes-ref) | `no` | string | Optional earlier disclosure event superseded by this one. |
| [`notes`](#field-notes) | `no` | string | Optional human-readable notes. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "event/type": {
      "pattern": "^incident/"
    }
  },
  "required": [
    "event/type"
  ]
}
```

Then:

```json
{
  "anyOf": [
    {
      "required": [
        "case/ref"
      ]
    },
    {
      "required": [
        "exception/ref"
      ]
    },
    {
      "properties": {
        "basis/refs": {
          "minItems": 1
        }
      },
      "required": [
        "basis/refs"
      ]
    }
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-disclosure-id"></a>
## `disclosure/id`

- Required: `yes`
- Shape: string

Stable identifier of this settlement policy disclosure event.

<a id="field-recorded-at"></a>
## `recorded-at`

- Required: `yes`
- Shape: string

Timestamp when the disclosure event was committed as an auditable fact.

<a id="field-effective-from"></a>
## `effective/from`

- Required: `yes`
- Shape: string

Timestamp from which the disclosed impact becomes effective.

<a id="field-effective-until"></a>
## `effective/until`

- Required: `no`
- Shape: string

Optional timestamp until which the disclosed impact remains effective.

<a id="field-federation-id"></a>
## `federation/id`

- Required: `yes`
- Shape: string

Federation scope in which the disclosed settlement policy event applies.

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

Referenced settlement policy affected by this disclosure event.

<a id="field-operator-org-ref"></a>
## `operator/org-ref`

- Required: `yes`
- Shape: string

Accountable organization operating the affected settlement policy at event time.

<a id="field-serving-node-id"></a>
## `serving/node-id`

- Required: `yes`
- Shape: string

Serving node observed under the affected settlement policy at event time.

<a id="field-event-type"></a>
## `event/type`

- Required: `yes`
- Shape: string

Open event namespace for settlement-policy disclosures. Example families: `lifecycle/suspended`, `limits/tightened`, `incident/opened`.

<a id="field-disclosure-scope"></a>
## `disclosure/scope`

- Required: `yes`
- Shape: enum: `internal-only`, `federation-redacted`, `federation-scoped`, `public-redacted`

Maximum disclosure scope admitted for this event.

<a id="field-impact-mode"></a>
## `impact/mode`

- Required: `yes`
- Shape: enum: `informational`, `degraded`, `blocked`, `manual-review-only`

Practical operator impact implied by the disclosed event.

<a id="field-reason-summary"></a>
## `reason/summary`

- Required: `yes`
- Shape: string

Short human-readable summary explaining why the disclosure event exists.

<a id="field-changed-fields"></a>
## `changed/fields`

- Required: `no`
- Shape: array

Optional policy fields or operational dimensions materially affected by this disclosure event.

<a id="field-case-ref"></a>
## `case/ref`

- Required: `no`
- Shape: string

Optional review or incident case reference.

<a id="field-exception-ref"></a>
## `exception/ref`

- Required: `no`
- Shape: string

Optional bounded exception record authorizing or constraining the disclosed event.

<a id="field-basis-refs"></a>
## `basis/refs`

- Required: `no`
- Shape: array

Optional references to receipts, holds, incident materials, or other audit artifacts that justify the disclosure event.

<a id="field-supersedes-ref"></a>
## `supersedes/ref`

- Required: `no`
- Shape: string

Optional earlier disclosure event superseded by this one.

<a id="field-notes"></a>
## `notes`

- Required: `no`
- Shape: string

Optional human-readable notes.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object
