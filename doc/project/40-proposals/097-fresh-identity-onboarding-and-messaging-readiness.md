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

This document records the reviewed repair direction. Stage A is implemented in
Node and qualified by separate conformance, fresh-identity runtime and strict
Story-010 regression evidence dated `2026-10-12`. Its DTO schemas are canonical and
mirrored in Node. Stage B is implemented and locally qualified by separately
pinned conformance, fresh-identity runtime and strict Story-010 measurements dated
`2026-10-13`. The tracker records this bounded completion. The proposal's `draft`
status, broader component implementation and release qualification remain separate.

Retained evidence: `node:docs/evidence/messaging-onboarding/README.md`.
Implementation contract: `node:docs/development/MESSAGING-ONBOARDING.md`.

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

The second stage always enforces typed local send authority. Generated profiles
are corrected; existing identities use explicit preparation or renewal. There is
no observation mode, legacy cohort, migration API or cutover. Lack of backward
compatibility is a deliberate decision before the first release. Migration after
release would be a new problem. Dated Stage A compatibility evidence stays historical.

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

The pre-repair strict Story-010 control passed 30 phases, including ordinary and recorded
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
| A second wizard matcher or a permanent observation mode | Rejected: matchers drift and observation can indefinitely leave authority unenforced. |
| Shared evaluator, explicit authority/deferral and always-enforced typed send | Selected: explicit preparation fixes generated and long-lived development profiles; qualify delayed effects separately. |

### 1. Two delivery stages

| Stage | Included behavior | Explicit boundary |
|---|---|---|
| A: read and onboarding repair | Exact selection; shared evaluator; truthful GET; federation issuer fact; signed request; deferral; idempotent preparation; fresh-identity delivery acceptance | Existing send execution policy remains in force. Missing preparation is visible, not a new implicit send denial. |
| B: execution enforcement | Typed send authorization before admission and delayed effects, durable provenance, explicit retry and bounded retention | Separate conformance, fresh-identity runtime and strict Story-010 measurements under `MSG-ONB-001c-01` through `04`; no migration/cutover mode. |

An empty local-gate requirement list is not evidence of a valid local passport.
The Messaging preparation plan owns which roles and prerequisites it requests.
Omission from a generic gate must not accidentally mark a requested Messaging role
ready or turn it into `not-requested`.

The dated Stage A reports retain the then-current compatibility policy. Stage B
uses execution authority to select `compose`; legacy execution is no longer an
allowed path. Readiness and explicit deferral remain independent of unrelated UI
work, while existing recipient, INAC and signing checks remain in force.

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
is now frozen by 001a as `messaging-local-send@v1`. Its typed scope contains
`participant_id` and purposes `["messaging"]`, with exactly one profile and an
exact caller kind/label/subject key. Top-level `capability_profile` must be absent.
Scope extras are limited to `capability_id`, `module_id` and `issued_by`; the last
field is descriptive. Stage A's bounded profile-less class is historical. Stage B
accepts only `messaging-local-send@v1`; profile-less or legacy artifacts produce
`passport-profile-unsupported`, and readiness offers explicit `prepare`. INAC push
and signer delegation never substitute for local authority. Ambiguous scopes are
ineligible. Local receive retains `messaging-receive@v1`, `wizard-local-route`,
wildcard senders, purpose `messaging` and the exact owned route/grant; this does not
redefine pairwise recipient consent.

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

Stage A uses the same composite revocation view for observation, auto-ready and
receipt retry. Its local read budget is 300 seconds after `checked_at`; absent,
future or older views cannot establish non-revocation. Known passport and delegated-key
target revocations remain decisive when stale. Evidence hashes both sorted sets.
Binding revision hashes include lifecycle withdrawal; this is a preparation read
policy and does not introduce Stage B execution enforcement.

Respect P076's typed participant/org subjects and custody rules. Org custodians
must not become independent sovereign issuers merely because their keys signed a
root pack. A staged replacement root has no runtime effect until verified activation
through restart. Cache keys/invalidation must include active-root digest and relevant
binding/revocation revisions; previous-root decisions cannot survive activation.

