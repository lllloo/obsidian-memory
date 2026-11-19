---
title: The Agents Were Fine. Everything Around Them Broke. — Joey Wang
description: AI Engineer 官方閱讀版，Harvey 的 Joey Wang 談內部 cloud agent 平台 Spectre 在量放大後壞掉的周邊系統，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/ktbAVYsAxpk-agents-were-fine-everything-around-them-broke
published: 2026-11-10
tags:
  - clippings
  - coding-agent
  - ai-agent
  - automation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript 下載 API，JSON 依時間每 6 段合併為一段、文字未改；原稿含辨識錯誤，如 Spectre 被辨識成 vector／spectctor、Claude Code 被辨識成 clock code／cloud code、repo 被辨識成 ripple）。對應 YouTube 影片 ID `ktbAVYsAxpk`（`https://www.youtube.com/watch?v=ktbAVYsAxpk`，頻道 AI Engineer，約 13 分鐘）；`published` 取 YouTube 上傳日（2026-11-19 以 yt-dlp 核對）。閱讀頁的投影片僅存圖片說明文字。

Loading slides…

At a glance

### Ideas worth remembering

- Give the platform responsibility for what follows the first patch. In Spectre, a failed CI check could drive another attempt before the reviewer’s working day began.
- Make each user action callable. A command for starting a task or enabling follow-up gives a laptop agent, a sandboxed worker and CI access to the same capability.
- Set limits before a person, agent or alert discovers how much work it can start. Routing repeat alerts to the open investigation prevents duplicate work. A fair dispatcher handles the different case where one person has hundreds of tasks to run.

01 [0:00 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=0s)

### What a cloud agent needs from Harvey

In the month before Joey Wang’s talk, Spectre, Harvey’s internal cloud agent platform, started more than one agent per minute on average, day and night. About 460 people used it that month. Agents had written 10,000 pull requests, and people were finding other uses for the same setup. They asked data questions in Slack and got answers back. Someone in marketing dropped a prototype and a talk track into a channel and asked for help turning them into a story for a product video.

Why build Spectre when engineers already have coding agents they like? Spectre runs those agents. Wang put the practical limit on a laptop at roughly five to ten at a time. Moving work to the cloud buys capacity, but a remote agent still needs a repository checkout, credentials and access to Harvey’s stack. It needs a way to pick up an alert or ticket and get a change through review. Spectre supplies that harness. Sharing it across the company adds another responsibility. Even when one engineer has plenty of work to hand off, the next person needs room to run.

[0:02](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=2s) [0:05](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=5s)

02 [2:38 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=158s)

### A 2 a.m. fix still has to pass CI

Engineers adopting Cursor had two immediate questions. How could they get access to Harvey’s secrets, and how could they test against the real stack? Wiring both into Cursor would leave the team with the same job the next time engineers switched tools. Harvey let engineers ask their preferred agent to use Spectre. A session could start on a laptop, move to the cloud and come back. The team could keep its test environment as engineers changed agents.

Take Wang’s example of an alert arriving in Slack at 2 a.m. An agent picks it up without anyone typing a prompt, writes a fix, spins up a copy of Harvey’s stack and posts evidence on the pull request. If continuous integration (CI) fails, the failure itself becomes input to the next attempt. A follow-up loop reads what failed and pushes another fix while the owner is asleep. By morning the PR is in the shared review queue under the same rules as any other change. Spectre waits until the owner’s working day begins to send a nudge. Once the change is approved, an agent can merge it automatically.

The follow-up loop was the stage Wang would build first. Harvey enabled it for everyone in early October. Of the agent-written PRs that merged into Harvey’s backend that month, four out of five had gone through the loop.

Testing a tricky service can depend on something one engineer knows, right down to which flag to leave alone. Spectre gave that knowledge a home in projects. People could record what mattered, agents could record what they learned, and a team could pin the skills it trusted. Any agent working in the project could draw on that knowledge. The project also kept a record of who ran what. Wang’s view was that whichever agent an engineer picked, the checks and the audit trail should be the same.

