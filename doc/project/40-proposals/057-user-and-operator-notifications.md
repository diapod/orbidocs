# Proposal 057: User and Operator Notifications

Date: `2026-05-15`
Status: Draft

Based on:

- `doc/project/20-memos/operator-participation-in-answer-channel.md`
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/20-memos/node-ui-htmx-hateoas-architecture.md`
- `doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/052-tauri-hosted-node-ui.md`
- `doc/project/40-proposals/056-orbiplex-tls-trust-policy.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

## Executive Summary

Orbiplex already names several situations where a node should draw human
attention: relevant whispers, answer-channel debates, readiness blockers,
completed long-running work, and desktop OS notifications. These references
should converge on one small semantic model.

This proposal defines **notifications** as UI-owned attention requests derived
from node facts, middleware requests, and local policy. A notification is not the
same as an event stream, an inbox view, or an operating-system popup. Those are
delivery and presentation layers. The notification contract answers a narrower
question:

> what should this node ask a user or operator to notice, why, how urgently, and
> under which local attention policy?

## Context and Problem Statement

Existing documents use notification language in multiple places, but each use
is local:

- Whisper can notify the user or operator that a relevant rumor exists.
- Answer-channel participation can ask the operator for live judgment.
- Node UI can poll or subscribe to daemon events.
- A future Tauri shell can surface native OS notifications.
- Exposure mode can influence notification fan-out.

Without a shared contract, these mechanisms risk becoming coupled to their first
UI surface. The daemon might emit raw events and expect every client to
interpret them. The desktop shell might implement notification policy itself.
Middleware might start treating OS notifications as capability authority or
injecting arbitrary UI fragments into the operator interface.

The system needs a thin boundary:

```text
facts/events -> notification decision -> inbox projection -> presentation surface
```

The persistent queue belongs to the UI stratum: operator UI and future user UI
need stable notification state across process restarts and browser sessions. The
daemon may host the storage and host capability, but notification semantics are
for human-facing attention management, not for core protocol authority.

## Proposed Model

### Notification

A notification is a semantic attention request stored in a durable local queue.
It should be represented as a small record with at least:

- `notification/id`
- `idempotency/key`
- `notification/kind`
- `correlation/id`
- `collapse/key`
- optional `supersedes`
- `version`
- `sender/id`
- `recipient/id`
- `recipient/class` (`operator`, `user`, `pod-user`, `role`)
- `subject/ref`
- `priority` (`1`, `2`, `3`; corresponding to low, medium, high)
- `reason/code`
- `delivered/at`
- optional `expires/at`
- `read/opened`
- `handled`
- `source/component`
- `policy/ref`
- `title`
- `body/text`
- optional `body/ref`
- optional schema-defined `actions`

`correlation/id` groups notifications derived from the same domain fact or
long-running condition. A repeated readiness blocker, recurring trust lifecycle
failure, or retried middleware warning should keep the same correlation id.

`collapse/key` is the producer-provided deduplication key. A newer notification
with the same collapse key replaces or updates the active attention item instead
of creating a new one. `supersedes` optionally points to the previous
notification id for audit and diagnostics. `version` is the optimistic
concurrency token for mutable flags such as `read/opened`, `handled`, and
`snoozed/until`.

`read/opened` means the recipient has opened or read the notification.
`handled` means the notification no longer needs attention and may be hidden
from the primary attention view. Handled notifications should remain available
in history while retention policy keeps them.

`idempotency/key` belongs to the producer request boundary. It makes
`notification.create` safe under retries and is scoped by `sender/id`.
The natural key is `(sender/id, idempotency/key)`. Replaying the same request
with the same idempotency key must return the original notification id or a
stable equivalent outcome.

`body/ref` points to the source subsystem record or diagnostic view that owns the
domain payload. A notification should not persist arbitrary structured body
payloads in the queue. Structured request payloads may be accepted by
`notification.create` as `body/input`, but that field is transport-only: the
service uses it for validation, redaction, policy evaluation, title/body
rendering, digest calculation, and action construction, then discards the full
input. The durable queue stores only the attention projection: title, body text,
body reference, subject/reference, actions, and optional digest or redacted
summary owned by the notification service. The domain payload remains in its
domain store.

