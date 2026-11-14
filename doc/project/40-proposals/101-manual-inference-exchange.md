# Proposal 101: Attended Manual Inference Exchange

Status: **Proposed (Draft)**. Date: **2026-11-14**.

Based on:

- [Challenge 101](../10-challenges/101-inference-without-an-automated-provider.md)
- [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md) and
  [Constitution](../../normative/40-constitution/en/CONSTITUTION.en.md): user agency,
  privacy and explicit authority; this optional implementation profile creates
  no new rights, publication authority or declassification power.
- [P063](063-inquirium-model-inquiry-organ.md),
  [P064](064-inquirium-implementation-recommendations.md),
  [P066](066-inquirium-assistant-channel.md), [P073](073-agent-orchestration-organ.md)
- [P089](089-external-agent-runtime-adapter-contract.md),
  [P090](090-inference-execution-provenance-and-non-local-disclosure.md),
  [P100](100-text-origin-labels-and-propagation.md),
  [P047](047-classification-label-propagation.md)
- [S029](../60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md),
  [S035](../60-solutions/035-interaction-broker/035-interaction-broker.md),
  [S039](../60-solutions/039-notifications/039-notifications.md),
  [S044](../60-solutions/044-inquirium/044-inquirium.md)

## Executive Summary

Provide one text inference through an operator-mediated exchange: Node prepares
an approved packet, the operator consults a separate chat, and Node admits the
pasted response. This is a host-native execution transport below Inquirium, not
a new Agent kind or a model that pretends to have known weights and parameters.
It can be the only configured inference candidate for an **attended** profile.

The common contract preserves classification, provenance, output validation and
effect admission. Waiting, recovery and commit belong to host/domain owners,
not a synchronous middleware adapter. All additions here are planned; existing
API, Agent and local-only assistant qualifications do not qualify this transport.
This proposal does not enlarge the current alpha release gate.

## Context and Problem Statement

P063 separates semantic inquiry from runtime/provider mechanics. S044 already
lists host-native fixture and middleware transports. P089 supplies useful
`AwaitingOperator`, `Committed` and `Replayed` result patterns, and S029 provides
deferred status and cancellation. Reuse those mechanisms rather than creating
another scheduler, question registry, provider credential store or Agent loop.

There are material gaps. In `node:daemon/src/host_capabilities_host.rs`, the
external runtime path maps `ExternalRuntimeRunResult::Unknown` to
`AgentRuntimeError::Deferred`, but rejects `AwaitingOperator`/`AwaitingTool` for
the current deliberation-only profile. P073's local controller is synchronous.
P066 widgets do not accept arbitrary model-response text. Integration is work,
not an inference from the existence of these interfaces.

## Proposed Model / Decision

### 1. Ownership and scope {#ownership}

| Owner | Responsibility |
|---|---|
| Inquirium / P063 | Bounded inquiry, capabilities, input/output contracts and policy admission |
| Host model-runtime / S044 | Native transport candidate, proposed `ModelTransportConfig::ManualExchange`; no long-lived adapter call |
| Host inquiry operation owner | Immutable packet custody, deferred result, answer admission and one logical commit |
| S029 / S035 | Status/cancel projection and existing operation-completion watches; not a second source of inquiry facts |
| S039 / P066 / UI | Notification and fixed host-owned export/import form, independent of model availability |
| Agent / JSON-e Flow / Corpus | Existing consumer contracts, explicit continuation and independent effect/acceptance gates |

The reusable concept is a **deferred inference result**. Extract only the proven
P089 lifecycle/commit mechanics, after inspecting their actual contracts; do not
copy external-runtime session authority or an entire Agent turn into it. A
future batch API might consume it, but that is a hypothesis, not v1 scope.

V1 supports text generation and text-based classification/transformation with
host-validated output. It rejects attachments, image/audio input, embeddings and
required streaming; it never silently drops them. The external browser is wholly
user-operated: no browser automation, cookie capture, automatic paste, scraping,
background sending or automatic clipboard reads. No subscription-access claim
or provider-specific entitlement follows from this profile.

### 2. Eligibility, startup and fallback {#eligibility}

