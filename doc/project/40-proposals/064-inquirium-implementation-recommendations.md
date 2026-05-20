# Proposal 064: Inquirium Implementation Recommendations

Based on:
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `node/DEV-GUIDELINES.md`

## Status

Draft

## Date

2026-05-20

## Executive Summary

This proposal refines Proposal 063 into implementation recommendations for
Inquirium. The goal is to keep Inquirium as a small, host-owned policy boundary
for model-backed inquiry while allowing many replaceable runtime adapters,
protocol gates, evaluators, tool bridges, agent bridges, and model adaptation
artifacts to evolve around it.

The core rule is:

```text
Inquirium Core owns semantic operations and policy.
Adapters translate execution details.
model-runtime owns lifecycle, health, supervision, and transport mapping.
Provider workers execute inference but hold no Orbiplex authority.
```

Model output remains candidate evidence, not authority. Every rejection,
failure, degraded result, fallback, continuation, retry, plan, tool call,
artifact, and adaptation result must be represented as a typed outcome.

## Design Commitments

These recommendations are filtered through the Node development guidelines:

- keep the trusted core small;
- keep data contracts explicit;
- authorize before effects;
- fail closed when authority or configuration is missing;
- avoid ambient filesystem, network, tool, model, or agent authority;
- prefer local-first operation;
- preserve exportable traces without leaking protected inputs;
- keep provider-specific mechanics out of workflow-facing contracts.

## Primary Rule: Adapters Translate Execution, Not Semantics

Inquirium Core is a host-owned policy boundary. An adapter is an execution
translator, not the owner of operation semantics. Operations such as
`generate`, `classify`, `embed`, `rerank`, `transform`, `train.adapt`, and
related verbs belong to Inquirium Core and its schemas. Provider-specific
payload mapping belongs inside adapters.

Runtime lifecycle, health, supervision, process management, and transport
mapping remain in `model-runtime`. Adapters do not receive ambient authority.
Model output remains candidate evidence. Every denial, failure, degradation,
fallback, continuation, and retry is a typed outcome. The preferred adapter is
replaceable, auditable, and boring.

## Adapter Vocabulary

`runtime adapter` translates request/result data between Inquirium,
`model-runtime`, and one concrete model execution surface.

`protocol gate` filters and shapes model communication according to a protocol
profile, role, and purpose.

`tool bridge adapter` maps external tools and resources to Orbiplex refs and
capability refs.

`agent bridge adapter` maps an external agent or agent protocol into candidate
evidence and typed outcomes.

`model adaptation artifact` is a LoRA/QLoRA adapter, prompt program,
checkpoint, or other result of adaptation. It is not a runtime adapter.

`provider worker` is a process, local server, remote endpoint, or API that
executes inference. It has no Orbiplex authority.

## Runtime Candidate Registry as Data

Inquirium should separate the registry of execution candidates from the
semantics of operations. A runtime candidate may have a canonical `runtime/ref`,
aliases for configuration migration, readiness metadata, configuration, and an
explicit selection priority. It must not define what `generate`, `embed`,
`classify`, or `train.adapt` means.

The selection contract should be data-driven:

- `profile/ref`;
- `operation`;
- operation requirements;
- candidate runtime list;
- selected runtime;
- typed rejection.

Aliases are useful for compatibility, but they must not change operation
meaning. Automatic priority should be an explicit field such as
`selection/weight` or `selection/order`, not an artifact of file loading order.

## Capability Metadata for Model and Runtime Selection

A runtime should declare its capabilities as data, not as hidden branches in an
adapter. The minimal capability record should include:

- supported operation classes;
- input and output modalities;
- context limits;
- input and output byte limits;
- locality class;
- egress policy;
- trace policy;
- retention profile;
- resource budgets;
- cost class;
- result class.

Model selection remains host policy, but host policy should operate over
explicit capability records. The host can then compare operation requirements
against runtime capabilities without knowing a concrete provider protocol.
This preserves the `what` and `how` separation: the caller describes the act of
inquiry, and lower layers choose how to execute it.

`supports-seed?` declares whether a runtime accepts a seed and whether that
seed influences output. Determinism remains best-effort, not a contract. The
same prompt, seed, parameters, and model may still yield different outputs
because of floating-point batch effects, parallel GPU reduction, or
provider-side nondeterminism outside the node's control. Replay equivalence for
generative outputs is limited to local runtimes with an explicit deterministic
mode. Remote runtime conformance should rely on schema checking, refusal
mapping, and metadata accounting, not bit-identical output.

## Inquirium Adapter Manifest

Every adapter should have a manifest as data. The manifest is an auditable
description of declared adapter capabilities, not a promise hidden in code. The
host uses the manifest for selection, configuration validation, conformance
test generation, and operator diagnostics.

Minimal shape:

