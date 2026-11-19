---
title: Your SKILL.md Is 70% Stuff the Model Already Knows — Nikolay Petrov
description: AI Engineer CODE 2026 官方閱讀版，Intel 的 Nikolay Petrov 談把 skill 拆成原子問答、有無 skill 對照量出模型已知內容，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-skills-knowledge
published: 2026-11-11
tags:
  - clippings
  - skill
  - evaluation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 Dokimi 被辨識成「the document」、Sonnet 被辨識成「sonet」）。逐字稿對應 Day 1 直播 `https://www.youtube.com/watch?v=ZZ19zhYnDKY`（影片 ID `ZZ19zhYnDKY`，本場 7:00:53–7:14:53，屬 Online Track 預錄內容）。`published` 取自該直播的 YouTube release_date。

Day 1 livestream · [7:00:53–7:14:53 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25253s). The player starts and stops at this session’s boundaries.

## Introduction

A skill can teach an agent something it does not know, or it can steer the agent through a process it already understands. Nikolay Petrov starts by keeping those purposes separate. Both can be useful. His talk asks how to measure the first kind of value without assuming that every sentence in a successful skill supplies new knowledge.

That distinction is essential to the title. “The model already knows this” is not the same as “this instruction is useless.” A reminder can constrain behavior even when it introduces no new concept. Petrov's proposal is a diagnostic for optimization, followed by task evaluation, not a license to delete most of every skill file.

[7:02:13 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25333s)

## Begin with tasks, not a feeling that the skill helps

At [07:02:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25333s), Petrov describes the ordinary with-skill/without-skill comparison. Define tasks, preferably with outcomes that can be checked deterministically, and run both arms. His illustrative example goes from three solved tasks out of five to all five. Token usage and completion time can matter alongside the solve rate.

This establishes that a skill helps, but not which pieces are responsible. Once the model changes or the skill grows, editing line by line becomes an expensive guessing exercise. Petrov wants a smaller unit of analysis than the whole document and a more meaningful unit than an arbitrary line break.

[7:04:53 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25493s)

## Break the instructions into testable atoms

Around [07:04:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25493s), he introduces atomic items inspired by fact-oriented evaluation. Each item becomes a question paired with the expected answer. Some items express general propositions; others specify contracts, such as exact required behavior or conditions.

For each item, the system queries the target model both with and without the skill. A judge, preferably from a different model family or a panel, grades the answers. Question construction must avoid leaking the answer. The experiment can also distinguish closed-book knowledge from practical performance with tools such as web access, depending on what is being measured.

The two arms produce four useful cases:

- Correct in both: the model can answer without the skill.
- Correct only with the skill: the skill supplies useful information.
- Correct only without the skill: the added context hurts this answer.
- Incorrect in both: the skill has not successfully taught the tested item.

These are observations about the question and evaluation setup. They do not by themselves establish how the agent will behave in a long, tool-using task. They do identify where to investigate first.

## Fix harm before chasing compression

Petrov turns first to the third category. Material that degrades an answer is a strong candidate for revision. In the popular skills he tested, he says this was uncommon, but less-developed skills showed more such problems. The method can color portions of a document according to their contribution, exposing where a skill adds information and where it restates known concepts.

He also addresses the cost of running the diagnostic, reporting a roughly $14 experiment across twenty-nine skills. That is an account of his setup, not a stable pricing promise. The practical attraction is that a targeted assessment can be cheaper than repeatedly trying arbitrary combinations of edits against the full task suite.

[7:10:09 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25809s)

## Knowing the concept is not knowing the exact rule

At [07:10:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25809s), Petrov changes the grading standard. Lenient grading accepts the general idea even if a detail is missing. Strict grading requires the full condition or instruction. The distinction dramatically changes the apparent amount of knowledge already present in the model.

