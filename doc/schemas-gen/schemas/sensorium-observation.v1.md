# Sensorium Observation v1

Source schema: [`doc/schemas/sensorium-observation.v1.schema.json`](../../schemas/sensorium-observation.v1.schema.json)

Admitted local Sensorium observation: a fact about the world normalized by sensorium-core after connector submission or after a successful directive. Rejected and quarantined submissions do not become observation records.

## Governing Basis

- [`doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`](../../project/40-proposals/045-sensorium-local-enaction-stratum.md)
- [`doc/project/40-proposals/046-agora-topic-key-namespace-conventions.md`](../../project/40-proposals/046-agora-topic-key-namespace-conventions.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006.md`](../../project/50-requirements/requirements-006.md)
- [`doc/project/50-requirements/requirements-010.md`](../../project/50-requirements/requirements-010.md)
- [`doc/project/50-requirements/requirements-011.md`](../../project/50-requirements/requirements-011.md)
- [`doc/project/50-requirements/requirements-014.md`](../../project/50-requirements/requirements-014.md)

### Stories

- [`doc/project/30-stories/story-001.md`](../../project/30-stories/story-001.md)
- [`doc/project/30-stories/story-004.md`](../../project/30-stories/story-004.md)
- [`doc/project/30-stories/story-005.md`](../../project/30-stories/story-005.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006.md`](../../project/30-stories/story-006.md)
- [`doc/project/30-stories/story-007.md`](../../project/30-stories/story-007.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-observation.v1` | Schema tag for the v1 Sensorium contract. |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` | Schema version. |
| [`observation/id`](#field-observation-id) | `yes` | string | Opaque observation identifier assigned by sensorium-core; recommended to be ULID-prefixed, e.g. obs:local:01J... |
| [`invocation/id`](#field-invocation-id) | `no` | string | Optional connector invocation trace id. Present for reactive observations produced by a directive or explicit connector invocation. |
| [`directive/id`](#field-directive-id) | `no` | string | Optional directive id when this observation was produced as a result of sensorium-directive.v1. |
| [`outcome/id`](#field-outcome-id) | `no` | string | Optional directive outcome id linking this observation to the audit-only sensorium-directive-outcome.v1 record. |
| [`correlation/id`](#field-correlation-id) | `no` | string | Optional opaque id threading this observation through a higher-level plan or workflow. |
| [`connector/id`](#field-connector-id) | `yes` | string | Registered connector module id that produced the submitted observation or executed the directive. |
| [`connector/kind`](#field-connector-kind) | `yes` | string | Domain-facing connector kind/class label, e.g. OS, public-network-reader, filesystem-watcher. |
| [`observed/at`](#field-observed-at) | `yes` | string | RFC 3339 timestamp of the source event or instrument-level observation. This is the time belonging to the world/source, not the time at which the connector or sensorium-core processed the record. |
| [`ingested/at`](#field-ingested-at) | `yes` | string | RFC 3339 timestamp when sensorium-core admitted the observation and wrote the admitted record. This is not the source event time; use observed/at for the instrument/source timestamp and connector/submitted_at when connector latency matters. |
| [`signal/kind`](#field-signal-kind) | `yes` | string | Authoritative local signal kind used for query and per-kind local Agora topic derivation. The value forms the suffix of local/sensorium/observations/{signal-kind}. Each '/'-separated segment is a dotted chain of lowercase tokens, which lets connectors carry reverse-DNS vendor prefixes (e.g. com.apple.ios.accelerometer/x-axis) for collision-free namespacing. Bare short names (e.g. release, github-release, filesystem/change) remain valid and represent the community-common namespace. Orbiplex-owned kinds SHOULD use the ai.orbiplex.* prefix per proposal 046. |
| [`signal/family`](#field-signal-family) | `no` | string | Optional generic signal-family identifier declared by the connector alongside signal/kind. Carries the vendor-independent family name (e.g. accelerometer/x-axis, workflow/completed) so consumers can query across providers or subscribe broadly and filter by envelope without maintaining a vendor-to-family mapping. MUST NOT contain dots; the no-dot pattern distinguishes the community-common family namespace from the dotted reverse-DNS namespace used by signal/kind. Source of truth is the connector module report; sensorium-core does not derive this value. No local/sensorium/observations-by-family topic tree exists in v1. |
| [`subject/kind`](#field-subject-kind) | `no` | string | Optional kind of observed subject, e.g. github-repository, url, filesystem-path, host, self, environment. Omit only when the observation is genuinely subjectless. |
| [`subject/id`](#field-subject-id) | `no` | string | Optional stable subject identifier within subject/kind. For node-self measurements use a stable self identifier rather than a blank value. |
| [`summary`](#field-summary) | `no` | object | Optional human-readable compact summary. Numeric or high-frequency observations MAY omit this field when a textual summary would add no value. |
| [`confidence`](#field-confidence) | `yes` | object |  |
| [`freshness`](#field-freshness) | `yes` | object |  |
| [`sensitivity`](#field-sensitivity) | `yes` | object |  |
| [`source/ref`](#field-source-ref) | `yes` | object |  |
| [`evidence/refs`](#field-evidence-refs) | `no` | array | Optional artifact or evidence references using the minimal artifact-lane contract from proposal 045. |
| [`policy/hints`](#field-policy-hints) | `no` | object | Connector-supplied policy hints. These are not authoritative. |
| [`admission`](#field-admission) | `yes` | object | Sensorium-authored authoritative admission decision. |
| [`connector/submitted_at`](#field-connector-submitted-at) | `no` | string | Optional RFC 3339 timestamp when the connector emitted or submitted the observation candidate to sensorium-core. Used to distinguish source lag (connector/submitted_at - observed/at) from admission lag (ingested/at - connector/submitted_at). |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`artifactRef`](#def-artifactref) | object | Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference. |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-observation.v1`

Schema tag for the v1 Sensorium contract.

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

Schema version.

<a id="field-observation-id"></a>
## `observation/id`

- Required: `yes`
- Shape: string

Opaque observation identifier assigned by sensorium-core; recommended to be ULID-prefixed, e.g. obs:local:01J...

<a id="field-invocation-id"></a>
## `invocation/id`

- Required: `no`
- Shape: string

Optional connector invocation trace id. Present for reactive observations produced by a directive or explicit connector invocation.

<a id="field-directive-id"></a>
## `directive/id`

- Required: `no`
- Shape: string

Optional directive id when this observation was produced as a result of sensorium-directive.v1.

<a id="field-outcome-id"></a>
## `outcome/id`

- Required: `no`
- Shape: string

Optional directive outcome id linking this observation to the audit-only sensorium-directive-outcome.v1 record.

<a id="field-correlation-id"></a>
## `correlation/id`

- Required: `no`
- Shape: string

Optional opaque id threading this observation through a higher-level plan or workflow.

<a id="field-connector-id"></a>
## `connector/id`

- Required: `yes`
- Shape: string

Registered connector module id that produced the submitted observation or executed the directive.

<a id="field-connector-kind"></a>
## `connector/kind`

- Required: `yes`
- Shape: string

Domain-facing connector kind/class label, e.g. OS, public-network-reader, filesystem-watcher.

<a id="field-observed-at"></a>
## `observed/at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp of the source event or instrument-level observation. This is the time belonging to the world/source, not the time at which the connector or sensorium-core processed the record.

<a id="field-ingested-at"></a>
## `ingested/at`

- Required: `yes`
- Shape: string

RFC 3339 timestamp when sensorium-core admitted the observation and wrote the admitted record. This is not the source event time; use observed/at for the instrument/source timestamp and connector/submitted_at when connector latency matters.

<a id="field-signal-kind"></a>
## `signal/kind`

- Required: `yes`
- Shape: string

Authoritative local signal kind used for query and per-kind local Agora topic derivation. The value forms the suffix of local/sensorium/observations/{signal-kind}. Each '/'-separated segment is a dotted chain of lowercase tokens, which lets connectors carry reverse-DNS vendor prefixes (e.g. com.apple.ios.accelerometer/x-axis) for collision-free namespacing. Bare short names (e.g. release, github-release, filesystem/change) remain valid and represent the community-common namespace. Orbiplex-owned kinds SHOULD use the ai.orbiplex.* prefix per proposal 046.

<a id="field-signal-family"></a>
## `signal/family`

- Required: `no`
- Shape: string

Optional generic signal-family identifier declared by the connector alongside signal/kind. Carries the vendor-independent family name (e.g. accelerometer/x-axis, workflow/completed) so consumers can query across providers or subscribe broadly and filter by envelope without maintaining a vendor-to-family mapping. MUST NOT contain dots; the no-dot pattern distinguishes the community-common family namespace from the dotted reverse-DNS namespace used by signal/kind. Source of truth is the connector module report; sensorium-core does not derive this value. No local/sensorium/observations-by-family topic tree exists in v1.

<a id="field-subject-kind"></a>
## `subject/kind`

- Required: `no`
- Shape: string

Optional kind of observed subject, e.g. github-repository, url, filesystem-path, host, self, environment. Omit only when the observation is genuinely subjectless.

<a id="field-subject-id"></a>
## `subject/id`

- Required: `no`
- Shape: string

Optional stable subject identifier within subject/kind. For node-self measurements use a stable self identifier rather than a blank value.

<a id="field-summary"></a>
## `summary`

- Required: `no`
- Shape: object

Optional human-readable compact summary. Numeric or high-frequency observations MAY omit this field when a textual summary would add no value.

<a id="field-confidence"></a>
## `confidence`

- Required: `yes`
- Shape: object

<a id="field-freshness"></a>
## `freshness`

- Required: `yes`
- Shape: object

<a id="field-sensitivity"></a>
## `sensitivity`

- Required: `yes`
- Shape: object

<a id="field-source-ref"></a>
## `source/ref`

- Required: `yes`
- Shape: object

<a id="field-evidence-refs"></a>
## `evidence/refs`

- Required: `no`
- Shape: array

Optional artifact or evidence references using the minimal artifact-lane contract from proposal 045.

<a id="field-policy-hints"></a>
## `policy/hints`

- Required: `no`
- Shape: object

Connector-supplied policy hints. These are not authoritative.

<a id="field-admission"></a>
## `admission`

- Required: `yes`
- Shape: object

Sensorium-authored authoritative admission decision.

<a id="field-connector-submitted-at"></a>
## `connector/submitted_at`

- Required: `no`
- Shape: string

Optional RFC 3339 timestamp when the connector emitted or submitted the observation candidate to sensorium-core. Used to distinguish source lag (connector/submitted_at - observed/at) from admission lag (ingested/at - connector/submitted_at).

## Definition Semantics

<a id="def-artifactref"></a>
## `$defs.artifactRef`

- Shape: object

Minimal artifact-lane reference. The artifact itself is stored outside this envelope and is addressed by a content or host-owned blob reference.
