# Minimal Role Module With JSON-e Flow

This example is the JSON-e-flow counterpart of `role-module-http/`. It exposes
the same role capability behind the same Dator offer, but it does not start a
Python HTTP process. The Node daemon owns the role provider and evaluates a
static `json_e_flow` configuration in-process.

## Stratum

```text
Arca or another workflow producer
  -> Dator service offer match
  -> dispatch.kind = "role-module"
  -> role host capability, for example role.example-summarizer.execute
  -> daemon-owned json_e_flow provider
  -> service-dispatch-response
```

The JSON-e-flow role adapter is good when the role is a small, static value
composition or a thin mediator around explicit host capabilities. It is not a
place for Git semantics, OS command construction, model prompting, filesystem
scans, or network clients. Those effects belong behind other capabilities, such
as `sensorium.directive.invoke`, with explicit allowlists and audit trails.

## Files

- `daemon-config.fragment.json` - daemon config fragment adding one
  `middleware_json_e_flow_services` entry.
- `dator-offer.fragment.json` - Dator offer fragment routing
  `example/summarize` to the role capability.
- `invocation.example.json` - dry-run invocation shaped like a Dator
  `role-module` dispatch.
- `mock-host-calls.example.json` - empty dry-run host-call mocks; this example
  has no `call` steps.

## Run A Dry-Run

Create a temporary daemon data directory, copy the config fragment into
`config/00-json-e-flow-example.json`, and run:

```sh
orbiplex-node-daemon json-e-flow-dry-run \
  --data-dir /tmp/orbiplex-json-e-role-example \
  --middleware-id example-summarizer-json-e-flow \
  --input invocation.example.json \
  --mock-responses mock-host-calls.example.json | jq .
```

The dry-run evaluates the same provider shape that the daemon uses at runtime,
but every host capability call must be mocked. Because this minimal role has no
host calls, the mock file is intentionally empty.

## Authoring Rules

- Keep `module_id` stable. It is the owner identity for module authtok, module
  store access, and capability provenance.
- `bindings.role_capability_id` is the role capability Dator targets.
- `context_projection` is the only place that maps incoming Dator fields into
  the JSON-e authoring context.
- `allowed_calls` is a static allowlist. A flow cannot call a capability that is
  not listed there.
- End with `validate` against `service-dispatch-response.v1` and then
  `respond`.
- Keep `answer/content` pointer-sized. Large data belongs in Git, Memarium,
  artifacts, Sensorium observations, or a module-owned store.
