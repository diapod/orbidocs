# Responsibility-maintenance-bindings.local.v2

Source schema: [`doc/schemas/responsibility-maintenance-bindings.local.v2.schema.json`](../../schemas/responsibility-maintenance-bindings.local.v2.schema.json)

Draft local maintenance contract. Shape validation grants no authority and does not open D7.

## Governing Basis

- [`doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [`doc/project/40-proposals/072-capability-registry.md`](../../project/40-proposals/072-capability-registry.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `responsibility-maintenance-bindings.local.v2` |  |
| [`profile`](#field-profile) | `yes` | const: `responsibility.maintenance-shadow.v2` |  |
| [`run/id`](#field-run-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`host/id`](#field-host-id) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`host/incarnation`](#field-host-incarnation) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id` |  |
| [`node`](#field-node) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Source` |  |
| [`orbidocs`](#field-orbidocs) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Source` |  |
| [`binaries`](#field-binaries) | `yes` | object |  |
| [`policy`](#field-policy) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding` |  |
| [`grants`](#field-grants) | `yes` | array |  |
| [`fixtures/digest`](#field-fixtures-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`configuration/digest`](#field-configuration-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`toolchain/digest`](#field-toolchain-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`qualifier/digest`](#field-qualifier-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`profile/digest`](#field-profile-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`schemas/digest`](#field-schemas-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
| [`scenarios`](#field-scenarios) | `yes` | object |  |
| [`budget`](#field-budget) | `yes` | const: `{'batch/rows': 100, 'sources/generation': 8192, 'ordinary-steps/generation': 1024, 'resident/generations': 16, 'resident/baseline-bytes': 33554432, 'resident/prepared-bytes': 33554432, 'request/bytes': 16384, 'result/bytes': 65536, 'terminal/slots-per-generation': 1, 'terminal/record-bytes': 8192, 'terminal/reserved-bytes': 131072, 'pending/commands': 64, 'receipt/resident-records': 1024, 'receipt/record-bytes': 8192, 'alert/pending-records': 256, 'alert/record-bytes': 4096, 'archive/index-records': 64, 'archive/manifest-bytes': 16384, 'archive/plaintext-bytes': 100663296, 'archive/resident-bytes': 268435456, 'conflict/alert-after': 3, 'retry/attempts': 8, 'retry/backoff-ms': [25, 50, 100, 200, 400, 800, 1000], 'report/bytes': 262144, 'observation/bytes': 65536, 'evidence/run-bytes': 4194304, 'evidence/refused-bytes': 262144, 'writer/storage-version': 4, 'archive/index-bytes': 65536, 'gate/full-wall-ns': 10000000000, 'gate/cpu-ns': 1000000000, 'gate/non-commit-wall-ns': 1000000000, 'v1/authority-timeout-ms': 12000, 'v1/e2e-max-ms': 14000, 'v1/route-timeout-ms': 15000, 'pending/ordinary-commands': 48, 'pending/control-commands': 16, 'hold/active-records': 336, 'hold/record-bytes': 4096, 'hold/resident-records': 1024, 'hold/resident-bytes': 4194304, 'control/episode-records': 16, 'control/episode-bytes': 65536, 'operation/event-records': 8192, 'operation/event-bytes': 33554432}` |  |
| [`safety`](#field-safety) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety` |  |
| [`validator/digest`](#field-validator-digest) | `yes` | ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `responsibility-maintenance-bindings.local.v2`

<a id="field-profile"></a>
## `profile`

- Required: `yes`
- Shape: const: `responsibility.maintenance-shadow.v2`

<a id="field-run-id"></a>
## `run/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-host-id"></a>
## `host/id`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-host-incarnation"></a>
## `host/incarnation`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Id`

<a id="field-node"></a>
## `node`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Source`

<a id="field-orbidocs"></a>
## `orbidocs`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Source`

<a id="field-binaries"></a>
## `binaries`

- Required: `yes`
- Shape: object

<a id="field-policy"></a>
## `policy`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Binding`

<a id="field-grants"></a>
## `grants`

- Required: `yes`
- Shape: array

<a id="field-fixtures-digest"></a>
## `fixtures/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-configuration-digest"></a>
## `configuration/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-toolchain-digest"></a>
## `toolchain/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-qualifier-digest"></a>
## `qualifier/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-profile-digest"></a>
## `profile/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-schemas-digest"></a>
## `schemas/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`

<a id="field-scenarios"></a>
## `scenarios`

- Required: `yes`
- Shape: object

<a id="field-budget"></a>
## `budget`

- Required: `yes`
- Shape: const: `{'batch/rows': 100, 'sources/generation': 8192, 'ordinary-steps/generation': 1024, 'resident/generations': 16, 'resident/baseline-bytes': 33554432, 'resident/prepared-bytes': 33554432, 'request/bytes': 16384, 'result/bytes': 65536, 'terminal/slots-per-generation': 1, 'terminal/record-bytes': 8192, 'terminal/reserved-bytes': 131072, 'pending/commands': 64, 'receipt/resident-records': 1024, 'receipt/record-bytes': 8192, 'alert/pending-records': 256, 'alert/record-bytes': 4096, 'archive/index-records': 64, 'archive/manifest-bytes': 16384, 'archive/plaintext-bytes': 100663296, 'archive/resident-bytes': 268435456, 'conflict/alert-after': 3, 'retry/attempts': 8, 'retry/backoff-ms': [25, 50, 100, 200, 400, 800, 1000], 'report/bytes': 262144, 'observation/bytes': 65536, 'evidence/run-bytes': 4194304, 'evidence/refused-bytes': 262144, 'writer/storage-version': 4, 'archive/index-bytes': 65536, 'gate/full-wall-ns': 10000000000, 'gate/cpu-ns': 1000000000, 'gate/non-commit-wall-ns': 1000000000, 'v1/authority-timeout-ms': 12000, 'v1/e2e-max-ms': 14000, 'v1/route-timeout-ms': 15000, 'pending/ordinary-commands': 48, 'pending/control-commands': 16, 'hold/active-records': 336, 'hold/record-bytes': 4096, 'hold/resident-records': 1024, 'hold/resident-bytes': 4194304, 'control/episode-records': 16, 'control/episode-bytes': 65536, 'operation/event-records': 8192, 'operation/event-bytes': 33554432}`

<a id="field-safety"></a>
## `safety`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Safety`

<a id="field-validator-digest"></a>
## `validator/digest`

- Required: `yes`
- Shape: ref: `responsibility-maintenance-common.local.v1.schema.json#/$defs/Digest`
