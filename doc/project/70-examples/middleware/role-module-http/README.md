# Minimal HTTP Role Module

This example shows the smallest useful middleware process that Dator can call
through a `dispatch.kind = "role-module"` offer.

## Stratum

```text
Arca or another workflow producer
  -> Dator service offer match
  -> dispatch.kind = "role-module"
  -> role host capability, for example role.example-summarizer.execute
  -> role module HTTP/JSON endpoint
  -> service-dispatch-response
```

The role module may call other host capabilities, such as Memarium or
`sensorium.directive.invoke`, but it must not call `sensorium.connector.invoke`
directly. Concrete OS, model, Git, filesystem, or network effects should remain
behind Sensorium-core mediation.

## Files

- `minimal_role_module.py` - standalone stdlib HTTP/JSON role module.
- `dator-offer.fragment.json` - Dator offer fragment routing a service type to
  the role capability.

## Run Locally

```sh
python3 minimal_role_module.py
curl -s http://127.0.0.1:47989/healthz | jq .
curl -s -X POST http://127.0.0.1:47989/v1/middleware/init | jq .
```

Example execution:

```sh
curl -s -X POST http://127.0.0.1:47989/v1/role/execute \
  -H 'content-type: application/json' \
  -d '{
    "schema_version": "v1",
    "capability_id": "role_task_execute",
    "role/capability_id": "role.example-summarizer.execute",
    "dispatch/id": "dispatch:example:1",
    "service_type": "example/summarize",
    "request/input": {"text": "A long input that should be summarized."},
    "workflow/run-id": "run:example",
    "workflow/phase-id": "summarize",
    "correlation/id": "run:example"
  }' | jq .
```

## Authoring Rules

- `role/capability_id` selects the role behavior.
- `request/input` is domain input owned by the workflow/service-order layer.
- Preserve `dispatch/id`, `workflow/run-id`, `workflow/phase-id`, and
  `correlation/id` in emitted facts, directives, or observations.
- Return `service-dispatch-response` with `completed`, `failed`, or
  `rejected-invalid-request`.
- Keep `answer/content` pointer-sized. Large bytes belong in explicit data
  planes: Git, Memarium, artifacts, or a module-owned store.
