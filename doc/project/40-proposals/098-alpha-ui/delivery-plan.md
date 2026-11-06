# P098: Delivery Plan and Tracker

Status: **Proposed**. Date: **2026-11-06**.

Parent: [Proposal 098: Alpha UI](../098-alpha-ui.md). This is the single canonical
location of P098 task definitions, delivery sequencing and acceptance criteria. Domain
contracts and implementation recommendations remain in the parent and owning proposals.
Moving the tracker changes no implementation status.

## Delivery Order and Parallel Tracks

This is a dependency-driven plan, not a calendar or duration estimate. Start each work
package when its own contract inputs exist. A delivery record reconciles
outputs/evidence; it does not impose another execution gate on the owner.

| Boundary | First deliverable / join | Concurrent work |
|---|---|---|
| Foundation record — P098-016 | Inventory P098-001, graph checker P098-011 and surface freeze P095-014 have independent starts. Catalog/configuration P098-002 follows inventory/surface freeze; rendering P098-003 follows catalog. | Freeze P007-LP-001 operator-role compatibility and implement P095-013. P057-018 → P057-019 bounded inbox and P036-004 retention work start independently. Graph tooling gates the delivery record, not P098-004a implementation. |
| First useful profile — P098-017 | P098-004a supplies home/theme, people contacts/chat/readiness, complete attention and handled/history return. P098-005a qualifies common guided mechanics early on P097. Both use role-aware local-primary admission. | Implement real P/Q provisioning and independent domain contracts. Adding P/Q must preserve O's home; unsupported P/Q get typed refusal. No independent domain runtime or Whisper review is required for this increment. |
| Independent compatibility record — P098-018 | P007-LP-001 unlocks provisioning P007-LP-002 and context freeze P024-009 in parallel; both meet at P024-010. P095-012 adds the verified session producer. Record compatibility of those actual versions. | No wait for local-primary delivery or module-carrier freeze/runtime. Existing owner evidence is reused; only missing cross-owner seams need another test. Module-backed consumers separately retain P080-048/049. |
| Domain lanes — derived report views | Existing P098-004b/012/015 deliver communication/inquiry, P098-005b/006 deliver guided Whisper/Rumors, and P098-009 delivers memory. The scope file lists each view's required outputs. | Lanes finish independently; a completed sub-outcome may become available while its aggregate remains partial. There is no extra lane task/status to close. |
| Return and final record — P098-022/023 | P098-022 checks P098-014 return links against exercised Messaging/inquiry and Whisper-review destinations. P098-007 supplies integrated acceptance; P098-023 reconciles the final profile record. | Activity contracts and section rendering start with their owner projections. Return does not wait for the My rumors record-link view or the explorer; final acceptance still requires those outcomes. |

### Parallel owner work and exact join points

- P024-009 unlocks P036-012, P080-048, P060-038, P026-014, P066-PA-001 and P073-PA-001.
  P036-012 then unlocks P024-011 and P013-PA-001; the latter unlocks P015-009.
  P098-010a/b/c reconcile their own inputs while runtime work proceeds. The aggregate
  contract gate does not delay the initial catalog/profile.
- After P024-010 and each branch's own freeze, P095-012, P080-049, P057-020, P060-039,
  P066-PA-002, P073-PA-002, P036-014, P024-012, P015-010 and P026-015 can progress
  independently. All existing prerequisites still apply, including P057-019 for
  independent notifications. Verifier completion is not domain access.
- Whisper intake P013-PA-002 joins its frozen custody contract with P036-014 producer
  bindings and P080-049 carriage. Crypto P015-010 and viewer P026-015 proceed with owner
  fixtures in parallel; P013-PA-003 composes them. P098-005b qualifies independent
  review using the frame proven by P098-005a. Complete Rumors P098-006 also needs
  P013-DFR-003 and P036-008 for confirmed record links.
- After P036-004, expiry P036-005 → P036-006 and records P036-007 → P036-008 are
  separate branches. P024-012 and P036-014 meet at P024-013 provisioning; those grants,
  bindings and P036-004–007 meet at P036-013. P047-001 and P098-009 qualify the
  explorer. Authoring and Resume do not wait for this read runtime.
- P057-020 enables independent attention P098-004b; P060-039 enables Messaging P098-012.
  P066-PA-002 and P073-PA-002 join at P098-015. P098-014 consumes their projections and
  retained P013 work. P098-022 checks actual return destinations from P098-012/015/005b,
  without requiring every Rumors view or another lane record.

