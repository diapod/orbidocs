# Proposal 100: Text Origin Labels and Propagation

Status: **Proposed (Draft)**. Date: **2026-11-09**.

Based on:

- [Vision](../../normative/20-vision/en/VISION.en.md), "Culture as a Low-Pass
  Filter" (synthetic content displacing human content)
- [P004: Human-Origin
  Flags](004-human-origin-flags-and-operator-participation.md)
  and `doc/project/50-requirements/requirements-005-transcript-segments.md`
  (today's `origin_class` vocabulary)
- [P047: Classification Label
  Propagation](047-classification-label-propagation.md)
  (label as data, join, edge-first staging, deferred `Tainted<T>`)
- [P090: Inference Execution
  Provenance](090-inference-execution-provenance-and-non-local-disclosure.md)
  (a separate axis that must compose with origin)
- [P013: Whisper](013-whisper-social-signal-exchange.md)
  (declared material origin and the "AI-assisted" label)
- [P064: Inquirium Implementation
  Recommendations](064-inquirium-implementation-recommendations.md)
  (observation transport and prompt-injection boundaries)

## Executive Summary

Text loses its origin as soon as it becomes a plain string. Today only
answer-room transcripts record where text came from, using one of three values,
and `node-generated` does not distinguish model output from static software
text. Other carriers declare origin by hand or not at all.

This proposal defines a small, set-valued **text origin label** that travels
with text segments across Node and middleware. A label records who produced the
words (`origin/classes`) and which origins could have shaped them
(`origin/influence`). It reuses P013's `origin/processing` for what was done to
the text and P090's evidence vocabulary for how the label was established, so
each fact keeps one spelling. Labels combine only by union, so no ordinary
operation can remove a name. An absent or lost label means `unknown`, which
every consumer treats as the worst case.

The label is deliberately sticky, in the spirit of taint flags in kernels and
templating systems. It is a provenance record: it grants nothing and proves no
authorship.

On the wire a label is a group of sorted name lists beside the text. In Rust it
is a small `Copy` value held beside existing text fields. A text type with no
implicit exit to `str` is reserved for paths where an audit shows label loss.
In Python it is a `str` subclass whose loss is detected at egress. Enforcement
starts at the edges, following P047; the interior is labeled only where text is
actually composed.

This proposal does not:

- prove that a human or a model wrote a given text;
- define confidentiality (P047), execution locality (P090) or material source
  (P013);
- change participation modes or room policy in P004;
- replace `String` across the codebase;
- enforce a gate on `origin/influence` in its first slice (section 14 starts
  in observe-only mode).

## Context and Problem Statement

| Existing carrier | Owner | Meaning | Gap |
| --- | --- | --- | --- |
| `origin_class` on transcript segments | P004, requirements-005 | One of `node-generated`, `node-mediated-human`, `human-live` | Transcripts only; model and software text are one value |
| `provenance/origin-classes` on response envelopes | `response-envelope.v1` | Classes materially present in an answer path | The settlement host derives it from one human-linked boolean |
| `origin/processing` with `model-assisted` | P013 | Publisher's declaration on a signed signal | Declared per publication, not tracked with the text |
| `classification.v1` | P047 | Who may see the data | Different axis |
| Inference execution provenance | P090 | Where inference ran | Different axis; P090 rejected merging it with origin |
| `PromptLayerOrigin` | Inquirium | Which host layer contributed a prompt layer | Host assembly fact, not text authorship |

Without a shared label, several questions have no answer once text has passed
through a few components: whether a summary rests on model output, whether a
corpus entry contains synthetic text, and whether a static host message is
being presented as an answer.

A search of Node on 2026-11-09 found no consumer of P047's `Classified<T>`
envelope outside its own crate, while `classification` travels as a sibling
field in 16 files. That is evidence for sibling fields on the wire, and against
assuming that a wrapper type will spread by itself.

## Proposed Model

### 1. A label is four small sets of named values

| Field | Question | Names | Vocabulary owner |
| --- | --- | --- | --- |
| `origin/classes` | Who produced these words? | Producer names | This proposal |
| `origin/influence` | What could have shaped them? | Producer names | This proposal |
| `origin/processing` | What was done to the text? | `extracted`, `grouped`, `human-edited`, `model-assisted`, `redacted`, `software-edited`, `summarized` | P013; `human-edited` and `software-edited` are added by P100-010 |
| `origin/evidence` | How was `origin/classes` established? | Evidence names | P090, plus `host-observed` and `module-declared` |

| Producer name | Meaning |
| --- | --- |
| `human` | Entered through a human-operated surface. Not proof of human composition: pasted model output is indistinguishable |
| `model` | Produced by an inference runtime |
| `software` | Produced by deterministic code: static templates, host messages, generated reports |
| `external` | Obtained from outside the node's own actors (web page, mail, document, sensor text); author not established |
| `unknown` | Label absent, lost or unrecognized |

| Evidence name | Meaning |
| --- | --- |
| `host-observed` | This host saw the text enter through the named surface or leave the named runtime |
| `module-declared` | A local module or connector declared the label |
| `peer-attested` | A peer declared the label. A signature authenticates the claim, not its truth |
| `derived` | Computed from another carrier, such as a legacy field |
| `unknown` | No basis is recorded |

Laws:

1. `origin/classes`, `origin/influence` and `origin/evidence` each hold at
   least one name. An empty set is invalid; it is not a way to say that nothing
   is known. `origin/processing` may be empty, which means that no step is
   recorded, not that none occurred.
2. `model-assisted` requires `model` in `origin/classes`, `human-edited`
   requires `human`, and `software-edited` requires `software`.
3. Join is field-wise set union: idempotent, commutative, associative and
   monotone. Valid labels stay valid under union.
4. No ordinary operation removes a name (see section 4).

`{human, model}` alone also arises from concatenating human text with model
text. `model-assisted` says that a model reworked supplied words,
`human-edited` that a human changed them, and `software-edited` that
deterministic code replaced or inserted words. None of them measures how much
changed, and a set does not record which came first.

| Situation | `origin/classes` | `origin/processing` | `origin/evidence` |
| --- | --- | --- | --- |
| Model answer | `{model}` | none | `{host-observed}` |
| Text typed by the operator | `{human}` | none | `{host-observed}` |
| Operator's text summarized by a model | `{human, model}` | `{model-assisted, summarized}` | `{host-observed}` |
| Model draft corrected by the operator on an edit surface | `{human, model}` | `{human-edited}` | `{host-observed}` |
| Operator's text changed by a host spelling corrector | `{human, software}` | `{software-edited}` | `{host-observed}` |
| Static host error message | `{software}` | none | `{host-observed}` |
| Web page quoted verbatim | `{external}` | none | `{host-observed}` |
| Text a peer labeled as human | `{human}` | none | `{peer-attested}` |
| Text a module returned as its own output | `{software}` | none | `{module-declared}` |
| Record that predates this proposal | `{unknown}` | none | `{unknown}` |

### 2. Two axes: who wrote it and what shaped it

A hostile web page can steer a model into writing text. The model authored
those words, yet the page influenced them. Prompt injection concerns influence,
so a single mask would hide the fact that matters most.

- `origin/classes` answers who produced these words.
- `origin/influence` answers which origins could have shaped them.

Both use the producer names. Text first admitted outside inference starts with
influence equal to its classes.

`origin/influence` is an upper bound only when every contributing segment is
labeled. Any unlabeled segment adds `unknown`, so during migration the field is
recorded and not used for decisions.

| Axis | Question | Owner | Join |
| --- | --- | --- | --- |
| `origin/classes` | Who produced these words? | P100 | Union |
| `origin/influence` | What could have shaped them? | P100 | Union |
| `origin/processing` | What was done to the text? | P013 vocabulary | Union |
| `origin/evidence` | How was `origin/classes` established? | P090 vocabulary | Union |
| Classification | Who may see this? | P047 | Most restrictive |
| Execution provenance | Where did inference run? | P090 | Conservative provenance join |
| Material origin | What source was it drawn from, as declared at publication? | P013 | Per publication |

Classification and execution provenance stay separate carriers. They are larger
values with their own join rules and cannot be reduced to bits.

### 3. An absent label means `unknown`

Templating systems mark text as *safe*, so a lost mark falls back to escaping.
A mark meaning "from a model" has the opposite polarity: once lost, the text
looks clean. This proposal therefore fixes the meaning of absence:

- a carrier with no label is read as `{unknown}` on both producer axes and for
  evidence, with no recorded processing;
- a name outside the closed vocabulary is refused by the schema on local
  carriers;
- carriers explicitly selecting the `ingress` profile in section 8 permit
  bounded unrecognized names in any facet; interpretation is facet-specific;
- `unknown` never projects to `human`, `software` or a legacy value that names
  an author (section 12);
- a consumer treats `unknown` as the worst case for its own decision.

This matches P013, where legacy records render origin as unknown, and P047,
where unlabeled ingress receives the highest restriction.

After a peer carrier passes its explicitly selected `ingress` schema and its
owner's applicable authentication checks, interpretation follows these rules:

| Facet | Unrecognized token |
| --- | --- |
| `origin/classes`, `origin/influence` | In the local interpretation, replace the token with `unknown`, keep all recognized names, then sort and deduplicate. Do not infer a missing producer from a processing token |
| `origin/evidence` | Ignore the incoming evidence claim whether recognized or not; the host stamps `peer-attested`. A bounded unknown evidence token does not invalidate interpretation. Outside the unchanged original carrier, it appears only in bounded diagnostics, never as interpreted evidence |
| `origin/processing` | Return the typed interpretation result `unsupported-processing-token`. The processing vocabulary has no `unknown` token; do not drop the operation or substitute an empty processing list |

The resulting producer interpretation still has to satisfy the laws in section
1.
For example, mapping an unrecognized producer to `unknown` does not satisfy
`human-edited`'s requirement for `human`. Such a label has a typed validity
refusal; interpretation must not invent the missing name.

An unsupported or invalid label is not a valid `TextOrigin` or a successful
empty-processing result. Consumers that require an interpreted label must not
automatically approve the operation from it. They expose the interpretation
failure and use their existing refusal or review path. This does not bypass
any existing publication or authority requirement.

Interpretation never rewrites signed arrays or reserializes a signed record as
its replacement. The original bytes remain the input to the carrier owner's
signature, schema and admission checks. Interpreting an unfamiliar label grants
no permission to admit a record rejected by those checks. A local interpretation
or diagnostic is a separate read model, not a repaired signed fact.

Required boundary vectors cover each facet, mixed recognized/unrecognized
processing tokens, preservation of recognized producer names, the cross-facet
validity refusal above, and unchanged signed bytes. Local closed-schema refusal
remains unchanged; a valid signature does not make an unsupported label known.
A strictly versioned signed carrier that rejects the token at Schema Gate never
enters this interpretation path. Being received from a peer does not select the
`ingress` profile. Module ingress retains section 5's `module-declared`
stamping.

Unknown processing remains a safe refusal to interpret in mixed-version
federations. The host provenance-ingress adapter owns the local diagnostic
store under S028; the pure codec returns diagnostics but performs no I/O.
The store is operator-only and uses a rolling seven-day retention window.
Reads and writes prune expired entries; restart does not restart retention.

A diagnostic key binds the admitted peer, carrier/schema version, receiver's
vocabulary version and sender's declared vocabulary version or `not-declared`.
Keep at most 256 keys and eight token samples per key, with one bounded overflow
aggregate for excess keys and counts. Samples retain the ingress token bound of
32 ASCII characters; counters saturate rather than creating more records.
The overflow aggregate follows the same seven-day retention. Samples expire
according to capture time, even if the same key receives later observations.

Peer-chosen samples are escaped at display and never exported, published,
sent to models or copied into notification payloads. Counts identify mismatch
for operator action without guessing an undeclared sender version. Repeated
failures update these counters rather than creating a review request each time.
The store grants no authority to relax interpretation or publication checks.

### 4. Labels grow; only an act replaces them

As with kernel taint flags, names accumulate. Producing a different label
requires a new artifact and a recorded act.

An operator approving a model draft does not change its label. Approval is a
separate fact owned by the surface that records it, such as a P066 consent or a
P013 publication review.

Editing is different, because the words change. When a surface holds the label
of the text it opens and receives changed text, the host keeps every existing
name, adds `human` to `origin/classes` and `origin/influence`, and adds
`human-edited` to `origin/processing`. One changed comma is enough, so
`human-edited` does not say that a human read or endorsed the whole text, and
it never removes `model`.

Deterministic code can also change words. A step that replaces or inserts words
in supplied text, such as a spelling corrector, keeps every existing name, adds
`software` to `origin/classes` and `origin/influence`, and adds
`software-edited` to `origin/processing`. A step that only trims, truncates,
normalizes or changes layout keeps the label unchanged (section 9). Composing
separately labeled segments stays a plain union.

Retyping text by hand, or pasting it into a surface with no link to its source,
yields a new `{human}` text. That cannot be prevented, and it is one reason
labels are not proof.

### 5. Who may assign which name

| Name | Assigned by |
| --- | --- |
| `human` | Host, on operator-facing input surfaces |
| `model`, `model-assisted` | Host, at the inference boundary. A module or peer may only relay them |
| `software` | Host or module, for its own static or generated text |
| `external` | Host or connector, at ingress of fetched, harvested or sensed text |
| `human-edited` | Host, on operator-facing edit surfaces that hold the source label. A module or peer may only relay it |
| `extracted`, `grouped`, `redacted`, `software-edited`, `summarized` | The party that performed the step |
| All of `origin/evidence` | Host only |

A module or peer cannot make a label more trustworthy. The host discards any
evidence that arrives with a label and writes its own: `module-declared` for a
module or connector, `peer-attested` for a peer. As in P090, a signature
authenticates a claim and does not promote it to `host-observed`.

A claimed `origin/influence` can only understate what shaped the text, so the
host adds `unknown` to it.

### 6. The inference boundary

No string operation crosses a model, because the output is new text. The host
therefore assigns the label when it receives a result:

- `origin/classes` is `{model}`;
- `origin/influence` is the union of `origin/classes` and `origin/influence` of
  every segment in the assembled context;
- `origin/evidence` is `{host-observed}` for a runtime that the host selected
  and dispatched, and `{peer-attested}` for a result returned by a peer.

An operation may be declared to rework supplied text:
`InquiriumOperation::Summarize`, `InquiriumOperation::Transform`, or a
host-selected flow that names its source segments. The host then also:

- adds the classes, processing and evidence of the source segments;
- records `model-assisted` in `origin/processing`, and `summarized` for
  `Summarize`.

The host never infers this from the content of the output.

Host prompt layers count as context, so influence on inference output almost
always contains `software`. Consumers test for the names relevant to them, such
as `external`, `unknown` or `model`.

Stamping is the first production source of `model-assisted`. A label containing
it does not by itself satisfy `MaterialLineage`, which still requires verified
inference lineage.

### 7. Granularity: segments, not characters

Union over a whole prompt quickly produces a label that names everything. Labels
therefore attach to segments that already exist: `InquiryContent`, prompt
layers,
`GenerateOutput` and transcript segments. Flattening segments into one string
joins their labels, so flattening should happen as late as possible. The
assembly trace keeps per-segment labels without content.

For `GenerateOutput::Structured`, the label covers the whole value. Strings
extracted from it inherit that label. Per-character spans are out of scope.

### 8. Wire form

A label is a group of sibling fields beside the text, never a wrapped string:

```json
{
  "type": "text",
  "text": "A short summary of the note.",
  "origin/classes": ["human", "model"],
  "origin/influence": ["external", "human", "software"],
  "origin/processing": ["model-assisted", "summarized"],
  "origin/evidence": ["host-observed"]
}
```

- Arrays are sorted and unique, and hold at most 16 names.
- `origin/classes`, `origin/influence` and `origin/evidence` appear together.
  Local writers omit `origin/processing` when empty; ingress may also carry
  an empty processing array. A partial label is invalid.
- `text-origin.v1` defines two explicit sub-schema profiles, `local` and
  `ingress`. The containing carrier selects one by `$ref`; a payload cannot
  select or override its profile. No schema failure triggers a profile fallback.
- `local` uses closed producer/evidence enums and references the processing
  definition in `whisper-origin.v2` (P100-010). It governs host authorship and
  local carriers.
- `ingress` bounds every token in all four facets to 1–32 ASCII characters,
  matching `^[a-z][a-z0-9-]{0,31}$` over the entire token, with an explicit
  length bound. Implementations match the entire token, for example with
  `re.fullmatch` in Python; trailing newlines are refused by the shared vectors.
  Every array has at most 16 tokens, is unique and sorted in ASCII byte order;
  the three required facets are
  nonempty. Processing may be omitted or empty. It permits unfamiliar names,
  not malformed structure or unbounded input. Schema acceptance precedes the
  separate semantic interpretation in section 3.
- The profiles share known spellings and interpreted validity laws. An ingress
  wire value is not deserialized directly into the closed `Processing` enum
  or treated as a validated `TextOrigin`.
- Labels on signed records are covered by the signature as canonical arrays.
- Numeric bit values never appear on the wire, in facts or in signatures. A
  rebuildable projection (S028) may store them only if positions are
  append-only.

The initial carrier disposition is:

| Carrier / boundary | Planned disposition |
| --- | --- |
| Local `InquiryContent`, prompt layers, normalized `GenerateOutput`, Whisper drafts and Python module output | `local` in their P100 carrier revisions; adapters cannot supply trusted labels |
| Proposed `response-envelope.v2` | One wire schema referencing `ingress`; P100-001 owns the schema and vectors. Host-authored output uses the typed emitter plus the local label check at `Boundary::Egress` |
| Proposed `transcript-segment.v2` authored by the local transcript owner | `local`; interpretation of peer source envelopes happens before transcript construction |
| Existing `response-envelope.v1` and `transcript-segment.v1` | Existing schemas and legacy projection only; no new ingress profile inferred |
| Peer import of `transcript-bundle.v1` | Strict import through its existing `transcript-segment.v1` reference; no ingress fallback |
| Proposed bundle version carrying `transcript-segment.v2` | P100-001 freezes its version and strict local-profile segment reference; peer import deterministically refuses vocabulary mismatch |
| `whisper-signal.v3` and its `whisper-origin.v1` dependency | Existing strict schemas; unknown processing is rejected before interpretation |
| Future signed records with a full text-origin label | No implicit adoption; a new carrier version must explicitly choose its profile |

P100-001 owns the new carrier schemas and their positive/refusal vectors,
including `response-envelope.v2`, `transcript-segment.v2` and the corresponding
bundle revision. It freezes the exhaustive carrier/version/profile inventory
with each owner. Schema Gate vectors establish that a bounded unfamiliar token
can reach interpretation through the peer envelope, while strict transcript
imports and existing signed carriers refuse mismatches. Expected interpretation
outcomes are vector data here; interpreter execution belongs to P100-002/003.
P100-005 implements carriers and projections against those frozen schemas.

There is exactly one wire schema for `response-envelope.v2`, referencing
`ingress`. Its host emitter accepts only validated `TextOrigin` values and
checks the label against `local` using the existing Schema Gate
`Boundary::Egress`, in addition to validating the full wire envelope. This is a
boundary check of the label, not a second envelope schema. Peer receipt uses
`Boundary::Ingress`, then the separate interpreter. Both checks keep the same
wire bytes; no profile is selected from untrusted payload data.

Until those new versions exist, this is a proposed contract, not runtime
compatibility. Signatures bind the original carrier, including unfamiliar but
schema-valid tokens; interpretation never changes those bytes.

### 9. Rust representation

```rust
/// Copy set of one facet's tokens. Union is the only combinator.
#[derive(Clone, Copy, PartialEq, Eq)]
pub struct TokenSet<T> {
    bits: u16,
    facet: PhantomData<T>,
}

/// A validated label. `classes`, `influence` and `evidence` are never empty.
#[derive(Clone, Copy, PartialEq, Eq)]
pub struct TextOrigin {
    classes: TokenSet<Producer>,
    influence: TokenSet<Producer>,
    processing: TokenSet<Processing>,
    evidence: TokenSet<Evidence>,
}

/// No `Deref`, `Display`, `AsRef<str>`, `From<String>` or direct serde impl.
pub struct AttributedText {
    text: String,
    origin: TextOrigin,
}
```

Peer wire input has a separate structural type in `text-origin-core`:

```rust
/// Private, bounded token vectors; structural validity only.
pub struct IngressOriginLabel {
    classes: Vec<IngressToken>,
    influence: Vec<IngressToken>,
    processing: Vec<IngressToken>,
    evidence: Vec<IngressToken>,
}

pub struct OriginInterpretation {
    pub result: Result<TextOrigin, OriginRefusal>,
    pub diagnostics: Vec<OriginDiagnostic>,
}

pub fn interpret(label: &IngressOriginLabel) -> OriginInterpretation;
```

`IngressToken` and the label have checked constructors/deserialization enforcing
section 8 before unbounded allocation. They validate structure, token limits,
ASCII ordering and uniqueness without requiring names to be known. The result
is never implicitly convertible into `TextOrigin`. `interpret` is pure and
specifically implements the peer-label rules in section 3; module and host
stamping remain distinct boundaries. It neither authenticates a peer nor admits
a carrier. Diagnostics are bounded by the input (at most 64 token entries);
the host attaches authenticated peer/version context and applies the store's
stricter sample/retention limits. No raw input is emitted as a valid label after
an interpretation refusal.

The bitset is chosen for its algebra rather than for memory: union is a single
OR, and the laws are trivial to property-test. Each facet has room for 16 tokens
and at most seven are in use. A `TextOrigin` is eight bytes, so `AttributedText`
is 32 bytes on 64-bit targets against 24 for `String`.

Local and interpreted carriers hold an optional `TextOrigin` beside their text.
Peer wire carriers hold `IngressOriginLabel` until interpretation (section 8).
`AttributedText` is introduced only on composition paths where an audit shows
that sibling fields lose labels (P100-008).

Where it exists, `AttributedText` deliberately does not behave like a string.
`Deref<Target = str>` would provide every string method, but each would return
an unlabeled `&str` or `String`, which is exactly how a label gets lost. P047
reached the same conclusion for `Tainted<T>`.

| Operation | Effect on the label |
| --- | --- |
| `as_text()` | Read-only, explicit and easy to search for; the result is unlabeled |
| `concat`, `join` | Union of all parts |
| `map_same_origin(f)` | Label kept; the caller states that `f` adds no new origin (trim, truncate, normalize). Never for a step that replaces or inserts words (section 4) |
| `into_parts()` | Explicit exit at an egress boundary |

`Debug` prints the labels and the byte length, never the text. Serialization
goes through the segment carriers in section 8. Union is an inherent `const fn`.
It obeys the same join laws as `classification::Join`, and the leaf crate
`text-origin-core` does not depend on that crate.

### 10. Python representation

Python exposes corresponding `IngressOriginLabel`, `OriginInterpretation`
and `interpret` contracts with the same structural checks, typed refusal codes
and bounded diagnostics. They use the shared vectors, including full-token
matching. The helper does not silently construct a trusted `LabeledStr` from
raw ingress tokens or from a failed interpretation.

The host delivers labels as JSON fields. A middleware helper,
`middleware-modules/lib/text_origin.py`, wraps the text in a `LabeledStr`
subclass of `str`, so existing code keeps working.

A probe on CPython 3.12.2 (2026-11-09) showed that a plain subclass loses its
label in all 15 operations tried, including `+`, slicing, `strip`, f-strings,
`join` and a JSON round trip. Overriding methods restores `"x" + t` and a lone
`f"{t}"`, but `f"{t}x"` and `"".join(...)` still return a plain `str`, and a
subclass cannot intercept them.

Propagation in Python therefore cannot be guaranteed, so loss must be safe:

- **a plain `str` reaching an egress helper is labeled `{unknown}`;**
- `LabeledStr` overrides the common operations and propagates by union;
- `join_labeled` and `format_labeled` cover what a subclass cannot intercept;
- a module's claim of `human` or `model` stays a declaration: the host writes
  `module-declared` as the evidence of anything a module returns (section 5).

### 11. Consumers at the edges

| Consumer | Rule |
| --- | --- |
| Whisper publication (P013) | Text whose `origin/classes` contains `model` must not be published without `model-assisted`. The label does not replace the verified inference lineage that `model-assisted` already requires. Text containing `unknown` cannot pass this check automatically and needs publication review. Drafts carry no label today, so this consumer includes that plumbing |
| Corpus | Keep the presence of human-origin material, promotion as human-origin material and training eligibility separate. Apply the criteria below; no origin label grants consent or training approval |
| Node UI | Shows the label as a badge; `unknown` is displayed as unknown, never hidden |
| Inquirium traces | Record per-segment labels and influence, without content |
| Future discussion artifacts (P026) | Reuse the label instead of a local flag |

#### Corpus presence, promotion and training

`contains-human-origin` describes the presence of human-originated source
material, not its eligibility. A recognized `human` contribution with an
evidence
basis accepted by the Corpus owner remains present in mixed material such as
`{human, model}`. A refusal to promote that mixture must not erase the human
contribution or bypass the consent rules that protect it. Lack of knowledge does
not establish `false`; when the source does not support a boolean assertion,
omit the optional field and preserve uncertainty in the label and provenance.
Use the same evidence-acceptance policy as promotion, defaulting to exactly
`{host-observed}`. For a valid, supported label with accepted evidence, set
`true` when `human` is present. Set `false` only when none of `human`, `unknown`
or `external` is present. Otherwise omit the field. Invalid/unsupported labels
or unaccepted evidence also yield omission, not `false`; thus a peer's claimed
`human` with `peer-attested` is omitted by default.

Automatic human-origin promotion requires all of:

1. A valid, supported label with `human` in `origin/classes`.
2. Neither `model` nor `unknown` in `origin/classes`.
3. No `external` contribution with unestablished authorship. Mixed
   `{human, external}` material requires explicit Corpus review rather than
   automatic promotion; review does not remove names from the label.
4. `origin/evidence` exactly `{host-observed}`, unless the Corpus owner's
   explicit policy accepts another basis. The original evidence basis remains
   visible; accepting it does not promote it to `host-observed`.

For `{human, software}`, composition facts mean the retained per-segment
labels in section 7's host assembly trace, bound to the exact candidate text.
No new peer assertion or separate composition artifact is introduced. Automatic
promotion requires all ordinary origin/evidence conditions and a complete trace:
no contributing segment is purely `{software}`, and every segment containing
`software` also contains `human` and records `software-edited`.

These conditions apply to retained source segments before concatenation. A
segment that has already flattened an unknown composition cannot establish them;
its source segments must still be available in the assembly trace, otherwise
review is required. This prevents a template and an edited human sentence from
being flattened into a single apparently eligible `{human, software}` segment.
An aggregate label alone requires review. A segment-level decision covers only
the selected eligible segments, not an aggregate containing an excluded
template.
No ratio of human to software words is inferred.

These are origin conditions only. `training/eligibility` remains a separate
curation decision (`blocked`, `needs-review` or `approved`) governed by consent,
the training profile and P004. Passing the origin conditions never sets it to
`approved`. The label still records observed entry or declared provenance, not
proof of human composition.

Required consumer vectors, with an otherwise accepted evidence basis:

| `origin/classes` | `contains-human-origin` | Automatic human-origin promotion |
| --- | --- | --- |
| `{human}` | `true` | Origin conditions met; independent consent and curation still apply |
| `{human, software}` | `true` | Only with the composition/segment evidence above; otherwise review |
| `{software}` | `false` | Refused: no `human` contribution |
| `{model}` | `false` | Refused: model contribution |
| `{external}` | Omitted | Refused: no established `human` contribution |
| `{human, model}` | `true` | Refused; the accepted human contribution remains recorded |
| `{human, unknown}` | `true` | Refused; uncertainty remains visible |
| `{human, external}` | `true` | Requires explicit Corpus review |
| `{unknown}` | Omitted | Refused; absence of knowledge does not establish `false` |

The suite also covers default refusal of `peer-attested` and `module-declared`
for promotion, an explicit policy accepting another evidence basis without
rewriting it, default omission of presence for `{human}` with `peer-attested`,
and consent refusal after all origin conditions pass. Composition vectors
include
human text edited by software, human text concatenated with a software template,
and that same concatenation also carrying `software-edited`: the token must not
bypass aggregate review. Invalid/unsupported labels never produce a presence
assertion or automatic promotion.

#### Publication projection

A publication is a broader projection than a segment. Any segment with `model`
in `origin/classes` makes the publication declare `model-assisted`, even when
no segment carries that value, because `origin/processing` on a publication
summarizes the whole material. `human-edited` and `software-edited` reach a
publication only on a contract version that defines them. Projecting to
`whisper-origin.v1` withholds them.

Effect gating on `origin/influence` is limited to the surfaces in section 14
and starts in observe-only mode.

### 12. Migration from `origin_class`

New labels project onto the existing closed enum in room contexts:

| New `origin/classes` | Legacy `origin_class` |
| --- | --- |
| Only `human`, and `operator-presence/mode` is `direct-live` | `human-live` |
| Contains `human` in any other case | `node-mediated-human` |
| Contains neither `human` nor `unknown` | `node-generated` |
| Contains `unknown` and no `human` | Omitted |

Reading old records must not invent facts the old value does not hold:

| Legacy `origin_class` | New `origin/classes` |
| --- | --- |
| `node-generated` | `{unknown}`: the old value cannot separate model from software |
| `node-mediated-human` | `{human, unknown}` |
| `human-live` | `{human}` |

Labels read this way carry `origin/evidence` `{derived}` and `origin/influence`
`{unknown}`.

A label with `unknown` and no `human` has no faithful legacy value. Writing
`node-generated` would turn absence into a declaration, which `ProjectionLaw`
forbids. `transcript-segment.v1` and `response-envelope.v1` require legacy
values and cannot express that case, so new versions make `origin/classes` the
required field and the legacy fields optional. No Rust or Python code implements
the transcript fields yet, so they need no data migration. Middleware binds
`provenance/origin-classes`, which keeps its current derivation until the new
envelope version exists.

New eligibility decisions must read the new label and must not use a legacy
projection as input.

### 13. Digests, adapters and export

- **Digests.** An unlabeled segment serializes without label fields, so its
  historical bytes do not change. `instruction/hash` identifies instructions
  given to the model, and labels never reach the model, so it is computed from
  a text-only projection. Every other commitment over a carrier decides
  inclusion explicitly.
- **Adapters.** Labels are never sent to a provider or written into prompt text.
  The host ignores any label in an adapter response and stamps the result
  itself.
- **Export.** `human` can reveal that an operator took part. Labels leaving the
  node follow P004 visibility and selective disclosure: a projection may
  withhold a label but cannot strengthen it.

### 14. Effect gating on `origin/influence`

`origin/influence` may gate only irreversible or outgoing effects, on four
surfaces. No other surface reads it for a decision.

| Surface | Effect | Entry point on 2026-11-09 |
| --- | --- | --- |
| Whisper publication | A signal leaves the node | Publication review in `daemon/src/weak_signal_harvester/review` |
| Message sending | A message leaves the node | `enqueue_outbound` in `messaging-service` |
| Actuation | A directive changes the world | `sensorium-actuation-core` |
| Settlement | Value moves | `daemon/src/settlement_host.rs` |

Gating starts in `observe-only` mode, which is the default on every surface.
The gate evaluates its rules and writes an audit-only record of what it would
decide. The effect proceeds exactly as it would without the gate, even if
evaluation fails.

- **Rules are data.** A versioned table yields `allow`, `ask` or `deny` for each
  surface and producer name, and each surface's owner owns its rows. Rules do
  not test `software`, because host prompt layers are almost always in context.
- **`allow` means only that no rule fired.** Pasted attack text is `human`
  (section 4), so `human` proves nothing about safety.
- **Influence travels with the request.** An effect request carries the
  `origin/influence` of the text that caused it. A request without it reads as
  `{unknown}`, and the record shows a coverage gap.
- **Approval is a separate fact.** `ask` maps to a P066 consent bound to the
  surface and a digest of the effect's arguments. It never removes a name.
- **Records hold no content.** They hold the surface, rule-table version,
  would-be decision, triggering names, contributing segment references and
  whether a fresh human act already covers the effect. They never reach a model
  or a peer.

An alarm means that text could have been shaped, not that an attack happened.
Real attacks are rare, so counting every alarm without an attack as false would
report nearly 100% and decide nothing. Observe-only mode therefore reports four
measures per surface:

| Measure | Definition | What it decides |
| --- | --- | --- |
| Added interruptions | Share of effects with a would-be `ask` or `deny` and no fresh human act | Operator burden |
| Cause split | Whether the trigger is only `unknown`, a name from the current turn or a name inherited from an earlier turn | Whether to fix coverage, rules or inheritance between turns |
| Reviewed false alarms | Share of a reviewed sample in which a reviewer judges that no human look was needed | Precision of the rules |
| Threat-case detection | Share of replayed injection cases that the rules catch | Whether the gate earns its cost |

Each surface's owner records acceptance thresholds before collection starts. A
surface moves to enforcement through an explicit host-owned setting, which a
module or model cannot request, and only when its thresholds are met and path
coverage is proven. Under enforcement, a failed evaluation fails closed.

If inherited names dominate, looser rules are the wrong remedy. The candidate
fix is quarantined reading: a separate inference without tool access returns
narrowly typed values. That is an Inquirium architecture decision outside this
proposal.

## Scenario: a note rewritten and published

1. The operator types a note in Node UI. The segment has `origin/classes`
   `{human}` and `origin/evidence` `{host-observed}`.
2. Harvester attaches a web excerpt, labeled `{external}`.
3. A `Transform` request supplies both as source text, with a host prompt layer
   labeled `{software}`. The output has `origin/classes`
   `{external, human, model}`, `origin/processing` `{model-assisted}`,
   `origin/influence` `{external, human, software}` and `origin/evidence`
   `{host-observed}`.
4. A Python module trims the result with `LabeledStr.strip()`. The names
   survive. When the text returns, the host writes `{module-declared}` as the
   evidence and adds `unknown` to the influence.
5. The Whisper draft carries a label containing `model`, so publication must
   declare `model-assisted`. Public views render "AI-assisted".
6. The signed signal carries only P013's origin summary in the first slice. The
   full label stays local.

If step 4 had used `f"{text}\n"`, the host would receive a plain `str` and label
it `{unknown}`. Publication would then require review instead of silently
passing as clean text.

## Trade-offs

| Decision | Benefit | Cost |
| --- | --- | --- |
| Set of names instead of one enum | Mixtures stay expressible; union is trivial | Consumers test membership instead of matching one value |
| No implicit exit from `AttributedText` | Loss is visible in code review | Less convenient than a string |
| Sibling fields on the wire | Existing carriers evolve additively | Text and label can be separated by a careless reader |
| Closed names on local carriers | Typos and drift are refused at the schema gate | A new name needs a schema version and a release |
| Reusing the P013 and P090 vocabularies | Each fact keeps one spelling | A label has four fields and two upstream vocabulary owners |
| Observe-only before enforcement | Rules are tuned on real traffic without blocking anyone | Attacks are not stopped during measurement |
| Segment granularity | Reuses existing structure | Flattened text has only a coarse label |

## Failure Modes and Mitigations

| Failure | Mitigation |
| --- | --- |
| A label is dropped in an interior path | Absence reads as `unknown`, which is the worst case |
| Unbounded tokens enter through the open ingress profile | Enforce the ASCII token pattern, 32-character limit, 16 tokens per facet and structural rules before interpretation; test exact bounds and one beyond |
| Mixed-version peers repeatedly send unsupported processing | Bounded per-peer/version diagnostics expose incompatibility without relaxing refusal or flooding review |
| An unfamiliar processing token is silently erased | Return `unsupported-processing-token`; no valid empty-processing fallback and no automatic approval |
| Ingress normalization changes a signed fact | Interpret separately from original signed bytes; the carrier owner retains signature, schema and admission authority |
| Non-human material meets only the negative Corpus checks | Require positive `human` membership as well as the exclusion and evidence conditions |
| Mixed material loses its human contribution when promotion is refused | Keep `contains-human-origin` separate from promotion and training eligibility; preserve consent requirements and uncertainty |
| Python operations lose the label | Egress labels plain `str` as `{unknown}` |
| `human` is claimed for pasted model text | `human` is defined as surface entry, and labels are documented as non-proof |
| A peer or module claims `human` falsely | The host writes the evidence itself, and human-origin promotion refuses `peer-attested` and `module-declared` by default |
| `human-edited` is read as review or as removal of `model` | Section 4 defines it as a change only; approval stays a separate fact and `model` stays in the label |
| `software-edited` spreads to every deterministic step | Section 4 limits it to steps that replace or insert words in supplied text |
| A label changes a digest | Unlabeled segments keep their bytes, and `instruction/hash` uses a text-only projection |
| An adapter sets its own label | The host ignores labels in adapter responses and stamps the result |
| A legacy projection invents an author | Section 12 omits the legacy value when the label holds `unknown` and no `human` |
| `origin/influence` is trusted before coverage is complete | Enforcement is enabled per surface and only with proven coverage; any unlabeled segment adds `unknown` |
| Injected content floods the operator with approval requests | Only four surfaces can ask, and added interruptions are measured before enforcement |
| Union makes labels uninformative | Segments keep separate labels, and consumers test specific names |
| Labels are mistaken for authority | The label grants nothing; existing owners keep admission and consent |
| A consumer reuses the legacy projection for eligibility | Section 12 forbids it; the P100-006 consumers read the new label |

## Alternatives Considered

### Give the type every string capability through `Deref`

Rejected. Every method would return unlabeled text, so the label would disappear
at the first ordinary operation and no one would notice.

### Extend P047

Rejected. P047 governs confidentiality, with an ordered lattice, egress refusal
and declassification. Origin has no "more restrictive" order and cannot be
declassified.

### Extend P004 alone

Rejected. P004 is scoped to answer rooms and operator participation. This label
also concerns Inquirium, Whisper, Corpus and middleware.

### New modifiers for rewriting and assertion

Rejected. `origin/processing` already records that a model reworked material,
and P090 already names evidence bases. A second spelling would let them drift,
and one assertion flag would conflate a supervised local module with a remote
peer.

### Reuse `adapter-declared` for module labels

Rejected. P100 ignores labels from inference adapters (section 13), and P090
uses that name for reports about execution. The token would only ever describe
components that are not adapters.

### Record a human edit as a plain union

Rejected. `{human, model}` alone cannot be told apart from concatenated text.

### A separate value for shallow model edits

Rejected. The host cannot verify depth without reading the content, so a module
could declare the lighter value for a full rewrite.

### An enum listing every combination

Rejected. The number of combinations grows quickly, and union becomes a table
that has to be maintained.

### A numeric mask on the wire

Rejected. A number is opaque in JSON and would freeze bit positions across Rust,
Python and versions.

### One mask for all axes

Rejected. Authorship, influence, classification and locality have different
meanings and different join rules.

### Per-character spans

Rejected for now. The cost is high, and existing segments already cover the
known consumers.

## Open Questions

1. Should the name be `human` or `human-entered`? *Recommended default:*
   `human`, with the definition in section 1. `human-entered` is more accurate
   but more awkward.
2. How does a host-selected flow declare its source segments for
   `model-assisted`? *Assumption:* a field in the flow's host-owned definition,
   to be frozen with P100-004.
3. When should `origin/classes` enter signed records such as a future Whisper
   signal? *Recommended default:* after the local consumers have shown value.
   This does not defer the explicitly planned peer `response-envelope.v2`
   ingress profile in section 8; existing signed Whisper schemas remain strict.
4. Should an extensible peer carrier explicitly declare its `whisper-origin`
   vocabulary version? Freeze any such field with the carrier owner, including
   binding it to the signed carrier where applicable. Unsupported declared
   versions should produce a deterministic version/schema refusal rather than
   repeated content review. Until that contract exists, diagnostics use the
   known carrier version and `not-declared`, without guessing compatibility.

Resolved 2026-11-09:

1. `TextOrigin` lives in the leaf crate `text-origin-core`, licensed
   `Apache-2.0`.
2. `origin/influence` may gate only irreversible or outgoing effects: Whisper
   publication, message sending, actuation and settlement. Gating starts in
   observe-only mode and measures false alarms first (section 14).
3. Module and connector labels use `module-declared`.
4. A human edit is recorded as `human-edited`, and a deterministic step that
   replaces or inserts words as `software-edited`, symmetric to
   `model-assisted`.

## Next Actions

1. Review the vocabulary, laws and axes in this draft.
2. Change the `origin/processing` contract (P100-010).
3. Freeze `text-origin.v1` with positive and refusal vectors.

## Implementation Recommendations

These recommendations come from a convergence review against Node `989c84a31`
and the Orbidocs schema catalogue on 2026-11-09, following the "Reusable Data
Abstractions" and "Retrospective Convergence Review" rules in
`node/DEV-GUIDELINES.md`. They are planning input.

### Layers

| Layer | Owner | Holds | Must not hold |
| --- | --- | --- | --- |
| Contract | `text-origin.v1` sub-schema and golden vectors | Token spellings, validity laws, refusal cases | Consumer policy |
| Algebra and codec | New leaf crate `text-origin-core` | Closed token enums, token sets, `TextOrigin`, wire codec | Transports, carriers, policy |
| Carriers | Owner of each carrier, such as `inquirium-core` | An optional label beside existing text | A private copy of names or union |
| Stamping | `inquirium-host` and host ingress surfaces | Assignment of names at trust boundaries | What a label permits |
| Projections | Owner of each legacy field | Typed one-way derivations | New facts |
| Consumers | Whisper, Corpus, Node UI | Decisions | Label construction |

`text-origin-core` depends only on `serde` and `thiserror`. Existing owners
were checked first:

| Candidate owner | Why not |
| --- | --- |
| `whisper-core` | Owns publication semantics and sits too high for Inquirium and middleware |
| `inference-provenance-core` | Owns the execution axis, which P090 keeps separate from origin |
| `classification` | Owns confidentiality; `whisper-core`, `middleware`, `room-core` and `control` do not depend on it |
| `workflow-vocabulary` | Owns workflow status tokens |

The closest precedents are `workflow-vocabulary`, which owns wire tokens but no
policy, and `relative-path-core`, which owns one law with golden vectors.

### One source of truth per concept

| Concept | Source of truth | Action |
| --- | --- | --- |
| Who produced the words | `origin/classes` in `text-origin.v1` | New. `provenance/origin-classes` becomes its derived projection on response envelopes |
| How the text was processed | `origin/processing` in `whisper-origin`; `whisper-core::Processing` | Reuse at segment level. Move the Rust enum to `text-origin-core` and re-export it from `whisper-core`. The `local` sub-schema `$ref`s the contract definition; the bounded `ingress` profile uses those known spellings during interpretation. `human-edited` and `software-edited` need a new contract version (see below) |
| How well a label is established | `evidence-basis` in `inference-provenance-common.v1` | Reuse `peer-attested`, `derived` and `unknown`. P090's host tokens describe egress and its `adapter-declared` describes execution reports, so origin adds `host-observed` and `module-declared` |
| What source the material came from | `origin/source-kinds` in P013 | Keep at publication level and bridge it (table below) |

| `origin/source-kinds` | `origin/classes` |
| --- | --- |
| `web`, `mail`, `document`, `sensorium` | `external` |
| `personal-report` | `human` |
| `unknown` | `unknown` |

These concepts stay separate:

| Field or type | Reason | Link to this label |
| --- | --- | --- |
| `gossip/source-kind` (`machine-assisted`) | Legacy disclosure aid, schema-only today | Derive `machine-assisted` from a label containing `model` |
| Whisper `source/class` | Signed authorship and preparation posture | Consistency check only |
| `corpus/model-class`, `hybrid` | Service posture mixing locality and authorship (P090 Decision 8) | None |
| `origin/collection-method`, `origin/coverage`, `origin/lineage` | Publication-level facts with different joins | None |
| `PromptLayerOrigin`, configuration `source/class`, `origin/actor-ref`, `CausalContext` | Similar words, different authority and lifecycle | None |

### Shared mechanism

The types in section 9 follow these rules:

- The facets share one algorithm and differ only in tokens, so one
  parameterized `TokenSet<T>` serves all of them. Distinct facet types keep a
  processing token from being tested against a producer set.
- A facet's capacity of 16 tokens matches the wire bound in section 8.
- Token enums come from a local macro in the style of `statuses!`, so that each
  declaration owns its wire spelling once. A test compares `ALL` with the
  schema enum, and the shared evidence names with `evidence-basis`.
- Parse, do not validate: private fields, `serde(try_from)` as in `WireOrigin`,
  and typed errors instead of panics.
- `TextOrigin::UNKNOWN` is the only representation of absence.
- Property tests prove the join laws in the style of the `classification`
  crate. Rust and Python run the same vectors from `protocol/contracts/golden`.
- Names are ASCII, so byte order, Rust `sort` and Python `sorted()` agree on
  the canonical array.

| Reuse candidate | Disposition | Revisit when |
| --- | --- | --- |
| `classification::Join` | Do not implement it from the leaf: that inverts layering for one external user. Use an inherent `const fn union` | A function generic over two lattices appears; then move the trait down |
| `ProjectionLaw` | Reuse for legacy projections. Implement on carriers in their owner crates | Not deferred |
| Closed-token macro | Local copy now; three variants already exist | A defect needs the same fix in two macros (owner: Node maintainers) |
| Registry as data (`vendor-media-types`) | Not needed for a small closed vocabulary | Names must ship without a Node release |
| `AttributedText` | Sibling fields first. `Classified<T>` has no consumer outside its crate, so a wrapper needs a demonstrated need | An audit finds label loss at a composition site |

### Carriers and digests

- Add optional fields with `#[serde(default, skip_serializing_if = ...)]`, so
  that unlabeled content keeps its historical bytes.
- Label `GenerateOutput::Text` first, then `InquiryContent::Text`, prompt
  layers and transcripts. `classification` stays request-wide beside
  per-segment labels.
- Add constructors such as `InquiryContent::text` before adding the field.
  About 95 construction sites exist, most of them in tests.
- Do not use `#[serde(flatten)]` on a type with `deny_unknown_fields`, because
  serde does not support that combination.
- `instruction_hash` serializes `InquiryTurn` values directly. Compute it from
  a text-only projection, since labels never reach the model, and pin the
  result with a regression test. Decide inclusion for every other commitment
  per carrier.

### Stamping

- `assembled_chat_messages` (`inquirium-host/src/lib.rs:2141`) is the point
  where segments flatten for a provider, and it already emits only role and
  text. Keep it that way, and add a test that labels do not reach the adapter
  body.
- `adapter_output_text` reads only `type` and `text`, although the adapter
  response schema allows additional properties. Stamp after normalization, on
  the return path that builds `BoundInferenceResult`, and test that an
  adapter-supplied `origin/classes` is ignored.
- Output capping (`inquirium-host/src/lib.rs:3395`) keeps the label unchanged.
- Stamping becomes the first production producer of
  `Processing::ModelAssisted`. It may feed `MaterialLineage` only through
  verified inference lineage.
- Before closing P100-004, list every other inference path with a disposition:
  `external-agent-runtime-*`, Agent controllers, JSON-e flows, `control[]` and
  streaming. A path left out stays `unknown`, which is safe but must be
  recorded.

### Legacy fields

- `origin_class`, `human_origin`, `contains_human_origin`,
  `contains-human-origin` and `human-linked/input` have no Rust or Python
  implementation yet. They can become derived fields in new schema versions
  without a data migration.
- `provenance/origin-classes` is bound in `middleware/src/marketplace.rs:705`
  as `Vec<String>` without a vocabulary check, and produced in
  `daemon/src/settlement_host.rs:1522` and `control/src/lib.rs:1917`. Parse it
  through the shared vocabulary. `middleware/tests/middleware_contract.rs:1385`
  uses values outside the schema enum, and that drift must be resolved first.

### Contract change for the edit values

`whisper-origin.v1` is closed, with `maxItems` 5, and `whisper-signal.v3`
references it inside signed content. `Processing` deserializes strictly, so an
older node refuses an unknown value. Editing v1 in place would break that
contract.

- Define `human-edited` and `software-edited` in `whisper-origin.v2`, with
  `maxItems` 7, and update P013 in both languages.
- The `local` profile of `text-origin.v1` references v2; `ingress` permits
  bounded wire tokens and interprets supported processing against that
  vocabulary.
  Existing schemas stay on v1 until their own
  next version, and projecting to v1 withholds both values, which
  `ProjectionLaw` allows.
- Record a disposition for each dependent: `whisper-signal.v3`,
  `whisper-origin-lineage.v1`, `public-gossip.v2`,
  `weak-signal-whisper-draft.local.v2` and `weak-signal-review.v1`.
- `whisper-signal-draft.local.v2` holds an inline copy of the enum. Its next
  version replaces that copy with a `$ref`.
- When `Processing` gains the variants, a test proves that a v3 signal carrying
  either value is still refused.
- The sync list in `scripts/sync-node-schemas.py`, the `ContractFamily` entries
  in `schema-gate` and the literals in `tools/acceptance/sensorium-web-v3`
  follow the new version.

### Effect gate

| Reuse candidate | Disposition |
| --- | --- |
| `observe-only` and `resolve_corpus_experiment_executor` | Reuse the token and the rule that an absent setting selects the safest mode. Keep a separate type, because that enum names Corpus executors |
| `MiddlewareEffectClass`, `MiddlewareEffectScope` | Consistency check, not the key. They describe declared middleware effects, while the gate names host surfaces. A component declaring `irreversible-external` or an `external` or `federated` scope outside the four surfaces is a review finding |
| `operator-consent-core` | Reuse for `ask`; P066 remains the only durable consent owner |
| `sensorium-directive-outcome.v1` | Precedent for an audit-only record |

The evaluator is a pure function of surface, influence and rule table. It does
not belong in `text-origin-core`, which holds no policy. *Assumption:* the four
surfaces meet in `daemon`, so it starts there and is extracted only if another
host needs it.

### Delivery and obligations

1. `whisper-origin.v2`, the `text-origin.v1` contract, vectors,
   `text-origin-core` and the `Processing` move. This step changes no behavior.
2. `GenerateOutput` stamping and trace fields, with the Node UI badge as the
   first consumer, because a badge needs no policy.
3. Whisper and Corpus checks. Whisper drafts carry no label today, so this step
   includes the plumbing.
4. The Python helper and middleware ingress. Python has no existing binding.
5. Room and transcript carriers.
6. The observe-only gate on the four surfaces, then enforcement per surface.

A new crate also requires a workspace entry, `rust-version.workspace`, an SPDX
header, `docs/development/source-headers.v1.json`,
`docs/implementation-ledger.toml` with a regenerated
`docs/IMPLEMENTATION-LEDGER.md`, and `docs/MVP.md`. The schema requires
`scripts/sync-node-schemas.py`, a `ContractFamily` in `schema-gate`, negative
fixtures and regenerated `doc/schemas-gen/**`.

`text-origin-core` is licensed `Apache-2.0` by owner decision on 2026-11-09.
Its Cargo manifest and SPDX headers declare that license, and
`docs/development/source-headers.v1.json` records the explicit grant, which
also covers `Processing` when it moves out of `whisper-core`. The Python helper
needs its own entry in that manifest.

## Implementation Tracker

Statuses: `todo`, `partial`, `blocked`, `done`. All entries are planned; `done`
requires the row's evidence and reconciliation with its implementation owner.

| ID | Task / owner | Depends on | Status | Completion gate |
| --- | --- | --- | --- | --- |
| P100-001 | Freeze vocabulary, laws and wire form / Orbidocs + Node | P100-010 | todo | `text-origin.v1` freezes local/ingress profiles and the exhaustive carrier/version/profile inventory; the local processing facet references `whisper-origin.v2`; P100-001 owns response-envelope.v2, transcript-segment.v2 and its bundle schema revision and all schema vectors; peer envelope vectors traverse Schema Gate with expected interpretation outcomes recorded as data, strict signed carriers refuse unknown tokens, and ingress bound/fallback tests (including trailing whitespace/newlines) pass; vectors and negative fixtures cover join laws, `model-assisted` without `model`, `human-edited` without `human`, `software-edited` without `software`, empty required sets, partial labels and names outside the closed vocabulary; section 3 vectors distinguish each facet, mixed known/unknown processing, cross-facet validity refusals and unchanged signed bytes |
| P100-002 | `text-origin-core` / Node | P100-001 | todo | Property tests prove the join laws; bounded IngressOriginLabel and the pure interpret API execute the frozen vectors; ingress interpretation preserves known producer names, stamps peer evidence regardless of incoming token knowledge and returns typed unsupported/invalid results without an empty-processing fallback; bounded result diagnostics pass; `Processing` moves out of `whisper-core` and gains `human-edited` and `software-edited`, while `whisper-signal.v3` still refuses both; bit positions stay out of facts and signatures; the crate declares `Apache-2.0` and the grant is recorded in the source-header manifest |
| P100-003 | `LabeledStr`, ingress interpretation and the egress rule / middleware | P100-001 | todo | Python IngressOriginLabel and interpret execute the same frozen vectors and refusal codes as Rust; tests pin the operations that lose a label and the `{unknown}` result at egress |
| P100-004 | Segment fields and inference stamping / Inquirium | P100-001, P100-002 | todo | Output labels follow section 6, including `Summarize`/`Transform`; labels leave `instruction/hash` unchanged; tests prove that labels do not reach the adapter body and that adapter-supplied labels are ignored; every other inference path has a recorded disposition; traces hold no content |
| P100-005 | Carrier implementation and legacy projections / Room and middleware owners | P100-001, P100-002 | todo | Implement the envelope, segment and bundle schemas frozen by P100-001; one envelope wire schema passes both boundary paths with the local label check at Egress; strict peer bundle import refuses mismatch; host-store checks cover seven-day expiry across restart, 256 keys plus overflow, eight samples per key and escaped operator-only display; both migration tables hold; new transcript and envelope versions require `origin/classes`; the legacy value is omitted where section 12 says so; `provenance/origin-classes` parses through the shared vocabulary |
| P100-006 | First consumers / Whisper, Corpus, Node UI | P100-004 | todo | Whisper drafts carry labels; the Whisper check refuses text labeled `model` without `model-assisted` and sends `unknown` to review; all section 11 Corpus vectors pass, including positive `human` membership, mixed external review, explicit true/false/omitted presence with the shared evidence policy, default evidence refusal, software-edit/concatenation/segment distinctions including a pre-flattened segment with missing ancestry, preservation of human contributions in mixtures and independent consent refusal; unsupported/invalid labels never authorize automatic approval; UI shows `unknown` |
| P100-007 | Observe-only gate on the four surfaces / Inquirium and surface owners | P100-004 | todo | All four surfaces evaluate the versioned rule table and write audit-only records without content; effects proceed unchanged, including when evaluation fails; thresholds are recorded before collection; the four measures in section 14 are reported per surface |
| P100-008 | Audit composition paths for `AttributedText` / Node | P100-004 | todo | A recorded finding per composition site; the type is added only where the audit shows label loss; where it exists, no implicit conversion to `str` exists and `Debug` never prints text |
| P100-009 | Enable enforcement per surface / surface owners and P064 owners | P100-007 | todo | A recorded decision per surface against its threshold; path coverage is proven; threat cases are replayed; `ask` uses a P066 consent bound to the effect digest; a failed evaluation fails closed |
| P100-010 | Add `human-edited` and `software-edited` to the `origin/processing` contract / Orbidocs + Whisper owners | — | todo | `whisper-origin.v2` defines both values and passes Schema Gate with negative fixtures; P013 lists them in both languages; every schema depending on v1 has a recorded disposition; projection to v1 withholds them; schema sync and generated artifacts are current |
| P100-011 | Stamp the edit values / Node UI, Whisper and step owners | P100-002 | todo | A surface holding the source label keeps its names and adds `human` and `human-edited` only when the text changed; approval without a change leaves the label unchanged; a surface with no link yields `{human}`; a step that replaces or inserts words adds `software` and `software-edited`; `map_same_origin` operations leave the label unchanged |
