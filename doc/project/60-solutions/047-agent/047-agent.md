# Agent

Based on:

- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/60-solutions/002-memarium/002-memarium.md`
- `doc/project/60-solutions/018-classification/018-classification.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`
- `doc/project/60-solutions/043-horizontal-protocol-primitives/043-horizontal-protocol-primitives.md`
- `doc/project/60-solutions/044-inquirium/044-inquirium.md`
- `doc/project/60-solutions/045-inquirium-assistant-channel/045-inquirium-assistant-channel.md`

Related schemas:

- `agent.spec.v1`
- `agent.session.v1`
- `agent.state.v1`
- `agent.lifecycle-command.v1`
- `agent.step.v1`
- `agent.step-decision.v1`
- `agent.step-trace.v1`
- `agent.memory-policy.v1`
- `agent.binding.v1`
- `agent.binding.v2`
- `agent.effect-proposal.v1`
- `agent.effect-proposal-outcome.v1`
- `agent.effect.dispatch.request.v1`
- `agent.effect.dispatch.response.v1`
- `agent.outcome.v1`
- `causal-context.v1`

## Status

Implemented node-local hard-MVP solution.

The node-local Agent contract, durable runtime, bounded controller, memory
projection, lifecycle, fork and budget accounting, effect-proposal boundary,
human-in-loop admission, recovery, lease reconciliation, and prompt-free audit
surface are implemented and refusal-tested. FlowNode, Assistant Channel, and
Corpus integrations are implemented consumers; they do not widen Agent
authority. Cross-node or federated Agent execution is not part of this solution.

## Date

2026-07-18

## Executive Summary

Agent is the node organ for durable, bounded, multi-step orchestration above
Inquirium. It binds a model-selection policy, remembered context, controller
policy, budget, grants, output sink, and explicit lifecycle to one addressable
session. The host owns admission, authority, accounting, and recovery.

```text
Agent orchestrates under host authority.
Inquirium answers.
Memarium remembers.
Agent declares observation needs and proposes effects.
The host resolves both through the owning domains and admits every transition.
```

An Agent may propose work, call admitted inference, fork within a narrowed
budget, and produce an inert outcome. It never authorizes its own effects and
never publishes its own result. This keeps model reasoning separate from
authority and makes every state transition recoverable and auditable.

## Context and Problem Statement

Bounded inquiry alone does not provide a durable entity that can pursue a goal
across multiple steps, remember a working context, suspend and resume, or create
strictly narrower helpers. Embedding that behavior in a model adapter would
turn transport code into an ambient agent. Implementing it separately in every
workflow would duplicate lifecycle, budget, recovery, and effect-admission
logic.

Agent provides one node-local orchestration organ with a small semantic core and
host-owned runtime. It composes existing organs through their public contracts
rather than acquiring their privileges or storage responsibilities.

## Proposed Model / Decision

### Stratified Ownership

The implementation is divided by meaning:

1. `agent-core` owns substrate-free values, validation, lifecycle transitions,
   monotone fork rules, memory policy, generic observation need/binding/evidence,
   effect proposal, and outcome contracts. It has no Sensorium or Workbench
   vocabulary or dependency.
2. `agent-host` owns pure controller decisions, operator-profile admission, and
   the closed registry that compiles admitted effect intents into
   transport-independent execution plans.
3. The Node host owns durable facts, recovery projections, capability admission,
   accounting, scheduling, leases, and calls into Inquirium, Sensorium, and
   Artifact Delivery.
4. Consumer components own the domain transition that accepts an Agent outcome.
   The Agent itself has no publication authority.

Dependency-direction checks keep the semantic crates independent from daemon,
transport, database, and provider-runtime details. `agent-core` has one named
vertical exception: it reuses the pure bounded-inference request/result DTOs
from `inquirium-core`, because inference is constitutive to an Agent session.
The exception includes no Inquirium host, provider, runtime, or authority code;
a positive direct-dependency allowlist makes every additional dependency an
explicit review event. Room, Corpus, Memarium, Sensorium, Workbench, and other
source/effect domains remain forbidden in the core vocabulary and dependency
graph.

### Horizontal Ports and the Composition Root

Agent describes **what it needs**, not which vertical subsystem should satisfy
it. An `AgentObservationNeed` carries an opaque `source/ref`, expected
`payload/schema-ref`, and freshness/byte bounds. The durable Agent binding fixes a
consumer-authorized `AgentObservationBinding`; successful resolution produces
prompt-free `AgentObservationEvidence` with the validated source P081
`causal/context` plus source-version and resolution refs.
Neither value names Room, Sensorium Interfaces, Workbench, or a provider.

The daemon is the composition root. It resolves an admitted need through a
registered domain adapter, validates the returned payload at schema-gate, and
rechecks the owning domain's grants and current authority. The Story 012 adapter
therefore knows the exact Room, relay, membership, recipient, and Sensorium
Interface rules while `agent-core` remains unchanged. Effects follow the same
shape in the other direction: Agent emits a generic immutable proposal and the
daemon compiles it through a closed, capability-specific adapter before policy,
lease, HIL, and execution admission.

JSON-e Flow supplies declarative wiring only. Operator-authored, digest-pinned
configuration predeclares bounded need-to-source mappings and grant requests;
rendered flow data may select or narrow those mappings but cannot create, widen,
or interpolate authority-significant refs. Its validator imports the Agent-owned
hard item, age, byte, and reference caps instead of maintaining parallel limits.
After caller-capability and ownership checks, binding admission requires exactly
one registered resolver for each source/schema pair before persistence; missing,
incompatible, and ambiguous registrations fail closed. Authorization,
classification, and payload interpretation remain compiled host semantics. The
Room/Sensorium path enters Interaction Broker under a typed internal Agent-host
principal rather than caller-controlled kind/module strings. The validated source
`causal/context` preserves causality, while the separate resolution ref makes the
selected wiring auditable without retaining the observation payload. Durable step
facts and traces additionally pin each evidence item to the enclosing Agent,
binding, and canonical passage identity.

The process-local latest-state inbox refuses two different content digests at
one relay epoch and sequence with a dedicated payload-free structured diagnostic.
The conflicting delivery cannot replace the already admitted observation.

The composed Story 012 process profile revokes C and waits for relay-audience
convergence before repair, dirty-restarts recipient B, then proves a newer passing
state for B while C remains refused. Its 17-entry refusal matrix names whether
each claim is evidenced directly by the composed runner or by the owning
P070/P082/P083 lower-stratum suite.

The implemented post-MVP operational-context extension remains source-owned by P082.
Agent Core carries only bounded generic qualifier refs and strict digests; the daemon
validates the exact source value, current generation, and effective publication,
computes a monotone local caution class, and passes the P064 host-authored layer to
Inquirium before feed-dependent inference. Agent defines no freshness TTL and treats
the P082-capped summary as inert data. This preserves the horizontal Agent port and
creates no observation or effect authority. Multi-feed, local-floor, stale-result,
qualifier-digest, provenance, and golden prompt-layer tests pin the boundary. The
daemon-owned provenance records the local policy ref and floor, selected class, and
each source class paired with its qualifier digest in request metadata and the durable
Inquirium trace. The composition root supplies the trace projection directly;
`agent-core` does not interpret or persist that vertical vocabulary.

### Neutral Consumer Policy and Authority Binding

The implemented `agent.binding.v1` binds one Agent to one consumer, session source,
output sink, grant set, budget, memory policy, review policy, and, for collaborative
consumers, participant and Room membership-attestation refs. The implemented compatible
`agent.binding.v2` revision generalizes the consumer-policy and authority-evidence
portion without adding Room, Corpus, Assistant Channel, Sensorium, or other vertical
vocabulary to Agent Core. V1 remains valid, while a v2 binding is admitted and recovered
only through a registered owning-domain resolver that verifies the exact current policy,
digest, review floor, and evidence set.

The neutral extension carries only host-authored, content-addressed evidence:

| Field | Meaning |
|---|---|
| `consumer-policy/ref` | immutable reference to the consumer-owned effective policy |
| `consumer-policy/digest` | canonical digest verified when binding, recovering, and using authority |
| `authority-evidence/refs` | sorted, unique, bounded refs proving the external authority used at admission |

The baseline cap is the shared Agent Core constant
`AGENT_AUTHORITY_EVIDENCE_REFS_MAX = 16`. Schema validation, binding admission,
recovery, and adapters import that value instead of repeating a literal. Bodies remain
in their owning stores and are interpreted only by a registered daemon composition
adapter. The collaborative v1 `membership-attestation/ref` remains the first
specialized evidence ref. The implemented v2 resolver projects that authority into
`authority-evidence/refs` while preserving the same validation and rejecting a v1/v2
conflict rather than silently accepting both values.

These fields are evidence, not capabilities. The binding's `grants` continue to name
only capabilities the Agent may request, and every concrete use still rechecks the
current consumer policy, owning-domain authority, target, lease, classification,
idempotency, and host policy. The binding-level `human-in-loop` value is a minimum
review floor; a consumer policy may require stricter review per operation but cannot
lower it. Caller-supplied refs are unresolved intent until the host validates them and
constructs the persisted binding.

The binding request digest covers the effective consumer-policy ref and digest,
authority-evidence refs, grants, budget, and output sink. Recovery refuses missing,
altered, conflicting, or unverifiable evidence. Revocation or narrowing in the owning
domain removes the affected effective operations and releases related leases; if the
binding can no longer satisfy its consumer contract, the host suspends or quarantines
the Agent according to current operator policy rather than retaining stale authority.

For Corpus chairing, the daemon adapter may resolve a Corpus chair-control policy and
current scoped Room delegation into generic capability grants and evidence refs. Agent
Core sees neither floor modes nor moderation operations. `CollaborativeChair` remains
the neutral consumer kind; dependency-direction checks and contract tests must reject
any floor, voice, kick, ban, Room scope, or Corpus policy vocabulary added to
`agent-core`. The Agent emits inert effect proposals, while Corpus and Room retain their
separate canonical admission paths.

### Lifecycle and Identity

An Agent is node-local and addressable by an opaque `agent/id`. Its lifecycle is
explicit: `spawn`, `fork`, `suspend`, `resume`, `status`, and `stop`. Lifecycle
commands are idempotent, actor-bound facts. Local control has administrative
authority; a module additionally needs an explicit bounded Agent grant and may
operate only on Agents it owns.

The host records an immutable admission snapshot at creation. Recovery replays
history against that snapshot and then evaluates current operator policy.
Removed or tightened policy quarantines the affected Agent and its descendants
without preventing unrelated Node services from starting.

### Bounded Controller and Forking

Every controller passage consumes explicit inputs and produces a pure decision
before the host performs any admitted work. Limits cover steps, wall time,
tokens, cost, depth, children, and concurrency. Termination is mandatory.

Forking is monotone narrowing. A child cannot widen classification, grants,
trust, model selection, controller limits, review policy, or budget. Child
budgets are reserved from the parent rather than duplicated, and unused
reservations return deterministically when descendants terminate.

### Durable Memory and Trace

Memarium facts are the durable source of truth for session, lifecycle, memory
policy, steps, effects, and outcomes. The hot working set is an ephemeral,
bounded projection of pinned facts, externally produced summaries, and an
allowlist of recall references. Agent does not summarize itself; summary
producer authority belongs to explicitly admitted external components.

Step traces contain references, digests, decisions, accounting, and causal
links, never raw prompts or generated response content. Content-addressed
products live outside status and notification projections.

### Effects Are Proposals

Agent output is evidence, not authority. A requested effect first becomes an
immutable `agent.effect-proposal.v1`. Host policy checks Agent grants,
classification, step freshness, target capability, binding authority, leases,
and review requirements. Sensitive proposals remain deferred until a human
decision is joined through the operator-question lifecycle.

Only admitted proposals are compiled by a registered closed policy adapter into
an execution plan for the owning host surface. Unknown effect kinds fail closed;
there is no generic fallback. Execution produces a separate durable outcome and
exact replay does not invoke the target again.

### Outcomes Remain Inert

Completed bound work produces a content-addressed `agent.outcome.v1`. The
binding fixes the consumer, session, grants, budget, and output sink. The
consumer validates the outcome and performs its own domain transition. Assistant
Channel may accept it as a render-only draft; Corpus may accept it as an inert
answer draft. Neither path grants Agent direct publication authority.

### Recovery and Maintenance

Startup rebuilds a bounded disposable projection from append-only facts,
repairs recognized partial fact bundles, reconstructs idempotency state, and
reconciles interrupted leases and deferred effect outcomes. Scheduler-owned
bounded jobs reap expired Agents, reconcile deferred effects, release stale
leases, and compact old inactive lease details into audit-preserving tombstones.

Operator control remains a separate host-local surface. A bounded paginated
list exposes lifecycle, policy, budget, pending-work, lease, and outcome
metadata without prompt or product bytes. Fixed-cardinality diagnostics report
recovery repairs, quarantine, reaper backlog, active-controller latency, pending HIL
and effects, leases, and projection capacity through stable reason codes. An
inspect-first maintenance endpoint builds one pure bounded plan. Dry-run
projects its counts and post-maintenance diagnostics without mutation; explicit
operator execution applies the same policy-reconciliation, TTL-reaper, and
terminal-lease cleanup plan. One exclusive cursor page bounds all three
maintenance classes, and lease counts come from actual registry releases rather
than global counter differences. Agent lifecycle facts remain authoritative for
expiry, the lease registry durably owns release state and reason, and
current-policy admission remains a disposable projection. Missing lineage and
an existing quarantined ancestor remain distinct diagnostic states. Maintenance
never rewrites durable history or duplicates another registry's state.

### Node-Local Hard-MVP Acceptance

The hard-MVP gate requires all of the following:

- substrate-free core and host strata with dependency-direction checks;
- a substrate-neutral observation/effect port with static, fail-closed wiring;
- durable lifecycle, facts, idempotency, bounded recovery, and quarantine;
- enforced controller, budget, fork, fan-out, deadline, and termination bounds;
- bounded memory projection with externally governed summaries;
- inert effect proposals, human-in-loop admission, closed effect adapters, and
  lease/accounting reconciliation;
- binding and outcome contracts that cannot self-publish;
- metadata-only operator status and prompt-free causal traces;
- bounded operator diagnostics and inspect-first maintenance;
- unit, refusal, failpoint, dirty-restart, process-level HTTP, and sustained
  short-session soak coverage.

These conditions are implemented. Node-local Agent is therefore a hard-MVP
component whose release gate is currently satisfied.

## Concrete Sequence

```text
authorized caller
  -> agent.spawn (profile + narrowed grants + budget)
  -> durable admission snapshot and running state
  -> agent.binding.create (consumer + session + output sink)
  -> agent.controller.run (expected step)
  -> pure step decision
     -> observation need -> daemon resolver -> bounded inert context
        -> admitted Inquirium call, or
     -> inert effect proposal -> policy/HIL -> owning host surface, or
     -> monotone child fork, or
     -> terminal outcome
  -> durable step, accounting, and prompt-free trace facts
  -> content-addressed agent.outcome.v1
  -> consumer-owned acceptance or publication transition
