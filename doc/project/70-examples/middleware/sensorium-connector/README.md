# Minimal Sensorium Connector

This example shows a small Sensorium connector middleware. It is a separate
supervised process with `module_role = "sensorium-connector"`. It is not a
Sensorium-core plugin.

## Stratum

```text
Consumer or role module
  -> sensorium.directive.invoke
  -> Sensorium-core policy, allowlist, audit, mediation
  -> sensorium.connector.invoke
  -> connector-owned HTTP/JSON endpoint
  -> connector result + optional observation candidates
  -> Sensorium-core admission, store, and local Agora publish
```

Consumers and role modules should never call `sensorium.connector.invoke`
directly. They call Sensorium-core. Sensorium-core owns admission, audit, and
connector selection.

## Files

- `minimal_sensorium_connector.py` - standalone stdlib HTTP/JSON connector.
- `sensorium-core-reference-action.fragment.json` - example Sensorium-core
  allowlist/reference action entry for the connector.

## Run Locally

```sh
python3 minimal_sensorium_connector.py
curl -s http://127.0.0.1:47990/healthz | jq .
curl -s -X POST http://127.0.0.1:47990/v1/middleware/init | jq .
```

Example connector invocation, normally sent by Sensorium-core:

```sh
curl -s -X POST http://127.0.0.1:47990/v1/sensorium/connector/invoke \
  -H 'content-type: application/json' \
  -d '{
    "schema": "sensorium-connector-directive.v1",
    "directive": {
      "directive/id": "directive:example:1",
      "action_id": "example.echo",
      "parameters": {"text": "hello"},
      "correlation/id": "run:example"
    },
    "allowlist_entry": {
      "action_id": "example.echo",
      "connector_id": "example-sensorium-connector",
      "result_contract": {
        "signal_kind": "ai.orbiplex.example/echo",
        "signal_family": "example/echo"
      }
    }
  }' | jq .
```

## Authoring Rules

- Declare `module_role: "sensorium-connector"` and at least one connector action
  or observation in the middleware module report.
- Treat `allowlist_entry` as policy supplied by Sensorium-core, not by the
  caller.
- Keep connector results structured and bounded.
- Return observation candidates only after the connector has a fact about the
  world. Sensorium-core assigns final IDs, admission metadata, storage metadata,
  and publish topics.
- Do not publish directly to Agora and do not write audit outcomes. Those are
  Sensorium-core responsibilities.
