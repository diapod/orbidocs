# Challenge 099: Private Companion Device Access

Recorded: `2026-11-07`.

## Executive Summary

A participant should be able to connect a companion device to their own Node
without a mandatory hosted intermediary. Pairing, scoped consent and bounded
delivery form the shared bridge. Its first profile brings selected Apple Health
observations to the computer without Apple account credentials on the Node;
the phone keeps control of local read/export consent.

## Context and Problem Statement

HealthKit is an on-device permission boundary. A desktop connector alone cannot
provide that permission, and a phone may be locked or disconnected while the Node
is asleep. Importing a file solves historical access but not incremental delivery,
deletions or honest freshness. Future mobile functions should reuse pairing and
delivery without silently inheriting permission to read health data.

## Proposed Direction

[P099: Companion App and Device-to-Node Bridge](../40-proposals/099-companion-app-and-device-bridge.md)
defines one phone-to-Node slice: a native read-only provider, bounded durable
synchronization into a Node-owned sample history, and Sensorium summaries of it.
It records pinned Pulso/HealthSync reuse candidates and separates upstream
licensing from project licensing and Apple distribution. It builds on
P006/P045/P082 rather than creating a mobile Node.

## Trade-offs

A native edge requires signing and real-device qualification. It gives direct
control over consent and recovery but cannot promise continuous iOS execution.
One paired Node keeps the first authority and synchronization model bounded.

## Failure Modes and Mitigations

Prevent empty reads from becoming zero measurements, lost acknowledgements from
duplicating data, old retries from resurrecting deletions, and local export consent
from becoming model or publication consent. Bound offline storage and expose gaps.

## Open Questions

Select the minimal reusable Swift source set, authenticate pairing through existing
Node owners, and resolve the application's license/distribution path before release.
The proposal owns these decisions and their acceptance gates.

## Next Actions

Follow P099-001–006 for reuse qualification, contracts, implementation and scoped
offline/device acceptance, with P099-008 qualifying the shared Sensorium admission
prerequisite from P045-OBS-001. P099-007 separately qualifies distribution. This
challenge changes no code or existing alpha release requirement.
