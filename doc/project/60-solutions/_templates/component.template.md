# Component Name

`Component Name` is a solution-level component in the Orbiplex architecture.

## Purpose

Describe what this component exists to do in the system and why it belongs in the solution architecture.

## Scope

This document defines solution-level responsibilities of the component.

It does not define:
- concrete module layout in an implementation repository,
- implementation-specific deployment details,
- whether this component is in-process or attached as a separate program/process,
- responsibilities owned by other components.

## Must Implement

### Capability Name

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/50-requirements/requirements-001.md`

Related schemas:
- `example-schema.v1`

Responsibilities:
- describe the first required responsibility,
- describe the second required responsibility.

Status:
- `todo`

## May Implement

### Optional Capability Name

Based on:
- `doc/project/40-proposals/example-proposal.md`

Related schemas:
- `optional-schema.v1`

Responsibilities:
- describe optional responsibility.

Status:
- `optional`

## Out of Scope

- explicitly name what this component should not own

## Consumes

- `input-schema.v1`

## Produces

- `output-schema.v1`

## Related Capability Data

- `component-caps.template.edn`

## Notes

Keep this document implementation-agnostic. Concrete module/file ownership belongs in the implementation repository.
