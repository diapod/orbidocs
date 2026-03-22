---
render_macros: true
---

# Memos Index

This directory holds short idea notes, seeds, and design prompts that are not yet mature enough to become proposals, requirements, or stories.

## Current Memos

{{ list_matching_pages("*.md", page=page, exclude="*.pl.md,*.en.md", summaries=true) }}

## Promotion Rule

Each memo should remain short. When an idea gains stable semantics, explicit actors, or implementation pressure, promote it into one of the following:

- `doc/project/30-stories/` for user-facing scenarios,
- `doc/project/40-proposals/` for architectural direction,
- `doc/project/50-requirements/` for concrete system requirements,
- `doc/normative/50-constitutional-ops/` if it becomes normative.
