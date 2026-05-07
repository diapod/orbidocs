# Orbiplex Semantic Index

`Orbiplex Semantic Index` is a node-local read-model component that turns
selected Memarium facts and other policy-accepted knowledge artifacts into
searchable semantic projections. It is not a memory store and it is not a
source of truth. It is a rebuildable index derived from append-only facts.

## Executive Summary

Memarium remains the authoritative local memory organ. Semantic Index is a
separate projection layer that periodically extracts eligible facts, computes
embeddings, writes them into a local vector index, and exposes retrieval-oriented
queries to agents, middleware, and future personal model tooling.

The first production-oriented backend should be SQLite-based, preferably with a
vector extension such as `sqlite-vec` once the dependency is adopted. Until then,
a plain SQLite table with stored vectors is acceptable for small local datasets
and smoke tests. Larger installations may later use a dedicated vector database
through the same adapter contract.

## Context and Problem Statement

Several project documents already require local retrieval assets and vector
memory, while Memarium deliberately does not freeze a concrete full-text or
vector-index implementation:

- `doc/project/50-requirements/requirements-001-node-onboarding.md` requires
  indexing discovered local content into a vector store and local orchestrator
  memory.
- `doc/project/30-stories/story-002-federated-peer-learning.md` allows accepted
  learning outcomes to be promoted into vector memory, indexed files, or a local
  knowledge-artifact queue.
- `doc/project/40-proposals/036-memarium.md` defines `MemariumIndex` as a
  rebuildable projection and leaves full-text and semantic index structures as
  runtime concerns.
- `doc/project/40-proposals/047-classification-label-propagation.md` states that
  embeddings, summaries, and other derivatives do not automatically declassify
  their inputs.

The missing component is a concrete solution-level boundary for semantic
indexing: where the embeddings live, how they are refreshed, which policies gate
them, and which future clustering/model-training jobs may consume them without
coupling directly to Memarium internals.

## Proposed Model / Decision

Semantic Index is a node-attached projection component:

```text
Memarium facts / promoted knowledge artifacts
  -> eligibility policy
  -> extraction and redaction
  -> embedding job
  -> semantic-index store
  -> retrieval API / clustering jobs / training-candidate selection
```

The canonical source remains:

```text
Memarium append-only facts
```

The rebuildable projection is:

```text
<data-dir>/semantic-index/semantic-index.sqlite
```

Implementations may choose a different backend path, but the important contract
is that the semantic index is outside the primary Memarium store. A corrupt,
missing, or stale semantic index must not corrupt or redefine Memarium facts; it
must be rebuildable from authorized source records.

### Storage Backend Ladder

1. **M1: plain SQLite**
   - Store vector bytes, dimensions, model id, source refs, classification, and
     extraction metadata.
   - Use brute-force similarity for small datasets and tests.
   - Keep this path simple and inspectable.
2. **M2: SQLite vector extension**
   - Adopt `sqlite-vec`, `sqlite-vss`, or a similar local extension when the
     operational dependency is accepted.
   - Keep the same domain adapter and data contract.
   - Treat ANN/HNSW/index internals as backend concerns, not Memarium semantics.
3. **M3: dedicated vector backend**
   - Allow a dedicated vector database behind the same adapter when local SQLite
     no longer meets latency, size, or concurrent query requirements.
   - Preserve Memarium as the source of truth and keep classification/egress
     gates at the component boundary.

### Periodic Projection

Semantic Index should be maintained by bounded jobs, not by ad hoc synchronous
work hidden inside Memarium writes.

The intended default loop is:

1. Read the last semantic-index cursor.
2. Pull new or changed eligible Memarium facts.
3. Apply classification, redaction, and extraction policy.
4. Compute embeddings through a configured embedding provider.
5. Upsert vector rows with deterministic idempotency keys.
6. Record cursor, skipped/rejected counts, and projection lag.

This job is a natural consumer of the Replay Scheduler solution:

- scheduler owns timing, jitter, retry, pause/resume, and launch accounting;
- Semantic Index owns source eligibility, extraction, embedding, vector storage,
  and query semantics.

### Classification and Secrecy Invariants

Semantic Index must preserve the classification lattice:

- embeddings inherit the effective classification of their source material by
  default;
- extraction, summarization, clustering, and embedding do not automatically
  declassify data;
- lowering the output tier requires an explicit declassification trail;
- personal-space material must remain local and sealed according to the source
  policy before any public or federated use;
- vector rows must carry enough source refs and classification metadata for
  egress guards to deny unsafe retrieval.

The index may store private embeddings locally, but private embeddings are still
private derivatives. They must not be exported, clustered for public use, or used
for cross-node matching without an explicit policy transition.

### Retrieval Contract

Semantic Index queries should return references and snippets/summaries under
policy, not raw unbounded source material by default.

Typical query result fields:

- `source/id`
- `source/kind`
- `source/space`
- `source/classification`
- `embedding/model-id`
- `score`
- `matched/fragment-ref`
- `matched/redacted-text` or `matched/summary`, when allowed
- `policy/egress-decision`

The retrieval API should be usable by local orchestrators, JSON-e Flow steps,
Sensorium OS actions, and future personal model tooling without each of them
learning Memarium storage internals.

### Clustering and Local Micro-Model Preparation

Batch clustering is a downstream consumer of Semantic Index, not part of the
core retrieval path.

An external library such as `clostera` may be useful later for CPU-first
clustering of dense vectors on one machine. This fits these jobs:

