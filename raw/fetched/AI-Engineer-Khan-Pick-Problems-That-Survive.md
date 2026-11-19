---
title: Pick Problems That Survive When AI Solves Coding — Ara Khan
description: AI Engineer CODE 2026 官方閱讀版，Ara Khan 談監督 agent 自動改 Cline harness 與職涯選題，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-cline-rsi
published:
tags:
  - clippings
  - coding-agent
  - evaluation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 Cline 被辨識成 Klein／client、Kimi K3 被辨識成 Kim K3／Ky K3、GPT-5.6 Sol 被辨識成 GPD 5.6 soul）。逐字稿對應 Day 1 直播 `https://www.youtube.com/watch?v=ZZ19zhYnDKY`（本場為 3:59:46–4:26:17 預錄線上場）。

Day 1 livestream · [3:59:46–4:26:17 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14386s). The player starts and stops at this session’s boundaries.

## Introduction

A coding agent can help build the system that makes coding agents better. That observation is easy to turn into a story about a distant intelligence explosion. Ara Khan instead begins with a nearer question: what should an engineer work on when a new model can erase the value of a side project overnight?

His answer is to move closer to the improvement loop. Not every application that calls a model participates in that loop. The distinguishing feature is a measurable feedback process: run something, observe where it fails, make a change, and find out whether the change survives another test. Khan connects that practical engineering discipline to recursive self-improvement, while leaving a considerable distance between the experiment he demonstrates and the future he imagines.

[4:09:01 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14941s)

## From answering questions to changing environments

Khan frames the recent progression of assistants as an expansion of what they can act on. A question-answering system produces text. A tool-using system can search, edit files, launch processes, and inspect the consequences. A coding agent can combine those actions into a task whose intermediate steps were not all specified in advance.

That changes evaluation. Asking an assistant a question and scoring its answer is not the same as asking it to set up an MCP integration. The latter might require finding configuration instructions, downloading dependencies, changing files, connecting a database, and running commands. The agent's final assertion that it succeeded is weak evidence. The environment must actually work.

At [04:09:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14941s), Khan turns to Terminal-Bench and the engineering around it. Tasks run in isolated environments with independent grading. The useful output is not just a score but a trajectory: tool calls, elapsed time, token use, and the sequence that led to success or failure. Evaluation also needs to distinguish genuine task completion from looking up a solution or exploiting the grader.

A failure can have very little to do with the model's abstract intelligence. A file-reading tool might be broken. A background process might not be managed correctly. The agent might repeat an action without recognizing that it is making no progress. Inference delays can consume the available time. Once those failures are classified, a harness becomes a collection of repairable mechanisms rather than an opaque wrapper around a model.

[4:13:00 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15180s)

## Put another agent around the evaluation loop

The next step is to give a supervising agent access to that process. It runs evaluations, reads failures, modifies the Cline harness, and runs the evaluation again. The evaluated agent is trying to complete individual tasks. The supervising agent is trying to improve the machinery used across tasks.

