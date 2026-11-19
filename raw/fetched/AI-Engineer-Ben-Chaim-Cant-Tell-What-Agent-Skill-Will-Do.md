---
title: You Can't Tell What an Agent Skill Will Do by Reading It — Roey Ben Chaim
description: AI Engineer 官方閱讀版：Roey Ben Chaim 談在沙箱實跑數千個 agent skill 與 Paperclip 仿冒竊密案，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/_7P580m4kPY-you-cant-tell-what-agent-skill-will
published: 2026-11-10
tags:
  - clippings
  - skill
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript 下載 API，JSON 轉純文字並每六句加時間碼）。逐字稿內有多段官方插入的 `[Editorial paraphrase]` 改寫，與講者原話混排，且含辨識錯誤（如 Vercel 寫成 Versell、detonation chamber 寫成 detonation shaver）。對應 YouTube 影片 ID `_7P580m4kPY`（`https://www.youtube.com/watch?v=_7P580m4kPY`，上傳日 2026-11-10，長約 14 分半）。

Loading slides…

Read the talk

## You Can't Tell What an Agent Skill Will Do by Reading It

![A task prompt and a skill feed an agent in an isolated environment. The agent’s messages and tool results form a trace for assessing the run.](https://www.ai.engineer/api/talk-essay-media/b6fa6907faeed9a9af51278f0b835e6971d05b7b6dd4b306a761dd2dd4832edc)

The team began with an isolated agent, a skill and a task, then examined what the agent did.

Roey Ben Chaim and the Zenity team ran thousands of agent skills in a detonation chamber. To understand a single run, they had to give the skill a plausible task and follow its effects from the agent’s tool call to the files and services a child process touched.

From a talk by [Roey Ben Chaim](https://www.ai.engineer/speakers/roey-ben-chaim)

At a glance

### Ideas worth remembering

- Interpret a sensitive read in the context of the task and the destination of the data. The Azure diagnostic and the Paperclip lookalike called for different conclusions once the researchers could account for the observed activity.
- A sandbox run tests a particular path. Supplying a missing service makes the path possible, and asking for snapshot recovery exercises different behavior from asking for a deployment.
- Keep the agent trace alongside process creation, filesystem and network records. A single package installation can account for multiple actions that never appear as separate model tool calls.

01 [0:03 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=3s)

### What does a sensitive read actually tell you?

An official Azure diagnostic checked the identity and configuration of a cloud environment. An information stealer might also look for sensitive information on that machine. If a security reviewer saw only the access event, how could they distinguish legitimate troubleshooting from credential theft? Roey Ben Chaim, a staff engineer at Zenity and a MATS research fellow, opens with this ambiguity. Even knowing which product supplied the skill leaves an investigator with the job of explaining what happened on a particular run.

A skill gives an agent a capability on demand. Someone else supplies the instructions, resources and sometimes executable code. That leaves anyone adopting a skill with two questions. What work did it cause the machine to do? Does that work make sense for the task the user gave it? Even a trace that answers the first question can leave the second open.

[0:55](https://www.youtube.com/watch?v=_7P580m4kPY&t=55s) [0:59](https://www.youtube.com/watch?v=_7P580m4kPY&t=59s)

02 [1:38 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=98s)

### What a scan of SKILL.md can miss

A skill can depend on packages, instructions or services outside its initial file. A reviewer examining the installed document sees what the author provided at that moment. The agent may encounter different material when it uses the skill. A thorough investigation needs to identify what influenced the run, including dependencies the user never selected directly.

Ben Chaim cites work by Trail of Bits in which an automated reviewer accepted a misleading explanation for a software change. The same material offered both the proposed change and the claim that somebody had authorized it. A reviewer needs an independent source for that assertion. Reading more words from the same source cannot establish who approved a change.

[1:49](https://www.youtube.com/watch?v=_7P580m4kPY&t=109s) [1:51](https://www.youtube.com/watch?v=_7P580m4kPY&t=111s)

03 [2:49 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=169s)

### Give the skill somewhere to run and something specific to do

![A highlighted world builder points to the isolated environment where the agent uses the skill. The task prompt, agent trace and assessment remain visible.](https://www.ai.engineer/api/talk-essay-media/610979bf10edeb181e360a8983c369c2c003771f696a252820125073f66f2a2b)

The world builder supplied the services and project context a skill expected.

Zenity borrowed detonation from malware research. The team put an agent and a skill in a sandbox, supplied a task prompt, let the agent work for minutes or hours, then examined its trace. The first version ran into a mundane problem. Many skills expected a command-line tool, a service or an existing project. A Notion skill in an empty sandbox has no Notion service to talk to. A run that stops there tells you little about what the skill does once it connects.

The team added a **world builder** that reads the skill and prepares the environment it expects. That addressed one reason a run could stall. The next was the assignment itself. A presentation skill needs a deck to make, a deployment skill needs a service to ship, and a brainstorming skill needs an idea to explore.

Even asking the agent to ship a service leaves choices. Configuring the service, deploying it and recovering it from a snapshot exercise different parts of the skill. A successful deployment says little about the recovery path. The team added an **operator** that reads the skill, identifies routes worth exercising and supplies prompts for them. Coverage depends on which routes the operator recognizes and which ones the agent follows.

A model can also stop in the middle of a test. Some agents declined to continue when a step looked unsafe. That is an observation worth retaining alongside the task and environment. It narrows what the team can conclude from that run. Ben Chaim notes that legitimate tasks can trigger a safeguard, too. Treating every refusal as proof of malice would misclassify some skills; treating an unfinished test as evidence of safety would hide what the researchers had yet to observe.

[2:53](https://www.youtube.com/watch?v=_7P580m4kPY&t=173s) [2:57](https://www.youtube.com/watch?v=_7P580m4kPY&t=177s)

04 [5:59 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=359s)

### Look below the model’s tool call

![The agent trace and three sources of activity from the isolated environment feed an analysis that links an instruction to its execution and observed effect.](https://www.ai.engineer/api/talk-essay-media/445a787a2d562e05f667fa18d72bcefad4cef0ad0076a749f5ef021528c12981)

The research environment joined host-level observations to the agent trace.

Suppose the agent trace shows a single installation. Can an investigator use that entry to say which files were touched? Some of the work happens outside the model’s conversation. Processes started during installation may have effects that the agent never describes. The model can report that its request succeeded without knowing the consequences for the rest of the machine.

The chamber kept the agent trace and added three kinds of evidence. Process creation events showed what the installer launched. Filesystem events showed what those processes touched. Network packet capture recorded their traffic. Together the records let an investigator work back from a file access or an outbound connection to the installation that set it in motion.

[6:08](https://www.youtube.com/watch?v=_7P580m4kPY&t=368s) [6:13](https://www.youtube.com/watch?v=_7P580m4kPY&t=373s)

05 [7:07 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=427s)

### The dependency the user never chose

In a harmless proof of concept by Zach Corman, the skill a user chose drew in another component. The first file gave no clear account of the behavior that followed. The chamber’s records let the researchers attribute the later action to an indirect dependency. A single successful test established a concrete possibility. It did not establish what every installation would do.

Across thousands of skills examined, Ben Chaim reported that the team identified 100 malicious skills and that those skills were taken down from `skills.sh`. That count describes findings in the collection the team examined. It leaves open how many malicious paths the chamber missed.

In another case, a skill appeared to use a Polymarket dependency. Its package identity differed slightly from the expected one, and the researchers traced it to an unofficial source. Inspection showed that the substituted software collected sensitive information. The meaningful comparison was between the dependency a user believed they had chosen and the one the installer actually supplied.

[7:07](https://www.youtube.com/watch?v=_7P580m4kPY&t=427s) [7:09](https://www.youtube.com/watch?v=_7P580m4kPY&t=429s)

06 [8:49 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=529s)

### What survives installation and changes the next run

An uninstall is an unusually good test of what a reviewer knows about the environment. Some skills returned after users thought they had removed them. In a separate case, an unofficial skill creator quietly replaced the familiar implementation. A product interface could appear unchanged while a different component handled the user’s next request. An inventory from before installation, followed by a fresh look after removal, gives the investigator something concrete to compare.

The installed package can also stay unchanged while the material it relies on changes. A remote source can be updated or change hands. Some skills can run in response to later activity, including work unrelated to the original assignment. A good review therefore has a date and a scope: which version, which dependencies, under what conditions, and which behavior did someone actually observe?

[8:58](https://www.youtube.com/watch?v=_7P580m4kPY&t=538s) [9:01](https://www.youtube.com/watch?v=_7P580m4kPY&t=541s)

07 [10:35 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=635s)

### Following a lookalike back to its source

Paperclip, an open-source project for orchestrating agents, gave the researchers a comparison case. They found an imitation of the project that looked familiar enough to borrow its reputation. Activity advertised as routine logging led somewhere outside the genuine project. Examining the destination gave the team a reason to investigate beyond the feature name.

In this case, the researchers established that sensitive authentication data left the machine and reached a service controlled by the attacker. They also observed that part of the activity was short-lived, which made the recording of the run especially important. Recall the genuine Azure diagnostic from the start of the talk. The destination and purpose of the transfer gave the team a much stronger basis for calling this credential theft.

The investigation linked the same infrastructure to software distributed through the Python ecosystem and then to a set of agent skills. Some packages disappeared quickly. The related skills had accumulated what Ben Chaim reported as **1.7 million total downloads**. This is a distribution count. It cannot tell a responder how many installations completed, how many machines ran the behavior or how many people lost credentials.

Finding the same infrastructure across distribution channels changed the response. Removing one copy of a package could leave users exposed through another source. Ben Chaim reports that after the team notified the relevant platforms, the remaining campaign material was removed within 12 hours.

[10:41](https://www.youtube.com/watch?v=_7P580m4kPY&t=641s) [10:47](https://www.youtube.com/watch?v=_7P580m4kPY&t=647s)

08 [13:33 ↗](https://www.youtube.com/watch?v=_7P580m4kPY&t=813s)

### Treat the skill as a software dependency

A skill is one way outside material enters an agent’s context. A website, a database row, a package or even a YouTube comment can also supply text the model reads while deciding what to do. Any of those sources can influence a task once the agent has read it.

Ben Chaim’s advice starts with established software dependency practices. Identify who supplies a skill and what it loads. Limit access to what its task requires. Keep enough runtime evidence to relate a sensitive action to the process that performed it and to the destination of any transfer. Someone who can answer those questions can explain why the Azure diagnostic and the Paperclip lookalike deserved different responses.

[Transcript download](https://www.ai.engineer/api/data/transcript?slug=youtube-38d1e04a22f6fc4d98c0&format=json)

Full transcript

Loading transcript…


## Official machine transcript

[0:03] Hi everyone, welcome to my talk about what happens when you detonate thousands of agent skills. This is a look inside our agent detonation chamber and what we saw when we put skills in there. My name is Roey. I'm a staff engineer at Zenity 

[0:19] and I'm a MATS research fellow. I talk a lot about AI safety and security. Follow me on Twitter and LinkedIn. Before we even start our uh session, we need to talk about what an agent skill is. Well, essentially an agent skill is 

[0:35] capability of capability on demand. It has a bunch of instructions, resources, new behavior. It can contain scripts and it can even contain code. The problem is that it was written by someone else. And this is exactly where the problem start. 

[0:51] So let's take a look at the skills trajectory. For instance, if we look at this uh if we look at the trajectory [Editorial paraphrase] The recorded activity involved cloud configuration and 

[1:03] identity information. That caught our attention because malicious software can also access sensitive information. 

[1:09] These events establish what the program touched; the trace by itself does not tell 

[1:16] the investigator whether that work belonged to the user's task. In this case the skill 

[1:24] was an official Azure diagnostic. an official Azure diagnostic skill. And this is exactly the point where it's kind of hard for us to identify whether a skill is malicious or benign. And we have to understand the original intent of the 

[1:35] skills according to its actions. And at this point, you might ask, okay, so we can just like scan the skill, right? Well, it's it's it's more complicated than that. The the first problem problem [Editorial paraphrase] The installed 

[1:49] skill file can refer to material that lives somewhere else. The reviewer sees what is 

[1:57] in the original file. The agent may see different instructions, additional software or dependencies 

[2:04] when it uses the skill. A static review ends too early if it stops at 

[2:12] the first document. We need to know which material actually influenced the run. you would lose all of that and you would have to create some sort of mechanism to 

[2:18] track all of these payloads if you don't want to lose them. The second problem that we've noticed is that LM analyzers can be tricked. Um there was a really [Editorial paraphrase] Trail of Bits showed that 

[2:29] an automated reviewer could accept a misleading explanation for a change to a project's package source. The 

[2:37] explanation was part of the material under review. It was not independent evidence of approval. A favorable 

[2:45] judgment from a model was therefore insufficient to establish that the change was authorized. bulletproof we've resorted to a different kind of action and we actually 

[2:53] decided to just run the skill with the agent. Um this is a technique employed by malware researchers for years now. Uh and it's called detonation donation and it's called detonation detonation chamber. So we created the same one but for agent for for agents and skills. And 

[3:09] this was our first version. In our first version uh we created a task prompt. We put an agent and a skill inside a sandbox. We let it operate over like minutes or or hours until until it completed a task. with unobserved agent 

[3:23] traces and analyzed it. You can imagine that it wasn't enough. Our first problem was that the environment was missing most of the time. A lot of skills rely on CLIs. They rely on specific services and even on on existence of the pro of 

[3:40] projects. You can imagine notion skill for instance. This will have to have a notion service available to talk to. So we've added a world builder that looks at a skill and builds the appropriate uh environment accordingly. 

[3:55] But then we'll cover another issue. A generic task prompt might not be enough for all skills. I mean think about it. You can have a presentation skill uh that needs to create a deck or deployment skill that need to ship a 

[4:08] service a brainstorming skill that needs to explore an idea. Each and every one of them has an entirely different modus operandi. Let's take shipping shipping a service for instance. You need to learn how to configure it. You need to learn 

[4:21] to deploy it. You need to tell it to recover from snapshots using snapshots. Um each and every one of them uh requires different set of prompts and you also need to need to make sure that you um cover every route in the in that 

[4:39] skill because one of them can be malicious. So we created the operator that does just that. It reads through the skill and tries to analyze what are the different trajectories um that we should invoke. And while it worked 

[4:52] pretty well, if you worked with agent, you can especially in the security [Editorial paraphrase] Our tests also ran into agent safeguards. Some agents 

[5:02] refused to continue when the requested behavior looked risky. A refusal affects how much 

[5:10] of the skill we can observe in one run. The team explored that limitation 

[5:18] inside its isolated research environment. We needed to distinguish a test that stopped early 

[5:25] from a test that showed the skill completed safely. The results depend on the 

[5:36] setting, the task and the particular decisions the agent made. There were false alarms too. 

[5:42] A legitimate skill may involve an operation that a model judges risky. The control 

[5:48] can act as intended and still limit what the researchers can conclude about that 

[5:55] run. We recorded the observed behavior and the limits of the evidence. would still be triggered. So up until now we were dealing with the 

[6:01] sandbox. At this point, we we we started to tackle the the the the capturing mechanism. So, agent traces can go that far. At some point, you'll be missing [Editorial paraphrase] A package 

[6:16] installation can have side effects beyond the tool call shown in the agent's conversation. Work done 

[6:24] by another process may touch files or communicate with a service. A reviewer following only 

[6:30] the model's messages could miss those effects. We wanted the system to capture what the 

[6:36] machine actually did during the installation. also events and signals that we need to capture and we did just that as part of the capturing mechanism. We added process creation event file system event 

[6:47] and network a network packet capturing given all of that along with the agent traces. We then moved it uh to a quality evidence and capture the behavior even this final form of the detonation chamber. Let's take a look at 

[7:07] at an example skill. So Zach Corman, you should follow him on Twitter. He created [Editorial paraphrase] In Zach Corman's proof of concept, the first skill introduced 

[7:17] another component whose behavior was absent from the file the user originally inspected. The additional 

[7:24] material influenced what the agent did. The researchers used an innocuous demonstration to make that 

[7:30] gap observable. It showed why reviewing a well-named component in isolation could give a misleading 

[7:37] impression of the complete task. Inspecting what was present at installation time left part of 

[7:44] the behavior unexplained. The chamber's evidence connected the later action with the earlier component that 

[7:53] caused it. That attribution came from a particular observed run. chamber. Using this approach, we were able to uncover 100 malicious skill out of 

[8:03] thousands and they were shut off uh the skills.sh framework. Now let's take a look at another example. Poly market. Uh this is this [Editorial paraphrase] Another skill claimed to 

[8:17] use a Polymarket dependency. The researchers found that its package identity differed from the expected 

[8:24] one and that its origin was unofficial. They compared what had actually been installed 

[8:34] with what a user would reasonably have expected. Further inspection showed that the substituted 

[8:41] software collected sensitive information. Similar names can hide a material difference in who supplied a 

[8:49] dependency and what it does. [Editorial paraphrase] The team also saw cases in which a skill could 

[8:58] return after someone removed it. Deleting the visible component did not always undo the changes 

[9:09] the installation had made to the environment. That matters to someone investigating a machine that appears 

[9:15] clean after an uninstall. Another example involved a third-party version of a skill creator silently 

[9:22] replacing the official version. Users could believe they were still invoking a familiar capability while a 

[9:30] different implementation answered. Those are observable changes to the installed environment, including changes a person 

[9:37] might never see during the interaction. trick that we've seen a lot of actors [Editorial paraphrase] A skill can depend on instructions 

[9:43] stored outside the installed package. Some legitimate skills do this too. The 

[9:50] important point for review is that the material available today can change 

[9:58] later, without a change to the local file. The original publisher may update 

[10:04] it and control of the external location itself can change. A reviewer 

[10:11] needs to distinguish what they actually inspected from what a later invocation received. 

[10:18] [Editorial paraphrase] Some skills could become active in response to ordinary user activity, even outside the task for 

[10:25] which they were originally chosen. That changes how often a risky behavior can occur and how visible 

[10:31] it is to the user. The team treated that as part of the security review. be aware of that. But let's talk about a campaign that we 

[10:37] that we've uncovered. Uh meet Carly or Carly paperclipipped as he known in GitHub. He faked the paperclip organization. And paperclipipped is a wellknown uh project is it's an open source uh project aimed for a a 

[10:53] orchestration of of various agents. Um early here basically created a fake organization that mimics it. He bought a he he registered the domain under kind of the same name, created a lookalike [Editorial paraphrase] Investigating the 

[11:08] Paperclip lookalike, the team found behavior absent from the legitimate project. Something presented as 

[11:15] ordinary application logging led to a service controlled by the attacker. Its relationship to 

[11:22] the surrounding application made the change easy to overlook. The name of the feature did 

[11:33] not establish what it did. [Editorial paraphrase] The additional software obtained sensitive local authentication material and 

[11:42] sent it to the attacker. The researchers observed that a component of the 

[11:51] activity was short-lived. The important evidence was the connection between access to sensitive information 

[11:56] and a destination controlled by someone other than the user. That gave the 

[12:05] team a much stronger basis for identifying credential theft than a record of a 

[12:14] sensitive file access in isolation. did the same thing in browser. Um but this this was a Python package but he used the same command and control and then he tried to publish it in Pi. That didn't work. It like under two hours it 

[12:26] was just dumb. He did the same thing with paperclip AI, which is the Python version of what we just saw. And that also went down after less than an hour. Well, at this point, you'd think that we'd be winning, but no, because the 

[12:40] skins that were using the same command and control were actually trading trending at that time to the point where they had 1.7 million total downloads. [Editorial paraphrase] Those skills had around 1.7 

[12:53] million total downloads. That measures distribution. It does not establish how many devices executed the malicious behavior 

[13:01] or how many credentials were stolen. When the researchers examined the skills, they connected them to the same 

[13:08] infrastructure and recognized the same credential-harvesting behavior as in the earlier investigation. Taking down a package in 

[13:15] one ecosystem had left another distribution route in place. same chain. We reported the incident to Versell and Microsoft and under lasted 12 hours they took everything down. If you want to read more about it, you 

[13:24] should read the Zenity Labs blog. It's very interesting, incredible work. [snorts] Um, skill is just one single part of uh of the agent supply chain. Everything that 

[13:39] goes inside the agent context is is part of it. It can be a website, it can be rows in your database, it can be packages, it can even be a YouTube comment. Everything that comes into the context is under risk. 

[13:52] And if we talk about skills in particular, you need to treat them as uh as package dependencies. Um you need to inspect everything that it loads, limit what it can access, lease privileges as you're 

[14:04] well aware, and observe what is actually being run. Now, this entire work on the detonation shaver was done by the entire research and engineering thing that you see over here. Highly talented people, and I 

[14:20] encourage you to follow them. And with that, if you want to test out your skills, it's available in neoto.io. This is detonation chamber.
