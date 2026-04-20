# Proposal 049: JSON-e Middleware Transformer Executor

Based on:

- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/027-middleware-peer-message-dispatch.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/70-examples/middleware/role-module/README.md`
- `node:nse/README.md`
- `node:middleware-runtime/README.md`

## Status

Draft

## Date

2026-04-20

## Executive Summary

Orbiplex Node should add a new low-power middleware executor class for
declarative JSON transformations and bounded host-owned flows:

- `json_e`
- `json_e_flow`

The executor evaluates a JSON-e template against a host-provided JSON context
and returns host-validated data: a middleware decision, a service dispatch
response, or an intermediate value in a host-owned flow.

A JSON-e middleware instance is still a first-class middleware instance. It can
be registered, bound into middleware chains, exposed as a role capability, traced,
validated, and operated like other middleware. Its distinctive property is that
the implementation artifact may be only configuration: one operator-owned JSON
fragment can define the middleware identity, bindings, context projection, helper
profile, limits, and template.

This proposal intentionally treats JSON-e as a **data transformer**, not as an
ambient scripting language. JSON-e may construct JSON values, apply conditions,
bind local values, map over collections, and call a small host-provided set of
pure helper functions. It MUST NOT perform filesystem, network, storage,
process, or host capability effects directly.

For effectful role-middleware use cases, the Node should add a companion flow
profile:

- `json_e_flow`

In that profile JSON-e renders step inputs, while the host executes explicitly
declared steps such as `validate`, `call`, `extract`, and `respond`. The host,
not the template, remains the authority over effects, passports, allowlists,
timeouts, audit, and failure policy.

The motivating use case is role middleware. Today a role module can be a
supervised HTTP service such as `story009-roles`. That is appropriate for
powerful domain logic, but too heavy for simple roles that only match a request,
construct a Sensorium directive, extract selected fields, and build a
`service-dispatch-response`. A JSON-e executor gives those cases a smaller,
more auditable authoring surface without making role middleware a special case.

For this proposal, MVP is proven when story-009 can replace the current
`story009-roles` supervised Python middleware layer with five small
configuration-driven `json_e_flow` middleware instances:

- `role.bielik-researcher.execute`,
- `role.bielik-illustrator.execute`,
- `role.bielik-editor-in-chief.execute`,
- `role.bielik-git-publisher.execute`,
- `role.bielik-publication-verifier.execute`.

Each instance owns its role capability id, Sensorium action id, context
projection, result-field allowlist, Memarium fact template, and final
`service-dispatch-response` template. The Sensorium OS scripts remain the
effectful execution layer; JSON-e flow replaces only the role adapter daemon.

## Context and Problem Statement

Orbiplex middleware currently has several execution surfaces:

- `nse_rhai` for in-process policy hooks,
- `command_stdio` for bounded one-shot command execution,
- `local_http_json` for unmanaged loopback HTTP JSON services,
- `http_local_json` for supervised long-lived loopback HTTP JSON services.

These surfaces cover powerful extension needs, but they leave a gap for
**declarative data adapters**.

The minimal role-module example in `70-examples` performs a small set of
mechanical tasks:

- validate `capability_id`,
- validate `role/capability_id`,
- read `request/input`,
- construct a `service-dispatch-response`.

The richer `story009-roles` module adds real story-specific behavior, but much
of its code is still mechanical:

- map `role/capability_id` to a Sensorium `action_id`,
- map `role/capability_id` to a `service_type`,
- filter the returned Sensorium JSON to an allowlisted field set,
- build a `sensorium-directive.v1`,
- build a Memarium fact request,
- derive an idempotency key,
- build a pointer-sized `service-dispatch-response`,
- optionally publish a workflow-step completion record.

Those actions are naturally data transformations plus host-owned effects. Using
a whole supervised HTTP service for every such adapter raises the entry cost and
the operational surface:

- authors need a process, port, health endpoint, init endpoint, and deployment
  shape,
- the daemon must supervise another component,
- security review must cover a general-purpose language runtime,
- simple mapping logic becomes harder to inspect than the data contract it
  implements.

Orbiplex needs a middle stratum between "full middleware process" and "hard-coded
Rust behavior": a constrained, inspectable data transformer.

## Design Principles

- **Data first.** The executor consumes and returns JSON values. The host maps
  those values into typed contracts and rejects invalid outputs.
- **No ambient effects.** JSON-e templates cannot open files, spawn processes,
  perform network calls, mutate storage, or invoke host capabilities.
- **Host-owned effects.** Any effectful step is declared outside JSON-e and
  executed by the host under the same passport, allowlist, timeout, and audit
  discipline as ordinary capability calls.
- **Standard language, local profile.** Orbiplex should use JSON-e semantics
  where possible and avoid patching the JSON-e parser or inventing hidden
  operators.
- **Small helper surface.** Host-provided functions are pure, explicit, and
  versioned as part of the executor profile.
- **Fail closed where authority is involved.** Invalid template output, missing
  required values, schema mismatch, or disallowed effect declarations reject the
  invocation according to the host hook's failure policy.
- **Trace every evaluation.** Each evaluation emits a trace with template id,
  template digest, executor profile version, input/output summaries, duration,
  and validation outcome.
- **Operator-owned projection.** The operator, not a distributed template author,
  decides which host values are projected into the JSON-e authoring context for a
  concrete middleware instance.
- **First-class middleware.** A JSON-e middleware instance is not a partial hook
  or an implementation detail. It participates in the same middleware registry,
  chain binding, role capability, trace, validation, and operator lifecycle
  concepts as other middleware executor classes.
- **Escalate when flow becomes orchestration.** When a `json_e_flow`
  middleware needs many steps, dynamic step generation, broad scratch state, or
  repeated loops to express its behavior, operators should consider `nse_rhai`
  or `http_local_json` instead. JSON-e flow is for bounded declarative host-owned
  call sequences, not for recreating a general orchestration engine.

## Executor Profiles

### `json_e`

`json_e` is the pure transformer profile.

Input:

- one JSON-e template,
- one host-provided context object conforming to a stable authoring contract,
- one expected output contract selected by the host configuration.

Output:

- one JSON value rendered by JSON-e.

The host then validates the value against the expected contract. Examples:

- `middleware-decision.v1`,
- `service-dispatch-response`,
- a route or annotation object owned by a specific hook,
- a host-local intermediate value.

The executor class name `json_e` identifies the execution surface. The concrete
semantics live in explicit profile fields, for example:

- `profile_version`: `orbiplex.json_e.v1`,
- `helper_profile`: `orbiplex.json_e.helpers.basic.v1`,
- `context_contract`: `json_e.context.role_execute.v1`,
- `output_contract`: `service-dispatch-response.v1`.

For the same template digest, helper profile, limits, and context JSON value,
`json_e` evaluation MUST produce the same output or the same validation failure
class.

The `json_e` executor is suitable for:

- simple role endpoints that only construct a response,
- payload normalization,
- annotation and rewrite decisions,
- route selection,
- filter-style decisions,
- fixture or demo middleware,
- pointer-sized response construction.

It is not suitable for:

- direct Sensorium action execution,
- direct Memarium writes,
- long-running tasks,
- streaming,
- retries and backoff,
- OS integration,
- persistent local state.

### `json_e_flow`

`json_e_flow` is a host-owned flow profile built around JSON-e.

A flow is a list of declarative steps. JSON-e renders step inputs, but the host
interprets and executes the step semantics.

Candidate step kinds:

- `render` — evaluate a JSON-e template into a named value,
- `validate` — validate a named value against a JSON Schema or typed host
  contract,
- `call` — invoke an allowlisted host capability with a named value,
- `extract` — select a named subvalue from a previous result,
- `respond` — return a host-validated response contract,
- `fail` — return a controlled rejected or failed response.

`json_e_flow` is suitable for role middleware that needs controlled host
capability calls, for example:

1. render a `sensorium-directive.v1`,
2. call `sensorium.directive.invoke`,
3. extract allowlisted result fields,
4. render a `memarium.write` request,
5. call `memarium.write`,
6. render a `service-dispatch-response`.

The host MUST validate every effectful `call` against:

- the invoking module's capability passport,
- local allowlists,
- the current hook's allowed call set,
- timeout and output-size budgets,
- audit policy,
- failure policy.

The statically owned parts of a flow, such as step kind, step name, capability
identifier, input path, output contract, helper profile, timeout override, and
allowed-call declaration, MUST be validated at load time where possible. JSON-e
templates may render request bodies and intermediate values, but they MUST NOT
select which host capability is invoked.

`json_e_flow` may later support loops, dynamically generated steps, temporary
registers, or scratch values when a concrete middleware use case needs that
power. Those features increase the evaluator's operational cost and make flow
behavior harder to audit. They MUST therefore be guarded by explicit profile
support, resource limits, trace coverage, and documentation that warns operators
to use them only when a simpler static flow is insufficient.

### Resource budget and execution timeout

Every `json_e` and `json_e_flow` middleware instance MUST declare an explicit
execution timeout in `limits.timeout_ms`. A JSON-e middleware must never have an
implicit unbounded evaluation window just because it is "only" a data
transformer.

For pure `json_e`, `limits.timeout_ms` is the wall-clock budget for one
transform invocation: context projection, template evaluation, and output
contract validation. At minimum, every conforming implementation MUST enforce
the budget across template evaluation and helper execution.

For `json_e_flow`, the same field is the overall budget for one flow invocation.
Individual host-owned `call` steps MAY also carry stricter per-call timeouts,
but they MUST NOT extend the total flow beyond the remaining
`limits.timeout_ms` budget.

This timeout is distinct from process and loopback-service timeouts used by
`command_stdio`, `local_http_json`, or `http_local_json`. JSON-e does not spawn a
process, but it still consumes CPU, memory, and operator attention; its
configuration therefore needs its own evaluation budget. Exceeding the budget
fails closed with a stable resource-limit or executor-timeout failure and emits
the measured duration in the evaluation trace.

Every `json_e_flow` middleware MUST have explicit step limits. Suggested defaults:

- `max_flow_steps`: 32 total executed steps per invocation,
- `max_loop_steps`: 128 total loop body executions per invocation.

Exceeding either limit fails the invocation with a stable resource-limit failure
class. A middleware that routinely needs higher limits should be reviewed as a
candidate for `nse_rhai` or `http_local_json`.

Policy-sensitive decisions such as egress classification SHOULD be represented
as host-owned `validate` or `decide` steps in `json_e_flow`, rather than as
ambient JSON-e helpers.

## Authoring Context

The JSON-e context is a stable, versioned authoring contract. It is not the raw
wire request and not a dump of daemon internals. For role execution, a host may
provide a contract such as:

- `json_e.context.role_execute.v1`

The contract defines stable field names and semantics for template authors, while
the operator controls which source values are projected into that context for a
specific middleware instance.

This projection MUST be local operator configuration, not a distribution-time
authority decision shipped by an unrelated module author. A module package may
document its expected context fields, but the Node operator decides which host
values are visible to the template in that deployment.

The projection should be easy to express near the concrete middleware
configuration. A representative shape:

```json
{
  "context_contract": "json_e.context.role_execute.v1",
  "context_projection": {
    "capability_id": "$.capability_id",
    "role_capability_id": "$['role/capability_id']",
    "dispatch_id": "$['dispatch/id']",
    "request_input": "$['request/input']",
    "workflow_run_id": "$['workflow/run-id']",
    "workflow_phase_id": "$['workflow/phase-id']",
    "correlation_id": "$['correlation/id']",
    "now": {"host_value": "invocation.rfc3339_now"}
  }
}
```

The exact projection syntax is an implementation detail. The contract is that
projection is explicit, reviewable, and evaluated by the host before JSON-e
receives a context value.

Context projection is part of the security boundary. Values MUST NOT be exposed
to a template merely because they are present in the invocation envelope.
Forbidden or strongly controlled context values include:

- raw bearer tokens,
- private keys and sealed payload plaintext,
- full capability passports when only a `capability_id` is needed,
- full classified facts when a label, digest, or field projection is enough,
- host internals such as filesystem paths, sockets, daemon configuration, and
  local process details.

## Operator Workflow

JSON-e middleware should be easy to create as configuration, without requiring a
separate script directory, service process, port, health endpoint, or launcher.
The operator workflow should be:

1. Create one JSON configuration fragment under the node configuration layer,
   for example `<data_dir>/config/50-role-example-summarizer.json`.
2. Add one JSON-e middleware entry under the node's JSON-e middleware registry,
   provisionally `middleware_json_e`.
3. Give the instance the same operational identity fields used by other
   middleware: `id`, `module_id`, `component_id`, human-facing name or
   description when supported, and chain or role bindings.
4. Select `profile_version`, `context_contract`, `context_projection`,
   `output_contract`, `helper_profile`, exposed `helpers`, `limits`, and
   `template`.
5. Run node configuration validation, for example
   `orbiplex-node-daemon check-config`, before enabling or reloading the daemon.

The exact top-level key should be finalized during implementation. The important
contract is that a JSON-e middleware instance is registered through the same
configuration-loading path as other operator-managed middleware. It should not
require a sidecar project layout merely to express a data transformation.

A representative operator-owned fragment:

```json
{
  "middleware_json_e": {
    "role-example-summarizer": {
      "id": "role-example-summarizer",
      "module_id": "role.example-summarizer",
      "component_id": "middleware.role.example-summarizer",
      "module_name": "Example summarizer role",
      "executor": {
        "kind": "json_e",
        "template_id": "role.example-summarizer.execute.v1",
        "profile_version": "orbiplex.json_e.v1",
        "context_contract": "json_e.context.role_execute.v1",
        "context_projection": {
          "capability_id": "$.capability_id",
          "role_capability_id": "$['role/capability_id']",
          "dispatch_id": "$['dispatch/id']",
          "request_input": "$['request/input']",
          "workflow_run_id": "$['workflow/run-id']",
          "workflow_phase_id": "$['workflow/phase-id']",
          "correlation_id": "$['correlation/id']",
          "now": {"host_value": "invocation.rfc3339_now"}
        },
        "output_contract": "service-dispatch-response.v1",
        "helper_profile": "orbiplex.json_e.helpers.basic.v1",
        "helpers": ["default", "has", "pick", "idempotency_key"],
        "limits": {
          "max_template_bytes": 32768,
          "max_context_bytes": 65536,
          "max_output_bytes": 65536,
          "max_evaluation_depth": 64,
          "max_flow_steps": 32,
          "max_loop_steps": 128,
          "timeout_ms": 100
        },
        "template": {
          "schema_version": "v1",
          "capability_id": "service_dispatch_execute",
          "status": "completed",
          "dispatch/id": "${dispatch_id}",
          "completed-at": "${now}",
          "answer/content": {"summary": "${request_input.text}"},
          "answer/format": "application/json",
          "confidence/signal": 0.75,
          "human-linked-participation": false,
          "provenance/origin-classes": ["role-module", "json-e"]
        }
      },
      "bindings": {
        "role_capability_id": "role.example-summarizer.execute"
      }
    }
  }
}
```

This shape is intentionally configuration-driven. A larger template may later be
loaded from an explicit host-owned module store or a config-relative reference,
but inline configuration should be sufficient for the MVP.

Distribution packages may provide examples or disabled default fragments, but
authority-bearing context projection remains an operator decision. Enabling a
JSON-e middleware instance means reviewing the projection, helper exposure,
limits, and bindings in the local configuration.

## JSON-e Use Profile

Orbiplex should keep the JSON-e language surface recognizable.

Allowed standard JSON-e features SHOULD include:

- string interpolation,
- `$eval`,
- `$if`,
- `$switch`,
- `$match`,
- `$let`,
- `$map`,
- `$reduce`,
- `$merge`,
- `$mergeDeep`,
- `$flatten`,
- `$json`.

The executor MAY restrict expensive or operationally risky constructs by local
profile limits, for example:

- maximum template size,
- maximum context size,
- maximum output size,
- maximum evaluation depth,
- maximum collection size for `$map` and `$reduce`,
- maximum string size,
- required wall-clock evaluation timeout (`limits.timeout_ms`).

The executor MUST reject templates that render non-finite numbers or values that
cannot be represented in the committed JSON contract.

## Extension Policy

Orbiplex SHOULD NOT extend the JSON-e parser or add custom `$orbiplex...`
operators as a first-line extension mechanism.

The preferred extension order is:

1. use standard JSON-e features,
2. add host-provided pure functions to the context,
3. add host-owned `json_e_flow` step kinds outside JSON-e,
4. only then consider an Orbiplex-specific JSON-e profile extension.

Host-provided functions MUST be exposed through an explicit `helper_profile`.
Each helper profile defines:

- function names,
- arity,
- JSON input and output contracts,
- determinism expectations,
- failure modes,
- resource-cost limits,
- confirmation that the function performs no effects.

The middleware configuration SHOULD explicitly select which functions from a
known helper profile are visible to the template. A representative shape:

```json
{
  "helper_profile": "orbiplex.json_e.helpers.basic.v1",
  "helpers": [
    "sha256_json",
    "sha256_text",
    "default",
    "has",
    "pick",
    "idempotency_key"
  ]
}
```

Host-provided functions MUST be explicit, versioned, auditable, and pure with
respect to their arguments. They may compute deterministic values from
materialized JSON inputs. They MUST NOT read ambient host state, consult mutable
policy stores, or smuggle authority into the template under the appearance of a
helper function.

Time is therefore supplied as a host-owned context value such as `now`, fixed once
per invocation, rather than as a JSON-e-callable clock function.

The initial `orbiplex.json_e.helpers.basic.v1` profile should contain only
mechanical helpers:

- `sha256_json(value)` — deterministic hash over canonical JSON,
- `sha256_text(value)` — hash over a UTF-8 string,
- `default(value, fallback)` — null/missing fallback,
- `has(value, path)` — path existence check,
- `pick(value, fields)` — object field projection,
- `idempotency_key(parts)` — deterministic idempotency key over explicit JSON
  parts.

`idempotency_key(parts)` MUST be deterministic across conforming Orbiplex Nodes
for the same helper profile version, canonical JSON serialization profile, and
the same `parts` JSON value. It MUST NOT include host-local identity, node id,
wall-clock time, random material, local configuration, or hidden salt. If a
deployment needs node-local idempotency, the operator must pass an explicit node
or deployment identifier as one of the `parts`.

Helper profile versions are compatibility contracts. A new helper profile version
such as `orbiplex.json_e.helpers.basic.v2` MUST load in parallel with earlier
supported versions during a deprecation window. Existing templates continue to
select their declared helper profile until the operator migrates them or the
profile is explicitly removed by a documented compatibility policy. Helper
semantics MUST NOT be silently changed in-place within a stable profile version.

Host-provided functions MUST NOT perform effects. Specifically, the following
are forbidden inside JSON-e:

- filesystem reads or writes,
- network calls,
- process execution,
- storage mutation,
- host capability invocation,
- signer, sealer, or key-backend access,
- access to ambient daemon internals.

If a template needs those effects, the surrounding `json_e_flow` must declare a
host-owned `call` step.

## Validation and Error Classes

The host should separate configuration errors, input/context errors, evaluation
errors, output validation errors, and authority errors. Suggested failure classes:

| Failure class | Meaning |
| :--- | :--- |
| `template-load-error` | The template or wrapper cannot be parsed, compiled, or accepted at configuration load time. |
| `context-contract-error` | The host cannot construct a context value that satisfies the selected context contract. |
| `evaluation-error` | JSON-e evaluation fails for reasons other than resource limits. |
| `resource-limit-exceeded` | Template evaluation exceeds a configured size, depth, collection, string, or time budget. |
| `max-flow-steps-exceeded` | A `json_e_flow` invocation exceeds its configured total executed step budget. |
| `max-loop-steps-exceeded` | A `json_e_flow` invocation exceeds its configured loop body execution budget. |
| `output-contract-error` | The rendered JSON value does not satisfy the selected output contract. |
| `disallowed-call` | A `json_e_flow` step requests a call not allowed by the flow profile, hook policy, passport, or local configuration. |
| `capability-call-failed` | A host-owned `json_e_flow` capability call was allowed but failed during execution. |
| `flow-policy-rejected` | A host-owned `json_e_flow` `validate` or `decide` step rejected the flow. |

Load-time validation should check:

- wrapper schema,
- profile version,
- output contract,
- context contract,
- helper profile and explicitly exposed helper names,
- resource limits,
- template syntax or compileability where the JSON-e implementation supports it,
- literal-only `$eval` usage, rejecting any form where an expression string could
  be supplied by invocation context,
- static flow step structure for `json_e_flow`,
- declared capability allowlists for `json_e_flow`.

Invocation-time validation should check:

- context projection and context contract,
- resource limits,
- rendered output contract,
- authority and policy for every host-owned `json_e_flow` call,
- failure mapping according to the current hook's failure policy.

## Trace and Replay Contract

JSON-e evaluation should be replayable without granting access to secrets. Each
evaluation should emit a trace event, but durable trace retention MAY use
sampling or adaptive retention to keep hot paths low-cost. Failures SHOULD be
retained at 100%. Successful evaluations MAY be sampled, aggregated, or retained
for a bounded window according to local policy.

Each trace event should include:

- template id,
- template digest,
- profile version,
- helper profile,
- exposed helper names,
- context contract,
- context digest,
- redacted context summary,
- output contract,
- output digest when rendering succeeds,
- validation outcome,
- duration,
- failure class when applicable.

Trace records MUST NOT contain raw secret-bearing context values unless the hook
explicitly authorizes retention for that field class. For `json_e_flow`, the flow
trace should additionally link step id, capability id, request digest, response
digest, and decision or failure reason.

When evaluation or validation fails, diagnostics SHOULD include a source-map
location that points to the template location responsible for the error: JSON
path at minimum, and line/column when the source representation preserves it.

## Relationship to NSE/Rhai

`nse_rhai` and `json_e` serve different strata.

`nse_rhai` is a bounded scripting layer for local policy hooks and mini
orchestration. It is appropriate when an operator needs real expressions,
branching, helper functions, and a script-like authoring model.

`json_e` is a data-template transformer. It is appropriate when the behavior can
be expressed as JSON construction, field projection, conditionals, and simple
collection transforms.

The two may coexist:

- `nse_rhai` for higher-power policy hooks,
- `json_e` for low-power, inspectable adapters,
- `http_local_json` for full supervised modules,
- `command_stdio` and Sensorium OS actions for actual OS/process effects.

The default recommendation is to start with the least powerful executor that
can express the behavior.

## Relationship to Role Middleware

Role middleware is not a special executor class. It is a hosted capability
surface that Dator can route service orders into.

Today a role can be implemented as a supervised HTTP service:

```text
Dator -> role capability -> http_local_json module
```

With this proposal, a role may also be implemented by `json_e` or
`json_e_flow`:

```text
Dator -> role capability -> json_e/json_e_flow executor
```

Both shapes expose the same host capability identity and return the same
`service-dispatch-response` contract. Both are first-class middleware instances;
the difference is implementation shape and power:

- JSON-e role modules are small, declarative, and effect-free unless wrapped by
  host-owned flow steps. Their implementation may be a single operator-owned
  configuration fragment.
- HTTP role modules are powerful, process-backed, and suitable for richer domain
  logic. Their implementation includes a service process plus supervisor-owned
  lifecycle and readiness concerns.

This gives operators and module authors a clear choice without changing Dator's
service-order routing semantics.

## Story-009 MVP Slice

Story-009 is the acceptance slice for the `json_e_flow` profile. The mechanism
reaches MVP when the `story009-roles` supervised Python middleware can be
replaced by five configuration-driven JSON-e flow middleware instances:

| Role capability | Sensorium action | Result projection | Memarium fact |
| :--- | :--- | :--- | :--- |
| `role.bielik-researcher.execute` | `story009.draft.compose` | draft branch, commit, path, signature tracker, Memarium id | `story009.git-commit-produced` |
| `role.bielik-illustrator.execute` | `story009.image.place` | illustrated commit, image paths/count, signature tracker, Memarium id | `story009.git-commit-produced` |
| `role.bielik-editor-in-chief.execute` | `story009.editorial.review` | editorial decision, rejection details, reviewed commit, notes, Memarium id | `story009.editorial-review` |
| `role.bielik-git-publisher.execute` | `story009.review.publish` | publish branch/commit, push status, rejection details, signature tracker, Memarium id | `story009.git-commit-produced` |
| `role.bielik-publication-verifier.execute` | `story009.publication.verify` | verification status/kind, evidence, retryability, commit and publication pointers, Memarium id | `story009.publication-verified` |

Each JSON-e flow instance should follow the same high-level shape:

1. validate role capability and service type,
2. render a `sensorium-directive.v1`,
3. call `sensorium.directive.invoke`,
4. extract an allowlisted result projection,
5. render a role-specific `memarium.write` fact request,
6. call `memarium.write`,
7. render a `workflow.step.completed` record and publish it through the
   host-owned `workflow.step.completed.publish` capability,
8. render a `service-dispatch-response.v1`,
9. respond.

This does not remove the story-009 Sensorium OS scripts. Those scripts still own
the domain effects: model execution, Git worktree access, commit production,
publication push, and publication verification. The JSON-e flow middleware owns
the declarative role-adapter layer between Dator, Sensorium, Memarium, and the
service-dispatch response.

The JSON-e flow engine MUST NOT know whether
`workflow.step.completed.publish` is backed by Agora, local storage, another
middleware component, or a future audit service. It only invokes the named host
capability under the ordinary passport, allowlist, timeout, audit, and failure
policy. Any concrete publication backend belongs behind that capability boundary,
or inside the concrete middleware configuration when an operator deliberately
chooses a lower-level capability.

For this capability, "publish" means host-owned admission of a validated workflow
step completion record into the node's configured workflow completion record
plane. A successful response means the host accepted the record, assigned or
resolved a stable `record_id`, and made the record available to local workflow
reconstruction according to the node configuration.

It does not imply global broadcast, peer delivery, final workflow completion, or
any specific backing store such as Agora. The published record remains the
domain fact, for example `record/kind = workflow.step.completed` with
`schema = story009.workflow-step-completed.v1`; the capability name denotes only
the host-owned operation that admits that fact.

The story-009 MVP should include at least one executable regression proving that
the five JSON-e flow middleware instances can replace the supervised
`story009-roles` HTTP-local adapter while preserving the existing acceptance
properties:

- Dator routes each service order to the matching role capability,
- each role invokes only its configured Sensorium action,
- each role writes its local Memarium fact with a deterministic idempotency key,
- the response remains pointer-sized,
- node C remains the only node exposing the publish action,
- the final workflow can still be reconstructed from local Memarium facts and
  editorial Agora records.

The official story-009 operator profile uses this JSON-e-flow role adapter
shape. Dator offers still point at the same `role.bielik-*.execute`
capabilities; the daemon now serves those capabilities from
`middleware_json_e_flow_services` entries instead of starting a dedicated
`story009-roles` Python service.

## Example: Pure Role Response

This example shows the pure `json_e` profile for a role that produces a simple
pointer-sized response without calling Sensorium or Memarium.

```json
{
  "schema": "middleware-json-e.v1",
  "template_id": "role.example-summarizer.execute.v1",
  "profile_version": "orbiplex.json_e.v1",
  "context_contract": "json_e.context.role_execute.v1",
  "context_projection": {
    "capability_id": "$.capability_id",
    "role_capability_id": "$['role/capability_id']",
    "dispatch_id": "$['dispatch/id']",
    "request_input": "$['request/input']",
    "workflow_run_id": "$['workflow/run-id']",
    "workflow_phase_id": "$['workflow/phase-id']",
    "correlation_id": "$['correlation/id']",
    "now": {"host_value": "invocation.rfc3339_now"}
  },
  "output_contract": "service-dispatch-response.v1",
  "helper_profile": "orbiplex.json_e.helpers.basic.v1",
  "helpers": [
    "sha256_json",
    "sha256_text",
    "default",
    "has",
    "pick",
    "idempotency_key"
  ],
  "template": {
    "schema_version": "v1",
    "capability_id": "service_dispatch_execute",
    "status": {
      "$if": "capability_id == 'role_task_execute' && role_capability_id == 'role.example-summarizer.execute'",
      "then": "completed",
      "else": "rejected-invalid-request"
    },
    "dispatch/id": "${dispatch_id}",
    "completed-at": "${now}",
    "answer/content": {
      "summary": "${request_input.text}",
      "workflow/run-id": "${workflow_run_id}",
      "workflow/phase-id": "${workflow_phase_id}",
      "correlation/id": "${correlation_id}"
    },
    "answer/format": "application/json",
    "confidence/signal": 0.75,
    "human-linked-participation": false,
    "provenance/origin-classes": ["role-module", "json-e"]
  }
}
```

The host supplies a normalized context with identifier-friendly aliases such as
`role_capability_id`, `request_input`, and `workflow_run_id`. This avoids making
authors fight path syntax for slash-delimited wire fields.

## Example: Flow Role Calling Sensorium

This example sketches the `json_e_flow` profile.

```json
{
  "schema": "middleware-json-e-flow.v1",
  "template_id": "story009.researcher-lite.v1",
  "profile_version": "orbiplex.json_e_flow.v1",
  "context_contract": "json_e.context.role_execute.v1",
  "role_capability_id": "role.bielik-researcher.execute",
  "allowed_calls": [
    "sensorium.directive.invoke",
    "memarium.write"
  ],
  "steps": [
    {
      "kind": "render",
      "as": "directive_request",
      "template": {
        "directive": {
          "schema": "sensorium-directive.v1",
          "schema/v": 1,
          "directive/id": "directive:story009:bielik-researcher:${safe_dispatch_id}",
          "directive/issued_at": "${now}",
          "issuer": {"module_id": "${module_id}"},
          "idempotency/key": "${dispatch_id}",
          "action_id": "story009.draft.compose",
          "parameters": {"$eval": "request_input"},
          "timing": {"timeout_ms": 30000, "mode": "sync"},
          "correlation/id": "${correlation_id}"
        }
      }
    },
    {
      "kind": "call",
      "capability": "sensorium.directive.invoke",
      "input": "$.directive_request",
      "as": "sensorium_result"
    },
    {
      "kind": "render",
      "as": "response",
      "template": {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "completed",
        "dispatch/id": "${dispatch_id}",
        "completed-at": "${now}",
        "answer/content": {
          "draft_commit": {"$eval": "sensorium_result.result.json.draft_commit"},
          "draft_path": {"$eval": "sensorium_result.result.json.draft_path"},
          "sensorium": {
            "directive_id": {"$eval": "sensorium_result['directive/id']"},
            "outcome_id": {"$eval": "sensorium_result['outcome/id']"}
          }
        },
        "answer/format": "application/json",
        "confidence/signal": 0.9,
        "provenance/origin-classes": [
          "role-module",
          "json-e-flow",
          "sensorium-directive"
        ]
      }
    },
    {
      "kind": "respond",
      "input": "$.response"
    }
  ]
}
```

The `call` step is not JSON-e. It is an Orbiplex host step. The host verifies
that the call is allowed and performs the actual capability invocation.

## Security Model

The `json_e` executor has no ambient authority.

The host MUST enforce:

- template source is loaded from explicit configuration or a host-owned module
  store record, not from untrusted request input,
- `$eval` expressions are literal expressions present in the loaded template,
  never strings read from context, `request_input`, previous results, or any
  other invocation-supplied value,
- template digest is recorded in every evaluation trace,
- explicit context projection before JSON-e evaluation,
- context and output size caps,
- output schema validation,
- failure policy per hook,
- no direct effect primitives in JSON-e,
- host-provided helper profile and function allowlist,
- deterministic `now` value per invocation when time is exposed,
- redaction of secret fields in traces.

The host SHOULD expose only context values needed by the template. Sensitive
values such as raw auth tokens, private keys, sealed payload plaintext, and
unredacted classified facts MUST NOT be passed into JSON-e unless the invoking
hook explicitly owns that authority and the output path is guarded.

For `json_e_flow`, every `call` step MUST be audited as a normal host capability
call. The flow trace should link:

- template id,
- step id,
- capability id,
- request digest,
- response digest,
- decision or failure reason.

## Implementation Sketch

Add a middleware-runtime executor:

```text
orbiplex-node-middleware-runtime
  src/json_e_executor.rs
