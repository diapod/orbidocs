# Panel-procedure.local.v1

Source schema: [`doc/schemas/panel-procedure.local.v1.schema.json`](../../schemas/panel-procedure.local.v1.schema.json)

Draft local fixture contract. Shape validation confers no admission, mandate, application receipt or normative ELL2 qualification.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md`](../../normative/50-constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `panel-procedure.local.v1` |  |
| [`id`](#field-id) | `yes` | string |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`context`](#field-context) | `yes` | object |  |
| [`inputs`](#field-inputs) | `yes` | ref: `panel-round-inputs.local.v1.schema.json` |  |
| [`round`](#field-round) | `yes` | integer |  |
| [`filed-at`](#field-filed-at) | `yes` | string |  |
| [`opened-at`](#field-opened-at) | `yes` | string |  |
| [`phase-until`](#field-phase-until) | `yes` | string |  |
| [`phase`](#field-phase) | `yes` | unspecified |  |
| [`declarations`](#field-declarations) | `yes` | object |  |
| [`pool`](#field-pool) | `yes` | array |  |
| [`exclusions`](#field-exclusions) | `yes` | object |  |
| [`commits`](#field-commits) | `yes` | object |  |
| [`reveals`](#field-reveals) | `yes` | object |  |
| [`transcript`](#field-transcript) | `yes` | unspecified |  |
| [`primaries`](#field-primaries) | `yes` | array |  |
| [`reserves`](#field-reserves) | `yes` | array |  |
| [`removed`](#field-removed) | `yes` | array |  |
| [`compromised`](#field-compromised) | `yes` | array |  |
| [`vetoes`](#field-vetoes) | `yes` | array |  |
| [`composition/revision`](#field-composition-revision) | `yes` | integer |  |
| [`proposal`](#field-proposal) | `yes` | unspecified |  |
| [`votes`](#field-votes) | `yes` | object |  |
| [`commands`](#field-commands) | `yes` | object |  |
| [`veto-history`](#field-veto-history) | `yes` | array | Durable veto history: one veto right per party for the whole selection procedure; replacement never renews it. |
| [`activity`](#field-activity) | `yes` | object | Last seating, deliberation start or panel action per seated node; the inactivity window is measured from it. |
| [`deliberation-until`](#field-deliberation-until) | `yes` | unspecified | Running deliberation deadline. Replacement extends it by replacement-extension instead of restarting the window. |
| [`rejected-proposals`](#field-rejected-proposals) | `yes` | array | Durable rejections bound to proposal id, voting composition revision and digest. A rejection reopens deliberation; it never concludes uphold. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `panel-procedure.local.v1`

<a id="field-id"></a>
## `id`

- Required: `yes`
- Shape: string

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-context"></a>
## `context`

- Required: `yes`
- Shape: object

<a id="field-inputs"></a>
## `inputs`

- Required: `yes`
- Shape: ref: `panel-round-inputs.local.v1.schema.json`

<a id="field-round"></a>
## `round`

- Required: `yes`
- Shape: integer

<a id="field-filed-at"></a>
## `filed-at`

- Required: `yes`
- Shape: string

<a id="field-opened-at"></a>
## `opened-at`

- Required: `yes`
- Shape: string

<a id="field-phase-until"></a>
## `phase-until`

- Required: `yes`
- Shape: string

<a id="field-phase"></a>
## `phase`

- Required: `yes`
- Shape: unspecified

<a id="field-declarations"></a>
## `declarations`

- Required: `yes`
- Shape: object

<a id="field-pool"></a>
## `pool`

- Required: `yes`
- Shape: array

<a id="field-exclusions"></a>
## `exclusions`

- Required: `yes`
- Shape: object

<a id="field-commits"></a>
## `commits`

- Required: `yes`
- Shape: object

<a id="field-reveals"></a>
## `reveals`

- Required: `yes`
- Shape: object

<a id="field-transcript"></a>
## `transcript`

- Required: `yes`
- Shape: unspecified

<a id="field-primaries"></a>
## `primaries`

- Required: `yes`
- Shape: array

<a id="field-reserves"></a>
## `reserves`

- Required: `yes`
- Shape: array

<a id="field-removed"></a>
## `removed`

- Required: `yes`
- Shape: array

<a id="field-compromised"></a>
## `compromised`

- Required: `yes`
- Shape: array

<a id="field-vetoes"></a>
## `vetoes`

- Required: `yes`
- Shape: array

<a id="field-composition-revision"></a>
## `composition/revision`

- Required: `yes`
- Shape: integer

<a id="field-proposal"></a>
## `proposal`

- Required: `yes`
- Shape: unspecified

<a id="field-votes"></a>
## `votes`

- Required: `yes`
- Shape: object

<a id="field-commands"></a>
## `commands`

- Required: `yes`
- Shape: object

<a id="field-veto-history"></a>
## `veto-history`

- Required: `yes`
- Shape: array

Durable veto history: one veto right per party for the whole selection procedure; replacement never renews it.

<a id="field-activity"></a>
## `activity`

- Required: `yes`
- Shape: object

Last seating, deliberation start or panel action per seated node; the inactivity window is measured from it.

<a id="field-deliberation-until"></a>
## `deliberation-until`

- Required: `yes`
- Shape: unspecified

Running deliberation deadline. Replacement extends it by replacement-extension instead of restarting the window.

<a id="field-rejected-proposals"></a>
## `rejected-proposals`

- Required: `yes`
- Shape: array

Durable rejections bound to proposal id, voting composition revision and digest. A rejection reopens deliberation; it never concludes uphold.
