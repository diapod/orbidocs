# P026-012b: closed Agent consumer of a viewer activation

Status: accepted design (2026-10-25); implementation present; clean runtime qualification pending.
Basis: P026 section 6; P066 consent ownership; P073 consumer/lifecycle boundaries; P080 authenticated ChannelJson; P090 provenance.

## Decision

An active P026-012a viewer does not authorize an Agent. A separate operator-only P066 question binds one fresh Agent, its binding, the exact source activation and intent digest, operator, daemon boot/executor/module/launch, one admitted subject, the versioned host task, existing compute budget and source deadline. The question expires within five minutes and no later than the source activation. Allow-once consumes one binding activation, not a read. Approval/retry cannot extend the source deadline. The operator is told about own and released peer assessments, inference, module-only result delivery and irreversible prior disclosure.

Only the exact holder's authenticated channel can start a passage and receive its result. Capture channel context before the worker. An HMAC alias locates an activation; it is not authority. Module HTTP, foreign consumers, generic controller/inference-Flow/external-runtime entrypoints and Agent dispatch cannot borrow the binding. Global CallerBinding remains module:*.

The first profile has a fresh passage, one host-constructed task for one subject, at most one inference, no caller prose/artifacts, history, summary, durable memory, recall, fork, catalog continuation, effect or other recipient. Observation content uses HostObservation in User/Postamble. Fixed host instructions remain separate. Withheld is valid data, never zero or a fallback trigger. Shared admitted urgent-protection semantics remain intact; the Agent cannot invent urgency or perform exposure transitions.

P066 remains the only durable authority owner. Identity host maintains bounded boot-local projections; P073 retains immutable binding/lifecycle/evidence facts. There is at most one active consumer per source activation and 32 per node. Same-intent proposals merge. Changes require consumer revoke/new consent. Source revoke blocks both readers; consumer revoke blocks only the Agent. Archive replay and daemon/module restart cannot reactivate authority. Same-launch reconnect can preserve grants, but old-session passages refuse. Resume starts fresh, never restoring context.

## Contracts and execution

Host-local operator operations are agent.assessment-viewer.request/list/revoke. The channel-only agent.assessment-viewer.run accepts an Agent ref and request identity, never a prompt. Existing agent.product.read delivers a private result only after exact-holder/current-authority admission. Management names are hidden from Agent catalog and dispatch.

New binding/outcome v3 values name a module consumer/private result without changing historical meanings. Consumer policy uses existing policy ref/digest/evidence fields. A namespace table composes the existing Corpus resolver and the assessment consumer resolver; unknown namespaces refuse.

Every context artifact carries a sorted bounded context/authority-dependencies set (maximum 16 opaque refs). The observation depends on the exact 012a and 012b activations; fixed instructions explicitly have no dependencies. Missing is not empty. Manifest and product inherit the union without truncation. This does not turn all observation authority/refs into revocable dependencies and does not establish inference ancestry. The controller uses AgentSuppliedInputManifest v2; the unrelated inference-Flow passage manifest stays outside this profile. Preserve P090 unknown provenance.

Read owners and capture consent/binding/activation/session/lifecycle witnesses before admission; reserve the shared source budget; read ordinary Agora; recheck before context handoff; seal exact input/layers; after all blocking owner work check only witnesses, fresh paired time, lifecycle, manifest, classification and compute budget at dispatch. No P066/SQLite reads or authority locks cross inference. Recheck before commit and result delivery. Observed terminal loss retires locally before fallible durable revoke; it cannot heal. Revocation cannot retract an already admitted disclosure.

Reuse 012a's strict dual deadlines, monotonic lower bound and two-second UTC-lag tolerance. Source and Agent share 30 admitted attempts per rolling 60 seconds/one read in flight. Charge before Agora independently of response. Operator counters split module/Agent attempts while preserving the total. A 429 refuses the passage without internal retry.

