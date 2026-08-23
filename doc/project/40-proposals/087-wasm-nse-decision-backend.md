# Proposal 087: WASM NSE Decision Backend

Based on:

- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`
- `doc/project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/048-operator-sovereign-extensibility/048-operator-sovereign-extensibility.md`
- `node:nse`
- `node:nse-table`
- `node:nse-rhai`

## Status

Draft; implementation-ready future work, non-blocking for P085 and hard-MVP.

## Date

2026-08-21

## Executive Summary

P085, now promoted to Solution 048, deliberately deferred its WASM Natural
Selection Engine backend until the
shared NSE contracts, table backend, refusal vocabulary, package lifecycle,
invalidation, inspection, and operational evidence were real. Those prerequisites
now exist. This proposal extracts historical tracker item `P085-017` into a
separate, implementable future workstream without making WASM part of P085 closure.

The WASM backend is a replaceable **decision producer**, not an authority source and
not a second policy engine. It receives one exact host-built `nse-hook-offer.v1`
value, executes a content-addressed module under deterministic and bounded host
controls, and returns one untrusted decision proposal. The existing hook-specific
validator in `nse` remains the only code allowed to construct an admitted decision.
No module can grant a capability, synthesize an offer, invoke an effect, access host
state, or reinterpret a refusal merely because its bytes are signed or executable.

The first reference profile uses a core WebAssembly module with no WASI and no host
imports. It has one closed byte-oriented ABI, fixed linear-memory bounds,
deterministic fuel, a wall-time emergency fence, bounded input and output, no
persistent guest instance, and no ambient filesystem, network, environment, clock,
randomness, process, thread, or device access. Package activation binds the exact
module, ABI, hook, execution profile, conformance report, operator authority, and
activation generation. Every use revalidates those facts before execution and again
before the returned proposal can enter ordinary NSE admission.

The implementation should use a mature embeddable Rust engine behind a private
adapter. Wasmtime is the initial reference choice because its resource limiter,
fuel, and interruption mechanisms match this profile. Engine identity and version
remain explicit evidence, not portable policy semantics, so another engine may be
added later only after passing the same golden vectors and adversarial matrix.

## Context and Problem Statement

P085 already provides two direct NSE producer classes:

- closed declarative tables for common reviewable policies;
- opt-in Rhai for local policies that exceed the table vocabulary.

Some operators and package authors will need a third form that is portable across
hosts, supports conventional compiled languages, and can execute code from less
trusted authors inside a materially narrower runtime than a native process. WASM is
useful for that purpose only when its embedding is intentionally small. Adding WASI,
ambient host functions, arbitrary imports, long-lived instances, or backend-owned
admission would recreate a general plugin runtime and undermine the authority model
P085 was designed to preserve.

The current accepted `operator-experiment-package.v1` contract also closes its
`backend` vocabulary to `table|rhai`. Silently adding `wasm` to that V1 enum would
change the meaning of an accepted schema. P087 therefore requires a versioned
package migration or a separately referenced producer contract, with explicit
mixed-version and conflict tests, before a WASM producer can be activated.

## Goals

- Make a portable WASM NSE producer implementable without changing NSE authority.
- Preserve one hook-owned admission path for table, Rhai, WASM, and future backends.
- Make module identity, provenance, ABI, engine profile, and limits explicit data.
- Reject ambient I/O and nondeterministic host facilities by construction.
- Bound compilation, instantiation, memory, tables, fuel, wall time, input, output,
  concurrency, cache occupancy, and retained diagnostics.
- Reuse P085 package activation, conformance, revocation, rollback, safe mode,
  restart recovery, refusal, and inspection mechanisms.
- Make exact replay and cross-engine conformance testable with shared golden vectors.
- Keep the reference implementation replaceable and outside contract-only `nse`.

## Non-Goals

- No WASI filesystem, sockets, HTTP, DNS, environment, arguments, stdio, clocks,
  randomness, subprocesses, devices, or inherited descriptors in V1.
- No general-purpose application plugin ABI.
- No stateful or continuously running WASM service.
- No module-originated capability, grant, effect, schema, offer, or admission.
- No direct calls from WASM into Inquirium, Agent, Corpus, Room, Sensorium, JSON-e,
  middleware, or daemon internals.
- No backend-specific semantic decision that bypasses a hook-owned validator.
- No automatic activation based on package-author signature or peer posture.
- No federation requirement that peers use the same WASM engine or machine code.
- No component-model or WASI dependency in the first profile merely for ecosystem
  convenience. A future revision may add one only as a separately admitted ABI.
- No requirement to implement P087 before P085 can close.

## Proposed Model / Decision

### 1. Authority Boundary

The authority chain remains:

```text
operator package activation
  -> exact WASM producer binding
  -> host-built NSE offer
  -> bounded WASM execution
  -> untrusted NseDecisionProposal<T>
  -> existing hook-specific NSE validator
  -> NseAdmittedDecision<T>
  -> ordinary owning-component admission and effect boundary
