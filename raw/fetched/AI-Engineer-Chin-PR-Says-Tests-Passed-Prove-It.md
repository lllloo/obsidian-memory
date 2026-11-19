---
title: Your PR Says the Tests Passed. Prove It. — Stephen Chin & Cassandra Chin
description: AI Engineer CODE 2026 官方閱讀版，Chin 父女談用嵌入式圖資料庫替 PR 撰寫者預先組好證據包、強 writer 配便宜 reviewer，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-stephen-cassandra
published: 2026-11-12
tags:
  - clippings
  - coding-agent
  - knowledge-graph
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 Tracetoon 被辨識成 Tracetune／Trace2／Tracedoon，Showtail 被辨識成 Showtale；Archie 是漫畫裡代表 Relate 的角色，非辨識錯誤）。逐字稿對應 Day 2 直播 `https://www.youtube.com/watch?v=y9JtCCZP2MQ`（影片 ID `y9JtCCZP2MQ`，本場 6:57:39–7:20:36）；`published` 取 YouTube 直播 release_date。

## Give the PR writer an evidence packet, not another context dump

A pull request can contain good code and still give its reviewer a bad account of what happened.

Stephen Chin

**Neo4j**

VP of Developer Relations

Cassandra Chin

**Independent**

Book Author, Keynote Speaker, and Kids Workshop Instructor

Day 2 livestream · [6:57:39–7:20:36 on YouTube](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25059s). The player starts and stops at this session’s boundaries.

## Introduction

A pull request can contain good code and still give its reviewer a bad account of what happened. The description may claim a check passed, omit an exception, or summarize an earlier version of the work as though it describes the submitted change. Stephen and Cassandra Chin build their talk around that gap between implementation and evidence.

Their presentation uses a comic about a developer, a reviewer, and an increasingly expensive cycle of revisions. The joke carries a practical problem: repeatedly asking an agent to reconstruct a history does not guarantee a more accurate description. It may simply make the same uncertainty more expensive.

## The diff cannot tell the whole story

Cassandra traces the project back to work on understanding how students produced programs with AI. The submitted program contains the result, but much of the effort and decision-making lives in prompts and agent sessions. The same missing history matters for a pull request.

A diff can show what changed. It cannot by itself establish why a command was run, which directory it used, whether a check applied to the final version, or which failed attempt a later run superseded. An agent writing from its current session may have compressed or lost that context. Reconstructing it from multiple traces creates a richer record, but also a new opportunity to combine facts incorrectly.

The speakers' project, presented visually as Tracetoon, gathers that context and uses separate writing and review steps. The original flow researches traces, writes a description, reviews it, and loops with more context when needed. That improves the available evidence, yet the loop can still produce unsupported claims.

Their example concerns checks and the order in which they ran. A statement that verification succeeded must describe the actual execution and submitted content, not merely the presence of test commands somewhere in a trace. Adding more prose around that ambiguity does not resolve it.

[7:11:05 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25865s)

## Compute the relationships before writing

The proposed change is an embedded graph layer, Relate. Instead of repeatedly paying a model to rediscover how pieces of evidence connect, the system records relationships and retrieves the relevant neighborhood for a change.

