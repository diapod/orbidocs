# Question Envelope v1

Source schema: [`doc/schemas/question-envelope.v1.schema.json`](../../schemas/question-envelope.v1.schema.json)

Machine-readable schema for signed question publication on the procurement event layer.

## Governing Basis

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/20-memos/nym-authored-payload-verification.md`](../../project/20-memos/nym-authored-payload-verification.md)
- [`doc/project/40-proposals/003-question-envelope-and-answer-channel.md`](../../project/40-proposals/003-question-envelope-and-answer-channel.md)
- [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`](../../project/40-proposals/015-nym-certificates-and-renewal-baseline.md)
- [`doc/project/40-proposals/009-communication-exposure-modes.md`](../../project/40-proposals/009-communication-exposure-modes.md)
- [`doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`](../../project/40-proposals/011-federated-answer-procurement-lifecycle.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`question/id`](#field-question-id) | `yes` | string | Stable lifecycle identifier that links the event layer, room layer, and later procurement artifacts. |
| [`created-at`](#field-created-at) | `yes` | string | Publication timestamp of the question envelope. |
| [`sender/node-id`](#field-sender-node-id) | `yes` | string | Swarm-facing routing and hosting identity of the Node that published the envelope. |
| [`sender/participant-id`](#field-sender-participant-id) | `no` | string | Participation-role identity that authored or initiated the question publication. In the MVP baseline this may be role-distinct but key-equal to the local `node-id`. This is the authored participation identity, not the network routing identity. |
| [`sender/federation-id`](#field-sender-federation-id) | `no` | string | Federation scope of the sender when publication is federation-bound. |
| [`sender/pod-user-id`](#field-sender-pod-user-id) | `no` | string | Hosted-user identity when publication is delegated through a later pod-backed client flow. This is additive to, not a replacement for, `sender/participant-id`, and it is not part of the networking routing contract. |
| [`sender/public-nym`](#field-sender-public-nym) | `no` | string | Optional public-facing pseudonym shown at protocol boundaries where policy allows it. This is optional presentation metadata, not a routing identity. |
| [`author/nym`](#field-author-nym) | `no` | string | Visible authored pseudonym when the envelope uses a nym-authored path instead of disclosing `sender/participant-id`. |
| [`auth/nym-certificate`](#field-auth-nym-certificate) | `no` | ref: `nym-certificate.v1.schema.json` | Attached council-issued nym certificate for the pseudonymous authored path. Its `nym/id` should match `author/nym`. |
| [`auth/nym-signature`](#field-auth-nym-signature) | `no` | ref: `#/$defs/signature` | Nym signature over the envelope body when the question uses the pseudonymous authored path. |
| [`ttl-sec`](#field-ttl-sec) | `yes` | integer | Time-to-live of the open request on the event layer. |
| [`question/text`](#field-question-text) | `yes` | string | Full textual question content published at the envelope layer in the current split architecture. |
| [`question/tags`](#field-question-tags) | `yes` | array | Semantic tags used for routing and responder matching. |
| [`question/urgency`](#field-question-urgency) | `no` | enum: `low`, `normal`, `high`, `critical` | Advisory urgency classification visible to eligible responders. |
| [`delivery/scope`](#field-delivery-scope) | `yes` | enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global` | Transport-level dissemination scope derived from the chosen exposure policy. |
| [`delivery/response-channel-id`](#field-delivery-response-channel-id) | `yes` | string | Room or channel identifier bound to the same question lifecycle. |
| [`follow-ups/allowed`](#field-follow-ups-allowed) | `no` | boolean | Whether responders may expect iterative clarification or debate after initial publication. |
| [`request/exposure-mode`](#field-request-exposure-mode) | `yes` | enum: `private-to-swarm`, `federation-local`, `public-call-for-help` | User-facing exposure policy chosen before submission. |
| [`room-policy/profile`](#field-room-policy-profile) | `no` | enum: `none`, `mediated-only`, `direct-live-allowed` | Requested room policy profile for the answer room created from this envelope. |
| [`responder/min-reputation`](#field-responder-min-reputation) | `no` | number | Minimum reputation threshold for eligible responders. |
| [`models/require`](#field-models-require) | `no` | array | Required model or capability labels. |
| [`models/exclude`](#field-models-exclude) | `no` | array | Disallowed model or capability labels. |
| [`languages`](#field-languages) | `no` | array | Preferred answer languages. |
| [`reward/mode`](#field-reward-mode) | `yes` | enum: `none`, `collaborative`, `procurement` | Whether the request seeks open collaboration only or explicit responder procurement. |
| [`procurement/max-price-amount`](#field-procurement-max-price-amount) | `no` | integer | Maximum acceptable price in minor units when procurement is enabled. When `procurement/price-currency = ORC`, the value uses ORC minor units with fixed scale `2`. |
| [`procurement/price-currency`](#field-procurement-price-currency) | `no` | string | Currency or settlement unit symbol associated with procurement ceiling and offers. |
| [`procurement/max-wait-sec`](#field-procurement-max-wait-sec) | `no` | integer | Maximum wait time acceptable to the asker when procurement is enabled. |
| [`signature`](#field-signature) | `no` | ref: `#/$defs/signature` | Detached or embedded signature container for the participant-authored publication path. |
| [`policy_annotations`](#field-policy-annotations) | `no` | object | Optional federation- or implementation-local policy annotations that do not change the core lifecycle semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`signature`](#def-signature) | object |  |

## Conditional Rules

### Rule 1

Constraint:

```json
{
  "oneOf": [
    {
      "required": [
        "sender/participant-id",
        "signature"
      ],
      "not": {
        "anyOf": [
          {
            "required": [
              "author/nym"
            ]
          },
          {
            "required": [
              "auth/nym-certificate"
            ]
          },
          {
            "required": [
              "auth/nym-signature"
            ]
          }
        ]
      }
    },
    {
      "required": [
        "author/nym",
        "auth/nym-certificate",
        "auth/nym-signature"
      ],
      "not": {
        "required": [
          "sender/participant-id"
        ]
      }
    }
  ]
}
```

### Rule 2

When:

```json
{
  "properties": {
    "request/exposure-mode": {
      "const": "private-to-swarm"
    }
  },
  "required": [
    "request/exposure-mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "delivery/scope": {
      "const": "private-to-swarm"
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "request/exposure-mode": {
      "const": "federation-local"
    }
  },
  "required": [
    "request/exposure-mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "delivery/scope": {
      "const": "federation-local"
    }
  },
  "required": [
    "sender/federation-id"
  ]
}
```

### Rule 4

When:

```json
{
  "properties": {
    "request/exposure-mode": {
      "const": "public-call-for-help"
    }
  },
  "required": [
    "request/exposure-mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "delivery/scope": {
      "enum": [
        "cross-federation",
        "global"
      ]
    }
  }
}
```

### Rule 5

When:

```json
{
  "properties": {
    "reward/mode": {
      "const": "procurement"
    }
  },
  "required": [
    "reward/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "procurement/max-price-amount",
    "procurement/price-currency",
    "procurement/max-wait-sec"
  ]
}
```

## Field Semantics

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-question-id"></a>
## `question/id`

- Required: `yes`
- Shape: string

Stable lifecycle identifier that links the event layer, room layer, and later procurement artifacts.

<a id="field-created-at"></a>
## `created-at`

- Required: `yes`
- Shape: string

Publication timestamp of the question envelope.

<a id="field-sender-node-id"></a>
## `sender/node-id`

- Required: `yes`
- Shape: string

Swarm-facing routing and hosting identity of the Node that published the envelope.

<a id="field-sender-participant-id"></a>
## `sender/participant-id`

- Required: `no`
- Shape: string

Participation-role identity that authored or initiated the question publication. In the MVP baseline this may be role-distinct but key-equal to the local `node-id`. This is the authored participation identity, not the network routing identity.

<a id="field-sender-federation-id"></a>
## `sender/federation-id`

- Required: `no`
- Shape: string

Federation scope of the sender when publication is federation-bound.

<a id="field-sender-pod-user-id"></a>
## `sender/pod-user-id`

- Required: `no`
- Shape: string

Hosted-user identity when publication is delegated through a later pod-backed client flow. This is additive to, not a replacement for, `sender/participant-id`, and it is not part of the networking routing contract.

<a id="field-sender-public-nym"></a>
## `sender/public-nym`

- Required: `no`
- Shape: string

Optional public-facing pseudonym shown at protocol boundaries where policy allows it. This is optional presentation metadata, not a routing identity.

<a id="field-author-nym"></a>
## `author/nym`

- Required: `no`
- Shape: string

Visible authored pseudonym when the envelope uses a nym-authored path instead of disclosing `sender/participant-id`.

<a id="field-auth-nym-certificate"></a>
## `auth/nym-certificate`

- Required: `no`
- Shape: ref: `nym-certificate.v1.schema.json`

Attached council-issued nym certificate for the pseudonymous authored path. Its `nym/id` should match `author/nym`.

<a id="field-auth-nym-signature"></a>
## `auth/nym-signature`

- Required: `no`
- Shape: ref: `#/$defs/signature`

Nym signature over the envelope body when the question uses the pseudonymous authored path.

<a id="field-ttl-sec"></a>
## `ttl-sec`

- Required: `yes`
- Shape: integer

Time-to-live of the open request on the event layer.

<a id="field-question-text"></a>
## `question/text`

- Required: `yes`
- Shape: string

Full textual question content published at the envelope layer in the current split architecture.

<a id="field-question-tags"></a>
## `question/tags`

- Required: `yes`
- Shape: array

Semantic tags used for routing and responder matching.

<a id="field-question-urgency"></a>
## `question/urgency`

- Required: `no`
- Shape: enum: `low`, `normal`, `high`, `critical`

Advisory urgency classification visible to eligible responders.

<a id="field-delivery-scope"></a>
## `delivery/scope`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `cross-federation`, `global`

Transport-level dissemination scope derived from the chosen exposure policy.

<a id="field-delivery-response-channel-id"></a>
## `delivery/response-channel-id`

- Required: `yes`
- Shape: string

Room or channel identifier bound to the same question lifecycle.

<a id="field-follow-ups-allowed"></a>
## `follow-ups/allowed`

- Required: `no`
- Shape: boolean

Whether responders may expect iterative clarification or debate after initial publication.

<a id="field-request-exposure-mode"></a>
## `request/exposure-mode`

- Required: `yes`
- Shape: enum: `private-to-swarm`, `federation-local`, `public-call-for-help`

User-facing exposure policy chosen before submission.

<a id="field-room-policy-profile"></a>
## `room-policy/profile`

- Required: `no`
- Shape: enum: `none`, `mediated-only`, `direct-live-allowed`

Requested room policy profile for the answer room created from this envelope.

<a id="field-responder-min-reputation"></a>
## `responder/min-reputation`

- Required: `no`
- Shape: number

Minimum reputation threshold for eligible responders.

<a id="field-models-require"></a>
## `models/require`

- Required: `no`
- Shape: array

Required model or capability labels.

<a id="field-models-exclude"></a>
## `models/exclude`

- Required: `no`
- Shape: array

Disallowed model or capability labels.

<a id="field-languages"></a>
## `languages`

- Required: `no`
- Shape: array

Preferred answer languages.

<a id="field-reward-mode"></a>
## `reward/mode`

- Required: `yes`
- Shape: enum: `none`, `collaborative`, `procurement`

Whether the request seeks open collaboration only or explicit responder procurement.

<a id="field-procurement-max-price-amount"></a>
## `procurement/max-price-amount`

- Required: `no`
- Shape: integer

Maximum acceptable price in minor units when procurement is enabled. When `procurement/price-currency = ORC`, the value uses ORC minor units with fixed scale `2`.

<a id="field-procurement-price-currency"></a>
## `procurement/price-currency`

- Required: `no`
- Shape: string

Currency or settlement unit symbol associated with procurement ceiling and offers.

<a id="field-procurement-max-wait-sec"></a>
## `procurement/max-wait-sec`

- Required: `no`
- Shape: integer

Maximum wait time acceptable to the asker when procurement is enabled.

<a id="field-signature"></a>
## `signature`

- Required: `no`
- Shape: ref: `#/$defs/signature`

Detached or embedded signature container for the participant-authored publication path.

<a id="field-policy-annotations"></a>
## `policy_annotations`

- Required: `no`
- Shape: object

Optional federation- or implementation-local policy annotations that do not change the core lifecycle semantics.

## Definition Semantics

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object
