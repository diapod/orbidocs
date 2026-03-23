# Ferment

`Ferment` is an optional development and experimentation tool that supports protocol testing, simulation, evaluation, and model-adjacent work around Orbiplex. It is not a required runtime component for protocol conformance.

## Purpose

Ferment exists to help developers and researchers:
- simulate protocol flows,
- run evaluation or training support workflows,
- inspect artifacts outside live production paths,
- accelerate iteration without turning the production Node into an overloaded dev shell.

## Scope

This document defines solution-level responsibilities of the Ferment component.

It does not define:
- mandatory protocol behavior,
- canonical Node persistence,
- public protocol conformance requirements.

## May Implement

### Scenario Runner

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-002.md`
- `doc/project/30-stories/story-003.md`

Related schemas:
- `question-envelope.v1`
- `response-envelope.v1`
- `learning-outcome.v1`
- `archival-package.v1`

Responsibilities:
- replay realistic protocol scenarios,
- generate deterministic test fixtures,
- support protocol-level smoke flows without coupling them to a specific UI.

Status:
- `todo`

### Evaluation and Training Support

Based on:
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`

Related schemas:
- `eval-report.v1`
- `model-card.v1`
- `training-job.v1`
- `adapter-artifact.v1`

Responsibilities:
- orchestrate evaluation support workflows,
- help prepare training and validation runs,
- emit reproducible artifacts for review without becoming the only execution path.

Status:
- `optional`

## Out of Scope

- required protocol conformance,
- mandatory federation runtime duties,
- canonical operator UI.

## Consumes

- `training-job.v1`
- `adapter-artifact.v1`
- `eval-report.v1`
- `model-card.v1`

## Produces

- test fixtures,
- scenario traces,
- optional development-side evaluation outputs

## Related Capability Data

- `ferment-caps.edn`

## Notes

Ferment should remain a modular side tool. The production Node must not depend on it for basic protocol behavior.
