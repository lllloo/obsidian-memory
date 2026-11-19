---
title: Beyond Better Assistants Software That Can Make a Decision — Diogo Almeida
description: AI Engineer CODE 2026 官方閱讀版，Diogo Almeida 談助理與自動化的差異、語意邏輯閘與 KV cache，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/diogo-almeida
published: 2026-11-11
tags:
  - clippings
  - ai-agent
  - automation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤；本檔所見如講者名被辨識成 Diego、Jev 被辨識成 Jeff／jeving、RLHF 被辨識成 RHF／Arlf）。官方閱讀頁場次名為〈Beyond Better Assistants: Software That Can Make a Decision〉，開場第一個主題為「where is all the automation」（vault 既有綜合頁以此稱呼本場），講者自述題目為「I love you so jevving much」。逐字稿對應 Day 1 直播 YouTube 影片 ID `ZZ19zhYnDKY`（`https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18418s`，5:06:58–5:29:53）；曾被推測的 `UCL4K36SHp0` 經 oEmbed 核對為 Brandon Thomas 場次，非本場。演講日 2026-11-11（Main stage）。

Day 1 livestream · [5:06:58–5:29:53 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18418s). The player starts and stops at this session’s boundaries.

## Introduction

A model can be impressive in a demo and still be unsuitable for unattended operation. Diogo Almeida makes that gap the center of his keynote. He likes the new tools; his objection is to treating a good assistant as if it were already a dependable automation component.

An assistant can hand its output to a human who interprets, corrects, and decides whether to use it. An automated process has to take the right action without that surrounding judgment every time. The second requirement is not merely the first requirement with a faster model.

Almeida's talk, titled “I love you so jevving much,” is both a critique of the current interface and an argument for different software primitives. It introduces his perspective on Jev, but much of the presentation concerns what engineers could build if intelligence were reliable enough to live inside ordinary control flow.

## Assistance and automation optimize different things

Almeida begins by questioning the distance between benchmark progress and changes in everyday automation. Human preference is useful when training a helpful assistant. It is not a complete specification for a machine making an unattended decision. A response can feel useful without being the correct action for a software system to take.

He attributes part of this mismatch to the emphasis on human-feedback training. That is his diagnosis, not a claim that every existing model or training method has the same limitation. He also acknowledges the attraction of verifiable rewards: some tasks give a system an objective signal of success. The difficulty is carrying that reliability into the messy decisions an application needs to make.

The familiar question is whether a model is smart enough. Almeida asks whether it was trained and evaluated for the right task. A model built to continue text, follow instructions, or satisfy a reviewer is not automatically optimized to be a dependable decision procedure embedded in software.

[5:12:00 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18720s)

## Choosing the task comes before scaling it

At [05:12:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18720s), he plays with the Bitter Lesson. Compute matters; data matters; but choosing the right task can matter before either. His point is not a new scaling law. It is a warning against spending more resources optimizing an objective that does not match the intended product.

Jev enters as an attempt to focus on the task of making useful machine-facing decisions, rather than simply presenting the same assistant through a cheaper or faster interface. Almeida's analogy is an assistant that is brilliant most of the time and disastrously foolish the rest. The percentages in the joke are not an error-rate measurement. The engineering problem is that a caller cannot safely automate a process if it cannot tell which kind of answer it has received.

This leads to a different product question. Instead of asking how to make the chatbot more impressive, ask which narrow decision a program needs, what evidence establishes that decision's quality, and whether the system can meet the reliability requirement at its point of use.

[5:18:20 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19100s)

## Just-in-time software is not the same as smart software

