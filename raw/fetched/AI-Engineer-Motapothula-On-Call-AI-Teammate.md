---
title: Give Your On-Call Its Own AI Teammate — Meta
description: AI Engineer CODE 2026 官方閱讀版，Meta 三位工程師談每個值班輪替配一個 AI 隊友、自主階梯與團隊記憶，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-meta-oncall
published: 2026-11-11
tags:
  - clippings
  - ai-agent
  - automation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 on-call 被辨識成 uncle）。逐字稿對應 Day 1 直播 `https://www.youtube.com/watch?v=ZZ19zhYnDKY`（約 1:58:35–2:14:14）。講者：Swaapnika Motapothula、Chinmay Gandhi、Vlad Tsvang（Meta）。

## From answering the page to sharing the on-call rotation

Twelve alerts arrive at two in the morning. An assistant can help explain a latency spike, inspect a deployment, and read a runbook. Someone still has to decide which alert matters, ask each question, connect the answers, and carry out the follow-up.

Chinmay Gandhi

**Meta**

Swaapnika Motapothula

**Meta**

Vlad Tsvang

**Meta**

Day 1 livestream · [1:58:35–2:14:14 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7115s). The player starts and stops at this session’s boundaries.

## Introduction

Twelve alerts arrive at two in the morning. An assistant can help explain a latency spike, inspect a deployment, and read a runbook. Someone still has to decide which alert matters, ask each question, connect the answers, and carry out the follow-up.

The Meta team opens with that distinction. Their simplified incident example already has capable AI on the left-hand side. What it lacks is continuity: the assistant waits to be asked, then goes dormant after answering. The person on call remains the coordinator.

On the other side of the example, an AI teammate has started before the person wakes up. It has grouped related signals, assembled a hypothesis, and prepared a fix for review. The point is not that the human disappears. The human starts with a decision to make rather than an investigation to assemble from scratch.

[2:01:49 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7309s)

## One rotation needs one continuing context

The [organizational problem](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7309s) is a collection of competent silos. An alert script knows that latency rose. A ticket bot knows customers are reporting a slowdown. A deployment tool knows a configuration changed. Incident history contains earlier examples.

Every clue exists somewhere. If each automation owns only its slice and forgets the rest, the person on call must connect them every time.

The proposal is one teammate per rotation: a continuing loop across signals, memory owned by the team, a distinct identity, and a human gate for consequential decisions. Underneath, the agent is a model calling tools and reading feedback. Most of the engineering is the system around that loop, which determines what it may do and how long it can safely keep running.

[2:03:25 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7405s)

## Earn autonomy one action at a time

The [autonomy ladder](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7405s) resembles onboarding an engineer to on call. First investigate without changing anything. Then draft actions for approval. Only later handle lower-criticality work without requiring a person to drive each step.

