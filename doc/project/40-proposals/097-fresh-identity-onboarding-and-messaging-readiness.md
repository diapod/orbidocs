# Proposal 097: Fresh-Identity Onboarding and Messaging Readiness

Based on:

- [Challenge 097: Fresh-Identity Messaging Onboarding](../10-challenges/097-fresh-identity-messaging-onboarding.md)
- [Story 010: Message to a Friend](../30-stories/story-010-message-to-a-friend.md)
- [Proposal 024: Capability Passports and Network Ledger Delegation](024-capability-passports-and-network-ledger-delegation.md)
- [Proposal 034: Node Operator Binding](034-node-operator-binding-and-derived-node-assurance.md)
- [Proposal 050: Local Readiness Gate](050-local-readiness-gate.md)
- [Proposal 060: Messaging Middleware](060-messaging-middleware.md)
- [Proposal 076: Federation Identity and Network Selector](076-federation-identity-and-network-selector.md)
- [Solution 006: Capability Binding](../60-solutions/006-capability-binding/006-capability-binding.md)
- [Solution 027: Messaging Middleware](../60-solutions/027-messaging-middleware/027-messaging-middleware.md)

Related:

- [Story 013: qmail Task Pack](../30-stories/story-013-qmail-task-pack.md), for the
  narrow guided-UI profile comparison; this proposal does not qualify its model/VM
  execution or the whole task-pack story.
- [Proposal 026: Resource Opinions and Discussion Surfaces](026-resource-opinions-and-discussion-surfaces.md),
  for the separation of conformance, runtime and regression evidence.

## Status

`draft`

This document records the reviewed repair direction and its proposed implementation
contract. All `MSG-ONB-*` tasks are `todo`. New DTOs, profile discriminators, action
names and request artifacts are proposed, not registered schemas or implemented APIs.
Persisting this proposal does not establish Node implementation, runtime acceptance,
hard-MVP qualification or release readiness.

## Date

`2026-10-12`

## Executive Summary

Repair fresh-identity onboarding without granting sovereign authority automatically.
A passport-issue refusal for an issuer absent from the active federation root is an
authority boundary. A readiness read that treats "no configured blocker" as "ready"
is a separate defect.

The first stage provides a profile-aware, participant-specific evaluator, side-effect
free GET reads, a separate federation issuer fact, explicit operator preparation and
durable setup idempotency. Federation and Messaging steps may be deferred so that
unrelated UI work remains accessible with visible, truthful status.

The second stage introduces execution-time enforcement of local send authority with
an explicit passport/profile migration. The first stage must not silently disable
existing sends through either daemon changes or UI action suppression.

Acceptance keeps three evidence classes separate: contract conformance, actual
delivery between fresh UI identities, and regression of strict Story-010. Existing
Story-010 delivery is an antecedent, not proof of the new onboarding path.

## Context and Problem Statement

### Inspected antecedents and evidence limits

Source review and a bounded local comparison on `2026-10-12` used Node revision
`16223992245f634bc2dedd5aeb266f79124b1885`. These are dated observations, not claims
that the proposed repair is already implemented.