### Full independent-profile blockers

| Boundary | Required owner/UI outputs | Limitation of earlier evidence |
|---|---|---|
| Actors and current authority | P007-LP-002; P024-010; P095-012 | Real O/P/Q custody and verified sessions are required; local-primary and fixture-only IDs prove less. |
| Module-backed entries | P080-049 plus the consumer's own gate | The bridge is specific to module paths; built-in operations do not wait for it. |
| Attention and Messaging | P057-020; P060-039; P098-004b/012 | Independent recipient, key/route, action and result ownership must work. |
| Ask or delegate | P066-PA-002; P073-PA-002; P098-015 | Real inquiry and a bounded delegated task need their respective grants, runtime and outcome evidence. |
| Rumors | P013-PA-002/003; P015-010; P026-015; P013-DFR-003; P098-005b/006 | Intake, crypto, viewer, publication/readback and confirmed record-link views all remain required. |
| Memory | P036-014; P024-013; P036-013; P047-001; P098-009 | Binding, obtainable grants, current policy/materialization and retention are distinct. |
| Return and overall acceptance | P098-014/022; P098-007/023 | Working destinations, actual retained work and browser/native/UX evidence remain required after backend admission. |

The newly assigned owner tasks remain `todo`. These are bottlenecks in the declared
graph, not a measured critical path. Custom editors/CSS, S022 semantic search and
optional ADC/LLR controls remain outside the baseline unless a selected owner profile
explicitly requires them. Missing required outcomes keep the final profile open; they
cannot disappear through a deployment-specific omission.

## Delivery Tracker

Required Alpha rows start as `todo`; the later editor and advanced CSS are explicitly
deferred. Completing documentation does not complete these rows. Node implementation
work must link its own ledger and evidence when scheduled.

