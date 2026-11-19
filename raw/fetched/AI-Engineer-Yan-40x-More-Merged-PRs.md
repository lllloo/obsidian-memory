---
title: 40x More Merged PRs With 2.7x the Engineers — Walden Yan
description: AI Engineer CODE 2026 官方閱讀版，Cognition 的 Walden Yan 談內部軟體工廠、可測試環境與給 agent 長期 job，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/walden-yan
published: 2026-11-13
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁（閱讀頁場次名為 A New Age of Software Engineering），正文後附官方機器逐字稿（原註明含辨識錯誤，如 Devin 被辨識成 Devon、Vera Rubin 被辨識成 Verorubin）。逐字稿對應 Day 2 直播 `https://www.youtube.com/watch?v=y9JtCCZP2MQ`（2:33:30–2:47:07）；剪輯單場版為 `https://www.youtube.com/watch?v=U92J5mCDLMc`（標題「40x More Merged PRs With 2.7x the Engineers — Walden Yan, Cognition」，2026-11-19 以 yt-dlp 核對）。`published` 取 Day 2 直播的 YouTube 上傳日。

Day 2 livestream · [2:33:30–2:47:07 on YouTube](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9210s). The player starts and stops at this session’s boundaries.

## Introduction

**Walden Yan**, cofounder and Chief Product Officer of Cognition, describes the infrastructure and team changes behind moving Devin from individual coding tasks to persistent engineering goals.

Cognition's merged pull requests grew much faster than its headcount. Yan opens with that internal comparison because it creates a more interesting question than whether an agent can write code: what does an engineering organization have to change to absorb all that work?

PR volume is not a complete productivity measure, and Yan's accompanying claim that quality stayed the same or improved is the company's assessment. The useful part of the talk is the operating system underneath the chart. His team is trying to make unattended engineering the default, with people handling the exceptions rather than supervising every edit.

[2:35:09 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9309s)

## Give small teams the whole customer problem

[02:35:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9309s)

The destination is a self-driving workflow: a bug arrives, an agent investigates, produces a change, validates it, and follows the result into production. Human intervention remains available, but it should occur because the work requires judgment, not because the agent ran out of instructions.

That does not mean turning engineers into people who forward tickets to Devin. Yan describes small pods of two or three engineers with vertical responsibility. A pod understands its customers, manages its own work, and takes on responsibilities that might otherwise be separated into product management, implementation, and QA. Agents expand the implementation capacity of that group; they do not supply its customer understanding.

The concrete example starts in Slack. A customer sends a video showing a bug. An engineer passes that context to Devin, which develops a fix and returns a video demonstrating the repaired behavior. The engineer can then respond to the customer without opening an IDE.

The video matters on both sides. The first makes the failure observable. The second gives the person a compact way to inspect whether the requested behavior changed. The workflow is shorter because it carries evidence across the handoffs, not simply because typing became faster.

[2:37:56 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9476s)

## Make a fresh environment cheaper than asking for help

[02:37:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9476s)

This customer-facing simplicity depends on substantial work underneath. Cognition moved services into Docker Compose and replaced external dependencies with mocks so that an agent could exercise the application on a single VM. Testing against a collection of live third-party services had made the environment harder to reproduce.

