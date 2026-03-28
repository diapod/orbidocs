# Workflow Coverage

Generated coverage snapshot for the current `doc/` structure.

## Normative Workflow

| Step | Markdown Files | PL | EN | Shared |
|---|---:|---:|---:|---:|
| `10-ideas` (Ideas) | `1` | `0` | `0` | `1` |
| `20-vision` (Vision) | `2` | `1` | `1` | `0` |
| `30-core-values` (Core Values) | `2` | `1` | `1` | `0` |
| `40-constitution` (Constitution) | `2` | `1` | `1` | `0` |
| `50-constitutional-ops` (Constitutional Ops) | `48` | `24` | `24` | `0` |

- Total normative markdown files: `61`

## Project Workflow

| Step | Markdown Files | With `Based on:` |
|---|---:|---:|
| `10-challenges` (Challenges) | `4` | `2` |
| `20-memos` (Memos) | `23` | `0` |
| `30-stories` (Stories) | `7` | `0` |
| `40-proposals` (Proposals) | `17` | `15` |
| `50-requirements` (Requirements) | `8` | `6` |
| `60-solutions` (Solutions) | `10` | `6` |

- Total project markdown files: `71`
- Proposals referencing source material: `15` / `17`
- Requirements referencing source material: `6` / `8`

## Schema Workflow