`body/input` must also stay out of ordinary diagnostics. Types carrying
transient input should avoid `Debug`; logs and audit facts should use redacted
or digest-only projections. `zeroize` may be used as best-effort hygiene for
buffers owned by the implementation, but the MVP does not claim heap-wide
erasure for `serde_json` internals or require heap-snapshot style tests.

The initial kind vocabulary should remain non-exhaustive but reserve common
production identifiers:

- `readiness-blocker`
- `long-running-task-completed`
- `whisper-relevant`
- `answer-room-human-input-requested`
- `policy-decision-required`
- `trust-remediation-required`
- `middleware-attention-requested`
- `delivery-failed`
- `inbound-admission-rejected`
- `peer-trust-changed`
- `capability-passport-expiring`
- `capability-passport-expired`
- `quota-exceeded`

Unknown kinds should be accepted only when permitted by local policy and should
be represented as extension kinds rather than rejected at the parser boundary.

### Durable Queue

Notifications must survive node restarts and browser sessions. The MVP storage
shape can be a local database table owned by the node UI / daemon integration
layer:

```text
notification_queue
  schema                # notification.v1; read path rejects unknown schema
  notification_id       # stable unique id
  idempotency_key       # nullable only for internally derived notifications
  correlation_id        # groups notifications from one domain fact
  collapse_key          # producer-provided active-item dedup key
  supersedes            # nullable previous notification_id
  version               # positive optimistic concurrency token
  sender_id             # component, node, operator, or system identity
  recipient_id          # operator/user/pod-user/role id
  recipient_class       # operator | user | pod-user | role
  notification_kind
  priority              # 1 low, 2 medium, 3 high
  reason_code           # nullable stable reason vocabulary
  delivered_at
  expires_at            # nullable
  snoozed_until         # nullable
  read_opened           # bool
  handled               # bool
  title
  body_text             # nullable
  body_ref              # nullable source subsystem reference
  body_digest           # nullable digest of the input payload or source view
  actions_json          # nullable schema-defined action list
  source_component
  policy_ref            # nullable
```

The queue is not an append-only public protocol log. It is a local UX state
store. Queue mutations such as `read/opened`, `handled`, `snoozed`, and
`retracted` should be mirrored into the local append-only notification audit.

MVP storage should still separate mutable UX state from append-only operational
facts:

- Mutable queue: SQLite under `<data-dir>/storage/notifications.sqlite`, using
  the same operational posture as other node-local ledgers where practical
  (`WAL`, `busy_timeout`, explicit `user_version` migrations).
- Append-only audit: `storage-jsonl::FileLedger` under
  `<data-dir>/storage/notification-audit/`, recording delivered, suppressed,
  opened, handled, snoozed, retracted, and action-submitted facts.

This split keeps the inbox cheap to query while preserving a defensible history
for "suppression is not deletion" and leak diagnostics.

The audit JSONL is the recovery source of truth. If the SQLite queue is lost
or corrupted, the inbox state is rebuildable by idempotent replay of audit
facts in order (delivered, opened, handled, snoozed, snooze-cleared,
retracted, superseded) reconciled against the idempotency table. Replay
must be pure: no SSE pings, no retract broadcasts, no producer-visible side
effects.

### Host Capability

Components may create notifications through a host capability, for example:

```text
notification.create
```

This is the recommended entry point for middleware and other components outside
the notification subsystem. It is intentionally not a Node UI endpoint: the
component asks for local attention, but it does not address a concrete UI
surface.

The host capability boundary must enforce:

- authenticated component identity,
- `sender/ref` absence or equality with the authenticated component identity,
- idempotency key semantics,
- allowed notification kind,
- allowed recipient class and recipient id,
- maximum title/body/action sizes,
- rejection or redaction of structured request payloads before persistence,
- allowed priority range,
- action schema validation,
- redaction policy for high-sensitivity payloads,
- rate limits per component and notification kind,
- rate limits per sender and notification kind, including host-owned internal
  producers that bypass `NotificationAllow` but not runtime throttling.

