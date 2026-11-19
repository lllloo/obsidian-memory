---
title: Rethinking Claude Code Best Practices — Lydia Hallie
description: AI Engineer CODE 2026 官方閱讀版，Lydia Hallie 談人退出迴圈後改由模型、harness 與環境接手，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/lydia-hallie
published: 2026-11-11
tags:
  - clippings
  - claude-code
  - coding-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 Claude 被辨識成 Cloud、Claude Code projects 被辨識成 CloakCode projects、Opus 5.5 被辨識成 Opus 55）。現場直播因 AV 問題中斷，講者事後自錄完整版；逐字稿與時間碼對應該替代錄影 `https://www.youtube.com/watch?v=vlfCjWuv4es`。

Official replacement recording · [0:00:00–0:17:31 on YouTube](https://www.youtube.com/watch?v=vlfCjWuv4es&t=0s). The player starts and stops at this session’s boundaries.

## Introduction

*The morning livestream was interrupted by AV problems. Hallie recorded this complete version afterward; all links below use that recording's clock.*

A setup built around an older model can become an obstacle for a newer one. Lydia Hallie starts with the habits of short coding sessions: approve commands, correct the model, add increasingly emphatic instructions, and remain present for most steps. She contrasts that with running many longer sessions that verify their results and sometimes orchestrate other sessions.

Stepping away from the loop creates a responsibility, not a disappearance of responsibility. Every job the person used to do must move somewhere: into the model, the harness, or the execution environment. Hallie's talk works through what can move and what must still be enforced.

[0:03:04 ↗](https://www.youtube.com/watch?v=vlfCjWuv4es&t=184s)

## Remove instructions that compensate for yesterday's model

At [00:03:04](https://www.youtube.com/watch?v=vlfCjWuv4es&t=184s), Hallie revisits `CLAUDE.md`. Instructions added to correct an earlier model may no longer help. Repeated emphasis and restrictive warnings can steer a more capable model into unnecessary calls or an unproductive path.

Her proposed filter is what the model cannot discover from the code. A hidden dependency on a legacy service may belong in the file. A description of the visible stack or obvious directory layout may not. This is a model-specific review of context, not a rule that all project documentation should be deleted.

She also describes a prompt-audit command that checks instructions and skills for the selected model. The larger practice is to reevaluate the environment when capabilities change instead of treating every past correction as permanent law.

[0:05:42 ↗](https://www.youtube.com/watch?v=vlfCjWuv4es&t=342s)

## Permission classification and enforcement do different jobs

Hallie describes auto mode as a classifier that approves actions it considers safe and blocks uncertain ones. Its configuration can include trusted repositories, destinations, and operations. That can reduce repetitive approvals, but a classifier is still making a fallible judgment.

The [important dividing line](https://www.youtube.com/watch?v=vlfCjWuv4es&t=342s) is whether a mistake can be taken back. Incorrect code can often be reverted. Exposing a secret or discarding uncommitted work may not be recoverable in the same way. Hallie recommends explicit deny rules for actions that must not occur, rather than relying on the model to remember a warning or the classifier to recognize every danger.

The talk's permission behavior is specific to the Claude Code setup being demonstrated. The general distinction is between asking a model to avoid something and arranging for the system to reject it.

[0:08:25 ↗](https://www.youtube.com/watch?v=vlfCjWuv4es&t=505s)

## A harmless-looking command can start harmful code

A permission check sees the proposed tool call. It does not necessarily know everything the command will do after it starts. Hallie's example is `npm test`: a normal action for verifying a change, but one that can execute dependencies or other code the person did not write.

Blocking every test would prevent useful work. Approving the command without constraining its effects leaves a different problem. A compromised script might try to read a sensitive file or contact an unexpected server even though the visible command looked routine.

[![The sandbox diagram places tests and dependency code inside operating-system enforcement, with controls on file reads, writes, and network destinations.](https://ai.engineer/reading/code-2026/images/lydia-hallie-505.jpg)](https://ai.engineer/reading/code-2026/images/lydia-hallie-505.jpg)

*At [00:08:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=505s), the diagram follows `npm test` into code it starts. The relevant controls concern what the process can reach, not just whether its initial command was approved.*

Hallie distinguishes shell sandboxing from isolation of the entire session. A shell sandbox can constrain commands and their child processes, but other parts of a setup, such as hooks or external integrations, may operate outside it. The protection depends on the component actually being covered.

She then moves the session to a separate cloud machine with a fresh repository copy. Personal files that were never copied there cannot be read from that machine. Network access and required secrets still need deliberate configuration. This is a smaller and more controllable environment, not a reason to stop thinking about permissions.

[0:10:23 ↗](https://www.youtube.com/watch?v=vlfCjWuv4es&t=623s)

## Disposable machines can still make lasting changes

At [00:10:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=623s), Hallie makes a useful qualification: the machine may be disposable, but a pushed commit or a message sent through a connector is not. Isolation limits access to the local environment; it does not undo authorized effects on external systems.

That is why she keeps permission controls alongside the cloud environment. These layers solve different problems. A small workspace, restricted network, and denied operations can reinforce each other, but none should be mistaken for proof that every remaining action is appropriate.

[0:10:54 ↗](https://www.youtube.com/watch?v=vlfCjWuv4es&t=654s)

## Define success at intermediate checkpoints

Verification becomes harder when nobody watched every change. Hallie's [authentication-migration example](https://www.youtube.com/watch?v=vlfCjWuv4es&t=654s) shows why an apparently clear request can still permit different outcomes: leave the old API in place, migrate only new logins, or move everything while logging existing users out.

All may look like progress toward the request. The desired behavior needs to become a check. A test that existing sessions remain valid narrows the agent's options before it reaches the end of a long implementation.

Hallie recommends defining what done looks like and splitting the work into tasks with their own verification. Asking for actual outputs also makes the final review more useful than accepting a claim that checks passed. Where a check must run, she moves it from a prompt into a hook.

[![Hooks run a linter after an edit, task-specific tests at task completion, and all tests at the end of the session.](https://ai.engineer/reading/code-2026/images/lydia-hallie-775.jpg)](https://ai.engineer/reading/code-2026/images/lydia-hallie-775.jpg)

*The [12:55 slide](https://www.youtube.com/watch?v=vlfCjWuv4es&t=775s) maps verification to three lifecycle points. The check belongs where its failure can send work back for repair.*

She calls out hook exit behavior as an implementation detail that matters: in the demonstrated setup, a blocking response must be communicated in the form the harness expects. A script reporting failure is ineffective if the surrounding system still treats the task as complete. The correct behavior needs to be checked for the hook and version in use.

## CI applies the same standard across sessions

Once several sessions run independently, repository CI becomes the common checkpoint. Different prompts, machines, and paths through the task should still meet the same checks before their PRs merge.

Hallie describes automated repair of failed CI, fresh-context review separate from the session that wrote the change, and human review proportional to risk. A small documentation change and a risky product change do not necessarily require the same number of people. Passing automation is a basis for a policy decision, not a universal instruction to enable automatic merge.

The final step is an orchestrator that starts and reviews other sessions. The orchestrator needs to judge and coordinate; the workers need to implement. Hallie describes choosing models separately for those roles and sending incomplete work back rather than making a person manage every thread.

The practical starting point is one task larger than the work normally delegated. Establish checks that catch what matters, configure the environment, and observe where the session still needs intervention. That remaining intervention identifies the next capability to build. The goal is not to remove the person everywhere at once; it is to know what took over each responsibility when the person stepped away.

Full transcript 528 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[0:00:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=0s) I had some technical difficulties during

[0:00:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=3s) my talk this morning, so I ran back home

[0:00:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=5s) and I'm just going to record it from my

[0:00:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=7s) computer instead. So, hi everyone. I'm

[0:00:09](https://www.youtube.com/watch?v=vlfCjWuv4es&t=9s) Lydia. I work on the Cloud Code team at

[0:00:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=11s) Anthropic. And the models have gotten

[0:00:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=14s) really good lately. So we have Opus 55,

[0:00:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=16s) which is my favorite daily driver. And

[0:00:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=19s) earlier this week, we also launched

[0:00:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=20s) Fable 52. And these models are extremely

[0:00:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=23s) good at long-running tasks and

[0:00:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=25s) understanding your codebase. And

[0:00:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=27s) especially Fable is also really good at

[0:00:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=29s) verifying its own output. But as these

[0:00:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=31s) models get better, the way that we work

[0:00:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=33s) with them in Cloud Code also changes.

[0:00:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=36s) So earlier this year, I don't know if

[0:00:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=38s) you remember, but sessions kind of used

[0:00:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=40s) to look like this. So we'd use a model

[0:00:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=41s) like Opus 45, which honestly for its

[0:00:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=44s) time was really good. I really enjoyed

[0:00:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=45s) working with Opus 45. But compared to

[0:00:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=48s) today, it would just stop a lot earlier.

[0:00:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=50s) So it would just run for shorter amounts

[0:00:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=52s) of time.

[0:00:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=53s) And we'd also keep correcting it. We'd

[0:00:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=55s) keep reminding it to do things, add

[0:00:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=57s) things like important, exclamation mark,

[0:00:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=59s) all these things to our Cloud MD file.

[0:01:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=61s) And also features like auto mode didn't

[0:01:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=63s) exist yet. So we were either approving

[0:01:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=65s) everything manually or taking the

[0:01:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=68s) riskier approach with dangerously skip

[0:01:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=70s) permission. So we were still very much

[0:01:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=73s) in the loop as humans.

[0:01:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=75s) But as these models got better at taking

[0:01:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=77s) on bigger tasks, our sessions also

[0:01:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=79s) changed. So nowadays, at least at

[0:01:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=81s) Anthropic, our sessions look more like

[0:01:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=83s) this. So we're running dozens of

[0:01:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=84s) sessions at the same time, running for

[0:01:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=86s) hours, verifying their own results along

[0:01:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=89s) the way, and we even have sessions

[0:01:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=91s) orchestrate other sessions. So whereas

[0:01:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=93s) we used to be in the loop for almost

[0:01:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=95s) every step and running one or just a

[0:01:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=97s) couple sessions at a time, we've now

[0:01:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=99s) essentially become managers for dozens

[0:01:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=102s) of sessions.

[0:01:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=103s) We also got a lot more done though. Now

[0:01:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=105s) you may have seen our blog post in

[0:01:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=106s) October about how Anthropic went from

[0:01:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=108s) about 2,500 changes a day in May to more

[0:01:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=111s) than 30,000 a day in September. But this

[0:01:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=115s) also means that we as developers just

[0:01:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=117s) have to rethink on what we're focused on

[0:01:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=119s) instead.

[0:02:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=120s) So, if you think about our best

[0:02:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=121s) practices from earlier this year, it was

[0:02:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=123s) mainly about steering sessions,

[0:02:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=125s) approving commands, saying no to certain

[0:02:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=128s) things or restricting what Claude could

[0:02:09](https://www.youtube.com/watch?v=vlfCjWuv4es&t=129s) do,

[0:02:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=131s) the output, and also starting the

[0:02:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=132s) sessions. So, everywhere that we now

[0:02:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=135s) step out of that loop, something else

[0:02:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=137s) has to take over. And this is either the

[0:02:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=139s) model, the harness, or the environment

[0:02:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=142s) that it's running in. So, if we are not

[0:02:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=144s) in the loop to approve every command and

[0:02:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=146s) we're running so many sessions at the

[0:02:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=147s) same time, how can we make sure that the

[0:02:30](https://www.youtube.com/watch?v=vlfCjWuv4es&t=150s) code it's writing is still high quality?

[0:02:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=152s) And most importantly, if these sessions

[0:02:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=154s) are running for hours without our

[0:02:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=156s) supervision, how can we make sure that

[0:02:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=158s) they're running safely? So, let's go

[0:02:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=160s) through that by taking this old session

[0:02:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=162s) and seeing what we have to change to get

[0:02:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=164s) to that end result that I showed

[0:02:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=165s) earlier.

[0:02:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=166s) Well, first of all, let's use the actual

[0:02:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=167s) defaults we start sessions in nowadays.

[0:02:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=169s) So, that's not really something you

[0:02:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=171s) should think about. So, let's update the

[0:02:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=172s) model here from Opus 4 5 to Opus 5 5 and

[0:02:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=175s) change the manual permission to auto

[0:02:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=177s) mode. And Opus 5 5 is a lot better at

[0:03:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=180s) understanding your intent and

[0:03:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=181s) understanding your code base. So, we

[0:03:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=183s) really don't have to steer it as much

[0:03:04](https://www.youtube.com/watch?v=vlfCjWuv4es&t=184s) anymore mid session. And you also no

[0:03:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=186s) longer have to approve every command

[0:03:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=188s) because we started making auto mode the

[0:03:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=190s) default permission mode back in August.

[0:03:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=192s) Now, being better at understanding your

[0:03:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=194s) intent and your code base also means

[0:03:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=196s) that we have to rethink the instructions

[0:03:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=198s) we have in our code base. So,

[0:03:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=200s) if you followed our best practices from

[0:03:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=201s) earlier this year, you may still have

[0:03:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=203s) things like important or never do this,

[0:03:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=205s) exclamation mark, all these things in

[0:03:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=207s) your cloud MD file. But with today's

[0:03:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=209s) models, you really don't need that and

[0:03:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=211s) it can actually make the model go off

[0:03:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=212s) track. So, you end up with more tool

[0:03:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=214s) calls and overall a worse results.

[0:03:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=217s) So, nowadays your cloud MD file should

[0:03:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=219s) only include the things the Claude

[0:03:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=220s) cannot see from your code. So, for

[0:03:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=222s) example, maybe you have a service that's

[0:03:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=224s) still using some legacy source

[0:03:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=226s) somewhere, but it's not directly

[0:03:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=227s) referenced in the code. That's still

[0:03:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=229s) good to keep in there. But everything

[0:03:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=231s) else, like what stack you're on or where

[0:03:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=233s) to look, you really don't need that

[0:03:54](https://www.youtube.com/watch?v=vlfCjWuv4es&t=234s) anymore. And we actually have a command

[0:03:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=236s) for this called doctor prompt audit,

[0:03:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=238s) which makes it really easy to optimize

[0:04:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=240s) your environment for a specific model.

[0:04:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=242s) So, if on Opus 55 here and you run this

[0:04:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=245s) command, it will automatically check

[0:04:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=246s) your cloud MD and your skills to see

[0:04:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=248s) what the new model no longer needs.

[0:04:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=251s) Now, auto mode is a permission mode that

[0:04:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=253s) runs a separate classifier on pretty

[0:04:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=255s) much everything that isn't just reading

[0:04:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=257s) or editing files in your project.

[0:04:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=260s) So, it automatically allows commands

[0:04:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=262s) that it knows are safe, like running

[0:04:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=263s) tests or installing dependencies, but it

[0:04:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=266s) still blocks commands where it's unsure

[0:04:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=268s) whether they're safe.

[0:04:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=269s) And normally that's pretty good. Uh

[0:04:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=271s) normally that's kind of, you know, what

[0:04:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=272s) we want. But for example here, if we ask

[0:04:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=275s) it to ship something to staging, we

[0:04:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=277s) would have just, you know, approved the

[0:04:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=279s) push to our deploy repo. But by default,

[0:04:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=282s) auto mode only trusts this folder and

[0:04:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=284s) this repo, so it would block that

[0:04:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=285s) command. So, we're back in the loop.

[0:04:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=288s) Now, the defaults should be good in most

[0:04:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=290s) cases, but if you still notice that you

[0:04:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=291s) have to approve a lot of uh commands

[0:04:54](https://www.youtube.com/watch?v=vlfCjWuv4es&t=294s) even in auto mode, the first thing to

[0:04:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=296s) look at is settings here because you can

[0:04:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=298s) configure auto mode in your own settings

[0:05:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=300s) just in plain English, and this is what

[0:05:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=301s) gets sent to the classifier, which then

[0:05:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=303s) decides whether to reject or allow

[0:05:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=305s) certain commands.

[0:05:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=307s) So, here we can just write which repos,

[0:05:09](https://www.youtube.com/watch?v=vlfCjWuv4es&t=309s) buckets, domains we trust um and what it

[0:05:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=311s) should always allow or never do. Okay,

[0:05:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=313s) so honestly this was pretty easy by just

[0:05:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=315s) using today's defaults. We've already

[0:05:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=317s) gotten rid of most of our in-the-loop

[0:05:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=319s) stuff

[0:05:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=320s) um because the model took over the

[0:05:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=321s) steering and auto mode took over all the

[0:05:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=323s) approving, so getting out of the loop is

[0:05:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=325s) easy. But the harder question now is how

[0:05:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=328s) do we make sure it's okay that we're not

[0:05:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=329s) there anymore? So, first is keeping it

[0:05:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=332s) safe and then also verification.

[0:05:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=334s) So, let's start with keeping it safe

[0:05:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=335s) because everything so far, so upgrading

[0:05:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=337s) the model and using auto mode is just

[0:05:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=340s) working with a model.

[0:05:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=342s) And in most cases it does what you tell

[0:05:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=344s) it to do, but that's not a guarantee.

[0:05:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=346s) So, in a study we published back in

[0:05:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=348s) August, we tested auto mode versus real

[0:05:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=350s) people in the loop, and only about 14%

[0:05:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=353s) of people caught a clearly dangerous

[0:05:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=355s) command. Auto mode blocked 89% of them,

[0:05:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=358s) so it is a lot better at it than we

[0:06:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=360s) were.

[0:06:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=361s) But about one in 10 of those commands

[0:06:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=363s) still went through. So, if do want the

[0:06:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=365s) guarantee, you can only enforce that in

[0:06:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=368s) the harness. And this is where some of

[0:06:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=370s) our older best practices still matters,

[0:06:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=371s) and that's permissions. So, for example,

[0:06:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=373s) if you have a deny rule for a specific

[0:06:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=376s) tool called in your project, Cloud Code

[0:06:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=378s) looks at this rule before the automo

[0:06:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=380s) classifier even looks at it. In fact, if

[0:06:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=382s) a tool called matches a deny rule, the

[0:06:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=384s) classifier never even sees it. So,

[0:06:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=386s) having deny rules is still the best way

[0:06:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=388s) to make sure Cloud actually never does

[0:06:30](https://www.youtube.com/watch?v=vlfCjWuv4es&t=390s) something.

[0:06:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=392s) But then how do you know what needs to

[0:06:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=393s) be a rule in your project versus what

[0:06:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=395s) the model can just know because they've

[0:06:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=397s) gotten so good at it? Um I think it kind

[0:06:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=399s) of just comes down to if Cloud gets this

[0:06:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=401s) wrong once, can I take it back? So, if

[0:06:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=404s) it writes the wrong code, you can still

[0:06:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=406s) revert that. Um so, you can still leave

[0:06:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=408s) that to the model. But if it throws away

[0:06:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=410s) our uncommitted changes or it reads a

[0:06:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=412s) key that's now in your transcript and

[0:06:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=413s) you don't don't want that, that should

[0:06:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=415s) still be a rule. So, for example, let's

[0:06:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=418s) say that we just never want Cloud

[0:06:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=419s) reading our.env file. Now, by default,

[0:07:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=422s) automo is fine with this, so it would

[0:07:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=423s) have just approved it.

[0:07:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=425s) So so, if you want to make sure that

[0:07:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=427s) Cloud can never read this file, you

[0:07:09](https://www.youtube.com/watch?v=vlfCjWuv4es&t=429s) should just add a deny rule. And then

[0:07:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=431s) commands like cat cannot open this file

[0:07:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=432s) either. But it's not always that

[0:07:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=434s) straightforward cuz sometimes certain

[0:07:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=436s) commands can have side effects. So, for

[0:07:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=439s) example, let's say that npm test here, a

[0:07:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=441s) very normal command, it's just a test,

[0:07:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=443s) so automo runs it, that's fine.

[0:07:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=445s) But when the script is running, it runs

[0:07:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=447s) code that you didn't write, like your

[0:07:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=448s) dependencies. Or maybe Cloud runs a

[0:07:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=451s) script real quick that it wrote just to

[0:07:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=453s) quickly check something.

[0:07:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=454s) So, if one of those scripts is

[0:07:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=456s) compromised, it could just open that

[0:07:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=458s) same.env file or your SSH keys and send

[0:07:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=461s) those to a server you've never heard of,

[0:07:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=463s) right? And even if we were still there

[0:07:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=466s) as humans approving everything,

[0:07:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=467s) honestly, we would have just clicked

[0:07:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=469s) allow cuz there's nothing to say no to.

[0:07:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=470s) It's just part of the script that in

[0:07:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=473s) this example case npm test runs. And

[0:07:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=476s) permissions only decide if a tool call

[0:07:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=479s) runs, but they cannot limit what it can

[0:08:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=481s) reach once it's running. So, we want to

[0:08:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=483s) make sure that these kinds of scripts

[0:08:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=485s) can still run because this is just part

[0:08:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=487s) of, you know, how Cloud can check its

[0:08:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=488s) own work running tests.

[0:08:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=490s) So we cannot just block npm tests, but

[0:08:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=492s) we want to limit its side effects. So

[0:08:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=494s) really, we just want to limit the

[0:08:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=495s) environment that it's running in.

[0:08:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=498s) So if you're running it locally or on

[0:08:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=500s) your own machine, you can run commands

[0:08:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=502s) like that in a sandbox. So then you have

[0:08:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=504s) control over which files in a command it

[0:08:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=506s) can read, which folders it can write to,

[0:08:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=509s) which hosts it can reach. And the

[0:08:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=511s) operating system enforces that.

[0:08:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=514s) Also, this also applies to everything

[0:08:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=515s) that command then starts, so any child

[0:08:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=517s) processes.

[0:08:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=519s) So on its own, that deny rule gets

[0:08:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=521s) checked by Cloud before the command

[0:08:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=522s) runs, but all it sees there is npm

[0:08:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=525s) tests. So it doesn't see which files

[0:08:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=527s) that script ends up opening. But with

[0:08:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=529s) the sandbox on, that same rule gets

[0:08:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=531s) passed on to the operating system. So

[0:08:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=533s) now when when that dependency tries to

[0:08:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=536s) open or end file, the operating system

[0:08:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=537s) just doesn't let it.

[0:08:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=539s) And by default, it can still read most

[0:09:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=540s) of your machine, so you'd want to add

[0:09:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=542s) another rule for your SSH keys if you

[0:09:04](https://www.youtube.com/watch?v=vlfCjWuv4es&t=544s) care about that.

[0:09:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=546s) And it also cannot reach a host that

[0:09:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=548s) wasn't approved.

[0:09:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=550s) But the sandbox only covers the shell

[0:09:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=552s) commands that Cloud runs and whatever

[0:09:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=554s) those start. But Cloud's own files, your

[0:09:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=556s) MCP servers, and all of your hooks still

[0:09:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=558s) run outside of it. So the rest of your

[0:09:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=561s) session still runs on your own machine

[0:09:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=562s) and everything that's on there. So

[0:09:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=564s) ideally, you want this whole thing to

[0:09:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=566s) run somewhere where none of that is even

[0:09:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=568s) there in the first place. And that is a

[0:09:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=571s) Cloud session because there it gets its

[0:09:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=573s) own machine with a fresh copy of a repo.

[0:09:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=576s) And this runs even when we close our

[0:09:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=577s) laptop, which is definitely something

[0:09:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=579s) you want for these longer running

[0:09:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=580s) sessions that run for hours.

[0:09:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=583s) So in this case, this automatically gets

[0:09:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=585s) rid of the end file issue because it's

[0:09:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=587s) not in Git, and neither are my SSH keys

[0:09:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=589s) or our GitHub token.

[0:09:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=591s) And if it still needs an API key, you

[0:09:54](https://www.youtube.com/watch?v=vlfCjWuv4es&t=594s) can add that as a network secret where

[0:09:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=595s) it will it will tell you like, hey, I'm

[0:09:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=597s) missing an API key mid-session,

[0:10:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=600s) so it can use it without actually ever

[0:10:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=601s) sending it to the model. And by default,

[0:10:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=603s) also in the Cloud session, network

[0:10:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=606s) access is limited to things like package

[0:10:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=608s) registries in GitHub. So you have to

[0:10:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=610s) explicitly add those domains to your

[0:10:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=612s) environment for Cloud to to reach other

[0:10:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=614s) hosts.

[0:10:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=616s) Okay, so with a Cloud session we can run

[0:10:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=618s) these long-running sessions even with

[0:10:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=620s) our laptop closed and it keeps us safe

[0:10:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=623s) because it runs in its own environment.

[0:10:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=626s) Now it's still good to remember that

[0:10:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=628s) this machine is disposable, but the

[0:10:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=629s) things that leave it aren't. So a commit

[0:10:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=631s) pushed or a message it sent through a

[0:10:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=633s) connector. So we still run it in auto

[0:10:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=636s) mode with our deny rules just commit it

[0:10:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=638s) into the repo so they come along. Uh so

[0:10:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=640s) it it could still catch things like a

[0:10:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=642s) forced push or a secret in a commit, all

[0:10:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=644s) that kind of stuff.

[0:10:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=647s) And beyond just safety um we also need

[0:10:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=650s) to make sure that Cloud is actually

[0:10:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=651s) working on the right thing. So next is

[0:10:54](https://www.youtube.com/watch?v=vlfCjWuv4es&t=654s) verification. And the nice thing about

[0:10:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=656s) being in a loop uh like we kind of knew

[0:10:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=658s) the work was good because we'd already

[0:11:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=660s) kind of seen every change, we'd approved

[0:11:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=662s) everything.

[0:11:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=663s) But now if Cloud works for hours in the

[0:11:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=665s) background, we don't have that anymore.

[0:11:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=667s) Um and we're not really going to read

[0:11:09](https://www.youtube.com/watch?v=vlfCjWuv4es&t=669s) every file at the end either.

[0:11:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=672s) So you know, say that we ask you to move

[0:11:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=674s) our auth to a new API. Well Cloud is

[0:11:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=677s) very good at understanding what we want,

[0:11:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=679s) but there are still a lot of small

[0:11:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=680s) decisions that it has to make along the

[0:11:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=682s) way. So with the exact same prompt, you

[0:11:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=684s) know, one run might move it over but

[0:11:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=686s) leave the old API in there or one might

[0:11:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=689s) move it but only for new logins and

[0:11:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=691s) another one might move it but log

[0:11:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=693s) everyone out. And these all look pretty

[0:11:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=695s) reasonable, but it really helps to set

[0:11:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=698s) up these verification points along the

[0:11:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=699s) way. So Cloud keeps verifying its own

[0:11:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=702s) results. And those can be anything that

[0:11:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=704s) comes back as a pass or fail. So tests,

[0:11:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=707s) a build, a screenshot, whatever you

[0:11:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=708s) have.

[0:11:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=709s) So now we just want to make sure that we

[0:11:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=711s) review these verification points. Uh

[0:11:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=713s) there are a lot shorter to review than

[0:11:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=715s) if we just had to you know, review the

[0:11:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=717s) whole change at the end. So so that's

[0:11:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=718s) pretty reasonable.

[0:12:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=720s) So if one of these runs would still log

[0:12:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=721s) everyone out, it doesn't get past that

[0:12:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=723s) first check and then it just has to find

[0:12:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=725s) another way. And there's a couple ways

[0:12:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=727s) to set this up. Um the easiest one is of

[0:12:09](https://www.youtube.com/watch?v=vlfCjWuv4es&t=729s) course just in your prompt. So you know,

[0:12:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=731s) you say what done looks like and ask it

[0:12:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=733s) to split that into tasks so they have

[0:12:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=735s) their own tests. Um, and I also like to

[0:12:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=737s) ask it to show the actual output because

[0:12:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=739s) you weren't there to see it. But again,

[0:12:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=741s) prompting is not a guarantee that a

[0:12:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=743s) model will do it. So for the ones that

[0:12:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=745s) have to run

[0:12:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=747s) guaranteed run, I would use hooks, um,

[0:12:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=749s) which are just, you know, scripts that

[0:12:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=751s) Cloud Code runs at a specific point.

[0:12:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=753s) And

[0:12:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=754s) those give you a lot of control because

[0:12:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=756s) you decide when they run and what they

[0:12:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=758s) run and what they check.

[0:12:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=759s) So for example, every time it edits a

[0:12:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=761s) file, we can run our linter. Every time

[0:12:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=763s) it wants to mark a task as complete, we

[0:12:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=765s) can run the tests for what it changed.

[0:12:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=767s) Um, so you know, if it touched our auth

[0:12:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=769s) code or something, it has to pass the

[0:12:51](https://www.youtube.com/watch?v=vlfCjWuv4es&t=771s) auth auth tests.

[0:12:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=772s) And when it wants to finish the whole

[0:12:54](https://www.youtube.com/watch?v=vlfCjWuv4es&t=774s) session, we can just run the entire test

[0:12:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=775s) suite.

[0:12:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=776s) And if one of those fails, it goes, oh,

[0:12:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=779s) that's still broken. It goes back until

[0:13:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=781s) it passes, so it fixes it. Now, just one

[0:13:04](https://www.youtube.com/watch?v=vlfCjWuv4es&t=784s) thing,

[0:13:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=785s) um, when a test fails, by default, most

[0:13:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=787s) tools that exit with a one exit code,

[0:13:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=790s) um, but with a one, that task by Cloud

[0:13:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=792s) Code just gets marked as completed

[0:13:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=794s) anyway. So make sure that your scripts

[0:13:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=797s) exit with a two exit code because that's

[0:13:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=799s) what actually sends Cloud back to fix

[0:13:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=801s) it.

[0:13:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=802s) So

[0:13:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=803s) okay, now we have one session that I'm

[0:13:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=805s) pretty comfortable with leaving alone.

[0:13:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=808s) So now we can start with a few more of

[0:13:30](https://www.youtube.com/watch?v=vlfCjWuv4es&t=810s) those because they've all got their own

[0:13:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=812s) machines, so they're, you know, not all

[0:13:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=813s) working in the same folder and we don't

[0:13:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=815s) really have to think about work trees

[0:13:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=816s) too much ourselves anymore.

[0:13:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=819s) But then we still start every session

[0:13:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=821s) ourselves and we review every one of

[0:13:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=823s) them. And honestly, this is already a

[0:13:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=825s) pretty good place to be. We are still

[0:13:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=827s) fully in control over what gets started

[0:13:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=830s) and when we call a task done.

[0:13:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=833s) But even there, um, you know, we're

[0:13:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=835s) still the ones kicking off every session

[0:13:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=837s) and we're still in the loop for all of

[0:13:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=839s) them. So I think the most important

[0:14:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=841s) thing to have in place here now is your

[0:14:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=842s) CI because

[0:14:04](https://www.youtube.com/watch?v=vlfCjWuv4es&t=844s) all of these sessions eventually open a

[0:14:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=846s) PR and your CI runs the same checks on

[0:14:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=848s) every one of them, no matter how that

[0:14:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=850s) session was set up or, you know, what

[0:14:11](https://www.youtube.com/watch?v=vlfCjWuv4es&t=851s) Cloud decided to do along the way. And

[0:14:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=853s) And you turn on auto fix, we have like

[0:14:15](https://www.youtube.com/watch?v=vlfCjWuv4es&t=855s) CI auto-fix,

[0:14:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=856s) Claude can also see when one of those

[0:14:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=858s) checks fails and then go back to fix it.

[0:14:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=860s) So you're not the one spending your

[0:14:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=862s) review on things that, you know, a check

[0:14:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=864s) could have already caught.

[0:14:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=867s) And for some of them, you can even turn

[0:14:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=868s) on merge when ready. So then GitHub

[0:14:30](https://www.youtube.com/watch?v=vlfCjWuv4es&t=870s) merges the PR once all of the checks

[0:14:32](https://www.youtube.com/watch?v=vlfCjWuv4es&t=872s) have passed. So you're not in the loop

[0:14:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=874s) to review. Um but again, that that's not

[0:14:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=877s) the default and that really depends on

[0:14:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=878s) how risky the change is. So for example,

[0:14:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=880s) on our team, every PR gets reviewed by

[0:14:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=883s) Claude first. So not by the session that

[0:14:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=885s) wrote it. So it comes with a fresh

[0:14:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=888s) context and also a separate group of

[0:14:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=890s) agents to just double check every bug it

[0:14:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=892s) finds.

[0:14:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=893s) And then how much we review ourselves

[0:14:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=895s) just depends on the risk. So smaller

[0:14:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=897s) changes like docs or copy, they don't

[0:14:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=899s) need a person. So once the automated

[0:15:01](https://www.youtube.com/watch?v=vlfCjWuv4es&t=901s) checks are green, we're pretty good to

[0:15:03](https://www.youtube.com/watch?v=vlfCjWuv4es&t=903s) go. Um maybe ordinary product changes

[0:15:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=905s) just need one reviewer and then risky

[0:15:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=907s) changes might need two.

[0:15:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=910s) Now ultimately, kind of where we see

[0:15:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=912s) things going um and we're already kind

[0:15:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=914s) of doing more of that at Anthropic is

[0:15:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=916s) that you're not really starting all of

[0:15:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=918s) those sessions yourself either. Because

[0:15:19](https://www.youtube.com/watch?v=vlfCjWuv4es&t=919s) if you're anything like me, I'm terrible

[0:15:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=921s) at context switching. So having to

[0:15:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=923s) manage so many sessions at the at the

[0:15:25](https://www.youtube.com/watch?v=vlfCjWuv4es&t=925s) same time doesn't always go well.

[0:15:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=927s) So instead, you just have one main

[0:15:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=929s) session that's your orchestrator and you

[0:15:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=931s) can already see this in things like

[0:15:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=933s) Claude Code projects, which is still in

[0:15:35](https://www.youtube.com/watch?v=vlfCjWuv4es&t=935s) beta, but

[0:15:37](https://www.youtube.com/watch?v=vlfCjWuv4es&t=937s) you just tell it what it needs to be

[0:15:39](https://www.youtube.com/watch?v=vlfCjWuv4es&t=939s) done and the orchestrator splits that up

[0:15:41](https://www.youtube.com/watch?v=vlfCjWuv4es&t=941s) and then starts other sessions for each

[0:15:43](https://www.youtube.com/watch?v=vlfCjWuv4es&t=943s) task and it keeps track of what comes

[0:15:45](https://www.youtube.com/watch?v=vlfCjWuv4es&t=945s) back. So it automatically starts and

[0:15:47](https://www.youtube.com/watch?v=vlfCjWuv4es&t=947s) verifies these threads which are just

[0:15:49](https://www.youtube.com/watch?v=vlfCjWuv4es&t=949s) new sessions. So instead of talking to

[0:15:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=952s) eight sessions, you're just talking to

[0:15:53](https://www.youtube.com/watch?v=vlfCjWuv4es&t=953s) one.

[0:15:55](https://www.youtube.com/watch?v=vlfCjWuv4es&t=955s) And the main session doesn't write the

[0:15:56](https://www.youtube.com/watch?v=vlfCjWuv4es&t=956s) code itself. So there you want a model

[0:15:58](https://www.youtube.com/watch?v=vlfCjWuv4es&t=958s) that's really good at deciding what to

[0:16:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=960s) do and judging what comes back, a model

[0:16:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=962s) like Fable. And if something comes back

[0:16:05](https://www.youtube.com/watch?v=vlfCjWuv4es&t=965s) that isn't actually done, it just, you

[0:16:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=966s) know, sends it back so until it's

[0:16:08](https://www.youtube.com/watch?v=vlfCjWuv4es&t=968s) actually done and passes everything.

[0:16:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=970s) And the threads need a model that's good

[0:16:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=972s) at actually doing the work like Opus 55.

[0:16:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=974s) And you can set those separately. So,

[0:16:17](https://www.youtube.com/watch?v=vlfCjWuv4es&t=977s) you know, one model for the main session

[0:16:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=978s) and then another one for the threads.

[0:16:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=980s) And another benefit is that with this

[0:16:22](https://www.youtube.com/watch?v=vlfCjWuv4es&t=982s) setup with CloakCode projects

[0:16:24](https://www.youtube.com/watch?v=vlfCjWuv4es&t=984s) specifically, we don't manage context

[0:16:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=986s) anymore. That's all done automatically

[0:16:28](https://www.youtube.com/watch?v=vlfCjWuv4es&t=988s) for us.

[0:16:29](https://www.youtube.com/watch?v=vlfCjWuv4es&t=989s) no longer have to think about, you know,

[0:16:31](https://www.youtube.com/watch?v=vlfCjWuv4es&t=991s) when to compact or clear all of that

[0:16:33](https://www.youtube.com/watch?v=vlfCjWuv4es&t=993s) stuff.

[0:16:34](https://www.youtube.com/watch?v=vlfCjWuv4es&t=994s) Okay, so if you look back at those old

[0:16:36](https://www.youtube.com/watch?v=vlfCjWuv4es&t=996s) best practices, they're all still there,

[0:16:38](https://www.youtube.com/watch?v=vlfCjWuv4es&t=998s) but they've just moved.

[0:16:40](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1000s) So, the model steers it now, um auto

[0:16:42](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1002s) mode approves your deny rules and the

[0:16:44](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1004s) environment restricts what's possible,

[0:16:46](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1006s) um your tests, your hooks, and your CI

[0:16:48](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1008s) checks it. And then ultimately, Cloud

[0:16:50](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1010s) can just start them as well. So, almost

[0:16:52](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1012s) everything we used to do ourselves is

[0:16:54](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1014s) now either the model, the harness, or

[0:16:57](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1017s) the environment. And we're really just

[0:16:59](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1019s) here to start that first one and to just

[0:17:00](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1020s) review what comes out.

[0:17:02](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1022s) So, if you want to try this in your own

[0:17:04](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1024s) setup, I would say just take one thing

[0:17:06](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1026s) that's way bigger than you normally give

[0:17:07](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1027s) Cloud. Make sure your CI actually

[0:17:10](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1030s) catches the things you care about, and

[0:17:12](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1032s) then spend a bit of time just

[0:17:13](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1033s) configuring your environment, like its

[0:17:14](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1034s) network access, its secret, and its, you

[0:17:16](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1036s) know, setup script.

[0:17:18](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1038s) And then start in the cloud and see

[0:17:20](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1040s) where your sessions get stuck and where

[0:17:21](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1041s) you're still in the loop because that's

[0:17:23](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1043s) the next thing to hand over to Cloud. I

[0:17:26](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1046s) also highly recommend checking out our

[0:17:27](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1047s) best practices in the docs as well.

[0:17:30](https://www.youtube.com/watch?v=vlfCjWuv4es&t=1050s) Thank you so much.
