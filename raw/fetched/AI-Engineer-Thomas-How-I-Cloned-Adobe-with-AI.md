---
title: How I cloned Adobe with AI — Brandon Thomas, ArtCraft
description: AI Engineer CODE 2026 官方閱讀版，Brandon Thomas 談用 agent 以 Rust 重做 Adobe 等應用並開源，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/brandon-thomas
published: 2026-11-12
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 shitification 應為 enshittification、NDesign 應為 InDesign、cloud code 應為 Claude Code）。閱讀頁場次名為 Let's Open Source the World，逐字稿對應 Day 2 直播 `https://www.youtube.com/watch?v=y9JtCCZP2MQ`（1:20:53–1:40:19）；剪輯單場版 `https://www.youtube.com/watch?v=UCL4K36SHp0`，YouTube 標題為 How I cloned Adobe with AI — Brandon Thomas, ArtCraft（AI Engineer 頻道，長度約 19:55，與直播區段長度相符；搜尋索引中舊標題為 Let's Open Source the World）。演講日 2026-11-12（官方議程 Thursday, November 12 · Main stage）。

Day 2 livestream · [1:20:53–1:40:19 on YouTube](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4853s). The player starts and stops at this session’s boundaries.

## Introduction

**Brandon Thomas**, CEO of ArtCraft, describes how agent-built creative applications turned into an open-source effort to give users more control over their tools.

Thomas arrives after a month in which a project he had not yet posted to Hacker News escaped into the wider internet. His team had built applications resembling familiar creative tools, including an image editor, and the response brought developers, artists, feature requests, and an unexpected volume of attention.

The talk is partly an account of that response and partly an argument about what it could enable. Thomas wants people to own and modify the applications they depend on. Coding agents, in his view, change who can participate in that modification.

[1:23:04 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4984s)

## Reopen the places where people used to build

Thomas begins at [01:23:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4984s) with his memory of the early web: self-hosted chat servers, third-party messaging clients, customizable pages, file ownership, and mashups built from public APIs. He contrasts that with a later world of consolidated platforms, restricted interfaces, and recurring licenses.

This is his framing of the change, not a complete history of the web. The distinction he cares about is the user's ability to act. A protocol or editable application leaves room for someone to build a new workflow. A closed product may leave that person waiting for its vendor to prioritize the same need.

His experience with artists made the question concrete. ArtCraft began with tools for professional creative work, placing generated files on the desktop alongside the editor rather than keeping the entire workflow in a web service. Thomas's advisers questioned whether artists cared about open source. Customers then started adapting the software with coding agents.

[1:28:28 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5308s)

## The user may want a smaller application

At [01:28:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5308s), Thomas describes studios with specialized delivery processes that no general-purpose product was likely to serve exactly. Someone on the team could use an agent, APIs, and existing components to construct a tailored interface.

This creates a different reason for open source. The customer need not want to become a maintainer or understand every implementation detail. They may want to remove most of an application's visible complexity and retain the pieces relevant to one role in a production pipeline.

Thomas imagines separate, constrained versions for different artists on the same team. One application need not expose every tool to every person. The value comes from shaping the software around the work rather than teaching everyone to navigate the same large interface.

[1:29:32 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5372s)

## Start with familiar behavior, then make it programmable

The team's image-editor experiment, discussed at [01:29:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5372s), used a large specification. It separated interface concerns from underlying functionality, asked for plans for individual tools, covered data structures and importers, and required CLI and MCP access.

Thomas reports that the first day produced a functional approximation that surprised the team. He explicitly distinguishes that result from full feature parity. The familiar appearance helped artists apply existing muscle memory, but it did not establish that every workflow or file format already behaved like the original product.

That was a deliberate sequence. First reproduce enough recognizable behavior to demonstrate useful capability; later explore new interfaces that are more directly agent-driven. A familiar interface is a bridge for existing users, while command-line and MCP access create a second path for automation.

