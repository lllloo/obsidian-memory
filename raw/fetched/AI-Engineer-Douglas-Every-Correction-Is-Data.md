---
title: Every Correction You Give Your Agent Is Data — Brian Douglas
description: AI Engineer CODE 2026 官方閱讀版，Brian Douglas 談標記 agent session 的 pushback 並寫成 skill 或微調 reviewer，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-brian-douglas
published: 2026-11-12
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（官方註明為機器產生、保留辨識錯誤；可見例子如 Claude Code 被辨識成 Cloud Codes／Quadco、Qwen 被辨識成 Quinn／Quintin、Addy Osmani 被辨識成 Addy Osmone／Adios Mani）。逐字稿對應 Day 2 直播 `https://www.youtube.com/watch?v=y9JtCCZP2MQ`（YouTube 影片 ID `y9JtCCZP2MQ`，本場約 1:59:06–2:11:53）。

Day 2 livestream · [1:59:06–2:11:53 on YouTube](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7146s). The player starts and stops at this session’s boundaries.

## Introduction

**Brian Douglas** shows how a teammate's corrections can become reusable review knowledge when the team records and labels agent sessions.

Douglas can ask an agent to write Rust, but he does not claim the same Rust judgment as his more experienced teammates. The code may compile and receive a positive automated review, then attract substantial pushback from a human who understands how the company wants its systems to fit together.

That gap gives the talk its practical question: how can the junior reviewer benefit from the corrections the senior reviewer has already made elsewhere?

[2:00:49 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7249s)

## Capture the repetitions that contain judgment

Douglas begins with a concern about learning. Engineers traditionally develop through repeated attempts and feedback. If agents perform more of those attempts, useful lessons can remain inside an interaction that only one person sees.

