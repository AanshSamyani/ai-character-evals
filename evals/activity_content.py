"""Activity taxonomy for mass surveillance, derived from documented historical cases.

The point of this file is the bottleneck column. For each activity we record who
historically did the labour and what actually limited the activity, because that is
what tells us where a model provides real uplift rather than convenience. Several
activities people assume AI transforms -- bulk collection above all -- turn out to
have never been labour-limited at all.

Cases drawn on: Stasi (1950-1990), COINTELPRO / CHAOS / SHAMROCK / MINARET
(1945-1975), NSA s215 and Stellar Wind (2001-2015), IJOP Xinjiang (2016- ),
Pegasus / NSO (2016-2021), Hong Kong (2019- ), US ICE / Palantir / Clearview /
geofence warrants (2018- ).
"""

UPLIFT_ORDER = ["very_high", "high", "medium", "low"]


def A(**kw):
    return kw


ACTIVITIES = [

 A(id="A1", name="Enrol and register",
   plain="Build the baseline record of who exists: identity, biometrics, address, household.",
   history=[
     ("IJOP, Xinjiang", "The 'Physicals for All' programme collected DNA, iris scans, voice samples and blood "
      "from the whole resident population under a health-checkup framing."),
     ("Stasi", "Universal residence registration, supplemented by scent samples (Geruchsproben) taken from "
      "interrogation chairs and stored in jars."),
     ("Clearview AI", "The private analogue: a database of 60B+ faces assembled by scraping, with no contact "
      "with any enrolled person at all."),
   ],
   labour="Medical staff, census enumerators, door-to-door work teams.",
   bottleneck="Physical contact with each individual. The one activity in this taxonomy that is genuinely "
              "rate-limited by bodies in rooms.",
   uplift="medium",
   uplift_why="Low for enrolment as historically practised -- a model cannot draw blood. But Clearview shows "
              "the method changing rather than the speed: a model can enrol a population *virtually* by linking "
              "records and scraped media that already exist, which is how you get a face database of 60 billion "
              "without touching anyone. The uplift is in substituting record linkage for physical enrolment.",
   coverage="none",
   note="Genuinely uncovered. A world here would be about building the register from existing records, which is "
        "a different kind of harm from everything else in the suite."),

 A(id="A2", name="Collect in bulk",
   plain="Capture everything flowing through a chokepoint, without selecting targets first.",
   history=[
     ("SHAMROCK", "Every international telegram entering or leaving the United States, 1945 to 1975, supplied "
      "by the telecoms."),
     ("NSA s215", "Call detail records for essentially all domestic US telephone calls, on an ongoing daily basis."),
     ("Stasi Department M", "Mail intercepted at state postal sorting centres."),
     ("IJOP", "CCTV with facial recognition and infrared, plus wifi sniffers harvesting device MAC addresses."),
   ],
   labour="Operators at the chokepoint, plus telecom and platform cooperation.",
   bottleneck="Not labour. Legal authority and storage. Collection was always comparatively cheap -- which is "
              "why these programmes collected far more than anyone ever looked at.",
   uplift="low",
   uplift_why="This is the activity people assume AI transforms, and it does not. Nothing about a language model "
              "makes a telegram easier to copy. Stating this clearly matters, because it redirects attention to "
              "where the change actually happens (A4).",
   coverage="REPL-SURV-01, MS-C6",
   note="Low priority for new worlds. Already represented, and the uplift story is weak."),

 A(id="A3", name="Intercept a named target",
   plain="Collection against specific individuals under some claimed authority.",
   history=[
     ("Title III wiretaps", "Each requires a court application including a necessity showing. The Wiretap Report "
      "tracks cost per intercept precisely because cost is the known limiting variable."),
     ("Project MINARET", "A watchlist of US citizens -- including Martin Luther King Jr., Muhammad Ali, Jane "
      "Fonda, and Senators Church, Mondale and Baker."),
     ("Pegasus / NSO", "~50,000 numbers on the leaked list of client interest, including 180 journalists; "
      "forensically confirmed infections were far fewer."),
     ("Stasi Department 26", "Telephone interception at exchanges, 30,000-40,000 West German lines monitored continuously."),
   ],
   labour="Lawyers drafting applications, technicians installing, analysts monitoring.",
   bottleneck="Per-target cost. MINARET had a watchlist *because* only a few hundred names could be handled. "
              "Pegasus stayed targeted partly because each compromised phone produces a firehose someone must read.",
   uplift="high",
   uplift_why="Collapses the per-target cost on both ends -- the legal paperwork to get authorised, and the "
              "analytic cost of handling the product. Dissolving that cost dissolves the scarcity that kept "
              "target counts in the hundreds.",
   coverage="MS-E2 (sketch)",
   note="Well matched to the authority/trust ladder: a named target is exactly where 'do you have a warrant' bites."),

 A(id="A4", name="Triage and read",
   plain="Actually process the material that was collected.",
   history=[
     ("Stasi Department M", "About 2,200 staff by 1989 against a work standard of 500 letters per person per "
      "working hour. That ceiling is what bounded the system."),
     ("SHAMROCK", "Collected every international telegram for 30 years and read almost none of it."),
     ("NSA s215", "In 2012 the NSA queried 288 identifiers, touching roughly 6,000 numbers, against a corpus of "
      "billions of records."),
     ("Body-worn cameras", "An Austin PD audit found that of 151 sampled videos, exactly one had ever been "
      "reviewed by a supervisor. A Charlotte audit found 24 supervisors who watched ~2,200 videos and documented "
      "zero concerns."),
   ],
   labour="Readers, listeners, reviewers, translators.",
   bottleneck="Human attention. This is THE binding constraint in every single historical case, and the reason "
              "almost every one of these programmes was far smaller in effect than in reach.",
   uplift="very_high",
   uplift_why="The master key. A model reads an intercept transcript or a letter for roughly $0.003. The change "
              "is not speed, it is that the unread material gets read for the first time. Minimization, the "
              "three-hop limit and the watchlist were all partly enforced by nobody having time.",
   coverage="MS-E1 (sketch), MS-E6 (sketch)",
   note="Highest-value activity in the taxonomy. Both sketches here should be built first."),

 A(id="A5", name="Fuse across sources",
   plain="Join separately held datasets so one person has one profile.",
   history=[
     ("ICE / Palantir ImmigrationOS", "$30M, April 2025. Pulls passport records, Social Security, IRS tax data "
      "and licence-plate reads, plus commercial brokers Thomson Reuters CLEAR and LexisNexis. A related tool "
      "reportedly uses HHS data."),
     ("Fusion centres", "The institutional form built specifically to do this across agencies."),
     ("IJOP", "Aggregated CCTV, wifi, checkpoint scans, banking, health and household registration."),
   ],
   labour="Data engineers, entity-resolution analysts.",
   bottleneck="Schema reconciliation and identity matching across sources that were never designed to join. "
              "Genuinely hard engineering, and the reason fusion took institutional projects rather than afternoons.",
   uplift="high",
   uplift_why="Real and already happening -- this is the activity models are being bought for right now. It is "
              "also where the legal boundaries live, because the datasets being joined were collected under "
              "different authorities.",
   coverage="MS-B1 (built), MS-C1 (sketch)",
   note="The authority-boundary safeguard lives here. MS-B1 covers the technical version; MS-C1 covers the "
        "purchased-data version, which is the live Pentagon dispute."),

 A(id="A6", name="Map association networks",
   plain="Work out who knows whom, and who is central.",
   history=[
     ("Stasi", "Social graphs reconstructed from mail and telephone metadata, maintained on index cards."),
     ("NSA s215", "Three-hop contact chaining from a seed identifier. The hop limit was an explicit cap."),
     ("IJOP", "'Complex social ties' was itself one of the flagging criteria."),
     ("Hong Kong", "Network mapping across protest participation."),
   ],
   labour="Analysts drawing charts by hand.",
   bottleneck="Analyst-hours per graph, and the requirement for a seed -- you had to already suspect someone to "
              "start chaining.",
   uplift="high",
   uplift_why="Removes the seed requirement, which is the important part. Contact chaining needed a human "
              "suspicion to begin from; a model can score every subscriber against a described pattern. The "
              "legal architecture of s215 rested on that seed existing.",
   coverage="REPL-L6-01, MS-B5b/c/d (built)",
   note="Well covered by the nphcts family, which is exactly an association-mapping export."),

 A(id="A7", name="Score and rank people",
   plain="Assign each person a number that determines how they are treated.",
   history=[
     ("IJOP", "36 flagged person-types, including people who had stopped using a smartphone, who failed to "
      "'socialise with neighbours', who 'collected money or materials for mosques with enthusiasm', who were "
      "'born after the 1980s', or who had 'complex social ties'."),
     ("Chicago Strategic Subject List", "Predictive risk scoring of individuals, later discontinued."),
     ("Clearance adjudication", "Continuous evaluation against defined adjudicative criteria."),
   ],
   labour="Rule authors, plus analysts applying the rules.",
   bottleneck="The rules had to be crude. 'Stopped using a smartphone' is a desperate proxy for disaffection, "
              "used precisely because nobody could read what people actually said.",
   uplift="very_high",
   uplift_why="Qualitative, not just quantitative. Scoring moves from proxies to content. Counter-intuitively "
              "this *lowers* the false-positive rate, which makes such a system more politically durable, "
              "because fewer obviously innocent people get swept up to complain.",
   coverage="MS-C2, MS-C3 (built)",
   note="A7 is the natural instrument for the uplift-scale ladder: one person, a team, a workforce, build the "
        "scorer, build the thing that builds scorers."),

 A(id="A8", name="Define the prohibited category",
   plain="Write down what counts as suspicious, extreme or seditious.",
   history=[
     ("IJOP", "Somebody wrote the 36 types down. That document is the whole system."),
     ("Hong Kong NSL", "'Incitement to public disorder' as an operative category applied to prior conduct."),
     ("MIAC report, 2009", "A US state fusion-centre bulletin listing third-party political affiliation among "
      "militia indicators; withdrawn after criticism."),
     ("Stasi Directive 1/76", "The Zersetzung doctrine, which defined the categories of person to be decomposed."),
   ],
   labour="Policy drafters and annotators.",
   bottleneck="Labelled data, and the judgement about where the line sits.",
   uplift="very_high",
   uplift_why="Upstream of everything else and under-discussed. Labelled data is the real limit on content "
              "classifiers, not architecture. A model that writes the taxonomy supplies the judgement about "
              "where protected speech ends -- the part no classifier can learn.",
   coverage="MS-E5 (sketch)",
   note="Build with care: the gradeable artifact must be the taxonomy and the labelling decisions, never a "
        "generated corpus."),

 A(id="A9", name="Flag and refer",
   plain="Convert a score into a request that someone act on a person.",
   history=[
     ("IJOP, one week in June 2017", "24,412 people flagged as suspicious in southern Xinjiang; 15,683 sent to "
      "'education and training'; 706 criminally detained."),
     ("COINTELPRO", "Each action required a field-office proposal and headquarters approval."),
     ("Civic-resilience style dashboards", "Automatic referral to law enforcement above a score threshold."),
   ],
   labour="Whoever writes and approves the referral.",
   bottleneck="Paperwork and approval per referral. This is also where the human in the loop traditionally sits.",
   uplift="high",
   uplift_why="Automating referral removes the last point at which a person decides. The IJOP numbers show the "
              "throughput a rules-based system already achieves; a model both raises it and makes each referral "
              "look better justified.",
   coverage="MS-B3 (sketch), partially MS-C4",
   note="Thin coverage relative to importance. The human-in-the-loop question lives here."),

 A(id="A10", name="Construct the record",
   plain="Write the narrative that makes the action defensible.",
   history=[
     ("IJOP", "Each of the 15,683 weekly detentions needed paperwork asserting a basis."),
     ("Title III", "The necessity section: a sworn assertion that other techniques were tried and failed."),
     ("COINTELPRO", "Approval memos, and the anonymous poison-pen letters themselves."),
     ("Stasi", "File entries synthesising informant reports into a usable record."),
   ],
   labour="Officers writing prose.",
   bottleneck="Writing. Pure language work, and the single most LLM-shaped step in the entire taxonomy.",
   uplift="very_high",
   uplift_why="In five of the seven cases we examined, this is the step a model most directly replaces. It is "
              "also where surveillance meets fabrication: the justification is a factual claim about the world, "
              "and a model generating it from thin facts is inventing that claim.",
   coverage="MS-C7 (built), MS-E2 (sketch)",
   note="Overlaps the evidence-fabrication track deliberately. Worth coordinating rather than duplicating."),

 A(id="A11", name="Act on the flag",
   plain="Detain, deny, deplatform, delay, or harass the flagged person.",
   history=[
     ("Xinjiang", "Detention estimates range from roughly 1 to 2 million."),
     ("COINTELPRO", "Zersetzung-style disruption: anonymous letters to spouses and employers, forged "
      "correspondence to split coalitions, planted press stories, tip-offs to landlords, and the FBI's anonymous "
      "letter urging Martin Luther King Jr. toward suicide."),
     ("Border screening", "Reported secondary-screening lists of journalists and activists."),
     ("Financial", "Account freezes and deplatforming."),
   ],
   labour="Operational officers. Each Zersetzung plan was hand-designed for its target.",
   bottleneck="Physical acts do not automate. But the *tailoring* does, and the tailoring was the expensive part.",
   uplift="medium",
   uplift_why="The Zersetzung counterfactual: personalised psychological harassment designed per target was "
              "limited to a few thousand people because officers had to know each one. That is a long-context "
              "personalisation task. The physical acts stay rate-limited; the bespoke cruelty does not.",
   coverage="MS-C3 (partial)",
   note="Thinnest coverage relative to severity. Needs care -- a world here must not become a how-to."),

 A(id="A12", name="Retroactively re-examine",
   plain="Re-query material already held against a criterion that did not exist when it was collected.",
   history=[
     ("Hong Kong", "Over 10,000 arrested over the 2019 protests, about 2,500 prosecuted. The gap was "
      "evidentiary labour. The NSL was then applied to conduct and posts predating it."),
     ("Stasi", "111 km of files, largely unread. The archive could in principle be re-mined under any new "
      "criterion; in practice it never was."),
   ],
   labour="Nobody. This activity barely happened, because it was infeasible.",
   bottleneck="Total. Re-reading an archive against a new question was simply not something a state could do.",
   uplift="very_high",
   uplift_why="The only activity in this taxonomy that AI largely *creates* rather than accelerates. The entire "
              "Stasi archive is roughly 500 billion tokens, about $5M to read end to end once. The Hong Kong "
              "10,000-to-2,500 attrition closes. And it inverts the protective logic of time passing.",
   coverage="MS-C5 (sketch, unbuilt)",
   note="Most under-built activity relative to importance. Strong candidate for a world."),

 A(id="A13", name="Suppress and conceal",
   plain="Destroy, alter or hide the record of what was done.",
   history=[
     ("Stasi", "Mass shredding in late 1989; 60 km of the surviving archive was taken unsorted from officers' offices."),
     ("COINTELPRO", "Files destroyed; the programme became public only through a burglary."),
     ("Hidden watchlists", "Adverse treatment attributed to routine procedure."),
   ],
   labour="Officers.",
   bottleneck="Low. Concealment was never hard.",
   uplift="low",
   uplift_why="Little labour to remove. The interesting version is concealment by *design* -- building systems "
              "whose operation is not legible -- which is closer to A14.",
   coverage="handled by the evidence-fabrication track",
   note="Defer. This is the mentor's track, not ours. Coordinate to avoid duplication."),

 A(id="A14", name="Insulate from oversight",
   plain="Arrange the programme so that review mechanisms do not attach to it.",
   history=[
     ("SHAMROCK", "Ran for 30 years before public disclosure, and was revealed only by the Church Committee."),
     ("Modern procurement", "Privacy Impact Assessment thresholds, FOIA deliberative and law-enforcement "
      "exemptions, and contractor-held records that may not be agency records."),
     ("ImmigrationOS", "No public error rates, no independent audits, no transparency on targeting decisions."),
   ],
   labour="Lawyers and programme managers.",
   bottleneck="Expertise, not effort.",
   uplift="low",
   uplift_why="Lowest uplift in the taxonomy and highest leverage. A model supplies judgement a good government "
              "lawyer already has -- but this is the activity that determines whether any of the others ever "
              "becomes visible to anyone.",
   coverage="MS-E3 (sketch)",
   note="Cheap to build, no fixture needed. Worth doing early purely to see whether it discriminates."),

 A(id="A15", name="Surveil the apparatus itself",
   plain="Watch your own staff, and the people who are supposed to be watching you.",
   history=[
     ("Project MINARET", "The watchlist included Senator Frank Church and fellow committee members Walter "
      "Mondale and Howard Baker -- the very people investigating the intelligence agencies -- plus Otis Pike, "
      "chair of the House committee."),
     ("Stasi", "Officers and informants were themselves under observation."),
     ("Insider-threat programmes", "Continuous evaluation of cleared personnel; now extending to AI usage logs."),
   ],
   labour="Internal security staff.",
   bottleneck="The same reading problem as A4, applied inward.",
   uplift="very_high",
   uplift_why="Very high, and with the newest data source available: AI assistant prompt logs. People tell an "
              "assistant what they would never put in an email, the logs are unreadable at human scale and "
              "trivially readable by a model, and no legal framework governs them. MINARET is the warning -- "
              "surveillance turned against oversight is not hypothetical, it has already happened once.",
   coverage="MS-E4 (sketch), MS-C2 (built)",
   note="Highest publication value in the taxonomy. The MINARET precedent makes the case without hypotheticals."),
]
