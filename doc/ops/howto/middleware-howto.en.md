# Middleware HOWTO

This HOWTO keeps the operational reference, configuration sketches, hook examples, and implementation patterns. The shorter [Middleware FAQ](../faq/middleware-faq.en.md) is the conceptual entry point.

## Authoring a channel JSON module

Use the standard Python adapter from `middleware-modules/lib/channel_module.py`.
The module supplies domain callables; the adapter owns hello/attach, bounded framing,
correlation, observation acknowledgement, cancellation, and the HTTP-shaped operator
bridge. A minimal entrypoint is:

```python
from channel_module import channel_mode_enabled, run_channel_module

if channel_mode_enabled():
    run_channel_module(
        module_report=middleware_init_payload,
        middleware_invoke=middleware_invoke_payload,
        http_dispatch=channel_http_dispatch,
    )
else:
    run_legacy_http_server()
```

The daemon injects `ORBIPLEX_MIDDLEWARE_CHANNEL_URL`, the launch id, and a token-file
path. Do not persist, log, or put those credentials in package configuration. The
module report must pass the standard schema gate. Declare bridgeable routes through
`api/surface`, `operator_surfaces`, or local route registrations; declarations are
descriptive route claims, not authorization.

Register the supervised process under `middleware_channel_services` with its module
and component ids, middleware home, launch/sandbox/restart policy, and bounded
`channel` limits. Use package-relative launch paths. Host-only modules must not start
a listener in channel mode. Mixed modules may keep a product listener, but should
remove host lifecycle and dispatch dependence on it. Keep explicit
`http_local_json` rollback config until the cohort smoke passes; never run both as
owners of the same semantic route.

For a repository-bundled module, make ownership explicit in its factory config:

```json
{
  "example_module": {
    "seed_config": true,
    "factory_executor": "channel_json",
    "product_listener_retained": false,
    "module_id": "example-module"
  }
}
```

A channel-only entry must not contain `listen_host` or `listen_port`. Set
`product_listener_retained` to `true` only when the same module intentionally keeps
a separately bounded product surface. Use `factory_executor = http_local_json` for
an intentional network service that is not a channel migration target. The checked
listener inventory must repeat and validate this ownership decision.
Its `classification` describes the pre-migration surface topology and architectural
intent; use `default_executor` and `product_listener_retained` as the facts about the
current bundled runtime. A mixed entry that still selects `http_local_json` is an
explicit non-migrated compatibility choice. Moving it requires a separately tracked
product/control split or migration rather than reinterpretation of the inventory.
In channel mode, a mixed Python module should use the shared
`retained_product_listener_marker(...)` scope after its product socket binds. The
scope writes the actual endpoint to `<middleware_home>/bind` and removes it during
shutdown. Do not call it for a channel-only module.

Operator-installed packages may continue to declare a complete executor under
`middleware_http_local_services`. Node treats this as
`explicit-http-local-json-legacy`, preserves it without conversion, and exposes the
mode in middleware inventory. Do not put old listener keys in a channel-only bundled
module subtree: config loading fails and asks for an explicit HTTP rollback instead.

Bundled Inquirium adapters use `run_channel_adapter(...)`, which preserves model and
provider semantics while replacing only local host transport. The current opt-in
default cohort is Dator, Arca, Agora Verifier, Snooper, the bundled Inquirium adapters,
Sensorium OS, Sensorium Workbench, and Offer Catalog. Contact Catalog, Attestation,
Messaging, Agora service, Recovery, and Whisper Intake retain intentional or mixed
listeners; Whisper Intake still requires a product/control split before it can become
channel-owned.

For an Inquirium runtime candidate, set its adapter-instance transport to
`channel_json` with `module_id`, the report-declared `invoke_path`, and a bounded
`timeout_ms`. Do not copy provider model names or authorization into the transport
config: model binding and policy are resolved by the host before invocation.

### Channel migration checklist

1. Build one `middleware-module-report.v1` value and validate it through the Node
   schema gate. Declare only routes and capabilities actually served on the channel.
2. Classify the module as channel-only, intentional product HTTP plus channel
   control, or legacy HTTP. Never let both executors own the same semantic route.
3. Map existing host-facing endpoints through `channel_http_dispatch`. Preserve a
   bounded query only when it is domain input; never use query text for routing or
   authorization. Keep product-facing endpoints on their explicit listener.
4. Register bounded launch, restart, timeout, and flow-control values under
   `middleware_channel_services`, then run the cross-language and supervised peer
   tests before enabling the cohort.
5. For a bundled module, set `factory_executor` and
   `product_listener_retained`, update the checked listener inventory, and prove that
   a channel-only config contains no listener allocation.

From the Node repository, the minimum reusable checks are:

```sh
python3 tools/test_middleware_channel_python.py
cargo test -p orbiplex-node-middleware-supervisor supervised_channel_peer_attaches_proves_readiness_and_cleans_runtime_files
cargo test -p orbiplex-node-daemon daemon_starts_channel_middleware_and_resolves_transport_neutral_dispatch
```

The behavior-free reference process is
`middleware-modules/channel-conformance-peer/service.py`. A real module should use
the same transport adapter but replace fixture handlers with its domain callables.

## What are middleware types?

Orbiplex middleware is not one web-style interceptor chain. It is a hosted
extension fabric where each module or declarative definition contributes behavior
through explicit contracts, while the Node host owns lifecycle, dispatch,
validation, capability gates, traces, and failure semantics.

The main execution and specialization types are:

- in-process Rust middleware,
- pure JSON-e middleware,
- JSON-e Flow middleware,
- command/stdio middleware,
- unmanaged local HTTP JSON middleware,
- supervised HTTP middleware,
- Sensorium connector middleware,
- middleware-hosted Inquirium runtime adapters.