| Schema | Properties | Described Fields | `x-dia-basis` | Generated Doc | Valid Examples | Invalid Examples |
|---|---:|---:|---|---|---:|---:|
| [`adapter-artifact.v1.schema.json`](schemas-gen/schemas/adapter-artifact.v1.md) | `13` | `13` | `yes` | `yes` | `1` | `1` |
| [`answer-room-metadata.v1.schema.json`](schemas-gen/schemas/answer-room-metadata.v1.md) | `16` | `1` | `no` | `yes` | `3` | `1` |
| [`archival-package.v1.schema.json`](schemas-gen/schemas/archival-package.v1.md) | `16` | `15` | `yes` | `yes` | `1` | `1` |
| [`archivist-advertisement.v1.schema.json`](schemas-gen/schemas/archivist-advertisement.v1.md) | `14` | `14` | `yes` | `yes` | `1` | `1` |
| [`association-room-proposal.v1.schema.json`](schemas-gen/schemas/association-room-proposal.v1.md) | `14` | `13` | `yes` | `yes` | `1` | `1` |
| [`capability-advertisement.v1.schema.json`](schemas-gen/schemas/capability-advertisement.v1.md) | `12` | `11` | `yes` | `yes` | `1` | `1` |
| [`corpus-entry.v1.schema.json`](schemas-gen/schemas/corpus-entry.v1.md) | `14` | `14` | `yes` | `yes` | `1` | `1` |
| [`curation-decision.v1.schema.json`](schemas-gen/schemas/curation-decision.v1.md) | `13` | `13` | `yes` | `yes` | `1` | `1` |
| [`eval-report.v1.schema.json`](schemas-gen/schemas/eval-report.v1.md) | `14` | `14` | `yes` | `yes` | `1` | `1` |
| [`knowledge-artifact.v1.schema.json`](schemas-gen/schemas/knowledge-artifact.v1.md) | `14` | `14` | `yes` | `yes` | `1` | `1` |
| [`learning-outcome.v1.schema.json`](schemas-gen/schemas/learning-outcome.v1.md) | `16` | `16` | `yes` | `yes` | `1` | `1` |
| [`model-card.v1.schema.json`](schemas-gen/schemas/model-card.v1.md) | `17` | `17` | `yes` | `yes` | `1` | `1` |
| [`node-advertisement.v1.schema.json`](schemas-gen/schemas/node-advertisement.v1.md) | `14` | `13` | `yes` | `yes` | `2` | `1` |
| [`node-identity.v1.schema.json`](schemas-gen/schemas/node-identity.v1.md) | `9` | `9` | `yes` | `yes` | `1` | `2` |
| [`nym-certificate.v1.schema.json`](schemas-gen/schemas/nym-certificate.v1.md) | `11` | `9` | `yes` | `yes` | `2` | `1` |
| [`nym-issue-request.v1.schema.json`](schemas-gen/schemas/nym-issue-request.v1.md) | `10` | `8` | `yes` | `yes` | `1` | `1` |
| [`nym-renew-rejected.v1.schema.json`](schemas-gen/schemas/nym-renew-rejected.v1.md) | `10` | `8` | `yes` | `yes` | `1` | `0` |
| [`nym-renew-request.v1.schema.json`](schemas-gen/schemas/nym-renew-request.v1.md) | `8` | `6` | `yes` | `yes` | `1` | `1` |
| [`nym-succession.v1.schema.json`](schemas-gen/schemas/nym-succession.v1.md) | `6` | `4` | `yes` | `yes` | `1` | `0` |
| [`peer-handshake.v1.schema.json`](schemas-gen/schemas/peer-handshake.v1.md) | `18` | `17` | `yes` | `yes` | `2` | `1` |
| [`procurement-contract.v1.schema.json`](schemas-gen/schemas/procurement-contract.v1.md) | `23` | `22` | `yes` | `yes` | `1` | `1` |
| [`procurement-offer.v1.schema.json`](schemas-gen/schemas/procurement-offer.v1.md) | `22` | `21` | `yes` | `yes` | `1` | `1` |
| [`procurement-receipt.v1.schema.json`](schemas-gen/schemas/procurement-receipt.v1.md) | `18` | `17` | `yes` | `yes` | `1` | `1` |
| [`proof-of-personhood-attestation.v1.schema.json`](schemas-gen/schemas/proof-of-personhood-attestation.v1.md) | `19` | `10` | `yes` | `yes` | `1` | `4` |
| [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md) | `30` | `30` | `yes` | `yes` | `2` | `2` |
| [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) | `18` | `17` | `yes` | `yes` | `1` | `1` |
| [`retrieval-request.v1.schema.json`](schemas-gen/schemas/retrieval-request.v1.md) | `11` | `11` | `yes` | `yes` | `1` | `1` |
| [`retrieval-response.v1.schema.json`](schemas-gen/schemas/retrieval-response.v1.md) | `14` | `13` | `yes` | `yes` | `1` | `1` |
| [`signal-marker.v1.schema.json`](schemas-gen/schemas/signal-marker.v1.md) | `12` | `8` | `yes` | `yes` | `1` | `1` |
| [`signal-transform-event.v1.schema.json`](schemas-gen/schemas/signal-transform-event.v1.md) | `15` | `11` | `yes` | `yes` | `0` | `0` |
| [`training-job.v1.schema.json`](schemas-gen/schemas/training-job.v1.md) | `13` | `13` | `yes` | `yes` | `1` | `1` |
| [`transcript-bundle.v1.schema.json`](schemas-gen/schemas/transcript-bundle.v1.md) | `18` | `2` | `no` | `yes` | `3` | `1` |
| [`transcript-segment.v1.schema.json`](schemas-gen/schemas/transcript-segment.v1.md) | `21` | `6` | `no` | `yes` | `3` | `1` |
| [`ubc-allocation.v1.schema.json`](schemas-gen/schemas/ubc-allocation.v1.md) | `17` | `12` | `yes` | `yes` | `1` | `2` |
| [`ubc-settlement.v1.schema.json`](schemas-gen/schemas/ubc-settlement.v1.md) | `16` | `7` | `yes` | `yes` | `1` | `1` |
| [`whisper-interest.v1.schema.json`](schemas-gen/schemas/whisper-interest.v1.md) | `12` | `11` | `yes` | `yes` | `1` | `1` |
| [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md) | `23` | `23` | `yes` | `yes` | `3` | `2` |
| [`whisper-threshold-reached.v1.schema.json`](schemas-gen/schemas/whisper-threshold-reached.v1.md) | `13` | `12` | `yes` | `yes` | `1` | `1` |

## Schema Project Lineage

