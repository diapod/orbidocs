# Proposal 064: Inquirium Implementation Recommendations

Based on:
- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `node/DEV-GUIDELINES.md`

Applies to:
- `doc/project/60-solutions/044-inquirium/044-inquirium.md`
- `doc/project/60-solutions/045-inquirium-assistant-channel/045-inquirium-assistant-channel.md`

## Status

Accepted implementation recommendations

## Date

2026-05-20

## Executive Summary

This proposal preserves the implementation recommendations behind Solution 044
Inquirium, promoted from Proposal 063, and the shared invariants used by
Solution 045 Inquirium Assistant Channel. It remains an implementation-guidance
document, not a separate solution component. The goal is to keep Inquirium as a
small, host-owned policy boundary for model-backed inquiry while allowing many
replaceable runtime adapters, protocol gates, evaluators, tool bridges, agent
bridges, and model adaptation artifacts to evolve around it.

The core rule is:

```text
Inquirium Core owns semantic operations and policy.
Adapters translate execution details.
model-runtime owns lifecycle, health, supervision, and transport mapping.
Provider workers execute inference but hold no Orbiplex authority.
```

Adapters may be middleware-hosted, but middleware hosting is an implementation
axis, not an authority grant. A middleware-hosted adapter remains an Inquirium
runtime adapter with a narrow role.

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

`middleware-hosted runtime adapter` is a runtime adapter implemented through the
Orbiplex middleware hosting fabric. Its executor may be `command_stdio`,
`local_http_json`, supervised `http_local_json`, an in-process handler, or a
later compatible executor. This says how the adapter runs; it does not widen what
the adapter may do.

## Adapter Hosting and Authority Axes

Keep adapter hosting separate from adapter authority. A runtime adapter may be
delivered as an operator-installed package, a bundled module, an in-process
component, a one-shot command, an unmanaged local HTTP endpoint, or a supervised
local HTTP service. Those shapes answer "how does it run?".

The semantic role answers a different question: "what may this component do?".
An Inquirium runtime adapter may translate requests, invoke a selected provider
worker, map provider responses into Inquirium outcomes, report health, expose
conformance metadata, and use explicitly granted lease/artifact/status
capabilities. It must not claim arbitrary middleware hooks, own workflow
dispatch, choose model policy outside the host decision, mutate Orbiplex state,
or turn provider-specific behavior into public Inquirium semantics.

Practical classification:

| Axis | Field or decision | Meaning |
| --- | --- | --- |
| Hosting | `hosting/kind` and optional middleware executor config | Process, transport, lifecycle, and packaging shape. |
| Adapter role | `adapter/kind`, `operations[]`, protocol family | Which Inquirium execution surface is translated. |
| Authority | `effects/allowed`, leases, egress, sandbox, conformance | What side effects and data paths are allowed for this adapter instance. |

Use the least powerful executor that can express the behavior. A pure mapping can
be declarative. A one-shot local command can use `command_stdio`. A long-lived
local model server usually belongs behind `local_http_json` if supervised
elsewhere, or supervised `http_local_json` when the Node host should own
readiness, restart, shutdown, and module reporting.

## Adapter Implementation, Instance, and Runtime Candidate

Do not use "adapter" for every layer. The implementation should distinguish:

| Layer | Meaning | Typical cardinality |
| --- | --- | --- |
| `adapter/ref` | Reusable code/package for one protocol family or execution interface. | One implementation can support many instances. |
| `adapter.instance/ref` | Configured and optionally supervised use of that implementation: endpoints, credentials, pools, queues, lifecycle, health, rate limits. | One instance can expose many runtime candidates. |
| `runtime/ref` | Host-visible routable execution candidate: adapter instance plus model binding, operation support, policies, health, and conformance. | One runtime candidate should point to one model binding. |
| `runtime.instance/ref` | Materialized live process, loaded model, session, or worker created by host/model-runtime supervision. | Zero or more live instances may back one runtime candidate. |
| `model.binding/ref` | Provider-facing model handle plus `model/ref`, digest/hash where available, default parameters, and constraints. | One binding may be reused by compatible runtimes, but policy may still split them. |
| `profile/ref` | Caller-facing policy class for model use. | One profile can select among many runtime candidates. |

The rule is: **adapter per interface, adapter instance per lifecycle/trust
boundary, runtime candidate per model-configuration**. Do not create one adapter
implementation per model unless protocol, trust boundary, isolation, or response
normalization differs. Do not hide two routable models inside one runtime
candidate merely because they share one server process or API standard.

Examples:

```text
adapter/openai-compatible-http
  adapter.instance/remote-provider-a
    runtime/remote-provider-a-small-chat
      model.binding/provider-a-small-chat
    runtime/remote-provider-a-large-chat
      model.binding/provider-a-large-chat

adapter/local-http-model-server
  adapter.instance/local-gpu-server
    runtime/local-gpu-server-llm-a
      model.binding/llm-a
    runtime/local-gpu-server-llm-b
      model.binding/llm-b
```

The adapter instance may maintain shared HTTP clients, connection pools, queues,
backpressure state, or a supervised server process. Those are performance and
lifecycle mechanisms. The host and `model-runtime` still select a `runtime/ref`,
not a hidden model inside the adapter.

Spawning follows the same rule. An adapter may implement `load`, `spawn`,
`unload`, or `pool` mechanics, but the decision to materialize a routable
runtime belongs to host-owned policy and `model-runtime`. A successful spawn or
load produces an explicit `runtime.instance/ref` or updated runtime candidate
state with health, model identity, resource budget, and conformance visible to
Inquirium.

## Correspondence With Common Agent-Orchestrator Layering

Existing agent orchestrators commonly separate provider configuration, model
selection, execution backend, and interaction channel. Inquirium should treat
that as a useful implementation pattern, not as its domain model. The mapping is:

| Common orchestrator layer | Inquirium / Orbiplex layer |
| --- | --- |
| Provider configuration, auth, discovery, endpoint defaults | `adapter/ref` plus `adapter.instance/ref` |
| Provider-facing model id and per-model defaults | `model.binding/ref` |
| Execution backend, local service, CLI wrapper, remote API client, worker pool | `runtime/ref` and `runtime.instance/ref` |
| Conversation channel, chat ingress, UI, messaging bridge | Host, Flow, Arca, Sensorium, or middleware outside Inquirium |

This correspondence is intentionally not one-to-one. A provider-style adapter
instance may expose many runtime candidates. A runtime candidate should still
name one model binding and one policy bundle. A channel should not become the
place where model selection, data leases, or inference policy are hidden.

When importing ideas from orchestrator designs, keep the invariant:

```text
provider mechanics are adapter concerns;
model identity is a model-binding concern;
routable execution is a runtime-candidate concern;
conversation orchestration is not an Inquirium adapter concern.
```

The practical benefit is reuse without flattening. One adapter implementation can
support multiple configured instances, one instance can reuse clients, process
supervision, queues, and caches, and the host can still audit and select each
routable model configuration explicitly.

## Agent Loop Lives Above Inquirium

The agentic mode — a stateful entity that binds a model, remembers a session,
holds parameters, and can be spawned, forked, or stopped — is a real need, but it
is **not** an Inquirium concern. It lives in the Agent organ (Proposal 073),
which sits above Inquirium and composes it: the Agent calls `inquirium.generate`
(and future operations) as an ordinary host-capability caller, and Inquirium
holds no knowledge of agents. This keeps the Proposal 063 invariant intact —
"Inquirium is not the agent loop" — while giving the loop a durable, host-owned,
bounded home. The Flow IR `bounded controller` defined later in this proposal is
the seed of that contract; the Agent organ generalizes it into a durable,
addressable, forkable entity with monotone-narrowing spawn, enforced budget, and
no self-authorization.

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
  adapter/ref   # implementation/package identity
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
  hosting/kind:
    in-process
    | middleware-hosted
    | external-endpoint
  middleware/executor?:
    in_process
    | command_stdio
    | local_http_json
    | http_local_json
    | json_e_flow
  implementation/ref?

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

The adapter manifest is implementation-level unless it explicitly states
otherwise. Adapter instance configuration and runtime candidate configuration
should be separate records owned by host/model-runtime configuration:

```text
InquiriumAdapterInstanceV1 {
  adapter.instance/ref
  adapter/ref
  hosting/kind
  lifecycle/config
  endpoint/config?
  auth/ref?
  egress/policy-ref?
  resource/policy-ref?
  health/config?
  pools/config?
}

InquiriumRuntimeCandidateV1 {
  runtime/ref
  adapter.instance/ref
  model.binding/ref
  profile/refs[]
  operations[]
  defaults/params
  policy/refs
  conformance/ref?
  health/status
}

InquiriumModelBindingV1 {
  model.binding/ref
  model/ref
  provider/model-name
  model/hash?
  defaults/params
  constraints
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

## Embedding Operation Contracts

`embed` and `batch.embed` should be modeled as separate operation contracts, not
as hidden variants of chat generation. A direct `embed` request accepts bounded
inline text inputs and returns bounded inline vectors:

```json
{
  "schema": "inquirium.embed.request.v1",
  "operation": "embed",
  "model": "provider-facing-model-name",
  "input": { "texts": ["alpha", "beta"] },
  "parameters": {
    "dimensions": 384,
    "normalize": true,
    "encoding_format": "float"
  },
  "metadata": {}
}
```

The matching `inquirium.embed.response.v1` carries `vectors[]` with stable
source indexes, a required `dimensions` field, provider-neutral `usage`, and
redacted `diagnostics`. Implementations must reject zero dimensions, empty
inputs, dimension mismatches, and non-finite vector values. Embeddings inherit
the retention and egress boundary of their source material; they are derived
content, not neutral telemetry.

`batch.embed` uses direct data-plane leases. The request carries
`source_lease_refs[]` and an optional `output_lease_ref`; `source_lease_refs[]`
is bounded and duplicate-free so one lease cannot be accidentally or
maliciously counted twice. The response returns
`inquirium.batch-embed.response.v1` with an `artifact_ref`, `dimensions`,
optional `item_count`, optional digest, usage, and diagnostics. The host remains
responsible for issuing leases, validating the produced artifact, writing it
through the object store, and binding provenance to `runtime/ref`,
`model.binding/ref`, and the operation id. Local file leases are canonicalized
against allowlisted roots, remote runtimes never receive raw `file://` leases,
and allowlisted file roots must not themselves be symbolic links.

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

### Operational Caution Is a Host-Owned Prompt Layer

When admitted context describes an enacted Sensorium resource, its owning source
may publish `sensorium-operational-context.v1` through P082. Inquirium does not own
that vocabulary and adapters do not interpret it. The daemon composition root first
validates the exact context through the source-domain resolver, applies a local
monotone policy floor, and gives `PromptAssemblyPolicyProvider` a host-authored
operation layer derived from the closed impact class.

