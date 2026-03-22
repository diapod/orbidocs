---
render_macros: true
---

# Stories Index

This directory contains scenario documents that describe user-facing or operator-facing flows in a concrete narrative form.

## Current Stories

{{ list_matching_pages("story-*.md", page=page) }}

## Promotion Rule

Promote a story into:

- `doc/project/50-requirements/` when the scenario stabilizes into explicit system behaviour,
- `doc/normative/50-constitutional-ops/` when the story implies rights, duties, thresholds, or governance semantics.
