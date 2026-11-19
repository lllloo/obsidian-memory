---
title: How One Founder Manages 20 AI Coding Agents at Once — Ryan Carson
description: AI Engineer 官方閱讀版，Ryan Carson 談 manager session 帶約 20 個 builder 與錄影招募，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/BTtyguoPvBU-one-founder-manages-20-ai-coding-agents
published: 2026-11-09
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（閱讀頁上的逐字稿為動態載入，defuddle 只抓到「Loading transcript…」，故改由閱讀頁提供的 Transcript download 連結 `https://ai.engineer/api/data/transcript?slug=youtube-e7acb7ea59dc31f44eae&format=json` 取得 JSON，按約 20 秒合併成段落並加上時間連結，文字未改寫；含辨識錯誤，如 Devin 被辨識成 Devon、merge queue 被辨識成 merge Q）。對應 YouTube 影片 ID `BTtyguoPvBU`（標題「How One Founder Manages 20 AI Coding Agents at Once - Ryan Carson, Untangle」，頻道 AI Engineer，長約 15:28，2026-11-09 上傳，2026-11-19 以 yt-dlp 核對）。`published` 取該影片上傳日。閱讀頁為主辦方改寫版，正文完全沒提到講者實際使用的 Devin，改稱「built-in reviewer」「built-in testing tool」。

Loading slides…

At a glance

### Ideas worth remembering

- One PR per ticket gives the manager a unit of work to assign. Dependencies guide its next assignment, and a scheduled 15-minute pass brings its attention back to every active builder.
- The builder and reviewer usually get up to three rounds together. Important findings can then go to the manager. A separate child session handles QA.
- Carson reads what a PR is supposed to do before watching its test video. Even when every case passes, the product owner still has to judge the behavior on screen.
- Untangle evaluates agent operators first on a familiar app, then invites the top five to a paid 16-hour trial on a company PR. Carson reserves the first live call for finalists.

01 [0:12 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=12s)

### From a customer priority to one pull request