| Fact | Source or retained observation | Consequence |
|---|---|---|
| Fresh UI identities with unlocked keys and active bindings were refused passport issuance because their issuer was absent from the root. Explicit test-root admission and restart let the same identities finish setup. | Identity owner API; `node:daemon/src/identity_host.rs`; `node:daemon/src/lib.rs` | Preserve the authority refusal; improve its presentation and preparation path. |
| Readiness and setup infer send readiness from the absence of a local-gate blocker. A profile with no required local passports can consequently appear prepared without a send passport. | `node:node-ui/src/handlers/user.rs`, `ensure_messaging_send_passport` and `messaging_send_readiness` | Derive readiness from positive evidence selected by the intended operation. |
| The normal outbound path does not currently enforce the local `messaging-send` passport. Existing signer, recipient-consent and transport checks are separate. | `node:daemon/src/endpoint_routes/common.rs`; `node:messaging-service/src/lib.rs` | Adding this check at execution is a behavior change, not merely a read-model fix. |
| `messaging-send` also appears in `inac-push@v1` passports restricted by `peer_node_ids`; `signing/messaging-send` is a signer delegation grant. | `node:daemon/src/peer_handler_tests.rs`; `node:capability/src/delegation.rs` | Capability id alone cannot select local send authority. |
| `first_incomplete_step` requires Messaging completion before `/app`. | `node:node-ui/src/handlers/user.rs` | Truthful readiness and explicit deferral must ship together. |
| `auto_ready_has_current_passport` checks capability, node, selected scope, expiry and locally recorded revocation, but not signature or current-root admission. An absent expected scope matches any scope. | `node:daemon/src/identity_host.rs`; issue-scope construction in `node:daemon/src/lib.rs` | Strengthen and reuse this mechanism rather than copying its current boolean result. |

The strict Story-010 control passed 30 phases, including ordinary and recorded
message delivery without INAC preauthorization. The fresh-identity comparison used
Story-010 and a relocated guided-UI configuration derived from Story-013; it did not
run full Story-013, inference or a VM. It established the issuance refusal and the
readiness gap, not delivery between the fresh UI identities. Demonstration mailbox
items were not delivery evidence.

**Hypothesis:** a diagnostic `messaging-send` lookup returning 404 with
`purpose=messaging` may reflect profile selection rather than absence of an issued
passport. A new selector fixture must establish the exact cause; 404 alone is not
the local-authority predicate.

### Ownership and upstream meaning

Human agency and auditable trust become explicit preparation actions and evidence
at this layer; they do not create a new authority source. P076 owns federation root
admission, issuer semantics, org custody and restart-only activation. P034 owns
operator binding and its consent lifecycle. P024 and Solution 006 own passport
verification. P060 and Solution 027 own Messaging behavior and readiness inputs.
Node UI presents permitted transitions without inferring or creating authority.

This proposal determines the composition and evidence contract across those owners.
It does not rewrite normative authority, root custody, recipient consent or INAC.

## Proposed Model / Decision

### Options considered

| Option | Decision and consequence |
|---|---|
| Keep the current boolean or merely improve the issuance error text | Rejected: missing evidence would still appear ready and execution semantics would remain ambiguous. |
| Automatically admit every fresh identity into the root | Rejected: onboarding would cross P076's authority boundary. |
| Add a separate wizard evaluator or immediately enforce the new read result | Rejected: a second matcher would drift; immediate enforcement would disable unmigrated profiles. |
| Strengthen the existing evaluator, separate authority and deferral, then migrate execution enforcement | Selected: preserve authority and current execution policy while exposing preparation gaps; accept durable coordination and a separately qualified second stage. |

### 1. Two delivery stages

| Stage | Included behavior | Explicit boundary |
|---|---|---|
| A: read and onboarding repair | Exact selection; shared evaluator; truthful GET; federation issuer fact; signed request; deferral; idempotent preparation; fresh-identity delivery acceptance | Existing send execution policy remains in force. Missing preparation is visible, not a new implicit send denial. |
| B: execution enforcement and migration | Profile inventory, migration, observation period, explicit cutover, checks before outbound effects | Requires separate implementation and release qualification under `MSG-ONB-001c`. Stage A completion does not close this stage. |

An empty local-gate requirement list is not evidence of a valid local passport.
The Messaging preparation plan owns which roles and prerequisites it requests.
Omission from a generic gate must not accidentally mark a requested Messaging role
ready or turn it into `not-requested`.

During Stage A, `allowed_actions` follows the actual execution policy. The UI must
distinguish incomplete preparation from a still-available legacy send action; it
must not introduce Stage B by hiding or disabling that action. Existing execution
checks remain effective throughout the transition.

### 2. Passport selection and compatibility