```text
InquiriumAdapterManifestV1 {
  adapter/ref
  adapter/kind:
    local-http
    | remote-http
    | command-stdio
    | openai-compatible
    | open-inference-protocol
    | mcp-bridge
    | a2a-bridge
    | evaluator
    | artifact-transformer

  version
  implementation/ref?
  runtime/ref?
  profile/refs[]

  operations[]:
    generate
    | classify
    | embed
    | summarize
    | rerank
    | transform
    | image.generate
    | image.edit
    | audio.transcribe
    | audio.synthesize
    | train.adapt
    | batch.embed

  modalities/input[]
  modalities/output[]
  request/schema-refs[]
  result/schema-refs[]

  streaming/support
  batch/support
  tool-call/support
  structured-output/support

  capabilities {
    context/max-tokens?
    input/max-bytes?
    output/max-bytes?
    embedding/dimensions?
    image/max-pixels?
    audio/max-duration-ms?
    supports-seed?
    supports-json-schema?
    supports-logprobs?
    supports-cache-prefix?
    returns/plan?
  }

  policy {
    locality/class
    egress/class
    retention/profile
    trace/default-level
    sandbox/profile
    data-lease/required
    tool-policy/default
  }

  budgets {
    timeout/default-ms
    timeout/max-ms
    retry/max-attempts
    concurrency/max
    cost/class?
    rate-limit/ref?
  }

  health {
    probe/kind
    probe/interval-ms
    readiness/criteria
    liveness/criteria
  }

  security {
    requires-secret-ref?
    secret/scope?
    supply-chain/provenance-ref?
    allowed-model-hashes[]?
    disallowed-model-hashes[]?
  }

  conformance {
    fixture-set/ref
    last-report/ref?
    required-tests[]
  }
}
```

The manifest should be loaded from the host-owned module store or an equivalent
controlled space, not from an incidental directory. An adapter without a
manifest is not routable.

`protocol gate` is not a normal runtime adapter. It is a host-owned policy
component driven by `ProtocolProfileV1`. It may have its own policy/profile
manifest, but it should not be treated as an interchangeable provider worker.
An `evaluator` adapter is allowed, but only as a separate class with bootstrap
conformance and without authority to make itself routable.

## Adapter Lifecycle and Routability

An adapter should not be treated as binary state: present or missing. The host
should distinguish installation, configuration, health, conformance, and
routability.

Minimal lifecycle:

```text
AdapterState =
  Discovered
  | Installed
  | Configured
  | ConformancePending
  | Healthy
  | Routable
  | Degraded { reason }
  | Disabled { reason }
  | Revoked { reason }
  | Deprecated { replacement/ref? }
```

`Healthy` does not imply `Routable`. An adapter may answer a health probe and
still fail egress, retention, sandbox, conformance, secret, model hash, or
profile policy.

Route decision:

```text
AdapterRouteDecision =
  Routable { adapter/ref, runtime/ref, profile/ref, constraints }
  | NotRoutable {
      code:
        missing-manifest
        | invalid-manifest
        | conformance-missing
        | conformance-failed
        | runtime-unhealthy
        | policy-denied
        | egress-denied
        | sandbox-denied
        | secret-missing
        | model-hash-denied
        | deprecated
        | revoked
      remediation?
    }
```

The route decision should be visible through `inquirium.runtime.status`, without
leaking secrets or protected prompts.

## Provider Protocol Families

Adapters should be grouped by protocol family, not by provider brand.

`openai-compatible` means a family of runtimes that implement some subset of
common chat, completions, responses, or embeddings endpoints. Adapters in this
family must declare exactly which endpoints and fields are supported, because
compatibility is often partial.

`open-inference-protocol` is a family for a classical inference data plane,
especially where health, metadata, and inference endpoints matter across
multiple serving frameworks.

`command-stdio` means a local worker. It requires strict limits for process
lifecycle, stdout, stderr, timeout, cwd, env, lease paths, and sandbox.

`local-http` means a local model server without full compatibility with the
`openai-compatible` family.

`remote-http` means a remote API, always requiring an egress decision and secret
scope.

Two providers in the same family must not be assumed to support the same fields,
streaming behavior, tool calls, multimodal input, structured output, or usage
accounting. The adapter manifest must say this explicitly.

## Fail Closed When Resolving Profile and Runtime

Missing profile, missing candidate, missing configuration, unhealthy runtime,
policy denial, egress denial, or missing lease should all be separate rejection
classes. They should not degrade into "try the default model", because that
mixes convenience with authorization.

Runtime selection result:

```text
RuntimeSelection =
  Selected {
    runtime/ref
    profile/ref
    config/ref
    capabilities
  }
  | Rejected {
    code: missing-profile
        | no-runtime-candidate
        | runtime-not-configured
        | runtime-unhealthy
        | policy-denied
        | egress-denied
        | lease-denied
    candidate/ref?
    remediation?
  }
```

This type forces callers to handle rejection as part of the contract. `None`,
empty string, or a generic exception are too weak for an authorization boundary.

## Quality Contract, Switch-On, Model Profile, and Dispatch Policy

Quality-driven dispatch requires three separate decisions. Entangling them
creates most runtime confusion.

### Quality Contract: `done.must / should / score-min`

Every request should be able to declare when it is done:

```text
done:
  must[]         # closed required predicates: schema-valid, patch-applies, ...
  should[]       # soft predicates: tests-pass, no-hallucinated-refs, ...
  score-min?     # optional evaluator/judge threshold
```

`must` is fail-closed. Missing `must` means `Rejected` with a concrete
`failed-predicate`, not a silent retry. `should` is a quality target. Missing
`should` does not block acceptance, but it influences retry/repair decisions
and is visible in trace. `score-min` activates an evaluator path. Falling below
the threshold triggers retry, fallback, or repair according to dispatch policy.

Without this contract, "done" becomes adapter-specific and inconsistent.

### Switch-On: Configurable Failure Taxonomy

Each dispatch policy declares a closed list of failure classes that trigger
fallback to another runtime:

```text
dispatch/switch-on:
  - context-too-large
  - rate-limited
  - runtime-transient-unavailable
  - schema-invalid-repairable
  # provider/refusal intentionally absent: terminal by default
```

Classes outside this list must not automatically enter retry or fallback.
Dispatch policy should separate three decisions:

- `retry/current-runtime`;
- `fallback/other-runtime`;
- `fail/request`.

`provider/refusal` is terminal for the whole request unless policy explicitly
defines another interpretation, such as retry after a protocol profile change
or human review. This keeps "which failure should retry, fallback, or fail" in
configuration, not in adapter-specific code.

### Model Profile vs Dispatch Policy Profile

These are orthogonal axes.

| Axis | Decision |
| --- | --- |
| `model/profile-ref` | Selects model/runtime capability class, locality, cost tier, context window, and modalities. Chooses who executes. |
| `dispatch/policy-ref` | Selects retry, fallback, repair aggressiveness, `score-min`, hedging, and time budget. Chooses how hard to pursue quality. |

Three named dispatch policies cover most cases:

| Profile | Retries | Fallback hops | Score-min | Hedging |
| --- | --- | --- | --- | --- |
| `low-latency` | 0-1 | 1 | n/a | none |
| `balanced` | 2 | 2 | 0.65 | opt-in per intent |
| `high-quality` | 3 | 3 | 0.85 | hedging + race |

Callers may select model and dispatch policy independently:

```text
request:
  model/profile-ref: "local-small-fast"
  dispatch/policy-ref: "high-quality"
```

Profiles inherit declaratively through configuration tables, not code. A new
profile should be a config record, not a runtime branch.

## Request Pipeline as Explicit Stages

An Inquirium request should not flow directly from caller input to adapter. Each
request should pass through an explicit pipeline. This keeps adapters simple and
gives the host one control point for safety, retention, trace, and cost.

Minimal pipeline:

```text
1. admit_request
   - schema gate
   - caller capability
   - operation class
   - idempotency key

2. resolve_policy
   - purpose
   - profile/ref or capability class
   - locality/egress/retention/trace
   - budget and autonomy

3. resolve_inputs
   - inline inputs under size limit
   - artifact refs
   - dataset refs
   - leases
   - declared/detected MIME

4. protocol_gate.input
   - protocol profile
   - input rails
   - prompt-injection classification
   - context visibility

5. shape_context
   - selected context refs
   - redaction
   - instruction hierarchy
   - prompt/runtime representation
   - token estimates

6. select_runtime
   - candidates
   - health
   - adapter route decision
   - model/profile decision

7. invoke_adapter
   - timeout
   - cancellation
   - retries if allowed
   - streaming/backpressure if applicable

8. protocol_gate.output
   - schema validation
   - output rails
   - repair-once if policy allows
   - final projection

9. persist_effects
   - artifact manifest
   - provenance
   - usage
   - feedback events
   - metadata trace

10. return_outcome
    - Completed
    - Degraded
    - Rejected
    - Deferred
    - Cancelled
    - Failed
```

Every stage returns a typed outcome. The adapter starts work only after
authorization, policy, input resolution, protocol gate, and context shaping.

## Direct Data Plane Through Leases

The host does not need to proxy every large sample, image, audio file, dataset
shard, or tensor. It must remain the control plane: authorize the operation,
classify data, issue leases, select runtime, enforce sandbox, egress, budget,
retention, and trace, then record manifest, provenance, and status.

A lease should describe read and write scope separately, deadline, data class,
operation id, sandbox profile, egress policy, and allowed data resolver. The
worker receives a handle or scoped path after validation, not ambient
filesystem access. If direct data plane becomes common, it should enter the
Inquirium schema rather than living as an adapter exception.

## Artifact References Instead of Raw Paths

Inquirium should prefer `artifact/ref`, `dataset/ref`, and
`model-artifact/ref` over raw paths. A reference is typed and resolved by the
host. The worker sees only the validated result: scoped path, object handle,
query handle, or content-addressed manifest.

Resolution should depend on an explicit reference scheme:

- `artifact://...` resolves through the artifact registry;
- `dataset://...` resolves through the dataset registry;
- `file://...` resolves through lease paths;
- `inline://...` resolves through byte limits;
- `remote://...` resolves through the egress gate.

There is no universal "open whatever" resolver. Each source class has its own
safety rules.

## Byte Limits and Typed Input Errors

Input and output limits are part of the operation and profile contract:

- `max/input-bytes`;
- `max/output-bytes`;
- `max/context-tokens`;
- `read-idle-timeout-ms`;
- `mime/allowed`;
- `artifact/class`.

The limit is not a transport detail, because violating it affects safety, cost,
and determinism.

On overflow, the stream should be closed or cancelled and the whole operation
rejected. Silent prefix truncation is allowed only as an explicit transformation
policy with trace. Default semantics are: reject the whole input, destroy the
source, and record a metadata-only incident.

```text
read_with_limit(stream, max_bytes):
  total = 0
  for chunk in stream:
    total += len(chunk)
    if total > max_bytes:
      cancel_or_destroy(stream)
      return Rejected { code: too-large, size: total, max: max_bytes }
    append(chunk)
  return Completed { bytes }
```

## Sniffing and Input Classes Without Full Loading

Input type should be detected from a small byte prefix, declared header, or
manifest, not by loading the whole artifact into memory. For large data,
sniffing is an auxiliary classification, not proof. The final contract should
include `declared/mime`, `detected/mime`, `artifact/class`, and the policy
decision.

If declaration and detection conflict, the runtime should not decide which one
to trust. The host should return a typed rejection or route the operation to a
review path, depending on sensitivity class and profile.

## Atomic Artifact Writes