[![General understanding and exact instruction recall differ](https://ai.engineer/reading/code-2026/images/online-skills-knowledge-25850.jpg)](https://ai.engineer/reading/code-2026/images/online-skills-knowledge-25850.jpg) *Original stream, 7:10:50. In the displayed comparison, Opus 5.5 drops from 70% to 22% of atoms known without the skill when grading becomes strict.*

The slide gives a particularly useful example: knowing that the user makes the decision is not the same as knowing to put each decision to the user **and wait**. Omitting the wait can fail a behavioral contract even though a lenient judge recognizes the general principle.

The displayed **Haiku 5.5** result falls from 45% to 18%; **Opus 5.5** falls from 70% to 22%. Petrov's interpretation is that larger models often know the concepts while still benefiting from precise keys, values, conditions, and steps. The headline 70% therefore depends on what counts as knowing, which model is tested, and which skills are included.

## Use novelty to propose edits, then rerun the real evaluations

Petrov next compares repositories and models, emphasizing that the amount of prior knowledge varies by skill. A directional process skill may reasonably contain familiar material. A knowledge skill targeting a smaller model may need explanations that a larger model can supply unaided. There is no single minimal skill independent of the model and job.

His closing procedure returns to the task evaluations from the opening. Remove or rewrite candidate material, then check whether the skill still solves the intended problems. If scores hold while the document shrinks, the saved context is real. If behavior deteriorates, apparent redundancy was doing useful work.

The framework he demonstrates can also examine routing, descriptions, and other context artifacts, but novelty is only one signal. The contribution of this talk is an intermediate layer between intuition and brute-force prompt editing: identify which atomic instructions are new, harmful, or still not understood, then use that evidence to choose experiments. A shorter `SKILL.md` is a successful outcome only if the agent continues to do the work.

Full transcript 285 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[7:00:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25253s) >> Hello, my name is Nikolai Petro and we

[7:00:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25255s) will be talking about skills and agents

[7:00:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25257s) knowledge of those skills.

[7:01:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25261s) We'll start it with the simple prompts

[7:01:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25263s) where we've been playing with the new

[7:01:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25266s) stuff, new work being done by the

[7:01:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25268s) agents, repeating those prompts over and

[7:01:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25270s) over again. And then we start packing

[7:01:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25272s) those into the skills,

[7:01:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25274s) creating repeatable, reproducible,

[7:01:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25277s) portable type of their functionality

[7:01:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25281s) or capabilities that we can teach agents

[7:01:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25285s) to work with. And some of those skills

[7:01:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25287s) are very important. hundreds of the

[7:01:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25288s) stars on GitHub.

[7:01:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25293s) There are different types of their

[7:01:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25294s) skills. Some teach models something new

[7:01:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25298s) bringing new knowledge or capabilities

[7:01:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25300s) to the model. But there are also types

[7:01:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25303s) of their just steering or process skills

[7:01:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25306s) where we

[7:01:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25308s) do not bring any additional information

[7:01:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25310s) but just getting repeatable

[7:01:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25313s) flow of the actions that we want agents

[7:01:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25315s) to perform. both are useful. In this

[7:01:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25319s) session, we will be talking about new

[7:02:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25321s) knowledge type of the skills and

[7:02:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25325s) we'll see what we can

[7:02:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25328s) get from the models understanding of

[7:02:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25330s) those skills.

[7:02:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25333s) So, we get our first skills packed,

[7:02:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25336s) start using them. Um, basically

[7:02:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25341s) starting with the the feel of does it

[7:02:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25344s) work or not. But there is also the more

[7:02:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25346s) technical way and more deterministic way

[7:02:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25348s) for the checking if skills are working

[7:02:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25350s) or not and what's the impacts of those

[7:02:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25353s) skills are evolves. There are different

[7:02:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25356s) formats where evolves can be defined.

[7:02:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25359s) But at the sense this is task definition

[7:02:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25361s) that you want your agent to be able to

[7:02:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25364s) solve.

[7:02:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25366s) You put it in the place ideally more

[7:02:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25368s) deterministic so we can uh validate it

[7:02:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25371s) and we can check two arms one there no

[7:02:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25376s) skill loaded and there second one where

[7:02:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25378s) we're loading the skill and providing

[7:02:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25379s) this additional information to the

[7:03:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25381s) context and we compare how the runs

[7:03:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25384s) there are multiple things one is how

[7:03:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25387s) many

[7:03:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25388s) evolves been solved in this case with no

[7:03:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25391s) skill we're solving three out of five

[7:03:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25394s) with skill we're solving all five

[7:03:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25396s) meaning that we get two more tasks.

[7:03:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25399s) There also would be implications on the

[7:03:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25401s) tokens usage or time that it took those

[7:03:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25405s) tasks to be completed and other factors.

[7:03:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25408s) But at the end we are comparing those

[7:03:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25410s) and seeing what makes sense, what not.

[7:03:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25412s) And this is one of the mains for

[7:03:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25415s) evaluating the skills and uh saying that

[7:03:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25418s) they not just nice ideas but actually

[7:03:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25421s) working pieces of instructions and

[7:03:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25423s) context for the agents.

[7:03:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25426s) But what next? We get to the stage where

[7:03:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25430s) we have their working skill. It solves

[7:03:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25432s) some evolves. But we know that there

[7:03:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25437s) should be a better way. We have models

[7:03:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25439s) evolving. We have u some

[7:04:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25443s) might be cases where we want

[7:04:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25447s) to get skill more efficient meaning

[7:04:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25450s) consuming less tokens. So what's their

[7:04:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25452s) the options there? One is just change

[7:04:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25455s) line by line and try brute force all the

[7:04:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25460s) different combinations. Another would be

[7:04:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25463s) to think through what makes sense. So

[7:04:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25465s) maybe use something as the user feedback

[7:04:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25469s) on the skills to see where the skills

[7:04:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25472s) perform well. Uh there it's not. And

[7:04:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25475s) with new models just running skill and

[7:04:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25478s) seeing how it works, what's the options

[7:04:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25481s) there? and how large those modifications

[7:04:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25485s) should be just

[7:04:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25487s) lines, sentences, ideas.

[7:04:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25493s) So what we found to be useful is instead

[7:04:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25497s) of relying on their luck, we can put

[7:05:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25500s) more deterministic process here using

[7:05:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25503s) idea of their items from their fact

[7:05:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25506s) score. uh

[7:05:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25508s) we can split their skill and

[7:05:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25511s) instructions into those items and

[7:05:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25516s) for each of those had the pair of

[7:05:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25519s) question and answer that we expect.

[7:05:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25522s) This could be either general ideas like

[7:05:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25525s) proposition in this case or contracts

[7:05:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25528s) there we put more definitive expectation

[7:05:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25532s) on their action

[7:05:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25537s) and in general we will be getting their

[7:05:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25543s) some predefined amount of the items per

[7:05:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25546s) skill and we will have let's say

[7:05:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25550s) 25 or 30 items arms per skill.

[7:05:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25554s) Then for each of the items, we will

[7:05:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25557s) again run two arms, one without skill

[7:06:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25560s) and one with skill.

[7:06:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25563s) And we will have judge or panel of

[7:06:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25567s) judges that will be evaluating model

[7:06:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25569s) answers. So we asking those questions to

[7:06:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25571s) the model that we're interested in.

[7:06:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25574s) We evalating those questions with the

[7:06:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25577s) judge ideally different family of the

[7:06:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25580s) models or panel of judges also ensures

[7:06:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25584s) that the question do not leak answers.

[7:06:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25589s) We depending on the case can compare

[7:06:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25592s) with no tools or additional um

[7:06:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25595s) information to check their internal

[7:06:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25597s) model understanding or provided with

[7:06:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25600s) their some tools like web access. So uh

[7:06:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25603s) it would be more practical

[7:06:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25605s) and we

[7:06:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25608s) can get the simple four outcomes matrix

[7:06:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25615s) basically where we are checking that the

[7:06:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25617s) model

[7:06:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25619s) uh knows or do not know something and

[7:07:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25623s) how this maps to their skill impact on

[7:07:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25625s) this. So the simplest option is where

[7:07:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25629s) model was able to answer this particular

[7:07:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25633s) questions even without skill or with

[7:07:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25636s) skill. This means that skill have no

[7:07:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25638s) impact on this and this was already part

[7:07:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25640s) of the model's knowledge. The second one

[7:07:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25643s) is where without skill actual model was

[7:07:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25645s) able to answer this correctly

[7:07:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25648s) and by adding skill we saw degradation

[7:07:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25652s) in performance and model capability to

[7:07:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25655s) talk or explain particular aspects.

[7:07:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25660s) The ideal case is where without skill

[7:07:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25663s) model wasn't able to answer something

[7:07:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25664s) and with skill we start seeing that it

[7:07:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25667s) can answer those new type of the

[7:07:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25669s) questions and scenarios and this is what

[7:07:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25671s) we were aiming for teach model something

[7:07:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25673s) new

[7:07:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25675s) but there also can be the fourth option

[7:07:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25677s) where skills were written not ideally or

[7:08:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25683s) in some maybe not clean way where model

[7:08:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25688s) wasn't able to answer it either without

[7:08:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25690s) skill or with skill. And while this

[7:08:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25692s) topic might be relevant and important

[7:08:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25694s) for the model, it still sort of misses

[7:08:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25696s) some of those concepts.

[7:08:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25701s) The simplest thing to fix are

[7:08:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25706s) instructions or items that actually hurt

[7:08:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25708s) performance. And

[7:08:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25711s) for popular skills, those are criteria.

[7:08:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25714s) So in the

[7:08:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25717s) uh box below you see that it's just one

[7:08:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25721s) case out of the mostly 400 items in

[7:08:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25725s) entropic skills and others don't have

[7:08:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25728s) those. But for their smaller skills that

[7:08:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25732s) are less popular, you probably having

[7:08:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25734s) more of those. This is what we're seeing

[7:08:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25735s) with some of our experiments.

[7:08:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25739s) And

[7:09:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25741s) this is just straightforward the

[7:09:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25743s) simplest thing to fix to ensure that

[7:09:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25746s) your skill do not reduce model

[7:09:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25748s) capabilities and performance and bring

[7:09:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25750s) only relevant

[7:09:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25752s) context there.

[7:09:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25755s) And we also can actually color this. In

[7:09:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25757s) this scenario, this is done by lines but

[7:09:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25760s) actually going with it atoms. You might

[7:09:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25762s) have their uh different coloring for a

[7:09:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25764s) single line or a single sentence.

[7:09:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25768s) And this just gives your example of

[7:09:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25770s) their uh visualization where this would

[7:09:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25774s) be helpful details and instructions in

[7:09:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25777s) terms what new stuff you bring to the

[7:09:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25780s) model and what is

[7:09:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25785s) something that model already knows.

[7:09:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25788s) Costwise

[7:09:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25789s) we are running all those questions and

[7:09:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25791s) asking model

[7:09:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25793s) but still relatively this is uh cheap

[7:09:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25796s) for 29 skills 14 bucks of their set and

[7:09:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25799s) ha calls with their sonet used as a

[7:10:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25803s) judge

[7:10:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25805s) and

[7:10:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25809s) there are couple ways how we also can

[7:10:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25812s) check their strictness of their some

[7:10:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25816s) knowledge. Um we have uh lang and strict

[7:10:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25820s) ways of the checking this where first

[7:10:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25823s) checks the general idea while the second

[7:10:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25826s) one is checking for exact details and

[7:10:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25830s) you can think about the difference

[7:10:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25832s) between general knowledge and

[7:10:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25833s) understanding of the topic to the

[7:10:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25836s) understanding of the exact keys

[7:10:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25838s) parameters and exact values or steps.

[7:10:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25843s) And what we see across the models is the

[7:10:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25846s) difference is large especially with the

[7:10:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25851s) um larger frontier models where we see

[7:10:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25853s) almost dropping from 70% understanding

[7:10:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25855s) of their skill in case of the general

[7:10:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25858s) understanding to just 22% of the

[7:11:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25862s) specific details.

[7:11:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25865s) And this is much our expectations. We

[7:11:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25868s) see that new models are pretty well

[7:11:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25870s) generalized to understand concepts but

[7:11:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25873s) it's still helpful to provide their with

[7:11:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25875s) exact details and data that will be

[7:11:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25877s) useful for their solving those problems.

[7:11:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25883s) Here is outlook of their um comparing

[7:11:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25888s) those three popular repos with the

[7:11:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25890s) skills across different models. So one

[7:11:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25894s) of the interesting observations here is

[7:11:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25896s) that smaller model have in general lower

[7:11:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25900s) understanding of the

[7:11:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25903s) skill

[7:11:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25905s) with their larger sonet having better

[7:11:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25907s) understanding which is

[7:11:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25910s) why we have bigger models. But also we

[7:11:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25913s) see that overall their models already

[7:11:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25915s) understand a lot of their

[7:12:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25921s) details and context of those skills. And

[7:12:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25923s) you would expect that with the newer

[7:12:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25925s) models and more advances in their uh

[7:12:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25929s) better training capabilities we will

[7:12:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25931s) have more and more

[7:12:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25934s) uh in terms of the models understanding.

[7:12:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25937s) But also we see that this pretty

[7:12:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25939s) significantly differs skill to skill

[7:12:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25942s) and it's not bad. Some skills are

[7:12:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25945s) intended to be directional

[7:12:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25948s) but it's also useful piece of

[7:12:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25950s) information to see how those

[7:12:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25953s) skills bring new knowledge uh to the

[7:12:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25956s) different model and different families.

[7:12:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25958s) And uh this should be run ideally in the

[7:12:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25960s) broader set of the models.

[7:12:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25968s) But just having their

[7:12:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25972s) this novelty piece of information is

[7:12:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25976s) just one of the signals. It's basically

[7:12:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25977s) initial vector for optimization. At the

[7:12:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25979s) end we still have to run evolves and

[7:13:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25982s) validate that all the changes that we

[7:13:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25986s) try make with their skill actually

[7:13:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25988s) works.

[7:13:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25990s) So the one of their simpler scenarios

[7:13:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25992s) would be we can look on their skill and

[7:13:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=25996s) try to remove some or all of the already

[7:13:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26000s) known pieces of information from the

[7:13:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26002s) skill and run evalation.

[7:13:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26006s) It might come up with their same

[7:13:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26007s) scoring. Basically we will be getting

[7:13:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26010s) their same results model still capable

[7:13:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26011s) of solving those problems. Then great we

[7:13:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26014s) can reduce skill size safe tokens safe

[7:13:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26017s) context.

[7:13:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26019s) And instead of there brute forcing and

[7:13:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26022s) guessing what we can or should remove or

[7:13:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26025s) add or how to fix their uh

[7:13:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26029s) degradations, we can have a guidance.

[7:13:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26034s) So all of those measurements experiments

[7:13:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26037s) been done with the document which is a

[7:14:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26040s) framework for the comparing

[7:14:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26042s) everything related to the agents and

[7:14:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26044s) context

[7:14:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26046s) where it's is scale agents MD MCP tools

[7:14:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26050s) whatever and novelty is one of their

[7:14:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26054s) pieces of the functionality where you

[7:14:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26056s) can get this initial vector for their

[7:14:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26059s) skill optimization and evalation but

[7:14:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26061s) there also uh evolves there Assessment

[7:14:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26065s) of the context impact, routing,

[7:14:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26067s) comparing the uh descriptions, naming,

[7:14:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26071s) bunch of the things that related to the

[7:14:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26075s) skills where it would be helpful to

[7:14:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26078s) actually get there more deterministic

[7:14:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26079s) relations to make conscious decisions in

[7:14:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26082s) terms of what should be done with the

[7:14:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26084s) skills.

[7:14:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26087s) So, thank you for your time and please

[7:14:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=26090s) go ahead and write better skills.
