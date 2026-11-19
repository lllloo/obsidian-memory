---
title: Your Spec Has Bugs. Catch Them Before Your Agent Codes. — Rajath Mahendrappa Kotyal
description: AI Engineer CODE 2026 官方閱讀版，AWS Kotyal 談用 LLM 翻譯需求、SMT solver 檢查矛盾與缺漏，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-aws-specification-analyzer
published: 2026-11-11
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如開頭的「KO specification analyzer」）。逐字稿對應 Day 1 直播 `https://www.youtube.com/watch?v=ZZ19zhYnDKY`（影片 ID `ZZ19zhYnDKY`，本場位於 1:50:46–1:58:35）；`published` 取該直播的 YouTube release date。

Day 1 livestream · [1:50:46–1:58:35 on YouTube](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6646s). The player starts and stops at this session’s boundaries.

## Introduction

An e-commerce specification says that an order should become a backorder when inventory is unavailable. Elsewhere, it says that no order should ever become a backorder.

Each sentence is easy to understand on its own. Together, they ask the coding agent to implement an impossible combination. Better code generation cannot settle which business rule the author actually meant.

Rajath Kotyal's talk moves the first check earlier: inspect the specification before handing it to the agent that writes the implementation. The project he describes combines an LLM's ability to translate natural language with a solver's ability to check relationships between formal statements.

[1:51:20 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6680s)

## Find the problem before it becomes code

The [backorder example](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6680s) illustrates a conflict across sentences. Other problems can hide inside a single sentence: a vague verb, an unstated condition, or a level of detail that leaves the implementation to guess.

There are also gaps. A set of rules may cover submitted and completed orders while saying nothing about an idle order. Nothing has to be directly contradictory for the agent to be left making a decision the specification's author never made.

This is familiar work in design reviews. Engineers draw flows and read requirements together to discover cases that prose obscures. Kotyal's proposal is to automate part of that first review, surfacing questions while they are still questions about intended behavior rather than bugs embedded in a codebase.

[1:54:20 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6860s)

## Let the LLM translate and the solver check

The pipeline begins by refining the wording. It then translates requirements into a formal representation and analyzes that representation for conflicts, gaps, and scenarios.