`MSG-ONB-001a` freezes a selection predicate over:

```text
capability + semantic profile + node + resolved caller + operation scope
```

The evaluated subject additionally includes participant identity and role. Evidence
must establish that the selected caller binding, Local Relationship owner and
routing subject belong to that participant; node-wide presence alone is insufficient.

| Meaning | Required distinction |
|---|---|
| Local application send authority | A local send profile and permitted operation/caller scope; not any passport named `messaging-send` |
| Recipient/peer push consent | `inac-push@v1`, including its peer and artifact restrictions; does not grant global local send authority |
| Participant envelope signing | `signing/messaging-send` delegation; evaluated under its own signing contract |

Top-level `capability_profile` and the profile discriminators in `scope.profiles`
are distinct fields; the selector must not conflate them. A local-send discriminator
is to be frozen in 001a, not presumed to exist today.

Existing profile-less local passports need an explicit, bounded compatibility rule
or reissuance. No rule may infer authority from an absent discriminator, a loose
capability-id match or an `issued_by` label. The rule must specify which signed
node/caller/scope evidence identifies an eligible legacy passport and how participant
ownership is established. Ambiguous evidence yields `unknown`, not global permission.
Stage B must document whether each legacy class is retained, reissued or retired.

### 3. Shared evaluator and active-root evidence

Refactor and strengthen `auto_ready_has_current_passport` rather than introducing
an independent wizard matcher. Reuse existing signature, caller-binding, profile and
revocation mechanisms from Capability Binding; extract read-only decision logic
where the existing authorization pipeline also writes caches or audit records.

The evaluator consumes an immutable observation context containing one evaluation
time, the verified active root fingerprint, participant/node/caller, binding and
revocation revisions, passport candidates, relationship/routing facts and service
phases. It returns decisions and evidence without issuing, publishing, unlocking,
starting services, updating root files or writing preparation state.

Required checks include the exact selector, cryptographic signature, validity
interval, revocation and its freshness, live caller binding, and current issuer
authority appropriate to the selected profile. For local issuer passports, the
issuer must still be admitted by the active root. A valid historical signature
alone does not establish current authority. Do not generalize this rule into a
sovereign-root requirement for every participant-issued recipient-consent artifact.

Respect P076's typed participant/org subjects and custody rules. Org custodians
must not become independent sovereign issuers merely because their keys signed a
root pack. A staged replacement root has no runtime effect until verified activation
through restart. Cache keys/invalidation must include active-root digest and relevant
binding/revocation revisions; previous-root decisions cannot survive activation.

At execution in Stage B, reevaluate current authority before effects. An earlier GET
result is explanatory evidence, not a reusable authorization token.

### 4. Proposed read contract: `messaging-readiness.local.v1`

This is a proposed DTO contract, not a new canonical JSON schema in this change.

| Field | Contract |
|---|---|
| `schema` | Constant `messaging-readiness.local.v1` |
| `subject` | Participant id, node id and resolved caller identity |
| `requirements` | Selected preparation profile and plan revision |
| `roles.send`, `roles.receive` | Separate status, reasons and evidence, with participant owner and route association where required |
| `setup/status` | Derived conjunction of the plan's required role/prerequisite evaluations |
| `observed_at` | RFC 3339 evaluation time shared by the observation context |
| `evidence` | Active root federation/version/digest, selected passport ids and profiles, binding id/revision, revocation revision/freshness, relationship owner, routing binding and service/storage phase |
| `allowed_actions` | Server-selected `{rel, method, href}` transitions allowed for this subject under the current policy |

Status is the closed set `ready | blocked | unknown | not-requested`:

1. `ready`: all required predicates have positive current evidence.
2. `blocked`: at least one required predicate has a demonstrated blocker.
3. `unknown`: no demonstrated blocker, but at least one required predicate cannot
   be evaluated with sufficient evidence.