| ID | Status | Dependencies | Deliverable and gate |
|---|---|---|---|
| P098-001 | todo | Owning solutions | Deliver a reproducible Node inventory command over registered Node UI routes, package/admission entry declarations and notification kinds/actions. Emit deterministic JSON pinned to Node/Orbidocs commit plus relevant content digests (or reject dirty sources), with coverage/refusal diagnostics for unparsed dynamic registration. Use the same sanitized artifact as catalog golden fixtures and a Node `make check-ui-inventory`/CI drift check; compare source-input digests and semantic inventory rather than volatile report timestamps or a self-containing artifact commit; never include live private participant data or treat inventory as permission. Record actual functions, owner gaps and each acceptance profile. |
| P098-002 | todo | P098-001; P095-014; accepted P091 composition and S019 package contracts | Freeze bounded catalog/configuration, `node-ui-appearance.v1` theme inputs, P091 descriptors/preset provenance and the versioned participant manifest section, full binding identity/generation, default JSON and activation/refusal rules. Include typed limits, inheritance/reset and cross-palette constraints from §5. Implement the three pure projections over values and supplied owner witnesses; golden/generative move/hide and admission-invalidation checks pass. Generic catalog delivery and the local-primary profile do not wait for independent-participant owner contracts; later entries consume those contracts at admission. Freeze non-reused complete admission identities across restart/restore, generation-matched owner witnesses and unknown-on-missing behavior. Pin theme state derivation and hex stylesheet emission with the preset; diagnostics identify contributing editable tokens. |
| P098-003 | todo | P098-002; P095-014 | Deliver responsive home/style tokens with guarded participant fragments and independent ordinary shell. Validate default and overridden palettes, derived states, density/type/radius bounds, keyboard, zoom/reflow, locale expansion, no-JS, context invalidation and native delivery. Use host-owned CSP-compatible style emission and keep passive modules unchanged. Exercise the frozen P095 conformance cases on new Alpha routes; inherited operator-route evidence does not close this gate. |
| P098-004 | todo | P098-004a; P098-004b | Complete home and attention integration for both named profiles. Preserve separate handled/domain outcomes and P026/P057 exclusions; completion of 004a alone leaves this aggregate open. Follow-on P057-015/016 domain notices remain separate. Full cross-owner activity/resume is P098-014. |
| P098-005 | todo | P098-005a; P098-005b | Complete both guided profiles while retaining their independent evidence. P098-005a qualifies common mechanics early on P097; P098-005b qualifies independent Whisper review. The aggregate remains open until both pass. |
| P098-006 | todo | P098-002; P098-003; P098-010a; P098-010c; P080-049; P095-012; P013-PA-003; P013-DFR-003 | Integrate Browse, Contribute through authorized result readback, and My rumors through §8 owner methods and package entries. Preserve distinct operation gates and P095 rendering; test participant isolation, P026 withholding and operator regressions. All three outcomes are required. P036-008 and the local exposure outputs are transitive owner prerequisites, not duplicate UI implementations. |
| P098-007 | todo | P098-003; P098-004; P098-005; P098-006; P098-009; P098-010; P098-011; P098-012; P098-014; P098-015 | Run integrated task-based usability/accessibility acceptance for the independent-participant profile in browser and separately in the supported native host. Keep earlier local-primary evidence separate. Verify current inventory and dependency checks, pin functions/source and record bounded findings. |
| P098-008 | deferred | P098-002; P091 change/approval contracts | Add an operator navigation/theme editor over the same file-backed descriptors: preset versus explicit-value provenance, field/pair diagnostics, preview, source-specific inheritance reset and active-value reporting. Preserve P091 activation/approval; no raw CSS or template authoring. |
| P098-009 | todo | P098-001; P098-002; P098-003; P098-010a; P098-010b; P095-012; P036-013; P047-001 | Integrate the owner-delivered binding/read profile with list/detail UI, bounded continuation, personal-record and source/retention context. Prove participant isolation, legacy exclusion, P095 privacy and unchanged v1 semantics. P024-012/013, P036-014 and P036-004–007 are transitive prerequisites; S022 is not required. |
| P098-010 | todo | P098-001; P098-010a; P098-010b; P098-010c; P066-PA-001; P073-PA-001 | Reconcile the accepted owner freezes in §8/§9 and canonical schemas: participant context, memory-view/profile, intake custody, Whisper operations, Assistant conversation and bounded Agent task/activity projections. Verify consistent issuer/admission, migration, limits and negative fixtures across the named tasks. Task allocation alone does not complete this contract gate; runtime and UI consumers remain separate. |
| P098-011 | todo | Existing tracker declarations | Deliver the repository dependency extractor, deterministic graph/report, Make target and CI check specified in §9. Source-qualified edges and explicit contract boundaries must remain distinguishable; bad/ambiguous references fail rather than disappear. Acyclicity does not prove missing work has been discovered. Consume the checked-in dependency-scopes.json roots/rules and generate each named scope separately; derive delivery-view status without a second status field. Pin source/scope/extraction digests. Cover MSG-ONB-001c-04 and legacy bare 002 resolution, reject ambiguous shorthand, and exclude retired 019–021 from task definitions/edges. |
| P098-012 | todo | P098-003; P098-010a; P060-039; P095-012 | Integrate Message someone for an independently admitted participant: owner-provided readiness, route/key selection, compose/thread/mailbox and result links. Prove actual P/Q send/receive and cross-participant refusal without operator authority or fallback; retain local-primary evidence separately. |
| P098-013 | deferred | P098-002; P098-003; P095-015 | Freeze and deliver advanced operator CSS packages under §5: versioned styling/resource contract, digest-bound local assets, explicit selection, synthetic preview, recovery without custom styles and P091 rollback. Obtain P095 admission/isolation for the style surface and qualify integrity, critical controls, accessibility and private-view lifecycle separately. No baseline dependency or V1 raw-CSS escape hatch. |
| P098-014 | todo | P098-003; P095-012; P013-PA-003; P060-039; P066-PA-002; P073-PA-002 | Integrate bounded My activity sections and Resume over the named owner projections in §1. Prove independent participant references, per-owner paging/failure, expired/unavailable drafts, uncertain versus completed outcomes and fresh authorization after module re-admission. Resume one retained Whisper draft across restart without effect replay. No global scan/count, transcript index or UI operation store. |
| P098-015 | todo | P098-003; P098-010a; P095-012; P066-PA-002; P073-PA-002 | Integrate Ask or delegate for independent participants: one real Assistant conversation and one named bounded Agent task with explicit scope/budget/effect admission, status and authorized result/stop controls. Keep channel and delegation visibly distinct; no Messaging peer, inferred spawn, automatic provider choice or operator fallback. Prove O/P/Q isolation and owner-unavailable recovery. |

P098-004 is split into independently tracked delivery slices, both initially `todo`:

