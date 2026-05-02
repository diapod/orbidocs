# Comment Thread Policy v1

Source schema: [`doc/schemas/comment-thread-policy.v1.schema.json`](../../schemas/comment-thread-policy.v1.schema.json)

Content schema for an Agora thread participation policy record. Used with `record/kind = thread-policy` and `content/schema = comment-thread-policy.v1`. The policy is intentionally separate from `plain-comment.v1`: comments carry speech, while this payload carries the access rule for joining a comment thread or subtree.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/60-solutions/045-agora-authority.md`](../../project/60-solutions/045-agora-authority.md)

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
| [`schema`](#field-schema) | `yes` | const: `comment-thread-policy.v1` | Content-level discriminator for consumers that inspect the payload outside its Agora envelope. |
| [`policy/thread-topic-key`](#field-policy-thread-topic-key) | `no` | string | Optional topic key of the comment thread this policy governs. When present, domain validators SHOULD require it to equal the enclosing Agora record's `topic/key`. |
| [`policy/root-record-id`](#field-policy-root-record-id) | `no` | string | Optional root comment record id. This may be absent when the policy record is published before the root comment so the root can reference the policy without a circular dependency. |
| [`policy/min-attestation`](#field-policy-min-attestation) | `yes` | string | Minimum author attestation required to publish a comment governed by this policy. Early expected values include `unknown`, `phone-confirmed`, `national-id`, `community-trusted`, and `sovereign-operator`. The ordering and equivalence rules are domain policy, not JSON Schema. |
| [`policy/inheritance`](#field-policy-inheritance) | `yes` | enum: `descendants` | Inheritance mode. `descendants` means the policy applies to replies below the record or topic it is attached to. |
| [`policy/may-tighten`](#field-policy-may-tighten) | `yes` | const: `True` | Whether descendant comments may attach a stricter policy for their own subtree. v1 requires `true` so moderation can narrow participation without mutating ancestors. |
| [`policy/may-loosen`](#field-policy-may-loosen) | `yes` | const: `False` | Whether descendant comments may weaken an inherited policy. v1 requires `false`; a child subtree may tighten inherited requirements but MUST NOT loosen them. |
| [`policy/rate-budget`](#field-policy-rate-budget) | `no` | object | Optional participation rate budget hint. Enforcement is domain-specific and may depend on author, topic, reputation, or relay-local anti-abuse policy. |
| [`policy/description`](#field-policy-description) | `no` | string | Optional human-readable explanation shown to participants before they join the thread. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `comment-thread-policy.v1`

Content-level discriminator for consumers that inspect the payload outside its Agora envelope.

<a id="field-policy-thread-topic-key"></a>
## `policy/thread-topic-key`

- Required: `no`
- Shape: string

Optional topic key of the comment thread this policy governs. When present, domain validators SHOULD require it to equal the enclosing Agora record's `topic/key`.

<a id="field-policy-root-record-id"></a>
## `policy/root-record-id`

- Required: `no`
- Shape: string

Optional root comment record id. This may be absent when the policy record is published before the root comment so the root can reference the policy without a circular dependency.

<a id="field-policy-min-attestation"></a>
## `policy/min-attestation`

- Required: `yes`
- Shape: string

Minimum author attestation required to publish a comment governed by this policy. Early expected values include `unknown`, `phone-confirmed`, `national-id`, `community-trusted`, and `sovereign-operator`. The ordering and equivalence rules are domain policy, not JSON Schema.

<a id="field-policy-inheritance"></a>
## `policy/inheritance`

- Required: `yes`
- Shape: enum: `descendants`

Inheritance mode. `descendants` means the policy applies to replies below the record or topic it is attached to.

<a id="field-policy-may-tighten"></a>
## `policy/may-tighten`

- Required: `yes`
- Shape: const: `True`

Whether descendant comments may attach a stricter policy for their own subtree. v1 requires `true` so moderation can narrow participation without mutating ancestors.

<a id="field-policy-may-loosen"></a>
## `policy/may-loosen`

- Required: `yes`
- Shape: const: `False`

Whether descendant comments may weaken an inherited policy. v1 requires `false`; a child subtree may tighten inherited requirements but MUST NOT loosen them.

<a id="field-policy-rate-budget"></a>
## `policy/rate-budget`

- Required: `no`
- Shape: object

Optional participation rate budget hint. Enforcement is domain-specific and may depend on author, topic, reputation, or relay-local anti-abuse policy.

<a id="field-policy-description"></a>
## `policy/description`

- Required: `no`
- Shape: string

Optional human-readable explanation shown to participants before they join the thread.
