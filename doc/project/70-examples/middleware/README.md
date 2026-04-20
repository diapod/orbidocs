# Middleware Examples

Orbiplex middleware modules are supervised application processes. They are not
in-process plugins and not Rack/Express/Ring-style interceptors. A module talks
to the Node daemon through HTTP/JSON, declares capabilities in its module report,
and receives work through host-owned routing.

## Examples

- `role-module/` - a minimal role module behind a Dator offer.
- `sensorium-connector/` - a minimal Sensorium connector called only by
  Sensorium-core.

## Common Shape

A small middleware module usually exposes:

- `GET /healthz` for local liveness checks.
- `POST /v1/middleware/init` returning a middleware module report.
- One or more module-owned invoke paths registered in `host_capability_handlers`.

The daemon owns process supervision, module auth tokens, host capability routing,
and auditability. The module owns only its local behavior behind the declared
capability.