[2:44](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=164s) [2:47](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=167s)

03 [5:19 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=319s)

### The command line lets one agent put others to work

In May, people usually opened a browser tab or tagged Spectre in Slack. Exactly one task that month came from a terminal. The team adopted a rule that any action a person could click should also be callable by an agent. The command-line interface could start a task, turn on the follow-up loop, enable auto-merge or publish a page. An agent on a laptop, an agent already inside a sandbox and a CI job could all use those commands.

Where did the new work come from? By October the command line was starting about 6,500 tasks a month, while web-app usage held up. Some people started hundreds of tasks a month without ever opening the app. One conversation with an agent could now set a whole batch of work in motion.

Wang used that access in two directions over the course of October.

- **Hand work out.** Wang asked a coding session to coordinate a large ticket. It divided the work into ten milestones, kept one for Wang and handed the rest to Spectre as hundreds of tasks. Each task got its own sandbox for end-to-end validation.
- **Bring decisions back.** Later that month, another agent watched Spectre for questions that were holding up work. It listed the questions, drafted Wang’s replies and sent them back once Wang approved them. Wang could answer workers without visiting each task to find out what it needed.

Each sandbox also needed code to work on. When the team measured where task time went, the slowest step was Git checkout. Checking out all of Harvey’s repositories took more than a minute on average. The team kept a copy of every repository on every machine and let each task borrow the local copy. A burst of tasks on the same machine could reuse repositories the machine already had.

[5:23](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=323s) [5:25](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=325s)

04 [7:38 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=458s)

### One bug started about 900 investigations

![A bad release triggered hundreds of workspace alerts. Tagging an agent on each alert generated about 900 tasks from one channel. At peak, all 27 nodes were occupied, and more than 1,000 pod scheduling attempts failed.](https://www.ai.engineer/api/talk-essay-media/1890d65ad04f0add95e0c8e57ec9e8449224d330b5dfbe62ceb70394e4b8f515)

A single recurring alert opened hundreds of investigations into the same release.

A mid-August release shipped a bug that fired an alert once per workspace. Hundreds of alerts landed in one Slack channel. A workflow tagged the agent on every alert, and every tag started a task. On an ordinary day that workflow started about 50 tasks. During the incident it started around 900 in four hours, all chasing the same bug until the cluster filled up.

What should happen when the next workspace reports the bug? Under the original workflow, that report was an instruction to launch a worker. With the fix, a repeat alert joined the investigation already open. The same investigation could collect reports from many workspaces.

### Where the next workspace alert goes

<svg width="460" height="529" aria-hidden="true"><defs><marker id="_R_1nmajalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 297.7894736842105 120 L 345 159 L 345 217.5" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nmajalm_)"></path><text x="345" y="155" text-anchor="middle"><tspan x="345" dy="0">Every alert triggers a</tspan> <tspan x="345" dy="16">tag</tspan></text></g> <g><path d="M 345 328.5 L 345 379 L 345 410" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nmajalm_)"></path><text x="345" y="383" text-anchor="middle"><tspan x="345" dy="0">Each tag starts a task</tspan></text></g> <g><path d="M 162.21052631578948 120 L 115 159 L 115 198" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nmajalm_)"></path><text x="115" y="155" text-anchor="middle"><tspan x="115" dy="0">Route the report to</tspan> <tspan x="115" dy="16">existing work</tspan></text></g></svg>

**Another workspace reports the bug** Its alert lands in the shared Slack channel.

**Tag the agent again** During the incident — The workflow tags the agent on every alert.

**Launch another task** During the incident — Another agent starts investigating the same bug.

**Join the open investigation** After the fix — The investigation already under way receives the repeat alert.

Follow the same repeat alert through the two versions of the workflow. Its destination determines whether another agent starts.

