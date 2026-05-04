# Moderation Marker v1

Source schema: [`doc/schemas/moderation-marker.v1.schema.json`](../../schemas/moderation-marker.v1.schema.json)

Machine-readable schema for the content body of an Agora record carrying a public moderation marker. The marker is an append-only public signal, not an imperative delete or hide command. The enclosing `agora-record.v1` envelope carries identity, authorship, topic routing, optional record/about references, and signature. Local, community, or namespace policy decides how markers affect visibility, reputation, quarantine, or appeal outcomes.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/60-solutions/008-agora/008-agora-dir-simplify-impl.md`](../../project/60-solutions/008-agora/008-agora-dir-simplify-impl.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `moderation-marker.v1` | Content-level discriminator for consumers that inspect the payload outside its Agora envelope. |
| [`marker/id`](#field-marker-id) | `yes` | string | Stable marker identifier assigned by the authoring component. It is not the Agora `record/id`; the latter remains the content address of the enclosing record. |
| [`marker/action`](#field-marker-action) | `yes` | enum: `flag`, `flag/support`, `flag/dispute`, `flag/clear`, `recommendation/hide`, `recommendation/unhide`, `reputation-signal` | Canonical moderation action. `flag/*` belongs to claim lifecycle, `recommendation/*` is projection advice, and `reputation-signal` affects trust/reputation projections. The marker remains a signal, never an imperative command. |
| [`marker/reason`](#field-marker-reason) | `yes` | enum: `content/spam`, `content/malware`, `content/sexual`, `content/non-consensual`, `content/off-topic`, `content/low-quality`, `content/malformed`, `content/misinformation`, `content/unsafe`, `content/copyright`, `content/other`, `aim/fraud`, `aim/harassment`, `aim/hate`, `aim/impersonation`, `aim/privacy-violation`, `aim/other`, `protocol/abuse`, `protocol/malformed`, `protocol/other`, `other` | Globally canonical v1 reason taxonomy. Unknown reasons are schema-invalid rather than open-world. Local policy may map these reasons to local visibility/reputation decisions. |
| [`marker/severity`](#field-marker-severity) | `no` | enum: `low`, `medium`, `high`, `critical` | Optional issuer-local severity hint. Consumers MUST NOT treat it as an automatic hide/delete decision without an explicit policy mapping. |
| [`target`](#field-target) | `yes` | ref: `#/$defs/target` |  |
| [`subject`](#field-subject) | `no` | ref: `#/$defs/identityRef` | Optional actor identity most directly associated with the target, when known. If a user publishes under a nym, moderation should target that nym unless policy explicitly allows escalation. |
| [`issuer`](#field-issuer) | `yes` | ref: `#/$defs/issuerRef` |  |
| [`policy/ref`](#field-policy-ref) | `yes` | string | Explicit moderation policy reference. The special value `default` means the default moderation policy for the Agora namespace that carries this marker. |
| [`proofs`](#field-proofs) | `yes` | object | Inline verification material. Orbiplex prefers offline-verifiable markers: attestation passports, key delegations, authority-root chains, or quorum proofs should travel with the marker whenever practical. |
| [`evidence`](#field-evidence) | `no` | array | Optional evidence references. For mutable locators such as URLs, the target is the canonical locator identity and observed content belongs here as time-bound evidence. |
| [`clears`](#field-clears) | `no` | object | Optional detail for `flag/clear`, naming the marker or reason class being cleared. |
| [`note`](#field-note) | `no` | string | Optional short public note. Renderers MUST treat it as untrusted input and escape appropriately. |
| [`created/at`](#field-created-at) | `yes` | ref: `#/$defs/rfc3339` |  |
| [`expires/at`](#field-expires-at) | `no` | unspecified | Optional marker expiry. Absence and null both mean no declared expiry; local policy may still apply retention or weighting windows. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`reason`](#def-reason) | enum: `content/spam`, `content/malware`, `content/sexual`, `content/non-consensual`, `content/off-topic`, `content/low-quality`, `content/malformed`, `content/misinformation`, `content/unsafe`, `content/copyright`, `content/other`, `aim/fraud`, `aim/harassment`, `aim/hate`, `aim/impersonation`, `aim/privacy-violation`, `aim/other`, `protocol/abuse`, `protocol/malformed`, `protocol/other`, `other` |  |
| [`rfc3339`](#def-rfc3339) | string |  |
| [`target`](#def-target) | object |  |
| [`identityRef`](#def-identityref) | object |  |
| [`issuerRef`](#def-issuerref) | object |  |
| [`proofObject`](#def-proofobject) | object |  |
| [`evidenceRef`](#def-evidenceref) | object |  |

## Conditional Rules

### Rule 1

When:

```json
{
  "properties": {
    "marker/action": {
      "const": "flag/clear"
    }
  },
  "required": [
    "marker/action"
  ]
}
```

Then:

```json
{
  "anyOf": [
    {
      "required": [
        "clears"
      ]
    },
    {
      "properties": {
        "target": {
          "properties": {
            "kind": {
              "const": "moderation-marker"
            }
          },
          "required": [
            "kind"
          ]
        }
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
    "target": {
      "properties": {
        "kind": {
          "const": "url"
        }
      },
      "required": [
        "kind"
      ]
    }
  },
  "required": [
    "target"
  ]
}
```

Then:

```json
{
  "properties": {
    "target": {
      "required": [
        "url/canonical"
      ]
    }
  }
}
```

## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `moderation-marker.v1`

Content-level discriminator for consumers that inspect the payload outside its Agora envelope.

<a id="field-marker-id"></a>
## `marker/id`

- Required: `yes`
- Shape: string

Stable marker identifier assigned by the authoring component. It is not the Agora `record/id`; the latter remains the content address of the enclosing record.

<a id="field-marker-action"></a>
## `marker/action`

- Required: `yes`
- Shape: enum: `flag`, `flag/support`, `flag/dispute`, `flag/clear`, `recommendation/hide`, `recommendation/unhide`, `reputation-signal`

Canonical moderation action. `flag/*` belongs to claim lifecycle, `recommendation/*` is projection advice, and `reputation-signal` affects trust/reputation projections. The marker remains a signal, never an imperative command.

<a id="field-marker-reason"></a>
## `marker/reason`

- Required: `yes`
- Shape: enum: `content/spam`, `content/malware`, `content/sexual`, `content/non-consensual`, `content/off-topic`, `content/low-quality`, `content/malformed`, `content/misinformation`, `content/unsafe`, `content/copyright`, `content/other`, `aim/fraud`, `aim/harassment`, `aim/hate`, `aim/impersonation`, `aim/privacy-violation`, `aim/other`, `protocol/abuse`, `protocol/malformed`, `protocol/other`, `other`

Globally canonical v1 reason taxonomy. Unknown reasons are schema-invalid rather than open-world. Local policy may map these reasons to local visibility/reputation decisions.

<a id="field-marker-severity"></a>
## `marker/severity`

- Required: `no`
- Shape: enum: `low`, `medium`, `high`, `critical`

Optional issuer-local severity hint. Consumers MUST NOT treat it as an automatic hide/delete decision without an explicit policy mapping.

<a id="field-target"></a>
## `target`

- Required: `yes`
- Shape: ref: `#/$defs/target`

<a id="field-subject"></a>
## `subject`

- Required: `no`
- Shape: ref: `#/$defs/identityRef`

Optional actor identity most directly associated with the target, when known. If a user publishes under a nym, moderation should target that nym unless policy explicitly allows escalation.

<a id="field-issuer"></a>
## `issuer`

- Required: `yes`
- Shape: ref: `#/$defs/issuerRef`

<a id="field-policy-ref"></a>
## `policy/ref`

- Required: `yes`
- Shape: string

Explicit moderation policy reference. The special value `default` means the default moderation policy for the Agora namespace that carries this marker.

<a id="field-proofs"></a>
## `proofs`

- Required: `yes`
- Shape: object

Inline verification material. Orbiplex prefers offline-verifiable markers: attestation passports, key delegations, authority-root chains, or quorum proofs should travel with the marker whenever practical.

<a id="field-evidence"></a>
## `evidence`

- Required: `no`
- Shape: array

Optional evidence references. For mutable locators such as URLs, the target is the canonical locator identity and observed content belongs here as time-bound evidence.

<a id="field-clears"></a>
## `clears`

- Required: `no`
- Shape: object

Optional detail for `flag/clear`, naming the marker or reason class being cleared.

<a id="field-note"></a>
## `note`

- Required: `no`
- Shape: string

Optional short public note. Renderers MUST treat it as untrusted input and escape appropriately.

<a id="field-created-at"></a>
## `created/at`

- Required: `yes`
- Shape: ref: `#/$defs/rfc3339`

<a id="field-expires-at"></a>
## `expires/at`

- Required: `no`
- Shape: unspecified

Optional marker expiry. Absence and null both mean no declared expiry; local policy may still apply retention or weighting windows.

## Definition Semantics

<a id="def-reason"></a>
## `$defs.reason`

- Shape: enum: `content/spam`, `content/malware`, `content/sexual`, `content/non-consensual`, `content/off-topic`, `content/low-quality`, `content/malformed`, `content/misinformation`, `content/unsafe`, `content/copyright`, `content/other`, `aim/fraud`, `aim/harassment`, `aim/hate`, `aim/impersonation`, `aim/privacy-violation`, `aim/other`, `protocol/abuse`, `protocol/malformed`, `protocol/other`, `other`

<a id="def-rfc3339"></a>
## `$defs.rfc3339`

- Shape: string

<a id="def-target"></a>
## `$defs.target`

- Shape: object

<a id="def-identityref"></a>
## `$defs.identityRef`

- Shape: object

<a id="def-issuerref"></a>
## `$defs.issuerRef`

- Shape: object

<a id="def-proofobject"></a>
## `$defs.proofObject`

- Shape: object

<a id="def-evidenceref"></a>
## `$defs.evidenceRef`

- Shape: object