- compact semantic-index rows into clusters and centroids;
- choose representative examples for local micro-model training;
- balance training candidates so repeated material does not dominate;
- detect recurring themes in personal, community, or public memory;
- group similar public Whisper, gossip, opinion, or moderation records.

The cluster output should be another derived artifact, for example:

```text
semantic-cluster.v1
```

It must preserve classification and provenance. Clusters and centroids are not
truth; they are read-model artifacts derived from source facts.

## Must Implement

### Rebuildable Semantic Projection

Based on:

- `doc/project/40-proposals/036-memarium.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/50-requirements/requirements-001-node-onboarding.md`
- `doc/project/30-stories/story-002-federated-peer-learning.md`

Responsibilities:

- maintain semantic index rows as an eventually consistent projection;
- store projection cursors and diagnostics separately from Memarium facts;
- rebuild from Memarium and accepted knowledge artifacts;
- expose stale/lagging/skipped/rejected projection status to operators.

Status:

- `planned`

### SQLite-First Vector Backend

Based on:

- `doc/project/40-proposals/036-memarium.md`

Responsibilities:

- provide a local SQLite backend under `<data-dir>/semantic-index/`;
- support a simple fallback path without requiring a production vector extension;
- allow later replacement by `sqlite-vec` or another SQLite vector extension
  without changing Semantic Index callers;
- keep backend-specific ANN structures out of protocol and Memarium contracts.

Status:

- `planned`

### Classification-Aware Extraction

Based on:

- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/60-solutions/018-classification/018-classification.md`

Responsibilities:

- require source classification on every indexed item;
- carry source refs, effective tier, bound subjects, and declassification trail
  into index metadata;
- prevent retrieval from returning material above the caller's allowed tier;
- treat embeddings and clusters as derivatives requiring their own policy
  checks.

Status:

- `planned`

### Bounded Projection Jobs

Based on:

- `doc/project/60-solutions/020-scheduler/020-scheduler.md`

Responsibilities:

- run extraction and embedding refresh as bounded scheduler jobs;
- use idempotency keys derived from source id, source revision/fact sequence,
  stage, and embedding model id;
- report projection lag, retryable failures, permanent policy denials, and
  embedding provider errors;
- support operator pause/resume/retry without modifying Memarium facts.

Status:

- `planned`

## May Implement

### Dedicated Vector Store Adapter

Responsibilities:

- move vector similarity search to a dedicated backend when SQLite no longer
  satisfies size or latency requirements;
- preserve the same domain adapter and query semantics;
- keep source-of-truth and classification gates unchanged.

Status:

- `optional`

### Batch Clustering Worker

Responsibilities:

- cluster indexed vectors into derived semantic groups;
- create representative examples for local micro-model training;
- emit classification-preserving `semantic-cluster.v1`-style artifacts;
- support optional libraries such as `clostera` without adding them to Memarium
  or Node core.

Status:

- `optional`

### Personal Micro-Model Dataset Preparation

Responsibilities:

- select, balance, and redact local training candidates from semantic clusters;
- keep dataset preparation separate from model-weight mutation;
- require explicit operator or policy approval before using Personal material
  for training.

Status:

- `optional`

## Out of Scope

- replacing Memarium as the source of truth;
- storing vector rows inside the primary Memarium database;
- federated Memarium replication;
- public export of private embeddings without explicit declassification;
- model training or model-weight mutation;
- choosing one mandatory vector database for all implementations;
- treating clusters, centroids, or summaries as authoritative facts.

## Consumes

- `MemariumFact`
- `MemariumEntry`
- `classification.v1`
- `knowledge-artifact.v1`
- `learning-outcome.v1`
- local embedding-provider configuration
- scheduler job launches

## Produces

- semantic index rows
- semantic projection cursors and diagnostics
- retrieval query responses
- optional `semantic-cluster.v1`-style derived artifacts
- optional training-candidate manifests

## Failure Modes and Mitigations

| Failure mode | Risk | Mitigation |
| :--- | :--- | :--- |
| Index becomes stale | Retrieval misses recent facts | Store projection cursors, expose lag, allow manual retry. |
| Backend corruption | Retrieval returns wrong or missing matches | Treat index as rebuildable; never mutate Memarium based on index state. |
| Embedding leaks private material | Private derivative becomes public signal | Carry classification and bound-subject metadata on every row; enforce egress gates. |
| Model upgrade changes vector space | Mixed embeddings become meaningless | Include `embedding/model-id` and dimensionality in idempotency keys and query filters. |
| Over-eager indexing contaminates retrieval | Untrusted or unresolved material appears as knowledge | Gate indexing by promotion policy and source classification. |
| Clustering becomes semantic authority | Derived clusters override facts | Treat clusters as read-model artifacts with provenance, never as source truth. |

## Open Questions

1. Which embedding provider should be the first local default?
2. Should the first implementation use plain SQLite only, or adopt `sqlite-vec`
   immediately?
3. What is the initial query API shape: host capability, middleware-local HTTP
   API, or both?
4. What is the first `semantic-cluster.v1` data shape, if clustering is enabled?
5. Which Personal-space facts are eligible for indexing by default, if any?

## Next Actions

1. Define a minimal Semantic Index adapter trait in the node implementation.
2. Add a SQLite backend under `<data-dir>/semantic-index/`.
3. Add a scheduler job that transfers eligible Memarium facts into the index.
4. Add classification-aware query tests.
5. Add an operator-visible projection status surface.

## External References

- `clostera`: `https://github.com/BaseModelAI/clostera` — potential optional
  batch clustering engine for dense vectors. It should remain a downstream
  worker/backend choice, not a core Memarium dependency.