| Schema | Requirements | Stories |
|---|---|---|
| [`adapter-artifact.v1.schema.json`](schemas-gen/schemas/adapter-artifact.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`answer-room-metadata.v1.schema.json`](schemas-gen/schemas/answer-room-metadata.v1.md) |  |  |
| [`archival-package.v1.schema.json`](schemas-gen/schemas/archival-package.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`archivist-advertisement.v1.schema.json`](schemas-gen/schemas/archivist-advertisement.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`association-room-proposal.v1.schema.json`](schemas-gen/schemas/association-room-proposal.v1.md) |  | [`story-005.md`](project/30-stories/story-005.md) |
| [`capability-advertisement.v1.schema.json`](schemas-gen/schemas/capability-advertisement.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`corpus-entry.v1.schema.json`](schemas-gen/schemas/corpus-entry.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`curation-decision.v1.schema.json`](schemas-gen/schemas/curation-decision.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`eval-report.v1.schema.json`](schemas-gen/schemas/eval-report.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`knowledge-artifact.v1.schema.json`](schemas-gen/schemas/knowledge-artifact.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`learning-outcome.v1.schema.json`](schemas-gen/schemas/learning-outcome.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`model-card.v1.schema.json`](schemas-gen/schemas/model-card.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`node-advertisement.v1.schema.json`](schemas-gen/schemas/node-advertisement.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`node-identity.v1.schema.json`](schemas-gen/schemas/node-identity.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`nym-certificate.v1.schema.json`](schemas-gen/schemas/nym-certificate.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`nym-issue-request.v1.schema.json`](schemas-gen/schemas/nym-issue-request.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`nym-renew-rejected.v1.schema.json`](schemas-gen/schemas/nym-renew-rejected.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`nym-renew-request.v1.schema.json`](schemas-gen/schemas/nym-renew-request.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`nym-succession.v1.schema.json`](schemas-gen/schemas/nym-succession.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`peer-handshake.v1.schema.json`](schemas-gen/schemas/peer-handshake.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md) |
| [`procurement-contract.v1.schema.json`](schemas-gen/schemas/procurement-contract.v1.md) | [`requirements-001.md`](project/50-requirements/requirements-001.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`procurement-offer.v1.schema.json`](schemas-gen/schemas/procurement-offer.v1.md) | [`requirements-001.md`](project/50-requirements/requirements-001.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`procurement-receipt.v1.schema.json`](schemas-gen/schemas/procurement-receipt.v1.md) | [`requirements-001.md`](project/50-requirements/requirements-001.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`proof-of-personhood-attestation.v1.schema.json`](schemas-gen/schemas/proof-of-personhood-attestation.v1.md) |  |  |
| [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) |  | [`story-001.md`](project/30-stories/story-001.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`retrieval-request.v1.schema.json`](schemas-gen/schemas/retrieval-request.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`retrieval-response.v1.schema.json`](schemas-gen/schemas/retrieval-response.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`signal-marker.v1.schema.json`](schemas-gen/schemas/signal-marker.v1.md) |  |  |
| [`signal-transform-event.v1.schema.json`](schemas-gen/schemas/signal-transform-event.v1.md) |  |  |
| [`training-job.v1.schema.json`](schemas-gen/schemas/training-job.v1.md) | [`requirements-002.md`](project/50-requirements/requirements-002.md), [`requirements-003.md`](project/50-requirements/requirements-003.md), [`requirements-004.md`](project/50-requirements/requirements-004.md), [`requirements-005.md`](project/50-requirements/requirements-005.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-002.md`](project/30-stories/story-002.md), [`story-003.md`](project/30-stories/story-003.md), [`story-004.md`](project/30-stories/story-004.md) |
| [`transcript-bundle.v1.schema.json`](schemas-gen/schemas/transcript-bundle.v1.md) |  |  |
| [`transcript-segment.v1.schema.json`](schemas-gen/schemas/transcript-segment.v1.md) |  |  |
| [`ubc-allocation.v1.schema.json`](schemas-gen/schemas/ubc-allocation.v1.md) |  |  |
| [`ubc-settlement.v1.schema.json`](schemas-gen/schemas/ubc-settlement.v1.md) |  |  |
| [`whisper-interest.v1.schema.json`](schemas-gen/schemas/whisper-interest.v1.md) |  | [`story-005.md`](project/30-stories/story-005.md) |
| [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md) | [`requirements-006.md`](project/50-requirements/requirements-006.md) | [`story-001.md`](project/30-stories/story-001.md), [`story-005.md`](project/30-stories/story-005.md) |
| [`whisper-threshold-reached.v1.schema.json`](schemas-gen/schemas/whisper-threshold-reached.v1.md) |  | [`story-005.md`](project/30-stories/story-005.md) |

## Schema Traceability

| Governing Doc | Schemas |
|---|---|
| [`doc/normative/40-constitution/pl/CONSTITUTION.pl.md`](normative/40-constitution/pl/CONSTITUTION.pl.md) | [`proof-of-personhood-attestation.v1.schema.json`](schemas-gen/schemas/proof-of-personhood-attestation.v1.md), [`signal-marker.v1.schema.json`](schemas-gen/schemas/signal-marker.v1.md), [`signal-transform-event.v1.schema.json`](schemas-gen/schemas/signal-transform-event.v1.md), [`ubc-allocation.v1.schema.json`](schemas-gen/schemas/ubc-allocation.v1.md), [`ubc-settlement.v1.schema.json`](schemas-gen/schemas/ubc-settlement.v1.md) |
| [`doc/normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md`](normative/50-constitutional-ops/pl/RAW-SIGNAL-POLICY.pl.md) | [`signal-marker.v1.schema.json`](schemas-gen/schemas/signal-marker.v1.md), [`signal-transform-event.v1.schema.json`](schemas-gen/schemas/signal-transform-event.v1.md) |
| [`doc/normative/50-constitutional-ops/pl/SWARM-ECONOMY-SUFFICIENCY.pl.md`](normative/50-constitutional-ops/pl/SWARM-ECONOMY-SUFFICIENCY.pl.md) | [`ubc-settlement.v1.schema.json`](schemas-gen/schemas/ubc-settlement.v1.md) |
| [`doc/normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md`](normative/50-constitutional-ops/pl/UBC-LIMIT-PROFILES.pl.md) | [`proof-of-personhood-attestation.v1.schema.json`](schemas-gen/schemas/proof-of-personhood-attestation.v1.md), [`ubc-allocation.v1.schema.json`](schemas-gen/schemas/ubc-allocation.v1.md) |
| [`doc/normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md`](normative/50-constitutional-ops/pl/UNIVERSAL-BASIC-COMPUTE.pl.md) | [`proof-of-personhood-attestation.v1.schema.json`](schemas-gen/schemas/proof-of-personhood-attestation.v1.md), [`ubc-allocation.v1.schema.json`](schemas-gen/schemas/ubc-allocation.v1.md), [`ubc-settlement.v1.schema.json`](schemas-gen/schemas/ubc-settlement.v1.md) |
| [`doc/project/20-memos/nym-authored-payload-verification.md`](project/20-memos/nym-authored-payload-verification.md) | [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md) |
| [`doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`](project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md) | [`nym-certificate.v1.schema.json`](schemas-gen/schemas/nym-certificate.v1.md), [`nym-issue-request.v1.schema.json`](schemas-gen/schemas/nym-issue-request.v1.md), [`nym-renew-rejected.v1.schema.json`](schemas-gen/schemas/nym-renew-rejected.v1.md), [`nym-renew-request.v1.schema.json`](schemas-gen/schemas/nym-renew-request.v1.md), [`nym-succession.v1.schema.json`](schemas-gen/schemas/nym-succession.v1.md) |
| [`doc/project/20-memos/orbiplex-anon.md`](project/20-memos/orbiplex-anon.md) | [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md) |
| [`doc/project/20-memos/orbiplex-whisper.md`](project/20-memos/orbiplex-whisper.md) | [`association-room-proposal.v1.schema.json`](schemas-gen/schemas/association-room-proposal.v1.md), [`whisper-interest.v1.schema.json`](schemas-gen/schemas/whisper-interest.v1.md), [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md), [`whisper-threshold-reached.v1.schema.json`](schemas-gen/schemas/whisper-threshold-reached.v1.md) |
| [`doc/project/30-stories/story-001.md`](project/30-stories/story-001.md) | [`procurement-contract.v1.schema.json`](schemas-gen/schemas/procurement-contract.v1.md), [`procurement-offer.v1.schema.json`](schemas-gen/schemas/procurement-offer.v1.md), [`procurement-receipt.v1.schema.json`](schemas-gen/schemas/procurement-receipt.v1.md), [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md), [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) |
| [`doc/project/30-stories/story-002.md`](project/30-stories/story-002.md) | [`knowledge-artifact.v1.schema.json`](schemas-gen/schemas/knowledge-artifact.v1.md), [`learning-outcome.v1.schema.json`](schemas-gen/schemas/learning-outcome.v1.md) |
| [`doc/project/30-stories/story-003.md`](project/30-stories/story-003.md) | [`archival-package.v1.schema.json`](schemas-gen/schemas/archival-package.v1.md), [`archivist-advertisement.v1.schema.json`](schemas-gen/schemas/archivist-advertisement.v1.md), [`retrieval-request.v1.schema.json`](schemas-gen/schemas/retrieval-request.v1.md), [`retrieval-response.v1.schema.json`](schemas-gen/schemas/retrieval-response.v1.md) |
| [`doc/project/30-stories/story-004.md`](project/30-stories/story-004.md) | [`procurement-contract.v1.schema.json`](schemas-gen/schemas/procurement-contract.v1.md), [`procurement-offer.v1.schema.json`](schemas-gen/schemas/procurement-offer.v1.md), [`procurement-receipt.v1.schema.json`](schemas-gen/schemas/procurement-receipt.v1.md), [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md), [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) |
| [`doc/project/30-stories/story-005.md`](project/30-stories/story-005.md) | [`association-room-proposal.v1.schema.json`](schemas-gen/schemas/association-room-proposal.v1.md), [`whisper-interest.v1.schema.json`](schemas-gen/schemas/whisper-interest.v1.md), [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md), [`whisper-threshold-reached.v1.schema.json`](schemas-gen/schemas/whisper-threshold-reached.v1.md) |
| [`doc/project/40-proposals/003-question-envelope-and-answer-channel.md`](project/40-proposals/003-question-envelope-and-answer-channel.md) | [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md) |
| [`doc/project/40-proposals/004-human-origin-flags-and-operator-participation.md`](project/40-proposals/004-human-origin-flags-and-operator-participation.md) | [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) |
| [`doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`](project/40-proposals/008-transcription-monitors-and-public-vaults.md) | [`archival-package.v1.schema.json`](schemas-gen/schemas/archival-package.v1.md), [`archivist-advertisement.v1.schema.json`](schemas-gen/schemas/archivist-advertisement.v1.md), [`curation-decision.v1.schema.json`](schemas-gen/schemas/curation-decision.v1.md), [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) |
| [`doc/project/40-proposals/009-communication-exposure-modes.md`](project/40-proposals/009-communication-exposure-modes.md) | [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md) |
| [`doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`](project/40-proposals/011-federated-answer-procurement-lifecycle.md) | [`procurement-contract.v1.schema.json`](schemas-gen/schemas/procurement-contract.v1.md), [`procurement-offer.v1.schema.json`](schemas-gen/schemas/procurement-offer.v1.md), [`procurement-receipt.v1.schema.json`](schemas-gen/schemas/procurement-receipt.v1.md), [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md), [`response-envelope.v1.schema.json`](schemas-gen/schemas/response-envelope.v1.md) |
| [`doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`](project/40-proposals/012-learning-outcomes-and-archival-contracts.md) | [`archival-package.v1.schema.json`](schemas-gen/schemas/archival-package.v1.md), [`archivist-advertisement.v1.schema.json`](schemas-gen/schemas/archivist-advertisement.v1.md), [`knowledge-artifact.v1.schema.json`](schemas-gen/schemas/knowledge-artifact.v1.md), [`learning-outcome.v1.schema.json`](schemas-gen/schemas/learning-outcome.v1.md), [`retrieval-request.v1.schema.json`](schemas-gen/schemas/retrieval-request.v1.md), [`retrieval-response.v1.schema.json`](schemas-gen/schemas/retrieval-response.v1.md) |
| [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](project/40-proposals/013-whisper-social-signal-exchange.md) | [`association-room-proposal.v1.schema.json`](schemas-gen/schemas/association-room-proposal.v1.md), [`whisper-interest.v1.schema.json`](schemas-gen/schemas/whisper-interest.v1.md), [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md), [`whisper-threshold-reached.v1.schema.json`](schemas-gen/schemas/whisper-threshold-reached.v1.md) |
| [`doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`](project/40-proposals/014-node-transport-and-discovery-mvp.md) | [`capability-advertisement.v1.schema.json`](schemas-gen/schemas/capability-advertisement.v1.md), [`node-advertisement.v1.schema.json`](schemas-gen/schemas/node-advertisement.v1.md), [`node-identity.v1.schema.json`](schemas-gen/schemas/node-identity.v1.md), [`peer-handshake.v1.schema.json`](schemas-gen/schemas/peer-handshake.v1.md) |
| [`doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`](project/40-proposals/015-nym-certificates-and-renewal-baseline.md) | [`nym-certificate.v1.schema.json`](schemas-gen/schemas/nym-certificate.v1.md), [`nym-issue-request.v1.schema.json`](schemas-gen/schemas/nym-issue-request.v1.md), [`nym-renew-rejected.v1.schema.json`](schemas-gen/schemas/nym-renew-rejected.v1.md), [`nym-renew-request.v1.schema.json`](schemas-gen/schemas/nym-renew-request.v1.md), [`nym-succession.v1.schema.json`](schemas-gen/schemas/nym-succession.v1.md), [`question-envelope.v1.schema.json`](schemas-gen/schemas/question-envelope.v1.md), [`whisper-signal.v1.schema.json`](schemas-gen/schemas/whisper-signal.v1.md) |
| [`doc/project/50-requirements/requirements-001.md`](project/50-requirements/requirements-001.md) | [`procurement-contract.v1.schema.json`](schemas-gen/schemas/procurement-contract.v1.md), [`procurement-offer.v1.schema.json`](schemas-gen/schemas/procurement-offer.v1.md), [`procurement-receipt.v1.schema.json`](schemas-gen/schemas/procurement-receipt.v1.md) |
| [`doc/project/50-requirements/requirements-002.md`](project/50-requirements/requirements-002.md) | [`corpus-entry.v1.schema.json`](schemas-gen/schemas/corpus-entry.v1.md), [`knowledge-artifact.v1.schema.json`](schemas-gen/schemas/knowledge-artifact.v1.md), [`learning-outcome.v1.schema.json`](schemas-gen/schemas/learning-outcome.v1.md) |
| [`doc/project/50-requirements/requirements-003.md`](project/50-requirements/requirements-003.md) | [`archival-package.v1.schema.json`](schemas-gen/schemas/archival-package.v1.md), [`archivist-advertisement.v1.schema.json`](schemas-gen/schemas/archivist-advertisement.v1.md), [`corpus-entry.v1.schema.json`](schemas-gen/schemas/corpus-entry.v1.md), [`curation-decision.v1.schema.json`](schemas-gen/schemas/curation-decision.v1.md), [`retrieval-request.v1.schema.json`](schemas-gen/schemas/retrieval-request.v1.md), [`retrieval-response.v1.schema.json`](schemas-gen/schemas/retrieval-response.v1.md) |
| [`doc/project/50-requirements/requirements-004.md`](project/50-requirements/requirements-004.md) | [`adapter-artifact.v1.schema.json`](schemas-gen/schemas/adapter-artifact.v1.md), [`corpus-entry.v1.schema.json`](schemas-gen/schemas/corpus-entry.v1.md), [`curation-decision.v1.schema.json`](schemas-gen/schemas/curation-decision.v1.md), [`eval-report.v1.schema.json`](schemas-gen/schemas/eval-report.v1.md), [`model-card.v1.schema.json`](schemas-gen/schemas/model-card.v1.md), [`training-job.v1.schema.json`](schemas-gen/schemas/training-job.v1.md) |
| [`doc/project/50-requirements/requirements-006.md`](project/50-requirements/requirements-006.md) | [`capability-advertisement.v1.schema.json`](schemas-gen/schemas/capability-advertisement.v1.md), [`node-advertisement.v1.schema.json`](schemas-gen/schemas/node-advertisement.v1.md), [`node-identity.v1.schema.json`](schemas-gen/schemas/node-identity.v1.md), [`peer-handshake.v1.schema.json`](schemas-gen/schemas/peer-handshake.v1.md) |
| [`doc/project/60-solutions/node.md`](project/60-solutions/node.md) | [`capability-advertisement.v1.schema.json`](schemas-gen/schemas/capability-advertisement.v1.md), [`node-advertisement.v1.schema.json`](schemas-gen/schemas/node-advertisement.v1.md), [`node-identity.v1.schema.json`](schemas-gen/schemas/node-identity.v1.md), [`peer-handshake.v1.schema.json`](schemas-gen/schemas/peer-handshake.v1.md) |

- Canonical schemas: `38`
- Generated schema docs: `38`
- Positive examples: `49`
- Negative examples: `42`