Inquirium outputs such as images, transcripts, embedding shards, model
adaptation artifacts, checkpoints, and metrics should enter the artifact store
through atomic writes. The pattern is: sanitize name, write a sibling temporary
file in the target directory, require exclusive create, compute hash, atomically
rename, then publish the manifest.

The manifest should include at least:

- `artifact/ref`;
- hash;
- byte size;
- MIME or artifact kind;
- `operation/id`;
- `runtime/ref`;
- `profile/ref`;
- `lease/id`;
- sensitivity class;
- retention profile.

TTL must not be a hidden cleanup rule. It should derive from retention policy
and be visible in provenance.

## Model Card, Training Job, and Eval Report as Required Adaptation Artifacts

If Inquirium creates a model adaptation artifact, checkpoint, LoRA/QLoRA
artifact, prompt program, or other model artifact, the result should not be just
a file. It should have a model card, training job record, and eval report.

Minimal relationships:

```text
TrainingJob {
  job/id
  base-model/ref
  method: lora | qlora | prompt-optimization | other
  dataset/refs[]
  protocol/profile-ref?
  policy/profile
  operator/ref
  status
  eval/report-ref?
  output/model-artifact-ref?
}

ModelCard {
  model-artifact/ref
  base-model/ref
  adapter/id?
  intended-use[]
  out-of-scope[]
  limitations[]
  excluded-data-classes[]
  known-risks[]
  evaluation/ref
  provenance/refs[]
  policy/profile
  deployment/scope
  status
}
```

Protocol Gate may generate `feedback/event` and `training-candidate` records,
but it must not adapt weights or publish model artifacts without a separate
`inquirium.train.adapt` operation and policy approval.

`inquirium.train.adapt` is idempotent by a deterministic key computed from
content-addressed inputs and the training environment, not loose refs. The
minimal key includes:

- `base-model/ref` as digest or verified model hash;
- `method`;
- `dataset-manifest/ref` and manifest hash;
- canonical sample ordering;
- `hyperparameters`;
- `seed`;
- `training-code/ref`;
- `training-code/hash`;
- runtime or container image digest;
- training toolchain version;
- policy profile;
- relevant feature flags.

Retrying the same training job with an identical key returns the existing
`model-artifact/ref` instead of producing a duplicate. The idempotency key is
sha256 over `canonical-json::JcsV1` of these fields. If any element changes,
the request is a new training job, even under the same caller-provided
`job/id`. The ledger returns an idempotency conflict instead of silently
publishing a second model artifact under the same alias.

### Dataset Manifest as Content-Addressed Artifact

A dataset used by `train.adapt` should have a manifest whose fields guarantee a
reproducible build:

```text
DatasetManifestV1 {
  manifest/ref
  dataset/refs[]
  split: train | valid | test
  counts {
    rows
    rows-by-label?
    rows-by-source-kind?
  }
  file-hashes[]
  filter-spec/ref
  time-window { from, to }
  redaction/audit {
    pii-replacements
    secret-strips
    rule-counters
  }
  config-snapshot-hash
  builder-version
  build-seed
}
```

Repeating the build with the same sources, filter spec, seed, and config
snapshot should produce an identical manifest: counts, file hashes, and audit
counters. Manifest mismatch for the same inputs is a pipeline bug, not noise.
CI should fail closed when the config snapshot hash changes from the last
accepted build unless the change is explicitly accepted.

### Promotion Gate as a Separate Operation

`inquirium.eval.gate` is a separate operation from `train.adapt`. It is never
implicit.

```text
PromotionGateRequestV1 {
  candidate/model-artifact-ref
  baseline/model-artifact-ref?
  eval/suite-refs[]
  thresholds {
    metric-name -> { min?, max?, regression-tolerance? }
  }
  blocking[]
  non-blocking[]
}

PromotionGateResultV1 {
  decision: accepted | rejected
  per-metric[] { name, value, baseline?, threshold, verdict }
  rejection-reasons[]
  report/ref
}
```

The report is deterministic. Replay should produce identical output. CLI or
automation wrappers should return non-zero exit code for `rejected`, enabling
CI integration. `rejection-reasons` is a closed enum, not a free-form string,
so operator dashboards can map it to actionable remediation.

## Event Stream with Correlation and Metadata

Inquirium should emit stable events:

- `request.started`;
- `runtime.selected`;
- `lease.issued`;
- `operation.deferred`;
- `usage.metrics`;
- `artifact.produced`;
- `request.failed`;
- `request.completed`.

Each event should include `session/id` when relevant, `operation/id`,
`attempt/seq`, timestamp, operation class, and a metadata-bounded payload.

Trace should answer: what happened, why, which input refs were used, which
policy applied, and which effects were produced. By default it must not contain
prompts, samples, audio, images, secrets, or full model responses. Richer trace
requires a separate grant, retention profile, and data classification.

## Trace Metadata and Trace Details

Trace should be structurally split into `trace/metadata` and `trace/details`.
Metadata is default, bounded, and exportable: duration, byte length, token
usage, selected runtime, denial code, lease refs, artifact refs. Details is
optional and may contain protected material only when policy, operator grant, or
caller grant allows it.

This is stronger than a list of fields not to log. The privacy boundary is a
data contract. Runtime adapters do not need to infer which fields are private;
they receive a decision: metadata-only or details-allowed with a concrete
retention profile.

## Event, Span, and Provenance Are Different Views

Inquirium should distinguish three causal accounting views.

Event is a discrete domain occurrence such as `request.started`,
`runtime.selected`, or `artifact.produced`.

Span is execution observability: duration, errors, retries, provider family,
model, token usage, and streaming status.

