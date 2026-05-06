# Agora Authority Policy v1

Source schema: [`doc/schemas/agora-authority-policy.v1.schema.json`](../../schemas/agora-authority-policy.v1.schema.json)

Node-global policy artifact describing accountable subjects that may establish Agora namespace authority, organization custody policies, publish/subscribe namespace policies, namespace defaults, and public decision-receipt diagnostics. Components consume an effective snapshot of this policy; authority roots are not Agora-private runtime settings.

## Governing Basis

- [`doc/project/60-solutions/008-agora/008-agora.md`](../../project/60-solutions/008-agora/008-agora.md)
- [`doc/project/60-solutions/021-agora-authority/021-agora-authority.md`](../../project/60-solutions/021-agora-authority/021-agora-authority.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-008-org-subject-rollout.md`](../../project/50-requirements/requirements-008-org-subject-rollout.md)
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
| [`schema`](#field-schema) | `yes` | const: `agora-authority-policy.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`policy/id`](#field-policy-id) | `yes` | string | Stable local or federated authority policy identifier. |
| [`valid_from`](#field-valid-from) | `no` | ref: `#/$defs/rfc3339` |  |
| [`valid_until`](#field-valid-until) | `no` | unspecified |  |
| [`authority_roots`](#field-authority-roots) | `yes` | array | Configured accountable subjects that may establish namespace authority. Empty means no protected namespace has local authority unless another local policy says public-open. |
| [`org_custody_policies`](#field-org-custody-policies) | `no` | array | Inline or referenced org custody policies available to org authority roots. Inline entries use the org-custody-policy.v1 shape. |
| [`publish_policies`](#field-publish-policies) | `no` | array |  |
| [`subscribe_policies`](#field-subscribe-policies) | `no` | array |  |
| [`namespace_defaults`](#field-namespace-defaults) | `yes` | array | Default posture for topic namespaces. Protected ai.orbiplex/** namespaces should be fail-closed unless explicitly public-open. |
| [`diagnostics`](#field-diagnostics) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`rfc3339`](#def-rfc3339) | string |  |
| [`subject`](#def-subject) | object |  |
| [`topic_pattern`](#def-topic-pattern) | string | Agora topic key or topic pattern. A trailing /** means prefix match. |
| [`authority_root`](#def-authority-root) | object |  |
| [`org_custody_policy_ref`](#def-org-custody-policy-ref) | object |  |
| [`topic_policy`](#def-topic-policy) | object |  |
| [`namespace_default`](#def-namespace-default) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `agora-authority-policy.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-policy-id"></a>
## `policy/id`

- Required: `yes`
- Shape: string

Stable local or federated authority policy identifier.

<a id="field-valid-from"></a>
## `valid_from`

- Required: `no`
- Shape: ref: `#/$defs/rfc3339`

<a id="field-valid-until"></a>
## `valid_until`

- Required: `no`
- Shape: unspecified

<a id="field-authority-roots"></a>
## `authority_roots`

- Required: `yes`
- Shape: array

Configured accountable subjects that may establish namespace authority. Empty means no protected namespace has local authority unless another local policy says public-open.

<a id="field-org-custody-policies"></a>
## `org_custody_policies`

- Required: `no`
- Shape: array

Inline or referenced org custody policies available to org authority roots. Inline entries use the org-custody-policy.v1 shape.

<a id="field-publish-policies"></a>
## `publish_policies`

- Required: `no`
- Shape: array

<a id="field-subscribe-policies"></a>
## `subscribe_policies`

- Required: `no`
- Shape: array

<a id="field-namespace-defaults"></a>
## `namespace_defaults`

- Required: `yes`
- Shape: array

Default posture for topic namespaces. Protected ai.orbiplex/** namespaces should be fail-closed unless explicitly public-open.

<a id="field-diagnostics"></a>
## `diagnostics`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-rfc3339"></a>
## `$defs.rfc3339`

- Shape: string

<a id="def-subject"></a>
## `$defs.subject`

- Shape: object

<a id="def-topic-pattern"></a>
## `$defs.topic_pattern`

- Shape: string

Agora topic key or topic pattern. A trailing /** means prefix match.

<a id="def-authority-root"></a>
## `$defs.authority_root`

- Shape: object

<a id="def-org-custody-policy-ref"></a>
## `$defs.org_custody_policy_ref`

- Shape: object

<a id="def-topic-policy"></a>
## `$defs.topic_policy`

- Shape: object

<a id="def-namespace-default"></a>
## `$defs.namespace_default`

- Shape: object