Components request attention; they do not decide whether a user is interrupted.
The local notification policy can still suppress, downgrade, expire, or convert
the notification to inbox-only.

### Notification Allow Policy

The authorization contract for `notification.create` should be data, not
hard-coded request-time intuition. It mirrors the `OutboundAllow` pattern used by
Artifact Delivery: an operator or package manifest declares what a component may
ask the node to surface.

Recommended shape:

```text
NotificationAllow
  component/id
  notification/kinds[]          # literal allowlist in MVP
  action/refs[]                 # optional host-owned registered action refs
  recipient/classes[]           # operator | user | pod-user | role
  recipient/ids[]               # optional narrower allowlist
  max/priority                  # component-specific cap
  rate/per-minute
  redaction/policy/ref
```

Effective notification allow policy should be validated at configuration and
readiness-gate time, not discovered only when the first notification arrives. A
middleware package that wants to create `priority = 3` operator notifications
must have that authority explicitly granted. Request-time validation then checks
the already materialized effective policy.

External middleware may request inline buttons such as `Approve` and `Cancel`
without forcing the operator to navigate to another page, but only when those
buttons target pre-registered notification action refs approved by the host or
operator during package installation/effective config materialization. Without
such registration, the safe fallback is a `link` action to a local UI route
owned by the middleware package.

### Internal Notification Service

`notification.create` should not be the only producer path. Internal daemon
subsystems such as readiness gate, workflow runtime, trust lifecycle, Artifact
Delivery recovery, or peer supervisor may create notifications through an
in-process service:

```text
NotificationService / NotificationSink
```

This internal service should use the same payload shape, validator, policy
evaluator, and durable queue as the host capability. The difference is transport
and call boundary, not semantics.

Recommended shape:

```text
component or middleware
  -> notification.create host capability
  -> NotificationService
  -> validation + local attention policy
  -> durable notification queue
  -> inbox / SSE indicator / optional OS notification

daemon subsystem
  -> NotificationService
  -> validation + local attention policy
  -> durable notification queue
  -> inbox / SSE indicator / optional OS notification
```

The SSE indicator is emitted by the daemon-side `NotificationService` after the
durable queue transaction and append-only audit write succeed. It should not be
implemented as a separate notification daemon and should not rely on periodic
database polling. The daemon already owns caller binding, host capability
authorization, policy evaluation, queue writes, audit writes, and the local
control/event stream; notification wake-up events belong at that boundary.

This keeps the boundary stratified:

- middleware receives an explicit capability rather than ambient UI access,
- daemon subsystems avoid unnecessary HTTP self-calls,
- all producers share one validator and one policy path,
- Node UI remains a projection and action surface, not the authority that
  decides whether a component may request attention,
- Node UI does not need direct access to the notification database.

The UI should never accept arbitrary component-authored notifications directly.
Doing so would couple components to a specific UI backend and would bypass the
host-owned attention policy.

Every external or out-of-process call inside `NotificationService` should
carry an explicit deadline and a typed retryable/terminal failure
classification, consistent with the project-wide "external calls have
budgets" rule. This applies to operator binding lookup, SQLite queue
transactions, JSONL audit appends, SSE publish, and background sweepers
(snooze expiry, retention cleanup). Audit append failure must block the
queue commit; SSE publish failure must not.

### Recipient Isolation

`recipient/class = "pod-user"` implies multiple human recipients on the same
node. The notification read path must filter by the recipient identity derived
from the caller binding. An operator inbox must not accidentally become a global
view of pod-user notifications, and one pod-user must not read another pod-user's
queue.

Minimum MVP rules:

- Operator UI reads operator-recipient queues through the operator binding store.
- User or pod-user UI reads only notifications where `recipient/id` matches the
  authenticated local identity.
- If no matching local caller binding exists, user and pod-user notification
  routes fail closed instead of treating the route parameter as authority.