His starting point is session capture. At [02:00:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7249s), he introduces [Tapes](https://tapes.dev/), a tool for recording coding-agent telemetry. He also describes reproducible agent environments and parallel maintenance tasks, including documentation, tests, and cleanup. These generate many traces of the system attempting work and receiving feedback.

The choice of collector is secondary to the data it preserves. A local history is useful to one engineer; a shared collection can include the corrections made by the whole team. Douglas's argument depends on capturing the interaction, not merely saving the final diff.

[2:03:29 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7409s)

## Pushback identifies knowledge the agent missed

At [02:03:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7409s), Douglas filters sessions with a pushback label. He looks especially at corrections from a teammate, Matt, on Go and Rust work.

A correction can contain information the compiler does not enforce. The team may have chosen a particular API structure. An agent may duplicate an existing service, misunderstand how components should interact, or rebuild a library the organization already uses. The code can be syntactically valid while violating those decisions.

Douglas may not recognize these problems while the agent is generating a patch. He therefore wants the previous corrections available before he sends another pull request to the human reviewer. The valuable signal is the reason for the disagreement, not the intensity of the language used to express it.

This also explains why pull-request comments alone can be an incomplete dataset. As review moves into coding-agent terminals, the discussion that changes the implementation may never be posted on GitHub. Capturing only the repository's final artifacts loses some of the reasoning that made them acceptable.

[2:05:11 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7511s)

## A reviewer trained on one teammate's corrections

Douglas demonstrates TwinReview at [02:05:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7511s). He provides a pull-request number and asks for comments informed by the labeled traces of Matt's previous corrections. The demo combines trace collection, dataset construction, and post-training.

[![A terminal review distinguishes one patch hunk that merits a comment from several it would let pass.](https://ai.engineer/reading/code-2026/images/online-brian-douglas-7560.jpg)](https://ai.engineer/reading/code-2026/images/online-brian-douglas-7560.jpg)

*The [demo at 2:06:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7560s) focuses on a specific architectural misunderstanding rather than commenting on every hunk. The displayed confidence is the tool's own output, not an independently validated accuracy measure.*

The intended behavior is selective. A useful reviewer should identify the changes that conflict with the team's judgment and leave routine changes alone. Repeating general style advice on every patch would not capture the value of an experienced colleague.

Douglas initially calls the reviewer open source, then corrects himself during the talk: TwinReview had not been released because its data included sensitive information. That distinction matters. The trace-capture tool and the private reviewer are different artifacts, and the demonstration does not make the underlying team conversations public training material.

[2:07:22 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7642s)

## Start with a skill before paying for training

At [02:07:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7642s), Douglas broadens the useful labels. Pushback is one category; exemplary sessions, regressions, and other marked outcomes can also guide what a future agent should repeat or avoid.

He recommends a simpler starting point than immediately training a model. Extract the lessons into a skill, use it in the review harness, and create evaluations that test whether it changes the desired behavior. If that proves insufficient, the same evidence can support a more specialized model.

The order reduces ambiguity. A team needs to know which judgment it is trying to reproduce and how it will recognize success before deciding that fine-tuning is the right implementation. A well-written skill may deliver much of the benefit without adding a training pipeline.

Douglas discusses his experiments with smaller models and the compute constraints he encountered when trying other training approaches. Those are observations from his setup, not general limits on which model sizes can support a particular method. The practical recommendation remains to use the least expensive mechanism that reliably carries the team's knowledge into the next review.

The closing request is modest: when an interaction contains a valuable correction, preserve the session and label what happened. The team is already producing examples of good engineering judgment. Recording them makes it possible to teach that judgment instead of asking the same senior engineer to repeat it at every pull request.

Full transcript 187 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[1:59:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7147s) Thanks for coming to my talk.

[1:59:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7148s) I'm BDougie, Brian Douglas, and I'm going to talk about if you are going to verbally abuse your agents, at least label the outcome.

[1:59:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7155s) Now, this is a talk I'm going to quickly just run through one example, and this will be a short talk, mainly because there's actually not too much to this.

[1:59:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7164s) But outside of that, I want to talk about some of the work I've been doing for the past six to eight months.

[1:59:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7170s) And it actually came out with this idea early this year.

[1:59:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7173s) Everyone definitely got AI pilled when it comes to agents.

[1:59:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7176s) So obviously, Cloud Codes got to be one of the most popular ones out there.

[1:59:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7180s) We've got quite a few other ones that you can leverage, like the Codex or ChatGPT.

[1:59:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7185s) And there was a book I read years ago, well, quite a handful of years ago, from Rick Rubin about the creative act, a way of being.

[1:59:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7192s) And this was actually around the idea that Rick Rubin produced the BC Boys and a number of other acts, but he's actually never played music.

[2:00:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7200s) And a lot of folks have made this correlation with vibe coding, where Rick Rubin can produce the best music without actually playing the piano.

[2:00:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7208s) We're now having, we're in a world where folks can vibe code a bunch of Rust code without never writing Rust.

[2:00:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7215s) And that's exactly where I'm at.

[2:00:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7217s) There was another article months ago from Addy Osmone,

[2:00:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7221s) who's now currently at the Anthropic team,

[2:00:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7225s) the Quadco team specifically,

[2:00:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7227s) and was talking about the opportunity for juniors,

[2:00:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7231s) or basically it's gone.

[2:00:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7233s) When it comes to junior engineering,

[2:00:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7235s) it was all about growing from junior to senior was about reps.

[2:00:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7239s) So the more reps you got,

[2:00:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7240s) the more engagement you got opportunity to basically just level up as an

[2:00:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7244s) engineer.

[2:00:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7245s) and without those reps, we're handing those reps specifically to agents,

[2:00:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7249s) we're losing the opportunity to level up.

[2:00:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7252s) So this comes out of something I was doing early this year,

[2:00:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7254s) which built this open source project called Tapes.

[2:00:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7257s) Tapes.dev is open source Apache 2.

[2:01:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7260s) There's a lot of other similar stuff out there,

[2:01:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7262s) but what I'm getting at is it's not about Tapes.

[2:01:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7264s) It's about the idea of collecting your agent's session data,

[2:01:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7267s) and that's what this does.

[2:01:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7268s) So a lot of hotel collectors, a lot of session capture services,

[2:01:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7272s) a lot of the harnesses are to do this for you out of the box.

[2:01:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7274s) I just want to mention that this is what I use.

[2:01:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7277s) You can use anything else you would like.

[2:01:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7279s) I've also, in addition to tapes, me and my team, we've developed this thing called stereos,

[2:01:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7283s) and this is the runtime for your agent.

[2:01:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7285s) Again, sandboxes, not a concept that everyone needs to hear about today,

[2:01:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7290s) but just knowing that in all the work I've been doing, I've been capturing these sessions

[2:01:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7294s) and recording them by having a reproducible environment.

[2:01:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7299s) And the environment themselves, they have these signals.

[2:01:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7302s) sin. The one thing I've been doing it with these, this little setup of tapes and stereos is I've

[2:01:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7307s) been building self-healing infrastructure. So this is a little project called Sweeper Agent

[2:01:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7311s) and Sweeper Agent itself is a way for me to build parallel agents. I can scale up to 10 about 10

[2:01:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7317s) of these at this point. I've done quite a few like Daytona sandboxes as well. I've done like

[2:02:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7322s) about 200 at the same time that will just solve a specific problem. So documentation, test writing,

[2:02:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7327s) code cleanup stuff that you want to scale that's like very very defined work that you want to spin

[2:02:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7333s) off to multiple agents in tandem now a lot of this has been cleaning up most of my vibe coding

[2:02:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7340s) software that i built in the last 18 months at this point but just pointing out that like there's

[2:02:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7346s) a lot of work we can do to basically solve these problems but it doesn't change the fact that i

[2:02:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7352s) still don't know how to write rust code i've never written write rust code specifically myself

[2:02:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7357s) professionally rather.

[2:02:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7359s) Ten years ago, I did write Rust code,

[2:02:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7360s) but it was mostly for little side projects to learn Rust.

[2:02:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7363s) But we use Rust day-to-day at the company I work for,

[2:02:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7366s) which is Paper Compute.

[2:02:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7367s) And what we've been doing is,

[2:02:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7369s) because of this technology underneath this called Tapes,

[2:02:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7372s) we've been capturing traces.

[2:02:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7374s) And Tapes is our trace capture service.

[2:02:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7377s) Telemetry capture and paper, we have a console.

[2:02:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7379s) So for the moment, I'll move away from the slides

[2:03:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7382s) and show you the paper console.

[2:03:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7384s) Now, paper console itself,

[2:03:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7385s) just showing that I can capture sessions.

[2:03:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7387s) The difference of doing this local and my own sessions

[2:03:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7390s) is that I can have a centralized data store

[2:03:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7393s) of not just me but also my teammate.

[2:03:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7395s) And what's cool about this is I can also label sessions.

[2:03:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7398s) So this is a session that...

[2:03:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7402s) Oh, interesting.

[2:03:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7403s) Yeah, sorry.

[2:03:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7404s) I've got to zoom out to see the labels.

[2:03:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7406s) But yeah, so here I can see I've got a session here

[2:03:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7409s) which is working with some paper cloud export memory limits

[2:03:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7412s) and we've got this label called pushback.

[2:03:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7414s) Now, I actually went to specifically a session that had pushback in it, and it's specifically every time an engineer pushes back on the agent.

[2:03:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7423s) Now, there's a thing that I think recently Anthropic, or I guess rumors, I don't know if this is actually grounded by any facts, but Anthropic was pushing back on if you're being rude to the agent, you could potentially lose your account or get blocked.

[2:03:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7438s) but what I find specifically when pushed back when I'm specifically looking for any Rust code

[2:04:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7445s) or Go code that Matt has written and whenever he pushes back it's a good signal that he has

[2:04:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7451s) knowledge that the agent does not and this usually comes in the form of we have decided our API

[2:04:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7457s) structure a certain way despite the fact that the Rust code compiler compiles we have made decisions

[2:04:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7462s) on how that code should be set up and how that code should interact with different parts of the

[2:04:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7466s) code base also pushing back on things like duplicating uh services that made the agent

[2:04:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7471s) didn't have context around there's a lot of other like a bunch of reasons but what i'm getting at

[2:04:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7476s) me as like quote unquote a junior rust engineer i don't have enough context to be able to push

[2:04:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7482s) back to the agent to say hey you're doing this wrong or you're making like weird choices

[2:04:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7485s) i usually take everything that the agent writes in rust for face value and what that ends up

[2:04:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7490s) turning into is when i open up pr i get a lot of pushback from the engineers the human engineers

[2:04:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7495s) at review time. This is mainly because we know I don't write rest code. There's not a lot of

[2:05:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7500s) pushback I can provide to the code base or even at the time of review. So by the time it gets to

[2:05:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7505s) greptile, it's a five out of five review. I just let it slide. So how do I prevent that pushback?

[2:05:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7511s) What I've done is actually started collecting every single one of these labels and the traces.

[2:05:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7515s) And then one thing I'll point out is that the console itself, I capture every single session.

[2:05:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7521s) I've got all the specific details.

[2:05:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7523s) This is actually just a command line version of that.

[2:05:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7526s) What I've been doing is I've been capturing all these sessions

[2:05:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7529s) and then dropping into a data set that's been labeled.

[2:05:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7532s) So now I can just run a little command line tool called TwinReview,

[2:05:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7536s) and then I'll grab a PR number, 381, and I'll run that.

[2:05:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7541s) And I'll actually run through and essentially review the code as if it was Matt.

[2:05:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7546s) Now, the way I'm doing this is I'm capturing traces.

[2:05:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7548s) I created the data set.

[2:05:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7549s) I've also done some post training.

[2:05:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7551s) and this is like where, you know, choose your own adventure,

[2:05:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7554s) but I've done some post training specifically

[2:05:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7556s) on every time Matt pushes back within Go or Rust code

[2:06:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7560s) and I asked for it to provide me comments

[2:06:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7563s) as a viewer, Matt, on my GitHub PR.

[2:06:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7566s) So this is all data.

[2:06:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7567s) It's only specifically within the traces.

[2:06:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7569s) So this is not taking any GitHub PR review data,

[2:06:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7571s) which I think you potentially could also follow that pattern.

[2:06:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7574s) But what I find is like the majority of our team

[2:06:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7577s) have started reviewing code on the command line.

[2:06:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7580s) So you'll have Claude review the code or the PyHarness review code, or you review this PR, but you don't do a lot of pushback or a lot of commentary on GitHub itself.

[2:06:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7589s) So what we're seeing right now, we're shifting from code being reviewed specifically on GitHub by agents, well, previously humans and now agents, to now codes is specifically just getting reviewed in your harness without any sort of oversight or commentary or anything that sort of navigates directly to your shared code base.

[2:06:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7610s) So with that being said, like what I've navigated is I've created this thing called a twin reviewer.

[2:06:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7615s) And this as well is open sourced.

[2:06:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7619s) So it is, and I did not have this open, but, oh, actually, TwinReview is not open source.

[2:07:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7626s) I realize I never open source it because I got sensitive data.

[2:07:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7630s) But what I've done is actually set up that same pattern using Fireworks and using Fireworks to post-train specifically.

[2:07:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7636s) And what's cool about this is, like, I've looked for any sort of pushbacks, apologies, any sort of golden sessions,

[2:07:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7642s) sessions that actually have been marked as you should probably pay attention to this and also

[2:07:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7648s) regressions for any things that usually agents will just fall over. A lot of times it turns into

[2:07:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7653s) like an agent will start reinventing Go libraries that already exist. That usually is granted to be

[2:07:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7660s) pushed back. Ideally, you should push back on that. But again, if you don't know these libraries

[2:07:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7664s) exist, you probably just take it for face value and then you're reinventing things like Kubernetes,

[2:07:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7668s) which sounds like an overstatement, but we've seen it reinvent things like mock libraries for testing, etc.

[2:07:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7676s) And very popular code base, or very popular open source projects.

[2:08:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7680s) So that's essentially it.

[2:08:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7681s) This is basically, if you're going to push back and you're going to have some really, really valuable insight under reviews in your code base,

[2:08:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7689s) my recommendation is take a look at opportunities within the traces to maybe train or post-train a model or create your own harness for reviews locally.

[2:08:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7700s) Choose your own adventure. I think you could actually do a lot of this by just building your own harness.

[2:08:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7704s) But if you did want to use a Quinn 3-8B, which I've done specifically in this situation, you'd also approach that.

[2:08:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7712s) A lot of the stuff is available to you, a lot of tools.

[2:08:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7715s) What I did actually to start is I started taking the paper traces and creating skills.

[2:08:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7720s) Skills that I can then specifically do things like check the tapes.

[2:08:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7724s) So if you have a database, which tapes specifically is a Postgres database local on my machine.

[2:08:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7729s) So you don't have to use the paper console.

[2:08:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7731s) Actually, paper console is currently waitlisted.

[2:08:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7733s) So probably best use case is going to use something like tapes or a brain trust or something similar to capture your traces.

[2:09:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7741s) And then what's cool about this is once you have skills, you can create evals.

[2:09:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7744s) Once you have evals, you can start post training on a Quinn model and for specific reasons,

[2:09:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7750s) for identifying if rush code is up to speed to how you're writing code across your organization.

[2:09:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7757s) So I did write a blog post around training a model instead of writing a skill.

[2:09:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7760s) My recommendation is probably write a skill first.

[2:09:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7762s) You can probably get most mileage out of a skill today.

[2:09:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7768s) and I specifically across my team we had about almost 80,000 sessions that we could create

[2:09:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7774s) skills from which is pretty cool. Cool thing about this is also you do specialized fine tuning or

[2:09:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7778s) direct preference optimization. The latter is going to take a lot more compute or a larger

[2:09:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7783s) some large hardware to do that so probably specialized fine tuning. If you know about

[2:09:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7787s) QuickQ or that's how I'm doing this I'm quantizing it on smaller GPUs like a 5090

[2:09:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7793s) and if you don't know about specialized fine-tuning this is like writing notes in the

[2:09:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7797s) margin of a book if your book is your model the notes in the

[2:10:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7800s) margin are your weights or your adapters, rather.

[2:10:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7803s) So the weights you generate on top of the model that's already been pre-trained. Cool. And I did this, as you saw, on a Quintin 4B model. It works pretty good.

[2:10:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7813s) I did try to do this on some larger models so specifically for direct preference optimization

[2:10:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7820s) it took a lot of compute the only time I could make this work is by using NVIDIA GPUs on the

[2:10:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7826s) Brev service or actually I never got access to some of the stuff on Fireworks so I only did

[2:10:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7832s) smaller six thousands but if you if you care to know direct preference optimization if the margin

[2:10:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7840s) notes are your specialized fine-tuning dpo is going to be like your cliff notes uh not not

[2:10:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7846s) possible doing a small language model or a small 4b model uh you would need like 70b plus uh which

[2:10:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7852s) is going to take some hardware uh me specifically i didn't have any as hardware local so i had to use

[2:10:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7857s) um the services that i mentioned fireworks and well not even fireworks brev was the only one i

[2:11:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7862s) can get access to at the time good luck if you can get access to larger uh well you got to prepay a

[2:11:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7868s) for this stuff.

[2:11:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7869s) So best of luck on that one.

[2:11:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7871s) But my suggestion is create skills.

[2:11:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7873s) Try out tapes.dev if you're interested

[2:11:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7875s) or leverage the tool that you have at year already.

[2:11:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7878s) And reminder, you should probably read this book.

[2:11:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7882s) This is a great book if you think about, you know,

[2:11:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7884s) how we're looking forward into,

[2:11:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7886s) how we're approaching this world

[2:11:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7887s) when it comes to AI and vibe coding

[2:11:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7889s) and leveraging agents to basically build your software factory.

[2:11:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7893s) And I do recommend, please check out Adios Mani's blog post.

[2:11:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7897s) has a series of these on the X.

[2:11:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7899s) I think they're all great.

[2:11:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7900s) Definitely take a look at them.

[2:11:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7901s) He's got some clear-minded dots to check out.

[2:11:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7905s) I'm BDougie, and I do appreciate you watching this video.

[2:11:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7908s) I've tried to keep it brief because it was pretty straightforward.

[2:11:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7910s) Hopefully it was.

[2:11:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7911s) Cheers.