[Untangle](https://untangle.us/) began as a consumer app for people going through a divorce. It soon shifted to selling an AI paralegal to family law firms. Founder and CEO Ryan Carson had seen his previous startup grow to about 110 people, and one part of the management job felt familiar. Someone still had to talk to customers, decide what mattered, and turn that decision into work. At Untangle, people kept the first two responsibilities and gave a cloud agent session the job of engineering manager.

The manager leaves all the coding to child sessions called builders. Carson mostly talks to the manager by voice because he finds a spoken update easier to absorb than a written one. He can follow one conversation while several changes are underway.

A Linear ticket board tells the manager what needs building. Untangle aims to size each ticket to one pull request (PR). That gives a builder a defined change to make and the team a single PR to review. The manager uses dependencies between tickets to decide which work can start next.

[0:14](https://www.youtube.com/watch?v=BTtyguoPvBU&t=14s) [0:20](https://www.youtube.com/watch?v=BTtyguoPvBU&t=20s)

02 [3:29 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=209s)

### One manager checks every builder every 15 minutes

![Below the manager, a Linear board assigns one builder per ticket, with 20 builders working at once. The manager checks in every 10 minutes. The reviewer sends bugs back for up to three rounds of fixes.](https://ai.engineer/api/talk-essay-media/6afc979a58f875603fa416e092b03021bebb304fb5bcd7fe9207c8ce0225a74e)

A manager distributes tickets to builders. Each ticket keeps its own agent and review assignment.

About 20 builders can work concurrently under one manager. Carson puts the working range at roughly five to 25. The upper end depends partly on the person listening to the updates. Even if the manager can reach every builder, it can have more changes underway than its human can follow.

Carson stays out of the individual builder sessions. A builder with a technical question sends it to the manager, which can often answer it or clear a small obstacle. Those ordinary questions are precisely the ones worth delegating. If each required Carson to open a session and recover its context, he would still have 20 conversations to manage.

What makes the manager check on a builder that has gone quiet? A scheduled automation tells the manager to read every child session and move stalled work along. The interval shown in the talk is 10 minutes. By the time he presented, Carson had settled on 15. The script makes the rounds happen on schedule, something he found unreliable when left to the agent. The manager still decides what each builder needs.

[3:32](https://www.youtube.com/watch?v=BTtyguoPvBU&t=212s) [3:35](https://www.youtube.com/watch?v=BTtyguoPvBU&t=215s)

03 [5:04 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=304s)

### Three review rounds and a separate QA agent

Each builder produces code and tests. Where does it send the change for a check, and how does a finding get back to Carson? Two kinds of session branch off the builder.

- **Code review.** The builder calls a built-in reviewer and can revise the PR in response to its findings. Untangle usually caps the exchange at three rounds. At that point the builder can raise important findings with the engineering manager, which can bring in Carson if needed.
- **Quality assurance.** A separate process starts a child of the builder to run QA. This gives the change another check outside the exchange between the builder and its code reviewer.

The cost Carson watches is the delay at the merge queue. He considers a QA session cheap enough to start wherever it helps. But every extra round spent picking at a PR keeps that change waiting to land. The cap gives the builder a point at which to take an important finding to someone who can decide what to do about it.

### How review, QA, and escalation connect to a builder

<svg width="739.25" height="464" aria-hidden="true"><defs><marker id="_R_1nlqjalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 272.3682795698925 100 L 214.25 147 L 179.75806451612902 194" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nlqjalm_)"></path><text x="214.25" y="151" text-anchor="middle"><tspan x="214.25" dy="0">Requests review</tspan></text></g> <g><path d="M 112.24193548387098 194 L 77.75 147 L 224.25 92.82703777335985" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nlqjalm_)"></path><text x="77.75" y="143" text-anchor="middle"><tspan x="77.75" dy="0">Returns findings in</tspan> <tspan x="77.75" dy="16">each round</tspan></text></g> <g><path d="M 361.4005376344086 100 L 394.25 147 L 394.25 194" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nlqjalm_)"></path><text x="394.25" y="151" text-anchor="middle"><tspan x="394.25" dy="0">Starts a QA child</tspan></text></g> <g><path d="M 434.25 87.10169491525423 L 624.25 147 L 624.25 194" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nlqjalm_)"></path><text x="624.25" y="135" text-anchor="middle"><tspan x="624.25" dy="0">Can raise important</tspan> <tspan x="624.25" dy="16">findings after about</tspan> <tspan x="624.25" dy="16">three rounds</tspan></text></g> <g><path d="M 624.25 286 L 624.25 325 L 624.25 364" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_1nlqjalm_)"></path><text x="624.25" y="321" text-anchor="middle"><tspan x="624.25" dy="0">Asks for help if</tspan> <tspan x="624.25" dy="16">needed</tspan></text></g></svg>

**Builder** Implements the ticket and writes tests.

**Code reviewer** Reviews the builder’s change.

**QA child session** Runs a separate check for the builder.

**Engineering manager** Handles findings the builder raises.

**Carson** Weighs in when the manager needs help.

Only the builder and reviewer participate in the capped exchange. QA runs in a child session of its own. The engineering manager receives important findings and decides whether Carson needs to weigh in.

Read the diagram as text
- **Builder.** Implements the ticket and writes tests.
- **Code reviewer.** Reviews the builder’s change.
- **QA child session.** Runs a separate check for the builder.
- **Engineering manager.** Handles findings the builder raises.
- **Carson.** Weighs in when the manager needs help.
- Builder → Code reviewer: Requests review.
- Code reviewer → Builder: Returns findings in each round.
- Builder → QA child session: Starts a QA child.
- Builder → Engineering manager: Can raise important findings after about three rounds.
- Engineering manager → Carson: Asks for help if needed.

[5:07](https://www.youtube.com/watch?v=BTtyguoPvBU&t=307s) [5:29](https://www.youtube.com/watch?v=BTtyguoPvBU&t=329s)

04 [6:25 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=385s)

### What the product owner looks for in a green test run

What did the user actually see while the tests passed? Every builder records the feature in use. The built-in testing tool creates test cases, records the interaction, and gives each case a green or red result. For a UI change, the product owner can compare the two outputs. The results identify which checks passed. The recording shows what the feature did and how it looked while passing them.

The manager alerts Carson when a video is ready. Coming back to one PR after directing many builders, he first reads a short summary of what the change is supposed to do. That gives him a specific expectation to check as he watches. The decision to ship belongs to a person, and this is where the product owner has to give one change their full attention.

Just before the talk, Carson was speaking to the manager on his phone when it told him a video was ready. He could carry on the conversation just fine. When he played the recording, though, he could barely make out the change. Tempted to approve it anyway, he held off until he could watch on his machine. After hundreds of adjustments, Carson credited the process with helping Untangle ship a lot of high-quality PRs. It worked for his team at the time, and he expected it to change quickly.

[6:34](https://www.youtube.com/watch?v=BTtyguoPvBU&t=394s) [6:36](https://www.youtube.com/watch?v=BTtyguoPvBU&t=396s)

05 [8:21 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=501s)

### Many managers, one merge queue

Carson’s advice to move development to the cloud follows from how he runs a team. Take his example of ten people working at once. Each would typically have an engineering manager session, and one person can have more than one. Carson himself had two running. The sessions need to know which other sessions exist and be able to message them directly. When one has information another needs, they can unblock each other without asking a person to relay the question.

Database migration numbers illustrate what still needs coordination across the team. Two builders working on different PRs can each reach for the same next migration number. Each number looks reasonable in its own PR. Bring the changes together and the numbers collide. Untangle assigns another session, the merge queue manager, to coordinate details like these across incoming PRs.

Like the engineering manager, the merge queue manager is an ordinary cloud session. Carson names it for its job and gives it latitude to work out how to coordinate the wave of changes. GitHub provides the merge queue itself.

[8:23](https://www.youtube.com/watch?v=BTtyguoPvBU&t=503s) [8:25](https://www.youtube.com/watch?v=BTtyguoPvBU&t=505s)

06 [11:07 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=667s)

### The first hiring screen is a feature PR

Running engineering this way changes the first question Untangle asks about a candidate. Can this person direct an agent through shipping a feature? Carson had found it easy to come away from a screening call impressed by someone’s hobbies or the way they spoke. Untangle delays that conversation until the team has seen the person work.

The first submission is an unpaid, roughly 45-minute recording of the candidate’s whole screen. The assignment is to ship a feature PR with an agent, typically on an application the candidate already maintains. Untangle leaves the method up to them. The PR shows what they shipped. The recording lets a reviewer follow the directions they gave the agent and what they did with its work.

A ranking agent takes the videos and transcripts and puts the candidates in order, saving someone the time it would take to watch every submission. Carson distrusted its first ranking. In hindsight, he thought he should have hired its first choice and attributed his resistance to his own bias. That was his judgment about one hiring decision. The recordings also vary in what they reveal. Some candidates narrate freely. When someone mumbles or works silently, a reviewer may see what they did and still have little idea why.

[11:30](https://www.youtube.com/watch?v=BTtyguoPvBU&t=690s) [11:32](https://www.youtube.com/watch?v=BTtyguoPvBU&t=692s)

07 [13:23 ↗](https://www.youtube.com/watch?v=BTtyguoPvBU&t=803s)

### The top five prepare a real PR for merge

![Candidates record 45-minute videos of their full screen as they use agents to ship a feature in an app they maintain. A ranking agent watches every video. The top five record their screens while preparing a pull request in Untangle’s codebase for a fixed fee, with a 16-hour limit. One finalist gets the first call.](https://ai.engineer/api/talk-essay-media/2d62f104339415c1729f2d43cbc57186a897011c77bdfbd40d150b749b48cd44)

Five finalists get a real pull request to prepare. The handoff from the ranking agent marks the start of that stage.

The five highest-ranked candidates receive an invitation to a paid trial. Untangle pays a fixed fee for 16 hours, asks each candidate to sign a nondisclosure agreement, and provides a seat in its cloud coding environment. This time the task is to get a real Untangle PR ready for merge. The team gets to see how someone who could ship a feature in a familiar app handles the work they would actually be hired to do.

Loom captures the trial, and Untangle gives the recordings to an agent for a recommendation. In the last round, Carson also watched 16 hours of footage himself. He found it grueling, but it gave him a feel for the candidates. He recommends choosing finalists before calling them, so an easy conversation has less chance to sway the assessment of their work. The call can then begin with the team already inclined to hire. It still serves two purposes Carson values: a final human judgment and a chance for the two people to connect.

[Transcript download](https://ai.engineer/api/data/transcript?slug=youtube-e7acb7ea59dc31f44eae&format=json)

Full transcript

Loading transcript…

## 官方機器逐字稿（Transcript download JSON）

[0:01](https://www.youtube.com/watch?v=BTtyguoPvBU&t=1s) [music] So, my name is Ryan Carson. I'm the founder and CEO of Untangle. So, we're building an AI parallegal specifically for family law, uh, focusing on divorce in particular. Um, so, quick audience

[0:25](https://www.youtube.com/watch?v=BTtyguoPvBU&t=25s) poll. Who has been divorced? Raise your hand. Raise it. Be don't be shy. Raise your hand. Who's been divorced? Okay, keep your hands up. Who knows somebody that's been divorced? Raise your hand. Everybody. Yeah. So, for you watching the video, everyone raised their hand by the end. Divorce touches a lot of people. Um, two of my sisters got divorced. My parents got divorced. Um, and it's one of the most painful things in your whole life. And I wanted to work

[0:47](https://www.youtube.com/watch?v=BTtyguoPvBU&t=47s) on that problem and just make it a little less painful. Um, started off as a consumer app. Uh, quickly pivoted to B2B and we sell to family law firms now. And thankfully product market fit is there and we're growing really fast. So that's really fun. Um so I've built and sold four companies. Um my last startup we scaled to about 110 people and I learned a lot about managing people and

[1:11](https://www.youtube.com/watch?v=BTtyguoPvBU&t=71s) it turns out managing people is like managing agents. And so I'm going to share with you how we manage agents at Untangle and how everything I've learned uh managing people kind of fits there. So I'm hoping to teach you some of those things. Um, I'm also going to show you how we hire. I I think hiring is very different in the age of agents. Um, I've hired a lot of people over my career. Um, I've made a lot of mistakes and I'm

[1:34](https://www.youtube.com/watch?v=BTtyguoPvBU&t=94s) going to share how we're hiring now at Untangle and I think how it's really working. Um, and then I'm going to show you a live demo. So, let's get started. This is me on X and this is Untangle. If you want to know more about us, if my little clicker works, you can do it. Okay, so what does the org chart look

[1:58](https://www.youtube.com/watch?v=BTtyguoPvBU&t=118s) like now in the age of agents? How do you run your agents? Um, so the way we do it is pretty straightforward. So we have humans at the top. Um, and obviously we set priorities, we talk to our customers, we're doing all the human stuff, but what we use are manager agents and these are literally just sessions. So we use Devon. Love Devon. We do all our engine the cloud. Um, I've done [clears throat] everything, you

[2:21](https://www.youtube.com/watch?v=BTtyguoPvBU&t=141s) know, from coding by hand to, you know, using cursor to here and we're in Devon. But we have a manager session. I'm going to show you this. It's literally just a session. I I call it engineer manager. Um, and it never writes code. And I mostly talk to this agent. Um, and it manages a bunch of children. So, I'll talk to you how about how we do that. We also I mostly use audio to manage this agent. Um, I don't know about you, but

[2:46](https://www.youtube.com/watch?v=BTtyguoPvBU&t=166s) I'm not a fast reader. I'm definitely not an agent and I prefer audio. I can ingest audio a lot better for some reason than reading. So, I talk mostly to my manager agent over audio. I'll show you that. Um, I just find it I I can absorb it. I can understand it. I can see what's happening. It's much more natural. So, I'm going to show you that as well. Now, the manager agent uh primarily works from a ticket board. We

[3:11](https://www.youtube.com/watch?v=BTtyguoPvBU&t=191s) use linear. Doesn't really matter what you use, but this is kind of the source of truth about what needs to be built. every ticket should be one PR um which is how we we work and that the uh manager agent knows which tickets to pull based off dependencies. It's like pretty basic engineering manager stuff here, but this is where it gets interesting. So each manager agent uh concurrently manages up to about 20

[3:35](https://www.youtube.com/watch?v=BTtyguoPvBU&t=215s) builder agents. Um this number varies like it can go anywhere from five to probably 25. Um, this is somewhat bottlenecked by your ability to talk to the manager agent and understand what's happening. Um, uh, I think if you push too hard on this, you you quickly spin out of control. Um, I find we can concurrently manage about 25 builders.

[3:58](https://www.youtube.com/watch?v=BTtyguoPvBU&t=238s) Um, now the key here is that the manager is talking to this these builders. You never go into these sessions. You never talk to them. You never manage them. You never do anything. Um, it's all done through the manager agent. And usually what it's doing is answering technical questions that don't I don't need to answer. Um or unblocking small things. Um I also have an automation that forces the manager agent

[4:22](https://www.youtube.com/watch?v=BTtyguoPvBU&t=262s) to read all the children sessions every it's like every 15 minutes. This says 10, but I've decided 15 is about the right call. You have to you have to build an automation. You can't trust your Androme your manager agent manager agent to do this right. It's not deterministic. So this is basically a script again in Devon. It has automations. You just tell it, hey, every 15 minutes go read every single

[4:46](https://www.youtube.com/watch?v=BTtyguoPvBU&t=286s) child, push things along, keep things moving, right? Um, and then any questions go back to the manager agent. So, who's tracking so far? Do you understand what I'm saying? Okay, good. And probably a lot of you are doing this. I'm not claiming this is rocket science, but this is what we're doing right now in prod and it's working, right? Um, each of these builder agents uh has a a a review agent that it calls

[5:10](https://www.youtube.com/watch?v=BTtyguoPvBU&t=310s) upon. Um, Devon has built-in reviews. Probably every code harness you have has built-in reviewers. Um, we typically stick to a three uh review max where uh we allow the builders to loop about three times with reviews. If they still have any important bugs that have been fixed, after three, then they bubble that back up to the manager agent. And if the manager agent needs to, it

[5:32](https://www.youtube.com/watch?v=BTtyguoPvBU&t=332s) bubbles it back up to me, right? Um, that seems to work pretty well. Okay, so what's happening under the code under under the hood here? Like all the normal stuff, right? You've got code plus tests. You've got a QA agent. This is actually an additional uh process that we run. Um, it actually spins up a child of the builder to run QA. Um, y'all, this is cheap. like you should be

[5:57](https://www.youtube.com/watch?v=BTtyguoPvBU&t=357s) spinning up as many agents as you can as long as you're not holding up your merge queue, right? So I this works well for us now. Um a a wonderful engineer named Dale recently joined. He helped install this QA process. I think it's working pretty well so far. The thing that you're all going to encounter is just merge Q slowdown. Um there's this fine balance of just, you know, pecking your PRs to death um versus just getting them

[6:22](https://www.youtube.com/watch?v=BTtyguoPvBU&t=382s) merged, right? Um, the other thing I love, love, love, love is videos. So, Devon has this built in. Um, if not, you should build this. Um, it's hard. Um, every builder records a video of the feature being used and passing tests. So, if it's a UI facing feature, you've got to look at it, right? Um, this is

[6:45](https://www.youtube.com/watch?v=BTtyguoPvBU&t=405s) how we know that what we've built looks good, how it works, right? So, in Devon, it's a built-in feature. It's called test. And basically it it builds test cases and then it records a video and it gives you green or or red on those on those tests. And if you get a video that's all green, you can watch it and know what we think is happening is happening and visually it looks good. Right? So this is the human in the loop where a human has to say ship it. So the

[7:11](https://www.youtube.com/watch?v=BTtyguoPvBU&t=431s) manager session will will let me know there's a video ready for you. Watch it. Right? So I watched the video and this is the hard part. you've got to zoom in and understand like what is this PR doing? Um what am I watching? Um so I usually read a summary of like what is this thing? What is it supposed to do? I watch it and I ga engage. And I would encourage you this is the part where you want to cut corners. You got to watch

[7:33](https://www.youtube.com/watch?v=BTtyguoPvBU&t=453s) the video. Like there is no this is the part of the bottleneck you have to engage in as a product owner. Um got to watch the video, got to pay attention. Usually it has to be on your laptop. Um I I I this literally before this talk I was on my phone you know talking to my manager my manager agent and it said there's a video for you. I watch it and I just couldn't see it well enough and I was so [snorts] tempted to be like it's

[7:56](https://www.youtube.com/watch?v=BTtyguoPvBU&t=476s) okay ship [laughter] it like no get back to my machine watch the watch the video. Um this is working like you know we we ship a lot of PRs uh at high quality this way. We've iterated, you know, hundreds of times on this process and I I feel pretty good about this. Now, this will change tomorrow [laughter] and probably will be useless a week from

[8:18](https://www.youtube.com/watch?v=BTtyguoPvBU&t=498s) now. Uh, but it works well today. Um, uh, the thing I will say is like if you're coding locally, stop. Like, you really need to be coding with a a cloud agent. I don't care if it's Devon or whatever it is, but if you're running local dev, you are screwing up. You're holding yourself back. You're holding your team back. You're holding everything back because you can't do this. Um so that's where we're going and I feel strongly about that.

[8:43](https://www.youtube.com/watch?v=BTtyguoPvBU&t=523s) So how does this work at scale? Well, you know, say you have 10 folks um uh in the who are working on things. Typically they'll have an engineering manager uh session each. Sometimes they'll have two like right now I have two running. Um and what's beautiful is that these things talk to each other. And so uh again in Devon this is built in. It's

[9:06](https://www.youtube.com/watch?v=BTtyguoPvBU&t=546s) probably built into whatever harness you use. the sessions all need to be able to talk to each other and they all need to know who each other is, right? And they're really good at this. Like this is such a delight. So what you'll see if if you if you zoom into any sessions, they're messaging each other. It's clear, it's straightforward, it's fast, it's good. Like you should be allowing your sessions to talk to each other. Um

[9:31](https://www.youtube.com/watch?v=BTtyguoPvBU&t=571s) and again, if you're not, you are holding yourself back and you're probably shipping worse software. Um so they all talk a lot. Um, and it's not chitchat or stupid stuff like this is important stuff that they need to know to unblock each other. Um, which is very useful. However, you still need what we call a merge Q manager. Um, so this is how we coordinate this just

[9:55](https://www.youtube.com/watch?v=BTtyguoPvBU&t=595s) wave of PRs that come in. You know, you have things like database migration numbers. These need to be coordinated. Like if all the agents are trying to grab these things, you constantly collide, right? So the merge manager just helps all that go away. It also is a little more intelligent about how the merge Q is happening. So this is really nice. Um it's working well for us. And

[10:18](https://www.youtube.com/watch?v=BTtyguoPvBU&t=618s) again, these are just sessions. This is not like something special. These are just sessions in Devon and I and I name them so I understand what's happening. Um and it's pretty straightforward. You know, the talk from the gentleman from OpenAI, you know, said basically you got to unhobble. Just unhobble the thing, right? So set up the roles and then unhobble the model, right? Um, and I

[10:41](https://www.youtube.com/watch?v=BTtyguoPvBU&t=641s) think just having a merge manager say, "Hey, make all this better." Uh, really works well. All right. Who's tracking so far? Good. Who thinks this is [&nbsp;__&nbsp;] Raise your hand. Oh, one guy. Two. Wait. One. Come on. Be be more brave. We have to talk afterwards. Where Where are you? Um, okay. And then we use GitHub merge cues. It's fine. It's not rocket

[11:04](https://www.youtube.com/watch?v=BTtyguoPvBU&t=664s) science. It works pretty well. So, all right. Next up, how we hire. Um, so who's hiring engineers or employees right now? Raise your hand. Yeah, decent number of you. Um, I think everything has changed. Every everything you used to do about hiring employees is over and none of it makes sense. Um, it's all outdated and I would encourage you to do something like this. So, we don't do

[11:30](https://www.youtube.com/watch?v=BTtyguoPvBU&t=690s) number one any sort of pre-screens. We don't do any video chats. We don't do anything with people um it for most of this process because it will bias you. You'll like their hobbies. You'll like the way they talk to you. You'll think they're interesting. And it's all noise. None of it is signal, right? All that matters is can they operate an agent, right? Can they do that? So, the way we

[11:54](https://www.youtube.com/watch?v=BTtyguoPvBU&t=714s) do that is we ask candidates to submit a 45ish minute video, whole screen recording. Um, and we ask them to ship a feature PR typically on a app that they already maintain and we just we just ask them to record that. No instruction, no guidance, no nothing. And we just want to see like how good of an agent

[12:16](https://www.youtube.com/watch?v=BTtyguoPvBU&t=736s) operator is this person, right? So, um, that is free. We don't pay for that. That's basically how you get in the door. Um, and what we then do is we feed these videos into a ranking agent and basically say watch the video, watch the transcript, stack rank these people. Um, now this what's interesting is I did this and I didn't trust it the first time. I didn't like what it said. Um,

[12:41](https://www.youtube.com/watch?v=BTtyguoPvBU&t=761s) and what's ironic is it actually was correct. Like the person that was number one, I I should have hired them. Um, uh, but I didn't trust it because I was I was biased. So you stack rank them. Now, this is just a lot of video to watch. You could watch all these videos if you want. If you have time, do it. But I think you'll find actually a very intelligent model is pretty good at understanding like how how good is this person. Um, what's interesting though is

[13:06](https://www.youtube.com/watch?v=BTtyguoPvBU&t=786s) uh candidates will mumble um or uh sometimes or they won't think out loud, which is kind of fascinating. So, you can't really tell what they're thinking or doing. Um, which is interesting. So, that's uh something to sort of note. Um, and some talk a lot. [laughter] So, you never know. Uh, then we basically pick the top five and we invite them to a paid project. So, we pay them a fixed

[13:28](https://www.youtube.com/watch?v=BTtyguoPvBU&t=808s) fee for 16 hours of their time. We actually give them a seat on Devon and we ask them to uh to get a real PR ready for merge. Um, we have them sign an NDA. Um, and we record all the video. This is 16 hours of video. Um, we basically use Loom and then uh we feed all the videos into uh our our agent basically Devon

[13:52](https://www.youtube.com/watch?v=BTtyguoPvBU&t=832s) and we say hey who you know which one should we pick? I actually watched all 16 hours of these videos for the last round. Uh it was brutal but it did give me a good read on the people. Um and then you basically pick one. You pick your finalists and then what's important is that you don't do calls before this. Um you will get biased. you'll get confused. You'll try to pick somebody

[14:16](https://www.youtube.com/watch?v=BTtyguoPvBU&t=856s) you shouldn't. And I would just call the finalists and say, "Hey, you know, we think we'd like to hire you. Let's talk a little bit." Um, and that gives you the final sort of human read, but you're going to watch videos of these people for hours. Like, you're not really going to need that call. Um, but I think there's a little bit of of of human connection there that's important. I think this is how everyone's going to hire. Like, this works. Um, you know,

[14:40](https://www.youtube.com/watch?v=BTtyguoPvBU&t=880s) I've hired hundreds and hundreds and hundreds of people in my career. This is just way easier and way better. Um, and I think it's where we're all moving to. So, I'm actually going to finish 3 minutes early. Um, if you want to know more about Untangle, just go to Untangle. Um, I'm on X like just all the time. I literally been on X for 20 years. Um,

[15:03](https://www.youtube.com/watch?v=BTtyguoPvBU&t=903s) and so, uh, that's where I live and breathe. So, if you want to know more about uh leading companies, managing agents, um that's where I am. If you're interested in family law and you're passionate about making divorce less painful, um get in touch. Um and that is all I have to say. Thanks everybody. Appreciate it. [applause]