[![Terminal-Bench score chart showing Cline harness improvements](https://ai.engineer/reading/code-2026/images/online-cline-rsi-15180.jpg)](https://ai.engineer/reading/code-2026/images/online-cline-rsi-15180.jpg)

*At [04:13:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15180s), Khan's slide separates a baseline, a frozen full-stack result, and a best run. Its intermediate step heights are explicitly schematic, not isolated measurements of each change.*

The chart makes the interventions concrete: bounded provider retries, progress-aware loop detection, file-index request liveness, and safe background-process guidance. The baseline is 69 of 89 tasks, or 77.5%. The frozen full stack reaches 77 of 89, or 86.5%; the best run is 79 of 89, or 88.8%. The slide also reports other configurations and a repeated mean of 77.5 of 89. These are Khan's presented results, not an independently reproduced benchmark.

The qualifications on the chart matter as much as the upward line. It says individual contributions were not isolated, retry attribution was partly ambiguous, process guidance was not enforcement, and two interrupted runs were excluded. This is evidence that an automated improvement process can find useful harness changes. It is not evidence that every step caused the amount of improvement suggested by its visual height, or that the best run is the only number worth reporting.

Khan also distinguishes this outer loop from an agent rewriting itself in the middle of a task. An immediate change can make the current task easier while making the general system worse. A harness improvement needs to transfer across a broader set of tasks. Otherwise the apparent self-improvement is task-specific overfitting.

## The same structure reaches below the harness

From there, Khan broadens the argument. Harnesses are one layer in a stack that includes training data, post-training, inference, kernels, and eventually hardware and physical interaction. He cites work on kernel optimization as an example of models contributing to the infrastructure on which models run. The general claim is not that a single agent has already mastered all of these layers. It is that each layer can expose a measurable objective and a feedback loop.

Even an ordinary human correction can become material for that process. If a model gets a cache's time-to-live behavior wrong, the correction is a small demonstration of a capability gap. Capturing the situation as a reproducible task is more useful than merely telling the agent the answer and moving on. The failure can become an evaluation or training signal.

Khan's physical example brings the abstraction back down to earth. A small device with a camera, microphone, and speaker can be impressive yet frustratingly slow. Improving it requires measuring end-to-end latency and locating the delay: firmware, tool calls, the model, speech recognition, or another component. Connect the device to a computer, expose tests, ask it questions about what it perceives, and let a coding agent work through the resulting measurements. The talk proposes that improvement workflow; it does not establish a particular measured speedup for the device.

[4:20:20 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15620s)

## Connecting loops is a forecast, not a benchmark result

At [04:20:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15620s), the argument becomes explicitly systemic. Cheaper inference buys more experiments per dollar. More experiments can improve data, models, or infrastructure. Those improvements might make subsequent experimentation cheaper again. Recursive self-improvement is the possibility that these loops reinforce one another.

The small harness experiment and the large economic forecast should not be conflated. Khan is concerned about who captures the gains if capability concentrates in model and infrastructure providers. His discussion of engineering careers follows from that concern, not from a demonstrated timetable for an intelligence explosion.

He recommends working on problems that benefit from scale without simply disappearing when scale arrives: inference, data, networking, hardware, post-training, and the infrastructure that converts a promising experiment into a reliable improvement. He also argues for attempting more ambitious projects with small, capable groups as the cost of iteration falls. Sometimes a task that is awkward today may be worth revisiting when the next model arrives rather than forcing an elaborate workaround now.

The practical destination is narrower than the grand title suggests. Build something that can tell whether it got better. Give the agent access to that evidence. Preserve the distinction between a local fix and a transferable improvement. Whatever happens to the larger recursive loop, those are useful engineering properties now.

Full transcript 764 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[3:59:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14386s) Uh, hey guys, this is Era. I'm a

[3:59:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14389s) founding engineer at Klein and today I'm

[3:59:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14391s) going to be talking about recursively

[3:59:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14392s) self-improving coding agents. So this is

[3:59:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14395s) a very interesting conversation in the

[3:59:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14399s) sense that everyone wants to understand

[4:00:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14401s) what RSI is, how we accomplish it, how

[4:00:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14403s) we go through it and how it affects our

[4:00:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14404s) career. So I'm going to start with

[4:00:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14406s) giving you just three goals of this

[4:00:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14408s) entire conversation. Just three simple

[4:00:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14410s) goals and that would help you understand

[4:00:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14413s) like what what we get out of it and what

[4:00:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14414s) the future uh for this looks like. So

[4:00:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14416s) the goal number first is that

[4:00:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14418s) understanding the intent of Frontier

[4:00:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14419s) Labs, right? Everyone who's outside of

[4:00:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14421s) the frontier lab is always trying to

[4:00:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14422s) speculate like hey what what is the

[4:00:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14424s) topic in open or what is deep mind going

[4:00:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14426s) to come out with or what what are they

[4:00:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14427s) trying to make and what's the future

[4:00:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14429s) going to look like who has cracked the

[4:00:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14431s) RSI so like this kind of helps you get

[4:00:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14434s) get a rough outline of what their road

[4:00:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14436s) map looks like and the second thing is

[4:00:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14437s) that like if the models are improving so

[4:00:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14440s) fast like how do you think about your

[4:00:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14441s) career or the next few years right that

[4:00:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14444s) is really what we want to understand we

[4:00:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14445s) want to understand like okay things are

[4:00:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14448s) changing so fast like the ground

[4:00:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14450s) underneath us is shifting so quickly.

[4:00:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14452s) Right now like it's like uh

[4:00:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14455s) there used to be a time when you could

[4:00:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14456s) like demonstrate your side projects on

[4:01:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14460s) your personal website or GitHub and now

[4:01:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14462s) it's just like you could literally

[4:01:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14463s) oneshot them using any Frontier Coding

[4:01:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14465s) Engine and with that it's like it's like

[4:01:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14468s) oh well how how do we demonstrate proof

[4:01:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14470s) of work? How do we demonstrate you know

[4:01:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14472s) that that that we know what we're doing

[4:01:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14474s) and how do we think of our career for

[4:01:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14475s) the next coming years, right? So it's a

[4:01:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14478s) very interesting times that we're living

[4:01:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14480s) in. And then the third and the most

[4:01:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14481s) important goal of the conversation is

[4:01:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14482s) escaping the permanent underclass,

[4:01:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14485s) right? So I know this seems like a joke,

[4:01:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14487s) but this really is a very valid

[4:01:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14489s) possibility that people are

[4:01:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14491s) contemplating, everyone's like, "Oh

[4:01:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14492s) well, if everything that we want to be

[4:01:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14495s) doing can potentially easily done by a

[4:01:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14497s) frontier model, like what are we what

[4:01:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14498s) are we good for?" And like where does

[4:01:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14500s) software go? Where where does the future

[4:01:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14502s) of technology going to go? And what are

[4:01:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14503s) we going to do as as things evolve so

[4:01:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14505s) fast, right? So I think that there's

[4:01:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14508s) like a lot of like fear-mongering but

[4:01:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14510s) also there's like some very valid merge

[4:01:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14512s) where people are concerned that like if

[4:01:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14514s) all the revenue of the planet is going

[4:01:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14516s) to go to um a few hardware companies

[4:01:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14519s) that make frontier GPUs and then a few

[4:02:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14521s) few uh AI companies that that make the

[4:02:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14525s) best models like how are we how are the

[4:02:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14527s) rest of us going to throw in what what

[4:02:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14528s) are we going to do here? So, I think

[4:02:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14531s) I'll I'll walk you through a few

[4:02:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14532s) examples and a few ideas that will like

[4:02:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14534s) really really help you reconsider the

[4:02:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14537s) career choices and and and the life

[4:02:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14539s) choices you're making and what your

[4:02:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14540s) problems you're picking up. And then and

[4:02:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14542s) then that will help you like realign

[4:02:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14545s) what it is that we should be working on

[4:02:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14547s) and what it is that you you know would

[4:02:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14549s) would that you could work on that will

[4:02:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14551s) stand the test of time and help you both

[4:02:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14553s) just not just like on a psychological

[4:02:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14555s) but like financial and other levels as

[4:02:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14556s) well. So uh to give you a very precise

[4:02:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14558s) example, let's start with something very

[4:02:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14560s) precise that I had done. So a couple

[4:02:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14562s) months ago I uh came up with recursive

[4:02:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14567s) improve improvements on a coding

[4:02:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14569s) harness. So this was the first probably

[4:02:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14571s) public example of uh an automatic eval

[4:02:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14574s) improvement. So to give you an example u

[4:02:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14577s) we \[snorts\] used to do this thing where

[4:02:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14578s) we would measure the quality of a coding

[4:03:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14581s) agent using evaluation scores.

[4:03:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14584s) on terminal bench 2.1 Kim K3 with client

[4:03:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14587s) would score um usually like you know um

[4:03:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14590s) 60 70% and then depending on like how

[4:03:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14594s) good the model is like you get better

[4:03:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14595s) scores on on terminal bench 2.1 so we

[4:03:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14598s) noticed that when Kim K3 came out our

[4:03:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14599s) score was 77.5% which is a good score

[4:03:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14602s) but we were like oh is this is this

[4:03:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14604s) truly is it truly the best score that

[4:03:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14606s) this model can get on this benchmark and

[4:03:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14608s) also like what does the model release

[4:03:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14611s) paper claim about what their best score

[4:03:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14613s) is so the model release paper said that

[4:03:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14614s) they could score up to 85% or even more.

[4:03:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14617s) So we were just like okay okay so we are

[4:03:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14620s) not getting the sort of score and often

[4:03:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14621s) what we do with model releases in client

[4:03:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14623s) is that we try to like optimize your

[4:03:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14625s) score and try to get the best out of the

[4:03:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14626s) model. So when we started hill climbing

[4:03:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14630s) on the on the model like we we realized

[4:03:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14633s) is we realized that like you know

[4:03:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14635s) there's a lot of steps that we do says

[4:03:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14637s) that we do it gracefully says that we

[4:03:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14638s) pursue the right kind of problems and do

[4:04:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14640s) it the right way and we started thinking

[4:04:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14643s) like okay if we there's a lot of ground

[4:04:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14645s) work here how do we automate it and this

[4:04:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14647s) is a demonstration of like how we

[4:04:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14648s) automated it. So I'll I'll just leave

[4:04:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14650s) that as a placeholder for now and we'll

[4:04:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14652s) get get back to it later where we talk

[4:04:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14653s) about in detail of like how does like

[4:04:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14655s) this automatic improvement loop of a

[4:04:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14658s) client harness work. So this basically

[4:04:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14660s) means that like you have a coding a

[4:04:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14661s) harness that could just like basically

[4:04:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14662s) improve itself and become better on on

[4:04:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14665s) the same set of problems. So let's start

[4:04:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14667s) with the ground terms. What is recursive

[4:04:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14669s) self? Recursive self-improvement is the

[4:04:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14671s) idea that an AI system that helps

[4:04:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14673s) \[snorts\] build a more capable successor

[4:04:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14676s) which repeats the process you know until

[4:04:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14677s) you hit artificial general intelligence

[4:04:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14680s) right you have better systems you have

[4:04:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14681s) better improvements you have a better

[4:04:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14682s) system and then you know you have

[4:04:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14683s) singularity so a classic example is like

[4:04:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14686s) a self-reing coding agent right

[4:04:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14688s) self-reving coding agent is just like a

[4:04:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14690s) coding agent that can improve itself so

[4:04:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14692s) you know this this is all like a pie in

[4:04:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14694s) the sky idea like it's like it's like

[4:04:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14695s) you know yeah sure this looks cool but

[4:04:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14697s) how how did this even come out to be

[4:04:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14698s) like how we even get to here. So if you

[4:05:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14702s) notice in topics road map in 2021 in

[4:05:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14705s) 2021's road map they very specifically

[4:05:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14707s) said that uh uh they wanted to develop a

[4:05:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14710s) general AI assistant that can interact

[4:05:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14712s) conversationally with a user to create

[4:05:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14714s) edit and explain software. It would

[4:05:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14716s) display all the capabilities of a

[4:05:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14718s) software engineer colleague. It would

[4:05:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14719s) write functions. It would identify bugs.

[4:05:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14721s) It would design an API discuss style and

[4:05:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14723s) best practices. Right? So we don't

[4:05:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14725s) expect to reach this goal right away but

[4:05:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14726s) it's in the direction which we're

[4:05:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14727s) striving. It's interesting how this was

[4:05:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14729s) more than five years ago. More than five

[4:05:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14731s) years ago, people had predicted that

[4:05:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14733s) there exist a day where you will have

[4:05:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14736s) like a full-blown journal assistant that

[4:05:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14737s) can basically act like a colleague,

[4:05:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14739s) which we do have right now. Um, then in

[4:05:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14741s) 2022, Chad Deputy got released. We all

[4:05:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14743s) know how that happened. It was it was a

[4:05:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14745s) fun moment. It was like the first time

[4:05:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14747s) things got sparked for us. Um, then in

[4:05:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14750s) 2023, 2024, there was the first time

[4:05:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14753s) chat models could call functions. These

[4:05:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14756s) functions would be simple functions like

[4:05:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14757s) hey what's the weather or you know

[4:05:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14759s) what's the what's you know what's this

[4:06:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14762s) competition over this computations

[4:06:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14764s) result in Python. Um and then finally in

[4:06:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14766s) 2024 when s 345 was released that was

[4:06:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14769s) when the agents could like truly call

[4:06:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14771s) like actual tools the way we call like

[4:06:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14774s) think of tools. So it's like reading a

[4:06:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14775s) file editing a file you know reading

[4:06:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14778s) searching something on web uh listing

[4:06:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14780s) listing a folder searching and grapping

[4:06:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14782s) through you know uh a file system things

[4:06:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14784s) like that. So and in 2024 we had the

[4:06:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14787s) intuition that like chatbot what if

[4:06:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14789s) chatbox could actually talk to each

[4:06:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14791s) other you know so then that's was the

[4:06:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14793s) first time when we had like you know uh

[4:06:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14795s) multi-agent conversations now at the

[4:06:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14797s) time these things were very janky right

[4:06:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14798s) like they were just like taped together

[4:06:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14800s) in this like weird weird uh bizarre ways

[4:06:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14804s) where you have just like these classes

[4:06:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14806s) and these links and then like these

[4:06:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14807s) hierarchies of classes and it was like

[4:06:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14809s) it was all like kind of like a very

[4:06:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14810s) janky attempt to like make us think that

[4:06:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14813s) like these these models to like have

[4:06:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14815s) these pipeline of flows of responses

[4:06:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14816s) that can all communicate with each

[4:06:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14818s) other. \[snorts\] A lot of it was like

[4:07:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14820s) mostly deterministic and it was like you

[4:07:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14822s) know it was not as free flowing as it is

[4:07:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14824s) right now. So and you know we started

[4:07:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14827s) getting the intention. So this was the

[4:07:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14828s) autogen project but like in only in 2025

[4:07:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14831s) we we started \[snorts\] getting the like

[4:07:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14832s) what if the agents just kept getting

[4:07:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14834s) better and faster and cheaper like what

[4:07:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14835s) what if that just kept happening and

[4:07:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14837s) then in 2026 uh we we had the intuition

[4:07:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14841s) that like what if what if the agent

[4:07:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14843s) could improve itself which is like the

[4:07:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14845s) final you know the final part of the

[4:07:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14847s) whole process. So let me give an example

[4:07:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14849s) like what does it mean for an agent to

[4:07:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14850s) improve itself right? So like it's like

[4:07:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14852s) a lot of times when we think of like

[4:07:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14854s) evaluating an agent, we initially used

[4:07:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14856s) to think of evaluating an agent in the

[4:07:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14858s) form of like just a single turn

[4:07:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14860s) conversation. So we would tell we would

[4:07:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14862s) tell like um um agents that like ask a

[4:07:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14865s) simple question like how many toes does

[4:07:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14868s) a dash animal has? It's like it could be

[4:07:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14870s) let's say how many toes does a cat have

[4:07:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14871s) and then al would go through and the

[4:07:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14873s) element would like prepare response and

[4:07:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14875s) then we would get the response. So like

[4:07:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14876s) a cat has maybe 10 toes, 18 toes,

[4:07:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14878s) however many. I don't I actually don't

[4:08:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14880s) know how many toes a cat has. But

[4:08:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14881s) anyway, um yeah. So then we create the

[4:08:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14885s) response as like a yes or no. But like

[4:08:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14887s) when you work with an agent, there's a

[4:08:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14889s) ton of things that you're doing. So let

[4:08:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14890s) me give an example. Let me give an

[4:08:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14892s) example. So for example, you're going to

[4:08:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14893s) ask an agent like hey set up this MCP

[4:08:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14895s) for me. So now it's not just like it's

[4:08:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14898s) not just like you know a trivial

[4:08:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14900s) oneshotable like thing like it will like

[4:08:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14902s) search online and go what's the MCP?

[4:08:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14904s) what is the config? So, I'll like edit

[4:08:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14906s) and download some soft files. Like maybe

[4:08:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14908s) I need to add database update the MCB

[4:08:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14910s) tool. Maybe I need to read and edit some

[4:08:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14912s) files. Maybe I need to run some bash

[4:08:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14914s) commands. Right? So, you do all of that

[4:08:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14916s) and then the agent response like, hey, I

[4:08:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14918s) did it. And then you grade that with a

[4:08:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14920s) bunch of tests to gauge like, hey, did

[4:08:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14922s) the agent actually accomplish the thing

[4:08:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14924s) that it said it would do? So to do that

[4:08:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14927s) thing the second part which is like more

[4:08:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14928s) intricate where you're actually like

[4:08:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14931s) truly you know testing agents like uh to

[4:08:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14934s) their best extent like it's like you

[4:08:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14936s) know um we use this thing called

[4:08:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14938s) terminal bench. terminal bench is a

[4:09:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14940s) benchmark for you know AI agents in

[4:09:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14941s) terminal environments and that is

[4:09:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14943s) something that we are we have a lot of

[4:09:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14945s) like experience with at client and uh

[4:09:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14948s) it's like a it's like one of the best

[4:09:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14949s) ways to like really gauge like is your

[4:09:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14951s) coding agent accomplishing uh in general

[4:09:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14953s) the task that you're doing uh that you

[4:09:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14955s) want to be doing with age model. So

[4:09:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14958s) there's a couple there's a many

[4:09:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14959s) different parts of evaluation suit. So

[4:09:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14961s) ideally you want that to run in um you

[4:09:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14965s) know \[snorts\] you you want that to run

[4:09:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14967s) in um individual sandboxes. Then you

[4:09:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14969s) have like independent graders that like

[4:09:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14971s) check everything like how many turns it

[4:09:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14973s) took, how many tokens it took, how much

[4:09:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14975s) latency it took, how many how many how

[4:09:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14977s) many tool calls did it make, what was

[4:09:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14979s) the trajectory looking like and then

[4:09:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14980s) grading all the results for things like

[4:09:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14982s) hey did you not reward hack? Did you not

[4:09:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14983s) cheat through the solution? Did you not

[4:09:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14985s) just like look up the solution online?

[4:09:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14987s) Things like that. Um so we we basically

[4:09:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14990s) like a lot of these uh data sets of

[4:09:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14992s) evaluation problems have a set of tasks.

[4:09:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14995s) So when a terminal bench 2.1 they have

[4:09:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=14997s) 89 tasks. So what we do is like we spin

[4:10:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15000s) up 89 parallel containers where they all

[4:10:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15003s) run online and they run in parallel and

[4:10:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15005s) they're sandbox and then they each try

[4:10:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15007s) to solve a problem. So then they're all

[4:10:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15010s) uh in parallel and independent of each

[4:10:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15011s) other. And then at the end we get get a

[4:10:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15014s) score. So our score could like give us

[4:10:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15016s) measures like is is a is this is the

[4:10:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15019s) model performing well and what kind of

[4:10:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15021s) failures it has right so like you run

[4:10:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15023s) the evaluation you get a score so you

[4:10:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15024s) get an aggregate score and there

[4:10:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15026s) aggregate score could reveal a set of

[4:10:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15028s) failures okay failures could be of any

[4:10:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15030s) kind failures could be hey the read file

[4:10:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15032s) tool is not working sometimes the

[4:10:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15034s) entrance is so slow that like you know

[4:10:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15036s) the agent's working it's doing it's

[4:10:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15037s) making progress maybe it's running a

[4:10:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15039s) circle but it's so slow that it

[4:10:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15040s) literally like runs out of time it runs

[4:10:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15042s) out of like 45 minutes or where that

[4:10:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15044s) were given for the task and just like

[4:10:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15046s) stop working. So once you do that once

[4:10:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15048s) you understand hey this is what we ran

[4:10:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15050s) this is what the failures we got we

[4:10:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15052s) bucket the failures in different

[4:10:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15053s) categories. So like 10 failures of you

[4:10:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15055s) know this kind of tool called 10 10 20

[4:10:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15057s) failures of like say inference not

[4:10:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15058s) working or something else right and then

[4:11:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15060s) we once we bucket the failures into

[4:11:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15062s) different categories where like we try

[4:11:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15063s) to make an improvement to the harness

[4:11:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15064s) because like what if there's like

[4:11:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15066s) something wrong with the harness that we

[4:11:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15068s) could change such that the model score

[4:11:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15069s) would improve right and on and on and on

[4:11:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15071s) and you do this iteratively it takes a

[4:11:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15073s) while it's just like you know hill

[4:11:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15074s) climbing is like a very groundworky kind

[4:11:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15076s) of process and you know usually usually

[4:11:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15079s) we we took we used to take a lot of time

[4:11:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15082s) trying to do this but it was a great way

[4:11:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15083s) for us to like learn how to improve

[4:11:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15085s) models. So \[snorts\] one way to hill

[4:11:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15088s) climb on top is that like you know we we

[4:11:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15092s) could have a thing where you know we

[4:11:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15094s) started doing this thing where we could

[4:11:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15096s) just like what if we could have like a

[4:11:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15099s) longunning agent that runs for a while

[4:11:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15100s) and automatically improves the model

[4:11:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15102s) score and that's what we did. So we ran

[4:11:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15104s) GPD 5.6 soul that led the work and that

[4:11:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15107s) was like the main agent and then uh Ky

[4:11:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15110s) K3 was just running eval. So what it was

[4:11:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15112s) doing is that like GBD 5.6 was like hey

[4:11:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15114s) run these events get these cores let me

[4:11:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15117s) look at the failures let me look at

[4:11:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15118s) where where it went wrong and then I'll

[4:12:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15121s) make changes to client's harness and

[4:12:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15123s) then I'll run these eval again and then

[4:12:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15125s) I'll keep trying. So again, you can see

[4:12:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15127s) how like very quickly this can like go

[4:12:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15129s) off the rails because this is supposed

[4:12:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15130s) to be like the running and evaluation

[4:12:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15131s) itself takes like an hour. Then you have

[4:12:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15133s) to read the feedback. Then you have to

[4:12:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15135s) like see if you're properly interpreting

[4:12:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15137s) the feedback to make reasonable changes

[4:12:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15139s) to the harness that are like not reward

[4:12:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15141s) hacking that are just like actual

[4:12:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15142s) genuine improvements and then run the

[4:12:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15143s) eval again. So we ran that for 17 hours

[4:12:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15146s) and uh when we ran that for 17 hours

[4:12:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15148s) there was like a legitimate hell

[4:12:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15150s) climbing and what we found that was very

[4:12:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15152s) interesting. This happened with a very

[4:12:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15154s) detailed prompt that accomplished this

[4:12:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15156s) is that like we had baseline score of

[4:12:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15159s) 27% and then you know we we found issues

[4:12:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15163s) like loop detection loop detection is

[4:12:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15164s) when a harness just runs in circles

[4:12:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15166s) around a problem right uh we found like

[4:12:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15168s) background process grinding where

[4:12:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15170s) background processes would run too long

[4:12:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15172s) uh we found some file index issues and

[4:12:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15174s) other things as well I mean when I say

[4:12:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15176s) we what I actually me 5.6 solve right so

[4:12:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15179s) that found those issues that found and

[4:13:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15181s) bucketed those issues it's like hey how

[4:13:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15183s) about I make those changes in the

[4:13:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15185s) harness and I run the eval again and it

[4:13:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15187s) iteratively built the hill climbing

[4:13:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15188s) process completely autonomously on its

[4:13:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15190s) own without my interference and 13 hours

[4:13:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15192s) later when I come back to it like it has

[4:13:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15194s) improved the harness's performance in so

[4:13:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15196s) many ways so see what does that mean

[4:13:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15199s) what does that mean it just it just

[4:13:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15200s) basically means that like we're at a

[4:13:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15203s) point where the experience could make

[4:13:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15206s) the harness better that like there's

[4:13:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15207s) like a tool level learning loop where

[4:13:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15209s) the harness does some action, interacts

[4:13:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15211s) with the environment, understands

[4:13:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15213s) whether or not it did the right thing or

[4:13:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15214s) the wrong thing and gets some reward and

[4:13:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15217s) and like almost and then has there's

[4:13:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15219s) like a meta agent that's observing the

[4:13:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15221s) main harness and finding the changes to

[4:13:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15224s) it and just like incorporating those

[4:13:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15226s) changes and improving. Now it's I think

[4:13:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15228s) in my personal opinion it's much harder

[4:13:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15229s) to do in real time because if you do it

[4:13:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15231s) in real time you overindex on solving

[4:13:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15234s) certain problems or you're just like too

[4:13:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15236s) cartel to a specific thing. But I do

[4:13:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15239s) think that this is something that works

[4:14:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15240s) like on a broader scale of like working

[4:14:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15242s) on a wider range of problems \[snorts\]

[4:14:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15244s) and you want to be able to like you want

[4:14:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15246s) you want to be able to justify the

[4:14:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15248s) changes you're making on a broader

[4:14:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15250s) applicability so that the changes you

[4:14:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15252s) make here will apply to a broader range

[4:14:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15254s) of problems as well. So what does that

[4:14:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15258s) mean? Like what am I trying to get at

[4:14:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15261s) here? The point I'm trying to get at is

[4:14:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15263s) that the models are so good right now

[4:14:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15264s) that they can if they can improve the

[4:14:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15265s) harness, they can improve a lot of other

[4:14:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15267s) things. So then what else can they

[4:14:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15268s) improve? So this is this is a this is a

[4:14:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15271s) post uh primarily from OpenAI where GP

[4:14:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15274s) 5.6 autonomously rewrote and optimized

[4:14:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15277s) its own production kernels and those

[4:14:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15279s) production kernel improvements remove

[4:14:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15281s) the end to-end serving costs by 20%. you

[4:14:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15284s) know it also had 15% higher to token

[4:14:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15287s) generation efficiency and this was like

[4:14:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15289s) completely done by 5.6 soul on itself,

[4:14:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15292s) right? So what that means is that like

[4:14:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15295s) inference is becoming much cheaper and

[4:14:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15297s) that means that like if on if if for a

[4:14:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15299s) company like OpenAI if you're having 20%

[4:15:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15302s) low lower serving cost for a frontier

[4:15:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15304s) model that could be a billions of

[4:15:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15306s) dollars of improvement in price and you

[4:15:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15308s) could you could do that as well for your

[4:15:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15309s) own models. Um another interesting thing

[4:15:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15312s) is that like when people have kernel

[4:15:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15314s) writing uh competitions so core auto is

[4:15:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15316s) a company which has a kernel writing

[4:15:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15318s) competitions and you'll notice that like

[4:15:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15320s) they they mentioned that like the person

[4:15:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15323s) who won the kernel writing competition

[4:15:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15325s) the explic said that I have never

[4:15:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15327s) handwritten a GPU operator it's all ALM

[4:15:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15329s) and agent driven so notice that like how

[4:15:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15332s) like the best uh inference improvements

[4:15:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15335s) kernel improvements are at this point

[4:15:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15336s) completely exclusively done by a swarm

[4:15:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15339s) of agents or generally like agents doing

[4:15:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15341s) some magic to you know magically improve

[4:15:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15343s) like the kernel kernel code and have

[4:15:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15345s) faster inference cheaper inference. Um

[4:15:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15348s) yeah so basically like the improvement

[4:15:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15351s) surface that you think of is not just

[4:15:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15354s) like the harness improvement it's

[4:15:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15355s) literally the whole surface stack right

[4:15:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15357s) so the whole stack from like evaluation

[4:16:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15360s) to harness improvements to training data

[4:16:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15362s) to post training to world interaction to

[4:16:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15364s) inference like literally the entire pip

[4:16:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15366s) part of the pipeline like all the way

[4:16:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15368s) from like electricity going through your

[4:16:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15371s) machine to like making a network request

[4:16:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15374s) going through the model models doing

[4:16:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15376s) inference um making a response and

[4:16:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15378s) getting back to you like every single

[4:16:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15379s) part of the pipeline we can optimize it.

[4:16:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15381s) So the whole RSI loop has like um

[4:16:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15384s) there's a couple different parts so it's

[4:16:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15385s) like pre-training um uh neatron examples

[4:16:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15388s) of like you know AI curated uh

[4:16:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15390s) pre-training data that was good um

[4:16:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15392s) there's like post- training examples

[4:16:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15393s) which are you know where there's like

[4:16:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15396s) constitutional AI examples of like post-

[4:16:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15398s) training uh improvements then inference

[4:16:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15400s) I gave you the example of GP 5.6 So for

[4:16:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15403s) eval generation, I give you our own

[4:16:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15406s) example of how we improved ourselves on

[4:16:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15407s) our own eval. Um, in general, what you

[4:16:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15410s) want to think of is that like anytime a

[4:16:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15412s) model is trying to do something and it's

[4:16:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15414s) like not able to do it or not able to

[4:16:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15416s) accomplish it. So for example, like

[4:16:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15417s) imagine you're having a long

[4:16:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15418s) conversation where you ask the model

[4:17:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15420s) something obvious. So like it's like or

[4:17:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15423s) something that you think is not

[4:17:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15425s) necessarily obvious, but it's like it's

[4:17:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15427s) hard, but you would assume that the

[4:17:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15428s) model could potentially do it. So to

[4:17:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15430s) give an example, let's say you want to

[4:17:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15432s) make add a new column to a database and

[4:17:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15435s) then fill that column, right? And then

[4:17:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15437s) put a cache in front of it. So what

[4:17:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15439s) happens is it does the whole thing, but

[4:17:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15441s) for some reason the way it pushes the

[4:17:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15443s) cache in front of the whole uh database

[4:17:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15444s) like it kind of doesn't do it right. So

[4:17:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15446s) at that point you're like, "Oh no, set

[4:17:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15448s) this cache differently. Set this as the

[4:17:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15450s) TTL." And then you give like a

[4:17:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15451s) correction signal and then that kind of

[4:17:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15453s) like fixes your problem and you kind of

[4:17:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15455s) go about your day.

[4:17:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15456s) The way I want to think of it is that I

[4:17:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15458s) want to think of like every single time

[4:17:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15460s) like a human correction to the digital

[4:17:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15462s) landscape is a part of a delta that

[4:17:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15467s) needs to be covered. And what that means

[4:17:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15469s) is that like every single time you're

[4:17:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15471s) finding like the edge of model

[4:17:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15472s) capabilities of like how far it can push

[4:17:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15474s) for infants, how much it can push for

[4:17:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15476s) this, how much it can push for, you

[4:17:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15478s) know, solving your problems. You want to

[4:18:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15480s) find that delta and we want to like push

[4:18:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15482s) that frontier a little bit further. a

[4:18:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15484s) little bit further and that's what post

[4:18:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15486s) training does, right? So post training

[4:18:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15488s) is is this is in that post training we

[4:18:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15491s) find these like really interesting and

[4:18:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15493s) really hard long horizon problems for uh

[4:18:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15495s) for coding agents or for other kinds of

[4:18:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15497s) problems and then just like slowly hill

[4:18:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15498s) climb the models on on those kind of

[4:18:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15501s) problems. So anything that has a

[4:18:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15502s) verifiable loop can be optimized but is

[4:18:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15506s) this is not just limited to software

[4:18:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15509s) like literally like the physical world

[4:18:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15510s) itself could have a verifiable loop. So

[4:18:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15513s) to give an example like let me let me

[4:18:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15515s) give you a very funny kind of bizarre

[4:18:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15517s) example where like it's like you you

[4:18:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15520s) look at this and uh you um

[4:18:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15524s) um look at this uh like robot and it's

[4:18:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15526s) it's typing something and it's like

[4:18:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15529s) really really like interesting what the

[4:18:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15531s) robot is typing.

[4:19:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15541s) So notice how like notice how the robot

[4:19:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15543s) is itself typing like how it wants to

[4:19:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15545s) like solve robotics and imagine if the

[4:19:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15548s) robot itself could like interpret the

[4:19:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15550s) results of of like the answers and just

[4:19:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15553s) like keep improving then that means that

[4:19:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15555s) like this is you know basically like an

[4:19:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15557s) ASI robot. Another example that I could

[4:19:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15559s) give you for my uh personal life is that

[4:19:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15562s) like um I have this um chip that has the

[4:19:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15565s) ability to see and has a speaker and has

[4:19:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15568s) a microphone inside of it. So I was

[4:19:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15569s) trying to set up this uh with my machine

[4:19:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15572s) and it was um a gift that I had for my

[4:19:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15576s) girlfriend. And uh what I found very

[4:19:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15578s) interesting about this is as I was

[4:19:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15580s) trying to set it up, it was very slow.

[4:19:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15582s) It was slow to respond. It had higher

[4:19:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15583s) latency. It had an agent in and of

[4:19:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15585s) itself. Right? So what I did was I

[4:19:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15587s) connected the step to my um computer and

[4:19:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15591s) I let um I let um putting agents run on

[4:19:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15595s) this hardware and basically run on this

[4:19:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15598s) hardware automatically make tests to it.

[4:20:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15601s) So like my computer would talk to my

[4:20:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15604s) hardware give it some tests like hey do

[4:20:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15606s) this do that and just like what do you

[4:20:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15608s) see right now? So then it would notice

[4:20:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15611s) the end to end latency of like the

[4:20:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15612s) inference response of like how fast uh

[4:20:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15615s) my hardware is responding and then um

[4:20:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15618s) what I found is that like it was able to

[4:20:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15620s) do the breakdown of like every single

[4:20:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15622s) case and scenario where there was like

[4:20:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15624s) high latency um slower response or or

[4:20:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15628s) just the algorithm wasn't right and I

[4:20:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15630s) could then set up a recursive loop where

[4:20:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15633s) both the firmware could be updated the

[4:20:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15636s) um the tool calls the inference model

[4:20:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15638s) used um the speech to text model used

[4:20:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15641s) all of those could be improved

[4:20:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15642s) automatically with like an open router

[4:20:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15644s) key which I'd given to a coding agent

[4:20:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15646s) and then overnight with self-running

[4:20:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15648s) experiments with the hardware uh my um

[4:20:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15651s) this tiny little piece of beautiful

[4:20:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15652s) hardware that I have was like deeply

[4:20:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15654s) optimized so this also like even

[4:20:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15657s) hardware could be a part of the RSI loop

[4:20:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15659s) so what happens when you connect these

[4:21:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15660s) loops right that's the next question

[4:21:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15661s) like you could have cheaper inference

[4:21:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15663s) you could have like more experiments

[4:21:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15665s) budget you have like you know better

[4:21:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15667s) data and better models. So, is it

[4:21:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15669s) singularity? It's a very question to ask

[4:21:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15672s) and I think that the part of the parts

[4:21:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15673s) of the loop are already weird, right?

[4:21:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15674s) Like we're we we are really we really

[4:21:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15677s) are very close to parts of the RSI loop,

[4:21:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15680s) right? And what do we do like what do we

[4:21:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15682s) do about this and it's like how do we

[4:21:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15684s) think of that in terms of like our

[4:21:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15686s) career and how do you think of that in

[4:21:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15687s) terms of you know our lives and what do

[4:21:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15689s) we want to do next? So here's my advice

[4:21:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15691s) to everyone who is watching this like

[4:21:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15693s) please please please please move closer

[4:21:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15695s) to the RS group right so it's like right

[4:21:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15698s) now like people are working on all these

[4:21:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15699s) like different kinds of software which

[4:21:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15701s) is like you know a agents for you know

[4:21:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15703s) construction agents for this agents for

[4:21:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15704s) that and it's like I think that you're

[4:21:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15707s) you know what the way I see those things

[4:21:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15710s) is that like I think of those as like

[4:21:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15711s) you're missing the forest for the for

[4:21:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15712s) the trees you really are and it's like

[4:21:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15715s) you have this like very interesting

[4:21:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15718s) godlike technology that can change parts

[4:22:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15720s) of humanity. And then we're not

[4:22:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15722s) ambitious enough to pursue the best

[4:22:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15724s) problems. We really are not. And we're

[4:22:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15726s) just like I think that it's not just

[4:22:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15728s) like the problem isn't just that we're

[4:22:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15730s) not ambitious and we're also like what

[4:22:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15732s) we're pursuing. A lot of those things

[4:22:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15734s) are just like one model release away

[4:22:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15736s) from like being completely like wiped

[4:22:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15738s) out, right? So like it's also like it's

[4:22:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15740s) also like it may not be that

[4:22:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15742s) intellectually simulating because like

[4:22:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15743s) all you're essentially all we're

[4:22:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15745s) essentially doing is like sitting all

[4:22:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15746s) day. It's like hey cloud do this for me.

[4:22:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15747s) Hey cloud do this for me. And I don't

[4:22:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15748s) know if that's like I don't know if

[4:22:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15749s) that's like the most intellectual

[4:22:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15751s) stimulating or like or like um

[4:22:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15753s) thoughtful use of a person's time like

[4:22:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15755s) maybe maybe you know we're supposed to

[4:22:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15757s) be solving harder and more uh more

[4:22:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15759s) frontier problems and I think that like

[4:22:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15760s) it's like the ceiling is like our

[4:22:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15762s) ambition. So instead of like working on

[4:22:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15764s) these kind of things my suggestion to

[4:22:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15766s) people is to like you know do things

[4:22:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15768s) that of course like goes without saying

[4:22:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15770s) but you should do things you believe in

[4:22:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15772s) and you know I'm just a guy on the

[4:22:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15773s) internet but do things that help you

[4:22:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15775s) move closer to the RSI loop right? So

[4:22:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15778s) like anything that just like the end to

[4:22:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15779s) end pipeline of like hey this is where

[4:23:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15783s) like the models are lacking like it's

[4:23:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15785s) like whether that's inference whether

[4:23:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15786s) that's post training whether that's

[4:23:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15787s) literally like physical interaction

[4:23:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15789s) whether that could be you know send

[4:23:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15792s) sending end to-end pipelines of truly

[4:23:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15793s) any kind you know whether that's

[4:23:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15795s) hardware problems whether that's um

[4:23:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15797s) networking problems whether that's um

[4:23:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15799s) building a sense community things that

[4:23:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15800s) just you know um things that just like

[4:23:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15803s) help um you as an engineer get closer to

[4:23:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15807s) the benefit benefits of the improvements

[4:23:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15809s) um in uh in uh um in in the model. So

[4:23:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15813s) this is a very interesting slide from

[4:23:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15815s) Sasha topic. So um um they mentioned

[4:23:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15819s) that like you want to have like this

[4:23:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15823s) you're in this space where it's like you

[4:23:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15824s) know you only you only have like one to

[4:23:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15826s) five years left to contribute to luxury

[4:23:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15827s) to the world. What do you do? Right? So

[4:23:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15829s) it's like um they they gave great

[4:23:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15831s) suggestions were like prefer ambitious

[4:23:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15833s) targeted and past collaborations right

[4:23:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15835s) and you know in general like the time

[4:23:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15838s) scale like all the timelines that you

[4:23:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15839s) give to yourself like they should be

[4:24:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15840s) just like completely squeezed out should

[4:24:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15842s) be completely squeezed out because it's

[4:24:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15843s) like a lot of times and you also have to

[4:24:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15845s) think through that like if if the model

[4:24:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15847s) if the problem that you're working on is

[4:24:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15848s) too ambitious like it's like is it

[4:24:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15850s) probably is it probably better to wait

[4:24:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15852s) for just like the next next frontier

[4:24:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15854s) model to come out or not like that's

[4:24:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15856s) that's something you also have to weigh

[4:24:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15857s) through Right. And uh you you ideally

[4:24:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15861s) want to work on problems that benefit

[4:24:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15863s) from scale and you know you also at the

[4:24:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15865s) same time want to avoid problems that

[4:24:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15866s) can be solved by sale alone because then

[4:24:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15868s) you know if even if you like it's like

[4:24:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15869s) if you're working on a problem and then

[4:24:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15871s) the next model release comes out it

[4:24:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15872s) solves the problem. So that's not that's

[4:24:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15873s) probably not a good thing to do. So it's

[4:24:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15875s) very like you have to like think

[4:24:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15876s) philosophically of like what is the

[4:24:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15879s) endeavor that benefits uh greatly from

[4:24:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15881s) auto improvements but like isn't also

[4:24:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15883s) completely wiped out from it. And then

[4:24:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15885s) ideally like it's like if the if the

[4:24:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15887s) endeavor could also uh be a part of the

[4:24:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15890s) the like the improvement pipeline uh

[4:24:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15893s) that could be amazing. So you see a lot

[4:24:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15895s) of companies raising on say um making

[4:24:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15898s) data pipelines and there's a lot of

[4:25:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15900s) money there. There's a a lot of

[4:25:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15902s) companies working on physical hardware

[4:25:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15903s) and stuff. So I think if you're a

[4:25:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15905s) software engineer watching these, it's

[4:25:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15906s) like I think that if you're if you feel

[4:25:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15908s) like you're like here the delta of your

[4:25:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15911s) intellect and ability in your

[4:25:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15913s) day-to-day, it's like not contributing

[4:25:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15915s) as in like you have the intellect, you

[4:25:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15917s) can make a difference. But like if cloud

[4:25:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15919s) is just like oneshotting all those

[4:25:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15921s) problems like in your day-to-day and

[4:25:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15922s) you're just like kind of like becoming a

[4:25:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15923s) me proxy, it's worth to think through.

[4:25:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15925s) Take a step back and think through. like

[4:25:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15927s) okay where are the problems where where

[4:25:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15929s) you're actually truly uh contributing

[4:25:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15931s) and that they will stand the test of

[4:25:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15932s) time and then that kind of reflection

[4:25:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15934s) and realignment right now would I think

[4:25:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15936s) like have like very interesting

[4:25:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15939s) consequences for you um in the long term

[4:25:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15942s) um so yeah so thank you so much you know

[4:25:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15944s) thank you so much for your time like I

[4:25:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15946s) think that uh I think that if you're

[4:25:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15948s) watching this and if you've gone this

[4:25:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15949s) far I think that you're definitely

[4:25:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15951s) contemplating like one of the most

[4:25:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15953s) interesting improvements in the course

[4:25:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15955s) of humanity And uh you know there's many

[4:25:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15958s) philosophical arguments here. Some

[4:25:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15959s) people might say hey you know I I think

[4:26:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15962s) I'm maybe I'm off on the timelines or

[4:26:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15964s) maybe maybe I'm I'm just being too

[4:26:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15966s) pessimistic or maybe I'm being too

[4:26:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15967s) optimistic. But I would love to hear all

[4:26:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15970s) those thoughts. So this is you know my

[4:26:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15971s) QR code. Please feel free to scan it and

[4:26:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15973s) let me know all your thoughts. Uh thank

[4:26:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15975s) you so much. Very kind of you to give me

[4:26:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=15976s) your time.
