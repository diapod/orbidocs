# Command Stdio Executor Config

Source schema: [`doc/schemas/command-stdio-executor-config.schema.json`](../../schemas/command-stdio-executor-config.schema.json)

Configuration contract for one bounded command_stdio middleware executor. The executor invokes one external process per envelope, sends a workflow envelope as one JSON line on stdin, expects one middleware-decision JSON value on stdout, and retains stderr only for bounded diagnostics.

## Governing Basis

- [`doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`](../../project/40-proposals/019-supervised-local-http-json-middleware-executor.md)
- [`doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`](../../project/40-proposals/049-json-e-middleware-transformer-executor.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)

### Stories

- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`id`](#field-id) | `yes` | string | Stable executor identifier used by hook policies, diagnostics, and execution traces. Runtime validation rejects empty or whitespace-only values. |
| [`executable`](#field-executable) | `yes` | string | Executable path or command name passed to the host process launcher. Runtime validation rejects empty or whitespace-only values. |
| [`args`](#field-args) | `yes` | array | Process arguments appended after the executable. Arguments are host-local launch data, not shell-interpreted command text. |
| [`cwd`](#field-cwd) | `yes` | string \| null | Optional working directory for the child process. null means inherit the host process working directory. |
| [`env`](#field-env) | `yes` | object | Extra environment variables injected before optional sandbox hooks run. This map is additive unless a sandbox profile later clears or rewrites the environment. |
| [`timeout_ms`](#field-timeout-ms) | `yes` | integer | Maximum wall-clock runtime for one external executor invocation, in milliseconds. This maps to the Rust Duration field named timeout. |
| [`max_stdout_bytes`](#field-max-stdout-bytes) | `yes` | integer | Maximum number of stdout bytes accepted from the child process before the invocation fails closed. |
| [`max_stderr_bytes`](#field-max-stderr-bytes) | `yes` | integer | Maximum number of stderr bytes retained from the child process for diagnostics before the invocation fails closed. |
## Field Semantics

<a id="field-id"></a>
## `id`

- Required: `yes`
- Shape: string

Stable executor identifier used by hook policies, diagnostics, and execution traces. Runtime validation rejects empty or whitespace-only values.

<a id="field-executable"></a>
## `executable`

- Required: `yes`
- Shape: string

Executable path or command name passed to the host process launcher. Runtime validation rejects empty or whitespace-only values.

<a id="field-args"></a>
## `args`

- Required: `yes`
- Shape: array

Process arguments appended after the executable. Arguments are host-local launch data, not shell-interpreted command text.

<a id="field-cwd"></a>
## `cwd`

- Required: `yes`
- Shape: string | null

Optional working directory for the child process. null means inherit the host process working directory.

<a id="field-env"></a>
## `env`

- Required: `yes`
- Shape: object

Extra environment variables injected before optional sandbox hooks run. This map is additive unless a sandbox profile later clears or rewrites the environment.

<a id="field-timeout-ms"></a>
## `timeout_ms`

- Required: `yes`
- Shape: integer

Maximum wall-clock runtime for one external executor invocation, in milliseconds. This maps to the Rust Duration field named timeout.

<a id="field-max-stdout-bytes"></a>
## `max_stdout_bytes`

- Required: `yes`
- Shape: integer

Maximum number of stdout bytes accepted from the child process before the invocation fails closed.

<a id="field-max-stderr-bytes"></a>
## `max_stderr_bytes`

- Required: `yes`
- Shape: integer

Maximum number of stderr bytes retained from the child process for diagnostics before the invocation fails closed.
