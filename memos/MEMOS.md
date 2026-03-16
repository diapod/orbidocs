# Memos Index

This directory holds short idea notes, seeds, and design prompts that are not yet mature enough to become proposals, requirements, or stories.

## Communication and Assistance

- `swarm-broadcast-assistance.md` - a user opens a communication window to the swarm as a whole and asks for help with an important issue.
- `swarm-communication-exposure-modes.md` - three exposure modes for user requests: `private-to-swarm`, `federation-local`, and `public-call-for-help`.
- `swarm-question-channel-transports.md` - candidate transport classes for question envelopes and large answer-channel conversations with redundant servers.
- `transcription-monitors-and-public-vaults.md` - transcription-monitor nodes preserve valuable discussions as source transcripts and archivist nodes publish them into durable vaults for later synthesis and training.
- `human-expertise-escalation.md` - the swarm asks a human specialist behind a node for help when it reaches the edge of its own certainty or competence.

## User Orientation and Filtering

- `filtrum.md` - a personal filtering component that prioritizes content based on user preferences, goals, characteristics, and current condition, potentially through a browser extension.

## Node UX and Discovery

- `client-simplicity.md` - node client should stay simple to install, configure, and run.
- `wide-caps.md` - hierarchical capability advertisement and lightweight semantic matching between node capabilities.

## Trust, Safety, and Control

- `bad-actors.md` - detecting bad actors and excluding or penalizing them through consensus.
- `model-requests.md` - requests may specify model fingerprints that must or must not be used.

## Promotion Rule

Each memo should remain short. When an idea gains stable semantics, explicit actors, or implementation pressure, promote it into one of the following:

- `stories/` for user-facing scenarios,
- `proposals/` for architectural direction,
- `requirements/` for concrete system requirements,
- `constitutional-ops/` if it becomes normative.
