# Responsibility-maintenance-common.local.v1

Source schema: [`doc/schemas/responsibility-maintenance-common.local.v1.schema.json`](../../schemas/responsibility-maintenance-common.local.v1.schema.json)

Draft M0 definitions only. None of these values is authenticated by shape validation.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`Id`](#def-id) | string |  |
| [`Digest`](#def-digest) | string |  |
| [`Time`](#def-time) | string |  |
| [`Path`](#def-path) | string |  |
| [`Git`](#def-git) | string |  |
| [`Binding`](#def-binding) | object |  |
| [`Head`](#def-head) | object |  |
| [`Boundary`](#def-boundary) | object |  |
| [`Safety`](#def-safety) | const: `{'authority': 'v1', 'd7': {'storage': False, 'composition': False, 'writers': False, 'replay': False, 'receipts': False}, 'participant-effects': False, 'cutover': False}` |  |
| [`Budget`](#def-budget) | const: `{'batch/rows': 100, 'sources/generation': 8192, 'ordinary-steps/generation': 1024, 'resident/generations': 16, 'resident/baseline-bytes': 33554432, 'resident/prepared-bytes': 33554432, 'request/bytes': 16384, 'result/bytes': 65536, 'terminal/slots-per-generation': 1, 'terminal/record-bytes': 8192, 'terminal/reserved-bytes': 131072, 'pending/commands': 64, 'receipt/resident-records': 1024, 'receipt/record-bytes': 8192, 'alert/pending-records': 256, 'alert/record-bytes': 4096, 'archive/index-records': 64, 'archive/manifest-bytes': 16384, 'archive/plaintext-bytes': 100663296, 'archive/resident-bytes': 268435456, 'conflict/alert-after': 3, 'retry/attempts': 8, 'retry/backoff-ms': [25, 50, 100, 200, 400, 800, 1000], 'report/bytes': 262144, 'observation/bytes': 65536, 'evidence/run-bytes': 4194304, 'evidence/refused-bytes': 262144, 'writer/storage-version': 4, 'archive/index-bytes': 65536}` |  |
| [`Compatibility`](#def-compatibility) | object |  |
| [`Artifact`](#def-artifact) | object |  |
| [`Request`](#def-request) | object |  |
| [`Result`](#def-result) | object |  |
| [`Generation`](#def-generation) | object |  |
| [`Abandoned`](#def-abandoned) | object |  |
| [`Alert`](#def-alert) | object |  |
| [`ArchiveContext`](#def-archivecontext) | object |  |
| [`Archive`](#def-archive) | object |  |
| [`Source`](#def-source) | object |  |
| [`Binary`](#def-binary) | object |  |
| [`Bindings`](#def-bindings) | object |  |
| [`Case`](#def-case) | object |  |
| [`Report`](#def-report) | object |  |
| [`ArchiveIndexEntry`](#def-archiveindexentry) | object |  |
| [`ArchiveIndex`](#def-archiveindex) | object |  |
| [`MaintenanceArchiveContext`](#def-maintenancearchivecontext) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-id"></a>
## `$defs.Id`

- Shape: string

<a id="def-digest"></a>
## `$defs.Digest`

- Shape: string

<a id="def-time"></a>
## `$defs.Time`

- Shape: string

<a id="def-path"></a>
## `$defs.Path`

- Shape: string

<a id="def-git"></a>
## `$defs.Git`

- Shape: string

<a id="def-binding"></a>
## `$defs.Binding`

- Shape: object

<a id="def-head"></a>
## `$defs.Head`

- Shape: object

<a id="def-boundary"></a>
## `$defs.Boundary`

- Shape: object

<a id="def-safety"></a>
## `$defs.Safety`

- Shape: const: `{'authority': 'v1', 'd7': {'storage': False, 'composition': False, 'writers': False, 'replay': False, 'receipts': False}, 'participant-effects': False, 'cutover': False}`

<a id="def-budget"></a>
## `$defs.Budget`

- Shape: const: `{'batch/rows': 100, 'sources/generation': 8192, 'ordinary-steps/generation': 1024, 'resident/generations': 16, 'resident/baseline-bytes': 33554432, 'resident/prepared-bytes': 33554432, 'request/bytes': 16384, 'result/bytes': 65536, 'terminal/slots-per-generation': 1, 'terminal/record-bytes': 8192, 'terminal/reserved-bytes': 131072, 'pending/commands': 64, 'receipt/resident-records': 1024, 'receipt/record-bytes': 8192, 'alert/pending-records': 256, 'alert/record-bytes': 4096, 'archive/index-records': 64, 'archive/manifest-bytes': 16384, 'archive/plaintext-bytes': 100663296, 'archive/resident-bytes': 268435456, 'conflict/alert-after': 3, 'retry/attempts': 8, 'retry/backoff-ms': [25, 50, 100, 200, 400, 800, 1000], 'report/bytes': 262144, 'observation/bytes': 65536, 'evidence/run-bytes': 4194304, 'evidence/refused-bytes': 262144, 'writer/storage-version': 4, 'archive/index-bytes': 65536}`

<a id="def-compatibility"></a>
## `$defs.Compatibility`

- Shape: object

<a id="def-artifact"></a>
## `$defs.Artifact`

- Shape: object

<a id="def-request"></a>
## `$defs.Request`

- Shape: object

<a id="def-result"></a>
## `$defs.Result`

- Shape: object

<a id="def-generation"></a>
## `$defs.Generation`

- Shape: object

<a id="def-abandoned"></a>
## `$defs.Abandoned`

- Shape: object

<a id="def-alert"></a>
## `$defs.Alert`

- Shape: object

<a id="def-archivecontext"></a>
## `$defs.ArchiveContext`

- Shape: object

<a id="def-archive"></a>
## `$defs.Archive`

- Shape: object

<a id="def-source"></a>
## `$defs.Source`

- Shape: object

<a id="def-binary"></a>
## `$defs.Binary`

- Shape: object

<a id="def-bindings"></a>
## `$defs.Bindings`

- Shape: object

<a id="def-case"></a>
## `$defs.Case`

- Shape: object

<a id="def-report"></a>
## `$defs.Report`

- Shape: object

<a id="def-archiveindexentry"></a>
## `$defs.ArchiveIndexEntry`

- Shape: object

<a id="def-archiveindex"></a>
## `$defs.ArchiveIndex`

- Shape: object

<a id="def-maintenancearchivecontext"></a>
## `$defs.MaintenanceArchiveContext`

- Shape: object
