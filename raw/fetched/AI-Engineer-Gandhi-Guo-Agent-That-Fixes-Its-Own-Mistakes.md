---
title: An Agent That Fixes Its Own Mistakes — Saloni Gandhi & Ziwei Guo, LinkedIn
description: AI Engineer 官方閱讀版，LinkedIn 以 judge、反思與 GEPA 迴圈改進使用者理解 agent 的 prompt，附官方機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/yH7_SIIgI-Y-agent-that-fixes-its-own-mistakes
published: 2026-11-10
tags:
  - clippings
  - ai-agent
  - evaluation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript 下載端點 JSON，僅把連續片段每 12 段合併並標上起始時間，文字未改；原文含辨識錯誤，如 LinkedIn 被辨識成 linking、GEPA 被辨識成 JPA／Japa、Ziwei 被辨識成 Zui）。對應 YouTube 影片 ID `yH7_SIIgI-Y`（`https://www.youtube.com/watch?v=yH7_SIIgI-Y`，2026-11-10 上傳，約 38 分 50 秒）。

Loading slides…

At a glance

### Ideas worth remembering

- Checking the titles an agent returned tests plausibility. Checking those titles against the member’s intent signals can also reveal a preference the agent omitted.
- A diagnostic judge needs a way to identify an incorrect score and evidence against which to check it. LinkedIn’s reflection agent sometimes blamed a sound rubric or repeated the first judge’s error.
- LinkedIn compared proposed prompt edits under a common rubric, tested the selected change on held-out examples and kept people involved in the production decision. The first GEPA-optimized pull request passed measurement and human review before release.

01 [0:01 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1s)

### Which part of the agent should a production failure change?

A production trace records what LinkedIn’s career agent did on a real request. When something goes wrong, the engineers maintaining the agent still have to decide what to change. Ziwei Guo and Saloni Gandhi built a system around one part of the career experience, the agent that infers a member’s goals and preferences. Their starting point was an evaluator that could inspect the traces and identify failures that mattered to members.

The team calls the process recursive self-improvement, or RSI. The agent logs its output and the steps that produced it. An improvement engine uses those records to evaluate the output, investigate the cause of a failure and propose an edit. Once a validated edit enters production, the revised agent produces the traces for a later round.

Several parts of the agent harness, the software around the base model, can influence an answer. Planning logic chooses an execution path. Context and memory preserve session state. Tool interfaces give the agent access to APIs and datasets, and storage retains outputs and generation logs. The team chose prompt edits as the simplest changes to propose and test while keeping the base model fixed.

Guo describes a progression in what the optimizer might eventually be allowed to edit. It could change how the agent’s context is structured, design the workflow, then modify the harness code that runs it. The most ambitious step would let the optimizer revise its own code. The production work in this talk tackles the first step, changing the instructions.

[0:15](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=15s) [0:42](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=42s)

02 [5:09 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=309s)

### How an edit earns its place in the next run

One iteration has seven steps. The first two produce evidence. Run the agent on a query, keeping its output and execution trace. Then have a judge evaluate the run and explain where the output succeeded or fell short.

Steps three and four turn a judgment into a proposed edit. A reflection agent investigates what could account for the score. Possibilities include a model error, a prompt that left something out, a tool problem or a mistake in evaluation. The diagnosis guides the proposal. This matters even when the only edit the optimizer can make is to a prompt. A low score by itself gives it little reason to change a particular instruction.

The last three steps test the proposal. The system evaluates candidates using the same judge and rubric, incorporates a promising edit into the prompt, then compares the revised agent with the previous version on a held-out set. That final comparison asks whether the change also helps on examples outside those used to choose it. A validated update becomes the baseline for the next iteration.

[5:17](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=317s) [5:23](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=323s)

03 [9:20 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=560s)

### From a member ID to an inferred job preference

The user-understanding agent takes a member ID. It fetches profile data, search history, location and preferences, then synthesizes those signals into fields describing the member. One field records which job titles the person appears to prefer. Entries might include *network manager* or *account manager*. What would let a reviewer check that inference?

Alongside the titles, the agent supplies its confidence, citations to member evidence and an explanation. If *network manager* appears frequently in saved searches, a citation can point to the activity behind that inference. The explanation can distinguish the roles of two sources of evidence. A preference the member stated can establish the primary title, while saved searches can support a related title the member might also consider.

The first-level judge, L1, assesses the output across 15 task dimensions using product-defined rubrics. One member’s output received an overall score of 2.31. Underneath it, fields such as goal summary and preferred job title each get a score and notes explaining the verdict. On this scale, 1 means poor, 2 fair and 3 very good. The field-level notes give the next stage a specific claim to investigate when an otherwise reasonable output scores poorly.

[9:35](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=575s) [9:46](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=586s)

04 [13:57 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=837s)

### Counting recurring problems across different members

Reflection starts by grouping failing rows from members’ traces according to the dimension that scored poorly. This first grouping just uses the existing scores. Within each group, a second-level judge, L2, examines each row and assigns a free-text diagnosis and a cause tag. A shared symptom, such as a low score for preferred titles, can have different causes across members.