Do not persist prompt, view, full request or GenerateResponse in the general object store. Keep only metadata, evidence, dependencies and private content commitments. RAM keeps only the last result per active binding: at most 32 results, at most 256 KiB each and any lower existing cap. Replacement, revoke, expiry and restart make content unavailable; replay cannot regenerate it. Private handles are not general object-store refs. Status exposes authority-blocked with metadata-only operator guidance, not a new lifecycle state.

## Acceptance and evidence

One ordinary daemon, actual ChannelJson application, production P066 provisioning, real Agora and the existing deterministic Inquirium adapter; no models. Foreign signed fixtures traverse admission and remain signed-fixture-input, not replication evidence. Pin clean paired sources and actual images/features; reject assessment-exposure-acceptance and check pins through cleanup.

Qualify consent/scope/holder refusal, withheld/released views, exact observation and manifest binding, construction-complete context, injection-as-data, shared budget, pre-dispatch and pre-delivery revocation/expiry/session/lifecycle loss, consumer-only/source revoke, fork/import/tool/recipient refusal, reconnect, restart/replay and unavailable RAM results. Retain component-only barriers/clock/persistence faults separately. Test strict byte/manifest equality with fixed public time/refs; ordinary-runtime comparisons retain raw inputs and declare the exact normalization allowlist, without claiming raw-byte equality.

The qualifier requires source activation -> consumer consent/consumption -> binding -> session -> observation -> manifest -> final admission -> execution/refusal -> result delivery. Removing/substituting/truncating each link refuses normally, under Python -O and after extraction. Preserve historical Q-02/012a evidence.

## Deferred work and completion

P026-012c separately owns durable memory/recall/history, dependent forks and additional recipients. A bounded 012b result cannot close their matrix, parent P026-012, broader P073, cognition, physical cancellation or release readiness. Freeze contracts first, implement, obtain clean acceptance, then update the ledger and measured claims.

Implementation freeze clarification: a private invocation is identified by Agent plus request ref; the existing observation passage ref remains its controller step coordinate. The manifest/outcome bind both. Failed or lifecycle-invalidated invocations cannot replay inference under the same request ref; a new explicit request starts a fresh context after resume. Final admission sees the assembled adapter input and uses atomic lifecycle/session/authority witnesses. Metadata is retained after execution, outside the runtime lock; boot-local bounded dispatch reservations prevent same-request reinvocation, and restart loses source authority.

Private product reads use agent.product.read.request.v2 and response.v2 on the existing operation. Historical v1 accepts only generic content-store refs and is unchanged. The v2 response preserves explicit authority dependencies.


## Implementation checkpoint

The Node closed consumer composes the P066 owner, source viewer, P073 controller
and local Inquirium transport. Its final callback receives the fully mapped HTTP
body immediately before send; queued/prompt assembly work precedes the witness
check. Closed-path HTTP content telemetry is suppressed independently of capture
interest. Immutable manifests/outcomes retain only metadata and private commitments.
Implementation is not measured acceptance; qualification remains pending here.


Encoding/owner clarification: input commitments preserve the existing observation
owner's `hmac-sha256` form as well as SHA-256; a private HMAC is not relabelled as
an unkeyed content hash. The observation also carries a qualifier for its exact
request-bound v2 manifest. The closed path uses its bounded per-request RAM
dispatch reservation rather than the generic controller's step-keyed paid journal;
source loss on restart prevents recovery from reactivating execution. Generic
controller journaling is unchanged. A fresh resume request may reuse an aborted
step coordinate while its manifest, outcome and observation qualifier bind the
distinct request. These corrections change no authority, scope or deadline.


Private producer boundary: the old Inquirium controller receipt continues to
require exact producer-response bytes and an object-store reference. The private
RAM envelope has a separate Node-local receipt binding the actual Inquirium
producer, exact request manifest, authority dependencies and private product
commitment. It asserts derivation, never byte identity or additional P090 context
ancestry. Its history cannot restore the RAM bytes or source authority on restart.