4. `not-requested`: the selected plan explicitly does not request this role or
   Messaging as a whole. It is not a substitute for deferring a blocked request.

The aggregation order is: explicitly unrequested plan -> `not-requested`; otherwise
any required `blocked` -> `blocked`; otherwise any required `unknown` -> `unknown`;
otherwise all required predicates satisfied -> `ready`. An absent or malformed plan
is `unknown`, not an empty successful conjunction. Do not persist a redundant setup
status that can diverge from its inputs.

001a must freeze a closed reason enum and its evidence mapping. Its initial codes
cover `issuer-not-admitted`, `passport-missing`, `passport-ineligible`,
`passport-signature-invalid`, `passport-expired`, `passport-revoked`,
`revocation-state-unavailable`, `binding-missing`, `binding-inactive`,
`participant-owner-mismatch`, `route-missing`, `service-not-ready`,
`storage-not-ready`, `contactability-not-ready`, `key-locked`, `root-unavailable`
and `observation-failed`. Human-readable detail does not create additional reason
codes. The enum must distinguish a known blocker from unavailable evidence.

`allowed_actions` supplies such transitions as defer, resume, request admission or
prepare, when currently permitted. These names are candidates for 001a. UI clients
must not reconstruct them from status alone. Mutating endpoints independently
revalidate their authorization; presenting an action is not an authorization grant.

### 5. Federation issuer fact and deferred onboarding

Add `federation_issuer_status` to `WelcomeReadiness` as a separate fact/step following
the Node UI README's "Adding a Wizard Step" pattern. Its result identifies the
evaluated participant, active root and relevant issuer role; admission and local key
availability are distinguishable inputs. Messaging and future passport-issuing
features consume this fact. P076 remains its semantic owner.

Store an explicit onboarding disposition, keyed by participant and plan revision,
separately from evaluated authority and readiness. Deferring Messaging or federation
preparation permits entry to `/app` after the other required identity/key/binding
steps. It does not set Messaging complete, modify root trust or invent a passport.
The app retains the blocked/unknown status, evidence and a resume action across
navigation and restart. A changed plan requires an explicit disposition policy.

A narrow Story-013-derived profile can therefore remain usable without claiming
Messaging readiness. The preparation gap is visible; unrelated work is not gated by
it. Another participant cannot inherit either readiness or a deferral decision.

### 6. Signed, non-authoritative issuer-admission request

Use a participant-signed request in the separate domain
`orbiplex.federation.issuer-admission-request.v1`. Freeze canonical encoding and
signature verification in 002 using existing signing primitives. The signing path
for this request must be narrowly permitted without granting passport-issue authority
or widening the general signer allowlist.

The signed payload binds participant id/key reference, node id, federation id,
intended operator audience, requested role/purpose, base root version/digest,
`issued_at`, `expires_at` and an unpredictable nonce. It contains no private keys,
unlock phrases, recovery material or other secrets. Verify identifier/key agreement,
signature/domain, audience, node/federation, expiry and replay before processing an
operator decision; root changes require renewed review of the request's context.

The signature proves key possession and the content of the request. It does not
prove eligibility or grant authority. The operator's explicit decision and P076
root procedure remain separate, including signed higher-version activation through
restart. A request must clearly disclose the requested role; ordinary Messaging
intent must not silently become a request for sovereign status.

Requests may be deferred or declined. Limited grants to ordinary participants are
an unresolved P076 policy, not a new issuance shortcut in this proposal.

### 7. Idempotent preparation and auto-ready convergence

The daemon owns a durable coordinator shared by wizard setup and configured
auto-ready. Its canonical issuance intent includes node, participant, capability,
profile, scope digest and plan revision. A caller idempotency key is bound to that
intent; reuse with different input is rejected. Equivalent issuance slots are
serialized/deduplicated even when two callers supply different request keys.

Persist intent/result association with passport issuance and define recovery of an
interrupted write. Concurrent POSTs and restart/retry return the same issued passport
for the same successful intent. Partial preparation resumes remaining steps without
duplicating completed issuance or publication. This is not a distributed transaction
across all services.

