# Challenge 091: Predictable Operator Configuration

## Executive Summary

An operator or power user should not have to discover a different control model
for every Node component. The challenge is not primarily the number of settings,
but uncertainty about where a setting belongs, what overrides it, and whether a
saved change is already active. Every durable behavioral setting should have an
inspectable, file-backed declaration and an explainable effective value.

## Context and Problem Statement

Node already has layered JSON configuration, middleware configuration fragments,
persisted UI toggles, and configuration inspection commands. Some domains also
explain their own policy composition. These mechanisms do not yet establish one
operator-facing contract across global settings, module instances and workflows.

The recurring questions are:

- Where do I inspect or change this setting without using the GUI?
- Which files contributed to this value or subtree, and which declarations lost?
- Is this a default, an explicit choice, a derived value, or an active constraint?
- Did saving the change apply it, or does it require reload, restart or approval?
- Can I remove my override without copying today's default into permanent config?

## Proposed Direction

Develop [Proposal 091: File-backed Configuration and Explainable Composition](../40-proposals/091-file-backed-configuration-and-explainable-composition.md).
Use one data contract for file editing, CLI and GUI, while retaining domain-owned
validation and authority boundaries. Explain both scalar settings and composed
subtrees in the context of a particular node, module or workflow.

## Trade-offs

Uniform access improves operator confidence, reproducibility and migration, but
requires explicit source tracking and configuration lifecycle semantics. A single
interface must not become a single giant configuration file, a second domain
policy engine, or a rule that every state transition is editable configuration.

## Failure Modes and Mitigations

- Hidden UI overrides: expose their files and precedence and migrate them without
  silently changing current choices.
- Materialized defaults mistaken for operator intent: preserve inheritance and
  distinguish explicit pinning from generated projections.
- Workflow settings broadening host authority: keep scope selection separate from
  domain admission and safety constraints.
- File edits treated as signed consent: preserve independent approval facts.
- Effective values leaking secrets: expose references and redacted diagnostics.

## Open Questions

The complete inventory of settings and runtime writers remains to be audited.
Proposal 091 tracks the inventory, bounded initial slice, compatibility decisions
and later coverage gate; this challenge does not claim a finished implementation.

## Next Actions

1. Deliver the initial source/writer inventory and verification gate under
   P091-001a; audit the remaining module-local and workflow controls under
   P091-001b. P091-001 aggregates completion of both audits.
2. Implement and verify the four representative cases defined by Proposal 091
   before extending the same contract to the remaining inventoried settings.
