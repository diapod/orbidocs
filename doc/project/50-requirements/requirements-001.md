# Requirements 001: Swarm Node Onboarding and Federated Answer Procurement

Based on: `doc/project/30-stories/story-001.md`
Date: `2026-02-22`
Status: Draft (MVP scope)

## Executive Summary

This document defines MVP requirements for onboarding a Swarm Node, building local
knowledge context, discovering remote specialist nodes, procuring answers through
explicit contracts and receipts, and returning traceable responses to the user.

The requirements prioritize:
- privacy-preserving discovery,
- explicit contracts for offers and settlement,
- deterministic selection and validation logic,
- auditable outcomes (receipt, reputation update, provenance).

## Context and Problem Statement

The system must answer domain-specific user questions using:
- local knowledge first (installed models + indexed local files),
- remote federation only when local knowledge is insufficient.

The main problem is to coordinate remote answer procurement without sacrificing
privacy, auditability, or economic fairness. The onboarding flow must also stay
practical for non-expert users (settlement profile handling, model installation,
directory ingestion).

## Proposed Model / Decision

### Actors and Boundaries

- `User`: defines node profile, asks questions, receives answers.
- `Local Swarm Node App`: orchestrates onboarding, indexing, discovery, selection,
  contracts, and response composition.
- `Remote Specialist Node`: offers and provides answers.
- `Arbiter` (optional): confirms answer acceptance for settlement.
- `Procurement Contract`: enforces payment/settlement conditions without mandating one
  payment rail.

### Core Data Contracts (normative)

- `QuestionEnvelope`:
  - `question/id`, `delivery/scope`, `request/exposure-mode`, `response-channel-id`,
    responder filters, procurement intent.
- `ProcurementOffer`:
  - `offer/id`, `responder/node-id`, `price`, `deadline`, `answer bounds`,
    `specialization/tags`, `reputation/evidence`.
- `ProcurementContract`:
  - `contract/id`, selected `offer/id`, `deadline`, `acceptance criteria`,
    `confirmation/mode`, optional arbiter set.
- `ProcurementReceipt`:
  - `receipt/id`, `contract/id`, `outcome`, payer/payee signatures, optional arbiter
    signatures, optional settlement reference.
- `ResponseEnvelope`:
  - `response/id`, `question/id`, `answer`, `source_node`, optional `contract_id`,
    `confidence_signal`, human-origin provenance.

### Concrete Scenario (MVP happy path)

1. User asks a question.
2. Local node fails sufficiency check and publishes `QuestionEnvelope`.
3. Remote nodes return `ProcurementOffer` objects.
4. Local node selects one offer, opens private channel, sends full encrypted question.
5. Local node performs funding and settlement precheck, creates `ProcurementContract`.
6. Remote node answers, arbiter confirms (if required), contract settles,
   `ProcurementReceipt` is stored, and `ResponseEnvelope` is returned with provenance.

### Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The system MUST collect node name and specialization set during onboarding. | Fact | Story steps 3 |
| FR-002 | The system MUST create or restore a dedicated operational settlement profile and warn against mixing node operations with personal finances. | Fact | Story step 5 |
| FR-003 | The system MUST allow an optional payout destination or billing reference for later surplus settlement. | Fact | Story step 5 |
| FR-004 | The system MUST present compatible installable models with best-fit descriptions. | Fact | Story step 6 |
| FR-005 | The system MUST allow directory scanning configuration and specialization-to-directory mapping. | Fact | Story step 7 |
| FR-006 | The system MUST download selected models and notify readiness asynchronously. | Fact | Story steps 8-9 |
| FR-007 | The system MUST connect to the current swarm transport baseline and support publication on the event layer plus live participation on the room layer. | Fact | Story step 9 |
| FR-008 | The system MUST index discovered local content into a vector store and local orchestrator memory. | Fact | Story step 11 |
| FR-009 | The system MUST answer immediately when local sufficiency check passes. | Fact | Story step 13 |
| FR-010 | Published `QuestionEnvelope` artifacts MUST include stable question identity, delivery scope, response-channel id, exposure mode, question text, tags, responder filters, and procurement intent. | Fact | Story step 14 |
| FR-011 | Remote offers MUST be structured `ProcurementOffer` artifacts and include at least price, deadline, min/max answer length, specialization tags, node public key reference, and reputation evidence. | Fact | Story step 16 |
| FR-012 | Offer selection MUST score reputation, leniency fit, price, wait time, answer length bounds, specialization fit, and node traits. | Fact | Story step 16 |
| FR-013 | The system MUST create a unique private execution channel with selected node and optional arbiters. | Fact | Story step 16 |
| FR-014 | The full question MUST be re-sent in execution channel and MAY be encrypted per recipient key; refinements MUST stay within `max_delta_tokens`. | Fact | Story step 16 |
| FR-015 | The system MUST perform funding and settlement precheck before contract creation. | Fact | Story step 19 |
| FR-016 | The system MUST create a procurement contract with explicit acceptance criteria and one of three modes: arbiter-confirmed, self-confirmed (no arbiter), or no-confirmation (explicit zero-price offer). | Fact | Story step 19 |
| FR-017 | The system MUST validate received answers against contract criteria before settlement. | Fact | Story step 18 |
| FR-018 | If required confirmation is present and validation passes, the contract MUST settle and transfer agreed payment. | Fact | Story step 18 |
| FR-019 | The system MUST persist a signed receipt and update node reputation after each completed interaction. | Inference | Story step 19 |
| FR-020 | The returned user-facing response MUST include provenance metadata (`source_node`, `contract_id`, confidence signal). | Fact | Story step 20 |

### Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Discovery stage MUST preserve confidentiality of full query content. | Fact | Story step 14 |
| NFR-002 | Selection logic MUST be deterministic for identical offer sets (tie-break order must be explicit and stable). | Inference | Story step 16 |
| NFR-003 | Contracts, offers, receipts, and provenance fields MUST be versioned schemas to support interoperability across nodes. | Inference | Core intent: interoperability |
| NFR-004 | Every payment-affecting decision MUST be auditable through stored contract and receipt identifiers, while the concrete settlement rail remains outside the protocol core. | Inference | Core intent: auditability |
| NFR-005 | Human operator MUST be able to configure max price, max wait, and arbitration mode defaults. | Inference | Core intent: human agency |
| NFR-006 | The system SHOULD degrade gracefully when remote procurement fails (timeout/no offers) by returning explicit failure reason and retry options. | Inference | Story open continuation |
| NFR-007 | Key handling MUST support recipient-specific encryption for private channels without exposing plaintext in transit logs. | Fact | Story step 16 |
| NFR-008 | Reputation records MUST be tamper-evident (signed receipts and integrity hash publication strategy). | Inference | Story step 19 |

## Trade-offs

1. Privacy vs discoverability:
   - Benefit: query hash in discovery lowers leakage risk.
   - Risk: less context may reduce offer quality.
2. Strong contract criteria vs flexibility:
   - Benefit: deterministic settlement and clearer dispute boundaries.
   - Risk: stricter format/length constraints may reject otherwise useful answers.
3. Optional arbiters vs speed/cost:
   - Benefit: better trust for paid answers.
   - Risk: extra latency and coordination overhead.
4. Rail-neutral settlement vs immediate automation:
   - Benefit: avoids early lock-in to crypto-operator duties and keeps the protocol portable.
   - Risk: some settlement rails will initially remain more manual.
5. Rich reputation signals vs Sybil resistance complexity:
   - Benefit: improved node selection quality over time.
   - Risk: harder bootstrapping and abuse resistance.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| No offers received before timeout | User gets no remote answer | Return explicit timeout, offer retry with widened constraints, keep local fallback. |
| Insufficient funds or settlement capacity | Contract cannot be created | Block remote execution early, present refill or billing guidance and exact deficit. |
| Malformed or schema-incompatible offer | Selection/contract errors | Reject offer at ingestion, emit validation error reason, continue collecting offers. |
| Answer misses contract criteria | Failed settlement or bad UX | Validate pre-settlement and request one bounded revision when allowed. |
| Arbiter unavailable | Settlement stall | Auto-fallback to configured mode if contract allows, otherwise expire contract at deadline. |
| Query leakage in public discovery channel | Privacy breach | Enforce hash-only discovery payload and lint outgoing message schema. |
| Reputation manipulation attempts | Poor node choices | Require signed receipts and weighted trust from verified interaction history. |
| Local indexing pipeline failure | Lower local-answer rate | Show ingestion health status and continue with remote discovery path. |

## Open Questions

1. Which distributed storage backend should back reputation in production (beyond MVP local + integrity hash publication)?
2. What canonical key model should be primary for encryption identity (`PGP`, protocol-native signing keys, or both with strict precedence)?
3. What is the exact deterministic tie-break sequence when final offer scores are equal?
4. Should zero-price "free sample" offers be limited per node pair and time window to prevent abuse?
5. What bounded revision policy should be allowed before contract rejection (`retries`, `deadline extension`, `price impact`)?
6. How should confidence be computed in `ResponseEnvelope` (model score, retrieval coverage, arbitration outcome, or composite)?

## Next Actions

1. Define and freeze v1 schemas for `DiscoveryRequest`, `Offer`, `ExecutionTerms`, `SettlementContract`, `SettlementReceipt`, and `ResponseEnvelope`.
2. Create ADR-001 for identity/encryption strategy (`PGP` vs protocol-native signing keys, precedence and rotation).
3. Create ADR-002 for settlement policy defaults and arbiter fallback semantics.
4. Implement contract-validation tests for length bounds, deadline, and format acceptance criteria.
5. Implement deterministic offer scoring tests including equal-score tie-break cases.
6. Implement an end-to-end MVP happy-path test: local miss -> discovery -> offer select -> contract -> settlement -> provenance response.
7. Propose reputation MVP storage and integrity publication plan, then validate with adversarial test cases.
