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

The manifest also shows how a package can point at a declarative config fragment. Daemon-side activation of config fragments requires a current package signature; the UI fragment itself stays a no-JavaScript host-rendered asset.
