# Resource Opinions and Discussion Surfaces

Orbiplex could support participant-authored opinions about arbitrary resources,
not only about nodes, participants, or contracts.

The minimal resource identity would be:

- `resource-kind`
- `resource-id`

Examples:

- `resource-kind = "url"` with `resource-id = "https://example.org/article"`
- `resource-kind = "ean"` with `resource-id = "5901234123457"`
- `resource-kind = "node"` with `resource-id = "node:did:key:z6MkExampleNode"`
- `resource-kind = "org"` with `resource-id = "org:did:key:z6MkExampleOrg"`
- `resource-kind = "gps"` with `resource-id = "51.107883,17.038538"`

The canonical resource key would be:

- `resource-key = resource-kind + ":" + resource-id`

This keeps the identity rule small while letting one system discuss many kinds
of external objects. Consumers should treat `resource-id` as opaque within a
given `resource-kind`; parsing the composite key should therefore split only on
the first `:`.

## Minimal Opinion Shape

One opinion record should be able to carry at least:

- envelope `record/about[0].resource/kind`
- envelope `record/about[0].resource/id`
- optional derived `resource/key` in read models
- envelope `author/participant-id`
- required free-text opinion body (`opinion/text`)
- optional `opinion/lang`
- optional coarse integer `opinion/rating` in `-1|0|1`
- envelope `authored/at`

This produces a simple contract:

- the target resource is stable,
- the opinion may be verbal,
- the verbal part can declare its language,
- and the resource may additionally receive one coarse scalar rating.

## Sketch: `resource-opinion.v1`

If this idea becomes a concrete artifact, the first portable shape could be:

- `schema = "resource-opinion.v1"`
- `opinion/text`
- optional `opinion/lang`
- optional `opinion/rating`
- optional `opinion/tags`

The concrete Agora envelope carries subject, author, timestamp,
signature, topic routing, and the canonical record id; the
`resource-opinion.v1` content body intentionally does not duplicate
those fields.

Recommended ingest invariants:

1. envelope `resource/kind` MUST be a small stable classifier such as `url`, `ean`,
   `node`, `org`, or `gps`
2. envelope `resource/id` MUST be treated as opaque within the given kind
3. `resource/key`, when projected, MUST equal `resource/kind + ":" + resource/id`
4. content `opinion/text` MUST be a non-empty string
5. content `opinion/rating`, when present, MUST be one of `-1`, `0`, or `1`
6. content `opinion/lang`, when present, annotates `opinion/text`
7. envelope `author/participant-id` SHOULD use the canonical `participant:did:key:...`
   shape

Example:

```json
{
  "schema": "agora-record.v1",
  "record/kind": "opinion",
  "topic/key": "ai.orbiplex.opinions/url",
  "record/about": [
    { "resource/kind": "url", "resource/id": "https://example.org/article" }
  ],
  "author/participant-id": "participant:did:key:z6MkExample",
  "authored/at": "2026-04-10T08:15:00Z",
  "content/schema": "resource-opinion.v1",
  "content": {
    "schema": "resource-opinion.v1",
    "opinion/text": "Useful overview, but the sourcing is thin in the final section.",
    "opinion/lang": "en",
    "opinion/rating": 1
  }
}
```

## Why This Is Useful

This gives the system one lightweight social layer for:

- reviews of public URLs, products, media, institutions, offers, nodes, swarm
  organizations, or geographic places,
- structured yet low-cost recommendation traces,
- and future aggregation or discovery without forcing one global ontology of
  resource types.

It should stay distinct from participant or node reputation:

- resource opinions describe the perceived quality or meaning of a resource,
- reputation signals describe standing, conduct, or trust attached to a subject.

This remains true even when `resource-kind` is `node` or `org`: the opinion is a
review or discussion surface, not a reputational verdict. Consumers must not
silently translate resource ratings into reputation or governance effects.

## Discussion Extension

A resource opinion system could later grow an attached discussion surface for the
same canonical resource key.

The first extension could be one of:

- a `channel-id` associated with the resource,
- or a less ephemeral `forum-thread-id` / comment thread.

That medium could admit both:

- human-authored messages,
- and AI-agent-authored messages operating on behalf of users or operators.

If this extension is pursued, the contract should make authorship explicit so
readers can distinguish:

- direct human speech,
- operator-approved agent speech,
- and autonomous agent contributions recorded under bounded policy.

## Open Questions

- Should `resource-id` be stored only as submitted, or also in a normalized form
  per `resource-kind`?
- Should `node` and `org` opinions require extra labeling or moderation because
  they can be confused with reputation?
- Should `gps` use WGS84 decimal `lat,lon`, geohash, or another
  precision-bounded location key?
- Should one author be allowed many opinions per resource, or only one current
  opinion plus append-only revisions?
- Should `opinion/rating` be optional on every opinion, or should rating and text be
  split into separate artifact families?
- Should the future discussion surface be ephemeral (`channel`) or archival
  (`forum`) by default?
- How should moderation, visibility, and federation policy attach to resource
  discussions without collapsing them into generic chat?

Related:

- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`

Promote further to: requirements or schema work when resource normalization,
revision/moderation rules, and discussion-surface semantics are frozen.