```

Public shape:

```text
JsonEExecutorConfig
  id
  module_id
  component_id
  bindings
  template_id
  profile_version
  context_contract
  context_projection
  output_contract
  template
  helper_profile
  helpers
  limits

JsonEExecutor
  impl MiddlewareExecutor
```

The implementation can land in phases, but the proposal's MVP is the story-009
role replacement slice. A first engineering phase may implement the pure
`json_e` substrate to prove template loading, context projection, helper
profiles, limits, validation, dry-run, and traces. The MVP is reached only after
`json_e_flow` can replace the `story009-roles` adapter daemon with five
configuration-driven role middleware instances.

Developer experience should be part of the runtime contract, not an afterthought.
The pure `json_e` profile should expose a dry-run path that accepts a candidate
context value and returns either the rendered output or structured diagnostics
without performing effects. For `json_e` this is straightforward because the
executor is pure. For `json_e_flow`, dry-run must either stop before effectful
`call` steps or use explicit host-provided mock responses.

Phase 1 substrate scope for `orbiplex.json_e.v1`:

- support the pure `json_e` executor only,
- support static configured templates,
- support first-class middleware registration from a node JSON configuration
  fragment, without requiring a middleware script or service directory,
- support a stable authoring context contract such as
  `json_e.context.role_execute.v1`,
- support operator-owned context projection near the concrete middleware
  configuration,
- support explicit `helper_profile` and explicitly exposed helper names,
- include only mechanical helpers in `orbiplex.json_e.helpers.basic.v1`,
- support `middleware-decision.v1` and/or `service-dispatch-response.v1`
  outputs, depending on the first implementation target,
- reject direct capability calls, filesystem access, network access, process
  execution, storage mutation, signer access, sealer access, and key-backend
  access,
- enforce template, context, output, depth, collection, string, and time limits,
- record replayable redacted traces,
- provide a dry-run validation/evaluation path for pure `json_e` middleware,
- report template errors with source-map diagnostics: JSON path at minimum and
  line/column when available.

MVP scope for story-009 `orbiplex.json_e_flow.v1`:

- support first-class `json_e_flow` middleware registration from node JSON
  configuration fragments,
- support five independent role middleware instances replacing
  `story009-roles`,
- support static host-owned steps: `render`, `validate`, `call`, `extract`,
  `respond`, and `fail`,
- support allowlisted calls to `sensorium.directive.invoke` and `memarium.write`,
- support allowlisted calls to `workflow.step.completed.publish` for publishing
  story-009 workflow-step completion records without exposing any Agora-specific
  knowledge to the JSON-e flow engine,
- validate statically declared capability calls at load time and invocation time,
- enforce `max_flow_steps` and `max_loop_steps` even if the MVP uses only static
  flows,
- support role-local result-field allowlists,
- render role-specific Memarium fact requests with deterministic idempotency
  keys,
- render `service-dispatch-response.v1` outputs compatible with current Dator and
  Arca expectations,
- include dry-run support for flow with mocked or stopped effectful calls,
- include a regression that runs story-009 without the `story009-roles`
  supervised Python daemon.

Post-MVP scope:

| Capability | Notes |
| :--- | :--- |
| `validate` and `decide` steps | Host-owned policy checks, including egress classification. |
| Flow loops | Optional, profile-gated, resource-limited, and traced. |
| Dynamically generated steps | Optional, profile-gated, and never allowed to bypass host authority checks. |
| Temporary registers or scratch values | Optional, resource-limited, and visible in redacted flow traces where useful. |
| Module-store template loading | Host-owned storage path after static configured templates have real users. |
| Additional helper profiles | Added only when a concrete use case cannot be expressed by basic mechanical helpers. |

## Implementation Plan

The work should land as small, reviewable layers. Each layer should have a
schema or test fixture that makes the boundary visible.

| Step | Scope | Done when |
| :--- | :--- | :--- |
| 1 | Commit JSON-e configuration schemas | Node can validate `json_e` and `json_e_flow` middleware configuration, limits, helper exposure, context projection, and static flow shape at config-load time. |
| 2 | Implement pure `json_e` substrate | Middleware runtime can evaluate a configured JSON-e template against an operator-projected context, validate output, expose basic helpers, enforce limits, produce diagnostics, and dry-run without effects. |
| 3 | Add first-class daemon registration | Daemon config can register JSON-e middleware instances through the same operator-managed configuration layer as other middleware classes. Component snapshots and validation errors identify them as middleware, not hidden hooks. |
| 4 | Implement static `json_e_flow` | Middleware runtime supports `render`, `validate`, `call`, `extract`, `respond`, and `fail`; all `call` steps are static, allowlisted, passport-checked, traced, and budgeted. |
| 5 | Add host capability for workflow step publication | `workflow.step.completed.publish` has a narrow request/response schema and can be called by `json_e_flow` without exposing any Agora-specific backend to the flow engine. |
| 6 | Build story-009 migration fixture | Five JSON-e flow role middleware configs replace the `story009-roles` Python adapter while keeping Sensorium OS scripts, Dator offers, Memarium writes, and pointer-sized responses intact. |
| 7 | Add story-009 regression | The existing story-009 acceptance path can run without starting `story009-roles`, and still proves routing, Sensorium action isolation, Memarium fact writes, publication authority shape, and reconstruction. |

The implementation should avoid dynamic flow features until the story-009 static
flow slice proves that they are needed. Raising limits or adding flow language
features should require a concrete migration case, not convenience pressure from
one oversized template.

## Story-009 Migration Fixture

The migration fixture should live in the Node repository as implementation-side
test data. A representative layout:

```text
node:middleware-runtime/fixtures/json-e-flow/story-009/
  README.md
  00-context-role-execute.sample.json
  10-role-bielik-researcher.json
  20-role-bielik-illustrator.json
  30-role-bielik-editor-in-chief.json
  40-role-bielik-git-publisher.json
  50-role-bielik-publication-verifier.json
  expected/
    bielik-researcher.response.json
    bielik-illustrator.response.json
    bielik-editor-in-chief.response.json
    bielik-git-publisher.response.json
    bielik-publication-verifier.response.json
