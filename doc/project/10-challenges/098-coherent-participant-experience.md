# Challenge 098: Coherent Participant Experience

Recorded: `2026-11-06`.

## Executive Summary

An ordinary participant needs a recognizable place to start, resume work and
understand what requires attention. Adding middleware must preserve that
orientation. Orbiplex needs a default experience as well as an extension mechanism:
an empty configurable shell would leave the central product decision unresolved.

## Context and Problem Statement

The source review recorded in [P098: Alpha UI](../40-proposals/098-alpha-ui.md)
found a participant home with illustrative content and repeated navigation
destinations, alongside working onboarding, contacts, chat and notification
mechanisms. Users would still need to infer how these surfaces fit together.
This is a source-based design diagnosis, not a measured usability result.

The requested direction combines a calm home organized around intentions with
guided processes inspired by ordering kiosks: a bounded decision, an explicit
continuation and a predictable way back. Conversation, reading and exploration
also need direct interaction without an unnecessary sequence of screens.

Packages should contribute discoverable functions. Operators should be able to
arrange them through configuration without becoming HTML, HTMX or JavaScript
template authors. Rumors need a recognizable place that preserves their provisional
epistemic status and their existing disclosure and authorship boundaries.

## Proposed Direction

P098 proposes the Alpha UI baseline: default categories and appearance, a common
navigation and guided-flow contract, a participant-scoped attention path, package
entry-point contributions and file-backed operator composition. It reuses P091,
P095 and P057 instead of creating configuration, interaction or notification owners.
Find material includes a proposed read-only Memarium explorer. Its participant
projection must preserve P036/S002 authority, classification and retention; a
Personal space is not automatically a per-user folder.

## Trade-offs

A stable common shell limits arbitrary composition. Guided decisions reduce the
amount presented at once but add navigation; use them for bounded processes.
Operator customization must preserve the participant's orientation and control.

## Failure Modes and Mitigations

Prevent decorative status being mistaken for live evidence, installed packages
being mistaken for permission, menu placement being mistaken for authorization,
and repeated rumors being mistaken for verified facts. Preserve entered choices,
explain unavailable actions, and make uncertain outcomes recoverable through
the owning service.

## Open Questions

Which labels and grouping work best for first-time participants? Which participant
Whisper and Memarium surfaces can be admitted under the existing contracts? P098
records these as separate UX and authority questions; neither is answered by a
mockup alone. Its architecture review also separates durable layout configuration
from current catalog/availability and from protected participant content.

## Next Actions

Review P098's defaults, freeze its bounded data contracts, then implement and
validate the tracked slices. The proposal and this challenge do not change Node
behavior or qualify an alpha release.