- Every read/open/handled/action-submit audit fact records the actor identity.
- Store v3 keeps routing metadata queryable in plaintext, but seals title,
  body, body refs, actions, and body digests per recipient before persistence.
  The node-local store uses `XChaCha20Poly1305` with a daemon-owned local seal
  key and per-recipient content keys derived with HKDF over recipient class and
  recipient id. The AEAD associated data binds notification id, recipient id,
  recipient class, and notification version; reads also reject sealed payloads
  whose decrypted `body_digest` no longer matches the plaintext routing
  metadata. The daemon-local seal key is an MVP filesystem-local root: if it is
  compromised together with the queue DB, all sealed local notification payloads
  on that node are compromised. The store does not receive participant root
  secrets. Missing local seal material fails closed for user and pod-user
  reads/actions.

### Schema-Defined Actions

Notification actions should be data, not arbitrary HTML or HTMX fragments.
Arbitrary UI fragments would let a component break layout, bypass accessibility
rules, or smuggle behavior into the UI layer. The notification renderer should
own all HTML.

An action is a HATEOAS-like affordance: it tells the UI which transition is
currently available to a human. It is not the transition implementation.

```text
notification
  -> schema-defined action affordances
  -> UI renders widgets
  -> submit goes to a host-owned action endpoint
  -> backend validates authority and freshness
  -> domain effect happens
  -> optional notification handled state update
```

The initial action vocabulary can include:

- `link` — open a local UI path or route.
- `button` — submit a predefined command or navigate to a local action path.
- `text-input` — collect a bounded text value.
- `single-choice` — choose one option from a fixed list.
- `multi-choice` — choose zero or more options from a fixed list.
- `confirm` — require an explicit confirmation before a host-owned action.

Each action should define:

- `action/id`
- `label`
- `kind`
- optional `description`
- optional `action/expires-at`
- `method`
- target local UI path or host-owned registered notification action reference
- input constraints for text or choice actions, expressed as JSON Schema where
  the input carries structured data
- whether handling the action marks the notification as handled

The UI may render these as buttons, forms, or widgets, but the sender only
provides the schema-defined action data.

An inline `Approve` / `Cancel` UX is allowed for external middleware if the
referenced actions were registered before the notification is created. The
notification payload does not define the effect of `Approve`; it only references
a host-owned registered action. The host registry binds that ref to the allowed
producer, notification kind, reason code, recipient class, input schema, and
domain-state validation. This keeps the interaction fast for the operator
without turning notifications into an arbitrary capability invocation channel.

The backend must re-check every action submit. It must not trust that an action
is valid merely because it was present in the stored notification. Checks should
include:

- recipient identity and authorization,
- notification expiry,
- action id membership in the current notification,
- action-specific expiry,
- current domain state,
- input schema validation,
- CSRF token validation for browser form submissions,
- replay/idempotency protection.

If the underlying domain state has changed, the action should fail cleanly with
`action-no-longer-available` rather than trying to replay stale intent.

Action execution should produce an `action/result` record or equivalent local
fact:

- `action/id`
- `notification/id`
- `submitted/at`
- `actor/id`
- `status` (`succeeded`, `denied`, `expired`, `validation-error`, `failed`)
- optional `reason/code`
- optional redacted `result/json`

This keeps diagnostics visible without turning notifications into a hidden
workflow engine.

`action/expires-at` is intentionally separate from notification expiry. A
notification about a trust-root candidate may remain useful for 24 hours, while
an `install-now` action may expire after 5 minutes and require a refreshed
evaluation. Form submissions should carry an `action/submission-id` with a short
TTL to prevent replay across browser tabs.

### Event Stream

The event stream is a transport for local observation. It may carry notification
state changes, but it is not the source of notification semantics.

`/v1/events` can remain a local SSE stream owned by the daemon. Its job is to
wake projections and user interfaces. It should not be the only durable place
where an attention request exists.

Notification SSE should be a thin ping. After `NotificationService` commits a
notification or a notification state transition, it publishes an event such as
`notification-state-changed`. The payload should be just enough for Node UI or a
browser client to know that it should refresh the relevant read model. It should
not carry the full notification body, action list, source payload, or domain
diagnostics.

Recommended flow:

```text
NotificationService.create(...)
  -> SQLite queue transaction
  -> JSONL audit append
  -> commit OK
  -> daemon SSE publish: notification-state-changed
  -> Node UI / browser receives ping
  -> HTMX refreshes /operator/notifications fragment or detail endpoint
```

