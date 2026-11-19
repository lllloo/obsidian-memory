---
title: 225,000 Lines of Tests, Written and Merged by Agents — Kush Agrawal, Duolingo
description: AI Engineer CODE 2026 官方閱讀版，Duolingo 用 Temporal 排程 coding agent 補 iOS 單元測試並管理 PR 生命週期，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-duolingo-tests
published: 2026-11-11
tags:
  - clippings
  - coding-agent
  - testing
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如開場「200,000,000 lines」實為 200,000、Claude Code 被辨識成 cloud code／clot code、Duolingo 被辨識成 Dualingo、LLM-as-judge 審查數「about,200」漏字）。逐字稿對應 Day 1 直播 `https://www.youtube.com/watch?v=ZZ19zhYnDKY`（影片 ID `ZZ19zhYnDKY`，本場 4:42:54–4:55:30）；`published` 取該直播影片在 YouTube 的上架日（美西時間），大會日期為 2026-11-10 至 11-12。

Day 1 livestream · [4:42:54–4:55:30 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16974s). The player starts and stops at this session’s boundaries.

## Introduction

Duolingo's iOS codebase contains roughly 1.8 million lines of code and a decade of accumulated decisions. Weekly releases and hundreds of concurrent experiments make test coverage valuable, but also make a sweeping rewrite unattractive. Kush Agrawal's account starts with a narrower opportunity: use coding agents to add tests to the parts of the application already structured to support them.

The title promises more than 200,000 lines of tests, not 200 million. The more instructive result is the system behind those lines: target selection, durable workflows, bounded retries, automated checks, human review, and feedback from rejected work.

## Start where tests can succeed

Duolingo had standardized newer code around model-view-viewmodel architecture, while a substantial legacy portion remained outside it. Agrawal begins with the standardized portion rather than treating every uncovered line as equally attractive.

He reports an initial 11% coverage across the codebase and 9% across the MVVM portion. Eight months later, those figures were 24% and 59%. The component breakdown moved from 11% to 72% for repositories, 9% to 58% for viewmodels, and 5% to 41% for data sources. These are Duolingo's reported measurements; the talk does not establish that every change was caused exclusively by the agent.

Tests serve two purposes in this account. They protect releases, and they provide a better feedback surface for future agent work. An agent that can check behavior has more to work with than one asked to infer correctness from a codebase alone.

[4:45:28 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17128s)

## Prove the workflow locally before scheduling it

At [04:45:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17128s), Agrawal lays out the loop: identify, write, verify, resolve, iterate. Temporal's Python workflows provide orchestration. S3 holds shared coverage state. Coding agents generate changes, GitHub manages pull requests and CI, and Datadog provides operational visibility.

The first version was a local command. It built the application with coverage, selected targets, delegated test writing, and opened pull requests. Early batches were not uniformly successful: one produced 17 PRs with eight merged; another produced 40 with 19 merged. Roughly half making it through was enough to reveal useful failure categories, not enough to justify pretending the workflow was finished.

Some problems were instructional. The repository mixed XCTest and Swift Testing, so the agent needed clearer rules. Other problems required changing the software itself. A large concrete user-client singleton was difficult to mock; the team introduced a protocol and linting to enforce the abstraction. Swift concurrency and timing-related flakiness needed better examples and testing skills. More prompting could not substitute for a testable architecture.

## Coverage becomes a work queue

In the production workflow, a GitHub Action generates coverage after merges to main and writes the latest report to S3. A selector ranks candidate files rather than simply taking the least-covered file.

MVVM code receives a boost. Legacy code is downweighted. UI code is excluded from this unit-test strategy where snapshot tests are a better fit. Large files receive a penalty. These choices encode the likelihood of obtaining a useful, reviewable contribution, not just the apparent size of a coverage gap.

Each selected file gets a child workflow. The agent clones the repository, reads the testing skill, writes tests and the necessary mocks or fakes, and opens a labeled pull request. The team's cloud-agent abstraction can be invoked from Slack, Temporal, or GitHub and can support different coding-agent backends. That abstraction also provides access to internal tools and cost logging.

