# AGENTS.md

## 1. Purpose

This repository contains foundational, strategic, and architectural documentation for
the **Orbiplex** system and protocols, under the **Distributed Intelligence Agency**
umbrella.

Orbiplex explores a federated swarm of AI nodes and orchestrators that can cooperate
across organizations, domains, and infrastructures to support open access to
knowledge.

Identity baseline:

1. Organization: **Distributed Intelligence Agency**
2. System and protocol brand: **Orbiplex**
3. Public website: `https://docs.orbiplex.ai/`
4. GitHub organization: `https://github.com/orgs/diapod/`

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
5. Do not write local absolute user-home paths into documentation or source-like
   text files. Prefer repository-relative paths, or, when a repository locator
   is clearer, `github.com/diapod/...` forms or optionally in short-forms like:
   `orbidocs:...` (when referring orbidocs) or `node:...` (when referring node
   component). This is checked in CI.

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

Use the stratified `doc/` tree as the canonical source:

- `doc/normative/` for the normative workflow.
- `doc/project/` for the project workflow.
- `doc/schemas/` for canonical machine-readable contracts.
- `doc/schemas-gen/` for generated human-facing schema pages.

For data shapes that express keys of associative structures, prefer Lisp-style
namespaced keys of the form `namespace/name` when semantic grouping or collision
avoidance is needed. The `namespace` part may contain dots to group meanings
from general to specific; the `name` part is the local key name. Do not force
dotted namespaces where the surrounding schema already disambiguates the keys
without conflict. Small, agile on-wire structures may omit the namespace part
entirely when the contract remains clear.

Normative workflow positions:
- `doc/normative/10-ideas/`
- `doc/normative/20-vision/`
- `doc/normative/30-core-values/`
- `doc/normative/40-constitution/`
- `doc/normative/50-constitutional-ops/`

Supplementary normative material outside the main workflow:
- `doc/normative/90-supplementary/`

Project workflow positions:
- `doc/project/10-challenges/`
- `doc/project/20-memos/`
- `doc/project/30-stories/`
- `doc/project/40-proposals/`
- `doc/project/50-requirements/`
- `doc/project/60-solutions/`

Under `doc/project/60-solutions/`, keep human-facing component pages in Markdown
(for example `node.md`, `node-ui.md`, `ferment.md`) and structured capability
catalogs in sidecar `*-caps.edn` files.

Treat `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md` and
`doc/project/60-solutions/CAPABILITY-REGISTRY.pl.md` as human-maintained read
models of stable `capability_id` semantics. Update them when capability ids,
wire names, semantic role boundaries, or primary runtime ownership change in:

- `node:capability/src/lib.rs`
- `doc/project/60-solutions/node.md`
- attached-role or capability proposals

Before considering a capability-registry edit done, run:
- `make check-capability-registry`

This checker compares the registry tables against
`../node/capability/src/lib.rs` and is the mechanical guard for
`capability_id -> wire name` drift. It does not replace semantic review.

For the sibling `node` repository, the implementation-side counterpart is
`../node/docs/implementation-ledger.toml` (assuming that node repository is cloned
into a sibling directory): it is maintained manually there from the `orbidocs`
solutions and schema layers plus selected implementation-relevant project documents;
see `README.md` and `TRACEABILITY.md`.

Node-attached roles such as archivist, memarium provider, or sensorium provider may
be documented there as separate solution components even if they are operationally
attached to the Node. Do not assume that such roles must live inside one in-process
monolith.

For challenge/proposal linkage, keep traceability explicit:
- each proposal file should reference its source challenge(s) in the header (for
  example: `Based on: doc/project/10-challenges/001-licensing.md`);
- use aligned numbering where practical (for example:
  `doc/project/10-challenges/001-*.md` -> `doc/project/40-proposals/001-*.md`).

When both exist for the same topic, keep traceability explicit:
- each requirements file should reference its source story in the header (for
  example: `Based on: doc/project/30-stories/story-001.md`);
- use aligned numbering where practical (for example: `story-001.md` ->
  `requirements-001.md`).

Memos under `doc/project/20-memos/` are informal, short-lived notes (idea seeds,
observations, backlog items).
They do not need to follow the full document quality contract (section 4), but should:
- have a title heading,
- contain at least one actionable sentence,
- be promoted into a challenge, story, or proposal when they mature.

Do not add new top-level workflow folders casually. If a new workflow position or
domain is needed, justify it in the relevant ADR or README update.

Treat the following as generated artifacts rather than hand-edited source:
- `doc/schemas-gen/**`
- `doc/COVERAGE.md`
- `doc/project/60-solutions/CAPABILITY-MATRIX.en.md`
- `doc/project/60-solutions/CAPABILITY-MATRIX.pl.md`

When changing their source inputs or generators, regenerate them before
considering the change done.

By contrast, `CAPABILITY-REGISTRY.*.md` is not generated. It should stay concise,
manual, and in sync with the current capability surface rather than with every
incidental runtime detail.

## 9. Diagrams

Use Mermaid diagrams through Material for MkDocs when a diagram clarifies system
structure, message flow, state transitions, data relationships, or operational
boundaries. Prefer diagram source that remains reviewable as text.

Diagram ownership follows the document unless the diagram is intentionally shared
across multiple documents:

1. Use embedded Mermaid blocks for small, local explanatory diagrams. This is the
   default for short flowcharts, sequences, state diagrams, and ER sketches that
   explain one nearby paragraph or section.