| Subgate | Status | Dependencies | Deliverable and gate | Consumers (not prerequisites) |
|---|---|---|---|---|
| P098-004a | todo | P098-001; P098-002; P098-003; P095-013; P057-019; MSG-ONB-004; MSG-ONB-006 | Deliver home, complete bounded attention and P057-backed handled/history return links for `alpha-local-primary@v1`. Require session-subject equality with the explicit operator-role binding, or the declared pre-migration legacy rule, and existing owner guards. Admit built-in contacts, chat and P097 readiness as the people category for this profile; pin exact route/entry IDs in 002 and exercise an existing supported contact/chat path. No operator-only surface is relabeled or operator client exposed. Missing route/readiness gets its owner recovery state; unrelated functions may remain unavailable. No evidence is claimed for independent participants. Omit Resume until a supported owner reports a recoverable item; cross-owner activity and retained-draft acceptance remain P098-014. Graph tooling is not an implementation prerequisite; delivery record 017 consumes it via 016. Include fixtures where P/Q exist and O retains this surface while unsupported P/Q receive typed refusal. | P098-004; P098-004b |
| P098-004b | todo | P098-004a; P098-010a; P024-010; P095-012; P057-020 | Deliver the same surface for `alpha-independent-participant@v1`, using P007-created identities and participant-bound recipients, actions and relationship state. Prove cross-participant refusals, switching, lost replies and private-fragment invalidation. | P098-004 |

P098-005 has two independently deliverable subgates, initially `todo`:

| Subgate | Status | Dependencies | Deliverable and gate | Consumers (not prerequisites) |
|---|---|---|---|---|
| P098-005a | todo | P098-002; P098-003; P095-013; MSG-ONB-004; MSG-ONB-006 | Qualify the common guided frame on local-primary P097 preparation/recovery: side-effect-free GET, revision/CSRF-checked POST and 303 GET, stable reviewed-effect identity across reload/Back/lost replies, changed-review invalidation, authorized readback and deferral. Reuse owner-retained intent/results; any missing P097 owner primitive needs a named owner prerequisite, not a UI effect ledger. No P095-012 or Whisper runtime is required. | P098-005; P098-005b; P098-017 |
| P098-005b | todo | P098-005a; P013-PA-003; P095-012 | Apply the qualified frame to independently admitted Whisper review and contribution. Prove candidate/audience revision invalidation, key/session changes, explicit approval and lost-response readback under P/Q authority; local-primary evidence does not qualify this participant context. | P098-005; Rumors delivery view |

P098-010 has three independently reviewable subgates, initially `todo`:

| Subgate | Status | Dependencies | Owning freeze | Consumers (not prerequisites) |
|---|---|---|---|---|
| P098-010a | todo | P024-009; P080-048 | Reconcile the trusted participant source/subject contract and receiver-bound host/module carrier. P095-012 implements the session producer later; its runtime is not needed to freeze the contract. | P098-004b; P098-006; P098-009; P098-012; P098-015 |
| P098-010b | todo | P036-012; P024-011 | Reconcile resource membership, participant read-view profile/API, legacy attribution, classification/materialization, issuer/provisioning policy and continuation limits. | P098-009; independent of Whisper runtime |
| P098-010c | todo | P013-PA-001; P015-009; P026-014 | Reconcile the contracts for Browse, Contribute and My rumors: participant viewer, intake custody, owner references and exact v2 review/authorship/publication binding. DFR-003 already owns My rumors semantics. | P098-006; independent of the explorer UI and optional ADC/LLR controls |

### Delivery Records

These are separate, initially `todo` tasks for accepting and recording delivery
increments. P098-019, P098-020 and P098-021 are retired IDs, reserved against reuse:
their aggregation role is replaced by the derived delivery views in
[dependency-scopes.json](dependency-scopes.json), with no stored task status.
P098-001–015 and the owner trackers remain the authoritative work packages. A
coordination row consumes their scoped outputs; it does not duplicate implementation,
change an owner's status or add a reverse prerequisite to that owner. The dependencies
below are **completion gates**. Work may start as soon as its own inputs are available;
unrelated lane completion is never a start barrier.

Each completion record identifies delivered functions, owner tasks and source and contract
versions, acceptance profile, evidence references, unavailable outcomes and authorized
recovery. Reuse existing owner/Node evidence locations; create no second implementation
ledger. A partial delivery is recorded as a note/output, while the coordination task
remains open until its full gate passes.