The renderer is deterministic, versioned, and golden-tested. It may tell a model,
for example, that a `production` source represents a live service and therefore
diagnosis should prefer observation, reversible proposals, and explicit effect
authorization. It must not copy a publisher-authored summary into a privileged
instruction, infer grants, or claim that model caution replaces host enforcement.
`critical` is stricter than `production`; lower layers and adapter-instance
adjustments cannot remove or weaken either layer.

Prompt assembly records each source class with its exact context digest, the local
policy ref and floor, selected class, rendered layer id, and resulting instruction
hash without recording the source payload or free-text summary. The host passes that
selection directly into the durable Inquirium trace rather than reconstructing it
from caller metadata or provider output. If the operation depends on a collaborative live feed
and the context is absent, stale, malformed, or inconsistent with the immutable
interface publication, assembly fails closed before adapter invocation. For multiple
feeds, the host renders the maximum class and retains all source qualifier refs in
metadata. This is context shaping, not a new Inquirium capability or adapter field.

Here `stale` has exactly the P082 meaning: the bound source generation is no longer
current or the interface publication was superseded for its source/projection slot.
Inquirium does not add a wall-clock TTL or another freshness heuristic. It consumes
only source-domain-admitted evidence. The optional publisher summary remains bounded
by P082 to 512 UTF-8 bytes and inert below the privileged instruction hierarchy.

## Configurable Prompt Assembly Policy

The instruction hierarchy above defines *precedence*; this section defines
*where each layer is configured* and *who may adjust it*. Today the daemon
assembles the adapter body essentially from `request.turns` plus
`max_tokens/temperature/top_p`. There is no host-owned layer that says "always
send X before (or after) every prompt", configurable once for the whole organ
and explicitly narrowed or extended per adapter. The correct shape is not a
prefix/suffix string inside the adapter — that leaks policy and audit into the
execution layer — but a host-owned assembly stage that hands the adapter an
already-rendered, explicit message stack.

### Layered Configuration Sources

Prompt assembly is configured as data, composed in increasing specificity:

```text
host-root prompt policy        (built-in, non-droppable)
> organ prompt policy          (Inquirium-owned defaults)
> operation prompt policy      (per generate/classify/transform/...)
> protocol profile             (protocol/model family adjustments)
> model-binding adjustment     (provider/model compatibility tweaks)
> adapter-instance adjustment  (per running adapter instance)
> caller turns + context       (request body)
```

A global Inquirium config provides the default policy. Profiles, model bindings,
and adapter instances do not redefine it; they reference it and may only apply
bounded adjustments. This keeps stratification intact: a change in the host-root
or organ policy propagates downward, while lower scopes specialize without
subverting policy.

### Monotone Adjustment Rule

Each lower scope may only do what the parent layer explicitly permits:

- **append** new layers into slots the parent marked `extendable`;
- **narrow** (drop or shorten) layers the parent marked `narrowable`;
- never edit, reorder, or remove layers marked `required`/`fixed`;
- never insert a layer above `host-root` or `organ` policy.

This mirrors the `ClassKeyed`/`ModeKeyed` monotonicity discipline (P066): an
adjustment can make the instruction stack stricter or more specific for one
adapter, never weaker than the host root. A rejected adjustment is recorded, not
silently dropped.

### `PromptAssemblyPolicy` Contract (`inquirium-core`)

The configured policy (input) is distinct from `InstructionAssembly` (the trace
output). `inquirium-core` should own the input contract:

```text
PromptAssemblyPolicy {
  protocol/epoch
  layers[] : PromptLayer
  caps {
    max-layers
    max-instruction-tokens
    allowed-roles[]            # system | developer | user | assistant
    adjustable-by[]            # which lower scopes may extend/narrow
  }
}

PromptLayer {
  layer/id
  origin                       # host-root | organ | operation | profile
                               #   | model-binding | adapter-instance
  position                     # preamble | postamble
  role                         # system | developer | user | assistant
  content/ref | text
  class/key?                   # ClassKeyed selector (P066), optional
  required                     # host-root/organ layers are non-droppable
  adjust                       # fixed | extendable | narrowable
}
```

Lower scopes use `PromptAssemblyPolicyAdjustment`, not a second full policy:

```text
PromptAssemblyPolicyAdjustment {
  narrow/layer-ids[]           # may remove only parent layers marked narrowable
  extend/layers[]              # new layers owned by the adjustment scope
}
```

The daemon resolves adjustments in increasing specificity: selected
`profile/ref`, selected `model.binding/ref`, then selected
`adapter.instance/ref`. An extended layer must declare the origin matching its
catalog scope, so an adapter instance cannot mint a `host-root` layer. A
narrowing attempt against `fixed`, `required`, or merely `extendable` layers is
rejected fail-closed. A single scoped adjustment may append at most 32 layers in
the foundation implementation, keeping misconfigured catalogs from producing
unbounded prompt-policy expansion at startup or invocation time.

`position` is what makes "always send before / after the prompt" first-class:
`preamble` layers render ahead of caller turns, `postamble` layers (output
contract, refusal reminders, format guards) render after them.

`layer/id` values are unique within one resolved policy. Duplicate layer ids are
configuration errors, not last-writer-wins overrides. `content/ref` is a
pre-materialization handle: `inquirium-core` can assemble it only when the host
passes an explicit resolver, so unresolved content refs fail closed as
`content-not-materialized`.

The ownership split is deliberate. `inquirium-core` owns the contract and a pure,
dependency-light resolver/renderer for layer ordering, monotone adjustment
validation, cap enforcement, role-fold decisions, and instruction hashing. The
daemon owns configuration loading, runtime/profile/model-binding lookup, adapter
capability lookup, operation admission, and trace writes. This keeps
`inquirium-core` free of daemon, HTTP, SQLite, async-runtime, and model-runtime
dependencies. It may use shared contract utilities such as canonical JSON
serialization for stable digests. This still prevents each adapter or daemon
route from reinventing prompt rendering.

Host-root caps such as `max-layers`, `max-instruction-tokens`, required layer
ids, and non-droppable host-root/organ layers are stamped by host-root policy and
cannot be widened by operation, profile, model-binding, adapter-instance, or
caller configuration.

### Daemon Assembly Stage

A host-owned assembly stage runs **before** `inquirium_generate_adapter_body`.
It resolves the effective policy (global default + permitted adjustments for the
selected profile/model-binding/adapter-instance), applies `ClassKeyed` selection
against the request classification, enforces `caps`, and renders an explicit,
provider-neutral message stack:

```text
AssembledPrompt {
  messages[]                   # explicit, role-tagged, ordered
  instruction/hash
  protocol/epoch
  hierarchy/version
  caller-turns/count
  accepted_layers[]            # + content/source: inline-text
                               #   | resolved-content-ref
  adapted_layers[]             # + rendered_as: layer kept but re-rendered to a
                               #   supported role/format (e.g. developer -> system)
                               #   + content/source
  rejected_layers[]            # + reason: cap-exceeded | narrowed-away
                               #            | override-denied
}
```

`instruction/hash` is computed over NFC-normalized canonical JSON for the
host-owned instruction material, accepted/adapted layer identity, content source,
and the caller turn count. It deliberately does **not** hash caller text or
rejected layers; audit/replay must supply caller turns separately and use the
accepted/adapted/rejected layer lists to explain the assembly decision. NFC
normalization is part of the prompt-assembly hash profile because prompt layers
are human-authored text that may arrive from different editors, clipboards, and
operating systems with different Unicode composition behavior.

Prompt instruction caps are enforced with a deterministic host estimator rather
than a provider tokenizer in this foundation slice: non-whitespace Unicode scalar
values are counted as approximately one token per four characters, rounded up.
This is a bounded approximation for admission and audit, not a claim that every
adapter uses the same tokenizer. Adapter-specific tokenizers and exact metering
belong to the later budget/metering layer.

`inquirium_generate_adapter_body` then consumes `AssembledPrompt.messages`
instead of raw `request.turns`. Prompt assembly applies only to instructional and
generative operations; the assistant-turn surface reuses this stage. `embed` does
**not** run text assembly: adding a preamble or postamble to embedding input
changes the vector and breaks the "embed this exact input" contract, so embedding
may consume only the policy, metadata, and trace parts of the stage. Any required
transformation of embedding input is a separate, explicit pre-processing
operation, never an implicit instruction layer.

Caller turns are inserted after preamble layers and before postamble layers in
their original order. Empty caller turns are legal only for operation/profile
contracts that explicitly allow a no-input inquiry, such as a health or
conformance fixture; ordinary `generate` requests still require at least one
caller turn at the request schema boundary. The boundary is represented in the
trace by `caller-turns/count`; host prompt layers remain separate turns around
the caller range, while caller content is not copied into prompt-assembly trace
metadata.

### Adapter Contract

The adapter receives the assembled `messages` plus `instruction/hash` and
`protocol/epoch`, and only maps them to the provider wire format. The adapter
**must not** append hidden instructions. If the manifest does not declare a role
(for example `developer`), the host folds that layer into the nearest supported
role (typically `system`) and records it in `adapted_layers[]` with `rendered_as`
— the instruction is still sent, only re-rendered, so this is adaptation, not
rejection. `rejected_layers[]` is reserved for layers actually dropped
(cap-exceeded, narrowed-away, override-denied). The adapter manifest declares
`supports/instruction-roles[]` so folding is a host decision, not an execution
detail.

Implementation note: the daemon projects the signed adapter-manifest role
claim into the typed model-runtime catalog as `adapter_implementations[*].
instruction_roles`. If prompt layers exist and a selected adapter implementation
has no declared instruction roles, prompt assembly fails closed instead of
assuming an all-role adapter.

This makes the always-before/always-after content auditable end to end: one
`instruction/hash` per request, a stable `protocol/epoch`, and an explicit
accepted/adapted/rejected layer list, with no policy living inside the adapter.

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

Foundation implementation note: the first implemented slice is intentionally
smaller than the full schema engine. It carries `output_contract.schema/ref`,
chooses a resolved enforcement tier from adapter declarations, forwards the
contract to the adapter, and validates that returned structured output carries
the requested `schema/ref`, stays within host JSON shape limits, and validates
against a host-owned output schema registry using a deliberately narrow JSON
Schema subset (`type`, `required`, `properties`, `items`, `enum`, `const`,
`additionalProperties`, and basic scalar/array/object bounds). Unsupported JSON
Schema keywords fail closed. Per-schema policy must explicitly allow provider-native
schema enforcement before the host may select a native tier, while repair policy
remains fail-closed until an explicit repair loop exists. It does not yet compile
grammars, support dynamic refs/recursion/combinators, map provider-native schema
engines, or perform repair attempts.
When validation fails, the host returns an `invalid` projection with violations
rather than passing the output as text. The foundation `OutputProjection` also
admits `Text` to make the no-structured-contract path explicit in traces.
`Plan`, `Stream`, `Repairable`, and `Unsafe` remain reserved for later slices
that add Flow IR admission, streaming cursors, repair loops, and rails policy.

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