At execution in Stage B, reevaluate current authority before effects. An earlier GET
result is explanatory evidence, not a reusable authorization token.

### 4. Current read contract: `messaging-readiness.local.v2`

The canonical [readiness schema](../../schemas/messaging-readiness.local.v2.schema.json)
freezes this DTO. Related contracts are
[preparation](../../schemas/capability-passport-preparation.local.v1.schema.json),
[disposition](../../schemas/messaging-onboarding-disposition.local.v1.schema.json),
[request creation](../../schemas/issuer-admission-request-create.local.v1.schema.json)
and [signed request](../../schemas/issuer-admission-request.v1.schema.json).

| Field | Contract |
|---|---|
| `schema` | Constant `messaging-readiness.local.v2` |
| `federation_issuer_status` | Sovereign membership only; a limited grant does not make this ready |
| `issuance_authority_status`, `issuance_authority_kind` | Usable bounded or sovereign issuance, with a closed `sovereign | delegated | none` kind |
| `roles.receive.receive/role-prepared`, `roles.receive.receive/open-consent` | Separate local role and any-sender consent facets, with identical meaning on both paths |
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

001a freezes a closed reason enum and its evidence mapping. Its codes
cover `issuer-not-admitted`, `passport-missing`, `passport-ineligible`,
`passport-signature-invalid`, `passport-expired`, `passport-revoked`,
`revocation-state-unavailable`, `binding-missing`, `binding-inactive`,
`participant-owner-mismatch`, `route-missing`, `service-not-ready`,
`storage-not-ready`, `contactability-not-ready`, `key-locked`, `root-unavailable`
and `observation-failed`. Stage B adds `passport-profile-unsupported`,
`revocation-view-stale`, `guard-unavailable` and `unattributed-entry` to the same
protocol enum used by HTTP, readiness, AD and outbox. Human-readable detail does not create additional reason
codes. The enum must distinguish a known blocker from unavailable evidence.

`allowed_actions` supplies such transitions as defer, resume, request admission or
prepare and compose, when currently permitted by the execution evaluator. The fixed relations are
`defer`, `resume`, `request-admission`, `prepare` and `compose`. UI clients
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
signature verification in 002 using existing signing primitives. The implemented
encoding is canonical JSON with `signature` omitted, preceded by the UTF-8 domain
and one NUL byte. Request expiry is bounded to 15 minutes; review retains at most
1024 public requests and refuses nonce replay. Review records are non-authoritative. The signing path
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

Named local routing-subject selection and creation are also serialized at the daemon
identity owner. Two fresh UI setup jobs must converge on the same owned route before
forming the receive-passport intent. UI POST returns before background setup ends;
acceptance waits for both terminal audit records and verifies one receive passport.

The coordinator stores intent/result association in the same private atomic artifact
as passport issuance, before installation. The intent also includes relative expiry;
keys are participant-scoped, bounded to 128 bytes and retained up to 64 per intent.
Wizard and equivalent local-send auto-ready preparation use a 90-day expiry. A
prepared record cannot be deleted through the normal artifact API, but can be revoked.
Process-crash recovery is qualified after the durable artifact appears and before
the client consumes the response; power loss and directory fsync remain outside this
qualification. Concurrent POSTs and restart/retry return the same issued passport
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
- Stage B uses explicit participant/caller/route inputs and host-owned provenance.
  Check authority before admission and every delayed protected effect; no earlier
  read or successful attempt becomes a reusable grant. Missing guard fails closed.
- Update contracts, schema mirrors, ledgers and capability documentation in their
  later implementation tasks. Do not mark this proposal's candidate DTO/profile as
  currently registered or qualify all of P060/P076 from one acceptance result.

### Acceptance Criteria

#### Evidence classes and closure rules