An old receipt is historical evidence, not proof that its passport is still usable.
Expiry, revocation or changed root are reevaluated. A new authorized preparation
requires a new plan revision where appropriate; a retry must not resurrect withdrawn
consent or override binding revocation.

Auto-ready keeps its existing explicit configuration and participant/key constraints.
It uses the same evaluator and coordinator for configured prerequisites, preserves
withdrawn binding history, and never performs issuer admission. Its role is a bounded
route to the same evaluated preparation state, not an alternative trust policy.

### Implementation Recommendations

- Keep the evaluator in the owning host/domain layer; UI and daemon auto-ready are
  consumers of its typed result. Pass snapshots and time explicitly so GET remains
  observational and conformance fixtures do not need live service preparation.
- Reuse capability verification primitives and signer domains. Do not call a
  mutating authorization/preparation workflow from a readiness GET.
- Replace the wizard's Messaging-only completion gate with explicit disposition
  handling in the same Stage A change. Add the separate issuer fact consistently
  to DTOs, step selection, templates and tests.
- Place issuance serialization/idempotency at the daemon owner boundary. A lock in
  one UI process does not cover another tab, auto-ready or another client.
- Preserve the separation between local send authority, recipient receive consent,
  INAC transport permission and participant signing delegation in diagnostics.
- For Stage B, inventory each installed profile and legacy passport class, publish
  migration/cutover rules, and migrate through an already authorized issuer. An
  observation period must not weaken current checks. Check authorization before
  enqueueing and before delayed outbound effects; define the disposition of queued
  messages when authority changes. No automatic sovereign promotion is a migration.
- Update contracts, schema mirrors, ledgers and capability documentation in their
  later implementation tasks. Do not mark this proposal's candidate DTO/profile as
  currently registered or qualify all of P060/P076 from one acceptance result.

### Acceptance Criteria

#### Evidence classes and closure rules

| Class | Required evidence | What it does not establish |
|---|---|---|
| Conformance | Deterministic selector, trust, aggregation, request and concurrency fixtures with exact assertions | Fresh UI identities actually delivering a message |
| Runtime | Fresh UI identities, explicit authority/consent transitions, setup and delivered content correlated with UI/storage evidence | Full Story-013 model/VM qualification or Stage B enforcement |
| Regression | Separate strict Story-010 report, without INAC preauthorization | Delivery through the newly created identities |

All records identify source revisions, run/profile, stage and execution policy,
subject ids, plan revision, active root fingerprint and observation times. Retained
reports contain references/digests, never secrets. Conformance or control delivery
must not substitute for the new runtime path.

#### Stage A: fresh UI identities and delivery

1. Start isolated Node A/B profiles with separate storage and host-only UI sessions
   at `a.localhost` and `b.localhost`. Verify loopback resolution and endpoint/callback
   configuration. Different ports on one hostname are insufficient cookie isolation;
   cookies must not have a shared parent-domain scope. Assert sessions do not cross.
2. Create both identities and protected keys through the real UI. Complete the
   required key/binding steps. Before issuer admission, demonstrate the issuance
   refusal and corresponding status without root mutation or automatic promotion.
3. Defer the blocked steps, enter `/app`, and retain visible status/resume actions
   across restart. Repeat with the narrow Story-013-derived guided profile.
4. Submit and verify signed admission requests. Explicitly approve the required
   issuer roles through the isolated test federation's P076 procedure, activate a
   higher-version signed root by restart, and preserve anti-rollback state. This
   fixture admission is operator-owned test setup, not a normal-user privilege policy.
5. Prepare the requested Messaging roles using the shared evaluator/coordinator.
   Verify selected passports, caller binding, participant owner, route, storage,
   contactability and service phase. Compare wizard and configured auto-ready paths
   under equivalent plans; auto-ready must not grant admission or renew consent.