The response also challenged a simple division between artists and AI users. Thomas says people who had resisted other uses of AI were willing to try tools that gave them more control, and some began providing bug reports and feature requests. He presents that as an opportunity to teach agentic workflows through a tool they already want to use.

[1:35:22 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5722s)

## A shared base can support many kinds of applications

The project expanded across image editing, page layout, video, audio, CAD, office documents, and collaborative design. Thomas describes both applications built by his team and projects growing through community contributions. The aim is broader than making isolated lookalikes: the community is decomposing the work into reusable two-dimensional, three-dimensional, and interface components.

At [01:35:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5722s), he emphasizes consequences for underserved users. Native desktop distribution can reach operating systems that commercial creative software does not serve. Localization and continued maintenance can matter to people whose language or established workflow is no longer a vendor's priority.

These are claims about the project's direction and adoption as Thomas presented them. A long catalogue of applications is not proof that each is production-ready for every professional workflow. His own distinction between approximation and parity remains important as the scope grows.

[1:37:00 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5820s)

## Native software moves the bottleneck

[![Brandon Thomas's slide lists native performance, installer size, memory footprint, memory safety, defect rate, and cold start as reasons for choosing Rust.](https://ai.engineer/reading/code-2026/images/brandon-thomas-5820.jpg)](https://ai.engineer/reading/code-2026/images/brandon-thomas-5820.jpg)

*The [slide at 1:37:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5820s) shows the team's selection criteria for Rust. It is Thomas's architectural argument, not a benchmark establishing that every Rust application wins each comparison.*

Thomas credits Rust with making the applications responsive, portable, and suitable for rich native interfaces. He also notes the ability to target the web through WebAssembly. Coding agents lower the barrier for teammates who have not previously worked in the language, while compile times remain a practical cost.

The workload then puts pressure on infrastructure around development. He describes CI capacity falling behind and the team arranging its own machines. Generating changes faster does not make compilation, testing, hosting, or coordination disappear.

His advice about autonomy depends on the kind of change. He reserves more direct human involvement for backend design, API decisions, and schema migrations, where mistakes can impose lasting costs. He is more willing to let agents iterate aggressively on desktop applications and games. That is his operating preference, not a guarantee that such projects are consequence-free.

[1:38:33 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5913s)

## Put the development process in the open too

Near [01:38:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5913s), Thomas describes Autocraft, a code-defined system for ingesting issues, triaging them, running agentic development, and retaining decisions for evaluations and post-training. He says it will be open sourced; the talk presents that release as forthcoming rather than already completed.

The ending connects the infrastructure to the original motivation. Open applications are easier to adapt when the process that maintains them is also available. Thomas wants users to move from renting an unchangeable tool to shaping their own application, and from rebuilding alone to contributing reusable parts that let the next person start further ahead.

Full transcript 371 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[1:20:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4856s) I had to put this together late last night.

[1:20:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4858s) I've been in a whirlwind after this project went viral

[1:21:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4861s) of unblocking thousands of open source developers.

[1:21:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4865s) We've had VCs approaching us.

[1:21:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4867s) I've been in constant meetings.

[1:21:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4869s) This has been a sleepless month of activity since this happened.

[1:21:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4874s) So if you're not familiar, I kind of cloned Adobe Photoshop

[1:21:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4878s) and a bunch of other apps, and that went super viral.

[1:21:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4882s) My phone, my inbox, everything has just been absolutely lit up.

[1:21:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4886s) And so I apologize for the structure of the talk.

[1:21:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4891s) This was thrown together as quickly as I can,

[1:21:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4893s) but I've got a lot of really exciting stuff to talk about.

[1:21:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4895s) And I think it talks about the future of not only the industry,

[1:21:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4900s) but just technology as a whole.

[1:21:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4902s) So we're going to open source the entire world.

[1:21:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4905s) Like, why not?

[1:21:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4906s) It's something that I've always wanted to do as a developer.

[1:21:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4910s) That's something that a lot of us in the open source community are interested in.

[1:21:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4914s) Open source powers a lot of the technology that we're familiar with,

[1:22:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4920s) but it's never been at the forefront.

[1:22:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4922s) Linux has always been a second-class citizen.

[1:22:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4924s) We've been pulled into a whole bunch of platforms where we don't really have ownership.

[1:22:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4929s) And AI kind of gives us a chance to take the web back, if you will.

[1:22:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4935s) So I might have to do this manually.

[1:22:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4940s) Cool.

[1:22:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4941s) So a little bit about myself.

[1:22:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4942s) I've been an engineer for about 15 years.

[1:22:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4945s) I spent eight years at Square doing heavy-hitting infra,

[1:22:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4949s) so online payments, the authentication stack,

[1:22:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4954s) basically anything that could take down the company,

[1:22:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4956s) my team was kind of in charge of,

[1:22:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4957s) and it was eight years of carrying the pager,

[1:22:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4959s) a lot of really heavy-hitting infrastructure work.

[1:22:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4962s) And then I've spent seven years doing startups,

[1:22:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4964s) and that's a whole different world.

[1:22:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4966s) It's a lot of risk, a lot of learning what the market needs,

[1:22:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4969s) a lot of correcting your own assumptions.

[1:22:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4972s) And I've also been, I'm based in Atlanta.

[1:22:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4975s) It's a big film state.

[1:22:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4976s) I've been very big in the arts.

[1:22:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4978s) So out of college, made lots of films,

[1:23:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4981s) built laser projectors that play video games

[1:23:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4983s) on the side of skyscrapers, that kind of thing.

[1:23:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4984s) And those are the sort of customers that our startups

[1:23:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4988s) or the startups that I built have catered to,

[1:23:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4990s) creatives, artists, filmmakers, and so forth.

[1:23:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4994s) I want to transport everybody back in time,

[1:23:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4997s) back to the very beginnings of the web and the Internet,

[1:23:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=4999s) the 90s, the early 2000s.

[1:23:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5003s) So for us millennials, we're going to feel old.

[1:23:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5006s) And for everybody that's younger,

[1:23:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5009s) just let me kind of set the stage for what the Internet was like.

[1:23:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5013s) We had a bunch of chat applications that were completely open.

[1:23:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5016s) So IRC is like Discord,

[1:23:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5018s) but you can spin up your own servers that you actually own.

[1:23:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5020s) You can use whatever programs to automate them and interrogate them.

[1:23:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5024s) without rules. All of the commercial messaging apps were basically, they didn't care if you

[1:23:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5030s) used third-party tools to connect to them. Every website had data exports. They had APIs.

[1:23:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5036s) You could literally build really cool mashups with Reddit and Flickr and Twitter. And these

[1:24:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5041s) were like trending on Slashdot before Hacker News was a thing. And then, you know, in the

[1:24:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5047s) more modern times, these kind of trickled down to a much slower pace because the APIs

[1:24:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5053s) got got removed. There's a bunch of file sharing. So not not just file sharing, you can actually

[1:24:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5059s) buy mp3s and feel a sense of ownership and and everything that you were doing on the

[1:24:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5063s) web. And now it's more licensing. There was so much open creativity because largely the

[1:24:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5070s) people on the internet were technical. They were early adopters. So flash kids were making

[1:24:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5075s) all kinds of animations. There were diffuse communities with PHP, PHP BB and envision

[1:24:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5081s) and just a ton of creativity that was happening at the time.

[1:24:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5086s) Wikipedia got started sort of in this ethos,

[1:24:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5089s) and we don't really see this kind of stuff anymore

[1:24:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5092s) in the current era and incarnation of tech.

[1:24:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5095s) Websites were highly customizable.

[1:24:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5098s) Like MySpace at the time, you could actually change the HTML and CSS

[1:25:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5101s) and make it look however you want.

[1:25:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5103s) So this was a totally different alien time

[1:25:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5107s) compared to what we have today.

[1:25:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5111s) When Web 2.0 happened, broadband, smartphones, it brought everybody into the fold.

[1:25:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5115s) So the technical people got sort of pushed to the sidelines.

[1:25:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5118s) And it's not a bad thing.

[1:25:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5120s) Like, we needed our parents and our grandparents to be able to use these products.

[1:25:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5123s) But we sort of, we rounded the edges on things.

[1:25:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5126s) We took away all the technical pieces.

[1:25:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5127s) We made everything easy for people to adapt because they couldn't contribute from a technical footing.

[1:25:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5133s) They didn't want to unpackage things.

[1:25:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5135s) They didn't know what APIs were.

[1:25:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5136s) And so the platforms and the protocols got replaced by platforms,

[1:25:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5141s) and they sort of grabbed as many users as they could.

[1:25:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5146s) And sort of the diffuse experimental early web started to disappear.

[1:25:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5149s) The APIs got taken away from us,

[1:25:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5152s) and then we started seeing distribution being gatekept by the big providers.

[1:25:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5157s) Like, we never once had a phone ecosystem where we could freely distribute to,

[1:26:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5163s) like we could on the desktop.

[1:26:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5166s) things started to cost more and more as startups began to like win market share they realized that

[1:26:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5173s) they had pricing power and suddenly your Netflix actually became cable once you started subscribing

[1:26:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5178s) to all the streaming services and then they started to get very extractive for companies

[1:26:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5184s) that maybe maybe hit the limits of their growth they started coming up with crazy crazy gotchas

[1:26:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5189s) So the one that got me is Adobe has this, you can subscribe to a monthly plan, and they don't tell you this.

[1:26:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5197s) It's in like the very small print.

[1:26:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5198s) If you cancel your monthly plan before the 12 months or 18 months, they actually charge you up to like $200 to unsubscribe,

[1:26:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5206s) which is really inconvenient if you're going to a film festival like once a year making a short film,

[1:26:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5211s) and then suddenly you've got an extra $200 bill for an application that you were just using over a weekend.

[1:26:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5216s) And that's hit so many people, and it's really frustrating.

[1:26:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5219s) that the web that was once really, really promising and open and free

[1:27:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5225s) has turned into this extractive, owned, rented, rent-seeking world.

[1:27:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5234s) So it used to be a very special place in the 90s and the 2000s,

[1:27:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5239s) and more and more has been extracted.

[1:27:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5243s) This is a term that's commonly used in shitification.

[1:27:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5247s) I think that aptly describes everything that happened.

[1:27:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5252s) Our company started with the ethos of let's build everything open source.

[1:27:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5256s) Like the applications that we built in the AI space were 100% open,

[1:27:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5261s) not only the desktop apps, but the actual infrastructure as well.

[1:27:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5264s) So Artcraft originally started as sort of like a professionally-minded Higgs field.

[1:27:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5269s) So all of the filmmakers that I know and that I've grown up with,

[1:27:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5273s) we were making a product for them to use rather than a UGC-centered approach,

[1:27:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5277s) like Higgs field or OpenArt or so forth have.

[1:28:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5282s) And that enabled us to give them a desktop tool that lived on their machine

[1:28:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5287s) where all the files that they were generating lived right next to their editor.

[1:28:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5291s) And one of the things that we observed, and my advisors thought I was absolutely crazy,

[1:28:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5296s) that artists, you know, they don't know what open source is.

[1:28:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5298s) They don't need it. They don't talk about it.

[1:28:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5300s) You know, GIMP isn't really used by artists.

[1:28:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5302s) we actually observed artists vibe coding their own workflows on top of the software that we gave them.

[1:28:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5308s) And that is something that was brand new to all of us.

[1:28:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5311s) There were micro drama studios that were doing order fulfillment for some of the top micro drama startups.

[1:28:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5318s) They would do 30 to 50 grand of fulfillment every single month.

[1:28:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5321s) And they had big teams and no product out there fits their needs.

[1:28:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5325s) Nobody's going to go and workshop and build that specifically for the type of delivery that they need.

[1:28:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5330s) Yet they in-house have people that know cloud code and they can take the APIs and they can generate an interface that's like that

[1:28:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5337s) So we started experimenting with completely open source giving it to our customers

[1:29:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5341s) And they really responded to that and then we thought

[1:29:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5345s) What if we could turn back time on everything like all of these things that they're consuming and building would be much more friendly and

[1:29:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5353s) And give them way more capacity to create if all of the infrastructure was open source

[1:29:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5359s) if all of the application shapes that they wanted to leverage were open source?

[1:29:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5364s) Like, they use Premiere. They use Adobe.

[1:29:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5366s) Like, what could we do to give them something that they could actually take away

[1:29:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5370s) all of the surface area that they don't use

[1:29:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5372s) and constrain the apps to their specific workflow?

[1:29:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5375s) What would it look like if they could do that, you know,

[1:29:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5378s) five or ten times for each different artist on their team

[1:29:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5381s) that's doing a particular part of that workflow?

[1:29:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5383s) And so we wanted to kind of undo what had happened during Web 2.0

[1:29:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5388s) and everything became owned and consolidated and gatekept

[1:29:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5394s) and just give people back their applications.

[1:29:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5396s) And AI really is the means for us to

[1:30:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5400s) do that.

[1:30:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5400s) So we took a stab at the Adobe Creative Suite. We looked at Photoshop first. We basically

[1:30:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5407s) prompted, you know, this is the basic shape of a photo editing app. You've consumed and

[1:30:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5413s) trained on all of the tutorials about what Photoshop is. That's in your training data.

[1:30:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5418s) laid out a large, large prompt to say, let's build out the application. Let's separate

[1:30:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5424s) the UI UX from that.

[1:30:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5426s) Let's make everything MCP and CLI compatible.

[1:30:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5429s) Let's build out plans for every single tool,

[1:30:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5432s) how all of those work.

[1:30:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5433s) Let's talk about the data structures,

[1:30:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5435s) the file format importers.

[1:30:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5436s) We basically built these large prompts.

[1:30:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5438s) And within 24 hours, we were looking

[1:30:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5440s) at a pretty good approximation of what Photoshop was.

[1:30:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5444s) And it kind of blew our minds away.

[1:30:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5447s) It was functional.

[1:30:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5449s) It was very familiar to us.

[1:30:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5450s) It started 10 times faster than the original Photoshop.

[1:30:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5453s) Now, we didn't actually cover the entire surface area of Photoshop.

[1:30:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5457s) There's a lot of work. We're still not at 100% parity.

[1:31:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5460s) But we're measuring ourselves against what needs to be done,

[1:31:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5463s) and we're getting closer and closer.

[1:31:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5465s) We were at 50%. We've just passed 60%.

[1:31:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5468s) And in the fullness of time, like Pareto principle,

[1:31:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5471s) we could reach 99.99% parity.

[1:31:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5475s) I'm going to take a little bit of a diatribe.

[1:31:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5478s) Our team has talked about whether we take this further now

[1:31:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5480s) or whether we just go for parity.

[1:31:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5481s) And right now, we want to fulfill the muscle memory of all the artists that use Adobe.

[1:31:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5488s) So we are going for Adobe, like their sort of interface and look and feel directly.

[1:31:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5492s) In the fullness of time, we will build net new apps that have new interfaces that are more agentic.

[1:31:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5497s) But we wanted to do that also as sort of like a proving function,

[1:31:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5500s) that we have actually accomplished something real, completely agentically.

[1:31:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5504s) So we did Photoshop. We did basically all of their apps.

[1:31:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5510s) We did InDesign.

[1:31:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5511s) We did Premiere.

[1:31:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5514s) And this, I did not expect this to go viral.

[1:31:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5518s) I was withholding posting it on Hacker News.

[1:31:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5519s) It got out on Reddit.

[1:32:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5521s) And then, like, two days later,

[1:32:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5522s) like, New York Times was asking me for an interview.

[1:32:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5525s) And our Discord went from 3,000 people to,

[1:32:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5527s) it's now got more people in our Discord

[1:32:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5529s) than Jev, Suno, Higgsfield.

[1:32:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5533s) I'm still struggling to bear with what has happened.

[1:32:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5535s) This was, it struck a nerve with people.

[1:32:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5537s) They've felt sort of maligned by Adobe

[1:32:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5539s) be in other tech companies.

[1:32:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5541s) And what we've built has really resonated with them.

[1:32:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5544s) And it's sort of built up this mission to build more.

[1:32:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5548s) So all of the anti-AI artists who have been pushing back

[1:32:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5551s) against AI all of this time, they've sort of turned around.

[1:32:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5555s) We actually love what you're doing.

[1:32:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5558s) They've started using these apps.

[1:32:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5559s) They've started giving us feature requests and bug reports.

[1:32:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5562s) And we're engaging them.

[1:32:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5564s) And I think we're going to be able to teach them

[1:32:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5566s) this is what an MCP is.

[1:32:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5567s) This is how you agentically create things.

[1:32:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5569s) And maybe we'll start pulling away some of these bloated interfaces

[1:32:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5572s) and giving them things that are faster, more fluid,

[1:32:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5575s) and let them do their work faster.

[1:32:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5577s) So we didn't stop with those apps.

[1:32:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5579s) We've done all kinds of stuff.

[1:33:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5580s) We've done CAD.

[1:33:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5581s) We've done Flash.

[1:33:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5585s) We've done a bunch of digital audio workstations.

[1:33:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5589s) It's not just us.

[1:33:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5590s) It's the community doing these things as well.

[1:33:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5592s) And there's really no limit in terms of what can be done.

[1:33:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5595s) So we've done the entire Microsoft,

[1:33:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5597s) well, the core apps within the Microsoft Office,

[1:33:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5599s) Suite, there's been Google Docs.

[1:33:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5601s) We have companies and universities and all sorts of people

[1:33:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5605s) approaching us wanting to use these things.

[1:33:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5607s) And we're basically trying to fulfill

[1:33:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5610s) all of these different asks.

[1:33:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5611s) They're being used on Linux, where they've never

[1:33:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5614s) been used before.

[1:33:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5616s) PDFcraft is probably the best app.

[1:33:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5617s) You should all go download it right now.

[1:33:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5618s) You'll never have to use Acrobat again.

[1:33:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5620s) This is really fast, really smooth.

[1:33:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5627s) It works on Linux.

[1:33:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5629s) It works on NetBSD.

[1:33:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5630s) It's brilliant.

[1:33:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5631s) This one's ready to go.

[1:33:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5632s) So go ahead and get this one.

[1:33:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5635s) We did Figma.

[1:33:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5636s) We've actually done the server component for this, too.

[1:33:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5638s) And you can basically have your team collaborate on documents.

[1:34:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5642s) It's got the wrapped Paxos multi-user setup.

[1:34:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5646s) So we're starting to go into infrastructure, too.

[1:34:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5648s) And the entire infrastructure and data model, all of it, is open source.

[1:34:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5651s) We're not keeping any of it proprietary.

[1:34:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5655s) There's a community that's working on SolidCraft that's led by engineers.

[1:34:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5658s) They've actually got an open engineering kernel that manages all of this.

[1:34:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5664s) And it's really solid.

[1:34:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5666s) Like the MCP, you can actually do 3D printing projects really quickly with SolidCraft.

[1:34:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5672s) We've had so, so much happen.

[1:34:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5674s) We've got over 300,000 GitHub stars.

[1:34:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5678s) 4,000 different people have been contributing to this project, and it's picking up.

[1:34:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5683s) It's actually become sort of a movement, if you will.

[1:34:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5686s) And we're trying to adapt to how much influx of people

[1:34:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5690s) trying to contribute to this.

[1:34:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5691s) I'm going to pick up the pace, because I've

[1:34:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5692s) been kind of lagging on this.

[1:34:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5693s) But we're getting about 1.7 million downloads a day.

[1:34:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5697s) And this is accelerating.

[1:34:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5698s) We've got a launcher app that puts us on the desktop.

[1:35:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5700s) And you can basically manage everything here.

[1:35:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5703s) It works on all operating systems.

[1:35:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5706s) A quarter of our users are on Linux, which is really

[1:35:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5709s) fascinating.

[1:35:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5709s) Linux has been historically really, really underserved,

[1:35:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5712s) and now they have super high-quality professional apps

[1:35:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5717s) for creative and office work, which is really nice.

[1:35:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5722s) So we love and respect all of the work

[1:35:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5726s) that's been done there in the past,

[1:35:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5727s) but people are really excited to use the apps

[1:35:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5729s) that they didn't have access to.

[1:35:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5732s) All of these things are MCP and CLI first class.

[1:35:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5735s) You can totally command these,

[1:35:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5737s) and you can watch them build and assemble creative projects right in front of you.

[1:35:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5741s) They've been localized into languages that were never officially supported by Adobe or Microsoft.

[1:35:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5747s) We were told that Arabic was not supported in NDesign.

[1:35:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5751s) We've also supported these apps past their support lifecycle.

[1:35:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5755s) Adobe Animate was being end of life, or it was being put on life support.

[1:36:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5760s) We've picked that up.

[1:36:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5761s) We've had basically animation studios come to us saying,

[1:36:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5763s) we use this for our jobs.

[1:36:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5765s) This is important.

[1:36:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5766s) Please, please support this.

[1:36:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5768s) So a lot of really fascinating things are happening

[1:36:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5771s) where we're getting this into more places

[1:36:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5773s) than they've ever been before.

[1:36:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5774s) And it's definitely not me.

[1:36:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5776s) Like, I started this, and now we've got a community

[1:36:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5778s) of, like, 4,000 developers.

[1:36:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5780s) This has taken on a life of its own.

[1:36:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5782s) They are doing everything from CI, CD.

[1:36:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5784s) It's incredible.

[1:36:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5785s) This is way bigger than just me.

[1:36:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5787s) I really got to pick up the pace here.

[1:36:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5789s) I've made way too much content.

[1:36:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5790s) So there are over 300 apps being developed by the community.

[1:36:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5794s) We've developed an app where non-technical people can start contributing and use the

[1:36:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5799s) basis of the apps that we've created, like the UI, UX libraries.

[1:36:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5802s) We're decomposing this into all of the components and primitives so that you can reuse them.

[1:36:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5806s) So you'll have nice 3D libraries, nice 2D libraries.

[1:36:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5810s) It's all great.

[1:36:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5811s) I'll get into the technical stuff.

[1:36:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5813s) So Rust was probably essential in this product's success.

[1:36:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5818s) We'd seen people do it at Electron before, but for high-quality, creative apps, you really

[1:37:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5822s) need something that's native.

[1:37:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5824s) There's just a lot of really, really good quality things

[1:37:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5827s) about Rust.

[1:37:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5828s) Google had papers about the low defect rate.

[1:37:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5831s) It starts really fast.

[1:37:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5832s) It's the best language for this.

[1:37:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5838s) It supports all different platforms and operating systems.

[1:37:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5843s) We've got this on NetBSD.

[1:37:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5844s) We've got this on tablets.

[1:37:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5845s) It natively deploys to the web via Wasm.

[1:37:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5849s) so it can get anywhere and everywhere.

[1:37:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5852s) Do you need to know Rust to start using Rust today as an engineer?

[1:37:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5857s) Definitely not.

[1:37:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5858s) I've been using Rust since pre-1.0 times,

[1:37:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5860s) but everybody on the team,

[1:37:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5861s) it's a mix of people that have never experienced the language before.

[1:37:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5864s) Your agents will drive it just fine.

[1:37:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5866s) You're not going to have any trouble.

[1:37:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5867s) It is a fantastic language.

[1:37:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5868s) The one big thing you're going to run into is compile times.

[1:37:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5872s) Is it GUI yet?

[1:37:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5873s) There's this famous series of websites in the Rust world.

[1:37:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5877s) Does it support modern features?

[1:37:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5878s) Yes, you can build rich GUI apps in Rust, UI, UX.

[1:38:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5882s) We've run into a lot of gotchas, like permissions,

[1:38:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5884s) GitHub, scaling, CI.

[1:38:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5886s) A lot of people talked about that.

[1:38:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5887s) I'm going to just speed through this,

[1:38:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5888s) because I'm kind of running out of time.

[1:38:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5889s) CI is falling over.

[1:38:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5892s) We've been spinning up our own.

[1:38:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5894s) We found a good place to get RAM on co-located servers.

[1:38:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5896s) We're moving to that.

[1:38:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5897s) This is a good one.

[1:38:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5898s) So agentic develop versus human review.

[1:38:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5901s) If you're doing back-end work or things that require schema

[1:38:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5904s) migrations, API design, let your humans do that.

[1:38:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5906s) But for like desktop apps and games and anything that's basically immutable, throw your agents at it and give them like full confidence

[1:38:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5913s) You don't need to be human in the loop fully like the upstream like directing where things go

[1:38:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5916s) Just just let it run tell it to build things somebody in our community is is building

[1:38:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5920s) They've got 40 machines rebuilding unreal engine in rust. So you don't even have to mind these things

[1:38:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5929s) Autocraft is a completely autonomous software factory that we're going to open source it ingest issues it triages them

[1:38:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5935s) It does agentic development.

[1:38:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5936s) It post trains and evals on all of the decisions.

[1:38:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5939s) This will be open source soon.

[1:39:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5941s) Basically, we've got an entire app factory that's designed in code.

[1:39:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5944s) You can express this.

[1:39:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5946s) We'll open source this soon.

[1:39:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5947s) I'm just going to have to hurry because I'm over time.

[1:39:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5949s) Injust issues.

[1:39:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5952s) This is open source code rabbit, open source all the things.

[1:39:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5955s) We're doing a lot here.

[1:39:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5956s) And I thought I would save more time for the technical.

[1:39:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5960s) But this is really good.

[1:39:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5960s) And please, please look out for this.

[1:39:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5963s) It will support all of your agentic development.

[1:39:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5965s) It supports all of the crafting and curating

[1:39:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5968s) how you approach a project.

[1:39:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5969s) It keeps your engineers on task.

[1:39:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5972s) Again, fully open source.

[1:39:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5973s) All of the decisions made by it are training data

[1:39:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5976s) that we're going to use for evals and post-training

[1:39:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5978s) on the decision trees.

[1:39:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5980s) Let's take back the entire internet.

[1:39:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5982s) Let's rebuild everything.

[1:39:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5983s) All software, all platforms.

[1:39:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5992s) We can turn all of these things into proper protocols.

[1:39:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5996s) We can open source the entire world.

[1:39:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=5998s) Let's own our apps, our infra,

[1:40:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6000s) our protocols, our models, all of it.

[1:40:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6004s) We are hiring, so if anybody's interested and wants to work on 100% open source,

[1:40:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6008s) none of our code is closed source. All of it is in the open.

[1:40:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6012s) You get time to work on your own projects, just reach out to me at hello at storyteller.ai.

[1:40:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6016s) And thank you so much, everybody.
