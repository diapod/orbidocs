# Proposal 102: Community Brand and Naming Layers

Status: **Proposed (Draft)**. Date: **2026-11-18**.

Based on:

- [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md) and
  [Constitution](../../normative/40-constitution/en/CONSTITUTION.en.md): federation over
  centralization, human agency, auditability. This proposal names a social layer and
  creates no rights, no authority and no root trust.
- [ORBIPLEX-MAIN-ROOT-CHARTER](../../normative/50-constitutional-ops/en/ORBIPLEX-MAIN-ROOT-CHARTER.en.md)
  (`DIA-ROOT-001`): the governance home of the `orbiplex-main` root. Nothing here
  touches custody, threshold, roster or the root-pack ceremony.
- [P076: Federation Identity and Network Selector](076-federation-identity-and-network-selector.md):
  `federation_id` is a node-wide, pre-runtime **network selector**, in the sense that
  `mainnet` and `testnet` are selectors in distributed-ledger systems.
- `README.md` brand identity block: organization **Distributed Intelligence Agency**,
  system and protocol brand **Orbiplex**.

## Executive Summary

Adopt **Emergat** as the name of the first public community of people and operators
around Orbiplex. The community is deliberately **unincorporated**: it is not a legal
entity, not a service provider, and not a trademark holder.

This fills a gap rather than renaming anything. The project already names its
organization (Distributed Intelligence), its system and protocol family (Orbiplex),
and its federation root selector (`orbiplex-main`). It had no name for the social
body that gathers around them, and `orbiplex-main` was being borrowed for that
purpose even though it is a technical selector, not a community name.

The canonical written form is **Emergat**. The domains `emergat.org`, `emergat.io`
and `emergat.ai` are held by the project owner. `emergat.org` is the primary home,
because a top-level domain tied to a disputed territory code should not be
load-bearing for a name intended to outlive it.

## 1. Context and Problem Statement

### 1.1 Three named layers and one unnamed one

| Layer | Name | Where it is anchored |
| :--- | :--- | :--- |
| Umbrella organization | Distributed Intelligence Agency | `README.md`, Constitution |
| System and protocol family | Orbiplex | `README.md`, protocol documents |
| Federation root selector | `orbiplex-main` | P076, `DIA-ROOT-001`, `federation-root.v1` |
| **Community of people and operators** | **absent** | – |

**Fact.** `orbiplex-main` appears in canonical schema fixtures, for example
`doc/schemas/examples/orbiplex-main.federation-root.json`, and in the root charter as an
org-kind threshold root identity.

**Inference.** Because the social layer had no name, documents and conversations reached
for either `orbiplex-main` or `Orbiplex` when they meant "the people and nodes who take
part". Both substitutions are category errors: the first names a configuration value,
the second names software.

### 1.2 What `orbiplex-main` is and is not

**Fact.** P076 defines `federation_id` as a node-wide, pre-runtime network selector,
explicitly analogous to `mainnet` and `testnet`.

**Fact.** Per `DIA-ROOT-001` section 1, until the custodian roster and key table are
filled, a production `federation-root.v1` pack is signed and production packaging
disables the bundled fixture, `orbiplex-main` remains a development bootstrap fixture
and MUST NOT be treated as production root authority (P076-004).

**Inference.** A selector and a community name answer different questions. "Which
network is this node configured for?" is answered by a stable, boring identifier that
should never change for brand reasons. "Whose community is this?" is answered by a name
people say out loud. Conflating them would couple protocol configuration to social
identity, which is exactly the kind of entanglement the stratification rules forbid.

## 2. Decision

### 2.1 Naming layers after this proposal

| Layer | Name | Changes here? |
| :--- | :--- | :--- |
| Umbrella organization | Distributed Intelligence Agency | no |
| System and protocol family | Orbiplex | no |
| Federation root selector | `orbiplex-main` | **no** |
| Community of people and operators | **Emergat** | new |

### 2.2 Canonical orthography

The canonical form is **Emergat**: one word, one capital letter, no suffix.

Do not write `EmergatIO`, `EmergatIo` or `Emergat.io` as the community name. The domain
is an address, not part of the name. A name with four competing spellings is not a name.

