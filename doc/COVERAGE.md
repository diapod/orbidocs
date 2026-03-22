# Workflow Coverage

Generated coverage snapshot for the current `doc/` structure.

## Normative Workflow

| Step | Markdown Files | PL | EN | Shared |
|---|---:|---:|---:|---:|
| `10-ideas` (Ideas) | `1` | `0` | `0` | `1` |
| `20-vision` (Vision) | `2` | `1` | `1` | `0` |
| `25-ai-manifesto` (AI Manifesto) | `2` | `1` | `1` | `0` |
| `30-core-values` (Core Values) | `2` | `1` | `1` | `0` |
| `40-constitution` (Constitution) | `2` | `1` | `1` | `0` |
| `50-constitutional-ops` (Constitutional Ops) | `48` | `24` | `24` | `0` |

- Total normative markdown files: `57`

## Project Workflow

| Step | Markdown Files | With `Based on:` |
|---|---:|---:|
| `10-challenges` (Challenges) | `4` | `2` |
| `20-memos` (Memos) | `15` | `0` |
| `30-stories` (Stories) | `5` | `0` |
| `40-proposals` (Proposals) | `12` | `10` |
| `50-requirements` (Requirements) | `7` | `5` |
| `60-solutions` (Solutions) | `0` | `0` |

- Total project markdown files: `45`
- Proposals referencing source material: `10` / `12`
- Requirements referencing source material: `5` / `7`

## Schema Workflow

| Schema | Properties | Described Fields | `x-dia-basis` | Generated Doc | Valid Examples | Invalid Examples |
|---|---:|---:|---|---|---:|---:|
| [`answer-room-metadata.v1.schema.json`](schemas-gen/schemas/answer-room-metadata.v1.md) | `16` | `1` | `no` | `yes` | `3` | `1` |
| [`proof-of-personhood-attestation.v1.schema.json`](schemas-gen/schemas/proof-of-personhood-attestation.v1.md) | `19` | `10` | `yes` | `yes` | `1` | `4` |
| [`signal-marker.v1.schema.json`](schemas-gen/schemas/signal-marker.v1.md) | `12` | `8` | `yes` | `yes` | `0` | `0` |
| [`signal-transform-event.v1.schema.json`](schemas-gen/schemas/signal-transform-event.v1.md) | `15` | `11` | `yes` | `yes` | `0` | `0` |
| [`transcript-bundle.v1.schema.json`](schemas-gen/schemas/transcript-bundle.v1.md) | `18` | `2` | `no` | `yes` | `3` | `1` |
| [`transcript-segment.v1.schema.json`](schemas-gen/schemas/transcript-segment.v1.md) | `21` | `6` | `no` | `yes` | `3` | `1` |
| [`ubc-allocation.v1.schema.json`](schemas-gen/schemas/ubc-allocation.v1.md) | `17` | `12` | `yes` | `yes` | `1` | `2` |
| [`ubc-settlement.v1.schema.json`](schemas-gen/schemas/ubc-settlement.v1.md) | `16` | `7` | `yes` | `yes` | `1` | `1` |

- Canonical schemas: `8`
- Generated schema docs: `8`
- Positive examples: `12`
- Negative examples: `10`