Provenance is the relation between entities: a request used artifact refs,
model, adapter, and dataset; an activity generated a result or artifact.

Minimal mapping:

```text
Inquirium request/operation = PROV Activity
Input artifact/context/dataset/model artifact = PROV Entity used
Output artifact/result/eval report = PROV Entity generated
Runtime adapter/model profile/operator/host policy = PROV Agent associated
Fine-tuned adapter/model-artifact = Entity derivedFrom base model + dataset
```

Trace metadata may contain refs and hashes. Trace details may contain protected
material only with a separate grant and retention profile.

## Tool Delegation as Policy

Model-backed inquiry may use tools, but tools are not ambient model
capabilities. Every operation should carry explicit `allowed/tools`,
`allowed/resources`, `disallowed/resources`, cost, deadline, and autonomy level.
Tool output is an input to inference or evidence artifact, not authorization to
mutate host state.

The tool list should be an enumeration of names or capability refs, not a regex
or "everything except" category. Example levels: `none`, `safe-read-only`,
`owner-approved`. A new tool class is denied until explicitly added to policy.

### Effects Are Orthogonal to Tools

`allowed/tools` answers which capability provider the model may call. It does
not answer which host effects are allowed. These are separate axes:

| Axis | Question | Scope |
| --- | --- | --- |
| `allowed/tools` | What may the model call? | Enumeration of capability refs. |
| `effects/allowed` | What host effect may happen? | Scoped grants such as `EffectGrant { kind, scope/ref, lease/ref?, destination/ref?, deadline, budget }`. |

`EffectGrant.kind` should be a closed enum, such as `fs/read`, `fs/write`,
`process/run`, `net/egress`, `identity/sign`, `agora/publish`, `ad/dispatch`,
or `none`. The `kind` is never sufficient by itself. Every grant needs a scope,
and where relevant a lease, destination, deadline, and budget.

Default effect allowlists are narrow:

```text
profile/default:
  effects/allowed: []

profile/safe-inference:
  effects/allowed:
    - { kind: fs/read, lease/ref: input-lease, scope/ref: request-inputs }

profile/training:
  effects/allowed:
    - { kind: fs/read, lease/ref: dataset-lease, scope/ref: training-inputs }
    - { kind: fs/write, lease/ref: artifact-output-lease, scope/ref: artifact-store }

profile/agent-bounded:
  effects/allowed:
    - { kind: fs/read, lease/ref: input-lease, scope/ref: request-inputs }
    - { kind: net/egress, destination/ref: approved-endpoint, budget: bounded }
```

Side effects require both a tool grant and an effect grant. A tool that can
write files requires `fs/write`, and that effect is valid only within its lease
and scope. This avoids granting a tool while accidentally allowing out-of-scope
effects.

## MCP and A2A as Bridges, Not Core Semantics

Inquirium may use agent protocols, but it should not import their semantics
into core. MCP and A2A are edge bridge adapters.

MCP bridge maps external resources, prompts, and tools to Orbiplex
`resource/ref`, `prompt-template/ref`, and `tool/ref`. It requires capability
negotiation before use; respects cancellation, progress, errors, and logging;
does not give the model ambient tool access; and sends every tool call through
`allowed/tools`, budget, deadline, trace, and output validation.

A2A bridge treats an external agent as an untrusted provider worker or remote
agent endpoint. It declares capability metadata, skills, and routability through
its manifest. It does not assume shared memory, shared secrets, or shared
policy. Its answer is candidate evidence. Each delegation carries an egress
decision, retention profile, data classification, and typed outcome.

```text
MCP = agent/tool bridge.
A2A = agent/agent bridge.
Inquirium Core = local host policy boundary.
```

The bridge may speak an external protocol. Core remains stratified, local, and
auditable.

## Autonomy Modes for Tool Results

Not every tool result should automatically trigger another model response.
Inquirium should separate:

- `tool-only`: tool result is an artifact and the operation ends;
- `single-turn`: one tool -> model -> result round is allowed;
- `multi-turn`: a controlled loop is allowed under max steps, cost, and time.

The model does not decide on its own that it may continue after each tool. The
host issues budget and step limits before effects.

## Protocol Gate

`Protocol Gate` is a host-owned policy boundary for communication with the
model. It is not a model, agent, or post-training process. If the component also
collects feedback for later adaptation, the name `Protocol Tutor` may be used
for the feedback/evaluation part only.

Protocol Gate performs four functions:

- context injection: protocol, role, session purpose, bootstrap instructions,
  and instruction hierarchy;
- input rail: accepts, rejects, or transforms input before the model;
- output rail: checks model response against protocol, schema, safety, and
  allowed actions;
- feedback recorder: records metadata about violations, repairs, and decisions
  as evaluation material or, with a separate grant, as training candidates.

Minimal profile:

```text
ProtocolProfileV1 {
  protocol/ref
  purpose
  role/ref
  instruction/hierarchy
  session/bootstrap
  turn/prefix-template?
  allowed/outputs
  disallowed/outputs
  response/schema-ref?
  refusal/schema-ref?
  tool-policy/ref?
  safety/profile
  retention/profile
  trace/profile
  revision/policy:
    none | repair-once | ask-model-to-revise-once | human-review
  feedback/policy:
    metadata-only | details-with-grant | training-candidate-with-grant
}
```

Input decision:

```text
ProtocolInputDecision =
  Accepted {
    shaped_request
    protocol/ref
    protocol/epoch
    instruction/hash
    cache/key?
  }
  | Rejected { code, reason, remediation? }
  | NeedsReview { review/ref, reason }
```