2. Use sidecar diagram files next to the owning document when a diagram becomes
   large, frequently edited, or distracting inline. Prefer `*.mmd` or
   `*.mermaid` source files. For several diagrams owned by one document, use a
   local directory such as `sealer.diagrams/` next to `sealer.md`.
3. Use a central `doc/diagrams/` tree only for canonical cross-document diagrams:
   system maps, architectural strata, protocol flows, or diagrams referenced from
   more than one document. Do not use it as a dumping ground for local diagrams.

Examples:

- `doc/project/60-solutions/sealer.md` may embed a short dispatch sequence
  directly.
- Larger Sealer-owned diagrams should live beside it, e.g.
  `doc/project/60-solutions/sealer.diagrams/dispatch-gate.mmd`.
- Shared architecture diagrams may live under
  `doc/diagrams/architecture/host-capability-strata.mmd`.

For multilingual documents, keep diagram labels in stable system terminology
where practical and translate captions or surrounding explanation instead. If a
diagram must be language-specific, treat it as owned by that localized document
version.

## 10. Collaboration Rules for Agents

1. Make small, reviewable edits.
2. Preserve existing intent unless explicitly asked to reframe it.
3. Avoid silent rewrites of terminology; update glossary when terms change.
4. Flag contradictions across documents and propose reconciliation.
5. If confidence is below ~95% on intent, ask a focused clarification question.

## 11. Non-Goals

1. This repo is not a code monorepo for runtime services.
2. This repo is not marketing copy.
3. This repo should not contain secrets, credentials, or private operational data.

## 12. Definition of Done (for doc changes)

A change is done when:

1. It is internally consistent.
2. Claims are classified (fact/inference/speculation where needed).
3. Terminology is consistent with glossary.
4. Trade-offs and risks are explicit.
5. Next actions are concrete.

## 13. Core Values

Core values live under `doc/normative/30-core-values/`, with locale subdirectories
and locale infixes in filenames, e.g.,
`doc/normative/30-core-values/pl/CORE-VALUES.pl.md` and
`doc/normative/30-core-values/en/CORE-VALUES.en.md`.

When user asks to add a value you should find a best spot to place it within a
document's structure. Then, after a value is added, you should synchronize contents
of document contents across different language versions. When editing or generating
text use "machine quotation marks" (e.g., "" for opening and closing double-quote, '
for ampersand and so on). Dash-set parentheticals should use en-dash characters (–).

You are free to correct any obvious syntactical, grammatical and stylistical mistakes
in text.

If a core value proposed by user is actually a core value we already have defined but
formulated in a different way or seen from a sifferent angle (or extended with
details), you should ask user whether they really want to add a new value or
integrate the given description into existing one.

## 14. Values → Constitution: what gets reduced, what gets added, what gets synthesized

Moving from "values" to a "constitution" does two things at once: it reduces poetry
and adds machinery.

Values can be broad and inspirational; a constitution must be unambiguous,
enforceable, and robust against interpretation "to fit a desired outcome" – so some
meanings get compressed into a few "constitutional laws".

### What gets reduced (examples)

1. "Rhetoric and emotional bandwidth"  
   Values may carry an inspiring tone; a constitution keeps the semantic core and
   removes ornament.

2. "Ambiguity and multi-meaning"  
   A value can be intentionally layered; a constitution forces definitions: what it
   means operationally, what counts as a violation, and where the boundaries are.

3. "Aspirations without obligations"  
   Values say "we want"; a constitution says "must / must not" and adds a way to
   verify compliance.

### What gets added (examples)

1. "Hierarchy and conflict resolution"  
   A constitution adds priorities, tests (e.g., reversibility, proportionality,
   transparency), an exception procedure, and decision traces.

2. "Rights, duties, and processes"  
   "Swarm citizenship" appears: minimal rights and duties of a node, sanctions,
   appeals, and federation rules.

3. "Enforcement and audit mechanisms"  
   The constitution translates values into operations: an event log, policy-id,
   reason, expiry, modes, reputation, oracles, and auditability.

4. "Definitions and interfaces"  
   A constitution names the entities and contracts: node, oracle, prediction,
   federation, compliance mode, and privilege boundaries.

### Do values get synthesized? (examples)

A constitution acts like a compressor: it turns 20-30 values into 5–7 "articles",
while the rest becomes commentary, rationale, and examples.

In current shape, the natural syntheses may look like this:

1. "Dignity and safety" as a super-value  
   Combines: dignity, privacy-by-default, sovereignty, non-violence, representation
   of harmed parties, responsible autonomy.

2. "Trust through evidence"  
   Combines: verifiability, transparent agent behavior, contracts, explicit
   tradeoffs, anti-sectarian epistemic hygiene, ground truth via oracles.

3. "Pluralism with contracts"  
   Combines: multi-paradigm thinking, protected diversity within boundaries, dispute
   procedures, the right to exit, federation.

4. "Swarm intelligence as a process"  
   Combines: collaborative sensemaking, reflective adaptation, predictive
   accountability, trend and early-signal sensing, living/open systems, productive
   imagination.

5. "Gift economy resilient to abuse"  
   Combines: reciprocity without bookkeeping, reputation as safety, anti-gaming and
   Sybil resistance, token governance, token/credit classes.

### How to do it in practice without losing the richness of values?

- "Values" remain the meta-layer: why we do this and what we intend.

- The "constitution" is the law-layer: what is allowed, what is forbidden,
  how conflicts and exceptions are resolved.

- Between them, it helps to add a bridge: "Interpretations and examples" – constitutional commentary
  that shows typical cases and maps them to articles.