## I/O Contract: Output Schema, Dialect, and Capability Negotiation

The projection above is the *result* contract. This section makes the
surrounding I/O behavior — how a schema is broadcast, reminded, validated,
pre-parsed, and how the model is asked to communicate — a host-owned data
contract too, so adapter authors declare capabilities and the host chooses
strategy. The goal is faster adapter authoring and typed data at the boundary,
without each adapter reinventing prompt shaping, parsing, or validation.

Each mechanism below pairs a contract with a short note on a known failure mode
and the guardrail Inquirium adopts against it.

### Output Schema Contract

A request, profile, or capability may carry an output `schema/ref`. The host
enforces it at the strongest tier the selected adapter declares, degrading
explicitly:

```text
native     — provider constrains generation to the schema
             (strict JSON-schema mode, GBNF/grammar-constrained decoding,
              or a forced single-tool call); strongest
primed     — schema + 1–2 exemplars injected as PromptAssemblyPolicy preamble
             layers ("respond only with JSON for this schema"); cheap, soft,
             never sufficient alone
validated  — host parses and validates the output, emitting
             Invalid { schema/ref, violations[] } with a JSON Pointer to each
             failing location
```

Tiers compose: `native + validated` is the default for any schema that gates a
downstream effect — constrain *and* verify. The chosen tier, `schema/ref`, and
any repair are recorded in trace.

Pitfalls others hit, and the guardrails:

- **Format tax on quality.** Forcing strict structure too early can reduce
  reasoning accuracy. Allow an optional bounded, user-visible `rationale` field
  *before* the constrained payload — not a hidden chain-of-thought trace and not
  persisted as one — or a two-phase reason-then-format step; never wrap a task in
  JSON when free text would do — dialect is opt-in per operation, not a global
  mandate.
- **JSON mode is not schema conformance.** Provider "JSON mode" guarantees
  syntactic JSON, not your fields, and left un-prompted can emit an unbounded
  whitespace stream until `max_tokens` (a documented provider footgun). `primed`
  always accompanies bare JSON mode, and `validated` is mandatory unless `native`
  strict is proven.
- **Not every schema is constrainable.** Native constraint engines support only
  a subset of JSON Schema (bounded nesting, `additionalProperties:false`,
  recursion limits, restricted `pattern`/`format`). Declare a `constrainable`
  profile with explicit limits such as max depth, max properties, max enum
  entries, supported `format` values, and whether recursion is allowed; schemas
  outside it fall back to `primed + validated` and are flagged, not silently
  downgraded.
- **Non-terminating grammars.** A grammar that never admits the stop token plus a
  high token budget runs away. Every constrained run carries a bounded
  `max_tokens`, and the grammar must admit termination. Conformance fixtures for
  grammar-capable adapters include a bounded termination check before the
  capability is trusted for routability.

### Schema Reminder and Bounded Recall

The schema is available on demand, not only at the start. A stable `schema/ref`
lets the host re-surface the schema (or a glossary, tool list, constitution) as a
reminder on a repair attempt or when the model drifts, and lets the model
*request* it through the dialect control channel — but only from a host-pinned
allowlist of refs, never an arbitrary fetch.

Pitfall: re-injecting the schema in the middle of the context invalidates
prompt/KV cache and triggers "lost in the middle" attention loss. Keep the schema
in the stable cached prefix (front) or append the reminder as a `postamble`; do
not splice it mid-context. See *Performance and Resource Hardening*.

### Pre-Parse and Bounded Repair

Before full validation the host bounds the raw output by byte size, nesting
budget, and array/object limits, then runs a tolerant structural pre-parse: strip
markdown fences and prose wrappers ("Here is the JSON:"), locate the envelope,
and produce typed `ParsedEnvelope { content, params, schema/ref }`. Downstream
flows consume typed data immediately; every normalization is recorded, never a
silent semantic fix (no guessing missing fields). The host cannot validate JSON
Schema before parsing JSON, but it must enforce size/depth limits before parsing
and validate semantics immediately after parsing.

On a schema violation the host may `repair-once`, bounded by policy:

```text
io.repair { max-attempts (default 1), include-violations: true,
            mark: Repairable -> repaired-in-trace }
```

Pitfalls:

- **Repair loops blow up cost/latency and often re-fail identically.** Output-fixer
  experience across libraries shows more than one or two repairs rarely helps.
  Prefer `native` over repair, cap attempts low, always feed the exact violation,
  and count repairs in trace and budget.
- **Parsing untrusted output is an attack surface.** Deeply nested or oversized
  model JSON can exhaust the parser (billion-laughs class). Bound depth, size, and
  array length *before* parsing (schema-as-gate); for streaming, use an
  incremental/partial-JSON parser rather than waiting for a closing brace.

### Input and Output Rails

`io.rails` are boundary rules independent of the model: required fields, max
sizes, deny patterns, content-class limits, and redaction, applied to the
assembled input before send and to the output after receive. The manifest
declares which rails the provider enforces natively; the host always enforces the
safety-critical ones regardless.

Pitfall: trusting provider-native moderation alone leaves coverage that varies by
provider and version; double-enforcing every rail wastes tokens and latency.
Host-enforce the safety-critical rails unconditionally, and use the native
declaration only to *skip redundant* non-critical checks, never to drop a
critical one. The first safety-critical rail set is closed and host-owned:
bounded size/depth, secret-pattern detection, explicit PII classes configured by
policy, egress-class compatibility, and schema-required redaction. Domain-specific
redaction is schema-aware: redact fields by contract and classification, not by
blind string replacement over the whole output.

### Communication Dialect

`io.dialect` declares *how* the model communicates, separating a content channel
from a control channel in one canonical envelope:

```text
GenerateOutputEnvelope {
  content
  epistemic
  params
  control
}
  content   : the answer — DATA, never interpreted as instructions
  epistemic : stance/confidence/grounded_in/caveats (generate.response.v1)
  params    : model-carried metadata (language, tags, score)
  control   : model requests (recall schema/ref, propose tool-call)
```

Adapters map provider output into this envelope; callers see one stable shape
across models. Existing `output[]` text blocks are the simplest `content`
projection. The envelope does not make `output[]` and structured output mutually
exclusive; it gives them one canonical home. A `null` or empty `content` is
allowed only as an explicit degraded/refusal/control-only outcome and is
projected as `Degraded { reason: "empty-content" }` or `Refusal`, not as a
successful answer.

Pitfall: if a `control` field can trigger effects, injected text in `content` may
try to forge it. The control channel is host-validated and capability-gated; a
model-asserted control item is a *request* authorized by policy, never
self-executing (mirrors *Missing Authority Means Denial*). `content` is always
data. `control` starts as a closed enum: `recall-schema`, `recall-glossary`,
`propose-tool-call`, `ask-operator`, and `revise-output`; each item carries a
host-pinned ref or capability ref and is admitted per operation, never globally.

The implemented `GenerateOutputEnvelope` keeps `control` closed, bounded, and
non-effectful while admitting the complete first domain vocabulary above. Each
kind has its own payload validator; `propose-tool-call` alone carries a
`capability/ref`, and no admitted item grants authority by shape.

The continuation decision freezes the complete first canonical vocabulary:
`recall-schema`, `recall-glossary`, `propose-tool-call`, `ask-operator`, and
`revise-output`. These values are closed, inert DTOs admitted through an
operation-specific allowlist. An admitted item never causes an implicit recall,
repair, tool invocation, operator prompt, or model re-invocation. It becomes data
for an explicit host, Agent, Sensorium, or Flow step; `ask-operator` may enter the
Proposal 066 operator-question lifecycle only after host admission. Unknown or
disallowed intents fail closed.

### Adapter Capability Negotiation

The adapter manifest declares structured-I/O capabilities; the host reads them to
choose tiers and role folding:

```text
supports/json-mode, supports/json-schema (+ constrainable subset),
supports/grammar, supports/tool-call,
supports/system-role, supports/developer-role,
supports/native-rails, supports/streaming, max-output-tokens
```

This is the lever that makes adapters cheap to write: authors declare facts; the
host orchestrates.

Pitfall: a manifest may claim `json-schema` while the provider version honors only
a subset, or drift as provider APIs change. A declared safety-relevant capability
is not trusted until a conformance fixture proves it (tie to *Adapter Conformance
Before Routability* / `inq-conformance-runner`); capability declarations are
versioned. Runtime request budgets and manifest limits combine by taking the most
restrictive value: effective output tokens are bounded by caller request,
adapter `max-output-tokens`, and runtime/profile budget. Missing required
ceilings are treated as denial for safety-critical generate paths: native/primed
output contracts and active host I/O rails.

### Session and Memory Policy

Inquirium owns durable conversation state; provider session/cache is an
optimization, not the source of truth. A `MemoryPolicy` declares what survives a
turn:

```text
MemoryPolicy {
  pinned-facts[]     # re-injected as stable preamble; never auto-summarized
  rolling-summary?   # bounded, lossy; excludes pinned facts
  recall-refs[]      # host-pinned allowlist (schema, glossary, tools)
  window/limit, drop-policy
}
```

This reuses *Projection Mode for Long-Lived Sessions* and *Prompt Cache and KV
Cache as Controlled Resources* rather than adding a second state model.

`MemoryPolicy` owns deterministic projection, not summary production. The first
slice retains pinned facts, the current bounded summary, and the newest admitted
unpinned facts, then removes the oldest unpinned facts according to
`drop-policy`. If pinned facts plus the current summary already exceed the
window, the turn is denied with a typed memory-window failure rather than
silently discarding either. Removal applies only to the per-turn projection;
durable source facts remain available to their owning store and summarizer.

Producing or updating `rolling-summary` is the explicit responsibility of a
separate configured component or workflow, such as a session owner, an Agent, or
a dedicated summarize pipeline. That producer uses the normal Inquirium
summarize contract when model inference is needed and persists the resulting
summary fact with source-range/digest, model-snapshot, and policy provenance.
Inquirium must never hide an additional summarization call inside context
assembly. This ownership boundary is a requirement, not merely an optimization
choice, so summary work cannot disappear between the memory projection and the
orchestration strata.

Pitfalls:

- **Lossy compaction erodes critical facts ("context rot") and summaries drift.**
  Tiered-memory systems show pinned facts must be explicit and exempt from
  summarization. `pinned-facts` are host-owned and never compacted away; the
  summary is bounded and reconstructable; provider-side session state is never
  relied on for durability.
- **Unbounded session growth means linear cost and quadratic attention.** Bound the
  window with summary plus pinned facts, and let token estimation (next section)
  gate turn admission.

## Performance and Resource Hardening for Prompt and Schema Layers

