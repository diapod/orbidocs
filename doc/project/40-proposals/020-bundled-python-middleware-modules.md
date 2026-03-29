# Proposal 020: Bundled Python Middleware Modules for Hard MVP

Based on:
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/30-stories/story-006.md`
- `doc/project/60-solutions/node.md`

## Status

Proposed (Draft)

## Date

2026-03-30

## Executive Summary

The hard MVP should treat `Orbiplex Dator` and `Orbiplex Arca` as bundled
middleware modules distributed together with `Orbiplex Node`.

They are:

- implemented in Python,
- launched as supervised local services,
- attached through the host-owned `http_local_json` executor,
- replaceable in principle, but shipped by default as part of the Node release.

This proposal freezes the packaging and operational shape of those modules so the
implementation can move without inventing a second deployment model for
"reference" middleware.

## Context and Problem Statement

Proposal 019 already freezes:

- a supervised `http_local_json` executor,
- host-owned lifecycle,
- bundled `Dator` and `Arca` as hard-MVP modules.

What is still missing is the packaging contract.

Without it, implementors can drift into incompatible patterns:

1. treat the modules as ad-hoc developer scripts,
2. require operators to install Python dependencies manually,
3. let the modules bypass host lifecycle by running them out-of-band,
4. couple module deployment to a specific Python toolchain hidden from the host.

That would slow implementation and weaken reproducibility.

## Goals

- Freeze one practical packaging model for hard-MVP Python middleware.
- Ensure `Dator` and `Arca` can be started by the Node through explicit launch
  contracts rather than human folklore.
- Keep the host authoritative over lifecycle, readiness, restart, and policy.
- Make the packaging shape simple enough to implement in CI and local builds now.

## Non-Goals

- This proposal does not freeze one universal Python build tool.
- This proposal does not require publishing the middleware modules as independent
  ecosystem packages before the MVP ships.
- This proposal does not turn the modules into privileged in-process plugins.

## Decision

The hard MVP distribution should package `Dator` and `Arca` as bundled Python
middleware modules with host-launchable entrypoints.

The Node host remains responsible for:

- the `http_local_json` runtime,
- launch command resolution,
- process supervision,
- readiness wait,
- `middleware-init`,
- operator-visible lifecycle state.

The module remains responsible only for:

- serving the local HTTP middleware contract,
- reporting readiness,
- returning `MiddlewareDecision`,
- returning module metadata on `middleware-init`.

## Proposed Packaging Model

Each bundled module should ship as a release-local module directory under a stable
Node-owned subtree, for example:

- `modules/dator/`
- `modules/arca/`

Each subtree should contain at least:

- the Python source or packaged runtime payload,
- a host-resolved executable entrypoint,
- static configuration needed by the module itself,
- version metadata visible to the release process.

The host should launch each module through an explicit executable path recorded in
its supervised `http_local_json` config. The Node must not depend on ambient shell
lookup or on operators manually activating a virtual environment.

In other words:

- the Node launches an explicit executable,
- the module serves loopback HTTP,
- the host owns everything else.

## MVP Operational Shape

The hard MVP should assume two supervised components:

- `middleware.dator`
- `middleware.arca`

Recommended launch shape:

- `middleware.dator` -> launch a Python entrypoint serving `/readyz`,
  `/healthz`, and `/v1/middleware/invoke`
- `middleware.arca` -> launch a Python entrypoint serving the same host contract
  surface

The exact Python packaging form may vary by build pipeline:

- virtualenv-backed executable,
- zipapp,
- PEX-like artifact,
- other host-addressable executable wrapper

But the host-visible contract is fixed:

- executable path is explicit,
- working directory is explicit,
- environment map is explicit,
- no operator-side manual installation is required for normal MVP startup.

## Security and Authority Boundary

Bundling the modules with Node does not elevate their authority.

Even when shipped together:

- they do not receive host private keys,
- they do not sign protocol artifacts directly,
- they do not own settlement authority,
- they do not own transport identity,
- they remain bounded by the host's middleware envelope and field policy.

## Trade-Offs

Advantages:

- faster implementation path,
- reproducible deployment shape,
- no second-class "example module" limbo,
- easier CI and integration testing.

Costs:

- Node release becomes a multi-runtime distribution,
- packaging discipline becomes part of MVP scope,
- release automation must account for Python module payloads.

## Open Questions

1. Should the release bundle ship one shared Python runtime for both modules, or
   two isolated module-local runtimes?
2. Which module version metadata should be surfaced through `middleware-init`
   versus release metadata?
3. Should the first MVP support disabling bundled modules individually at install
   time, or only at runtime?

## Next Actions

1. Define release-local directory and executable naming conventions for bundled
   middleware modules.
2. Add hard-MVP component configs for `middleware.dator` and `middleware.arca`.
3. Add build and CI steps that materialize host-launchable Python entrypoints.
4. Add integration tests proving bundled startup under the supervised
   `http_local_json` executor.