Output decision:

```text
ProtocolOutputDecision =
  Accepted { projected_result, protocol/score?, violations[] }
  | ReviseOnce { critique, revised_request }
  | Rejected { code, violations[], remediation? }
  | NeedsReview { review/ref, violations[] }
  | Degraded { fallback, reason }
```

The gate may start a session with a bootstrap prompt describing protocol,
purpose, roles, output format, and boundaries. It may add turn-level
instructions, but only through `context/shaping`, not through a private string
builder in the adapter.

For sessions with cache or KV state, include:

```text
protocol/epoch
instruction/hash
cache/policy
cache/key
kv-cache/ref?
kv-cache/lease?
```

Changing protocol, role, instruction, or material policy increments
`protocol/epoch` and forces a new bootstrap. This lets prompt-prefix caching,
session bootstrap, and later KV mechanisms coexist without pretending the model
has been trained.

Do not call ordinary accept/reject behavior by the gate "training" unless an
approved dataset is produced and a separate `inquirium.train.adapt` operation is
started. Runtime behavior here is protocol conditioning, context shaping,
output critique, or feedback recording. Training/adaptation begins only with a
dataset handle, `model-artifact/ref`, eval report, and separate grant.

## Instruction Hierarchy and Instruction Conflict

Inquirium should have its own explicit instruction hierarchy independent of any
provider format. The adapter maps that hierarchy to a provider representation,
but it must not flatten it without trace.

Proposed order:

```text
host-root policy
> organ policy
> operation policy
> protocol profile
> model profile
> caller purpose
> session bootstrap
> user/input messages
> retrieved context
> tool results
```

Conflicts resolve upward in the hierarchy. Tool results and retrieved context
are data, not instructions, unless the host explicitly transforms them into
instruction-bearing content.

`context/shaping` should emit:

```text
InstructionAssembly {
  instruction/hash
  hierarchy/version
  accepted_layers[]
  rejected_layers[]
  conflict/resolutions[]
  provider/rendered-form/ref?
}
```

## Prompt and Context Shaping as a Separate Stage

Prompt or runtime input construction should not be a private string builder in
the adapter. Inquirium should have a `context/shaping` layer that accepts the
question, messages, refs, context window, redaction profiles, style hints,
limits, and visibility policy, then returns admitted context, rejected refs,
token estimates, and runtime representation.

The contract separates:

```text
input data -> context selection -> redaction -> template -> runtime input -> result projection
```

Different runtimes may receive different formats, but callers see stable
semantics: which context was admitted and which part of the result may leave
Inquirium.

## Structured Output and Schema-Constrained Results

For `classify`, `transform`, `rerank`, tool planning, and protocol conformance,
Inquirium should prefer output contracts based on schema, not prompt wording.
JSON Schema or a local equivalent should be part of the request, profile, or
capability.

Model output passes through projection:

```text
OutputProjection =
  Parsed { value, schema/ref }
  | Plan { flow/ref, bindings? }
  | Stream { stream/ref, schema/ref? }
  | Refusal { reason, provider/refusal? }
  | Invalid { schema/ref, violations[] }
  | Repairable { violations[], repair-policy }
  | Unsafe { policy/ref, reason }
```

If an adapter/provider supports native structured outputs, the manifest should
declare that. If not, Inquirium may use parsing and repair-once, but repaired
output must remain marked in trace.

### Capability as Compiler: `Plan` as Candidate Return

`Parsed` and `Stream` are straightforward. `Plan` is less obvious and must be
treated as candidate Flow IR, not an executable command. An adapter may propose
a plan for a composite operation, but the host-owned Flow IR compiler/gate
decides whether the plan fits the original request contract.

Examples:

- `inquirium.transform` proposes classify -> reformat per branch;
- `inquirium.train.adapt` proposes redact -> split -> train -> eval -> gate;
- compound `inquirium.summarize` proposes chunk -> summarize each -> aggregate.

The host validates `Plan` through Flow IR schema gate, policy/budget check,
effect/tool grants, and plan limits: `max-depth`, `max-nodes`,
`max-tool-calls`, `max-cost`, `max-time`, and `no-implicit-recursion`.
Sub-operations must not exceed the original `operation`, `purpose`,
`allowed/tools`, `effects/allowed`, egress, retention, and policy. Callers do
not need to know sub-steps, but adapter authority must not widen.

Invariant: `Plan` as return requires the adapter manifest to declare
`returns/plan: true`. Without that, the host rejects a Plan response as
`Invalid`. Even with that capability, the plan remains `CandidatePlan` for host
acceptance, not a self-executing program.

## Token Estimation Before and After Context Assembly

Token limits should not be checked only on the final prompt. In long sessions,
the final prompt may be shorter than source state, while the runtime or session
layer still carries a larger context. Distinguish:

- input context space limit;
- session/transcript limit;
- tool result limit;
- final runtime input limit.

`context/shaping` should return multiple estimates and identify which estimate
is authoritative for rejection:

```text
TokenCheck =
  Accepted { assembled_tokens, source_tokens, tool_tokens }
  | Rejected {
      code: context-too-large
      max_tokens
      assembled_tokens
      source_tokens
      tool_tokens
    }
```

## Projection Mode for Long-Lived Sessions

Long-lived sessions need an explicit context projection mode. `per-turn` means
each operation receives a fresh complete prompt or runtime input.
`session-bootstrap` means the host injects context once for an epoch and later
steps send only deltas. Epoch change forces context reload.

