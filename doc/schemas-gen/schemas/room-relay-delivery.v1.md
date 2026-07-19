# Room Relay Delivery v1

Source schema: [`doc/schemas/room-relay-delivery.v1.schema.json`](../../schemas/room-relay-delivery.v1.schema.json)

Ephemeral member-visible relay delivery that binds a validated Room carrier payload to one relay epoch and total-order sequence. A bounded audience carries source-admission evidence for recipient-filtered payloads but grants no independent authority. The explicit delivery/kind discriminator prevents ambiguity with encrypted deliveries. It MUST NOT contain session bearers.

## Governing Basis

- [`P070`](../../project/40-proposals/070-room-primitive.md)
- [`P082`](../../project/40-proposals/082-sensorium-interfaces.md)
- [`P083`](../../project/40-proposals/083-sensorium-interactive-interfaces.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`delivery/kind`](#field-delivery-kind) | `yes` | const: `member-visible` |  |
| [`room/id`](#field-room-id) | `yes` | ref: `room.v1.schema.json#/$defs/room_id` |  |
| [`relay/epoch`](#field-relay-epoch) | `yes` | integer |  |
| [`relay/seq-no`](#field-relay-seq-no) | `yes` | integer |  |
| [`sender/subject`](#field-sender-subject) | `yes` | ref: `room.v1.schema.json#/$defs/subject` |  |
| [`payload/class`](#field-payload-class) | `yes` | enum: `room-live`, `sensorium-latest-state`, `sensorium-status`, `sensorium-claim`, `sensorium-control`, `sensorium-invoke`, `sensorium-receipt` |  |
| [`payload/schema`](#field-payload-schema) | `yes` | string |  |
| [`payload/digest`](#field-payload-digest) | `yes` | string |  |
| [`audience`](#field-audience) | `yes` | array | Complete bounded recipient-admission set for this member-visible delivery. Every authorized recipient and the content-visible relay can inspect every entry; deployments requiring recipient-set confidentiality must use a sealed profile that does not expose this array. |
| [`payload`](#field-payload) | `yes` | object |  |
| [`accepted-at`](#field-accepted-at) | `yes` | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "payload/class": {
      "const": "sensorium-latest-state"
    }
  }
}
```

Then:

```json
{
  "properties": {
    "audience": {
      "minItems": 1
    }
  }
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-delivery-kind"></a>
## `delivery/kind`

- Required: `yes`
- Shape: const: `member-visible`

<a id="field-room-id"></a>
## `room/id`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/room_id`

<a id="field-relay-epoch"></a>
## `relay/epoch`

- Required: `yes`
- Shape: integer

<a id="field-relay-seq-no"></a>
## `relay/seq-no`

- Required: `yes`
- Shape: integer

<a id="field-sender-subject"></a>
## `sender/subject`

- Required: `yes`
- Shape: ref: `room.v1.schema.json#/$defs/subject`

<a id="field-payload-class"></a>
## `payload/class`

- Required: `yes`
- Shape: enum: `room-live`, `sensorium-latest-state`, `sensorium-status`, `sensorium-claim`, `sensorium-control`, `sensorium-invoke`, `sensorium-receipt`

<a id="field-payload-schema"></a>
## `payload/schema`

- Required: `yes`
- Shape: string

<a id="field-payload-digest"></a>
## `payload/digest`

- Required: `yes`
- Shape: string

<a id="field-audience"></a>
## `audience`

- Required: `yes`
- Shape: array

Complete bounded recipient-admission set for this member-visible delivery. Every authorized recipient and the content-visible relay can inspect every entry; deployments requiring recipient-set confidentiality must use a sealed profile that does not expose this array.

<a id="field-payload"></a>
## `payload`

- Required: `yes`
- Shape: object

<a id="field-accepted-at"></a>
## `accepted-at`

- Required: `yes`
- Shape: string