Free text creates a counting problem. One diagnosis says the member’s profile data is missing. Another says the profile gives an incomplete picture of the member’s browsing history. In Guo’s example, both identify a problem at the same level of detail for the team’s purposes. The available profile evidence cannot support the agent’s conclusion. Merging these descriptions under a common issue label makes their combined frequency visible. Ranking the labels then requires no further model judgment.

Who uses the diagnoses after a run? Engineers get a scorecard showing which problems recur most often. L2 gets something different on a later run. The system saves prior diagnoses and supplies them as context when L2 investigates fresh failures.

### Where a row’s diagnosis goes

<svg width="541" height="676" aria-hidden="true"><defs><marker id="_R_3faajalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 246.625 119 L 246.625 158 L 246.625 197" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="246.625" y="154" text-anchor="middle"><tspan x="246.625" dy="0">Pass each row for</tspan> <tspan x="246.625" dy="16">diagnosis</tspan></text></g> <g><path d="M 305.2083333333333 308 L 346.375 347 L 346.375 386" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="346.375" y="343" text-anchor="middle"><tspan x="346.375" dy="0">Collect near-duplicate</tspan> <tspan x="346.375" dy="16">diagnoses</tspan></text></g> <g><path d="M 389.46617647058827 478 L 426 517 L 426 556" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="426" y="513" text-anchor="middle"><tspan x="426" dy="0">Count occurrences of</tspan> <tspan x="426" dy="16">each issue</tspan></text></g> <g><path d="M 284.1397058823529 478 L 231.375 517 L 179.925 566" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="231.375" y="513" text-anchor="middle"><tspan x="231.375" dy="0">Retain the identified</tspan> <tspan x="231.375" dy="16">causes</tspan></text></g> <g><path d="M 110.2592105263158 566 L 87.5 517 L 87.5 432 L 87.5 347 L 153.17063492063494 308" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="87.5" y="428" text-anchor="middle"><tspan x="87.5" dy="0">Supply prior diagnoses</tspan> <tspan x="87.5" dy="16">on a later run</tspan></text></g></svg>

**Failing rows** Group traces by the dimension that scored poorly.

**L2 diagnosis** Assign each row a cause tag and a free-text explanation.

**Common issue labels** Merge descriptions of the same underlying problem.

**Scorecard for engineers** Rank recurring issues by frequency.

**Saved root causes** Keep diagnoses available for future investigations.

The scorecard counts issues across members in this run. The return path carries prior diagnoses into a later run, when L2 has new rows to examine.

Read the diagram as text
- **Failing rows.** Group traces by the dimension that scored poorly.
- **L2 diagnosis.** Assign each row a cause tag and a free-text explanation.
- **Common issue labels.** Merge descriptions of the same underlying problem.
- **Scorecard for engineers.** Rank recurring issues by frequency.
- **Saved root causes.** Keep diagnoses available for future investigations.
- Failing rows → L2 diagnosis: Pass each row for diagnosis.
- L2 diagnosis → Common issue labels: Collect near-duplicate diagnoses.
- Common issue labels → Scorecard for engineers: Count occurrences of each issue.
- Common issue labels → Saved root causes: Retain the identified causes.
- Saved root causes → L2 diagnosis: Supply prior diagnoses on a later run.

[14:33](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=873s) [14:36](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=876s)

05 [18:37 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1117s)

### The first GEPA-optimized prompt reaches production

