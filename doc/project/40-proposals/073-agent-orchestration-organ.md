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

Lifecycle operations are **host capabilities**, not Inquirium operations. Each is
registered in the Capability Registry (Proposal 072), authorized by the host,
metered against budget, and recorded in a decision ledger.

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

`stop` is authoritative and idempotent: it cancels in-flight Inquirium/Sensorium
operations, releases data leases, frees budget, and writes a terminal fact.
`suspend` freezes the controller while preserving session context; `resume`
continues from the last durable checkpoint, not a replayed prompt.

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

Session context and lifecycle transitions are append-only facts in Memarium
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
- **Degraded mode mirrors the assistant.** When Memarium is disabled or
  unavailable, the agent runs on a local ephemeral working set plus a local
  non-federating fallback (the baseline must work without Memarium); durability,
  audit, and federation resume when Memarium returns. The working set is always
  rebuildable from the durable facts, so `suspend`/`resume` and crash recovery
  never depend on hot state surviving.

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
- `spawn/status/stop` local-control E2E with idempotent `stop`;
- unknown fields and missing termination condition fail closed;
- classification ceiling defaults fail closed;
- no ambient capability: an agent without a grant cannot invoke Inquirium or
  propose Sensorium/AD effects;
- monotone fork denial for widened grants, classification, autonomy, tool set,
  or budget once `fork` is enabled;
- bounded fan-out defaults prevent more than the configured children/concurrency;
- prompt-free step/status traces contain refs, digests, budget deltas, and
  decisions, but not prompt text, model output, or raw context.

## Data Contracts

- `agent.spec.v1` — declarative agent specification (model-selection, params,
  budget, controller, requested grants).
- `agent.state.v1` — lifecycle transition fact (state, reason, at, by).
- `agent.session.v1` — Memarium-backed session context envelope (pinned facts,
  summary ref, recall refs).
- `agent.step.v1` — one controller step record (inference call ref, evidence
  digest, proposed effect ref, decision).
- `agent.spawn.request.v1` / `agent.fork.request.v1` /
  `agent.suspend.request.v1` / `agent.resume.request.v1` /
  `agent.stop.request.v1` — lifecycle mutation request bodies.
- `agent.status.response.v1` — read-only lifecycle and budget projection.
- `agent.step-trace.v1` — prompt-free operational trace (step count, budget spent,
  model snapshot, instruction hash, spawn/effect refs; no prompt, output, or
  context content).

All requests reject unknown fields at the boundary; classification defaults
fail-closed; identifiers are explicit and canonical.

## Relationship to Existing Mechanisms

