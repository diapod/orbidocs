# Proposal 073: Agent — Bounded Stateful Orchestration Organ

## Status

Draft

## Date

2026-06-26

## Executive Summary

Orbiplex should introduce **Agent** as the node organ for stateful, bounded,
multi-step orchestration that sits **above** Inquirium. An Agent is a durable,
addressable entity that binds a model-selection policy, a remembered session
context, parameters, a budget, and a bounded controller loop, with an explicit
lifecycle: `spawn`, `fork`, `suspend`, `resume`, `stop`.

An Agent **composes** other organs and owns none of them. It calls Inquirium for
inference, Sensorium for effects, and Memarium for durable memory (not the
agent's hot working/KV memory); the host owns authority, budget, and lifecycle. This realizes the agentic mode — an entity with
an attached model, remembered context, and parameters, plus actions that
multiply or stop agents — that Inquirium deliberately excludes:

> "In Orbiplex, Inquirium is not the agent loop. … Flow, Arca, Sensorium, and the
> host own broader orchestration." — Proposal 063

Agent is that missing home, defined so that no model ever gains ambient authority.

The governing rule is:

```text
Agent is the bounded controller with identity, memory, and a lifecycle.
Inquirium answers; Sensorium acts; Memarium remembers; the host authorizes.
The agent proposes and orchestrates; it never self-authorizes an effect.
```

## Context and Problem Statement

Inquirium is bounded inquiry and is explicitly *not* the agent loop (Proposal
063; Proposal 064 invariant "conversation orchestration is not an Inquirium
adapter concern"). Proposal 064's Flow IR permits only an inline `bounded
controller` (`max_steps`, `max_cost`, `max_time`, `allowed_tools`,
`termination_condition`, review policy). Proposal 066 defers agentic effects to a
capability-gated Phase 3.

Yet real workflows need a stateful agent: an entity that remembers a session,
holds parameters, runs several inference steps toward a goal, may spawn helpers,
and can be stopped. Today that entity has no home. Putting it inside Inquirium
would make a model adapter an ambient agent — the named threat "Inquirium becomes
a general AI agent with ambient authority" (Proposal 063). Leaving it ad hoc
invites the classic agent failure modes: unbounded loops, fork bombs, orphaned
state, runaway cost, and effects without accountability.

Agent gives that entity one durable, host-owned, auditable home with an explicit
lifecycle and authority that is bounded by construction.

## Goals

- A first-class, durable, addressable `Agent` abstraction binding model-selection
  policy, remembered session context, parameters, budget, and a bounded
  controller.
- Explicit lifecycle operations `spawn`, `fork` (multiply), `suspend`, `resume`,
  `stop` as host capabilities — budget-metered, ledgered, fail-closed.
- Strict stratification: Agent consumes Inquirium, Sensorium, Memarium, and host
  authority; it owns none of them, and those organs hold no knowledge of agents.
- Bounded by construction: monotone narrowing on fork, bounded fan-out, enforced
  budget, mandatory termination, no self-authorizing agents.
- Full causal trace: every step, spawn, effect proposal, and lifecycle transition
  is an auditable, prompt-free fact.

## Non-Goals

- Not an inference engine (Inquirium), effect engine (Sensorium), memory store
  (Memarium), or authority root (host).
- Not ambient autonomy and not a general AI agent with standing authority.
- Not a replacement for Flow IR's declarative DAG; the two are complementary (an
  Agent may run a Flow; a Flow may spawn an Agent).
- Not a cross-node/federated agent runtime in this slice (deferred).

## Decision

### 1. Agent is a stateful organ above Inquirium

An `Agent` is a durable record plus a host-run controller. It binds, by
reference, everything an agentic session needs, and nothing it must not own:

```text
Agent {
  agent/id
  agent/parent?            # lineage for forked/spawned agents
  model-selection          # profile/ref or runtime-candidate constraints;
                           #   host-owned binding, never a raw provider key
  session/ref              # Memarium-backed remembered context (durable facts)
  params                   # AssistantMode (ModeKeyed), plurality, classification
                           #   ceiling, instruction profile (PromptAssemblyPolicy)
  budget                   # token / cost / wall-time / step ceilings (enforced)
  controller               # bounded loop policy (see 3)
  grants[]                 # capability ids this agent may request (gated)
  trust/locality           # default local-only / strict_local
  lifecycle/state          # pending | running | suspended | completed
                           #   | stopped | failed
}
```

The boundary is hard: Inquirium has **zero knowledge of agents**. The Agent calls
`inquirium.generate` (and future operations) as a normal host-capability caller,
subject to the same classification, inference grants, and trace discipline as any
other caller. Inquirium output remains *evidence*, never authority.

The same boundary applies to collaborative rooms. A model-backed participant in a
Room or Corpus deliberation is represented by an Agent controlled by an
accountable subject or node role; a raw Inquirium adapter or model runtime is not
a room member. If a deployment wants a one-shot model respondent, it should use a
degenerate Agent profile with one step and an explicit budget rather than admit
the adapter as a speaking actor.

### 2. Lifecycle: spawn, fork, suspend, resume, stop

Lifecycle operations are **host capabilities**, not Inquirium operations. The
node-local slice registers `agent.spawn`, `agent.status`, `agent.stop`,
`agent.fork`, `agent.suspend`, and `agent.resume` in the Capability Registry
(Solution 037). Every mutation carries an idempotency key and is admitted by the
host before an append-only lifecycle command/state fact is written. The command
fact is the commit marker and authoritative replay record; the state fact is its
rebuildable audit projection, so a partial multi-fact write cannot lose the
idempotency decision. The current
caller policy is deliberately local-control-only; module callers remain denied
until a separate, explicit Agent lifecycle grant vocabulary exists.

```text
agent.spawn   { spec | template/ref, budget, grants }       -> Agent (pending)
agent.fork    { agent/id, narrowing }                        -> child Agent
agent.suspend { agent/id }                                   -> suspended
agent.resume  { agent/id }                                   -> running
agent.stop    { agent/id, reason }                           -> terminal
agent.status  { agent/id }                                   -> read-only projection
```

State machine:

```text
pending -> running -> { suspended <-> running } -> completed | stopped | failed
```

In the current node-local slice, lifecycle mutations are authoritative and
exactly replayable from durable command facts: an exact retry returns the prior
result while reuse of an idempotency key with a different request fails closed.
`suspend` freezes the controller while preserving its fact projection; `resume`
continues from the latest durable state rather than replaying a prompt. Terminal
state and TTL reaping are durable. Cancellation of future in-flight
Inquirium/Sensorium work, Agent-owned lease release, and return of unused child
budget remain controller-runtime work because the current slice does not yet own
such live resources.

### 3. Multiplication is monotone narrowing with bounded fan-out

`agent.fork` is the "multiply" action, and it can only narrow. On **every** axis a
child is a subset of its parent: `grants ⊆ parent.grants`, classification ceiling
no higher, autonomy no looser, `allowed_tools ⊆ parent`. The parent's budget is
**split**, not duplicated — a child draws from a reserved slice of the parent's
remaining budget. This mirrors the monotone discipline of `ClassKeyed`/`ModeKeyed`
and `PromptAssemblyPolicy`: a lower scope may specialize, never widen.

Fan-out is bounded by construction to prevent fork bombs and resource exhaustion:

```text
controller {
  max_steps
  max_depth                # spawn-tree depth cap
  max_children             # direct children per agent
  max_concurrent           # live descendants across the tree
  aggregate_budget         # whole-tree token/cost/time ceiling
  termination_condition    # mandatory; an agent with no terminator is rejected
  review_policy            # when a human gate is required
}
```

There are **no self-authorizing agents**: an agent cannot grant itself a
capability, raise its own budget, or spawn a child with authority it does not
hold.

### 4. Agent state is durable facts, not mutated objects

Session seeds and lifecycle transitions are append-only facts in Memarium
(Proposal 036), not mutated in place. This gives `as of` queries, audit, and
replay: the trajectory of an agent — what it knew, decided, spawned, and stopped
— is reconstructable. The live controller holds only a cache derived from those
facts; the facts are the source of truth. `resume` and crash recovery both rebuild
from the same fact stream.

Memory follows the `MemoryPolicy` from Proposal 064: pinned facts (never
auto-summarized), a bounded rolling summary, and a host-pinned recall allowlist —
so context does not grow without bound.

#### Memory model: durable plane vs working set

Memarium is the agent's **durable, governed memory** — the source of truth — not
its hot working memory. The two are distinct strata and must not be conflated:

```text
durable fact plane (Memarium)    source of truth: governed, classified, "as of",
   |  MemoryPolicy projects v        auditable, replayable, optionally federated
working set / assembled context  ephemeral, per-step, token-bounded
   |  rendered into v
provider KV / prompt cache        optimization, runtime/provider-side, discardable
```

Two consequences:

- **Memarium is off the hot path.** The agent reads through a projection (the
  working set built by `MemoryPolicy`) and writes only *meaningful facts* —
  turns, results, decisions, observations — never the KV cache token by token.
  This keeps the per-step path fast and the governed log free of bulk or
  ephemeral content (Proposal 066: `memarium.write` stays a fact-plane).
- **Degraded mode mirrors the assistant.** When Memarium is disabled at startup,
  the agent runs on a local ephemeral, non-federating fact store and reports that
  durability explicitly in status. When a configured Memarium write fails, the
  mutation fails closed rather than silently changing durability. A later
  transition between these modes requires an explicit reconciliation protocol;
  the current process does not switch sources of truth dynamically.

By memory type: the working set is **working memory** (KV-like, ephemeral);
Memarium holds **episodic** (this session) and **semantic/long-term** (across
sessions) memory; procedural memory lives in grants and templates, not Memarium.

### 5. Effects are proposals; inference is evidence

A controller step calls Inquirium for inference, routes the (evidence-only)
output back into the loop, and may *propose* an effect. The agent never executes
an effect directly. Effects flow through Sensorium / Artifact Delivery as
capability-gated operations; sensitive classes (relationship, governance,
external publication, egress) require human-in-the-loop approval, inheriting
Proposal 066's Phase 3 contract. An Inquirium `Plan` return remains a
`CandidatePlan` the host compiles or rejects (Proposal 064); the agent is the
durable, addressable form of that same host-first orchestration, not an escape
hatch around it.

### 6. Stratification and crates

```text
agent-core (thin contract crate)
  - Agent / controller / budget / grant DTOs
  - lifecycle state machine + monotone-narrowing validator
  - depends only on: classification, inquirium-core contracts, serde/error
  - MUST NOT depend on substrate (daemon, model-runtime, HTTP, async, SQLite),
    enforced by a dependency-direction lint mirroring inquirium-core

daemon (substrate)
  - agent.* host capabilities and the bounded controller runtime
  - durable agent/session store (Memarium-backed) + spawn-tree budget metering
  - capability gating, lease lifecycle, decision ledger, trace
```

## Implementation Recommendations

Implement Agent as a stratified host organ, not as an Inquirium operation, model
adapter, Flow shortcut, or ambient daemon side loop. The first runtime slice
should use a **daemon-owned controller** that may call Flow IR for bounded
sub-steps, but the controller lifecycle, authority checks, budget metering, and
stop/suspend/resume semantics remain host-owned. This keeps one orchestration
substrate responsible for live agent state while still allowing declarative Flow
plans to be one of the things an agent executes.

Build the implementation in layers:

1. Keep `agent-core` as the substrate-free contract crate: DTOs, validation,
   lifecycle state machine, monotone fork validator, and schema constants only.
   It must not gain daemon, model-runtime, HTTP, async runtime, SQLite, or store
   dependencies.
2. Add the daemon host facade and local-control surfaces for the smallest useful
   lifecycle: `agent.spawn`, `agent.status`, and `agent.stop`. `fork`,
   `suspend`, `resume`, effects, and assistant escalation come after this slice
   can create, inspect, stop, and audit a bounded local agent.
3. Persist lifecycle transitions as append-only facts. The live controller may
   keep an in-memory working projection, but that projection is cache-like and
   disposable. It is not Memarium, not authority, and not required for crash
   recovery semantics.
4. Add budget/fan-out enforcement before enabling `fork` or effect proposal
   routing. A fork without budget split and monotone narrowing is not an agent
   feature; it is a fork bomb waiting for policy.
5. Route effects only as proposals through Sensorium / Artifact Delivery and
   existing host capabilities. Agent output may ask for an effect; the host and
   operator remain the authority that admits, denies, delays, or scopes it.

The first implementation slice is **node-local only**. Cross-node or federated
agents are explicitly deferred to a later proposal and must not leak into the
first controller through remote spawn, remote resume, or federated state
replication. A local agent may call existing federated organs through explicit
capabilities, but the agent lifecycle itself is local.

Memarium is the durable fact plane, not the live cache. The first working set
should be an **in-memory / ephemeral projection** derived from the agent request
and any admitted local facts. A dedicated projection cache may be introduced
later if profiling shows the need, but it should be a rebuildable optimization
with clear lifecycle, not a second source of truth.

Explicit non-goal: **do not dump the in-memory runtime cache to disk and reload
it verbatim on restart.** That would make the ephemeral projection a second
source of truth by the back door. The only sanctioned path to surviving a
restart is `agent-durable-state` (append-only `agent.state.v1`/`agent.session.v1`
facts) plus `agent-memory-projection` (rebuilding the working set *from* those
facts) — never a serialized snapshot of the cache itself.

The current implemented slice has a Memarium-backed append-only fact store and a
disposable in-memory projection. Lifecycle commands, session seeds, state,
initial steps, budget traces, effect proposals, and effect outcomes survive a
restart when Memarium is enabled. Exact lifecycle retries rebuild their
idempotency result from those facts. If Memarium is disabled, status reports an
ephemeral, non-federating mode rather than pretending crash recovery exists.

Active lifecycle capabilities remain local-control-only: module callers are
denied until an explicit Agent lifecycle grant model exists. Local-control
mutations are attributed as `local-control`; future module-authorized calls must
preserve the concrete caller module id in lifecycle facts. The rebuilt
idempotency projection has a fail-closed bound: once its configured capacity is
reached, new mutations are denied rather than evicting replay evidence and
making duplicate execution possible.

Use conservative, overridable developer defaults for the first profile:

```text
max_steps       = 8
max_depth       = 1
max_children    = 0 or 1
max_concurrent  = 1
wall_time_ttl   = short, deployment-configured
```

These defaults are a safety floor, not a constitutional constant. Distributors
and operators may override them in agent configuration, but widening must remain
explicit, validated, and visible in status/trace. The default profile should
reject agents without a termination condition, agents with unbounded budget,
unknown capability grants, or effects that try to execute without a host grant.

Minimum test matrix for the first slices:

- lifecycle state-machine transitions, including invalid transition denial;
- `spawn/fork/suspend/resume/status/stop` local-control E2E with exact mutation
  replay and conflicting idempotency reuse denied;
- unknown fields and missing termination condition fail closed;
- classification ceiling defaults fail closed;
- no ambient capability: an agent without a grant cannot invoke Inquirium or
  propose Sensorium/AD effects;
- monotone fork denial for widened grants, classification, autonomy, tool set,
  or budget once `fork` is enabled;
- bounded fan-out defaults prevent more than the configured children/concurrency;
- prompt-free step/status traces contain refs, digests, budget deltas, and
  decisions, but not prompt text, model output, or raw context.

### Controller as a functional core (`agent-host`)

The "daemon-owned controller" above should follow the same functional-core /
imperative-shell split already used by `inquirium-host`: the per-step controller
*decision* is a pure value computed in an `agent-host` service stratum, and the
daemon performs the effects. Each tick produces an `agent.step-decision.v1`:

```text
agent.step-decision.v1 {
  step/no
  action            # call-inquirium {request-ref} | propose-effect {proposal-ref}
                    #   | spawn-child {child-spec-ref} | await-human | complete | fail
  budget-charge
  termination-satisfied
}
```

The daemon executes the chosen action and feeds the result back; the decision
itself is replayable and unit-testable without sinks. This keeps the agent loop
from accreting daemon coupling, mirroring the Inquirium decoupling. Stratify as
`agent-core` (contracts + state machine) → `agent-host` (pure step decisions plus
read-ports) → daemon (effects, persistence, budget metering), guarded by a
dependency-direction lint.

Lifecycle requests carry an `idempotency/key`: a retried `spawn`/`fork` must
replay the prior result, not create a second agent or a second child.

### Consumer binding (Corpus chair, assistant, Flow node)

Agent is driven by domain consumers, not invoked bare. The recurring shape is one
binding contract, `agent.binding.v1`, that attaches an agent to a consumer's
session and output sink under narrowed authority:

```text
agent.binding.v1 {
  binding/id, agent/ref
  consumer/kind                 # corpus-chair | assistant-channel | flow-node
  consumer/ref                  # query/id (Corpus) | session/ref (assistant) | flow/node-ref
  session-source/ref            # room/ref | transcript/ref | dataset/ref  (ref vocabulary)
  output-sink/kind              # corpus-answer-draft | assistant-response-draft | flow-result
  grants[]                      # MUST be a subset of the consumer's own grants
  budget                        # from the consumer policy (deliberation budget / assistant rigor)
  participant/ref?              # host-minted accountable principal; never model identity or model-supplied
  membership-attestation/ref?   # room-membership-attestation.v1 for corpus-chair
  human-in-loop                 # approval policy for effect proposals
}
```

Invariants:

- **Grants are monotone-narrowing from the consumer.** A consumer cannot grant the
  agent more authority than it holds — the same discipline as `fork`
  (`validate_fork_from`). Corpus and the assistant narrow; they never widen.
- **The agent is a Room participant, never a raw model adapter.** For
  `corpus-chair`, the agent joins the deliberation room through
  `room-membership-attestation.v1` (Solution 036); its contributions are room facts
  signed by its principal, satisfying Proposal 069's "no raw model adapters as room
  participants".
- **Output is a draft, not an effect.** The agent produces a content-addressed
  product (`agent.outcome.v1`); the consumer admits it (Corpus answer acceptance is
  chair-signed; the assistant surfaces a response draft). The agent never publishes
  or settles on its own.

Reuse, do not reinvent: agent context comes through the existing
`inquirium.context-assembly.request.v1` plus context-source grants and
`MemoryPolicy` (Proposals 064/066), so the agent reads context through the same
classification/grant gates rather than raw; human-in-the-loop for an effect
proposal reuses `inquirium.operator-question.request.v1` (Proposal 066) rather than
a new approval surface; durable facts use the `memarium.write` fact plane.

## Data Contracts

- `agent.spec.v1` — declarative agent specification (model-selection, params,
  budget, controller, requested grants).
- `agent.state.v1` — lifecycle transition fact (state, reason, at, by).
- `agent.session.v1` — durable session seed binding the validated spec, selected
  runtime profile, creation command digest, actor, and expiry. Pinned facts,
  summary refs, and recall refs belong to the separate memory projection tracked
  below; they are not silently embedded in this lifecycle seed.
- `agent.lifecycle-command.v1` — durable idempotency fact for lifecycle mutations,
  binding operation, request digest, actor, result state, and related child where
  applicable.
- `agent.step.v1` — the durable step **fact after** execution or denial: the
  decision taken, the effect outcome, budget spent, evidence/effect refs, and the
  causal predecessor step. Distinct from `agent.step-decision.v1`, which is the pure
  decision computed *before* the effect.
- `agent.spawn.request.v1` / `agent.spawn.response.v1` /
  `agent.fork.request.v1` /
  `agent.suspend.request.v1` / `agent.resume.request.v1` /
  `agent.stop.request.v1` / `agent.stop.response.v1` — lifecycle mutation
  request/response bodies.
- `agent.status.request.v1` / `agent.status.response.v1` — read-only lifecycle
  and budget projection.
- `agent.step-trace.v1` — prompt-free operational trace (step count, budget spent,
  model snapshot, instruction hash, spawn/effect refs; no prompt, output, or
  context content).
- `agent.binding.v1` — how a domain consumer (Corpus chair, assistant, Flow node)
  attaches an agent to a session source and output sink under narrowed grants (see
  *Consumer binding*).
- `agent.effect-proposal.v1` — an agent's **immutable** request to invoke a host
  capability: `proposal/ref`, `capability/id`, `args/digest`, a validated
  `classification` value (or store-side equivalent reference where the envelope
  owns the value), prompt-free `reason/code`, optional `evidence/refs`, and
  `requires-human-in-loop`. The proposal is a fact and is never mutated.
- `agent.effect-proposal-outcome.v1` — a separate host-authored fact, joined to the
  proposal by `proposal/ref`, recording the decision: `outcome`
  (`admitted` | `denied` | `deferred` | `superseded`), `decided-by`, `at`, and an
  optional `reason/ref`, operator-question ref, or bound directive ref. The
  outcome is a fact *about* the proposal, not a field inside it (facts over
  overwriting).
- `agent.outcome.v1` — the terminal product a consumer picks up: terminal state,
  `product/kind`, content-addressed `product/ref` (a draft, never inline),
  `budget-spent`, and `trace/ref`.
- `agent.step-decision.v1` — the pure, replayable controller decision computed by
  `agent-host` from read-ports **before** any effect; the daemon executes the chosen
  action and records the result as an `agent.step.v1` fact.

All requests reject unknown fields at the boundary; classification defaults
fail-closed; identifiers are explicit and canonical.

## Relationship to Existing Mechanisms

- **Swarm Broadcast Assistance (077, advisory companion).** Assistance
  decomposition/routing and unattended multi-agent deliberation ride bounded
  Agent sessions: human-in-the-loop gates *effects, budgets, and acceptance* —
  never individual conversational turns. What agents may do unattended is
  reason; what they may not do unattended is commit.
- **Weak Signal Harvester (078).** A bounded Agent may orchestrate a harvesting
  pass: scan configured sources, request Inquirium grouping/redaction, emit
  finding files, and stop. It must not widen source grants, bypass the findings
  directory, or publish Whisper/network artifacts directly.
- **Inquirium (Solution 044 / Proposal 064).** Agent is the consumer that 063 names ("Flow … and the
  host own broader orchestration"). The Flow IR `bounded controller` (064) is the
  seed; Agent generalizes it into a durable, addressable, forkable entity. The
  Inquirium boundary is unchanged — see the new P064 note *Agent Loop Lives Above
  Inquirium*.
- **Flow IR (064) / workflow orchestration (033).** Complementary: Flow is a
  declarative DAG of steps; an Agent is a stateful controller with memory and a
  lifecycle that may compile and run Flows, and a Flow node may spawn an Agent.
- **Sensorium (045).** All agent effects route through Sensorium / Artifact
  Delivery under capability gates; the agent proposes, the host/operator
  authorizes.
- **Memarium (036).** Session context and lifecycle are durable facts; Agent adds
  no second memory store.
- **Capability Registry (072).** `agent.spawn/fork/suspend/resume/stop/status`
  are registered capability ids with fail-closed admission.
- **Assistant Channel (Solution 045).** The assistant Phase 3 agentic effects land here: the
  assistant stays advise-only/local-only baseline, and an operator may, with
  explicit capability and human-in-the-loop, drive an Agent from the assistant
  surface. The assistant is one operator-facing surface over Agent, not the Agent
  itself.
- **Corpus (069).** Corpus live deliberation drives an Agent as the host-owned
  reasoning **chair** bound to a Room (`agent.binding.v1`,
  `consumer/kind = corpus-chair`); the chair Agent participates via Room membership
  attestation, and its answer-draft product feeds Corpus answer acceptance. Corpus
  owns reasoning, chairing, and settlement semantics; the Agent owns the bounded
  session.
- **Enforced budget (064 `inq-cost-budget-enforcement`).** Agent budgets reuse the
  same metering and `BudgetExceeded` contract at agent and spawn-tree scope.

## Failure Modes and Guardrails

These are the agent-orchestration mistakes that recur in practice, with the
guardrail Agent adopts against each:

- **Fork bomb / resource exhaustion.** Budget is split (not duplicated) on fork;
  `max_depth`, `max_children`, `max_concurrent`, and `aggregate_budget` bound the
  whole tree.
- **Non-terminating loops.** `termination_condition` is mandatory; an agent
  without one is rejected. `max_steps`/`max_time` are hard watchdogs.
- **Privilege escalation via spawn.** Monotone narrowing on every axis; no
  self-authorization; the host is the only authority root.
- **Orphaned agents / leaked leases.** Lifecycle is durable facts; `stop` is
  authoritative and idempotent; a bounded scheduler reaper records terminal
  state for agents past TTL. Agent-owned lease tracking and release must be added
  before controller actions can retain leases across steps.
- **Cost blowup.** Enforced per-agent and per-tree budgets with typed
  `BudgetExceeded`; spend attributable in trace.
- **Unbounded context growth.** `MemoryPolicy` (pinned + bounded summary +
  recall) with token estimation gating each step.
- **Effects without accountability.** Effects are capability-gated proposals;
  sensitive classes are human-in-the-loop; every effect is an auditable fact.
- **Non-reproducible runs.** Each step records the resolved model snapshot,
  instruction hash, and controller decision, so a trajectory can be explained and
  replayed.

## Resolved Decisions

- Agent is a **separate organ above Inquirium**, not an Inquirium operation;
  Inquirium stays "not the agent loop".
- Authority is **host-owned**; agents never self-authorize and fork only narrows.
- Agent state is **durable facts** (Memarium), not mutated objects.
- The contract lives in a thin `agent-core` crate guarded by a dependency lint.
- The first controller runtime is **daemon-owned** and may use Flow IR for
  bounded sub-steps; Flow IR is not the lifecycle owner.
- The first runtime slice is **node-local only**; cross-node/federated agents are
  deferred to a separate proposal after the node-local lifecycle, budget, trace,
  and effect-proposal model is proven.
- The first live working set is an **in-memory / ephemeral projection**. Memarium
  remains the durable fact plane, not a cache; a dedicated projection cache can be
  evaluated later after real profiling data and clear lifecycle requirements.
- Production fan-out and budget profiles are **operator-defined**, not limited to
  a fixed preset catalog. The implementation still provides conservative,
  configurable developer defaults:
  `max_steps = 8`, `max_depth = 1`, `max_children = 0 or 1`,
  `max_concurrent = 1`, and a short deployment-configured wall-time TTL.

### Additional Decisions For Durable Runtime Slice

The first node-local slice is decision-complete. These choices govern the next
durable/runtime slice:

1. `agent.spawn`, `agent.status`, and `agent.stop` remain host-local lifecycle
   capabilities. Their Capability Registry shape stays
   `dispatchable=true`, `surfaces=["host-local"]`, and
   `passport/eligible=false`. Any future federated agent request surface requires
   a separate proposal and a distinct authorization model.
2. `budget_remaining` in `agent.status.response.v1` is derived only from
   daemon-owned metering records. Controllers, adapters, or models may report
   usage as evidence, but the daemon validates and records the spend before it
   affects status.
3. `agent/id` remains an opaque ref. Locality is enforced by storage, routing,
   and host registry boundaries rather than by embedding a node namespace into
   the identifier format.
4. Production Agent profiles are loaded from daemon/operator configuration.
   `agent-host` provides reusable DTOs, validation, and the conservative
   developer default; it must not gain compile-time production profile presets
   that move deployment policy into the functional core.
5. Durable recovery preserves an immutable admission snapshot: the admitted
   profile identity and canonical constraint snapshot travel with the session.
   Historical facts may be reconstructed under that snapshot, but resume, new
   inference, forks, and effects must also pass current operator policy. A
   session that no longer passes becomes quarantined and must not prevent
   unrelated daemon services from starting.

Deferred work that does not require a new decision is already tracked below:
cross-node/federated agents require a separate proposal; a dedicated projection
cache waits for profiling data and a clear lifecycle; and production fan-out/
budget profiles are operator-defined with the conservative developer defaults
above as the initial built-in profile.

## Open Questions

No open questions remain for the first node-local durable runtime slice.

## Implementation Tracker

Status values: `todo`, `in-progress`, `done`, `deferred`.

| ID | Work item | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- |
| `agent-core-crate` | Create thin `agent-core` contract crate with Agent/controller/budget/grant DTOs and the lifecycle state machine. | `done` | `node/agent-core` compiles as a substrate-free contract crate: `AgentSpec`/`AgentParams`/`AgentBudget`/`ControllerPolicy`/`TerminationCondition`/`CapabilityGrant` DTOs with `deny_unknown_fields` and `validate()`, fail-closed classification ceiling, conservative developer defaults, `idempotency/key` on spawn, `agent.step-decision.v1`, `agent.spawn.response.v1`, `agent.status.request.v1`, `agent.status.response.v1`, `agent.stop.response.v1`, the `AgentLifecycleState::apply` state machine, and the `validate_fork_from` monotone-narrowing validator. Evidence: `cargo test -p orbiplex-node-agent-core`, `cargo clippy -p orbiplex-node-agent-core -- -D warnings`, and `python3 tools/check-agent-core-deps.py` pass. Runtime budget metering, fork budget split, and durable wiring are tracked separately below. |
| `agent-dep-direction-lint` | Add a dependency-direction lint so `agent-core` cannot import substrate. | `done` | `node/tools/check-agent-core-deps.py` mirrors the `inquirium-core` guard (bans daemon/model-runtime/HTTP/async/SQLite via `cargo tree`) and is wired into `.github/workflows/docs.yml`; the check passes for the current contract crate. An `xtask`-level lint may later replace the standalone script. |
| `agent-inquirium-boundary-docs` | Document that the durable agent loop lives above Inquirium and that assistant agentic effects are realized through Agent. | `done` | Proposal 064 now has the *Agent Loop Lives Above Inquirium* boundary note, Proposal 066 Phase 3 points agentic effects at Proposal 073, and this proposal owns the lifecycle/controller/budget tracker. |
| `agent-lifecycle-capabilities` | Add `agent.spawn/fork/suspend/resume/stop/status` host capabilities. | `in-progress` | All six node-local ids are active, host-local, non-passport-eligible capabilities with table-driven dispatch. Mutations write `agent.lifecycle-command.v1` plus state/session facts, preserve the local-control actor, replay exact idempotency keys after restart, and reject conflicting reuse. Remaining: explicit module lifecycle grants, cancellation of future in-flight controller work, and a process-level HTTP lifecycle smoke. |
| `agent-monotone-fork` | Enforce monotone narrowing and budget split on `fork`. | `done` | `AgentSpec::validate_fork_from` prevents widened grants, classification, trust, model selection, controller bounds, and budget; daemon fork admission requires a running parent, reserves the child's budget from parent remaining budget, prevents the child deadline from exceeding the parent's remaining absolute TTL, records lineage durably, and rejects a second child under the default fan-out profile. Core and daemon negative/recovery tests pass. |
| `agent-bounded-fanout` | Enforce `max_steps/max_depth/max_children/max_concurrent/aggregate_budget` and mandatory `termination_condition`. | `in-progress` | Core/profile admission enforces bounded steps, depth, children, live descendants, per-agent and aggregate budget ceilings, and a mandatory terminator; daemon fork admission enforces depth/direct-child/root-concurrency limits; operator profiles are loaded from daemon config; and the TTL reaper is scheduler-owned. Remaining: applying these caps to a real concurrent controller executor and releasing/reconciling unused child reservations. |
| `agent-durable-state` | Persist session context and lifecycle as Memarium-backed durable facts with replay/recovery. | `done` | The daemon persists validated `agent.session.v1`, `agent.state.v1`, `agent.lifecycle-command.v1`, initial step/trace, budget trace, and effect facts through a narrow `AgentFactStore` backed by Memarium Personal facts. The lifecycle command is the commit marker; recovery repairs missing state/initial-step projections and initial effect outcomes after a partial bundle. Startup rebuilds the disposable projection and lifecycle idempotency ledger through bounded pages over the ordered stream rather than a lifetime fact-count ceiling, caches parsed deadlines, and repairs only the latest missing state projection so a late historical repair cannot regress current state. Memarium generic fact queries provide the append-only `as of` source. With Memarium disabled, status explicitly reports ephemeral durability. |
| `agent-profile-recovery-policy` | Implement recovery when an admission profile is removed or tightened. | `todo` | Persist the admitted profile identity and canonical constraint snapshot, reconstruct historical facts against that immutable snapshot, apply current operator policy before resume/new inference/fork/effect transitions, quarantine incompatible sessions, and prove that one incompatible historical Agent cannot silently widen authority or prevent unrelated daemon services from starting. |
| `agent-memory-projection` | Build the working set as a projection of durable Memarium facts via `MemoryPolicy`, with fail-closed degradation. | `todo` | Working set is rebuilt per step from facts (pinned + bounded summary + recall), kept off the hot Memarium path; only meaningful facts (turn/result/decision/observation) are written, never the KV cache; with Memarium disabled the agent runs on a local ephemeral working set plus a local non-federating fallback, and durability/audit/federation resume when Memarium returns. |
| `agent-controller-step-records` | Persist each controller step as an auditable `agent.step.v1` fact. | `in-progress` | Spawn and fork write a durable initial `agent.step.v1`; durable budget traces preserve causal predecessors and charge refs/digests. Remaining: execute the real controller loop and record each inference/effect decision, evidence digest, and outcome as a completed step fact. |
| `agent-effects-as-proposals` | Route effects through Sensorium/AD capability gates with human-in-loop for sensitive classes. | `in-progress` | Immutable proposals and separate outcomes are durable. Admission checks running state, Agent grants, step freshness, classification, and review policy. Proposal refs have one global Agent owner, question refs use a direct projection index, and each outcome history follows a bounded host-validated transition sequence. HIL proposals project to the existing operator-question lifecycle; Confirm answers normalize boolean and registered `yes`/`no` values, timeout transitions are audited, admitted Workbench requests must match the canonical proposal, and one Sensorium directive binding is persisted. Remaining: a generic Artifact Delivery execution bridge and broader capability-specific executors. |
| `agent-budget-enforcement` | Reuse the enforced token/cost budget at agent and spawn-tree scope. | `in-progress` | Inquirium charges carrying `agent/ref` are preflighted against host-owned spend plus reservations, replayed exactly, persisted as prompt-free traces, and rebuilt after restart. Fork reserves rather than duplicates parent budget and root live-descendant caps are enforced. Remaining: live controller wall-time/step charging, unused child-budget reconciliation, and resource/lease costs. |
| `agent-step-trace` | Add prompt-free `agent.step-trace.v1` with model snapshot, instruction hash, and decision. | `in-progress` | `agent.step-trace.v1` is a durable validated fact with decision, cumulative/delta budget, model/instruction slots, refs, predecessor, and timestamp; initial lifecycle traces and Inquirium budget-charge refs/digests survive recovery without prompt/output content. Remaining: populate model snapshot, instruction hash, and effect refs from real controller execution. |
| `agent-reaper` | Add a TTL reaper for orphaned/stale agents that releases leases. | `in-progress` | A bounded Replay Scheduler job reaps expired non-terminal sessions in deterministic batches, writes idempotent `Reap` lifecycle/state facts, and recovers terminal state after restart. Agent-owned lease references do not exist in this slice; lease release becomes mandatory before such ownership is introduced. |
| `agent-assistant-surface` | Let the assistant (P066) drive an Agent under explicit capability and human-in-loop. | `deferred` | Assistant stays advise-only baseline; agentic escalation requires capability + operator approval; no ambient initiation. |
| `agent-host-stratum` | Add an `agent-host` service stratum so the controller step decision is a pure value and the daemon performs effects. | `done` | `node/agent-host` computes `agent.step-decision.v1` as a pure value over `agent-core` contracts, exposes the conservative developer profile, contains no storage/HTTP/async/runtime substrate, and is guarded by `node/tools/check-agent-host-deps.py` in CI. Evidence: `cargo test -p orbiplex-node-agent-core -p orbiplex-node-agent-host`, `cargo clippy -p orbiplex-node-agent-host -- -D warnings`, and agent core/host dependency checks pass. The daemon executes actions in later tracker items. |
| `agent-binding-contract` | Add `agent.binding.v1` so consumers (Corpus chair, assistant, Flow node) drive an agent under narrowed grants. | `todo` | Binding carries `consumer/kind`, session-source, output-sink, monotone-narrowed grants, consumer budget, and optional Room `participant/ref`/attestation; grants ⊆ consumer; output is a content-addressed draft (`agent.outcome.v1`), never a self-published effect. |
| `agent-effect-proposal` | Add an immutable `agent.effect-proposal.v1` plus a separate `agent.effect-proposal-outcome.v1` fact joined by `proposal/ref`, with operator-question human-in-loop. | `in-progress` | Core owns validated proposal/outcome DTOs; daemon persists them in Memarium, replays exact proposals, rejects conflicting bodies and cross-Agent proposal-ref reuse, caps and validates outcome transitions, projects deferred proposals to Confirm questions with fail-closed timeout defaults, joins validated boolean or registered `yes`/`no` answers as admitted/denied outcomes, audits timeout transitions, and binds admitted Workbench directives once. Remaining: generic AD dispatch and an operator-facing Agent proposal/status projection. |
| `agent-corpus-chair` | Let Corpus (069) drive an Agent as the deliberation chair bound to a Room. | `deferred` | Chair Agent joins via `room-membership-attestation.v1`; its answer-draft feeds Corpus answer acceptance; blocked on the live-deliberation slice (P069/P070). |

## Next Actions

1. Implement the frozen admission-snapshot/current-policy recovery rule and its
   quarantine projection.
2. Connect the pure `agent-host` step decision to a real bounded daemon
   controller loop and persist every decision/result as `agent.step.v1` plus a
   prompt-free trace.
3. Implement `agent-memory-projection`: admitted pinned facts, externally
   produced bounded summaries, and recall allowlists assembled from Memarium
   without putting Memarium on the token-by-token hot path.
4. Add `agent.binding.v1` for the first domain consumer, then add explicit module
   lifecycle grants rather than weakening the current local-control-only gate.
5. Complete generic admitted-effect execution through Sensorium/Artifact
   Delivery and introduce Agent-owned lease accounting only together with
   terminal/reaper release semantics.

## Related Capability Data

- implemented capabilities: `agent.spawn`, `agent.fork`, `agent.suspend`,
  `agent.resume`, `agent.stop`, `agent.status`, `agent.effect.propose`.
- schemas: `agent.spec.v1`, `agent.state.v1`, `agent.session.v1`,
  `agent.lifecycle-command.v1`, `agent.step.v1`, `agent.step-decision.v1`, `agent.spawn.request.v1`,
  `agent.spawn.response.v1`, `agent.fork.request.v1`, `agent.suspend.request.v1`,
  `agent.resume.request.v1`, `agent.stop.request.v1`, `agent.stop.response.v1`,
  `agent.status.request.v1`, `agent.status.response.v1`, `agent.step-trace.v1`,
  `agent.binding.v1`, `agent.effect-proposal.v1`,
  `agent.effect-proposal-outcome.v1`, `agent.outcome.v1`.