The spelling **Emergatio** is recognized as a secondary reading of the `.io` address and
may be explained in community-facing prose, but it is not the canonical name. See
section 3.2.

### 2.3 Polish declension

Polish-language documents inflect the name natively, with no special scheme. This is a
deliberate advantage over `Orbiplex`, which required an explicit oblique stem
(`Orbipleks-`):

| Case | Form |
| :--- | :--- |
| Nominative | Emergat |
| Genitive | Emergatu |
| Dative | Emergatowi |
| Accusative | Emergat |
| Instrumental | Emergatem |
| Locative | w Emergacie |
| Vocative | Emergacie |

### 2.4 What this proposal does not change

1. No schema, fixture or `federation_id` value changes. `orbiplex-main` stays.
2. No normative act is amended. `DIA-ROOT-001` keeps its scope.
3. No legal entity is created, and no authority is delegated to the community as such.
4. No trademark application follows from this proposal (section 5.4).
5. The product and service naming question stays open (section 9).

## 3. Etymology and Semantics

### 3.1 Emergat

**Fact.** *Emergat* is the Latin present active subjunctive, third person singular, of
*emergere* ("to rise out, to surface"), formed from *e-* ("out of") and *mergere* ("to
submerge"). It means **"let it emerge"** or "may it come forth".

**Fact.** This places the name in the family of Latin subjunctives that entered English
as nouns: *fiat* ("let it be done"), *caveat* ("let them beware"), *exeat*, *placet*.

**Inference.** The name is therefore a **jussive**, not a description. Every other
candidate considered (section 8) named a thing: an allotment, a place, a sign, a
relation, a property. This one names an intention, and the intention it names –
emergence of capability from interaction between autonomous nodes – is the mechanism the
project exists to enable.

**Inference.** The suffix `-at` carries a second, analogical reading across European
languages as a marker of institutions and jurisdictions: *emirate*, *caliphate*,
*patriarchate*, *consulate*, *secretariat*. This reading is **analogical, not
etymological**: Latin `-atus` attaches to a noun of office (*consul* → *consulatus*), and
*emerg-* is not such a noun. The subjunctive reading is the strict one.

### 3.2 Emergatio

**Inference.** Read as a word, `EmergatIO` yields *Emergatio*, which scans as a Latin
verbal noun in `-tio` (genitive `-tionis`), the formation behind *creatio*, *generatio*,
*emanatio* and *communicatio*. The sense would be "the emerging, the act of coming
forth".

**Fact.** The classical deverbal noun from *emergere* is *emersio*, formed on the supine
stem *emersus*, as *immersio* is from *immergere*. *Emergatio* is not attested classical
Latin.

**Inference.** *Emergatio* is therefore a transparent neologism rather than a
restoration. Its value is that it completes a pair with the canonical name – *emergat*
as the call, *emergatio* as what the call names – which is why it is worth explaining
once in community prose and then leaving alone.

## 4. Registry and Domain Status

**Fact.** Domains held, as recorded in WHOIS on 2026-11-18, all registered through
Cloudflare:

| Domain | Created (UTC) | Registry expiry |
| :--- | :--- | :--- |
| `emergat.ai` | 2026-11-17T23:11:24Z | 2027-11-17 |
| `emergat.io` | 2026-11-17T23:22:51Z | 2027-11-17 |
| `emergat.org` | 2026-11-17T23:26:09Z | 2028-11-17 |

**Decision.** `emergat.org` is the primary community home. `emergat.io` and `emergat.ai`
redirect to it.

**Fact.** `.io` is the country-code top-level domain assigned to the British Indian Ocean
Territory. A UK–Mauritius treaty on the Chagos Archipelago was signed on 2025-05-22;
reporting as of this document's date is inconsistent about whether it is in force or
suspended, and no retirement of `.io` has been announced. Retirement would require the
`IO` code to leave ISO 3166-1, and the registry operator runs the TLD independently of
the territory's status.

**Inference.** The risk is remote and would unfold over years, so the domain is usable.
But a community name meant to last decades should not embed a TLD whose existence depends
on an unresolved sovereignty question. This is the second, independent reason the
canonical name excludes `io` (section 2.2).

**Fact.** Screened on 2026-11-15 and re-checked 2026-11-18: `emergat` was free on
crates.io and the npm registry, with zero repositories matching the name on GitHub.

## 5. Trademark Due Diligence

### 5.1 Method

Searched USPTO (`tmsearch.uspto.gov`) and TMview (`tmdn.org/tmview`) on 2026-11-18.

Each zero result was validated with a **control query** known to return hits, because an
earlier search in this workstream returned a false "no results found" when a URL
parameter was silently ignored. Exact-match queries were widened with wildcards, because
protection extends to confusingly similar marks, not only identical ones.

TMview states that it is not an official register and that its data has no legal effect.
Nothing in this section is a freedom-to-operate opinion; a formal clearance search is
attorney work.

### 5.2 Emergat itself

**Fact.** USPTO: `emergat` returns **0 results**. Control: `emergent` returns 214.

**Fact.** TMview: `emergat` returns **0 rows**. Control: `emergant` returns 2.

**Fact.** **No company** trading as "Emergat" was found.

### 5.3 The potentially conflicting mark: EMERGA

**Fact.** Widening to `emerga` in TMview returned 34 marks. The material ones belong to
**EmerGa Association**, Toulouse, France:

| Register | Number | Nice class | Scope | Status |
| :--- | :--- | :--- | :--- | :--- |
| France INPI | 5074358 | **42** | software design and development, SaaS, cloud computing, IT consultancy, server hosting, electronic data storage | registered 2024-11-15 |
| EUIPO | 019087755 | **9** | IT devices, software, databases (electronic and interactive), recorded data sets | registered, status date 2025-01-27 |

**Fact.** Also live: `EMERGA` at UKIPO in classes 9 and 35 (filed 2023-10-24), and
`EMERGA CHARGE` at EUIPO and UKIPO.

**Fact.** `EMERGANT` is live at USPTO in class **36** (financial investment in business
valuation), owned by Emergant LLC, Delaware, filed 2021-09-16 and 2021-09-17.

**Inference.** `EMERGA` and `EMERGAT` share their first six characters and differ only in
a final consonant. In similarity assessment the beginning of a mark carries the most
weight. The goods and services overlap completely with what a federated network service
would claim, and the EUIPO registration covers the whole Union. A trademark application
for `EMERGAT` in classes 9 or 42 would therefore be contested in at least two
jurisdictions.

**Inference.** `EMERGANT` is a weaker concern: a different interior letter, a different
class, and unrelated services.

### 5.4 Why this does not block the decision

**Inference.** Trademark rights restrain use **in commerce**, as a mark identifying goods
or services. An unincorporated community that offers no services under the name, sells
nothing and holds no mark operates outside that scope. The residual exposure is a demand
to stop using the name, not an opposition proceeding, because no application exists to
oppose.

**Decision.** Do not file a trademark application for Emergat. Record the EMERGA finding
here so that any later move toward formalization – a legal entity, a paid service, a
trademark – re-opens this section first rather than starting a fresh search.

**Constraint.** If the community ever formalizes and begins offering services under
the name in classes 9 or 42, this proposal must be revisited before that happens, not
after.

## 6. Trade-offs

**Benefits**

1. Fills the social layer without touching protocol, schemas or normative acts.
2. Names the project's mechanism (emergence) rather than its topography or its law.
3. Inflects natively in Polish, unlike `Orbiplex`.
4. Free across the technical registries checked, with no repository squatting.
5. A jussive name states an intention, which suits a community that grows by accession.

**Risks**

1. `EMERGA` blocks the trademark path in the EU and UK (section 5.3).
2. In English, `emerg-` is dominated by *emergency*, not *emergence*; non-technical
   listeners will hear the alarm sense first.
3. `g` before `a` is orthographically hard /g/, but analogy to *emerge* and *emergent*
   pulls some readers toward /dʒ/. Polish readers are unambiguous.
4. The `emergent` field is crowded (Emergent BioSolutions, Emergent Software, EmergentX),
   so search results will be noisy.
5. Initial unstressed `e-` reduces in English and is exposed to aphaeresis.

**Constraints**

1. The canonical spelling must be enforced in documentation and CI-adjacent text.
2. `orbiplex-main` must not be re-labelled in schemas or fixtures to match the community
   name.

## 7. Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| Spelling fragments into `EmergatIO`, `Emergatio`, `emergatIO` | Section 2.2 fixes one canonical form; style guidance and review enforce it |
| `Nemorat`/`Nemoron`-style typo lands on an English slur; swapping the adjacent `e`/`o` in related coinages produced *moron* during screening | Register defensive spellings only if abuse appears; do not treat typo space as free |
| Community name drifts into protocol identity, for example a `federation_id` rename | Section 2.4 forbids it; P076 keeps the selector decoupled |
| `.io` retired after a Chagos settlement | `emergat.org` is already primary; the name contains no TLD |
| EmerGa Association objects to the use | No mark is claimed, no services are offered under the name, and the community can rename its social layer without touching any protocol identifier |
| Readers take the `-at` institutional reading as etymological fact | Section 3.1 marks it as analogical |

## 8. Options Considered

Five candidates completed etymological, registry and – for the final four – trademark
review. Over one hundred further names were screened and rejected earlier in the same
workstream.

**Inference.** The two cleanest names rest on Greek roots nobody
commercialized. Emergat and another considered are encumbered because they stand on
roots with live, popular meaning in European languages. Accepting Emergat trades
legal exclusivity for semantic precision – a defensible trade for an unincorporated
community, and an indefensible one for a commercial service.

Whole families were rejected on structural grounds worth recording, so they are not
re-proposed:

- **Descriptive stems** (`connector`, `tech-`, `code-`, `base-`): unprotectable as mark
  elements, discounted in similarity assessment, and invisible in search. `coden`
  additionally collides with CODEN, the bibliographic serial identifier administered
  through the International CODEN Service – a clash inside this project's own
  metadata vocabulary.
- **Property-naming suffixes** (`-ity`: *basity*, *codencity*, *comensity*): these name a
  quality, not a community or a place.
- **Component morphology** (`-rium`, `-rion`): `memarium`, `sensorium` and `inquirium` are
  already parts. A whole must not wear the morphology of its parts, which also rules out
  otherwise attractive forms.
- **The `sem-` prefix**, despite σημεῖον ("sign") being the best-fitting root found: in
  English, `sem-` before `i` or `u` is heard as `semi-` ("half"), and before `e`+`n` it
  produces *semen*. Only `sema-` is safe, which left just two acceptable forms.
- **`ageron`**, from ἀγείρω ("to gather, to convene") – semantically ideal for a
  federation – collides with a well-known individual's identity in the machine-learning
  community. Its derivatives would additionally collide inside this repository,
  where *agora* is already taken by
  [S021 Agora Authority](../60-solutions/021-agora-authority/021-agora-authority.md).

## 9. Open Questions

1. **Product and service naming.** Emergat names the community. The user-facing
   application and the hosted service are still unnamed.
2. **Umbrella organization.** Whether "Distributed Intelligence Agency" (or
   "Distributed Intelligence") stays is a separate decision and is not addressed
   here.
3. **Formalization trigger.** No criterion is yet defined for when the community would
   need a legal form, which is also when section 5 must be re-opened.
4. **Localized community prose.** Whether `Emergatio` is explained in Polish and Czech
   community material, or only in English.

## 10. Next Actions

1. Add **Emergat** to the glossary with the layer boundary from section 2.1 and the
   declension table from section 2.3.
2. Point `emergat.io` and `emergat.ai` at `emergat.org`.
3. State the canonical spelling rule from section 2.2 wherever documentation style is
   defined, so review can enforce it.
4. Re-open section 5 before any of: incorporating a legal entity, offering a paid service
   under the name, or filing a trademark application.
5. Decide the product and service name (question 1) before the root-pack ceremony closes
   the practical renaming window.
6. Do not alter `federation_id`, `orbiplex-main` fixtures or `DIA-ROOT-001` on account of
   this proposal.