This supports runtimes with session memory, prompt cache, or conversation state
without exposing those mechanics to callers. The caller sees `session/id`,
`context/epoch`, and retention policy, not backend mechanics.

## Prompt Cache and KV Cache as Controlled Resources

Prompt prefix cache, session state, and KV cache should not be treated as hidden
model memory. In Inquirium, they are controlled session resources.

Minimal fields:

```text
CachePolicy {
  cache/class: none | prompt-prefix | kv | provider-managed
  retention/max-age-ms
  scope: operation | session | protocol-epoch | profile
  key/material:
    instruction/hash
    protocol/epoch
    context/hash
    model/ref
    adapter/ref
  privacy/class
  evict/on-policy-change: true
}
```

Cache hit/miss should be metadata trace, not an adapter detail. If the provider
maintains its own cache, the adapter must declare that in the manifest and
return usage metadata when available.

## Streaming and Sessions as a Separate Operation Class

Streaming audio, realtime transcription, live multimodal interactions, and
interactive tool use should be modeled as `session operations`, not blocking
requests. Minimal lifecycle:

```text
created -> ready -> streaming -> completed | cancelled | failed
```

Every transition should be a trace event with a typed reason.

Minimal session contract:

- `session/id`;
- `operation/id`;
- `transport/class`;
- `input-sink policy`;
- `output-sink policy`;
- `cancel semantics`;
- `usage metrics`;
- `close reason`;
- `retention profile`.

Cancellation has at least two levels:

- `interrupt-output`, which stops current output;
- `terminate-session`, which ends the whole operation.

## Backpressure and Output Sink Availability

Streaming operations should check whether the output sink still exists and can
accept data. If the sink is closed, the runtime should not continue producing
expensive output without a policy decision. This matters for audio, video, and
multimodal streams, where missing backpressure quickly becomes cost and privacy
risk.

Session contracts should distinguish:

- `sink-closed`;
- `transport-closed`;
- `provider-closed`;
- `policy-cancelled`;
- `operator-cancelled`.

These classes matter for retry, accounting, and diagnostics.

## Inquirium Flow IR: Flow as Data

Inquirium should not become a general workflow engine, but it should have a
small flow representation for multi-step operations: guard -> context selection
-> model -> tool -> validation -> artifact -> review. Such representation
helps debug, replay, test, and move execution into bounded deferred operations.

Minimal model:

```text
InquiryFlowV1 {
  flow/id
  operation/id
  purpose
  nodes[]
  edges[]
  budgets
  policy/ref
  trace/ref?
}

FlowNode =
  InputNode
  | PolicyDecisionNode
  | ProtocolGateNode
  | ContextShapingNode
  | RuntimeSelectionNode
  | ModelInvocationNode
  | ToolInvocationNode
  | HumanReviewNode
  | ArtifactWriteNode
  | EvaluationNode
  | OutputProjectionNode

FlowEdge =
  depends-on
  | consumes
  | produces
  | guards
  | delegates-to
  | resumes-from
  | retries-after
  | derives-from

NodeState =
  Pending
  | Running
  | Completed
  | Rejected
  | Degraded
  | Deferred
  | Cancelled
  | Failed
```

By default, flow is a DAG. Controlled agent loops are allowed only as a
`bounded controller` with `max_steps`, `max_cost`, `max_time`, `allowed_tools`,
`termination_condition`, and explicit review policy. Anything with dependency,
cost, retry, tool call, or output artifact should exist as a node/edge in Flow
IR rather than hidden call stack.

## Adapter Conformance Before Routability

An adapter may be installed without being routable. It should not become
routable without a minimal conformance report. Conformance tests should be
generated from the manifest and fixture set.

Minimal report:

```text
AdapterConformanceReportV1 {
  report/ref
  adapter/ref
  adapter/version
  runtime/ref?
  fixture-set/ref
  generated-at
  outcome: passed | failed | partial
  tests[] {
    name
    operation
    outcome
    failure/class?
    trace/ref?
  }
}
```

Minimal test classes:

- schema gate;
- provider mapping;
- refusal mapping;
- timeout and cancellation;
- retryable vs terminal failures;
- streaming chunks;
- backpressure and sink-closed;
- structured output;
- tool call denial;
- allowed tool call;
- trace redaction;
- egress denied;
- lease denied;
- model hash allowed/denied;
- idempotency/replay;
- cost/token usage accounting when declared.

## Eval Before Route

A new adapter, protocol profile, or model profile should not automatically enter
the production routing pool. It should pass minimal evals first.

For an adapter:

- conformance fixtures;
- mapping errors;
- refusal mapping;
- redaction tests;
- latency/budget smoke test;
- cancellation/retry test.

For a protocol profile:

- protocol-following fixtures;
- prompt injection fixtures;
- refusal fixtures;
- schema-valid output fixtures;
- over-answering and under-answering fixtures;
- tool-use denial fixtures.

For a model adaptation artifact:

- base eval report;
- protocol conformance eval;
- regression against safety fixtures;
- data provenance check;
- model card update.

Routing policy may admit a profile in modes such as `canary`, `owner-only`,
`local-only`, `metadata-trace-only`, or `disabled`.

An `evaluator` adapter is itself model-backed and must not evaluate itself.
Evaluator adapters bootstrap through deterministic offline fixtures:
rule-based, schema-only, regex/AST-level fixtures that can be verified without
calling another model. Only this fixed fixture set may grant evaluator
`Routable` state. Model-evaluates-model becomes allowed only after this step
and with explicit `evaluator/provenance-ref` pointing at the evaluator
conformance report.