![Two panels report that the first RSI-generated changes reached production after human review and quantitative measurement, and that human annotation helped improve the evaluation judge and rubric and reduce evaluation variance.](https://ai.engineer/api/talk-essay-media/a57e018dfd148b6cdba801daaa51a836f0436defdccddcf56e57d519f37c9ef3)

The first production changes were paired with a study of how the evaluator’s judgments compared with human review.

GEPA uses the judge’s evidence and the reflection results to propose changes to the agent’s instructions. It works over mini-batches of sampled traces. Candidate prompts advance to validation, where the team can compare how well they address the observed problems. A prompt that survives the held-out comparison can replace the previous production baseline.

The team used human annotations to improve both L1 and L2 and studied variation across agent runs and model judgments. Meanwhile, engineers packaged the seven steps into a workflow that could suggest edits weekly, every two weeks or monthly, depending on need. Scheduling proposals left the release decision with people. The first GEPA-optimized pull request shipped after quantitative measurement and human review.

Gandhi describes a second outcome from comparing the evaluators’ decisions with human reviews. Disagreements exposed recurring faults in both the scoring rules and the system that explained failures. That raised two separate questions. Could L1 recognize a poor answer? And when L1 flagged one, could L2 identify what had gone wrong?

[19:09](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1149s) [19:12](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1152s)

06 [25:12 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1512s)

### Human reviewers agreed most often with a score of 3

Where was L1 reliable enough to guide an edit? The team analyzed about 180–200 human reviews, grouping them first by the score L1 had assigned. Full agreement was roughly 55% for outputs scored 1, 57% for those scored 2 and 80% for those scored 3. The judge recognized strong work more reliably than it distinguished degrees of weak work. Those low scores were precisely the ones that sent examples into reflection. [Score agreement in the recording, 25:31](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1531s)

Grouping the reviews by field reveals a different source of disagreement. Preferred job titles had among the weakest agreement. For domain or area of expertise, agreement was about 47%, and for work type it was about 50%. The two breakdowns point to different questions for the rubric. What distinguishes a 1 from a 2? What evidence should count for this particular field?

The annotations put concrete cases behind those figures.

- **Preferred titles.** L1 could accept a plausible title even when the agent had overlooked an important signal of the member’s intent. A reviewer checking the input could spot a missing preference that a check of the returned titles alone would miss.
- **Fields of expertise.** In the team’s example, *software engineering* is a domain, *machine learning engineer* is a role and *machine learning* is a skill. The rubric blurred those categories. It also gave little guidance on how much credit to award when an answer mixed correct and incorrect entries.
- **Formatting and inference.** The judge sometimes penalized harmless differences in how a value was written. A harder disagreement arose when the agent inferred a preference from current employment and the member had never stated that preference explicitly. Reviewers needed a rule for when that inference was justified.

Of the 37 judgments reviewers identified as too harsh, 31 involved an output L1 had scored 1. That concentration made partial credit a practical priority. A rule for recognizing the correct parts of a mixed answer could keep that answer from being treated as a complete failure.

07 [28:31 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1711s)

### When the scoring rule is wrong, and when the judge is wrong

![Bullets describe missed job-title preferences, inconsistent partial credit for expertise, formatting penalties and disputes over inferred preferences. Of 37 judgments reviewers marked too harsh, 31 received score 1. The slide calls for clearer rules for partial credit and inferred evidence.](https://ai.engineer/api/talk-essay-media/86dd45128618494ec7ee6fe23d80579a98e8c9a69cc8ed7118f55d2f0272e5a9)

The review breaks disagreements down by score and failure mode, including overly harsh judgments and gaps in the rubric.

Take the work-type value *full-time*. Capitalization alone could cost the agent credit. The revised rubric accepted formatting variants with the same meaning. The team also added guidance for normalizing job titles, handling concurrent employment and assessing inferences about seniority and geography. It revised the scoring rules to distinguish a poor answer from a partially correct one.

After the rubric changes, reported L1 agreement with human reviewers rose from about 57% to 64%. Mean error also fell, though the scale of that measure was unspecified. The agreement gain measures a change in the evaluator. Engineers had made the product’s definition of a correct judgment more explicit.

Reviewing L2 exposed a different problem. Human reviewers agreed more often when L2 attributed a failure to the underlying model. Agreement was much lower when it blamed the rubric. The original list of cause tags gave L2 no way to say that L1 had made a mistake. Faced with a reasonable rule that L1 had applied incorrectly, L2 sometimes labeled the rule itself defective.

L2 also sometimes repeated L1’s rationale without checking it against the agent’s output. A single mistaken judgment could then look like a finding that two evaluators agreed on. If GEPA acted on that diagnosis, it could propose an edit to a component that had behaved correctly. Improving L2’s ability to identify the cause became a priority in its own right.

For decisions about individual edits, the team used majority voting to reduce the influence of any one model judgment and held-out evaluations to check whether gains carried over. Gandhi also reports an improvement involving the threshold for adopting an edit and the reported confidence interval, without specifying a value or direction of change for either measure.

[28:42](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1722s) [28:46](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1726s)

08 [33:03 ↗](https://www.youtube.com/watch?v=yH7_SIIgI-Y&t=1983s)

### What another agent team would need

At the scale of a team, adoption poses a different question. What fraction of its prompt changes can RSI reliably generate and validate? LinkedIn also wants to measure downstream response quality and the time engineers save maintaining an agent. These are proposed measures for broader use. A count of edits would rise even if the quality of the answers stayed flat.

Many teams already have an agent that answers questions, summarizes material or completes a workflow. Their ability to evaluate it varies. Some have bespoke tests, others inspect outputs by hand, and relatively few have a reliable evaluation they can run repeatedly. That gap limits what a shared optimizer could do for them. To propose a targeted fix, it needs a diagnosis. To investigate the cause, the diagnostic system needs a dependable way to identify a failure in the first place.

LinkedIn’s proposed shared infrastructure would give teams five capabilities.

- **Evaluation.** Reuse evaluation frameworks and metrics, with judges that teams can calibrate against human feedback.
- **Feedback collection.** Collect execution traces continuously so recurring failures can be detected and investigated.
- **Optimization.** Use reflection and prompt optimization to generate and test candidate changes in a repeatable way.
- **Validation.** Compare candidates on held-out examples and run regression tests for behavior an edit might damage.
- **Self-service adoption.** Package the components so a team with an existing agent can use them without building the whole pipeline.

Gandhi frames the longer-term goal in terms of a slope. The target agent infers member preferences. The improvement engine finds failures, investigates them and tests changes. If agent quality is a function of time, an individual release can raise quality at one point on the curve. The ambition for the engine is to increase the rate of improvement across releases. For that slope to mean anything, the team has to be able to trust that a measured gain reflects a better answer for the member.

[Transcript download](https://ai.engineer/api/data/transcript?slug=youtube-6551b711b64e35c5656e&format=json)

Full transcript

## 官方機器逐字稿

[0:01] Uh hello everyone. Uh so my name is uh Zui and today uh together with uh Saloni so we are going to present the recursive self-improvement uh project that we are doing at linking and for this RSI work we focus on the user understanding and yeah super excited to share the uh RSI work we did at linking. So first uh just a high level or overview on what is a recursive self-improvement. So the recursive self-improvement is a build around some uh AI system and uh

[0:34] this is the purpose of doing this is we want to get a system that self-improvements uh self-improves. So it can learns from issues in production trace and that work. So the AI system can be some uh agent and I linking. So one example is uh our career uh agent to help uh our uh linking users members to achieve their career goals and from the agent so uh and there's uh many daily development work that we discover the issues we want to address and also we

[1:09] will get the production traces and that we can uh so they like we can log the issues we found during the production traffic and once we have this informations So we will have some evaluation engine for example the ar judge and to uh check our uh traces and to identify the issues and gives feedbacks and based on the feedbacks and we will uh use those feedback to keep uh continuously uh iterate our system. So we build this kind of like a loop to

[1:41] keep uh improve our um AI system. And uh one key thing we want to uh call out is uh during this uh recursive self improvement process the evaluation is very critical and it must be objective and well aligned with the user feedback because this is a key to uh like identify where the bottleneck is and guide the next step for the uh system AI system improvement. And uh next we want to uh uh like describe like show uh what kind of like

[2:12] uh which component of the AI system we can uh optimize. Uh so here take the harness uh as as an example or like as orchestrator. So there are different components we can uh use we can uh optimize by using the RSI. So for example the first is a planning and logics which is used to orchestrator orchestrates execution and make a decision uh past and the second is a context and the memory where we preserve and manage the session state and the

[2:44] third one is a two interface that interacts with external and internal APIs and data sets. The last uh last but not least is artifact storage uh that where we stores outputs and the generation logs and so they like uh and we are on top of those we definitely have some like evaluation uh logic and uh so that to help us to evaluate uh each um component and help us to keep uh improve the uh AI system and we want to uh like uh uh and another thing to uh

[3:16] keep in mind that all those uh like harness is a powered by the base uh iron model but for the RSI uh so it's currently the optimize of this base model uh itself is not in uh scope but we focus on the uh harness optimization uh first and uh here we want to uh like show uh like this is the ladders that we can climb to optimize the uh AI system by using the uh RSI. So uh at the beginning so typically so this is a start from

[3:52] simple uh process at the beginning we can focus on the prompts uh updates because this is a most uh this is the easiest and the most straightforward way to uh keep iterate our AI system and after that uh we can uh continue to optimize the structured context of the AI system and uh uh the and the for the this is the L1 uh ladder and for the L2 tool ladder and which is after the structure context optimization. We can uh expand our scope to design the auto

[4:26] automatically design the entire uh workflow and uh uh so this is kind of like uh like a meta information uh design and uh after that and we can automize the harness code uh itself and as at the end we can uh go very compactly to optimize the optimizer code uh itself. So this is kind of the different optimization ladders uh with increasing complexity and uh uh for our project. So currently uh our active focus is a prompt uh optimization but uh

[5:01] uh definitely like moving forward we are extend our scope to uh more and more complicated uh optimization uh in future and uh here we want to show our uh uh RSI uh strategy. So we break down our uh RSI uh uh process uh into seven uh steps. So the first step is to uh run the agent and uh generate some uh samples. So basically like for our career agent uh that we are optimizing for. So given a query we'll generate some uh output and we will lock those uh

[5:37] process in the uh traces for example the last miss traces and uh once so this is basically just the uh like the uh kind of the agent uh trajectories and the traces that we can uh uh use to uh optimize and once we got those information the next step step two is we uh runs through the evation uh engine for example the judge and to uh get some judge uh output to tell us uh where we are uh good at and we are where we are not good at. So to get the uh uh future

[6:11] iteration and then uh once we get the uh um judge output then we go uh we we are going to the RSI components and uh starting from the uh step three. So this is a kind of the RSI in the inside the RSI loop and the first step is we will uh we will do the agent reflection uh sometime we also call it a root causing so they like based on the judge uh output we want to understand what is a root cause uh that we don't have a good uh output for example is this is a agent

[6:45] issue a model issue u prompt issue or like a two uh two two issue or some other issues or sometimes it's Even it can even be a judge issue or rubric issue. And uh once we got the root cause and uh uh we will uh the next step is to uh based on the root cause uh we identified we want uh we can generate some uh addits proposal. So uh currently the addits proposal are just uh prompt but as we are climbing the climbing the ladder uh for the SI loop. So in future

[7:19] this uh additis can also be some like a new design of the workflow the harness code or even the optimizer optimizer code and uh uh so yeah that's uh step four to generate the edits proposal and the next step is to uh validate our edits because uh some edits can be uh good some can be bad uh so we will use the same uh evaluation engine for example the same judge with the same rubrics to uh to uh evaluate uh our addit validation and uh uh once we found

[7:54] some like a good candidates and we will uh naturally the next step is to uh evolve our uh prompt to adapt the uh the uh the proposed edits uh we have and uh uh once we uh once the prompt is uh updated. So the very last step which is a step seven here is we run the evaluation uh again on a hold up side and to confirm uh our uh this kind of the uh new system is indeed performs better uh than the old system after the SI optimization and uh uh this will and

[8:30] also like uh after this hold out validation uh like we will make the uh prompt updates and this will become our uh new baseline and uh and we are uh in future we will like continue to do this uh RSI uh iteration to keep improving uh our system uh with some uh cadence. Uh okay. Yeah. Next uh like uh we are we can uh like dig deeper into uh each step so that we can get uh so so to help you to understand more details on what we are uh doing here. for example, what is

[9:05] the agent we are optimizing and what is like a steps uh like a detail steps uh in each uh this high level steps to uh help us uh to help you to understand more of of our uh SI work here. So the first step I I want to show uh so this is the first uh the step we generated the output and the generated trace and uh so first we want to I want to uh help you to understand the agent uh we are optimizing here. So this is a uh user uh understanding uh agent uh at linking. So

[9:39] uh so like you can see we uh in this slide we are showing the input and the output of this uh agent. So the input is just a simply member ID also it's just a user ID and uh uh by uh given user ID we can fetch uh some information uh of this user for example this user search history uh profile data uh and also some like a location data and the preference data those kind of things and we have this user understanding agent to uh like take those users uh history or behavior

[10:12] data profile data as a input and uh do the uh do a lot like this kind of um uh agentic uh synthesize steps and we generate the uh output. So for this output we call it is a uh memor sending or the user understanding uh output. So here is a high level uh structure of the uh this output is so given a member. So we will generate some uh fields to describe uh this uh member based on our agent understanding. For example, what is the preferred uh job title uh of this

[10:46] member? This is just one uh field of this uh this user understanding uh output. So for this one, this is just a example of the preferred job titles. So it can be some like a network manager, account manager those kind of things and we'll give a confidence on like how confidence this uh agent think uh like this is indeed the preferred job titles for this user and uh also uh we'll get uh generate some uh citation data. So they like this is the uh like why the

[11:18] this is where we can tell why the agent think those uh titles is a preferred job title for this particular uh member. Uh for example it could be uh the reason could be like uh in the users uh save the search history like those job titles uh appears very frequently. So the agent think oh this is a strong evidence uh that to support that the preferred job title is a network uh manager uh for this uh for this uh user and uh uh as a uh and uh finally this agent can also

[11:52] output the reasoning on like why like just a reasoning like why the agent think those are preferred job titles like for example the state preference anchors the primary title save search agent uh adjacent one those kind of So this is a kind of uh uh one example of the user understanding agent that we are optimizing. So the step two is once we uh got this uh agents trace and we'll run the judge and to uh get a quality readings of this

[12:26] uh of the agent uh output and uh for this particular user agent uh the score is over uh 15 uh task of the dimensions by judge where are some um product uh defender uh rubrics. So here is one example of the uh judge uh output. So you can say for particular um member the user and we will generate a judge uh score which is 2.31 and uh we will show and it will also tell like this score is for uh which um and [clears throat] it'll show the breakdowns uh of the you

[13:01] know the each dimensions score for example the go summary dimensions and we also have some other dimension for the the second one is a prefer job title dimensions and for each this kind of dimensions we give a detailed uh score uh for each dimension and also the notes. So the notes is uh just the rationale also the uh vertx like why uh we give this score uh to this uh to this particular uh dimension and for this particular uh judge is the agent. So the

[13:34] uh judge score is one to three uh scale. So the score one means uh this is not a high uh good is not a good yeah the quality is not good and the two is a fair uh quality and the three means this is a very good quality. Yeah. And uh uh so yeah that's our uh um judge and uh after we got the judge score uh for each dimension of our user understanding agent and the next step is we will run this uh agent reflection process. So as we mentioned earlier so this is a kind

[14:11] of uh uh process for us to understand okay if this is a low score then what is the root cause uh lead to the uh this low score. So uh this is a so for this uh step three so actually uh internally there are four uh like we can call it a mini steps for the agent reflection. So the first step is a clustering. So we are group the failing uh rows because like in a production trace so we are we will have a lot of like uh examples a lot of users and we will group uh the

[14:48] those users also the traces by the failing uh dimension. So for this uh step so this is just a pure clustering uh without uh any um cost and uh once we get the clustering and uh uh so the next step is we call it L2 uh judge so b within each uh class. So we are run the um uh cause to diagnose uh each row and uh and then for each row we are assign a root cause and plus tag. So b like this is a u uh place that we uh can like rely on the to uh let us know uh uh if we

[15:31] think uh this is a for example this dimension has a low score is that due to the prompt issue uh agent issue harness issue code issue or like even the judge issue or rubric issue. So they will be covered by the root cause and tag uh here. So uh the then once we get the perole level root cause and the tag so the next step is to merge the uh issues because uh in the second step uh so we it's just a we is based right so so the root cost is more like the free tax but

[16:08] uh uh some root cause uh even the tax is not um uh exactly the same but they may just describe very similar thing or uh so that's why like we want to do this kind of uh dduping so we merge the issues if we think uh the root cause is uh near uh duplicates so uh I can give one example here so for example uh for one row for one member uh the root cause can be uh the members uh profile data is uh missing uh and another row uh uh so the arm can

[16:47] the profile data is uh not showing the full picture of this users uh like a browsing history or whatever. So b like they are uh both of them are describing the same thing. So the profile data is not supporting the uh this agent output. So uh but they just use a different text. So that's we are like that's why we need this um kind like a dduplication uh step to merge the similar issues so we can get some uh canonical uh issue I say the roo uh labels

[17:21] and uh once we finish the step three so the next step is to based on the uh canonical issues we found we are group and rank them by the uh frequency and uh this step uh there's no am required so this is just to help us to understand uh what is the major issues bottlenecks uh in our uh AI system and uh once we uh do the group and ranking and we are generated the uh scorec card for the human to uh get uh to just uh get a human to act on to uh

[17:56] continue uh iterate our uh AI system and all uh and also we are uh uh like basically just a cache I say save those root cause uh somewhere and it will continue use this for the self question loop. So that's why so you can see uh like there's a arrow here like a go back to the uh L2 judge. So be like it will guide us on like what is basically the pri prior diagnose prime on the next turn. Uh so that is easier for the uh like to judge to identify the issues uh

[18:30] in future runs. So that's uh uh like the what we do for the agent uh reflection. Uh so the next step is a generator edits proposal because from the step three uh the previous slide we know uh we already know okay so what is the root cause right why like the agent fails so the next step is naturally like given uh those root cause those issues we want to fix so what what can we do right what is u new edits we want to propose and uh here like

[19:04] we have uh again like this kind of we call it the proposal uh life cycle. So based on the judge uh evidence and the reflection artifact we will propose the input and uh we will run uh some methodology. So uh for this project uh we are using the uh JPA to uh given the uh you know the uh lookout and to uh propose the new prompt change and uh and like given a trace sample we do it in a mini batch uh fashion and uh and generated the new uh prompt updates

[19:40] proposal and once we generate the promp uh updates proposal we'll uh select the window prompts and do the uh validation validation uh set and uh once we uh found a good prompt candidates and we run the uh you know the validation set and we think uh it is uh become uh it is a good uh prompt updates and uh we are just um updates our prompt in our system. So this will be and into the production and this will become our new uh kind of like a

[20:15] baseline and we will continue to uh do the uh like the future uh RSI uh iterations. So yeah that's uh kind of like the and uh yeah that's a kind of like the entire life cycle of this RSI uh iteration. And uh next this slide uh we want to show our primary focus for this RSI work. So we so currently we have three major focuses. So the first is the quality, second is automation and the third is a production uh updates. So quality uh like we are focused on the

[20:50] different uh uh things uh on the quality. So um and we uh did many uh iterations to trying to improve the uh quality of our agent uh judge and this RSI loop. For example, we did extensive human annotations so that we can improve the judge both the L1 judge and the L2 judge uh quality and we did uh many study and analysis on assess agent judge uh uh variance so that we can uh make sure we can kind of mitigate the impact from the non nondeterministic nature of

[21:27] the LM and uh uh the third one is we push quality updates to both Asian judge and RSI reflection uh based on our annotation and the variance analysis uh mentioned uh above. So that's on the CI side and the second focus is uh automation uh because as we mentioned so there are seven steps in the RSI iteration and uh so that's why like here like I we build a uh this kind like workflow so that we can kick off this workflow with some uh cadence for weekly

[22:03] or bi-weekly or monthly based on the needs uh so that it can u automatically running and keep suggesting the uh like the prompt updates uh with some uh cadence and the third focus is production uh updates. So definitely like we want to uh build a uh useful uh RSI uh system that can help uh keep continuously uh improve our uh you know product. So that's why like we the third focus uh for the our our uh work is to make updates to the current agent in

[22:37] production with human in the loop uh like for now to uh ensure like the production uh uh quality uh is there but later like once we think uh the quality is good enough like we gradually uh uh like reduce the human effort and uh and hopefully we can achieve a higher automation uh kind of uh state. Uh cool. Yeah. Next, I will hand over uh to Saloni to uh share more details about the outcomes and uh learnings of our our work.

[23:16] I will share my screen. Sure. Yeah. Um, can you see my screen? Yeah. Yeah. Yeah. Um, so yeah. Hi, I'm Salon. And so far we described how the RSI system is designed. Uh, but one of the most interesting aspects of this work has been understanding what happens when we actually try to make this process reliable. And in particular, we learned that the quality of the evaluator is

[23:52] just as important as the quality of the optimization system. So let's walk through some of those um findings. Um so there are two major outcomes we want to highlight. So the first is that we successfully like deployed our initial RSI improvements into uh production which was like um landing a first PR which was optimized by Japa and through the loop which we just described. Um so these changes went through human review and quantitative measurement before

[24:19] deployment and it was an important milestone in moving RSI like beyond just an experimental workflow. The second major improvement was around like um evaluation quality where we invested substantial effort and like human annotations for the user understanding judge and as well as like analyzing where its judgment sort of like disagreed with like human reviewers. And this process revealed several recurring weaknesses in both our evaluation

[24:45] rubrics as well as our like our reflection system. And by investigating those disagreements, we were able to like make targeted improvements which further strengthen the reliability as well as like reduce the evaluation variance which we have. And uh before we could trust a system to like improve an agent automatically, we had to understand whether the feedback driving those improvements was also itself trustworthy. And this was like a major

[25:09] area of our engineering work. Um to so to understand the quality of our like um L1 which was our evaluation judge. We analyzed about 180 to 200 human reviews. We were particularly interested in how the judge agreed with human reviewers both across different score categories and across the individual evaluation dimensions. Starting with the chart on the left, we see basically that um for outputs we assigned a score of like one um a full judgment alignment was

[25:38] approximately 55% and for score two it was around 57%. But for score three the alignment increased to approximately like 80%. Which indicates an interesting pattern which was that the judge was considerably like better at recognizing stronger outputs than it was at like distinguishing between different sort of like weaker outputs. And we found that many of its uh lowest scores were like also overly harsh. And um now looking at the chart on right agreement also varied

[26:08] significantly across like different dimensions where higher preferred dimensions like titles had like the weakest observed alignment as well as like uh domains or like the expertise or area of work was around like 47% and the sort of like work type was around 50%. which told us like the evaluation quality was uniform across all the tasks which we cared about and certain dimensions required more clearer definitions better evidence handling

[26:35] rules as well as like more explicit scoring guidance. Um so when we look more closely at the human annotations several recurring patterns emerged. the first involved like using job titles. We found cases where the judge would accept like a return title because it was plausible would but would miss the fact that the agent had omitted an expected um signal or like an ignored and basically an ignored and important intent signal. Um

[27:02] in other words, sometimes the judge was sometimes evaluating the plausibility rather than the completeness of the facts which were stated. Uh the second issue was primarily around primarily around the fields of expertise. Here the distinction between like a domain, function and a skill wasn't like always clear where um a domain could be like um say software engineering and a function or a role could be like for example a machine learning engineer while skill

[27:27] being uh machine learning. Um the rubric also like lack consistent partial credit rules for output containing like a mixture of like correct and incorrect information. And another issue was involving around formatting and inference. So in some cases the judge penalized harmless formatting differences. In other words, uh it made it inconsistent assumptions about what could be inferred from like a member's existing employment information too. We

[27:53] also examined like the distribution of overly harsh judgments. Out of like the 37 um judgments identified as too harsh, 31 of them involved outputs that had been assigned a score of one, which suggested that the boundaries between our scores needed to be like recalibrated. Um, another recurring source of disagreement was whether an inferred member's preference should be considered valid when the evidence wasn't like

[28:18] explicitly stated. And the broader lesson here was that many evaluation disagreements were not simply like model periods. They were reflecting ambiguities in the rubric as well as like the underlying evaluation policy. Um, based on these findings, we introduced several targeted improvements to our evaluation rubrics. One was like basically fixing harmless formatting differences. Um, previously like a value such as like you know full-time could

[28:44] receive an incorrect score because of like capitalization or incorrect formatting. We updated the rubrics so that these differences would not be treated as like semantic failures. Similarly, we introduced normalization guidance for like titles. Um we also clarified how the judge should handle concurrent employment like you know sort of impairing seniority as well as like impairing geographic references of the user and more broadly we recalibrated

[29:09] the rules uh separating low scores from like partially correct outputs and these changes resulted like resulted in like measurable improvements uh where human alignment increased from like 57% to like 64% and um at the same time the mean error decreased from like 96 to 74 What we're trying to achieve here is to get our system as high or like as highly aligning to humans as much as possible. And what we find particularly

[29:35] interesting here is that we didn't achieve these improvements by only like handling the model, but we also improved specifications of what like the correct evaluation should look like. That is like rubric design as well as like um evidences which our evaluator is like spitting out. Um moving forward uh we perform like a similar human review analysis for our reflection agent which was described earlier in our pipeline. We should

[30:00] recall that our L2 takes an evaluation failure and then it tries to identify the root cause. For example, it basically identifies was the problem caused by the agent itself by the evaluation rubric or by some other issue with the available context. What we discovered was that root cause attribution was substantially harder than like simply identifying a failure. Human reviewers agreed more often when L2 attributed a problem to like the

[30:27] underlying model, but agreement was much lower for other causes, particularly like rubric related issues. Um, one important issue was that our original reflection taxonomy didn't include a way to explicitly say that or Elvin judge could have been wrong. Um, as a result, sometimes the reflection agent fell back to blaming the rubric even when the real problem was like an incorrect um, L1 judgment. Um, and like another issue was like the uh, reflection agent sometimes

[30:56] used the L1 judge's rationale without like independently validating or independently thinking over it against the agents output. And um we exposed an important risk here which was like a reflection system can produce convincing explanations while still like identifying misidentifying like the underlying problem and if we use those explanations to generate prompt changes we could like end up modifying like the wrong component of the system. So

[31:21] improving the L2 uh like reflection chart like became our next priority. Um so to talk about some of the quality improvements um these findings led us to like focus on improving both layers of evaluation. At L1 the goal was to make sure that the scoring was more accurate and more better aligned with human judgment. And at L2 the goal was to improve the reliability of the root cause diagnosis. And um the next this slide basically

[31:53] summarizes some of like the changes we made to the system and the impact that we observed. We introduced like several targeted changes to address the um the reflection failures um identified through like human review and um we we were basically like trying to measure the impact here in terms of like how do we translate all this evaluation and reflection work into like measurable impact. So there are two levels to

[32:19] consider here. The first is like improving the reliability of the RSI process itself. So by improving L1 we make the um evaluation scores more stable and like more better aligned with human expectations and by improving L2 we increase like the uh like the root cause diagnosis as we mentioned earlier. So we also use like majority voting sort of and like held out evaluations to like help mitigate um variance from like individual uh LLM judgments and together

[32:49] these improvements support like a more reliable optimization process. Um importantly like one of the observed improvement here was about the required adoption threshold and the reported confidence interval as well. Uh the second level of impact is where we want to measure the RSI where the RSI adoption grows. This includes the percentage of like agent prompt changes that can reliably be generated and validated through recursive

[33:14] self-improvements in like downstream response quality and also productivity gains for engineering for engineers like maintaining these systems. Um those broader metrics are a part of how we want to like basically think about evaluation evaluating these systems at scale because the ultimate goal isn't to like maximize the number of like automated prompt edits. It's to like produce measurable improvements in like agent quality while maintaining some

[33:38] sort of a confidence that those changes are like genuinely beneficial. And this brings up brings us to like the final part of our talk which is how do we scale these um capabilities um which is like through an acceleration plan. So so far we focused on like one implementation of RSI for user understanding but like the broader opportunity is like much larger. If we are able to like um kind of like standardize evaluation, reflection and

[34:05] optimization, we could potentially uh reuse this loop for like or the cycle for like many other agent teams. And um moving forward like um to understand the end toend evals the current state is like this diagram basically shows progression of capabilities that we believe are like necessary to support RSI at scale. At the foundation, we obviously have like the base agent where most teams already have agents that perform like useful tasks whether that's

[34:31] like question answering, summarizing, chat agents um or like just completing workflows as such. The next layer is agent evaluation and this is where we begin to like see gaps because some teams have built their own bespoke evaluation workflows. Other rely on like one-off analysis or like manually inspecting outputs. But only a few of them have like relatively standardized reliable evaluation processes that can be continuously reused. And above um

[34:58] evaluation we have agentic reflection which means being able to systematically investigate or do some sort of like root cause diagnosis. Um and finally at the top we have the RSI loop itself which connects evaluation and reflection to like optimization and validation. The the important observation here is that these layers like they depend on one another and you can't build like a trustworthy loop without like reliable diagnosis. That's why we see like

[35:24] leveling up evaluation infrastructure as a prerequisite to like scaling RSI and rather than asking every team to like independently build all these components, there's an opportunity over here to like provide some sort of like a shared um infrastructure. So uh what would it like basically take to make RSI like a reusable capability across an enterprise is like uh we've identified like five strong areas. First is like standardizing evaluation

[35:50] infrastructure. So we need reusable evaluation frameworks, metrics, judges which can be calibrated with human feedback and um the second is like automating feedback loops. So we want systems that can continuously collect execution traces, detect recurring failures and perform some sort of loop case analysis. Um the third one is we need to scale um automated optimization that includes prompt optimization, agent reflection.

[36:15] So instead of making like ad hoc changes, we want improvement processes where candidates where candidate updates can be like generated and tested in more like a repeatable way. Um the fourth area is like validation and trust. So any automated improvement needs evidence that it actually you know works which means like having robust hold out evaluations and some sort of regression testing. And finally, we want to like obviously democratize RSI across teams

[36:40] where the goal is to develop reusable components and self-service infra so that teams can adopt these capabilities without having to build an entire RSI pipeline themselves which is what our broader vision is. And I think that this is an important shift in how we approach the engineering of like AI systems. Um so in recursive self-improvement we basically just to summarize we have like two key components which is the improvement engine and the target agent.

[37:07] The target agent in the AI system is something we're trying to make better while the improvement engine is you know responsible for driving that change by evaluating performance identifying failures root causes and proposing improvements. But the objective of the RSI system isn't simply to improve the agents performance at like a given point in time. It's to like accelerate how quickly the agent gets better. And if we think of like the agent performance as a

[37:32] function of time, we are interested in increasing its first like its first derivative. If we think about it essentially like making the performance um improvement curve steeper and in our case like the target agent is our user understanding agent while the improvement engine is like the RSI pipeline which brings together evaluation, reflection and firmed optimization. Um before I close, we want to like

[37:56] acknowledge the people who helped make this work possible. This has been like an collaborative effort across the core team, our evaluation team and our engineering partners and leadership. Uh we we particularly like to thank all the team members and collaborators listed here for their contributions. Um a lot of the work we have described for evaluation quality to reflection and production required collaborations across these different areas of

[38:20] expertise and we're grateful for the support and um feedback we have received. Um yep so thank you and uh I guess we just want to conclude by saying that um most important part of like improvement processes is like being able to you know trust the changes we are making to make the system better. So that's some of the directions we're exploring with um recursive self-improvement here. So yeah, thank you so much for listening.
