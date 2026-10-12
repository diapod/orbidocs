# Challenge 097: Fresh-Identity Messaging Onboarding

## Executive Summary

Fresh identities created in Node UI need an honest, recoverable path through local
preparation without acquiring federation issuer authority automatically. Messaging
readiness must describe demonstrated prerequisites, while a narrow acceptance profile
must remain usable when Messaging preparation is deferred.

Recorded: `2026-10-12`.

## Context and Problem Statement

A local participant, an unlocked key and an active operator binding do not admit that
participant as a federation passport issuer. The observed refusal to issue passports
for an unadmitted fresh identity protects this authority boundary.

A separate read-model defect equates the absence of a configured readiness blocker
with a usable local send passport. Correcting that read can expose another problem:
the pre-repair Welcome Wizard required Messaging completion before entering `/app`.
Narrow profiles can consequently become trapped in a step outside their purpose.

## Proposed Direction

[Proposal 097](../40-proposals/097-fresh-identity-onboarding-and-messaging-readiness.md)
defines participant-specific readiness, a shared evaluator, a separate federation
issuer fact, explicitly deferred onboarding, signed non-authoritative admission
requests, durable setup idempotency, and fresh-identity message-delivery acceptance.
It separates the initial read/onboarding repair from later execution enforcement and
passport migration. Federation authority remains owned by
[Proposal 076](../40-proposals/076-federation-identity-and-network-selector.md).

## Trade-offs

Truthful readiness can expose incomplete profiles that previously appeared ready.
Explicit deferral preserves access to unrelated UI work without erasing those gaps.
A later enforcement change needs migration because existing sends do not uniformly
require a local `messaging-send` passport.

## Failure Modes and Mitigations

Prevent automatic sovereign admission, per-peer passports being counted as global
send permission, another participant's readiness being inherited, duplicate passport
issuance, and GET-driven preparation. Retain evidence for each evaluated prerequisite
and distinguish proposed behavior from measured runtime results.

## Open Questions

How should ordinary participants receive limited grants without becoming sovereign
issuers? P076 owns this unresolved policy; the current issue API must not decide it
implicitly through onboarding.

## Next Actions

P097 Stage A is implemented and locally qualified on `2026-10-12`, including delivery
between fresh UI identities and continued access to `/app` from a deferred narrow
profile. See `node:docs/evidence/messaging-onboarding/README.md` for the separate
runtime, conformance and strict Story-010 evidence classes. This is not full
Story-013 model/VM execution or a general ordinary-participant grant policy.
Schedule execution enforcement only through its separate migration stage.