If Node UI exposes a browser-facing SSE route, it should proxy or translate the
daemon event rather than reading the notification database directly. The
daemon's read API remains the source of inbox projections.

### Inbox

An inbox is a read model over the durable notification queue. It answers:

- what currently needs attention,
- what is snoozed or muted,
- what was acknowledged,
- which actions are available now.

The inbox should exist in both operator UI and future user UI. The operator UI
path can start as:

```text
/operator/notifications
```

The list view should show title, sender, recipient, priority, delivery time,
expiry, read/opened state, and handled state. The detail view should show full
body text, `body/ref`, optional redacted diagnostic summary, and schema-defined
actions rendered by the UI.

The inbox may be projected by Node UI, a pod thin client, or a desktop shell,
but the durable notification state belongs to the local node.

### OS Notification

An OS notification is only a presentation effect. It should be produced after
local policy decides that a notification is eligible for interruption.

OS notifications must not carry secrets, raw private payloads, or unredacted
rumor content. They should carry a short summary and a local deep link into the
Node UI or desktop shell.

## Operator UI Integration

The operator UI should expose notifications in two layers:

1. A full notification view at `/operator/notifications`.
2. A compact top-bar indicator showing unread or unhandled attention state.

The top-bar indicator can use the existing local SSE infrastructure. A template
that wants live notification state should explicitly enable the HTMX SSE
extension and subscribe to a daemon/UI endpoint that emits notification count or
state changes. The SSE event should only say that notification state changed; it
should not carry full sensitive notification bodies.

Concrete payload shape:

```json
{
  "schema": "notification-state-changed.v1",
  "recipient/id": "operator:bind:abc",
  "unread/count": 3,
  "max/unread-priority": 2,
  "last/changed-at": "2026-05-15T12:00:00Z"
}
```

The payload must not include notification title, body, kind, subject, or action
details. The UI can fetch the inbox read model after receiving the wake-up event.

Useful top-bar states:

- no unread/unhandled notifications,
- unread low/medium notifications,
- unread high-priority notification,
- expired-but-unhandled notification,
- notification delivery degraded.

The detail page should render actions from the notification action schema. If a
component needs richer UI than the schema can express, it should register its own
operator UI route and link to it through a `link` action rather than embedding
HTML in the notification.

## Attention Policy

Notification policy is local and operator/user controlled. It should include:

- quiet hours,
- timezone for quiet-hours evaluation, operator-configurable with UTC fallback,
- per-kind enablement,
- urgency thresholds,
- priority override rules,
- local operator presence,
- topic filters,
- trust thresholds,
- exposure-mode-derived fan-out profiles,
- rate limits,
- delivery surfaces (`inbox`, `local-ui`, `desktop-os`, future mobile/pod push),
- redaction level for presentation.

The policy decision should be explicit:

```text
candidate notification + local attention policy -> suppress | inbox-only | interrupt | defer
```

Suppression is not deletion. A suppressed notification may still be visible in
diagnostics or history depending on retention policy.

The evaluator should be pure and testable, mirroring the `service-ca-trust`
pattern:

```rust
pub fn evaluate(
    notification: &Notification,
    policy: &NotificationDeliveryPolicy,
    operator_presence: OperatorPresence,
    now: OffsetDateTime,
) -> DeliveryDecision
```

Where:

```text
DeliveryDecision =
  Interrupt
  InboxOnly
  Suppress { reason }
  Defer { until }
```

`priority = 3` should be able to override quiet hours when the local policy
marks the kind as safety-critical. Local operator presence, for example an
active operator UI session, is a valid input to local policy. Remote presence is
not a notification signal and must stay a separate explicit artifact if it ever
exists.

Every policy decision should emit or append an audit fact explaining the
decision, including suppression and defer decisions. Otherwise "why did the UI
not interrupt me?" becomes a log archaeology problem.

### Trust Remediation Mapping

`trust-remediation-required` must be actionable. Trust lifecycle producers
should map stable trust states into notification `reason/code` values, for
example:

