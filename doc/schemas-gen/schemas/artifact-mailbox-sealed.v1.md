# Artifact Mailbox Sealed Transport Envelope v1

Source schema: [`doc/schemas/artifact-mailbox-sealed.v1.schema.json`](../../schemas/artifact-mailbox-sealed.v1.schema.json)

Transport-only Matrix mailbox envelope for store-and-forward Artifact Delivery / INAC messages. Matrix is the carrier, not authority; receivers unseal and revalidate the embedded control frame before admission.

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `artifact-mailbox-sealed.v1` |  |
| [`source/adapter`](#field-source-adapter) | `yes` | const: `daemon.matrix-mailbox` |  |
| [`sender/node-id`](#field-sender-node-id) | `yes` | string |  |
| [`recipient/node-id`](#field-recipient-node-id) | `yes` | string |  |
| [`control/schema`](#field-control-schema) | `yes` | const: `inac-control.v1` |  |
| [`payload/security`](#field-payload-security) | `yes` | const: `sealed` |  |
| [`sealed/payload`](#field-sealed-payload) | `yes` | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `artifact-mailbox-sealed.v1`

<a id="field-source-adapter"></a>
## `source/adapter`

- Required: `yes`
- Shape: const: `daemon.matrix-mailbox`

<a id="field-sender-node-id"></a>
## `sender/node-id`

- Required: `yes`
- Shape: string

<a id="field-recipient-node-id"></a>
## `recipient/node-id`

- Required: `yes`
- Shape: string

<a id="field-control-schema"></a>
## `control/schema`

- Required: `yes`
- Shape: const: `inac-control.v1`

<a id="field-payload-security"></a>
## `payload/security`

- Required: `yes`
- Shape: const: `sealed`

<a id="field-sealed-payload"></a>
## `sealed/payload`

- Required: `yes`
- Shape: object