Distribution is a separate axis: the same execution type may be factory-bundled,
installed by the operator, or materialized from a profile/config fragment. See
[Distribution models](#distribution-models).

### In-Process Rust

In-process Rust middleware is compiled into the Node binary or one of its
node-attached crates. It is the least isolated and most privileged shape, so it is
reserved for host-owned behavior that belongs close to the daemon boundary. This
type is useful when the behavior needs tight access to host runtime structures,
deterministic startup, low latency, or a very small trusted implementation surface.
It should not be used merely because it is convenient to write Rust code in the
daemon. If a behavior can be expressed through a declared capability, a JSON-e
template, or a supervised module, that weaker form is usually preferable. The
contract should still look like middleware: explicit input, explicit output,
traceable decision, and host-owned validation.

#### Registration shape

- Rust crate or module compiled into the Node workspace.
- Route, hook, or capability registration owned by daemon code.
- Tests in the Rust crate that owns the behavior.

#### Use cases

- Host-owned dispatch bridges that must not depend on external processes.
- Small policy gates tightly coupled to daemon runtime state.
- Low-level adapters where process supervision would add no useful boundary.

#### Examples

```rust
pub fn register_builtin_middleware(registry: &mut HostRegistry) {
    registry.register("example.builtin", |input| {
        MiddlewareDecision::continue_with(input)
    });
}
```

### Pure JSON-e

Pure `json_e` middleware is a declarative data transformer. A concrete registered
JSON-e definition is treated as a separate operational middleware component, even
though the daemon evaluates it through a shared executor. It receives an
operator-projected JSON context, renders a JSON value, and the host validates that
value against an expected output contract. It has no ambient authority: it cannot
open files, call the network, mutate storage, invoke host capabilities, or inspect
data not projected into its context. This type is the right default for matching,
field selection, small rewrites, normalization, route decisions, and
pointer-sized response construction. If the template starts needing effects,
retry policy, long-lived state, or broad branching, move to JSON-e Flow or a
supervised module.

#### Registration shape

- A JSON config entry declaring middleware identity, template, limits, context
  projection, helper profile, and output contract.
- Optional package-shipped config fragment under `middleware-packages/<id>/config/`.
- Host-generated trace records with template id, digest, input/output summary, and
  validation result.

#### Use cases

- Normalize an incoming payload before another component sees it.
- Build a `middleware-decision.v1` from a small projected context.
- Render a simple `service-dispatch-response` without a process.
- Select a route or annotate a request using explicit data.

#### Examples

```json
{
  "schema": "middleware-json-e.v1",
  "id": "example.normalizer",
  "profile_version": "orbiplex.json_e.v1",
  "limits": { "timeout_ms": 100 },
  "context_projection": {
    "title": "$.request.title"
  },
  "template": {
    "decision": "allow",
    "payload": { "title": "${title}" }
  },
  "output_contract": "middleware-decision.v1"
}
```

### JSON-e Flow

`json_e_flow` middleware is a host-owned flow built around JSON-e-rendered step
inputs. Each flow definition is operationally a separate thin middleware
component with its own identity, bindings, limits, allowed calls, trace records,
raw-signal declaration, and operator status. The shared engine executes the flow,
but the flow definition owns the middleware boundary. JSON-e renders values; the
host executes declared steps such as `render`, `validate`, `call`, `extract`,
`respond`, and `fail`. This keeps effects outside the template while still
allowing the flow to call explicitly allowlisted host capabilities. Use it for
small bounded adapters that need one or a few controlled effects. If the flow
becomes orchestration with dynamic step generation, broad scratch state, or
complex domain policy, use supervised HTTP middleware instead.

#### Registration shape

- A `middleware_json_e_flow_services` daemon config entry.
- Flow templates, step definitions, limits, allowed calls, and context projection.
- Optional package config fragments and operator UI metadata.
- Step traces and digests under daemon-owned trace surfaces.

#### Use cases

- Adapt a Dator role request into a Sensorium directive.
- Call `memarium.write` after rendering a bounded fact.
- Publish a workflow-step completion record after a successful capability call.
- Provide low-code middleware for operators who should not need OS-level scripting.

#### Examples

```json
{
  "id": "example.role.summary",
  "module_id": "example.json-e-flow.roles",
  "profile_version": "orbiplex.json_e_flow.v1",
  "limits": { "timeout_ms": 500, "max_steps": 8 },
  "bindings": {
    "role_capability_id": "role/example.summary.execute"
  },
  "allowed_calls": [
    { "capability": "memarium.write", "operation": "write" }
  ],
  "steps": [
    {
      "id": "response",
      "kind": "respond",
      "template": {
        "status": "ok",
        "result": { "summary": "${request.input.text}" }
      }
    }
  ]
}
```

### Command/Stdio

Command/stdio middleware runs a bounded command as a one-shot process. It is more
powerful than JSON-e because it can execute program code, but it is still bounded
by timeout, input, output, and host policy. This type is useful for small tools
that are naturally command-line shaped and do not need to stay alive between
requests. It should not be used for long-running services, queueing, streaming,
or complex local state. The host should treat stdout, stderr, exit code, timeout,
and output size as part of the contract. Operators should avoid handing it broad
filesystem or network access unless the use case explicitly requires it.

#### Registration shape

- Command path and argv configuration.
- Timeout and output-size limits.
- Optional package-provided executable or script.
- Invocation trace containing command identity, exit status, and bounded output
  summaries.

#### Use cases

- Call a deterministic local converter.
- Run a small checker over a bounded JSON payload.
- Wrap a mature CLI tool without supervising a daemon.

#### Examples

```json
{
  "executor": "command_stdio",
  "module_id": "example.slugify",
  "command": ["./bin/slugify"],
  "limits": {
    "timeout_ms": 1000,
    "stdout_max_bytes": 8192,
    "stderr_max_bytes": 4096
  }
}
```

### Unmanaged Local HTTP JSON

Unmanaged local HTTP JSON middleware uses an already-running local service. The
Node host knows how to call the endpoint, but it does not own the service
lifecycle. This keeps the adapter thin and useful for development, integration
with operator-managed local services, or cases where another supervisor already
owns the process. It is weaker than supervised HTTP as an operational contract
because readiness, restart policy, logs, and shutdown are outside Node control.
The daemon should still enforce request shape, timeout, response-size limit,
module auth, and host capability boundaries. Use this type when the service truly
belongs outside the Node lifecycle.

#### Registration shape

- Endpoint URL, method, headers, timeout, and response-size configuration.
- No daemon-owned process definition.
- Optional local auth token or loopback binding policy.

#### Use cases

- Connect to a developer-run local service during prototyping.
- Bridge a local service managed by systemd, launchd, Docker, or another supervisor.
- Integrate a tool that has its own lifecycle and health model.

#### Examples

```json
{
  "executor": "local_http_json",
  "module_id": "example.external-service",
  "endpoint": "http://127.0.0.1:49110/v1/invoke",
  "method": "POST",
  "limits": {
    "timeout_ms": 2000,
    "response_max_bytes": 65536
  }
}
```

### Supervised HTTP

Supervised HTTP middleware is a long-lived local HTTP JSON service started,
observed, and stopped by the Node host. It is the normal shape for powerful
middleware that needs its own runtime, state, queues, domain logic, HTML operator
surface, or interaction with adjacent systems. The module communicates with the
daemon through explicit HTTP/JSON contracts and receives a module auth token
rather than ambient daemon privilege. During startup it should expose health and
init/report endpoints so the daemon can discover routes, host capability handlers,
operator surfaces, and readiness. This type is appropriate for Python, Rust, or
other process-backed modules whose behavior is too rich for JSON-e Flow. It is
heavier than declarative middleware, so use it only when the extra process
boundary and lifecycle are buying clarity or capability.

#### Registration shape

- Service code shipped as a bundled module or installed package.
- `GET /healthz`.
- `POST /v1/middleware/init`.
- Module report declaring routes, capabilities, and UI surfaces.
- Runtime files under `<data-dir>/middleware/<module-id>/`.

#### Use cases

- Dator-like offer catalogs and dispatch providers.
- Arca-like workflow orchestration.
- Operator UI surfaces that need live server-rendered HTML.
- Connectors that need queues, caches, retries, or external tool access.

#### Examples

```python
from http.server import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

    def do_POST(self):
        if self.path == "/v1/middleware/init":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"module_id":"example.supervised","status":"ready"}')
```

### How do I make a middleware endpoint visible in OpenAPI / Swagger?

Do not start a separate Swagger server inside the middleware. The Node daemon
owns one descriptive OpenAPI 3.1 projection at `GET /v1/openapi.json`; an
optional Swagger UI reads that daemon projection. Middleware contributes data,
not another documentation runtime.

For supervised HTTP middleware, add an `api/surface` section to the module report
returned by `POST /v1/middleware/init`. The section must conform to
`orbiplex.api-descriptor.v1`.

Minimal module-report fragment:

```json
{
  "schema_version": "v1",
  "module_id": "example.inquirium",
  "module_name": "Example Inquirium Adapter",
  "api/surface": {
    "schema": "orbiplex.api-descriptor.v1",
    "component/id": "example.inquirium",
    "base/path": "/",
    "endpoints": [
      {
        "method": "POST",
        "path": "/v1/inquirium/invoke",
        "summary": "Invoke the adapter through the host-owned Inquirium contract.",
        "tags": ["inquirium", "middleware"],
        "surface": "internal-loopback",
        "path/owner": "middleware-direct",
        "path/exposure": "internal-loopback",
        "loopback/path": "/v1/inquirium/invoke",
        "path/params": [],
        "request": {
          "schema_ref": "urn:orbiplex:schema:inquirium-adapter-invoke:v1"
        },
        "responses": {
          "200": {
            "schema_ref": "urn:orbiplex:schema:inquirium-adapter-response:v1"
          }
        },
        "x-orbiplex-auth": "module-authtok",
        "x-orbiplex-effect": "mutates-state",
        "x-orbiplex-idempotency": "optional",
        "x-orbiplex-authority": "descriptive-only"
      }
    ]
  }
}
```

For Python middleware, prefer one shared route table used by both dispatch and
descriptor generation:

```python
ROUTES = (
    {
        "method": "POST",
        "path": "/v1/inquirium/invoke",
        "handler": handle_inquirium_invoke,
        "summary": "Invoke the adapter through the host-owned Inquirium contract.",
        "tags": ["inquirium", "middleware"],
        "surface": "internal-loopback",
        "path_owner": "middleware-direct",
        "path_exposure": "internal-loopback",
        "request_schema_ref": "urn:orbiplex:schema:inquirium-adapter-invoke:v1",
        "response_schema_ref": "urn:orbiplex:schema:inquirium-adapter-response:v1",
    },
)

def api_surface_descriptor(module_id):
    return {
        "schema": "orbiplex.api-descriptor.v1",
        "component/id": module_id,
        "base/path": "/",
        "endpoints": [
            {
                "method": route["method"],
                "path": route["path"],
                "summary": route["summary"],
                "tags": route["tags"],
                "surface": route["surface"],
                "path/owner": route["path_owner"],
                "path/exposure": route["path_exposure"],
                "loopback/path": route["path"],
                "path/params": [],
                "request": {"schema_ref": route["request_schema_ref"]},
                "responses": {"200": {"schema_ref": route["response_schema_ref"]}},
                "x-orbiplex-auth": "module-authtok",
                "x-orbiplex-effect": "mutates-state",
                "x-orbiplex-idempotency": "optional",
                "x-orbiplex-authority": "descriptive-only",
            }
            for route in ROUTES
        ],
    }
```

Rules of thumb:

- `path` is the host-exposed path that appears in the daemon projection.
- `loopback/path` is the raw middleware-local path; it is required for
  `internal-loopback` exposure.
- Path parameters use canonical OpenAPI-style `{snake_case}` segments, and every
  path parameter must also appear in `path/params`.
- Use `schema_ref` only for schemas committed to the canonical registry. Use a
  small `inline` schema only for temporary compatibility surfaces.
- Never put auth token values, secrets, prompts, sealed payloads, or local
  absolute paths in `api/surface`.
- `x-orbiplex-auth` is a descriptive label such as `module-authtok`, not the
  token itself.
- `x-orbiplex-authority` is always `descriptive-only`; OpenAPI describes shape,
  not the authority or full security policy.
- The default OpenAPI projection includes only `protocol` surface entries.
  Developer/operator inspection may opt in to other surfaces with
  `?include=operator,developer,internal-loopback`.

For externally managed or package-installed HTTP components that do not return a
module report, the daemon may also load validated descriptor sidecars from
`<data-dir>/api-descriptors/`. Prefer the init-report path whenever the component
is supervised by the node.

### Sensorium Connector

A Sensorium connector is a separate middleware module that implements actions
behind the Sensorium organ boundary. `sensorium-core` is the mediator between the
daemon and connector action catalogs; the connector itself, such as
`sensorium-os`, is still middleware. A connector action is not a separate
middleware module: it is an operation declared by the connector and mediated by
Sensorium Core. This shape is appropriate when a module needs controlled contact
with the operating system, local applications, sensors, tools, or other enacted
surfaces. Consumers should depend on Sensorium capability, action-class, and
action-catalog contracts, not on a hard-coded connector implementation. A
specialized deployment may clone or replace a connector as a new middleware
module, but that should be visible as a new module identity and action catalog.

For the current hard-MVP `sensorium-os` connector, the available runtime surface
is intentionally narrow: script-backed C1/C2 actions can run through the signed
catalog, while binary C1 and C3-C7 actions are reported as unavailable and fail
closed until their enforcement envelopes exist. The authorized catalog entry is
the executable source of truth; request-local allowlist entries or host-policy
overrides are rejected.

#### Registration shape

- Connector service or package.
- Sensorium action catalog.
- Module report declaring connector capabilities and operator surfaces.
- Optional action scripts, templates, or policy files.

#### Use cases

- OS-level actions such as bounded Git checks, deterministic local scripts, or
  deployment-specific wrappers whose action class and result contract are
  explicit in the catalog.
- Safe mediation between declarative role middleware and powerful local effects.
- Deployment-specific connectors with a restricted action catalog.

#### Examples

```json
{
  "module_id": "sensorium-os",
  "kind": "sensorium-connector",
  "actions": [
    {
      "action_id": "story009.publication.verify",
      "class": "allowlisted-script",
      "input_schema": "sensorium-directive.v1",
      "output_schema": "sensorium-directive-outcome.v1"
    }
  ]
}
```

### Middleware-Hosted Inquirium Runtime Adapter

An Inquirium runtime adapter may be middleware in the execution and hosting
sense, but semantically it remains an Inquirium runtime adapter. This distinction
is intentional: the execution type answers "how does this component run?", while
the Inquirium adapter role answers "which execution translation may this
component perform?". Such an adapter may run through `command_stdio`, unmanaged
`local_http_json`, supervised `http_local_json`, an in-process handler, or a later
compatible executor, but that does not give it general middleware authority over
routes, hooks, workflows, or model policy.

Inquirium Core remains the owner of operation semantics such as `generate`,
`embed`, `classify`, `rerank`, `image.generate`, or `train.adapt`.
`model-runtime` owns the runtime catalog, lifecycle, health, supervision, and
transport. The adapter translates request/result data and provider protocol
details, while the model worker executes computation without Orbiplex authority.
If the adapter needs access to large local data, it should receive explicit
leases and artifact handles, not ambient filesystem, network, or host capability
access.

The same adapter does not imply one model. The preferred split is: adapter
implementation for the interface, adapter instance for lifecycle/trust-boundary
configuration, and one `runtime/ref` for each routable model configuration. This
lets one adapter instance keep a shared HTTP pool, queue, process supervisor, or
client cache, while the host still sees each model as a separate runtime
candidate with its own policy, health, conformance, and trace.

This mirrors a common agent-orchestrator layering pattern: provider mechanics,
model identity, execution backend, and interaction channel are separate concerns.
For middleware classification, only the execution backend may be middleware-hosted.
Provider mechanics remain adapter concerns, model identity remains a model-binding
concern, and channel or workflow orchestration remains outside the adapter role.

#### Registration shape

- Inquirium adapter manifest with `adapter/ref`, protocol family, operations,
  modalities, limits, trace/retention policy, and conformance report.
- Optional middleware executor configuration such as `command_stdio`,
  `local_http_json`, or `http_local_json`.
- Health/status and init/report when the adapter is attachable or supervised.
- Explicit leases, egress, sandbox, and `effects/allowed` for effectful
  operations.

#### Use cases

- Bridge to a local model server managed by the operator or by the Node host.
- One-shot wrapper around a CLI tool that performs bounded inference.
- Remote API adapter requiring egress policy, secrets, limits, and refusal
  mapping.
- Post-training, batch embedding, or audio/vision processing through a worker
  that reads and writes only through scoped leases.

#### Examples

```json
{
  "module_id": "inquirium.local-model-runtime",
  "kind": "inquirium-runtime-adapter",
  "executor": "http_local_json",
  "adapter_manifest": {
    "adapter/ref": "adapter:local-model-runtime",
    "hosting/kind": "middleware-hosted",
    "operations": ["generate", "embed", "batch.embed"],
    "modalities/input": ["text"],
    "modalities/output": ["text", "embedding"],
    "effects/allowed": [
      { "kind": "fs/read", "lease/ref": "input-lease" },
      { "kind": "fs/write", "lease/ref": "artifact-output-lease" }
    ]
  }
}
```

## What is Role Middleware?

Role middleware is middleware that acts as a provider or dispatcher for a named
role/service contract. It is not an execution type like supervised HTTP,
JSON-e Flow, command/stdio, or in-process Rust. It is a functional role: the
component receives a bounded request such as "perform this editorial-review role"
or "execute this offer-catalog provider role", selects the appropriate behavior,
and returns a `service-dispatch-response`-style result under the declared
contract. The same role middleware pattern can be implemented with different
execution types depending on how much authority, state, and runtime complexity
the role needs.

The useful distinction is:

- execution type answers "how does this middleware run?",
- role middleware answers "what dispatch responsibility does this middleware
  perform?".

A role middleware should not become a generic script runner or a hidden
application server. It should advertise the role capability it provides, validate
the incoming role request, produce a traceable response, and use host
capabilities only through explicit allowlists. In Story-009, the role providers
for draft composition, illustration preparation, editorial review, publish, and
verification are examples of this shape. Some are better as JSON-e Flow because
they are bounded adapters; others may become supervised HTTP modules if they need
state, queues, richer policy, or an operator UI.

### Role middleware with supervised HTTP

A supervised HTTP role middleware is useful when the provider needs a real
process: durable local state, queueing, non-trivial domain logic, an HTML
operator surface, or integration with adjacent tools. The daemon starts and
monitors the process, sends the module init/report handshake, and dispatches role
requests to the module through an explicit HTTP/JSON contract. The module should
branch on the role capability or service type in the request, not on hidden
daemon state.

```json
{
  "module_id": "story009-roles-http",
  "executor": "http_local_json",
  "capabilities": [
    {
      "capability_id": "role/story009.editorial-review.execute",
      "kind": "service-dispatch-provider"
    }
  ],
  "invoke_path": "/v1/roles/dispatch"
}
```

```python
def dispatch_role(request):
    role = request["role_capability_id"]

    if role == "role/story009.editorial-review.execute":
        return {
            "schema_version": "v1",
            "capability_id": "service_dispatch_execute",
            "status": "completed",
            "dispatch/id": request["dispatch/id"],
            "answer/content": {"decision": "accepted"},
            "answer/format": "json",
            "confidence/signal": 0.82,
            "human-linked-participation": False
        }

    return {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "rejected-invalid-request",
        "dispatch/id": request.get("dispatch/id"),
        "reason": "unsupported role capability"
    }
```

This shape is appropriate for Dator-like providers, Arca-adjacent role services,
or operator-installed modules whose behavior is too rich for a declarative flow.

### Role middleware with JSON-e Flow

JSON-e Flow role middleware is the preferred low-code shape when the role is a
bounded adapter: render a request, optionally call an allowlisted host
capability, extract a result, and respond. Each flow definition is operationally
a separate role middleware component even though it runs through the shared
JSON-e Flow executor. This lets an operator install or inspect a role provider as
data without granting it OS access.

```json
{
  "id": "story009.editorial.review",
  "module_id": "story009.editorial.review",
  "executor": "json_e_flow",
  "bindings": {
    "role_capability_id": "role/story009.editorial-review.execute"
  },
  "limits": { "timeout_ms": 500, "max_steps": 6 },
  "steps": [
    {
      "id": "respond",
      "kind": "respond",
      "template": {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "completed",
        "dispatch/id": "${request.dispatch/id}",
        "completed-at": "${now}",
        "answer/content": {
          "decision": "accepted",
          "notes": "Rendered by a bounded JSON-e Flow role provider."
        },
        "answer/format": "json",
        "confidence/signal": 1.0,
        "human-linked-participation": false
      }
    }
  ]
}
```

Use JSON-e Flow role middleware for role adapters that can be described as data
and whose effects are narrow enough to be declared as host-owned steps. Move to
supervised HTTP when the role starts needing a richer runtime boundary.

## Where can middleware attach to the node data path?

Middleware can attach to different places in the node's data path. The hook says
where a message becomes visible to a component and what kind of decision the
component may return. This is separate from execution type: a supervised HTTP
module, JSON-e Flow definition, or in-process Rust handler may all participate in
dispatch, but each does so through a host-owned surface with explicit validation,
timeouts, capability gates, and trace records. The host remains responsible for
routing and authority; middleware contributes a bounded behavior at a declared
attachment point. A module should attach at the narrowest hook that matches its
real need, rather than subscribing to a broad phase because it is convenient.

The generic middleware decision vocabulary is hook-specific, but the current
names are:

- `allow` - pass the input to the next host stage or handler.
- `annotate` - keep the input moving while adding host-visible metadata where
  the hook has a concrete annotation carrier.
- `rewrite` - replace or patch the host-visible payload before continuing.
- `route` - choose an explicit target or next route where the hook supports it;
  the current standard chain allowlists do not admit `route` as a standalone
  decision, and local routing uses route directives carried alongside allowed
  local decisions.
- `return` - short-circuit with a response or final payload.
- `drop` - stop processing without a successful response.
- `defer` - decline to decide now and let another host policy stage continue.
- `reject` - refuse the request with an explicit error/status.

Not every hook may emit every decision. Some attachment points, such as host
capability calls or operator UI routes, use their own response contracts rather
than `middleware-decision.v1`.

### Pre-Input Phase Hook

`pre-input` is the first host-owned pass before a request enters a concrete
dispatch family. It is meant for cross-cutting treatment of an incoming trigger:
normalization, redaction, raw-signal preservation, early classification, or local
policy checks that must happen before the daemon decides whether the input is a
local HTTP request, peer message, broadcast event, or workflow task. It should be
used sparingly because broad hooks increase cognitive load and can become hidden
coupling. A `pre-input` participant should normally annotate or prepare the trace
context rather than take over domain-specific handling.

#### Use cases

- Preserve `raw_signal` for execution paths that require it.
- Initialize `causality_id` and `component_path[]`.
- Apply local redaction or classification before narrower dispatch begins.

#### Example attachment

```json
{
  "module_id": "example.pre-input-policy",
  "input_chains": ["pre-input"],
  "decision_contract": "middleware-decision.v1"
}
```

#### Possible decisions

- `allow` - continue into the normal dispatch family selection.
- `annotate` - add local metadata and continue where the host can represent the
  annotation. In the current peer-message `pre-input` path, annotation is
  accepted by the vocabulary but not yet represented on `PeerMessageEnvelope`,
  so it is effectively pass-through.
- `rewrite` - normalize or redact the trigger before narrower dispatch begins.
- `drop` - stop processing before any concrete dispatch family sees the input.

#### Implementation sketch

Configuration declares the broad hook; implementation should stay small:

```json
{
  "module_id": "example.pre-input-policy",
  "input_chains": ["pre-input"],
  "executor": "json_e",
  "output_contract": "middleware-decision.v1"
}
```

```json
{
  "decision": "annotate",
  "annotations": { "classification": "operator-local" },
  "diagnostics": {}
}
```

#### Known uses

- Raw-signal and component-path dispatch context in the daemon.
- No current factory middleware should rely on this as a broad business-logic
  interception point.

#### Compatible middleware types

- In-process Rust middleware.
- Pure JSON-e middleware, for pure normalization or decision rendering.
- JSON-e Flow middleware, when the phase needs bounded host-owned effects.
- Command/stdio middleware, technically possible but usually too heavy for this
  broad phase.
- Unmanaged local HTTP JSON middleware, for operator-owned local policy services.
- Supervised HTTP middleware, for powerful local policy services that justify
  the broad hook.
- Sensorium connector middleware only indirectly, when it is also a supervised
  service and has an explicit reason to participate; broad pre-input attachment
  should not be the default for connectors.

### Claimed Local Routes and Inbound Local Hooks

Local dispatch covers HTTP requests received by the local daemon. A module may
claim an exclusive local route, commonly under `/v1/enact/*`, or participate in a
more generic `inbound-local` chain. Claimed routes are appropriate when the
module owns a concrete local API surface. Generic inbound-local hooks are better
for small request annotations, local policy decisions, or routing helpers. If a
claimed route exists but its owning module is not ready, the host returns a local
unavailable response rather than silently routing to another component.

#### Use cases

- Expose module-owned local APIs.
- Add operator-local request handling without changing daemon code.
- Adapt local application calls into middleware decisions.

#### Example attachment

```json
{
  "module_id": "example.local-route",
  "claimed_routes": [
    { "method": "POST", "path": "/v1/enact/example.local-route/run" }
  ]
}
```

#### Possible decisions

- `allow` - let the local request continue to the next local handler.
- `rewrite` - patch or replace the local request payload before continuing.
- `return` - short-circuit with a local HTTP response.
- `reject` - refuse the request with an explicit local error/status.

#### Implementation sketch

Configuration claims the route; the live module then handles the request through
its normal local HTTP service:

```json
{
  "module_id": "example.local-route",
  "executor": "http_local_json",
  "claimed_routes": [
    { "method": "POST", "path": "/v1/enact/example.local-route/run" }
  ]
}
```

```python
def handle_run(request):
    return {
        "status": "ok",
        "result": {"echo": request["json"]}
    }
```

#### Known uses

- Supervised HTTP middleware that publishes module routes through
  `middleware-module-report`.
- Operator-installed packages that contribute UI or local route metadata.

#### Compatible middleware types

- In-process Rust middleware.
- Pure JSON-e middleware, for generic `inbound-local` transformations; it should
  not own rich HTTP route behavior by itself.
- JSON-e Flow middleware, for local request adapters with declared steps.
- Command/stdio middleware, for bounded one-shot local request handlers.
- Unmanaged local HTTP JSON middleware, when another supervisor owns the local
  service.
- Supervised HTTP middleware, the normal shape for claimed module routes.
- Sensorium connector middleware, when the connector exposes local module routes
  through its supervised service or package metadata.

### Role and Service Dispatch

Role and service dispatch is the hook family used when a workflow asks for a
capability-like service rather than a raw process call. The host routes a
`service-dispatch-request` or role request to a provider, validates the response,
and records trace material. This is the natural surface for Dator and Arca-style
workflows, because the request is already phrased as "perform this role/service
under this contract" rather than "handle this HTTP path." Declarative adapters
such as JSON-e Flow fit well here when they only need to transform a bounded role
request and invoke allowlisted host capabilities.

#### Use cases

- Route Arca workflow steps to Dator-discovered providers.
- Adapt role requests into Sensorium directives.
- Return bounded `service-dispatch-response` values with traceable decision
  semantics.

#### Example attachment

```json
{
  "module_id": "story009.editorial.review",
  "role_capability_id": "role/story009.editorial-review.execute",
  "executor": "json_e_flow"
}
```

#### Possible decisions

- `completed` - provider completed the request and returns answer content,
  answer format, confidence signal, and completion metadata.
- `rejected-invalid-request` - provider refused the request because the request
  did not satisfy its contract.
- `failed` - provider attempted or admitted the work but could not complete it.

#### Implementation sketch

Configuration binds a provider identity to a role capability; implementation can
be a JSON-e Flow or a supervised service:

```json
{
  "module_id": "story009.editorial.review",
  "executor": "json_e_flow",
  "bindings": {
    "role_capability_id": "role/story009.editorial-review.execute"
  },
  "steps": [
    {
      "id": "response",
      "kind": "respond",
      "template": {
        "schema_version": "v1",
        "capability_id": "service_dispatch_execute",
        "status": "completed",
        "dispatch/id": "dispatch:story009.editorial.review:example",
        "completed-at": "${now}",
        "answer/content": { "decision": "accepted" },
        "answer/format": "json",
        "confidence/signal": 1.0,
        "human-linked-participation": false
      }
    }
  ]
}
```

#### Known uses

- `arca` - workflow-side orchestration and role/service request emission.
- `dator` - offer catalog and provider-side service dispatch.
- Story-009 JSON-e Flow role definitions - bounded adapters between role
  requests and host capability calls.

#### Compatible middleware types

- In-process Rust middleware, for host-owned role providers.
- Pure JSON-e middleware, for response-only role adapters that need no effects.
- JSON-e Flow middleware, the preferred declarative shape for bounded role
  adapters with allowlisted host calls.
- Command/stdio middleware, for one-shot role providers with strict limits.
- Unmanaged local HTTP JSON middleware, for externally supervised providers.
- Supervised HTTP middleware, the normal shape for rich providers such as Dator
  and Arca-adjacent services.
- Sensorium connector middleware usually participates behind Sensorium Core
  rather than as a direct role provider.

### Host Capability Bridge

The host capability bridge is used when middleware needs a bounded operation
owned by the daemon or an organ, such as writing a Memarium fact, emitting a
notification, dispatching a peer message, issuing a capability passport, or
invoking a Sensorium action. The module does not receive ambient daemon
authority; it receives only the host calls declared and granted through local
config, module auth, capability passports, and dispatch gates. This hook is the
right place to cross from middleware behavior into host-owned effects. It should
not be used as a generic escape hatch for arbitrary internal APIs.

#### Use cases

- Write a bounded fact to Memarium from a JSON-e Flow step.
- Emit an operator notification after a module decision.
- Invoke Sensorium Core to mediate a Sensorium connector action.
- Dispatch peer messages through host-owned network surfaces.

#### Example attachment

```json
{
  "module_id": "example.fact-writer",
  "allowed_calls": [
    { "capability": "memarium.write", "operation": "write" }
  ]
}
```

#### Possible decisions

The host capability bridge does not use `middleware-decision.v1` directly.
Concrete capabilities have their own response contracts, but the implemented
outcome classes are:

- `success` - the host capability returns HTTP `200`, `201`, or `202` and no
  semantic failure status is detected in the response body.
- `host_capability_forbidden` - the caller/module is not allowed to invoke that
  host capability.
- `host_capability_unavailable` - no registered handler exists or the handler
  module is not ready.
- `host_capability_dispatch_error` - the host could not build or authorize the
  local dispatch request.
- `host_capability_dispatch_failed` - the handler call failed or its response
  could not be read.
- semantic failure statuses such as `failed`, `error`, `timed_out`, `timeout`,
  `rejected`, `rejected-invalid-request`, `not_authorized`,
  `revocation_stale`, `passport_expired`, `passport_invalid`,
  `passport_revoked`, and `policy_denied` - treated by JSON-e Flow as failed
  host-capability execution.

#### Implementation sketch

Configuration declares the allowed call; implementation invokes the capability
through a host-owned step or module endpoint, not by importing daemon internals:

```json
{
  "module_id": "example.fact-writer",
  "executor": "json_e_flow",
  "allowed_calls": [
    { "capability": "memarium.write", "operation": "write" }
  ],
  "steps": [
    {
      "id": "write-fact",
      "kind": "call",
      "capability": "memarium.write",
      "operation": "write"
    }
  ]
}
```

#### Known uses

- Story-009 JSON-e Flow role definitions - `memarium.write` and workflow fact
  publication.
- `sensorium-core` and `sensorium-os` - Sensorium action mediation.
- `arca` and `dator` - workflow, dispatch, and publication-related host calls.

#### Compatible middleware types

- In-process Rust middleware.
- JSON-e Flow middleware, because effects are declared as host-executed steps.
- Command/stdio middleware, only through a host wrapper that grants explicit
  capability calls; the command itself should not receive ambient authority.
- Unmanaged local HTTP JSON middleware, when bound with module auth and explicit
  allowed calls.
- Supervised HTTP middleware, the standard process-backed shape for host
  capability consumers.
- Sensorium connector middleware, through Sensorium-owned capability/action
  mediation.
- Pure JSON-e middleware is not compatible with direct host capability calls; use
  JSON-e Flow when the template needs effects.

### Peer Message Dispatch

Peer message dispatch is the hook family for messages that arrive after
network/session decoding. It is narrower than local HTTP routing and carries
peer-oriented contracts such as peer message invocation, session establishment,
artifact exchange, or capability presentation. Built-in protocol handlers should
own protocol truth, but middleware may participate where extension behavior is
explicitly declared. A peer-message hook must be especially careful about
timeouts, replay semantics, input validation, and refusal diagnostics because it
sits on a federated boundary.

#### Use cases

- Handle extension peer messages without changing the core protocol handler.
- Route inter-node artifact channel work to an out-of-process participant.
- Attach offer catalog or capability presentation behavior at the peer boundary.

#### Example attachment

```json
{
  "module_id": "example.peer-handler",
  "input_chains": ["inbound-peer"],
  "message_kinds": ["example.peer-message.v1"]
}
```

#### Possible decisions

- `allow` - pass the peer message to built-in or later peer handlers.
- `rewrite` - normalize the decoded peer message before continuing.
- `return` - produce a peer response and stop further peer dispatch.
- `drop` - stop processing the peer message without a successful response.

#### Implementation sketch

Configuration subscribes to the peer chain and message kind; implementation
returns a bounded decision or peer response through the host contract:

```json
{
  "module_id": "example.peer-handler",
  "executor": "http_local_json",
  "input_chains": ["inbound-peer"],
  "message_kinds": ["example.peer-message.v1"]
}
```

```json
{
  "decision": "return",
  "annotations": {},
  "diagnostics": {},
  "patch_strategy": "json_merge_patch",
  "patch": { "response": { "status": "ok" } }
}
```

#### Known uses

- Built-in peer protocol handlers for capability, schema, ledger, and artifact
  exchange.
- Future out-of-process peer handlers using `http_local_json` or
  `local_http_json` attachment.

#### Compatible middleware types

- In-process Rust middleware, for protocol-adjacent handlers.
- Pure JSON-e middleware, for narrow peer-message normalization or decision
  rendering.
- JSON-e Flow middleware, for bounded peer-message adapters with declared calls.
- Command/stdio middleware, technically possible for bounded handlers but
  usually too costly for federated hot paths.
- Unmanaged local HTTP JSON middleware, for externally supervised peer handlers.
- Supervised HTTP middleware, for out-of-process peer handlers with readiness and
  lifecycle.
- Sensorium connector middleware is not a natural peer-message hook; use a role,
  service, or host capability bridge when peer input should trigger local
  enaction.

### Broadcast Hooks

Broadcast hooks observe or transform broadcast events before they become local
effects or outgoing relay material. They are useful for moderation, annotation,
local policy, and filtering, but they should not become a hidden global order of
business logic. Broadcast handling should preserve the distinction between an
event being seen, locally accepted, forwarded, or stored. If a module needs
durable interpretation, it should usually write an explicit fact through a host
capability rather than mutate the broadcast in place.

#### Use cases

- Annotate or classify broadcast events.
- Apply local moderation policy before forwarding.
- Drop or quarantine broadcast material according to operator policy.

#### Example attachment

```json
{
  "module_id": "example.broadcast-policy",
  "input_chains": ["inbound-broadcast"],
  "decision_contract": "middleware-decision.v1"
}
```

#### Possible decisions

- `allow` - accept the broadcast event into the next host stage.
- `annotate` - add policy metadata and continue.
- `rewrite` - patch the broadcast-visible payload before continuing.
- `drop` - stop local processing or forwarding of this event.
- `defer` - decline to decide and let another policy stage continue.

#### Implementation sketch

Configuration subscribes to the broadcast chain; implementation emits a narrow
policy decision:

```json
{
  "module_id": "example.broadcast-policy",
  "executor": "json_e",
  "input_chains": ["inbound-broadcast"],
  "output_contract": "middleware-decision.v1"
}
```

```json
{
  "decision": "drop",
  "reason": "blocked by local relay policy",
  "annotations": {},
  "diagnostics": { "policy": "example.broadcast-policy" }
}
```

#### Known uses

- No production factory middleware is currently documented as owning a dedicated
  broadcast hook.
- Agora-facing components are the likely future users for relay and broadcast
  policy surfaces.

#### Compatible middleware types

- In-process Rust middleware.
- Pure JSON-e middleware, for annotation, classification, or policy decisions.
- JSON-e Flow middleware, when broadcast handling needs bounded host-owned
  effects.
- Command/stdio middleware, for slow-path or operator-local broadcast checks.
- Unmanaged local HTTP JSON middleware, for externally supervised policy
  services.
- Supervised HTTP middleware, for richer moderation, relay, or policy services.
- Sensorium connector middleware is usually not appropriate unless a broadcast
  event intentionally becomes a Sensorium-mediated local action.

### Pre-Send and Egress Hooks

`pre-send` is the last mutation or decision point before a response, peer
message, or broadcast event leaves the current host-owned dispatch path. It is
not a place to rediscover business meaning; it is a final boundary for response
shaping, metadata, local redaction, or deny/drop decisions that must happen
after the main handler has produced an output. Because it sits late in the path,
it should be deterministic and small. Expensive work belongs in role/service
dispatch, host capability calls, or a richer supervised module before egress.

#### Use cases

- Add final local metadata before egress.
- Redact or normalize outgoing payloads at the boundary.
- Drop an outgoing message that violates local policy.

#### Example attachment

```json
{
  "module_id": "example.pre-send-policy",
  "input_chains": ["pre-send"],
  "decision_contract": "middleware-decision.v1"
}
```

#### Possible decisions

- `allow` - send the current output unchanged.
- `rewrite` - patch or replace the outgoing payload before sending.
- `drop` - stop the output from leaving this dispatch path.

#### Implementation sketch

Configuration subscribes to the egress chain; implementation returns a small
boundary decision:

```json
{
  "module_id": "example.pre-send-policy",
  "executor": "json_e",
  "input_chains": ["pre-send"],
  "output_contract": "middleware-decision.v1"
}
```

```json
{
  "decision": "rewrite",
  "patch_strategy": "json_merge_patch",
  "patch": { "headers": { "x-orbiplex-local-policy": "applied" } },
  "annotations": {},
  "diagnostics": {}
}
```

#### Known uses

- Response shaping, metadata, deny/drop policy, and final local redaction.
- No production factory middleware is currently documented as owning a dedicated
  `pre-send` hook.

#### Compatible middleware types

- In-process Rust middleware.
- Pure JSON-e middleware, for final pure transformations.
- JSON-e Flow middleware, only when egress requires bounded host-owned effects.
- Command/stdio middleware, technically possible but usually too costly for this
  late boundary.
- Unmanaged local HTTP JSON middleware, for operator-owned egress policy
  services.
- Supervised HTTP middleware, for richer egress policy surfaces when latency is
  acceptable.
- Sensorium connector middleware is not a natural egress hook; use Sensorium
  action mediation earlier in the path.

### Operator UI Surfaces

Operator UI surfaces are not data-plane hooks, but they are an important
attachment point for middleware. A module or package may contribute UI templates,
static assets, route metadata, and operator workflows so the built-in Node UI
does not need hard-coded knowledge of every future module. The daemon still owns
route mounting, session context, authorization, and safe rendering boundaries.
This is the right surface for module-local dashboards, action review screens,
package configuration, and human-readable trace explorers.

#### Use cases

- Expose module run history and status pages.
- Add operator configuration pages for installed packages.
- Render module-specific action review or readiness workflows.

#### Example attachment

```json
{
  "module_id": "example.operator-ui",
  "operator_surfaces": [
    { "path": "/middleware/example/", "template": "ui/index.html" }
  ]
}
```

#### Possible decisions

Operator UI surfaces do not use `middleware-decision.v1`; their code-level
choices are rendering ownership modes and HTTP/UI outcomes:

- `host-mediated` - Node UI owns the rendered HTML using package/module metadata.
- `server-html` - a live middleware module owns the HTML and Node UI proxies the
  same-origin surface.
- `unavailable` - Node UI renders an unavailable/error page when the package,
  surface, or backing module cannot be resolved.
- `redirect-rewrite` - same-origin redirects from proxied server HTML may be
  rewritten under the mounted surface; external redirects are rejected.

#### Implementation sketch

Configuration declares the surface; implementation may be static package UI or a
live supervised route:

```json
{
  "module_id": "example.operator-ui",
  "operator_surfaces": [
    {
      "path": "/middleware/example/",
      "template": "ui/index.html",
      "requires_operator_session": true
    }
  ]
}
```

```html
<section>
  <h1>Example middleware</h1>
  <p>Status is rendered by the host from module report data.</p>
</section>
```

#### Known uses

- `arca` - workflow run UI.
- JSON-e Flow trace surfaces.
- Operator-installed package examples with `ui/` and `ui-op/` material.

#### Compatible middleware types

- In-process Rust middleware, when the UI is host-owned.
- Pure JSON-e middleware, through metadata and trace/config views rather than a
  live UI server.
- JSON-e Flow middleware, through trace, status, and config surfaces.
- Command/stdio middleware, through host-rendered status/config surfaces.
- Unmanaged local HTTP JSON middleware, if the operator explicitly accepts an
  externally managed UI endpoint.
- Supervised HTTP middleware, the normal shape for live module UI.
- Sensorium connector middleware, through connector action catalogs and
  connector-owned operator surfaces.
- Operator-installed packages and factory-bundled modules may both contribute UI
  assets; this is a distribution-model concern layered on top of execution type.

### Observers and Audit Hooks

Observers and audit hooks are visibility surfaces. They are meant to record what
happened, not to become another hidden decision layer. New consumers should
prefer phase observers and post-chain observers for visibility; `audit` remains
the post-dispatch compatibility surface. Trace records should preserve
causality, component path, selected summaries, and configured raw-signal or
component I/O details without leaking secrets or unnecessary payloads. If an
observer needs to influence behavior, it should be modeled as a real dispatch
hook instead of an audit side effect.

#### Use cases

- Record component I/O trace summaries.
- Emit audit records for authorization or dispatch decisions.
- Provide operator diagnostics without changing runtime behavior.

#### Example attachment

```json
{
  "module_id": "example.trace-observer",
  "observes": ["pre-input", "inbound-local", "post-chain"],
  "mode": "observer"
}
```

#### Possible decisions

- `allow` - the compatibility response expected by legacy audit invoke handlers.
  The observation must not alter the functional dispatch outcome, and observer
  requests using `peer-message-observe.v1` do not use `middleware-decision.v1`.

Observer invocation failures are host policy, not middleware decisions. The
current peer audit path invokes observers asynchronously and logs failures
without changing the caller-visible outcome.

#### Implementation sketch

Configuration declares observation only; implementation records and returns no
business decision:

```json
{
  "module_id": "example.trace-observer",
  "observes": ["pre-input", "inbound-local", "post-chain"],
  "mode": "observer"
}
```

```rust
fn record(event: TraceEvent) {
    tracing::info!(
        event = "middleware_trace_observed",
        component_path = ?event.component_path,
        decision = ?event.decision
    );
}
```

#### Known uses

- Daemon trace surfaces for middleware dispatch.
- Authorization and host-capability audit sinks.
- JSON-e Flow step trace and digest views.

#### Compatible middleware types

- In-process Rust middleware, for host-owned audit sinks and trace collectors.
- Pure JSON-e middleware, for pure projection of trace summaries.
- JSON-e Flow middleware, for bounded observer workflows.
- Command/stdio middleware, for bounded export or diagnostic jobs.
- Unmanaged local HTTP JSON middleware, for operator-managed observability
  services.
- Supervised HTTP middleware, for richer audit/trace consumers with their own
  lifecycle.
- Sensorium connector middleware should normally emit observations through
  Sensorium and host audit surfaces, not attach as a generic observer unless that
  role is explicitly declared.

## How does one HTTP middleware distinguish calls from multiple hooks?

A supervised HTTP middleware may attach to more than one hook. For example, one
module may handle an input chain and also observe the audit chain. The host may
call the same HTTP endpoint for both hooks if the module report or local config
uses the same `invoke_url` for both registrations. That is legal, but the route
path is not the semantic discriminator. The canonical discriminator is the
request envelope, especially `chain_kind`.

For peer-message handler paths, the host sends a `PeerMessageInvokeRequest`.
The legacy peer-message `audit` surface also uses that invoke shape, but its
result is observational: returned decisions and invocation failures do not alter
the caller-visible dispatch outcome. The same endpoint can receive both
`inbound-peer` and legacy `audit` invocations:

```json
{
  "schema_version": "v1",
  "envelope_kind": "peer-message",
  "msg": "example.message.v1",
  "chain_kind": "audit",
  "correlation_id": "corr:example",
  "remote_node_id": "node:did:key:z6Mk...",
  "payload": {
    "input_payload": { "example": true },
    "response": null,
    "elapsed_ms": 7
  }
}
```

For local HTTP dispatch, the same rule applies through the local input invoke
envelope: the module should branch on `chain_kind`, not on an implicit assumption
about the route that was called.

For phase observers and post-chain observers, the host sends
`peer-message-observe.v1` with `envelope_kind = "peer-message-observe"` and
`observation_kind = "phase"` or `"post-chain"`. Those observer requests are
metadata/trace surfaces, not decision points.

```python
def handle_hook(request):
    chain = request["chain_kind"]

    if chain == "inbound-local":
        return handle_inbound_local(request)

    if chain == "audit":
        record_audit(request)
        return {
            "decision": "allow",
            "annotations": {},
            "diagnostics": {}
        }

    return {
        "decision": "reject",
        "reason": f"unsupported chain_kind {chain}",
        "annotations": {},
        "diagnostics": {}
    }
```

Using one endpoint is reasonable for a small module with one internal dispatcher.
For larger modules, separate HTTP paths are usually clearer operationally:

```json
{
  "module_id": "example.multi-hook",
  "hooks": [
    {
      "chain_kind": "inbound-peer",
      "invoke_url": "http://127.0.0.1:49120/hooks/inbound-peer"
    },
    {
      "chain_kind": "audit",
      "invoke_url": "http://127.0.0.1:49120/hooks/audit"
    }
  ]
}
```

Even then, `chain_kind` remains part of the contract. The path is a diagnostic
and routing convenience; the envelope is the source of truth.

## Distribution models

Execution type says how middleware runs. Distribution model says how the code,
definition, config, or package arrives at a node and how the operator accepts it.
These axes intentionally cross: a supervised HTTP module can be bundled or
operator-installed, and a JSON-e Flow definition can be shipped as an acceptance
profile without becoming a standalone process module.

### Factory-Bundled Middleware

Bundled middleware is distributed with the Node source or binary distribution. It
may still be supervised HTTP, JSON-e Flow, in-process Rust, or another executor
type; "bundled" describes distribution and trust posture, not execution
mechanics. Bundled modules are useful when a capability is part of the reference
system but should remain outside the trusted daemon core. They can receive
first-class runbook coverage, tests, default config fragments, and operator UI
integration. Bundling does not remove the need for module reports, host
capability gates, readiness, traces, or least privilege. If a bundled module is
not required by a deployment, the operator should be able to disable it.

#### Delivery path

- Source code or executable shipped in the Node distribution.
- Default config fragments.
- Acceptance profiles or fixtures.
- Tests, runbooks, and operator UI assets when applicable.

#### Factory-shipped middleware

- `sensorium-core` - bundled in-process Sensorium organ boundary.
- `sensorium-os` - bundled Sensorium connector middleware.
- `arca` - bundled workflow/orchestration middleware.
- `dator` - bundled offer catalog and dispatch middleware.
- `recovery-service` - bundled recovery-service middleware.
- `snooper` - bundled observational/debug middleware.
- `whisper-intake` - bundled Whisper intake middleware.
- `agora-service` - bundled Agora-facing service middleware.
- `agora-verifier` - bundled Agora verification helper middleware.
- `agora-demo` - bundled Agora demonstration middleware.

#### Use cases

- Reference Arca, Dator, Sensorium OS, or Seed Directory modules.
- Hard-MVP capabilities that should work out of the box.
- Demonstration modules used by acceptance stories.

#### Examples

```json
{
  "module_id": "example.bundled",
  "executor": "http_local_json",
  "bundle": {
    "kind": "python-module",
    "entrypoint": "middleware-modules/example/service.py"
  },
  "enabled": true
}
```

### Profile-Distributed Definitions

Profile-distributed definitions are middleware definitions shipped as part of an
acceptance profile, runbook fixture, or factory config skeleton rather than as a
standalone module package. This distribution model is useful for declarative
middleware, especially JSON-e Flow, where the operational component is the flow
definition itself. The profile may materialize config fragments into a data
directory during bootstrap, but runtime state still belongs under the normal
daemon-owned runtime directories. Operators should be able to inspect and accept
the materialized definitions before they become active in production-like
profiles. This model should not hide powerful behavior: host capability calls,
limits, raw-signal access, and operator UI routes remain explicit in the
definition.

#### Delivery path

- Acceptance profile, bootstrap skeleton, or runbook fixture.
- Factory config fragments materialized into the node data directory.
- Declarative middleware definitions such as JSON-e Flow service entries.
- Optional generated passports, bindings, or readiness artifacts needed by the
  profile.

#### Factory-shipped middleware

- Story-009 JSON-e Flow role definitions - bundled acceptance-profile flow
  definitions used to adapt role requests into bounded host-capability calls.

#### Use cases

- Ship a complete story or acceptance profile that works without a bespoke
  process module.
- Materialize low-code role adapters as data.
- Keep demonstration and bootstrap middleware reproducible without making each
  definition a separately versioned package.

#### Examples

```json
{
  "profile": "story-009",
  "materializes": [
    "middleware_json_e_flow_services.story009.editorial.review",
    "middleware_json_e_flow_services.story009.sensorium.prepare"
  ]
}
```

### Operator-Installed Package

An operator-installed middleware package is an artifact placed under
`<data-dir>/middleware-packages/<package-id>/`. It can contribute module config,
static UI fragments, operator-surface metadata, scripts, templates, and other
package-owned files. The package tree is treated as an artifact surface: semantic
files should be signed or otherwise approved before the daemon activates the
contributed config. Runtime state does not belong in the package tree; it belongs
under `<data-dir>/middleware/<module-id>/`. This type is useful for local
extensibility without requiring the built-in UI or daemon to know every future
module. The package may install a declarative flow, a supervised service, or UI
surfaces, but the host still owns activation and policy.

#### Delivery path

- `middleware.package.json`.
- `config/*.json` package config fragments.
- `ui/` static host-rendered UI fragments.
- `ui-op/` operator-surface declarations.
- Optional `.signatures/` sidecars.

#### Included examples

- No production package is currently treated as a factory-installed operator
  package. The documentation ships package examples such as
  `middleware-package-ui`, `middleware-python-package-ui`, `role-module-http`,
  `role-module-json-e`, `json-e-flow-role`, and `sensorium-connector`.

#### Use cases

- Install third-party or local operator middleware.
- Add operator UI surfaces without changing Node UI code.
- Ship predefined JSON-e Flow adapters as data.
- Keep package material separate from runtime state.

#### Examples

```text
middleware-packages/example-package/
  middleware.package.json
  config/
    50-example-flow.json
  ui/
    index.html
  ui-op/
    operator-surfaces.json
```

```json
{
  "schema": "middleware.package.v1",
  "package_id": "example-package",
  "modules": [
    { "module_id": "example.flow", "config": "config/50-example-flow.json" }
  ]
}
```
