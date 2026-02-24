# AGENTS.md

## 1. Purpose

This repository contains foundational, strategic, and architectural documentation for the **Orbiplex** system and protocols, under the **Distributed Intelligence Agency** umbrella.

Orbiplex explores a federated swarm of AI nodes and orchestrators that can cooperate across organizations, domains, and infrastructures to support open access to knowledge.

Identity baseline:
1. Umbrella project / organization: **Distributed Intelligence Agency**
2. System and protocol brand: **Orbiplex**
3. Public website: `https://distributed-intelligence.agency/`
4. Contact email: `team@distributed-intelligence.agency`
5. GitHub organization: `https://github.com/orgs/diapod/`

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
- `challenges/` for challenge analyses and risk/problem framing.
- `proposals/` for ADR-style strategic and architectural proposals.
- `stories/` for scenario narratives (step-by-step user/node flows).
- `requirements/` for requirement specifications derived from stories.

For challenge/proposal linkage, keep traceability explicit:
- each proposal file should reference its source challenge(s) in the header (for example: `Based on: challenges/001-licensing-a.md`);
- use aligned numbering where practical (for example: `challenges/001-*.md` -> `proposals/001-*.md`).

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

## 12. Values

There is a directory called `core-values`. It contains files with infixes communicating
document's language, e.g., `CORE-VALUES.pl.md` is in Polish and `CORE-VALUES.en.md` is
in English.

When user asks to add a value you should find a best spot to place it within
a document's structure. Then, after a value is added, you should synchronize contents
of document contents across different language versions. When editing or generating text
use "machine quotation marks" (e.g., "" for opening and closing double-quote,
' for ampersand and so on). Dash-set parentheticals should use en-dash characters (–).

## 13. Values → Constitution: what gets reduced, what gets added, what gets synthesized

Moving from "values" to a "constitution" does two things at once:
it reduces poetry and adds machinery.

Values can be broad and inspirational; a constitution must be unambiguous, enforceable,
and robust against interpretation "to fit a desired outcome" – so some meanings
get compressed into a few "constitutional laws".

### What gets reduced (examples)

1. "Rhetoric and emotional bandwidth"  
   Values may carry an inspiring tone; a constitution keeps the semantic core and removes ornament.

2. "Ambiguity and multi-meaning"  
   A value can be intentionally layered; a constitution forces definitions: what it means operationally, what counts as a violation, and where the boundaries are.

3. "Aspirations without obligations"  
   Values say "we want"; a constitution says "must / must not" and adds a way to verify compliance.

### What gets added (examples)

1. "Hierarchy and conflict resolution"  
   A constitution adds priorities, tests (e.g., reversibility, proportionality, transparency), an exception procedure, and decision traces.

2. "Rights, duties, and processes"  
   "Swarm citizenship" appears: minimal rights and duties of a node, sanctions, appeals, and federation rules.

3. "Enforcement and audit mechanisms"  
   The constitution translates values into operations: an event log, policy-id, reason, expiry, modes, reputation, oracles, and auditability.

4. "Definitions and interfaces"  
   A constitution names the entities and contracts: node, oracle, prediction, federation, compliance mode, and privilege boundaries.

### Do values get synthesized? (examples)

A constitution acts like a compressor: it turns 20-30 values into 5–7 "articles",
while the rest becomes commentary, rationale, and examples.

In current shape, the natural syntheses may look like this:

1. "Dignity and safety" as a super-value  
   Combines: dignity, privacy-by-default, sovereignty, non-violence, representation of harmed parties, responsible autonomy.

2. "Trust through evidence"  
   Combines: verifiability, transparent agent behavior, contracts, explicit tradeoffs, anti-sectarian epistemic hygiene, ground truth via oracles.

3. "Pluralism with contracts"  
   Combines: multi-paradigm thinking, protected diversity within boundaries, dispute procedures, the right to exit, federation.

4. "Swarm intelligence as a process"  
   Combines: collaborative sensemaking, reflective adaptation, predictive accountability, trend and early-signal sensing, living/open systems, productive imagination.

5. "Gift economy resilient to abuse"  
   Combines: reciprocity without bookkeeping, reputation as safety, anti-gaming and Sybil resistance, token governance, token/credit classes.

### How to do it in practice without losing the richness of values?

- "Values" remain the meta-layer: why we do this and what we intend.

- The "constitution" is the law-layer: what is allowed, what is forbidden,
  how conflicts and exceptions are resolved.

- Between them, it helps to add a bridge: "Interpretations and examples" – constitutional commentary
  that shows typical cases and maps them to articles.