The mechanisms above add always-on preambles, schema constraints, validation, and
per-turn memory. Left naive, these are exactly where model systems pay in latency,
tokens, and server memory. The cross-cutting rules, each from a problem real
deployments have paid for:

- **Cache-prefix discipline.** A persistent preamble (host-root + organ + schema +
  exemplars) only amortizes if it is a *byte-stable prefix*; any change near the
  front invalidates the whole cache. Order `PromptAssemblyPolicy` layers
  most-stable-first, volatile content (caller turns, context) last, and place
  reminders as `postamble`. Respect provider realities: caches impose a
  provider-specific minimum cacheable size and a short TTL, and a cache write
  costs more than a read — so do not cache tiny or rarely-reused preambles. Treat
  the size and TTL as configuration validated against the active provider.
- **Constrained-decoding compile cost.** Compiling a grammar/FSM from a schema is
  expensive on first use and cheap thereafter. Compile lazily and cache the
  compiled artifact keyed by `(schema-hash, tokenizer/model)`; never recompile per
  request.
- **KV-cache memory is finite.** Shared long prefixes pin server KV memory and
  trade memory for compute. Treat the preamble budget as a managed resource with
  eviction; very large pinned contexts compete with request concurrency.
- **Format tax vs accuracy.** Strict structure can cost reasoning quality; reserve
  hard constraint for effect-gating schemas and allow a pre-payload bounded
  `rationale` field elsewhere. (Stated per mechanism; here as a global budget
  rule.)
- **Lost in the middle.** Long contexts attend worst to the middle; keep
  schema/instructions at the front (and cached) or near the end, never buried
  mid-context.
- **Retry and repair storms.** Schema-repair and conformance retries multiply load
  under stress. Bound repair attempts, apply jittered backoff, route through the
  existing *Backpressure and Output Sink Availability* limits, and stop a repair
  that re-fails identically rather than looping.
- **Validation is bounded before it runs.** Depth, size, and array caps precede
  parsing so a hostile or runaway output cannot exhaust the validator.

Every choice here is recorded — tier used, cache hit/miss, repair count, compile
reuse — so cost and behavior stay reproducible and auditable rather than folklore.

## Temporal and Locale Context

Two context inputs are trivial to omit and visibly break behavior when missing.

**Temporal context.** A model does not know the current time. The host injects a
`temporal` layer (a host-owned `PromptAssemblyPolicy` preamble) carrying the
current date, time, and timezone, plus the model's stated knowledge-cutoff where
known, so freshness-sensitive answers and "as of" reasoning are correct. The
value is host-supplied data, never inferred by the model. To avoid invalidating
the prompt cache on every call, the cache-stable prefix carries only a coarse
value (for example rounded to the day); finer granularity goes in a volatile
postamble.

**Locale.** Instruction language and content language are distinct. A `locale`
policy declares the operator/caller response language and formatting conventions,
surfaced through `dialect.params.language`; schema field names stay canonical
while `content` is localized. Default is the operator locale; callers may narrow,
not silently switch the instruction language.

Locale identifiers use canonical BCP 47 language tags. Distributor/operator
configuration owns the allowed locale set and default; an authenticated caller
may select only an admitted response locale. Prompt content and model output
cannot change the effective locale, and the instruction language remains a
separate host-owned prompt-policy concern.

## Model Snapshot and Prompt Versioning for Reproducibility

Determinism is already best-effort (`supports-seed?`); reproducibility needs two
more records that are easy to forget.

**Model snapshot.** Providers silently update a model behind a stable alias, so
the same `model/binding-ref` can drift in quality. The host records the
provider-reported resolved model snapshot (for example a dated version id) in the
inference trace beside `runtime/ref` and the effective sampling parameters.
Without it, "why did quality change?" is undiagnosable and a run cannot be
reproduced. This is distinct from the dataset build's `config-snapshot-hash`,
which pins training inputs, not the inference model version.

**Prompt as a versioned artifact.** `instruction/hash` and `protocol/epoch`
identify an assembly; they should also be governed like code. The assembled
instruction stack is a versioned, reviewable artifact with diffable layers and
rollback, and a change to any host/organ/profile layer is gated by a regression
check against a golden set before it becomes the active epoch. This is distinct
from *Eval Before Route* (which gates the runtime, not the prompt): here a
preamble tweak cannot silently regress quality, because the prompt change is
reviewed and measured like any other change.

## Deterministic Response Cache

Separate from the prompt/KV cache: the host may cache the full result, keyed by a
domain-separated digest over operation/contract version, assembled input, model
snapshot, effective sampling parameters, effective classification, and effective
policy digest, but only when the result is genuinely reproducible. Embeddings are
the natural case. Classification qualifies only conditionally: the runtime must
declare a deterministic mode, sampling must be deterministic (`temperature 0`,
and a fixed seed where the runtime honors it), and the full assembled prompt plus
model snapshot must be in the key. Because the assembled prompt includes any
volatile temporal or context layer, those layers change the key and invalidate
stale entries — a cache hit must never outlive the inputs it was computed from.

The cache is opt-in and must be refused for sampled generation (`temperature >
0`), where identical input legitimately yields different output, so a hit never
masks intended variation. Cache hits are recorded in trace, and the model
snapshot in the key means a provider update invalidates stale results.

The first backend is a bounded two-level host cache: an ephemeral in-memory L1
in front of a durable node-local SQLite L2. Lookup order is L1 -> L2 -> runtime;
an L2 hit repopulates L1, while a validated and cache-eligible runtime result is
written to L2 and then L1. Both levels are non-authoritative optimizations and
may be evicted without changing domain truth. The cache is disabled by default,
never uses Memarium, and stores no raw input solely to construct its key.

The L2 record repeats the key inputs as validation metadata and binds them to
creation/expiry metadata plus the validated result or bounded result reference.
Eligibility, TTL, size ceilings, and eviction are class- and policy-bounded.
Cache hits produce cache-accounting and trace evidence but never fabricate
provider token or cost usage.

## Output Safety Rail

Output rails (`io.rails`) should include a host-owned safety classification of the
model output before it reaches a user surface or an effect: leak, toxic,
self-harm, or policy-class content. This generalizes the assistant-specific
`crisis-candidate` (P066) into a boundary rail available to every operation. The
classification is host-owned and capability-gated, never the adapter's
improvisation, and a failed safety rail produces a typed `Unsafe { policy/ref,
reason }` rather than passing content through. The first implementation may use
deterministic rules for secrets, explicit PII classes, and schema-level policy
markers; model-backed critics are allowed only as separately conformed evaluator
runtimes under a signed/versioned host-owned policy registry.

## Enforced Token and Cost Budget

Capability metadata already carries `budgets`/`cost/class` and dispatch policy
carries a `time budget`; this makes the budget an enforced contract rather than a
hint. Each operation and session has metered token and cost ceilings with a hard
cap; on exhaustion the host returns a typed `BudgetExceeded { scope, limit,
spent }` instead of an unbounded bill. Metering counts assembled-prompt tokens,
output tokens, repair attempts, and cache writes, and the spend is recorded in
trace so cost is attributable per caller, operation, and session.

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

Ownership is host-first. An adapter may return a `Plan` only as a
`CandidatePlan` when its manifest declares `returns/plan: true`; the host then
compiles or rejects that candidate into `InquiryFlowV1`. The adapter never emits
an executable flow. The host-owned compiler applies schema validation,
capability/tool grants, budget limits, effect policy, and loop bounds before any
node can run. A loop whose termination condition is not reached exits as
`Cancelled { reason: "max-steps-exceeded" | "max-cost-exceeded" |
"max-time-exceeded" }`, not as a hidden retry. Flow traces carry secret refs and
artifact refs, never secret values or raw protected payloads.

The first implementation stops at contracts plus a pure
`CandidatePlan -> InquiryFlowV1` validator/compiler in `inquirium-host`.
Inquirium does not own a Flow scheduler, lifecycle registry, retry loop, or
effect executor. Execution is delegated explicitly to the daemon composition
root, JSON-e Flow, or Agent according to the admitted consumer boundary.

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

## Production Local Model Provisioning

Proposal 066 Decision 8.5.1 is the policy source of truth for production local
model packaging. Implement it as a host-owned provisioning pipeline around the
existing baseline profile renderer, not as provider-specific logic inside
Inquirium Core:

1. Parse and schema-gate a bounded package manifest before network, filesystem,
   process, or profile effects.
2. Resolve source authority separately from artifact authority. A trusted HTTPS
   origin or canonical local root permits staging only; it never substitutes for
   the expected digest, package signature, or operator endorsement.
3. Stage runtime/model bytes into a dedicated content-addressed asset store.
   Streams are size-bounded, resumable only under an exact manifest identity,
   verified before commit, and cleaned after interrupted or failed installs.
4. Admit either a distributor-signed manifest or a host-computed manifest with a
   detached operator signature. Operator approval is projected through the
   existing registered operator-question and notification path; the model may
   not author the question shape or approval scope.
5. Render the selected `llama-server` or conformant MLX candidate into the
   existing runtime catalog and profile format. Packaging does not create a
   parallel invocation protocol or supervisor.
6. Run the existing `BaselineAssistantProfile` conformance suite against the
   exact runtime/model/backend digest tuple. Installation success alone never
   makes a candidate routable.
7. Activate the verified profile atomically and retain the prior verified
   activation as the rollback target. Recovery derives one authoritative state
   from the asset store, install receipts, and active-profile projection.
8. Expose operator-visible source, signer, model card, license, size, backend,
   conformance, active/rollback refs, and failure diagnostics without exposing
   secrets or raw signing material.
9. Feed measured latency, memory, throughput, and context capability to status
   and NSE diagnostics. These measurements inform selection but are not v1
   correctness gates.

Current implementation evidence covers the effect-free plan, signed authority
registry, bounded local/HTTPS staging, verified lifecycle journal, recovery,
generation-guarded activation, rollback/removal, and the release gate enforced
inside each journaled profile transition. Durable leases and random attempt refs
serialize competing install/recovery workers; one-shot source trust is committed
only after that exact claim exists. Rollback binds the expected current
generation and receipt to the exact target, while release admission compares the
duplicate-free manifest/receipt/profile asset sets and repeats before commit.
HTTPS resolution rejects any special-use destination and pins the complete
public address set into the request client, preventing a second DNS lookup from
rebinding an admitted origin; transfer progress has a separate rolling floor in
addition to the large-file total timeout. Receipt state is checked again in the
same SQLite transaction that advances the active generation, and every CAS object
is digest/size verified before the transition begins. Primary failures precede operator-visible, restart-recoverable
install/removal cleanup rather than being obscured by it. The
remaining product boundary is intentionally above those mechanisms: the daemon
must derive authority projections from its operator-question and signer strata,
then bind an activated package profile into the existing supervisor and
conformance registry. Internal admitted-authority DTOs are not wire credentials
and must never be populated directly from caller JSON.