| Class | Required evidence | What it does not establish |
|---|---|---|
| Conformance | Deterministic selector, trust, aggregation, request and concurrency fixtures with exact assertions | Fresh UI identities actually delivering a message |
| Runtime | Fresh UI identities, explicit authority/consent transitions, setup and delivered content correlated with UI/storage evidence | Full Story-013 model/VM qualification; dated Stage A runs alone do not establish Stage B enforcement |
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
   Load `/middleware/messaging` with a fresh pseudonymous draft before attestation;
   absent/null optional attestation objects must render `draft` and blank fields
   without changing readiness or authority.
7. Retain the independent strict Story-010 regression result. In Stage A, verify
   that truthful readiness did not introduce new send enforcement on legacy/narrow
   profiles. Preserve existing execution checks and classify that compatibility
   behavior explicitly instead of treating it as prepared local send authority.

This acceptance needs no inference or VM. If a launcher requires model metadata,
use an explicit resolved per-run metadata directory without downloading weights;
reject unresolved `{slot}` paths. Model root and VM location remain distinct
settings even when they share a volume. A guided-UI clone must relocate every mutable
storage path; this is not permission to run or qualify full Story-013.

For a cloned guided profile, assert empty contact/relationship stores and
accepted-request receipts as well as transport/outbox/mailbox histories. Retained
contact/recovery state can restore an earlier consent or trigger reciprocal
auto-accept; such a case does not prove a new explicit consent transition.
Reusing already approved identities must be reported separately from new UI
identity creation and issuer admission.

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

#### Stage B: execution contract

The evaluator is `evaluate(participant, caller, route, now)` over immutable facts.
The host resolves actual caller and route ownership; client declarations establish
neither. Current policy covers the local operator, but the evaluator's input is not
hard-coded to that role. Do not extend the accepted issuer policy.

Local issuer lifecycle ownership selects the authoritative local revocation store,
with no directory freshness budget. `issued_by` and artifact location do not prove
locality. Remote verified observations have a 300-second budget; known revocations
remain decisive when stale. Missing observations or a guard produce HTTP 503;
proven refusals produce 403. AD carries the shared reason in a structured field.

A bounded 1024-entry cache keys participant, node, caller, route/owner, passport and
active-root digests and binding/revocation revisions. Passport/binding intervals,
current key availability and remote observation age are checked on every use.
Staged roots have no effect; verified activation by restart changes the root digest.
`POST /v1/host/capabilities/messaging.send.authorize` returns reasons, time and
evidence without issuance or durable authorization. Provenance observations require a
non-null `body/digest`; the profile-only observation arm has no message content.
Recipient `inac-push@v1` passports are excluded before local candidate diagnostics;
only missing local authority yields `passport-missing`. Issuer admission is checked
against the selected passport's actual issuer without expanding today's self-issued
policy. Runtime callers are resolved from the authenticated request binding.

The host publishes immutable binding/passport snapshots and their digests/revisions
at its serialized write boundary. Draft changes atomically publish their file and
memory snapshot. Revocation revision and facts come from one authoritative-source
observation. Peer execution reuses these snapshots and a bounded provenance cache;
it does not reread the whole issued-artifact directory on each frame. Out-of-band
profile-file changes become active after restart.

Explicit setup creates a new preparation generation after expiry or unsupported
profile. An old idempotency key retains its old result; concurrent new keys share
one current issuance slot. Wizard and auto-ready share selector/coordinator. GET,
auto-ready, unlock and retry never renew historical intent or withdrawn consent.

Admission precedes EML, outbox, signing and outgoing contact requests. Send authority
does not depend on whole setup readiness or the sender's receive role. The daemon
persists immutable `message/id`, participant/node, resolved caller, route/owner,
creation time and intent/content digests. Outbox, AD and peer transport retain only
references to that provenance. The provenance proves origin, never future authority.
One provenance reference owns one outbox row, enforced by a unique index. A duplicate
adoption returns its original receipt without rewriting EML or appending an enqueue
event. A different envelope cannot claim the same provenance.