Read the diagram as text
- **Another workspace reports the bug.** Its alert lands in the shared Slack channel.
- **Tag the agent again.** During the incident — The workflow tags the agent on every alert.
- **Launch another task.** During the incident — Another agent starts investigating the same bug.
- **Join the open investigation.** After the fix — The investigation already under way receives the repeat alert.
- Another workspace reports the bug → Tag the agent again: Every alert triggers a tag.
- Tag the agent again → Launch another task: Each tag starts a task.
- Another workspace reports the bug → Join the open investigation: Route the report to existing work.

[7:40](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=460s) [7:44](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=464s)

05 [8:25 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=505s)

### A fair launch queue for a shared cluster

![The queue reserves 40 interactive slots and allows 25 concurrent tasks per person, rising to 50 when capacity permits. In a synthetic 300-task burst, enabling the queue reduced concurrent tasks from 240 to 20 and p95 worker heartbeat latency from 5.3 seconds to 19 milliseconds.](https://www.ai.engineer/api/talk-essay-media/06f155a0ab97a0cc1a4391f9d22a9fb860448a48d98f4dc76f6dfc2f78601994)

Interactive work gets a reserved share of the cluster. Excess work waits in a per-user queue.

Two months later, an engineer did exactly what the team had encouraged and handed work to Spectre. One laptop submitted about 950 command-line tasks in about three hours. The cluster filled, and everyone else’s work sat behind that laptop. Routing repeat alerts to an open investigation addressed the August failure. This time Spectre needed a way to accept a large batch and still let other people work.

Four days later the team had a fair launch queue. Submitting a task gave its owner a visible place in line. A dispatcher started work when the cluster had room, giving priority to people waiting at a keyboard. Each user had a fair share of capacity and could borrow more while the cluster was quiet. A large batch could use idle machines while the dispatcher retained control over who got the next opening.

What happened to completion as volume rose? On the busy August day Wang used for comparison, about one task in ten failed to finish. On November 4, Spectre handled more than twice that day’s volume, and a larger share of tasks finished. Several changes landed together, so Wang couldn’t say which fix contributed most.

[8:21](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=501s) [8:23](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=503s)

06 [10:06 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=606s)

### The merge queue became the next bottleneck

At the end of October, Harvey’s developer platform team raised a different alarm. Company-wide PR volume had jumped around 60% in one month. Merging a change used to take 15 to 30 minutes. Now it took over an hour, and the team repeatedly had to switch off the merge queue.

With the queue off, a PR rebased onto `main`, reran CI and merged if the checks passed. Every PR depended on that shared starting point. If `main` broke, everyone’s CI broke with it. The fair launch queue could make room for people to start work. How to keep their finished changes moving through merge was still open.

[10:06](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=606s) [10:08](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=608s)

07 [10:45 ↗](https://www.youtube.com/watch?v=ktbAVYsAxpk&t=645s)

### Who starts the work when nobody is watching?

Spectre’s fastest-growing source of work was automation. A schedule or an event could wake an agent to triage an alert, read a PR or write a post. About 110 people had automations running in the month before the talk. An unattended agent could start thousands of tasks, so each automation switched itself off after five consecutive failures. Its owner could also give it a budget or an expiry date.

Wang wondered what would happen if every Slack channel had a persistent agent that could follow a conversation and recognize when to begin work on its own. For reviewers, the question was whether every PR could arrive with evidence that the change worked before a human even looked at it. At the time of the talk, only one merge in 20 carried that kind of proof. And even a change that came with proof would face the question Harvey had yet to answer. How do you merge when agents keep opening PRs?

[Transcript download](https://www.ai.engineer/api/data/transcript?slug=youtube-341c05f0a2a08d64277c&format=json)

## 官方機器逐字稿

[0:00] Let me start with one number from last month. On average, more than one agent has started on our platform every single minute, day and night. And honestly, the agents were the easy part.

[0:15] Hi, I'm Joey. I bu the cloud agent platform we built inside Harvey. After 10,000 PRs, the biggest lesson I can share is this. The thing that broke was an agent. It was everything around them.

[0:33] So, what does one submit add up to? 10,000 PRs that an agent wrote. And it isn't just Tavac team playing with a toy. Last month, about 460 different people at Harvey use it. And over the summer, it stopped being only about

[0:53] code. People started asking a data question in Slack and getting answers back. My favorite recently someone on our marketing team dropped a prototype and a talk track into Slack and ask for a story book for a product video.

[1:10] Once the harness exists, people bring the work that you never planned for. So a promise up front. This is not a talk about models, evos or leaderboard. This is talk about hardness, odd things around the model,

[1:29] checking out the ripple, holding the key, opening the PR, getting the merged. When we first wrote about Spectre back in April, we put it like this. At some point, a harness become the product. Now, whenever I tell people this, I get

[1:46] the same question. Why on earth would you build this when clock or cursor already exist? My answer, we don't compete with them. We run them. And here's how I see it as my own view. Agents on your laptop are

[2:02] powerful, but they don't scale. You can realistically run five to 10 of them. Pass that you need a cloud. And cloud needs our secrets, our real stack, our alerts and tickets, one set of rules and enough capacity that nobody gets

[2:20] starved. Those single two owns that for us. So we build layer and that layer exactly what broke. So I want to tell three stories today. How we stopped competing on writing code. how we let any agent drive and were broke once they

[2:38] did. The first story start with the question we keep hearing. More of our engineers were using cursor and they ask how do I get our secret there? How do I test against our real stack? We could have rebuilt all that

[2:56] inside cursor and then again for next to and the one after that. Instead, the answer became one sentence. Just ask cursor to use vector. And that's really the whole idea. People will always have a favorite agent and

[3:13] the favorite keeps changing. So pick yours. Cloud code, codeex, cursor, trag your own hands. Start on your laptop, push the session to the cloud, put it back. That's how Spectre sits underneath all of that.

[3:30] Because once the code was written, the real group starts picture appears day. Alert files in Slack at 2 in the morning. An agent picks up nobody typing. It writes a fix, spins up real copy of our stack and post

[3:48] the proof on the PR. When CI fails, the follow-up loop reads the failure and pushes another fix while everyone still sleep. By morning, the PR sits in one review queue under the same rule as other PR whichever agents wrote it. The

[4:07] owner gets a notch and only once your working day starts and once approved a agent can automerge it. If you only build one of those stages that I described, build a follow-up loop. We switched on for everyone in

[4:25] early October and that months. Four out of five agent PRs merged into our backend PR had been through it. That's the difference between agent that write code and an agent that finished the job.

[4:41] And then there's the knowledge. Every team has that one person who knows exactly how to test the tricky service. Uh which flag you never touch. And that knowledge leaves in their head. of their laptop.

[4:55] So we gave it a hope projects people write down what matters. Adrian write down what they learn. Team pings the skills you trust and there's a record of who rent what. Any agent working in the project with

[5:11] the same page. My personal view whichever agent you pick the audit trail and the checks should be the same. The second story is about rule. Back in May, if you want a spectctor to do something, you open a browser tab or

[5:28] tacking Slack. The whole month, exactly one task came out from terminal. So, we made a rule. If a person can click it, an agent can call it. Start a task. Turn on the follow-up loop on automerge, publish a page, all from

[5:47] CLI, which means your laptop agent can call it. A agent inside the sandbox can also call it. Even CI can call it too. And then people ran with it. By October, the command line was starting about 6,500 ts

[6:04] a month. The web app didn't shrink. Everyone else just grew around it. Task started from the terminal were merging mops and task started in browser and the new kind of users showed up. People who start hundreds of tasks a

[6:21] month and never open the app at all. And this is where it gets fun. In October, I had a big task. So I bought code session and asked to be the coordinator. It split the tickets into 10 different

[6:37] milestones. K one for me and the rest to Spectre with hundreds of tasks. Each has its own sandbox to validate end to end. Then at the end of the October, our it give everyone trag now watch Spectre for me. It list the

[6:56] question Spectre is waiting on draft my answers and once I say yes, send them back. I actually DM to my friend like that. I just use cursor clock code or whatever to spam spectre. Now,

[7:11] well, that's the dream, but it's also the problem. A quick detour. When we look at where our task time actually went, the slowest step wasn't model syncing. It was get just checking out every ripple we own

[7:26] took over a minute on average. The fix keep a copy of every ripple on every machine and let each task borrow it. The third story is the one where it broke in mid August. A release goes out

[7:44] with a bug. That bug triggers alert that fires once per workspace. So one bug become hundreds of alerts all landing in one single S channel. Someone has set up workflow that tag our agent on every alert and every tag

[8:01] started task. On normal day those task started about 50 task. That day in about four hours they started around 900. 900 agents are chasing the same bug until that wasn't room left for a single note.

[8:18] The fix was almost boring. A repeat alert now joins the investigation that's already open. Two months later, it happened again. And this time, it wasn't a bot. On October, the engineer did exactly what we've been

[8:35] asking everyone to do. Hand work to Spectre. About 950 tasks from the command line. In about 3 hours, nothing in our platform can work. The cluster filled up and everyone else work sat in line

[8:53] behind one laptop. That's not a user problem. That's our problem. 4 days later, we had a real fix. A fair launch queue. Now starting a task gives you a place in line and the dispatcher started when there's room. People

[9:12] sitting at keyboard goes first. Everyone gets a fair share and can borrow more than the cluster is quite. And whenever you start a task, you can see a placing line. When we hit it with a 300 task burst in low test, the task

[9:28] lit went from almost 2 seconds to 70 milliseconds. So did it work? When it's the busiest day of every week back in August, two certain task and about one in 10 didn't finish.

[9:45] Then in November 4th, more than twice that and much better in the finish line, but we still have some room to grow. I will be modest, we change several things at once, so I cannot tell you which fix mattered the most, but the

[10:01] birds kept getting bigger and the platform kept up. And just when that was on the crunch show, the model neck moves. At the end of the October, our dev platform team raised an alarm. PRS

[10:16] across the company had jumped around 60% in a single month. A merge that used to take 15 to 30 minutes was taking over an hour now. And merge Q kept having to be switched off. So now a PR rebase onto main rerun CI and merge if it's green.

[10:37] If main breaks everyone CI breaks with it. Alterately we haven't cracked this one yet. But before I go there's one more thing. While we were busy fixing all it something else was quite growing. Most

[10:55] of what I've been showing you start with a person asking. The fastest growing source of the work on Spectre doesn't these are automations agent that wake up on schedule on an event and just do the work tri alert

[11:13] read the PR write the post. Last month about 110 people had automation running and we learned to give them a guardrail on day one. If one fails five times in a row, it switch itself off and it can carry a

[11:30] budget or expiry date because when no one's watching, an agent can start thousands of tasks, too. So, here's what I'm chasing next, and I don't have an answer yet, honestly. What if every Slack channel had its own

[11:46] agent that never locks off? One that follows competition and start work on its own. What if every pure prove it works before a human even look at it? Today only one merge in 20 carries that kind of proof.

[12:03] And how do you merge when agents never stop opening PRs? Ask me again 6 months. I will tell you what broke. If you're building something like this when you work, here's three things I do again. Oh, what happens

[12:19] after code is written. Make Eric action something an agent can call and cap what an agent, human or alert can start before they find out what they can do with it. And one last thought, that's my own

[12:36] view. Engineers can write code with whichever agent they like. The work that's lost is the harness that runs it, checks it, and get it merged. Thank you so much for watching. Come find me on linking if you are

[12:53] building similar things.