| Trust lifecycle condition | Notification reason code | Expected UI affordance |
|---|---|---|
| `candidate-rejected` | `trust/candidate-rejected` | Link to candidate evaluation details. |
| `fingerprint-mismatch` | `trust/fingerprint-mismatch` | Link to endpoint evidence and observed certificate. |
| `accepted-not-installed` | `trust/accepted-not-installed` | Action to install scoped root after re-evaluation. |
| `rotation-overlap-missing` | `trust/rotation-overlap-missing` | Link to rotation guidance. |
| `revoked-root-observed` | `trust/revoked-root-observed` | Action to disable scoped installation. |
| `endpoint-evidence-stale` | `trust/endpoint-evidence-stale` | Action to retry probe or mark endpoint suspect. |

The mapping keeps notifications in the operator's action language while the
trust subsystem remains the authority for evidence, evaluation, and install
state.

## Stratification

The layers should remain separate:

| Layer | Responsibility |
|---|---|
| Protocol/domain facts | Describe what happened. |
| Notification host capability | Accept bounded attention requests from components. |
| Internal notification service | Accept in-process attention requests from daemon subsystems using the same contract. |
| Notification decision | Decide whether the fact deserves attention. |
| Durable queue | Preserve notification state across sessions and restarts. |
| Notification audit | Preserve append-only delivered/opened/handled/suppressed/action facts. |
| Inbox projection | Present current attention state and available actions. |
| Transport/event stream | Wake clients and projections. |
| OS/native shell | Show optional local interruption affordances. |

This prevents a UI feature from becoming an authority boundary.

The UI does not hold a copy of `NotificationDeliveryPolicy`. It consumes a
pre-projected read model (unread count, max unread priority, available
actions) and renders affordances; it does not decide whether a notification
is snoozed, suppressed, or eligible for interrupt. All delivery decisions
remain in the daemon-side `NotificationService`.

## Example Scenarios

### Relevant Whisper

1. A node receives or derives a `whisper-signal`.
2. Local relevance policy marks it as relevant to the operator.
3. The notification layer creates `notification/kind = "whisper-relevant"`.
4. Quiet-hours policy decides whether this is inbox-only or interrupting.
5. The user sees a redacted inbox item with actions such as `review`,
   `ignore`, `mark-spam`, or `express-interest`.

### Answer-Channel Human Input

1. A node participates in an active answer-room debate.
2. The debate crosses urgency and trust thresholds.
3. The node creates `answer-room-human-input-requested`.
4. The operator can choose mediated consultation or direct human-origin
   participation.

### Readiness Blocker

1. The readiness gate records a pending operator action.
2. The notification layer derives `readiness-blocker`.
3. `correlation/id` identifies the blocker condition and `collapse/key`
   replaces repeated reminders.
4. Node UI shows it in the operator inbox.
5. A desktop shell may additionally display an OS notification if policy allows.

## Failure Modes and Mitigations

1. **Notification spam**
   - Mitigation: per-kind rate limits, deduplication, collapse keys, and quiet
     hours.

2. **Leaking sensitive content into OS notifications**
   - Mitigation: redacted summaries by default; deep link into local UI for
     details.

3. **Event stream treated as durable notification storage**
   - Mitigation: model notifications as node facts or durable projections; use
     SSE only as wake-up transport.

4. **Middleware bypasses local attention policy**
   - Mitigation: middleware can request attention, but host-owned notification
     policy decides delivery.

5. **UI endpoint becomes a hidden component integration API**
   - Mitigation: components use `notification.create`; UI endpoints read and
     mutate notification state for humans only.

6. **Remote participants infer local human availability**
   - Mitigation: notifications are local by default; any remote presence signal
     must be a separate explicit artifact.

7. **Component-provided UI breaks the operator interface**
   - Mitigation: notification actions are schema-defined data; UI-owned
     renderers produce HTML.

8. **Notifications vanish between sessions**
   - Mitigation: notification state is persisted in the durable local queue
     before delivery surfaces are updated.

9. **Duplicate notifications after producer retries**
   - Mitigation: require `idempotency/key` on `notification.create` and return a
     stable result for repeated requests.

