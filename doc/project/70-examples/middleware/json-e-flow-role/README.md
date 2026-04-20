# JSON-e Flow Role Provider

This directory shows the minimal daemon configuration shape for a host-owned
`json_e_flow` middleware provider. Unlike `role-module-http/`, no supervised
application process is launched. The daemon exposes the configured role
capability directly and evaluates the static flow when Dator dispatches a role
module task.

Use this pattern when the role behavior is declarative and small:

- render a `service-dispatch-response`,
- call one or a few explicit host capabilities,
- write a small audit fact,
- publish a workflow-step completion record,
- or adapt one stable data shape into another.

Do not use it as a hidden scripting language. If the role needs domain-heavy
logic, long branching, network clients, filesystem traversal, Git commands, or
model prompts, put that behavior behind a proper capability provider such as a
Sensorium connector or a supervised middleware module.

## Files

- `daemon-config.fragment.json` - a minimal `middleware_json_e_flow_services`
  entry using a mocked host capability call.
- `invocation.example.json` - sample role invocation for dry-run.
- `mock-host-calls.example.json` - dry-run responses for host capability calls.

## Runtime Boundary

```text
Dator role dispatch
  -> daemon host capability registry
  -> json_e_flow provider selected by role capability
  -> static render/call/validate/respond steps
  -> service-dispatch-response
```

The flow has no ambient authority. It can only use values projected into its
context and host capabilities listed in `allowed_calls`.