An `operator-gated` candidate requires an explicit, current attended interaction
grant, an authenticated recipient and a usable local UI surface. A background
Agent, Scheduler job or unattended/headless deployment cannot select it in v1.
A merely connected browser is not an attention grant. Bound outstanding requests
and requested exchanges per principal and operation; absence never creates an
unbounded queue. Lost presence pauses surfacing, then expires under the original
deadline; it does not start another consultation.

Startup, authentication, packet assembly, consent, notification, import and
cancel must work with **zero automatic model providers**. Static host templates
create the first prompt. The assistant may render an exchange card, but is not
needed to produce one. S035 `WaitCondition::OperationDone` wakes consumers after
completion; S039 exposes pending work in an inbox, independently of the original
chat view. Supported tasks work; unsupported capabilities remain unavailable.

Keep host-only structural conformance before routability; test with a simulated
operator through the real endpoint. Do not call a real person or external model
as an activation healthcheck. Such conformance proves bridge behavior, not the
identity or quality of an external model. Consumers requiring verified model
identity or calibrated model evidence cannot use this unverified candidate.

P064 owns candidate/failure policy; the adapter does not select fallbacks.
Its [execution-failure closeout](064-inquirium-implementation-recommendations.md#execution-failure-fallback)
tracks the shared host chain as P064-FBK-001/002 and the manual tail as
P064-FBK-003. An enabled manual candidate must be last in the admitted ordered
plan; conflicting order is rejected rather than silently changed. A manual-only
plan is valid and needs no automatic runtime or completed automatic-fallback
implementation. Pending human input never advances the chain.
Manual fallback is opt-in for explicitly admitted classes such as transient
unavailability. Never fall back from `provider/refusal`, policy denial,
revocation, operator cancellation or expiry. `StrictLocal` cannot select this
unknown-locality transport. A user may explicitly start a new inquiry under a
separately admitted export profile; an ack does not override StrictLocal.

### 3. Export is admitted before visibility {#export}

Treat **packet issuance**, including display or download, as the export boundary
for policy. Reuse P047 `evaluate_egress` with `Surface::Export` and P066's
`egress/ack-ref`, bound to the exact packet, principal, profile and revision.
Before ack, show only a safe summary, destination uncertainty, classifications,
size and consequences; do not render the export body in hidden DOM, logs or
notifications. This is conservative authorization, not proof a provider received
the text. Clipboard copy requires a further explicit click after admission.

V1 refuses raw Personal and higher protected-class exports. A separately redacted
text projection may be offered, but must independently pass existing classification
and export policy. P090 `projection/kind: redacted` describes provenance projection,
not proof that the input text was redacted. Redaction is not automatic downgrading;
operator ownership/consent is not authority over other people's protected data.
Destination declaration is optional for the v1 eligible low-class profile and
remains asserted. Higher-class release is deferred pending a separate decision;
even a mandatory destination declaration would not prove confinement.

The ack explains that the Node cannot enforce the external chat's retention,
training settings, memory, custom instructions or `store:false`. Suggest a fresh
temporary chat when available without claiming that it proves deletion. Expose
packet bytes and a configurable warning threshold; never hardcode another chat's
changing input limit. A self-contained packet carries no private storage paths,
raw internal references, credentials or authority tokens. Manual copy may also
reach clipboard history/synchronization outside Node control.

### 4. Exchange data and strict import {#exchange}

Recommended logical shapes, to freeze during P101-001; these are **not existing
schemas**. Keep internal bindings separate from the exportable text:

| Shape | Minimum fields |
|---|---|
| Private exchange record | `operation/ref`, `exchange/ref`, `principal/ref`, request/input revision, `profile/ref`, `packet/ref`, exact `packet/digest`, `egress/ack-ref`, deadline, state and attention budget |
| Export packet | Public opaque `exchange/ref`, operation-bound fresh nonce, task/instructions, admitted text, output format and exact closing marker |
| Import request | Operation/exchange binding, nonce-bearing envelope text; principal derived from authenticated session, never body-supplied |
| Committed result | Exact packet/input binding, raw-import digest, parser-profile revision, parsed result digest, asserted provenance ref and durable commit ref |

Use a new opaque exchange id and nonce for each newly admitted operation/attempt;
never derive them from prompt content. Reuse the nonce on replay of that same
frozen exchange, not on a new identical question. Nonce and closing marker are
correlation/framing data, never authentication or evidence of independent work.
The external template asks for one JSON code block containing the envelope and
closing marker. Complete framing detects some truncation, not semantic completeness
or an honest model execution; an operator can construct the whole envelope.

The v1 parser is deterministic and bounded:

1. Enforce input byte/depth/string limits before parsing. Retain the raw-import
   digest privately for the finite exchange lifetime.
2. Permit removal of one leading BOM and surrounding ASCII whitespace, and one
   complete outer `json`/unlabelled code fence. Normalize CRLF only in framing or
   JSON structural whitespace, never inside string payloads. Reject multiple
   blocks, trailing prose, missing closing fence or marker, and wrong nonce.
3. Parse strict JSON and reject duplicate decoded keys recursively. Reuse the
   existing `node:model-runtime-http/src/output_envelope.rs` decoder where its
   contract fits: it already rejects duplicate keys. The manual framing layer
   must not weaken the API decoder, which currently rejects fences.
4. Do **not** globally strip zero-width characters or replace typographic quotes.
   Preserve legitimate payload text; reject ambiguous structural characters with
   actionable diagnostics. Smart-quote repair is not silent normalization in v1.
5. Validate envelope schema, the exact question/output contract and all context
   bindings. Unknown or malformed controls fail closed. V1 can return text or
   structured data; tool/question controls stay disabled unless a separately
   qualified consumer reuses normal host tool/effect/question gates.

Only the authenticated packet recipient/ack principal may import, or a narrowly
and explicitly delegated responder if that profile is later enabled. Recheck
current grants, operation state and revision; CSRF/session and replay protections
reuse the existing host action boundary. UI possession, localhost access and
administrator role alone are not substitution authority. A new session of the
same principal after restart still needs fresh authentication and current rights.

### 5. Durable waiting, recovery and attention {#recovery}

Use a host-native waiting outcome with `request_ref`, mapped by the host to S029
deferred execution. A native provider returns promptly; no thread, HTTP request,
runtime lease or synchronous middleware invocation waits for a person.

```text
prepared -> issued/awaiting-operator -> validated -> committed
    |                 |                   |
    +-----------------+-------------------+-> cancelled / expired / revoked
```

The domain owner stores a sealed immutable packet and exact bindings before
issuance. S029 stores bounded references/status, **not plaintext packet bodies**
or a second authoritative result. Use existing protected custody and retention
mechanisms, not another blob store. Recovery reoffers the same packet/nonce only
after current access/export checks and an explicit operator action; never
reconstruct changed context or resend automatically. If an ack/grant no longer
applies, require an explicit new admitted action or refuse.

Commit once under the operation identity with P089's compare/replay pattern.
Concurrent identical imports yield the same commit; a different second body is
a conflict. Return `Replayed` for a matching retry after lost response. Couple
the result fact to a durable pending-consumption marker so restart between commit
and consumer wake-up cannot lose or duplicate continuation. Reuse existing S029
continuation/consumer idempotency; do not claim exactly-once physical delivery.

Use one logical result consumption and reacquire/recheck execution grants before
consumer continuation. Agent lifecycle changes and expired wall-time remain
binding. Time awaiting the person is measured separately from computational work,
but never silently extends an absolute operation deadline, lease or Agent budget.
An explicit attended profile must define those separate finite limits. Do not
borrow the synchronous GUIDE deadline unchanged and promise hours of waiting.

Default to no model-driven repair; allow at most one explicitly requested further
exchange in the initial profile, with a fresh attempt binding and export ack.
Show a maximum of N exchanges before starting a multi-step consumer. Enforce
per-principal pending-byte/count quotas and preserve cancellation at capacity.

Packets/raw imports have a finite deadline no later than the owning inquiry's
retention ceiling. Purge terminal packet bodies after durable result handoff and
replay facts are secured; expire/cancel purges bodies without erasing still-needed
negative/idempotency facts. Result retention follows its admitted consumer;
never turn a packet into durable memory by default. Deletion cannot retract
external copies or attest to provider deletion.

### 6. Honest provenance and parameters {#provenance}

| Property | Manual profile |
|---|---|
| Provider/model identity, locality | Unknown; optional operator declarations stored as assertions |
| External dispatch | `ambiguous` after issuance; a pasted result alone does not prove provider I/O |
| Input egress | Conservatively `possible` after issuance; actual recipient delivery remains unobserved |
| Provider disclosure | `unknown`; operator declarations do not become verified provider facts |
| Text origin | Proposed P100 surface profile: model origin with asserted evidence, not human origin merely because pasted |
| Sampling, seed, system-role isolation | Unsupported as enforceable requirements; style instructions are advisory |
| Token use | Unknown or explicitly estimated, never provider-metered |
| JSON/size/context binding | Host-enforced on import, not a guarantee of external generation |

Keep local issuance/import facts and operator execution claims separate. Do not
set `dispatch: dispatched` or `input-egress: occurred` solely because someone
pasted text or claimed to have sent it. P090 owns any future assertion-backed
projection; the observed evidence cannot be upgraded. Local UI does not establish
local inference. Reuse P100's separate origin and evidence facets: the shorthand
`{model, asserted}` is not a two-member `origin/classes` set. `asserted` needs an
explicit vocabulary/profile extension before schema implementation. Known human
edits preserve/join origin rather than cleansing it.

### 7. Implementation recommendations and acceptance {#implementation}

Inspect `node:docs/development/reuse-index.v1.json` first, then confirm the actual
contracts. Favor native host transport and existing owner composition; do not add
a new provider process, background polling service or generic Agent subclass.

| Reuse candidate | Required boundary check |
|---|---|
| P089 result/commit patterns; `external_agent_runtime.rs` | Extract only matching lifecycle mechanics; manual wait is not wired merely because the enum exists |
| `AgentRuntimeError::Deferred`, host continuation | Implement waiting-to-deferred mapping and durable single consumption explicitly |
| S029 registry and S035 `OperationDone` | Registry is projection; pending notification and terminal wake are distinct |
| P066 questions/P057 actions | Fixed host-only import form; preserve allowlisted consent widgets and forbid model-selected import UI |
| P047 export, P066 ack, P090-007a preflight | Before issuance; one packet attempt, repeated display is not a second execution |
| Existing strict output decoder / Schema Gate | Qualify framing and duplicate-key behavior; share pure logic only where semantics match |
| P091 settings | Opt-in profile, finite limits and explainable eligibility, not hidden fallback |

One shared acceptance report owns the following matrix; owner trackers link to
it rather than manufacturing separate completion claims. No real model, external
chat or browser automation is needed for initial offline fixtures. The simulated
operator uses the same authenticated import endpoint as the UI, never a private
test completion hook. UI qualification is separate from API/owner fixture proof.

- Cold start with all automatic providers absent; host renders consent and first
  packet. A text inquiry reaches one result; Agent and Assistant consume it through
  normal boundaries. Corpus consumes it only as an explicitly selected,
  unverified candidate: no calibrated evaluation, source corroboration, evidence
  admission or public release is inferred.
- Restart before issuance, after issuance, after answer commit and before consumer
  acknowledgement; freeze bytes/nonce, preserve pending/replay facts and consume
  once. Cover lost import reply and concurrent identical/conflicting answers.
- Wrong nonce, truncated envelope/marker, exact fenced JSON, BOM/CRLF, smart quotes,
  legitimate zero-width payload, duplicate and escaped-duplicate keys, trailing
  prose, oversize/deep JSON and injection controls. No silent content rewrite.
- Different principal, stale session/grant, expiry/cancel, revoked export ack and
  StrictLocal: refusal before disclosure or continuation as appropriate; no body
  in notifications, logs, hidden DOM or denied HTTP responses.
- Unsupported modalities/parameters, unavailable operator, background/scheduler
  calls, attention quota, failure after capacity exhaustion and terminal provider
  refusal: typed outcomes, no silent downgrade or repeated prompts.
- Import-only model origin/asserted evidence, unknown provider/locality and
  ambiguous external dispatch survive restart and consumer projection; copying
  does not produce proof of provider identity, token usage or retained privacy.
- Operator sees exact export, byte count, waiting/expiry state, copy and cancel;
  textarea/import works without a model, clipboard convenience requires a click.
  Manual real-chat trials later qualify usability only, with explicit permission.

## Invariants

1. One inference is the v1 exchange unit; no whole-turn external authority.
2. No model is required to start, display, import, cancel or recover an exchange.
3. Export permission precedes packet visibility; copying is not a permission gate.
4. Correlation is not authentication; model output is not authority or evidence of execution.
5. No browser automation, silent remote fallback or unattended manual routing.
6. Waiting holds no execution lease and extends no authority; one result commit
   and logical consumption survive restart without resending.
7. Declared capability/quality evidence remains narrower than API/model guarantees.

## Trade-offs

The same inquiry contract becomes useful without an automated provider, but only
with operator attention. Restricting Personal export and strong identity consumers
limits coverage deliberately. Strict parsing may require a manual correction;
silent text repair would sacrifice integrity. Unknown chat memory/retention and
unverifiable model identity prevent equivalent automated-provider qualification.

## Failure Modes and Mitigations

| Failure | Response |
|---|---|
| Operator leaves or chat stalls | Finite wait, explicit cancellation/expiry, no background retries |
| Output is fabricated, edited or injected | Asserted origin, strict parser and ordinary consumer/effect admission |
| Restart loses dispatch knowledge | Persist issued state; ambiguous external dispatch, no automatic reissue |
| Packet context changes | Immutable packet; new operation for changed inputs, no rebinding old approval |
| Invalid JSON repair loop | Local diagnostics, finite attention budget, no implicit model repair |
| Consumer cannot defer or requires verified execution | Typed unavailability until the consumer profile is qualified |

## Open Questions

- What separately reviewed policy, if any, should permit raw Personal export?
  V1 forbids it; declaration of destination alone cannot settle confinement.
- Which consumers beyond the initial attended text profile can accept asserted
  origin and unknown execution without weakening their quality contracts?
- Whether a future batch provider shares enough deferred-result semantics to
  justify further extraction requires a second concrete consumer.

Decisions for v1: destination assertion optional for eligible low-class export;
single text inference; host-only import UI; no delegate responder by default.

## Next Actions

Freeze contracts before transport implementation; then build the smallest
model-free exchange through the real authenticated endpoints, recovery and UI.
Qualify consumers individually. Do not require a commercial chat or additional
model to run structural acceptance.

## Implementation Tracker

All rows are `todo`; documentary adoption is not runtime completion.

| ID | Task | Status | Depends on | Acceptance / owners |
|---|---|---|---|---|
| P101-001 | Freeze deferred inference, attended candidate, packet/import and provenance contracts | todo | Existing P063/P064/P089/P090/P100 contracts | Exact schemas/typed refusals planned; host-only parser and origin profiles, trust/parameter matrix, owner map and no conformance bypass; coordinate owner MEX rows |
| P101-002 | Host-native transport and durable deferred result lifecycle | todo | P101-001 | S044/S029/P089 reuse; no blocking call, immutable sealed custody, quotas, restart, replay and one logical consumption |
| P101-003 | Pre-issuance export admission and honest provenance | todo | P101-001 | P047/P066/P090/P100 reuse; exact ack and principal, Personal policy, ambiguous dispatch, asserted origin, bounded retained bytes |
| P101-004 | Model-free notification, packet view and strict authenticated import | todo | P101-002; P101-003 | S035/S039/P066 reuse; host-only form, copy after ack/click, exact parser, nonce/marker and principal controls, no browser automation |
| P101-005 | Attended consumer continuation and explicit fallback policy | todo | P101-002; P101-003; P101-004 | P073/P066/P069 reuse; individual consumer qualification, fresh rights at resume, no StrictLocal/refusal downgrade, separate attention and execution budgets. Qualify manual-only continuation independently; switching from a failed automatic candidate is separately owned by P064-FBK-003 and jointly checked in P064-FBK-004. Do not add that optional integration as a prerequisite of the sole-provider proof. |
| P101-006 | Qualify sole-provider offline and UI acceptance | todo | P101-004; P101-005 | Full matrix above, shared source-bound report, no other models or test-only completion path; preserve existing alpha/baseline statuses |