10. **Cross-recipient leak in a multi-user node**
    - Mitigation: filter read paths by recipient binding and audit every
      read/open/action-submit transition.

11. **Attention policy scattered across UI handlers**
    - Mitigation: express policy as data and evaluate it through a pure
      `NotificationDeliveryPolicy` evaluator.

12. **Trust remediation notification lacks an action path**
    - Mitigation: map trust lifecycle reason codes to stable UI affordances and
      host-owned actions.

## MVP Decisions

1. `notification.v1` is schema-backed from the beginning. The host capability,
   durable queue, UI read model, and tests use one contract.
2. `NotificationAllow` lives in effective host configuration. Middleware package
   manifests may request notification permissions, but the host materializes and
   approves the final policy.
3. Idempotency uses the natural key `(sender/id, idempotency/key)`. Storage names
   this owner `sender_id`; `component/id` remains configuration vocabulary for
   middleware allow rules, not the idempotency owner.
   `sender/ref` on `notification.create` is compatibility/advisory input:
   the daemon canonicalizes it to the authenticated component identity and
   rejects mismatches.
4. `body/input` is transport-only. Durable notification state stores `body/ref`,
   optional user-facing text, and digests or redacted projections, not persistent
   raw body payloads. `body/input` still participates in the idempotency
   `request_digest`, so a retry with the same `(sender/id, idempotency/key)` and
   different transient input is a conflict rather than a silent overwrite.
5. `snoozed/until` is part of the MVP model and storage. `null` means no snooze;
   a timestamp removes the notification from unread and top-bar attention counts
   until the value expires or is cleared.
6. External middleware actions may target local UI paths or host-owned registered
   notification action refs approved in effective configuration. They may not
   invoke arbitrary host capabilities by embedding a capability reference in the
   notification.
7. Daemon-owned SSE is a thin notification ping after queue/audit commit. The
   current daemon SSE bus emits event `id:` values but does not provide
   `Last-Event-ID` replay or a per-recipient sequence buffer, so MVP reconnect
   recovery is a current state snapshot plus read-model refresh.
8. `notification.create` returns success when attention policy suppresses a
   notification. The request was valid; delivery was intentionally reduced by
   host policy.
9. Sender retract is allowed only for the same sender and matching
   `correlation/id` or `collapse/key`, with append-only audit.
10. Mutable flags use optimistic concurrency through `version`, with idempotent
    handling for safe repeated UI actions.
11. Operator timezone is explicit configuration with UTC fallback.
12. OS notifications and cross-node notification aggregation are post-MVP and do
    not add fields to `notification.v1`.
13. Host-owned action refs may be implemented incrementally. The first concrete
    daemon-owned refs are `inac.invitation.accept`,
    `inac.invitation.reject`, `contact-request.accept`,
    `contact-request.reject`, and `mailbox.open`; they are local actions that
    call narrowly wired host/domain handlers. They do not make notifications a
    generic capability invocation channel.

## Post-MVP Questions

1. Should daemon SSE grow a shared `Last-Event-ID` replay buffer and
   per-recipient sequence numbers for all SSE consumers?
2. Should `NotificationAllow` later support namespaced extension prefixes such
   as `vendor.example/*`, or should it remain literal-only?
3. When pod-user authentication/session binding becomes first-class, should pod
   users receive independent attention policies or inherit operator defaults
   with per-recipient overrides?
4. Should OS notification adapters be added for desktop shells, and which
   redaction profile should they use?
5. Should cross-node notification aggregation be modelled as a separate artifact
   family rather than extending local `notification.v1`?

## Tests Required

The first implementation should include tests for:

- `notification.create` idempotency with the same `idempotency/key`.
- `NotificationAllow` denying disallowed kind, recipient class, recipient id,
  excessive priority, and rate-limit violations.
- Policy evaluator coverage for each `DeliveryDecision` variant.
- Quiet-hours timezone behavior and priority override.
- Action submit after another tab set `handled = true`, returning
  `action-no-longer-available`.
- `action/expires-at` rejecting a stale action while leaving the notification
  readable.
- CSRF and `action/submission-id` replay protection for browser form submits.
- SSE indicator payload not containing title, body, kind, subject, or action
  details.
