# P026-012a: production assessment viewer grants

Status: accepted design (2026-10-24); bounded P026-012a implementation and qualification complete (2026-10-25). Parent 012/P073 remain partial and 012b remains todo.
Based on: [P026 §6 and tracker](026-resource-opinions-and-discussion-surfaces.md), P066 operator consent, P073 consumer boundaries and P080 authenticated ChannelJson sessions.

## Executive Summary

012a grants a ChannelJson module bounded read access as its own local operator. 012b separately owns Agent consumer binding and final inference admission. Human control, private disclosure facts and knowledge symmetry are preserved through the existing admit → expose → render pipeline.

## Context and Problem Statement

Q-02 qualified a harness-bound viewer, not production provisioning. Global CallerBinding remains module:*; sharing a passport key does not identify the represented participant. A module cannot grant itself participant authority.

## Decision

Only authenticated ChannelJson host-capability.invoke may use the projection. Capture executor, module, component, launch, session and epoch before scheduling the worker; compare the captured session against ChannelSessionRegistry at admission and final handoff. Never recover the originating generation from a current module label. Same-launch reconnect may retain the activation; old-session requests refuse. Module HTTP and Agent cannot borrow this authority.

P066 owns proposal, decision, allow-once consumption and revoke. The question reference is stable; an approval reference is scope-specific and may change on deny or timeout. Pending projections follow the stable question, not an assumed permanent pending approval reference. Identity host holds only a bounded RAM projection, keyed by daemon boot/executor/module/launch, with immutable intent digest and current consent/binding witnesses. Consumption and decision commit before publication. No archive activation, additional durable registry or activation endpoint exists. Daemon restart clears projections; boot identity prevents historical recovery. Module restart requires an operator-initiated new proposal. Duplicate proposals merge; no automatic questions on restart.

Scope is agora.assessment.read for 1–32 explicit ResourceRef values, without wildcard/prefix semantics or exposure transitions. One active grant per module/launch; at most 32 active grants per node. Pending uses P066's existing limit. TTL at proposal: 60–3600 seconds, default 900, capped by exact local operator binding validity. Retry and approval do not move deadlines. The P066 question expires within 300 seconds and before the grant; after activation its question deadline does not truncate the grant.

Host-local identity.assessment-viewer.request and revoke require local operator control; list gives the operator pages of 32 and a channel module only its own status, scope and deadline, without handles or counters. All three are hidden from Agent catalog and denied by Agent dispatch. Read input remains subject alone. Launch aliases use domain-separated HMAC under a random per-boot secret; token values and plain token hashes never enter intent or caller context.

Consent uses deny and allow-once for one activation. The question states: the module can read your admitted own assessments; after disclosure also admitted peer assessments; it may retain content; revocation cannot undo knowledge. Existing operator UI authentication and CSRF apply. Wrong operator, timeout, modified intent and module self-answer refuse.

For one coherent now=(UTC, monotonic) sample, require monotonic < deadline, UTC < deadline, monotonic >= proposal, and UTC elapsed >= monotonic elapsed − 2 seconds, using checked arithmetic. Tolerance is relative to proposal, not refreshed. Final handoff samples again after I/O. Observed expiration or invalid time is terminal, persisted by P066 revoke. No physical-clock or hostile-OS guarantee is claimed.

Each activation admits 30 attempts per rolling 60 seconds, at most one in flight, atomically before Agora. The next attempt receives 429 and retry guidance without an Agora call. An admitted attempt is charged even on backend failure. Replay never resets the budget. Operator RAM statistics count admitted attempts and last attempt time independently of result, withholding or peer cardinality. Retain active entries plus the last 128 terminal summaries; unavailable statistics are not zero. No resource-read list or durable read journal is added.

## Trade-offs

Each process restart requires fresh operator approval; crash loops create no automatic prompts. One-node acceptance uses an actual SDK consumer application, not a product-module integration. Foreign signed fixtures traverse real admission but do not qualify replication.

## Failure Modes and Mitigations

Consent, binding, session, launch, scope, time and budget admission precede Agora and are checked again before handoff. Revoke changes P066 authority epochs. Failed persistence refuses activation or continued use. Already admitted disclosure may have occurred; private exposure facts survive revoke, re-grant and projection rebuild. Agent observation/inference remains unchanged until 012b.

## Open Questions

No contract decision blocks 012a. Positive P073 consumer semantics and supervised-restart reconfirmation belong to future work.

## Acceptance and Next Actions

Freeze contracts first, implement, obtain clean acceptance, then update measured status. One ordinary daemon must have pinned Cargo features excluding assessment-exposure-acceptance. The application itself sends channel calls; the harness never reads or uses its token. Exercise browser consent/revoke, refusal/timeout/wrong actor/CSRF/modified intent, stale module/launch/session including a queued pre-restart request, exact scope, transition refusal, byte-identical withheld privacy, 31st attempt and concurrency, rolling reset without lease extension, actual expiry, revoke, module/daemon restart, replay and durable exposure rebuild. Component evidence separately covers paired clocks, delayed I/O and persistence failures. Agent operations remain hidden and denied. Qualifier binds proposal → P066 decision → consumption → session → result → usage/lifecycle; removing/substituting each link must refuse normally, under Python -O and after extraction. Label foreign records signed-fixture-input. Preserve historical Q-02 evidence. Parent 012 and P073 remain partial until separate 012b qualification.

### Measured checkpoint (2026-10-25)

Run 06 at clean Node e726624c / Orbidocs 2e73ed3a qualifies eight ordinary-daemon/application/browser cases, empty Cargo feature sets, actual SDK-originated calls and source/image agreement after cleanup. Component checks at Node 5d6200a1 separately cover authenticated queued origin, wrong actor/modified intent, persistence faults, paired clocks and concurrency; these are not forced-queue or independent query-meter measurements in the ordinary process. Current normal/-O and loose/extracted qualification agrees, with 59 negative controls per location. See `node:docs/evidence/agent-runtime/2026-10-24-p026-012a/README.md`. The bounded 012a tracker closes; product-module/replication, physical clock/power loss, positive Agent consumer and release qualification remain outside this result. Historical Q-02 is unchanged.

### Critical-review clarification (2026-10-25)

Observed terminal time loss retires the boot-local projection before fallible P066 reads/revoke writes; a later clock correction or archive replay cannot reactivate it. Activation rechecks fresh paired time after durable consumption and all blocking identity/registry reads. Module status also validates the current operator, originating session and fresh time at handoff, without charging a read attempt. A failed durable revoke may require operator retry, but never reconstructs an active projection. These are enforcement details of the accepted semantics, not new authority. The historical checkpoint above remains unchanged; review qualification is recorded separately in Node.
