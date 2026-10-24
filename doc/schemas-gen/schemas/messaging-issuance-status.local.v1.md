# Messaging-issuance-status.local.v1

Source schema: [`doc/schemas/messaging-issuance-status.local.v1.schema.json`](../../schemas/messaging-issuance-status.local.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/076-limited-messaging-grants-decision.md`](../../project/40-proposals/076-limited-messaging-grants-decision.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `messaging-issuance-status.local.v1` |  |
| [`participant_id`](#field-participant-id) | `yes` | string |  |
| [`observed_at`](#field-observed-at) | `yes` | string |  |
| [`grants`](#field-grants) | `yes` | array |  |
| [`consent_window`](#field-consent-window) | `no` | object | Optional host-selected child window, global or restricted to the requested delegation_id. Child IDs and withdrawal lists refer only to this window; passport_total counts all local children of each selected grant. No off-window scopes are serialized. |
| [`presentation_observations`](#field-presentation-observations) | `no` | object | Optional host-lifetime metadata counters, not authorization or delivery counts. Omitted when the counter observation is unavailable. |

## Conditional Rules

### Rule 1

When:

```json
{
  "required": [
    "consent_window"
  ]
}
```

Then:

```json
{
  "properties": {
    "grants": {
      "items": {
        "required": [
          "passport_total"
        ],
        "properties": {
          "passports": {
            "maxItems": 25
          },
          "passport_ids": {
            "maxItems": 25
          },
          "withdrawn_passport_ids": {
            "maxItems": 25
          },
          "withdrawal_publication_pending": {
            "maxItems": 25
          }
        }
      }
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `messaging-issuance-status.local.v1`

<a id="field-participant-id"></a>
## `participant_id`

- Required: `yes`
- Shape: string

<a id="field-observed-at"></a>
## `observed_at`

- Required: `yes`
- Shape: string

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: array

<a id="field-consent-window"></a>
## `consent_window`

- Required: `no`
- Shape: object

Optional host-selected child window, global or restricted to the requested delegation_id. Child IDs and withdrawal lists refer only to this window; passport_total counts all local children of each selected grant. No off-window scopes are serialized.

<a id="field-presentation-observations"></a>
## `presentation_observations`

- Required: `no`
- Shape: object

Optional host-lifetime metadata counters, not authorization or delivery counts. Omitted when the counter observation is unavailable.
