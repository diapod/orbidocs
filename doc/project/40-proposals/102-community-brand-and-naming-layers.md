# Proposal 102: Community Brand and Naming Layers

Status: **Naming decision adopted; operational rollout pending**. Date: **2026-11-18**.

Based on:

- [Vision](../../normative/20-vision/en/VISION.en.md) and
  [Ontological Basis](../../normative/90-supplementary/en/ONTOLOGICAL-BASIS.en.md):
  relational agency, enactive participation and the limits of objectification.
  These explain the name and call; they do not create duties to participate.
- [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md) and
  [Constitution](../../normative/40-constitution/en/CONSTITUTION.en.md): federation over
  centralization, human agency, auditability. This proposal names a social layer and
  creates no governance authority, membership rights or root trust.
- [ORBIPLEX-MAIN-ROOT-CHARTER](../../normative/50-constitutional-ops/en/ORBIPLEX-MAIN-ROOT-CHARTER.en.md)
  (`DIA-ROOT-001`): the governance home of the `orbiplex-main` root. Nothing here
  touches custody, threshold, roster or the root-pack ceremony.
- [P076: Federation Identity and Network Selector](076-federation-identity-and-network-selector.md):
  `federation_id` is a node-wide, pre-runtime **network selector**, in the sense that
  `mainnet` and `testnet` are selectors in distributed-ledger systems.
- `README.md` brand identity block: organization **Distributed Intelligence Agency**,
  system and protocol brand **Orbiplex**.

## Executive Summary

Adopt **Emergat** as the public name of the first public federation built with
Orbiplex and of its community of participants and operators. Its primary domain
is **`emergat.org`**. This names the intended federation; it does not announce
production activation or establish that public operation is ready.

The community is currently **unincorporated**. This decision creates no legal
entity and appoints no service provider. Actual operators remain responsible for
their services; the absence of incorporation does not settle trademark risk.

This fills a gap rather than renaming anything. The project already names its
organization (Distributed Intelligence Agency), its system and protocol family (Orbiplex),
and its federation root selector (`orbiplex-main`). It had no name for the social
body that gathers around them, and `orbiplex-main` was being borrowed for that
purpose even though it is a technical selector, not a community name.

The canonical written form is **Emergat**. Paweł Wilk reports ownership of
`emergat.org`, `emergat.io` and `emergat.ai`; the latter two are secondary addresses.
The name is independent of every domain suffix. The proposed community call is
**“Emergat. Agency emerges from participation.”**, with its Polish counterpart
**“Emergat. Sprawczość wyłania się z uczestnictwa.”** (section 3.3).

## 1. Context and Problem Statement

### 1.1 Three named layers and one unnamed one

| Layer | Name | Where it is anchored |
| :--- | :--- | :--- |
| Umbrella organization | Distributed Intelligence Agency | `README.md`, Constitution |
| System and protocol family | Orbiplex | `README.md`, protocol documents |
| Federation root selector | `orbiplex-main` | P076, `DIA-ROOT-001`, `federation-root.v1` |
| **Public name of the first federation and its community** | **previously absent** | now defined by this proposal |

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
| Public name of the first federation and its community | **Emergat** | new |
| Primary domain of that federation/community | **`emergat.org`** | new |

This table is the canonical naming reference. Emergat is one federation using
Orbiplex, not a new name for all Orbiplex installations or federations. The
federation's operational identity remains governed by P076 and S041; its public
name does not replace the selector or root pack. The project site remains
`orbiplex.ai`, and technical documentation remains at `docs.orbiplex.ai`.

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
| Locative | w Emergacie |
| Vocative | Emergacie |

### 2.4 What this proposal does not change

1. This documentation change does not alter schemas, fixtures or `federation_id`.
   `orbiplex-main` stays. The root presentation extension in section 10.1 is
   planned separately; historical signed packs must not be rewritten.
2. No normative act is amended. `DIA-ROOT-001` keeps its scope.
3. No legal entity is created, and no authority is delegated to the community as such.
4. No trademark application follows from this proposal (section 5.4).
5. Orbiplex remains the system/protocol brand. Naming a distinct application or
   hosted service remains a separate decision (section 9).
6. A domain, HTTPS certificate, logo or tagline does not prove federation
   membership or confer issuer authority. Bootstrap still verifies the signed
   root pack and local policy; do not infer trusted service endpoints from DNS.

## 3. Etymology and Semantics

### 3.1 Emergat

