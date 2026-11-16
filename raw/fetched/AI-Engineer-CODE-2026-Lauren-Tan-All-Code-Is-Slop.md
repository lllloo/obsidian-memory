---
title: All Code Is Slop (Except Mine) — Lauren Tan
description: AI Engineer CODE 2026 官方閱讀版，Lauren Tan 談把對 agent 的糾正寫進程式庫、lint 與驗證，附機器逐字稿
created: 2026-11-16
updated: 2026-11-16
source: https://ai.engineer/code/2026/talks/lauren-tan
published:
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 Grok Bot 被辨識成 Grabbot／Graphbot）。逐字稿對應 Day 1 直播 `https://www.youtube.com/watch?v=ZZ19zhYnDKY`；剪輯單場版另見 `https://www.youtube.com/watch?v=O_zcc6Xl12g`。

Day 1 livestream · [1:01:02–1:18:38 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3662s). The player starts and stops at this session’s boundaries.

## Introduction

When an agent makes the same mistake again, it is tempting to add another warning to `AGENTS.md`. Lauren Tan wants the correction to land somewhere harder to ignore: the codebase, an API, or an executable check.

She opens with the experience of shipping thousands of pull requests after months of investment in the environment around her agents. Volume is the provocative result. The actual subject is trust: how to increase the amount of generated code without multiplying the defects that people must catch afterward.

[1:03:09 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3789s)

## Put the strongest constraints in the code

Tan's [trust pyramid](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3789s) puts codebase design and static analysis ahead of prose instructions. Good interfaces, clear architecture, refactoring, lint rules, types, and tests constrain what an agent can produce. Verification adds evidence about behavior. Written rules are useful for judgment that cannot be encoded more directly.