The module-only `messaging.send.provenance.sync` port reconciles already-committed
outbox adoption and terminal facts. Response loss/restart replays that reconciliation.
Operational `intents` and their `artifacts` expire 30 days after `delivered`,
`expired-unsent` or `discarded-unsent`; outbox audit facts and recordings remain.
Unadopted intents expire after 60 minutes. Sweep only after pending outbox facts have
been reconciled; unavailable reconciliation retains the proof and does not prevent
fail-closed execution checks. Each transactional sweep removes at most 256 intents
and their artifacts together and invalidates their cached observations.

AD's daemon-independent guard statically protects `message-envelope.v1` and outbound
`contact-request.v1`. Admission, retry and actual adapter effects validate current
authority, class, provenance and digest, including referenced artifacts and indirect
adapters. Each protected peer frame is checked before emission; refusal does not
disconnect the peer. Missing guard is `guard-unavailable`.

A started transfer does not grant permission for subsequent protected INAC chunks:
the built-in adapter attaches artifact identity and provenance to every chunk, so
revocation stops the next unsent chunk. Already emitted bytes cannot be recalled;
partial bytes alone do not establish completed message delivery. A previously shared
`artifact-object-pointer.v1` has a different boundary: fetching its object consumes
the separately issued, expiring, one-use fetch grant. Revoking local send authority
blocks new protected publication, but does not retroactively revoke that fetch grant.

A refused existing intent becomes `authority-blocked` with reason/evidence. AD ends
the attempt as `OutboundDenied`, without automatic retry. Restart, replay/reindex,
unlock and auto-ready preserve the pause. Unattributed old entries get
`unattributed-entry`; explicit discard or resending content as a new ID are the only
paths forward. Never infer the historical sender from the current operator.

Single retry and participant `POST /v1/messaging/outbox/retry-blocked` reevaluate each
intent. Bulk operations durably pin their selection and operation key; each intent
has its own persisted attempt generation/idempotency key. Concurrent requests do
not duplicate attempts; unresolved previous AD outcomes must be resolved first.
A completed contact-request AD without a receive passport is not completed message
delivery; explicit retry returns to waiting for recipient consent. Completed bulk
operation receipts expire 30 days after all selected items have durable results.
Incomplete operations remain recoverable; the 4096-operation bound is a temporary
capacity refusal, with completed history reclaimed transactionally before admission.
Reusing a key after that window starts a new operation.
Retention bounds paused entries to 256 per participant, 1024 per node, and 30 days
from creation. Unattributed entries count at node level. Oldest entries, ordered by
creation and then ID, terminate as `expired-unsent`. Commit terminal evidence before
deleting transport copies; repeat cleanup after crashes. Audit metadata and separate
recordings survive; replay and EML recovery cannot resurrect a terminal result.

Operator `GET /v1/identity/messaging-send-audit` evaluates profiles and unsent intents
with the same evaluator, pages at most 100 records, omits content and performs no
durable write. It is a one-shot diagnostic, never an observation mode.

Review regression gates also cover orphan/terminal provenance cleanup and cache
invalidation, transactional cleanup failure/restart, a full 4096-operation history,
concurrent 1:1 adoption, a mismatched evaluator caller, recipient-push-only readiness,
required content digest, generated stream-chunk revocation and pointer-fetch grant
independence. Keep these measurements source-bound and separately dated from the
original Stage B qualification.

#### Stage B: separate acceptance measurements