[![Three source-slide steps show advise, act with approval, and autonomous lower-criticality work, with high-criticality decisions retained by humans.](https://ai.engineer/reading/code-2026/images/online-meta-oncall-7460.jpg)](https://ai.engineer/reading/code-2026/images/online-meta-oncall-7460.jpg)

*At [02:04:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7460s), the ladder's conditions are explicit: mistakes should be cheap, detectable, and backed by a track record on that particular action.*

The unit of trust is the action, not the agent's general reputation. Closing a noisy alert and performing a production mitigation have different consequences. An agent that has handled the former reliably has not thereby earned permission for the latter.

At the first level, the agent investigates and provides a root-cause analysis. At the second, it drafts a fix and test plan, responds to review comments, and repairs CI failures. Human approval still gates production changes. The speakers emphasize that many drafts do not land; review is doing its job by filtering them.

The third level targets the number of items demanding attention. A better explanation for every alert is helpful, but it can leave the same pile of alerts waiting for a human. Handling duplicates, noisy signals, and routine low-risk work reduces that pile. Critical incidents remain human-owned, with the evidence and proposed action ready when the person arrives.

[2:05:30 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7530s)

## A decision queue should travel to the person

The talk's [board and digest example](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7530s) distinguishes work that needs a decision, work already handled, and work still in progress. Those are different states and should not all become notifications.

The morning digest summarizes resolved routine work and gives each item needing attention a concrete next step. In the incident interface, a person can ask for evidence or a regional breakdown without reconstructing the whole context. A rollback can be drafted in the same conversation while approval remains a separate step.

These examples show the desired interaction, not measured time savings. The speakers later say they want a rigorous study before putting a number on reduced on-call load.

[2:08:01 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7681s)

## Unattended work needs maintenance of its own

The system is built around three [automation responsibilities](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7681s): investigate new signals, keep runs healthy, and hand off the shift.

[![Source architecture groups investigation, scheduled self-repair, and shift handoff, with each path returning useful work or escalation.](https://ai.engineer/reading/code-2026/images/online-meta-oncall-7725.jpg)](https://ai.engineer/reading/code-2026/images/online-meta-oncall-7725.jpg)

*At [02:08:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7725s), maintaining the automation is a separate path. A quiet agent is not necessarily a healthy one.*

New alerts, tasks, and failures route to appropriate investigators or coding agents. Scheduled maintenance looks for stuck runs, failed work, and broken schedules, retrying or repairing when it can and escalating when it cannot. Handoffs summarize what happened and notify the next person on call.

Teams can supply agents and skills they already trust. The common system provides the continuing loop; the team's runbooks, memory, and tools provide the expertise. Logged trajectories let another engineer inspect a run or resume the conversation rather than accept an opaque conclusion.

[2:10:10 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7810s)

## Memory belongs to the team and must stay correctable

The [shared-memory example](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7810s) follows knowledge from one shift to another. An engineer teaches the agent how to respond to a particular configuration-related timeout. A later engineer encounters the same pattern and receives a proposed fix with its source.

That is useful only if memory can change. The speakers describe retrieving relevant entries, evaluating whether they helped, and promoting or retiring them. A correction reopens the item and becomes input to future behavior. The agent should not preserve a mistaken instruction merely because someone once wrote it confidently.

The same separation supports reuse across teams: common infrastructure, but per-rotation identity, configuration, permissions, and memory. Adding a rotation becomes configuration rather than another fork of the product.

The next steps stay tied to evidence. Grade proposed mitigations by their outcomes, make it easier to turn team knowledge into skills, measure time saved, and earn permission for more consequential work. The intended change in the human's job is specific: less time joining clues and shepherding routine tasks, more time making the decisions that still require judgment.

Full transcript 339 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[1:58:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7118s) and Vlad. We're excited to share our

[1:58:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7120s) journey as well as our learnings around

[1:58:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7123s) building an AI on call teammate at Meta

[1:58:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7126s) that now runs real on call rotations

[1:58:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7128s) every day and around the clock.

[1:58:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7131s) We are part of the engineering team that

[1:58:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7133s) builds the tooling platform and

[1:58:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7135s) infrastructure for incident response on

[1:58:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7138s) call experience and mitigations at meta.

[1:59:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7141s) That space is evolving rapidly with the

[1:59:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7144s) increase in AI capabilities.

[1:59:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7147s) AI changed how fast we write code. About

[1:59:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7150s) 3/4 of new code is now written with AI.

[1:59:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7153s) And more AI generated changes reach

[1:59:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7156s) production every single day. And some of

[1:59:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7159s) it can cause production failures just

[1:59:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7162s) like any other code change can.

[1:59:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7165s) But on call did not speed up with it.

[1:59:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7168s) Highquality code can pass review and

[1:59:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7171s) still break in production. and when it

[1:59:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7173s) does, someone still gets paged at 2 a.m.

[1:59:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7176s) The bottleneck moved from writing code

[1:59:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7178s) to operating it in production. And on

[1:59:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7182s) call is where that operational load

[1:59:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7184s) lands. So we asked if AI is writing the

[1:59:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7188s) code, can AI also help operate it?

[1:59:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7193s) And we think it can. Now let's quickly

[1:59:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7197s) run through one of those on call pages

[1:59:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7199s) with a simplified example.

[2:00:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7202s) It's 2:00 a.m. and 12 alerts are firing.

[2:00:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7205s) Same night, it can go two different

[2:00:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7207s) ways. On the left is how most of us do

[2:00:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7209s) this today. And notice we already have

[2:00:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7212s) good AI. First, you sort the alerts by

[2:00:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7215s) yourself. Checkout, payments, disk,

[2:00:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7218s) which one to pick first. Let's say you

[2:00:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7219s) pick checkout. Then you ask your

[2:00:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7222s) assistant why P99 latency is high.

[2:00:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7226s) It's genuinely useful. It pulls the

[2:00:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7227s) metrics and finds the deployment at 149.

[2:00:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7231s) And when you ask, it reads what changed

[2:00:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7234s) and checks the runbook.

[2:00:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7236s) It figured out that the time config was

[2:00:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7238s) changed to a lower value. And based on

[2:00:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7241s) the runbook, it suggests to roll back,

[2:00:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7244s) which is all very helpful. However, if

[2:00:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7247s) you look at the shape of it, it waited

[2:00:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7249s) to be asked.

[2:00:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7251s) You picked every next step. You were the

[2:00:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7254s) glue between the questions and once it

[2:00:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7258s) answered, it went dormant.

[2:01:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7260s) At 239, you know the cause, but the roll

[2:01:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7265s) back, the changes, and the follow-ups

[2:01:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7267s) are still yours.

[2:01:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7270s) Now, on the right, the same 12 alerts,

[2:01:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7274s) but an AI teammate started before you

[2:01:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7277s) woke up. It had already ranked them.

[2:01:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7281s) Checkouts first, payments merged in as

[2:01:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7284s) the same cause, and the other 10 handled

[2:01:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7286s) separately.

[2:01:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7288s) It read the dashboards, difficed

[2:01:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7293s) two past incidents.

[2:01:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7295s) You get a hypothesis, a 30-cond way to

[2:01:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7299s) verify it, and a fix waiting for your

[2:01:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7302s) review. At 2011, you verified it and

[2:01:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7306s) you're back to sleep. That gap is what

[2:01:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7309s) this talk is about.

[2:01:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7313s) So why were you the glue?

[2:01:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7316s) Every team was bolting automation onto

[2:01:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7318s) on call one silo at a time. An alert

[2:02:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7323s) script for alerts, a triage bot for

[2:02:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7325s) tickets, a deploy bot for deploys, a fix

[2:02:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7328s) it agent for incidents.

[2:02:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7330s) Each one solves its slice, keeps its own

[2:02:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7333s) context, and forgets it. Now replaying

[2:02:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7336s) your 2 AM page, the alert script saw P99

[2:02:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7340s) latency above 2 seconds. The triage bot

[2:02:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7343s) saw three tickets saying checkout is

[2:02:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7345s) slow. The deploy bot knew about a config

[2:02:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7348s) change at 149 and the incident history

[2:02:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7350s) had two similar past incidents. Every

[2:02:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7353s) clue existed,

[2:02:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7355s) but nothing connected them. So the on

[2:02:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7359s) call became the glue exactly

[2:02:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7362s) as we saw on the left side of the

[2:02:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7364s) previous slide.

[2:02:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7366s) Our bet was one AI teammate per rotation

[2:02:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7370s) instead.

[2:02:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7372s) One loop across every signal, one team

[2:02:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7375s) memory that learns every shift, its own

[2:02:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7378s) identity so it acts as itself and a

[2:03:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7381s) human gate so you approve instead of

[2:03:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7383s) operate. But giving one agent all that

[2:03:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7387s) context and reach raises the stakes.

[2:03:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7389s) Which is why autonomy has to be earned.

[2:03:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7395s) Under the hood, the teammate or the AI

[2:03:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7398s) teammate is the simplest agent. There is

[2:03:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7401s) model using tools in a loop acting on an

[2:03:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7404s) environment and reading the feedback.

[2:03:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7407s) Everything else in this talk is what we

[2:03:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7409s) \[music\] build around that loop to make

[2:03:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7412s) it safe to leave it running. And for

[2:03:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7415s) that I will hand over to Swapnikai and

[2:03:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7417s) Vlad next to get into the actual details

[2:03:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7420s) of how it works.

[2:03:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7423s) To achieve this we started with an

[2:03:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7425s) autonomy ladder. Think about how you

[2:03:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7427s) onboard a new engineer to on call. First

[2:03:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7430s) the shadow. The investigators suggest

[2:03:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7433s) but they don't touch production. Then

[2:03:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7436s) the pair the right to fix and another

[2:03:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7439s) engineer approves it. With time they

[2:04:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7441s) gain knowledge. We give our agent

[2:04:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7444s) exactly the same ladder. At level one,

[2:04:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7447s) it investigates and tells you what it

[2:04:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7449s) found. It changes nothing. At level two,

[2:04:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7452s) it acts with approval. It drafts the

[2:04:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7454s) fix, but nothing reaches production

[2:04:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7456s) until a human approves. At level three,

[2:04:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7459s) it clears lower criticality work on its

[2:04:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7462s) own and only interrupts you for what

[2:04:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7464s) matters. High criticality work stays

[2:04:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7467s) with humans.

[2:04:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7469s) So what earns the next run? We use a

[2:04:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7472s) simple test. How costly is a mistake and

[2:04:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7475s) how easy is it to catch? So an action

[2:04:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7478s) climbs only when mistakes are cheap.

[2:04:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7481s) They're caught by tests, CI or review.

[2:04:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7485s) and the agent already has a track record

[2:04:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7487s) on that exact action. That's why the

[2:04:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7490s) agent can close a noisy alert on its own

[2:04:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7493s) while a production mitigation still

[2:04:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7495s) waits for a human.

[2:04:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7498s) At level one, the investigation is

[2:05:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7500s) layered and stops at the first confident

[2:05:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7502s) answer. The agent investigated the issue

[2:05:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7505s) using the team's memory and runbook. It

[2:05:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7508s) also shared the root cause analysis, but

[2:05:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7510s) human had to apply the fix.

[2:05:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7513s) At level two, it writes the fix with the

[2:05:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7517s) root cause and a test plan. It answers

[2:05:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7520s) reviewer's comments and fixes CI, but

[2:05:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7523s) nothing reaches production until a human

[2:05:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7525s) approves.

[2:05:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7526s) Most drafts don't land, and that's fine.

[2:05:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7530s) Review is the filter. At both levels,

[2:05:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7533s) the agent does the homework, but you

[2:05:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7536s) still had to grade every single paper.

[2:05:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7539s) The help got much better, but the tasks

[2:05:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7542s) requiring human input didn't get

[2:05:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7544s) smaller. Level three shrinks the pile.

[2:05:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7550s) Look at this example. 23 items came in,

[2:05:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7553s) but only three need you. On the right,

[2:05:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7557s) the agent handled the long tail, noisy

[2:05:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7559s) alerts, duplicates, routine fixes that

[2:06:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7562s) went through normal review and CI. Two

[2:06:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7565s) more are still being worked. You don't

[2:06:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7568s) have to drive each one to completion. In

[2:06:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7571s) the middle is your much smaller decision

[2:06:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7573s) queue. Each item makes clear what it

[2:06:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7577s) needs from you with a run this button

[2:06:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7579s) that has a call to action. And remember

[2:06:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7582s) our 2 a.m. check out page that still

[2:06:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7585s) stays human owned. The agent brings the

[2:06:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7587s) investigation. The human owns the

[2:06:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7590s) critical decision. It's the new high

[2:06:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7592s) ladder again. Trusted to handle routine

[2:06:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7595s) work, ready with the homework when it

[2:06:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7597s) needs help. Not just less work per item,

[2:06:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7600s) but fewer items waiting on you.

[2:06:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7605s) That board is where the work lives. But

[2:06:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7607s) nobody stares at a board all the time,

[2:06:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7610s) right? So the agent is also available

[2:06:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7612s) across many surfaces like chat and

[2:06:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7615s) native incident surfaces. At 9 every

[2:06:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7618s) morning, it posts a digest. 23 came in,

[2:07:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7622s) three need you, 18 handled. Each thing

[2:07:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7626s) that needs you come with a one-click

[2:07:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7628s) next step. So approving the quota bump

[2:07:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7632s) takes one tap from your phone. The 18 it

[2:07:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7635s) handled are summarized, not listed. And

[2:07:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7638s) the two that are still in progress tell

[2:07:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7640s) you what it's doing about them. And when

[2:07:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7643s) you want to dig in, you just reply in

[2:07:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7645s) the thread. As you see on the right

[2:07:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7648s) here, you open the checkout incident and

[2:07:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7650s) ask for the evidence. It already has it.

[2:07:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7654s) Errors start at 8:41, 2 minutes after a

[2:07:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7657s) config push cut the payment client

[2:07:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7659s) timeout. The same pattern as two past

[2:07:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7661s) incidents. You ask a follow-up, is it

[2:07:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7664s) only EU? And it answers with a

[2:07:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7666s) breakdown. It drafts the roll back. You

[2:07:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7669s) approve it right there and errors start

[2:07:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7672s) recovering. You never opened a dashboard

[2:07:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7674s) and you never had to explain the context

[2:07:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7677s) because it was already there. That's

[2:07:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7679s) what a teammate feels like. A morning

[2:08:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7681s) hand off a colleague you can ask.

[2:08:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7686s) Now under the hood of this AI teammate,

[2:08:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7689s) it's AI automations. The first

[2:08:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7692s) investigates on every new signal auto

[2:08:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7695s) triage classifies it, checks its

[2:08:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7698s) criticality and kicks off the right

[2:08:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7700s) agent. An alert goes to the incident

[2:08:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7703s) investigator, a task to the team's own

[2:08:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7705s) agent, a test failure to a coding agent,

[2:08:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7709s) a look up to memory and code search.

[2:08:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7712s) The second keeps the system healthy.

[2:08:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7715s) Unattended automation fails quietly. So

[2:08:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7719s) on a schedule, it looks for stuck or

[2:08:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7721s) failed runs, retrace and repairs broken

[2:08:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7724s) schedules, and it only pages a human if

[2:08:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7727s) it can't fix it itself.

[2:08:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7730s) Nothing stalls silently.

[2:08:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7733s) The third hands off at every shift

[2:08:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7736s) change and every morning at 9, it

[2:08:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7738s) summarizes the shift. What needs you

[2:09:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7740s) with the fix ready and what it handled

[2:09:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7743s) on its own posted to the team chat. Not

[2:09:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7746s) only in the morning, but every urgent

[2:09:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7748s) issue that needs user attention gets

[2:09:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7750s) notified in chat with findings and draft

[2:09:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7753s) fixes. It also tags the next on call in

[2:09:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7755s) the chat during handoff. The entire

[2:09:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7758s) cycle still continues

[2:09:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7763s) and because it belongs to the team, it

[2:09:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7766s) runs the agents and the skills the team

[2:09:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7768s) already trusts. That's the slot in the

[2:09:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7770s) middle. Bring your own agent, add your

[2:09:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7773s) own skills. If a team already has an

[2:09:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7776s) agent that has the team's runbooks and

[2:09:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7778s) the knowledge base, the automations

[2:09:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7780s) leverage it. Alongside that, it has our

[2:09:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7783s) own incident investigator and a deep

[2:09:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7785s) dive coding session.

[2:09:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7788s) Work comes in from alerts, tickets,

[2:09:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7791s) incidents, team posts, and chat. The

[2:09:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7795s) agent itself is generic. What makes it

[2:09:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7797s) good at an on call rotation is the

[2:09:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7799s) team's agents skills, memory, and

[2:10:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7802s) playbook. And every run is logged, so

[2:10:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7805s) anyone on the team can inspect the

[2:10:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7808s) trajectory or resume the conversation.

[2:10:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7811s) Now, I'm handing off to my teammate Vlad

[2:10:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7813s) to talk more on the shared agent.

[2:10:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7819s) An uncle agent can't belong to just a

[2:10:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7821s) single person because the uncle itself

[2:10:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7823s) doesn't. So it belongs to the team.

[2:10:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7826s) There's one teammate per rotation on one

[2:10:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7829s) board. Wherever's on call can ask it to

[2:10:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7832s) correct it or pick up its work mid

[2:10:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7833s) investigation. It carries the team's

[2:10:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7836s) uncle expertise, the playbook, lord

[2:10:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7838s) profiles and past decisions from one

[2:10:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7840s) shift to the next one the way a good

[2:10:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7842s) handoff should. Here's what that looks

[2:10:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7845s) like. Monday at 2 am, Sam is on call and

[2:10:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7848s) tells it remember if checkout time is

[2:10:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7851s) out after a config push, roll back the

[2:10:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7853s) config first. It saves it to the memory.

[2:10:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7857s) Three days later, Jordan is on call hits

[2:11:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7860s) the exact same alert and just asks for a

[2:11:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7863s) fix. The agent answers with some fix,

[2:11:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7866s) says where it came from, and has the

[2:11:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7868s) roll back drafted. Teach it once, the

[2:11:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7871s) next phone call gets it.

[2:11:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7874s) And it access the team its own identity

[2:11:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7877s) owned by the rotation with only the

[2:11:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7879s) access the team is comfortable granting

[2:11:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7881s) it.

[2:11:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7884s) And it learns from every uncle shift.

[2:11:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7886s) Handoffs, decisions, and corrections all

[2:11:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7889s) flow into memory. So ship number 30 is

[2:11:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7892s) better than the ship number one. The

[2:11:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7894s) same way a new uncle gets better every

[2:11:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7896s) week. But memory erodess over time. So

[2:11:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7900s) ours has to earn its place. It retrieves

[2:11:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7903s) semantically uses what it finds, scores

[2:11:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7906s) where it actually helped and promotes or

[2:11:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7909s) retires entries automatically.

[2:11:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7912s) When someone says that was wrong, the

[2:11:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7914s) item reopens and the correction becomes

[2:11:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7916s) memory.

[2:11:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7919s) Three things made this work beyond our

[2:12:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7921s) team.

[2:12:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7922s) First, a loop that never stops

[2:12:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7925s) listening. Every piece of feedback or

[2:12:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7927s) course correction reopens the item and

[2:12:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7929s) ultimately gets absorbed into memory.

[2:12:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7932s) Feedback is an input to the system, not

[2:12:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7935s) a story read once a quarter. Second,

[2:12:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7938s) customize instead of forking. Teams

[2:12:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7942s) bring their own playbooks and skill

[2:12:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7944s) workflows, and it's still the same

[2:12:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7946s) teammate underneath.

[2:12:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7948s) Third, what we call one rotation to end.

[2:12:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7952s) Identity, config, and memory are per

[2:12:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7954s) team. So, add a rotation becomes a

[2:12:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7957s) setup, not a new project.

[2:12:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7959s) The agent is generic while the expertise

[2:12:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7961s) is owned by the team.

[2:12:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7965s) So what has changed for the people on

[2:12:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7967s) call? Well, first their job shifted from

[2:12:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7970s) driving deep investigations to making

[2:12:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7972s) key decisions. They start from a

[2:12:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7974s) hypothesis with linked evidence, not a

[2:12:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7976s) blank task or dashboard.

[2:12:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7979s) Second, the load is getting lighter.

[2:13:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7982s) Early signs of on call load reduction

[2:13:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7984s) are promising for teams that run it

[2:13:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7986s) automatic autonomously and we want to

[2:13:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7988s) measure it rigorously before we put a

[2:13:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7990s) number on it.

[2:13:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7992s) And the third every change that agent

[2:13:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7994s) writes still meets a human. Fixes land

[2:13:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7998s) only through normal review and

[2:13:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8000s) continuous integration. And most drafts

[2:13:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8002s) don't land. That's the point. Review is

[2:13:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8005s) the filter.

[2:13:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8007s) Uncle stops being attacks and becomes a

[2:13:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8009s) review cube. Here's

[2:13:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8012s) what we're focusing on next. First,

[2:13:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8015s) mitigations that get approved, not just

[2:13:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8017s) drafted. We great every mitigation that

[2:13:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8020s) agent proposes and feed the outcome back

[2:13:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8022s) so it earns its next level instead of

[2:13:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8024s) being handed it. Second, skills are

[2:13:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8027s) written from the chat so a team can turn

[2:13:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8030s) its runbooks into skills without writing

[2:13:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8032s) any code. And third, measuring the time

[2:13:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8035s) we give back properly with a rigorous

[2:13:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8037s) study of uncall time saved rather than

[2:13:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8039s) usage counts.

[2:14:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8041s) And the next rung on the ladder is uh

[2:14:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8044s) earning medium criticality autonomy with

[2:14:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8047s) evidence. On that, thank you so much for

[2:14:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8050s) listening to us and hopefully that was

[2:14:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=8052s) helpful. Bye.