[![Cognition's agent-testable codebase: a single VM, hourly snapshots, and maintained testing skills](https://ai.engineer/reading/code-2026/images/walden-yan-9515.jpg)](https://ai.engineer/reading/code-2026/images/walden-yan-9515.jpg)

*At 2:38:35, the slide connects three changes: consolidate the application into one VM, build hourly snapshots, and let agents maintain the testing skills they use.*

The team rebuilds these environments against the latest repository on an hourly cadence. When a build fails, agents are the first responders. A successful snapshot gives subsequent runs a known starting point rather than a long setup procedure whose failure consumes human attention.

Testing instructions are also maintained as artifacts. Agents use skills to run checks and repair those skills when the application changes. A fresh machine alone is not enough if its instructions describe last month's UI.

Yan extends the example to more complicated interactions, including multiple accounts participating in a Zoom-style session. The ambition is to make the relevant behavior testable by the agent, not to declare that every application fits into a trivial unit-test loop. His aside about engineers working from iPads illustrates where the development environment now lives: the cloud run, rather than the person's local laptop, holds the operational state.

[2:40:31 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9631s)

## Use run history to improve the factory

[02:40:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9631s)

Once engineering runs happen in a shared environment, they leave a common record. Cognition can inspect where agents spend time and tokens, identify repeated work, and turn that repetition into scripts or better tests. Yan describes agents generating suggestions in Slack about how to improve the workflow itself.

This is a second feedback loop. One loop fixes the customer problem. The other asks why fixing that class of problem took so many steps. Without the second, an organization can run the same expensive investigation hundreds of times and mistake activity for progress.

## Replace a task with a measurable ongoing job

The next transition is from a bounded assignment to a persistent goal. Instead of asking for one latency optimization, an engineer can give an agent responsibility for improving p99 latency. That job begins with instrumentation and a baseline, then continues through alerts, investigation, candidate changes, and progress reports.

The distinction is important: “make it faster” is not a durable control signal. A measured latency target, a way to reproduce regressions, and an agreed reporting cadence give the agent something it can keep evaluating after its first patch.

Yan gives related examples: layout shifts measured through changes in element bounding boxes, click latency, and onboarding retention. These goals differ in how directly a code change can be evaluated, but they all require the desired outcome to be visible. The agent needs more than an open-ended mandate to keep itself busy.

He also describes longer-running inference optimization work with dedicated hardware and human approval of the final changes. The claim is not that autonomy removes review; it allows exploration to continue without requiring a person to schedule every experiment.

[2:44:20 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9860s)

## Maintain parity after the first version works

[02:44:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9860s)

The closing example is an Android application. Cognition had substantial iOS work underway but less bandwidth for Android. Rather than treating the Android port as a single prompt, the team gave an agent an ongoing maintenance job: watch repository changes, collect feedback, compare behavior with iOS, perform live QA, and keep the implementation aligned.

The result Yan shows is still described as forthcoming, not a released product. He reports a long-running effort with many days requiring little direct messaging, while important decisions still escalate and people inspect videos of the result.

That last example makes the organizational change concrete. A task ends when a patch is ready. A job continues because the product around it keeps changing. Making that job useful requires the testable environment, durable evidence, measurable goals, and escalation path established earlier in the talk.

Full transcript 217 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[2:33:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9216s) Walden. I'm one of the co-founders and chief product officer at Cognition. We build an

[2:33:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9221s) AI product called Devon. I want to spend most of my time here today, though, kind of abstracting

[2:33:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9227s) a bit away from that and focusing on what are we doing internally as an engineering

[2:33:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9232s) team to move way faster.

[2:33:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9234s) And so the backdrop I would put for all this

[2:33:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9236s) is this is what our merged PR throughput looks like at Cognition.

[2:34:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9241s) The start of this is around 12 months ago.

[2:34:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9244s) So you're looking at about a snapshot of a year.

[2:34:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9246s) And over this last year, this blue chart here, this 40x,

[2:34:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9250s) is a 40x in the number of merged PRs

[2:34:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9253s) we are producing on our engineering team.

[2:34:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9255s) Now, you might also notice there's

[2:34:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9257s) a small black line along the bottom there.

[2:34:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9260s) It's easy to miss.

[2:34:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9260s) But that 2.7x, that is our engineering headcount growth in the same period.

[2:34:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9265s) So we have been hiring engineers, but each of our engineers is now more than 10x more productive than they were before.

[2:34:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9272s) And I would dare to say that these PRs are just as high quality, if not higher quality, than they were a year ago.

[2:34:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9278s) So really the crux of what I want to talk about today is what did we do to unlock this 40x engineering throughput?

[2:34:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9288s) And there's a lot of things we did from both the code base to the way we structure engineering

[2:34:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9293s) teams that I think are very practical steps you can take if you want to reproduce the

[2:34:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9297s) same results.

[2:34:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9299s) Many of you are probably familiar with the software factory.

[2:35:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9301s) How many of you guys have heard of software factory?

[2:35:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9302s) Let's see a raise of hands.

[2:35:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9304s) Cool.

[2:35:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9305s) So I'll start with the basics and then I'll work my way up to the more advanced stuff.

[2:35:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9309s) The basic idea of a software factory is, yeah, by default everything should be self-driving.

[2:35:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9315s) we have PRs that go from initial bug report to final merge and monitoring and maintenance

[2:35:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9321s) without a single human involved. Oftentimes human judgment is needed though, and that's where we

[2:35:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9325s) have escalations. But by default, our entire software development process is just run by

[2:35:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9330s) Devon from end to end. One of the things this means is that the role of the software engineer

[2:35:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9336s) has to change quite a bit. Around March of this year, we had this conversation with the engineering

[2:35:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9342s) team. And we said, look, if you are right now just picking off tickets off a linear board and then

[2:35:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9348s) sending that to an agent and implementing it, you're not going to really be set up for success

[2:35:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9351s) in the age of AI, because anything that is described and can be implemented will be able

[2:35:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9356s) to send to Devin. So really, everyone has to change the way that they're developing.

[2:36:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9362s) And the way we've enforced this is we've taken our larger teams and we've broken them up into

[2:36:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9366s) smaller pods. And the smaller pods not only are given swarms of agents to do work for them,

[2:36:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9372s) they are given more vertical responsibility.

[2:36:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9374s) So instead, you might have only two or three engineers

[2:36:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9378s) on a team at a time, but they're responsible for everything

[2:36:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9381s) beyond the engineering as well.

[2:36:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9382s) They're responsible for listening to customer bug reports.

[2:36:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9385s) They're responsible for doing QA testing.

[2:36:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9387s) They're responsible for doing the PMing and product management.

[2:36:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9390s) And basically, every engineer manages

[2:36:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9392s) their entire own linear board of things to do,

[2:36:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9395s) they send that to an agent to implement for them.

[2:36:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9397s) So it's really a fundamental change in the way

[2:36:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9399s) that our engineers do work.

[2:36:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9400s) This has been one of the things that we've implemented over the last year and we've been helping a lot of large organizations implement for themselves as well

[2:36:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9410s) Another thing I'd really like to highlight is we work from slack everywhere

[2:36:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9413s) so this is an example of what a customer bug report might look like they send me a video on slack and

[2:36:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9419s) We just forward bug reports straight into our internal channel and we tagged Devin and say hey, please fix this

[2:37:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9427s) Devon immediately comes up, shows up at PR, but then also sends back a video with the

[2:37:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9433s) fix and proof.

[2:37:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9436s) And this makes our lives so much easier because I literally don't have to leave Slack for

[2:37:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9439s) most of my work.

[2:37:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9440s) We've abstracted away all the development to be based on evidence, videos, and I can

[2:37:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9446s) just send the proof that the fix is ready right back to the customer without having to open

[2:37:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9450s) an IDE or even GitHub most of the time.

[2:37:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9454s) So this is kind of the end goal you want to reach which is a point where you can do your entire development lifecycle

[2:37:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9460s) Without opening up an IDE or without opening up a single coding agent

[2:37:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9466s) But to get to this point there's a lot of infrastructure

[2:37:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9470s) We had to change underneath and so this is the hard part that really every engineering team has to do if they want to get to that point

[2:37:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9476s) It's not just you purchase a coding agent

[2:37:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9477s) You got to go change the way you build so before when we test our applications

[2:38:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9481s) we'd be testing them against cloud deployments.

[2:38:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9483s) We'd have a staging environment, connect to a staging database,

[2:38:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9486s) connect to live servers, and then we'd

[2:38:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9488s) have our engineers manually go click through and verify

[2:38:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9490s) that the flows work end to end.

[2:38:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9492s) We did a big migration to move every service

[2:38:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9495s) to be able to run locally with Docker Compose.

[2:38:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9498s) We've made it so every third party service,

[2:38:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9500s) we have mocked versions to be able to run locally.

[2:38:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9502s) And these can all run inside a single virtual machine

[2:38:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9506s) that every Devon has access to.

[2:38:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9508s) And every coding agent in our company now

[2:38:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9510s) does not need to touch any live services at all to test their changes.

[2:38:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9515s) In fact, these VMs, we rebuild them every hour at the company.

[2:38:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9520s) Every hour, we pull the latest version of the code.

[2:38:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9522s) We rebuild the entire code base from scratch

[2:38:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9524s) to be able to run very quickly and easily from scratch.

[2:38:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9527s) And if these builds ever fail because your code base is rapidly changing,

[2:38:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9532s) we also have Devon be the first response there.

[2:38:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9534s) And they're always immediately fixing these VM snapshots.

[2:38:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9537s) So every time we spin up an agent from Slack,

[2:39:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9540s) it goes to a fresh machine on a fresh version of the code base with the latest updates.

[2:39:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9544s) And by the way, these agents, you need to teach them how to test your code base as well.

[2:39:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9550s) But the benefit of using cloud coding agents is that they can self-maintain their training loops.

[2:39:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9555s) So that last section there on testing, Devin will write its own skills for how to test our code base.

[2:39:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9562s) The code base will change over time, so the way you test it will change,

[2:39:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9564s) but Devin can keep on updating these skills so that it tests it over and over again.

[2:39:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9568s) So the end result of this is literally people do not need to open their laptops anymore to test any code changes

[2:39:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9573s) In fact several engineers at cognition have already moved to using iPads for the development process

[2:39:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9580s) By the way iPads are also more secure, you know a lot you see a lot of these hacks recently a lot of it is because of

[2:39:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9584s) DevOps and and people leaking keys who knows what's on your developer machine

[2:39:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9588s) You might have secrets all over the place when everything is in the cloud within these controlled VMs direction a much more secure spot

[2:39:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9596s) I've showed some basic versions of things you can test.

[2:39:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9598s) We've also tested advanced multiplayer

[2:40:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9600s) setups which is really cool. We've often times when we were developing Devon's ability to

[2:40:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9604s) join voice in Zoom calls, we actually had Devon, when it tests, create multiple accounts,

[2:40:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9610s) have them join the same Zoom call, all from within their one VM, and send voice memos back

[2:40:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9615s) and forth to make sure that the functionality is working. So you can do quite advanced setups

[2:40:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9619s) if you really push the limits of your code base.

[2:40:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9623s) And actually, on top of all this,

[2:40:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9625s) you obviously want recursive self-improvement.

[2:40:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9628s) I think people think about this from the model sense quite a lot.

[2:40:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9631s) But actually, if you think about it,

[2:40:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9634s) every single line of code that's being written,

[2:40:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9636s) every single PR that's being generated, every decision,

[2:40:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9639s) if you have a cloud agent setup,

[2:40:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9640s) that's all tracked across your entire code base.

[2:40:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9643s) So there's no reason why you shouldn't also be able to run agents

[2:40:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9645s) on top of that, do the data analysis,

[2:40:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9647s) and figure out where are we wasting time,

[2:40:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9649s) Where are we wasting tokens?

[2:40:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9651s) What things can be turned into scripts?

[2:40:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9653s) What tests can we be adding to improve this process?

[2:40:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9656s) And so we have a channel where Devon every day posts ideas about,

[2:41:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9660s) hey, if we change our node setup, we can shave a minute off of our CI.

[2:41:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9665s) If we change this lint script, we can catch 20% more of these bugs

[2:41:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9669s) before they ever hit AI code review.

[2:41:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9671s) And this has actually been a huge unlock

[2:41:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9673s) where you can just set up these systems,

[2:41:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9675s) and the agents will go and optimize your software factory for you.

[2:41:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9679s) This has been really exciting.

[2:41:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9681s) One of the things that I don't hear people talking about a lot,

[2:41:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9685s) but I think is really where things are going next,

[2:41:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9687s) is moving from the world where you're giving tasks to your agents

[2:41:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9691s) to giving jobs to your agents.

[2:41:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9693s) And this is a bit of a paradigm shift.

[2:41:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9695s) You really have to start treating these things like coworkers.

[2:41:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9698s) So what does giving a job to an agent look like?

[2:41:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9701s) Imagine I care about back-end performance.

[2:41:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9705s) Really, this is what the development flow of the future should look like.

[2:41:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9707s) You should send to your agent, hey, I want to improve P99 latency of my application.

[2:41:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9712s) Instead of you telling it what to do to do that, it should say, okay, P99 latency.

[2:41:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9717s) Let me add the telemetry to figure out where our P99 latency is today.

[2:42:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9721s) Let me set up alerts so I can figure out where we need to be in the future.

[2:42:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9724s) Let me go break down every single task we need to do to be able to move this latency.

[2:42:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9729s) Let me create data dog alerts.

[2:42:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9731s) Let me create weekly reports in Slack.

[2:42:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9733s) and let me send you updates on your phone every day on here's where P99 latency is and here's how much it's improved.

[2:42:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9739s) This is

[2:42:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9740s) fundamentally the type of systems that we encourage all of our engineers to be building at Cognition.

[2:42:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9745s) We don't even we don't even want you to be prompting your agents most of the time.

[2:42:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9748s) We want you to just be giving your agent goals that they can work toward over long durations of time.

[2:42:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9753s) And anything in your company that you think isn't measurable, find a way to measure it.

[2:42:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9758s) You know, do you care about your application performance?

[2:42:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9761s) go measure, you know, the latency of clicks on your application. If your

[2:42:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9764s) application has a lot of weird layout shifts, go measure the bounding boxes and

[2:42:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9768s) try to figure out how you can minimize layout shifts across your application.

[2:42:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9771s) There's obviously P99 latency, but there's also things like, you know,

[2:42:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9774s) onboarding retention. How much of what you guys do as engineers is things you

[2:42:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9779s) can boil down to a single number or metric, and I encourage you that if you

[2:43:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9782s) can do that, you should just set up an agent to go optimize that number 24-7.

[2:43:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9787s) So a great example of this is inference latency.

[2:43:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9790s) At Cognition, we're lucky to be the first receivers of NVIDIA's new class of Verorubin GPUs.

[2:43:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9798s) Kernels were not built for these GPUs when we received them.

[2:43:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9800s) So we had to, from scratch, figure out how do we build our own inference stack on top of this new hardware that's coming out.

[2:43:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9807s) And agents have allowed us to do this in a way that is much more efficient than before.

[2:43:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9812s) So we just tell it, hey, we care about the throughput, our TPM.

[2:43:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9816s) these GPUs go figure out how to push that to its limits and over the course of what is about I guess here like a week

[2:43:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9825s) The agent was able to go we allocated it a permanent set of GPUs to work on

[2:43:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9830s) It was able to go find different strategies test them the strategies that it found worked best

[2:43:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9835s) It was sent to a human engineer for final approval

[2:43:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9837s) But basically there's eight or nine different things that were roughly discovered

[2:44:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9843s) via just giving these agents these high-level goals,

[2:44:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9846s) and we were able to push the throughput

[2:44:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9849s) on these new and very Rubin GPUs

[2:44:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9851s) from what was worse than the new GB300s

[2:44:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9854s) to what is now significantly better

[2:44:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9856s) than the previous class of GB300 GPUs.

[2:44:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9859s) And again, this is all done

[2:44:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9860s) by just giving an end goal to your agents.

[2:44:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9866s) Another example that I like to share with folks,

[2:44:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9870s) we are a fairly small engineering team,

[2:44:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9873s) It means we do not have, oftentimes, the bandwidth to fully staff things that we might want to

[2:44:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9877s) do, like an Android application.

[2:44:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9880s) But the other day, one of our engineers on our team, Sam Yoke, he had this brilliant idea.

[2:44:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9884s) He said, okay, look, we have a team of people working on building a great iOS application.

[2:44:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9890s) Can't we just use that as a blueprint for our Android application and tell Devin, hey,

[2:44:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9895s) go maintain parity from our iOS application to our Android application end-to-end?

[2:45:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9901s) And that is exactly what he did.

[2:45:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9903s) But it wasn't just, hey, one dev in session to go do all this.

[2:45:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9907s) He said, set up permanent hooks against our code base to monitor the iOS application.

[2:45:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9912s) You know, go listen to the Slack channels for user feedback about our applications.

[2:45:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9918s) And then go recursively improve our application.

[2:45:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9920s) Go do live QA testing of every detail and making sure it all works.

[2:45:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9925s) Syncing these things live has been really cool.

[2:45:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9928s) And I think the final results here are actually quite sick.

[2:45:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9938s) So we really just gave our agent this one high-level prompt, which is, hey, go manage

[2:45:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9943s) the entire Android application.

[2:45:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9944s) And over the course of 44 days, we have a working application, which we'll be putting

[2:45:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9949s) out soon.

[2:45:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9950s) But as a time lapse, most days, there's not a single human message going to this agent

[2:45:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9955s) working on it.

[2:45:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9957s) And on those days, you know, it's merging upward of like 40, 50 PRs a day.

[2:46:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9963s) All this is being live QA tested against the iOS application, pixel for pixel, testing

[2:46:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9969s) what are, you know, escalating only the most important decisions to a human at the end

[2:46:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9973s) of the day.

[2:46:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9976s) And most of the time, our engineers don't even need to open Devon, they're just from

[2:46:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9979s) Slack, look at the recordings that it sends back to them.

[2:46:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9987s) So in the end, the human is barely doing anything in this loop.

[2:46:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9990s) This is how many messages a human actually had to send to our agent in this entire process.

[2:46:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9998s) Yeah.

[2:46:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=9998s) And it's not a slop application.

[2:46:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10000s) This is actually something that we will be going live with very soon.

[2:46:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10009s) So cool.

[2:46:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10010s) That's actually all I had.

[2:46:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10012s) I think the end message from all of this is if you set up the loops for your agents correctly,

[2:46:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10017s) you can do some pretty incredible stuff.

[2:47:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10020s) So I think really most teams are limited by the amount of ambition they have.

[2:47:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10024s) So it's time to be ambitious.

[2:47:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=10026s) Thank you.