| ID | Status | Dependencies | Delivery task and completion gate |
|---|---|---|---|
| P098-016 | todo | P098-001; P098-011; P095-014 | Accept the implementation foundation handoff: pinned route/package/action inventory, executable dependency check and exact surface conformance cases. Record owner assignments, source/contract inputs and both profile boundaries; verify unresolved prerequisites remain visible. This is a reusable engineering output, not a participant release. |
| P098-017 | todo | P098-016; P098-004a; P098-005a | Deliver and record the first usable `alpha-local-primary@v1` increment: home/catalog/theme, a usable people entry for existing contacts/chat/P097 readiness, complete bounded attention and handled/history return under the restricted role-aware client. Qualify the guided P097 mechanics in 005a before this first delivery. Exercise an owner-backed attention path in browser and supported native host, including unavailable/unknown outcomes. Document unavailable functions and the absence of P/Q qualification; require no independent identity or independent-participant domain runtime. |
| P098-018 | todo | P024-010; P095-012 | Record compatibility of the actual P024 verifier, P095 session adapter and P007 role/custody outputs against the accepted P024-009 context contract, with pinned versions and evidence links. Reuse owner tests and run only missing cross-owner seams: role-model migration preserves O while P/Q remain explicitly unsupported in local-primary mode, then independent mode admits P/Q without authority leakage. This receipt introduces no new verifier or domain gate and does not require module runtime. |
| P098-022 | todo | P098-014; P098-012; P098-015; P098-005b | Deliver the cross-owner return increment. Reconcile bounded activity sections with the exercised conversation/task/Messaging and Whisper-review/result destinations; resume a retained Whisper draft across restart and module re-admission. Prove per-owner failure independence, expired/unknown states, current authorization and absence of effect replay. Section work starts before the required destination outputs are usable; the explorer is not a completion prerequisite. My rumors/record-link and explorer completion are not prerequisites for these return destinations. |
| P098-023 | todo | P098-017; P098-018; P098-022; P098-007 | Close the `alpha-independent-participant@v1` delivery record only after all required domain outputs and integrated acceptance pass. Reconcile inventory, dependency graph, owner evidence and Node ledger; retain separate browser/native, accessibility, observed usability and earlier local-primary claims. List all remaining extensions explicitly. Reuse P098-007 results rather than inventing another full test campaign; no release qualification is implied. |

### Acceptance and evidence

The first useful slice is P098-001/002/003/004a/005a under `alpha-local-primary@v1`,
recorded through P098-016/017 with P098-011 tooling. It has a real
start/attention/return path, but is not whole Alpha UI completion and does not require
independent local identities. The final baseline requires P098-001–007, P098-009–012,
P098-014/015 and their upstream outputs, including 004b and the local identity/Messaging
owner tracks. P098-016/017/018/022/023 organize their delivery records; P098-019–021 are
retired in favor of derived report views. P098-023 is the final delivery gate and
consumes P098-007's integrated acceptance. There is no reverse dependency from
implementation/owner tasks to these coordination rows. P098-008/013 and P095-015 are
deferred and outside this closure. Ask or delegate requires both P066 inquiry and one
bounded P073 task (P098-015); My activity/Resume requires the named owner projections
and a real recoverable draft (P098-014). Message someone requires P098-012; Find
material includes the scoped Memarium explorer, and Rumors requires **Browse, Contribute
and My rumors**. This is a bounded target, not every planned Whisper extension. Earlier
delivery may expose a subset, but cannot close the baseline. Deployed profiles may omit
unavailable categories as specified above. Scope reductions need an explicit proposal
amendment, not a green tracker with an unimplemented category excluded.