| Class / case | Required assertion |
|---|---|
| Conformance | Typed selection and one reason enum; legacy, INAC and signer grants fail; invalid signature, expiry, revocation, node/caller/owner fail; cache invalidates by facts and expires without revision changes. |
| Execution boundaries | Controlled barriers change authority after GET, admission, AD waiting and peer enqueue. No protected effect follows refusal. |
| Missing guard / provenance | Protected AD classes fail `guard-unavailable`; missing/substituted provenance and referenced classes cannot bypass direct or indirect adapters. |
| Seed Directory offline | Discover route and obtain ordinary consents, then disable only directory access for more than 300 seconds. Show stale remote observation and actual delivery with locally issued authority. |
| Renewal / retry | Parallel setup after expiry or unsupported profile yields one typed passport; single and bulk explicit retries deliver without duplicates. |
| Durability | Unattributed entries, restart/crash, unlock, replay/reindex, count/age bounds and crash between terminal commit and file deletion preserve authority and terminal outcomes. |
| Fresh UI runtime | Separate `a.localhost` / `b.localhost` sessions; refusal before explicit issuer admission; defer into `/app`; setup, send and open. One bundle correlates message/envelope ID, sender/receiver UI, outbox, mailbox and content digest. |
| Strict regression | Story-010 has typed send passports and ordinary recipient/INAC approvals, without preauthorization. Narrow profile still enters `/app` but cannot send without authority. No inference/model or VM execution. |

Every completed tracker gate pins sources, generated profiles, binary digests and
its own measured evidence. Local qualification is not release readiness. Stage A's
dated records cannot establish Stage B enforcement.

## Trade-offs

Truthful status exposes profile gaps previously hidden by a successful boolean.
Deferral keeps unrelated work accessible while making the incomplete preparation
visible. Shared evaluation reduces drift between wizard and auto-ready but requires
precise selection and profile-dependent trust rather than one generic id check.

Evidence-rich reads improve diagnosis of "ready earlier, blocked later" without
making snapshots durable grants. Idempotency requires durable coordination and
recovery semantics, but avoids hidden races between independent preparation clients.
Always-enforced typed authority removes policy modes and transitional cohorts.
Pre-release profiles must be prepared explicitly; that intentional compatibility
break does not establish a post-release migration policy.

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
2. **Post-release migration:** deliberately outside the pre-release Stage B scope.
   Any later compatibility commitment requires a new proposal and evidence.

## Next Actions

### Repeatable Browser and Recovery Qualification (2026-10-16)

The accepted follow-up separates the no-JavaScript HTML driver from a real pinned
headless browser for HTMX/JavaScript interactions. Node's acceptance-only capsule
uses Python Playwright `1.63.0` and Chromium Headless Shell `153.0.8010.12`, revision
`1243`. Installation uses hash-locked offline wheels and an inventoried browser
capsule; the run refuses changed bytes. This dependency is confined to acceptance,
where HTML parsing cannot establish JavaScript execution or competing browser tabs.
The harness explicitly maps `a.localhost` and `b.localhost` to loopback in both
Python and Chromium; cookies remain isolated by host.

`MSG-ONB-005` records three distinct proof classes: UI blocking and durable deferral
before admission; a test operator's signed root ceremony with the staged digest and
unchanged antirollback state; and ready preparation after verified activation by
restart. Creating an identity or running the browser never authorizes the ceremony
implicitly. An explicitly authorized synthetic federation may automate its isolated
operator ceremony. It must not alter an existing user's profile. Deferred Messaging
and federation steps reach `/app` with visible status, including after restart.
INAC invitations and recipient relationship consent are separate actual UI actions.
A delivery bundle correlates message/envelope IDs, content digest, sender UI/outbox,
recipient mailbox/UI and the explicit read action.

`MSG-ONB-006` uses the existing issue API with a short 30-second TTL and retained
`expires_at`, without a product test clock. It covers expiry, local revocation,
locked issuer keys, explicit unlock/setup renewal and one new typed passport from
two competing setup tabs. Restart, observation, unlock, renewal and normal processing
do not resume `authority-blocked`. Single and bulk retry cover double clicks and
simultaneous tabs, distinct overlapping operation keys, same-key response-loss replay
and exactly one retry generation/delivery. Active-root removal remains conformance.

The harness parameter `issuer-path=sovereign|delegated` separates authority paths.
The [accepted P076 decision](076-limited-messaging-grants-decision.md) owns the
bounded issuance proof and its online signed status source. The first development
slice is `delegated-local-send`: B remains outside root and sends to sovereign A.
This does not qualify delegated receive/INAC, org custody or a release candidate.
MSG-ONB-005/006 keep their completed sovereign scope; new delegated evidence uses
separate tracker rows, never a sovereign fallback.