[![The source trust pyramid places codebase and static analysis above verification, prose, and human review.](https://ai.engineer/reading/code-2026/images/lauren-tan-3835.jpg)](https://ai.engineer/reading/code-2026/images/lauren-tan-3835.jpg)

*At [01:03:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3835s), the pyramid shows where Tan wants repeated corrections to move: toward reusable constraints rather than recurring human intervention.*

The codebase is also one of the agent's largest inputs. A workaround that remains in the repository becomes an example for the next change. A deprecated pattern can spread because it looks like the established way to solve the problem.

Tan uses a garden analogy. When code arrived a few pull requests at a time, a reviewer could inspect much of the new growth. When hundreds of agents produce a stream of changes, the structures around that growth matter more. Cleaning up old examples is part of improving future output, not merely paying down historical debt.

[1:06:17 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3977s)

## Eliminate a class of mistake instead of reviewing it forever

The [Dune framework example](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3977s) makes this concrete. Tan describes a desktop client framework with constraints learned from building Electron applications. Some APIs require too much nuance to be a safe default in ordinary product code.

Her team restricts React's `useEffect` to selected framework internals rather than asking every agent to use it perfectly. The framework provides the supported path; a check rejects the inappropriate alternative. That is a local architecture choice, not a claim that the hook is universally wrong.

The next example concerns Electron's process split. Importing main-process code into renderer code can create work in the wrong place and hurt responsiveness. Tan describes explicit `electron-main` and `electron-renderer` directories, with dependency analysis and lint rules forbidding imports across the wrong boundary. Directory names communicate the design, while executable checks enforce it.

These restrictions buy back review attention. Once a whole class of invalid change is rejected mechanically, the reviewer no longer needs to rediscover it in every pull request.

[1:11:00 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4260s)

## Review behavior and evidence, not only the diff

At [01:11:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4260s), the discussion moves from preventing invalid code to verifying the code that remains. Tan describes reviewing artifacts such as videos, screenshots, diagrams, and formal-verification results.

Runtime verification starts with something practical: let the agent run the application and use debugging tools. A feature map names the application from the user's point of view, so a request about a sidebar does not depend on the agent guessing which control the person means. Reusable command-line tools and drivers give agents a consistent way to operate the app and give the team something testable to maintain.

The team is also experimenting with model checking, proofs for selected algorithms, and property-based UI testing. Tan presents those as additional layers, not a silver bullet. A statechart helps a reviewer inspect which user-visible states exist and what transitions are allowed; a screenshot of one successful state cannot show that by itself.

Her economic argument is that these techniques were often expensive to create and maintain by hand. Agents can lower that cost, making deeper verification practical on more of the product. The result is not that verification disappears. More of the budget goes into it.

[1:17:45 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4665s)

## Automate the outer loop after improving the inner one

Tan reports that her team shipped roughly 11,000 pull requests in the previous month, with a relative revert rate around half a percent and improvements in several client performance measures. These are her team's reported outcomes, not a controlled experiment proving that every repository will improve as merge volume rises.

The order of operations is the transferable part. Improve the code agents learn from. Make constraints executable. Give agents a strong way to test behavior. Only then expand the automation that repeatedly invokes them.

Near the [end of the talk](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4665s), Tan describes a release routine that starts a project to fuzz the application, opens fixes for discovered bugs, and can automatically merge them. That level of autonomy rests on the environment built earlier. Adding an outer loop to an unreliable inner loop would generate more unreliable work.

A factory does not rescue a bad process by running it faster. In Tan's version, the factory becomes possible because the recurring mistakes have been designed out, rejected automatically, or exposed by verification before a person has to find them again.

Full transcript 441 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[1:01:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3662s) Hello everyone.

[1:01:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3664s) Don't know if you can see my slides, but

[1:01:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3666s) uh my name is Potato, also known as

[1:01:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3669s) Lauren, and I'm very excited to chat

[1:01:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3671s) with all of you today. Maybe you can get

[1:01:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3673s) a big round of applause for our tech

[1:01:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3675s) team helping me with my laptop.

[1:01:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3677s) \[applause\]

[1:01:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3684s) Good.

[1:01:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3687s) I don't see it.

[1:01:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3694s) >> Ah, there you go.

[1:01:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3697s) All right. Um, so again, I'm my name is

[1:01:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3700s) Potato. Uh, I work on Grabbot at

[1:01:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3703s) SpaceXsi.

[1:01:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3705s) And can I just get a quick show of

[1:01:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3706s) hands? How many of you have ever looked

[1:01:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3709s) at code that somebody else wrote and you

[1:01:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3712s) thought that's all slap?

[1:01:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3714s) >> \[laughter\]

[1:01:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3715s) >> Well, I have too,

[1:01:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3719s) but today I'm going to convince you that

[1:02:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3720s) you can turn that slop into gold.

[1:02:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3726s) Uh, and so I did something crazy last

[1:02:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3728s) month and I shipped 3,000 ploy crust to

[1:02:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3731s) production. Now, before agents, we never

[1:02:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3734s) really cared about volume. Uh, except

[1:02:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3736s) for the outliers.

[1:02:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3738s) And at my previous company, we called

[1:02:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3740s) these people coding machines. people

[1:02:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3742s) like Brett Taylor who famously rewrote

[1:02:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3744s) all of Google Maps uh in the weekend

[1:02:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3747s) just an insanely productive engineer. Uh

[1:02:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3750s) and well with agents anyone can now be a

[1:02:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3752s) coding machine. And my thesis is that

[1:02:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3755s) the job of a software engineer the meta

[1:02:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3757s) of being a software engineer is figuring

[1:02:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3759s) out how to maintain or even improve the

[1:02:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3762s) quality of your code while massively

[1:02:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3764s) increasing your productivity.

[1:02:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3767s) To get there, some people like to call

[1:02:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3769s) this a software factory. Uh, but I like

[1:02:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3771s) to keep it simple and I think of it as

[1:02:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3774s) all about trust.

[1:02:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3776s) Not blind trust, but investing in your

[1:02:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3779s) agents environment so you can trust that

[1:03:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3781s) your agents are going to do the right

[1:03:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3783s) thing. Now, it takes quite a lot of

[1:03:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3786s) effort to get there. Um, and it took me

[1:03:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3789s) six months to get to a point where I

[1:03:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3791s) could ship thousands of pull requests, a

[1:03:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3793s) lot of them in my sleep, but it's

[1:03:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3795s) certainly possible and it will take you

[1:03:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3798s) much less time than I did. So let's

[1:03:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3800s) start by talking about how we move from

[1:03:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3802s) a low trust environment to a high trust

[1:03:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3805s) one.

[1:03:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3807s) So this inverse pyramid is how I think

[1:03:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3809s) about where to spend time on your agents

[1:03:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3812s) environment.

[1:03:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3814s) The first two layers are deterministic.

[1:03:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3816s) So using your code itself. So things

[1:03:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3818s) like good API design, architecture,

[1:03:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3821s) refactoring or using lint rules, type

[1:03:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3824s) systems, compilers or you know different

[1:03:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3826s) kinds of testing. And you can use both

[1:03:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3829s) of these layers together to constrain

[1:03:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3831s) what agents can do and force them to do

[1:03:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3834s) the right thing by default.

[1:03:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3836s) Verification, both runtime and formal,

[1:03:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3839s) are great tools to layer on to find bugs

[1:04:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3842s) and check properties and the invariance

[1:04:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3844s) in your system that you want to hold

[1:04:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3845s) true and also help you check whether or

[1:04:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3848s) not the agent understood your goals and

[1:04:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3850s) your intent.

[1:04:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3852s) And then finally, you want to layer with

[1:04:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3854s) a little bit of pros. So things like

[1:04:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3856s) rules, skills, agents.mmd, things that

[1:04:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3860s) require judgment.

[1:04:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3863s) But let's start with your codebase.

[1:04:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3865s) Agents generate their outputs based on

[1:04:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3867s) their inputs. And so the the quality of

[1:04:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3870s) the input really matters. And it just so

[1:04:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3872s) happens that your codebase is one of the

[1:04:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3874s) largest inputs. So whenever you're

[1:04:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3877s) correcting your agent, think about how

[1:04:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3879s) you can make that a deterministic check

[1:04:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3881s) instead of adding another line to your

[1:04:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3883s) rules or your agents.mmd because it's

[1:04:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3886s) far more reproducible when it's in code

[1:04:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3888s) and it lets you trust it more.

[1:04:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3891s) And the analogy that I like to use is

[1:04:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3893s) that your codebase is kind of like a

[1:04:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3895s) garden. You know, code used to arrive a

[1:04:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3898s) few pull requests at a time. And uh I

[1:05:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3901s) remember going into work in 2024 and

[1:05:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3904s) reviewing the three pull requests that

[1:05:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3906s) my colleagues wrote colleagues wrote and

[1:05:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3908s) today that number is more like 300. So

[1:05:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3912s) uh you know every engineer is now a team

[1:05:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3914s) of hundreds or even thousands of agents

[1:05:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3917s) and code is arriving so rapidly that it

[1:05:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3920s) almost feels like a continuous stream

[1:05:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3922s) and it almost feels organic like a

[1:05:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3925s) living thing.

[1:05:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3927s) And in this analogy, your codebase, the

[1:05:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3930s) constraints that you impose, the

[1:05:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3932s) guardrails that you put up are the

[1:05:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3934s) concrete foundations that the new code

[1:05:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3936s) that your agents write grow around just

[1:05:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3939s) like uh the building in this picture.

[1:05:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3942s) And so in many ways, the job of being a

[1:05:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3943s) software engineer is kind of becoming

[1:05:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3945s) like gardening

[1:05:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3948s) because code is the biggest input for

[1:05:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3950s) agents. It means that any workarounds um

[1:05:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3954s) anti-atterns deprecated code tech is now

[1:05:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3958s) likely to be just copied by the next

[1:05:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3959s) agent since it looks like the

[1:06:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3961s) established pattern in your codebase and

[1:06:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3964s) uh it's like you have some weeds or

[1:06:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3967s) pests growing in your garden and then

[1:06:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3969s) they spread everywhere before you know

[1:06:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3971s) it.

[1:06:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3975s) So you want to make your codebase as

[1:06:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3977s) pristine as possible so that agents are

[1:06:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3979s) always copying the good stuff. All

[1:06:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3982s) right, let's look at some real examples.

[1:06:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3984s) Uh so Dune is a client framework that we

[1:06:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3987s) created for graphbot to implement this

[1:06:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3989s) idea for organic architecture.

[1:06:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3992s) It's not really that interesting

[1:06:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3993s) technically. Uh you can kind of think of

[1:06:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3995s) Dune as um kind of like Nex.js for

[1:06:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=3998s) Electron apps. But the interesting part

[1:06:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4000s) of Dune is that it has a lot of

[1:06:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4002s) constraints and lit rules that we've

[1:06:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4004s) encoded uh a lot of the lessons that

[1:06:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4006s) we've learned building desktop

[1:06:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4008s) applications.

[1:06:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4010s) And one such lesson is that anything

[1:06:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4012s) that requires nuance to use well often

[1:06:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4015s) leads to slop. Uh you know your classic

[1:06:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4018s) example is uh you know use effect in

[1:07:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4020s) React, right? It has its use cases uh

[1:07:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4023s) but it's often misused. You know some

[1:07:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4025s) people joke that you need a PhD to use

[1:07:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4027s) use effect. Um and in in other words, it

[1:07:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4030s) really requires a lot of nuance to use

[1:07:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4033s) ball and agents are not good at using

[1:07:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4035s) it. Um so our solution has been to just

[1:07:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4039s) ban it in product code and it's really

[1:07:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4041s) only allowed in some places inside of

[1:07:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4044s) Dune APIs

[1:07:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4046s) and effectively this problem has now

[1:07:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4048s) been categorically eliminated and we

[1:07:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4051s) never need to catch that during code

[1:07:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4052s) review again.

[1:07:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4054s) Another interesting pattern that we use

[1:07:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4056s) is context through directory structure.

[1:07:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4059s) Uh so one antiattern that we saw with

[1:07:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4061s) cursor which is an electron app is that

[1:07:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4064s) agents would often import main thread

[1:07:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4066s) code into the renderer thread which

[1:07:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4068s) would cause long tasks and jank.

[1:07:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4072s) So in uh grapot and in dunes we've made

[1:07:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4075s) this very very conventional. Uh we have

[1:07:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4077s) these two top level directories

[1:07:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4079s) literally called electron renderer and

[1:08:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4081s) electron main and imports between them

[1:08:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4084s) are forbidden or banned by our

[1:08:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4086s) dependency graph analyzer and some lint

[1:08:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4089s) rules. And again you know these are

[1:08:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4091s) simple lint rules to set up but it means

[1:08:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4093s) one less thing that we need to review

[1:08:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4095s) and think about uh you know during code

[1:08:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4098s) review.

[1:08:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4100s) And then one more surprising thing that

[1:08:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4103s) I've seen is agents using markdown. So

[1:08:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4106s) things like documentation, uh, code

[1:08:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4108s) comments, rules or skills, and they use

[1:08:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4111s) this as a place to write down their

[1:08:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4113s) justifications for not doing the right

[1:08:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4115s) thing. Or, I don't know if you've ever

[1:08:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4117s) seen this, but they'll over rotate on

[1:08:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4119s) some small correction that you made, and

[1:08:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4121s) they treat it like a hard rule that can

[1:08:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4123s) never be broken ever again.

[1:08:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4126s) And here's another example from cursor.

[1:08:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4129s) So agents really loved using imperative

[1:08:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4131s) timers. So things like set timeout,

[1:08:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4133s) request animation frame, request idle

[1:08:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4135s) call back. And they were using these as

[1:08:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4137s) quick fixes because they were really

[1:09:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4140s) patching over an architecture clash

[1:09:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4142s) between uh VS Code's imperative style

[1:09:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4145s) and React's declarative style.

[1:09:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4148s) So our choice of architecture actually

[1:09:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4150s) made both the client and the agent

[1:09:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4153s) performance much worse. And if you've

[1:09:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4156s) ever done any performance work in

[1:09:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4157s) JavaScript, you'll know that when you

[1:09:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4158s) have tons of timers being rapidly

[1:09:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4160s) created and destroyed causes a lot of uh

[1:09:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4163s) major garbage collection, which causes a

[1:09:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4165s) lot of lag and jen. Uh but the worst

[1:09:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4168s) part is that agents wrote a lot of code

[1:09:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4170s) comments like you can see in red here

[1:09:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4172s) explaining why this quick fix was

[1:09:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4174s) justified and before you know it, we had

[1:09:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4178s) timers spreading everywhere and the you

[1:09:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4180s) know the performance of the app really

[1:09:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4182s) suffered.

[1:09:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4184s) Now in Grockbot uh we learned our lesson

[1:09:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4187s) there and we decided to just ban 99% of

[1:09:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4189s) comments uh because they go stale

[1:09:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4192s) easily. Uh you know humans just really

[1:09:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4194s) don't bother reading the comment slop

[1:09:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4196s) anyway. And again it gives an agent the

[1:09:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4199s) an escape hatch to justify not doing the

[1:10:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4202s) right thing because it's hard. Um and

[1:10:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4205s) the worst part about comments though is

[1:10:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4207s) that they're not enforcable. So what

[1:10:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4209s) seems well-intentioned, you know, like

[1:10:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4212s) I'm going to tell the the next agent not

[1:10:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4214s) to do something, never ends up actually

[1:10:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4216s) being anything that you can trust. So in

[1:10:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4220s) Grockbot and Dune and in Dune, uh we now

[1:10:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4222s) have lint rules that give uh good and

[1:10:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4225s) very helpful error messages telling the

[1:10:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4227s) agent to fix the root cause, the real

[1:10:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4230s) problem, uh rather than just patch

[1:10:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4232s) around it.

[1:10:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4234s) And so our general principle is that

[1:10:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4236s) every time we correct our agents, it

[1:10:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4237s) turns into one of these deterministic

[1:10:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4239s) checks or we think about how to

[1:10:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4241s) categorically eliminate that problem in

[1:10:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4243s) the code through better API design,

[1:10:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4245s) through better uh architecture. And if

[1:10:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4248s) you do this enough times, you'll find

[1:10:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4250s) that you have just less things to look

[1:10:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4253s) out for in code review. And at some

[1:10:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4255s) point, you'll realize there's there's

[1:10:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4257s) nothing left to review, and you can just

[1:10:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4259s) let agents merge their most of their own

[1:11:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4261s) pull requests.

[1:11:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4264s) All right. Uh, moving on. Verification

[1:11:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4267s) is also a really big part of how we make

[1:11:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4269s) our agents more autonomous and also

[1:11:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4272s) increase our confidence and trust in

[1:11:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4273s) their work. And our code review process

[1:11:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4276s) has now really shrunk into looking at

[1:11:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4278s) verification artifacts instead. So

[1:11:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4280s) things like videos, screenshots,

[1:11:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4282s) diagrams, formal verification.

[1:11:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4286s) Um, and the most basic example of this

[1:11:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4288s) is runtime verification. uh which is

[1:11:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4290s) just a fancy way of saying giving your

[1:11:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4292s) agent a way to run the code for itself

[1:11:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4294s) and use debugging tools that you know

[1:11:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4296s) human developers use as well like the

[1:11:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4298s) Chrome DevTools protocol. Um in our

[1:11:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4301s) runtime verification skills we have this

[1:11:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4303s) thing that we call a feature map and

[1:11:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4305s) that's basically kind of like a site map

[1:11:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4308s) of all of the features that are

[1:11:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4309s) available in your application from the

[1:11:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4311s) user's point of view. And so with this

[1:11:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4314s) agents don't need to guess when you say

[1:11:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4316s) you know the thingy in the left sidebar.

[1:11:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4318s) It gives you some shared vocabulary

[1:12:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4321s) and we also make use of custom CLIs

[1:12:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4323s) inside these skills so that uh agents

[1:12:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4326s) can reuse the the CLI and the driver

[1:12:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4329s) every time which cuts down on token

[1:12:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4330s) usage and is also testable.

[1:12:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4334s) Um and then recently we've also started

[1:12:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4336s) looking at formal verification. Uh so we

[1:12:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4339s) now use TA plus to do some model

[1:12:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4341s) checking of major user flows such as uh

[1:12:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4343s) notifications across multiple devices

[1:12:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4345s) and platforms. Uh we use a lean as well

[1:12:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4348s) for proving certain algorithms. Uh for

[1:12:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4350s) example, we have our own we wrote our

[1:12:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4352s) own custom virtualization library and we

[1:12:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4354s) use lean there to check that we don't

[1:12:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4356s) have you know flickering or jittering

[1:12:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4358s) problems. Um and we're still

[1:12:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4360s) experimenting with this approach.

[1:12:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4362s) Overall it seems very promising. Uh

[1:12:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4364s) we've already found quite a few bugs uh

[1:12:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4366s) with formal verification.

[1:12:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4369s) uh but it's certainly not a silver

[1:12:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4370s) bullet and we're treating it as another

[1:12:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4374s) tool, another layer in our agents uh

[1:12:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4377s) environment.

[1:12:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4379s) Uh and then this is a very fast video

[1:13:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4381s) but uh another thing that we just

[1:13:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4383s) started looking at is property based

[1:13:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4385s) testing as well for UIs. Uh so we use

[1:13:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4387s) this library called Bombadil. Um and

[1:13:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4390s) this has also caught a few UI bugs for

[1:13:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4392s) us already.

[1:13:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4395s) Okay, so zooming out, I saw this tweet

[1:13:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4397s) from Cindy and six months ago she she

[1:13:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4400s) said that she was or she was talking

[1:13:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4402s) about not being able to trust her agents

[1:13:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4405s) because of subtle bugs that were getting

[1:13:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4407s) merged.

[1:13:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4409s) And really what was missing for her in

[1:13:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4410s) being able to trust her agents was the

[1:13:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4412s) verification process. And now 6 months

[1:13:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4415s) later, she says that 70% of her daily

[1:13:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4417s) tokens go into verification. And I'd say

[1:13:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4420s) that that tracks with what I see as

[1:13:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4422s) well, that most of my token usage goes

[1:13:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4424s) to verification.

[1:13:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4426s) And if you really look closely at our

[1:13:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4427s) process, none of these things here are

[1:13:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4430s) new or novel techniques that we've never

[1:13:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4432s) had before.

[1:13:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4434s) These are just good software engineering

[1:13:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4436s) tools, but ones that might have been

[1:13:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4438s) prohibitively expensive to use before as

[1:14:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4441s) they were hard to understand or write or

[1:14:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4443s) maintain. But agents drastically cut

[1:14:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4446s) this cost down. And really, we're

[1:14:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4448s) entering a golden age of software

[1:14:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4450s) testing and verification because agents

[1:14:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4452s) let us test everything to a much greater

[1:14:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4454s) degree than used to be economical.

[1:14:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4458s) And then formal verification can also

[1:14:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4460s) help you better reason about how your

[1:14:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4462s) product should work and whether your

[1:14:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4463s) agents really understand your intent and

[1:14:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4465s) goals. Uh I made this new skill called

[1:14:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4468s) state chart uh in my plug-in PAC potato

[1:14:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4471s) stack uh which helps you visualize state

[1:14:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4473s) machines from uh from the user's point

[1:14:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4476s) of view. Uh, and it's I find this much

[1:14:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4478s) easier to review alongside the videos

[1:14:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4480s) and screenshots that we provide. Um, and

[1:14:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4483s) so that's been great. Sorry for the

[1:14:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4485s) flashbang. Uh, okay. Now, let's look at

[1:14:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4488s) what the promised land looks like. What

[1:14:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4491s) do you get in return for all of this uh,

[1:14:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4493s) you know, investment?

[1:14:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4496s) So, on the graphbot team, our velocity

[1:14:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4498s) is uh, taking off and rapidly

[1:15:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4500s) increasing. And last month, our team

[1:15:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4502s) shipped a ridiculous 11,000 pull

[1:15:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4506s) requests to production, which is a wild

[1:15:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4508s) number. And our pace of releasing the

[1:15:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4512s) client has also increased. And we cut a

[1:15:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4514s) new stable version about once a day.

[1:15:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4518s) And then the core team is also shipping

[1:15:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4520s) much more. And we also have uh a lot

[1:15:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4522s) more casual or driveby contributors who

[1:15:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4525s) don't always have a lot of context uh

[1:15:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4528s) but they're also contributing. Um, and

[1:15:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4530s) in October we had about 227 people who

[1:15:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4534s) contributed at least one pull request.

[1:15:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4538s) So despite this velocity accelerating,

[1:15:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4540s) you might be thinking to yourself like,

[1:15:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4541s) isn't this going to be chaos? You know,

[1:15:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4543s) isn't this going to be a bunch of slop?

[1:15:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4545s) But actually, the number of uh PRs that

[1:15:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4547s) get reverted has actually gotten lower

[1:15:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4549s) on a relative basis and is steady at

[1:15:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4551s) about half a percent.

[1:15:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4554s) But I think the really interesting thing

[1:15:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4556s) about this shipping pace and this volume

[1:15:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4558s) of pull requests is that the performance

[1:16:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4562s) of Grathbot has stayed not just stable

[1:16:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4564s) but has improved on multiple dimensions

[1:16:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4566s) compared to when we launched. So startup

[1:16:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4569s) typing, opening new chats, switching

[1:16:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4572s) chats, all of this has gotten faster and

[1:16:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4575s) keep in mind Grathbot is still an

[1:16:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4577s) Electron app for now. Uh so there is a

[1:16:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4580s) ceiling, right? But it's already much

[1:16:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4582s) faster than many other agent UIs out

[1:16:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4585s) there. And for an Electron app with this

[1:16:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4589s) high velocity and this many people

[1:16:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4591s) contributing, I'd say that's pretty

[1:16:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4593s) good.

[1:16:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4595s) So before you jump into building out a

[1:16:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4597s) software factory and you know automating

[1:16:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4599s) everything that you can, whenever you

[1:16:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4601s) correct your agent, try and do it by

[1:16:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4603s) improving your codebase first. you know,

[1:16:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4605s) start with a lint rule to prevent new

[1:16:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4607s) occurrences of anti-atterns and then

[1:16:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4609s) clean up those uh old patterns as well

[1:16:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4612s) and then make sure that your

[1:16:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4613s) verification story is really strong.

[1:16:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4616s) A lot of this work is a prerequisite to

[1:16:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4618s) automation anyway. And if your inner

[1:17:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4621s) coding loop uh produces slop, then

[1:17:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4624s) automating that loop just produces more

[1:17:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4626s) slop and you need to throw more and more

[1:17:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4628s) and more tokens at the problem, which we

[1:17:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4630s) all know is very expensive.

[1:17:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4633s) And once you've made these investments

[1:17:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4634s) into, you know, code into your codebase,

[1:17:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4637s) static analysis, runtime informal

[1:17:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4639s) verification, you'll start to find that

[1:17:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4641s) many things become possible with these

[1:17:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4644s) foundations and that you can really

[1:17:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4646s) easily build your own factory on top of

[1:17:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4648s) these foundations.

[1:17:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4651s) And when you're ready, Grabbot is a

[1:17:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4652s) great way to build that uh outer loop.

[1:17:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4654s) We have tons of connectors, routines

[1:17:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4656s) that can kick off cursor cloud agents

[1:17:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4658s) and projects uh which let you

[1:17:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4660s) orchestrate thousands of hundreds or

[1:17:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4663s) even thousands of agents. And as a quick

[1:17:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4665s) example, you know, whenever we cut a new

[1:17:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4667s) release now, Grockbot will automatically

[1:17:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4669s) spin up a new cursor project for us that

[1:17:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4672s) will fuzz the entire application, the

[1:17:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4674s) entire build, and it will find bugs uh

[1:17:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4676s) by running the app and using it like a

[1:17:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4678s) real user. And then it's going to open

[1:18:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4681s) fixed PRs for each of those bugs that it

[1:18:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4683s) finds and it's going to automerge it as

[1:18:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4685s) uh crazy as that sounds. And that's

[1:18:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4688s) because our code base is good enough

[1:18:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4690s) that pull requests tend to just be good

[1:18:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4692s) by default. And most product code that

[1:18:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4694s) we land no longer really requires deep

[1:18:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4696s) human review.

[1:18:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4700s) So when you have solid foundations and

[1:18:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4703s) good organic architecture, you can turn

[1:18:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4705s) slop into gold and you can ship with

[1:18:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4708s) high quality uh high velocity without

[1:18:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4711s) compromising on quality. My name is

[1:18:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4713s) Potato, also known as Lauren. Thanks you

[1:18:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=4716s) again for listening to my talk.