Use deterministic fixtures for catalog composition, role/identity visibility,
empty/error states and a list exceeding the current eight-item rail. Then exercise
actual owner-backed flows; a clickable prototype or fixture does not prove delivery.
Initial-profile acceptance includes a visible usable people entry, supported
contacts/chat/readiness, early P097 PRG/idempotency and preserved O access while P/Q
receive typed refusal. Test legacy-to-explicit-role migration without implying that
cardinality grants a role after migration. Exercise the ephemeral Resume slot on session
switch/logout/restart and verify absence from durable/browser storage. Contract checks
must cover duplicate/unknown references, invalid activation, changed packages,
unavailable owners, stale permissions, repeated submissions and unknown results. Reuse
the relevant P095 browser/native privacy and lifecycle gates. Include unresolved package
references versus invalid setting keys, single-entry move/hide across layered files,
simultaneous module instances, refused startup and pending activation. For private
home/attention/memory views, exercise identity A/B, key lock, no-JS shell, delayed
response and unavailable owner without private fallback. For Memarium, include
quarantine, forgotten entries, protected owner journals, inaccessible linked targets and
stale index results. These are future implementation gates; this document review has not
executed them. Theme fixtures cover sparse overrides across layers, explicit values
equal to a preset default, preset changes with retained overrides, empty-map inheritance
and source-specific reset. Refuse unknown token/CSS keys, null, CSS expressions/URLs,
out-of-range values and invalid resolved contrast in either palette. Distinguish
preview/save from active consumption and exercise invalid-source startup recovery.
P098-003 qualifies representative parameter combinations, bounds and user zoom in
browser/native rendering; it does not qualify deferred arbitrary CSS. Also cover
identical-byte reinstall with a new admission generation, pure projection fixtures with
no owner I/O, memory cursors with equal recorded times and changed
view/filter/participant, and legacy NULL-owner intake exclusion. Guided-flow checks must
show stable effect identity across review reload/Back/lost reply and invalidation after
edits. Initial HTML canaries and rendered boundary/focus contrast are separate from
owner-side access and palette arithmetic.

Participant-access acceptance uses **operator O and two distinct participants P/Q**,
provisioned through P007-LP-002 owner create/import and activation, not just the
operator opening the user window or three fixture IDs. The initial local-primary slice
records its narrower evidence explicitly. Required independent-profile cases:

- P's session/context cannot be replaced by a body/path/header value, a bare module
  credential or the UI control token. Q cannot use P's view, cursor, record, intake,
  certification, review, publication or result reference. Test scope at every host
  entry, not only through browser controls.
- Memory grants are obtained through P024-013's supported issuance/delivery path;
  missing/unavailable issuer, renewal and revocation have typed recovery/refusal. A
  valid session without a valid grant fails; a valid grant without current view
  membership fails. New participant-view profiles cannot invoke generic unscoped v1
  reads. Existing operator/module v1 behavior retains its documented scope.
- Membership, retention, quarantine or session revocation between list and detail or
  between pages prevents further disclosure. Legacy unbound entries, owner-only journals
  and another participant's intake cannot influence visible counts/snippets. An
  unavailable sidecar or materializer does not permit raw-store fallback.
- A participant intake stays local through edit/redaction; its SQLite rows, Memarium
  stages and retained review/results have consistent ownership and bounded custody.
  Changed candidate/profile/audience invalidates approval. A locked participant key
  cannot cause selection of the operator key or a legacy local-primary author.
- Q's certification or another participant's signed document cannot be paired with P's
  operation. Lost responses preserve the original participant-bound operation and
  require authorized readback; do not repeat effects. Signing, transport delivery and
  disclosure remain independently evidenced.
- Public browsing works without initiating certification. Private fragments remain
  absent from no-JS shells and invalidated DOM; P026 withholding applies to the actual
  participant viewer. Backend isolation and browser/native presentation evidence are
  separate, and existing operator acceptance does not qualify P/Q.

Task-based review asks participants to start an Assistant conversation, submit and
inspect one bounded delegated task, exchange a message through their own route, locate a
retained material through Memarium, resume a retained Whisper draft, handle an attention
item and correct a guided decision. Activity must expose the real owner results and
distinct unknown/expired states. Module restart/re-admission invalidates stale
presentation without deleting retained owner work or replaying an effect; include this
recovery case. Baseline review includes browsing rumors, preparing and explicitly
publishing a reviewed contribution, and finding its authorized result in My rumors, plus
a confirmed record–rumor link. Earlier partial slices identify which outcomes and
upstream gates remain open. Record completion, misnavigation, assistance, recovery and
understanding of the final effect; select the cohort and success criteria before running
the review. Findings can revise copy/grouping without rewriting owner contracts. Do not
fabricate a percentage or generalize a small cohort into proof of universal usability.

Retain separate statements for schema/contract conformance, actual browser runtime,
native runtime, accessibility checks and observed usability. Any incomplete item stays
explicit. Publish the integration map and bounded results alongside the Node
implementation record; this proposal alone changes none of those statuses.
