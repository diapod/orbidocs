# Sensorium-brainflow-budget-profile.v1

Source schema: [`doc/schemas/sensorium-brainflow-budget-profile.v1.schema.json`](../../schemas/sensorium-brainflow-budget-profile.v1.schema.json)

Predeclared first-slice design budgets, not measured acceptance. Hash this whole canonical profile before execution and bind it to each report. Native buffer accounting covers every allocated preset. Queue age is monotonic. No retry after killed workers; reconnect applies only to surviving workers under current admission.

## Governing Basis

- [`doc/project/40-proposals/096-sensorium-brainflow-connector.md`](../../project/40-proposals/096-sensorium-brainflow-connector.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-001-node-onboarding.md`](../../project/50-requirements/requirements-001-node-onboarding.md)
- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `sensorium-brainflow-budget-profile.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`profile/id`](#field-profile-id) | `yes` | const: `sensorium.first-slice.mac-arm64.v1` |  |
| [`revision`](#field-revision) | `yes` | integer |  |
| [`limits`](#field-limits) | `yes` | const: `{'prepare/ms': 15000, 'first-data/ms': 5000, 'drain/ms': 25, 'aggregation/ms': 100, 'block/channels': 32, 'block/samples': 128, 'native/samples-per-preset': 2048, 'native/bytes': 2097152, 'channel/bytes': 65536, 'worker-queue/blocks': 16, 'worker-queue/bytes': 524288, 'worker-queue/age-ms': 1000, 'source/blocks': 256, 'source/bytes': 1048576, 'source/age-ms': 5000, 'read/consumers': 4, 'read/batch-frames': 8, 'read/batch-bytes': 65536, 'read/in-flight': 1, 'worker/rss-bytes': 536870912, 'host/buffer-bytes': 16777216, 'latency/p95-ms': 250, 'latency/p99-ms': 500, 'latency/max-ms': 1000, 'protected-stop/receipt-ms': 250, 'host/fence-ms': 100, 'process/exit-ms': 5000, 'cleanup/uncertain-ms': 10000, 'pressure/recovery-ms': 5000, 'reconnect/attempts': 2, 'reconnect/window-ms': 45000, 'consent/max-s': 1800, 'qualification/warmup-s': 120, 'qualification/runs-per-mode': 3, 'qualification/run-s': 300, 'qualification/rate-tolerance-percent': 5, 'carrier/blocks': 8, 'carrier/bytes': 65536, 'carrier/age-ms': 1000, 'read/revocation-propagation-ms': 100}` |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `sensorium-brainflow-budget-profile.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-profile-id"></a>
## `profile/id`

- Required: `yes`
- Shape: const: `sensorium.first-slice.mac-arm64.v1`

<a id="field-revision"></a>
## `revision`

- Required: `yes`
- Shape: integer

<a id="field-limits"></a>
## `limits`

- Required: `yes`
- Shape: const: `{'prepare/ms': 15000, 'first-data/ms': 5000, 'drain/ms': 25, 'aggregation/ms': 100, 'block/channels': 32, 'block/samples': 128, 'native/samples-per-preset': 2048, 'native/bytes': 2097152, 'channel/bytes': 65536, 'worker-queue/blocks': 16, 'worker-queue/bytes': 524288, 'worker-queue/age-ms': 1000, 'source/blocks': 256, 'source/bytes': 1048576, 'source/age-ms': 5000, 'read/consumers': 4, 'read/batch-frames': 8, 'read/batch-bytes': 65536, 'read/in-flight': 1, 'worker/rss-bytes': 536870912, 'host/buffer-bytes': 16777216, 'latency/p95-ms': 250, 'latency/p99-ms': 500, 'latency/max-ms': 1000, 'protected-stop/receipt-ms': 250, 'host/fence-ms': 100, 'process/exit-ms': 5000, 'cleanup/uncertain-ms': 10000, 'pressure/recovery-ms': 5000, 'reconnect/attempts': 2, 'reconnect/window-ms': 45000, 'consent/max-s': 1800, 'qualification/warmup-s': 120, 'qualification/runs-per-mode': 3, 'qualification/run-s': 300, 'qualification/rate-tolerance-percent': 5, 'carrier/blocks': 8, 'carrier/bytes': 65536, 'carrier/age-ms': 1000, 'read/revocation-propagation-ms': 100}`
