# Proposed amendment on community self-government

**Status of the text.** DIA has yet to be formally constituted as an organization.
Both the [current Constitution](CONSTITUTION.en.md#const:norm.6) and the text at
revision `cbe276fda89e62621bc5f0f90c9bb3fad6b1a2c2` are drafts. The author
also treated the Constitution as a draft when root charter 0.1.0 was adopted.
That decision covered the charter alone.

**Author's approval.** On 28 November 2026, Paweł Wilk approved the proposed
change to the protected core. He stated that he is the Constitution's sole author
to date and that no public federation exists yet. The approved wording is now
part of the draft. Formal adoption of the first Constitution remains a separate
decision. Forming the organization will not itself bring the Constitution into force.

## What changes and who decides

| Matter | Proposed source and limit of authority |
| --- | --- |
| DIA and Orbiplex | The Constitution governs the project, its organs and those acting on its behalf. The project's duty to protect people follows the exercise of its power, including delegated operations. |
| A community's constitution | The community chooses the text and its own constituent procedure. The DIA hierarchy operates inside DIA. Its provisions are available as models elsewhere. |
| A technical federation | The accepted root identifies a trust domain. Verification checks signatures, purpose, scope, expiry and revocation under the applicable protocol. Trust in that root supplies no evidence of constitutional assent. |
| A shared activity | Its parties identify the service, access rights, delegates, adjudication, appeal and exit. They can amend or end that arrangement under its terms. No broader mandate follows. |

For example, a community assembly can adopt Article III.3 of a pinned revision
for its communal archive, with its local export rule prevailing in a conflict.
The record names the adopting body and its authority, those protected or bound,
the decision date, the controlling text and the procedure to amend or end it.
For supplementary application it also identifies the gap, who decides whether
it exists and which local rule takes precedence. A bare citation creates no duty.

## Transition on entry into force

1. On first formal adoption, the competent body publishes both language versions,
   the act of adoption and the effective date.
   From that date an obligation based solely on using the technology has no continuing force.
2. Each operator or body relying on an earlier commitment identifies its evidence,
   parties, version, subject matter, duration, renewal, exit and dispute procedure.
   Genuine undertakings run to their agreed end or are changed by those authorized.
   Notice goes privately to affected parties where the evidence contains personal data.
   An unsupported claim of authority cannot justify further access, collection or sanctions.
3. Existing providers secure entrusted data and honour applicable confidentiality, export,
   return, erasure and agreed retention. At exit the responsible operator and participant
   arrange a safe handover or deletion, recording completion or a specific surviving
   basis and expiry. An earlier claim or appeal survives within its original jurisdiction.
   Neither transition nor uncertainty authorizes indefinite retention or loss of access
   to one's own data.
4. Where terms or evidence are disputed, preserve the minimum needed for safe handover
   or a pending claim, name a responsible person and review date, and offer the existing
   appeal path. Continued cooperation beyond the established mandate needs a fresh act.
   A lapse of public authority does not undo a valid prior decision or technical signature.

## Impact of the draft and protection of the core after adoption

Changing who is bound materially narrows the scope of the core in the previous
draft, especially the protection users can claim from operators (Article III.11)
and the founders' authority. The author's approval of this revision opened
neither an inter-federation proceeding nor the 90-day reflection period.

If the Constitution is adopted in this form, subsequent changes to the core
will be governed by Article XVI.8-9, `const:core.2` and `const:core.3`. Those
safeguards will also apply to adopting or weakening the core's defense procedure.
The [entrenchment clause §2.2](../../50-constitutional-ops/en/ENTRENCHMENT-CLAUSE.en.md)
and the [membership and quorum rules §§7-8](../../50-constitutional-ops/en/FEDERATION-MEMBERSHIP-AND-QUORUM.en.md)
describe the proposed procedure for such a subsequent change:

- At formal opening, use the rules in force before the proposed change to identify
  the electorate and group federations under common control. The process requires
  at least one eligible block and an explicit yes from every block in that snapshot.
- Obtain independent adversarial review by at least three nodes with high procedural
  reputation, independent of the initiators and free of conflicts; publish their rationale.
  Allow at least 90 days between formal submission and vote for public counterarguments.
  Permanently archive the submission, impact analysis, arguments, votes and reasons.
  Project founders have no exemption. No clock starts merely because a file was edited.

### Separate decisions and effects on communities

- Revise the [root charter §10](../../50-constitutional-ops/en/ORBIPLEX-MAIN-ROOT-CHARTER.en.md)
  only with the custody threshold then in force and a new charter version. If unavailable,
  retain 0.1.0. This separate decision cannot enact the Constitution, appoint Guardians
  or activate the production root. Local adoptions and service agreements require their
  own authorized acts.
- Self-government and exit become usable without loss of project protections. The risks
  are a provider relabelling its own duties as local law, coercive service terms, and
  orphaned data on exit. Review actual mandates, refusals and safe handovers.
  Rehearse the cases below with fictitious parties before first formal adoption.
  At the first retrospective
  count undocumented mandates, unresolved returns and contested decisions and publish
  aggregate results. After the Constitution takes effect, changes to the scope of the
  adopted core protections follow the applicable procedure. Later project decisions
  cannot rewrite a community's existing act retroactively.

## Tests of the proposed text

| Case | Result and rule |
| --- | --- |
| 1. A community writes its constitution from scratch. | Its own act suffices. No root or founder permission is required (Norms 12, Definition 7). |
| 2. A preamble cites DIA as inspiration. | No duty, priority or jurisdiction follows (Norm 13). |
| 3. An assembly adopts selected clauses of a fixed version. | Only the named matters and addressees are covered; the recorded conflict rule governs (Norms 13-14). |
| 4. The community adopts the whole text with a future amendment procedure. | The specified procedure determines subsequent versions. Article XIII.1 keeps project and local offices distinct. |
| 5. Two communities share a relay under different constitutions. | The agreement governs access, revocation and disputes about the relay. Neither grants votes or general jurisdiction (Norm 15). |
| 6. A community uses another federation's infrastructure. | The operator checks technical grants. Outside the agreed service the local constitution governs; participation alone grants no resources (Norms 15-16). |
| 7. Guardians, founders and council seats are held by different people. | Each acts under a separate mandate (Definition 16, Article XIII.1). |
| 8. The Guardians sign a valid root pack. | Its technical effects follow the custody policy. It appoints no political representative and proves no local adoption (Norm 16, Definition 7). |
| 9. DIA revises a text adopted at a fixed version. | The existing local commitment stays at that version until a new act unless an update procedure was expressly accepted (Norm 14). |

## Implementation boundary

S041 binds a running node to one active federation root. Several communities using
that infrastructure, or a community using several deployments, do not require a change
to that rule. Existing selectors, root packs, custody references and protocol grants
retain their meanings. If a service needs to *automate* proof of local adoption, track
that separately with its owner: specify an independently versioned decision record and
verify scope, authority, expiry and withdrawal before relying on it. The competent
body can document adoption and agreements without such an implementation.
