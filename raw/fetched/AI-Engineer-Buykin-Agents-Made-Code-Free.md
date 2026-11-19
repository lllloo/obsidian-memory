---
title: Agents Made Code Free. Maintaining It Didn't Get Cheaper. — Dmitry Buykin
description: AI Engineer CODE 2026 官方閱讀版，Buykin（Maersk）談每週小幅修剪、專家決策表與真實任務重播，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-dmitry-maintenance
published: 2026-11-11
tags:
  - clippings
  - coding-agent
  - ai-agent
  - testing
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 prose 被辨識成 pros、write 被辨識成 right）。逐字稿對應官方單場重錄版 YouTube 影片 `oeknLUsN_GE`（`https://www.youtube.com/watch?v=oeknLUsN_GE`，上傳日 2026-11-11，長 18:03）。

Official replacement recording · [0:00:00–0:18:03 on YouTube](https://www.youtube.com/watch?v=oeknLUsN_GE&t=0s). The player starts and stops at this session’s boundaries.

## Introduction

**Dmitry Buykin**, Maersk, replaces periodic destructive rewrites with smaller, evidence-driven maintenance loops that people can still understand.

*This reading edition uses the complete official standalone recording, which restores the ending missing from the livestream excerpt. Links below use its clock.*

Buykin once dealt with an expanding AI-written project by deleting unused tests and boilerplate, then rewriting the whole thing. Useful pieces disappeared with the mess. Worse, the rewrite did not solve the process that created it: agents kept adding code, and complexity grew back.

His Thanos analogy is deliberately uncomfortable. Keep everything and drown in accumulated change, or delete aggressively and break something people use. The third option is less dramatic: small weekly sweeps, bounded changes, and feedback loops that preserve evidence of what should survive.

[0:01:34 ↗](https://www.youtube.com/watch?v=oeknLUsN_GE&t=94s)

## Decide who knows what correct means

At [00:01:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=94s), Buykin introduces a recurring task: changing the amount on an already approved order. Coding agents maintain the instructions; runtime agents follow them in production. A task belongs to a slice defined by a process and a country, and changes stay within that slice by default.

Much of the system consists of prose instructions rather than conventional code. Buykin tried deliberately breaking sentences to see whether tests noticed. Many did not. Passing tests could not tell him whether the business instructions still meant the right thing.

The expertise is distributed. Business specialists know the rules; developers investigate the traces, available data, and connections between systems. A request to check with a team might describe a decision that must remain human, or a step that could be automated once the relevant facts are available. Neither group can decide that alone.

The result is one document for two kinds of readers. Agents consume precise structured portions; experts read the surrounding explanation and approve it. Maintaining a second, separate account would create another opportunity for drift. Experts also need plain-language explanations of code so they can recognize a wrong outcome and turn it into a concrete correction.

[0:05:13 ↗](https://www.youtube.com/watch?v=oeknLUsN_GE&t=313s)

## Turn repeated paths into tools, but keep the decisions visible

At [00:05:13](https://www.youtube.com/watch?v=oeknLUsN_GE&t=313s), the order example exposes a contradiction: prose and code disagree about the allowed limit. No compiler necessarily complains. The agent simply encounters inconsistent instructions.

Buykin adds linting and tracks the paths agents take through the instructions. A path that repeats consistently across countries can become a workflow tool. The first attempt made things worse because the old prose still described the steps now inside the tool. Agents performed those steps again.

The repair was to remove the duplicated procedure and retain the decisions. Code prepares facts and performs actions. Experts own the decision table. The model chooses the applicable row, and a person takes over when no row fits.

[![The order decision table sends an over-limit request to a team lead, an in-limit request to confirmation, and unmatched cases to a person.](https://ai.engineer/reading/code-2026/images/online-dmitry-maintenance-standalone-410.jpg)](https://ai.engineer/reading/code-2026/images/online-dmitry-maintenance-standalone-410.jpg)

*At [00:06:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=410s), the same order passes through preparation, expert-owned decisions, and execution. The visible example uses an amount of 1,250 against a 1,000 limit.*

This is not a one-way migration from prose to code. Buykin also moves complicated expressions out of code when experts cannot read them. Stable mechanics belong in code; variable judgment must remain somewhere the responsible person can inspect. He explicitly describes a further composition of small model decisions and workflows as a next step not yet built.

[0:07:18 ↗](https://www.youtube.com/watch?v=oeknLUsN_GE&t=438s)

## Control what the agent sees and what a write can do

At [00:07:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=438s), control begins before permission checking. When an agent could load everything, it invented a pricing check because prices happened to be available. More context gave it another reason to act, not necessarily a better reason.

The runtime now selects the facts needed for the decision. It retains the full record and gives the model a smaller representation. For large data, the model passes a handle to information held by the runtime rather than copying the whole object into context. The runtime checks that handle before a write and validates consistency.

Buykin layers checks around actions as well as around development changes. A journal prevents a retried write from executing twice when an earlier attempt appeared to fail. Permission at the outer edge is only one part of controlling the effect of an agent's decision.

[0:09:24 ↗](https://www.youtube.com/watch?v=oeknLUsN_GE&t=564s)

## Protect the reviewer as well as the system

The system had guardrails, but its architect was still becoming a bottleneck. At [00:09:24](https://www.youtube.com/watch?v=oeknLUsN_GE&t=564s), Buykin describes reading every change until the volume exceeded his attention. A green dashboard did not mean he could explain what had happened.

He treats that inability as a signal to repair the process, rather than waiting for a more convenient metric. Instrumentation helps identify where deeper reading is worth the time: abrupt changes, wider effects, or clusters of similar failures across process-country slices.

An expert's correction becomes an evaluation case. An agent searches related slices for the same failure, but fixes only the places where the failure is confirmed. Markets and laws differ intentionally; copying a repair everywhere would erase valid variation.

To stop himself becoming the message bus, Buykin gives users a way to evaluate outcomes and records each loop in a ledger. Session memory moves into files that distinguish what happened from what is currently true. A new agent should begin from the current state rather than reconstructing it from a pile of unresolved historical events.

[0:13:08 ↗](https://www.youtube.com/watch?v=oeknLUsN_GE&t=788s)

## A green result needs evidence behind it

The recovered ending, beginning around [00:13:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=788s), makes verification the limiting resource. Buykin ranks evidence by what it proves and places replay of real tasks above a generic success signal. Before results arrive, he writes down what would disprove the change. A new check must be made to fail intentionally before he trusts it.

[![A before-and-after branch diagram marks a lost over-limit branch and blocks the refactor.](https://ai.engineer/reading/code-2026/images/online-dmitry-maintenance-standalone-840.jpg)](https://ai.engineer/reading/code-2026/images/online-dmitry-maintenance-standalone-840.jpg)

*The [diagram at 14:00](https://www.youtube.com/watch?v=oeknLUsN_GE&t=840s) follows the order example through a refactor. Losing the over-limit branch would bypass the team lead, even if other branches still worked.*

Real tasks become a frozen replay set for comparing old and new versions. If no task exercises a branch, the status is missing evidence, not demonstrated correctness. A second agent reviews against a checklist without the author's reasoning, reducing the chance that a persuasive explanation substitutes for checking.

The ledger also reveals incomplete batches. Agents can finish many items and silently leave others behind, particularly when context fills up. Counting apparent coverage is weaker than counting items whose closure has supporting evidence.

## Prune the behavior, including its tests

The last maintenance loop addresses regrowth. Real use determines which variants still matter. An unreachable path gets a name and an evidence trail before removal. When a variant is retired, tests that preserve that obsolete variant must retire with it; otherwise agents will continue treating the tests as instructions to keep the behavior alive.

Buykin describes current and planned gauges separately. The aim is a ratchet that prevents complexity from quietly growing past the reviewable limit, applied in small amounts every week rather than in one destructive rewrite.

He closes with a consequence of teaching agents through correction: the system absorbs the habits and biases of whoever corrects it. Its skills and memory can preserve an engineer's judgment, including the parts worth questioning. His checklist is an invitation to inspect that inheritance while the team can still understand each change, before another dramatic cleanup feels like the only remaining option.

Full transcript 353 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[0:00:00](https://www.youtube.com/watch?v=oeknLUsN_GE&t=0s) Hi, I'm Dimmitri. In this session, I

[0:00:03](https://www.youtube.com/watch?v=oeknLUsN_GE&t=3s) will show how I work on maintaining

[0:00:05](https://www.youtube.com/watch?v=oeknLUsN_GE&t=5s) large AI coding projects. Coding agents

[0:00:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=8s) made code cheap. They made entropy even

[0:00:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=12s) cheaper. In the Marvel movie, Thanos

[0:00:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=15s) watched his home planet Titan collapse

[0:00:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=18s) under its own growth. So, when the

[0:00:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=20s) universe got crowded, he raised half of

[0:00:23](https://www.youtube.com/watch?v=oeknLUsN_GE&t=23s) everything. This talk is about the one

[0:00:26](https://www.youtube.com/watch?v=oeknLUsN_GE&t=26s) time I did the same in one project. Our

[0:00:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=30s) code was growing the way Titan did. When

[0:00:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=32s) I found what my agents had done, I

[0:00:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=36s) deleted tests and boil the plate code

[0:00:40](https://www.youtube.com/watch?v=oeknLUsN_GE&t=40s) nobody used. I had to rewrite the whole

[0:00:43](https://www.youtube.com/watch?v=oeknLUsN_GE&t=43s) project and I lost some useful pieces.

[0:00:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=46s) And that's the dilemma. Drown and chaos

[0:00:49](https://www.youtube.com/watch?v=oeknLUsN_GE&t=49s) or break what people use. And here we'll

[0:00:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=53s) build the third option for that project.

[0:00:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=56s) The rewrite didn't hold. The agents kept

[0:01:00](https://www.youtube.com/watch?v=oeknLUsN_GE&t=60s) writing and the mess grew back. So I

[0:01:03](https://www.youtube.com/watch?v=oeknLUsN_GE&t=63s) drew a line above it. There is more

[0:01:06](https://www.youtube.com/watch?v=oeknLUsN_GE&t=66s) change than anyone can check. The third

[0:01:09](https://www.youtube.com/watch?v=oeknLUsN_GE&t=69s) option is to stay under it with small

[0:01:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=72s) sweeps every week and feedback loops

[0:01:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=75s) built into the system. Each chapter of

[0:01:17](https://www.youtube.com/watch?v=oeknLUsN_GE&t=77s) this talk is one thing I had to learn to

[0:01:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=79s) get there. Thanos needed six stones for

[0:01:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=82s) one snap. Ours are six questions and

[0:01:26](https://www.youtube.com/watch?v=oeknLUsN_GE&t=86s) they light up in the corner as we go.

[0:01:29](https://www.youtube.com/watch?v=oeknLUsN_GE&t=89s) The first one is time. How do we stay

[0:01:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=92s) under the line?

[0:01:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=94s) Chapter one. To stay under the line. I

[0:01:37](https://www.youtube.com/watch?v=oeknLUsN_GE&t=97s) first had to know what's right means

[0:01:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=99s) here. I used to think that tests decide

[0:01:42](https://www.youtube.com/watch?v=oeknLUsN_GE&t=102s) that. So what does right actually depend

[0:01:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=106s) on?

[0:01:48](https://www.youtube.com/watch?v=oeknLUsN_GE&t=108s) Let's keep one task in mind. Someone

[0:01:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=110s) wants to change the amount on an order

[0:01:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=113s) we already approved. Two kinds of agents

[0:01:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=116s) meet here. One wrote the instructions

[0:01:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=119s) and the other follows them in

[0:02:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=121s) production.

[0:02:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=124s) We run this in 110 countries with about

[0:02:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=127s) 10,000 scenarios of pros instructions.

[0:02:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=131s) Every task lands in a slice. One process

[0:02:14](https://www.youtube.com/watch?v=oeknLUsN_GE&t=134s) in one country. There's a second stone

[0:02:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=138s) space. It asks where a change is allowed

[0:02:21](https://www.youtube.com/watch?v=oeknLUsN_GE&t=141s) to go. By default, it stays inside its

[0:02:25](https://www.youtube.com/watch?v=oeknLUsN_GE&t=145s) slice.

[0:02:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=147s) Most of this system is pros about three

[0:02:29](https://www.youtube.com/watch?v=oeknLUsN_GE&t=149s) quarters by my estimate. So pros needs

[0:02:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=152s) engineering too. At start we borrowed

[0:02:35](https://www.youtube.com/watch?v=oeknLUsN_GE&t=155s) mutation testing. You break one sentence

[0:02:37](https://www.youtube.com/watch?v=oeknLUsN_GE&t=157s) on purpose and you watch for red test.

[0:02:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=161s) Here almost none turned red. And if your

[0:02:44](https://www.youtube.com/watch?v=oeknLUsN_GE&t=164s) wrapper is all code, your agent

[0:02:47](https://www.youtube.com/watch?v=oeknLUsN_GE&t=167s) instructions and your tests are your

[0:02:49](https://www.youtube.com/watch?v=oeknLUsN_GE&t=169s) pros. With agents, a rewrite is easy.

[0:02:54](https://www.youtube.com/watch?v=oeknLUsN_GE&t=174s) The hard part is knowing what has to

[0:02:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=176s) survive it. For code, tests can tell

[0:02:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=179s) you. For pros, only people can. Agents

[0:03:02](https://www.youtube.com/watch?v=oeknLUsN_GE&t=182s) can't build a complex system on their

[0:03:05](https://www.youtube.com/watch?v=oeknLUsN_GE&t=185s) own. They fix what is easy to see and

[0:03:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=188s) break consistency on the way. And people

[0:03:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=191s) also get tired. So we spend their

[0:03:13](https://www.youtube.com/watch?v=oeknLUsN_GE&t=193s) judgment only where it's needed. When

[0:03:17](https://www.youtube.com/watch?v=oeknLUsN_GE&t=197s) business asked check with the team, it

[0:03:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=200s) hides a real question. Is this a human

[0:03:23](https://www.youtube.com/watch?v=oeknLUsN_GE&t=203s) step or can we automate it? Experts

[0:03:25](https://www.youtube.com/watch?v=oeknLUsN_GE&t=205s) can't answer that. They don't see how

[0:03:28](https://www.youtube.com/watch?v=oeknLUsN_GE&t=208s) the systems connect inside. So

[0:03:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=210s) developers dig through the traces and

[0:03:33](https://www.youtube.com/watch?v=oeknLUsN_GE&t=213s) logs with their coding agents and they

[0:03:35](https://www.youtube.com/watch?v=oeknLUsN_GE&t=215s) decide which it is. In our task, the

[0:03:38](https://www.youtube.com/watch?v=oeknLUsN_GE&t=218s) team leads decision stays human. The

[0:03:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=221s) limit was data we could connect.

[0:03:45](https://www.youtube.com/watch?v=oeknLUsN_GE&t=225s) Business experts see the rules.

[0:03:47](https://www.youtube.com/watch?v=oeknLUsN_GE&t=227s) Developers see what's under the water.

[0:03:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=230s) And that's where most bugs leave. They

[0:03:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=233s) have their coding agents write those

[0:03:55](https://www.youtube.com/watch?v=oeknLUsN_GE&t=235s) links down so the runtime can check

[0:03:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=238s) them. Our guide for experts says it

[0:04:00](https://www.youtube.com/watch?v=oeknLUsN_GE&t=240s) simply business tell us what we work out

[0:04:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=244s) how. One document to readers. Agents

[0:04:09](https://www.youtube.com/watch?v=oeknLUsN_GE&t=249s) read the blogs. So their blocks have to

[0:04:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=251s) be exact. Experts read the text around

[0:04:14](https://www.youtube.com/watch?v=oeknLUsN_GE&t=254s) them and they sign it. We keep one copy,

[0:04:17](https://www.youtube.com/watch?v=oeknLUsN_GE&t=257s) a second one with drift and works both

[0:04:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=260s) ways. Our code needs a plain description

[0:04:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=262s) for experts too. Experts can only fix

[0:04:26](https://www.youtube.com/watch?v=oeknLUsN_GE&t=266s) what they can see. Each of them reviews

[0:04:29](https://www.youtube.com/watch?v=oeknLUsN_GE&t=269s) a task exactly the way the agent saw it.

[0:04:33](https://www.youtube.com/watch?v=oeknLUsN_GE&t=273s) The node becomes the next change made by

[0:04:35](https://www.youtube.com/watch?v=oeknLUsN_GE&t=275s) a coding agent and test it on the same

[0:04:38](https://www.youtube.com/watch?v=oeknLUsN_GE&t=278s) task. So right depends on people. No

[0:04:42](https://www.youtube.com/watch?v=oeknLUsN_GE&t=282s) single person knows it. A group of

[0:04:45](https://www.youtube.com/watch?v=oeknLUsN_GE&t=285s) experts decides and that's why we bring

[0:04:48](https://www.youtube.com/watch?v=oeknLUsN_GE&t=288s) them in from the start. You'll see the

[0:04:51](https://www.youtube.com/watch?v=oeknLUsN_GE&t=291s) soul stone here a lot. We take it in

[0:04:54](https://www.youtube.com/watch?v=oeknLUsN_GE&t=294s) chapter 4.

[0:04:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=296s) Chapter two. Experts correct one task at

[0:04:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=299s) a time while agents run the same pros

[0:05:02](https://www.youtube.com/watch?v=oeknLUsN_GE&t=302s) all day. We track every outcome accepted

[0:05:06](https://www.youtube.com/watch?v=oeknLUsN_GE&t=306s) or rejected. The accuracy shows us where

[0:05:10](https://www.youtube.com/watch?v=oeknLUsN_GE&t=310s) people still need to look. I used to

[0:05:13](https://www.youtube.com/watch?v=oeknLUsN_GE&t=313s) think the goal was to move everything

[0:05:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=315s) into code. So where do we still need

[0:05:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=318s) judgment? Here is our task again. The

[0:05:21](https://www.youtube.com/watch?v=oeknLUsN_GE&t=321s) pro says the limit is 1,500. The code

[0:05:25](https://www.youtube.com/watch?v=oeknLUsN_GE&t=325s) says a,000. The same order is fine in

[0:05:28](https://www.youtube.com/watch?v=oeknLUsN_GE&t=328s) one place and too high in the other and

[0:05:31](https://www.youtube.com/watch?v=oeknLUsN_GE&t=331s) nothing throws an error. Even a line

[0:05:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=334s) like do not call X teaches the model

[0:05:37](https://www.youtube.com/watch?v=oeknLUsN_GE&t=337s) that X exists. That's the third stone

[0:05:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=341s) reality. Is it true or does it only look

[0:05:44](https://www.youtube.com/watch?v=oeknLUsN_GE&t=344s) true for the model? Pros has no

[0:05:47](https://www.youtube.com/watch?v=oeknLUsN_GE&t=347s) compiler. So we built one. Then the

[0:05:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=350s) author lints every changed file into

[0:05:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=353s) ledger just like code.

[0:05:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=358s) Lind can't stop copies drifting aparts.

[0:06:02](https://www.youtube.com/watch?v=oeknLUsN_GE&t=362s) So we watched the walks. A walk is the

[0:06:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=364s) path one agent takes through the pros.

[0:06:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=367s) When agents keep walking in the same

[0:06:09](https://www.youtube.com/watch?v=oeknLUsN_GE&t=369s) path, we turn it into one workflow tool

[0:06:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=372s) and we delete the pros that walked it.

[0:06:16](https://www.youtube.com/watch?v=oeknLUsN_GE&t=376s) Our first workflow of tools made things

[0:06:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=379s) worse. The pros still named the steps

[0:06:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=382s) inside them. So agents run those steps

[0:06:25](https://www.youtube.com/watch?v=oeknLUsN_GE&t=385s) again. It worked once. The pros kept

[0:06:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=387s) only the decisions. Now a walk becomes

[0:06:31](https://www.youtube.com/watch?v=oeknLUsN_GE&t=391s) code only when it repeats and agrees

[0:06:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=394s) across countries otherwise it stays

[0:06:37](https://www.youtube.com/watch?v=oeknLUsN_GE&t=397s) pros. What still varies stays in pros

[0:06:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=401s) inside the frame. Code prepares the

[0:06:44](https://www.youtube.com/watch?v=oeknLUsN_GE&t=404s) facts and carries out the decision.

[0:06:47](https://www.youtube.com/watch?v=oeknLUsN_GE&t=407s) Experts own the decision table and the

[0:06:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=410s) model only picks a row. If no row fits,

[0:06:54](https://www.youtube.com/watch?v=oeknLUsN_GE&t=414s) a person takes over. We haven't built

[0:06:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=416s) the next step yet. The model will take

[0:06:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=418s) the small decisions and workflows will

[0:07:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=421s) connect them. This boundary moves both

[0:07:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=424s) ways. We moved hundreds of lines of

[0:07:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=427s) expressions out of code and into pros

[0:07:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=431s) because experts couldn't read them. A

[0:07:14](https://www.youtube.com/watch?v=oeknLUsN_GE&t=434s) reax is still fine for spotting a

[0:07:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=435s) critical signal. When there are many,

[0:07:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=438s) they move into config. Judgment stays

[0:07:21](https://www.youtube.com/watch?v=oeknLUsN_GE&t=441s) wherever the answer varies in a place an

[0:07:24](https://www.youtube.com/watch?v=oeknLUsN_GE&t=444s) expert can read. Chapter three. Now the

[0:07:28](https://www.youtube.com/watch?v=oeknLUsN_GE&t=448s) model decides and its decision becomes

[0:07:31](https://www.youtube.com/watch?v=oeknLUsN_GE&t=451s) an action. I used to think control meant

[0:07:35](https://www.youtube.com/watch?v=oeknLUsN_GE&t=455s) permissions on the agent. So what does

[0:07:37](https://www.youtube.com/watch?v=oeknLUsN_GE&t=457s) it mean to stay in control?

[0:07:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=461s) Control starts with what the model sees.

[0:07:44](https://www.youtube.com/watch?v=oeknLUsN_GE&t=464s) That's what the fourth stone mind. What

[0:07:47](https://www.youtube.com/watch?v=oeknLUsN_GE&t=467s) does the model know? When we let it

[0:07:49](https://www.youtube.com/watch?v=oeknLUsN_GE&t=469s) choose what to load, it loaded

[0:07:52](https://www.youtube.com/watch?v=oeknLUsN_GE&t=472s) everything. Then it invented a pricing

[0:07:55](https://www.youtube.com/watch?v=oeknLUsN_GE&t=475s) check just because prices were visible.

[0:07:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=478s) Whatever sits in its context becomes a

[0:08:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=481s) reason to act. The runtime decides

[0:08:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=484s) what's the model sees for our task.

[0:08:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=487s) That's three facts from the order. The

[0:08:09](https://www.youtube.com/watch?v=oeknLUsN_GE&t=489s) full record stays with the runtime and

[0:08:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=492s) the model makes fewer wrong moves.

[0:08:17](https://www.youtube.com/watch?v=oeknLUsN_GE&t=497s) Here how we minimize context blo for a

[0:08:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=500s) big set. The model passes a handle, a

[0:08:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=502s) short name for date that the runtime

[0:08:24](https://www.youtube.com/watch?v=oeknLUsN_GE&t=504s) already holds. The runtime checks it

[0:08:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=507s) before any write. It keeps the context

[0:08:29](https://www.youtube.com/watch?v=oeknLUsN_GE&t=509s) small and still enough for the decision.

[0:08:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=512s) At the same time, it uh validates

[0:08:35](https://www.youtube.com/watch?v=oeknLUsN_GE&t=515s) context for consistency. A model with

[0:08:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=519s) the right facts can still do damage.

[0:08:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=521s) That's the fifth stone, power. What made

[0:08:45](https://www.youtube.com/watch?v=oeknLUsN_GE&t=525s) change? We control a change twice.

[0:08:47](https://www.youtube.com/watch?v=oeknLUsN_GE&t=527s) during development and again at the

[0:08:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=530s) right at runtime only code opens the

[0:08:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=533s) right path so we can change pros many

[0:08:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=536s) times a day the open rings are the parts

[0:08:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=539s) that still depend on people let's zoom

[0:09:02](https://www.youtube.com/watch?v=oeknLUsN_GE&t=542s) in and run right five walls stand in

[0:09:06](https://www.youtube.com/watch?v=oeknLUsN_GE&t=546s) front of it and the sixth checks that it

[0:09:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=548s) landed if a right looks like it failed

[0:09:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=552s) an agent retries and the journal makes

[0:09:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=555s) sure it runs only once means much more

[0:09:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=558s) than permissions on the agent.

[0:09:24](https://www.youtube.com/watch?v=oeknLUsN_GE&t=564s) Chapter 4. Most days I glide over the

[0:09:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=567s) system. From up here, everything looks

[0:09:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=570s) fine, so I don't go down into every

[0:09:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=572s) change my agents made. Then the surface

[0:09:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=576s) gets rough. How do we know we're losing

[0:09:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=579s) control?

[0:09:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=581s) All those controls protect the system.

[0:09:43](https://www.youtube.com/watch?v=oeknLUsN_GE&t=583s) Nothing protected my attention. At the

[0:09:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=586s) start, I read every change and that's

[0:09:48](https://www.youtube.com/watch?v=oeknLUsN_GE&t=588s) how the system picked up my habits. Then

[0:09:52](https://www.youtube.com/watch?v=oeknLUsN_GE&t=592s) the volume grew past what one person can

[0:09:55](https://www.youtube.com/watch?v=oeknLUsN_GE&t=595s) read. I was burning out and I stopped

[0:09:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=598s) reading every change. That was the price

[0:10:00](https://www.youtube.com/watch?v=oeknLUsN_GE&t=600s) of the last stone. So, who judges and

[0:10:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=604s) what does it cost? With it, the gauntlet

[0:10:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=607s) is complete. Every tech lead I know has

[0:10:10](https://www.youtube.com/watch?v=oeknLUsN_GE&t=610s) been here. The one person every change

[0:10:13](https://www.youtube.com/watch?v=oeknLUsN_GE&t=613s) waits on. agents just get you there in

[0:10:16](https://www.youtube.com/watch?v=oeknLUsN_GE&t=616s) weeks instead of years. I needed a way

[0:10:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=619s) of working that doesn't run through one

[0:10:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=622s) head. And the first gauge was me. When

[0:10:25](https://www.youtube.com/watch?v=oeknLUsN_GE&t=625s) I'm tired and I can't explain what

[0:10:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=627s) changed, that's the signal. The

[0:10:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=630s) dashboard can be green while that gauge

[0:10:33](https://www.youtube.com/watch?v=oeknLUsN_GE&t=633s) is firing. So, I stop and fix the

[0:10:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=636s) process first. I don't wait for a

[0:10:38](https://www.youtube.com/watch?v=oeknLUsN_GE&t=638s) number. I couldn't read every div

[0:10:41](https://www.youtube.com/watch?v=oeknLUsN_GE&t=641s) anymore. So I built instruments that

[0:10:44](https://www.youtube.com/watch?v=oeknLUsN_GE&t=644s) watch how things change and their

[0:10:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=646s) derivatives. One of them is blast

[0:10:49](https://www.youtube.com/watch?v=oeknLUsN_GE&t=649s) radius. Before we built one new check,

[0:10:52](https://www.youtube.com/watch?v=oeknLUsN_GE&t=652s) we replayed its rule over several

[0:10:54](https://www.youtube.com/watch?v=oeknLUsN_GE&t=654s) thousand past sessions. It would have

[0:10:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=656s) fired on less than 1%. Where the numbers

[0:11:00](https://www.youtube.com/watch?v=oeknLUsN_GE&t=660s) jump, I go down and read. When something

[0:11:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=664s) looks wrong, we wait. One signal waits

[0:11:06](https://www.youtube.com/watch?v=oeknLUsN_GE&t=666s) until it comes back, even when it comes

[0:11:09](https://www.youtube.com/watch?v=oeknLUsN_GE&t=669s) from an expert. A cluster across slices

[0:11:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=672s) is different. Then we fix the concept

[0:11:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=675s) behind it once. Left alone, an agent

[0:11:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=678s) keeps adding conditions until today's

[0:11:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=680s) tasks pass. The eval score drops when

[0:11:23](https://www.youtube.com/watch?v=oeknLUsN_GE&t=683s) you take them out and you get an honest

[0:11:26](https://www.youtube.com/watch?v=oeknLUsN_GE&t=686s) list of gaps.

[0:11:31](https://www.youtube.com/watch?v=oeknLUsN_GE&t=691s) One red slice is rarely alone. The

[0:11:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=694s) experts note becomes an eval and an

[0:11:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=696s) agent searches the siblings for the same

[0:11:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=699s) failure. Siblings differ on purpose by

[0:11:42](https://www.youtube.com/watch?v=oeknLUsN_GE&t=702s) market and by local law. So we sweep

[0:11:45](https://www.youtube.com/watch?v=oeknLUsN_GE&t=705s) them and the fix goes only where the

[0:11:48](https://www.youtube.com/watch?v=oeknLUsN_GE&t=708s) failure is confirmed.

[0:11:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=713s) At any time 10 to 20 of these loops are

[0:11:57](https://www.youtube.com/watch?v=oeknLUsN_GE&t=717s) open. At one point I had become the

[0:11:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=719s) message bus between users and my agents.

[0:12:03](https://www.youtube.com/watch?v=oeknLUsN_GE&t=723s) At this scale, every user has to be an

[0:12:06](https://www.youtube.com/watch?v=oeknLUsN_GE&t=726s) evaluator with a screen to give feedback

[0:12:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=728s) without me. My job as the architect is

[0:12:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=732s) to build those loops into the system.

[0:12:15](https://www.youtube.com/watch?v=oeknLUsN_GE&t=735s) Each loop writes to a ledger. So nothing

[0:12:18](https://www.youtube.com/watch?v=oeknLUsN_GE&t=738s) waits on my memory and nothing waits on

[0:12:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=740s) me.

[0:12:24](https://www.youtube.com/watch?v=oeknLUsN_GE&t=744s) Agents forget everything when a session

[0:12:26](https://www.youtube.com/watch?v=oeknLUsN_GE&t=746s) ends. So the memory has to leave in

[0:12:29](https://www.youtube.com/watch?v=oeknLUsN_GE&t=749s) files. We keep two kinds. what happened

[0:12:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=752s) and what is true now. The next session

[0:12:35](https://www.youtube.com/watch?v=oeknLUsN_GE&t=755s) starts from what is true now.

[0:12:40](https://www.youtube.com/watch?v=oeknLUsN_GE&t=760s) Every issue has to connect to its root

[0:12:43](https://www.youtube.com/watch?v=oeknLUsN_GE&t=763s) cause. Without that, the agent decides

[0:12:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=766s) on wrong facts and the check has nothing

[0:12:49](https://www.youtube.com/watch?v=oeknLUsN_GE&t=769s) to count. So we don't act without

[0:12:51](https://www.youtube.com/watch?v=oeknLUsN_GE&t=771s) evidence.

[0:12:54](https://www.youtube.com/watch?v=oeknLUsN_GE&t=774s) Reality comes back. In chapter two, it

[0:12:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=778s) asked if the pros is true. Now it asks

[0:13:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=781s) if the change is I used to trust green.

[0:13:05](https://www.youtube.com/watch?v=oeknLUsN_GE&t=785s) So what would make us change our mind?

[0:13:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=788s) Green was tempting because checking is

[0:13:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=791s) where the times goes. My agent spend

[0:13:14](https://www.youtube.com/watch?v=oeknLUsN_GE&t=794s) almost 9/10en of that time on a change

[0:13:17](https://www.youtube.com/watch?v=oeknLUsN_GE&t=797s) just checking it and checking took a

[0:13:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=799s) bigger share of my own week too.

[0:13:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=802s) Verification speed is the limit.

[0:13:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=807s) We rank evidence by what it proves. A

[0:13:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=810s) replay on real tasks sits at the top.

[0:13:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=814s) Before the data arrives, we write down

[0:13:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=816s) what would prove us wrong. And every new

[0:13:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=819s) check has to fail once on purpose before

[0:13:42](https://www.youtube.com/watch?v=oeknLUsN_GE&t=822s) we trust it.

[0:13:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=826s) AI refactors fail quietly. Every

[0:13:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=830s) condition and every decision table row

[0:13:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=833s) is a branch. And after a refactor, each

[0:13:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=836s) one has to land exactly once. Here the

[0:13:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=839s) branch for amounts over the limit got

[0:14:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=841s) lost. Our \[snorts\] order would have gone

[0:14:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=844s) through without the team lead. Real

[0:14:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=847s) tasks decide what we test. We freeze

[0:14:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=851s) them as a set and replay the old version

[0:14:14](https://www.youtube.com/watch?v=oeknLUsN_GE&t=854s) against the new one. If no real task

[0:14:17](https://www.youtube.com/watch?v=oeknLUsN_GE&t=857s) takes a branch, we call that no

[0:14:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=859s) evidence.

[0:14:21](https://www.youtube.com/watch?v=oeknLUsN_GE&t=861s) You can't trust one agent to judge its

[0:14:24](https://www.youtube.com/watch?v=oeknLUsN_GE&t=864s) own work. A second agent checks it with

[0:14:28](https://www.youtube.com/watch?v=oeknLUsN_GE&t=868s) a checklist and without the author's

[0:14:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=870s) reasoning. It can't be talked into

[0:14:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=872s) agreeing. Over 6 months, it grew to most

[0:14:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=876s) of my checking.

[0:14:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=879s) Coding agents finish most of a batch and

[0:14:43](https://www.youtube.com/watch?v=oeknLUsN_GE&t=883s) quietly skipped the rest, especially

[0:14:45](https://www.youtube.com/watch?v=oeknLUsN_GE&t=885s) when their context is full. The ledger

[0:14:48](https://www.youtube.com/watch?v=oeknLUsN_GE&t=888s) shows what was skipped in one backlog.

[0:14:51](https://www.youtube.com/watch?v=oeknLUsN_GE&t=891s) Most items looks covered, but only about

[0:14:54](https://www.youtube.com/watch?v=oeknLUsN_GE&t=894s) a quarter could really be closed. So now

[0:14:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=898s) evidence we can count is what changes

[0:15:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=901s) our mind. And this is the third option

[0:15:05](https://www.youtube.com/watch?v=oeknLUsN_GE&t=905s) from the start of the talk. I used to

[0:15:08](https://www.youtube.com/watch?v=oeknLUsN_GE&t=908s) think there were two choices. Keep

[0:15:11](https://www.youtube.com/watch?v=oeknLUsN_GE&t=911s) everything or snap. So what is worth

[0:15:14](https://www.youtube.com/watch?v=oeknLUsN_GE&t=914s) carrying forward?

[0:15:16](https://www.youtube.com/watch?v=oeknLUsN_GE&t=916s) This one process over a year. Some

[0:15:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=919s) branches merged back, some still drift,

[0:15:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=922s) and some are dead but still look alive.

[0:15:25](https://www.youtube.com/watch?v=oeknLUsN_GE&t=925s) Which ones deserve to survive?

[0:15:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=930s) A fix is only a moment. These forces

[0:15:33](https://www.youtube.com/watch?v=oeknLUsN_GE&t=933s) keep pushing right after it. You've met

[0:15:36](https://www.youtube.com/watch?v=oeknLUsN_GE&t=936s) most of them already. This chapter deals

[0:15:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=939s) with regrowth and branching.

[0:15:44](https://www.youtube.com/watch?v=oeknLUsN_GE&t=944s) The first gauge was me back in chapter

[0:15:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=946s) 4. These are the gauges for the code.

[0:15:50](https://www.youtube.com/watch?v=oeknLUsN_GE&t=950s) Time gets its answers here. The bridge

[0:15:53](https://www.youtube.com/watch?v=oeknLUsN_GE&t=953s) line comes back as a number. A ratchet

[0:15:56](https://www.youtube.com/watch?v=oeknLUsN_GE&t=956s) means the count can only go down. Two

[0:15:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=958s) gauges run today and six more are next.

[0:16:04](https://www.youtube.com/watch?v=oeknLUsN_GE&t=964s) Every week real use decides what stays.

[0:16:07](https://www.youtube.com/watch?v=oeknLUsN_GE&t=967s) Anything no real task reaches gets a

[0:16:10](https://www.youtube.com/watch?v=oeknLUsN_GE&t=970s) name and its evidence before it goes.

[0:16:13](https://www.youtube.com/watch?v=oeknLUsN_GE&t=973s) Test the evidence I didn't have when I

[0:16:16](https://www.youtube.com/watch?v=oeknLUsN_GE&t=976s) snapped. Tests kept that variants alive.

[0:16:20](https://www.youtube.com/watch?v=oeknLUsN_GE&t=980s) Agents kept every option a test still

[0:16:23](https://www.youtube.com/watch?v=oeknLUsN_GE&t=983s) mentioned. Now retired variant takes its

[0:16:27](https://www.youtube.com/watch?v=oeknLUsN_GE&t=987s) test with it. Here's the whole method as

[0:16:30](https://www.youtube.com/watch?v=oeknLUsN_GE&t=990s) one week. This is the third option as a

[0:16:34](https://www.youtube.com/watch?v=oeknLUsN_GE&t=994s) process.

[0:16:39](https://www.youtube.com/watch?v=oeknLUsN_GE&t=999s) together. That's the full gauntlet.

[0:16:42](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1002s) Thanos used his for one snap. We use

[0:16:45](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1005s) ours every week in small doses with

[0:16:48](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1008s) evidence. I haven't had to snap again.

[0:16:55](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1015s) Soul had a second price and I only saw

[0:16:58](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1018s) it later. After we deliver it to

[0:17:01](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1021s) production, I found my own engineering

[0:17:03](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1023s) principles built into the systems

[0:17:06](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1026s) design. Its skills and its memory carry

[0:17:09](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1029s) my habits and my biases. Conway said the

[0:17:12](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1032s) system copies the orc chart. Ours copies

[0:17:16](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1036s) whoever corrects it. Here are 18

[0:17:19](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1039s) questions, three for each stone. I'm

[0:17:22](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1042s) using them when working on my projects.

[0:17:26](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1046s) Pause here and pick one your own

[0:17:29](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1049s) repository can't answer yet. That's

[0:17:32](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1052s) where to start.

[0:17:37](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1057s) I learned to use this process when I was

[0:17:40](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1060s) already burning out. If you're the one

[0:17:43](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1063s) your team's changes weight on today,

[0:17:46](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1066s) this is for you. Use your stones while

[0:17:49](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1069s) you can still read every change. In the

[0:17:52](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1072s) end, Thanos retires to a garden. Maybe

[0:17:55](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1075s) he should start using them daily. Thank

[0:17:59](https://www.youtube.com/watch?v=oeknLUsN_GE&t=1079s) you.