The first release matrix is macOS arm64/Metal and Linux x86_64/CPU. A parallel
MLX-family evaluation on Apple Silicon must choose a supervised loopback server
that speaks the same OpenAI-compatible contract as the managed
`llama-server` path. Shared conformance vectors, rather than provider branding,
decide whether it qualifies.

## Open Questions

No unresolved questions remain in this section for the current slice. The
following decisions record the operator-approved defaults so future
implementation does not reopen them accidentally.

### I/O Rail Violation Shape

Decision: keep first-match fail-closed behavior for the current slice.

This preserves the existing response and trace shape, and the content is already
suppressed once any safety-critical rail fires. A later rail diagnostics slice
may still add a bounded `violations[]` projection with explicit priority such as
`secret > credential > PII > self-harm > content-policy`, provided traces remain
prompt/output-free and do not leak matched text.

### Inquirium Config Ownership

Decision: reusable Inquirium config types and domain constants belong to the
Inquirium host-service stratum, while config source loading and composition stay
in the daemon for now.

The daemon still owns file/env loading, layered config composition, runtime
catalog validation, and effect authority; it no longer owns the reusable data
types and domain defaults for prompt assembly base policy, prompt content refs,
temporal context, I/O rail config, or output schema registry composition. If
distributor/operator configuration later grows beyond the current JSON-file
composition model, that should be evaluated as a shared host config substrate
proposal rather than hidden inside Inquirium.

### Capability Dispatch Registration

Decision: keep Inquirium's table-driven dispatch local to the daemon composition
root for now and treat it as the reference pattern.

The Capability Registry remains the admission authority; the registration table
only routes already-defined capability ids to daemon-owned handler closures. If
a second organ-host needs the same pattern, extract a shared helper only if it
removes real duplication without making organ-specific authority implicit.

### Effect Intent Consumption Boundary

Decision: move the active Inquirium effect write path to returned-value effect
intents across the Inquirium surface, not only as a one-operation pilot.

The migration should still be staged safely: define operation-level decision
values that return response/denial plus effect intents, then have the daemon
execute those intents through the existing stores. Do not add write ports to
`inquirium-host`; writes remain daemon effects. Until that migration lands, the
current vocabulary remains public, validated data and the daemon continues to
execute trace, transcript, and budget effects through its existing
composition-root paths.

### Baseline Assistant Conformance Runner Scope

Decision: implement `BaselineAssistantProfile` conformance as an extension of
the existing report-backed model-runtime conformance runner, not as a separate
assistant-only gate.

The baseline assistant is a profile-level contract over runtime candidates. The
runner should therefore reuse the same fixture digest, durable report store, and
routability semantics already used by runtime conformance, adding profile-aware
fixture suites rather than a parallel certification path. A candidate is
baseline-selectable only when the current node has a fresh passing report for
`profile/baseline-assistant`, the selected `runtime/ref`, the current fixture
digest, and the deployment-controlled canonical `host-class/...` value within
the configured baseline TTL. Missing, stale, or failing reports deny baseline
routing fail-closed, and the assistant must not fall back to a remote runtime.

### Continuation Decisions for Remaining P064 Work

The following operator-approved decisions are frozen for the next implementation
slices:

1. The communication dialect admits the complete first canonical control
   vocabulary as closed, inert, operation-allowlisted data. No control item
   executes or starts an implicit model loop.
2. `MemoryPolicy` performs deterministic projection only. A separate configured
   component or workflow owns summary production and persistence; Inquirium does
   not hide summarization inside context assembly.
3. The deterministic response cache uses bounded in-memory L1 followed by
   durable node-local SQLite L2. It is opt-in, non-authoritative, and separate
   from Memarium.
4. Flow IR in Inquirium consists of contracts and a pure host-owned compiler.
   Scheduling, lifecycle, retries, and effects remain outside Inquirium.
5. Response locales use an operator/distributor allowlist of canonical BCP 47
   tags. An authenticated caller may narrow within that set; instruction language
   remains independently host-owned.
6. The current prompt-assembly policy slice is complete. Support for a future
   text-generative operation becomes a separate tracker item only when that
   operation is introduced; speculative operation loaders do not keep the
   current task open.

## Implementation Tracking

This section is a lightweight, manually maintained tracker for implementation
work derived from this proposal. Add rows as implementation tasks start or land.
Rows marked `done` should point to concrete evidence such as code paths, schema
fixtures, tests, operator surfaces, or migration notes.

Implementation order matters for the open items. The natural dependency front is:

```text
class-keyed-mechanism-in-classification
  -> inq-prompt-assembly-policy
       -> inq-temporal-context
       -> inq-model-snapshot-trace
       -> inq-prompt-versioning-regression
       -> inq-io-schema-contract

inq-io-schema-contract
  -> inq-comm-dialect-envelope
  -> inq-adapter-capability-negotiation
  -> inq-io-rails
       -> inq-output-safety-rail

inq-flow-ir
  depends on prompt assembly, I/O schema contract, and conformance evidence.
```

Rows may be implemented incrementally, but dependent rows should not be marked
`done` before their prerequisite contracts exist and have fixtures.

Status values:

- `todo` — not started,
- `in-progress` — design or implementation has started,
- `done` — implemented and covered by tests, schema validation, or documented
  operator evidence,
- `deferred` — intentionally postponed.

The tracker below covers the completed Inquirium organ/runtime implementation
slice used by the hard-MVP readiness calculation. Post-MVP local-model package
productization is tracked separately in Proposal 066 under
`assistant-model-*`; its partial release and operator-wiring rows do not reopen
the completed P064 hard-MVP slice.

**Invariants to preserve (landed decisions with sharp edges).** These are
implemented and easy to break in a well-meaning refactor; treat each change as
a migration event, not a tweak:

1. The instruction hash is canonical JSON under `JcsNfcStringsV1`
   (NFC-normalized strings) and includes the caller-turn count
   (`caller_turns_count` in the digest material; projected as
   `caller-turns/count` in the public prompt assembly shape); the golden
   vector `inquirium-prompt-assembly-resolved.v1.json` is the replay contract.
   Changing the canonical profile, the layer serialization, or the hash inputs
   requires a new golden vector and an explicit migration note — a silent
   "equivalent" change breaks trace replay across every recorded turn.
2. The instruction token estimator is exactly `non_whitespace_chars.div_ceil(4)`
   (minimum 1 for non-empty text). Configured token caps are priced against
   this function; swapping in a "better" estimator re-prices every cap.
3. The baseline-assistant local transport check is an **allowlist**
   (`is_allowed_baseline_local_transport`) — a newly added transport variant
   fails closed until explicitly allowed. Do not revert it to a
   deny-known-remote list; that silently admits future variants.
4. Conformance freshness fails closed end to end: unrepresentable TTLs deny,
   and stale/missing/failed reports all make the candidate non-routable. The
   16 KiB host-visible output cap is asserted *in the conformance runner*, not
   only enforced at the host boundary — removing the runner assertion because
   "the host enforces it anyway" reopens the silent-regression gap it closed.
5. The default host-root boundary prompt is versioned
   (`DEFAULT_HOST_ROOT_INQUIRIUM_BOUNDARY_PROMPT_V1`); editing its text changes
   every downstream instruction hash. Version-bump and note it — never edit in
   place.
6. Role folding is recorded as *adapted*, never *rejected* — trace consumers
   distinguish "reshaped for this adapter" from "refused"; collapsing the two
   changes the meaning of recorded turns.