6. On B, compose and send a unique message to A through the actual UI, using the
   normal discovery, operator INAC approval and recipient contact-consent path.
   Open the actual received message in A's UI. Retain one evidence bundle linking
   the same `message/id` in the sender UI, B outbox and A mailbox/UI, recipient route,
   delivered state and digest of the canonical message content. Demonstration inbox
   entries, counters or an unrelated control message do not satisfy this criterion.
7. Retain the independent strict Story-010 regression result. In Stage A, verify
   that truthful readiness did not introduce new send enforcement on legacy/narrow
   profiles. Preserve existing execution checks and classify that compatibility
   behavior explicitly instead of treating it as prepared local send authority.

This acceptance needs no inference or VM. If a launcher requires model metadata,
use an explicit resolved per-run metadata directory without downloading weights;
reject unresolved `{slot}` paths. Model root and VM location remain distinct
settings even when they share a volume. A guided-UI clone must relocate every mutable
storage path; this is not permission to run or qualify full Story-013.

#### Required negative and recovery cases

| Case | Required assertion |
|---|---|
| Empty generic local-gate passport list | A requested Messaging role cannot become ready from absence of a blocker. |
| Per-peer `inac-push@v1` passport only | It does not satisfy local send authority; signer delegation alone does not satisfy it either. |
| Invalid signature, expiry, revocation, wrong node/caller/scope | Exact affected predicate is refused with typed reason and evidence. |
| Root removes a previously admitted issuer | After verified higher-version activation and restart, the still-cryptographically-valid passport no longer counts as current; root digest changes and old decisions are invalidated. Stage A proves readiness refusal; Stage B separately proves execution refusal. |
| Missing root/revocation/service observation | The appropriate predicate is `unknown`, never inferred ready; GET does not prepare missing state. |
| Second local participant | Another participant's binding, relationship owner, route or deferral does not satisfy this participant's readiness. This does not claim complete multi-participant service support. |
| Narrow profile with operator-required preparation | Explicit deferral reaches `/app` with truthful visible status, including after restart. |
| Two concurrent setup POSTs | Same intent yields one passport/result; different request keys cannot duplicate the same issuance slot. Same key/different input is rejected. |
| Crash/retry and expired/revoked prior result | Durable retry resumes without duplicate issuance; historical success does not imply current readiness or renew withdrawn consent. |
| Tampered request participant/node/federation/role | Signature/context verification rejects it before an authoritative operator action. |
| Expired or replayed admission request | Refused or recognized as the same already processed request; no second admission action. |
| Repeated readiness GET | No issuance, publication, key unlock, service start, root update or preparation-state write. |

#### Stage B: separate enforcement acceptance

`MSG-ONB-001c` requires a pinned profile inventory and migration report, preserved
recipient/INAC/signing controls, and explicit execution-policy cutover. It must
demonstrate refusal before outbound effects for absent or ineligible local send
authority, issuer removal, revocation and changed owner/caller. Include authority
changes after observation and while a message waits in the queue; the GET decision
must not authorize later dispatch. Migrated fresh and legacy profiles must still
complete actual delivery and strict Story-010 regression. These results are separate
from Stage A and cannot be inferred from its readiness assertions.

## Trade-offs

Truthful status exposes profile gaps previously hidden by a successful boolean.
Deferral keeps unrelated work accessible while making the incomplete preparation
visible. Shared evaluation reduces drift between wizard and auto-ready but requires
precise selection and profile-dependent trust rather than one generic id check.