### Constitution and Critic as Data

An evaluator needs two data shapes whose contracts are stable across
implementations:

```text
ConstitutionV1 {
  constitution/ref
  rules[] {
    rule/id
    kind: schema | predicate | rubric
    severity: must | should | nice
    description
    spec/ref
  }
  scoring/policy?
}

EvaluationResultV1 {
  evaluation/id
  evaluator/ref
  constitution/ref
  target/ref
  pass: true | false
  score?
  per-rule[] {
    rule/id
    verdict: pass | fail | skipped
    reason?
    evidence/ref?
  }
  reject-or-repair?
}
```

Constitution is data, not code. It can be changed without rebuilding the
evaluator. If a rule points to a predicate ref, that predicate must come from a
signed, host-owned registry with versioning, conformance, and explicitly
declared effects. Adapters and protocol profiles must not provide arbitrary
code as predicates.

Critic is an evaluator invoked automatically after inference. It returns
`EvaluationResultV1`, which the host uses for retry, repair, or fallback under
the quality contract. Per-rule audit trails go through trace details with a
separate grant, or through trace metadata as verdict summary without evidence.

This makes "the evaluator applies some rules" a declarative contract. Operators
can see which rules failed and change constitution data without rewriting
evaluator code.

## Threat Matrix for Model-Backed Inquiry

Every new operation and adapter should pass through a small threat matrix. This
is not a full formal security analysis of Orbiplex, but a minimum hygiene check
for model-backed inquiry.

```text
Prompt injection
  -> context separation, instruction hierarchy, input rails, tool isolation

Insecure output handling
  -> structured output, output projection, sandboxed side effects, no authority

Training/data poisoning
  -> dataset provenance, model card, eval report, operator grant

Model denial of service
  -> token/byte/time/cost budgets, concurrency caps, cancellation

Supply chain risk
  -> adapter manifest, module provenance, model hash allow/deny, model cards

Sensitive information disclosure
  -> metadata-only trace, redaction, retention profile, egress gate

Insecure plugin/tool design
  -> allowed/tools enumeration, tool call policy, no ambient capabilities

Excessive agency
  -> autonomy level, max steps, human review, no self-authorizing agents

Overreliance
  -> model output as candidate evidence, downstream policy decides

Model theft / model artifact leakage
  -> model-artifact refs, scoped leases, egress control, artifact retention
```

Every threat should have at least one negative fixture in conformance or
acceptance tests.

## Fallbacks as Degraded Results

Fallback is not successful inference. If the model produced no result, the
operation was interrupted, the runtime was unavailable, or output could not be
projected, the outcome should be `degraded`, `rejected`, `cancelled`, or
`failed`, not `completed`.

Practical shape:

```text
InquiriumResult =
  Completed { payload, usage, model/used }
  | Degraded { fallback, reason, failure/class?, runtime/used? }
  | Rejected { code, message, remediation? }
  | Deferred { operation/id, status/ref }
  | Cancelled { reason }
  | Failed { error/class, retryable }
```

Downstream can then distinguish candidate evidence, fallback text, policy
denial, asynchronous operation, and failure. This is required for auditability
and reliable automation.

## Typed Outcomes for Every Boundary

The same sum-type result pattern should apply to runtime selection, lease
resolution, input validation, context shaping, inference execution, artifact
write, and trace emission. Each boundary returns a closed set of variants, not
a loose text error.

```text
BoundaryResult =
  Accepted { value, metadata }
  | Degraded { value?, reason, diagnostics/ref? }
  | Rejected { code, reason, remediation? }
  | Deferred { operation/id }
  | Cancelled { reason }
  | Failed { class, retryable, diagnostics/ref? }
```

Rejection, retry, and degraded mode are part of the contract, not exceptions
hidden in control flow.

## Appendix: Lease Path and Artifact Store Hardening

### Structural Lease Path Validation

Lease path validation should not be a regex over raw strings. A safer pipeline:
canonical normalization, reject empty values, NUL, root paths, drive roots, and
special segments, split into segments, then compare to an explicit list of
allowed patterns. Wildcard, if allowed, should operate at segment level, not as
arbitrary glob.

```text
validate_lease_path(candidate, allowed_roots):
  path = normalize_absolute_path(candidate)
  reject if path is empty, root, contains NUL
  segments = split_path_segments(path)
  reject if segments contain "." or ".."
  return any(root_pattern_matches_segments(root, segments)
             for root in allowed_roots)
```

This style resists bypasses through `//`, `..`, `./`, mixed separators, and
encoded characters. Lease path validation failure is a terminal rejection, not
a reason to expand roots dynamically.

### Validate Identifiers Before Building Paths

Every external identifier used to build a path should be validated before it is
joined with a base directory. This applies to `artifact/id`, `dataset/id`,
`model-artifact/id`, `lease/id`, `operation/id`, and auxiliary names from user
input or runtime output.

Minimum segment rules:

- non-empty;
- no `/`;
- no `\`;
- no NUL;
- not `.`;
- not `..`;
- bounded length;
- stable character set or explicit sanitizer.

This is boundary validation, not cleanup after path construction.

### Temporary Files as Contract, Not Trash

The artifact store temporary directory should have explicit rules: minimum file
age before cleanup, no deletion of active operations, idempotent cleanup, and
scope limited to the store-controlled directory. If cleanup races a write, the
write path may recreate the directory and retry once, but it must not mask
errors such as out-of-space.

This improves post-failure reasoning. After restart, the host can distinguish
complete artifacts from temporary leftovers, and the operator can see what is
safe to remove.
