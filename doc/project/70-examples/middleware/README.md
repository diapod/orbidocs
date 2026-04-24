# Middleware Examples

Orbiplex middleware behavior is routed by host-owned capabilities. The common
shape is a supervised application process that talks to the Node daemon through
HTTP/JSON, but small static role adapters may also be hosted directly by the
daemon as `json_e_flow` providers.

Neither shape is a Rack/Express/Ring-style interceptor chain. The daemon owns
capability routing, supervision where applicable, module auth tokens, and the
audit boundary. The module or flow owns only its local behavior behind the
declared capability.

## Examples

- `role-module-http/` - a minimal supervised HTTP/JSON role module behind a
  Dator offer.
- `role-module-json-e/` - the same role-module idea as a daemon-hosted
  `json_e_flow` provider.
- `json-e-flow-role/` - a minimal generic `json_e_flow` role provider with a
  mocked host capability call.
- `middleware-package-ui/` - minimal `middleware.package.v1` package that
  contributes a no-JavaScript Node UI surface and can carry signed config
  fragments.
- `sensorium-connector/` - a minimal Sensorium connector called only by
  Sensorium-core.

## Supervised HTTP Shape

A small middleware module usually exposes:

- `GET /healthz` for local liveness checks.
- `POST /v1/middleware/init` returning a middleware module report.
- One or more module-owned invoke paths registered in `host_capability_handlers`.

The daemon owns process supervision, module auth tokens, host capability routing,
and auditability. The module owns only its local behavior behind the declared
capability.

## JSON-e Flow Shape

A JSON-e-flow role provider usually declares:

- one `middleware_json_e_flow_services` entry in daemon config,
- stable `module_id`, `component_id`, and `template_id`,
- `bindings.role_capability_id` for Dator dispatch,
- optional per-flow `raw_signal_access` if this flow needs the initial raw
  invocation payload or prior component input snapshots,
- `context_projection` mapping the incoming role invocation into authoring
  variables,
- `allowed_calls` as the static host capability allowlist,
- a small `render` / `call` / `validate` / `respond` step list.

`raw_signal_access` is a permission to expose host-preserved context, not a
template variable by itself. To use it, the flow must also project the needed
field, for example:

```json
{
  "raw_signal_access": {
    "requires_raw_signal": true,
    "requires_component_io_trace": false,
    "reason": "compare normalized request with the original role invocation"
  },
  "context_projection": {
    "raw_signal": "$.trace.raw_signal_access.raw_signal"
  }
}
```

Use `requires_component_io_trace` only when the flow really needs the history of
prior component inputs in the same local passage. It is heavier than preserving
the initial raw signal.

Use JSON-e-flow for small declarative adapters. Move domain-heavy behavior to a
proper capability provider, such as a supervised middleware module or a
Sensorium connector.

## Middleware Package Shape

External packages live under `<data_dir>/middleware-packages/<package>/` and are
described by `middleware.package.v1`. A package may contribute host-rendered UI
fragments and declarative config fragments. Config fragments are activated by
the daemon only after the package artifact has a current operator signature;
the package remains data, not executable JavaScript.