Evidence-rich reads improve diagnosis of "ready earlier, blocked later" without
making snapshots durable grants. Idempotency requires durable coordination and
recovery semantics, but avoids hidden races between independent preparation clients.
Staged enforcement preserves existing behavior temporarily and makes the migration
cost explicit; Stage A must not be described as full send-authority enforcement.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
|---|---|
| Creating an identity or binding silently grants issuer authority | Separate issuer fact, non-authoritative signed request and explicit P076 decision. |
| Correct read traps users in the wizard | Ship truthful status and durable explicit deferral together. |
| A boolean hides missing evidence | Closed statuses/reasons, positive predicates and derived setup status. |
| A peer consent or signer grant becomes global send permission | Exact profile/caller/scope selector and negative fixtures. |
| Root rotation leaves a cached ready decision | Active-root evidence and cache invalidation; use current trust at evaluation/execution. |
| GET creates prerequisites while observing them | Pure evaluator over read snapshots and assertions against domain writes. |
| Auto-ready and wizard issue conflicting artifacts | Same plan/evaluator and durable owner-side issuance coordinator. |
| A replay or altered request changes admission | Signed context, nonce/expiry, replay records and separately authorized operator action. |
| Stage A silently enforces Stage B through UI | Allowed actions reflect current execution policy; narrow/legacy regression assertions. |
| Strict control delivery is reported as fresh-identity delivery | Separate evidence classes and one correlated message/content bundle for the new path. |

## Open Questions

1. **Limited grants for ordinary participants:** P076 owns the issuer/delegation
   policy that enables restricted capabilities without sovereign admission. See
   [P076's open question](076-federation-identity-and-network-selector.md#open-questions).
   This proposal does not resolve it through the current issue API.
2. **Concrete local-send profile and legacy selection:** 001a must freeze the
   discriminator, operation scope and bounded compatibility classes before evaluator
   implementation. Ambiguous old passports are not silently global grants.
3. **Enforcement migration/cutover:** 001c must choose explicit release/configuration
   scope, migration assistance and queued-message handling from a retained inventory.
   Stage A does not settle an enforcement default or release date.

## Next Actions

### Implementation Tracker

Stable task ids preserve the reviewed `MSG-ONB-*` workstream. All rows remain `todo`;
this documentation change does not close implementation or acceptance tasks.

| Task | Stage | Depends on | Status | Completion gate |
|---|---|---|---|---|
| MSG-ONB-001a | A | – | todo | Freeze exact selector, local-send profile/legacy classes, participant/role evidence, `messaging-readiness.local.v1`, aggregation, closed reasons and allowed actions; retain selection/conformance fixtures. |
| MSG-ONB-001b | A | MSG-ONB-001a | todo | Strengthen/refactor the existing evaluator with signature, active-root/profile authority, revocation, owner/caller and pinned evidence; reuse read-only verification; invalidate decisions across root/binding changes. |
| MSG-ONB-002 | A | MSG-ONB-001a, MSG-ONB-001b | todo | Add separate issuer fact/step, signed request verification, explicit operator handoff and durable deferred Messaging/federation steps; retain `/app` status without automatic admission or false completion. |
| MSG-ONB-003 | A | MSG-ONB-001a, MSG-ONB-001b | todo | Shared daemon preparation coordinator for wizard/auto-ready, durable intent/result idempotency, concurrent/crash recovery and preserved withdrawn-consent behavior. |
| MSG-ONB-004 | A | MSG-ONB-001a, MSG-ONB-001b, MSG-ONB-002, MSG-ONB-003 | todo | Retain all Stage A conformance/negative cases, fresh-UI-identity message/content evidence and separate strict Story-010 regression; document legacy execution compatibility and the narrow-profile deferral result. |
| MSG-ONB-001c | B | MSG-ONB-004 | todo | Separate announced enforcement change: inventory, explicit migration, observation/cutover policy, execution rechecks and queued-message disposition; retain Stage B refusal/delivery/regression evidence before release qualification. |

Start with 001a. Implement 001b, then the onboarding and preparation work; qualify
Stage A as a coherent slice so truthful reads never ship with the old mandatory
Messaging gate. Stage B follows a separately reviewed migration/cutover plan. Resolve
P076's limited-grant question before claiming support for ordinary non-sovereign users
through a new authority path.