```

The fixture is not a new daemon module. It is a set of operator-style
configuration fragments that can be loaded by tests or copied into a node
configuration layer.

Each role fixture should contain:

- middleware identity: `id`, `module_id`, `component_id`, and role binding,
- `profile_version`: `orbiplex.json_e_flow.v1`,
- `context_contract`: `json_e.context.role_execute.v1`,
- `context_projection` for dispatch id, role capability id, service type,
  request input, workflow ids, correlation id, execution ref, timeout, and
  invocation time,
- static `allowed_calls` containing only the capabilities needed by that role,
- role-local `result_fields` allowlist,
- a `render` step for `sensorium-directive.v1`,
- a `call` step for `sensorium.directive.invoke`,
- `extract` or `render` steps for the pointer-sized answer content,
- a `render` step for the role-specific `memarium.write` request,
- a `call` step for `memarium.write`,
- a `render` step for `workflow.step.completed`,
- a `call` step for `workflow.step.completed.publish`,
- a final `respond` step returning `service-dispatch-response.v1`.

The five fixtures should keep the role-specific data explicit:

| Fixture | Role capability | Sensorium action | Memarium fact kind |
| :--- | :--- | :--- | :--- |
| `10-role-bielik-researcher.json` | `role.bielik-researcher.execute` | `story009.draft.compose` | `story009.git-commit-produced` |
| `20-role-bielik-illustrator.json` | `role.bielik-illustrator.execute` | `story009.image.place` | `story009.git-commit-produced` |
| `30-role-bielik-editor-in-chief.json` | `role.bielik-editor-in-chief.execute` | `story009.editorial.review` | `story009.editorial-review` |
| `40-role-bielik-git-publisher.json` | `role.bielik-git-publisher.execute` | `story009.review.publish` | `story009.git-commit-produced` |
| `50-role-bielik-publication-verifier.json` | `role.bielik-publication-verifier.execute` | `story009.publication.verify` | `story009.publication-verified` |

The fixture should include mocked host-call responses for dry-run tests:

- a successful `sensorium.directive.invoke` response for each role,
- a successful `memarium.write` response with one fact id,
- a successful `workflow.step.completed.publish` response,
- one failure fixture for Sensorium failure mapping,
- one failure fixture for Memarium write failure mapping,
- one failure fixture for invalid role capability or service type.

The fixture acceptance test should run in two modes:

1. dry-run mode, using mocked host-call responses and asserting rendered
   intermediate values;
2. integration mode, using the existing story-009 Sensorium OS scripts and host
   capabilities, with the `story009-roles` supervised Python middleware disabled.

Acceptance criteria for the pure profile:

- validate wrapper schema, profile version, context contract, output contract,
  helper profile, exposed helper names, and limits at config-load time,
- validate JSON-e middleware identity and bindings through the same daemon
  configuration validation path used by other middleware classes,
- compile or validate template at config-load time where the chosen Rust crate
  allows it,
- build a normalized authoring context through operator-owned context projection,
- validate the projected context before JSON-e evaluation,
- validate output against the configured contract,
- record execution trace,
- reject oversized input or output,
- emit stable failure classes for load, context, evaluation, resource-limit, and
  output-contract failures,
- satisfy the determinism invariant for identical template digest, helper
  profile, limits, and context JSON value,
- include unit tests for `$if`, `$switch`, `$let`, `$map`, and missing-field
  failure behavior,
- include negative tests proving `$eval` cannot evaluate expressions sourced
  from context or request input,
- include dry-run tests for success, evaluation failure, and output-contract
  failure,
- include a role-module fixture matching the `70-examples` minimal summarizer.

Candidate dependency:

- JSON-e Rust implementation, after a focused dependency review for maturity,
  maintenance, license, parser behavior, error semantics, and resource-limit
  controls.

If the available Rust JSON-e implementation is not sufficient, Orbiplex should
prefer a small compatibility subset over silently switching to a more powerful
general-purpose scripting language.

## Open Questions

1. Which Rust JSON-e implementation should be adopted after dependency review?
2. What exact projection syntax should operators use for
   `context_projection`?
3. What exact request and response schema should
   `workflow.step.completed.publish` use for story-009 and future workflow
   publishers?
4. Should JSON-e templates live in the host-owned module store, middleware config
   fragments, or both?
5. Which `json_e_flow` dynamic features, if any, are justified by real middleware
   migration cases after the pure profile has landed?

## Non-Goals

- This proposal does not replace `http_local_json`.
- This proposal does not replace `nse_rhai`.
- This proposal does not define a new wire-visible protocol artifact.
- This proposal does not let templates perform direct host capability calls.
- This proposal does not let template authors decide what authority is projected
  into a concrete deployment's JSON-e context.
- This proposal does not standardize a public federation-wide template package
  format.
- This proposal does not make JSON-e the semantic source of truth for protocol
  invariants, cryptography, identity, storage durability, or authority checks.
- This proposal does not replace story-009 Sensorium OS scripts, model wrappers,
  Git scripts, or connector action declarations.

## Consequences

Positive:

- lower authoring threshold for simple middleware,
- less process supervision overhead for pure data adapters,
- better auditability than small arbitrary Python services for mapping-only
  logic,
- reusable execution surface beyond role middleware,
- cleaner least-power ladder across JSON-e, Rhai, HTTP middleware, and Sensorium
  OS actions.

Negative or risky:

- introduces another dependency and authoring surface,
- JSON-e implementation maturity in Rust must be verified,
- insufficient resource limits could make templates unexpectedly expensive,
- too many host helper functions could recreate an implicit scripting language,
- flow semantics could become a second orchestration engine if operators ignore
  the escalation criteria and raise limits instead of moving complex behavior to
  `nse_rhai` or `http_local_json`.

The discipline is therefore simple: JSON-e constructs data; the host owns
meaning and effects.
