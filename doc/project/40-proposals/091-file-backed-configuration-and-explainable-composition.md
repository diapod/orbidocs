# Proposal 091: File-backed Configuration and Explainable Composition

Based on:

- [Challenge 091: Predictable Operator Configuration](../10-challenges/091-predictable-operator-configuration.md)
- [Ontological Basis](../../normative/90-supplementary/en/ONTOLOGICAL-BASIS.en.md)
- [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md)
- [Vision](../../normative/20-vision/en/VISION.en.md)
- [Constitution](../../normative/40-constitution/en/CONSTITUTION.en.md)
- [Node](../60-solutions/000-node/000-node.md)
- [Node UI](../60-solutions/001-node-ui/001-node-ui.md)
- [Arca](../60-solutions/003-arca/003-arca.md)
- [Middleware](../60-solutions/019-middleware/019-middleware.md)
- [Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md)
- [Proposal 019: Supervised Local Middleware](019-supervised-local-http-json-middleware-executor.md)
- [Proposal 029: Workflow Template Catalog](029-workflow-template-catalog.md)
- [Proposal 033: Workflow Fan-Out and Temporal Orchestration](033-workflow-fan-out-and-temporal-orchestration.md)
- [Proposal 049: JSON-e Middleware](049-json-e-middleware-transformer-executor.md)
- [Proposal 071: Sensorium Workbench](071-sensorium-workbench.md)
- [Proposal 072: Capability Registry](072-capability-registry.md)
- [Proposal 080: Multiplexed Middleware Channel](080-multiplexed-middleware-channel-executor.md)
- [Proposal 085: Operator-Sovereign Extensibility](085-operator-sovereign-extensibility-and-experiment-packages.md)
- [Operator's Manuals](../../ops/manuals/MANUAL.en.md)
- `node:DEV-GUIDELINES.md`

Related: [Proposal 090: Inference Execution Provenance](090-inference-execution-provenance-and-non-local-disclosure.md).
Configuration explains selected behavior; P090 describes evidence about a realized
inference. Neither descriptor substitutes for the other.

## Status

Proposed. The operator requested this design direction on 2026-09-06. Existing
mechanisms below are antecedents, not evidence that this horizontal contract is
implemented. The dated audit is retained in Node. New schema and CLI names in
examples are design candidates, not
registered contracts or available commands. Implementation remains in the tracker.
The operator resolved OQ-01/02/03 on 2026-09-06 as A/A/B respectively, with a
component-name resolution contract and common-file fallback for OQ-03. These
adopted design choices do not change the proposal's implementation status. The
operator also selected retention of the existing middleware on/off implementation
behind the shared P091 control contract; P091-007a owns the wrapper and call-site
integration, not a replacement lifecycle engine. On 2026-09-25 the operator accepted
the bounded P091-002 contract freeze; see
[contract acceptance](#contract-acceptance-of-the-p091-002-freeze-2026-09-25). The
proposal as a whole remains proposed.

## Date

2026-09-06

## Executive Summary

Adopt the operator-facing rule:

> Every durable setting that controls Node behavior has an unambiguous key, a
> declaration in local configuration files, and explicit composition rules. GUI
> and CLI edit that same configuration. Every effective value can explain its
> sources, scope and derivation.

The objective is cognitive predictability, not the fewest settings. An operator
should know where to look even when a new module adds a new configurable behavior.
One interface must support global, module-instance and workflow-scoped settings,
without making their meanings or authority interchangeable.

This proposal adds a common configuration address space, source-aware resolution,
an inspectable change/apply lifecycle and shared CLI/GUI operations. It preserves
JSON files, small domain-owned contracts and current package boundaries. It does
not require a new configuration language, universal policy engine, or monolithic
configuration service before delivering a useful first slice.

The reuse audit sharpens this direction: extend the existing Rust JSON primitive
with source-aware configuration contracts, retain domain resolvers, and expose
the same values to Python through the existing host capability/channel boundary.
A shared programmer interface does not require two independent policy engines.
Process startup must also work before that bridge is ready, using an explicitly
bound configuration snapshot rather than a second live filesystem resolver.

## Context and Problem Statement

### Reuse baseline and design consequences

The dated Node Configuration Reuse Audit (`node:docs/audits/CONFIGURATION-REUSE-AUDIT.md`)
retains the 2026-09-06 source/workflow tables, errata and scoped evidence.
It was the input to P091-001a/001b; its 2026-09-21 addendum links the executable
inventory completion, which still is not runtime completion.

Reuse `json-utils` for mechanical JSON composition; keep domain interpretation
with existing resolvers. Separate daemon bootstrap/materialization and the raw
loader's retirement-policy check from the new read-only path. Python consumes the
same Rust-owned contract via P080/retained host bridges or explicit snapshots.
Workflow scope reuses definition/handler and executor-instance bindings; Arca
already provides a non-JSON-e-Flow case.

Preserve known legacy source-selection/error profiles, toggle precedence and
factory identity naming until explicit migration. Reuse sealed-registry CAS,
tri-state admission, bounded carriers, field-wise disclosure and temporal storage
as design idioms, not as interchangeable domain types. Decisions below own their
configuration meaning; later code-audit updates belong in Node.

### Affected documents and integration boundaries

This map identifies the configuration surfaces affected by P091, not new
implementation claims or dependencies on completing every linked proposal.
The linked solutions retain component ownership; each proposal links back to
the planned integration. First-slice and wider-inventory work remain distinct.

| Surface | Related proposals | Owning solutions | P091 impact / boundary |
| :--- | :--- | :--- | :--- |
| Host configuration and operator UI | [P052: Node UI desktop host](052-tauri-hosted-node-ui.md) | [S000: Node](../60-solutions/000-node/000-node.md), [S001: Node UI](../60-solutions/001-node-ui/001-node-ui.md) | Shared addresses, source resolution, predicted-value plans and apply receipts; P091-005/006/008. Desktop-specific durable settings join the wider inventory, not the initial four-case acceptance. |
| Supervised modules, Python clients and on/off | [P019: lifecycle antecedent](019-supervised-local-http-json-middleware-executor.md), [P020: bundled modules](020-bundled-python-middleware-modules.md), [P080: current channel executor](080-multiplexed-middleware-channel-executor.md) | [S019: Middleware](../60-solutions/019-middleware/019-middleware.md), [S004: Dator](../60-solutions/004-dator/004-dator.md) | Read-only acquisition, pre-channel snapshots, thin Python consumption and retained on/off wrapper; P091-003/005/007a/010/011. No revival of the retired supervised HTTP executor. |
| Workflow definitions, templates and parameters | [P029: template catalog](029-workflow-template-catalog.md), [P033: fan-out and temporal orchestration](033-workflow-fan-out-and-temporal-orchestration.md), [P049: JSON-e / Flow](049-json-e-middleware-transformer-executor.md) | [S003: Arca](../60-solutions/003-arca/003-arca.md), [S019: Middleware](../60-solutions/019-middleware/019-middleware.md) | Owner-bound durable declarations and source migration; P091-009a/009/010. Run state, template publication and orchestration semantics do not become configuration or a universal Flow language. |
| Separate-process configuration readers | [P035: Agora](035-agora-topic-addressed-record-relay.md), [P067: shared offer catalog](067-shared-offer-catalog-over-agora.md) | [S008: Agora](../60-solutions/008-agora/008-agora.md), [S033: Shared Offer Catalog](../60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md) | Inventory legacy selection/error profiles, consolidate readers and prove scoped consumption; P091-001a/001b/010a/011/015. No change to record, offer or relay authority. |
| Sensorium connector configuration | [P045: Sensorium](045-sensorium-local-enaction-stratum.md), [P048: OS connector](048-sensorium-os-connector-action-classes.md) | [S030: Sensorium](../60-solutions/030-sensorium/030-sensorium.md) | Wider module-local source/loader adoption in P091-001b/010a/015; observation/directive admission and signed action catalogs stay domain-owned. |
| Workbench configuration and sidecars | [P071: Workbench](071-sensorium-workbench.md) | [S042: Sensorium Workbench](../60-solutions/042-sensorium-workbench/042-sensorium-workbench.md) | Owner/stem resolution and signed-sidecar separation in P091-004/006/010/015; file edits cannot substitute for approval, revocation or actuation authority. |
| Inquirium profiles and adapters | [P063: Inquirium](063-inquirium-model-inquiry-organ.md), [P064: implementation guidance](064-inquirium-implementation-recommendations.md) | [S044: Inquirium](../60-solutions/044-inquirium/044-inquirium.md) | Existing profile derivations feed shared explanation/consumption; P091-004/011/014. Inference semantics and provider execution remain in their existing layers. |
| Extension descriptors and resource envelopes | [P085: operator-sovereign extensibility](085-operator-sovereign-extensibility-and-experiment-packages.md) | [S048: Operator-Sovereign Extensibility](../60-solutions/048-operator-sovereign-extensibility/048-operator-sovereign-extensibility.md) | Descriptor admission/withdrawal and existing limit algebra constrain composition; P091-002/004/006/014. File order is not signer authority or a replacement for an envelope. |
| Federation-derived runtime configuration | [P076: federation identity and selector](076-federation-identity-and-network-selector.md) | [S041: Federation Root](../60-solutions/041-federation-root/041-federation-root.md) | Preserve root-derived values as explicit domain derivations during inventory/resolution/migration; P091-001a/004/010/015. Root activation and authority remain separate, including restart-only application. |
| Discovery and API description | [P072: capability registry](072-capability-registry.md), [P068: API projection](068-api-surface-projection.md) | [S037: Capability Registry](../60-solutions/037-capability-registry/037-capability-registry.md), [S034: API Surface Projection](../60-solutions/034-api-surface-projection/034-api-surface-projection.md) | Register five operations with distinct read-dispatch/operator-control flags and project implemented routes/DTOs; P091-002/005a/015. Discoverability grants no authority and does not advertise unimplemented routes. |
| Commit/application history and recovery | [P062: temporal storage convention](062-temporal-storage-convention.md) | [S028: Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md) | P091-006/007 consume append-only facts and rebuildable projections; the file/journal ordering protocol is P091 work, not atomicity already supplied by S028. |

[P090: Inference Execution Provenance](090-inference-execution-provenance-and-non-local-disclosure.md)
is a related **reuse and semantic-boundary reference**, not a configuration
consumer changed by this proposal. Its carrier, projection, registry-CAS and
inventory idioms inform P091; configuration never proves realized locality or
egress. Likewise, the Corpus examples in the Node audit are precedents, not a
requirement to change Corpus or Room contracts for the first configuration slice.

P091-015 must extend this map and the reciprocal proposal links when later
adoption work identifies another concrete integration owner. Do not link
every domain merely because it has settings, or infer proposal-wide readiness
from a reference or a completed configuration fixture.

### Upstream intent and receiving-layer responsibility

User sovereignty, inspectability, explicit trade-offs and local-first operation
motivate this work. The Ontological Basis is a critical lens, not a deduction of a
particular directory layout. This proposal makes the engineering choice concrete:
operators can locate decisions, inspect their derivation and change them without
depending on one interface or memorizing hidden channels.

The receiving layer adds stable setting addresses, source and activation records,
and testable change semantics. It does not create authority or rewrite the
Constitution, operator-binding, consent, package-admission or revocation contracts.

## Identity and revision vocabulary

The following names are normative within P091. Do not use an unqualified
"generation" for different identities or derive one counter from another.

| Field | Identifies / owns change | Equality and fencing |
| :--- | :--- | :--- |
| `source-set/revision` | An immutable, context-selected source snapshot, including membership, selection rules, order, absent-target markers and content revisions | A canonical digest, not a counter; changes when any bound input changes. A relevant plan subset has its own explicit membership and revision. |
| `descriptor-set/generation` | Revision counter owned by one sealed, admitted descriptor-set artifact | Monotonic JSON-safe integer 1..9007199254740991, paired with `descriptor-set/ref` and `descriptor-set/digest`; expected-digest CAS, checked increment, exhaustion refuses. Never compare counters across different sets. |
| `resolution/id` | Immutable resolved view binding `source-set/revision`, exact descriptor-set identity, context, constraint snapshot and resolver/normalization revisions | Content-bound identity, not an activation counter; equal values alone do not imply equal resolutions. Retained evidence allows replay. |
| `activation/generation` | Durable, per-component-instance application sequence binding the selected `resolution/id` and consumption receipt | Owner-local monotonic JSON-safe counter with the same nonzero range; restart must not reset/reuse it. Pending attempts do not manufacture acknowledged consumption. |

`descriptor-set/generation` follows `InferenceProviderRegistry`'s sealed-artifact
CAS idiom, not a global allocator. Registry admission may reuse
`SemanticRegistryBinding.activation_generation` as an existing domain field;
that field is not P091's `activation/generation`. Source revisions and resolution
identities are not aliases for either counter. Host persistence serializes CAS;
a pure checked increment is not cross-process synchronization.

Exact digests belong to authorized internal bindings. Redacted exports may replace
sensitive identities with audience-scoped opaque handles; a public digest must not
become an oracle for low-entropy settings or secrets. Such a projection is not a
new editable source or an unredacted CAS credential.

## Proposed Model / Decisions

### 1. A setting has an address, not an incidental storage location

A durable behavioral setting is an operator- or user-declared value intended to
control future behavior until changed. Its address consists of:

- an admitted scope, such as node, module instance or workflow definition;
- a canonical key/path owned by the responsible component;
- the relevant definition or contract revision when meanings can evolve.

The physical file is an editable source for that address, not its identity. Use
JSON Pointer for exact tree selection, including escaping namespaced keys: the
literal key `classify/labels-max` occupies the segment `classify~1labels-max`.
Human aliases may exist, but must resolve to one address or report ambiguity.

Domain owners expose setting descriptors with type/schema, default source,
supported scopes, composition rule, validation owner, sensitivity, editable
targets, application mode and manual reference. Share the descriptor mechanism,
not a hard-coded closed list of all components, workflows or profile meanings.
Installed modules may contribute descriptors through host-admitted package data;
configuration cannot invent a new executable merge operation or authority root.

Known active settings reject misspelled keys and unsupported scopes. Uninstalled
or inactive module declarations may be retained as explicitly unvalidated source
material, but must not silently take effect or count as validated coverage.

Descriptor admission, source precedence and runtime consumption are independent.
Use `SemanticEntryHeader`/sealing and `SemanticEntryProvenance` as reference idioms
for descriptor origin, and the registry's explicit unresolved ceilings for
admission constraints. Distribution/operator-enabled inputs are concrete sets in
that precedent; not every axis is already tri-state. Configuration descriptors
specialize the header idiom as `CorpusThematicProfile` does, without importing
Corpus semantics or making the semantic registry a JSON value merger.

For example, uninstalling middleware may withdraw its descriptor while leaving
`50-<config_key>.json` unchanged. Then `descriptor-set/generation` changes and
`source-set/revision` can stay equal; the new `resolution/id` cannot reuse the
old validation result. Retain the old resolution for historical explanation.
Report `descriptor-invalidated` for an affected prior application binding;
re-evaluate current-use authority and the domain's stop/degrade rules before new
work. Neither retained bytes nor an old consumption acknowledgement re-admits the
descriptor. Withdrawal, replacement and re-admission require explicit host facts.

### 2. File-backed declarations are the source of durable behavioral intent

Ordinary durable settings must not exist only in a GUI database, browser storage,
process environment or service manager argument. GUI, CLI and text editing target
the same declared files. A database may index configuration, record transactions
or retain activation history; it must not become a competing hidden source of
ordinary configuration values.

Distinguish the following classes:

| Class | File-facing contract | Independent boundary |
| :--- | :--- | :--- |
| Ordinary durable setting | Editable declaration or inherited default with an editable target | Component validation and application policy |
| Secret | Configured reference to an approved secret source, not mandatory plaintext | Secret-store access and disclosure policy |
| Signed consent, resource envelope, passport or revocation | Inspectable reference/projection and an explicit admission operation | Existing signer, operator-binding, scope, expiry and revocation facts |
| Runtime observation, conversation, counter, result or lease | Read model linked where relevant, not an editable setting | Owning runtime/domain state machine |
| One execution's input or temporary narrowing | Explicit invocation/context source, not silently persisted as a global preference | Caller authority and domain limits |

A source file can request a policy or reference a signed artifact; editing it does
not manufacture approval. P071's approval ledger and derived sidecars retain their
roles. Deleting a projected file is not revocation, and restoring an old file is
not permission to restore an expired grant.

### 3. Preserve recognizable files and make source selection explicit

The initial compatibility baseline is the existing node configuration directory,
module-local configuration and admitted package fragments. Ordinary operator JSON
fragments already fit the existing loader; automatic target selection and the new
diagnostic/recovery contracts remain P091 work. The selected V1 layout preserves
existing workflow declarations and uses per-component operator fragments with a
common fallback (resolved OQ-02/OQ-03):

```text
<data-dir>/
  config/
    10-base.json
    50-<config_key>.json
    80-operator.json
    90-operator-<component-name>.json
  middleware/
    <module-id>/config/
  middleware-packages/
    <package-id>/config/
  storage/
    <configuration-owner-store>/
```

- Keep existing `10-base.json` and module fragments readable during migration.
- `90-operator-<component-name>.json` is the default for sparse interactive changes;
  `80-operator.json` is the fallback defined below. GUI and CLI share selection and
  display its reason. Files are created only on an authorized commit, not inspection.
- For the first JSON-e Flow case, use an existing instance entry in an
  operator fragment, addressed by its admitted identity and revision. For example,
  the inspected typed map is `middleware_json_e_flow_services`; its instance-local
  `limits` remain owned by the Flow contract. The host binds a workflow context to
  that entry; a filename or display label is not workflow identity or authority.
- The earlier `config/workflows/<workflow-file>.json` and `node-scoped-config.v1`
  sketch was not selected for V1. Reuse the declaring owner's current mechanism;
  this applies to other workflows too, not just JSON-e Flow (Decision 13).
- Package configuration remains read-only factory input. Runtime-home files must
  declare whether they are operator inputs or generated projections; a generated
  projection must never be reloaded as a new independent declaration.
- Follow Solution 028 for persistence. Commit intent/outcome and application facts
  use the existing storage/temporal-log boundary (logical streams such as
  `trace/config/commits/<target-ref>` and `fact/config/activation/<component-ref>`);
  active views are rebuildable projections. Stream refs use validated opaque
  bindings, not client paths. Do not create separate `control/config-transactions/`
  or `control/config-active/` semantic stores. The storage owner chooses the
  physical backend; ordinary readers create neither journals nor projections.
  Transaction-local staging beside a target file is not a second source tree.

Source discovery records explicit file bindings, order and content revisions.
Avoid arbitrary recursive includes or ambient searches through the home directory.
The initial loader preserves documented compatibility order, while reporting
legacy inputs and conflicts. New source kinds require bounded host-owned loaders.

Factory defaults must be inspectable by version and key, including defaults
compiled into domain types. A generated reference file/catalog is acceptable;
copying every default into active operator config is not required. Full expansion
is an explicit export/pinning operation, distinct from sparse materialization.

#### Component name and write-target resolution

Reuse the existing factory inventory and admitted runtime/descriptor ownership
bindings. In `identity_store.rs`, `middleware_seed_fragment_path` builds
`50-<config_key>.json`; `bundled_middleware_module_id` reads `module_id` with a
`config_key` fallback. `middleware_settings.rs` already correlates `config_key`,
executor and module identity with a component. Consolidate these lookups behind
one configuration-owner binding; do not derive identity from `module_name`, a
directory basename or the text of a runtime `component_id`.

There is also a domain-owned filename precedent:
`node:operator-storage/src/lib.rs` exposes
`operator_storage_profile_config_filename()` for
`90-operator-storage-profiles.json`, consumed by
`node:daemon/src/operator_storage_host.rs`. Preserve this explicit source binding;
the new default convention must not rename it or capture it for another owner.

For a validated setting address, select the target in this order:

1. Honor an explicitly selected, authorized source binding or an existing
   domain-owned write target. Do not accept an arbitrary client-supplied path.
2. Otherwise resolve exactly one configuration owner. For admitted middleware,
   reuse the existing `module_id`, or its existing `config_key` fallback when
   `module_id` is absent. A host-admitted explicit file stem may override filename
   presentation without changing that identity. Native components use an explicit
   owner binding rather than masquerading as middleware.
3. A filename stem must match `[a-z0-9]+(?:-[a-z0-9]+)*` and be at most 96 ASCII
   bytes. A matching resolved module identifier can be used unchanged. Do not
   lossy-normalize underscores, case, Unicode, slashes or dots into hyphens.
   A valid but non-filename-safe identity needs an admitted stem or the common
   fallback; an invalid explicit stem is an error, not a fallback trigger.
4. A subcomponent without its own admitted filename binding shares the owning
   component's file. Keep its exact key path and instance identity inside the
   declaration. A separate subcomponent stem needs an explicit unique binding;
   do not split `component/middleware/...`, dotted IDs or execution trace paths
   to invent hierarchy. Multiple instances may share one owner file while their
   declarations remain distinctly scoped.
5. When a known setting has no component-specific filename binding (for example
   a node-wide setting), select `80-operator.json` if it is an allowed target and
   report the fallback reason. Missing component files are created on commit;
   their absence alone does not trigger fallback. Unknown setting/owner, ambiguous
   ownership, reserved-name collision, path escape, permission denial or a failed
   write refuses; none redirects the write into the common file.

| Existing identity/source | Selected default or retained target |
| :--- | :--- |
| `config_key=arca`, `module_id=arca` | `90-operator-arca.json`, retaining the `arca` key |
| `config_key=sensorium_workbench`, `module_id=sensorium-workbench` | `90-operator-sensorium-workbench.json`, retaining the `sensorium_workbench` key |
| Subcomponent owned by `sensorium-workbench`, no separate file binding | The same Workbench file, with its own nested key/scope |
| Known node-wide setting without a component file binding | `80-operator.json`, with an explicit fallback reason |
| Existing operator-storage profile writer | Retain `90-operator-storage-profiles.json` through its domain-owned binding |

Validate uniqueness of owner/stem and reserved target bindings before admission.
Do not choose a winner by discovery order, auto-number a collision, or rename
existing `50-*.json` files. A changed owner/stem is an explicit source migration.
The common fallback file may hold several owners; authorization stays per setting,
not per filename. Group multi-owner patches by their selected targets and preview
each group; do not silently collapse them into the fallback to obtain one write.

Retain existing deterministic filename ordering: `80-operator.json` naturally
precedes `90-operator-<component-name>.json`. No special comparator, source-group
priority or new filename parser is needed. Specific ordinary values may override
common ones; neither prefix bypasses domain constraints or scoped authorization.
An existing `90-operator.json`, if present, remains an explicit legacy source until
an authorized migration previews its move/merge into `80-operator.json` and proves
the intended effective values. Do not maintain two fallback files or silently
discard a later legacy override. Other source classes retain their declared order;
explanations and source-set checks bind actual order and owner-mapping revisions.

Multiple sources may declare the same address: that is layering, not an ownership
error. For every affected address, `plan` must predict the effective value after
the proposed commit under the pinned resolution inputs. Editing `80-operator.json`
while `90-operator-arca.json` still wins yields an unchanged predicted value and
a derived `shadowed` diagnostic. An explicitly confirmed shadowed commit is
allowed; its receipt says no resolved-value change for those addresses, not
"applied". It does not assert equality with an already different active runtime.

Reset removes only the selected declaration. If the shared file becomes `{}`,
retain that empty object and its file permissions/identity; it contributes no
setting values. Removing the empty file is a separate authorized cleanup, not an
implicit side effect of reset or inspection.

### 4. Scope, precedence and authority are separate axes

Select sources for an exact context before composing their values. A typical
ordinary setting sees distribution/package defaults, applicable operator files,
and an admitted workflow overlay. File order is deterministic within each source
class; scope selection must not silently change source authority.

There is no universal rule that the most specific scope wins. A workflow may
replace an ordinary preference where allowed, but cannot widen a host safety
ceiling merely by being more specific. A module cannot replace another module's
namespace or an operator restriction through a late-sorting filename.

For every selected source retain its actual class: a copied factory value is not
proof of signed operator approval, and peer policy is not local operator policy.
Federation-root activation and other post-load domain transformations must remain
explicit derivations rather than being mislabeled as a file override.

Bootstrap needs a small exception: CLI/environment can locate the node data/config
root before those files can be read. Secret-source mechanisms are explicit too.
Every other legacy behavioral CLI/environment input receives an inventory entry,
a canonical setting address and a migration path. Do not add new environment-only
behavioral settings. Existing invocation overrides remain visible as ephemeral
sources until migrated; they never silently write themselves into durable intent.
An active diagnostic snapshot records their non-secret contribution so online
inspection can explain behavior which offline file inspection alone cannot know.

Authority context must be supplied by its admitting owner and pinned explicitly;
file presence, a package name or a copied factory value is not that context.
`CorpusReasoningAnswerV2::bind_unknown` is an analogous boundary rule: it requires
an explicit owner-supplied processing boundary instead of inferring it from the
respondent. P091 reuses this discipline, not Corpus's inference DTO.

### 5. Composition is deterministic and remembers its derivation

Separate source acquisition from a pure operation of the following shape:

```text
resolve(retained_inputs, detail = values-only | with-derivation)
  -> resolution + diagnostics + optional derivation_index
read(resolution_id, admitted_address) -> immutable value_or_refusal
explain(resolution_id, admitted_selection, projection) -> bounded explanation
```

The pure resolver performs no filesystem, network, secret-store, process or
activation I/O. Host adapters acquire and authorize bounded snapshots; existing
domain resolvers own policy meaning and current-use revalidation.

Default composition rules:

| Value/contract | Rule |
| :--- | :--- |
| Ordinary object | Recursively compose declared keys |
| Ordinary scalar or array | Later applicable source replaces the earlier value |
| Identified collection | Domain-declared replacement, keyed composition or append-only rule; never guessed from JSON shape |
| Safety limit or permission set | Domain-owned `min`, `max`, intersection or another registered relation |
| Signed approval/profile | Existing admission, revision, validity and domain composition rules |
| Incompatible values or unsupported operation | Typed refusal, not silent coercion or arbitrary selection |

Omission means inherit. An explicit value remains an explicit declaration even
when equal to today's default; this does not falsely claim that it narrowed a
P085 limit. `null` retains schema-defined meaning and is not a universal delete
operator. Removing a declaration from a chosen writable source restores
inheritance from that source; it does not remove another source's constraint.
If a domain supports tombstones, they are a separately declared operation.

Separate retention from materialization. Before a resolution can be provisioned
or acknowledged, retain bounded replay inputs: selected source values/revisions,
the exact descriptor artifacts and admission context, constraints, scope,
resolver/domain-port versions, and normalization inputs/record. Secret values
are not copied into public history; retain protected evidence or explicitly mark
a historical explanation unavailable when it can no longer be reconstructed.

The startup `values-only` path need not construct contributor lists. A later
explanation deterministically replays these pinned inputs and lazily builds an
index by JSON Pointer, never reconstructing provenance from the final JSON or
today's files/descriptors. A merge/normalization log captured during resolution
is valid source evidence. The indexed view, not an unstructured event list, is
the query contract. Cache it in memory; authorized host materialization may persist
a rebuildable artifact keyed by `resolution/id`. Ordinary inspection still writes
nothing. Both modes must return identical values and validation/refusal decisions.

A subtree has per-pointer contributors, not one guessed owner. Preserve decisive,
equal, shadowed and rejected inputs where needed to explain intersections,
replacement of arrays/ancestors, empty objects and domain-derived paths. Do not
promise one winner for an intersection, or allocate only for declared leaves
while losing implicit defaults, structural replacement or derived values.

### 6. Declared, resolved, active and observed are distinct

| View | Meaning |
| :--- | :--- |
| `declared` | Exact declarations in selected source revisions, with validation status |
| `resolved` | Candidate values validated for the pinned inputs of one `resolution/id` |
| `active` | Resolution acknowledged as consumed by the owning component instance, bound to `activation/generation` |
| Runtime observation | What happened during an operation; linked separately, never inferred from a save |

Use separate closed, kebab-case types for application state and operation refusal.
`ConfigApplicationState` contains `provisioned`, `active`, `pending-reload`,
`pending-restart`, `approval-required`, `application-rejected`,
`descriptor-invalidated` and `unknown`. A reason code and owner binding accompany
every non-active result. `ConfigRefusal` is an operation failure, not one of these
states: `missing-key`, `denied`, `unavailable-context`, `host-unavailable`,
`unsupported-contract`, `invalid-source`, `source-conflict`,
`descriptor-conflict`, `constraint-conflict`, `resolution-unavailable`,
`invalid-target`, `limit-exceeded`, `persistence-failed` or
`recovery-required`. Refusal detail codes are versioned and bounded, not raw
error text. Serialization uses `#[serde(rename_all = "kebab-case")]`.

`provisioned` means the host delivered the named resolution but has no consumption
acknowledgement. It must not be reported as `active` or collapsed into an
unexplained `unknown`. Component unavailability is a separate observation;
retain a last-known acknowledgement with freshness rather than claiming current
liveness. An apply failure preserves any prior acknowledgement and reports the
failed target separately. Descriptor withdrawal invalidates current admission,
not the historical fact that an older resolution was consumed.

P091-002 freezes a table-driven transition/receipt contract: provision precedes
acknowledgement, pending/approval states do not imply delivery, refusal is not
activation, and descriptor invalidation prevents automatic re-admission. An active
query uses retained inputs for the acknowledged `resolution/id`, not current files.
Multi-component queries return per-instance `activation/generation` and mismatch;
there is no invented atomically active whole-node counter.

#### Historical replay does not renew time-limited authority

Replay evaluates the retained inputs at their recorded validation time. It may
correctly reproduce a historical admission that is no longer usable. Keep that
preimage and `resolution/id` unchanged; current-use admission is a separate
evaluation bound to that resolution, phase, current constraint evidence and a
fresh host-owned time context. Record its `evaluated/at`, outcome and evidence
refs separately, not as a replacement historical verdict.

`commit` rechecks the plan's commit deadline and applicable authority windows.
Every `apply`, including queued dispatch, restart recovery and retry, rechecks
time-dependent authority/constraints immediately before applying behavior. A
commit receipt or provisioned snapshot is not a lease extending their validity.
Use the owning domain's interval semantics (an exclusive `valid/until` refuses
at or after its boundary); client-supplied replay time cannot establish current
validity. Unavailable/unreliable time evidence refuses as `unavailable-context`
with `time-context-unavailable`, rather than assuming the recorded time is current.

Expired constraints return `ConfigRefusal::ConstraintConflict` (wire
`constraint-conflict`) with reason `constraint-expired`; a not-yet-valid window
uses `constraint-not-yet-valid`. The attempted application is
`application-rejected`, with that reason and no new consumption acknowledgement.
Preserve the durable save and any prior historical acknowledgement. Renewal or
fallback that changes resolved values or admitted inputs requires a fresh
resolution and applicable approval, not silent recomposition during `apply`.
No additional application-state variant is needed for expiry.

Retain `config-time-expiry-between-phases`: plan at T under an envelope valid
until T+1h, commit at T+50m, apply at T+70m must refuse without lifecycle effects,
while historical replay still reproduces the original verdict. Controlled-clock
fixtures also cover pre-commit expiry, the exact expiry boundary, not-yet-valid
constraints, unavailable current time, and expiry during queued/recovered apply.

In-flight work retains its admitted binding, subject to expiry, immediate
revocation and safety checks. Replay cannot bypass current-use authority or
rewrite operation evidence. P090 locality and egress observations cannot be
inferred from an active configuration. Atomic activation groups require a
separate owner/protocol.

### 7. Explain any key or subtree through one read contract

The proposed CLI spelling is illustrative:

```sh
orbiplex-node-daemon explain-config /inquirium/resource_profile --workflow research --view resolved
orbiplex-node-daemon explain-config /inquirium/resource_profile --workflow research --view active --format json
```

The same bounded host read contract serves CLI and GUI. An explanation includes:

- exact address, context and requested view;
- value or explicit unavailable/redacted status;
- source ref, source class, revision/digest, file and JSON Pointer where applicable;
- the per-key derivation rule and participating, shadowed or rejected declarations;
- descriptor and resolver revision, and the bound constraint context;
- requested `resolution/id`, acknowledged `resolution/id`, per-instance
  `activation/generation` and application status;
- writable targets, permission/approval requirements and a manual reference.

Read access is scoped independently of edit access. The host checks the caller
and requested scope before acquiring sources; a key query must not become an
arbitrary-file reader or reveal another participant's private configuration.
An unavailable workflow, hidden source or denied scope produces a bounded refusal
without leaking its contents. Source paths are resolved only through admitted
bindings and confined loaders, not directly from a caller-supplied path string.

For example, a hypothetical `classify/labels-max` value of 8 can explain
`min(distribution: 32, node: 16, workflow: 8)`. Another key in the same queried map
may inherit only its distribution value. An equal-valued declaration remains
visible without changing the existing domain resolver's narrowing semantics.

Offline `declared`/`resolved` inspection reads the selected files and available
versioned descriptors without starting middleware, fetching remote packages,
materializing defaults or retrieving secret values. Missing authority/context
produces an explicit unresolved constraint, not an optimistic approximation.
For package-supplied descriptors, offline validation is explicitly unresolved
unless a pinned export supplies the admitted descriptor set and its owner-issued
admission/constraint context. Use the semantics of
`SemanticRegistryCeiling::Unresolved`, never infer admission from installed files.
A historical export proves only resolution at that bound context, not current
package approval, revocation status or permission to execute.
Offline inspection does not claim `active`; a retained acknowledgement is shown
only as last-known with its `resolution/id`, `activation/generation` and freshness.
Authenticated CLI-to-host transport is compatible with read-only online
inspection; the prohibition concerns implicit source fetching and producer I/O,
not transport of the inspection request itself.

Separate a local diagnostic projection from a redacted export using per-field
`Retain | Redact` choices for values, source identities, paths and secret refs.
These choices request disclosure; they do not grant it. Redaction must not turn
an unresolved/refused result into an apparently validated one. Secret values must
not leak through losing declarations, diffs, diagnostics, hashes or error text.
Use opaque secret refs/revisions, not public hashes of low-entropy secret values.
Absolute local paths may be shown in authorized local inspection, but are not
written into committed documentation or portable/durable audit exports.
Bound source count, bytes, depth, derivation fan-out, subtree size, output size and
history retention. At a fan-out bound, require an authorized aggregate reference
or return `limit-exceeded` with a conservative summary; never silently drop a
constraint, refusal or contributor. Details may be unavailable, not falsely
complete. Compose diagnostic summaries through an explicit conservative decision
table (admit/warn/deny idiom), keeping reasons distinct.

### 8. GUI, CLI and file editing share the change semantics

GUI/CLI submit a source-targeted patch, expected `source-set/revision`, pinned
descriptor-set identity and constraint context, and intended application mode.
The host:

1. checks caller authority, target ownership and path confinement before acquisition;
2. acquires bounded inputs and binds the plan to a base `resolution/id`;
3. patches the declaration, not the expanded effective tree;
4. resolves/validates the candidate through the same domain ports as inspection;
5. returns the source diff **and predicted effective values for every affected
   address**, including derived dependents, with shadowing, impact and approvals;
6. rechecks all plan preconditions, the commit deadline and current authority
   windows under writer coordination;
7. persists intent, atomically replaces the target, records durable outcome, then
   separately requests and records application with Decision 6's fresh time gate.

"Relevant source set" means every input that contributes to, or could shadow,
a touched address or its dependent result: ancestor/object/array replacements,
defaults, ephemeral overrides, and membership/order/selection rules too. Bind
directory/source-selection membership so a newly appearing fragment conflicts
even if no formerly selected file changed. If a domain cannot safely narrow this
dependency closure, bind the full selected set. Descriptor-set and constraint
preconditions are separate: unchanged source bytes do not preserve validation
after withdrawal. Any changed bound input requires a new plan; diagnostics name
the changed class without leaking unauthorized data.

A narrowed source precondition must not authorize activating stale, untouched
values from a broader old resolution. Bind the complete application unit's inputs
when that unit is replaced; otherwise require its owner's explicit scoped-apply
contract. V1 may conservatively use the full selected set.

Keep `source-conflict` as the refusal family, with a closed, bounded reason:
`affected-input-changed`, `unrelated-source-content-changed`, or
`source-change-unclassified`. The second reason requires host proof that only
content outside the affected dependency closure changed, with source selection,
order, descriptor bindings and constraints unchanged. An ancestor replacement or
an unknown dependency is not an unrelated edit. Classify from retained/current
inputs, not merely the final value; disclose no unauthorized paths or values.

For example, an edit of owner A's independent address in `80-operator.json` can
invalidate owner B's plan through whole-file fencing. The host may identify that
as unrelated; it still refuses the stale commit. A client may request a bounded
automatic **replan** preserving B's exact patch and target, but receives a new plan
with fresh preconditions and predicted values. This is not permission to reuse
the stale plan, silently commit/apply, or transfer its approval. Existing explicit
automation authority must independently cover any subsequent write. If safe
classification or disclosure is unavailable, use `source-change-unclassified`.

Host seeding, including `middleware_seed_fragment_path` writes, participates in
the same serialization protocol. Bootstrap materialization and pending recovery
finish before operator commits are admitted; later seed/package source updates
take the same host lock and invalidate affected plans. Reads never seed. Manual
non-cooperating writers remain a documented filesystem limitation, not an excuse
to omit coordination between the host's own writers.

GUI must expose the affected key and file, allow authorized target selection, and
support explicit inheritance restoration. A later source that shadows the write
must be derived and reported before saving; a saved-but-shadowed change is not
an applied value. Commit may accept that explicit plan, with a receipt indicating
no resolved-value change for the affected addresses. Redacted callers receive
authorized projections of predictions, not leaked secret values or fingerprints. Persist only requested deltas, preserving unrelated declarations.

Manual editing remains a first-class path. A read/validate/apply operation sees
file edits through the same loader and validators without requiring GUI state.
For pre-existing or externally edited files, startup/explicit apply records an
admitted durable source snapshot and its `resolution/id`, not a fictitious GUI
commit or retroactive intent. This observed-source admission is separate from
the intent/replace/outcome protocol for P091-owned writes; both feed the same
application boundary. File access does not bypass approval of activation. Simultaneous
GUI/CLI edits use conflict detection rather than silent last-writer wins. External
editors should participate in the documented lock/edit protocol; do not claim
atomic compare-and-swap against arbitrary non-cooperating filesystem writers.

Successful configuration commit does not automatically authorize a separate
external effect. Reload, restart, signed approval and irreversible operations
retain their own contracts. Partial activation or an unavailable component is
reported and reconciled, not disguised as successful whole-node application.

#### Existing middleware on/off remains behind the shared interface

Retain the existing middleware on/off implementation. P091 adds a thin host-owned
wrapper around its settings and application operations, not another supervisor
or a second implementation of toggle semantics. This follows P019's component
control boundary and P080's dependency-aware lifecycle contract.

The shared P091 contract becomes the single programmatic control path for durable
`enabled` changes: GUI, CLI and retained middleware-settings endpoints use the
same source selection, validation, commit and application accounting. Existing
entry points remain compatibility adapters; they must not retain an independent
writer that bypasses the shared contract. Manual file edits remain first-class
declarations consumed through the same resolution and explicit apply path.
One control contract does not mean one physical configuration file.

Keep toggle eligibility, protected-component checks and runtime application with
their existing host/domain owners. Preserve dependency ordering, bounded shutdown,
`operator_stopped`, readiness and current authority checks. Operational start,
stop and restart remain distinct from changing durable `enabled`; the wrapper
must not silently persist those commands as configuration. A successful save is
not proof that the component is running or ready, and a shadowed requested value
must not be applied as though it were the resolved configuration.

The current `control/middleware-settings.json` may remain an explicitly declared
legacy source behind the wrapper until Decision 9's migration. Preserving the
implementation does not freeze its hard-coded file target or mutating read path:
small extractions and call-site changes are required to join the shared contract.
Do not create a permanent mirror between that file and operator fragments.

### 9. Compatibility and migration preserve intent

Migration is an explicit operation with a source inventory, preview, recoverable
backup, exact before/after resolution comparison and post-restart verification.
No automatic migration runs as a side effect of `explain-config` or validation.

The initial migration must handle:

- middleware toggle files, naming drift and their current precedence;
- factory seeding, generated runtime sections and copied defaults;
- module-local versus node-wide loading, including Python consumers;
- legacy file-selection behavior and filename ordering;
- standalone Node UI arguments and non-bootstrap environment/CLI settings;
- existing signed artifacts and domain-specific sidecar projections.

Do not guess whether an old materialized `enabled` was intentional. Preserve its
effective behavior as an explicit legacy declaration with uncertain intent, then
let the operator choose inheritance. A dry run must show which old sources remain
active; obsolete sources are retired only through an explicit transition, without
maintaining permanent bidirectional mirrors.

Restoring a previous configuration is a new validated change against current
contracts and authority. Retain a protected pre-migration backup plus the source,
descriptor, constraint and resolver inputs needed to establish its effective-value
baseline. A restore fixture must prove equal effective values at all covered
addresses, not just identical bytes. With incompatible current descriptors or
authority, report incompatibility/refuse instead of passing a byte-only test or
silently re-admitting an obsolete descriptor. Compare historical values using the
pinned baseline, then independently validate the proposed restoration for current
use. Counters must not roll back.

Restore does not reverse external effects, resurrect revoked permissions or
justify fallback after integrity failure. Fresh startup with invalid inputs
refuses or enters a named safe degraded mode. A running component may retain its
last admitted resolution only under its domain's current-use rules.

### 10. Documentation is part of the interface

Add a shared Node configuration manual describing source locations, ordering,
scope selection, the three configuration views, inheritance and change lifecycle.
Component manuals retain the meaning of their settings and link to that common
model. Their configuration tables should expose exact keys, types, default
sources, allowed scopes, composition rules, sensitivity and reload behavior.

Reuse descriptor data for mechanical tables and CLI help where practical; domain
rationale remains human-authored. Ship task-oriented HOWTOs for bootstrap, locating
a value, editing a workflow, resolving shadowing and restoring inheritance.
Every interactive setting should lead to its key, explanation and manual.

### 11. A bounded first slice, then an explicit coverage gate

The first retained vertical contains four cases:

1. An ordinary daemon setting, such as `logging.level`.
2. A middleware `enabled` setting edited through GUI and a file.
3. One workflow-scoped configurable parameter, initially demonstrated with an
   existing JSON-e Flow instance. An Arca non-Flow contract fixture must also
   demonstrate that the common scope is not specific to this executor.
4. An Inquirium resource limit using P085's actual narrowing/envelope semantics.

Each case must support locate, explain, edit, validate, save, apply, inspect after
restart, and restore inheritance. A full subtree case must combine inherited and
overridden leaves, including a value constrained by multiple sources.

This vertical does not prove coverage of every component. P091-015 closes the
remaining inventoried durable settings and introduces a gate for newly added ones.
Completion of this proposal requires that wider coverage, not just a useful demo.

### 12. One programmer contract, existing host bridges, explicit standalone mode

Expose a small data-oriented interface rather than requiring each consumer to
know directory order or reconstruct host policy. The following operation names
describe candidate contracts, not registered capabilities:

| Operation | Input | Result / boundary |
| :--- | :--- | :--- |
| Describe | Admitted scope and bounded key selection | Domain-owned descriptors, supported operations and source targets visible to this caller |
| Read / explain | Admitted scope, JSON Pointer, view and `resolution/id` (active also binds component receipt) | Immutable value/subtree, validation status and bounded derivation; no implicit reload |
| Plan change | Source binding, sparse patch/reset, base `resolution/id` and expected input identities | Candidate resolution, predicted effective values and semantic impact; no writes or activation |
| Commit | Authorized plan and expected source/descriptor/constraint bindings | Durable save receipt or typed conflict/refusal; no implicit application |
| Apply / inspect application | Durably admitted `resolution/id`, admitted component instance and expected `activation/generation` where present | Existing lifecycle operation and separately queryable application receipt |

The port has the same value, refusal and identity semantics in Rust and Python,
not necessarily identical function signatures. Distinguish missing key, denied
scope, unavailable context/host, unsupported contract, invalid source, source-set
conflict and pending/rejected application. A getter must not silently turn any of
these into a local default; defaults belong to admitted descriptors/sources.
Acquire/resolve once, then query an immutable handle explicitly carrying
`resolution/id`. The high-level CLI may acquire that handle for the operator;
low-level `read(resolution_id, address)` must not rescan files per key. Unknown,
expired or evicted identities return `resolution-unavailable`, not a fresh view
under an old ID. Reading a newer view never activates it.

Recommended reference implementation:

1. Rust consumers use the pure configuration contract and domain ports directly.
   Extend/reuse `json-utils` for ordinary mechanical merging; keep source identity,
   configuration validation and domain policy out of that utility crate.
2. Supervised Python uses a small non-UI configuration client. Once attached, it
   invokes the same host operations through P080 `host-capability.invoke`, using
   `ChannelJsonRuntime.invoke_host_capability`. Retained HTTP deployments use the
   existing `/v1/host/capabilities/<capability-id>` family. Both terminate in one
   handler/contract; transport is not a second semantic implementation.
3. Before process launch, the host can supply a bounded, immutable, module-scoped
   snapshot bound to component/instance, schema and `resolution/id`. Python startup
   decodes that snapshot instead of depending on a not-yet-ready channel or merging
   mutable directory contents again. Reuse supervisor provisioning and admitted
   runtime-home projections; the snapshot is derived, not another editable source.
   Read-only access and source binding are enforced by the host, not inferred from
   a module's claim about a file digest. A component reports successful consumption
   separately from the host merely making the snapshot available (`provisioned`).
   Use a digest/size/inline-or-ref carrier; 16 KiB is the initial inline ceiling,
   with smaller transport limits allowed and finite total limits frozen in
   P091-002. Above it, reuse the admitted object store. Before channel readiness,
   the supervisor provides a verified scoped file/handle; startup cannot require
   a capability call to retrieve the snapshot that initializes the channel.
   Process environment carries a locator/binding, not the whole configuration.
   Content addressing alone grants no access.
4. A Python unit test or standalone library may receive an explicit value snapshot
   by dependency injection. Offline operator resolution can use the same Rust core
   through a one-shot CLI adapter without starting the daemon. A Python-only
   installation can consume an exported snapshot; full live resolution without a
   Rust helper is outside selected V1 scope (resolved OQ-01), not an implicit fallback.

This follows `inference.policy.evaluate` and `service.order.result.prepare`: Python
packages requests and checks bound responses; Rust owns shared semantics. It does
not require all configuration clients to depend on the UI helper package. Reuse
its environment/HTTP mechanics through a non-UI seam where justified.

Read access is separately admitted by scope/key, including for a module reading
its own configuration. Operator plan/commit/apply stays on the operator control
boundary; a middleware host token or self-asserted component id is not a daemon
control credential. Any delegated write needs a separately scoped grant.
Register all five operations in one discoverable P072 inventory, with the
following policy. P091-002 registers these contract identities; runtime routes
remain unimplemented and unavailable:

| Candidate operation | `dispatchable` | `host-route` | `docs.human-registry` | Invocation boundary |
| :--- | :--- | :--- | :--- | :--- |
| `config.setting.describe` | `true` | `true` | `true` | Scoped host read |
| `config.value.explain` | `true` | `true` | `true` | Scoped host read, including value-only selection |
| `config.change.plan` | `false` | `true` | `false` | Authorized operator control |
| `config.change.commit` | `false` | `true` | `false` | Authorized operator control |
| `config.activation.apply` | `false` | `true` | `false` | Authorized operator control |

`docs.human-registry` denotes `docs: {"human-registry": ...}`, separate from
`flags`. It selects the curated `CAPABILITY-REGISTRY.en.md` / `.pl.md` tables;
it is neither a visibility permission nor a general "documented" flag. Include
the two common read contracts there, following `inference.policy.evaluate`;
keep the three operator-control entries out of that table, following
`operator.extension.lifecycle`. All five still belong in the machine registry,
appropriate API projection and operator documentation. P091-002 synchronizes the
two human tables and passes `make check-capability-registry` on registration.

All use `surfaces: [host-local]`, `advertisable: false`,
`federated-discovery: false` and `passport/eligible: false`. Do not invent a
signing domain for an unsigned local operation (`signing-domain: false`). Registration/discovery is not a
grant: generic module dispatch must refuse the three non-dispatchable operations,
even when it knows their schemas. Host routing independently checks operator
credentials and target scope. Discoverable descriptors are projected only within
the caller's authorized scope; no unrestricted enumeration.

Do not send the complete node configuration or secret values to every module.
Secret references retain their independent access rules; a configuration snapshot
does not issue or renew a grant.

No silent switching is allowed from the host-managed mode to ambient file/env
loading after timeout, denial, version mismatch or channel failure. Retaining an
already admitted snapshot is a domain-governed action, never evidence of current
authority. Migration may retain an explicitly selected legacy loader with visible
coverage limits; it must not claim P091 conformance or mix old and new sources.

### 13. Workflow configuration is an owner-bound scope, not an executor synonym

In P091, workflow settings are durable declarations controlling a named workflow's
future behavior: for example parameters, dependency/selection policies and limits
supported by that workflow's owning contract. This is broader than JSON-e Flow
and independent of the plan language or implementation language. One run's inputs,
results, retries already performed and progress remain invocation data or facts,
not editable configuration. A template example is not active operator intent until
explicitly selected and instantiated/admitted.

Reuse existing owner-specific definitions and configuration mechanisms (OQ-02 A),
with a thin configuration binding containing:

- the admitted owner/handler identity and definition or instance identity;
- the definition/source revision and relevant plan/setting contract revision;
- an exact setting path, editable source binding and domain-owned validation;
- the bound run context when inspecting an invocation's effective values.

`workflow_kind` selects a handler family, not a unique workflow, filename or grant.
Resolve it through the existing supervisor contract and bind the actual owner;
missing or ambiguous handlers do not become JSON-e Flow or another default engine.
For JSON-e Flow, the port uses the existing executor/instance binding instead;
do not invent a workflow-kind registration merely to expose its configuration.
CLI workflow aliases must resolve to these identities, not just match a label.

Arca's `arca.workflow` configuration and JSON-e Flow's existing instance fragments
provide two concrete source adapters. Their parameter schemas, normalization,
merge constraints and apply rules remain domain-owned. Future workflow handlers
can supply the same small descriptor/resolution port without a central enum of
workflow meanings or a mandatory JSON-e representation. P091 is not a replacement
orchestration engine and does not claim that every declaration is executable by
every handler.

The generic definition CRUD currently stores open `plan` values in append-only
records. P091-001a classifies fields needed for first-slice bindings; P091-001b
classifies the remaining fields. Neither exempts durable behavioral controls
merely because they are stored as domain resources. Such controls need file-backed
sources and owner-mediated projection/admission to claim P091 coverage. Retain
definition/run identity and historical records; migrate selected controls with
explicit source/revision bindings rather than adding an unsynchronized JSON copy
of the whole workflow store. Authoring or editing a file never triggers a run.
Non-file-backed controls remain a named migration gap until P091-010/P091-015
cover them. This preserves 2A without pretending that all current workflow CRUD
already satisfies the file-backed rule.

The first live acceptance can remain JSON-e Flow. P091-009a requires an early Arca
contract fixture for scope, source selection and refusal; P091-015 owns the
remaining actual consumers. This demonstrates an open boundary without making
all of P029/P033 or every orchestration extension a prerequisite of the first slice.

## Implementation Recommendations

### Ownership and minimal reusable core

Follow `node:DEV-GUIDELINES.md`: immutable data, domain-owned semantics, validation
at boundaries, pure transitions, and refusal/replay evidence before promotion.
Use `configuration-core`, not `config` (an existing data directory). Extract
`configuration-host` only when multiple host consumers justify that seam; do not
create an empty architectural layer. Add dependency-boundary checks with every
current higher-layer consumer listed, including provider/runtime adapter crates.

| Responsibility | Recommended owner | Must not absorb |
| :--- | :--- | :--- |
| Mechanical JSON value transformations | Existing `orbiplex-node-json-utils`; keep its public value behavior compatible | Configuration source order, provenance, I/O and policy |
| Setting addresses, source records, source-aware composition and derivation index | `configuration-core`, over existing `json-utils`; usable by daemon, standalone Rust and offline helper | Filesystem, daemon lifecycle, UI, inference-domain types or domain authority |
| Domain descriptors, constraints and semantic derivations | Existing component core/host contracts | Other domains' policy meanings |
| Bounded source acquisition, target authorization, durable writes and activation coordination | Node host/daemon adapters | A second implementation of domain merge rules |
| CLI and GUI | Clients of shared read/change/apply contracts | Hidden settings stores or client-side policy authority |
| Signed approvals and revocation | Existing P071/P085 and signing owners | Ordinary configuration becoming a signing bypass |
| Materialized module inputs and Python access | Supervisor-provisioned scoped snapshots plus a thin client of the shared host contract | Independent ad-hoc Python/Rust precedence rules, broad config access or a bootstrap RPC cycle |

Do not repurpose `config-sidecar-core` as a generic overwrite engine: its
append-only conflict contract is intentional. Reuse Inquirium's existing profile
resolver and retain its digest encoding and source semantics. P091 may wrap or
reference that result; it must not silently redefine existing signed bytes.

Extract shared owner lookup and a validated filename builder from the current
factory/seed helpers rather than creating another component-name registry. Keep
legacy `50-<config_key>.json` spelling unchanged, including underscores. Apply the
new safe-stem contract to newly selected operator targets only. Reuse explicit
domain filename functions as admitted target bindings; a prefix match alone does
not enroll an existing file into the new ownership model.

### Data contracts before endpoints

The following V1 families now have canonical schemas and Node mirrors. P091-002
still owns completion of their relational freeze gate; schema registration alone
is not proof of complete semantics or implemented routes.

| Candidate artifact | Required semantics / representative fields |
| :--- | :--- |
| `config-setting-descriptor.v1` | `setting/address` (scope, pointer, contract revision), `value/schema-ref`, `scopes/supported`, `composition/rule`, `validator/ref`, sensitivity, `application/mode`, `targets/editable`, `manual/ref`, descriptor provenance and canonical digest |
| `config-source-binding.v1` | `source/ref`, `source/class`, content `source/revision`, optional file/pointer, `order/index`, explicit `admitted/by`; absent targets and selector membership represented in the source-set snapshot |
| `config-resolution.v1` | `resolution/id`, `source-set/revision`, descriptor-set identity, pinned inputs/constraints/context, resolver/normalization revisions and `resolved/at`; activation identity belongs only to the separate receipt, never this preimage |
| `config-derivation.v1` | `derivation/digest`, `derivation/size-bytes`, inline or `derivation/ref`; per-pointer contributors (`source/ref`, role, rule), completeness and `aggregate/ref` when required |
| `config-describe.request.v1` / `config-describe.response.v1` | Admitted bounded selection and projected setting descriptors; refusal before acquisition |
| `config-explain.request.v1` / `config-explain.response.v1` | `view: declared \| resolved \| active`, exact binding, detail selection and field-wise disclosure policy for values/sources/paths/secret refs; validated value or explicit unavailable/refused result |
| `config-change-plan.v1` | Source-targeted patch/reset, base and candidate `resolution/id`, explicit `expected/source-set-revision`, expected descriptor-set identity/constraints, predicted values/impact and expiry |
| `config-commit-receipt.v1` | Transaction/plan refs, verified source outcome, candidate `resolution/id`, per-address resolved-value impact; never an application acknowledgement |
| `config-activation-receipt.v1` | Component-instance binding, `resolution/id`, `activation/generation` where allocated, `ConfigApplicationState`, reason and consumption/freshness evidence |

Freeze separate closed enums for `ConfigView`, source classes and contributor
roles (`decisive | shadowed | equal | rejected`); domain refusal codes extend only
through a versioned contract. Descriptor provenance follows
`SemanticEntryProvenance` (`distribution-default | operator-package`); it is not
the value source-class enum. That enum must also represent compiled defaults,
module/node/operator declarations, invocation overrides and admitted constraints
identified by P091-001a. A generated projection is never an independent source.
Use typed `ConfigApplicationState` and `ConfigRefusal` from Decision 6.

Reuse JCS through `CanonicalJsonProfile::JcsV1` and
`sha256_base64url_canonical_json_prefixed`, with a distinct declared domain per
artifact. Keep display labels/manual text out of semantic identity using a
specified canonical preimage, not arbitrary field deletion. Source content
revisions bind the admitted source content; commit/recovery additionally binds
exact file bytes. Freeze these distinct preimages. Resolution identity excludes
presentation and bookkeeping timestamps such as `resolved/at`, but includes any
time/expiry context that actually affects historical validation. Decision 6's
current-use time evaluation is separate and cannot renew this preimage. Full
internal digests may be sensitive; projected handles/digests must not expose a
hidden preimage.
When signatures are needed, use existing `DomainTag` / `apply_domain_wrap`;
do not change another contract's signed bytes.

Reuse bounded carrier and projection idioms from P090, not its inference DTOs.
Index derivation by JSON Pointer (for example `BTreeMap<JsonPointer, ...>`),
including structural and derived nodes needed to explain a declared selection.
Bound contributor count independently of pointer count: a map alone is not an
O(number-of-declarations) guarantee. Lazy materialization reduces startup work,
not mandatory retention or validation. Digest/ref/size and aggregate consistency
need negative fixtures; refusing excessive detail must preserve the decision.

DTOs crossing P080/HTTP or export/import are middleware contracts: use Schema Gate
with the appropriate `Ingress`/`Egress`/`Import`/`Export` checks at the actual
boundaries. Editable local configuration files may use a direct local JSON Schema
validator as allowed by DEV-GUIDELINES; document the local-only rationale. This is
not a requirement to turn every source file into a middleware DTO.
JSON Schema validates shape; pure core/domain ports enforce relational rules and
authority. Every conditional `if` carries the discriminating `required` fields.

New schemas carry `x-dia-workflow`, `x-dia-status` and `x-dia-basis` naming
`doc/project/40-proposals/091-file-backed-configuration-and-explainable-composition.md`.
Register plan/commit/apply request/response bindings as well as their plan/receipt
values; use the five-operation route matrix in Decision 12. Synchronize schema
mirrors, generated index and COVERAGE only when those artifacts actually exist.

### Reuse ports and transport without copying semantics

Keep transport-neutral request/result DTOs and pure source/derivation operations
outside daemon internals. Do not introduce FFI, PyO3, another long-running process
or a custom RPC protocol merely to let Python read configuration. Existing P080
channel and host dispatch already provide that seam. Register new operations
through P072 and Schema Gate; use the existing operator control family for writes
and lifecycle. Under the retained-on/off decision, existing
`/v1/middleware/settings` endpoints become compatibility adapters to those
operations, not a second write path.

When derivation is requested, capture contributors during composition/replay,
including equal and shadowed declarations. Startup may retain only Decision 5's
complete replay inputs. Differential fixtures cover both modes; the final merged
object alone is never provenance. Domain ports return their existing result plus
explainable references, not instructions for Python to repeat domain policy.

The Python facade belongs with shared middleware helpers, not under an Inquirium
provider adapter or UI-only dependency. Inject a snapshot reader/host-call function
so domain tests do not need a daemon. Verify response schema, selected scope/key,
`resolution/id`, receipt bindings and declared completeness before exposing values.
Bound request/response bytes, depth, deadlines and queues on both sides; the
inspected generic HTTP
`HostClient` uses an unbounded `response.read()`, so it is a transport starting
point, not proof of P091 resource safety. Bind caller identity from the admitted
session/token and host mapping, not a caller-supplied header or JSON field.

At bootstrap, project only the configuration needed by the admitted component;
keep snapshots out of directories read as editable config layers. Missing or
mismatched launch snapshots refuse startup in managed mode. After startup,
reads target named `resolution/id` values; apply additionally fences
`activation/generation`. Reading a newer resolution does not activate it. Pin an
offline one-shot Rust helper through the existing installation/launch contract;
use bounded
structured I/O without shell interpolation, and report missing binary or contract
mismatch. Never download a helper or fall back to a different resolver implicitly.

### Wrap existing middleware toggles and repoint callers

P091-007a integrates the shared contract with the existing implementation:

1. Reuse the domain checks in `node:daemon/src/middleware_settings.rs` and the
   application behavior of `apply_middleware_enabled_runtime` in
   `node:daemon/src/middleware_supervisor_host.rs`. Extract narrow helpers where
   the current operations combine validation, materialization, persistence and
   snapshot reads; do not copy their domain rules into the generic resolver.
2. Repoint the middleware-settings route handlers and their Node UI/CLI callers
   to the shared use case. The one-way call chain is client or compatibility
   endpoint -> P091 host wrapper -> retained domain/persistence/application
   primitives. The wrapper must not call a compatibility endpoint back into itself.
3. Route the selected source update through P091-006's commit contract, reusing
   compatible low-level persistence code without a second legacy-file write.
   Bind runtime application to the validated `resolution/id` through
   P091-007. Existing live start/stop stays available; do not replace it with an
   unconditional restart requirement. Separate explicit bootstrap materialization
   from reads, as required by P091-003.
4. Retain regression fixtures for both compatibility and new entry points:
   identical source/value resolution, one declaration commit per change, no
   duplicate lifecycle dispatch on retry, protected/unauthorized refusal, provider
   dependency closure and operator-stopped behavior. File edits, shadowed writes,
   live application, save-success/apply-failure and post-restart inspection must
   preserve the distinction between desired, active and observed states.

This is a bounded integration and call-site refactoring task, not a middleware
rewrite. P091-010 separately owns physical source migration and retirement of
obsolete inputs; wrapping alone does not establish migration completion.

### Read path and derivation retention

Separate `discover/read`, `resolve`, `plan`, `commit` and `apply` functions. Remove
seeding and toggle-file writes from the read path; keep explicit bootstrap and
materialization commands. Preserve evidence of defaults and later normalizations
before typed decoding or projection discards their origin.

Use immutable bounded replay inputs (Decision 5). Online active inspection binds
the component's acknowledged resolution, while offline resolution uses explicit
admission evidence or an unresolved constraint. Configuration acquisition must
detect changes during reads and return a consistent snapshot or conflict; even
one source changing cannot produce a mixed-revision answer. Pin the descriptor-set
artifacts as well as source content. Retain them before provision/acknowledgement,
without granting a historical export present-day authority. Expired/evicted evidence
is explicitly unavailable, never silently reconstructed from current inputs.

Keep legacy acquisition profiles explicit until migration: selected suffixes,
ignored files, root shape, missing-directory behavior, read/parse failures and
module/node ordering. New admitted P091 sources fail on malformed or unreadable
selected input. This is a visible compatibility change for Agora's skip behavior,
not something to "preserve" by reporting a partial configuration as fully valid.

### Write, activation and recovery boundaries

V1 commits one target file. Use Solution 028's append-only facts plus rebuildable
read projections; reuse `StorageWrite::append`, `StorageRead::read_stream` and
the temporal-log helpers as appropriate to the owning storage adapter.
`append_corpus_inference_evaluation` is a precedent for decision-before-transition,
not an existing atomic file/journal implementation.

The ordering contract under the shared writer lock is:

1. Revalidate plan, authority, source selection/membership and descriptor/constraint
   bindings. Persist a durable `intent` with transaction/plan ID, confined target,
   old byte digest or explicit absence, intended new byte digest, expected identities
   and a protected recovery payload/reference. No mutation before durable intent.
2. Prepare a unique target-directory temporary file, preserve required permissions,
   validate bytes, flush it and atomically replace the target. Apply platform
   directory/file durability primitives. The atomic rename protects target-file
   shape, not atomicity with the journal or non-cooperating editors.
3. Append a durable `outcome` bound to that intent and verified replacement.
   Return save success only after that outcome. If outcome persistence fails after
   replacement, return recovery-required with the known save uncertainty, never
   "unchanged" and never start application.
4. Apply is a separate authorized operation after a reconciled committed outcome.
   Re-evaluate time-dependent constraints with fresh host time at the application
   boundary, including deferred/recovered attempts, as required by Decision 6;
   expiry refuses without lifecycle effects. Append per-instance application and
   consumption facts. Rebuild active projections from those facts, not from the
   currently editable file.

Recovery scans bounded unresolved intents under the same coordination. If the
target equals the old binding (including expected absence), record not-committed;
if it equals the intended new binding, record a recovered committed source outcome,
then independently revalidate for any requested application. Equal old/new digests
permit a no-op outcome but do not prove that this process performed a replacement.
A third digest, unexpected absence, invalid bytes or unreadable target requires an
explicit conflict/recovery result; never overwrite it from an old intent. Digest
comparison proves content equality, not which writer produced it. It cannot
establish causality against arbitrary outside writers or restore their lost intent.

Retain idempotency keys and bounded recovery inputs; a retry cannot duplicate
declaration commits, application dispatch or external effects. An uncertain external
effect requires owner reconciliation, not a blind retry or an exactly-once claim.
Test interruptions
before/after intent, rename and outcome, plus disk-full, retention eviction,
permission failure and journal corruption. Garbage collection cannot discard an
unresolved intent or its required recovery evidence. No cross-file atomicity is
claimed by V1; multi-target plans expose separate commits and visible partial
completion rather than silently collapsing targets.

A restart-only setting is acceptable when its owner cannot reload safely.
Neither recovery nor restart may weaken current-use revocation, roll counters
back, rewrite historic operation evidence or label last-known consumption as
current liveness. New file bytes and new resolution identities do not create
permission to execute.

Reuse middleware supervisor start/stop and daemon control operations for application.
Inventory their actual capabilities before labeling a setting reloadable or
restart-only. V1 requires an explicit apply action (which may be explicitly combined
with save), not a new filesystem watcher that silently activates every file edit.

### P091-001: Inventory sources, writers and semantic ownership

Foundation guidance recorded on **2026-09-21** and implemented by
P091-001a/001b as an auditable map before changing loaders. Start from the dated
`node:docs/audits/CONFIGURATION-REUSE-AUDIT.md`, then verify its claims against
current symbols and tests; the audit is neither exhaustive nor current runtime
acceptance. Follow `node:DEV-GUIDELINES.md`: data and contracts first, narrow
mutation, validation at the owning boundary, explicit failures and scoped evidence.

#### Inventory record and discovery algorithm

Use one entry per semantic setting at an explicit scope, not one entry per JSON
file or UI widget. Separate reusable seam, writer, legacy-profile and verification
records and reference them by stable inventory-local IDs. Several settings can
share a loader without sharing a validator, application mode or retirement plan.
These are candidate inventory shapes, not P091-002 runtime DTOs or a new registry
of domain authority. Every setting entry must supply the following information,
directly or through checked references:

| Field | Required content |
| :--- | :--- |
| `id`, `classification`, `status` | Stable inventory ID; ordinary durable setting, invocation input, bootstrap input, secret locator, projection or non-setting with justification. Use the inventory status vocabulary below, not tracker `todo`. State the exact coverage claim. |
| `address` | Scope, semantic owner/subject or instance binding, JSON Pointer and contract revision. Keep the semantic address separate from each physical source pointer; array position, filename and display label are not owner identity. |
| `semantic_owner` | Existing component/contract that defines meaning, constraints and allowed transitions; link its code and manual. Distinguish this owner from acquisition, persistence and application owners. |
| `sources` | Ordered source bindings/classes, selectors, default origins and missing-source behavior; include invocation inputs and pinned domain constraints where applicable. Record locators and identity recipes, not secret values. |
| `writers` | Every production write/materialization path, caller and target, including manual edits, bootstrap, CLI, UI and domain projection. Record create/replace/append behavior, trigger, coordination/recovery and which source membership or content it can change. |
| `selection_precedence` | Named/versioned selection profile: filename filters, ignore rules, ordering, absent/invalid/root-shape behavior, overlay stages and domain derivation. Keep observed legacy behavior separate from the proposed admitted behavior. |
| `validator` | Actual parser/schema/typed guard and domain-policy ports, their order, refusal behavior and owner. Schema-backed protocol/middleware boundaries use the Node schema gate; local configuration validation does not become a substitute for that boundary. |
| `resolver` | Mechanical primitive plus domain normalization/constraint functions, with input/output bindings and code references. Mark impure orchestration and undeclared inputs; a merged `Value` is not provenance. |
| `application_mode` | Proven startup, reload, start/stop, next-invocation or other owner-defined behavior, affected instance/unit and acknowledgement boundary. Record requested, supported and observed behavior separately; unsupported/unknown is not silently reloadable. |
| `legacy_profile` | A named acquisition/interpretation profile with current compatibility differences and migration conditions, or an explicit justified not-applicable value. A profile names a gap; it does not grant P091 conformance. |
| `retirement_owner` | Component responsible for removing/repointing each legacy reader/writer, linked tracker task and equivalence/rollback gate. Keep this migration responsibility distinct from the retired-executor policy owner. |
| `evidence`, `verification` | Repository-relative path plus symbol, inspected revision/date, manual/discrepancies, executable command refs, expected fixtures/assertions, retained result and scope. Distinguish source inspection, legacy behavior, new contract proof and actual consumption. |

Do not infer that an omitted field means not applicable. An unknown has an owner,
reason and tracked completion condition; it blocks any claim that requires that
knowledge. Keep audit coverage and runtime-adoption claims distinct: recording an
existing test does not make a setting P091-compliant. Non-settings retain a reason
and owning contract, not an invented setting address.

Discover in two directions. First enumerate readers, merge calls, configuration
environment reads, CLI parsers and write/materialization functions within reviewed
source roots. Trace each reader upstream to inputs and downstream through typed
decoding, normalization and consumption. Then trace each UI/CLI/domain writer back
to its persisted target and forward to every affected reader/application unit.
Join these maps by explicit source/owner bindings; flag unclassified candidates,
unreferenced writers and contradictory manuals for review. Use deterministic
sorted records and ID-to-record indexes, with referential-integrity checks rather
than an inferred call graph as proof of coverage. Bound discovery inputs and
verification work; do not traverse runtime data directories or execute discovered
command text automatically.

#### Three daemon entry seams and a separate retirement-policy port

Record all three entries in `node:daemon/src/identity_store.rs` independently,
including callers and transitive effects, even when one delegates to another:

| Entry seam | Responsibility to inventory | Separation required by P091 |
| :--- | :--- | :--- |
| `load_merged_config_json` | Raw directory acquisition: sorted non-ignored regular files, missing/empty directory, parse/I/O errors, root shapes and per-source retirement validation before `deep_merge_json`. The current selector is not simply `*.json`. | Host owns acquisition; `json-utils` owns mechanical merge; daemon policy owns retirement refusal. Do not call the whole function a pure merger or silently narrow its accepted legacy file set. |
| `build_effective_runtime_config_json` | Factory-module discovery, initial node read, missing seed creation, node re-read, middleware-settings materialization/read, settings overlay, conditional factory inclusion, final composition and runtime-default projection. | Model the ordered stages and their inputs/outputs explicitly. Bootstrap/materialization is a write phase; default projection is a named derivation. Read-only resolve/explain cannot wrap this orchestration unchanged. |
| `load_layered_daemon_config_json` | Delegating public-to-crate loading boundary used by typed daemon configuration. It inherits the effective builder's writes and policy, despite its read-like name. | Keep a distinct call-site inventory and redirect callers deliberately; do not introduce a third resolver or treat delegation as independent purity evidence. |

Inventory `node:daemon/src/retired_middleware.rs::reject_in_config` as a separate
daemon-owned policy port. Its input is a selected parsed declaration plus source
binding; its output is acceptance or a typed, safely projected refusal. The
mechanical JSON algebra must know neither retired executor names nor daemon error
types. P091-003/004 extract/bind that policy without weakening it: validate every
selected source before ordinary folding, so a later overlay cannot hide a retired
root or nested executor reference. Keep `reject_in_package_manifest` at its separate
package-admission boundary. An empty retired root still refuses; unrelated product
HTTP configuration does not. Test both positive and refusal paths and the
"retired declaration shadowed by a later source" case. P091-001 records these
requirements; it does not perform the extraction or retire the safety guard.

#### Writers, bootstrap and invocation inputs

- Inventory `seed_missing_factory_module_fragments`,
  `materialize_middleware_last_settings`, `write_daemon_config_file` and their
  callers in `identity_store.rs`; also include explicit materialize commands and
  migration writers. Preserve `50-<config_key>.json` spelling and the actual
  `control/middleware-settings.json` target. Record `module_id`/`config_key`
  fallback separately from newly validated operator-target stems.
- Include `middleware_settings_snapshot` as a read-labelled path that can
  materialize, and `update_middleware_enabled` as a retained write path in
  `node:daemon/src/middleware_settings.rs`. Trace the supervisor handler and
  `apply_middleware_enabled_runtime` separately. Generated initial defaults and
  later explicit operator toggles need distinct migration evidence; an existing
  materialized `enabled` value alone does not establish operator intent.
- Classify CLI/env at the consuming seam, not by spelling alone. Trace daemon
  `DaemonCliOptions`, `DaemonConfig::apply_overrides` and `main.rs::resolve_config`,
  Node UI startup configuration, and supervisor/Python launch inputs. Record
  whether each value is a durable declaration, ephemeral override, bootstrap
  locator, explicit secret source or transport binding, including its precedence
  and lifetime. A CLI override must not be persisted merely because it wins.
- In particular, `--log-level` is an invocation override; Node UI's `password_env`
  is an explicit secret locator with its own exclusivity/authentication rules.
  `MiddlewareEnv.from_env` and host-provided directory/channel bindings are not
  automatically behavioral settings. Trace actual module/node projection before
  adding overlays; no duplicated node layer, silent host-denial fallback or
  expanded ambient host authority.
- Compare factory seeds, toggle storage, manual edits and planned 80/90 operator
  files as distinct writer/target bindings. Record concurrent creation as source
  membership change. P091-010 owns explicit first-slice migration; P091-010a owns
  remaining loader consolidation. Preview, protected backup, pinned effective-value
  equivalence and restoration evidence are required before retiring a writer.

#### Four first-slice inventory cases

Each case must instantiate the full record above; the following are concrete
starting bindings and required evidence, not pre-completed inventory entries.
Use named legacy profiles derived from the observed stages rather than one
universal "legacy merge" profile.

1. **`logging.level`.** Address `/logging/level` at node scope; daemon logging
   owns meaning through `DaemonLoggingConfig` and `DaemonLogLevel`. Map compiled
   defaults, selected node files and final `--log-level` override through
   `with_config_dir_overrides`, `apply_overrides`, `apply_cli_overrides` and
   `main.rs::resolve_config`.
   Writers are manual/config-materialization paths and, later, the shared
   operator target; the CLI is an ephemeral source, not a writer. Validator and
   resolver are typed level decoding plus ordered ordinary composition, not a
   tracing-library side effect. Trace startup `init_tracing` and control-path
   `reload_tracing` before claiming reload/application success. Name the legacy
   daemon effective/CLI profile and daemon-owned retirement work in P091-003/010.
   Retain source probes plus the Step 3 fixture: default/file/CLI precedence,
   invalid level, no read-time writes and saved-versus-consumed distinction.
   No existing source probe alone proves the new read-only contract.
2. **Middleware `enabled`.** Bind the module identity and its physical
   `/<config_key>/enabled` source pointer explicitly; daemon middleware settings
   and supervisor lifecycle own eligibility and application. Sources include
   factory/default/seed/node declarations and the legacy last-settings overlay;
   writers include bootstrap materialization, retained toggle API/UI callers and
   manual edits. Record `default_middleware_enabled`, persisted-settings decoding,
   protected-module/dependency guards and conditional factory inclusion as separate
   rules. Application can be eligible live start/stop, pending or restart-bound;
   an enabled JSON value is not a running-instance receipt. Name the legacy toggle
   materialization profile. Retirement belongs to those same daemon owners through
   P091-007a/010, preserving the on/off mechanism. Baseline tests below cover seed,
   overlay and refusal behavior; add no-write inspection, shadowing, save/apply
   separation and restart/consumption fixtures before claiming P091 adoption.
3. **JSON-e Flow, with Arca as a non-Flow control.** Create two owner-bound
   entries, not one generic workflow blob. For Flow, select an existing executor
   instance under `middleware_json_e_flow_services`, bind its exact identity and
   declaration pointer, and use `JsonEFlowExecutorConfig::validate` plus its schema
   gate. For Arca, bind a concrete `/arca/workflow` declaration/owned setting and
   the relevant definition/handler revision; retain
   `WorkflowDefinitionRecord`, `WorkflowKindHandlerRegistration` and
   `normalize_plan_from_trigger`. Inventory factory/node/module declarations,
   Python launch projection, manual/config writers and owner-mediated definition
   or template materialization. Classify per-run inputs/history separately; record
   non-file-backed durable controls as migration gaps. Selection, normalization,
   validation and next-run/restart behavior remain owner-specific; authoring must
   not trigger a run. Name separate Flow-instance and Arca legacy acquisition
   profiles, with middleware-runtime/daemon and Arca owners respectively retiring
   them through P091-009/010/010a. Existing Flow schema and Arca normalization
   checks are baseline evidence; P091-009a adds exact scope/source/revision,
   ambiguous-handler refusal and no Flow-schema coercion without claiming live
   Arca consumption. P091-001a includes enough pre-channel Python binding to
   freeze the shared DTO without inventing a universal plan language.
4. **An Inquirium resource limit under P085.** Use the existing
   `classify/labels-max` axis as a concrete candidate; the declaration pointer is
   `/inquirium/resource_profile/limits/classify~1labels-max`, with the profile,
   operation and class/context bound separately. `inquirium-core` owns limit
   algebra; daemon Inquirium/resource-envelope hosts own acquisition and current-use
   admission. Map distribution defaults, local operator profile, admitted signed
   envelopes, distributor safety ranges and task/session narrowing as distinct
   inputs. Ordinary config/manual writers do not become envelope issuers; signed
   sidecar/envelope and revocation writers retain their append-only/admission
   contracts. Reuse profile validation and
   `resolve_inquirium_resource_profile_sources_with_envelopes_and_safety_ranges`:
   axis-specific min/max, bounded signed widening, applicable-envelope intersection
   and final task narrowing are not last-writer-wins file order. Keep the existing
   digest encoding and pre-policy boundary-safety limits. Record legacy profile
   acquisition and the exact future-operation/application boundary, including
   `require_active_exact(..., &now)` and fresh expiry/revocation checks; historical
   resolution is not current authority. Retirement belongs to the Inquirium/daemon
   owners through P091-004/010, not removal of P085 policy. Baselines below cover
   narrowing/envelope semantics; add wrong-context, expired/revoked constraint,
   unchanged-bytes/changed-authority and no generic-merge bypass proofs.

#### Verification commands and foundation completion

Attach reviewed commands as structured `argv`, repository-relative `cwd`, bounded
timeout/output, expected tests/assertions and retained result references. The
following are concrete baseline commands to verify when populating the inventory;
listing them here does not assert they were rerun or that P091 exists. CWD is
`node` except the Arca row. A zero-test filtered run is not a pass. Source probes
establish locations only; record missing behavioral fixtures as pending work.

| Coverage | Command / evidence boundary |
| :--- | :--- |
| All three daemon seams and materialization | `rg -n -e 'fn load_merged_config_json' -e 'fn build_effective_runtime_config_json' -e 'fn load_layered_daemon_config_json' -e 'fn seed_missing_factory_module_fragments' -e 'fn materialize_middleware_last_settings' daemon/src/identity_store.rs` — inspect bodies/callers; presence alone proves no behavior. |
| Ordinary mechanical merge | `cargo test -p orbiplex-node-json-utils` — no source-selection, policy or consumption claim. |
| Retirement policy | `cargo test -p orbiplex-node-daemon --lib retired_middleware::tests` and `cargo test -p orbiplex-node-daemon --lib persisted_middleware_settings_reject_retired_executor_on_restart` — add the cross-source shadowing fixture if absent. |
| Logging acquisition/application | `rg -n -e log_level -e 'logging.level' -e resolve_config -e init_tracing -e reload_tracing daemon/src/config.rs daemon/src/main.rs daemon/src/lib.rs` — source probe; add the Step 3 behavioral test command after implementing that fixture. |
| Toggle bootstrap and persistence | `cargo test -p orbiplex-node-daemon --lib middleware_last_settings_` — test names mentioning restart do not prove live application. |
| Flow contract | `cargo test -p orbiplex-node-middleware-runtime --test runtime json_e_flow_story009_fixture_configs_validate` — owner-schema baseline, not a P091 operator run. |
| Arca non-Flow normalization | From `node/middleware-modules/arca`: `python3 -m unittest test_service.ModuleReportTests test_service.ArcaWorkflowPlanTests` — local owner/plan baseline, not cross-process consumption. |
| Inquirium profile and envelopes | `cargo test -p orbiplex-node-inquirium-core resource_profile::tests` and `cargo test -p orbiplex-node-daemon --lib inquirium_resource_envelopes::tests` — domain/core and host checks; bind each claimed invariant to actual test names. |

The implemented P091-001a delivers the inventory, checker, structural tests and
day-one CI hook specified below, with reviewed foundation entries for these cases, all three seams,
the policy port, writers, Agora/Node UI differences and minimum launch/workflow
bindings. Test the checker with a missing seam, dangling writer/profile ref,
unclassified override, renamed symbol, unsupported status, empty/zero-test evidence
and a hidden required migration gap. Run structural mode and `--verify-current`;
reserve `--promote` for completed required adoption, not inventory creation.
The implemented P091-001b extends the same map to remaining module-local and
record-backed controls.
P091-001 closes the audit when coverage, discrepancies and owned gaps are explicit;
it does not close those migration gaps or promote runtime status. Unknowns needed
to freeze ownership, inputs or cross-language bindings still block P091-002.

#### Implemented audit foundation — 2026-09-21

P091-001, P091-001a and P091-001b are complete at their deliberately bounded
inventory layer. The canonical artifacts are
`node:docs/configuration-inventory.v1.json`,
`node:tools/check-configuration-inventory.py`, its 18 negative-control tests and
the dated completion addendum in
`node:docs/audits/CONFIGURATION-REUSE-AUDIT.md`. Node documentation CI executes
the structural suite and `--verify-current`.

The inventory contains 120 deterministic entries, the three distinct daemon
seams, the separate retirement-policy port, ten writer/explicit-absence records
and all discovered daemon override fields, daemon CLI fields, workflow-record fields,
Node UI options, eight Python layered loaders and 35 static environment inputs in
the reviewed roots. Two projection/non-setting claims are `done`, nine
legacy-evidence claims are `partial` and 109 migration/adoption claims remain
`pending`. Accordingly, `--promote` still refuses: audit closure is not shared
runtime adoption. The executable baseline additionally retains the cross-source
retired-declaration shadowing regression required above.

This completion changes no runtime reader, writer, route, capability, ledger row
or MVP claim. P091-002 was the next dependency-ordered task at inventory closure;
its subsequent contract freeze is recorded below. P091-003/010/010a
own the recorded reader/writer migrations, and P091-015 still owns the separate
source-boundary checker and broad promotion gate.

### Conformance and drift checks

Maintain `node:docs/configuration-inventory.v1.json`, mapping each behavior to its
address, sources/writers, validator, resolver, application mode, manual, evidence
commands and retirement owner. Reuse the structural/status/verification idiom of
`check-inference-provenance-inventory.py` and the middleware listener inventory,
not their domain-specific field enums. P091-001a delivered the initial artifact
and `node:tools/check-configuration-inventory.py`; CI runs structural checks and
`--verify-current` in `node:.github/workflows/docs.yml` from the first day.
Only `done`/`partial` entries assert current executable evidence.
`planned`/`pending` remain visible gaps; an empty verification set is not
completion. Bound verification count (initial maximum 64), execute only
repository-reviewed commands, and use `--require ID` for scoped checks.
P091-015's `--promote` rejects unfinished required coverage.

Track non-settings and legacy exceptions explicitly. Add
`node:tools/check-config-source-boundaries.py` for configuration acquisition,
behavioral environment reads and duplicate configuration merging outside approved
seams. Use a reviewed source inventory/allow-list with ownership and narrow
exemptions for bootstrap, explicit secret sources, transport plumbing and tests.
Do not ban all `std::env`, `env::var` or JSON transformations. In particular,
Node UI's explicit `password_env` is not an undeclared setting fallback.
New durable env-only behavior and unregistered configuration loaders fail the gate.
Named legacy acquisition profiles may remain visibly incomplete during migration.

Test ordinary merge order with reference/golden cases; it is not generally
commutative or associative across type replacement. Property-test only laws valid
for the specific domain algebra, such as monotonic narrowing or intersection.
For all covered settings, test determinism for fixed inputs, equivalent CLI/GUI/file
changes, exact replay of acknowledged resolutions and no mutation by inspection.

Retain shared golden fixtures for Rust direct calls, the Python facade and each
supported transport/offline mode: nested maps, arrays, null versus missing,
scalar/object replacement, equal-valued layers, escaped JSON Pointers and mixed
subtree origins. Parsing fixtures include duplicate keys, non-finite numbers and
numeric representation limits; freeze a common admitted JSON profile rather than
inheriting Python's permissive `json.loads` behavior. Test invalid selected files,
source ordering, defaults isolation, source/descriptor/resolution/activation mismatches, unauthorized namespace,
bounded response refusal and absence of fallback after host denial/unavailability.
Under OQ-01 A, independent Python source resolution is not a second conformance
target. Tests cover the thin client, injected/exported snapshots and the installed
Rust offline helper; host refusal never activates a native legacy resolver.

Target-selection fixtures must cover both Workbench spellings (JSON key versus
module name), missing `module_id`, subcomponent inheritance, explicit domain
targets, reserved-name collision and refusal without fallback. An ordering fixture
must use the ordinary loader with `80-operator.json` and detailed `90-operator-*`
files, plus an explicit legacy `90-operator.json` migration case. Workflow fixtures
cover JSON-e Flow and Arca without translating one into the other's plan schema.

Security is a prerequisite to exposing new read/control routes, not a late UI
polish step. P091-005a owns these named executable fixtures:

| Fixture ID | Required refusal/disclosure proof |
| :--- | :--- |
| `config-security-path-escape` | Traversal, symlink escape and unsafe target bindings refuse without reading/writing an escaped source |
| `config-security-cross-module` | A scoped client cannot read or edit another module's settings |
| `config-security-losing-secret` | Secret-bearing losing/equal/rejected declarations remain protected in values, derivation and errors |
| `config-security-diff-secret` | Plans, predicted values, receipts and failed changes do not leak secrets |
| `config-security-digest-oracle` | Low-entropy hidden values cannot be tested through exposed digests, sizes or equality fingerprints |
| `config-security-scope-enumeration` | Describe/list cannot enumerate unauthorized owners, addresses or source existence |
| `config-security-deny-before-acquire` | Instrumented loaders prove zero acquisition, source fetch or secret-store calls on denied requests |
| `config-security-control-dispatch` | Generic module dispatch refuses plan/commit/apply; registry visibility and host attachment do not confer operator authority |

These are fixture requirements, not an invented existing `security-review`
command. Verify each supported transport and offline/export boundary as applicable;
a later adapter cannot inherit untested security coverage.

When implementation changes coverage, reconcile
`node:docs/implementation-ledger.toml`, regenerate
`node:docs/IMPLEMENTATION-LEDGER.md` through
`node:tools/generate-implementation-ledger.py`, and synchronize
`node:docs/MVP.md` for any affected hard-MVP scope. P091-002 (contract surface),
P091-014 (retained acceptance) and P091-015 (wide rollout) each include this
checkpoint. Docs-only planning does not promote runtime status.

### Four implementation steps after the foundation inventory

After the [P091-001 foundation inventory](#p091-001-inventory-sources-writers-and-semantic-ownership),
use the following engineering guidance recorded on **2026-09-21**. These four steps refine the
existing tracker under `node:DEV-GUIDELINES.md`, especially Data and Contracts,
Implementation Style, Host-Owned Runtime Primitives and Code Reviewing Guidelines.
The type names and record sketches below are implementation candidates; P091-002
still owns the exact wire contract and freeze gate. They do not register schemas,
enable routes or promote implementation status. Keep code-specific API documentation
and measured evidence beside their Node owners when implemented.

| Step | Tracker ownership | Reviewable result |
| :--- | :--- | :--- |
| 1. Freeze executable contracts | P091-002, after P091-001a | Versioned shapes, identity preimages, transition tables and shared positive/refusal fixtures |
| 2. Build resolution and domain ports | P091-003 and P091-004 | Pure deterministic composition plus owner-bound validation/derivation ports; both workstreams use Step 1's contracts |
| 3. Prove read-only `logging.level` | A bounded checkpoint within P091-003/004 and preparation for P091-005 | Direct describe/resolve/explain tests over one immutable resolution, without exposing a route |
| 4. Add change, application and exposure | P091-005/006/007, P091-005a, then P091-007a | Durable source outcomes, separately acknowledged consumption, security fixtures and retained toggle integration |

The completed P091-001b inventory remains an input alongside these steps. The
single-setting checkpoint is intentionally narrower than any claim of complete P091-003/004,
P091-005 or four-case runtime acceptance. Implementation dependencies remain those
in the tracker; Step 4 is an integration sequence, not one atomic milestone.

#### Step 1: Freeze data shapes, identity functions and transition tables

Begin with representative input/output fixtures from all four first-slice owners,
including the Arca non-Flow binding and Python pre-channel launch. Infer shared
structure from these cases while retaining domain validation in the owning port.
Use small immutable records and tagged alternatives for mutually exclusive cases:

| Candidate structure | Data and invariant |
| :--- | :--- |
| `SettingAddress` | Admitted scope kind, owner/subject binding, JSON Pointer and contract revision. A workflow binding retains its exact definition/handler or executor/instance identity; a label never selects an owner. |
| `SourceSlot` | Stable source ref/class, selector position and `Present(content-revision, retained-value-ref)` or `Absent(target-binding)`. An absent interactive target participates in membership fencing. |
| `SourceSetSnapshot` | Selection-profile revision, scope, owner-mapping revision and ordered source slots; an explicit digest identifies this immutable selection. |
| `DescriptorSetBinding` | Exact ref, digest and checked generation, with retained descriptor and owner-issued admission evidence. Admission availability is explicit and is not an empty descriptor list. |
| `ResolutionInputs` | Source snapshot, descriptor binding, pinned constraint/context evidence, resolver/domain-port revisions and normalization inputs, including historical validation time where semantically relevant. |
| `ResolutionResult` | Validated values or a typed refusal/unresolved result, with input binding and bounded diagnostics. Requested explanation detail is separate from the semantic result. |
| `DerivationEntry` | Output pointer, rule ref/revision, ordered contributor refs/roles and structural or domain dependency refs; completeness is explicit. |
| `ChangeIntent` | Exact source target, bounded declaration edits, expected identities, application-unit binding and requested apply policy. |
| `ApplicationBinding` | Component instance, resolution id, owner-local activation generation when allocated, consumption receipt and freshness. It is separate from a commit receipt. |

In Rust, distinguish source revision, descriptor digest/generation, resolution id
and activation generation with validated newtypes. Keep closed protocol states
as enums with exhaustive handling and explicit wire spellings; keep the repertoire
of domain owners and versioned rule implementations open through admitted ports.
Deserialize neutral DTOs at the responsible boundary, then construct validated
values. A valid DTO or a type named `Admitted` does not itself prove host authority.
Use `Result` for failure; distinguish missing, explicit JSON `null`, unavailable
context and denial rather than encoding all four as `None` or an empty map.
Serializable transition data remains necessary even if local typestate proves
some sequencing constraints.

Specify each identity as a named projection into canonical JSON followed by the
existing domain-separated digest helper. A proposed preimage decomposition is:

```text
source-set preimage = selection profile + scope + owner mapping + ordered slots
descriptor-set preimage = set identity + generation + admitted descriptor revisions
resolution preimage = source-set revision + descriptor-set binding
                    + constraint/context binding + resolver/domain-port revisions
                    + normalization inputs and semantic historical time
activation binding = component instance + durable owner sequence + resolution id
```

Freeze exact fields, domain tags and normalization rules as test vectors. Include
the evidence revisions that change admission; exclude presentation labels,
`resolved/at` bookkeeping and requested detail/projection from resolution identity.
Keep admitted-content revisions distinct from exact file-byte digests used for
commit/recovery: a whitespace-only edit may preserve content identity while
invalidating the file precondition. Encode absent targets explicitly rather than
hashing them as empty objects. Counters reject zero and any increment beyond
9007199254740991; that upper value is valid, but cannot be incremented. Never wrap,
saturate or reset counters on restart. Storage locators and arena indices stay
outside semantic preimages; retain content revisions and semantic source bindings
instead. Preserve existing domain encodings, such as Inquirium's effective-profile
digest, behind their own types instead of recoding them as P091 identities.

Freeze a common JSON admission profile before typed decoding: reject duplicate
object keys, non-finite numbers, unsupported numeric representations, malformed
pointers and invalid active-setting fields. Use a duplicate-detecting parser at
the bytes-to-value boundary; a later validator cannot recover overwritten keys.
Decode pointer escapes once into segments, retain their canonical encoding and
match ancestry by segment boundaries. Require object roots for admitted
configuration documents while preserving `json-utils`' generic value contract.
Version intentional extension objects explicitly; avoid a blanket unknown-field
policy that either hides misspellings or closes every domain's extension point.

Represent limits in a validated `ResolutionBudget` and separate host
acquisition/output/history budgets. The initial measurement candidates, qualified
on 2026-09-21 as finite first-slice contract defaults (not deployment capacity), are
64 selected sources, 1 MiB per source,
8 MiB total retained input including descriptors/context, depth 64, 65536 visited
JSON nodes, 262144 contributor links and 1 MiB response bytes. Preserve Decision
12's 16 KiB inline carrier ceiling. The measured four-case corpus and complete
axis table are retained in the
[Node freeze evidence](https://github.com/diapod/node/blob/master/docs/audits/P091-002-FREEZE-EVIDENCE.md).
V1 additionally freezes 4096 descriptors, 262144 dependency edges, 2048-byte
pointers, 65536-byte strings, 1048576 work steps, 1024 history records and 64 MiB
history bytes. Ordinary retention is an explicit 90-day engineering policy, not
a benchmark-derived lifetime. Protected unresolved/active evidence cannot be
evicted to admit new work. Replans are bounded to three per request, each with a
fresh whole-plan approval. Account before allocation, use checked
addition/multiplication, and specify which owner enforces each limit. Exceeding
one returns a bounded refusal; callers cannot disable structural ceilings.

Use an executable transition relation of the form
`(prior-state, event, verified-bindings) -> next-state + facts-to-record | refusal`.
Give commit/recovery and per-instance application separate relations. Cover every
Decision 6 state, duplicate events and mismatched receipts without adding a
generic boolean `success` that erases pending or unknown consumption. Freeze
phase-specific current-use time checks separately from historical replay.

**Verification checkpoint:** positive/negative schema fixtures plus relational
tests cover substituted identities, expiry, counter boundaries, conditional
required fields, all state/event pairs, disclosure and inline/ref consistency.
Run the same JSON vectors through Rust DTOs and the thin Python snapshot decoder;
Python tests check binding and refusal propagation, not a second merge algorithm.
Register all five operations with Decision 12's flags and complete the final
P091-002 freeze gate, including schema mirrors, registry projections and the
contract-only ledger entry. Routes remain disabled until P091-005a.

#### Step 2: Implement the pure fold and owner-bound derivation ports

Keep three explicit transformations:

```text
authorized host acquisition -> immutable ResolutionInputs
resolve(ResolutionInputs, domain ports, detail) -> ResolutionResult
project(ResolutionResult, admitted selection, disclosure policy) -> read DTO
```

The host supplies snapshots and authority evidence. The resolver borrows values
and builds a new result; mutation is confined to its local accumulator. Store
sources in an ordered vector, descriptors in an address-indexed map and retained
values once per source. A deterministic `BTreeMap` is a reasonable initial index
for addresses and JSON Pointers; it does not replace JCS serialization or define
source precedence. Share immutable inputs across consumers only when ownership
requires it; avoid an `Arc<Mutex<...>>` around an entire mutable configuration.

For ordinary JSON composition, use a **left fold in admitted source order**.
Visit object keys deterministically, recursively combine object/object pairs and
replace the slot for other pairs. Arrays remain whole replacement values;
omission inherits and `null` retains the descriptor's meaning. Keep the mechanical
walk in `json-utils`: if instrumentation is needed, add a narrow observer for
structural events with the existing public functions delegating through a no-op
observer. Configuration interprets these events; the utility receives no source
identity, policy, filesystem or activation types. A depth guard or explicit stack
must bound the walk before descending, including inserted/replaced subtrees.

Do not parallel-reduce or regroup ordinary layers. For example, composing
`{"a":{"x":1}}`, then `{"a":0}`, then `{"a":{}}` yields `{"a":{}}`;
merging the last two first can preserve `x` incorrectly. Differential fixtures
against the existing primitive pin this behavior. `values-only` and
`with-derivation` run the same validation and value algorithm; the optional
observer changes evidence materialization only.

For explanation, retain a bounded arena/vector of structural contributions and
index entries by output pointer. Store source indices/refs and input pointers
instead of copying entire JSON subtrees into every contributor. Record replacement
at an ancestor, then resolve affected descendants through that ancestor edge;
do not report displaced child declarations as current winners. Empty objects,
arrays, equal declarations, defaults and derived nodes need explicit coverage.
Contributor roles describe the selected result: an overwritten declaration is
shadowed; equality remains visible; rejection records the owner's reason and
cannot silently remove a constraint. Multi-source narrowing may have several
decisive inputs. Compact structural edges are acceptable only if queries expand
them completely within bounds or report unavailable detail.

Budget actual traversal, value-copy and contributor work. With `V` visited nodes,
`E` retained contribution/dependency links and `P` indexed pointers, index work is
approximately `O((V + E) log P)` plus parsing, copying and domain validation; it
is not automatically linear in the number of declared leaves. Count subtree
replacement/replay expansion too. Measure this simple baseline before introducing
tries, persistent trees or interning.

Let a host-admitted registry map an exact rule/validator ref and revision to a
small domain port. A candidate port takes ordered scoped declarations, pinned
constraints/context and a budget, and returns the existing domain result plus
bounded derivation/dependency refs or a typed refusal. The port is deterministic
and performs no I/O; host adapters obtain signatures, revocation views and fresh
time before calling it. Use a trait object for heterogeneous runtime-selected
ports when needed and ordinary functions for local fixed algorithms. Never
dispatch by an incidental component name or execute code supplied in JSON.

Reuse Inquirium's resource-profile functions, including their per-axis min/max,
envelope and task narrowing behavior. The adapter preserves the existing output
and digest and enriches evidence at the owning derivation seam; generic P091 code
does not recompute policy from a final value. Keep retirement checks, toggle
eligibility and signed-sidecar validation with their owners. Missing, ambiguous,
withdrawn or unsupported port bindings refuse before producing validated values.
An offline export supplies exact admitted bindings or explicit unresolved context.

When domain-derived settings depend on other settings, use declared read/write
sets and a bounded directed graph. Topologically order it with Kahn's algorithm
and a stable ready-set order; reject cycles, missing inputs and ambiguous output
ownership before evaluation. This graph orders configuration derivations only.
Store reverse edges for later impact analysis. If a domain cannot expose a safe
dependency closure, bind and recompute its entire declared application unit; never
guess dependencies from the shape of its returned JSON.

Retain input artifacts and resolver/port versions for lazy explanation. Replaying
an old resolution uses those inputs, not the current registry; an unavailable
historic implementation or retained input yields `resolution-unavailable`.
Cache derived indexes in memory by resolution and detail contract. If caching
projected output, also bind caller disclosure context and recheck access on every
read. Optional detail-budget exhaustion preserves the semantic resolution/refusal
and reports incomplete/unavailable detail; it cannot turn a denied value into an
admitted one or make a truncated explanation appear complete.

**Verification checkpoint:** determinism, immutable inputs, parity of both detail
modes, scalar/object/array replacement, equal layers, escaped pointers and lazy
historical replay. Use property tests for applicable laws such as P085 narrowing,
with explicit non-associative counterexamples for ordinary merging. Domain tests
cover descriptor withdrawal without a source change, offline missing authority,
Arca/Flow owner mismatch, graph cycles and budget refusal. Dependency guards
enumerate current workspace consumers and forbid host/UI/provider dependencies
from `configuration-core`; no helper extraction may retire a domain refusal.

#### Step 3: Exercise `logging.level` through a read-only local seam

Use `logging.level` as the first concrete setting, addressed by `/logging/level`
in an admitted node scope. Bind its descriptor to the daemon's `DaemonLogLevel`
vocabulary (`trace`, `debug`, `info`, `warn`, `error`), existing default source and
validation semantics. Reuse the owner and safe-target lookup from Decision 3;
the fixture may bind `80-operator.json` explicitly without inventing a component
stem for the daemon. A proposed local test input is:

```json
{
  "selection": {"scope": "node", "pointer": "/logging/level"},
  "layers": [
    {"ref": "compiled-default", "value": {"logging": {"level": "info"}}},
    {"ref": "10-base.json", "value": {"logging": {"level": "warn"}}},
    {"ref": "80-operator.json", "value": {"logging": {"level": "debug"}}},
    {"ref": "invocation:log-level", "value": {"logging": {"level": "trace"}}}
  ]
}
```

This is a fixture recipe, not a complete wire DTO: its builder must supply the
source classes/revisions, descriptor/context bindings and budgets from Steps 1/2.
The expected resolved value is `trace`; without the explicit invocation source it
is `debug`. Removing only the operator declaration in a new in-memory candidate
restores `warn` when no invocation override exists. A same-valued operator
declaration remains explicit. Offline acquisition without an invocation snapshot
must not claim to reproduce a running process's `--log-level` override.

Exercise `describe`, `resolve`, `read` and `explain` as direct library/host-adapter
calls in tests. First inject immutable inputs, then add a confined temporary-file
acquisition test with explicit caller admission. Separate the raw reader from
`build_effective_runtime_config_json` and its seed/materialization behavior;
retain `retired_middleware::reject_in_config` at the appropriate owner validation
boundary. Do not call an existing mutating loader merely because its return type
is JSON. Keep legacy selection/error profiles named during extraction.

The acquisition algorithm admits scope first, enumerates a bounded selected set,
opens confined source handles, reads bounded bytes and builds the pinned snapshot.
Cooperating source writers use shared coordination. Detect changes in membership
and content while acquiring, and return a coherent snapshot or `source-conflict`
after a finite retry budget. Metadata/mtime checks alone are insufficient; even
repeated digest passes do not provide atomic snapshots against arbitrary
non-cooperating editors. Keep that limitation explicit and never re-read a source
inside an individual getter. Look up `resolution/id` once, then query its immutable
handle; different file bytes produce a newly acquired candidate, never a changed
answer under the old identity.

**Verification checkpoint:** assert the fixture values and contributor roles,
including a `/logging` subtree; preserve the old explanation after changing its
source or current descriptor. Unknown level, duplicate key, wrong scope, changed
source set and exceeded budget return exact refusals. Instrument reads and
effects: denied scope performs zero acquisitions; inspection performs zero
writes, directory creation, secret/provider calls, tracing reloads and process
starts/stops. Compare temporary-file membership/content/permissions before and
after to complement the effect counters. Existing daemon behavior remains the
value oracle on explicitly prepared legacy fixtures, not a callable dependency
of the new read path.

The descriptor may advertise an owner-supported apply mode after inventory
verification, but these tests never invoke it. The daemon's tracing reload path
is the later application seam; a resolved JSON value is not evidence that its
subscriber accepted the new level. This step has no active-consumption claim and
does not expose CLI, HTTP or P080 operations before the security gate.

#### Step 4: Compose planning, durable commit, application and exposure

Implement read adapters and the write/application host use cases behind disabled
routes, retaining the Step 2 pure resolver as their common value oracle. Start
with one-file transactions and full selected-input fencing. Narrowing the fence
is an optimization requiring a proven dependency closure and compatible scoped
application semantics.

Represent declaration edits as a bounded ordered sequence of
`Set(pointer, JSON-value)` or `Reset(pointer)` against one admitted target. These
are candidate edit operations, not JSON Merge Patch: `Set(..., null)` must not
mean deletion. Reject duplicate or ancestor-overlapping edits in one V1 plan
rather than inventing ambiguous patch order. The owner defines allowed targets
and paths; use whole-array replacement unless it explicitly supports narrower
edits. Reset removes only that declaration and preserves unrelated values plus
the empty root `{}`. It does not remove the file or manufacture a default.

A concrete planner copies the target declaration once, applies edits, constructs
a candidate source snapshot and runs the same resolver/domain ports. Compute
impacted addresses from edited paths, ancestor replacements and the reverse
dependency graph, conservatively widening to the full application unit when
needed. Compare base/candidate resolved values and separately record declaration
changes and effective-value impact. Derive `shadowed` from contributions, not
just equal output: an explicit equal declaration and a shadowed declaration can
both leave the value unchanged for different reasons. A plan binds its target,
ordered edits, old/new byte digests, source membership, descriptor/constraint
identities, base/candidate resolution, predictions, expiry and application unit.
Authorization is checked independently against that exact plan at commit time.

Use Decision 8's conflict family and three reason codes. Compare pinned/current
membership, order, source content and domain dependencies; classify a change as
unrelated only with positive host evidence. Even an unrelated content change
refuses the stale plan. A bounded replan returns a new id, fresh authority checks
and new predictions; no approval transfers implicitly. Exact-byte fencing also
catches formatting edits without treating them as changed semantic values. Use a
specified deterministic source serializer to prepare the candidate bytes during
planning, preserve unrelated declarations and revalidate the exact bytes before
replacement. Hash those bytes separately from canonical semantic preimages.

For durable commit, reuse Solution 028's append-only facts and rebuildable
projections. A candidate `CommitIntent` carries transaction/idempotency key,
plan binding, confined target, explicit old absence or old byte digest, intended
new byte digest and a protected recovery payload ref. A separate `CommitOutcome`
records the verified source result. An indexed pending-intent projection allows
bounded recovery pages; it is rebuildable from those facts.

Under shared host-writer coordination, revalidate current bindings/authority,
append durable intent, prepare and flush a unique sibling temporary file,
atomically replace the target and persist the durable verified outcome. Include
bootstrap/package writers in the same protocol. Keep storage transactions short;
do not hold them across provider/lifecycle work. A target replacement can be
visible before the outcome is durable, so failure then means `recovery-required`
and no application. Do not claim filesystem/journal atomicity or hide uncertainty
behind an automatic restore.

Implement recovery as a pure classifier over a bounded observation, followed by
explicit host actions:

| Observed target versus retained intent | Recovery decision |
| :--- | :--- |
| Old bytes or explicitly expected old absence | Record not-committed; no apply |
| Intended new bytes, distinct from old | Record recovered committed outcome; any apply needs fresh authorization |
| Observed bytes match both identical old and new bindings | Record no-op content outcome; do not claim which process wrote it |
| Third version, unexpected absence, unreadable or invalid bytes | Record conflict/recovery-required; preserve the observed target |

After validating the observed target, check whether it matches both old and new
before choosing either exclusive case. Equal planned digests alone do not classify
a third version or unreadable target as a no-op. Retention
must protect unresolved intents and their recovery payloads, active/pending
resolution evidence and acknowledged bindings needed by the supported history
contract. If protected evidence fills the budget, refuse new admission instead
of evicting recovery data. Temporary-file cleanup is scoped to owned transactions.

Application consumes either a reconciled commit outcome or an explicit durable
observed-source admission for manual file edits. Use a pure decision table over
the prior per-instance application state, requested resolution, fresh domain
admission and consumption events. Serialize concurrent apply admission with
owner-local expected-generation checks and durable allocation. Persist attempts
and generation allocation before lifecycle dispatch; record `active` only after
an exact bound consumption
acknowledgement. Keep the previous acknowledgement when the attempted new apply
fails. A delayed acknowledgement for a superseded instance/generation cannot
advance the current projection. Reconstruct durable sequence allocation on
restart; an uncertain dispatched effect requires owner reconciliation before
retry, not a fresh generation and blind repeat.

Classify each concrete effect using DEV-GUIDELINES' recovery classes and record
its owner, key, deadline and reconciliation/disposal policy. File replacement
uses the journal protocol above; stopping a process cannot undo work it already
published. Reuse the existing supervisor dependency graph for provider-first
startup, dependent-first drain, readiness and `operator_stopped` behavior. Recheck
expiry/revocation at queued dispatch, retry and recovery; a saved or provisioned
resolution never renews authority. Long application operations use the existing
[Bounded Deferred Operations](../60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md)
contract, with bounded reconciliation through the
[Replay Scheduler](../60-solutions/020-scheduler/020-scheduler.md).
Link operation and application ids explicitly; do not add a private polling loop.

P091-005 adapters share the same scoped request/result bindings and thin Python
facade, including exported/injected and supervisor-provisioned snapshots. Reuse
P080 dispatch and existing operator-control routes with Schema Gate at actual
ingress/egress/import/export boundaries. Retained Rust HTTP clients use the
host-owned HTTP runtime and bounded bodies prescribed by DEV-GUIDELINES; Python
uses bounded reads and validates the requested scope, resolution and completeness.
The one-shot offline helper remains installed/pinned and uses bounded structured
I/O. No adapter adds a resolver fallback after denial or outage.

**Exposure and verification checkpoint:** P091-005a must pass all eight named
`config-security-*` fixtures on the relevant adapters before enabling any new
route or repointing UI/compatibility callers. P091-007's consumption/recovery
evidence is also required before P091-007a integrates middleware on/off. Repoint
compatibility handlers to the shared use case, with one source commit and one
authorized lifecycle dispatch; retain eligibility and dependency checks behind
it. Physical legacy-file migration remains P091-010.

Retain tests for each crash boundary around intent/replace/outcome, file and
journal failure, third-version recovery, shared-file conflicts, stale/revoked
plans, expiry after successful save, lost/duplicate acknowledgements and restart
fencing. Test shadowed `enabled` edits against the actual resolved value, saved
but not applied outcomes, repeated compatibility calls and provider loss. Assert
effect counts as well as receipts; an idempotency key alone proves no effect
guarantee. Update the exact contract/runtime ledger scope and generated view at
each completed milestone; P091-014/015 still own the four-case and broad coverage
claims respectively.

## Trade-offs

- **Benefit:** one discoverable control model reduces memorized locations and
  makes GUI changes reproducible without making GUI mandatory.
- **Benefit:** per-key derivations explain layered maps, constraints and shadowing
  without forcing operators to manually reconstruct merge order.
- **Cost:** retaining source identity and application history adds bounded metadata
  and requires explicit reload/recovery contracts.
- **Cost:** manual editing and concurrent UI writes require cooperation and conflict
  handling; an ordinary filesystem is not a distributed transactional database.
- **Deliberate limit:** uniform operations do not make every limit overridable or
  eliminate signed approvals, secrets stores and domain state machines.
- **Migration risk:** blindly flattening defaults or deleting legacy toggles can
  change behavior. Preserve current intent before improving inheritance ergonomics.

### Alternatives considered

1. **One giant file:** easy to locate, but obscures ownership and increases write
   conflicts; keep a common address space across bounded sources instead.
2. **GUI database plus periodic export:** leaves files as a secondary mirror and
   violates the promise of first-class text editing for ordinary settings.
3. **Universal deep merge:** simple mechanically, but unsafe for permissions,
   append-only approvals and P085 limit algebra.
4. **More manuals only:** useful immediately, but cannot explain exact active
   sources, detect stale resolution bindings or enforce shared write semantics.
5. **New configuration DSL first:** defers operator value and adds another model
   to learn; keep JSON and typed data contracts for the initial implementation.

## Failure Modes and Mitigations

| Failure | Required behavior/evidence |
| :--- | :--- |
| GUI stores a preference outside the declared file sources | Inventory gate rejects coverage; UI names the source it actually changes |
| A read seeds or rewrites files | Snapshot-before/after test proves zero filesystem mutations, producer starts and implicit source-fetch network calls |
| Removing an override writes today's default instead | Inheritance test changes the lower source and observes the inherited update |
| A file edit is silently shadowed | An `80-operator.json` / `90-operator-arca.json` fixture predicts unchanged effective values plus `shadowed`; explicit commit reports no resolved-value change, not activation |
| A map is attributed to one file despite mixed leaves | Per-leaf derivation fixture with at least three source classes |
| Workflow specificity widens host authority | Domain refusal test; scope order does not replace admission |
| Stale GUI or a host seed write invalidates a plan | Relevant source membership/order/content and descriptor/constraint preconditions conflict; all cooperating host writers serialize; new shadowing file and ancestor replacement fixtures |
| An unrelated shared-file edit invalidates another owner's plan | Host-proven `unrelated-source-content-changed` permits bounded replan, never stale commit or carried-over approval; affected/ancestor/unclassified changes and redaction have separate fixtures |
| Save succeeds but activation fails or only partly completes | Separate durable save outcome and per-instance application state; preserve prior acknowledgement, do not claim whole-node activation |
| A legacy on/off endpoint bypasses P091 or the wrapper writes/applies twice | Compatibility-path fixtures prove the same source resolution and commit path, bounded retry without duplicate dispatch, and retained domain/lifecycle guards |
| Restart fabricates history from current files | Replay pinned source, descriptor, constraint and normalization inputs for the retained `resolution/id`, or report unavailable history |
| Secret leaks through a losing value, diff or digest | Redaction fixtures cover successful and refused queries and exports |
| A key query reads an arbitrary file or another participant's scope | Read authorization and source-confinement fixtures refuse before source acquisition |
| Migration changes default inheritance or drops an old source | Dry-run equivalence report and explicit operator resolution before commit |
| Unknown module/schema/merge rule becomes active | Typed unsupported/unvalidated result; no implicit execution or authority |
| Python recomputes settings after host refusal or reads mutable files after launch | No managed ambient fallback; startup and later reads bind exact scoped `resolution/id` and consumption evidence |
| Two loaders disagree on selected files or invalid JSON | Differential fixtures and explicit legacy profiles; migration reports changed admission instead of claiming parity |
| A config client becomes a route to host control or all node settings | Read/write grants remain separate; cross-module and forged-identity requests refuse before disclosure or effects |
| A module cannot start until the channel it initializes is ready | Supervisor supplies a bounded launch snapshot; startup test requires no configuration RPC |
| A display label, component path or duplicate stem selects a file | Resolve admitted owner bindings; reject ambiguous/reserved/unsafe targets, never auto-sanitize or redirect failed writes |
| Common defaults overwrite detailed settings due to naming | Use existing sort order with `80-operator.json` before `90-operator-<component-name>.json`; legacy `90-operator.json` requires explicit migration |
| Workflow scope only works for JSON-e Flow | Arca non-Flow fixture uses the same binding contract with its own schema/normalization; unknown kinds and wrong definition/run bindings refuse |
| Descriptor withdrawn but its `50-*.json` remains | `source-set/revision` stays equal, descriptor-set changes; `descriptor-invalidated` blocks new admission, while the old resolution remains historically explainable |
| Snapshot delivered but never consumed | `provisioned` remains distinct from acknowledgement, component outage and `unknown` |
| Authority expires between plan, commit and apply, including queued/recovered apply | `config-time-expiry-between-phases` preserves the historical verdict and save but refuses current apply as `constraint-conflict` / `constraint-expired`, reports `application-rejected`, and records no lifecycle effect or new consumption acknowledgement |
| Crash leaves intent without outcome | Old/new/third/absent/unreadable/no-op fixtures reconcile or refuse; no automatic overwrite, successful receipt or application before a durable outcome |
| Offline package files are mistaken for approval | No owner-issued pinned descriptor/admission export means unresolved validation; historical exports grant no current authority |
| Lazy explanation uses today's descriptor set | Values-only and detailed modes replay identical retained inputs, even after withdrawal/file edits; evicted evidence is explicitly unavailable |
| Reset leaves an empty shared file | Retain `{}` with unchanged unrelated declarations/permissions; no value contributor, no implicit deletion |
| Backup restore passes on byte equality but behavior differs | Compare pre-migration effective values under pinned baseline inputs; independently validate current authority and report incompatible descriptors |
| Excessive derivation silently omits a denying constraint | Bound exceeded requires admitted aggregate or refusal; summary cannot become more permissive |
| Registered operator route becomes module-dispatchable | All five operations are discoverable within scope; only describe/explain permit module dispatch, with independent read admission |

## Implementation Tracker

P091-001/001a/001b are complete at the bounded audit layer; the remaining rows
retain their implementation status below. The tracker vocabulary is
`todo | partial | done`; an abandoned task must retain an explicit dated
supersession, not silently disappear. Inventory vocabulary is
`planned | pending | partial | done`: planned/identified unfinished items map
to tracker `todo`, not a literal inventory state named `todo`.
The dated Node audit is input, not complete machine-readable coverage.

Dependencies are completion prerequisites; fixtures can be authored earlier.
Code/DTO registration can exist behind disabled routes while security evidence is
pending. No new route is enabled before P091-005a covers its boundary.
A task cannot be `done` while the ledger marks **the same claimed surface**
partial. A completed contract-only slice may coexist with a partial component
only when both explicitly delimit that narrower claim.

| ID | Work item | Depends on | Status | Completion gate |
| :--- | :--- | :--- | :--- | :--- |
| `P091-001` | Close the configuration/reuse inventory audit | `P091-001a`, `P091-001b` | `done` | Completed 2026-09-21 at the audit layer: source/writer and retirement ownership are mapped, discrepancies are retained in the dated Node audit and every remaining migration/adoption gap is represented in the machine-readable inventory. No runtime-completion claim. |
| `P091-001a` | Inventory foundation sources/writers and establish the executable inventory | — | `done` | Completed 2026-09-21: delivered `node:docs/configuration-inventory.v1.json`, the bounded checker, 18 structural/negative-control tests and CI `--verify-current`; mapped the three daemon seams, policy port, bootstrap/toggle writers, Agora, Node UI, four first-slice cases and minimum Python/Arca/Flow bindings. Pending/partial inventory states remain explicit. |
| `P091-001b` | Inventory remaining module-local and record-backed controls | — | `done` | Completed 2026-09-21: the common inventory covers production Python loaders, workflow record fields, daemon/UI CLI, reviewed environment inputs, launch projections, the operator-storage non-setting and named retirement owners. This does not turn domain resources into settings. |
| `P091-002` | Freeze shared contracts under resolved operator choices | `P091-001a` | `done` | 2026-09-21 follow-up closes Review 283's contract-only gaps: measured five-owner/four-case corpus and finite budget boundaries; executable retained replay/detail-mode and disclosure relations; predicted values, exact approval/replan, durable-data attempt/receipt and old/new/third/no-op recovery vectors. See the Node freeze evidence map below. Existing 21 schemas, 20 positive/6 conditional-negative vectors, Rust/Python DTOs, Schema Gate and five-operation registry remain synchronized. The bounded reference model is not P091-003's production resolver; disk/crash/cross-process acceptance stays with P091-006/007/013. No route, writer or component application is enabled; P091-005a remains mandatory. |
| `P091-003` | Implement pure source-aware resolution over reused JSON primitives | `P091-002` | `partial` | 2026-09-21 logging checkpoint: production `configuration-core` resolver folds immutable retained inputs through an observed `json-utils` primitive; default/base/operator/invocation precedence, values/detail parity, `/logging/level` plus `/logging` evidence, historical replay and in-path budgets pass. See the Node evidence note below. Review 284 additionally verified bounded preflight, child-closed structural provenance and ancestor replacement barriers. 2026-09-25 retirement-policy checkpoint: `configuration-core` owns the owner-neutral `SourceAdmissionPolicy` port and `resolve_admitted_ordered_json`, which admit every selected source after preflight and before any fold; the daemon owns `RetiredMiddlewareSourcePolicy` over the same predicate as its legacy loader guard. 2026-09-25 Step 3 checkpoint: the daemon's read-only `logging.level` seam admits the node scope before any read, acquires the legacy node configuration files through a confined, bounded reader with two agreeing passes and a finite `source-conflict` retry budget, and resolves them with the production `DaemonLoggingPort` and the retired-middleware policy bound in production; `ResolvedSnapshot` answers describe, read and explain from one resolution identity. Remaining: general domain dependency evaluation, acquisition for other scopes and owners, and bootstrap/materialization separation beyond this read seam. No route, writer, apply or read-time mutation. |
| `P091-004` | Bind descriptors, admission and domain derivation ports | `P091-002` | `partial` | Reuse registry sealing/CAS and explicit unresolved constraints with separate identity axes. First-slice owners retain validation/merge policy, P085 and sidecar semantics. Withdrawal with unchanged source bytes invalidates new resolution/admission but preserves historical explanation; offline admission never inferred from file presence. 2026-09-25 checkpoint: the first production owner port, `DaemonLoggingPort`, validates `logging` with the typed daemon vocabulary under an owner-issued descriptor admission, replacing the test fixture on the Step 3 seam. Registry sealing/CAS, withdrawal semantics, offline admission and the remaining first-slice owners are open. |
| `P091-005` | Build scoped read/explain adapters and deliver the offline helper | `P091-003`, `P091-004` | `todo` | Rust, P080 and retained HTTP share resolution-bound DTOs; thin non-UI Python facade validates responses, has no fallback. Deliver/install/pin the one-shot Rust helper with bounded structured I/O and missing-binary/version refusals; support injected/exported snapshots. Bounded carrier/projection/aggregate fixtures pass. New routes remain disabled pending P091-005a. |
| `P091-005a` | Pass the named security boundary fixtures before exposure | `P091-005`, `P091-006` | `todo` | All eight `config-security-*` fixtures cover relevant transports/offline/export paths; instrumented denial precedes source acquisition. Route flags do not grant scope or operator authority. No UI/compatibility adoption or enabled new API without this proof. Later adapters require equivalent coverage. |
| `P091-006` | Implement shared targets, predicted-value plans and durable commit | `P091-003`, `P091-004` | `todo` | Reuse owner/stem and explicit domain targets; preserve 80/90 lexical order and legacy 90 common-file case. Sparse patch/reset retains unrelated values and empty `{}`. Plans predict every affected effective value and derive shadowing. Affected/unrelated/unclassified conflict diagnostics and bounded replan without stale authorization are tested. Source membership, bootstrap writers and separate descriptor/constraint changes conflict. Intent/rename/outcome ordering, old/new/third/no-op recovery, durable failure and no pre-outcome apply are tested behind the exposure gate. |
| `P091-007` | Bind application identity, consumption and lifecycle recovery | `P091-006` | `todo` | Reuse supervisor/daemon control and S028 facts/projections. Per-instance `activation/generation` binds a durably admitted resolution (commit or observed-source admission); provisioned, acknowledged, pending, rejected and invalidated remain distinct. `config-time-expiry-between-phases` and controlled-clock edge cases prove fresh current-use checks before apply/retry/recovery; expiry yields `constraint-conflict` / `constraint-expired` and `application-rejected` without effects, preserving replay and save facts. Pre-channel scoped provisioning, restart fencing and idempotent retry pass without repeating effects or reviving authority. |
| `P091-007a` | Wrap retained middleware on/off and repoint existing callers | `P091-005a`, `P091-007` | `todo` | Preserve the existing toggle/supervisor implementation and domain guards. Repoint handlers/UI/CLI to the shared contract with minimal helper extraction, no bypass writer, dual-file mirror or duplicate apply. Test eligibility, dependencies, operator-stopped, shadowing, saved-not-applied and restart; reads never materialize. Physical source migration remains P091-010. |
| `P091-008` | Project shared contracts into Node UI | `P091-005a`, `P091-007`, `P091-007a` | `todo` | Expose keys, files, projected derivation, source and predicted-value diffs, apply modes and per-instance receipts. No private setting store or implicit pinning; file/GUI changes agree after reload/restart. |
| `P091-009a` | Retain the early Arca non-Flow contract fixture | `P091-002`, `P091-004` | `todo` | Scope/owner/source/definition/run binding, normalization and refusal goldens work without a live UI/control stack or universal plan schema. Do not claim runtime consumption. |
| `P091-009` | Bind workflow configuration to live domain owners | `P091-009a`, `P091-005a`, `P091-007` | `todo` | Live JSON-e Flow case plus retained Arca contract proof use existing definitions/validators and exact revisions. Wrong or ambiguous handlers and schemas refuse. No duplicate workflow store or closed thematic repertoire. |
| `P091-010` | Migrate first-slice sources and readers explicitly | `P091-001a`, `P091-003`, `P091-005a`, `P091-007a` | `todo` | Preview/protected backup/effective-value equivalence cover seeding, toggles, first-slice Python loading, env/CLI and optional legacy 90-to-80 migration. Test restoration against pinned pre-migration effective values and independently current authority; changed descriptors report incompatibility. Preserve factory/domain targets unless separately migrated. No read-time migration/workflow trigger. |
| `P091-010a` | Consolidate remaining configuration loaders and register legacy profiles | `P091-001b`, `P091-003`, `P091-005` | `todo` | Each configuration deep-merge/acquisition copy migrates to shared primitives/contracts or has a named legacy profile with owner/retirement evidence. Include Agora selection/skip-malformed semantics and listed Python copies. No unregistered local configuration merge outside approved seams; unrelated domain JSON patching is not banned. Remaining ordinary-setting gaps block P091-015 promotion. |
| `P091-011` | Prove cross-process and standalone consumption | `P091-004`, `P091-005a`, `P091-007`, `P091-009`, `P091-010` | `todo` | Actual supervised Python and separate-process Rust consumers, plus daemon/Node UI, consume explained resolutions. Cover pre-channel inline/ref snapshots, acknowledgement, host denial/outage without fallback, pinned Rust helper and Python exports/injection. Histories retain descriptor/context evidence and no current-use grant is inferred. |
| `P091-012` | Publish shared manual, component references and HOWTOs | `P091-002`, `P091-005`, `P091-008`, `P091-009`, `P091-010`, `P091-011` | `todo` | Exact keys/sources, four identity names, views, shadowed commits, restore/invalidation and apply modes agree across manual/navigation/CLI/UI. Separate proposed, legacy and supported behavior. |
| `P091-013` | Complete refusal, concurrency and recovery evidence | `P091-005a`, `P091-007`, `P091-007a`, `P091-008`, `P091-009`, `P091-010`, `P091-011` | `todo` | Every failure row has retained executable evidence, including journal/file crash points, host-seed races, descriptor withdrawal/expiry, clock failures, shared-file conflict classification and replan, no-op/third-version recovery, secret redaction and evicted replay inputs. |
| `P091-014` | Retain the four-case operator slice and synchronize evidence | `P091-011`, `P091-012`, `P091-013` | `todo` | All cases complete locate/explain/edit/apply/restart/reset through files and interfaces. Update `node:docs/implementation-ledger.toml`, regenerate via `node:tools/generate-implementation-ledger.py`, reconcile `node:docs/MVP.md` for affected scope. Record usability obstacles, not universal cognitive-load reduction. |
| `P091-015` | Close broad coverage and enforce drift/promotion gates | `P091-001`, `P091-010a`, `P091-014` | `todo` | `check-configuration-inventory.py --verify-current` and `check-config-source-boundaries.py` run in Node `.github/workflows/docs.yml`; `--promote` rejects unfinished required settings. Every ordinary durable setting has file-backed shared control; bootstrap/non-setting exceptions stay narrow. Reconcile ledger, generated view, affected MVP/manual coverage and schema indexes; hidden ordinary stores or partial same-surface ledger rows prevent done. |

#### P091-002 implementation evidence — 2026-09-21

The **contract-only freeze is complete** after the 2026-09-21 follow-up. Review 283
correctly rejected the earlier inventory-only/projection-only evidence. Its gaps
are now closed by the
[Node gate-to-evidence map](https://github.com/diapod/node/blob/master/docs/audits/P091-002-FREEZE-EVIDENCE.md),
with executable relation tests, native semantic-owner checks and retained corpus
measurements. At P091-002 closure the logging replay/derivation model was explicitly
a bounded freeze specification rather than a production resolver. The later
P091-003 checkpoint below replaces that test-local algorithm; no runtime adoption
is claimed.
`node:configuration-core` owns validated addresses, closed enums, four distinct
identity types and domain-tagged canonical preimages, safe counters, bounded JSON
admission, deterministic target selection, current-use/withdrawal checks,
application and commit-phase relations, conflict classification and typed DTOs.
Pure generation-fenced allocation/receipt and byte-observation recovery relations
now have executable vectors; host durability and concurrent CAS remain later work.
Its dependency guard excludes host, daemon, filesystem, network, database, UI and
clock authority in production dependencies; test-only Schema Gate is intentionally
allowed, along with the existing mechanical `json-utils` test oracle. Finite
structural ceilings are qualified against the five-owner/four-scenario corpus,
64-source sizing model and exact boundary tests. Native P085 composition preserves
its own digest and refusal semantics. Inline/reference carriers bind typed detail,
canonical size and digest; missing retained detail is explicitly unavailable.

The Node protocol tree carries the common schema plus twenty exact artifact and
request/response schemas. Schema Gate embeds them with positive fixtures and six
conditional negative controls. Rust decodes, re-encodes and Schema-Gate-validates the same twenty vectors; the thin
Python decoder consumes the shared launch/offline DTO, requires exact scope and
resolution bindings, propagates typed refusal and has only an injected reader.
`configuration-first-slice.v1.golden.json` records the full address, owner,
sources, writers, precedence, validator, resolver, application mode, legacy
profile, retirement owner, evidence and verification command for logging,
middleware enablement, separate Flow and Arca owner entries, and the P085
Inquirium limit case. These five owner records cover four scenarios and remain
inventory evidence, not domain resolution or application acceptance.

The [Node review record](https://github.com/diapod/node/blob/master/docs/audits/REVIEW-283-CONFIGURATION.md)
records all CR-283 dispositions and independent fixes. Source-set identity now
excludes raw-byte CAS digests and retained-storage locators; DTOs preserve
missing versus explicit null, invalidation is sticky, generations cannot regress,
post-replace bookkeeping is independent of plan expiry, and Python snapshots are
recursively immutable. URN resolution and bounded verification capture have
regression coverage.

Capability Registry records all five operation identities with the exact
dispatch/host-route/human-registry flags decided above. Registration is not
availability: no daemon route or writer was added. The Node implementation ledger
therefore remains `partial` and `out-of-scope` for hard MVP, and P091-005a remains
the non-bypassable prerequisite for route exposure.

#### P091-003 logging resolver checkpoint — 2026-09-21

The first bounded P091-003 checkpoint is implemented. `configuration-core` now
owns serializable immutable retained inputs and one production ordered-JSON
resolver. It verifies exact source, descriptor, context, normalization, resolver
and domain-port bindings, then folds sources through the existing `json-utils`
mechanism into a private accumulator. `json-utils` gained a fallible,
domain-neutral structural observer; its existing public merge functions reuse
the same walk with instrumentation disabled and preserve their value, stable
map-order behavior and direct subtree moves.
The dependency guard continues to exclude host and domain runtimes.

The shared path resolves the four logging sources — compiled default, base file,
operator file and explicit invocation override — and gives identical values,
identities and semantic refusals in `values-only` and `with-derivation` modes.
The optional observer materializes bounded contributor evidence for
`/logging/level` and `/logging`. Its exhaustion reports unavailable detail while
preserving the validated value. Retained snapshots replay after separate current
source/descriptor changes; missing, substituted or revision-incompatible inputs
refuse. Source, retained-byte, structural, work, pointer, contributor, dependency,
response and inline-detail limits are enforced by the actual resolver path.

Review 284 corrected input preflight ordering and structural explanation: a
selected subtree now includes all child dependencies, preserves multiple decisive
sources and accounts for ancestor replacement. Descriptor scopes/references and
owner evidence bindings are checked; unimplemented domain dependencies yield
unavailable detail. These corrections and per-finding dispositions are recorded
in [Node Review 284](https://github.com/diapod/node/blob/master/docs/audits/REVIEW-284-CONFIGURATION.md).

The complete command/evidence map is the
[Node P091-003 logging resolver slice](https://github.com/diapod/node/blob/master/docs/audits/P091-003-LOGGING-RESOLVER-SLICE.md).
This is intentionally not P091-003 completion. The logging owner in current tests
is a pure fixture port mirroring the daemon vocabulary; P091-004 still owns the
production owner binding and remaining domain ports. General domain dependency
evaluation, acquisition, bootstrap/materialization, routes, writers, application
and runtime consumption also remain open. P091-005a still blocks exposure.

#### P091 Step 3 read-only logging seam — 2026-09-25

Step 3 now runs on production parts rather than test fixtures, still without any
route, CLI, HTTP or P080 operation. The daemon's `configuration_host` module:

- admits the requested scope first; any scope other than the local node refuses
  as `denied` before a single enumeration or read;
- acquires the compiled default, the legacy node configuration files under a
  named `daemon-node-config-dir:legacy-v1` selection profile, and the explicit
  invocation override, through a confined reader that refuses symbolic links and
  other non-regular entries and bounds every file by the resolution budget;
- reads every source twice per attempt and accepts only agreeing passes, retrying
  a finite number of times before refusing with `source-conflict`; this detects
  cooperative and most accidental changes but is not an atomic snapshot against
  arbitrary editors;
- builds one immutable source selection in `configuration-core` and resolves it
  with the production `DaemonLoggingPort` and the retired-middleware
  source-admission policy, so the retirement guard is bound on this path; and
- answers `describe`, `read` and `explain` from one `ResolvedSnapshot`, whose
  identity never changes; changed bytes require a new acquisition.

`explain` supports the `resolved` view, derivation detail limited to the address
subtree, and disclosure narrowed by the host grant; its responses pass Schema
Gate. The `declared` and `active` views refuse as unsupported until per-source
declaration projection and application receipts exist. An admitted address
without a value refuses as `missing-key`, because the contract's value states are
`present`, `redacted` and `unavailable`.

The new path is deliberately stricter than the legacy loader: duplicate JSON keys,
symbolic links and non-regular entries refuse. Tests use the legacy loader only as
the value oracle over prepared fixtures and prove the Step 3 checkpoint: fixture
precedence, contributor roles for `/logging/level` and `/logging`, a same-valued
operator declaration kept explicit, an old explanation surviving a later source
change, exact refusals, zero reads for a denied scope, and an unchanged data
directory after inspection. The evidence map is
`node:docs/audits/P091-STEP-3-LOGGING-READ-SEAM.md`.

The checkpoint exposed a contract gap: a descriptor document carried its own
`descriptor/digest`, but nothing related it to the digest its revision binds, and
the resolver checked only the latter. The
[descriptor identity amendment](#amendment-descriptor-identity-2026-09-25)
closes it by removing the self-digest from the document.

#### P091-003 retirement-policy checkpoint — 2026-09-25

The retirement policy is now a separate, owner-supplied source-admission port, as
required by the three-entry-seam inventory above. `configuration-core` defines the
refusal-only `SourceAdmissionPolicy` and `resolve_admitted_ordered_json`. Every
policy inspects every selected, present source after resolver preflight has
bounded it and its content digest has been verified, and before the first fold,
so a later overlay cannot hide a retired root or nested executor, and a
substituted input stays unavailable instead of becoming a policy refusal. A refusal names the source and the policy and carries a
bounded machine code; both detail modes refuse identically. The core knows no
retired executor names or daemon error types.

Admission is a current-use gate, not part of resolution identity. Pinning a
policy revision in `resolution-inputs` would expand the accepted contract, whose
schema is closed; the retained inputs and resolution identity are therefore
unchanged, and historical replay may run through `resolve_ordered_json` without
current policies.

The daemon owns `RetiredMiddlewareSourcePolicy`. It walks the same single
predicate as the legacy `reject_in_config` guard, charging one work step per
visited node, and a parity test keeps the two paths in agreement. An empty retired
root still refuses; unrelated product HTTP configuration does not.
`reject_in_package_manifest` stays at its separate package-admission boundary. No
production resolution path calls the policy yet: binding it together with host
acquisition belongs to the remaining P091-003/004 seams.

### Dependency-ordered slices

Start P091-001a and P091-001b concurrently as audit work; only the bounded foundation
audit blocks P091-002. Contract freeze opens P091-003/004. Read and change adapters
follow; their named security gate opens exposure and the retained on/off wrapper.
P091-009a's Arca contract fixture can run before the live control/UI stack.
P091-007/007a, P091-008 and P091-009 then converge with first-slice migration on
P091-011's actual process evidence. Design Python/launch DTO fixtures during the
foundation, not for the first time at cross-process acceptance.

Use the [P091-001 guidance](#p091-001-inventory-sources-writers-and-semantic-ownership)
for the entry contract, seam/writer audit and first-slice evidence. Then use the
[four implementation steps](#four-implementation-steps-after-the-foundation-inventory)
for candidate algorithms, data structures and verification checkpoints. The
read-only logging checkpoint does not replace any task's full completion gate.

P091-010a consolidates remaining loaders independently of first-slice acceptance.
P091-014 closes that coherent operator stage; P091-015 additionally requires the
complete inventory and broader adoption. No task requires finishing all of P085,
P090, Sensorium, Room or Corpus; reuse the exact existing contracts needed by the
selected cases and preserve their separate implementation claims.

## Resolved 2026-09-06

The operator selected A/A/B, refined the common filename to preserve ordinary
lexical ordering, and chose to wrap the existing middleware on/off implementation.
These are adopted decisions; alternatives are retained below as history, not
active implementation branches.

### OQ-01: One reference resolver and a thin Python client — A

Managed Python uses Rust-host operations/snapshots. Standalone resolution uses
the same Rust core through an installed one-shot helper; Python without Rust can
consume an exported or injected snapshot. Fresh composition requires that helper
or a new export. Local getters and unit tests need neither daemon nor RPC.

Alternative B, a native Python resolver, was not selected: it would support
independent Python-only composition at the cost of another semantic implementation
and permanent parity tests. No implicit fallback to it is allowed.
Affected tasks: P091-002/003/005/010/011.

### OQ-02: Reuse existing owner-specific workflow declarations — A

Use existing declaration mechanisms, identities, revisions and validators.
JSON-e Flow remains the initial concrete example, not the meaning of workflow:
the additional audit established the broader definition/handler boundary and
Arca's declarative orchestration path (Decision 13).

Alternative B, a new `config/workflows/` values wrapper in V1, was not selected.
The choice does not exempt record-backed behavioral controls from file-backed
configuration; their migration is explicit rather than a duplicate workflow store.
Affected tasks: P091-002/003/006/009/010/012.

### OQ-03: Per-component operator fragments, with common fallback — B

Use `90-operator-<component-name>.json`, for example `90-operator-arca.json` and
`90-operator-sensorium-workbench.json`. Reuse existing module identity/owner
bindings and domain-specific write targets as detailed in Decision 3.
The common fallback is **`80-operator.json`**, as subsequently requested by the
operator: existing lexical ordering then places it before detailed files.

The original common-only option A and initial `90-operator.json` fallback are
superseded. The intermediate special-ordering idea is also superseded; no custom
comparator is needed. Existing legacy files migrate explicitly with source/value
comparison. Fallback is a target-selection result, not a way around invalid
ownership or failed writes. Affected tasks: P091-002/006/008/010/012.

### Middleware on/off: retain implementation behind the P091 wrapper

The operator chose implementation reuse with minimal helper extraction and
call-site refactoring: the shared contract controls durable `enabled`, while the
existing middleware mechanism and supervisor retain execution ownership
(Decision 8). Neither a permanently independent on/off writer nor a replacement
lifecycle engine was selected. The existing file may remain a declared legacy
source until explicit migration; this choice does not reopen OQ-03 or require
an immediate file move. Affected tasks: P091-002/007/007a/008/010/013.

### Review integration: explicit identities and reuse boundaries

On 2026-09-06 the operator accepted the follow-up review integration: four distinct
identity axes; retained replay inputs with lazy derivation; all five operations in
the scoped registry with writes non-dispatchable; shared temporal persistence and
explicit intent/replace/outcome recovery; predicted effective values for shadowed
commits; descriptor invalidation and owner-issued offline admission context.
Retain empty shared files on reset and test effective-value restoration, not just
byte restoration. Named security evidence precedes new interface exposure.

The follow-up review on 2026-09-06 made time-dependent current-use admission
explicit at commit/apply/retry/recovery without changing historical replay.
Expiry uses the existing `constraint-conflict` refusal family and
`application-rejected` state. Shared-file conflicts receive host-proven reason
codes; automatic replan does not transfer write approval. The two read operations
join the curated human registry, while operator writes remain machine-registered
and separately documented. These refinements do not promote implementation status.

The dated source/workflow audit moved to Node. This refines, rather than reopens,
A/A/B and the retained on/off wrapper. Earlier suggestions of one counter, a
blanket environment ban, unregistered write operations or new control-directory
stores were not selected. Reuse precedents do not make these P091 mechanisms
implemented. Affected tasks are defined in the updated tracker above.

## Contract acceptance of the P091-002 freeze (2026-09-25)

The operator accepted the contract frozen by `P091-002`, in the bounded P092 sense:
the acceptance unit is the Node ledger row
`node:docs/implementation-ledger.toml#file-backed-configuration-contract-foundation`
and ends at that row's stated exclusions. It covers the identity and revision
vocabulary, finite budgets, canonical JSON admission, detail-mode and disclosure
relations, plan approval and bounded replan, generation-fenced attempt, receipt
and recovery relations, the Rust/Python/launch/offline DTOs, the five registry
identities, and the twenty `config-*` schemas that row lists, as evidenced by
`node:docs/audits/P091-002-FREEZE-EVIDENCE.md`.

The acceptance does not promote this proposal, does not accept any item in the
row's `next_steps`, and claims no runtime adoption: owner ports, domain
dependency evaluation, host acquisition, routes, writers, filesystem effects,
application, and UI remain unaccepted and unimplemented. `P091-005a` remains
mandatory before any route exposure. A material expansion of the frozen contract
returns to `draft` until separately accepted. The ledger records this decision as
`p091-configuration-contract-freeze`.

### Amendment: descriptor identity (2026-09-25)

The operator amended `config-setting-descriptor.v1` in place and accepted the
amendment as a separate decision, recorded in the ledger as
`p091-descriptor-identity-amendment`. Nothing was released and no consumer outside
the Node fixtures and tests used the removed field, so no `v2` is introduced.

The Step 3 checkpoint showed that the frozen descriptor carried two near-identical
identities. The document held its own `descriptor/digest`, the descriptor revision
bound a digest of the whole retained document, and the resolver verified only the
second. Producers and tests had already filled the two differently.

The amendment keeps exactly one identity:

- a descriptor document carries no digest of itself; `descriptor/digest` is removed
  from `config-setting-descriptor.v1`, and a document that still contains it is
  refused by Schema Gate and by the resolver (`descriptor-embeds-digest`);
- the semantic identity is `descriptor_digest(document)`, the SHA-256 of the
  canonical JSON preimage
  `{"domain": "orbiplex/config-descriptor/v1", "payload": document}`, in the
  naming style of the other P091 identity domains;
- a descriptor revision binds that digest from outside, and the resolver
  recomputes it from the retained document and refuses a difference as
  `descriptor-digest-mismatch`; and
- `descriptor-set/id` continues to bind the digest together with the descriptor
  ref, address, admission evidence, and generation, while exact file bytes stay a
  separate concern from this semantic identity.

A `describe` answer therefore no longer carries a digest. A client that pins a
revision recomputes `descriptor_digest`; if that becomes inconvenient, the right
change is an envelope in the `describe` response, not a digest inside the
document. The P091-002 budget measurements were regenerated for the smaller
descriptor model, and the identity golden vectors changed with the descriptor
digest. The rest of the frozen contract and its exclusions are unchanged.

## Open Questions

No unanswered operator choices remain from OQ-01/02/03. Engineering closure and
evidence-driven extensions below remain separate from those resolved decisions.

### Engineering closure items, owned by P091-002

The reuse audit resolves the earlier route-family uncertainty: reuse P080 host
capability dispatch for admitted reads and existing operator control for
changes/application. The five-operation flag matrix and candidate DTO family are
specified and registered with shape fixtures; the 2026-09-21 follow-up freezes
relational evidence and measured first-slice contract budgets. Deployment capacity
and runtime adoption remain separate acceptance work.
Workflow-kind/definition and Flow instance bindings are available; Decision 13
defines their distinct configuration ports under resolved OQ-02 A.

Freeze finite source/file/byte/depth/derivation/output/history budgets, the common
JSON admission profile and descriptor application modes using the inventory and
boundary tests. These require measured engineering defaults, not an unsupported
promise that every setting reloads live. Configuration inspection cannot disable
the host's structural safety guards; do not inherit unbounded helper reads.

### Post-first-slice, evidence-driven

1. Is single-file commit sufficient for common operator workflows, or is an
   activation-group transaction justified by observed multi-component changes?
2. Which explanation details belong in the default CLI view versus an expanded
   derivation view? Retain the full bounded data contract in either case.
3. Do operator trials justify additional editable formats? JSON is sufficient for
   V1; preserving comments or adding a DSL is not a prerequisite for uniformity.

## Next Actions

1. Complete the remaining P091-003 domain dependency work and acquisition for
   other scopes and owners; the Step 3 read seam for `logging.level` is done and
   binds the retirement policy in production. Then bind the remaining P091-004
   owner ports from the completed inventory and contract
   freeze; extend existing primitives, supervisor provisioning and host bridges
   before implementing UI.
2. Complete the four-case slice with real cross-process consumption, then expand
   by inventory rather than
   declaring that every subsystem became configurable through one demonstration.

### P091-002 freeze gate

P091-002 is done only when the P091-001a evidence freezes the preceding contract
as executable data: address/owner/stem rules and 80/90 ordering; separate source,
descriptor, resolution and activation identities with exact CAS/digest preimages
and safe counter ranges; closed views/source classes/application/refusal enums and
transition tables; descriptor withdrawal, time-dependent current-use gates and
explicit offline admission; retained
replay inputs, both detail modes, per-pointer/aggregate derivation and disclosure;
predicted-value plans, classified source conflicts, bounded replan without reused
approval, source-membership/host-writer conflicts and crash-safe
single-file outcomes; typed Rust/Python/launch/offline DTOs; all five registry
operations with read dispatch versus operator-only host routing and explicit
`docs.human-registry` choices; finite
source/file/byte/depth/history/output budgets, canonical JSON admission and the
16 KiB inline ceiling. Positive/negative Schema Gate and pure-core fixtures cover
these relations, including conditional-required fields; local source validation
remains explicitly local. Register the exact request/response/plan/receipt schemas
with P091 basis metadata, synchronize mirrors/index/COVERAGE and the two curated
human registry tables, pass `make check-capability-registry`, and record exact
contract-only coverage in `node:docs/implementation-ledger.toml`, regenerate via
`node:tools/generate-implementation-ledger.py` and reconcile affected
`node:docs/MVP.md` scope. P091-005a remains mandatory before route exposure:
contract freeze does not claim runtime adoption or replace security evidence.