- Cross-recipient isolation: operator A cannot read operator B's or pod-user's
  queue.
- Collapse key behavior: the second active notification with the same key
  supersedes or updates the first.
- Snooze and restore round-trip.
- OS notification redaction: no secrets or raw private payloads in short
  summaries.
- Trust remediation mapping from service-ca-trust or endpoint evidence reason
  code to notification reason code and UI affordance.

## Next Actions

1. Define the minimal `notification.create` host capability payload and
   `notification.v1` queue record shape, including idempotency, correlation,
   collapse, supersedes, and version fields.
2. Implement `NotificationService` as the in-process service used by both the
   host capability and daemon subsystems.
3. Define `NotificationAllow` and wire it into effective config/readiness-gate
   validation.
4. Implement `NotificationDeliveryPolicy` as data plus a pure evaluator with an
   audit trail.
5. Implement durable SQLite queue plus append-only JSONL notification audit.
6. Add `/operator/notifications` list and detail views.
7. Add SSE-backed top-bar unread/unhandled indicator with the
   `notification-state-changed.v1` privacy contract.
8. Map existing readiness, workflow, trust lifecycle, Artifact Delivery,
   whisper, and answer-room attention paths to notification kinds and reason
   codes.
9. Keep OS notifications as a desktop-shell adapter, not as the semantic source
   of truth.

## Tracking

| ID | Feature | Status | Evidence |
|---|---|---|---|
| P057-001 | Schema-backed notification contracts | done | `notification*.v1` schemas exist in `doc/schemas/` and are synchronized into `node/protocol/contracts/schemas/`. |
| P057-002 | Pure notification core and policy evaluator | done | `orbiplex-node-notification-core` defines typed contracts, `NotificationAllow`, idempotency digests, and `NotificationDeliveryPolicy`. |
| P057-003 | Durable queue and append-only audit | done | `orbiplex-node-notification-store` owns SQLite queue state with `schema` and positive `version` validation, JSONL audit events for create, conflict, opened, handled, snooze, delete, and suppression paths, and Store v3 per-recipient sealing for user/pod-user payload fields. |
| P057-004 | Legacy `notify_emit` compatibility | done | Daemon `notify_emit` adapts into `notification.create` semantics and persists through the new store. |
| P057-005 | Host capability `notification.create` | done | Daemon exposes `/v1/host/capabilities/notification.create`, validates through schema-gate, binds `sender/ref` to the authenticated component identity, enforces `NotificationAllow`, evaluates policy, stores, and emits state pings. |
| P057-006 | Operator notification API | done | Daemon exposes list/detail/opened/handled/snooze/delete routes under `/v1/operator/notifications` and `/v1/admin/notifications`. |
| P057-007 | Operator UI inbox | done | Node UI exposes `/operator/notifications` and `/admin/notifications` list/detail views with opened, handled, and snooze actions. |
| P057-008 | Privacy-minimal SSE ping | done | Daemon publishes only `notification-state-changed.v1` payloads; title, body, kind, subject, and action details are excluded. |
| P057-009 | Inline action execution registry | done | Daemon action execution dispatches wired refs including `contact-request.accept`, `contact-request.reject`, INAC invitation actions, and `mailbox.open`; unknown refs return `action-target-not-implemented`. Node UI renders active controls for wired refs and disabled controls for unwired/expired refs. Action audit facts record the bound actor identity. |
| P057-010 | Rate limiting per sender/kind | done | `NotificationAllow` carries `rate/per-minute`; daemon runtime enforces it per `(sender/id, notification/kind)` before queue/idempotency write, and internal daemon producers use their own configured minute cap. |
| P057-011 | Cross-recipient user inboxes | partial | Recipient class/id are first-class in model and store; daemon exposes user and pod-user scoped read/action routes; Node UI has user and pod-user inbox list surfaces; Store v3 seals notification payload per recipient; daemon read/action routes now require a matching authenticated caller binding and fail closed without one. Remaining work: first-class pod-user session/auth UX. |
| P057-012 | OS notifications | deferred | Explicitly post-MVP; no desktop-shell adapter is implemented. |