[![Source slide shows the three stages: LLM refine, LLM formalize, and SMT solver analyze.](https://ai.engineer/reading/code-2026/images/online-aws-specification-analyzer-6860.jpg)](https://ai.engineer/reading/code-2026/images/online-aws-specification-analyzer-6860.jpg)

*At [01:54:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6860s), the slide separates the LLM's translation work from the solver's checking work. It runs on requirements before code generation.*

An SMT solver checks logical constraints expressed in a formal language. For the order example, the important relationship is between the condition “submitted with no available inventory” and the required backorder state, together with the global prohibition against that state. Expressing those relationships makes it possible to ask whether the relevant constraints can hold together.

That precision applies to the formalized requirements. It does not prove that the translation captured the author's intent. An LLM can turn an ambiguous sentence into one perfectly consistent interpretation while silently discarding another plausible reading.

Kotyal therefore adds a second kind of check: compare translations rather than trusting the first one.

[1:55:00 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6900s)

## Sample interpretations, then compare their meaning

At [01:55:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6900s), Kotyal describes asking the model to translate the same requirement multiple times, then clustering the outputs by logical equivalence.

Different wording is not necessarily disagreement. Two formal expressions can mean the same thing. Conversely, superficially similar outputs can encode different assumptions. Clustering by meaning is meant to separate those cases.

[![Source slide shows sample, cluster by logical equivalence, and decide: accept, ask, or abstain.](https://ai.engineer/reading/code-2026/images/online-aws-specification-analyzer-6940.jpg)](https://ai.engineer/reading/code-2026/images/online-aws-specification-analyzer-6940.jpg)

*The [1:55:40 slide](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6940s) turns model disagreement into an explicit decision point instead of letting one arbitrary interpretation reach the codebase.*

The next action depends on the result. The system can accept a sufficiently clear interpretation, ask the author to resolve the ambiguity, or abstain from implementing the requirement. Repeating a translation is useful because it exposes alternative assumptions, not because repetition converts generated text into ground truth.

“Remove the record” is the talk's concrete example. Does that mean deleting the data, or retaining it while hiding it from users? Both can produce plausible implementations. They have different consequences for retention, recovery, and future queries. The tool should present the choice rather than settle it accidentally through code.

[1:56:35 ↗](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6995s)

## The author still owns the intended behavior

The [ending](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6995s) puts a limit on the entire pipeline. There is no automatic oracle for what a specification should mean. Domain knowledge can be implicit, and even a logically consistent specification can describe the wrong product.

Formal checking is useful precisely when its scope stays clear. It can expose a contradiction in the represented rules or show that the sampled interpretations disagree. It cannot decide whether the business wants backorders, whether “remove” should preserve a legal record, or whether an omitted state is intentionally outside scope.

Kotyal also describes the evidence for this emerging approach cautiously. The useful takeaway is a division of work: the LLM translates, the solver checks, and a human makes the consequential choice when the intended rule is unresolved.

That gives the coding agent a better starting point. Instead of asking it to repair code written from conflicting instructions, resolve the contradiction before the implementation exists.

Full transcript 161 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[1:50:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6648s) I'm part of the automated reasoning

[1:50:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6650s) group at AWS and today I'm going to talk

[1:50:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6653s) about a project I worked on recently

[1:50:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6656s) called KO specification analyzer and u

[1:51:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6660s) we use certain techniques which involves

[1:51:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6662s) formal methods and automated reasoning

[1:51:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6664s) to prove specification that goes to your

[1:51:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6667s) coding agent before it writes code.

[1:51:16](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6676s) So let's take a certain bug right

[1:51:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6680s) this is a specification

[1:51:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6683s) uh snippet and there are two rules for

[1:51:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6686s) example and uh the rule two says when an

[1:51:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6689s) order is submitted and this is for a a

[1:51:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6692s) general e-commerce website let's say

[1:51:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6695s) when an order is submitted and the

[1:51:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6696s) inventory is unavailable we place the

[1:51:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6699s) order as a back order which makes sense

[1:51:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6701s) when you read it individually and

[1:51:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6703s) there's also another rule in the same

[1:51:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6705s) specification file uh which you hand to

[1:51:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6707s) the coding agent which says u no order

[1:51:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6710s) shall be placed as a back order and this

[1:51:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6712s) is a rule we've set so individually read

[1:51:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6716s) these two lines make sense right but in

[1:52:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6720s) when an LLM reads this reads both the

[1:52:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6722s) rules together both cannot hold true at

[1:52:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6725s) the same time so we need to make sure

[1:52:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6728s) the we resolve this ambiguity that the

[1:52:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6730s) LLM is observing

[1:52:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6734s) and uh

[1:52:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6737s) the scope and the reason we

[1:52:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6742s) uh put an effort into this project is

[1:52:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6744s) based on public research and recent

[1:52:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6747s) research we've observed there's a 20 to

[1:52:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6748s) 40% drop with unclear prompts on the

[1:52:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6752s) accuracy the LLM uh generates on the

[1:52:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6755s) code accuracy right and 60 to 90% % of

[1:52:38](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6758s) valid code is still wrong after it

[1:52:40](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6760s) writes it and also in that case we

[1:52:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6763s) observe two times the more more

[1:52:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6765s) regressions when we uh deploy that code

[1:52:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6771s) so where do bugs like these hide right

[1:52:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6774s) we want to detect these bugs before they

[1:52:56](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6776s) reach the code base and the way only way

[1:52:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6779s) to do that it's similar to how we write

[1:53:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6781s) design docs similar to how we draw

[1:53:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6784s) diagrams and flowcharts to make sure the

[1:53:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6786s) flow is set before we write any code. We

[1:53:08](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6788s) want to verify that without a human or

[1:53:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6792s) anyone reading these files as the first

[1:53:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6795s) reviewer.

[1:53:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6797s) In one sentence, let's say the ambiguity

[1:53:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6800s) and wording wrong level of detail, but

[1:53:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6803s) across sentences, we can observe

[1:53:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6805s) conflicts and gaps in the specification

[1:53:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6808s) or rules, right? Sentences need reveals

[1:53:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6811s) that need search and between them and

[1:53:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6814s) ambiguity searches.

[1:53:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6816s) So we have a three-step process to do

[1:53:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6819s) this where the LLM will first refine it.

[1:53:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6822s) It will try to clean up the wording on

[1:53:43](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6823s) its own and um if it succeeds then well

[1:53:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6827s) and good but if it cannot we then

[1:53:49](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6829s) formalize

[1:53:50](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6830s) the um English language into SMT

[1:53:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6834s) formulas. So SMT lib is a certain set of

[1:53:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6839s) type of function which we pass to a SAT

[1:54:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6841s) solver a satisfiability checker where

[1:54:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6844s) it's going to give out a boolean saying

[1:54:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6846s) this expression that you've given me is

[1:54:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6849s) valid true or false invalid

[1:54:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6853s) and then once the solver gets back to us

[1:54:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6855s) if that expression is valid then we

[1:54:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6857s) don't do anything. But if it detects any

[1:54:19](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6859s) ambiguity between two sentences or

[1:54:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6861s) within a sentence where there's two

[1:54:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6863s) meanings to a sentence, then we detect

[1:54:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6865s) that and tell the LLM to recheck that

[1:54:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6869s) sentence and it's going to reiterate on

[1:54:31](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6871s) that.

[1:54:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6873s) For example, the rules we saw,

[1:54:37](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6877s) we've seen when order is submitted and

[1:54:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6879s) inventory is unavailable, we shall place

[1:54:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6881s) the order as a back order. And in SMT

[1:54:45](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6885s) format, it kind of looks like this. This

[1:54:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6887s) is like a mass formula, right?

[1:54:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6894s) Once we go deeper, we

[1:54:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6897s) once we detect this, we also do a

[1:55:00](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6900s) three-step process again where we sample

[1:55:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6903s) the translations again and again. We ask

[1:55:05](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6905s) the LLM to translate it seven times or

[1:55:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6907s) 10 times and to understand whether this

[1:55:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6910s) LLM is behaving this way uh based on

[1:55:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6915s) its inherent capabilities or is

[1:55:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6917s) something affecting it to behave this

[1:55:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6918s) way and then based on logical

[1:55:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6921s) equivalence of these seven or 10 um

[1:55:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6924s) different set of interpretations by the

[1:55:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6926s) LLM we cluster them on logical

[1:55:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6928s) equivalence which sets which uh um

[1:55:33](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6933s) entries came under which uh assumptions

[1:55:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6936s) that the LLM made for itself and then we

[1:55:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6939s) accept or ask the user to clear out the

[1:55:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6942s) ambiguity or abstain from implementing

[1:55:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6944s) that in the codebase.

[1:55:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6951s) This is an example of asking the human

[1:55:55](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6955s) um what you want to do with that spec

[1:55:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6959s) rule that was um perhaps contradicting.

[1:56:02](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6962s) remove the record is very a very vague

[1:56:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6964s) statement. The LLM cannot can interpret

[1:56:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6967s) anything it wants but we shouldn't allow

[1:56:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6969s) that to happen and we either give two

[1:56:12](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6972s) options we keep it as is the record is

[1:56:14](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6974s) deleted or we retain it and but hide it

[1:56:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6977s) from the users which one does the user.

[1:56:23](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6983s) Um

[1:56:25](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6985s) a conflict is when the examples we

[1:56:27](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6987s) example we saw rule one it's conflicting

[1:56:29](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6989s) with rule three and a gap is where no

[1:56:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6992s) rule covers an idle order in this

[1:56:35](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6995s) example where the LLM detected an actual

[1:56:39](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=6999s) sorry

[1:56:41](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7001s) process or pipeline detected there's no

[1:56:44](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7004s) um entry for this rule where you are

[1:56:47](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7007s) missing something

[1:56:52](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7012s) all in Well, it cannot do a lot of

[1:56:54](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7014s) things. End of the day, we want to make

[1:56:58](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7018s) sure there is no oracle uh for for

[1:57:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7021s) specification correctness other than the

[1:57:03](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7023s) user. User needs to make sure to check

[1:57:06](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7026s) every part of the snippet part of the

[1:57:09](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7029s) rule book before sending it to the LLM.

[1:57:11](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7031s) And um we as a tool only can help them

[1:57:17](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7037s) and the user is more important here

[1:57:20](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7040s) because of implicit domain knowledge.

[1:57:22](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7042s) The LLM doesn't know a lot of domain

[1:57:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7044s) knowledge and there's no guarantee I

[1:57:26](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7046s) mean LLM only uh user can give that

[1:57:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7050s) guarantee right and there's thin

[1:57:32](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7052s) evidence right now for formalization and

[1:57:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7054s) how it can be used in agents we are

[1:57:36](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7056s) emerging in this technology

[1:57:42](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7062s) what do we take back from this um talk

[1:57:46](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7066s) check the spec always before you pass it

[1:57:48](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7068s) down to the agent uh cluster the

[1:57:51](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7071s) translation We what we do is we cluster

[1:57:53](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7073s) the translation by logical equivalent to

[1:57:57](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7077s) determine the different LLM

[1:57:59](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7079s) interpretations and where it's genuinely

[1:58:01](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7081s) going wrong. The LLM translates the

[1:58:04](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7084s) solver checks and the human decide. We

[1:58:07](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7087s) give give the human uh options and if

[1:58:10](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7090s) there's no answer to that we use LLM

[1:58:13](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7093s) judges or abstain from implementing that

[1:58:15](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7095s) piece.

[1:58:18](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7098s) Here are the references and um this work

[1:58:21](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7101s) has been majorly contributed by my team

[1:58:24](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7104s) um Anda Jin, Stefan, Nia and Delmos. You

[1:58:28](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7108s) can check out their blog in the website

[1:58:30](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7110s) link provided and um del deeper into

[1:58:34](https://www.youtube.com/watch?v=ZZ19zhYnDKY&t=7114s) this. Thank you.