[![A connected evidence packet replaces repeated archive reconstruction](https://ai.engineer/reading/code-2026/images/online-stephen-cassandra-25865.jpg)](https://ai.engineer/reading/code-2026/images/online-stephen-cassandra-25865.jpg) *At [07:11:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25865s), the comic describes the architecture directly: bring the evidence for this change with its sources, rather than carrying the whole archive every time.*

The graph is useful because the questions are relational. Which command belongs to this working directory? Which check ran against this version? What explanation connects to this edit? A compact packet can carry the relevant facts and their provenance together.

The speakers describe the database work as local computation rather than LLM inference. That does not make the whole system free: collection, storage, and computation still exist. It changes which component performs the repeated retrieval and relationship work. The language model receives a prepared brief instead of being responsible for every stage of evidence reconstruction.

This also gives the writer and reviewers a common reference. A reviewer can compare a claim with a bounded packet instead of independently inventing another account from a large, messy history.

## Keep the better writer; narrow the reviewers' job

The model-allocation choice is deliberately counterintuitive. The team retains a stronger writer while using cheaper reviewers for more focused cross-checking. They report that a cheaper writer often turns feedback into a mechanical checklist rather than a clear explanation, even after repeated revisions.

Review becomes more constrained when the relevant evidence is already organized. The reviewer looks for unsupported claims, missing findings, and mismatches between the draft and the packet. It is not asked to solve the entire research problem again.

That is a workload-specific argument, not a rule that reviewers should always use smaller models. It works here because the architecture changes what reviewing requires. The difficult work is partly moved into deterministic relationships and a shared brief.

## Measure the whole drafting loop

The speakers evaluate versions through their PR benchmark, using audit traces, code, model judging, and human review. They report better description quality and roughly halved token use for the graph-backed approach. Those are results presented by the project team, not an independently reproduced benchmark in this article.

The mechanism explains why both could move together. Fewer repeated searches and fewer revision loops reduce token use. Better attribution and connected evidence reduce opportunities for the writer to tell the wrong story. The comic is an optional output; the evidence packet is the architectural contribution.

The talk closes by generalizing to other evidence-heavy workflows. Before asking an agent to reason over an archive again, identify the relationships that can be stored and queried reliably. A smaller, connected record may be more useful than a larger context window. For a pull request, the goal is straightforward: let the reviewer understand what changed, why it changed, and what was actually verified.

Full transcript 327 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[6:57:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25059s) Hello and welcome to our AIA Engineer San Francisco talk.

[6:57:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25064s) My name is Stephen Chin.

[6:57:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25065s) I'm joined by Cassandra Chen, who's the creator of Tracetune framework.

[6:57:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25071s) Hi, I'm Cassandra Chen. I built Tracetune because I wanted to improve PRs. I see a lot of developers

[6:57:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25079s) doing great things. The speed of innovation is as fast as it has ever been with AI technologies,

[6:58:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25085s) but a lot of pull requests are getting rejected. And it's not because the code is bad, it's because

[6:58:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25091s) because the PRs often contain incorrect information

[6:58:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25094s) or are written poorly.

[6:58:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25097s) So hopefully with Tracetune, we can improve that.

[6:58:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25100s) It also has the option to add a fun comic

[6:58:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25102s) to help explain your pull requests in a funny way.

[6:58:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25108s) What we're gonna do today

[6:58:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25109s) is we're gonna go through a little bit

[6:58:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25111s) about kind of the common issues of PRs,

[6:58:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25114s) how to improve the quality,

[6:58:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25115s) how to improve token efficiency on this,

[6:58:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25117s) and hopefully help everyone to be a better AI engineer for your organization,

[6:58:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25123s) like our main character, Alex, who all he wants in life is to get an AI engineer hoodie.

[6:58:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25133s) That's a really neat hoodie.

[6:58:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25134s) I have a lot of AI engineer t-shirts, but I don't have the hoodie yet.

[6:59:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25140s) Get Swix to make this AI engineer hoodie, everyone.

[6:59:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25146s) And this is enough motivation that hopefully he's going to do an amazing talk at the conference about his use case study on what he's doing in his company to improve the quality of PRs.

[6:59:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25160s) Here is a picture of the token factory where Alex works.

[6:59:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25165s) So Alex works together with a bunch of agents.

[6:59:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25170s) He has, of course, finance looking over his shoulder

[6:59:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25173s) Because we all spend too much tokens

[6:59:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25175s) And they want to make sure we're keeping up with costs

[6:59:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25178s) His buddy there, Pip, he's walking with

[6:59:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25180s) Carries all the evidence

[6:59:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25182s) And looks into the archives

[6:59:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25184s) And what's actually happening

[6:59:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25186s) And then Mira does all the reviews

[6:59:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25188s) So she's keeping track of things

[6:59:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25191s) It looks like Pip left his station empty

[6:59:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25198s) Part of the factory

[7:00:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25202s) Until he sees what Alex produced for a PR.

[7:00:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25205s) Oh, no.

[7:00:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25207s) That's a very long ledger.

[7:00:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25210s) A lot to review.

[7:00:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25214s) So it's hard.

[7:00:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25216s) And Mira's going through everything for the fine-tuned comb.

[7:00:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25219s) She actually is red.

[7:00:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25222s) Found some issues with the PR.

[7:00:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25226s) And this is a real PR that I think is actually one of your Tracetune PRs where it needs to have exact preview links for the URLs, command attribution, make sure the earlier work is qualified as well, and explain all of this in detail in the PR record to be accepted by Mira's very critical review.

[7:00:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25247s) This was interesting because as I was building Tracetune, I was actually, like, as I was building it, I was using Tracetune to test it.

[7:00:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25256s) So I would have Tracetune build the PRs.

[7:00:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25258s) And as I improved the PRs, it would, like, get better.

[7:01:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25263s) You got amazing comics along the way, too, just to have fun while you were building stuff.

[7:01:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25268s) Yeah.

[7:01:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25269s) Effective.

[7:01:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25275s) So you can see that the repeated PRs, which Alex is doing to try to get good quality results, are not working out.

[7:01:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25283s) Well, it's working out for his token billionaire card.

[7:01:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25286s) Do you know anything about the token billionaire program?

[7:01:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25289s) Yeah, so actually I am a token billionaire.

[7:01:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25292s) I spent lots and lots of tokens to build Tracetune.

[7:01:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25299s) That's kind of unfortunate. Was that all my money?

[7:01:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25304s) Don't sweat the details.

[7:01:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25307s) Okay. So I think there's a lot of good uses for tokens and for spending more AI work. Maybe doing repeated PRs is not where you want to spend your token.

[7:01:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25318s) And definitely the finance department is not happy with this.

[7:02:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25321s) So he wants a result, and he wants to make sure that the PRs are accurate, are working, and they don't have to keep getting repeated again and again by reviewing the logs and reconstructing the evidence repeatedly.

[7:02:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25335s) And it's interesting because normally when you're just coding on your agent, you're in your session and you ask it to write a PR.

[7:02:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25345s) it just reads your session log to try to figure out what it should have done using its inflated

[7:02:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25354s) context window. It actually often like as it's churning it compresses its context window

[7:02:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25360s) so it gets more and more inaccurate as it goes along. So instead what we're doing here is with

[7:02:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25367s) Tracetune we're having it read through different sessions on your computer to try to really figure

[7:02:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25374s) out what you built and what happened. Yeah, and I think like that concept of

[7:03:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25381s) looking through the audit trails, looking through like what the agents have actually done

[7:03:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25385s) is a lot of what you were doing with the Showtale project you were doing for education.

[7:03:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25391s) Yeah, I actually started this project with this Showtale project because there was this like

[7:03:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25397s) academic research study I was supporting, but basically the issue they hit is students were

[7:03:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25404s) creating programs, but there was no way to trace back the actual work and effort they did.

[7:03:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25409s) Because with AI coding, what you submit is the final work, the program, but most of the work

[7:03:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25416s) is the prompting and everything that came before, and that doesn't get submitted with the program.

[7:03:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25423s) And I use the technology and theory behind that to be like, well, I can also improve pull requests with all this data collection.

[7:03:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25434s) Cool. And I think that improvement in pull requests is something that benefits everybody because now you can find the evidence, like logging the change directory or the CWD before the CD runs, explaining why maybe other test data is leaking into other repos.

[7:04:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25451s) and explaining what's happening behind the scenes on the PR

[7:04:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25456s) rather than what most AI PRs read like,

[7:04:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25459s) which is a line-by-line explanation of the diffs

[7:04:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25461s) since that's what they build the PRs off of.

[7:04:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25468s) But incorrect facts can still pollute the information,

[7:04:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25472s) can cause a problem with conflicting PRs,

[7:04:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25475s) and then still give you back inaccurate results.

[7:04:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25480s) so maybe we have a solution for this what do you what do you think you have a solution cassandra

[7:04:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25485s) yeah everyone should use trace tune because of the comics so because the comics not because

[7:04:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25493s) it gives you better prs right well i started with the comics and i kind of went backwards and like

[7:04:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25499s) oh i need to actually make the prs better well hopefully better prs better comics and

[7:05:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25508s) and maybe better token savings by the end of this.

[7:05:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25512s) Maybe.

[7:05:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25513s) It should be.

[7:05:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25516s) So TraceDude is an open source project.

[7:05:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25518s) It lets you improve the quality of your PRs by pulling in agent context,

[7:05:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25523s) by pulling in information about the code,

[7:05:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25526s) and then having an independent writer, independent reviewer,

[7:05:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25530s) build better quality PRs, plus optionally giving you an amazing comic,

[7:05:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25535s) which, what do you think the best feature is here, Cassandra?

[7:05:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25539s) I think it's obviously the comics.

[7:05:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25542s) This is one of the earlier comics from when I was using Trace Tune to build it.

[7:05:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25550s) That's good.

[7:05:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25551s) And then you made sure that there's new characters every episode,

[7:05:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25554s) none of this repeating characters.

[7:05:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25556s) Yeah, that's what this PR was about.

[7:06:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25561s) Okay, and then this is a description of the original trace student flow.

[7:06:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25566s) So it finds all the traces for a particular branch.

[7:06:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25569s) It researches them, reviews the description, adds more context,

[7:06:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25573s) and kind of goes in a loop until it gets all of the evidence it needs to make a quality PR.

[7:06:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25579s) And subjectively but also through PRBench, which is a testing framework,

[7:06:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25586s) gives you better quality, better research,

[7:06:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25589s) lower rate of inaccuracies in the PRs.

[7:06:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25593s) I think at this point, the PRs were already better

[7:06:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25596s) than if you don't use Tracedoon.

[7:06:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25598s) But I found that it still makes some mistakes occasionally.

[7:06:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25602s) You can see at the end that it tries to revise with more context.

[7:06:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25606s) I think that's where the mistakes come in.

[7:06:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25610s) Okay, well, Alex thinks it's good enough.

[7:06:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25612s) He's going to try to solve the token crisis.

[7:06:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25614s) the factory with Trace2 and see if this will solve all of his problems.

[7:06:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25618s) Polish checked. Alex looks very, very happy. But Mira doesn't look that happy.

[7:07:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25626s) It looks like we still hit a mistake here, like I was saying earlier.

[7:07:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25631s) So the original PR claim was no later passing run is recorded.

[7:07:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25636s) And the problem here is in the actual Trace, it shows it running a button test

[7:07:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25644s) at the same time as the

[7:07:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25645s) bun x tsc

[7:07:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25648s) and you can't run those two

[7:07:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25650s) at the same time they have to be

[7:07:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25651s) run sequentially for the test to pass

[7:07:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25654s) yeah exactly

[7:07:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25656s) so he claims test passing

[7:07:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25658s) and all the checks were run

[7:07:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25659s) and actually that's not what the

[7:07:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25662s) code did so

[7:07:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25664s) poor Alex another

[7:07:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25665s) failed PR very angry

[7:07:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25668s) badger with all the token cost

[7:07:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25671s) kind of makes me feel like

[7:07:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25673s) Monday morning with the Neo4j finance department looking at my token spend each week.

[7:07:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25677s) But they're very forgiving, especially when it's an important project like this.

[7:08:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25686s) So maybe Alex can save some costs by using cheaper writers.

[7:08:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25689s) This is the number one thing finance has me to do.

[7:08:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25692s) They're like, hey, no more opus, sonnet, haiku, do something cheaper, please.

[7:08:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25697s) Does this work?

[7:08:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25699s) I feel like the quality is a bit lower

[7:08:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25702s) when you do it like that

[7:08:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25703s) just reducing the cost doesn't quite help

[7:08:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25706s) yeah so we were trying to get better quality

[7:08:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25708s) and we ended up getting worse quality

[7:08:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25710s) by just using cheaper writers

[7:08:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25714s) and obviously Alex is in a bind here right

[7:08:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25717s) he's spent too much on revisions

[7:08:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25719s) he doesn't have a solution for reducing token costs

[7:08:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25722s) he's not getting the results he wants out of his PRs

[7:08:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25725s) but

[7:08:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25727s) maybe there's

[7:08:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25728s) something Pip can help us with.

[7:08:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25730s) Pip has a friend.

[7:08:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25732s) I wonder who this friend could be.

[7:08:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25735s) Oh.

[7:08:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25736s) Well, I think you know from

[7:08:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25738s) my previous talks that this friend

[7:09:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25740s) is definitely going to be

[7:09:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25742s) a graph.

[7:09:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25744s) You're the graph guy. We're doing another

[7:09:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25746s) graph again.

[7:09:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25748s) Yeah, there's always a new graph.

[7:09:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25750s) But this is not the same old graph.

[7:09:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25752s) This is not the Neo4j

[7:09:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25755s) database. This is our new friend, Archie,

[7:09:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25759s) who is a embedded database written in Rust

[7:09:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25763s) called Relate that actually is being launched this week

[7:09:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25769s) at the Nodes Conference and also this talk at A Engineer

[7:09:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25772s) in San Francisco. And it's an open source

[7:09:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25777s) database which allows us to get a lot of the benefits

[7:09:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25780s) of more accuracy, multi-hop queries,

[7:09:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25784s) more explainable traces,

[7:09:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25786s) without having the heavyweight approach.

[7:09:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25789s) So it's kind of an agent-focused graph database

[7:09:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25792s) specifically for these sort of embedded use cases.

[7:09:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25798s) Okay, so let's see how Archie can

[7:10:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25800s) help us out. So before we were relying a lot on agents and loops of agents to resolve the problem, but graph databases can store relationships, can find different things which are clustered, build a brief which connects all this information together, and then give the agents, even a cheaper agent, better information and more context to give a good drafting decision

[7:10:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25824s) And the good thing about Archie is he has zero LLM costs.

[7:10:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25828s) It's all local compute costs and storage,

[7:10:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25832s) and it's a fully in-memory database and REST,

[7:10:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25834s) so it's highly optimized.

[7:10:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25835s) So we get this providence about all these submitted changes

[7:10:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25840s) and this evidence graph basically for free

[7:10:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25843s) compared to all the LLM and token costs,

[7:10:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25845s) which we were doing before.

[7:10:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25847s) And this means our buddy Alex doesn't need to research.

[7:10:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25850s) He doesn't need to go through and find all the facts again

[7:10:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25853s) and go through the sources.

[7:10:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25855s) because relate is going to do all that hard work for him

[7:10:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25859s) and build an evidence packet that he can use for trace tune.

[7:11:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25863s) It all sounds really great.

[7:11:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25864s) Maybe we do need more graphs.

[7:11:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25868s) I'm surprised to hear that from you

[7:11:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25870s) after all the graph talks you've had to put up with.

[7:11:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25872s) Okay, but we can do this

[7:11:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25875s) and make it even better with a neighborhood brief.

[7:11:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25878s) So basically taking all of the why, the code, the checks,

[7:11:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25881s) putting attributions and relationships between those

[7:11:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25884s) and then returning back a connected set of information as a packet.

[7:11:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25888s) by doing this, then when the agent is drafting up the PR,

[7:11:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25893s) it has all the connected facts with their sources together in a single source.

[7:11:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25898s) And that makes the writer draft more accurate with fewer passes.

[7:11:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25904s) And it also makes the reviewer's job much easier.

[7:11:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25907s) So we don't need an expensive reviewer.

[7:11:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25909s) We can save by using a few haiku reviewers instead of a sonnet reviewer or a Luna in the case of Codex to come up with the findings, check those against the draft, redo the writing, and then we retain the higher quality writer, a sonnet or tarot class writer to make sure we have a high quality brief that will pass human approval.

[7:12:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25933s) When we were building this, it felt very counterintuitive to have the writer be higher quality than the reviewers.

[7:12:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25940s) Actually, it's common that people always want to have the planner, the reviewer, the checker to be the highest quality model.

[7:12:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25948s) But if you're doing high quality writing, a lower model, no matter how many iterations and how much feedback you give it, can't do it.

[7:12:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25956s) It just turns things into a checklist and makes it very mechanical.

[7:12:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25959s) So to give writing which feels human-like, you do need a higher quality model.

[7:12:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25964s) And it's actually the reviewing and the cross-checking step, which is more mechanical.

[7:12:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25968s) So it's a little counterintuitive, but that works out quite well.

[7:12:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25972s) It's also a little counterintuitive that our badger has a thumbs up coming out of his chest, but let's ignore the high-quality AI artwork.

[7:13:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25985s) Okay, so we've checked all the claims against the evidence.

[7:13:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25988s) We've looked for missing findings with our cheaper reviewer.

[7:13:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25991s) Did the focus work?

[7:13:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25993s) And then found the things which were connected information

[7:13:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=25997s) to give a better draft and review for Mira.

[7:13:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26003s) And here's the output.

[7:13:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26005s) So it has the Y.

[7:13:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26007s) So log CWD, and that describes the shell before the TD runs.

[7:13:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26011s) What's the exception?

[7:13:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26013s) So the CD targets in repo, or the command mentions a root.

[7:13:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26017s) what passed. It has type check plus 71 tests, checked on submitted content, not before.

[7:13:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26024s) And then it starts in correlate.ts inspecting the leading CD exception.

[7:13:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26029s) And Mira looks pretty happy with these results, right?

[7:13:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26034s) Yeah, this might be the first scene where she's genuinely happy.

[7:13:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26039s) I think she was kind of happy with the AI engineer sweatshirt before she realized that Alex actually

[7:14:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26045s) was a was a goof okay so here are some of the actual data and results from the side-by-side

[7:14:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26052s) analysis using PR bench which is a pull request benchmark which uses audit traces plus code and

[7:14:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26061s) LM judges to review the quality of the work of course reviewed by human as well for accuracy

[7:14:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26067s) and you can see that on both Claude and Codex you get a significant quality improvements on a scale

[7:14:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26073s) one to 100 the judges by and large almost unilaterally liked the trace tune plus relate

[7:14:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26081s) quality better um on a one to 100 scale it was like 74 to 76 82 to 86 so plus two plus four point

[7:14:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26089s) these tests contributed to my token billionaire card because we were running lots and lots of

[7:14:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26096s) tests we created this side project called pr bench just for testing and we would have different

[7:15:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26102s) agents test over different pull requests and compare the results. Initially, I had it running

[7:15:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26110s) sequentially. It'll do one test and finish it, then do the next. But then we decided to run them

[7:15:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26116s) all in parallel. It's a very quick way to reach high spend. Yeah, that's kind of funny. At the

[7:15:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26124s) current testing rate with the number of use cases and tests on the benchmark, we can fully saturate

[7:15:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26130s) my high-end gaming computer with as many threads as Linux can handle simultaneously.

[7:15:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26137s) And of course, the token spend is slightly higher than what we'd like.

[7:15:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26143s) But it's all for the good of improving the quality of pull requests for the world.

[7:15:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26147s) So you all get the benefit of all these test runs and having the highest quality improvements.

[7:15:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26152s) And you save on tokens.

[7:15:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26155s) So we've spent the tokens for you in advance because Tracetune with the graph solution takes about half as many tokens as it did previously, which is an amazing result from the graph because now you're pre-computing.

[7:16:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26170s) You're getting all this evidence graph constructed in advance.

[7:16:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26174s) The writing's cheaper.

[7:16:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26176s) The reviewing's cheaper with a higher quality result.

[7:16:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26180s) I wasn't sure about the whole graph thing initially, but after seeing the cost tank almost in half, like it's not even a question to making this program work.

[7:16:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26193s) and this is something we did for the TraceTune project

[7:16:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26196s) but you can do this for pretty much any project

[7:16:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26198s) where you have data, you have relationships

[7:16:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26201s) you have evidence, you have things which you're trying to compare

[7:16:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26204s) because agents are not that good

[7:16:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26207s) at doing the data analysis

[7:16:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26209s) at doing all of the evaluation and the curation

[7:16:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26211s) so if you give them a help at the front end

[7:16:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26214s) by creating a custom graph layer

[7:16:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26217s) with an in-memory database like Relate

[7:17:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26220s) suddenly your costs go down, your quality goes up, and

[7:17:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26224s) you too can be a token billionaire like our friend Alex.

[7:17:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26229s) Well, I guess now he's using it as a bookmark.

[7:17:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26232s) I think that's a good use for it. It's a really high-quality bookmark.

[7:17:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26236s) It's heavier than a credit card.

[7:17:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26240s) It is a nice prize for spending all those tokens on PR bench.

[7:17:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26246s) so finance is happy

[7:17:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26247s) lower drafting costs that they can reasonably fund

[7:17:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26251s) Alex is happy he has his new bookmark

[7:17:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26254s) he now has a great case study

[7:17:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26257s) with the connections doing neighborhood retrievable facts

[7:17:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26261s) so that it's a better brief

[7:17:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26263s) focusing the reviews so the reviewers get the same compact brief

[7:17:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26266s) Mira gets exactly the evidence she needs

[7:17:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26269s) and then here's Alex on stage at

[7:17:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26272s) AI engineer. Somewhere in the world,

[7:17:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26275s) better PRs, lower drafting

[7:17:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26277s) costs with

[7:17:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26278s) a graph plus open

[7:18:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26281s) source. Trace to

[7:18:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26282s) build, which also gives you

[7:18:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26285s) amazing comics.

[7:18:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26290s) Okay.

[7:18:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26291s) So, big round of applause for our

[7:18:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26293s) friend Alex, who's now

[7:18:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26294s) earned the AI engineer

[7:18:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26296s) hoodie.

[7:18:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26298s) I think that's definitely a

[7:18:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26300s) wardrobe upgrade for him. Yeah, I don't think the pocket protector look was that great for him. So

[7:18:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26307s) good for him. I think we'll see Swix on stage with one of these hoodies soon. He can't not do it now

[7:18:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26313s) that we shamed into doing it at his own conference. The token O'Billion program is amazing. A big

[7:18:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26319s) kudos to the team for coming up with ways to incentivize and reward people who are in the

[7:18:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26324s) leading edge of AI usage and learning how to make it really effective for the rest of us.

[7:18:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26332s) And now you too can have better PRs impress your coworkers by having well-researched, effectively written, and lower-cost PRs.

[7:19:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26343s) With a comic.

[7:19:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26345s) With a comic.

[7:19:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26346s) So for more information, go to tracetune.com.

[7:19:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26349s) Learn about Trace2 and give it a try.

[7:19:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26351s) It works with Quad.

[7:19:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26352s) It works with Codex.

[7:19:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26353s) It works with all your favorite AI tools.

[7:19:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26355s) and if you want to do these same sort of amazing results

[7:19:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26358s) on your own project, try out Relate,

[7:19:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26361s) our new Rust-based embedded open source graph database,

[7:19:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26365s) which brings context to your agents

[7:19:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26367s) and helps you build more efficient applications

[7:19:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26369s) that just work better or cheaper

[7:19:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26372s) and give you better results.

[7:19:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26374s) So thank you all for joining our

[7:19:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26376s) AI Engineer San Francisco talk

[7:19:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26378s) and if you're watching this talk this week

[7:19:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26381s) at San Francisco,

[7:19:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26383s) what should you do this weekend with your kids on Saturday, Cassandra?

[7:19:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26388s) We are running an AI Engineer Kids Day.

[7:19:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26391s) So anyone who's available, just sign your kids up.

[7:19:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26395s) We're teaching kids workshops.

[7:19:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26396s) Kids will be learning how to do AI programming to make their own

[7:20:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26400s) games.

[7:20:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26400s) And I think we're also doing a, no, it's just the gaming one.

[7:20:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26406s) No, we'll do the robots too.

[7:20:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26408s) Okay. Yeah, we'll also be doing robots. So kids will get to control these little soda can robots using AI.

[7:20:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26415s) Yeah. So a lot of fun. Physical AI, gaming AI, all in one place.

[7:20:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26421s) sign up at AI Engineer Kids Day

[7:20:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26423s) and bring your kids, bring your nieces, bring your nephews

[7:20:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26427s) and let's train the next generation of AI engineers.

[7:20:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=26432s) All right, thanks so much and enjoy the rest of the conference.