| Task | Scope | Status | Completion gate |
|---|---|---|---|
| MSG-ONB-007 | Fresh delegated onboarding and bidirectional Messaging | todo | Two ordinary identities absent from root; separate UI block, grant ceremony and unlock evidence; explicit contact/INAC consent; correlated delivery/open in both directions |
| MSG-ONB-008 | Delegated authority loss and explicit recovery | todo | Short child/parent TTL, stale remote status, parent withdrawal cascading to receive and INAC, locked delegate, restart and competing setup/retry from two tabs without duplicate or implicit resume |

Candidate qualification has a closed set: conformance prerequisites, strict
Story-010, `005 sovereign`, `006 sovereign`, and `S027-008`. One run pins clean source
revisions, six unchanged binaries, generated profile digests and the browser capsule.
A local candidate qualification does not establish release readiness. Historical
Stage A/B evidence keeps its original date and scope.

### Implementation Tracker

Stable task ids preserve the reviewed `MSG-ONB-*` workstream. Stage A completion is
bounded to the local operator preparation/read flow and the retained evidence below;
it does not qualify all P060/P076, real federation users or release readiness.

| Task | Stage | Depends on | Status | Completion gate |
|---|---|---|---|---|
| MSG-ONB-001a | A | – | done | Freeze exact selector, local-send profile/legacy classes, participant/role evidence, `messaging-readiness.local.v1`, aggregation, closed reasons and allowed actions; retain selection/conformance fixtures. |
| MSG-ONB-001b | A | MSG-ONB-001a | done | Strengthen/refactor the existing evaluator with signature, active-root/profile authority, revocation, owner/caller and pinned evidence; reuse read-only verification; invalidate decisions across root/binding changes. |
| MSG-ONB-002 | A | MSG-ONB-001a, MSG-ONB-001b | done | Add separate issuer fact/step, signed request verification, explicit operator handoff and durable deferred Messaging/federation steps; retain `/app` status without automatic admission or false completion. |
| MSG-ONB-003 | A | MSG-ONB-001a, MSG-ONB-001b | done | Shared daemon preparation coordinator for wizard/auto-ready, durable intent/result idempotency, concurrent/crash recovery and preserved withdrawn-consent behavior. |
| MSG-ONB-004 | A | MSG-ONB-001a, MSG-ONB-001b, MSG-ONB-002, MSG-ONB-003 | done | Retain all Stage A conformance/negative cases, fresh-UI-identity message/content evidence and separate strict Story-010 regression; document legacy execution compatibility and the narrow-profile deferral result. |
| MSG-ONB-001c-01 | B | MSG-ONB-004 | done | Evaluator, revocation/cache, shared reasons and DTOs; pinned conformance. |
| MSG-ONB-001c-02 | B | MSG-ONB-001c-01 | done | Host evaluator/port, admission provenance and setup renewal; refusal before effects and idempotent typed issuance. |
| MSG-ONB-001c-03 | B | MSG-ONB-001c-02 | done | AD/peer guards, bounded paused queue and explicit idempotent retry; queue/concurrency/restart/crash evidence. |
| MSG-ONB-001c-04 | B | MSG-ONB-001c-01, MSG-ONB-001c-02, MSG-ONB-001c-03 | done | Generators, read-only audit and three separate evidence classes; reconcile P097, S027, Node ledger and MVP. |
| MSG-ONB-005 | Follow-up | MSG-ONB-001c-04 | done | Pinned offline real-browser fresh identity flow; pre-ceremony blocking/deferred `/app`, separately evidenced signed operator ceremony, post-restart preparation, actual INAC/contact actions and correlated opened/read message. |
| MSG-ONB-006 | Follow-up | MSG-ONB-005 | done | Short-TTL expiry and local revocation; locked-key renewal, concurrent setup and single/bulk browser retries, response-loss replay, restart persistence and exactly-once delivery. |

