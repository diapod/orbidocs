# Proposal 051: Swarm Membership, Reputation Bootstrap, and Public Adjudication

Based on:
- `doc/normative/30-core-values/en/CORE-VALUES.en.md`
- `doc/project/50-requirements/requirements-001-node-onboarding.md`
- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`
- `doc/project/20-memos/nym-layer-roadmap-and-revocable-anonymity.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/40-proposals/026-resource-opinions-and-discussion-surfaces.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`
- `doc/normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md`
- `doc/normative/50-constitutional-ops/en/PARTICIPANT-COVENANT.en.md`
- `doc/normative/50-constitutional-ops/en/ADVOCACY-AND-SOLICITATION-POLICY.en.md`
- `doc/normative/50-constitutional-ops/en/MARKETPLACE-ANTI-FRAUD-POLICY.en.md`
- `doc/normative/50-constitutional-ops/en/PANEL-SELECTION-PROTOCOL.en.md`
- `doc/normative/50-constitutional-ops/en/ABUSE-DISCLOSURE-PROTOCOL.en.md`
- `doc/normative/50-constitutional-ops/en/PROCEDURAL-REPUTATION-SPEC.en.md`
- `doc/normative/50-constitutional-ops/en/REPUTATION-VALIDATION-PROTOCOL.en.md`
- `doc/normative/50-constitutional-ops/en/NODE-RIGHTS-CARD.en.md`

## Status

Draft

## Date

2026-04-23

Design/reuse review: 2026-10-10. The original date and frozen decisions remain;
the social-correction integration below is planned, not a runtime completion claim.

Systemic-repair follow-up: 2026-10-13. P051-010–014 translate the protection,
reintegration and systemic-repair norms into planned contracts and runtime work;
they do not reopen or extend the qualified local baseline.

Sequencing clarification: 2026-10-14. The preferred lower-rework order below is
separate from the manual slice's necessary dependencies and qualification scope.

## MVP Decisions Frozen on 2026-05-27

The following decisions are frozen for the MVP membership/sponsorship contract.
Later documents may refine scoring, UX, or federation policy without changing these primitives:

1. Entry is per influence surface, not one global membership bit.
2. Entry classes are defined by `doc/schemas/_shared/membership-enums.v1.schema.json`.
3. Influence surfaces are defined by the same shared enum; the high-trust surface is `public-trust`, while `public-trust-role` remains an entry class.
4. `surface-access-policy.v1` is the canonical policy-axis source of truth.
5. `participant-entry-profile.v1` is a computed subject read model, not an independent source of per-surface permission truth.
6. `participant-effective-limits.v1` is the runtime-facing composed read model for entry defaults, surface policies, capability sanctions, and appeal results.
7. Sponsorship gives candidacy, not authority.
8. Sponsor liability is one-hop by default and becomes wider only after an anti-collusion process establishes a sponsor ring.
9. Sponsorship uses named templates and ordinal liability classes instead of ad-hoc numeric exposure parameters.
10. Public-object adjudication separates alarm, review, mediation/appeal, sanction, and anti-collusion sweep.
11. Anti-collusion MVP baselines are sponsorship velocity, co-flagging coherence, and closed-loop receipt detection.

## Executive Summary

Orbiplex already states that reputation is a safety instrument rather than a
status ladder, that endorsements carry asymmetric risk, and that major
decisions must leave a trace and an appeal path. What is still missing is one
proposal that freezes the bootstrap shape of swarm membership and the first
adjudication layer for public pseudonymous objects.

This proposal covers:

- how a new member enters,
- how sponsorship works,
- how early trust and early accountability compose,
- how artifact-level judgments can turn into participant-level reputation
  events,
- how public objects should be flagged, reviewed, mediated, escalated, and
  appealed,
- and how anti-collusion logic should remain a separate layer rather than a
  hidden side effect of one case.

The decisions of this proposal are:

1. swarm membership SHOULD begin through invitation or sponsorship by at least
   one existing member rather than through anonymous open self-enrollment,
2. sponsorship is not a symbolic gesture; it creates bounded reputational
   exposure for the sponsor,
3. first-run node onboarding SHOULD guide the operator through identity
   creation, role choice, service posture, and community-surface selection,
4. participant reputation is procedural and event-based, not a single global
   score,
5. artifact reputation may affect author reputation only after explicit
   quantity and quality thresholds are crossed,
6. for public pseudonymous artifacts, signaling danger, community judgment, and
   reputational sanction MUST be treated as distinct layers,
7. a participant MAY choose mediation with the parties who influenced a
   reputation event before opening a formal appeal,
8. formal appeal is handled by a randomly selected independent community group
   that did not participate in the original decision and is at least as large
   as the decision-forming group within the applicable panel-size rules,
9. a separate anti-collusion sweep SHOULD continuously look for correlated
   group behavior and procedural contamination across cases,
10. concrete mechanisms MUST vary by pseudonymization class and accountability
    surface rather than assuming one universal identity regime.

This keeps the stratification clean:

- constitutional and values documents define the principles,
- this proposal defines the bootstrap procedure and decision frame,
- later schemas and implementations specialize by community policy and
  pseudonymization class.

## Context and Problem Statement

Orbiplex already has strong language for:

- procedural reputation,
- appeal rights,
- asymmetric endorsement risk,
- revocable pseudonymity,
- and evidence-based challenge paths.

What it does not yet have is one explicit project-level contract for:

- the first phase of swarm membership,
- the transition from artifact-level judgments to reputation events,
- and the public-object adjudication path that separates alarm from sanction.

Without that contract:

- "joining the community" remains folklore,
- invitation and sponsorship have unclear operational meaning,
- artifact evaluation may drift into ad-hoc author scoring,
- public-object review can collapse into majoritarian reflex,
- appeal rights exist normatively but not yet as a concrete bootstrap flow,
- and privacy-sensitive communities may accidentally copy the wrong
  accountability posture from public or federation-facing layers.

The hard part is not only technical. The membership edge is where:

- trust is weakest,
- social attack cost is lowest,
- Sybil pressure is highest,
- and privacy/accountability trade-offs are easiest to oversimplify.

There is one more problem specific to public pseudonymous surfaces. Some public
objects become strongly nootically charged: an opinion, comment, rating, or
short utterance starts carrying one or several memes in the memetic sense. From
there, groups do not always behave like stable permanent factions. Sometimes the
system is facing exactly that; sometimes it is facing an ad-hoc cluster of
correlated action temporarily assembled around one charged symbol, fear,
identity marker, grievance, or worldview cue.

In a more apophatic and enactive reading, the system should avoid prematurely
reifying "the cartel" as a single durable substance. What must be detected
first is correlated procedural force:

- repeated co-flagging,
- unusually dense co-voting,
- synchronized threshold-pushing,
- asymmetric targeting,
- or self-reinforcing reputation exchange.

This proposal therefore treats collusion primarily as a dynamic procedural
pattern, not only as a named faction with stable membership.

## Goals

- Define the recommended bootstrap path for entering a swarm community.
- Define sponsorship as a first-class accountability relation.
- Freeze the distinction between artifact-level reputation and participant-level
  reputation.
- Define a bootstrap adjudication path for public pseudonymous artifacts.
- Separate alarm, review, sanction, and anti-collusion sweep.
- Define mediation and appeal ordering for bootstrap governance.
- Make pseudonymization class a first-class parameter of these mechanisms.
- Define membership as access to bounded influence surfaces rather than as one
  global "accepted participant" switch.
- Define newcomer capability slow-start as a default safety posture, not as a
  permanent caste.

## Non-Goals

- This proposal does not define the final global reputation engine.
- This proposal does not define exact scoring formulas, weight functions, or
  aggregation math.
- This proposal does not define private deniable communication moderation rules.
- This proposal does not define the final random-selection protocol for every
  review and appeal pool.
- This proposal does not define the final schema family for every membership,
  sponsorship, review, mediation, appeal, or collusion artifact.
- This proposal does not require one network-wide uniform policy. Federations,
  communities, organizations, and private groups may tune thresholds and
  visibility surfaces.

## Decision

### 1. Membership Bootstrap Is Relational

Joining a swarm community SHOULD begin through invitation or sponsorship by at
least one existing member.

The design intent is not aristocratic gatekeeping. The intent is to make entry
into a trust-bearing network social and auditable rather than purely
mechanical. An invitation means:

- an existing participant is willing to create a local trust edge,
- the new participant starts with bounded but non-zero social context,
- and the network can reason about early accountability without pretending that
  all fresh identities are equivalent.

Communities MAY require more than one sponsor for higher-risk roles or broader
service exposure.

Open self-enrollment is not forbidden forever, but if a community permits it,
that path SHOULD carry lower initial trust, tighter capability limits, and
slower eligibility for trust-bearing roles.

The practical rule is:

```text
Orbiplex does not build a wall around personhood.
It builds sluices around shared influence.
```

Membership SHOULD therefore be evaluated per influence surface rather than as a
single global admission bit. Common surfaces include:

- `local-read`,
- `contactability`,
- `public-comment`,
- `public-publishing`,
- `unsolicited-dm`,
- `broadcast`,
- `marketplace`,
- `custody`,
- `routing`,
- `moderation`,
- `arbitration`,
- `governance`,
- and `public-trust`.

Each surface may have its own threshold: contact attestation, sponsorship,
probation, reputation, IAL, source diversity, anti-collusion checks, conflict
disclosure, multisig, or manual review.

The entry class for high-stakes role eligibility remains `public-trust-role`.
The surface where that authority is exercised is `public-trust`.

The default entry ladder is:

- `guest`,
- `contactable-participant`,
- `sponsored-candidate`,
- `probationary-member`,
- `full-participant`,
- `public-trust-role`.

Contact attestation is useful for anti-spam and recovery, but it is not civil
identity and not a substitute for reputation, IAL, or public-trust screening.

### 2. Sponsorship Creates Bounded Reputational Exposure

Sponsorship is not a ceremonial marker. It is a bounded reputational relation.

If a sponsored participant later causes harm, repeatedly violates contracts, or
accumulates serious evidence-backed negative procedural events, the sponsors and
introducers MAY themselves receive derived reputation events proportional to:

- their proximity to the sponsored participant,
- the sponsorship template and declared scope,
- the freshness of that sponsorship,
- and the severity of the resulting harm.

This is the bootstrap form of endorsement asymmetry already present in the
normative layer. The purpose is not collective punishment. The purpose is to
make trust extension carry real care and discernment.

Federation or community policy SHOULD cap how far this derived liability can
propagate and MUST keep it challengeable by evidence and context.

The sponsor does not guarantee the moral essence of the invitee. The sponsor
states only:

> I know this subject well enough to introduce it to this Orbiplex surface, in
> this scope and risk limit, and I accept bounded reputational exposure if that
> act of trust proves grossly careless or collusive.

Sponsorship gives candidacy, not authority. The sponsored participant must still
pass the threshold of the target surface.

The first sponsorship artifact is `membership-sponsorship.v1`.
It SHOULD carry sponsor subject, invitee subject, scopes, `sponsorship/template`,
issued and expiry times, probation window, structured due-diligence references,
revocability, revocation-tail duration, and evidence policy.

Sponsorship templates avoid false precision. The first template set is:

- `light-vouch`,
- `standard-introduction`,
- `strong-vouch`,
- `mentor-with-liability`.

Derived liability SHOULD be bounded by policy and classified ordinally rather
than calculated as a product of local coefficients.
The first liability classes are:

- `negligible`,
- `mitigated`,
- `moderate`,
- `serious`,
- `collusive`.

Each liability decision should state the triggered conditions and evidence refs.
For example, "classified as `serious` because the sponsor ignored three prior
red flags and continued mass-sponsoring into the same surface" is more
auditable than an unexplained numeric score.

Derived sponsor liability is one-hop by default. It should propagate further
only when a separate anti-collusion process establishes an organized
`sponsor-ring`.

To prevent clan capture, a sponsor SHOULD only sponsor into surfaces where the
sponsor has sufficient reputation and authority. Higher-risk surfaces SHOULD
require multiple sponsors from sufficiently independent clusters, active
sponsorship caps, and anti-sponsor-ring monitoring.

### 3. First-Run Node Onboarding Should Be a Guided Wizard

A user starting a local Node SHOULD be guided by a multi-step onboarding wizard
rather than dropped into raw configuration.

The wizard SHOULD at minimum:

- generate or import the operator's identity material,
- explain the selected accountability surface and pseudonymization posture,
- ask which services or roles the operator wants to expose,
- ask whether the node is joining an existing community or starting a new local
  one,
- collect invitation or sponsorship material when applicable,
- and explain the consequences of joining with a public, accountable, or more
  private participation surface.

The first-run experience matters because social bootstrap is part of system
security. Incorrectly defaulting a participant into the wrong visibility or
accountability surface is not a cosmetic error; it can become a privacy breach
or a governance mismatch.

### 4. Reputation Is Event-Based and Multi-Surface

Every participant identity that is visible on a reputation-bearing surface has
reputation, but that reputation MUST be modeled as a history of events and
domain-specific projections rather than as one timeless scalar score.

The practical bootstrap invariant is:

- evidence or judgments produce append-only reputation events,
- read models derive local, domain, and community views from those events,
- and authority decisions should key off those bounded views, not off a myth of
  one universal number.

This keeps reputation auditable and lets communities apply different thresholds
for:

- safety,
- competence,
- reliability,
- social care,
- moderation,
- or service stewardship.

### 5. Artifact Reputation Precedes Author Reputation

When a community evaluates an artifact, service output, publication, or other
user-authored result, the first reputation subject SHOULD be the artifact or
event itself. Participant-level reputation impact should arise only after an
explicit threshold is crossed.

Examples of threshold parameters include:

- minimum number of independent evaluations,
- minimum evidence quality,
- minimum evaluator diversity,
- waiting period before projection to author reputation,
- and conflict-of-interest filtering.

This avoids premature personal scoring from a handful of reactions and keeps the
system closer to facts before identity-level consequences are derived.

A later implementation MAY emit an explicit derived event such as:

- "artifact X crossed threshold T and now contributes procedural/community
  signal Y to author Z".

The threshold policy is local or federation-scoped, not global protocol law.

### 6. Public Adjudication Must Separate Alarm from Sanction

For public objects in a public or otherwise reputation-bearing pseudonymous
surface, Orbiplex SHOULD explicitly distinguish at least four layers:

- `flagging`
- `review`
- `appeal`
- `cartel-detection`

The core invariant is:

```text
Flagging raises an alarm.
Review forms a provisional social judgment.
Appeal challenges that judgment.
Sanction happens only after the judgment path is sufficiently grounded.
```

A cluster of flags MUST NOT by itself be treated as a final reputation penalty.
Otherwise the system becomes cheap to weaponize by:

- majoritarian pressure,
- factional mobilization,
- dynamic meme-driven clustering,
- or ordinary ideological bubbles.

The default public adjudication flow is:

```mermaid
stateDiagram-v2
    [*] --> Clear
    Clear --> Alarm: effective threshold crossed
    Alarm --> Review: open first review
    Review --> Clear: dismiss alert
    Review --> Contested: concern remains but sanction is not grounded
    Review --> Mediation: author requests mediation
    Review --> Substantiation: plural review needed
    Review --> Contaminated: procedure contaminated
    Mediation --> Clear: support falls below threshold
    Mediation --> Contested: disagreement remains
    Mediation --> Substantiation: mediation fails
    Substantiation --> JudgedSubjective: subjective dispute
    Substantiation --> JudgedSubstantiated: substantiated deregulation
    Substantiation --> Contaminated: contamination found
    JudgedSubjective --> Appeal: formal appeal
    JudgedSubstantiated --> Appeal: formal appeal
    Appeal --> Clear: appeal succeeds
    Appeal --> JudgedSubjective: prior subjective judgment upheld
    Appeal --> JudgedSubstantiated: prior substantiated judgment upheld
    Appeal --> Contested: merits review finds sanction basis insufficient
    Appeal --> AppealBlocked: eligible pool or quorum unavailable
    AppealBlocked --> Appeal: independent pool restored
    AppealBlocked --> Council: authorized escalation
    Contaminated --> Council: high-significance or repeated failure
    Council --> Review: remit for independent reconsideration
    Council --> Appeal: constitute independent appeal
    Council --> AppealBlocked: no authorized quorate path available
    Clear --> Withdrawn: author withdrawal
    Contested --> Withdrawn: author withdrawal
    JudgedSubjective --> Withdrawn: author withdrawal
    JudgedSubstantiated --> Withdrawn: author withdrawal