**Fact.** *Emergat* is the Latin present active subjunctive, third person singular, of
*emergere* ("to rise out, to surface"), formed from *e-* ("out of") and *mergere* ("to
submerge"). It means **"let it emerge"** or "may it come forth".

Comparable subjunctive forms used as nouns include *fiat* ("let it be done"),
*caveat* ("let him or her beware") and *exeat* ("let him or her leave").

**Author's intended reading.** The name is a **jussive** invitation, rather than a
description; the verbal form alone does not force that reading in every context
([Allen and Greenough, §439](https://dcc.dickinson.edu/grammar/latin/hortatory-subjunctive)). Every other
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

**Author's wordplay.** *Emergatio* is used here as a neologism, not as a claim of
classical attestation. Its value is that it completes a pair with the canonical name – *emergat*
as the call, *emergatio* as what the call names – which is why it is worth explaining
once in community prose and then leaving alone.

### 3.3 Proposed tagline and community call

| Language | With the name | Standalone |
| :--- | :--- | :--- |
| English | **Emergat. Agency emerges from participation.** | **Agency emerges from participation.** |
| Polish | **Emergat. Sprawczość wyłania się z uczestnictwa.** | **Sprawczość wyłania się z uczestnictwa.** |

**Authorship record.** Paweł Wilk is the sole author of both formulations, as
declared by him on 2026-11-18. They are proposed for community use, together with
the name or independently. This records provenance; it does not assert trademark
registration, determine legal protectability or change existing licensing grants.
Keep this provenance in the proposal; the public website introductions omit an
authorship note, as requested by the author.

**Meaning intended by the author.** The call follows the Vision's account of
agency arising in relationships and the Ontological Basis's
[enactive participation](../../normative/90-supplementary/en/ONTOLOGICAL-BASIS.en.md):
participating in the world makes cooperation and agency possible. “Emerges” also
evokes *appearing* at the first described boundary of the
[scale of epistemization](../../normative/90-supplementary/en/ONTOLOGICAL-BASIS.en.md),
before a subject–object division, schematization, linguistic inference and
objectification. That source explicitly treats appearing as a **boundary of the
model, not an observed transition**. The call does not turn it into an object or
claim an empirical sequence of the world's creation.

These are related readings, not an equation of preconceptual appearing with
system-level emergence. Socially, the invitation is to recognize and work across
barriers of sense between perspectives and layers, so that people can cooperate
without reducing every perspective to one grammar. Emergat should help with that
translation; it does not promise to erase meaningful distinctions, consent,
privacy or boundaries of authority.

**Use boundary.** This is an invitation, not an eligibility rule: dignity, rights
and the freedom to decline participation do not depend on contributing. Keep the
approved wording and punctuation; the Polish non-breaking space after `z` is a
typographic equivalent, not a different formulation. Do not present the call as
a technical availability, security or production-readiness claim.

## 4. Registry and Domain Status

**Owner-reported record.** The author recorded the following WHOIS information
on 2026-11-18, with Cloudflare as registrar. This review does not independently
verify registration, renewal, DNS, HTTPS or serving status:

| Domain | Created (UTC) | Registry expiry |
| :--- | :--- | :--- |
| `emergat.ai` | 2026-11-17T23:11:24Z | 2027-11-17 |
| `emergat.io` | 2026-11-17T23:22:51Z | 2027-11-17 |
| `emergat.org` | 2026-11-17T23:26:09Z | 2028-11-17 |

**Decision.** `emergat.org` is the primary federation/community home. Configure
`emergat.io` and `emergat.ai` as redirects to it during operational rollout; this
applies to the apex web addresses, not every subdomain. In particular, the
service hosts under `emergat.io` selected in section 10.2 must not be caught by
a wildcard website redirect. This document does not claim that redirects or
services are already deployed. The name and federation authority remain
independent of domain availability; running services still depend on their
configured endpoints.

**Owner-reported screening.** On 2026-11-15 and again on 2026-11-18, `emergat`
was reported available on crates.io and npm, with no matching GitHub repository.
This is dated discovery evidence, not a reserved namespace or proof of legal
availability. No package or repository rename follows from it.

## 5. Trademark Due Diligence

### 5.1 Method

The author's draft records searches of USPTO (`tmsearch.uspto.gov`) and TMview
(`tmdn.org/tmview`) on 2026-11-18. Sections 5.2–5.3 preserve those reported results;
they were not independently reproduced during this review and do not establish
current registration status or an exhaustive search.

Each zero result was validated with a **control query** known to return hits, because an
earlier search in this workstream returned a false "no results found" when a URL
parameter was silently ignored. Exact-match queries were widened with wildcards, because
protection extends to confusingly similar marks, not only identical ones.

TMview states that it is not an official register and that its data has no legal effect.
Nothing in this section is a freedom-to-operate opinion; a formal clearance search is
attorney work.

### 5.2 Emergat itself

**Reported result.** USPTO: `emergat` returned **0 results**. Control: `emergent` returned 214.

**Reported result.** TMview: `emergat` returned **0 rows**. Control: `emergant` returned 2.

**Reported result.** No company trading as "Emergat" was found in the author's
screening. The search scope is not sufficient to claim worldwide absence.

### 5.3 The potentially conflicting mark: EMERGA

**Reported result.** Widening to `emerga` in TMview returned 34 marks. The draft
identified the following as belonging to
**EmerGa Association**, Toulouse, France:

| Register | Number | Nice class | Scope | Status |
| :--- | :--- | :--- | :--- | :--- |
| France INPI | 5074358 | **42** | software design and development, SaaS, cloud computing, IT consultancy, server hosting, electronic data storage | registered 2024-11-15 |
| EUIPO | 019087755 | **9** | IT devices, software, databases (electronic and interactive), recorded data sets | registered, status date 2025-01-27 |

**Reported result.** Also listed as live: `EMERGA` at UKIPO in classes 9 and 35 (filed 2023-10-24), and
`EMERGA CHARGE` at EUIPO and UKIPO.

**Reported result.** `EMERGANT` was listed as live at USPTO in class **36** (financial investment in business
valuation), owned by Emergant LLC, Delaware, filed 2021-09-16 and 2021-09-17.

**Inference.** The similarity of `EMERGA` and `EMERGAT`, together with the reported
software/service coverage, warrants review of the intended uses. It does not
establish infringement, an inevitable opposition or an unavailable registration.
The actual specification of goods/services and context matter, not merely a
shared prefix or Nice class number. The apparently different `EMERGANT` context
also requires checking before treating it as irrelevant.

### 5.4 Naming decision and unresolved clearance

**Legal boundary.** Nonprofit purpose, lack of incorporation and not applying for
a mark do not automatically put a use outside trademark law. Article 9 of
[Regulation (EU) 2017/1001](https://eur-lex.europa.eu/eli/reg/2017/1001/oj/eng)
sets conditions for restricting use in the course of trade; the CJEU's
[C-298/23 judgment](https://juris.curia.europa.eu/juris/document/document_print.jsf?docid=315003&doclang=EN)
also distinguishes an organisation's nonprofit purpose from whether it acts as
an economic operator. These sources define a boundary, not a verdict on Emergat.

**Decision.** Adopt the name and domain in project materials, without filing a
trademark application through this proposal. Keep the reported findings for a
qualified review of actual public uses, including free hosted services, before
launch. Clearance remains unresolved (P102-005); no legal immunity or legal
exclusivity is claimed here. Renaming this public layer remains possible without
changing protocol identifiers or the root-pack ceremony.

## 6. Trade-offs

**Benefits**

1. Fills the social layer without touching protocol, schemas or normative acts.
2. Names the project's mechanism (emergence) rather than its topography or its law.
3. Inflects natively in Polish, unlike `Orbiplex`.
4. Separates a stable technical identity from a public name that can evolve.
5. A jussive name states an intention, which suits a community that grows by accession.

**Risks**

1. Reported similar marks leave legal clearance unresolved (section 5).
2. In English, `emerg-` is dominated by *emergency*, not *emergence*; non-technical
   listeners may hear the alarm sense first; this is a hypothesis to test.
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
| Community name drifts into protocol identity, for example a `federation_id` rename | Section 2.4 forbids it; P076 keeps the selector decoupled |
| A secondary domain becomes unavailable | `emergat.org` is primary; neither the name nor federation authority depends on a secondary domain |
| A rights holder objects to a public use | Review the specific use and response with qualified advice; the public layer can be renamed without changing protocol identifiers |
| A branded page is mistaken for a production federation or trust anchor | State rollout status and keep root-pack/admission gates explicit; DNS and WebPKI do not confer federation authority |
| The call is read as making rights conditional on contribution | Preserve the voluntary-participation boundary in section 3.3 |
| Readers take the `-at` institutional reading as etymological fact | Section 3.1 marks it as analogical |

## 8. Options Considered

The author reports screening over one hundred names, with five reaching
etymological/registry review and four reaching preliminary trademark searches.
These are design-history notes, not completed legal clearance. Emergat was chosen
for its semantic fit; neither exclusivity nor lack of conflicting rights follows
from that choice.

Whole families were rejected on structural grounds worth recording, so they are not
re-proposed:

- **Descriptive stems** (`connector`, `tech-`, `code-`, `base-`): less distinctive
  for the author's naming purpose and difficult to distinguish in search. `coden`
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

1. **Product and service naming.** Emergat names the first public federation and
   its community. Orbiplex remains the system brand; any separate application
   or hosted-service brand requires its own decision.
2. **Umbrella organization.** Whether "Distributed Intelligence Agency" (or
   "Distributed Intelligence") stays is a separate decision and is not addressed
   here.
3. **Operational stewardship.** Who will operate the public domain and services,
   and under which legal form if any? This is distinct from trademark clearance,
   which depends on actual uses, not only incorporation or charging fees.
4. **Localized community prose.** Whether `Emergatio` is explained in Polish and Czech
   community material, or only in English.

## 10. Implementation Guidance and Tracker

Reuse the existing documentation and bilingual Hugo site. Section 2 is the
naming reference and section 3.3 owns the call and authorship record; other
surfaces link here rather than inventing independent naming policies. The
Orbiplex project site can introduce Emergat without moving to `emergat.org`.
A future community site at that domain is a separate deployment.

### 10.1 Federation presentation from root configuration

Root configuration holds the federation's **name** and three optional fields:
**tagline**, **description** and **logo**.
[P076](076-federation-identity-and-network-selector.md#federation-presentation-metadata-planned)
owns the planned typed, localized presentation block; S041 owns its projection
from the verified active root. The current `federation-root.v1` schema and loader
reject unknown fields, so these fields must not be appended to existing packs
before the versioned contract and loader support are implemented.

**Welcome screen:** show the federation's name as the heading. If a tagline is
defined for the selected locale/fallback, show it **below the name**. Both tagline
and description are optional; missing values produce no empty placeholders.
The description may provide supporting introductory text. The footer reads
**“powered by Orbiplex.AI”**, distinguishing the underlying software from the
federation. This footer spelling is a presentation attribution, not a change to
the Orbiplex protocol brand.

When the active root supplies a logo visible to the reader, place it beside
the name. Keep the name as text and give this adjacent decorative image an empty
`alt`. If the logo is absent or unavailable, show the same heading on its own.
P076 defines the signed, self-contained PNG representation. The source artwork
may be vector-based.

For Emergat, the presentation name is `Emergat`, the primary home is
`https://emergat.org/`, and tagline values use the standalone forms from section
3.3, so the name is not repeated. Suggested descriptions:

- EN: “The first public federation built with Orbiplex, and its community of
  participants and operators.”
- PL: “Pierwsza publiczna federacja korzystająca z Orbipleksu oraz jej społeczność
  uczestników i operatorów.”

Descriptions introduce the federation; they do not replace the separate,
owner-backed operational readiness indicator. Root metadata must be explicitly
public before appearing in an unauthenticated welcome shell; otherwise use the
existing guarded view. With no accepted displayable metadata, keep a neutral
`Orbiplex.AI` welcome heading. Never substitute Emergat for another federation.

### 10.2 Rollout and evidence

Use **Emergat** in first-federation introductions and human-facing descriptions.
Keep **Orbiplex** for software, protocol documentation and other federations'
installations. A runtime display name must remain scoped to the selected
federation, not hardcoded as the name of every node. Do not replace identifiers,
signed bytes, historical evidence, package names, API paths or default trust
configuration as part of branding. No new runtime abstraction is needed here.

**Initial public-service addresses (planned, selected 2026-11-18)**

| Hostname | Intended role | Existing root-pack field |
| :--- | :--- | :--- |
| `seed-001.emergat.io` | First Seed Directory API | One `seed_directory_bootstrap[]` entry with a full HTTPS `endpoint` |
| `seed-002.emergat.io` | Second Seed Directory API | A second `seed_directory_bootstrap[]` entry with a full HTTPS `endpoint` |
| `primus.emergat.io` | Optional initial peer, if a separate bootstrap peer is needed | A `bootstrap_seed_peers[]` entry with a full WSS `endpoint_url` |

These are selected deployment names, not active endpoints, signed identities or
proof of official-service status. Reuse the existing
[P076 root-pack contract](076-federation-identity-and-network-selector.md) and
[S031 Seed Directory](../60-solutions/031-seed-directory/031-seed-directory.md):
`presentation.homepage` remains the human-facing site, while
`seed_directory_bootstrap[]` locates the catalogues. Do not add a parallel
`service-root` field or derive service authority from a DNS name. `primus` names
a bootstrap peer, not a privileged trust root or mandatory central node.

Before activation, determine the API/WSS paths and any non-default ports, bind
each endpoint to its real `node_id`, provision TLS, and set the directory's
explicit `enabled`, `trust_level` and `weight`. Official directory status must
carry a verified inline `federation-service-endorsement.v1`; do not fabricate
identities or unsigned production fixtures to fill the plan. Use the existing
root authoring/signing and activation path. This service rollout does not depend
on the later presentation-metadata extension P076-BRAND-001.

Two hostnames alone do not establish fault independence. Record whether their
operators, hosts and network paths are independent; both names share the
`emergat.io` DNS dependency. Verify bounded behaviour with either directory
unavailable and refusal of invalid official-service proofs. Publish the actual
topology and evidence scope rather than claiming redundancy from names alone.

| ID | Task | Status | Acceptance / evidence |
| :--- | :--- | :--- | :--- |
| P102-001 | Adopt the naming reference and synchronize documentation entry points | done | P102, Orbidocs README/style guidance, Node README and P076/S041 distinguish Emergat, Orbiplex, `orbiplex-main` and domain authority; no selector/schema/fixture change |
| P102-002 | Record the bilingual call, sole authorship and interpretive grounding | done | Section 3.3 contains both full and standalone forms, Paweł Wilk's declaration, upstream links and the voluntary-participation boundary |
| P102-003 | Prepare the bilingual introduction on the existing project site | done | Focused local Hugo production build (2026-11-18) and rendered-HTML checks cover EN/PL wording, primary domain and navigation, without a public authorship note for the call; the site stays at `orbiplex.ai`. Full-site build remains blocked by legacy HTML content admission, outside these pages; deployment is not claimed |
| P102-004 | Deploy the community home and secondary-domain redirects | todo | Operator records hosting/DNS ownership, HTTPS checks for all three domains, primary canonical URL and verified redirects; renewal responsibility is assigned; no change to federation authority |
| P102-005 | Review the intended public uses against the reported trademark findings | todo | Current official records and actual use scope reviewed; outcome and any naming constraints recorded; no inference of immunity from nonprofit/unincorporated status |
| P102-006 | Render federation presentation on the Node UI welcome screen | todo | Depends on P076-BRAND-001 and existing P095/P098 public/private view contracts. Read the active root projection; heading = name, optional logo beside it, optional tagline below, optional description, footer exactly `powered by Orbiplex.AI`. Browser acceptance covers EN/PL/fallback, absent optional fields, absent/public/private metadata, escaped markup, another federation and restart with a changed active root. Verify offline logo display without external requests, direct image access denied without read admission, and the text heading alone when the logo is omitted. The earlier logo URL ceases to serve its image and the shell shows only current branding. No change to admission, readiness, configuration ownership or signed historical fixtures. |
| P102-007 | Provision and qualify initial Seed Directory endpoints and optional bootstrap peer | todo | After P102-005 for the intended uses, record full URLs, real node identities, TLS, topology and root-pack bindings for `seed-001.emergat.io` and `seed-002.emergat.io`; explicitly activate or omit `primus.emergat.io`. Verify discovery through the normal consumer path, either-directory outage, rejection of invalid official proof and absence of website redirects on service hosts. Reuse P076/S031 and production activation gates; naming, DNS provisioning or a health response alone is not completion. |

P102-004 follows P102-005 for the intended public uses. It does not close the
separate production-federation gates in P076-004 or `DIA-ROOT-001`. A landing page,
a root-pack ceremony and participant-facing operational readiness are separate
outcomes; choosing a product name is not a prerequisite for the ceremony.

**Next actions:** resolve the public-use review and the existing whole-site build
blocker before arranging deployment. Continue federation activation under
its existing owners and acceptance criteria. Implement root presentation through
P076-BRAND-001, then consume it through P102-006; website content does not prove
that either runtime task is complete. P102-007 separately qualifies the service
addresses above using existing bootstrap contracts.
