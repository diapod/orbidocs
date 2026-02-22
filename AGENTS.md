# AGENTS.md

## 1. Purpose
This repository contains foundational, strategic, and architectural documentation for **Orbiplex**.

Orbiplex explores a federated swarm of AI nodes and orchestrators that can cooperate across organizations, domains, and infrastructures to support open access to knowledge.

## 2. Core Intent
When writing or updating docs, optimize for:

1. **Knowledge symmetry**: broad, fair access to capabilities and understanding.
2. **Federation over centralization**: avoid single-entity lock-in.
3. **Interoperability**: components should compose through explicit contracts.
4. **Auditability**: strategic and technical claims must be traceable.
5. **Human agency**: humans remain accountable for governance and outcomes.

## 3. Language and Tone
1. Write documentation in **English**.
2. Keep style precise, technical, and readable.
3. Prefer concrete statements over slogans.
4. Mark uncertainty explicitly (for example: `Assumption`, `Hypothesis`, `Speculation`).

## 4. Document Quality Contract
Every substantial document should include, in this order:

1. **Executive Summary** (short, operationally useful)
2. **Context and Problem Statement**
3. **Proposed Model / Decision**
4. **Trade-offs** (benefits, risks, constraints)
5. **Failure Modes and Mitigations**
6. **Open Questions**
7. **Next Actions** (clear, testable)

If content is time-sensitive, include a concrete date in ISO format (for example `2026-02-21`).

## 5. Facts vs Interpretation
Keep a strict distinction:

1. **Fact**: verifiable statement with source or evidence.
2. **Inference**: reasoned conclusion from facts.
3. **Speculation**: plausible but unverified idea.

Do not present speculation as fact.

## 6. Architecture and Strategy Documentation Rules
1. Use explicit contracts (interfaces, protocols, responsibilities).
2. Prefer layered design: primitives -> services -> orchestration -> governance.
3. Document boundaries clearly (node, orchestrator, policy engine, human operator).
4. Describe expected invariants and what can break them.
5. Include at least one concrete scenario or sequence for non-trivial proposals.

## 7. Decision Records
For non-trivial strategic or architectural choices, create/update an ADR-style record with:

1. Title
2. Status
3. Date
4. Context
5. Options considered
6. Decision
7. Consequences (short- and long-term)

Do not remove superseded decisions; mark them as replaced and link forward.

## 8. Repository Conventions
Until a different structure is approved, use:

- `README.md` for project entry point.
- `docs/` for long-form architecture and strategy documentation.
- `docs/adr/` for architectural decision records.
- `docs/glossary.md` for core terms.
- `stories/` for scenario narratives (step-by-step user/node flows).
- `requirements/` for requirement specifications derived from stories.

When both exist for the same topic, keep traceability explicit:
- each requirements file should reference its source story in the header (for example: `Based on: stories/story-001.md`);
- use aligned numbering where practical (for example: `story-001.md` -> `requirements-001.md`).

When adding new top-level folders, justify them in the relevant ADR or README update.

## 9. Collaboration Rules for Agents
1. Make small, reviewable edits.
2. Preserve existing intent unless explicitly asked to reframe it.
3. Avoid silent rewrites of terminology; update glossary when terms change.
4. Flag contradictions across documents and propose reconciliation.
5. If confidence is below ~95% on intent, ask a focused clarification question.

## 10. Non-Goals
1. This repo is not a code monorepo for runtime services.
2. This repo is not marketing copy.
3. This repo should not contain secrets, credentials, or private operational data.

## 11. Definition of Done (for doc changes)
A change is done when:

1. It is internally consistent.
2. Claims are classified (fact/inference/speculation where needed).
3. Terminology is consistent with glossary.
4. Trade-offs and risks are explicit.
5. Next actions are concrete.
