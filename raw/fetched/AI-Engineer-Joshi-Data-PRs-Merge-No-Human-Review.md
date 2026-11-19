---
title: 60% of Our Data PRs Now Merge With No Human Review — Chetas Joshi, Robinhood
description: AI Engineer 官方閱讀版，Robinhood 資料平台 Chetas Joshi 談腳本查事實、agent 判風險、人管保護決策的 data PR 混合審查，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/MQiojLnK-E0-60-our-data-prs-now-merge-no
published: 2026-11-10
tags:
  - clippings
  - coding-agent
  - ai-agent
  - automation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript JSON 端點，依時間碼每 12 段併成一段，文字未改；含辨識錯誤，如 linter 寫成 linder、ingestion 寫成 injection、講者自稱被辨識成 Jas）。對應 YouTube 影片 ID `MQiojLnK-E0`（`https://www.youtube.com/watch?v=MQiojLnK-E0`，AI Engineer 頻道，上傳日 2026-11-10，約 28 分鐘）。閱讀頁段落編號由 04 跳到 06，缺第 05 段（回饋迴圈與加密欄位例），該段內容僅見於逐字稿約 17:39–20:11；閱讀頁中「Loading slides…」「Loading transcript…」為動態載入佔位字。

Loading slides…

At a glance

### Ideas worth remembering

- A passing lineage check establishes compatibility for registered readers. A repository search can reveal another reader, and an engineer can check whether it is active in production.
- An escalation can save engineering time when it names the changed line, traces the dependency and leaves the reviewer a specific question to resolve.
- Unsafe approvals can reveal a missing search rule. Unnecessary escalations can reveal missing context. A human explanation helps the on-call engineer decide which change to make.

01 [0:00 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=0s)

### The queue forms around the people who know the table

A schema change passes its tests and the linter. Is it safe to merge? A pipeline can produce correct data too late to meet its freshness deadline. A change can break a consumer three teams away or give someone access to sensitive data. For Chetas Joshi’s data platform team at Robinhood, answering the merge question means understanding who depends on the changed code and what they expect from it.

Coding assistants could open a PR for a new query, schema change or access grant in minutes. Reviews of pipeline code and configuration also landed with the data platform team. CI and human review already caught broken code, inefficient queries and data leaks. What slowed the queue was waiting for one of the few engineers who knew who read a table, how large it was and what sensitive data it held. The number of people carrying that context stayed flat as the PRs piled up.

Robinhood split the work by the kind of answer each reviewer could give. A script can look up a fact in a schema registry or catalog and block a PR if the check fails. An agent can read the code, assess risk, and either approve or ask a person to decide. Its rules tell it which questions the scripts cover, saving the cost of asking a model to reconstruct a fact the team can look up. A merge needs both passing checks and an approving review.