| ID | Work item | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- |
| `inq-operational-context-prompt-framing` | Render admitted Sensorium operational impact as a pre-inference host-owned caution layer. | `done` | The daemon-owned prompt resolver accepts only qualifiers produced after exact P082 current-generation/current-publication validation, applies a monotone local floor and multi-feed maximum, and renders a closed, versioned Developer caution layer before feed-dependent inference. Host-owned request metadata and the durable Inquirium trace record the local policy ref, local floor, selected class, and a deterministic per-source list pairing each source class with its exact context digest, so an audit distinguishes source declaration from local elevation. The trace projection is passed from the composition root rather than inferred from caller metadata or provider output. The at-most-512-byte publisher summary remains retrieved data below the instruction hierarchy. Golden ordering and instruction-hash tests, provenance, missing-floor refusal, order-independence, and non-droppable production/critical tests cover the boundary without introducing an Inquirium TTL or adapter-owned policy. |
| `inq-runtime-catalog-v02` | Move the lower model-runtime catalog to adapter implementations, adapter instances, model bindings, runtime candidates, runtime profiles, and conformance fixtures. | `done` | `node/model-runtime` contract v0.2 validates cross references and rejects missing adapter/model/conformance references. |
| `inq-http-adapter-instance-handles` | Key HTTP lifecycle handles by adapter instance while invoking by selected runtime candidate. | `done` | `node/model-runtime-http` accepts `RuntimeInvocationContext`, supports one HTTP adapter instance serving multiple runtime candidates, rejects caller override of host-owned model keys, and now maps neutral Inquirium generate requests directly to local OpenAI-compatible `/v1/chat/completions` servers through the built-in `openai_chat_completions` request/response mapping. HTTP mapping validation has two valid modes: both request/response mapping formats absent for provider-native passthrough, or both set to the same supported format for mapped mode; half-mapped and unsupported formats fail closed during adapter-instance config validation. Mapped provider responses are bounded before JSON parsing, and oversized bodies are rejected by stopping the bounded read instead of buffering the full response. Daemon `inquirium.generate` invokes HTTP adapter instances through this context, Story 005 verifies the path with the opt-in simulator runtime, and the baseline assistant E2E uses direct local chat-completions without a Python HTTP proxy. |
| `inq-command-stdio-invocation-context` | Apply the same host-built runtime invocation context to command-stdio adapter instances. | `done` | `node/daemon` merges runtime defaults, model binding parameters, and caller body before stdin serialization; caller override of `model` fails closed in daemon lifecycle coverage. |
| `inq-daemon-runtime-routing` | Supervise adapter instances and route by `runtime/ref` in the daemon. | `done` | Daemon status separates `healthy` from `routable`, reports adapter/model binding refs, and counts only routable candidates. Focused daemon runtime tests pass sequentially. |
| `inq-nse-use-runtime` | Make NSE choose runtime candidates instead of runtime/model pairs. | `done` | `nse` and `nse-rhai` use `UseRuntime { runtime_id, reason }`; Rhai scripts return `decision: "use-runtime"`. |
| `inq-signed-adapter-manifests` | Treat adapter manifests as signed data, not hidden code promises. | `done` | Bundled Python Inquirium adapters declare `adapter_manifest` using `inquirium.adapter.manifest.v1` and register that fragment through `signed_config_artifacts[]` with the `orbiplex.inquirium.adapter-manifest.v1` signing domain. The shared adapter report returns the manifest from config, and the daemon signed-config loader now resolves hyphenated module ids against underscore config keys so those adapter-manifest sidecars are discovered. |
| `inq-python-remote-provider-adapters` | Add first middleware-hosted remote provider adapters while preserving adapter-instance/runtime-candidate stratification. | `done` | The OpenAI adapter maps neutral generation and host-authorized JSON Schema to Responses and neutral embedding to the native `/v1/embeddings` endpoint; the Anthropic adapter maps generation and the same schema subset to Messages and deliberately does not claim an embedding API. Both share `node/middleware-modules/lib/inquirium_adapter`, expose neutral and chat-compatible endpoints, read secrets from env/file config, and have fake-provider coverage. `model-runtime-http` starts each adapter as a managed process, exercises invoke and shutdown, verifies one OpenAI instance serving two model bindings, and covers provider-backed OpenAI embeddings end to end. Host validation and rails remain authoritative after normalization. |
| `inq-embedding-contracts` | Add explicit direct and batch embedding request/response contracts. | `done` | `node/inquirium-core` owns `inquirium.embed.{request,response}.v1` and `inquirium.batch-embed.{request,response}.v1` DTOs with validation for schema, operation, dimensions, leases, bounded duplicate-free batch source lease refs, vector shape, finite vector values, and stable slash-scoped artifact/lease refs. `node/model-runtime` re-exports these DTOs for runtime-facing compatibility. |
| `inq-embed-host-surface` | Expose direct embedding through the same host capability and audit model as text generation. | `done` | Daemon exposes `POST /v1/host/capabilities/inquirium.embed`, advertises it through host capability discovery when an implemented handler is routable, requires explicit inference grants for module callers, selects `embed` runtime candidates by host-owned model binding, and writes metadata-only traces under `trace/inquirium/embed` with host-keyed request digests and no input text or vector values. `node/inquirium-host` owns direct request validation, profile/classification/locality/trust eligibility, and model-binding admission; missing classification fails closed to Personal/local-only. Daemon executes deterministic, HTTP-local, HTTP-API, or channel adapter handlers and revalidates vector count, order, dimensions, finiteness, and host-owned runtime/model refs. OpenAI provider-backed embedding and supervised process lifecycle are covered; Anthropic remains generation-only because its native API exposes no embedding operation. |
| `inq-direct-data-plane` | Add durable direct data-plane leases, artifact output persistence, and deferred long operations. | `done` | Daemon persists model-runtime leases in SQLite, exposes local lease create/read APIs, rejects remote raw file leases, rejects symlinked allowed file roots and symlink escapes through canonical containment, hides expired leases, restricts caller metadata with per-value and total caps, admits `batch.embed` through `DeferredOperationRegistry`, and verifies/writes pilot output artifacts through the object store with selected-binding and operation-bound write-lease provenance. Pilot artifact output is now planned as an `ArtifactOutputIntent` and executed by the shared daemon artifact-output effect interpreter rather than as an inline endpoint write. |
| `inq-conformance-runner` | Add conformance fixture execution, durable reports, and report-backed routability. | `done` | Daemon persists reports in SQLite, exposes `run-conformance`, evaluates generate/embed/classify/rerank fixtures plus profile-aware candidate requirements, scopes baseline reports by profile and deployment host class, applies TTL freshness fail-closed, and keeps required candidates non-routable until the current fixture digest passes. Baseline checks retain the local-transport allowlist and 16 KiB output-cap assertion. Tests cover classify/rerank report-backed routing, stale/registry-error/disabled candidates, denied remote or command-stdio baseline transports, non-offline candidates, oversized output, TTL overflow, profile mismatch, bounded failure payloads, and direct local baseline E2E. The SQLite registry now uses explicit schema v1 → v2 migration and rejects unsupported future versions instead of silently applying additive columns. |
| `inq-baseline-profile-renderer` | Turn an installed local OpenAI-compatible runtime into explicit baseline-assistant operator configuration without adding a proxy. | `done` | `node/tools/inquirium-baseline-profile.py` renders the validated reference catalog for an unmanaged loopback Ollama endpoint or a managed local `llama-server`; it rejects non-loopback endpoints, verifies executable/model files, records the model SHA-256 digest in binding/candidate metadata, and leaves provider-binary installation to the distributor or operator. Its Ollama path has a read-only, non-redirecting loopback doctor, an explicit model-pull plan that executes only with `--execute` and never through a shell, atomic profile activation with mode `0600`, active status, and scoped deactivation. Daemon health and conformance remain runtime authority. Unit tests cover model-name injection denial, plan-only behavior, explicit pull, loopback denial, executable checks, digest binding, activation/deactivation, invalid status, and symlink escape refusal. |
| `inq-model-package-contracts` | Freeze the local-model package and lifecycle data boundary before installer effects. | `done` | `node/inquirium-model-package-core` plus six accepted, mirrored, Schema Gate-registered contracts define manifest, source trust, operator endorsement, install receipt, active profile, and inert install plan values. Canonical digest, source, platform, asset, authority-mode, lifecycle, and rollback invariants are covered by semantic tests plus one structural negative boundary assertion per schema family. |
| `inq-model-asset-store` | Provide a dedicated immutable content-addressed store below package installation. | `done` | `node/inquirium-model-asset-store` owns bounded staging, streaming digest/size checks, verified atomic commit with post-publication rollback, explicit SQLite durability settings, restrictive read-only object permissions, pins, reference-aware GC, size-and-digest recovery diagnostics, and explicit schema migration/refusal without depending on daemon effects. Download/resume remains an installer concern rather than a missing store responsibility. |
| `inq-model-storage-root` | Separate host control metadata from configurable bulk model bytes under one owned root. | `done` | Daemon config and the store resolve explicit config before `ORBIPLEX_MODEL_ROOT` before the `data-dir` default. Canonical marker/registry identity, one non-configurable persisted owner ref, generation, exclusive locking, pre-effect runtime-layout containment, and fail-closed mismatch tests prevent silent fallback, cross-node GC, symlink escape, and a second live writer. |
| `inq-model-storage-domains` | Separate immutable authority from mutable native interop and experiment trees. | `done` | Host-exclusive root-level `managed/` owns CAS and staging; `engines/<family>/host/` is the distinct host-owned runtime view, while engine `shared/` and `workspaces/` are mutable untrusted surfaces outside managed GC. Native bytes cross into authority only through descriptor-bound verified import. Typed `ENOSPC`, partial-stage discard, same-filesystem publication, and bounded recovery are tested. |
| `inq-model-runtime-storage-layouts` | Project versioned runtime-native paths without package-controlled process environment. | `done` | A host-owned registry validates runtime families, semantic storage areas, versions, and a closed environment-name allowlist, rejects process-execution variables, and renders contained child-only paths. Store materialization APIs require a registered family rather than accepting a manifest-supplied layout. |
| `inq-model-native-materialization` | Build immutable launch views while preserving CAS integrity and external-tool interoperability. | `done` | Materialization verifies CAS input, uses reflink or verified-copy fallback, verifies before publication, restricts the destination, and re-verifies immediately before launch. Shared native files require explicit streamed import; writable hard-link and symlink aliases into CAS are absent. |
| `inq-model-storage-root-migration` | Rebind model storage through a journaled single-authority migration. | `done` | Migration holds source and destination locks, copies and verifies every managed object, commits the root identity and generation atomically, then finalizes markers. Recovery rolls back a pre-commit provisional tree or completes a post-commit marker transition; it never copies mutable interop trees or infers recovery authority from accessible bytes. |
| `inq-model-package-plan` | Make installation intent deterministic data before admitting effects. | `done` | `node/inquirium-model-package-installer` consumes already admitted authority plus asset inventory and emits canonical `inquirium.model-package.install-plan.v1`; missing trust and descriptor conflicts block completion, `effects/executed` is always false, and an integration test proves real store inventory produces reuse/stage steps without downloading or activation. |
| `inq-feedback-training-grants` | Verify separate operator authority before feedback becomes adaptation material. | `done` | `inquirium-core` defines closed training-grant issue and revoke requests; daemon local control persists exact participant/feedback-bound expiring grants, archives participant-bound idempotent revocations, and rejects candidate-marked feedback unless the referenced grant exists, is current, not revoked, and matches both bindings. Dataset-manifest and `train.adapt` admission now re-run the same authorization before consuming candidate data. |
| `inq-train-adapt-admission` | Add a reproducible dataset manifest and grant-rechecking `train.adapt` admission path. | `done` | `inquirium-core` owns a bounded, canonically hashed, deterministically ordered dataset manifest whose samples bind source leases and digests to exact feedback/training-grant refs, plus a content-addressed `train.adapt` request keyed by base model, manifest, hyperparameters, seed, code, runtime image, toolchain, and policy. The local model-runtime operations endpoint validates the selected binding and declared `train_adapt` capability, binds `base-model/ref` to the binding's semantic `model/ref` rather than its provider-facing model name, positively allowlists the exact `http_local` trainer handler implemented by the first worker (other local transports remain denied until implemented), rechecks every live grant in one registry snapshot, validates operation-bound read/write leases, and registers only a metadata-safe public deferred status while retaining the full request as private continuation data. A fixed-thread, bounded daemon worker consumes and restart-recovers pending/running/publishing continuations through operation-kind/status-scoped bounded pages, recognizes an already persisted publication idempotently, rechecks grants and leases before new adapter work, reports progress, surfaces recovery-store failures, supports cooperative cancellation with typed terminal/conflict outcomes, and atomically closes cancellation before publication. The neutral local training-adapter request/result contract requires evaluation evidence; only a passing result up to the 96 MiB decoded artifact cap with a verified object-store-canonical `sha256:<base64url-no-pad>` digest and matching size becomes an `ArtifactOutputIntent` and object-store descriptor with exact lease/runtime/model-binding/operation provenance. The simulator trainer is deterministic lifecycle/conformance machinery, not a weight-optimization claim. |
| `inq-classify-rerank-vertical` | Carry classify and rerank through host policy, runtime execution, audit, budgets, adapters, and conformance. | `done` | `inquirium-core` owns bounded request/response pair validation; `inquirium-host` owns local-only/strict-local and model-binding predicates; daemon host capabilities require inference authority, select routable candidates, execute deterministic or local HTTP handlers, charge shared budgets, and write host-keyed metadata-only traces; the simulator exposes explicit classifier/reranker bindings; conformance runs both operation classes. These first-slice outputs are closed labels, caller-supplied candidate refs, ranks, and bounded scores, so they do not reuse the free-text generate output rail. Any future provider-authored free-text rationale or externally propagated explanation must add an operation-specific rail before release rather than inheriting a silent exemption. |
| `inq-summarize-transform-image-vertical` | Add bounded summarize/transform/image contracts and complete deterministic host verticals. | `done` | `inquirium-core` owns bounded summarize and schema-constrained transform contracts plus artifact-only image generate/edit contracts and golden vectors. The daemon registers all four host capabilities under the shared inference-authority table, applies shared budgets, records operation-domain-separated metadata-only traces, and compiles summarize/transform into the hardened generate substrate. Image generate/edit require explicitly declared runtime operations, host policy and model-binding admission, operation-bound source/output leases, and object-store persistence through `ArtifactOutputIntent`; deterministic PPM output remains the contract/conformance/smoke target. The supervised OpenAI adapter now supplies the first live provider path by mapping neutral generation to `/v1/images/generations` and edit to bounded multipart `/v1/images/edits`; one 32 MiB pre-read source cap, host model/dimension checks, PNG/JPEG/WebP/PPM magic-byte/media validation, digest/size verification, and artifact-only release still run after provider normalization. Compound summarize chunking remains a separate later operation profile. |
| `inq-host-service-stratum` | Extract host-owned Inquirium orchestration into an `inquirium-host` service stratum while keeping daemon effects at the composition root. | `done` | `inquirium-host` owns pure generate budget/prompt/adapter decisions, schema normalization, bounded repair framing, I/O rails and redaction, egress-class admission, embed/classify/rerank/image admission and binding predicates, image-provider normalization, training evaluation/publication planning, assistant output/transcript planning, reusable config including monotone assistant escalation policy, returned-value effect intents, operation decision wrappers, complete assembled-prompt token estimation, and `INQUIRIUM_HOST_API_VERSION`. Daemon owns file/env loading, catalog iteration, supervision, concrete transport, persistence, trace sinks, HTTP, effect execution, leases, and grant authority. Dependency-direction lints guard the core/host split and non-daemon trace consumers. Future operation families must add pure decisions to this stratum before daemon wiring; that extension rule does not leave the present extraction incomplete. |
| `inq-prompt-assembly-policy` | Add a host-owned, layered prompt/instruction assembly stage (see *Configurable Prompt Assembly Policy*): configurable globally and explicitly extended or narrowed per profile, model-binding, and adapter-instance, feeding adapters an already-rendered explicit message stack. | `done` | `node/inquirium-core` now owns `PromptAssemblyPolicy`/`PromptAssemblyPolicyAdjustment`/`PromptLayer`/`AssembledPrompt` with preamble/postamble positions, `class/key` selection, unique `layer/id` validation, scoped `extend/layers` and `narrow/layer-ids`, fixed/required/narrowable enforcement, bounded layer/token caps, a 32-layer cap per scoped adjustment, role-fold adaptation trace, rejected-layer trace, NFC-normalized canonical-JSON-backed `instruction/hash`, `caller-turns/count`, `content/source` on accepted/adapted layers, fail-closed unknown-field handling for layer content, and a host-supplied resolver path for `content/ref`. `node/daemon` owns the `inquirium.prompt_assembly` sourcechain (`host_root` -> `organ` -> `operation.generate`) with a default fixed host-root boundary layer, non-empty host_root enforcement, startup validation for origin monotonicity, required/fixed host-root and organ layers, and fail-closed unknown operation keys; the effective generate policy is stamped into `node/model-runtime` catalog `prompt_assembly`. `node/model-runtime` also carries scoped prompt adjustments on runtime profiles/model bindings/adapter instances and adapter implementation `instruction_roles`; `node/daemon` validates configured `generate` runtime candidates, including profile-specific sourcechains, during config loading so misordered or unsupported layers fail before the daemon accepts the catalog. `node/inquirium-host` now owns the `PromptContentResolver` port, `assemble_generate_prompt` execution wrapper, `GeneratePromptAssembly`, prompt-assembly metadata projection, generate policy eligibility, effective parameter merging, and selected-runtime `GenerateAdapterRequestPlan` construction. `node/daemon` resolves profile -> model-binding -> adapter-instance adjustments into `RuntimeInvocationContext.prompt_assembly`, refuses prompt layers when the selected adapter implementation has no manifest-declared roles, materializes host-owned `content/ref` through `inquirium.prompt_content_refs` and built-in temporal content via that port, and asks `inquirium-host` to build the selected adapter request plan; daemon still owns catalog iteration, routability/conformance gates, supervision, concrete transport invocation, traces, and HTTP routes. Bundled Python adapter manifests now declare `supports/instruction-roles[]`. Unit and golden tests, including `node/protocol/contracts/golden/inquirium-prompt-assembly-resolved.v1.json`, cover override-above-host-root ordering, duplicate layer ids, required cap-exceeded fail-closed, fixed-layer narrow denial, scoped origin mismatch, sourcechain ordering, empty-base extension, adapter-instance scoped extension, per-adjustment extend cap, profile/binding/adapter merge, manifest role requirement, resolved policy wire shape, resolved message order, daemon config sourcechain loading, candidate sourcechain startup denial, spoofed stratum-origin denial, unknown operation-key denial, unknown prompt content refs at config load, empty host-root denial, default host-root framing through HTTP adapters, four-character token-estimator cap, role-fold-recorded-as-adapted-not-rejected, content-ref materialization/source trace, temporal content-ref materialization, caller boundary count in the hash, Unicode-normalized instruction hashing, layer-content unknown-field rejection, daemon adapter-body trace projection, and `embed` rejecting text prompt-assembly payloads. The current slice is complete. When a future text-generative operation requires its own policy loader, that extension receives a separate tracker item rather than reopening this one. |
| `inq-io-schema-contract` | Host-owned Output Schema Contract: broadcast a `schema/ref`, enforce it at the strongest available tier, validate, pre-parse, and bound repair (see *I/O Contract*). | `done` | `inquirium-core` carries optional bounded output contracts and a narrow registered JSON Schema subset with canonical digests. `inquirium-host` resolves the strongest tier, compacts admitted schemas for provider use, normalizes output, enforces host byte/shape/schema checks, and returns typed invalid projections capped at 32 violations. OpenAI and Anthropic adapters compile the subset into native structured-output fields and normalize provider JSON, but native selection requires adapter support, selected runtime/model `supports_json_schema`, and per-schema `allow_native_enforcement`; host rails and semantic validation are never skipped. A schema may explicitly admit at most two host-framed repair attempts; repair instructions contain only bounded violation codes/pointers, use a manifest-supported instruction role, and every attempt is included in preflight reservation and final provider-usage aggregation. Dynamic refs, recursion, combinators, and grammar artifact caching remain post-v1 extensions rather than gaps in the bounded contract. |
| `inq-adapter-capability-negotiation` | Let adapters declare structured-I/O capabilities so the host chooses I/O strategy instead of each adapter reimplementing it. | `done` | `AdapterIoCapabilities` flows from adapter implementation into `RuntimeInvocationContext`; the host intersects it with selected runtime/model capabilities and schema policy before choosing native, primed, or validated enforcement. Unsupported explicit tiers fail closed. Bundled manifests declare the closed capability set, remote adapters map native JSON Schema, and future grammar/tool/streaming features extend this negotiation rather than changing ownership. |
| `inq-comm-dialect-envelope` | Add the canonical content/control communication envelope so model output is typed at the boundary. | `done` | `node/inquirium-core` defines `inquirium.generate.output-envelope.v1` with `content`, `epistemic`, bounded `params`, and a closed, payload-validated control vocabulary: `recall_schema`, `recall_glossary`, `propose_tool_call`, `ask_operator`, `revise_output`, plus typed crisis/degraded/refusal signals. Native `inquirium.adapter.response.v1` responses may carry the three non-content channels beside provider output; its schema uses discriminated closed control payload variants and requires `capability/ref` for tool-call proposals. The shared Python adapter helper preserves the channels, and `node/inquirium-host` assembles and validates the canonical envelope, rejects projection drift or malformed control data, rejects parameter-only empty envelopes while preserving host epistemic caveats on terminal denied/invalid outcomes, applies the configured per-operation allowlist, and returns admitted values without granting authority or executing effects. Generic `inquirium.generate` therefore forwards inert proposals only; the assistant channel is an explicit consumer of admitted operator-question and crisis proposals, persistent generate/assistant traces retain only admitted control kind names and never payloads, output capping preserves already validated channels, and idempotent transcript replay preserves the admitted control values. Unit, schema-gate, and native `http_local` daemon tests cover the adapter boundary. |
| `inq-io-rails` | Make input/output rails explicit boundary data independent of the model. | `done` | `node/inquirium-host` owns neutral `IoRailPolicy` / `IoRailMarker` data, request and output rail evaluation, JSON/string leaf traversal, deterministic marker matching, checked config conversion, and unsafe-output projection that preserves usage/cost accountability. Rails remain ordered marker data, not regex code. Input rails deny explicit secret/credential assignment markers before routing; output rails inspect normalized text, structured string leaves, and the response envelope after model return. The first policy-ordered match remains the decision reason, while diagnostics carry up to eight distinct safe policy violations without matched content. Registered schemas may declare up to 32 sorted JSON Pointers for v1 string-field redaction before semantic revalidation and release. Every non-local generate/embed/image candidate also declares its maximum egress classification; new or broader remote routes fail closed above that limit. Closed classify/rerank outputs stay under their own local-only contracts, and any future free-text rationale must add an operation-specific rail. Signed/versioned model-based evaluator critics remain an optional later evaluator implementation, not authority required by the deterministic v1 boundary. |
| `inq-session-memory-policy` | Add a host-owned `MemoryPolicy` for durable session state, reusing Projection Mode and Prompt Cache. | `done` | `node/inquirium-core` defines bounded `MemoryPolicy`, immutable `MemoryFact`, externally produced `MemorySummary`, and `MemoryProjection` contracts. The pure `node/inquirium-host::project_session_memory` function keeps pinned facts, the current summary, and the newest suffix of admitted recent facts; it reports dropped refs without mutating durable source facts and denies pinned-plus-summary overflow. The projection recomputes and validates its stable v1 token estimate rather than trusting a carried counter. Recall refs are host allowlisted. Summary production and persistence remain explicitly outside Inquirium and must be provided by another configured component or workflow with provenance. |
| `inq-temporal-context` | Inject host-owned current date/time/timezone (and known knowledge-cutoff) as a prompt layer so freshness-sensitive reasoning is correct. | `done` | `node/daemon` ships a fixed host-root `content/inquirium/temporal-context` prompt layer resolved by host-owned `inquirium.temporal_context`. The default materialized preamble carries a coarse current UTC date, validated IANA timezone, and optional host-declared knowledge cutoff; full timestamp materialization is available only through the explicit volatile `content/inquirium/temporal-context/volatile` ref for postamble/profile use. Tests use `fixed_now_utc` for deterministic regression coverage and prove the stable preamble omits the second-level timestamp. The resolved layer appears in prompt assembly metadata through `content/source = resolved-content-ref` and participates in `instruction/hash`; disabling the temporal resolver while the layer is configured fails closed at config validation or invocation, and operator-defined `content/inquirium/*` refs are rejected because the prefix is host-reserved. |
| `inq-model-snapshot-trace` | Record the provider-resolved model snapshot and effective sampling parameters in the inference trace. | `done` | `node/daemon` copies provider-reported adapter response `model` into safe `provider/model_snapshot` diagnostics, stamps deterministic-stub invocations as `deterministic_stub:v1`, records effective `max_tokens`/`temperature`/`top_p` in adapter metadata and response diagnostics, and appends metadata-only generate trace fields for `model_snapshot`, `sampling`, and `budget` beside `runtime/ref` and `model/binding-ref`. |
| `inq-prompt-versioning-regression` | Treat the assembled instruction stack as a versioned, reviewable artifact gated by golden-set regression. | `done` | `PromptAssemblyPolicy` carries `protocol/epoch`, `hierarchy/version`, a canonical policy digest, and accepted/adapted/rejected layer trace. Golden vectors cover resolved policy and adapter-body projection. Default epoch/version remain implicit only for v1; activating a non-default epoch or hierarchy fails closed unless the operation's configured `accepted_policy_digests` contains the exact canonical digest, giving distributor/operator config an explicit promotion gate. |
| `inq-response-cache` | Add an opt-in, deterministic-only response cache keyed by assembled input, model snapshot, and params. | `done` | `node/inquirium-host` defines a domain-separated canonical key over operation/contract version, selected runtime and model-binding refs, assembled input, stable model snapshot, request/runtime/model-binding parameters, effective classification, and effective policy digest. `node/daemon` implements bounded in-memory L1 over durable node-local SQLite L2 at `storage/inquirium-response-cache.sqlite`, disabled by default and separate from Memarium; both tiers repeat canonical key material, apply independent TTL and entry/byte bounds, write transactionally to SQLite before L1, repopulate L1 on hits, and reject unknown future schema versions. Entries that fit L2 but exceed the L1 byte bound remain durable L2-only values; one set-based transactional prune enforces both L2 entry and byte limits. The first admitted operation is deterministic `embed`; candidates without a stable model hash bypass the cache, conformance runs bypass it, validated hits preserve runtime/binding affinity and clear provider usage so accounting is not charged twice, and cache corruption or storage failure falls back to a real invocation. Sampled generation and other operations remain uncached until they gain an explicit deterministic admission rule. |
| `inq-output-safety-rail` | Add a host-owned output safety classification rail producing a typed unsafe outcome. | `done` | `node/inquirium-core` includes `GenerateOutcome::Unsafe` plus `OutputProjection::Unsafe { policy/ref, reason }`; `node/inquirium-host` converts completed output matching deterministic host rules into an empty-output unsafe response before caller release, preserves usage/cost accountability, and emits bounded multi-violation diagnostics. Schema-owned string redaction is applied before semantic revalidation; invalid pointers or non-string targets fail closed rather than weakening the schema. `node/daemon` supplies policy data and persists only safe diagnostics. Broader taxonomies, operator review workflows, and signed evaluator runtimes are additive later profiles. |
| `inq-flow-ir` | Treat model-authored multi-step plans as candidate data compiled by the host, never as executable flows emitted by an adapter. | `done` | `node/inquirium-core` defines bounded `CandidatePlan` and host-owned `InquiryFlowV1` graph contracts with budgets, cancellation policy, typed inquiry/effect-proposal nodes, and bounded loop edges. Adapter-authored candidates carry `adapter.manifest/ref`; the pure `node/inquirium-host::compile_candidate_plan` compiler requires `returns/plan` and exact selected-manifest equality. Portable envelope-admitted candidates must omit that local implementation ref and use the separate `compile_portable_candidate_plan` entry point. Both compilers validate operation policy, host grants, budget ceilings, and cycle bounds, bind grant refs, and emit only `pending` nodes under a content-addressed flow ref. Neither performs scheduling or effects; execution, retries, lifecycle, and terminal `Cancelled` outcomes remain responsibilities of Agent, JSON-e Flow, Sensorium, or the daemon composition root. |
| `inq-corpus-experiment-handoff` | Carry a content-addressed `CandidatePlan` from Corpus deliberation into requester-owned host admission without turning model text into authority. | `done` | `corpus-reasoning-experiment-proposal.v1` binds a portable plan artifact with no `adapter.manifest/ref` to the exact query, Room, retained turn, author node, executor, classification, expiry, and signature. The daemon resolves requester choice through monotone distributor/operator/interface ceilings, verifies and loads the bounded artifact, invokes the portable pure compiler under a host-owned operation allowlist plus grant, budget, and loop ceilings, and persists only an `admitted-inert` flow. Effect-bearing plans fail closed without a current host-verified executor binding and its exact grant. The first executable Story 012 vertical prepares a metadata-only latest-state passage for a local Agent, verifies the content-addressed Inquirium product under a closed `propose|no-effect` decision contract, prevents `no-effect` from reaching claim/invoke, and binds `propose` to the exact flow node, actuation interface, grant, generation, operational context, method, input schema, payload digest, classification, lease ceiling, and proposal expiry. It then requires HIL and delegates `claim -> invoke -> release` to P083 so no lease exists during inference. Remote Chair, participant, and deterministic compiler modes remain portable policy vocabulary but fail daemon admission until separately evidenced passage adapters exist. |
| `inq-cost-budget-enforcement` | Make token and cost budgets enforced contracts with metering and a typed exhaustion outcome. | `done` | `node/inquirium-host` owns the pure generate budget snapshot plus durable policy config with per-principal, per-session, per-operation, and per-agent token/cost ceilings. `node/daemon` injects bounded output limits, persists scoped SQLite charges, replays exact duplicate charges idempotently, checks configured counters before generate/embed/assistant invocation, requires matching scope refs, rejects orphan agent charges, returns typed `budget_exceeded`, and records final provider usage. Generate planning uses the complete assembled message estimate for context-window admission. Structured-output preflight now reserves the primary call plus every admitted repair; final usage aggregates all actual repair attempts before charge emission. Current transports have no hidden automatic retry loop. Deterministic embedding-cache hits clear provider usage before the shared final-charge path and retain the original counters only under `cache/origin-usage`, so a hit is not charged as a second provider invocation. Any future retry or cached operation must pass through the same accounting boundary. |
| `inq-locale-policy` | Declare the operator/caller response locale distinct from the instruction language. | `done` | `node/inquirium-core` defines canonical, bounded BCP 47-shaped `LocalePolicy` with at most 32 allowed response locales and explicit `response/locale` request fields. Structural validation covers language/extlang/script/region/variant ordering, extension singletons and required values, terminal private-use subtags, and duplicate extension/variant rejection; it intentionally does not claim IANA registry validation. `node/inquirium-host` resolves the operator locale by default, admits authenticated caller narrowing only within the configured allowlist, keeps `instruction/locale` independent, and injects the resolved response locale as a required fixed HostRoot prompt layer plus `dialect.params.language`/trace metadata. The locale layer participates in the prompt token budget and `instruction/hash`. Daemon config owns the policy; model output cannot override it, and provider field names remain canonical. |
| `inq-config-ownership` | Move Inquirium config types and domain constants out of daemon-local config into an Inquirium-owned config module. | `done` | `node/inquirium-host` now owns reusable Inquirium config data and defaults for `InquiriumConfig`, `PromptAssemblyPolicyProviderConfig`, `PromptContentRefConfig`, `InquiriumTemporalContextConfig`, `InquiriumIoRailsConfig`, built-in temporal `content/ref` constants, prompt content-ref byte caps, and base prompt assembly constants. `node/daemon` keeps file/env loading, layered config composition, runtime catalog sourcechain validation, and effect authority, while using compatibility aliases and mapping host validation failures to `DaemonError::InvalidConfig`. Coverage includes `cargo test -p orbiplex-node-daemon config::tests --lib`, `cargo test -p orbiplex-node-daemon model_runtime_host::tests --lib`, and `cargo clippy -p orbiplex-node-inquirium-host --lib --no-deps -- -W clippy::pedantic`. |
| `inq-capability-dispatch-table` | Replace hand-wired `inquirium.*` daemon host-capability routing with table-driven organ-host registration. | `done` | `node/daemon` now keeps Inquirium host-capability dispatch registrations as data: each registered `inquirium.*` capability maps an already Capability Registry-defined id to daemon-owned handler functions plus inference-authority and local-control policy metadata. Discovery and dispatch share that table, unknown or duplicate coverage is tested fail-closed, and Capability Registry remains the admission authority rather than the registration table redefining capability meaning. The shared `host-capabilities` fallback policy no longer carries Inquirium-specific authorization rules, so the table is the single Inquirium dispatch-policy source. |
| `inq-effect-intent-vocabulary` | Define returned-value effect intents such as `GenerateDecision`, `TraceFact`, `TranscriptWriteIntent`, and `BudgetCharge`. | `done` | `node/inquirium-host` owns the typed returned-value effect intent vocabulary: `TraceFactIntent`, `TranscriptWriteIntent`, expanded `BudgetCharge`, `ArtifactOutputIntent`, the `InquiriumEffectIntent` sum type, and operation decision wrappers for generate, embed, and assistant turn. These are serializable data with validation, required idempotency/correlation handles for effect execution, strict `request/digest` plus `request/digest-alg` pairing, final-charge operation/runtime invariants, artifact output provenance refs, and no daemon write ports. Tests cover validation and assistant transcript plan conversion into transcript-write intents. |
| `inq-effect-intent-execution-path` | Make returned-value effect intents the active daemon execution path across Inquirium. | `done` | Follow-up from the resolved Effect Intent Consumption Boundary decision. `node/daemon` now has Inquirium effect-intent interpreters at the composition roots that own the required effect authority. Generate, embed, and assistant trace records are executed as `TraceFactIntent`; assistant transcript turn/result facts are returned as `TranscriptWriteIntent` values and written through the interpreter into the existing Memarium-first/local-fallback transcript store. Duplicate assistant replay still writes only duplicate metadata trace and does not duplicate transcript facts. Budget-charge intents are durably recorded under the daemon-owned `<data-dir>/storage/inquirium-budget.sqlite` registry with idempotency-key replay protection and conflict rejection; generate, embed, and assistant-turn responses that carry token/cost usage metadata emit final budget charges through the interpreter. `inquirium.embed.response.v1` carries selected `runtime/ref` and `model.binding/ref`, so direct embed metering no longer depends on diagnostics fields. `batch.embed` artifact output is planned as an `ArtifactOutputIntent`; the shared daemon artifact-output effect interpreter validates the operation-bound write lease, verifies digest and size through the object store, persists `inquirium.model-runtime.artifact-descriptor.v1`, and rejects conflicting descriptor replay for the same `artifact/ref`. Future operation-specific writes should add typed intents before daemon execution rather than reopening inline endpoint writes. |