The follow-up candidate dated `2026-10-16` passes the closed gate from clean Node
`6cb581de650c249ec24ce2abb4d4fd9f31652c7f` and Orbidocs
`8aa917b913ec9061e45e9a160ded5e4da017b680`, with one unchanged six-binary set.
It retains 492 conformance/capsule test executions, 18 actual-browser onboarding
cases, 21 actual-browser authority-recovery cases, 23 independent host-Memarium
recovery cases and 34 strict Story-010 phases. The strict profile also uses explicit
INAC operator approval, with no contact-request auto-admit or preauthorization.
UI blocking/deferral, signed operator root ceremony and post-restart preparation
remain separate proof classes. Local expiry, revocation, locked-key renewal,
overlapping retry operations and one lost response each retain measured results.

Source/profile/binary/capsule pins, sanitized reports and milestone review are at
`node:docs/evidence/messaging-onboarding/2026-10-16/README.md`. S027-008 additionally
fixes logical mailbox identity during reindex and the missing discard proxy exposed
by runtime measurement. These dated results cover sovereign issuance; the later
P076 decision and delegated qualification are tracked separately.
This is local qualification, not release readiness; historical measurements below
retain their original scope and date.

Stage A evidence includes 16 fresh-UI runtime cases, the correlated message/content
bundle, two completed parallel fresh UI setup jobs, concurrent first issuance,
process-crash/response-loss retry, revocation history,
withdrawn consent, signed request tampering/replay, active-root removal, an independently
run empty-generic-plan deferral profile, and separate strict Story-010 regression.
Conformance and lifecycle tests are retained separately. The narrow control uses a
Story-010 topology with Story-013-like omitted generic prerequisites; it does not run
full Story-013. No model or VM runs in this qualification.

Original Stage B evidence dated `2026-10-13` retains 804 conformance tests, separate
daemon/host/UI gates, 24 fresh-identity runtime cases, seven narrow-profile cases
and 31 strict Story-010 regression phases. Source files, terminal profile configs
and unchanged executable digests are pinned in
`node:docs/evidence/messaging-onboarding/2026-10-13/candidate-manifest.json`.
Actual loopback WSS and indirect adapter tests cover delayed effects; explicit
renewal/retry delivers once, and local authority delivers after directory isolation
beyond 300 seconds. Historical Stage A evidence remains unchanged. This is local
debug-build qualification, not release readiness.

A separately pinned review closeout dated `2026-10-13` retains 810 conformance
tests with additional native gates, 25 fresh-identity cases, seven narrow-profile
cases and 31 strict Story-010 phases. It measures durable provenance adoption and
terminal reconciliation, while controlled tests qualify provenance/history cleanup,
unique enqueue, immutable observations, actual caller/issuer selection and the
chunk/fetch boundary. Directory isolation lasts 323 seconds before actual delivery.
The source/profile/binary manifest and four-stage commit plan are retained at
`node:docs/evidence/messaging-onboarding/2026-10-13-review/README.md`.
The original reports are unchanged; local qualification does not establish release
readiness or broader participant policy.

A scoped browser follow-up dated `2026-10-13` corrects optional attestation
rendering and adds three regressions; the full Node UI suite passes 307 tests.
Actual browser interaction on separate localhost hosts reuses exactly the two
previously approved UI-created identities, with clean contact/transport histories
and guided Story-013 readiness on B. A narrow INAC invitation and a separate
contact request are explicitly accepted before the sole message is delivered and
opened/read. Sender UI, outbox, recipient mailbox/UI and content digest correlate.
This is additional UI evidence, not a new fresh-creation, strict Story-010,
model/VM or release qualification. Retained measurements and source/profile/binary
digests are at `node:docs/evidence/messaging-onboarding/2026-10-13-browser/README.md`.

Stage B follows the always-enforce plan above. Resolve
P076's limited-grant question before claiming support for ordinary non-sovereign users
through a new authority path.