```

Mediation and council review are branches of one state machine, not parallel
systems of authority.
The diagram summarizes the procedure, not effect-application state. An unsuccessful
appeal does not upgrade a subjective dispute into substantiated misconduct;
only a competent merits review finding the sanction's basis insufficient leads
from appeal to `Contested`. An appellant's failure to supply new evidence does
not itself invalidate the prior finding.

`AppealBlocked` is a procedural-liveness state, neither exoneration nor confirmation
of the prior finding. Retain that finding as history; the recorded applicable
policy separately determines whether its effects are stayed or remain effective,
subject to current authority and expiry. Blockage cannot renew a hold, create guilt
or remove unrelated restrictions. The first local profile uses Council to remit
or arrange independent review, not as an additional unqualified merits authority.

### 7. Public Adjudication Applies to Publicly Indexed User Objects

The protocol described here is intended for public objects in a public or
otherwise reputation-bearing pseudonymous mode, especially:

- opinions,
- comments,
- ratings,
- short public statements,
- and other publicly indexed user-authored content.

It does not directly govern private deniable communication. At most, aggregate
and anonymized traces from private layers may inform higher-level abuse
detection, but not by silently importing private content into public
adjudication.

### 8. Protocol States Must Preserve Semantic Distinctions

A public object under adjudication SHOULD move through explicit protocol states
rather than a binary "acceptable / punished" model.

The minimum recommended state shape is three orthogonal axes:

- `lifecycle`: `clear`, `under-review`, `judged`, `withdrawn`
- `judgment_qualifier`: `contested`, `subjective`, `substantiated`, `contaminated`
- `withdrawal_reverts_event`: boolean, meaningful only when `lifecycle = withdrawn`

The equivalent diagnostic labels can be rendered as `judged.substantiated`,
`under-review.contaminated`, or `withdrawn.reverted` without multiplying the
wire enum into every possible combination.
Case-procedure progress, including `AppealBlocked`, and effect-application status
are separate from these public-object axes. Do not overwrite a judgment qualifier
with a scheduling or pool-availability failure.
These axes matter because the system must be able to say:

- "this object triggered concern",
- "this object is controversial",
- "this object was judged procedurally unsafe",
- or "this case was contaminated and cannot ground a clean sanction"

without collapsing all of those into one punitive label.

### 9. Alarm Thresholds Must Use Independence, Not Raw Count

When participants flag an object as potentially deregulating, the system SHOULD
store not only the raw signal but also enough metadata to reason about
independence and contamination.

At minimum this includes:

- object identity,
- flagger pseudonyms,
- timestamps,
- local justification or reason codes,
- and correlation hints between participating flaggers.

The system SHOULD then derive at least:

- raw flag count,
- effective independent support,
- cluster dispersion,
- growth velocity,
- and historical co-action coherence.

An alert should trigger only when all of the following are true:

- the raw threshold is reached,
- the effective independent threshold is reached,
- and initial contamination is not already too high.

Crossing that threshold creates an alert and review state, not a final author
sanction.

### 10. Provisional Holds Must Stay Mild and Reversible

If a deployment wants immediate defensive reaction, it MAY apply only a mild and
reversible provisional hold at alert time.

The hold:

- MUST have a bounded lifetime and an explicit removal/compensation path,
- MUST NOT be treated as final guilt,
- and MUST cease to affect current admission when it expires or the later review
  does not substantiate the case. A failed cleanup job must not prolong its authority.

"Reversible" concerns the continuing restriction, not erasure of past effects:
a missed opportunity or a disclosed allegation cannot be undone by clearing a
record. Preserve the original facts, append the correction, and identify any
remaining repair obligation. Soft penalties need their own validity boundary;
expiry of a hard block does not currently expire the soft factors in S040.

This keeps the safety posture responsive without letting the alert threshold
silently become punishment.

### 11. First Review Must Be Anti-Collusive and Temporarily Blind

The first review answers a narrower question than the final sanction path:

> does this alert appear to come from plural enough social concern, or mainly
> from a local faction, correlated cluster, or contaminated process?

The reviewing group SHOULD therefore be:

- smaller than the later escalation jury,
- selected with anti-collusion filters,
- and hidden until the voting window closes.

Selection SHOULD be drawn from several baskets at once, for example:

- high procedural reputation,
- medium but stable reputation,
- graph distance from the author and principal flaggers,
- topic competence,
- and low historical co-voting correlation.

Candidates SHOULD be excluded when they:

- are too close to the author,
- are too close to the primary flagging cluster,
- belong to an already overrepresented dense cluster,
- show strong prior signs of collusive co-action,
- or have an active conflict of interest.

The first review SHOULD be able to emit at least:

- `dismiss-alert`
- `continue-as-contested`
- `continue-to-mediation`
- `continue-to-substantiation`
- `mark-review-contaminated`

These baskets and temporary blindness describe lightweight anti-collusion triage,
not a replacement for a normative panel. Where `DIA-PANEL-SEL-001` applies,
reputation is an eligibility gate, not a draw weight; its uniform selection,
disclosure and party-veto rules take precedence. Hiding votes must not hide the
composition information needed to exercise those rights.

### 12. Mediation Comes Before Formal Appeal When the Participant Chooses It

Before opening a formal appeal, the affected participant MAY choose mediation
with the person or group that influenced the reputation event.

Typical cases include:

- evaluators of an artifact,
- a moderation subgroup,
- sponsors contesting how derived liability was applied,
- or other participants whose judgments contributed directly to the event.

Mediation is not mandatory. It is an optional lower-cost path that can:

- correct misunderstanding,
- add missing context,
- retract low-quality inputs,
- or narrow the dispute before it reaches a formal review group.

If mediation fails, is refused, or is inappropriate due to direct safety risk,
the participant retains the full right to formal appeal.

For public-object adjudication, mediation is especially useful after a first
review but before larger escalation. It is one bounded chance to let the author
submit justification and let original flaggers:

- maintain their flag,
- withdraw it,
- soften their classification,
- or remain silent until expiry.

If mediation drops the effective support below the safety threshold, the object
SHOULD return to `contested` or `clear`, and any provisional hold MUST be
reverted.

### 13. Community Escalation Must Be Larger, More Plural, and Anti-Collusive

If the case continues, the next layer is community escalation through a larger,
plural, anti-collusively selected jury.

This jury SHOULD:

- be substantially larger than the first review pool,
- preserve strict anti-cluster composition rules,
- require both nominal quorum and effective pluralistic participation,
- and receive the object plus structured case material, but not a herd-forming
  "N people already condemned this" summary.

Jurors SHOULD be asked on multiple axes rather than by a single binary button.
The minimum useful questions are:

1. does the object violate conditions of cooperation?
2. is the current classification too strong?
3. does the case mainly express ideological disagreement?
4. does the input procedure appear contaminated?

Each juror SHOULD also choose one class such as:

- `not-deregulation`
- `subjective-dispute`
- `possible-deregulation`
- `substantiated-deregulation`
- `procedural-contamination`

and provide a short justification.

Larger here means relative to lightweight first triage, not an unbounded crowd.
Where the normative panel protocol applies, its panel-size and quorum rules govern;
additional advisory reviewers do not acquire votes or expand the adjudicating panel.

If quorum is insufficient, the result SHOULD be `insufficient-quorum` and the
protocol MAY re-open the case only through backoff windows rather than immediate
retries.

### 14. Final Reputation Events Require Substantiation

The cautious default is:

- alert stage -> at most provisional hold,
- substantiated escalation result -> final reputation event,
- successful challenge or contamination finding -> retract or supersede the
  affected reputation consequence and recompute current projections while
  preserving procedural metadata. Already observed external effects require
  correction or compensation, not a claim that history was rolled back.

This is the point where the proposal most clearly rejects soft tyranny by raw
majority. The sanction should be grounded only after enough independent review
has survived:

- anti-collusion filtering,
- mediation or challenge opportunity,
- and a plural final review path.

### 15. Object Withdrawal Should Revert the Linked Reputation Event When Early Enough

The author MAY withdraw the object regardless of case status.

If the object is withdrawn within a policy-defined early window, the system MAY:

- mark the object as withdrawn,
- revert the linked reputation event,
- and keep only the procedural metadata needed for audit, cartel detection, and
  historical reconstruction.

This gives the protocol a repair path without pretending that the case never
happened.

### 16. Formal Appeal Uses an Independent Randomly Selected Community Group

A formal appeal MUST be handled by an independent randomly selected community
group whose members:

- did not participate in the original decision,
- have supplied an admissible COI declaration and have no disqualifying conflict
  of interest in the matter,
- and are numerous enough to avoid being weaker than the original decision
  surface.

The bootstrap minimum is:

- the appeal group is at least as large as the group whose decision or combined
  judgments produced the original reputation event, within the governing panel
  protocol's size limits. The admitted first-instance policy must make this
  compatible in advance; flaggers and advisory reviewers are not panel members.

The purpose is procedural symmetry. A participant should not need to overturn a
group decision before a smaller or less independent body than the one that
produced it.

The governing rules are not a blank slate: `DIA-PANEL-SEL-001` defines eligibility,
recusal, party veto, quorum and insufficient-pool escalation for panels in its scope.
Its VRF mechanism remains a hypothesis. Different lightweight local profiles may
specialize admissible pools and selection only within their declared competence
and the normative floor described in section 25. The resulting process stays:

- auditable,
- conflict-aware,
- and challengeable.

This rule applies both to ordinary appeal of participant-level decisions and to
appeal of public-object adjudication results.

### 17. Newcomers Use Slow-Start Capability Limits

A new or low-evidence participant SHOULD receive narrow initial influence
limits.
The canonical newcomer fixtures are:

- `doc/schemas/examples/default.surface-access-policy.json`
- `doc/schemas/examples/newcomer.participant-entry-profile.json`
- `doc/schemas/examples/newcomer.participant-effective-limits.json`

These limits are not a punishment. They represent influence that has not yet
been earned. `participant-entry-profile.v1` is a computed subject read model.
`participant-effective-limits.v1` composes entry defaults, surface policy,
sanctions, and appeal results into the runtime-facing view.
A separate `participant-capability-limits.v1` artifact may express sanctions or
explicit restrictions, but it should not be confused with ordinary newcomer
entry policy.

### 18. Spam, Solicitation, Advocacy, and Fraud Are Surface-Abuse Classes

Orbiplex SHOULD avoid global worldview bans. It SHOULD instead regulate how
shared communication and marketplace surfaces are used.

The default abuse rules are:

- no broadcast or unlimited unsolicited DM for fresh participants,
- no mass import of contacts without relationship or recipient consent,
- no unsolicited political, ideological, religious, campaign, or financial
  persuasion outside opt-in surfaces,
- clear tags for advocacy and campaign content,
- material conflict-of-interest and sponsorship disclosure,
- marketplace offers through explicit marketplace/service surfaces, not hidden
  acquisition funnels,
- low value caps and escrow/procurement contracts for newcomers,
- no transferable reputation from self-dealing or closed receipt loops.

This preserves pluralism while defending the surfaces on which pluralism
depends.

### 19. Governance Council Is Reserved for High-Significance or Contaminated Cases

The governance-council layer SHOULD remain exceptional.

It is appropriate only for cases such as:

- highly precedent-setting disputes,
- very large or heavily contested public cases,
- repeated failed escalation attempts,
- explicit `review-contaminated` outcomes,
- or disputes that require constitutional interpretation.

The design goal is not to create a standing aristocracy. The goal is to provide
one higher procedural layer for rare cases where ordinary community escalation
is insufficient or itself compromised.

Council composition SHOULD mix:

- attested expertise,
- procedurally trusted participants,
- anti-cluster random selection,
- and rotating civic assessors.

Council decisions SHOULD permit:

- full justification,
- separate opinions,
- conflict-of-interest registry,
- ex post audit,
- and doctrinal revision later without forcing retroactive erasure of every old
  case.

For the first local correction profile, the Council destination must identify an
authorized body able to arrange independent review or remit a contaminated case.
If that route is also unavailable, retain an explicit blockage, not a synthetic
ruling. Any later merits-adjudication role requires its own applicable mandate and
panel safeguards; the label `Council` alone grants none.

### 20. Anti-Collusion Sweep Must Be a Separate Continuous Subsystem

Cartel detection should not live only inside one case file. Orbiplex SHOULD run
it as a separate periodic sweep over many cases.

Its purpose is not primarily punitive. It is to:

- detect correlated procedural force,
- reduce the influence of highly correlated groups,
- improve future jury selection,
- mark cases as potentially contaminated,
- and, only when needed, open separate procedural-abuse review.

Useful sweep inputs include:

- flagging history,
- co-voting history,
- co-occurrence in disputes,
- timing patterns,
- mutual reputation boosting,
- topic distribution,
- asymmetry of targeting,
- and mediation and escalation metadata.

The MVP baseline detectors are deliberately narrow:

- sponsorship: abnormal sponsorship velocity,
- public adjudication: co-flagging coherence across objects,
- marketplace: closed-loop receipt detection.

Additional detector families should be added only when a concrete operational
need appears, so "anti-collusion" does not become an unbounded bucket.

The sweep SHOULD prefer graded outputs such as:

- `low-correlation`
- `watch`
- `elevated-collusion-risk`
- `high-collusion-risk`

rather than a binary "cartel / not cartel" ontology.

This again matches the apophatic-enactive caution of the proposal: the system
should first see dynamic correlated patterns before it reifies them as enduring
factions.

### 21. Influence Weighting Must Track Independence

The effective force of a set of flags or votes SHOULD depend not only on the
number of accounts but on their independence.

In practice this weighting should inform:

- alert thresholds,
- mediation outcome assessment,
- escalation validity,
- contamination scoring,
- and future reviewer selection.

This means that 150 accounts from one dense correlation cluster need not count
as 150 independent judgments.

### 22. Public Agora Nodes May Host Aggregates, Not Final Authority

Public Agora nodes MAY host public aggregation and query surfaces for
reputation-relevant artifacts, for example:

- public counts of flags, reviews, and appeals,
- public timelines of object-case state transitions,
- public derived read models for artifact reputation,
- public candidate projections of participant or nym reputation,
- and public dashboards of collusion-risk or contamination markers.

This is acceptable because Agora is already the public substrate for ingest,
query, and subscription of relevant records. What MUST remain separated is the
difference between:

- storing and serving public facts,
- projecting those facts into one read model,
- and issuing an authoritative reputation judgment.

Therefore a public Agora-backed reputation surface is allowed only as:

- an index,
- a projection,
- a read model,
- or a publicly inspectable candidate view.

It MUST NOT silently become the sole authoritative reputation layer for the
network.

If a federation or community wants a public Agora-backed reputation service,
that service SHOULD be modeled as a separate policy-bearing component operating
over Agora data, not as Agora itself.

This preserves the stratification:

- Agora stores and serves records,
- reputation components evaluate policy and derive judgments,
- nodes remain free to accept, reject, or down-weight a given public projection
  under local policy.

### 23. Pseudonymization Class Changes the Appropriate Mechanism

The concrete membership, sponsorship, reputation, review, mediation, appeal,
and collusion-handling mechanics MUST depend on the pseudonymization class and
accountability surface defined elsewhere in Orbiplex.

This proposal explicitly does **not** assume that one mechanism fits:

- `accountable-nym`,
- `private-nym`,
- public federation participation,
- local community participation,
- organization-scoped membership,
- or future stronger anonymity constructions.

Examples:

- in an `accountable-nym` context, ordinary public or domain reputation and
  sponsor liability may be appropriate,
- in a `private-nym` context, community-local invite graphs, scoped reputation,
  sealed adjudication, or group-local exclusion handles may be more appropriate
  than portable public sanctions,
- a private group may need stronger local exclusion without creating a global
  cross-group correlation handle,
- and an organization may use different membership visibility and appeal pools
  from a public federation.

Therefore the invariant is:

```text
The stronger the public blast radius, the stronger the accountability hook.
The more consent-bound and private the context, the stronger the unlinkability default.
```

This proposal should be implemented in conjunction with the evolving nym and
root-identity documents, not as an independent identity regime.

### 24. Concrete Mechanisms Remain Community-Policy Objects

The following items are intentionally left as policy parameters or later
artifacts:

- sponsor count required for entry,
- sponsor-liability window,
- alert thresholds,
- minimum effective-independent support,
- contamination cutoffs,
- thresholds for artifact-to-author reputation projection,
- mediation timeout and admissibility,
- size and eligibility of review and appeal pools,
- evidence threshold for high-stakes sanctions,
- whether reputation is public, domain-local, community-local, or hidden,
- and how pseudonymization-class-specific exclusions are implemented.

Orbiplex should freeze the shape early, but not pretend that every community
must share identical social mechanics.

### 25. Close the Correction Loop Without Creating Another Authority Plane

P051 owns the social procedure; [S040](../60-solutions/040-capability-limited-restrictions/040-capability-limited-restrictions.md)
owns restriction enforcement under P018. Neither a Room role, a Corpus Chair
decision, a signed artifact nor a notification action supplies adjudication
authority by itself. An admitted community policy must name the authorized
decision makers, affected surface, evidence threshold, conflict exclusions and
appeal path. Operator authority to run a host is not automatically authority to
judge its participants.

The first local profile is a bounded, non-disclosure community correction procedure,
not an implementation claim for the full constitutional panel system. It must
declare stakes, competence and limits. Constitutional, high-stakes or identifying
disclosure cases cannot remain in this lighter procedure merely because it is
locally available; route them to the applicable normative procedure or expose the
missing route as blocked. Local autonomy does not waive the rights floor.

| Upstream norm | What this slice preserves and newly determines |
| --- | --- |
| [Panel Selection](../../normative/50-constitutional-ops/en/PANEL-SELECTION-PROTOCOL.en.md), `DIA-PANEL-SEL-001`, sections 2–8 and 11 | Full panel rules govern constitutional/high-stakes/adversarial panels: eligibility, uniform draw, COI and prior-service exclusions, veto, quorum and tiered escalation. P051-002 names the lighter triage scope and the boundary requiring this procedure; it does not replace those rules with reputation baskets. VRF selection remains a mechanism hypothesis. |
| [Abuse Disclosure](../../normative/50-constitutional-ops/en/ABUSE-DISCLOSURE-PROTOCOL.en.md), section 9 | Notice, appeal and a new review composition apply on its sanction/disclosure track. The first local profile adopts at least 14 days to file an appeal; urgent protective isolation is a separate decision, not automatic closure of that window. |
| [Procedural Reputation](../../normative/50-constitutional-ops/en/PROCEDURAL-REPUTATION-SPEC.en.md), sections 2 and 8 | Procedural reputation and identity assurance remain separate eligibility gates; evidence is portable, not an automatically accepted score. Local fixtures do not validate the hypothetical scoring functions. |
| [Reputation Validation](../../normative/50-constitutional-ops/en/REPUTATION-VALIDATION-PROTOCOL.en.md), M11 and section 5 | Reuse M11's reason, review/expiry and appeal-path evidence for denials. P051-008 qualifies a local correction mechanism, not the simulation/shadow/pilot/adversarial-review sequence for reputation leverage. |
| [Node Rights Card](../../normative/50-constitutional-ops/en/NODE-RIGHTS-CARD.en.md), rights and graduated enforcement | Preserve inspection, appeal, subsidiarity and the rights floor against an operator. This slice binds each sanction to its author, basis, deadline and route back, without granting the operator adjudicative power. |

The 14-day local floor is an explicit profile decision, not a claim that every
normative track has the same deadline: Panel Selection section 7 lists 14 days for
normal and 7 for critical appeals, while Abuse Disclosure section 9 requires at
least 14 days with an earlier-isolation clause. P051-002 must pin the applicable
track and window-start/notice rule; neither a queued notice nor a failed delivery
alone proves that a participant had the required appeal opportunity. Longer
applicable protections remain in force.

The smallest useful implementation is one community-local public-object case:

```text
signal -> case + assigned owner -> bounded review / optional mediation
       -> reasoned decision -> authorized effect -> observed effect receipt
       -> notice + independent appeal -> correction -> recomputed effects + notice
