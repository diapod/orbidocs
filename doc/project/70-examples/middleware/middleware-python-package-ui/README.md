# Python Middleware Package UI Example

This example shows a supervised Python middleware package that contributes a
runtime `server-html` operator surface.

It is the Python counterpart of `middleware-package-ui/`. The JSON package UI
example contributes install-time host-rendered fragments from `ui/`; this
example has a live Python service that declares `operator_surfaces` during
`middleware-init` and serves its own HATEOAS/HTMX HTML under `entry_path`.

## Shape

```text
middleware.package.json
config/
  http-local-service.json
service.py
ui-op/
  operator-surfaces.json
```

There is intentionally no `ui/` directory here. The HTML is not a static
install-time fragment. It is rendered by the Python middleware service at:

```text
/ui
/ui/status
```

Node UI exposes it under the host-owned mount:

```text
/middleware/example-python/...
```

The stable public route is derived from `surface_id`, not from the middleware's
local port.

## Runtime contract

`POST /v1/middleware/init` returns a module report with:

```json
{
  "operator_surfaces": [
    {
      "surface_id": "example-python",
      "label": "Example Python",
      "rendering": "server-html",
      "entry_path": "ui"
    }
  ]
}
```

The Node UI proxy then maps:

```text
/middleware/example-python/status -> /ui/status
```

on the live supervised module.

## Developer notes

The example imports `orbiplex_middleware_ui`. In a supervised Node environment,
the daemon provides the helper through `ORBIPLEX_MIDDLEWARE_UI_PYTHON_LIB_DIR`
and `PYTHONPATH`. A distributable package may also vendor the helper under
`lib/ui/python/` and prepend it to `sys.path` before importing.

The browser never receives the daemon authtok or the host capability token.
Browser requests go to Node UI. Module-to-daemon capability calls happen
server-side from Python through the host capability API.
