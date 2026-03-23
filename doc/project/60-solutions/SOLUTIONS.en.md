---
render_macros: true
---

# Solutions Index

This directory defines solution-level components that bridge project requirements and implementation repositories.

It captures what the solution architecture expects from core components such as the Orbiplex Node, thin control clients, and optional development tools, without leaking concrete module layout from any one implementation repository.

Node-scoped roles may later appear here as separate components even if they are operationally attached to the Node. For example, an archivist, memarium provider, or sensorium provider may be implemented as a separate program or process with its own API and runtime, while still remaining part of the Node solution surface.

## Current Solution Components

{{ list_matching_pages("*.md", page=page, exclude="SOLUTIONS*.md", summaries=true) }}

## Generated Views

- [Solution Capability Matrix](CAPABILITY-MATRIX.en.md)