```

This is a composition of existing contracts with a small case-domain state
machine, not a new transport, global reputation service or generic workflow engine.
No sanction, insufficient evidence, voluntary repair and contamination are legitimate
outcomes. Insufficient quorum is an explicit procedural blockage, not a merits
verdict. Silence, missed notification or an expired review window is not agreement,
guilt or permission to extend a hold.

Each open case must retain an accountable procedure owner, a next action, its
deadline, and an explicit escalation destination. Ownership transfers require
acceptance by the successor and a durable handoff. Departure, expiry or revocation
of an owner leaves an actionable unassigned/blocked state; it neither closes the
case nor silently delegates it to the infrastructure operator. Historical
decisions retain their authors after handoff.

The case owner persists distinct review deadlines, appeal-filing windows and
effect-validity limits. S020 owns wake-ups and bounded reconciliation launches,
not the meaning of those deadlines. Admission checks current mandate/effect validity
synchronously, independently of scheduled cleanup. Read-only inspection may derive
an overdue status but must not execute a correction. The baseline does not promise
proactive detection while Scheduler and all declared triggers are unavailable:
validity is enforced on use; durable reconciliation and notices resume through an
authorized execution path or resumed scheduled work. A stronger proactive guarantee
needs a separately declared independent monitor, outside this slice, not a private
timer loop hidden in the case service.

Record separately the signal author, subject, reviewer, decision authority,
effect executor and appeal authority. Bind actions to the exact case revision,
object revision/digest, policy revision, target decision and admitted mandate.
Historical replay uses retained inputs; new effects recheck current authority,
revocation and time validity. A policy change must not silently rewrite the
standards used to judge the original action.

Appeal can be filed without participating in the disputed Room or receiving a
notification. Selection retains auditable eligibility, recusal and randomness
evidence under the chosen policy; another agent or nym controlled by the original
decision maker is not evidence of independence. If a valid appeal pool cannot be
formed, expose that blockage and use the declared escalation path, not the
original group relabeled as an appeal body. Do not require civil-identity
disclosure or cross-community correlation merely to establish a review pool.
If the case owner or host operator is a party, they cannot accept the case as its
adjudicator, including through controlled alternate identities. Transfer requires
an independently authorized recipient's acceptance; otherwise record the blockage
and escalation destination. OQ6 concerns provisioning that route, not permission
for self-adjudication. The admitted policy must also state the effect-stay rule
during an appeal or blockage; runtime must not invent one.

### 26. Correct the Targeted Consequence, Not the Whole Participant

A correction targets identified decisions and their derived effects. It does not
grant new privileges, erase unrelated sanctions, override protected floors or
reopen revoked capability passports. Newcomer defaults remain entry policy, not
evidence of misconduct.

Maintain case/source attribution above S040 and recompute the remaining applicable
restrictions after a retraction. The current participant-wide clear operation is
not a case-specific undo. Likewise, `membership-policy-core`'s ordered overlays
are a deterministic composition mechanism, not authority precedence: an
`appeal-result` appended last must not defeat an unrelated case merely because
its value is `allow`.

The composition adapter must account for existing operator-imported restrictions
as independent sources and serialize or fence all competing writers. Unknown
source attribution blocks automatic relaxation and is visible for reconciliation;
it is not permission to retain an already-expired case effect. Recompute only
from still-applicable sources, with explicit bounds on sources and evidence.

Before the adapter's first case effect or correction, P018-13 must inventory the
existing restriction records and clear tombstones and retain a revision/digest-bound
baseline. Represent retained operator inputs as `legacy-operator-source`, preserving
their original evidence and unknown attribution; the label is not proof of a signed
verdict or recovered case ownership. Fence every writer during cutover and verify
effective restrictions at the same evaluation time for valid, unambiguous sources.
Malformed or ambiguous inputs retain their source and a typed refusal/diagnostic;
preserving a legacy fail-open result is not a compatibility goal. Resume a partial
migration idempotently before enabling correction. Unresolved inputs require
explicit reconciliation, not guessed attribution or silent removal.

Keep procedural outcome and effect application status separate. A successful
appeal can coexist with pending local recomposition or unacknowledged remote
correction delivery. Completion requires receipts for the declared effect scope;
unreachable consumers remain pending or explicitly unresolved. A local clear
cannot retract a publication already observed elsewhere.

### 27. Separate Protection, Reintegration and Systemic Repair

This extension implements the direction in [Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md),
"Care and Justice as Two Relational Modes", [Membership and Sponsorship](../../normative/50-constitutional-ops/en/MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md),
"Sanctions and Return Path", [Abuse Disclosure](../../normative/50-constitutional-ops/en/ABUSE-DISCLOSURE-PROTOCOL.en.md),
section 7, and [Reputation Validation](../../normative/50-constitutional-ops/en/REPUTATION-VALIDATION-PROTOCOL.en.md),
M8 and intervention-effectiveness review. It adds reviewable responsibility and
evidence, not a new sanction ladder or adjudication mandate.

| Concern | Responsibility | Boundary |
| --- | --- | --- |
| Protection | Contain a specific evidenced risk through existing P018/S040 effects, with individual grounds, current admission and independent validity. | Systemic review or repair must not delay necessary protection; aggregate prevalence is not individual evidence. |
| Reintegration | Record explicit, reviewable return conditions tied to repair and behavior, and evidence of their assessment. Request any authorized narrowing through existing source-addressed correction. | Meeting return conditions does not clear unrelated restrictions, grant missing entry rights, rewrite historical findings or establish that return is safe without assessment. |
| Systemic repair | Review access rules, incentives and sponsorship practices; record a proposed correction, accepted responsibility or escalation, execution evidence and outcome review. | A plan does not authorize its execution. Responsibility must use the target component's authorized interface, not mutate its configuration or policy directly. |

The prevalence of violations is grounds for reviewing the conditions of
cooperation, not an independent basis for increasing or reducing sanctions against
a particular participant. Do not introduce a demoralization score, a universal
percentage threshold, collective guilt or automatic sanction changes from report
volume. Agent/Corpus analysis may support review, never supply authority.

Preserve the norms' MUST/SHOULD distinction: record justified non-applicability or
deferral where appropriate rather than making every repair field a prerequisite
for urgent protection. An unavailable or conflicted owner requires a competent
recipient or explicit blockage; infrastructure ownership does not authorize
self-adjudication. Neither a missed repair deadline nor a pending outcome review
renews a protective restriction or establishes a new violation by itself.

## Reuse and Implementation Recommendations

### Existing Seams and Their Limits

Inspected on 2026-10-10 against the working tree and
`node:docs/implementation-ledger.toml`. These are implementation entry points,
not runtime acceptance results. This table records the pre-slice inspection;
the 2026-10-10 implementation checkpoint below supersedes its restriction gaps.

| Concern | Reuse | Boundary still to implement for P051 |
| --- | --- | --- |
| Surface policy and effective limits | `node:membership-policy-core/src/lib.rs`: `decide_surface`, `project_effective_limits`, source-tagged overlays and fixture/property tests | Ledger `membership-surface-access-policy-core` is `partial`: no complete daemon/storage/UI admission path. Admit sources, check validity and authority, then supply deterministic, case-aware composition. |
| Restriction application | S040/P018; `node:daemon/src/execution_host.rs`, `node:daemon/src/lib.rs`, `node:daemon/src/state_checkpoint.rs`, `node:daemon/src/tests/participant_policy.rs` | One current record per participant; clear is participant-wide; one hard expiry does not cover the soft layer or several independently expiring cases. Schema validation and `decision/author` text do not authenticate a community verdict. The pre-slice snapshot dropped an unparseable hard expiry through `.ok()?`; P018-13/14 now replace runtime reads with source-aware composition and retain malformed sources with explicit refusal diagnostics. |
| Identity and bounded relationships | P034 and S032; existing caller bindings and `local-relationship-core` | Reuse verified actor/owner context and private eligibility inputs. Relationship membership is not a grant; node-operator assurance is not reputation or a jury mandate. |
| Facts and recovery | S028; `node:temporal-event-log`, `node:storage-runtime`; existing restriction commit stream and notification store | One case-domain source of truth, rebuildable projections and an idempotent effect outbox; do not invent a global transaction registry or copy the case history into S040. |
| Attention and human action | [S039](../60-solutions/039-notifications/039-notifications.md), P057; `node:notification-core`, `node:notification-store`, `node:daemon/src/notifications_host.rs` | Recipient-bound case notices and registered actions must call the case owner, recheck revision/mandate, and report its result. Queue insertion, delivery, opening and substantive response are distinct. |
| Deadlines and long work | S020 Replay Scheduler; S029/P055 Bounded Deferred Operations | Scheduler wakes bounded reconciliation jobs; deferred handles describe individual work, not the lifetime of a social case. Admission itself checks expiry even if the scheduler is down. |
| Evidence exchange and provenance | S023 Artifact Delivery; S043/P081 causal context and execution receipts; P090/P086 evidence distinctions | Add domain acceptors and case-specific evidence references. Delivery, signature verification and host observation do not establish guilt, independent support or final adjudication. |
| Optional deliberation and policy extension | S036 Room, S038 Corpus, S047 Agent; P085 and `node:semantic-registry-core` | Reuse conversation/review assistance and exact revision-bound policy admission patterns. No existing generic social-policy registry or autonomous adjudicator is claimed. Agent output remains advisory; private case data needs its own disclosure/egress admission. |

Canonical companion contracts:

- [S019 Middleware](../60-solutions/019-middleware/019-middleware.md) and
  [P080 channel executor](080-multiplexed-middleware-channel-executor.md), with
  [S015 Module Store](../60-solutions/015-host-owned-module-store/015-host-owned-module-store.md)
  and [S016 bounded runtime](../60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md);
- [P034 operator binding](034-node-operator-binding-and-derived-node-assurance.md)
  and [S032 local relationships](../60-solutions/032-local-relationship-layer/032-local-relationship-layer.md);
- [S028 temporal storage](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md),
  [S020 Scheduler](../60-solutions/020-scheduler/020-scheduler.md) and
  [S029 deferred operations](../60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md);
- [S023 Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md)
  and [S043 horizontal primitives](../60-solutions/043-horizontal-protocol-primitives/043-horizontal-protocol-primitives.md);
- [S036 Room](../60-solutions/036-room/036-room.md),
  [S038 Corpus](../60-solutions/038-corpus/038-corpus.md) and
  [S047 Agent](../60-solutions/047-agent/047-agent.md);
- [P085 extension admission](085-operator-sovereign-extensibility-and-experiment-packages.md),
  [P090 inference provenance](090-inference-execution-provenance-and-non-local-disclosure.md)
  and [P086 observation](086-component-communication-observation-and-trace-sessions.md).

### Case Service Hosting Decision

The implementation direction is a small Rust domain core, a case service hosted
through existing middleware, and a host-owned enforcement adapter. The service
records and guards the procedure; it is not an autonomous judge, a generic ticket
system or a new workflow engine. A procedural owner recorded in a case remains an
accountable actor, not the service process or its infrastructure operator.

1. **Rust core.** Keep case data, the transition table, semantic validation and
   replay/projection pure. Supply time and verified authority context explicitly;
   the core does not read the clock, files, network or daemon state. Reuse
   `membership-policy-core` vocabulary and evaluators where their semantics match;
   do not move the case lifecycle into that kernel or copy its policy composition.
   Keep runtime dependencies above the core and enforce that direction in tests.
2. **Middleware-hosted service.** Use S019/P080's supervised `channel_json`
   lifecycle, authenticated session, module reports, declared routes and host-call
   bridge. Reuse existing package admission, module data-directory and bounded
   runtime facilities instead of adding a private supervisor, listener or IPC
   protocol. The service owns the case fact store, rebuildable read models and
   durable effect outbox under S028, reusing existing storage primitives. Case
   transition and pending-effect intent share a transaction; host application is
   a separate, recoverable step, not a cross-store atomicity claim.
3. **Host-owned enforcement adapter.** Keep P018/S040 source composition, current
   authorization and restriction application behind the host boundary. The service
   requests a case-scoped effect through the existing host-call mechanism; the
   host checks caller binding, case/decision revision, mandate, target, revocation,
   validity and idempotency before applying it and returning an outcome. Module
   admission is not adjudicative authority. Do not expose unrestricted operator
   import/clear to the service or let it write the restriction store directly.

P051-002 defines the narrow command/outcome boundary jointly with P018-12. Any
missing operation is explicitly registered and schema-gated under P072; the
existing bridge is reused, not assumed to already provide a case-effect API.
`responsibility-core` / `responsibility-service` settle the local crate and process
boundary under P051-003 without duplicating the
Rust rules in a second implementation. Follow `node:DEV-GUIDELINES.md`; create
separate crates only where the dependency boundary warrants them. Daemon routing
stays a thin adapter, not the owner of social procedure.

Reuse S039 for notices and action delivery, S020 for bounded reconciliation
launches, and S029 when one operation needs a deferred handle. None replaces the
case's durable history. Detachment or loss of a required host capability leaves
pending work and an explicit unavailable/blocked outcome; reattachment revalidates
authority before retrying. It cannot transfer adjudication to the host operator,
renew a restriction or turn an unacknowledged effect into success. Existing host
admission continues to enforce effect validity independently of service uptime.

### Small Contracts Before Endpoints

Specialize only the first required artifacts from the family below. Freeze a
transition table and semantic validators before implementing UI or importing
remote judgments. Common case bindings should include `case/id`, `case/revision`,
`subject/ref`, `object/ref` plus digest, `surface/id`, `policy/ref` plus revision,
actor/mandate references, validity and targeted predecessor/effect references.
These are design requirements, not newly published schema fields.

Keep community criteria and thresholds in admitted policy data; do not create a
closed repertoire of acceptable opinions, problem topics or successful outcomes.
Start with explicit local policy admission; portability and signed community
packages are later adapters, not prerequisites for local correction. Where a
semantic-registry specialization is used, preserve exact binding, expiry,
revocation and unresolved-ceiling semantics. Package admission cannot create
adjudicative authority by itself.

Schema Gate must protect the exposed contracts, with semantic checks for current
mandates, target identity and permitted transitions in the owning core/host.
Register operations under P072 with their actual dispatch/host-route boundaries;
an inspection capability must not expose operator mutation. Reuse existing
signing, canonicalization, delivery and caller-binding facilities, not ad hoc
signatures, HTTP callbacks or UI-supplied actor identities.

### Durable Correction and Bounded Attention

Persist the authorized case transition and pending effects atomically in the case
store. Apply effects through existing owners with a case/effect-scoped idempotency
key; append their outcome references. Retry after restart without double sanction,
duplicate reputation events or repeated notices. Cross-store failure stays a
reconcilable pending effect, not a fabricated atomic success.

Use source-addressed retractions/supersessions for reputation projections. Keep
sealed or access-controlled evidence separate from minimal case metadata and
public corrections; neither notifications, SSE nor traces may export the full
private case. Bound retention, payload size, fan-out, queue length and retry time;
cleanup must preserve live appeal obligations and disclose evidence-retention gaps.

Protected access needs a real path: an affected participant must be able to read
the admissible reasons and file a bounded appeal despite a publication/marketplace
restriction, Room removal or muted notifications. "Not hard-blocked" alone is
insufficient; test soft cooldowns and ordinary anti-abuse limits for starvation.
This does not grant unlimited messaging or bypass recipient privacy.

### Structured Review and Repair Without a Parallel Workflow Engine

P051-010–014 extend the existing case service. The current
`node:responsibility-core/src/contracts.rs` has `RecordReview { reason }`,
decisions, evidence references and targeted correction; these are reuse entry
points, not evidence that structured repair is already implemented. Inspect the
current contracts and callers before selecting fields or new operations.

1. **Small contract extension.** Extend case/review artifacts or attach a bounded,
   case-bound artifact where that avoids coupling independent lifecycles. Freeze
   the minimal transition table before endpoints. Represent reviewed scope and
   observation window, evidence references and uncertainty, an alleged mechanism
   separately from an established finding, intended correction/outcome, owner and
   mandate bindings, accepted ownership or escalation, return conditions, review
   deadline, execution evidence and outcome assessment. These are semantic
   requirements, not preselected schema names or a closed catalogue of repairs.
   Keep criteria in admitted policy data; missing legacy information is unknown
   or not assessed, never completed, safe or harmless.
2. **Separate claims and authority.** Proposed, authorized, accepted, executed
   and outcome-reviewed claims require their own evidence. Reuse signed commands,
   current host admission and the accepted-handoff pattern rather than treating
   an owner label as acceptance. A plan's acceptance does not extend a mandate;
   execution must pass the owning component's current authorization. Preserve
   protected reasons/appeal access and the existing conflict/independence rules.
   Version changed wire/replay semantics where necessary, preserving historical
   signed bytes. Use canonical schemas, Node mirrors, Schema Gate and P072's
   existing registration boundaries; do not make operator writes module-dispatchable.
3. **Existing runtime and storage.** Keep transitions and validation pure in
   `responsibility-core`, durable coordination in `responsibility-service` through
   S019/P080 `channel_json`, and enforcement in the P018/S040 host adapter. Reuse
   S028 facts, rebuildable projections, transactional outboxes, exact receipts and
   idempotency. No second restriction engine, listener, supervisor or generic
   workflow engine. Bound cross-case references, history and review work so that
   repair analysis cannot starve protection, participant rights or correction.
4. **Attention and deadlines.** Extend the existing signed API and ParticipantSession
   UI; reuse S039 recipient-bound actions/notices. A queued notice does not prove
   acceptance, execution or receipt by the participant. P051-013 integrates review
   deadlines through P051-007/S020 bounded jobs, never a private timer. Before that
   integration, provide authorized manual review and explicit overdue/unavailable
   inspection without claiming proactive scheduling. Service/scheduler outages
   neither extend effects nor turn pending work into success.
5. **Outcome evidence, not a success score.** Build a bounded read model from
   authorized facts, distinguishing reports from confirmed harm and repeated
   reports of one incident from independent incidents. Preserve observation scope,
   window, policy/measurement revision, changes in reporting practices, evidence
   limits and participants who have not returned. Increased reporting may reflect
   better detection or trust; fewer reports or a short return time alone do not
   establish improvement. Missing follow-up stays unknown. Reviewer conclusions
   carry their basis and uncertainty; the system does not infer causality from
   these counts. Keep private cross-case evidence sealed/access-controlled and
   redact participant projections, notifications and traces.

### Necessary Dependencies Versus Lower-Rework Sequencing

The recommended implementation order is:

**A → N → B → C → D → P051-010/011/012/014 → optionally P051-013.**

The stage labels group the broader Responsibility follow-up and do not imply
completion. Normalization and recovery have separately scoped implementation
tasks P051-015/016 under their existing owners:

| Stage | Scope / existing ownership | Why prefer it before the repair slice? |
| --- | --- | --- |
| A | Admitted membership facts and runtime entry-policy integration under P051-001/004 | Reuse real admission and effective access composition when evaluating return, rather than rebuilding that integration later. |
| N | Host-state normalization under S028 and the existing Responsibility/P018 host owners | Put new facts, authorization snapshots, source revisions and receipts into the target stores, instead of extending a format already scheduled for migration. N precedes B in this follow-up plan. |
| B | Local panel procedure under P051-006 and versioned P018/S040 effect lifecycle | Reuse revisioned suspension, resumption and terminal retraction without confusing a panel disposition with applied consequences. |
| C | Procedural deadlines under P051-007/S020 | Establish the shared bounded-job mechanism; its availability does not itself implement scheduled repair reviews under P051-013. |
| D | Same-host backup, restore, reconciliation and compaction under S028 and the existing store owners | Reuse host-incarnation and receipt semantics, retention and recovery boundaries instead of qualifying a second interpretation later. |

This is a cost-of-rework recommendation, not a new hard dependency chain for the
manual repair slice. Its necessary task dependencies remain in the tracker:
P051-010 → P051-011 → P051-012 → P051-014, using the qualified
P051-002/003/005 and P018-13/14 baseline. Completion of all membership admission,
independent panels, scheduling or restore work is not a universal prerequisite.
N and D need separately scoped implementation/evidence work under their existing
owners; the ordering label does not add them to a completed baseline task.

Perform a short P051-010 contract-alignment pass **before N/B/D freeze their
interfaces**, without treating that pass as completion of P051-010 or starting
the whole repair implementation. Record the selected contract revisions,
owners, compatibility decisions and required regressions:

| Alignment point | Contract to agree | Required preservation / test |
| --- | --- | --- |
| N: durable review identity | Repair reviews have explicit identity, revision and their own deadline; facts refer to immutable authority snapshots and accepted ownership without granting a mandate. Map them to normalized stores, projections and outboxes using existing primitives. | Preserve signed source bytes, CAS, replay, idempotency and pending obligations across migration. Compare old/new projections at the same evaluation time; do not clone global authority state per repair command. |
| B: decision versus effect | Bind any repair-driven correction to the exact source and revision. Agree how `applied`, `suspended` and terminal `retracted` effects are inspected and corrected, independently of panel decisions and repair-plan status. | Correcting one source cannot clear another, resume a terminally retracted source, extend original validity or turn plan acceptance into execution authority. Preserve stale-command refusal and protected access. |
| D: execution evidence after restore | Bind new host execution receipts to the applicable incarnation. Historical evidence remains historical; current application requires explicit confirmation under the recovery contract. Include repair facts, evidence bindings, pending outboxes and live review obligations in snapshot/retention rules. | Restore preserves unfinished work without fabricating current application; compaction cannot remove live obligations, required authority evidence, idempotency or terminal fences. Extend existing D regressions rather than create a repair-only backup mechanism. |

The preferred path completes A–D first, then refreshes P051-010 against the actual
qualified baseline and implements the manual slice. An earlier insertion **after
A and N** is reasonable if the B/D interfaces above have been agreed, unsupported
operations remain explicitly unavailable, and later migration/regression work is
recorded. Contract agreement is not evidence that B or D works; exclude unbuilt
panel/restore behavior from that earlier profile. Do not run competing rewrites of
the same signed-command, host-store and replay contracts in parallel.

Reuse whichever prerequisite interfaces are actually complete. Excluding the
broader A–D work from the repair slice means not redoing or expanding it, not
avoiding its existing interfaces. Keep manual review independently usable even
after C lands. Integrating repair-specific scheduled jobs still belongs to
P051-013 and needs its own runtime evidence. This sequencing does not merge the
workstreams or promote local mechanism tests to real-participant readiness.

### Systemic-Repair Slice Acceptance

P051-014 qualifies a new local test-subject profile using the existing
local-accountability runner/report/qualifier ownership below. Freeze the scope
before execution; do not relabel historical review-v2 evidence. Exercise actual
commands, service persistence, host enforcement, participant inspection and S039
delivery, not injected final states. Required cases include:

- aggregate prevalence alone cannot alter a participant's restriction; repeated
  reports do not manufacture independent findings;
- a protective action proceeds while systemic repair remains pending; a missed
  repair deadline does not renew the protective effect;
- absent mandate, conflicted/unavailable owner or missing escalation destination
  produces an explicit refusal/blockage, not self-authorization;
- plan acceptance, execution evidence and outcome review remain distinct; no
  receipt means no confirmed external effect;
- safe-return correction removes only named effects while preserving unrelated
  case/operator sources and missing entry authority;
- restart, duplicate commands, delayed receipts and unavailable dependencies
  preserve ownership, deadlines, protected access and truthful pending states;
- legacy cases remain readable without invented review outcomes; unauthorized
  inspection cannot reveal private cross-case evidence;
- rising report counts, non-returners and absent follow-up cannot manufacture an
  effectiveness verdict.

The first profile may qualify manual review with explicit overdue inspection.
Scheduled reviews require P051-013's additional source-bound runtime evidence;
do not claim them from the manual profile. Keep real-participant sanctions,
independent appeal readiness and federation outside this slice. Mechanism
acceptance does not establish that a social intervention actually reduces harm.

When the tested baseline includes N/B/D, P051-014 must additionally retain repair
integration regressions for normalized persistence, revisioned effect lifecycle
and restore/compaction of unfinished repair obligations. An earlier bounded
profile must state which of these remain unimplemented; later qualification must
use fresh evidence, not promote the earlier report to the expanded scope.

## Cross-Component Acceptance: Local Accountability

P051 owns the semantic acceptance scenario and aggregate closure, not a new
protocol. Node homes exist for the bounded local profile below; the wider
P051-008 matrix remains open:

- `node:tools/acceptance/local-accountability/README.md` and its runner for
  reproducible procedures, linked from the acceptance index;
- `node:docs/evidence/local-accountability/` for revision-bound results, linked
  from the evidence index;
- a short `node:docs/integration/` guide only if the implemented flow needs one,
  linked from its index and owning service README, not another tracker.

First prove one host with separately authorized participant roles and deterministic
fixtures, not an LLM or physical multi-host dependency. Seed review-pool eligibility
explicitly and exercise the selected selection policy; report that seeded identities
prove separation of authority, not real-world human independence. Add a two-host
Artifact Delivery correction profile only after local closure. Corpus/Room-assisted
review is optional and must not become necessary to file an appeal.

| Case | Required retained evidence |
| --- | --- |
| Signal, review, decision, notice, appeal, correction | Each transition names actor, mandate, policy, target and next owner; decision and observed enforcement are separate receipts. |
| Two independent restrictions, appeal of one | Corrected case disappears from the current effect; unrelated case and newcomer defaults remain. Duplicate or reordered correction cannot resurrect it. |
| Hard hold and soft penalty expire during outage | Current checks stop both expired effects; reconciliation after restart records the transition without renewal or fabricated consent. |
| Scheduler unavailable, then resumed | Persisted review/appeal/effect deadlines remain distinct. With no access or other trigger, no proactive notice is claimed; read-only inspection exposes overdue state without mutation. Admission enforces validity; resumed reconciliation is idempotent and does not renew effects. |
| Legacy restrictions at adapter activation | Pinned record/tombstone inventory, explicit legacy sources, all-writer fencing and same-time effective-value equivalence for valid sources; malformed/ambiguous inputs retain evidence and typed refusal, not a legacy fail-open result. Restart cannot lose a source or enable premature correction. |
| Malformed expiry in recovered restriction data | Recovery/admission exposes a typed validity failure; affected privileged admission is refused, not silently unblocked. Protected inspection/appeal remains usable; corruption is not a new misconduct finding. |
| Crash or middleware detachment between decision, effect and notification | Real channel-hosted service replay/reattachment converges to the same projection; retries revalidate authority and do not duplicate effects; pending work remains inspectable without fallback to operator authority. |
| Owner revoked or leaves with an open case | Stale approval/action is refused; accepted handoff preserves the original authors and deadlines, or exposes an unassigned blockage. |
| No independent pool or insufficient appeal quorum | `AppealBlocked` preserves prior findings as history; effects follow the explicit stay/expiry policy. Council remits/arranges independent review or records continued blockage, never automatic exoneration, guilt or renewal. |
| Optional mediation refused | Direct formal appeal remains available; refusal is not guilt and mediation is not mandatory. |
| Host operator or case owner is a party | Self-adjudication and controlled alternate identities are refused; an independently authorized recipient accepts durable handoff, or the case exposes blockage and escalation. Existing deadlines and effect policy are preserved. |
| Restricted participant with Room removal and quiet notifications | Direct authorized case inspection and bounded appeal remain usable; no cross-recipient evidence disclosure. |
| Correction crosses hosts | Recipient authenticates domain authority and target, records application or refusal, and exposes delivery/retention gaps; transport acknowledgement alone does not close the case. |

The cross-host row belongs to P051-009; the other rows form the P051-008 local gate.
The local profile must exercise actual case, enforcement and notification adapters,
not merely unit reducers or manually imported synthetic final states. Reports name
real/substituted boundaries, repository revisions, commands, failures and remaining
limits. Passing it demonstrates a correction mechanism, not fairness of every
community policy or measured reduction of the Ringelmann effect. Denial fixtures
must retain M11's reason, review/expiry and appeal path, without claiming the wider
reputation-validation programme has passed.

The bounded local slice freezes `node:docs/contracts/local-accountability-report.v1.schema.json`
and its qualifier before the runner. The remaining P051-008 matrix must likewise
freeze a new explicit profile before extending runtime qualification. Reuse the scope and source-retention patterns in
`node:tools/acceptance/story-013-qmail-task-pack/README.md` and `retain_report.py`,
not their qmail-specific profile, run identifiers or assertions. This is an
acceptance artifact, not another federation protocol. At minimum:

- reports declare `profile/id`, `evidence/class`, `qualification/scope` and
  `qualification/exclusions`; CLI arguments check these claims, not promote them;
- each required case binds observed owner receipts, refusals and pending outcomes,
  rather than only asserting success booleans;
- pin the tested Node commit/tree, scenario/policy/fixture digests and qualifier
  revision; retain exact source and original report bytes/digest immutably;
- requalification preserves original execution scope: old, unit-only or local
  evidence cannot become a fresh or cross-host runtime run;
- redacted exports retain verifiable bindings for their declared scope, or state
  which qualification they cannot preserve. Do not expose private evidence merely
  to obtain a public passing report.

Qualifier fixtures must reject missing/duplicate cases, substituted bindings,
scope mismatches, mismatched source pins and historical-scope promotion. Its job
is to verify the declared evidence contract, not automate the social truth of a
judgment. Reuse existing atomic report persistence; extract genuinely shared
retention helpers only where needed rather than cloning Story 013's runner.

## Trade-offs and Failure Modes

- Composition avoids parallel stores, transports and UI engines, but source-aware
  correction is still new domain work; existing timestamps and `reason/ref` do
  not supply it automatically.
- Pinned case policy supports audit; fresh authority/expiry checks prevent replay
  from granting expired power. Preserve both contexts rather than choosing one.
- Independent review costs time and available people. Bounded holds and explicit
  unresolved outcomes are safer than relaxing independence to force completion.
- Multiple identities or models can share one controller. Unknown independence is
  not plural support; scoped evidence must not become an ambient surveillance graph.
- Provisional actions can cause irreversible external harm. State the remaining
  repair obligation even after the current restriction has been removed.

## Suggested Future Artifact Families

This proposal now freezes the first small membership and surface-policy artifact
family. These are the immediate contracts:

- `membership-invitation.v1`
- `membership-sponsorship.v1`
- `membership-acceptance.v1`
- `participant-entry-profile.v1`
- `participant-effective-limits.v1`
- `surface-access-policy.v1`

The broader public adjudication and reputation family remains future work:

- `object-review-case.v1`
- `object-flag-event.v1`
- `review-round.v1`
- `review-vote.v1`
- `reputation-event.v1` or a specialization of `reputation-signal.v1`
- `reputation-mediation-request.v1`
- `reputation-mediation-outcome.v1`
- `reputation-appeal-request.v1`
- `reputation-appeal-decision.v1`
- `collusion-signal.v1`

The preferred shape is append-only facts plus read models, not mutable
"membership status" rows as the primary source of truth.

## Resolved Design Decisions

- Sponsor liability is direct and one-hop by default; further propagation is
  reserved for proven sponsor-ring behavior.
- Contact attestation unlocks contactability and anti-spam affordances only; it
  is not legal identity and not public-trust eligibility.
- Open self-enrollment is allowed only as low-trust entry with tighter limits
  and slower access to high-impact surfaces.
- Newcomer limits are entry policy. `participant-capability-limits.v1` remains
  sanction or restriction policy.
- `surface-access-policy.v1` is the policy-axis source of truth.
  `participant-entry-profile.v1` and `participant-effective-limits.v1` are
  computed read models.
- Sponsorship uses templates and ordinal liability classes instead of numeric
  pseudo-precision.
- Public-object state uses lifecycle, judgment qualifier, and withdrawal-reverts
  axes instead of one compound enum.
- The first anti-collusion baselines are sponsorship velocity, co-flagging
  coherence, and closed-loop receipt detection.
- Political, ideological, religious, and campaign content is allowed on
  explicit opt-in surfaces; non-consensual high fan-out persuasion is the abuse
  class.
- Marketplace reputation must be evidence-backed through settled interactions,
  not self-dealing or closed-loop boosting.

## Open Questions

1. What minimal diversity constraints should be required before artifact-level
   sentiment becomes author-level reputation?
2. Which implementation and audit profile should realize the remaining random
   selection mechanism? `DIA-PANEL-SEL-001` already fixes in-scope eligibility,
   recusal, uniform drawing, veto and escalation; its VRF/entropy construction
   remains a hypothesis, not a reason to redesign those settled safeguards.
3. Which contamination heuristics should remain only heuristic signals, and
   which are strong enough to trigger procedural rollback by default?
4. Which parts of membership bootstrap belong to the local node wizard, and
   which should remain explicit social actions performed outside the node?
5. Which bootstrap and dispute artifacts should be portable across communities,
   and which must remain local to the group's policy surface?
6. Which first community policy supplies a sufficiently independent appeal pool
   and an escalation destination when the local operator is a party? Until selected,
   fixtures may demonstrate the contract but cannot certify live social readiness.
   The prohibition on self-adjudication is settled; only the independent recipient
   and operational availability of that path remain open.


## Local implementation checkpoint: 2026-10-10

The bounded implementation decision is **local case → restriction → targeted
correction**, for explicitly admitted test subjects on one host. P051 owns
procedure and responsibility; P018/S040 own source composition and enforcement.
The frozen contracts and Node ownership are recorded in
`node:docs/development/LOCAL-ACCOUNTABILITY-CONTRACT.md`.

`responsibility-core` is pure. `responsibility-service` persists append-only
SQLite facts, rebuildable projections and atomic effect/notice outboxes through
S019/P080 `channel_json`. The host independently verifies signed command,
actor, mandate, policy, object and case revision, mirrors accepted procedural
facts and applies exact P018 sources under the shared writer gate. Transport
registration does not create a mandate. Review, appeal and effect validity are
separate axes; an appeal or `AppealBlocked` leaves the original effect expiry
unchanged. Acknowledgment names the exact reasons and opens at least 14 days;
without acknowledgment filing remains open, including before notification.

P018-12 settles compatibility: `participant-capability-limits.v1` remains
operator input. New `participant-restriction-source.v1` facts preserve each
case/decision/effect's operation scope and validity; hard blocks compose by
union and soft factors by minimum. v1 export refuses lossy composition, and
participant-wide DELETE refuses active or unresolved case sources. A pinned
legacy baseline preserves operator records, tombstones and unknown authorship;
malformed validity is retained and refuses affected privileged operations.

ParticipantSession UI, direct signed APIs and registered S039 actions all call
the same service. Inspection, exact reasons acknowledgment and appeal remain
available without a Room or notification. Private evidence uses a separate
sealed host table and case-bound references. Bounded history, command, source,
evidence and outbox budgets reserve work for participant rights and correction.

The retained Node runtime evidence at
`node:docs/evidence/local-accountability/2026-10-10-qualified-local/` uses the frozen `local-accountability.test-subjects.v1` report and qualifier,
with original tested source, policy, fixtures, receipts, refusals and pending
outcomes. Review corrected the reporting claim to 18 runtime cases and two
conformance bindings; the original bytes remain historical and do not qualify
the corrected implementation. P051-002/003/005 are now done for
`local-accountability.test-subjects.review-v2` after fresh source-bound gates:
18 runtime cases plus two conformance bindings, 713 checks across 15 suites and
27 qualifier tests (one positive and 26 negative). Current original report and
qualification are
`node:docs/evidence/local-accountability/2026-10-10-review/passage-3/report.json`
and `qualification.json`, with report digest
`sha256:4c16aa570954c29bb2cb1c45317f837c9dad563e9d8b2871ad2dbaea96d91b72`.
Findings and unqualified attempts remain in the parent review record.
The scope is not the complete acceptance matrix below. Case effects remain disabled by default. Declared
controller groups and explicit fixture mandates prove local contract behavior;
they do not establish an independent social institution or authorize sanctions
against real participants. Proposal status and normative adoption are unchanged. The local selector takes
the first eligible independently declared actor; full DIA-PANEL-SEL-001 selection,
appeal merits dispositions and procedural deadline escalation are unmodeled
P051-006/007 work, not implied by the minimal contract.

## Implementation Direction

The earlier bootstrap-first sequence remains useful for onboarding, but the pure
policy kernel and restriction runtime now let the correction work proceed without
waiting for a complete wizard, reputation engine or anti-collusion service.

### Implementation Tracker

Statuses: `todo`, `partial`, `done`, `deferred`. `done` requires the named evidence
and matching Node ledger scope; contract maturity, hard-MVP inclusion and runtime
qualification remain separate. This review does not promote P051 to accepted or
expand the current release scope. Implementation tasks must update the Node ledger,
regenerate its view and reconcile `docs/MVP.md` when its covered scope changes.

`Depends on` lists necessary task gates. The recommended A–D sequence and early
N/B/D contract alignment are defined in
[Necessary Dependencies Versus Lower-Rework Sequencing](#necessary-dependencies-versus-lower-rework-sequencing);
they are not additional blanket completion prerequisites for P051-010–014.

| ID | Work / owner | Status | Depends on | Completion gate |
| --- | --- | --- | --- | --- |
| P051-001 | Membership policy baseline / membership-policy-core | partial | Existing frozen family | The pure kernel now has a separate host-admitted procurement consumer. Six source-bound runtime cases qualify local candidacy/admission/revocation/expiry and own-entry UI; signed Agora carrier import remains a fixture, not publication/subscription proof. Monetary caps and the complete operation matrix remain open. Evidence: node:docs/evidence/local-accountability/2026-10-14-admitted-entry/passage-4/report.json. Do not duplicate the kernel or promote this subset to complete entry-policy qualification. |
| P051-002 | First case/policy contract and ownership / Rust domain core boundary | done | Existing P051/S040 contracts | review-v2 freezes the scoped case/policy/mandate/command/effect contracts, three deadline axes, exact acknowledgment with 14-day floor, controller independence, retryable AppealBlocked and recipient-bound correction. New authority is domain-only; historical proof has separate host-bound narrowing/receipt transport. Canonical schemas, mirrors, Gate, negative fixtures and split P072 operations pass. Local first-eligible selection, absent merits dispositions and procedural escalation are explicitly bounded P051-006/007 work. Evidence: node:docs/evidence/local-accountability/2026-10-10-review/passage-3/report.json. |
| P051-003 | Rust case core and durable middleware-hosted service / case domain | done | 002 | Pure responsibility-core and channel_json service with append-only SQLite facts, rebuildable projections, accepted handoff and atomic transition/intents. Ordered outboxes retain accepted narrowing through revocation, prepared evidence is preflighted and typed mirror desync fences later work without claiming success; reasons/listing survive, blocked mutations are explicit. Historical replay/transport and bound receipts have named regressions. Actual outage/restart is qualified; automatic cross-store desync repair/portable backup remain unqualified. Evidence: node:docs/evidence/local-accountability/2026-10-10-review/passage-3/host-tests.json and report.json. |
| P051-004 | Targeted restriction and entry-policy integration / host-owned P018-S040 adapter | partial | 001, 003, P018-12, P018-13 | Targeted P018 host application/correction and independent expiry are implemented and locally qualified. A separately qualified admitted procurement subset now consumes the pure evaluator, composing with independent P018 sources. Full entry-policy admission, Agora publication/subscription and operation/value mappings still require P051-001. Evidence: node:docs/evidence/local-accountability/2026-10-14-admitted-entry/passage-4/report.json. No complete P051-004 claim. |
| P051-005 | Participant notice, case inspection and appeal actions / case service consuming P057-S039 | done | 003 | S039 recipient-bound subject/appeal/handoff notices, direct reasons/acknowledgment/appeal and ParticipantSession UI use the same service. Actual default host signer emits verified domain proofs; UI preserves owner refusal/unavailable status and only bound withdrawal receipts show retracted. A/B/C UI list and exact second-policy reasons remain available with profile disabled, subject removed and policy revoked. CSRF, stale actions, independent acknowledgment/handling, sealed evidence and protected reserves pass; no notification or Room prerequisite. Evidence: node:docs/evidence/local-accountability/2026-10-10-review/passage-3/report.json. |
| P051-006 | Independent appeal and repair / case domain | todo | 003, 004, 005, 015 | Policy-bound pool with recusal/randomness evidence and applicable DIA-PANEL-SEL-001 safeguards; no self-review or reuse of original decision makers. Exercise AppealBlocked, explicit effect-stay policy and Council exits without a merits verdict from missing quorum; source-addressed correction survives restart. Agent/Corpus advice cannot decide sanctions. The Node checkpoint adds eleven procedure tests, three signed-input tests, a complete public draw golden and an independent framing/PRNG reference for the explicitly experimental `local-panel.tai-fixtures.v1` profile; current normative PL requires ELL2. Eleven canonical draft panel/input/lifecycle contracts and historical COI mirrors have structural Gate coverage. Five case-journal and four host-input conformance tests cover atomic facts, original bytes, independent admission, replay and corruption under the existing storage/write owners. This is conformance only: the journal and host input lane are internal, while endpoint/channel integration, supplementary orchestration, sealed VRF custody, protected UI, lifecycle application and runtime qualification remain open, so this row is not closed. |
| P051-007 | Bounded deadlines, ownership and contamination inputs / domain jobs | todo | 003 | Persist separate review/appeal/effect deadlines; shared S020 Scheduler launches bounded case-service actions through existing dispatch, not a private timer loop; use S029 for deferred individual operations where needed. Host admission enforces current validity. Prove outage with no proactive-notice claim, read-only overdue inspection and idempotent resumed reconciliation. Unavailable owner, dropped notice or failed job never extend a hold or imply guilt. Sweep signals enter review, not direct sanctions. |
| P051-008 | Local-accountability acceptance / cross-component harness | partial | 004, 005, 006, 007, P018-14 | Node-local v2 report/qualifier qualifies exactly P051-002/003/005 and P018-12/13/14: 18 runtime cases plus two conformance bindings, 713 checks/15 suites and 27 qualifier tests (one positive, 26 negative), source/binary-bound original bytes. Historical v1 and failed review attempts remain immutable. Full acceptance including P051-001/006/007 is open; no historical scope promotion. Evidence: node:docs/evidence/local-accountability/2026-10-10-review/passage-3/qualification.json. |
| P051-009 | Remote correction acceptance / case Artifact Delivery acceptor | deferred | 008 | Two-host authenticated decision/correction delivery, local admission, duplicate/reorder/restart and unreachable-recipient evidence; bounded P081 causal/replication primitives only where needed, no global sanction propagation. |
| P051-010 | Protection, reintegration and systemic-repair contracts / case domain | todo | 002 | Map section 27's norms to existing contracts and missing behavior; freeze separate claims, transition/authority table, applicability/deferral and legacy semantics. Record the N/B/D alignment decisions before their interface freeze, then refresh against the selected implementation baseline; this early pass alone does not complete 010. Pin schema/versioning, signature/replay compatibility, canonical schemas, mirrors and Schema Gate negative fixtures. No aggregate-to-individual authority, fixed prevalence threshold or closed repair repertoire. |
| P051-011 | Durable structured review and repair / responsibility-core and responsibility-service | todo | 010, 003, P018-13 | Implement the bounded local lifecycle using current signed commands, accepted ownership/handoff, S028 facts and outboxes. Preserve independent protection, return review and systemic repair; reuse exact host receipts and source-targeted narrowing. Outcome read model distinguishes reports/findings, duplicates, non-returners and unknown follow-up. Prove refusal, restart/idempotency, legacy replay and unrelated-source preservation; do not implement a second enforcement or workflow engine. |
| P051-012 | Repair inspection and participant actions / existing API, UI and S039 | todo | 011, 005 | Existing signed API and ParticipantSession UI expose authorized plan/acceptance/execution/outcome actions, return conditions and manual review with explicit overdue/blocked status. Notices remain minimal and recipient-bound; queueing is not acceptance. Verify mandate/COI checks, stale actions, protected access and cross-case privacy. No new UI-owned state machine. |
| P051-013 | Scheduled repair outcome reviews / existing domain jobs and S020 | todo | 007, 011, 012 | Extend the shared scheduler-owned bounded jobs, not a private timer. Freshly check action authority and separate repair review from effect expiry. Retain runtime evidence for due review, scheduler/service outage, manual fallback and idempotent resumption; overdue work cannot renew restrictions or infer guilt. A manual-only acceptance report cannot satisfy this gate. |
| P051-014 | Systemic-repair local acceptance / existing local-accountability harness | todo | 011, 012, P018-14 | Freeze a new explicit report/qualifier profile and run every Systemic-Repair Slice Acceptance case through real service, host, inspection and notice paths, including restart. Bind sources, policy, fixtures and receipts; reject incomplete/substituted evidence and historical-scope promotion. Include N/B/D repair integration regressions when present in the tested baseline; otherwise declare exclusions and required later requalification. Manual review is the first bounded scope; scheduled claims additionally require 013 evidence. No real-subject, federation or social-effectiveness qualification. |
| P051-015 | Host-state normalization / S028 and existing Responsibility-P018 owners | partial | 003, P018-13 | Normalize projections and shared immutable authority material before panel facts. Preserve exact signed facts, source CAS, receipts and pending work; replay-gate resumable migration. Prove changed-record writes and subject/operation admission costs with a new N runtime report. Three runtime cases and two conformance bindings qualify N passage 4: node:docs/evidence/local-accountability/2026-10-14-normalization/passage-4/report.json. The original N report predates the internal panel-input lane, which requires separate runtime qualification; the A report predates N and cannot close this gate. Early 010 alignment confers no mandate and does not implement repair. |
| P051-016 | Local maintenance, restore and retention / host and case-store owners | todo | 015, 003, 007 | Separate D scope after A–N–B–C: quiescent encrypted backup, fresh-directory restore with new incarnation, exact-byte reconciliation and retention preserving live appeals, pending outboxes, unfinished reviews and terminal fences. Safe manifests only in evidence; no distributed clone fencing or real-subject qualification. |

The detailed enforcement work belongs to P018-12 through P018-14, linked from S040;
P051 owns integration and social semantics. P057 and P081 are dependencies, not
duplicate backlog owners: add tasks there only if implementation exposes a missing
generic notification or causal primitive. Their existing completion claims do not
cover this new consumer. Broader onboarding, sponsor-ring detection and public
reputation projections remain separate follow-ups, not hidden acceptance prerequisites.

P051-010–014 are additive scope, not a reopening of P051-002/003/005 or P018-12–14.
The manual local slice can proceed without completing the whole entry-policy,
independent-appeal or scheduler backlog. Its dependency on existing enforcement
does not qualify missing entry-policy integration. P051-013 separately owns
proactive review scheduling; P051-014 does not close the broader P051-008 matrix.
Update the Node ledger and affected generated views during implementation, with
explicit evidence scope; this proposal-only change is not an implementation claim.

### Next Actions

1. Perform the short P051-010 alignment pass before N/B/D freeze their contracts.
   Record shared ownership, revisions, compatibility and regression obligations;
   do not count this pass as the completed repair contract or implementation.
2. Prefer A → N → B → C → D for the broader follow-up: complete admission and
   runtime consumption under P051-001/004, normalize host state before panels,
   implement the local P051-006 procedure and P051-007 deadlines, then qualify
   same-host recovery. Scope N/D work separately under the existing owners.
   Local fixtures are not live sanction readiness.
3. Refresh P051-010 against the resulting baseline, then implement and qualify
   P051-011/012/014 as a separate manual slice. Earlier insertion after A/N is
   allowed under the contract-alignment and explicit-exclusion conditions above;
   it is not the default lower-rework path.
4. Add repair-specific scheduled reviews under P051-013 only with their own
   evidence. Extend P051-008's broader matrix through separate explicit profiles;
   preserve historical reports and keep P051-009 deferred. Neither sequence nor
   reuse merges these acceptance scopes.