- **Inquirium (063/064).** Agent is the consumer that 063 names ("Flow … and the
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
- **Assistant Channel (066).** Proposal 066 Phase 3 agentic effects land here: the
  assistant stays advise-only/local-only baseline, and an operator may, with
  explicit capability and human-in-the-loop, drive an Agent from the assistant
  surface. The assistant is one operator-facing surface over Agent, not the Agent
  itself.
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
  authoritative and idempotent; a reaper terminates agents past TTL and releases
  their leases (every store/queue has a lifecycle).
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
  deferred to a separate proposal.
- The first live working set is an **in-memory / ephemeral projection**. Memarium
  remains the durable fact plane, not a cache; a dedicated projection cache can
  be evaluated later.
- The first profile uses conservative, configurable developer defaults:
  `max_steps = 8`, `max_depth = 1`, `max_children = 0 or 1`,
  `max_concurrent = 1`, and a short deployment-configured wall-time TTL.

## Open Questions

None block the first node-local implementation slice.

Deferred questions:

1. Cross-node / federated agents: define in a separate proposal after the
   node-local lifecycle, budget, trace, and effect-proposal model is proven.
2. Dedicated live projection cache: evaluate after the in-memory working set has
   real profiling data and clear lifecycle requirements.
3. Production fan-out/budget profiles: define after the conservative developer
   profile has operational evidence.

## Implementation Tracker

Status values: `todo`, `in-progress`, `done`, `deferred`.

| ID | Work item | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- |
| `agent-core-crate` | Create thin `agent-core` contract crate with Agent/controller/budget/grant DTOs and the lifecycle state machine. | `in-progress` | `node/agent-core` scaffolded and compiling: `AgentSpec`/`AgentParams`/`AgentBudget`/`ControllerPolicy`/`TerminationCondition`/`CapabilityGrant` DTOs with `deny_unknown_fields` and `validate()`, fail-closed classification ceiling, the `AgentLifecycleState::apply` state machine, the `validate_fork_from` monotone-narrowing validator, and lifecycle request DTOs; 8 unit tests pass and the crate is clippy/rustdoc clean under `-D warnings`. Runtime budget metering, fork budget split, and durable wiring remain. |
| `agent-dep-direction-lint` | Add a dependency-direction lint so `agent-core` cannot import substrate. | `in-progress` | `node/tools/check-agent-core-deps.py` mirrors the `inquirium-core` guard (bans daemon/model-runtime/HTTP/async/SQLite via `cargo tree`) and is wired into `.github/workflows/docs.yml`; the check passes for the current scaffold. An `xtask`-level lint may later replace the standalone script. |
| `agent-inquirium-boundary-docs` | Document that the durable agent loop lives above Inquirium and that assistant agentic effects are realized through Agent. | `done` | Proposal 064 now has the *Agent Loop Lives Above Inquirium* boundary note, Proposal 066 Phase 3 points agentic effects at Proposal 073, and this proposal owns the lifecycle/controller/budget tracker. |
| `agent-lifecycle-capabilities` | Add `agent.spawn/fork/suspend/resume/stop/status` host capabilities. | `todo` | Registered in Capability Registry; fail-closed admission; request/response schemas for spawn/fork/suspend/resume/stop/status; budget-metered; decision ledger entries; local-control E2E. |
| `agent-monotone-fork` | Enforce monotone narrowing and budget split on `fork`. | `todo` | Child grants/classification/autonomy/tools ⊆ parent; parent budget is split not duplicated; negative tests for widening and self-authorization. |
| `agent-bounded-fanout` | Enforce `max_steps/max_depth/max_children/max_concurrent/aggregate_budget` and mandatory `termination_condition`. | `todo` | An agent without a terminator is rejected; fork-bomb test stays bounded; watchdog stops runaway loops. |
| `agent-durable-state` | Persist session context and lifecycle as Memarium-backed durable facts with replay/recovery. | `todo` | `agent.state.v1`/`agent.session.v1` facts; `resume` and crash recovery rebuild from facts; `as of` query works. |
| `agent-memory-projection` | Build the working set as a projection of durable Memarium facts via `MemoryPolicy`, with fail-closed degradation. | `todo` | Working set is rebuilt per step from facts (pinned + bounded summary + recall), kept off the hot Memarium path; only meaningful facts (turn/result/decision/observation) are written, never the KV cache; with Memarium disabled the agent runs on a local ephemeral working set plus a local non-federating fallback, and durability/audit/federation resume when Memarium returns. |
| `agent-controller-step-records` | Persist each controller step as an auditable `agent.step.v1` fact. | `todo` | Each step records inference call ref, evidence digest, proposed effect ref, decision, budget delta, and causal predecessor; replay can reconstruct the trajectory without prompt/output content. |
| `agent-effects-as-proposals` | Route effects through Sensorium/AD capability gates with human-in-loop for sensitive classes. | `todo` | Agent never self-executes; sensitive-class effects require operator approval; every effect is an auditable fact. |
| `agent-budget-enforcement` | Reuse the enforced token/cost budget at agent and spawn-tree scope. | `todo` | Per-agent and per-tree caps; typed `BudgetExceeded`; spend attributable in trace; shares the `inq-cost-budget-enforcement` contract. |
| `agent-step-trace` | Add prompt-free `agent.step-trace.v1` with model snapshot, instruction hash, and decision. | `todo` | Trace omits prompt/output/context content; records step count, budget spent, spawn/effect refs; reproducibility fields present. |
| `agent-reaper` | Add a TTL reaper for orphaned/stale agents that releases leases. | `todo` | Agents past TTL are stopped and their leases released; reaper is idempotent and recorded. |
| `agent-assistant-surface` | Let the assistant (P066) drive an Agent under explicit capability and human-in-loop. | `deferred` | Assistant stays advise-only baseline; agentic escalation requires capability + operator approval; no ambient initiation. |

## Next Actions

1. Land `agent-core` with the Agent/controller/budget DTOs and the
   monotone-narrowing validator behind the dependency lint.
2. Add the `agent.spawn/stop/status` minimal lifecycle slice with durable facts
   and budget metering, before `fork`/effects.
3. Register the `agent.*` capabilities in the Capability Registry and keep the
   P064/P066 boundary notes in sync as the first implementation slice lands.

## Related Capability Data

- capabilities: `agent.spawn`, `agent.fork`, `agent.suspend`, `agent.resume`,
  `agent.stop`, `agent.status`.
- schemas: `agent.spec.v1`, `agent.state.v1`, `agent.session.v1`,
  `agent.step.v1`, `agent.spawn.request.v1`, `agent.fork.request.v1`,
  `agent.suspend.request.v1`, `agent.resume.request.v1`,
  `agent.stop.request.v1`, `agent.status.response.v1`, `agent.step-trace.v1`.