[0:03](https://www.youtube.com/watch?v=MQiojLnK-E0&t=3s) [0:06](https://www.youtube.com/watch?v=MQiojLnK-E0&t=6s)

02 [5:24 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=324s)

### What four green checks establish about one schema change

![The schema registry confirms the new column exists upstream. The data catalog confirms ownership and PII labeling. Both checks pass for this pull request. A banner says CI blocks the pull request if either check fails.](https://www.ai.engineer/api/talk-essay-media/6f9725c5e15241d8b0f6c2c6eacf9ce3d2703e0bac8c8105d7c6186a84e7aee3)

The registry and catalog answer separate questions about the new column and ownership of the table.

An ingestion pipeline reads an upstream source table and writes to a table in the data lake. One PR makes two changes. The source has gained a column, and the pipeline will bring it into the lake. A different column, already in the lake table, will widen from `INTEGER` to `BIGINT` so it can hold larger values. The first edit raises a question about the source. The second raises a question about every job that reads the widened column.

- **Data contract.** A script compares the proposed schema and keys with the schema registry. The registry confirms that the new column exists upstream.
- **Required tags.** Every table needs an owner, and personally identifiable information (PII) needs a label in the catalog. A direct catalog lookup confirms both for this table.
- **Downstream dependencies.** The lineage tool records which jobs read a column. A script walks every job registered for the widened column and checks whether the type change breaks it.
- **Performance.** CI runs the change in staging with mock data at production volume. The run checks whether the cluster is sized for the job and whether the job can finish in time to meet its freshness service-level agreement.

A failed check blocks the PR until someone fixes it. Here all four passed. How far downstream did that green result reach? Every registered consumer could handle the wider type. The word *registered* matters. The script starts with the lineage tool’s list, so a job missing from that list contributes nothing to the result.

[5:36](https://www.youtube.com/watch?v=MQiojLnK-E0&t=336s) [5:41](https://www.youtube.com/watch?v=MQiojLnK-E0&t=341s)

03 [10:26 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=626s)

### A repository search finds the narrower destination

The agent starts with the diff. The PR description and commit messages explain what the author intended, but a finding in the code takes precedence over a claim that the change is safe. The agent can list, search and read files across the repository. It has no direct access to the live catalog, lineage tool or production state.

The type of change tells the agent what to look for. In a query, an unpartitioned cross join can return the right answer while hammering a cluster. In an access grant, an ordinary-looking edit can open sensitive data. For a schema change, the rules direct the agent into pipeline definitions and access grants to find consumers beyond those recorded in lineage. For this PR, the question was where a value would go after a job read it from the `BIGINT` column.

The search found a job defined in the repository that had never been registered in lineage. It read the widened column and copied the value to another table, where the receiving column was still `INTEGER`. Values within the original range would continue to fit. The first value large enough to need the wider range would reach that last write and fail. The agent’s review comment traced the path from the changed column through the job to the destination.

Each query engine has to publish its own lineage. If an engine omits a relationship, a repository search can still recover it from a job definition. The search has limits of its own. An ad hoc query someone runs by hand, or a dashboard defined outside the codebase, leaves the agent nothing to read. When a search comes up empty, the agent reports where it looked and that it found no consumers there.

### Where would the first out-of-range value fail?

<svg width="460" height="489" aria-hidden="true"><defs><marker id="_R_3f9qjalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 297.53968253968253 119 L 345 158 L 345 197" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="345" y="154" text-anchor="middle"><tspan x="345" dy="0">Read the widened</tspan> <tspan x="345" dy="16">column</tspan></text></g> <g><path d="M 162.46031746031747 119 L 115 158 L 115 197" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="115" y="162" text-anchor="middle"><tspan x="115" dy="0">Reads the same column</tspan></text></g> <g><path d="M 115 308 L 115 339 L 115 370" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="115" y="343" text-anchor="middle"><tspan x="115" dy="0">Writes the value</tspan></text></g></svg>

**Lake table** The PR widens an existing column from INTEGER to BIGINT.

**Registered consumers** Every reader listed for the column passes the lineage check.

**Unregistered job** The repository contains the job that copies this column onward.

**Downstream table** Its INTEGER column cannot store a value outside the original range.

Follow the data out of the lake table. The lineage check covered the registered branch. Following the other branch through repository code revealed a write to a narrower column.

Read the diagram as text
- **Lake table.** The PR widens an existing column from INTEGER to BIGINT.
- **Registered consumers.** Every reader listed for the column passes the lineage check.
- **Unregistered job.** The repository contains the job that copies this column onward.
- **Downstream table.** Its INTEGER column cannot store a value outside the original range.
- Lake table → Registered consumers: Read the widened column.
- Lake table → Unregistered job: Reads the same column.
- Unregistered job → Downstream table: Writes the value.

[10:28](https://www.youtube.com/watch?v=MQiojLnK-E0&t=628s) [10:33](https://www.youtube.com/watch?v=MQiojLnK-E0&t=633s)

04 [14:36 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=876s)

### The reviewer changes the rollout order

![A diagram traces a widened column to an unregistered job. Three boxes show the agent flagging a write-failure risk, a person confirming the job runs in production, and the downstream table’s column being widened to bigint.](https://www.ai.engineer/api/talk-essay-media/b189cea2cb4d778a31b53b7a5073a69071fee7e4ad6c0c3491acf14758a6baa9)

The order of operations matters: widen the downstream destination before merging the upstream schema change.

The agent attaches its reasoning to specific lines and scores the severity of what it found. For an ordinary change, a confident review with no serious finding can supply the approval needed alongside passing CI. For the widening PR, the agent scored the downstream write as high risk and escalated. The engineer who picked it up already knew which job to investigate. The open question was whether that job actually ran in production.

The human reviewer confirmed the consumer was live. The PR waited while the team widened the receiving column in the downstream table. Once that destination could hold the larger values, the original PR merged and deployed without incident.

Some decisions always go to a person. In each case, the agent passes along its findings and reasoning.

- **Sensitive access grants.** A person decides who may reach sensitive data, however confident the agent sounds.
- **Migrations that appear to change meaning.** If a migration changes what the data represents, a person decides whether that change of intent is acceptable.
- **Low-confidence verdicts.** Even when the search turns up no concrete defect, uncertainty sends the review to a person.

[14:47](https://www.youtube.com/watch?v=MQiojLnK-E0&t=887s) [14:56](https://www.youtube.com/watch?v=MQiojLnK-E0&t=896s)

06 [20:14 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1214s)

### A false alarm costs time. A missed reader breaks.

![A two-by-two matrix compares the agent’s decision with the quality of a pull request. Approving a bad change is a miss. Escalating a sound change costs a reviewer time. The other two cells show correct approvals and escalations.](https://www.ai.engineer/api/talk-essay-media/0b0637e3170bac66f7af9e57e9372384810395d374cf19bb33eb971dc2253193)

The four cells distinguish useful escalations, false alarms, missed issues and changes safe to pass.

How can the team tell whether a review rule helps? Cross the agent’s decision with the decision the PR needed. Approving a safe change and escalating a risky one are both correct. Approving a risky change is a miss that lets the change ship. Escalating a safe change unnecessarily consumes an engineer’s time. A reviewer could avoid every unsafe approval by forwarding every PR, leaving the original queue intact.

As of August 31, 2026, Joshi reported a miss rate of about 2%, without specifying the denominator. The team traced most misses to gaps in the review rules. It had no single reliable rate for false escalations, but the most common cause was missing context of the kind the encrypted-column example exposed.

One miss started as a privacy correction. A downstream job read several columns from an open copy of a dataset. When the privacy team retagged the columns as personal information, they moved to a restricted copy and disappeared from the open one. The retag itself looked reasonable. The reviewer approved it, the PR merged, and the job broke when it tried to read the missing columns.

The team added a rule with a specific trigger and search target. When a column is retagged as sensitive, search the codebase for readers that still reference that column in the copy about to lose it. That gives the reviewer a way to flag a broken read even when the privacy classification is correct.

[20:21](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1221s) [20:27](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1227s)

07 [22:34 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1354s)

### Even escalated PRs took less work to review

As of August 31, 2026, about 60% of Robinhood’s data pipeline PRs merged without human review. The team reported about 75% less manual review effort, saving roughly 132 engineering hours a month. The widening PR illustrates how an escalation could also save work. The engineer could go straight to checking whether a particular consumer was live because the agent had already traced the dependency.

The team also observed about 30% fewer incidents tied to these PRs. That figure describes the team’s experience with the hybrid reviewer in place, including the engineers who decided protected cases and investigated escalations.

[23:03](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1383s) [23:09](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1389s)

08 [24:20 ↗](https://www.youtube.com/watch?v=MQiojLnK-E0&t=1460s)

### Two independent reviewers and a proposal for one entry point

The two layers in the deployed design run in parallel. Separate triggers start the scripts and the agent on the same PR, and each produces its own result. The agent knows which checks are configured, but it cannot see whether a particular check passed, failed or hit an outage. Nor can it call a check when its investigation turns up a question about production. Merge still requires passing CI and approval. If either system cannot finish, the team waits for a human.

What would a single entry point change? In the proposed design, a classifier would examine the whole PR before deciding which changes to review together and which to handle separately. That would let the grouping decision account for relationships across files. The agent would also get callable deterministic checks alongside its repository tools, so it could request a live fact when the code raised a question. The team was exploring this design. The reported savings came from the parallel systems already in use.

Joshi would carry three decisions into that redesign. Keep yes-or-no lookups in scripts, where each lookup saves model work. Give people the final call on sensitive grants, migrations that change meaning and uncertain verdicts. And count unnecessary escalations alongside misses. Each needless referral spends the time of the same few engineers the reviewer was built to free up.

[Transcript download](https://www.ai.engineer/api/data/transcript?slug=youtube-5ffdaaaecd14534ea422&format=json)

Full transcript

Loading transcript…


## 官方機器逐字稿

[0:00] Picture a pull request. It changes a schema in one of our data pipelines. It goes green in CI. The tests pass. The linder is happy. And everything about it looks clean. So, is it safe to merge? Because a change like this can still break something downstream. Maybe it blows a freshness SLA. Or maybe it breaks a consumer three teams away who never saw it coming. Or maybe it exposes data that never supposed to be reachable. That gap between CI past and 

[0:32] this change was actually safe is the gap my team has to close every day. Hello everyone, I'm Jas. I'm an engineer on the data platform team at Robin Hood. I design and build the distributed data injection and processing frameworks behind our data lake. The ones teams across the company rely on to make decisions with data. Notice the title of this talk. The bots in it are the ones opening the pull requests and as you will see the ones 

[1:01] reviewing them as well. Today I want to show you how we answer that question when the PRs are coming in faster than any of us can read them. So here's the problem in one sentence. Pull requests to our production data pipelines now arrive at machine speed. But reviewing them safely still runs at human speed. First, a quick word on the scope of this talk because it shapes everything else in this talk. 

[1:32] AI coding assistants have made pull requests cheap to open. A new query, a schema change, or an access grant now takes just a few minutes. And an assistant can open pull requests far faster than any team of humans ever could. The PRs I'm talking about today are the PRs to our data pipelines like schema changes, pipeline code, configuration changes, and grants that give someone access to data. 

[2:03] Data platform is the team that owns reviewing that kind of PR. So when those PRs pile up, they pile up on us. And the reviewer I'm about to describe is the system we built to handle them. So the people who feel this are a small group. The engineers who carry the context to say what is safe to merge into production and everyone who is waiting on them. So why is this a problem? AI open PRs just keep arriving. 

[2:34] And to be fair, the safety net we already had works. CI checks together with a human review have always caught a lot of real bugs like broken code, inefficient queries and risks like downstream breakage or sensitive data leaks. But the human half only works at the human speed and only with the context a person happens to carry in their head. Who reads this table? How big is it? And how sensitive is the data in it? The PRs are coming in at the 

[3:06] machine speed, but the number of people who understand what is safe to merge into a production data pipeline did not grow at all. That's the mismatch. The queue builds up in front of the few people with the context and that's where things start to slip. So the problem we set out to solve was this. Build a PR reviewer using AI that can keep up with the speed at which PRs are being opened. So here's the whole answer before we get 

[3:36] into the details. Three duties, three owners. Scripts prove what can be proven. An agent judges what needs context and people own the calls only they should make. We took a hybrid approach. Scripts for the facts and AI for judgment. We did not want AI reviewing every change when some questions already have an authoritative answer. And that's layer one. Deterministic scripts check a source of truth like the 

[4:08] schema registry or a catalog. A failed check turns CI red and blocks the PR until it is fixed. Layer two is the agent. The agents rules tell it what layer 1 already checks. So it focuses on the risks those checks cannot catch. It reviews the PR, scores the risk and approves or escalates to a person. Both these layers review the same PR. Merge requires passing checks and an approving review. And this also keeps AI costs down. We 

[4:43] use AI for judgment, not to rediscover facts a script can look up. So here is where we are going today. We have covered the problem and the approach. Now I'll walk you through the hybrid reviewer we built and the decisions we deliberately keep with the people. After that how the reviewer learns from the human feedback and what results we have seen so far. And we'll finish with the lessons we would pass on to you. 

[5:12] Three things to listen for as we go. Scripts for facts and agent for the judgment and people for the protected calls. I'll come back to all three at the end. So to make this concrete, let me show you the one PR will follow through the rest of this talk. This PR makes two changes to a table in our data lake. It adds a new column and widens an existing column from integer to big integer. It's the kind of PR we 

[5:43] see all the time. On the left is an upstream source table. Our injection pipeline reads from it and writes into a table in the data lake. call it our table. The first change, the source has gained a new column and this PR makes injection bring that new column into our lake table. The second change is to a column of a table already has its type gets widened from integer to 

[6:12] big integer so it can hold bigger values on its own. That sounds completely harmless. Widening a type is about the safest schema change you can make, right? Well, whenever a column changes, the real question is who reads it downstream? Some of those readers are registered in our lineage tool. So, we know about them. But keep a second question in the back of your mind. Are those all of them? 

[6:40] Hold on to this picture. We will come back to this exact diagram each time the PR moves forward through the reviewer. So let's start with layer one. Layer one is the scripts and their whole job is checking facts in the live systems. Things the code alone cannot tell you. Here are the two of those checks and what they said about our running PR. First data contracts. When a PR changes a schema, a script compares the schema and keys against a source of truth, the 

[7:16] schema registry. for our PR. The question is simple. Does that new column actually exist upstream as registered in the registry? It does. So that check passes. Second require tags. Every table needs an owner and any PII has to be labeled in the catalog. The script checks the catalog directly. Does our table have an owner? Yes. Is its PII labeled? Yes. pass again. And if either of those had failed, there 

[7:50] is no debate and no model involved. CI goes red like any other failing checks and the PR is blocked until it is fixed. Contracts and tags are two of the layer 1 checks. Next, the two that look at downstream impact and performance. So these are the other two layer 1 checks. They look past the table itself, what happens downstream and whether the job will still run in time. First, the lineage blast radius. When a column changes, like the one our PR 

[8:24] widens, a script walks every downstream job the lineage tool has on record for that column and asks a simple question. Does any of them break? It's a real check against a real system. But notice the boundary I have drawn. It can only see what is recorded in lineage. Its view of downstream is exactly as complete as that record. No more. Second, the performance. A correct change can still be too slow or too expensive. So the CI performance test 

[8:57] runs the change in staging at the same data volume as production using mock data. So that tells us two things before the PR merges. whether the cluster is sized right for the job and whether the job will still make its freshness SLA. Those are the kind of problems that otherwise show up weeks later as an incident. So that's the full set of layer 1 checks. Let's see what they said about our PR. So back to our running PR. Same picture 

[9:30] as before. Here's what the layer one said about it. The data contract check went to the schema registry and asked whether the new column really exists upstream as register. It does and the check passes. The leanage blast radius check walked every registered consumer of the widen column. The jobs the lenage tool has on record. None of them break when the column goes from integer to big integer. They all look fine. Along with that tags 

[10:01] pass, performance passes. Every check is green. As far as the scripts can see, this PR is safe. But I chose those words carefully. As far as the scripts can see, everything on the slide is a statement about the registered picture, the jobs and the columns our systems have a record of. And keep that in mind. It is not the whole story. Now let's look at the agent with the diff. What actually changed? 

[10:31] The PR description and the commit messages explain the author's intent, but intent never explains away a real finding. If the description says it is safe and the code says otherwise, the code wins. File tools let the agent read, search, and list the files across the repository. It follows changes beyond the diff into pipeline definitions and access grants looking for the relationships the author may have 

[10:58] missed. These are the repository repository tools only. The agent cannot query the live catalog lineage tool or production state. Life facts stay layer 1's job. The agent reasons over the code. So why walk that code for a schema change? Because registered lineage is not the whole picture. The rules define where the judgment belongs. They are configured by the change type in the PR knowing what layer 

[11:30] 1 already covers. They target query anti patterns, sensitive data asks and consumers outside lineage. For example, an unpartitioned cross join can run correctly and still hammer a cluster. A grant can look ordinary and still open sensitive data. And for the schema changes, the agent walks the pipeline definitions and access grants in the repository to find consumers that were not registered. It's a tedious search uh a person would 

[12:00] otherwise do by hand. Let's return to our PR and see what that search found. So back to our running PR. Same picture. Layer 1 said every registered consumer of the vid column looks fine. Now the agent walks the code and it finds a job that lineage never knew about. It's right there in the repository. It reads our widen column from our late table but it was never registered in the lineage which is 

[12:30] exactly why the layer 1 check could not see it. And that job takes the value and writes it into another table. And in that other table, the column is still an integer. Now follow it through. Our column is a big integer. Now the first time a value comes through that's bigger than an integer can hold that right fails. A valid schema change green in CI passes every registered check and a downstream job still breaks. 

[13:03] The agent flagged exactly this chain in its review comment with the reasoning. So a person could see the whole path from our column to the failing right. We'll get to what happened next in a moment. So why did the lineage miss that job? Because the enterprise data world is messy. Workloads run across different query engines and each engine has to publish its own lineage. If one does not publish, that relationship is missing 

[13:30] from the picture. There's a single catalog that automatically sees everything. So the registered picture is useful but it is not the whole picture. Now I don't want to oversell the codewalk. It's genuinely useful but it cannot see everything. The agent can search what is in the repo. Pipeline code access grants and the jobs defined there that read our tables. That's where it found our unregistered job. But plenty of data use 

[14:02] lives outside the codebase. Ad hawk queries that someone runs by hand. Dashboards, those are completely invisible to a repository search. A consumer out there never shows up, no matter how carefully the agent looks. So we make the agent honest about that limit. If it does not find anything, it does not get to say no downstream consumers exist. It says it found none in the places it searched. None found is not the same as none exist and the agent 

[14:31] never gets to claim an allcle. So the agent has walked the code. What does it actually produce? A review the same shape a good human reviewer would give you. First review comments on the specific lines that matter each with its reasoning. Not awake looks risky but this line changes this column. And here is the job that reads it. Second, a risk score. How severe is what it found. That's what drives the next 

[15:04] step. Then it makes a call. If there is no serious risk, it can approve. If there is a risk that needs a person, it escalates to a human and the comments and reasoning go with it. So the person has the context to investigate instead of starting from scratch. And to be clear about what it takes to merge, layer 1's checks have to pass and the review has to approve either the agent or after an escalation a person. Both have to say yes. Now let's see what 

[15:36] that looked like for our PR. Here is how our running PR actually ended. Same picture. The registered consumers look fine and the core walk found an unregistered job that writes our widened column into a table where it is still an integer because the agent found a real downstream break. It scored the risk high and escalated to a human with the whole chain spelled out in its review comment. Now the human does the part the 

[16:06] agent cannot. The agent only reasons over the repo. It cannot see whether the job is actually running in production. human reviewer checked and confirmed that the consumer the agent found was live and active. So this was not a theoretical risk. The PR waited the f the fix was about order not about rejecting the change. The downstream table was updated first so its column could handle the wider type and only then did our PR merge and 

[16:38] deploy. No incident. The scripts in layer 1 said safe. The agent found the gap and a human made the call. And that was not a one-time thing. Most changes can be cleared by the agent. When the checks pass and the agent is confident in its verdict, it approves on its own. But there's a whole category of changes where the agent never gets to say approved. And no matter how confident it sounds, grants touching sensitive data are one. 

[17:10] Who can reach sensitive data is a decision we want a person to own every time. A migration that looks like it changes intent, not just mechanics, is another. If a change alters what the data means rather than just how it is moved or stored, a person decides. And if the agent itself is not confident in its own verdict, that's the third. It does not get to round up to approve just because nothing concrete came back 

[17:39] wrong. In all the all the three cases, its job is only able to surface the risk and its reasoning. The decision stays with a person. That is one PR. Now, how does this hold up across every PR we see? And how does the reviewer get better over time? How do we know the flags are useful or whether a rule change helps? We start with the agents verdict and its reasoning in the review comments. A person replies agreeing or disagreeing 

[18:12] and explaining why. That explanation is what makes the feedback useful rather than just a vote. Those replies are collected every day. Once a week, the on call reads the feedback and updates the review rules by hand. Those rules shape the next review. I know this is manual today. Nothing retrains itself and no rule changes automatically. But we have an idea to let an incident investigation agent help with that weekly pass. But it is not 

[18:43] built. Without the feedback, every rule change would be a guess. So let me show you an example where a human corrected the agent and we use that feedback to improve its next review. So here's a real one. And note the label in the corner. This is a separate example, not our schema change PR. A column was marked as personal information in the source database. But by the time it lands in the data lake, the injection pipeline has already 

[19:14] encrypted it. So the PR proposed labeling it nonsensitive in the data lake even though the upstream data is still PII. The agent flagged this. From where it stood, the upstream says PII, so a nonsensitive label looked wrong. The author pushed back and asked the agent to look at how similar columns on the other tables were already classified instead of going purely off the upstream tagging. 

[19:42] A human agreed with the author. The encryption before write made the nonsensitive label look okay for this column. And that kind of correction is exactly the signal that teaches the rules to get smarter because the next time a similar column comes through that context can stop a needless escalation. One caution though, this depends on the specific pipeline encrypting before the right. It's not a blanket rule that encryption always makes data 

[20:11] nonsensitive. So how do we know whether the reviewer is actually doing a good job? We look at two kinds of mistakes. Bad PRs it approved and fine PRs it unnecessarily send to a person. That matrix separates four possibilities. A fine PR approved and a bad PR escalated are the two correct outcomes. A bad PR approved is a miss. That's dangerous because the change ships. A fine PR escalated is a false 

[20:44] escalation that costs a person's time. A gate that escalates everything may avoid misses, but it has not reduced the review load. As of August 31st, 2026, our miss rate was about 2%. Mostly from the gaps in the rules rather than the failures of the judgment. We don't have a clean single false escalation number. But the dominant cause is missing context like the encrypted column example that I just 

[21:14] gave you. Misses give us new rules and false escalation show us context the reviewer needs. So here is one of those misses. Again know the label. This is a separate example, not our schema change PR. We have an open copy of the sum of some data. some of its columns are about to be rettagged and there is a downstream reader that reads those columns from the open copy. Privacy retag those columns as personal 

[21:43] information. When that happens, they move into a more restricted copy of the data and they are gone from the open copy. The retag looked fine and it merged. But what nobody checked was whether anything downstream was still reading those columns from the old open copy. something was. And once the columns were gone, that reader broke. That's a miss. A PR that should have been escalated got approved. 

[22:11] It wasn't a failure of judgment. It was a gap in the rules. A coroner case nobody had written down. So, it became a new rule. When a column gets retagged as sensitive, search the codebase for anyone still reading it from the copy that's about to lose it. And that's how the rules get better. the misses get found and get turned into new rules. So let's pull it all together. You remember the pull request from the start, the one that was green in CI. 

[22:42] Three things happened to it. First, scripts proved what a source of truth could prove. The contracts, the tags, the registered lineage and performance all passed. Second, the agent read the code and found what the scripts could not see. A job that Lineage never knew about, quietly waiting to fail on a wider column, it flagged the whole chain and escalated. Third, a person confirmed the job was live. Uh, the downstream table 

[23:11] was fixed first and only then did the PR merge. No incident. And behind all of that, the reviewer keeps getting better because every correction a person makes can become a rule. These results are as of August 31st, 2026. So you might ask, Jas, does it all work? Yes, about 60% of the data pipeline PRs merged without a human review. We have seen about 75% less manual review effort. The agent specific comments and reasoning help focus the 

[23:45] review rather than making a person reconstruct every risk from scratch. The time saved comes to about 132 engineering hours a month. Incidents tied to these PRs are down about 30%. And that does not mean human free review. The protected decisions still reach a person by design. The goal is less review work, not removing accountability. And those are the results. Now, let's look at the architecture choices we got wrong. 

[24:20] Here is what we got wrong today. Layer 1 and layer 2 are separate systems triggered independently and running in parallel. Each produces its own result that seemed like an obvious design when we built it, but neither sees the others pass fail or outage state. Layer 2 knows what the scripts are configured to cover, not what happened when they ran. Merge still needs passing checks and an approving review, but no single system has a full 

[24:51] runtime picture. The agent also cannot call live layer 1 checks. Its tools only read, search and list the repository files. If a judgment needs a live fact from a live production system, it cannot fetch that fact itself. When one site cannot finish, we wait for a human. There is no automatic fallback. These are current limitations and they motivate the proposal. On the next slide, platform team is exploring one 

[25:22] entry point. This is a proposal and not what's running today. The left panel is the current design and the right is where we want to go. A classifier looks at the whole PR then decides which changes to review separately and which to review together. This is a whole PR decision, not independent routing of each file. The agent would also get the layer 1 checks as collable tools alongside its repository tools. When judgment needs a 

[25:52] live fact, it could request the appropriate check instead of being limited to code alone. The aim here is one system with the whole PR in view. We haven't built this yet. So, it's a direction, not a result. Let me close with what we would carry forward. So, here is the whole talk in three lines. Deterministic evaluations. First, if something can be proven against a source 

[26:17] of truth, let a script prove it. Don't spend a judgment call on a yes or no fact. It's not just cleaner, it's cheaper, too. Every fact a script proves is review work that never needs AI. So, the cost of running this stays down. Flag never clear. Not for every PR, but for the changes that actually scare people, like sensitive grants, migration intent, and low confidence verdicts. There, the agent's job stops at surfacing the risk and the reasoning 

[26:50] behind it. The decision stays with the person every time. Count the false escalations. A gate that escalates everything is not actually saving anyone any time. It's just moving the work around. measure that cost the same way you measure a miss. So I started with a pull request that was green in CI and a problem PRs arriving at machine speed and too few people with the context to review them safely. We built a hybrid reviewer scripts for the 

[27:21] facts and agent for judgment and people for the protected calls. We walked one PR through all three saw it get lighter without going human free and saw how it learns from the corrections. We told you what we got wrong and we left you with three lessons. Prove what you can cheaply. Flag and never clear the scary changes. And count the false escalations. So who reviews the bots? Scripts for everything a source of truth can prove, 

[27:51] an agent for everything that needs context and judgment, and humans for the calls only they get to make. Thank you for listening.