The PR declares that its author is an agent. A human can approve, edit, reassign, or close it with feedback. Automation supplies work; it does not make the human approval disappear.

[4:50:40 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17440s)

## Most of the engineering is what happens after the PR opens

[![Duolingo's PR lifecycle workflow](https://ai.engineer/reading/code-2026/images/online-duolingo-tests-17440.jpg)](https://ai.engineer/reading/code-2026/images/online-duolingo-tests-17440.jpg)

*At [04:50:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17440s), the lifecycle branches between verification and resolution. The diagram makes clear that generation is only one part of keeping a PR moving.*

A recurring workflow examines open agent PRs and takes at most one action per PR per pass. Conflicted or sufficiently stale work is closed. Work with CI still running, or with a reviewer actively involved, is left alone. Green CI leads toward reviewer assignment. Red CI leads toward repair.

Deterministic problems such as pre-commit fixes go through deterministic automation. For test failures, an agent reads the logs and attempts a repair, with a maximum of five attempts before the PR is closed. Git blame helps identify a suitable reviewer. Auto-merge is downstream of approval, not a substitute for it. A rejected file can enter a 30-day cooldown so the workflow does not repeatedly hand humans the same unhelpful task.

The same machinery supports an on-demand mode. A human adds a test-writing label to a PR, and the system selects from that PR's changed files, creates a linked draft test PR, and reuses the existing verification and review lifecycle.

## Shorten feedback, then constrain shortcuts

The initial Linux environment could not run Xcode. Agents waited 20–30 minutes for CI feedback. Agrawal reports lint failures on 30.6% of PRs, with two rules accounting for 62% of those failures. Better examples, automatic fixes, and removing low-signal rules helped. Moving execution onto Mac runners allowed the agent to build and lint locally, closing a feedback loop that had previously required a remote round trip.

A separate problem was agents satisfying the goal by taking shortcuts: editing production code, deleting or disabling tests, or adding excessive waits. The defense is layered. Deterministic checks restrict changes to allowed test and support-file categories. An AI review identifies serious issues before human review. A specialized review agent checks for forbidden production edits, test deletion or disabling, and long waits. No single prose instruction carries the whole safety boundary.

Agrawal reports more than 700 human-approved merged PRs and 225,000 lines of tests. He also notes that humans increasingly write tests themselves, so a decreasing agent share can coexist with an improving testing culture. The purpose is healthier software, not maximizing an agent's share of commits.

He closes by applying the same loop to other migrations and modernization work, then speculates about replacing portions of the handcrafted PR decision tree with a fast classifier. That classifier is a proposed next step, not part of the demonstrated system. The shipped lesson is already substantial: a productive coding agent is often a carefully managed queue of changes, with as much design invested in rejection and repair as in generation.

Full transcript 440 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[4:42:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16974s) Hey everyone, thanks for tuning in.

[4:42:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16976s) Today I'm going to walk you through how

[4:42:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16977s) we use AI agents at Dualingo to write

[4:42:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16979s) and ship more than 200,000,000 lines of

[4:43:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16981s) unit tests on iOS codebase. I'll share

[4:43:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16983s) what we built and what we learned along

[4:43:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16984s) the way. Uh I'm Kush. I'm a staff

[4:43:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16986s) engineer on the platform team here at

[4:43:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16987s) Dualingo. My job is to build developer

[4:43:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16989s) tooling and AI assisted workflows for

[4:43:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16990s) the 100 plus engineers who contribute to

[4:43:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16991s) our client apps. Before Duelingo, I

[4:43:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16993s) spent close to a decade at Stripe and

[4:43:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16994s) Uber working across a few teams there.

[4:43:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16997s) Let's start with some background on the

[4:43:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=16998s) scale of mobile at Dualingo. Uh we ship

[4:43:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17001s) our apps to the app store every week. Um

[4:43:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17003s) we're also a very experiment-driven

[4:43:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17005s) company. So at any given point of time,

[4:43:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17006s) we have more than 600 AB tests running

[4:43:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17008s) live. And our code bases are pretty

[4:43:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17010s) mature. Both the iOS and Android apps

[4:43:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17012s) have been around for more than 10 years

[4:43:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17013s) at this point.

[4:43:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17015s) Here's also the number of executable

[4:43:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17016s) lines of app code in our iOS repository.

[4:43:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17018s) So, as you can see, back in 2019, we

[4:43:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17020s) were at about 200,000 lines, and today

[4:43:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17022s) we're hit close to 2 million. And as AI

[4:43:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17024s) assisted coding picks up, you can see

[4:43:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17025s) that curve starting to bend upward. And

[4:43:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17028s) it's not just the amount of code that's

[4:43:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17029s) changing, it's also who's writing it.

[4:43:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17031s) So, last year about 200 people

[4:43:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17033s) contributed to the iOS repository. And

[4:43:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17034s) this year, we've already crossed 250.

[4:43:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17036s) And a lot of these folks aren't even iOS

[4:43:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17038s) engineers. We have backend engineers,

[4:43:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17039s) Android engineers, even PMs and

[4:44:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17041s) designers all shipping code to the iOS

[4:44:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17042s) app and that's mostly been unlocked by

[4:44:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17044s) AI coding tools like cursor and cloud

[4:44:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17046s) code. Um, another thing to note about

[4:44:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17048s) our codebase is that it's a codebased in

[4:44:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17049s) transition. So a few years ago we

[4:44:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17051s) standardized on the MVVM architecture

[4:44:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17052s) pattern. Today about half the code in

[4:44:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17054s) our repository follows that pattern and

[4:44:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17056s) the other half is still legacy code that

[4:44:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17057s) we're in the process of migrating. Since

[4:44:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17059s) the MVVM half is the easiest to test,

[4:44:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17061s) that's where we focused on this project.

[4:44:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17064s) Here's where we started back in March of

[4:44:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17065s) this year. We were at overall unit test

[4:44:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17068s) coverage of 11%. The MVVM layers were a

[4:44:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17070s) bit lower. Repositories were at 11%,

[4:44:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17072s) view models at 9, data sources at five,

[4:44:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17074s) and combined we are about 9% for the

[4:44:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17076s) MBVM slice of the app.

[4:44:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17079s) So why does this matter now more than it

[4:44:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17081s) used to? As agents and humans write more

[4:44:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17083s) code and write it faster, writing code

[4:44:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17085s) isn't the hard part anymore. Verifying

[4:44:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17086s) it is. So when someone puts up a PR, how

[4:44:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17089s) do you know that it's actually safe to

[4:44:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17090s) ship? The bottleneck is really shifting

[4:44:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17091s) from writing to verifying. And that's

[4:44:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17094s) where unit tests come in. They make up

[4:44:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17095s) the base of the testing pyramid. They're

[4:44:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17097s) pretty cheap to write and fast to run.

[4:44:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17098s) And they also act as guardrails for

[4:44:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17099s) agents. So when an agent's change breaks

[4:45:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17101s) a test in CI, it gets immediate feedback

[4:45:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17103s) on what to fix. They also act as living

[4:45:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17105s) documentation on what the code is

[4:45:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17106s) supposed to do. And here's where we

[4:45:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17108s) ended up 8 months later. Overall unit

[4:45:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17109s) test coverage went from 11% to 24%,

[4:45:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17112s) repositories went from 11 to 72, view

[4:45:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17114s) models from 9 to 58, data sources from 5

[4:45:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17116s) to 41, and the combined MVVM slice of

[4:45:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17118s) the app went from 9% to 59%. So what do

[4:45:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17121s) we actually end up building? On paper,

[4:45:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17123s) it's a pretty simple loop. First you

[4:45:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17125s) identify the files that need tests. Then

[4:45:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17126s) you write those tests with an agent. You

[4:45:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17128s) verify that the tests are good quality

[4:45:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17129s) and they pass CI. Then you resolve the

[4:45:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17131s) PR which means getting reviewed by an

[4:45:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17132s) engineer merged. And finally iterate on

[4:45:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17134s) the feedback so that the next batch of

[4:45:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17136s) PRs is better than the last one. When

[4:45:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17138s) production it's a little messier. This

[4:45:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17140s) is what our system ended up looking

[4:45:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17141s) like. I won't go through every box right

[4:45:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17142s) now, but at a high level it's a few

[4:45:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17144s) temporal workflows that coordinate

[4:45:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17145s) through shared state stored in S3. And

[4:45:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17147s) every box you see here maps back to one

[4:45:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17149s) of the five steps I just talked about.

[4:45:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17151s) Here are the building blocks that we

[4:45:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17152s) ended up using. Temporal handles

[4:45:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17154s) workflow orchestration and execution.

[4:45:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17156s) Cloud code acts as the coding agent. S3

[4:45:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17158s) holds the shared state that keeps our

[4:45:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17159s) workflows in sync. And we use GitHub for

[4:46:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17161s) actions, labels, and PRs. Data dogs acts

[4:46:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17164s) as an observability layer where we keep

[4:46:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17165s) an eye on the health of our pipelines.

[4:46:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17168s) If you haven't used temporal before,

[4:46:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17169s) it's basically a durable workflow

[4:46:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17171s) execution engine. You write your

[4:46:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17172s) workflows as normal Python code, and if

[4:46:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17174s) a worker crashes, the workflow just

[4:46:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17175s) picks up right where it left off. This

[4:46:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17177s) fits agents really well. An agent

[4:46:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17179s) session can run for seconds to hours and

[4:46:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17180s) it can call out to tools like GitHub,

[4:46:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17182s) CI, S3 and Claude. We also lean on a few

[4:46:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17185s) built-in features of temporal. There are

[4:46:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17187s) schedules which are basically crown-like

[4:46:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17188s) schedules for our jobs. There are

[4:46:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17190s) composible workflows so that we can fan

[4:46:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17191s) out work in parallel. Then there's first

[4:46:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17193s) class support for retries and timeouts

[4:46:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17194s) and item potency so that we never kick

[4:46:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17196s) off duplicate runs of the same file.

[4:46:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17198s) To split up this work, we split this

[4:46:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17200s) project into four milestones. The first

[4:46:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17202s) was local validation. Basically, is this

[4:46:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17204s) project even viable? The second was a

[4:46:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17205s) scheduled backfield workflow to write

[4:46:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17207s) tests for existing code. The third was a

[4:46:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17209s) PR life cycle workflow to actually get

[4:46:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17211s) those PRs merged. And the fourth was a

[4:46:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17212s) label trigger so engineers can get tests

[4:46:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17214s) for the new code that they're writing.

[4:46:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17216s) Now, we'll go through each of these in

[4:46:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17217s) order. Before building anything real, we

[4:46:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17219s) wanted to do the least amount of work

[4:47:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17220s) possible that would tell us whether an

[4:47:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17222s) agent could actually do this job well

[4:47:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17223s) and do it at scale. We started with a

[4:47:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17225s) very simple local clot code setup where

[4:47:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17227s) we had one cloud code command that acted

[4:47:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17228s) as an orchestrator. It ran an Xcode

[4:47:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17230s) build script to generate a code coverage

[4:47:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17232s) report locally. Then it fed that report

[4:47:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17234s) through a file selection script that we

[4:47:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17235s) wrote and then it handed each selected

[4:47:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17237s) file off of sub two sub aents. One wrote

[4:47:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17240s) the tests and the other one opened the

[4:47:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17241s) PR. We ran this in a loop and generated

[4:47:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17243s) a bunch of PRs. We basically ran this in

[4:47:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17246s) two batches. The first batch had 17 PRs

[4:47:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17247s) and we merged eight of them. The second

[4:47:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17249s) had 40 PRs and we merged 19. So that's

[4:47:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17251s) roughly a 50% merge rate. But the goal

[4:47:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17252s) here wasn't to merge a lot of PRs. It

[4:47:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17254s) was to learn how the agents fail and to

[4:47:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17255s) fix those paper cuts before

[4:47:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17256s) productionizing anything. Here are some

[4:47:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17258s) of the failure modes that we saw. Since

[4:47:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17260s) we're a large legacy code base with both

[4:47:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17261s) XC test and swift testing, the agents

[4:47:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17263s) would sometimes get confused and mix the

[4:47:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17264s) two in one file. We fixed that by giving

[4:47:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17266s) the agents clear rules on when to use

[4:47:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17267s) each. We also had a giant user client

[4:47:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17269s) singleton class. Some code passed around

[4:47:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17271s) the concrete version of this class which

[4:47:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17272s) is really hard to mock whereas others

[4:47:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17273s) passed around a protocolized version. So

[4:47:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17275s) we migrated the entire code base over to

[4:47:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17276s) the protocolized version and added lint

[4:47:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17278s) rule to enforce it. This made the whole

[4:48:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17280s) host of files easier to test for agents

[4:48:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17282s) and for humans. We also ran to six

[4:48:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17285s) concurrency related issues and agents

[4:48:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17286s) writing timing based tests which are a

[4:48:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17288s) big source of flakiness in CI. So we

[4:48:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17290s) improved the state for both of these

[4:48:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17291s) with better rules and examples in our

[4:48:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17292s) testing skills.

[4:48:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17294s) Now this brings us to milestone 2. Since

[4:48:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17296s) we're so far behind on code coverage,

[4:48:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17297s) the biggest leverage that we saw was

[4:48:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17299s) backfilling tests for code that was

[4:48:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17300s) already merged in. That's where the

[4:48:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17302s) scheduled backfill workflow comes in.

[4:48:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17303s) This is a system design diagram of our

[4:48:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17305s) workflow as it runs in production. And

[4:48:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17306s) it essentially does two jobs. The left

[4:48:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17308s) half is to identify which is picking the

[4:48:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17310s) files that need tests and the right half

[4:48:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17312s) is right which is having the agents

[4:48:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17314s) actually write those tests. Let's start

[4:48:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17316s) with identify. Every time a PR merges to

[4:48:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17318s) the main branch in the iOS repo, we kick

[4:48:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17320s) off a GitHub access job that generates

[4:48:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17321s) an Xcode coverage report and uploads it

[4:48:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17323s) to S3 that becomes a source of truth for

[4:48:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17325s) the latest code coverage. The backfield

[4:48:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17327s) workflow then fetches that report and

[4:48:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17328s) runs it through a selector script which

[4:48:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17329s) picks the next set of files to test.

[4:48:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17332s) Let's get a deeper a little deeper into

[4:48:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17333s) the selector script. Its job is

[4:48:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17335s) essentially to score every Swift file

[4:48:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17336s) based on how confident we are that an

[4:48:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17338s) agent can write a good test for it. The

[4:49:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17340s) strongest signal is file type. So view

[4:49:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17342s) models, repositories, and data sources

[4:49:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17343s) get a 2.5x boost while legacy files get

[4:49:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17345s) pushed down. We skipped UI code

[4:49:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17347s) completely for now since snapshot tests

[4:49:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17348s) are better fit there and larger files

[4:49:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17350s) also get a penalty. So we prioritize

[4:49:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17352s) code that we're confident that we can

[4:49:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17353s) test well.

[4:49:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17355s) The next step is to actually write the

[4:49:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17357s) tests. We kick off one child workflow

[4:49:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17359s) per file all running in parallel. In

[4:49:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17361s) each one of these runs, the agent clones

[4:49:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17362s) the iOS repository, reads the testing

[4:49:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17364s) skill that we keep in the repo, which

[4:49:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17366s) spells out how to write a good test.

[4:49:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17368s) Then it writes the test plus any mocks

[4:49:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17369s) and fakes it needs and opens a PR with a

[4:49:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17371s) generated test label so we can identify

[4:49:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17373s) it easily later.

[4:49:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17375s) These agents run on Dualingo's cloud

[4:49:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17377s) coding agent which is a platform that

[4:49:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17378s) also runs on Nepor. The simplest way to

[4:49:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17380s) think about it is as an abstraction on

[4:49:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17381s) top of cloud code and codex running in

[4:49:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17382s) the cloud. We can invoke it from slack,

[4:49:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17384s) temporal or github. It talks to a bunch

[4:49:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17386s) of our internal tools for MCP and it

[4:49:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17387s) logs a bunch of events so we can see

[4:49:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17389s) what each agent run is doing and how

[4:49:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17390s) much it costs. We started running these

[4:49:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17393s) on Linux machines and then later move

[4:49:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17395s) them to MacRunners which will become

[4:49:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17396s) important in a minute. Here's what a

[4:49:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17398s) generated test PR looks like. Every PR

[4:50:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17400s) description follows the same template

[4:50:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17402s) and it says explicitly that the PR is AI

[4:50:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17404s) generated. The reviewer has four

[4:50:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17405s) options. They can approve it in the PR

[4:50:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17407s) auto modes. They can push changes to it

[4:50:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17409s) directly. They can reassign it to

[4:50:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17410s) someone better suited or they can close

[4:50:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17411s) it out with feedback on why it isn't

[4:50:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17413s) mergeable.

[4:50:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17414s) Now once we had the backfill running in

[4:50:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17416s) production, we had a slightly new

[4:50:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17417s) problem. We suddenly had tens of tens to

[4:50:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17419s) hundreds of open PRs that nobody could

[4:50:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17420s) manage by hand. So how do we get all of

[4:50:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17422s) these to a mergeable state and in front

[4:50:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17424s) of the right reviewer?

[4:50:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17426s) That's where the PR life cycle workflow

[4:50:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17427s) comes in. You can think of it as a state

[4:50:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17429s) machine. It runs every couple of hours,

[4:50:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17430s) looks through every open generated test

[4:50:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17432s) PR and takes exactly one action on each.

[4:50:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17435s) It covers the next two steps of our

[4:50:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17436s) loop. Verify, which is does this PR pass

[4:50:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17439s) CI and is it high quality and resolve,

[4:50:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17440s) which is getting a human to review it

[4:50:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17442s) and merge it. The logic for this

[4:50:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17444s) workflow is a simple decision tree. If

[4:50:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17446s) there are any merge conflicts or the PR

[4:50:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17447s) has been open for about 3 weeks, we

[4:50:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17448s) close it out and mark it as still. If CI

[4:50:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17450s) is still running or a reviewer is

[4:50:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17451s) already on it, we skip it. If CI is

[4:50:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17453s) green and there's no reviewers, we find

[4:50:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17454s) one and sign them. If CI is red, we try

[4:50:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17456s) to fix it. And if the reviewer rejects

[4:50:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17458s) the PR, the file goes into 30-day cool

[4:51:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17460s) down. So we're not spamming engineers

[4:51:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17461s) with the same PR again and again.

[4:51:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17463s) When CI fails, the first thing we check

[4:51:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17465s) is which job failed. If it's pre-comit,

[4:51:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17467s) a GitHub action applies the fix. It's

[4:51:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17469s) cheap, it's deterministic, and there's

[4:51:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17470s) no agent needed. If it's a real test

[4:51:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17472s) failure, we kick off another agent that

[4:51:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17473s) reads the CI logs and pushes a fix to

[4:51:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17474s) the PR. We cap that whole loop at five

[4:51:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17477s) attemps. Pass that we close the PR

[4:51:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17478s) rather than trying to fix it forever.

[4:51:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17480s) Once CI is green, we need to find the

[4:51:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17482s) right reviewer. What we do is we run get

[4:51:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17484s) blame on the source file being tested.

[4:51:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17485s) find the top contributor and assign it

[4:51:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17487s) to them and turn on auto merge. If they

[4:51:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17488s) approve it, the PR gets merged. If they

[4:51:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17490s) reject it, the file goes into the 30-day

[4:51:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17491s) cool down which I previously mentioned.

[4:51:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17493s) This brings us to milestone four. Once

[4:51:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17495s) all of this was back filling tests for

[4:51:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17497s) existing code, we wanted to make it just

[4:51:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17498s) as easy to get tests for the new code

[4:51:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17500s) engineers were writing. Now, any

[4:51:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17502s) engineer can add or write test label to

[4:51:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17503s) their own PR. It hooks into the same

[4:51:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17505s) temporal infrastructure we just walked

[4:51:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17506s) through. The only real difference is

[4:51:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17508s) selection. Instead of the selection

[4:51:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17509s) script, we take the file straight from

[4:51:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17510s) the engineer's PR. The agent writes the

[4:51:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17512s) test and you get a draft SPR link back

[4:51:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17514s) to your original one. Now let's talk

[4:51:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17515s) about some of the challenges that we ran

[4:51:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17516s) into. Our agents originally ran on Linux

[4:51:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17519s) machines which don't have X code of Lint

[4:52:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17521s) installed. So when an agent would open a

[4:52:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17522s) PR after about 20 or 30 minutes CI would

[4:52:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17524s) fail frequently on Lint. This waste the

[4:52:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17526s) agents time and CI time as well which is

[4:52:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17528s) an increasingly scarce resource. For a

[4:52:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17530s) while 30.6% of our PRs were failing due

[4:52:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17532s) to lint and then when we dug into it 62%

[4:52:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17534s) of those failures came from just two

[4:52:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17535s) lint rules. We fixed this in layers. The

[4:52:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17538s) first was better examples in the prompt

[4:52:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17540s) along with pitfalls to avoid. The second

[4:52:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17542s) was a GitHub action that autofixes lint

[4:52:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17543s) errors in CI. The third was an audit of

[4:52:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17545s) the rules that couldn't be autofixed. We

[4:52:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17547s) essentially removed the ones that

[4:52:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17548s) weren't high signal. And this made life

[4:52:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17549s) easier for both agents and human

[4:52:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17551s) engineers. And finally, the real fix

[4:52:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17552s) came when we moved the agents to Mac

[4:52:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17554s) runners. So now the agents could build

[4:52:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17556s) and lend the code locally before opening

[4:52:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17557s) up PR. The second challenge was PR

[4:52:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17560s) quality. When we assign a PR to a human,

[4:52:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17562s) we want it to be something they'd

[4:52:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17563s) actually feel comfortable proving. But

[4:52:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17565s) agents sometimes take the shortest path

[4:52:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17566s) to green CI. We saw agents editing

[4:52:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17568s) production code to make a failing test

[4:52:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17570s) pass. We also saw them modifying,

[4:52:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17571s) deleting or silencing existing tests.

[4:52:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17572s) And then we saw them adding long weight

[4:52:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17574s) to tests which can make CI flicky.

[4:52:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17577s) Again, there was no single fix here. So

[4:52:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17578s) we built three layers. The first is the

[4:53:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17580s) deterministic rule. If a PR touches any

[4:53:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17582s) file that isn't a test, a mock, a fake

[4:53:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17584s) or a stop, we close it out. The second

[4:53:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17586s) builds in our AI code review. At

[4:53:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17588s) Dualingo, we use Claude and Codex to

[4:53:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17589s) review every PR and those bots often

[4:53:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17591s) leave comments. So we built an agent

[4:53:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17593s) that resolves any P 0 comments before a

[4:53:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17595s) human ever looks at the PR. And the

[4:53:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17597s) third is an LLM as a judge. It's a

[4:53:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17598s) reviewer agent built just for these test

[4:53:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17600s) PRs. It reads the PR diff and rejects

[4:53:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17602s) production edits, changed or deleted

[4:53:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17604s) tests, disabled tests, and long weights.

[4:53:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17606s) And as you learn more, we keep adding

[4:53:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17607s) additional checks to it.

[4:53:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17610s) So far, the LLM as a judge has reviewed

[4:53:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17611s) about,200 PRs and rejected 73 of them.

[4:53:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17614s) Every rejection comes with a comment

[4:53:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17615s) like this one saying exactly why the PR

[4:53:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17617s) was rejected. We then read that feedback

[4:53:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17619s) and fold it back into our prompts and

[4:53:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17620s) skills so the same mistakes get less

[4:53:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17622s) likely each time. So, let's talk about

[4:53:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17624s) what all of this added up to. Since we

[4:53:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17626s) started, the pipeline has merged more

[4:53:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17627s) than 700 test PRs, adding about 225,000

[4:53:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17630s) lines of test code. Every one of those

[4:53:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17632s) PRs was reviewed and approved by a

[4:53:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17633s) human. MVVM test coverage went from 9%

[4:53:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17636s) to 59% and overall coverage went from

[4:53:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17638s) 11% to 24%. Most importantly, we now

[4:54:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17640s) have a code base so engineers and agents

[4:54:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17642s) can ship faster and with more

[4:54:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17643s) confidence. Here's a few more

[4:54:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17645s) interesting stats. Since March, the

[4:54:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17646s) pipeline has written 34% of all new test

[4:54:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17648s) files in the repo, 44% of all new test

[4:54:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17650s) cases, and 10% of every strip line added

[4:54:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17652s) to the codebase. And interestingly, that

[4:54:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17653s) share has actually dripped in the last

[4:54:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17655s) few weeks because engineers are now

[4:54:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17656s) writing a lot more tests themselves,

[4:54:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17657s) which is honestly the end goal.

[4:54:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17660s) Um, and here's the coverage curve since

[4:54:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17662s) April when the backfield started running

[4:54:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17663s) on a schedule. You can see it bend

[4:54:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17665s) slightly upward around June and July,

[4:54:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17666s) which is when we really wrapped up the

[4:54:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17668s) pipeline.

[4:54:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17669s) So, what have we learned while doing

[4:54:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17670s) this project? The first thing is that

[4:54:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17672s) this pattern generalizes the loop we

[4:54:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17674s) talked about identify, write, verify,

[4:54:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17676s) resolve, iterate, it isn't specific to

[4:54:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17677s) testing. Unit tests were just the lowest

[4:54:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17679s) hanging fruit and any job that fits the

[4:54:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17680s) shape can run on the same

[4:54:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17681s) infrastructure. And that's exactly what

[4:54:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17683s) we're starting to do as a company. We're

[4:54:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17684s) applying the same loop to modernization

[4:54:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17686s) to modernizing screens to MVBM and Swift

[4:54:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17688s) UI, migrating code uh on Android to

[4:54:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17690s) Corines and generating snapshot tests.

[4:54:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17693s) So before I wrap up, I want to leave you

[4:54:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17695s) with a thought experiment. There's a new

[4:54:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17697s) class of fast general purpose

[4:54:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17698s) classifiers like Jev. They take in some

[4:55:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17700s) state and output an action in

[4:55:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17701s) milliseconds. So what if we replace a

[4:55:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17702s) handwritten decision tree in the VR life

[4:55:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17704s) cycle workflow with one of these? PR

[4:55:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17706s) state goes in, the classifier picks the

[4:55:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17708s) next action and we execute it all in

[4:55:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17709s) milliseconds.

[4:55:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17712s) I also want to thank a few folks who

[4:55:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17713s) worked on this with me. Jesse, Gordalup,

[4:55:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17715s) Hunter, and Jiha. They built a lot of

[4:55:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17716s) the platform pieces this project stands

[4:55:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17718s) on and helped review a lot of this code.

[4:55:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17720s) That's it for me. Thank you so much for

[4:55:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17721s) making it this far. If you want to go

[4:55:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17723s) deeper, we've written about this

[4:55:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17723s) pipeline on the dual engineering blog.

[4:55:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17725s) And I'd also love to hear from you if

[4:55:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17726s) you're building something similar. You

[4:55:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=17727s) can find me on LinkedIn or next.
