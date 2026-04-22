# Proposal 048: Sensorium OS Connector Action Classes

Based on:
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/schemas/sensorium-directive.v1.schema.json`
- `doc/schemas/sensorium-observation.v1.schema.json`
- `doc/schemas/sensorium-directive-outcome.v1.schema.json`
- `doc/schemas/sensorium-os-error-codes.v1.schema.json`

## Status

Draft

## Date

2026-04-19

## Executive Summary

The Sensorium OS connector is the Node's **generic gateway to local
operating-system actions**. It is not a gateway to any particular program
family and MUST NOT encode semantics of any specific tool. A program
invocation is simply a triple — executable path, argv, environment — bounded
by policy.

Proposal 045 established a single reference action (read-only process spawn).
That shape is no longer sufficient: real-world enaction scenarios require
scripts, filesystem writes, and outbound network calls. Rather than let
specific programs leak their semantics into the connector, this proposal
defines a **small closed catalog of action classes** from which concrete
allowlisted actions are composed. Each class describes a category of OS
effect, independent of which program realizes it, together with the
enforcement envelope the connector applies to every member of that class.

The core maxim is:

> The OS connector knows about *processes*, *files*, *sockets*, *bytes*, and
> *time*. It does not know about any program. Program semantics belong to the
> caller and to the action-declaration author, never to the connector.

Action declarations are authored by the node operator by editing the OS
connector's configuration file. Once declared there, they become the
connector's **known action catalog**: the connector advertises the catalog
through its `middleware-module-report`, `sensorium-core` picks it up as the
resolution map for `action_id`, and consumers address each action by its
stable identifier without knowing its executable path, class, or
enforcement envelope. A production deployment MAY additionally bind a
host-owned overlay to restrict or extend the connector-declared catalog;
without an overlay, the connector configuration is the single source of
truth.

This means that the **operator-authored declaration** is the place where
concrete local-action semantics live. A declaration may say that
`story009.git.commit-signed` is realised by a particular script with a
particular argv shape, environment, timeout, write root, and result
contract. The connector implementation still remains program-agnostic: it
renders argv, enforces the selected class envelope, exposes only the
scoped grants named by the declaration, and captures results. It does not
contain Git-specific code, model-specific code, or any switch on domain
program names.

This proposal is an additive refinement of proposal 045's connector contract.
It does not change the four-lane Sensorium I/O model, it does not change the
`sensorium-observation.v1` or `sensorium-directive.v1` schemas, and it does
not grant any new capability to consumers.

## Motivation

Across Orbiplex workloads the OS connector is asked to mediate actions with
materially different risk and capture shapes:

- reading public sources through short-lived one-shot processes,
- running bundled scripts that wrap local models, archivers, or analyzers,
- writing files into scoped workspaces,
- producing captured artifacts too large for a JSON envelope,
- making outbound network calls under bounded hosts/bytes limits.

Handling each as a unique action id forces the connector to encode
per-program policy and produces an unbounded, auditor-hostile surface. On
the other hand, a single "spawn" action is too coarse: its envelope must be
the **intersection** of every possible action's constraints, which forces
callers into awkward workarounds and defeats policy.

Action classes are the middle position: a **small, closed set** of generic
categories, each with its own enforcement envelope. A concrete allowlisted
action names exactly one class and contributes program-level parameters
(path, argv shape, caps). The connector enforces the class invariants; the
allowlist author names the concrete tool; the caller supplies parameters.
No layer needs to know what the program *does*.

## Design Principles

- **Program-agnostic.** No action class references any specific binary,
  script, protocol, file format, repository kind, or vendor. Examples in
  this proposal deliberately use placeholders (`<binary>`, `<script>`).
- **Closed catalog.** The class catalog is small and changes only by
  proposal. New classes are added when a genuinely new enforcement envelope
  is required, not when a new tool is introduced.
- **Composable through allowlist, not through class arithmetic.** A concrete
  allowlisted action names exactly one class. If a workload needs combined
  effects (e.g. write + network), it picks the class whose envelope
  permits both; it does not union classes at call time.
- **Connector enforces, core resolves, caller parameterizes.** The
  connector applies the class envelope per action. `sensorium-core` resolves
  `action_id` to one allowlist entry. The caller supplies typed parameters
  constrained by that entry's `parameters_schema`.
- **Default deny.** Anything not expressly permitted by the named class and
  the allowlist entry is denied by the connector. This includes, but is
  not limited to, interactive terminals, privilege escalation, unscoped
  writes, and unbounded network calls.
- **Bytes stay out of the directive envelope.** Large outputs are returned
  as artifact references via the Sensorium artifact lane, never inlined
  into the directive result or an observation.

## Action Class Catalog

Each class defines:

- **Effect profile** — what kinds of OS effect the class permits.
- **Enforcement envelope** — what the connector MUST apply to every action
  of this class.
- **Capture shape** — what the connector returns to `sensorium-core`.
- **Baseline incidental effects** — the minimum the connector declares in
  outcomes and observations; allowlist entries MAY declare additional
  effects but MUST NOT subtract from the baseline.
- **Baseline sensitivity class** — the minimum `sensitivity.class` the
  connector attaches to emitted observations; allowlist entries MAY raise
  it.

Unless noted otherwise, every class imposes this **universal baseline**:

- no controlling terminal, no TTY attach, stdin closed;
- no privilege escalation, no setuid/setgid elevation, no capability grants;
- no interactive prompts, no password helpers, no credential plumbing;
- explicit working directory confined to an allowlisted root;
- explicit, curated environment (no inheritance by default);
- wall-clock timeout enforced by the connector;
- stdout and stderr bounded by size caps; overflow is truncated and
  flagged in the result;
- exit code, duration, and argv recorded in the outcome;
- unknown or unresolved `action_id` is a hard reject before any spawn.

### C1: `read-only-spawn`

- **Effect profile.** Process may read from the filesystem and system-level
  interfaces it is explicitly granted. No filesystem writes outside a
  per-invocation scratch area the connector owns. No outbound network
  calls. No ingress listeners.
- **Enforcement envelope.** Writable filesystem path is a connector-owned
  temporary directory, removed after the action. Network namespace or
  equivalent isolation MUST be configured to refuse egress; if platform
  support is unavailable, the allowlist entry MUST document the gap.
- **Capture shape.** stdout, stderr, exit code, duration; optionally a
  structured JSON payload parsed from stdout when the allowlist entry
  declares `stdout_format: json`.
- **Baseline incidental effects.** `disk-access-timestamp-update`.
- **Baseline sensitivity class.** `operational-sensitive`.

### C2: `allowlisted-script`

- **Effect profile.** Same as `read-only-spawn`, with the additional
  restriction that the executable MUST be a script file resolved under a
  connector-controlled allowlist of script roots. The interpreter is
  named by the allowlist entry; shell invocation is forbidden.
- **Enforcement envelope.** Before spawn, the connector resolves the
  script path, rejects any path outside the allowlisted roots, and
  rejects symlinks that escape those roots. Parameters are passed as
  **canonical JSON argv** (one `--params-json <value>` argv pair), never
  through shell interpolation. Optional content-hash check (`sha256`) MAY
  be declared in the allowlist entry; when declared, the connector
  verifies it before spawn.
- **Capture shape.** As in `read-only-spawn`. When `stdout_format: json`
  is declared, the parsed payload MAY include a `pointers` object whose
  keys are enumerated by the allowlist entry's `result_pointer_fields`.
  The connector propagates only those keys into the outcome summary.
- **Baseline incidental effects.** `disk-access-timestamp-update`.
- **Baseline sensitivity class.** `operational-sensitive`.

### C3: `scoped-fs-write`

- **Effect profile.** Process may write within a bounded filesystem subtree
  declared by the allowlist entry. No writes outside that subtree. No
  outbound network calls.
- **Enforcement envelope.** Write root is an absolute path in the
  allowlist entry; the connector enforces that path as a real,
  canonicalized directory (no symlink escape, no parent traversal). Per-
  invocation size cap (total bytes written) and per-file size cap are
  declared in the allowlist entry and enforced by the connector via a
  sandbox mechanism appropriate to the platform (overlay, seccomp,
  landlock, sandbox-exec, or equivalent). When no such mechanism is
  available the connector MUST refuse to execute this class.
- **Capture shape.** In addition to stdout/stderr, the connector records
  the list of files touched (paths relative to the write root, byte
  counts, and content hashes) in the result.
- **Baseline incidental effects.** `disk-access-timestamp-update`,
  `local-filesystem-write`.
- **Baseline sensitivity class.** `operational-sensitive`.

### C4: `egress-network-spawn`

- **Effect profile.** Process may make outbound network calls to a
  declared host allowlist. No filesystem writes outside a connector-owned
  scratch area. No ingress listeners.
- **Enforcement envelope.** Host allowlist is a set of `(host, port,
  protocol)` tuples in the allowlist entry. Egress is mediated by a
  platform-appropriate mechanism (per-process firewall, network
  namespace + reverse proxy, or equivalent). DNS resolution MUST respect
  the same allowlist. Total egress byte cap and per-connection byte cap
  are declared by the allowlist entry and enforced by the connector.
- **Capture shape.** As in `read-only-spawn`, plus a network transcript:
  list of `(host, port, protocol, bytes_sent, bytes_received,
  duration_ms)` tuples. No payload bodies are captured in the directive
  envelope; any body the caller needs MUST be saved as an artifact.
- **Baseline incidental effects.** `network-egress`.
- **Baseline sensitivity class.** `operational-sensitive`.

### C5: `artifact-producing-spawn`

- **Effect profile.** Process produces captured artifacts too large or
  binary to carry in the directive result envelope. Artifacts are
  written into a connector-owned artifact scratch area, then promoted
  to the Sensorium artifact lane with content-addressed identifiers.
  No writes outside the scratch area. No network access.
- **Enforcement envelope.** Scratch area is connector-managed and
  per-invocation. The allowlist entry declares `max_artifact_count`,
  `max_artifact_bytes_per`, `max_artifact_bytes_total`, and the set of
  permitted `media_type` values. The connector refuses promotion of any
  artifact whose declared or sniffed media type is outside the set.
- **Capture shape.** Exit code, stdout (small, capped), stderr (small,
  capped), and an ordered list of artifact references in the form
  required by `sensorium-observation.v1 / evidence/refs`
  (content-addressed identifier, role, optional media type, size).
- **Baseline incidental effects.** `disk-access-timestamp-update`,
  `artifact-lane-write`.
- **Baseline sensitivity class.** `operational-sensitive`.

### C6: `composed-spawn`

- **Effect profile.** Permits a declared subset of effects from classes
  C1..C5 combined within one action. This class exists so that genuinely
  multi-effect actions have a single, explicit declaration point rather
  than implicit widening of a narrower class.
- **Enforcement envelope.** The allowlist entry MUST declare a
  `composed_effects` array naming the permitted effect categories from
  `{read, scoped-fs-write, egress-network, artifact-produce}`. For each
  named category the corresponding parameters from C1..C5 MUST be
  supplied (e.g. `write_root` if `scoped-fs-write` is named,
  `network_allowlist` if `egress-network` is named). Sensitivity
  baseline is the **strictest** of the included classes. Incidental
  effects are the **union** of the included classes' baselines.
- **Capture shape.** Union of the capture shapes of the named
  categories.
- **Baseline incidental effects.** Union of baselines of named
  categories.
- **Baseline sensitivity class.** Maximum (strictest) of included
  classes.

### C7: `operator-gated-spawn`

- **Effect profile.** Reserved identifier for actions that require an
  explicit, per-invocation operator approval in addition to the usual
  allowlist decision. Not part of the default v1 enforcement catalog.
- **Enforcement envelope.** Out of scope for this proposal. Reserved so
  that future operator-in-the-loop actions have a named home without
  reshaping the class hierarchy.

## What the Class System Deliberately Excludes

- **Interactive processes.** No class permits stdin, TTY, or prompts.
- **Long-running services.** No class permits a process that outlives
  the directive. A future class is the proper home, not a special case
  inside an existing class.
- **Privileged execution.** No class permits setuid, setgid, capability
  grants, or sudo-style elevation. If a workload requires privilege, the
  right answer is a different, operator-signed surface — not this
  connector.
- **Unbounded effects.** No class permits writes or network calls
  without size and scope caps enforced by the connector.
- **Program identity.** No class references any specific program family,
  protocol, file format, repository kind, or vendor.

## Action Declaration Shape (class-aware)

An action declaration is authored by the operator in the OS connector's
configuration file. This proposal adds a required `class` field and a
small set of class-specific fields. Existing fields from proposal 045
(`action_id`, `connector_id`, `parameters_schema`, `limits`,
`default_timeout_ms`, `max_timeout_ms`, `connector_incidental_effects`)
remain.

```
{
  "action_id": "<lowercase dotted action id>",
  "connector_id": "<connector module id>",
  "class": "read-only-spawn" | "allowlisted-script" | "scoped-fs-write"
         | "egress-network-spawn" | "artifact-producing-spawn"
         | "composed-spawn" | "operator-gated-spawn",

  "executable": {
    "kind": "binary" | "script",
    "path": "<absolute path>",
    "argv_shape": "<declarative argv template, see below>",
    "interpreter": "<optional absolute path; scripts only>",
    "sha256": "<optional, verified before spawn>"
  },

  "parameters_schema": { ... JSON Schema ... },
  "default_timeout_ms": <integer>,
  "max_timeout_ms": <integer>,
  "limits": {
    "stdout_max_bytes": <integer>,
    "stderr_max_bytes": <integer>
  },

  // Class-specific blocks — present only when the class requires them:
  "script": {
    "allowed_roots": ["<absolute dir>", ...]
  },
  "fs_write": {
    "write_root": "<absolute dir>",
    "max_bytes_total": <integer>,
    "max_bytes_per_file": <integer>,
    "path_pattern": "<optional POSIX-regex relative to write_root>"
  },
  "egress_network": {
    "endpoints": [{ "host": "...", "port": <n>, "protocol": "tcp" | "udp" | "https" | "http" }, ...],
    "max_bytes_total": <integer>,
    "max_bytes_per_connection": <integer>
  },
  "artifact": {
    "max_count": <integer>,
    "max_bytes_per": <integer>,
    "max_bytes_total": <integer>,
    "allowed_media_types": ["...", ...]
  },
  "composed": {
    "effects": ["read", "scoped-fs-write", "egress-network", "artifact-produce"]
  },

  "environment": {
    "inherit": false,
    "set": { "<KEY>": "<value>", ... }
  },

  "signing": {
    "allowed_domains": ["<domain-tag>", ...],
    "key_ref": { "kind": "primary-participant" | "proxy" | "derived", "...": "..." },
    "max_signatures": <integer>
  },

  "result_contract": {
    "stdout_format": "text" | "json",
    "result_pointer_fields": ["...", ...],
    "signal_kind": "<observation signal/kind>",
    "signal_family": "<observation signal/family>"
  },

  "connector_incidental_effects": ["..."]
}
```

The `argv_shape` is a declarative template. The connector substitutes
parameter values by name only; the caller never supplies raw argv. This
eliminates shell injection as a category. The template is intentionally
small:

- each argv element is a separate JSON string; there is no shell string;
- placeholders name directive parameters or connector-provided values;
- structured values are passed only through explicit serializers such as
  `{{params_json}}` or a declaration-defined `{{paths_json}}` value;
- no conditionals, loops, defaults, command substitution, or environment
  expansion are available;
- a declaration that tries to use `sh -c`, unbounded raw argv, or a
  caller-supplied executable path is outside this contract and MUST be
  rejected.

The optional `signing` block does not make the connector a signing oracle.
It describes a scoped, per-directive signer grant under proposal 037:
domains are enumerated, key scope is explicit, and `max_signatures`
bounds use. Authorization and enforcement belong to `sensorium-core` and the
host signer. The OS connector treats any resulting helper material as opaque
process setup; it does not interpret domains and does not sign. For example,
an action declaration MAY allow one signature under `git.commit.v1`; the
script invoked by that declaration knows how to construct the canonical commit
payload and call the scoped signer helper, while the host signer ensures that
no other signing domain or extra signature is available.

## Operator-Editable Action Catalog

The OS connector's configuration file is the **primary home** of action
declarations. The operator adds, removes, or adjusts entries by editing
the file; the connector reloads the catalog on supervised restart. No
source-code change is required to expose a new command set.

The connector validates the catalog at load time:

- each declaration MUST name exactly one `class`;
- each declaration MUST satisfy the class-specific invariants (executable
  path resolvable, script root present for `allowlisted-script`, write
  root present for `scoped-fs-write`, etc.);
- each `action_id` MUST be unique within the connector and MUST match the
  Sensorium action-id pattern;
- each `parameters_schema` MUST be a well-formed JSON Schema;
- each `result_contract.signal_kind` MUST match the Sensorium signal-kind
  pattern.

Declarations that fail validation are rejected at startup; the connector
refuses to run with a partial catalog. This is intentional: a silent
dropped action is a harder operator failure mode than a refusing module.

Per-action result contracts may additionally declare a closed
`result_contract.pointer_fields` list. For such actions, every listed field
MUST be present in the structured JSON result returned by the script. A missing
field is a contract failure, not an optional omission: the connector returns a
structured diagnostic (`result-pointer-missing`) and Sensorium records an
action-invalid observation. This prevents latent corruption where a script and a
role module silently drift on names such as `review_commit` vs
`reviewed_commit`.

### Diagnostic Code Vocabulary

The reference OS connector uses the shared schema
`sensorium-os-error-codes.v1` for operator-facing diagnostic codes. The current
v1 vocabulary is intentionally small and implementation-facing:

- `action-catalog-unauthorized`
- `action-not-allowlisted`
- `script-hash-mismatch`
- `working-directory-forbidden`
- `parameters-schema-invalid`
- `result-schema-invalid`
- `result-pointer-missing`
- `action-timeout`
- `directive-missing`
- `parameters-invalid`
- `script-not-executable`

Free-form diagnostic messages remain useful for humans, but routing,
dashboards, tests, and audit reconstruction SHOULD branch on these stable
codes. Unknown connector families may define their own vocabularies; the
reference OS connector should not grow ad-hoc strings outside this schema.

### Publication path

Once validated, the connector publishes its action catalog through the
standard `middleware-module-report.connector_actions` array (see proposal
045). `sensorium-core` reads the report and builds its
`action_id → declaration` resolution map from it. When a directive
arrives at `sensorium-core`, resolution consults this map; no hard-coded
action table lives in `sensorium-core`.

### Operator Authorization via Sidecar Signature

The operator's act of **editing** the connector configuration and the
act of **authorizing** that configuration to run are separated by
design. Editing produces the effective configuration; authorization
binds that configuration to the operator's participant key through a
detached sidecar signature. Without a valid signature the connector
refuses to expose its action catalog (with a narrow, explicit bootstrap
exception, below).

> **Scope note.** The sidecar-signature + node-signed-factory-bootstrap
> pattern described in this section is **not specific to Sensorium OS
> connectors**. It is a general mechanism for authorizing the effective
> configuration of any Orbiplex module whose behavior is sensitive to
> operator edits — other connectors, role modules, Arca templates,
> ledger policies, and so on. OS connectors are simply the first place
> where the mechanism is mandatory, because the blast radius of an
> unauthorized catalog entry (arbitrary shell invocation) is the
> highest in the system. Other modules MAY adopt the same machinery,
> with the same sidecar schema, the same JCS + sha-256 pipeline, and
> the same node-vs-operator signer distinction; a future proposal can
> generalize the contract and host-side implementation once a second
> consumer appears. This proposal only codifies the rules for OS
> connectors; it does not forbid wider reuse.

#### What is signed

Orbiplex middleware configurations are typically merged from multiple
files — bundled seed defaults, operator overrides, deployment-specific
fragments. At startup the connector performs this merge in memory and
obtains the **effective configuration** as a single canonical JSON
document. This merged document — not any individual source file — is
what the signature covers. Canonicalization uses the same rules as
other Orbiplex signed payloads (RFC 8785 JCS). Any change in the
effective configuration, however small, produces a different hash and
requires re-authorization.

Signing the merged result rather than individual fragments matches the
operator's mental model: they authorize what will actually run, not
one of several contributing files. It also aligns with review flow —
the operator inspects the effective catalog and its hash, not a
diff-of-diffs across sources.

#### Signing key

The signature is produced by the operator's **participant key** — the
same identity used elsewhere to sign operator acts. The connector
never holds or computes the signature itself; it only verifies. The
participant-key binding is what makes the authorization auditable and
distinguishable from any module-local mutation.

#### Sidecar file

The sidecar is a single separate file placed in the node's **active
configuration area** — the writable directory where the node keeps
operator-managed state — **not** in any factory/shipped/read-only
configuration tree that came with the distribution or module package.
Because a connector's effective configuration MAY be assembled from
several sources (base file, per-environment overlays, drop-in
fragments), the sidecar is **not** attached to any one of them — it is
a single artifact that authorizes the **merged effective
configuration** as a whole, placed in a deterministic location inside
the node's active configuration area. Its shape is:

```
{
  "schema": "orbiplex-connector-config-signature.v1",
  "schema/v": 1,
  "connector_id": "<module id>",
  "config_hash": {
    "alg": "sha-256",
    "value": "<hex>"
  },
  "signed_at": "<RFC 3339>",
  "signer": {
    "participant/id": "<did>",
    "key/id": "<key id>"
  },
  "signature": {
    "alg": "ed25519",
    "value": "<base64url>"
  }
}
```

The filename is derived from the connector's `module_id` (for example
`<active-config-dir>/.signatures/<module-id>.sig.json`, where
`<active-config-dir>` is the node-owned, writable active configuration
directory — never the factory/package-shipped configuration tree).
Exact layout is left to the implementation; the contract is only that
the location be deterministic, live inside the node's active
configuration area, and be discoverable from the connector's own
configuration root — regardless of how many source files contributed
to the merged effective configuration.

#### Startup verification flow

On every supervised connector start:

1. Read all configuration sources for this connector.
2. Merge them in memory into the effective configuration.
3. Compute the canonical JCS serialization and its sha-256 hash.
4. Locate the sidecar file for this connector.
5. Verify that the sidecar's `connector_id` matches, its
   `config_hash.value` equals the computed hash, and its signature is
   valid under the named participant key.
6. **On success** — expose the action catalog; report
   `config/authorized: true` in the module report.
7. **On missing sidecar, hash mismatch, or invalid signature** —
   do not expose the action catalog; emit a diagnostic
   (`config/authorization: missing | hash-mismatch | signature-invalid`);
   follow the posture below.

Startup verification is necessary but not sufficient. A connector MUST NOT keep
an authorization decision forever in process memory without a reload contract.
At dispatch time it MUST either re-read and verify the active sidecar, or prove
that a host-owned reload/invalidation mechanism has invalidated the cached
decision after any sidecar or effective-configuration change. The simple v1
reference posture is stateless per-invocation verification: a stale sidecar on
disk causes the next action dispatch to fail before spawn.

#### Factory-default materialization and node-signed sidecars

To avoid requiring every module distributor to hold (and expose)
signing material for every shipped configuration file, the rule is:

> **If the connector's merged effective configuration is byte-for-byte
> identical to the factory defaults it shipped with — i.e. the operator
> has introduced no edits, overlays, or drop-ins of their own — operator
> authorization is not required.**

The technical subtlety is that a node's first run typically
**materializes** factory defaults into the writable active
configuration area, so that the operator has a ready-to-edit template
for every configurable component. This means brand-new files appear on
first run, through no operator action, and the "has the operator
touched this" question cannot be answered by file presence alone.

The resolution:

1. The routine that copies factory defaults into the active
   configuration area (and which already runs at first start or
   whenever a new component is introduced) is extended to **report
   which modules had their configuration materialized during this
   run**. The unit of reporting is the module/middleware, not the
   individual file — because a module's effective configuration is a
   merge of factory defaults and operator-authored sources from
   potentially many files, the only reliable statement the routine
   can make is "module *X* received factory materialization in this
   startup". Per-file reporting would be both noisier and less
   meaningful given the merge semantics.
2. Once materialization has finished for all components in a given
   startup, the node iterates over the reported **modules** and, for
   each of them, takes the **in-memory merged effective configuration
   as it will actually run**, and **automatically produces a
   node-signed sidecar** over that value (same JCS + sha-256 pipeline
   described above), using the **node-self identity key** — which
   is itself a trusted signer in the local trust model. Anchoring the
   signature on the in-memory merged value (rather than on any
   individual file) is what keeps this mechanism correct in the
   presence of multi-source configuration.
3. From that point the verification flow in the previous subsection
   applies unchanged: on subsequent starts, the sidecar's hash must
   still match the merged effective configuration. The moment the
   operator edits any of the materialized files (or adds an overlay),
   the hash changes, the node-signed sidecar becomes stale, and the
   normal Strict-posture prompt appears — at which point the
   authorization transitions from **node-signed** to **operator-signed**
   and remains so for the lifetime of that edit lineage.

Observable consequences and guarantees:

- Pristine factory configurations run without any operator ceremony
  and without requiring distributors to ship signatures.
- The first operator edit is always surfaced and requires explicit
  admittance; there is no silent drift from "factory" to "customized".
- Every authorized configuration, whether node-signed or
  operator-signed, carries an identifiable signer subject:
  `signer.node_id` for node-self bootstrap and `signer.participant_id`
  for operator authorization. Audit can therefore tell
  node-bootstrapped authorizations apart from operator authorizations
  without ambiguity.
- The sidecar file lives in the same active configuration area in
  both cases — the signer identity is what differs, not the location
  or the schema.

A node-signed sidecar is **not** a substitute for operator
authorization of a modified configuration; it is only the
machine-produced statement "this is the untouched factory default as
materialized by this node". It MUST be replaced by an operator-signed
sidecar at the first operator modification.

#### Re-authorization posture

The sidecar-signature mechanism is a specialization of a more general
**signed middleware configuration artifact** mechanism. A middleware may declare
one or more signed artifacts in its active config, each with an `artifact_id`,
a JSON Pointer to the effective config fragment, and a signing domain. The host
then computes the canonical hash of that fragment, writes the detached sidecar
under `<middleware-home>/config/.signatures/`, and blocks stale or denied
artifacts as Local Readiness Gate items (proposal 050). Sensorium OS uses
this generic mechanism with the first built-in artifact:
`module_id = "sensorium-os"`, `artifact_id = "action-catalog"`,
`config_pointer = "/sensorium_os/action_catalog"`, and
`signing_domain = "sensorium.os.action-catalog.v1"`.

- **Strict posture (default for non-bootstrap deployments).** The
  connector reports `config/authorized: false` and refuses to expose
  its action catalog. The host surfaces an operator prompt — "the
  effective configuration of `<connector_id>` has changed; review the
  diff and sign or reject." On approval the operator performs a
  three-part act — **admit the effective configuration, create the
  detached signature over its canonical hash, and write the sidecar
  signature file**. On rejection the host disables the middleware
  until the configuration is reverted or re-signed.
  A host MAY implement this as Local Readiness Gate (proposal 050): keep the
  daemon control/UI plane alive, block dependent middleware runtime,
  expose the blocking sidecar path and catalog hash to the operator,
  and resume only after an explicit signed grant or deny artifact is
  written.
- **Host bootstrap posture (default for missing sidecars).** If the
  sidecar is absent, the host MAY create a node-self signed bootstrap
  sidecar before starting the connector. This posture is limited to
  absence. A present-but-stale sidecar MUST NOT be silently replaced by
  the node; it enters Strict posture and requires an explicit operator
  decision.
- **Bootstrap posture (explicit and narrow).** A top-level
  `allow_unsigned_bootstrap` boolean in the connector configuration
  MAY be set to `true` during initial development. When set, a
  missing sidecar is tolerated with a prominent diagnostic, but the
  module report continues to carry `config/authorized: false`, and
  audit outcomes MUST carry `connector/unauthorized: true`. The host
  MAY refuse to dispatch directives to an unauthorized connector
  based on deployment policy. This flag MUST NOT be set in production
  and is expected to be flipped off permanently once the first
  signature has been produced.

#### Re-signing workflow

The canonical loop is: **edit → restart → verify → (if invalid) sign
→ restart**. The "sign" step is a minimal UI prompt (or, in
headless/bootstrap setups, a dedicated CLI tool) that:

- shows the operator the effective configuration as it will run,
- shows its canonical hash,
- asks for approval,
- on approval, performs the three-part act: admits the effective
  configuration, creates a detached Ed25519 signature over its
  canonical hash using the operator's participant key, and writes the
  sidecar signature file inside the node's active (writable)
  configuration area — never in the factory/shipped configuration
  tree. One sidecar authorizes the merged effective configuration,
  regardless of how many source files contributed to it.

The UI surface is intentionally narrow: it is **not** an editor for
the catalog. Editing remains a text-file operation, consistent with
the design principle established earlier in this proposal.

#### Why the sidecar supersedes a separate overlay

An earlier draft of this proposal posited a separately-signed
"restriction overlay" file in addition to the connector configuration.
The sidecar model makes that unnecessary: if the operator wishes to
restrict a declaration (lower a cap, remove an action, pin a content
hash), they edit the effective configuration directly and re-sign.
There is exactly one authorization surface, and it is the merged
configuration itself. This halves the number of trust artifacts and
removes the conceptual question "what does the overlay say that the
base config does not" from the operator's mental model.

### Why a file, not a UI

The catalog is authored by editing a file rather than through a graphical
operator UI, and this is deliberate, not a missing feature. A graphical
builder would force the declaration surface down to whatever it can
render, and the connector's declaration surface is intentionally as
expressive as the shell and the scripts it invokes — which is strictly
more expressive than any declarative workflow editor would be.

The file-editing barrier is also part of the security posture. Adding or
modifying an action that will run on the operator's machine with real
effects is a load-bearing decision. Requiring the operator to locate the
correct configuration file on disk, edit it, and restart the supervised
connector is a small, honest barrier that filters out casual changes
without obstructing the workflow of an operator who actually intends to
make one. Ease-of-entry is not a goal for this surface; clarity and
reviewability are.

### Operator ergonomics

The configuration file is expected to be hand-editable and reviewable
in a pull request. Two ergonomic consequences follow:

- declarations SHOULD carry an optional human-readable `description`
  and `rationale` field (free text, not schema-constrained) so that a
  reviewer can understand why the declaration exists;
- declarations SHOULD be grouped by a free-text `group` label (e.g.
  `"publishing"`, `"research"`, `"diagnostics"`) so that large catalogs
  remain navigable without forcing a hierarchical action-id scheme.

Neither field carries enforcement semantics; both are audit aids.

### Example: three hand-declared actions

This example illustrates three declarations an operator might author to
expose, respectively, a read-only tool invocation (C1), an allowlisted
local script that post-processes text (C2), and a composed action that
combines a scoped filesystem write with bounded network egress (C6).
Program names are intentionally placeholders; the OS connector neither
knows nor cares what the programs do.

```json
{
  "action_catalog": [
    {
      "action_id": "node.fetch.remote-refs",
      "class": "read-only-spawn",
      "group": "publishing",
      "description": "Fetches remote references for a named working tree.",
      "executable": {
        "kind": "binary",
        "path": "/usr/bin/<binary>",
        "argv_shape": ["<binary>", "--op", "fetch", "--path", "{{workspace}}", "--ref", "{{ref}}"]
      },
      "parameters_schema": {
        "type": "object",
        "required": ["workspace", "ref"],
        "properties": {
          "workspace": { "type": "string", "minLength": 1 },
          "ref":       { "type": "string", "pattern": "^[A-Za-z0-9._/-]+$" }
        },
        "additionalProperties": false
      },
      "default_timeout_ms": 30000,
      "max_timeout_ms": 60000,
      "limits": { "stdout_max_bytes": 65536, "stderr_max_bytes": 65536 },
      "environment": { "inherit": false, "set": {} },
      "result_contract": {
        "stdout_format": "text",
        "signal_kind": "ai.orbiplex.os/fetch-result",
        "signal_family": "os/fetch-result"
      }
    },
    {
      "action_id": "node.text.refine-local",
      "class": "allowlisted-script",
      "group": "research",
      "description": "Runs a local text-refinement script wrapping an on-node language model.",
      "executable": {
        "kind": "script",
        "path": "<absolute-script-path>",
        "interpreter": "/usr/bin/env",
        "argv_shape": ["python3", "<script-path>", "--params-json", "{{params_json}}"]
      },
      "script": { "allowed_roots": ["<absolute-scripts-dir>"] },
      "parameters_schema": {
        "type": "object",
        "required": ["input_path"],
        "properties": {
          "input_path":  { "type": "string", "minLength": 1 },
          "max_tokens":  { "type": "integer", "minimum": 1, "maximum": 4096 }
        },
        "additionalProperties": false
      },
      "default_timeout_ms": 45000,
      "max_timeout_ms": 120000,
      "limits": { "stdout_max_bytes": 262144, "stderr_max_bytes": 65536 },
      "environment": {
        "inherit": false,
        "set": { "NODE_MODEL_HOME": "<absolute-model-dir>" }
      },
      "result_contract": {
        "stdout_format": "json",
        "result_pointer_fields": ["revision_path", "token_count"],
        "signal_kind": "ai.orbiplex.os/text-refined",
        "signal_family": "os/text-refined"
      }
    },
    {
      "action_id": "node.workspace.compose-and-publish",
      "class": "composed-spawn",
      "group": "publishing",
      "description": "Composes a workspace artifact and pushes it to a declared endpoint.",
      "composed": {
        "effects": ["scoped-fs-write", "egress-network"]
      },
      "executable": {
        "kind": "script",
        "path": "<absolute-script-path>",
        "interpreter": "/usr/bin/env",
        "argv_shape": ["python3", "<script-path>", "--params-json", "{{params_json}}"]
      },
      "script": { "allowed_roots": ["<absolute-scripts-dir>"] },
      "signing": {
        "allowed_domains": ["<domain-tag>"],
        "key_ref": { "kind": "primary-participant" },
        "max_signatures": 1
      },
      "fs_write": {
        "write_root": "<absolute-workspace-root>",
        "max_bytes_total": 8388608,
        "max_bytes_per_file": 1048576
      },
      "egress_network": {
        "endpoints": [{ "host": "<publish-host>", "port": 443, "protocol": "https" }],
        "max_bytes_total": 4194304,
        "max_bytes_per_connection": 4194304
      },
      "parameters_schema": {
        "type": "object",
        "required": ["workspace", "source_path", "endpoint_ref"],
        "properties": {
          "workspace":    { "type": "string", "minLength": 1 },
          "source_path":  { "type": "string", "minLength": 1 },
          "endpoint_ref": { "type": "string", "minLength": 1 }
        },
        "additionalProperties": false
      },
      "default_timeout_ms": 60000,
      "max_timeout_ms": 180000,
      "limits": { "stdout_max_bytes": 262144, "stderr_max_bytes": 131072 },
      "environment": { "inherit": false, "set": {} },
      "result_contract": {
        "stdout_format": "json",
        "result_pointer_fields": ["artifact_ref", "endpoint_response_hash"],
        "signal_kind": "ai.orbiplex.os/workspace-published",
        "signal_family": "os/workspace-published"
      }
    }
  ]
}
```

An operator reviewing this file can tell, without reading any connector
source code, exactly what each declaration will do, under which envelope,
and what shape of result to expect. That is the intended experience.

## Responsibility Split

- **Caller (role module, agent, workflow).** Holds
  `sensorium.directive.invoke`. Names the `action_id`, supplies typed
  parameters, sets timing. Knows nothing about executables, paths, or
  classes.
- **`sensorium-core`.** Resolves `action_id` to exactly one declaration
  sourced from the connector's published catalog (with optional
  host-owned overlay applied). Validates parameters against
  `parameters_schema`. Applies sensitivity/consent policy. Dispatches
  to the named connector through the host-internal
  `sensorium.connector.invoke` seam, hard-blocked from external callers
  as established by proposal 045. When a declaration contains `signing`,
  core also checks that the requested directive is allowed to receive the
  scoped signer grant and arranges only that bounded grant through the host
  signer boundary.
- **OS connector.** Loads and validates the action catalog from its
  configuration file at startup, and revalidates sidecar authorization before
  dispatch unless the host provides an explicit reload/invalidation channel.
  Publishes the catalog through its module report. Enforces the class envelope
  for every action. Renders the declaration's argv shape without shell
  interpolation, applies only
  opaque process setup material already authorized by `sensorium-core` and
  the host, spawns the process, and captures results under the class's
  capture shape. Emits one or more observations where the declaration names
  `result_contract.signal_kind`. Records outcomes through the Sensorium audit
  lane. It never implements program-family behavior such as Git branching,
  commit signing, model inference, or archive extraction in connector code.
- **Operator.** Authors the action catalog by editing the connector's
  configuration file. Names the concrete program or script, selects its
  class, declares argv shape, enforcement parameters, optional scoped
  signing domains, and result contract, then reviews the file in the same
  way as any other configuration change. Optionally authors and signs
  a host-owned overlay to restrict or tighten the catalog in
  production-leaning deployments. The OS connector never chooses the
  class or the program semantics.

## Migration from the Current Single Action

Proposal 045 introduced a single reference action (`os.process.spawn-read-only`).
Under this proposal that action becomes the canonical `read-only-spawn`
(C1) entry and keeps its behavior unchanged. No existing caller is
affected. New actions declare their class explicitly. The connector
version MAY advertise the catalog it understands through
`middleware-module-report`'s `connector_actions` array so operators can
audit coverage.

## Out of Scope

- Specific tool integrations and their semantics.
- Any program-family specific allowlist guidance (those belong in
  separate operator playbooks, not here).
- Long-running local services.
- Operator-in-the-loop approval flows (reserved as `operator-gated-spawn`).
- Artifact promotion details beyond the existing Sensorium artifact lane
  contract.
- Federation of allowlist entries across nodes.

## Open Questions

- **Platform enforcement mechanism per class.** C3 and C4 need sandboxing
  primitives that differ by platform. Should the connector refuse to
  start on a platform where required primitives are unavailable, or run
  with a prominent downgrade notice?
- **Composed-spawn sensitivity arithmetic.** Maximum-of-components is a
  safe default, but some workloads may legitimately need a narrower
  declared class. Add a `sensitivity.override` field in the allowlist
  entry gated by operator signature?
- **Result pointer enumeration.** `result_pointer_fields` is strict
  enumeration. Should wildcards be permitted for dynamic output shapes?
  Preference: no — explicit enumeration is a feature, not a limitation.
- **Relationship to emergency activation.** When a node is in an
  elevated emergency posture, should certain classes (C3, C4, C5) be
  automatically refused? Proposal-level hook left for a follow-up.

## Non-Goals

This proposal is not a sandbox specification, is not a container runtime
contract, and is not a replacement for operating-system-level isolation.
It is a **class-aware policy envelope** the connector applies on top of
whatever platform isolation is configured. Platform-level isolation
belongs to deployment, not to the connector contract.

It is also not a graphical editor, a low-code surface, or an end-user
installer for local actions. The authoring experience is a text file
edited by an operator who has already located it on disk. That is the
intended barrier.