```

## Trade-offs

The design adds explicit lifecycle, grant, binding, and persistence machinery
around model-driven loops. This is more work than an adapter-local loop, but it
prevents provider code from becoming an authority boundary and makes restart,
budget, and effect behavior inspectable.

Node-local scope deliberately postpones mobility and remote execution. It keeps
the first trusted runtime small and mature before federation introduces remote
identity, distributed leases, clock, migration, and split-brain concerns.

## Failure Modes and Mitigations

- **Unbounded loop or fork storm:** admission and every passage enforce step,
  time, depth, child, concurrency, and aggregate budget limits.
- **Child widens authority:** fork validation permits only monotone narrowing and
  reserves budget from the parent.
- **Model self-authorizes an effect:** model output can create only an inert
  proposal; host policy and, when required, operator approval admit execution.
- **Policy changes after restart:** immutable historical admission is preserved,
  while current-policy reconciliation quarantines invalid sessions and lineage.
- **Interrupted durable write:** lifecycle commands and completed steps are
  commit markers; bounded recovery repairs only recognized partial bundles.
- **Duplicate external effect:** exact effect replay returns the durable outcome
  without target reinvocation; ambiguous provider inference still requires the
  provider boundary's own idempotency support.
- **Sensitive content leaks through status:** status and traces expose bounded
  metadata, refs, and digests rather than prompts or generated product bytes.
- **Lease survives Agent termination:** startup and scheduler reconciliation
  release stragglers and retain compact audit tombstones.
- **Operational repair creates a second state machine:** maintenance reuses the
  current-policy, durable reaper, and lease-registry paths through one pure
  preview/apply plan; dry-run is non-mutating and deferred-effect reconciliation
  remains scheduler-owned.
- **Aggregate status leaks generated content:** operator list and diagnostics
  expose fixed metadata and refs only, use bounded pagination/cardinality, and
  remain unavailable to module-authenticated callers.
- **A consumer-policy ref is mistaken for authority:** refs and digests are admission
  evidence only; every operation rechecks current owning-domain authority, effective
  policy, binding grants, review floor, target, lease, and classification.
- **Consumer policy changes while an Agent is active:** recovery and runtime use verify
  the bound digest and reconcile current authority; narrowing removes operations and
  leases, while an unsatisfied consumer contract suspends or quarantines the Agent.

## Open Questions

No open question blocks the node-local hard-MVP solution. Cross-node execution,
Agent mobility, and federated authority require a separate proposal rather than
an extension hidden inside this solution.

## Next Actions

1. Keep node-local Agent on the hard-MVP release gate and preserve the full
   process-level dirty-restart acceptance suite.
2. Add effect-policy adapters only with a concrete consumer and owning host
   surface; unknown capabilities must continue to fail closed.
3. Keep node-local operator list, diagnostics, maintenance, failpoint matrix,
   and standalone process/soak pack on the Agent release gate before proposing
   cross-node or federated execution.
4. Keep detailed implementation evidence and future recommendations in Proposal
   073 rather than duplicating tracker prose here.
5. Keep the implemented Story 012 path as a daemon-owned Sensorium resolver for
   the generic Agent observation port: statically bind one need to one opaque
   source, bind the resolved read result and inline snapshot to one Room recipient
   and Agent passage, preserve its validated P081 causal context, keep content
   ephemeral, and deny dynamic wiring, implicit actuation, or membership-derived
   authority. New sources extend daemon wiring, not `agent-core`. Keep the
   passing composed three-node runner on the release gate: it reuses Story 011's
   bootstrap and proves distinct participant evidence, local repair observation,
   observer revocation, dirty restart, and unpublished chair output.
6. Keep the implemented neutral consumer-policy and authority-evidence binding v2 on
   its current-policy recovery gate. Corpus is the first concrete resolver and golden
   recovery consumer. Preserve v1 compatibility, exact v1/v2 conflict refusal,
   revocation checks, and `AGENT_AUTHORITY_EVIDENCE_REFS_MAX = 16` as the one imported
   bound across schema, admission, recovery, and adapter layers.

## Must Implement

- node-local lifecycle, binding, controller, memory, effect, and outcome
  contracts;
- durable fact storage, bounded recovery, quarantine, and idempotency;
- monotone fork, aggregate budget, deadline, fan-out, and termination controls;
- host-authorized Inquirium calls and inert effect proposals;
- generic observation needs, durable static bindings, prompt-free resolution
  evidence preserving P081 causal context, and daemon-owned source resolvers;
- closed Sensorium and Artifact Delivery effect-plan boundaries;
- scheduler-owned reaping, deferred reconciliation, and lease cleanup;
- prompt-free trace, bounded operator status, diagnostics, and inspect-first
  maintenance;
- hard-MVP unit, refusal, failpoint, restart, process smoke, and sustained
  short-session soak coverage.

## May Implement

- Assistant Channel escalation and render-only outcome acceptance;
- FlowNode bindings, JSON-e Flow Agent grants, and static observation wiring;
- Corpus chair and selected-participant bindings;
- neutral content-addressed consumer-policy and authority-evidence binding for
  operator-bounded domain integrations;
- additional capability-specific effect-policy adapters;
- specialized projection caches justified by measured workload.

The first three optional integrations are implemented. They remain optional to
the Agent organ because their owning components may be absent from a deployment.

## Out of Scope

- cross-node or federated Agent execution, migration, or ownership transfer;
- ambient autonomy or standing effect authority;
- model/provider transport, inference semantics, or model selection internals;
- durable storage implementation owned by Agent itself;
- direct publication, Room authority, or consumer-domain state transitions;
- generic tool execution that bypasses Sensorium or Artifact Delivery policy.

## Consumes

- operator Agent profiles and current admission policy;
- authenticated local-control or module capability context;
- Inquirium inference capabilities and usage evidence;
- Memarium fact append/query surfaces;
- operator-authored static observation wiring and separately admitted grants;
- daemon-owned Sensorium and Artifact Delivery host adapters and plans;
- operator-question decisions and model-runtime leases.

## Produces

- durable Agent lifecycle, step, memory, effect, and outcome facts;
- bounded node-local status and recovery projections;
- prompt-free causal and accounting traces;
- bounded observation evidence with validated P081 causal context and opaque
  source-version and resolution refs;
- inert effect proposals and execution outcomes;
- content-addressed `agent.outcome.v1` values for consumer-owned acceptance.

## Related Capability Data

Machine-readable capability data for this solution lives in:

- `doc/project/60-solutions/047-agent/047-agent-caps.edn`

## Implementation Recommendations

Proposal 073 remains the implementation-recommendation and evidence document
for this solution. Its tracker records concrete crate ownership, schemas,
runtime paths, refusal cases, process smokes, and deferred work. Promotion does
not turn those implementation details into protocol semantics.
