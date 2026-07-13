# Whisper Trace v1

Source schema: [`doc/schemas/whisper-trace.v1.schema.json`](../../schemas/whisper-trace.v1.schema.json)

Content-body contract for a bounded Whisper provenance statement about creating, dispatching, receiving, or holding an artifact. A trace is a signed assertion by the enclosing envelope author, not by itself proof of delivery, possession, or truth. The default disclosure is digest-only; inline bytes require an explicit consent reference and remain subject to stricter host policy and byte limits.

## Governing Basis

- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/042-inter-node-artifact-channel.md`](../../project/40-proposals/042-inter-node-artifact-channel.md)
- [`doc/project/40-proposals/081-horizontal-protocol-primitives.md`](../../project/40-proposals/081-horizontal-protocol-primitives.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `whisper-trace.v1` |  |
| [`trace/kind`](#field-trace-kind) | `yes` | enum: `artifact-created`, `artifact-dispatched`, `artifact-received`, `artifact-held` | The author's bounded assertion. `artifact-dispatched` means handed to an outbound transport, not delivered to the recipient. `artifact-received` and `artifact-held` remain claims unless strengthened by an independently verifiable evidence reference. |
| [`trace/occurred-at`](#field-trace-occurred-at) | `yes` | string | Author-asserted event time. The enclosing signed record timestamp remains the publication time. |
| [`artifact`](#field-artifact) | `yes` | ref: `#/$defs/artifact` |  |
| [`disclosure/mode`](#field-disclosure-mode) | `yes` | enum: `digest-only`, `digest-and-content` | Disclosure shape. `digest-only` minimizes transferred data but is not anonymous: a digest of predictable content may remain guessable and linkable. `digest-and-content` requires exact sender-host consent resolution and transient integrity validation. |
| [`disclosure/scope`](#field-disclosure-scope) | `yes` | enum: `private-correlation`, `federation-scoped`, `cross-federation`, `public` | Maximum disclosure surface for this trace. Public Agora deployments reject `private-correlation`; direct-only traces travel through AD/INAC. |
| [`consent/ref`](#field-consent-ref) | `no` | ref: `#/$defs/ref` | Opaque reference to the sender-side authorization or consent fact that permitted disclosure of inline content. Presence is not proof of valid consent; before publication the authoring host must resolve an active decision bound to the exact artifact digest, disclosure scope, represented subject or authority, and validity window. |
| [`causal/context`](#field-causal-context) | `no` | ref: `causal-context.v1.schema.json` | Optional canonical causal context for the operation that produced this trace. Transport request ids and local sequence numbers do not belong here. |
| [`operation/ref`](#field-operation-ref) | `no` | ref: `#/$defs/ref` |  |
| [`delivery/ref`](#field-delivery-ref) | `no` | ref: `#/$defs/ref` |  |
| [`evidence/refs`](#field-evidence-refs) | `no` | array | Optional refs to receipts, attestations, or other independently verifiable facts. Their presence may strengthen the assertion but does not change this artifact into a receipt. |
| [`context/facets`](#field-context-facets) | `no` | array |  |
| [`routing/profile`](#field-routing-profile) | `yes` | enum: `direct`, `relayed`, `onion-relayed` |  |
| [`routing/failure-mode`](#field-routing-failure-mode) | `yes` | enum: `soft-fail`, `hard-fail` |  |
| [`forwarding/max-hops`](#field-forwarding-max-hops) | `yes` | integer |  |
| [`extensions`](#field-extensions) | `no` | object | Explicit extension namespace. Extensions may add advisory metadata but must not redefine trace kind, artifact identity, consent, disclosure, or routing semantics. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifact`](#def-artifact) | object |  |
| [`ref`](#def-ref) | string |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "disclosure/mode": {
      "const": "digest-and-content"
    }
  },
  "required": [
    "disclosure/mode"
  ]
}
```

Then:

```json
{
  "required": [
    "consent/ref"
  ],
  "properties": {
    "artifact": {
      "required": [
        "bytes/base64"
      ],
      "properties": {
        "size/bytes": {
          "maximum": 32768
        }
      }
    }
  }
}
```

### Rule 2

When:

```json
{
  "properties": {
    "routing/profile": {
      "const": "direct"
    }
  },
  "required": [
    "routing/profile"
  ]
}
```

Then:

```json
{
  "properties": {
    "forwarding/max-hops": {
      "const": 0
    }
  }
}
```

### Rule 3

When:

```json
{
  "properties": {
    "routing/failure-mode": {
      "const": "hard-fail"
    }
  },
  "required": [
    "routing/failure-mode"
  ]
}
```

Then:

```json
{
  "properties": {
    "routing/profile": {
      "enum": [
        "relayed",
        "onion-relayed"
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `whisper-trace.v1`

<a id="field-trace-kind"></a>
## `trace/kind`

- Required: `yes`
- Shape: enum: `artifact-created`, `artifact-dispatched`, `artifact-received`, `artifact-held`

The author's bounded assertion. `artifact-dispatched` means handed to an outbound transport, not delivered to the recipient. `artifact-received` and `artifact-held` remain claims unless strengthened by an independently verifiable evidence reference.

<a id="field-trace-occurred-at"></a>
## `trace/occurred-at`

- Required: `yes`
- Shape: string

Author-asserted event time. The enclosing signed record timestamp remains the publication time.

<a id="field-artifact"></a>
## `artifact`

- Required: `yes`
- Shape: ref: `#/$defs/artifact`

<a id="field-disclosure-mode"></a>
## `disclosure/mode`

- Required: `yes`
- Shape: enum: `digest-only`, `digest-and-content`

Disclosure shape. `digest-only` minimizes transferred data but is not anonymous: a digest of predictable content may remain guessable and linkable. `digest-and-content` requires exact sender-host consent resolution and transient integrity validation.

<a id="field-disclosure-scope"></a>
## `disclosure/scope`

- Required: `yes`
- Shape: enum: `private-correlation`, `federation-scoped`, `cross-federation`, `public`

Maximum disclosure surface for this trace. Public Agora deployments reject `private-correlation`; direct-only traces travel through AD/INAC.

<a id="field-consent-ref"></a>
## `consent/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

Opaque reference to the sender-side authorization or consent fact that permitted disclosure of inline content. Presence is not proof of valid consent; before publication the authoring host must resolve an active decision bound to the exact artifact digest, disclosure scope, represented subject or authority, and validity window.

<a id="field-causal-context"></a>
## `causal/context`

- Required: `no`
- Shape: ref: `causal-context.v1.schema.json`

Optional canonical causal context for the operation that produced this trace. Transport request ids and local sequence numbers do not belong here.

<a id="field-operation-ref"></a>
## `operation/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-delivery-ref"></a>
## `delivery/ref`

- Required: `no`
- Shape: ref: `#/$defs/ref`

<a id="field-evidence-refs"></a>
## `evidence/refs`

- Required: `no`
- Shape: array

Optional refs to receipts, attestations, or other independently verifiable facts. Their presence may strengthen the assertion but does not change this artifact into a receipt.

<a id="field-context-facets"></a>
## `context/facets`

- Required: `no`
- Shape: array

<a id="field-routing-profile"></a>
## `routing/profile`

- Required: `yes`
- Shape: enum: `direct`, `relayed`, `onion-relayed`

<a id="field-routing-failure-mode"></a>
## `routing/failure-mode`

- Required: `yes`
- Shape: enum: `soft-fail`, `hard-fail`

<a id="field-forwarding-max-hops"></a>
## `forwarding/max-hops`

- Required: `yes`
- Shape: integer

<a id="field-extensions"></a>
## `extensions`

- Required: `no`
- Shape: object

Explicit extension namespace. Extensions may add advisory metadata but must not redefine trace kind, artifact identity, consent, disclosure, or routing semantics.

## Definition Semantics

<a id="def-artifact"></a>
## `$defs.artifact`

- Shape: object

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string
