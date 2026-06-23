# Room Policy v1

Source schema: [`doc/schemas/room-policy.v1.schema.json`](../../schemas/room-policy.v1.schema.json)

Room access, exposure and retention policy referenced by room.v1.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)
- [`P009`](../../project/40-proposals/009-communication-exposure-modes.md)
- [`P005`](../../project/40-proposals/005-operator-participation-room-policy-profiles.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string |  |
| [`access/closed`](#field-access-closed) | `yes` | boolean |  |
| [`access/list`](#field-access-list) | `yes` | array |  |
| [`exposure`](#field-exposure) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` |  |
| [`policy/profile`](#field-policy-profile) | `yes` | enum: `none`, `mediated-only`, `direct-live-allowed` |  |
| [`human/linked-messages`](#field-human-linked-messages) | `yes` | enum: `denied`, `allowed-via-node-mediation`, `allowed` |  |
| [`human/live-participation`](#field-human-live-participation) | `yes` | enum: `denied`, `allowed` |  |
| [`live/retention`](#field-live-retention) | `yes` | enum: `non-retained`, `member-local-capture-only`, `public-policy-defined` |  |
| [`max/live-message-bytes`](#field-max-live-message-bytes) | `no` | integer |  |
| [`created-at`](#field-created-at) | `yes` | string |  |
| [`expires-at`](#field-expires-at) | `no` | string |  |
| [`extensions`](#field-extensions) | `no` | ref: `room.v1.schema.json#/$defs/extensions` |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "policy/profile": {
      "const": "none"
    }
  },
  "required": [
    "policy/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "human/linked-messages": {
      "const": "denied"
    },
    "human/live-participation": {
      "const": "denied"
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "policy/profile": {
      "const": "mediated-only"
    }
  },
  "required": [
    "policy/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "human/linked-messages": {
      "const": "allowed-via-node-mediation"
    },
    "human/live-participation": {
      "const": "denied"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "policy/profile": {
      "const": "direct-live-allowed"
    }
  },
  "required": [
    "policy/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "human/linked-messages": {
      "const": "allowed"
    },
    "human/live-participation": {
      "const": "allowed"
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

<a id="field-access-closed"></a>
## `access/closed`

- Required: `yes`
- Shape: boolean

<a id="field-access-list"></a>
## `access/list`

- Required: `yes`
- Shape: array

<a id="field-exposure"></a>
## `exposure`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

<a id="field-policy-profile"></a>
## `policy/profile`

- Required: `yes`
- Shape: enum: `none`, `mediated-only`, `direct-live-allowed`

<a id="field-human-linked-messages"></a>
## `human/linked-messages`

- Required: `yes`
- Shape: enum: `denied`, `allowed-via-node-mediation`, `allowed`

<a id="field-human-live-participation"></a>
## `human/live-participation`

- Required: `yes`
- Shape: enum: `denied`, `allowed`

<a id="field-live-retention"></a>
## `live/retention`

- Required: `yes`
- Shape: enum: `non-retained`, `member-local-capture-only`, `public-policy-defined`

<a id="field-max-live-message-bytes"></a>
## `max/live-message-bytes`

- Required: `no`
- Shape: integer

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

<a id="field-expires-at"></a>
## `expires-at`

- Required: `no`
- Shape: string

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: ref: `room.v1.schema.json#/$defs/extensions`
