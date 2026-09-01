# Agent External Runtime Event v1

Source schema: [`doc/schemas/agent.external-runtime.event.v1.schema.json`](../../schemas/agent.external-runtime.event.v1.schema.json)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`digest`](#def-digest) | string |  |
| [`at`](#def-at) | string |  |
| [`base-properties`](#def-base-properties) | object |  |
| [`progress`](#def-progress) | object |  |
| [`action-candidate`](#def-action-candidate) | object |  |
| [`product-candidate`](#def-product-candidate) | object |  |
| [`tool-request`](#def-tool-request) | object |  |
| [`operator-question`](#def-operator-question) | object |  |
| [`usage`](#def-usage) | object |  |
| [`turn-outcome`](#def-turn-outcome) | object |  |
| [`usage-value`](#def-usage-value) | object |  |
| [`reason-code`](#def-reason-code) | enum: `completed`, `policy-denied`, `binding-missing`, `binding-stale`, `binding-mismatch`, `binding-expired`, `binding-revoked`, `profile-disabled`, `profile-mismatch`, `budget-exhausted`, `usage-missing`, `usage-malformed`, `usage-overflow`, `usage-conflict`, `session-fence-mismatch`, `session-lost`, `event-malformed`, `event-duplicate`, `event-reordered`, `event-oversized`, `event-unauthorized`, `event-stale`, `event-timeout`, `tool-not-admitted`, `approval-not-admitted`, `provider-unavailable`, `cancelled`, `unknown` |  |
## Field Semantics

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-at"></a>
## `$defs.at`

- Shape: string

<a id="def-base-properties"></a>
## `$defs.base-properties`

- Shape: object

<a id="def-progress"></a>
## `$defs.progress`

- Shape: object

<a id="def-action-candidate"></a>
## `$defs.action-candidate`

- Shape: object

<a id="def-product-candidate"></a>
## `$defs.product-candidate`

- Shape: object

<a id="def-tool-request"></a>
## `$defs.tool-request`

- Shape: object

<a id="def-operator-question"></a>
## `$defs.operator-question`

- Shape: object

<a id="def-usage"></a>
## `$defs.usage`

- Shape: object

<a id="def-turn-outcome"></a>
## `$defs.turn-outcome`

- Shape: object

<a id="def-usage-value"></a>
## `$defs.usage-value`

- Shape: object

<a id="def-reason-code"></a>
## `$defs.reason-code`

- Shape: enum: `completed`, `policy-denied`, `binding-missing`, `binding-stale`, `binding-mismatch`, `binding-expired`, `binding-revoked`, `profile-disabled`, `profile-mismatch`, `budget-exhausted`, `usage-missing`, `usage-malformed`, `usage-overflow`, `usage-conflict`, `session-fence-mismatch`, `session-lost`, `event-malformed`, `event-duplicate`, `event-reordered`, `event-oversized`, `event-unauthorized`, `event-stale`, `event-timeout`, `tool-not-admitted`, `approval-not-admitted`, `provider-unavailable`, `cancelled`, `unknown`
