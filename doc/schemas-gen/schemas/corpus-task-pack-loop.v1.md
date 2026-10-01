# Corpus Task-pack Loop v1

Source schema: [`doc/schemas/corpus-task-pack-loop.v1.schema.json`](../../schemas/corpus-task-pack-loop.v1.schema.json)

The bounded experiment loop of one Corpus query (P094-023c): its append-only facts and their projection. The requester's Flow drives the deliberation; the host holds its bounds. A claimed passage spends `max/passages` and, for an implementer or a reviewer, its role's counter; a signed proposal opens a cycle; an admitted experiment spends a run, and needs its cycle. A charge has one key, so a replay spends nothing. The loop stops on a verified run, on a run concluded `unknown`, on a run refused for safety, or on cancellation; a run that fails verification, is denied by HIL or is cancelled leaves it going. An exhausted counter or a passed deadline refuses the next charge, and a passed deadline refuses every new effect of an admitted run.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `corpus-task-pack-loop.v1` |  |
| [`query/id`](#field-query-id) | `yes` | string |  |
| [`binding/ref`](#field-binding-ref) | `yes` | string |  |
| [`state`](#field-state) | `yes` | enum: `open`, `deadline-passed`, `stopped` | `open` takes charges; `deadline-passed` waits for a renewal; `stopped` takes nothing more. |
| [`limits`](#field-limits) | `yes` | ref: `#/$defs/limits` |  |
| [`deadline`](#field-deadline) | `yes` | string |  |
| [`spent`](#field-spent) | `yes` | ref: `#/$defs/spent` |  |
| [`stop`](#field-stop) | `no` | ref: `#/$defs/stop` |  |
| [`facts`](#field-facts) | `yes` | array | At most 1366 facts by the loop's own bounds: its opening, every counter at the contract's widest, a conclusion per run, 64 renewals and one cancellation. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`limits`](#def-limits) | ref: `operator-task-common.v1.schema.json#/$defs/deliberationLimits` | The effective limits: every counter is stated. |
| [`spent`](#def-spent) | object |  |
| [`stop`](#def-stop) | unspecified |  |
| [`fact`](#def-fact) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "state": {
      "const": "stopped"
    }
  }
}
```

Then:

```json
{
  "required": [
    "stop"
  ]
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `corpus-task-pack-loop.v1`

<a id="field-query-id"></a>
## `query/id`

- Required: `yes`
- Shape: string

<a id="field-binding-ref"></a>
## `binding/ref`

- Required: `yes`
- Shape: string

<a id="field-state"></a>
## `state`

- Required: `yes`
- Shape: enum: `open`, `deadline-passed`, `stopped`

`open` takes charges; `deadline-passed` waits for a renewal; `stopped` takes nothing more.

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: ref: `#/$defs/limits`

<a id="field-deadline"></a>
## `deadline`

- Required: `yes`
- Shape: string

<a id="field-spent"></a>
## `spent`

- Required: `yes`
- Shape: ref: `#/$defs/spent`

<a id="field-stop"></a>
## `stop`

- Required: `no`
- Shape: ref: `#/$defs/stop`

<a id="field-facts"></a>
## `facts`

- Required: `yes`
- Shape: array

At most 1366 facts by the loop's own bounds: its opening, every counter at the contract's widest, a conclusion per run, 64 renewals and one cancellation.

## Definition Semantics

<a id="def-limits"></a>
## `$defs.limits`

- Shape: ref: `operator-task-common.v1.schema.json#/$defs/deliberationLimits`

The effective limits: every counter is stated.

<a id="def-spent"></a>
## `$defs.spent`

- Shape: object

<a id="def-stop"></a>
## `$defs.stop`

- Shape: unspecified

<a id="def-fact"></a>
## `$defs.fact`

- Shape: object
