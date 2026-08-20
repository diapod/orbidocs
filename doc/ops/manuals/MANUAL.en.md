---
render_macros: true
---

# Operator's Manuals

An operator's manual is the **reference document for a component**. It explains
what the component does, how it works, and what it communicates with. It also
collects its data contracts, settings, limits, possible refusals, and durable
state.

Boundaries between the operational documentation families:

- **Manual** — component and contract reference. *What it is, how to configure
  it, and what data it exposes.*
- **Runbook** — incident procedure. *What to do when a specific
  situation occurs.*
- **[HOWTO](../howto/HOWTO.en.md)** — step-by-step guidance for a specific task.
- **[FAQ](../faq/FAQ.en.md)** — an answer to a question.

A manual **links** to a runbook instead of repeating the procedure.
Type names, configuration fields, routes, and error codes remain in their exact
`code` form. Explanatory prose uses plain language and introduces a technical
term on first use.

## Manual structure

The document heading contains the **component name**. The opening paragraph
briefly explains its role and points to the FAQ and HOWTO. The remaining
sections follow a fixed order:

1. Purpose and functions
2. How it works
3. Architectural placement and communication channels (with a justification per channel)
4. Data contracts — schemas, purpose of use, channel of flow
5. Limits and behaviour when exceeded
6. Failure and status vocabularies (code, meaning, retryability)
7. Authority and its revocation
8. Trust boundaries — what the component verifies itself and what it accepts from the caller
9. Dependencies and degraded modes
10. Durable state and restart
11. Configuration — layer composition, sources, default values
12. Observability — status, traces, counters
13. Cost and resources
14. Contract versions and compatibility
15. Known limitations
16. Implementation references

Section 16 is mandatory. It names the implementation-ledger row, Rust crates,
schemas, capabilities, and routes associated with the component. This makes
drift between the manual and the code detectable. The rule lives in
[TRACEABILITY.md](../../../TRACEABILITY.md).

## Available manuals

{{ list_matching_pages("*-manual.en.md", page=page) }}