[![Traditional, just-in-time, and smart software compared](https://ai.engineer/reading/code-2026/images/diogo-almeida-19100.jpg)](https://ai.engineer/reading/code-2026/images/diogo-almeida-19100.jpg)

*The slide at [05:18:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19100s) distinguishes generating software with intelligence from inserting intelligence into the running software's structure.*

Almeida calls one direction just-in-time software: use a model to produce code more cheaply or when it is needed. That can change who builds software and how quickly, but the resulting application may still operate through conventional deterministic branches.

Smart software puts an intelligent operation inside the running application. A branch might depend on semantic intent, not only a field's literal value. A program might recognize whether something makes sense in context, instead of surrounding a conventional interface with a conversational assistant.

His analogy is the blue LED. Adding blue to red and green unlocked combinations and applications that were not obvious from thinking about each component alone. Similarly, an inexpensive, reliable semantic operation could combine with existing software primitives in ways that a chatbot interface does not reveal.

The proposed “fourth logic gate” is an analogy, not a claim about a new Boolean gate. It names a desired programming capability: make a context-sensitive judgment at the point where a program currently has only literal tests. An email address can satisfy a syntactic pattern yet still be inappropriate or implausible in its actual context. The interesting primitive would help express that difference.

[5:22:50 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19370s)

## Recover ordinary software engineering inside agent systems

The talk then returns to decomposition, encapsulation, and explicit state. These are familiar ideas, but current agent designs can make them awkward. A large shared conversational context is not a replacement for deciding which component owns which state or which intermediate result can be verified.

[![Questions about agent designs constrained by the KV cache](https://ai.engineer/reading/code-2026/images/diogo-almeida-19370.jpg)](https://ai.engineer/reading/code-2026/images/diogo-almeida-19370.jpg)

*At [05:22:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19370s), Almeida questions linear memory access, unshared state, and restrictions on routing and subagents. These are design questions, not demonstrated solutions.*

He argues that too much agent architecture is shaped by the economics and mechanics of the KV cache. Why must memory behave like a growing sequence? Why is state not shared naturally between agents? Why does routing become expensive or awkward? Why does an agent repeatedly rediscover a codebase rather than benefit from a more structured representation?

Almeida does not present a finished architecture that resolves those questions. He uses them to identify assumptions that engineers should stop treating as permanent. A system built around smaller, verifiable decisions could expose different opportunities for composition than one centered on an ever-growing context window.

## New primitives invite experiments, not only wrappers

The later examples explore what that composition might enable. A low-latency decision component could help inspect actions in a security workflow. Semantic checks could supplement conventional types or lint rules with properties that are difficult to express syntactically. Voice interfaces could better support the user's intended operation. Generative interfaces could adapt the interaction rather than simply adding a chat panel next to it.

These are proposed directions, not a list of deployed Jev capabilities demonstrated in the talk. Their common requirement is demanding: the decision must be fast, affordable, and reliable enough for the place it occupies in the program. If it still requires a human to carefully review every result, it may remain assistance rather than automation.

Almeida also points to an economic asymmetry in low-quality generated content. Generation is becoming cheap, but review costs can be pushed onto the recipient. Better generation alone does not repair that imbalance. Better decisions about what to accept, reject, or route might.

He closes by encouraging exploratory software work, including playful and strange experiments whose value is not immediately obvious. The blue-LED analogy returns implicitly: a new primitive's most useful combinations may not be visible before people try them. His suggested timelines remain speculative, and his reliability standard remains high.

The lasting challenge is to move from “could an AI do this?” to “what work would make this a dependable part of a system?” That work includes choosing the task, defining failure, exposing state, verifying intermediate decisions, and designing the surrounding software. Better assistance is useful. Almeida is asking engineers to build the additional machinery that makes automation a different product.

Full transcript 656 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[5:06:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18418s) >> Give me a sec to make sure this is

[5:06:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18419s) working. Heck yeah. I'm Diego Almeida

[5:07:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18423s) and this talk is I love you so jeving

[5:07:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18426s) much. Um glass animals reference. We're

[5:07:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18429s) not just weird. Um like I said, I'm

[5:07:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18432s) Diego Almeida. I'm known as the Jev guy,

[5:07:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18435s) sometimes Jevy Pinkman. Um, also

[5:07:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18438s) co-created chat GPT, RLHF, and Instruct

[5:07:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18441s) GPT, but I assume that for the crowd

[5:07:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18443s) today, you all know who I am, at least

[5:07:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18445s) mostly. Um, I have like a bunch of AI

[5:07:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18450s) specific stuff I want to get to, but I

[5:07:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18451s) like going into my favorite topics in

[5:07:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18453s) AI. First one is what the is

[5:07:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18456s) actually going on and where is all the

[5:07:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18458s) automation. If you've heard me say this

[5:07:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18460s) before, I'm sorry, but it's such an

[5:07:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18462s) important thing to beat into the field

[5:07:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18464s) because people still do not get it and I

[5:07:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18466s) need to yell this until everyone really

[5:07:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18468s) understands what the is going on.

[5:07:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18471s) And if you're an AI, you should have a

[5:07:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18472s) really good answer about why AI can do

[5:07:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18475s) so many awesome things and yet still be

[5:07:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18477s) so useless for a bunch of other ones. My

[5:08:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18480s) relationship to chat GPT is somewhat

[5:08:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18482s) unique. One of the few people who hates

[5:08:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18484s) on chat GPT who made it. I don't hate

[5:08:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18487s) chat GPT to be clear. I love using

[5:08:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18490s) agents. I love using coding agents. I

[5:08:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18492s) love chat bots. They're just quite

[5:08:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18493s) limited. And in particular, I think it's

[5:08:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18495s) a little tragic how much they've

[5:08:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18497s) bifurcated the field into overpromise,

[5:08:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18499s) underdeliver. Really, really terrible

[5:08:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18501s) stuff for the world in my opinion. And I

[5:08:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18504s) like to talk about like the two cults in

[5:08:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18506s) AI and how we can resolve the cognitive

[5:08:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18509s) dissonance that everyone I think should

[5:08:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18512s) be having unless they have a very good

[5:08:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18513s) answer. There's cult one, which is, you

[5:08:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18516s) know, the cult of like EAs. They look at

[5:08:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18518s) all the benchmarks and they say like not

[5:08:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18520s) only are LM surpassing human level on

[5:08:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18523s) basically every benchmark they have been

[5:08:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18525s) for two years we've been announcing AGI

[5:08:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18527s) three months away for two years now even

[5:08:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18529s) since like the 03 days do people

[5:08:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18531s) remember that no one even car cares

[5:08:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18532s) about that model anymore and it was that

[5:08:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18535s) that was like peak internal to openai

[5:08:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18537s) AGI hype and on the other hand you look

[5:08:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18539s) at the nonbenchmarks and you look at the

[5:09:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18542s) reality and you see the rest of the

[5:09:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18544s) world especially if you guys go outside

[5:09:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18545s) and leave San Francisco a lot of the

[5:09:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18547s) world is like really unchanged despite

[5:09:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18550s) AI being so cool. And I think AI

[5:09:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18552s) is transformative. It's a rare point of

[5:09:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18554s) view to actually think AI is cool and

[5:09:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18557s) transformative and also like

[5:09:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18559s) underwhelming the world right now. And

[5:09:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18561s) the tricky part is this is the same

[5:09:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18563s) field and we are all seeing the same

[5:09:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18565s) facts. So what gives you know why is AI

[5:09:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18568s) jagged so to speak like why can it be so

[5:09:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18570s) good at some things and so not good at

[5:09:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18573s) other things and what is the aams razor

[5:09:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18576s) explanation for that um I will be

[5:09:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18578s) blasting through my slides fast I'm

[5:09:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18580s) sorry maybe I could slow down for people

[5:09:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18582s) taking pictures um but uh I'm noticing

[5:09:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18585s) that uh this is going to go fast is all

[5:09:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18587s) I'm saying so I think that we as a field

[5:09:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18590s) should have an aams razor explanation

[5:09:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18592s) for why are there some things that are

[5:09:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18595s) Not just good, they're unbelievably

[5:09:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18597s) good, superhuman, like millennium price

[5:09:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18599s) problems in math. But on the other hand,

[5:10:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18602s) they're not just bad, they're so

[5:10:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18603s) useless, they can't even be used to

[5:10:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18605s) touch accounting. That sounds way easier

[5:10:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18607s) than million prize problems in math,

[5:10:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18608s) right? I could do the latter. I

[5:10:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18609s) definitely could not do the former. And

[5:10:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18611s) I was a mathlete. So what gives here?

[5:10:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18613s) What is the reason for this? And I

[5:10:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18616s) normally love this as an interactive

[5:10:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18617s) thing, but I will instead just tell you

[5:10:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18619s) my answer. Sorry for the power dynamic.

[5:10:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18621s) Um, everything on the left side is

[5:10:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18624s) intrinsically a human in the loop task.

[5:10:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18626s) Like deep research, I could not do

[5:10:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18628s) better than deep research. The models

[5:10:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18629s) are so good at that. But if gun

[5:10:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18632s) to my head or gun to your head, you had

[5:10:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18634s) to pick between me and deep research.

[5:10:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18636s) And the answer had to be correct, not

[5:10:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18638s) well written, you'd probably pick me

[5:10:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18639s) every time. And that's the distinction

[5:10:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18641s) between like optimizing for automation,

[5:10:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18644s) which tends to be a lot easier and a lot

[5:10:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18646s) simpler. Yet m AI keeps failing at this.

[5:10:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18649s) Every year there's like an infamous

[5:10:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18651s) failure of AI failing to even automate

[5:10:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18653s) drive-throughs. And that should be kind

[5:10:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18655s) of shocking to people. And my claim is

[5:10:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18658s) actually for these tasks pleasing a

[5:11:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18660s) human is nothing to do with doing the

[5:11:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18662s) task. What you want to do is basically

[5:11:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18664s) be an abstraction away. You want the

[5:11:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18666s) decision to be made and you want to get

[5:11:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18668s) back into doing automation and code is

[5:11:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18670s) the language of automation. Therefore,

[5:11:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18672s) you need to integrate with code. This is

[5:11:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18673s) a lot but I will summarize it again. I

[5:11:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18675s) get the irony that uh you know I've

[5:11:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18678s) co-created RHF and I do believe RLHF is

[5:11:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18680s) part of the problem and RHF in

[5:11:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18683s) particular is why all AI today does

[5:11:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18686s) require a human in the loop with an

[5:11:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18688s) asterisk unless the task is like very

[5:11:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18690s) trivially verifiable and can run on its

[5:11:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18692s) own but still requires a human in the

[5:11:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18693s) loop to verify it afterwards. It is

[5:11:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18695s) because we literally put it in that is

[5:11:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18697s) what the HF is in RHF. And my claim is

[5:11:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18700s) that there's a better way. You know, my

[5:11:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18703s) summary of the state is 100% of LMS

[5:11:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18705s) today are optimized for assistance. You

[5:11:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18707s) might talk about RLVR, but the RLVR

[5:11:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18709s) models are very bad to interact with if

[5:11:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18711s) they've not been RHFed. The result is

[5:11:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18714s) LMS become too good to be true at

[5:11:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18716s) assistance. They are just so

[5:11:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18718s) good. Like, you should never pick me

[5:11:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18719s) over chat GPT for your chat GPT queries.

[5:12:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18722s) But for actually doing like you know run

[5:12:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18725s) in the background cognitive work you

[5:12:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18727s) should not trust LMS at all because they

[5:12:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18729s) have not been optimized for that which

[5:12:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18730s) is why they're so bad at the tasks of

[5:12:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18732s) automation and I would also guess that

[5:12:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18734s) automation is a lot more valuable than

[5:12:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18736s) assistants because you can do way cooler

[5:12:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18738s) deeper I'm going to get into this later

[5:12:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18739s) but I think there's going to be so much

[5:12:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18741s) stuff that we can do and we are just

[5:12:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18742s) scratching the surface of that right now

[5:12:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18744s) and that's the tragic thing about AI uh

[5:12:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18746s) the state of AI for me let's talk about

[5:12:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18750s) the evolution Um, I I can't tell if this

[5:12:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18753s) is appropriate, but it's too late. Um,

[5:12:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18756s) oh god, don't take pictures of this one.

[5:12:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18758s) Um, cool. Oh, I'm getting a thumbs up.

[5:12:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18762s) Yeah. Uh, excellent. So, we're we

[5:12:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18764s) instead of doing RHF, we just have to do

[5:12:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18766s) something else. We need to think from

[5:12:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18767s) first principles. How do we optimize for

[5:12:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18769s) machine native AI? You guys hopefully

[5:12:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18771s) know the interface of Jev and that is

[5:12:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18772s) what we are doing. more important than

[5:12:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18774s) optimizing for its interface, we are uh

[5:12:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18777s) rethinking how AI should be done because

[5:12:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18779s) this is what we did again for Arlf for

[5:13:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18782s) Sutton's bitter lesson. I'm going to

[5:13:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18785s) loosely paraphrase to make my point

[5:13:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18786s) easier to say is that scaling um and

[5:13:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18790s) compute matters more than algorithms.

[5:13:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18792s) This is why people become like scaling

[5:13:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18793s) pill jironies. And I would argue that

[5:13:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18796s) there's an even bitter lesson than that

[5:13:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18798s) which is data always matters more than

[5:13:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18800s) compute. We are learning that quite a

[5:13:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18802s) bit in the field now, but it has been

[5:13:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18803s) obvious since the beginning of time.

[5:13:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18806s) I'll tell you when the this is the one

[5:13:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18807s) you should be photographing. I would

[5:13:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18809s) argue that the the bitterest lesson is

[5:13:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18811s) doing the right task. And doing the

[5:13:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18813s) right task is like a weird thing to

[5:13:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18815s) think about especially for ML people

[5:13:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18817s) because they like algorithms. They want

[5:13:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18819s) number goes down or up or whichever is

[5:13:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18821s) good direction. They don't want to think

[5:13:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18822s) about the real world. But this is always

[5:13:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18824s) how you make gigantic gains in

[5:13:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18826s) performance. This is how the big

[5:13:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18828s) breakthroughs happen. 100% of the time

[5:13:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18829s) it comes from this and this is true for

[5:13:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18832s) classical RL games. This is why Sutton

[5:13:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18834s) had his bitter lesson it which is data

[5:13:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18837s) is derived by compute when you're doing

[5:13:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18839s) rollouts like there's there's why would

[5:14:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18840s) you need off policy data when playing

[5:14:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18842s) chess or something like that and doing

[5:14:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18844s) the right task is defined by the rules.

[5:14:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18846s) So actually when you're doing RL you

[5:14:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18848s) don't even need to think about the right

[5:14:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18849s) task for pre-training we actually as a

[5:14:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18852s) field had to do a lot of thinking about

[5:14:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18854s) the right task. I don't know if people

[5:14:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18855s) remember the birth days with um masked

[5:14:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18858s) language modeling, but it took a while

[5:14:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18860s) and it was very unclear to figure out

[5:14:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18862s) that next pro token prediction was super

[5:14:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18864s) cool. Not because it was better

[5:14:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18866s) at masked language modeling. You know,

[5:14:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18868s) the objectives on their own aren't

[5:14:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18870s) special. It's about what you can do with

[5:14:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18871s) them afterwards. And it turns out next

[5:14:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18873s) token prediction is incredible at

[5:14:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18874s) generating strings, which is what these

[5:14:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18876s) pre-trained models were so good at. So

[5:14:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18878s) no level of mass language modeling even

[5:14:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18880s) if you had today's compute and

[5:14:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18881s) algorithms would make it as interesting

[5:14:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18883s) as GPT3 was because it was just doing a

[5:14:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18886s) different task and data you know the

[5:14:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18888s) internet is obviously a giant

[5:14:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18890s) bottleneck. Now we're like you know

[5:14:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18891s) burning books or whatever in order to

[5:14:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18892s) get more data but data obviously matters

[5:14:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18894s) a lot more than compute and people keep

[5:14:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18896s) like rediscovering this and figuring

[5:14:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18898s) this out. It's extra true for making

[5:15:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18900s) LLMs useful. um before RHF even existed

[5:15:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18904s) the data for RHF didn't exist and you

[5:15:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18906s) could like it was night and day I'll

[5:15:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18909s) just show you the next slide this is the

[5:15:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18910s) probably the relevant part this is what

[5:15:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18911s) this was the work in the RHF paper and

[5:15:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18914s) \[snorts\] the high level was that even

[5:15:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18916s) with the dumbest algorithms in the world

[5:15:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18918s) even with a GPT2 sized model you got

[5:15:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18921s) something like GPT9 level performance

[5:15:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18923s) like real GPT9 not today's like fake GPT

[5:15:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18926s) numbers like the numbers used to mean

[5:15:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18928s) like a 100x scaling and effective

[5:15:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18930s) compute for pre-training and they've

[5:15:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18931s) given up on that because it just can't

[5:15:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18933s) scale anymore. And still even with that,

[5:15:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18935s) it would take something like GPT7 to9 to

[5:15:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18937s) match GPT to the model from like 2018 or

[5:15:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18941s) whatever it was at the task of

[5:15:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18943s) instruction following. That is kind of

[5:15:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18945s) wild because you think big LMS are so

[5:15:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18947s) important for this and they are, but

[5:15:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18949s) that is not the most important thing

[5:15:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18951s) compared to even the gigantic jump of

[5:15:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18954s) doing the right task. And spoilers, this

[5:15:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18956s) is what we did for Jeff, right? like we

[5:15:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18957s) made this gigantic leap in the field

[5:15:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18959s) that no one realized could be coming

[5:16:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18961s) because we were optimizing for a task

[5:16:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18963s) and very few people think about the

[5:16:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18964s) right task. Um this is why Jev has the

[5:16:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18969s) Jeb Nissiqua. Um that's a really smart

[5:16:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18972s) bun I think. Um

[5:16:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18976s) little bit of a pity laugh, but thank

[5:16:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18977s) you. Um you get what you optimize for. I

[5:16:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18980s) I'm looking for a better word than

[5:16:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18981s) reliable. So if you guys have

[5:16:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18983s) suggestions, let me know. But there's

[5:16:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18985s) there's this reliability of intelligence

[5:16:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18987s) that's really missing in LLMs. I often

[5:16:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18989s) call it you get Einstein 95% of the

[5:16:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18992s) time, but Mr. Bean 5% of the time. And

[5:16:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18994s) if you can't sell which is which, how

[5:16:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18996s) the are you going to automate

[5:16:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18997s) anything? And instead, instead of like

[5:16:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=18999s) focusing on like sometimes occasional

[5:16:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19001s) smarts that you can then verify, what if

[5:16:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19003s) you focused on extreme extreme narrow

[5:16:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19005s) focused reliability so you can get that

[5:16:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19008s) smarts every time? And this doesn't show

[5:16:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19010s) up on benchmarks. It is the reason why

[5:16:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19011s) people love Jev. And this is also I

[5:16:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19013s) realized in hindsight we obviously

[5:16:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19014s) didn't prepare for a chat GPT moment for

[5:16:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19017s) developers. But it happened because

[5:16:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19019s) people in the AI space just overpromise

[5:17:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19022s) underdel so much that having a

[5:17:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19024s) model that actually don't do that was a

[5:17:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19026s) surprise. And it is not the speed cost

[5:17:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19028s) or even interface. This is something

[5:17:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19030s) that you know my team tells me I

[5:17:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19032s) shouldn't be telling people so that we

[5:17:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19034s) can have a long-term advantage and I

[5:17:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19035s) just care too much. Like it's reliable

[5:17:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19037s) intelligence. Make sick models please.

[5:17:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19039s) even if we, you know, if it doesn't

[5:17:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19041s) involve our models. Um, we see that Jev

[5:17:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19044s) as like a foundation for smart software.

[5:17:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19046s) I'm going to skip all over this, but I

[5:17:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19047s) think software is going to be so

[5:17:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19049s) back. I think the narrative of SAS

[5:17:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19051s) apocalypse is obviously not going to

[5:17:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19053s) happen, but I think that even calling it

[5:17:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19056s) a SAS Palooa is like an understatement

[5:17:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19058s) and I will get into that a bit and you

[5:17:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19060s) guys ideally are the perfect crowd for

[5:17:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19061s) this. I'm so excited for this part

[5:17:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19063s) because that's the part that's new to

[5:17:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19064s) me. Um, I want to make the distinction

[5:17:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19067s) between smart software and just in time

[5:17:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19069s) software. The the crazy part is AI is so

[5:17:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19072s) transformative and yet somehow despite

[5:17:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19075s) AI being so awesome, software has

[5:17:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19078s) essentially unchanged in the last decade

[5:18:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19080s) except being cheaper to write. Isn't

[5:18:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19082s) that weird? Isn't the it weird that the

[5:18:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19084s) best we can do in software is having a

[5:18:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19086s) chatbot to the side that sometimes

[5:18:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19088s) interacts with a software but cannot

[5:18:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19090s) take expensive decisions for you. That

[5:18:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19092s) is kind of like a a weird thing if AI

[5:18:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19094s) was really that transformative. And I

[5:18:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19096s) think the problem is we're focusing too

[5:18:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19097s) much on coding agents and not enough

[5:18:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19100s) about putting the intelligence into the

[5:18:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19101s) inner loop, which I'm going to get more

[5:18:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19102s) into a bit. And people are jeving.

[5:18:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19105s) There's been tons of successes. We don't

[5:18:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19107s) need to flex this. There's so many cool

[5:18:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19108s) things, but my AIE secret is going to be

[5:18:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19112s) that the field isn't jeving hard enough.

[5:18:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19114s) And this is what Swix said that I can

[5:18:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19116s) make a call to action for you guys

[5:18:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19117s) that's unique. And hopefully I have

[5:18:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19118s) enough time for this. I think the world

[5:18:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19120s) still has LLM Stockholm syndrome. We are

[5:18:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19123s) still thinking from a really LLM pill

[5:18:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19125s) place which is I think tragic you know

[5:18:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19128s) like I I I love the software saying the

[5:18:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19130s) tools you use change the way you think

[5:18:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19132s) and I think that it's changed the way we

[5:18:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19134s) think way too much and we're not really

[5:18:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19136s) rethinking software like I think the

[5:18:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19138s) field needs. I think that we could just

[5:19:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19140s) do be doing so much more. Hopefully I

[5:19:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19142s) can try to do my best for my remaining

[5:19:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19143s) time to convince you guys of that. Um so

[5:19:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19146s) let's Jev to the future. Um

[5:19:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19150s) I an analogy I love bear with me is

[5:19:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19153s) about LEDs. Before there was the blue

[5:19:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19156s) LED there was red and green LEDs. These

[5:19:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19158s) were really limited in capability and

[5:19:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19160s) they were used for like simple

[5:19:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19161s) indicators and you know like clocks and

[5:19:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19163s) stuff like that. And when the blue LED

[5:19:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19166s) was made discovered I actually don't

[5:19:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19168s) really know how things outside of

[5:19:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19169s) computer science work. Um, but when it

[5:19:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19171s) existed, I guess, um, it enabled not

[5:19:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19174s) just like 50% more use cases, which what

[5:19:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19177s) you'd expect about like changing colors

[5:19:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19178s) from two to three, it enabled so many

[5:19:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19180s) more. Like now LEDs could be used for

[5:19:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19182s) white light. It could be used for like

[5:19:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19184s) the displays that we all use right now.

[5:19:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19185s) And it created a revolution in lighting.

[5:19:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19188s) And it's it's it's unfathomable how much

[5:19:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19190s) bigger the capabilities of LEDs were.

[5:19:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19193s) Just ex, you know, adding a new

[5:19:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19195s) primitive that composes together with a

[5:19:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19197s) old primitive. So you can see where I'm

[5:19:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19199s) going here. maybe. And I think it's a

[5:20:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19201s) similar story for software. Software is

[5:20:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19204s) so incredible. Ignore AI for the

[5:20:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19206s) last, you know, half decade. But

[5:20:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19207s) software has done so many insanely cool

[5:20:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19210s) things. We've done a lot of stuff, you

[5:20:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19212s) know, like do I love using SAS? Not

[5:20:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19216s) really. But does it solve problems? Abso

[5:20:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19218s) lutely. And it's incredible how

[5:20:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19220s) much we've done with three fundamental

[5:20:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19222s) logic gates. You know, like we are doing

[5:20:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19224s) this with like simple binary operations

[5:20:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19226s) that can do things like greater than,

[5:20:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19228s) less than, equal. It's kind of nuts how

[5:20:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19230s) much software has been built from such

[5:20:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19232s) simple primitives. And my claim is that

[5:20:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19236s) what we are doing with AI now when we're

[5:20:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19238s) making a intelligence machine native

[5:20:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19240s) this is kind of conceptually adding a

[5:20:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19242s) fourth semantic logic gate. What if we

[5:20:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19245s) can program with common sense with

[5:20:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19247s) intention with human understanding? Like

[5:20:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19250s) do we still need reexes with like crazy

[5:20:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19252s) things or can we just say like we want a

[5:20:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19253s) Gmail email address or a real looking

[5:20:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19255s) one? There's so much that we can do that

[5:20:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19257s) we're going to need to push the f, you

[5:20:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19258s) know, push the frontiers of cheap,

[5:21:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19260s) smart, fast in order to get done. But I

[5:21:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19263s) think that there's going to be like so

[5:21:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19264s) many things here. And I think just like

[5:21:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19266s) the blue LED, it's going to be way

[5:21:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19268s) bigger than just increasing the

[5:21:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19270s) representational ability of software by

[5:21:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19272s) 33%. Because it's adding effectively

[5:21:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19274s) another kind of sort of logic gate. And

[5:21:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19277s) this sci-fi is the stuff that I think

[5:21:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19278s) will be impossible to predict. Just like

[5:21:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19280s) who could predict how powerful the

[5:21:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19282s) internet would have been because it

[5:21:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19284s) requires it's like much more grassroots

[5:21:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19285s) and decentralized and it requires people

[5:21:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19287s) to be empowered to do insane stuff. Um I

[5:21:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19290s) call this software research. Um that's

[5:21:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19294s) not a joke. Um but uh I I think that

[5:21:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19297s) there's going to be like an explosion of

[5:21:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19299s) what software can do and we will want

[5:21:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19302s) people to be exploring those boundaries

[5:21:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19304s) of software. Not necessarily because

[5:21:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19306s) it's valuable, but because they can.

[5:21:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19308s) Because we have like new frontiers to

[5:21:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19310s) explore and this is what the early

[5:21:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19311s) internet was like. Should all of those

[5:21:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19313s) websites existed? Probably not. But like

[5:21:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19316s) it was very cool and we found a lot of

[5:21:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19318s) awesome stuff from that. And I think we

[5:22:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19320s) we, you know, we have another

[5:22:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19321s) opportunity for that. So we should not

[5:22:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19323s) just keep living in this little, you

[5:22:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19325s) know, fish tank that we are the victims

[5:22:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19327s) of open anthropic on whatever they ship

[5:22:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19329s) and we just have to be like LM rappers.

[5:22:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19331s) So I'm going to pitch software research

[5:22:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19333s) as a direction here. The theme is going

[5:22:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19335s) to be real software engineering, not

[5:22:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19338s) just vibe coding. There's it's going to

[5:22:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19340s) be like the kind of stuff that everyone

[5:22:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19341s) has known if you've been a software

[5:22:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19343s) engineer. Decomposition, breaking tasks

[5:22:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19345s) down. We need to think about stages,

[5:22:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19347s) ideally ones that can be verified so we

[5:22:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19349s) have real encapsulation. And we need to

[5:22:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19351s) actually do state management instead of

[5:22:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19353s) assuming everything is global state

[5:22:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19355s) within a KV cache. And the theme is just

[5:22:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19357s) going to be like real

[5:22:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19358s) engineering by people who care a lot

[5:22:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19360s) about the end result. It doesn't have to

[5:22:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19362s) be valuable. Ideally, it's sick as

[5:22:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19364s) Um, and you know, we should be pushing

[5:22:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19366s) the limits. I'm going to go into a

[5:22:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19369s) couple of like my favorite ideas and I

[5:22:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19371s) want to figure out how to encourage

[5:22:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19373s) these in the world. So, this is my first

[5:22:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19375s) step at this. I'm just going to talk

[5:22:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19376s) about it. We have raised a bunch of

[5:22:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19378s) money. So, I would like to figure out

[5:22:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19379s) how to fund this, but we don't have the

[5:23:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19380s) operations help to do that. But here are

[5:23:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19382s) just some ideas out there. Um, I think

[5:23:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19385s) agents are they're very cool, but like

[5:23:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19389s) they're they're so inflexible in their

[5:23:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19391s) design because of the tyranny of the KV

[5:23:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19393s) cache. I don't have the time for this if

[5:23:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19395s) this timer is to be believed, but

[5:23:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19397s) believe me that there's so much that

[5:23:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19398s) people have tried to do but failed at

[5:23:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19400s) because it ends up becoming inefficient

[5:23:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19402s) because it fights against the KV cache.

[5:23:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19404s) But I think there's a lot more to do.

[5:23:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19406s) Why is memory o of nan, right? Like why

[5:23:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19408s) can't we have all of our history of

[5:23:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19410s) coding agents always included in every

[5:23:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19412s) new call? That is how continual learning

[5:23:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19415s) works, right? And we have the memory

[5:23:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19417s) available. It's just that we don't have

[5:23:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19419s) the smarts to map produce over the

[5:23:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19420s) memory to find out like what you should

[5:23:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19423s) what you should remember, what should

[5:23:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19424s) you shouldn't. Um I think there's many

[5:23:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19426s) ways to do login or even better lookups.

[5:23:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19428s) Why when you're making many agents at

[5:23:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19430s) once, why can't they not share state?

[5:23:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19432s) Why do they need to rediscover the same

[5:23:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19434s) patterns of the codebase over and over

[5:23:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19436s) and over again? And why can't non-naive

[5:23:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19438s) routing and sub agents work? Like even

[5:23:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19439s) naive routing doesn't work, but like why

[5:24:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19441s) can't we do these things? And why does

[5:24:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19443s) like the you know the big labs keep

[5:24:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19444s) going back and forth on whether or not

[5:24:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19445s) sub agents work? Um I think that like

[5:24:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19448s) from an engineering perspective there's

[5:24:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19450s) elegance to it but they fight against

[5:24:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19452s) the KV cache and I think that if we

[5:24:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19454s) design agents around that we could do so

[5:24:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19456s) much more. This one's the the probably

[5:24:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19459s) the most vague of my directions but I

[5:24:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19460s) feel very strongly about it. Um the

[5:24:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19463s) world is full of principal agent

[5:24:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19464s) problems. This is when you have like you

[5:24:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19466s) know ulterior motives between this is

[5:24:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19468s) not a coding agent but like any agent.

[5:24:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19470s) The the classic example is citizens

[5:24:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19472s) versus elected officials. I don't want

[5:24:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19474s) to make a too political claim here, but

[5:24:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19476s) like there's misalignment in all levels

[5:24:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19478s) of society. And this results in like

[5:24:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19480s) waste, fraud, bad things, and it it

[5:24:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19484s) results in for a society that wants

[5:24:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19485s) fairness, you need to overemphasize the

[5:24:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19488s) letter over the spirit, which then

[5:24:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19489s) results in loopholes and play uh pay to-

[5:24:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19492s) win dynamics in the world. And I think

[5:24:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19494s) the root of that problem is we can't

[5:24:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19495s) encode the spirit. Just like with

[5:24:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19497s) software, we're constrained to encoding

[5:24:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19499s) bits instead of what we actually meant

[5:25:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19501s) in that situation. And I think so many

[5:25:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19504s) organization, society could be

[5:25:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19505s) transformed by really encoding the

[5:25:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19507s) spirit all over the place. Obviously,

[5:25:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19509s) real-time intelligence security, can we

[5:25:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19512s) prevent the OpenAI hugging face sandbox,

[5:25:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19514s) blah blah blah. Um, why did why couldn't

[5:25:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19517s) they prevent it? It is not because they

[5:25:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19519s) didn't have the intelligence. I would

[5:25:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19520s) argue it's a lot easier to figure out

[5:25:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19522s) they're doing a naughty thing than to

[5:25:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19523s) actually do the naughty thing. It is

[5:25:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19525s) because it was not fast, cheap, and

[5:25:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19527s) reliable enough to actually run real

[5:25:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19529s) time. And what happens when every

[5:25:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19532s) corporation has their own real-time

[5:25:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19534s) security that's actually smart? How cool

[5:25:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19536s) would that be? I can't talk

[5:25:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19538s) about generative UIs because people are

[5:25:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19540s) going to be talking about it afterwards.

[5:25:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19541s) I don't want to steal their thunder, but

[5:25:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19543s) it's cool as Trust me. Um,

[5:25:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19546s) like semantic dependent typing. Why

[5:25:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19548s) can't we have like a type system that

[5:25:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19552s) actually is semantic, right? like why

[5:25:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19554s) can't we like declare what local

[5:25:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19557s) properties we want so we don't have to

[5:25:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19559s) read a chain of dependencies deep down

[5:26:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19561s) these all should be possible and imagine

[5:26:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19563s) if you could like run a jeike model in

[5:26:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19565s) your lint checker to check if you're

[5:26:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19567s) it's all type safe and it could you know

[5:26:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19569s) uphold semantic properties it would be

[5:26:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19571s) so cool there's there was a

[5:26:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19575s) great Twitter video on um like a voice

[5:26:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19577s) interface in general I think new

[5:26:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19579s) interfaces are so exciting this is to me

[5:26:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19582s) the return of like this is going to show

[5:26:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19583s) by agent software like do what I mean.

[5:26:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19585s) This used to be like a popular thing but

[5:26:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19587s) it never really worked because you it

[5:26:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19589s) was it was too many hard-coded rules to

[5:26:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19591s) really figure out what I mean. Um

[5:26:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19593s) there's stopping slop obviously a big

[5:26:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19596s) theme of here but like we definitely

[5:26:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19598s) believe this. This is my props. I have

[5:26:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19599s) to we have a stop geni baseball bat for

[5:26:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19602s) type safe. It is very very awesome. I

[5:26:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19605s) want to talk about the root of slop. Um

[5:26:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19607s) the the root of slop is that AI is

[5:26:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19609s) unreliable. Therefore, you as a company

[5:26:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19612s) or you as you know like someone who's

[5:26:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19614s) doing stuff, it can't be used for

[5:26:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19615s) decisions that costs you stuff. But it's

[5:26:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19618s) actually totally fine to push the costs

[5:26:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19619s) into other people, which is horrible.

[5:27:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19621s) You know, externalized costs and then

[5:27:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19622s) this is what ends up becoming stop. You

[5:27:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19625s) know, if people actually read the stuff

[5:27:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19626s) and filter it and like care about the

[5:27:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19628s) quality, it becomes not slop, but now

[5:27:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19630s) the world is full of this because

[5:27:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19632s) there's an asymmetric advantage for

[5:27:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19633s) people who are like bad actors and don't

[5:27:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19635s) give a So, I think that we can

[5:27:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19637s) save the world from at least inbound

[5:27:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19639s) hell among many other things and that

[5:27:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19640s) would be very cool. Um, and even

[5:27:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19643s) something I think is super sick is

[5:27:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19645s) cursed software. Like why if you guys

[5:27:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19648s) have ever seen the subreddit bad UI

[5:27:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19650s) battles, it is so cool. Even

[5:27:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19652s) though they make the horrible interfaces

[5:27:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19654s) like this whole game of like would you

[5:27:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19655s) like to delete your account becomes you

[5:27:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19657s) know a random thing. And and I actually

[5:27:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19660s) think doing things because we can is

[5:27:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19662s) what software engineering is about

[5:27:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19664s) because who knows maybe 1% of these

[5:27:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19666s) ideas actually lead to something super

[5:27:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19668s) awesome. And I think like really

[5:27:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19670s) cultivating even bad ideas is kind of

[5:27:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19673s) what being like this you know playful

[5:27:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19674s) hacker is all about and generally just

[5:27:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19678s) automating everything. This is what the

[5:28:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19681s) followup this is this is a slop image

[5:28:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19682s) but uh sorry logo is a little bit wrong

[5:28:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19684s) but don't stare at that. That's a little

[5:28:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19686s) weird. Um, this is what a lot of the

[5:28:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19688s) follow-up talks are going to be about.

[5:28:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19690s) Thank you. Um, and and if you're a

[5:28:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19693s) software engineer, you almost certainly

[5:28:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19695s) think in the world of bits. If you know

[5:28:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19697s) anything about software, uh, and you've

[5:28:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19699s) interacted with software, you know that

[5:28:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19701s) there are things software can do and

[5:28:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19703s) software cannot do because that is just

[5:28:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19705s) only obvious, right? Like there's some

[5:28:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19708s) things that you know you need to do

[5:28:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19710s) because that is not compatible with

[5:28:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19711s) software. But what if those constraints

[5:28:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19713s) were no longer true? Maybe not today,

[5:28:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19715s) but maybe in like six months or a year.

[5:28:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19717s) What couldn't we automate? And that's

[5:28:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19719s) kind of where I want to leave this whole

[5:28:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19721s) thing because I think there is very

[5:28:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19723s) likely to be a future where it's not a

[5:28:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19725s) question of whether or not we can

[5:28:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19726s) automate something. It's going to be a

[5:28:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19728s) question of like how much work is it,

[5:28:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19729s) which is how it is right now for the

[5:28:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19731s) stuff that can be automated. And that

[5:28:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19732s) would be cool as So, hell yeah.

[5:28:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19735s) Thank you. Um,

[5:28:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19737s) \[applause\]

[5:28:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19739s) I'm super overtime, but thank you to the

[5:29:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19742s) early believers. You know, we had no

[5:29:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19744s) idea so many people would resonate with

[5:29:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19745s) this. We thought we were the insane

[5:29:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19747s) ones, but it turns out like we were

[5:29:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19749s) actually the majority of the world who

[5:29:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19750s) realized AI could be so much more. Thank

[5:29:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19753s) you to like the people who are like

[5:29:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19754s) really realistic about reliability.

[5:29:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19756s) Everyone knows I hate benchmarks and a

[5:29:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19758s) lot of other people are really screaming

[5:29:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19759s) out like benchmarks suck.

[5:29:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19761s) They're actually they hurt the people

[5:29:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19763s) who do not have time for anything other

[5:29:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19765s) than benchmarks most. It's tragic. And

[5:29:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19767s) for the people who are pushing the

[5:29:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19768s) limits of software, like yes. And

[5:29:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19771s) we want to be there with you helping you

[5:29:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19773s) all do that. The the dreamers and the

[5:29:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19775s) people who don't want to be limited by

[5:29:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19777s) everything that has happened so far. We

[5:29:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19780s) want to really fight for you and we want

[5:29:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19782s) this to be as reliable as a fourth logic

[5:29:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19785s) gate and that is a very high bar and we

[5:29:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19788s) have like a lot of work to do. So thank

[5:29:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=19790s) you. Thank you.
