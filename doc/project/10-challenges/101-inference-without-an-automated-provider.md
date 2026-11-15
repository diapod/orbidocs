# Challenge 101: Inference Without an Automated Provider

Recorded: `2026-11-14`.

## Executive Summary

A Node should support an explicitly attended text-inquiry profile when its only
available model is a chat operated separately by the user. Preparing an export
packet and importing a response must not require an already working model.

## Context and Problem Statement

Copy-paste can connect an external consultation to the existing inference
contract, but does not establish provider identity, locality or execution.
Waiting for a person must survive restart without keeping a runtime invocation
open, replaying disclosure, or extending grants. User participation does not
override confidentiality or authorize publication.

## Proposed Direction

[P101](../40-proposals/101-manual-inference-exchange.md) defines a native host
manual-exchange transport under Inquirium, reusing P089 result/commit patterns,
S029 deferred operations, P066 consent and existing interaction surfaces.
Agent, Assistant Channel and Corpus remain consumers, not separate bridge owners.

## Trade-offs

This removes the requirement for an automated model provider for supported
attended inquiries, at the cost of human attention, latency and unverifiable
external execution. It does not supply embeddings or autonomous background work.

## Failure Modes and Mitigations

Gate export before packet visibility; bind imports to principal and operation;
persist one immutable packet under finite retention; reject ambiguous framing;
never automate the external browser or upgrade an assertion into execution proof.

## Open Questions

Higher-class export, multimedia and unattended batch providers remain outside
the first profile. They require separate decisions and evidence.

## Next Actions

Freeze P101's contracts and qualify a restartable exchange through the real UI
endpoint with all automated model candidates absent.
