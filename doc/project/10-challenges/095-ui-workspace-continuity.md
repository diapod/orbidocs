# Challenge 095: UI Workspace Continuity

## Executive Summary

Make everyday Node UI work feel continuous without replacing HTMX/HATEOAS or
moving domain authority into the client.

## Context and Problem Statement

Opening supporting evidence or inspecting a setting should not lose a conversation,
draft, scroll position or keyboard focus. Existing modal and transition helpers
are useful antecedents, not yet proof of a shared workspace interaction contract.

## Proposed Direction

[Proposal 095](../40-proposals/095-node-ui-interaction-layer.md) defines a small
interaction layer over server-rendered HTML, with Stimulus as the preferred
candidate for controller lifecycle management, subject to a bounded compatibility
spike. The first slice is one conversation with a detail panel and return path.

## Trade-offs

Shared presentation mechanics can reduce repeated code and cognitive load, but a
new client router or domain store would undermine the existing architecture.

## Failure Modes and Mitigations

Guard against duplicate requests, lost drafts, leaked history, stale approvals and
inaccessible panels through explicit ownership and retained interaction tests.

## Open Questions

Does Stimulus simplify the existing helpers enough to justify its dependency?
Which existing conversation/detail pair provides the smallest representative slice?

## Next Actions

Start framework-independent history hardening (P095-007) and the P095-001
inventory, then run P095-002's isolated browser/WebView spike. Production
controller adoption also requires P095-008's fragment, CSP and native-command
boundary checks. Do not infer measured usability gains from a framework choice.