```

The WASM runtime can construct only serialized proposal bytes. It cannot construct
the opaque admitted Rust type. A module trap, malformed output, budget exhaustion,
missing producer, stale generation, or current-authority loss produces a typed
refusal; none selects a host default unless the owning hook contract explicitly
defines a pre-existing fallback outside the failed required producer.

### 2. Crate and Dependency Direction

The initial implementation adds one `nse-wasm` crate. It owns module admission,
the closed ABI, static validation, engine adaptation, execution limits, and
backend-specific diagnostics. It may depend on `nse`, canonical JSON, the selected
WASM engine, and a structural WASM parser. It must not depend on daemon, organ hosts,
HTTP clients, filesystem policy, package stores, databases, or capability dispatch.

`nse` remains contract-only and must not depend on `nse-wasm` or any WASM engine.
The daemon owns the thin adapter from an active package producer to `nse-wasm`, then
passes the returned proposal through the same `nse` composition and admission used
by table and Rhai producers.

Do not split an engine-neutral crate from an engine-specific crate in the first
slice. Keep the engine behind a private adapter inside `nse-wasm`; extract a second
crate only when a second real engine needs the interface. Add a dependency/source
guard proving that WASM dependencies cannot enter `nse`.

### 3. Versioned Package and Producer Contracts

P087 introduces these accepted contracts before runtime activation:

- `nse-wasm-module.v1`: module ref and digest, ABI id/version, supported hook ids and
  versions, required feature profile, and declared memory/table shape;
- `nse-wasm-execution-profile.v1`: distributor ceilings and operator narrowing for
  module bytes, compile time, memory, tables, fuel, wall time, input, output,
  concurrency, and compiled-cache occupancy;
- `nse-wasm-conformance-report.v1`: exact module/profile/engine identities, golden
  vector results, negative-matrix results, and terminal pass/refusal status.

The package integration must not mutate `operator-experiment-package.v1`. Prefer an
`operator-experiment-package.v2` hook registration that adds an exact WASM producer
descriptor while preserving V1 table/Rhai meanings. A separate sidecar contract is
acceptable only if V2 binds its ref and digest and conflict rules reject two producer
descriptions for one hook registration. Migration tests must cover V1 validity,
V2 WASM admission, V1/V2 conflict, unknown backend, missing module, changed digest,
and rollback to a prior non-WASM generation.

Module bytes are content-addressed package assets. The portable manifest carries no
host path, engine-native compiled artifact, live activation ref, operator binding,
or host identity. Native compiled code is rebuildable local cache data and is never
distributed as module authority.

### 4. Closed V1 ABI

The first ABI id is `orbiplex:nse-decision-producer@1`. It uses a core WebAssembly
module, not WASI or the Component Model. The module:

- imports nothing;
- exports exactly one non-shared linear memory with an explicit equal minimum and
  maximum;
- exports `nse_alloc_v1(i32) -> i32`;
- exports `nse_dealloc_v1(i32, i32)`;
- exports `nse_decide_v1(i32, i32) -> i64`;
- has no start function and no exported mutable global used as cross-call state.

The memory and these three functions are the complete export set. Unknown exports,
export aliases, and signature mismatches fail static admission.

The host writes canonical UTF-8 JSON bytes for the exact offer into guest memory.
`nse_decide_v1` returns a packed unsigned pointer/length pair: high 32 bits are the
output pointer and low 32 bits are the output length. The host validates pointer
arithmetic without wrapping, checks that the complete range belongs to guest memory,
applies the output cap before copying, copies bytes once, requires UTF-8, parses the
closed proposal contract, and then discards the instance.

Both input and output are existing schema-gated NSE values. ABI bytes do not become
a new semantic contract. A future ABI uses a new id and conformance corpus; it never
changes `@1` in place.

### 5. Deterministic and Bounded Execution

The V1 reference profile uses all of these controls together:

1. Static validation rejects imports, WASI, start functions, shared memory, threads,
   atomics, reference types not required by the ABI, floating-point instructions,
   SIMD, memory/table growth, and a memory whose minimum differs from its maximum.
2. Module byte size and compile time are bounded before activation. Compilation is
   a conformance/deferred operation, never unbounded work on the request path.
3. Every invocation creates a fresh store and instance from immutable compiled code.
   Guest memory and globals never carry state between offers.
4. Deterministic fuel is the primary CPU budget. Out-of-fuel is a terminal producer
   timeout/budget refusal for that invocation.
5. Wall time is an independent emergency fence against engine or host defects. It
   may interrupt at a nondeterministic instruction boundary, so it is evidence of
   refusal rather than a reproducible semantic result.
6. A store-local resource limiter caps linear memory, tables, instances, and related
   engine resources. Host-side allocations and compiled-cache bytes are measured
   separately because a guest-memory limiter does not cover them.
7. Effective input, output, and timeout limits are the minimum of the existing
   host-built offer bounds, the activated execution profile, and compile-time safety
   ceilings. An operator can narrow but never widen distributor or host ceilings.
8. Concurrency is acquired before instantiation. Queue depth is bounded; overload
   refuses before module execution rather than waiting without a budget.

Initial laptop defaults should be conservative and configuration-backed: one
concurrent invocation, queue depth eight, 16 MiB fixed guest memory, 1,000,000 fuel,
250 ms wall time, 1 MiB input, 64 KiB output, 1 MiB module bytes, and 64 compiled
cache entries. Compile-time hard ceilings must be at least as strict as the host's
safe allocation envelope. Measured acceptance evidence may later justify changing
distribution defaults without changing the ABI.

### 6. Lifecycle, Cache, and Current-Use Fencing

Installation is inert. Conformance and activation reuse P085 rather than introducing
a WASM-local package manager or authority store. Activation requires:

- current package and module digests;
- current trusted signing provenance;
- exact ABI and execution-profile digests;
- exact hook ids and versions;
- passing conformance for the current engine build and feature profile;
- current operator binding and activation generation;
- compatibility with host OS, architecture, and engine capabilities;
- no safe mode, revocation, supersession, expiry, or sanction.

The compiled-module cache is bounded and keyed by module digest, ABI id, engine id,
engine version, target architecture, deterministic feature profile, and execution-
profile digest. Cache entries are rebuildable mechanics, not authority. Every use
rechecks the current package producer and activation generation before execution and
again before proposal admission. Revocation, rollback, safe mode, trust loss,
conformance loss, or engine-profile change makes old cache entries unreachable
immediately; asynchronous deletion is only storage cleanup.

Restart discards live stores, instances, queues, and execution claims. Durable
package facts recover through P085. Compiled code may be reused after restart only
after its complete cache key and current producer authority are revalidated.

### 7. Refusals, Audit, and Inspection

WASM failures map into the existing closed producer refusal classes wherever the
meaning is already exact:

- fuel or wall-time exhaustion -> `producer/timeout`;
- trap or engine termination -> `producer/crash`;
- invalid UTF-8, pointer range, output size, JSON, schema, or proposal shape ->
  `producer/output-malformed`;
- missing/stale/revoked producer or activation -> `producer/required-failed` or the
  more specific existing lifecycle refusal;
- unavailable aggregate bounds -> `producer/budget-unavailable`.

If static module admission or ABI incompatibility cannot be represented honestly by
an existing code, extend the refusal contract in a new version and add one distinct
reaching fixture per new code. Do not overload `contract/unknown-schema` or retain a
dead code for convenience.

Prompt-free traces may contain module, package, producer, ABI, profile, engine,
activation, offer, invocation, decision, and refusal refs/digests; fuel consumed;
elapsed time; input/output byte counts; cache hit/miss; and trap class. They must not
contain offer payloads, decision payloads, module bytes, guest memory, stack traces,
host paths, secrets, or arbitrary engine error strings. Detailed developer traces
remain bounded local diagnostics under explicit capture policy.

### 8. Federation and Portability

A node may publish that it supports the P087 ABI and an exact semantic entry, but a
peer declaration does not activate a module locally. Federation binds portable
module and policy digests plus ABI and hook identities, not native compiled code or
engine internals. A receiving node applies its own trust, compatibility, operational
class, execution profile, conformance, and operator activation.

Peers need not use the same engine. Cross-engine equivalence is claimed only for a
module and profile that pass the same canonical golden vectors. A mismatch, unknown
ABI, unavailable feature profile, modified module, or revoked implementation refuses
without substituting a local table, Rhai script, or semantically similar module.

## Implementation Recommendations

1. Start with one hand-auditable WAT fixture and one small `no_std` Rust fixture.
   Do not begin with a third-party policy package.
2. Implement the parser/static-admission pass before adding the engine dependency.
   Golden tests should prove that every forbidden import, section, opcode, feature,
   memory shape, and export shape is rejected without compiling the module.
3. Keep the Wasmtime adapter private to `nse-wasm`. Expose a small function over
   immutable values rather than leaking `Engine`, `Store`, `Module`, or linker types
   into daemon or NSE contracts.
4. Construct an empty linker. Do not add WASI and do not provide logging, clock,
   random, configuration, artifact, schema, or callback imports in V1.
5. Use fuel for reproducible CPU bounding and a separate wall-time fence for host
   liveness. Record which fence fired; never treat wall-clock interruption as a
   deterministic decision.
6. Reject memory growth and allocate the fixed maximum before invocation where the
   engine permits it. Treat host allocation failure as refusal before guest code.
7. Compile only after package bytes, digest, ABI metadata, static shape, compatibility,
   and current conformance request have passed. Store no native cache entry before
   the content-addressed module identity is known.
8. Instantiate per invocation. Optimize compilation first; do not pool mutable guest
   instances until a future proposal defines a verifiable reset contract.
9. Reserve aggregate producer budget and concurrency before execution, then consume
   one-use offer authority using the existing NSE ordering. A failed module run must
   not turn the same offer into an implicit retry token.
10. Pass the output through the existing `NseDecisionProposal<T>` deserializer and hook
    validator. Never add `admit_*` functions to `nse-wasm`.
11. Reuse P085 conformance, activation, revocation, rollback, safe mode, inspection,
    deferred operation, and refusal-corpus stores. Every new store or cache must have
    a cap, owner, recovery rule, lifecycle, and operator-visible occupancy.
12. Add compile-fail and dependency-direction guards proving that `nse`, organ cores,
    and WASM modules cannot construct admitted decisions or import host authority.

## Security Invariants

- **INV-WASM-NO-NEW-AUTHORITY:** Module execution cannot create authority absent from
  the exact host offer, current producer activation, and owning hook validator.
- **INV-WASM-NO-AMBIENT-IO:** A V1 module has no imports and therefore no ambient host
  filesystem, network, environment, clock, randomness, process, device, or logging
  channel.
- **INV-WASM-EXACT-BYTES:** Package, activation, conformance, cache, invocation, and
  trace bind the same module digest and ABI id.
- **INV-WASM-BOUNDED-BEFORE-RUN:** Input, output, fuel, wall time, memory, tables,
  concurrency, and queue capacity are reserved or checked before guest execution.
- **INV-WASM-FRESH-INSTANCE:** No guest memory or mutable state survives from one
  offer to another in V1.
- **INV-WASM-VALIDATOR-UNIQUE:** Only the hook-owned `nse` validator can turn a WASM
  proposal into an admitted decision.
- **INV-WASM-REVOCATION-CURRENT:** Current authority is checked at execution and
  admission; cached compiled code never preserves revoked authority.
- **INV-WASM-NO-SEMANTIC-FALLBACK:** Failure cannot silently select a table, Rhai, or
  local module with similar meaning.
- **INV-WASM-PROMPT-FREE-AUDIT:** Durable traces expose bounded metadata, never policy
  inputs, outputs, module bytes, guest memory, or private reasoning.

## Trade-offs

### Benefits

- Portable compiled policies can use the same authority and validation model as
  existing table and Rhai producers.
- No-WASI, no-import execution gives the first profile a small audit surface.
- Fixed ABI bytes preserve the existing JSON contracts and avoid engine types in
  domain layers.
- Fresh instances and deterministic fuel make replay and resource behavior easier
  to reason about.
- Versioned package migration avoids silently changing accepted V1 semantics.

### Costs

- A WASM engine materially increases dependency, compile-time, binary-size, and
  vulnerability-maintenance surface.
- Rejecting floating point, growth, imports, and WASI limits source-language and
  library choices.
- Per-invocation instantiation costs more than pooling mutable instances.
- Cross-engine determinism requires a strict feature profile and golden vectors.
- Operator inspection must explain module, engine, profile, conformance, activation,
  and current-use fences without overwhelming the reader.

## Failure Modes and Mitigations

| Failure mode | Consequence | Mitigation |
| :--- | :--- | :--- |
| WASI or a convenience import is linked | ambient I/O becomes hidden authority | empty linker, import-free static validation, negative fixtures |
| Module loops or allocates excessively | daemon starvation or memory pressure | fuel, wall-time fence, fixed memory, resource limiter, bounded concurrency |
| Output pointer wraps or escapes memory | host memory-safety or parser confusion | checked arithmetic, full-range validation, cap before copy, fuzzing |
| Same module behaves differently across hosts | federation or replay divergence | closed feature profile, integer-only ABI, fixed memory, fuel, cross-engine vectors |
| Cached native code survives revocation | stale producer regains authority | current-use generation/digest checks; cache is never authority |
| Instance state leaks across offers | one caller influences another | fresh store and instance per invocation |
| Signed author module activates automatically | provenance is mistaken for operator trust | inert install plus current local activation and conformance |
| Engine error text enters durable trace | host paths or untrusted content leak | closed trap classes and bounded prompt-free projection |
| Package V1 is widened in place | accepted contract changes silently | package V2 or exact sidecar binding with migration/conflict tests |
| Required WASM producer fails and host falls back | policy intent is silently replaced | typed terminal refusal, no semantic fallback |

## Open Questions

No architecture-blocking question remains for the first slice. These operational
choices are intentionally deferred to implementation-time evidence:

1. **Exact Wasmtime release pin.** Default: choose one audited repository-wide
   version when implementation starts, record its feature set, and upgrade only with
   the full conformance and adversarial matrix.
2. **Second engine.** Default: do not add one until a real portability consumer exists;
   then require exact golden-vector parity before claiming compatibility.
3. **WASM Component Model.** Default: keep it outside V1. A future ABI proposal may
   adopt it without changing `orbiplex:nse-decision-producer@1`.

## Tracker

| ID | Work item | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- |
| `P087-001` | Freeze WASM module, execution-profile, and conformance contracts | `todo` | Three accepted schemas, positive and negative fixtures, canonical digest vectors, Schema Gate import/export coverage, and generated docs exist. |
| `P087-002` | Version experiment-package integration | `todo` | Package V1 remains unchanged; V2 or an exact V2-bound sidecar admits WASM producers and has migration, conflict, rollback, unknown-backend, and digest-substitution tests. |
| `P087-003` | Create the isolated `nse-wasm` crate and purity guards | `todo` | Dependency direction is `daemon -> nse-wasm -> nse`; `nse` has no WASM dependency; source/dependency guards fail on reversed ownership or ambient I/O dependencies. |
| `P087-004` | Implement static module admission | `todo` | Import, WASI, start, feature, opcode, export, memory, table, module-size, and ABI violations have distinct deterministic refusals before engine compilation. |
| `P087-005` | Implement bounded deterministic execution | `todo` | Fresh-instance execution enforces fuel, wall time, fixed memory, resource, input/output, concurrency, and queue bounds; pointer/range handling is fuzzed and fail-closed. |
| `P087-006` | Integrate package conformance and activation | `todo` | Module compilation is a bounded deferred conformance operation; inert install, current operator activation, safe mode, revocation, rollback, expiry, and restart reuse the P085 lifecycle. |
| `P087-007` | Integrate WASM as an NSE producer | `todo` | The daemon adapter returns only `NseDecisionProposal<T>`; all existing hook validators remain authoritative; required-producer failure has no semantic fallback. |
| `P087-008` | Add cache and current-use fencing | `todo` | A bounded compiled cache uses the complete engine/module/ABI/profile key; stale generation, trust loss, conformance loss, revocation, rollback, and engine change refuse before execution and admission. |
| `P087-009` | Extend refusal reachability and inspection | `todo` | Every new refusal code has one reaching fixture; inspection reports bounded module/engine/profile/resource/cache metadata without payloads, module bytes, paths, or raw trap strings. |
| `P087-010` | Add shared backend conformance vectors | `todo` | Table, Rhai, and WASM produce proposals admitted or refused identically for the same applicable hook vectors; Rust and guest fixtures agree on canonical bytes and digests. |
| `P087-011` | Complete the adversarial matrix | `todo` | Tests cover malformed module, forbidden import/opcode, oversized sections, compile bomb, infinite loop, fuel and wall timeout, memory pressure, invalid pointers, oversized/malformed output, trap, replay, stale generation, revocation race, cache substitution, restart, and no-fallback behavior. |
| `P087-012` | Run process and federation acceptance and synchronize docs | `todo` | A local process run and a three-node profile prove activation, decision, refusal, restart, rollback, revocation, exact peer posture binding, cross-engine vectors when applicable, prompt-free traces, and no local semantic fallback; ledger, P085, operator guides, and readiness are synchronized. |

## Next Actions

1. Keep this proposal unscheduled until an operator policy materially benefits from
   portability beyond table and Rhai.
2. When scheduled, implement `P087-001` through `P087-004` before adding executable
   engine dispatch to the daemon.
3. Do not enable a WASM producer until `P087-005`, `P087-006`, `P087-009`, and
   `P087-011` are green for the exact pinned engine profile.
4. Treat `P087-012` as the promotion gate for a future Solution; documentation or a
   compiling engine adapter alone is not sufficient.
