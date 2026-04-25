# Middleware Package UI Example

This is the smallest external Node UI surface package.

Install it by copying this directory to:

```sh
<data_dir>/middleware-packages/example-middleware/
```

The Node UI reads `middleware.package.json`, adds the declared navigation entry, and serves the HTML fragment from:

```text
/middleware/example/_ui
```

The package follows the recommended directory convention:

```text
ui/
  index.html
ui-op/
  operator-surfaces.json
config/
  json-e-flow-services.json
```

`ui/` contains renderable HTML(X) fragments. `ui-op/` contains operator-surface
metadata that corresponds to what a live middleware module would report in
`middleware-module-report.operator_surfaces`. The manifest also shows how a
package can point at a declarative config fragment. Daemon-side activation of
config fragments requires a current package signature; the UI fragment itself
stays a no-JavaScript host-rendered asset.
