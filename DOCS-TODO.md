# Docs Swipe Report — Orbiplex Documentation Audit

Date: `2026-04-30`

This report tracks only issues that remain open after the 2026-04-30
documentation sweep. Items that were fixed or confirmed as intentional have
been removed.

---

## 1. Missing Solution-Level Home

### 1.1 No dedicated `signer` solution doc

**Severity:** Low

The codebase has `signer-core`, `signer-service`, and `signer-http` crates with
substantial implementation behind proposal 037. There is no dedicated
`signer.md` or `signer-caps.edn` in `60-solutions/`.

Signer concerns are partially covered under capability-binding and the generic
signing-service parts of `000-node`, but a dedicated solution-level home would
make the implemented host capability easier to discover and track in the
capability matrix.

**Possible fix:** Add a new numbered solution directory for Signer, with a
short overview and caps sidecar derived from proposal 037 and the signer crates.

---

## 2. Schema Coverage Gaps

### 2.1 Middleware/internal schemas referenced by caps but not published under `doc/schemas/`

**Severity:** Medium

Several schemas are referenced in solution caps sidecars but do not currently
exist as formal JSON Schema files in `doc/schemas/`.

| Schema | Referenced In |
|---|---|
| `trusted-provider.v1` | 003-arca |
| `workflow-template.v1` | 003-arca |
| `workflow-dispatch.v1` | 003-arca |
| `workflow-envelope.schema.json` | 013-raw-signal-access |
| `json-e-flow-middleware.schema.json` | 013-raw-signal-access |
| `json-e-context-role-execute.schema.json` | 013-raw-signal-access |
| `middleware-init.schema.json` | 003-arca |
| `middleware-module-report.schema.json` | 003-arca, 013-raw-signal-access |
| `local-input-invoke.v1.schema.json` | 003-arca |
| `peer-message-invoke.v1` | 003-arca |

These are mostly middleware-internal contracts that exist in `node/` as Rust
types or local executor schemas. The open decision is whether all of them
should become public `orbidocs` schemas or remain node-local implementation
contracts rendered as plain names in the capability matrix.

**Possible fix:** Classify each missing schema as either:

- public protocol/schema contract -> add to `doc/schemas/`, sync to `node/`,
  add examples, and include in generated schema docs;
- node-local implementation contract -> keep out of `doc/schemas/` and
  document that caps sidecars may reference local contracts by name.

### 2.2 Schemas with zero examples

**Severity:** Low

Some schemas in `COVERAGE.md` still have no positive or negative example
fixtures. This weakens schema-regression coverage and makes generated schema
docs less useful.

Examples listed as zero-coverage in the previous sweep included:

- `capability-passport-revocation.v1`
- `capability-passport.v1`
- `key-delegation.v1`
- `command-stdio-executor-config`
- `plain-comment.v1`
- `public-log-entry.v1`
- `resource-ref.v1`
- `sensorium-directive-outcome.v1`
- `sensorium-directive-result.v1`
- `sensorium-directive.v1`
- `sensorium-observation.v1`
- `sensorium-os-error-codes.v1`
- `signal-transform-event.v1`

**Possible fix:** Add at least one accepted fixture and one intentionally
invalid fixture for each public schema that is part of an active or near-term
runtime surface.

---

## 3. Summary

| Priority | Count | Key Items |
|---|---:|---|
| **Medium** | 1 | Decide and document whether middleware/internal contracts should become public `doc/schemas` schemas |
| **Low** | 2 | Add a dedicated Signer solution doc; add missing schema examples |

**Total open issues: 3.**
