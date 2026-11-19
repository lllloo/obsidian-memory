---
title: Merge Is the Bottleneck — Prasanna Sankar
description: AI Engineer 官方閱讀版，Vorflux 的 Sankar 談雲端 agent 從環境到 merge 的瓶頸與常駐 Autobot，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/TlOAhw9t5DA-merge-is-bottleneck
published: 2026-11-10
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript JSON，依時間每約 30 秒併段、文字未改；原稿含辨識錯誤，如 Vorflux 被辨識成 Warflex／Warflex 2.0、Rippling 成 Ripling、Claude 成 clot／claude、Sentry 成 centuries／sentries、PagerDuty 成 page your duty、CI 成 CA）。對應 YouTube 影片 ID `TlOAhw9t5DA`（`https://www.youtube.com/watch?v=TlOAhw9t5DA`，AI Engineer 頻道，上傳日 2026-11-10，約 20 分鐘）。

Loading slides…

At a glance

### Ideas worth remembering

- Count the developer’s time through to merge. A plan returned in two minutes can cost several rounds of clarification, a cloud change can require a local test, and a reviewed branch can fall behind while it waits.
- Before giving a bot an ongoing assignment, identify the signal that justifies starting work, the person who owns the outcome, and the budget for pursuing it. A blanket instruction to fix every alert leaves those decisions unresolved.

01 [0:05 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=5s)

### From autocomplete to a job you can leave running

[Prasanna Sankar](https://www.linkedin.com/in/myprasanna/) had ranked first in India as a competitive programmer at 18. A year at Microsoft taught him how much the pace of a large team could limit what he accomplished with that speed. He moved to Silicon Valley around 2009 to build companies. Years later, writing software for himself, he saw models winning the kinds of contests he had entered. What caught his attention was how those systems used the model once they had a problem to solve.

The shift he associated with **Opus 4.5** was visible at the keyboard. IDE autocomplete could suggest the next piece of code. A terminal agent could take an assignment and work on it alone for a few minutes. Meanwhile, the systems winning programming contests devoted substantially more compute to each problem at inference time than a typical coding agent did. The harness, the software directing the model’s work, gave Sankar somewhere to make that trade himself.

Sankar started building [Vorflux](https://vorflux.com/) for his own use. He was willing to spend more tokens on a task if it saved him time, and he expected those few minutes of independent work to grow into hours. For a job that long, he wanted to be able to leave it running in the cloud. The first obstacle was everything his laptop already knew how to do.

[0:23](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=23s) [0:31](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=31s)

02 [3:58 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=238s)

### Reproduce localhost, then give the plan two audiences

A cloud agent might manage to start the service it was editing. Testing a change could still require other services, the expected ports, working authentication, and data to test against. Vorflux paid that setup cost during onboarding. Subagents started with a raw EC2 instance, brought up the development environment, connected the ports, and worked through machine secrets, authentication, and seed data. With those dependencies in place, a session could run the whole application.

Watching developers use the agents exposed a cost that a fast response could conceal. The planning agent usually came back in a minute or two. Then the developer spent several turns working through the plan with it. Vorflux spent more tokens before that first response. Several exploratory subagents worked in parallel on the design, producing a detailed plan that the harness condensed for the developer.

How could the developer read a short summary while the agents still knew which parts to build together? The underlying plan retained a dependency graph. A developer splitting up a large change would ordinarily have to identify the pieces and work out which could proceed independently. The graph gave the harness that information, so it could assign independent pieces to build subagents while respecting prerequisites elsewhere in the plan.

### Who uses the detailed plan?

<svg width="460" height="432" aria-hidden="true"><defs><marker id="_R_3f9ajalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 230 100 L 230 131 L 230 162" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="230" y="135" text-anchor="middle"><tspan x="230" dy="0">Contribute design work</tspan></text></g> <g><path d="M 292.2352941176471 254 L 345 293 L 345 332" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="345" y="297" text-anchor="middle"><tspan x="345" dy="0">Condense for reading</tspan></text></g> <g><path d="M 167.76470588235293 254 L 115 293 L 115 332" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="115" y="289" text-anchor="middle"><tspan x="115" dy="0">Assign work by</tspan> <tspan x="115" dy="16">dependency</tspan></text></g></svg>

**Exploratory subagents** Investigate the design in parallel.

**Detailed plan** Describes the work and its dependencies.

**Developer** Reads a summary of the design.

**Build subagents** Work on pieces that can proceed independently.

The summary and the build assignments draw on the same design. The summary reduces how much the developer has to read. The dependency graph preserves the detail needed to divide the work.

Read the diagram as text
- **Exploratory subagents.** Investigate the design in parallel.
- **Detailed plan.** Describes the work and its dependencies.
- **Developer.** Reads a summary of the design.
- **Build subagents.** Work on pieces that can proceed independently.
- Exploratory subagents → Detailed plan: Contribute design work.
- Detailed plan → Developer: Condense for reading.
- Detailed plan → Build subagents: Assign work by dependency.

[4:13](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=253s) [4:16](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=256s)

03 [6:41 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=401s)

### Give the reviewer a running feature

Testing still tied the developer to a laptop if every cloud session ended with a request to pull the branch and run the app locally. Vorflux ran browser and end-to-end tests on the cloud machine. The effort spent reproducing the environment now paid off twice. The agent could exercise the feature with its dependencies in place, and a person could inspect the result where it ran.

What did the test actually exercise? Sankar liked being able to watch a video of the interaction and see the new feature work. A feature-specific staging link answered a different question. What would happen if he tried something else? With the app already running on the remote machine, he could open the link and choose his own path through the feature.

[6:47](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=407s) [6:49](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=409s)

04 [7:45 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=465s)

### Keep a reviewed change mergeable

Developers were already asking a second model to review the first model’s work. Vorflux made that division of labor configurable in the harness. One arrangement used **Claude** to build and **GPT** to review. A team could also assign several reviewer subagents to examine the same change from different angles, without the developer having to arrange each review by hand.

A reviewed pull request could still be waiting when another developer or agent landed a change. The base branch had moved. A branch that was ready to merge a moment ago might now need a rebase. With many pull requests open at once, keeping them mergeable became a job in its own right. Vorflux built a merge queue that repeatedly rebased pending changes against `master` and landed the pull requests. In Vorflux 1.0, a developer could start a multi-hour cloud session and have it carry the change through to merge.

[7:48](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=468s) [7:51](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=471s)

05 [9:00 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=540s)

### Who keeps track of 20 or 30 sessions?

Sankar put his experience at roughly three to five parallel tasks on the desktop and 20 to 30 with long-running cloud agents. His own ability to keep track started to give out around ten. He still had to remember which ideas needed starting, see which sessions needed attention, and decide whether the changes that landed were useful. More capacity to write code had given him a project management job.

The subagent design suggested a way to divide that job. A main agent could hold the plan, start sessions, and track progress. Each worker could do its detailed work in a fresh context window, leaving the main agent room to coordinate the assignments. Vorflux 2.0 applied that design to persistent agents called Autobots. Each had an ongoing goal and could decide when to start a session in pursuit of it.

Consider a customer call that ends with several to-dos. Someone has already expressed what they want. To feed each item to a coding agent, a person still has to notice the commitment, remember it after the call, and write up the task. The transcript can supply that intent directly. A production alert can likewise identify a problem to investigate. When several sessions start this way, the people who own different parts of the work need a shared place to see what is happening and help it land.

This gave Sankar a criterion for choosing assignments. Incremental work suits an Autobot when the conversation, alert, or codebase already contains enough information to identify the next change. Zero-to-one product work demands a different judgment. A customer can describe a bug they encountered. Imagining a product they could never have asked for is a job Sankar wanted to keep.

[9:08](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=548s) [9:13](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=553s)

06 [12:58 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=778s)

### What goes wrong when every alert starts a fix

![Streams converge on a central icon. To its right, a bright upper branch reads “Handled,” a person icon marks “Needs you,” and a faint lower row reads “Noise.”](https://www.ai.engineer/api/talk-essay-media/1a2cab1af5af9d5b24833df53574f5a19fbce533f2f3ccc56bf6c9871498447e)

Incoming signals are sorted into handled work, noise and work that needs a person.

Tell an agent to fix every incoming error and it can open more pull requests than anyone has time to merge. Each comes with another interruption. Worse, a change can silence the alert while leaving its cause in place. If the agent spends hours on an issue nobody wanted it to pursue, the team pays for both the tokens and the review. Recognizing an error is considerably easier than deciding how much attention it deserves.

Sankar’s comparison was a new hire. Give the bot an important, specific responsibility and expect frequent check-ins early. Set a budget and make its work visible. Expand its responsibility when the results hold up and narrow it when they fall short. An Autobot gets a goal, an owner, and a home channel. Webhooks supply the events it can act on. Vorflux also built a directory of bots that teams could adapt, starting with assignments that had worked inside the company.

- **On call.** Triage incoming alerts and investigate before bringing in an engineer. The engineer can begin with what the bot has already learned about the incident.
- **Continuous integration.** Keep working on build speed. A slowdown gives the bot a concrete problem to investigate, and a tested fix gives the team something to review.
- **Project management.** Keep a project in one channel, report progress and blockers each day, and tag a reviewer when a particular change needs attention.

[13:06](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=786s) [13:08](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=788s)

07 [15:36 ↗](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=936s)

### A missing Slack reply becomes a customer follow-up

![Clockwise from the upper left, the call ends, a to-do is found, an engineer is tagged and you approve. The engineer fixes the issue, the fix is deployed, a follow-up is drafted and you approve and send it.](https://www.ai.engineer/api/talk-essay-media/69a878ea44c007c13ca093b04b717738b8b0040ff9f9913e09341645221beb5b)

The diagram follows one customer call through a fix, a draft reply and the human decision to send it.

During a beta rollout with a friendly customer, a bot failed to reply in Slack. Sankar would usually have taken a screenshot and tagged Vorflux to investigate. This time an Autobot that watched customer calls picked up the task after the meeting. It found Sankar’s to-do in the transcript and used the timestamp to locate the corresponding moment in the recorded screen share. The words identified the unfinished work. The recording supplied the screen context he would otherwise have had to capture. [15:39](https://www.youtube.com/watch?v=TlOAhw9t5DA&t=939s)

Who needed to approve what? The Autobot first asked Sankar whether to take on the fix. He agreed. It tagged the responsible engineer and came back with a pull request. The engineer approved the code, and the change merged and deployed. With the fix shipped, the bot closed the item and drafted a message telling the customer it was fixed. Sankar approved the wording, and the message went out.

Sankar could imagine routine work coming to feel like “approve, approve, approve.” In this case each approval had a purpose, and the bot saved the people involved from having to remember the next handoff. His expectation was that a bot with a track record could take on more of those decisions over time.

[Transcript download](https://www.ai.engineer/api/data/transcript?slug=youtube-b25fb39cc531f4070d85&format=json)

Full transcript

## Full transcript（官方機器逐字稿）

[0:05] Hey guys, um my name is Prasana and I really appreciate the opportunity to speak in front of all of you guys today. Um AI has really accelerated leverage and you know this is a story of leverage. Um I'll start with my own personal background. Um I'm a software engineer. Um was ranked number one coder in India when I was 18 years old during my college days. Um I won [clears throat] all these programming contests like top coder. I was ranked number one there. Um I was two times world finalist in both Google code jam and um ACMCPC. These are the you know

[0:39] the top programming contests in the world and uh did really well there. Um represented India quite a few times now. Um [clears throat] the models have gotten way better than any of us. They perfect score these programming contests. So it's an interesting time to be alive and you know super exciting time. Um I want to talk a little bit about you know my own background right like my own journey after college I kind of like worked at Microsoft for a year quickly realized you know the bottleneck to uh um impact on the real world or my own personal leverage um was uh other people um like

[1:15] working in big teams um [clears throat] and then there was the the alternate path I came across Paul Graham's blogs um Silicon Valley was happening internet companies were getting a lot cheaper to hard so a lot more people like myself um were able to access it um and Paul Graham's blogs gave me a path towards living a life of higher leverage so I moved to the valley sometime around 2009 to um you know start building companies at this point I'm a three times YC founder um [clears throat] the most successful company that I founded was a

[1:50] company called Ripling which is worth more than 10 billion today u more recently I've started a company called Warflex it's a it's a part of the latest YC batch as well. We've raised around $15 million and uh it's a AI software engineer u or AI coworker um the highest leverage AI co-orker. So the way I got there is like you know post founding rippling uh I was just like building things for myself and I was uh building things of like higher and higher leverage. Something interesting happened in in in my world with the launch of uh Opus 4.5. I think it was like almost a

[2:24] year ago at this point. It was a magical moment. Um software went from autocomplete in in the IDE to um [clears throat] um agents working by themselves for a few minutes at a time. So you could suddenly sort of move from completely skip the ID and move into the terminal. That was seminal. You know it was naturally obvious that you know that was just going to take off. Those few minutes are going to get longer and longer and longer. So um you [clears throat] know at the same time these models started winning all these programming contest and it was kind of like fairly clear to me like they were

[2:57] better than me in just like raw reasoning. Um especially you know but then the the harnesses that won these programming contests were not a vanilla clot code or a codeex harness. They spent a lot more on inference time compute. a lot more inference time compute to like you know access higher order intelligence. Um so that's what I wanted to build for myself you know the higher leverage version which spends a bit more tokens but you know uh saves a lot of time you know gives me like a lot more intelligence so I started building

[3:32] Warflex for myself and uh you know the first obvious thing is like you know once agents start running beyond a few minutes into um into a time uh especially if you're able to solve a bunch of these bottleness that that I'm going to talk about um you really want them running on the cloud. You don't want them running on your machine because uh you know um that's where they belong. Uh a task that runs hours at a time. So [snorts] I think that's the first big bottleneck that people need to solve like you know cloud agents need to solve to get um people moving from the

[4:05] desktop to to the to the cloud is a perfect environment setup. Like today cloud agents run like most cloud agents run blind. at best they run the one service that you're trying to change. But really like for for like good testing, the reason why um people sort of like do all this stuff on their local host is because um there are a lot of other dependencies and you want to be able to run, you know, you want to be able to almost like mirror the local host environment on the cloud to truly transport someone. So we spent a lot of

[4:37] tokens and money and time uh solving the machine setup bottleneck where you can just like on board and we start a bunch of sub aents to like go set up a raw EC2 instance um with your whole environment, wire up the ports, um figure out the machine secrets, solve authentication, solve seed data and a bunch of these things. Spend tokens up front migrating the user to the cloud. I think that's really important. That's something that most cloud agents miss. So that's that's like one of the major bottlenecks to moving from desktop to the cloud. Um

[5:10] once you saw that what you realize is like if you you know when I was profiling how people were spending their time including myself a lot of the time was being spent on the planning phase and u um you know [clears throat] um like back then um the planning agents um were not spending as much tokens. um the agents weren't as spending as much tokens on the planning phase. you know they usually come back within a minute or two and you were iterating a lot back and forth back and forth on the planning phase and you know obviously if human

[5:43] time is being spent there that's where I want to throw more tokens right so what you know what flex we sort of scaled up um inference time compute at the planning stage we launched a bunch of parallel explore sub agents which sort of built a built a design or an architecture of what needs to be done and uh you know we sort of came up with a plan of plans which like a lot more detailed and uh you know and then sort of produced a summary out of it um to help solve the time spent by humans on the planning phase. Right? So that that

[6:18] was like a major bottleneck that we were trying to solve. Then comes orchestration. People usually often like break down like a large task into a bunch of small tasks and like work hard trying to land each one of them. Um we are like default sub agent build. You know once a plan is built you know it has a dependent it comes with a dependency graph and sub aents go do independent pieces of work right. Um and then testing is like another major bottleneck. If um um um [clears throat] if you still need to pull stuff to local host to test like like you you can't

[6:52] transition to the cloud. So we built um like a a detailed testing framework where you know browser testing happens on the machine um end to end testing happens and uh you know uh the output is something that the that proves to the user that things are working right so for me like I really enjoy like looking at a video which proves that the the new feature actually works or you know sometimes like I really you know it also gives me like staging link where um for

[7:26] that particular feature I can click around um because it's anyways hosted on a machine right so you can just like run the whole app on that machine click around play with it and um um and see if it works so that's the that's the way to like completely remove localost as a requirement for testing um post that code review becomes a big bottleneck um often times people ask multiple models to do reviews for you And we baked that in inside the harness. You can customize the harness. And many people often ask

[7:58] often build with claude and get uh GPT to do their review. Um and you can have like multiple reviewers looking at like different angles. These are all sub agents. Um so you can basically customize the harness which uh um solves a lot of the reviewing bottlenecks. Then comes the merge. Um often in fastmoving teams when people are agents are opening a lot of PRs in parallel um you need something like a merge queue which we built which uh constantly like rebases keeps uh keeps you mergeable with master

[8:34] and like lands the PR by itself. So you have a bunch of these bottlenecks um that needs to be solved before you can transport the user entirely into into the cloud and uh really enable longunning multi-hour running cloud agents. So that was Warflex 1.0 which we launched about um about a couple of months ago I believe and uh that has sort of like really taken off and we learned a lot from it. [clears throat] So the biggest thing that we realized was now the bottleneck changed. Now that longunning agents are possible, we were

[9:08] able to run a lot more tasks. You know, if desktop coding sort of enabled maybe 3 to five things in parallel, longunning cloud agents started enabling 20 30 things in parallel, right? So you know obviously it sort of provided a lot more leverage and now the bottleneck sort of changed from writing code to project management and uh you know making sure like the stuff lands and is actually useful um in making sure the things that are in my head are actually started you know because I have a limited context

[9:42] window once it sort of like exceeds um 10 tasks in parallel it gets like really really hard. So the bottleneck moves into project management. Actually the model advances of the recent months also point in this direction. The latest gains have come from orchestration. So you know most of the latest models try to offload um the chunk of heavy lifting into sub aents and the main agent you know wants to act as a orchestrator so that you maximally use the maximally generate

[10:18] intelligence within a context window. So fresh context windows um give a lot more intelligence budget and you know that's the way things are pointing. So that enables um a really nice project manager which starts and orchestrates a bunch of sessions and uh um and lands things for you. So that's Warflex 2.0. Warflex 2.0 is basically uh um a bunch of Autobots. These are 24 + 7 employees that work towards a goal. the the bottleneck actually changed from um giving a task

[10:53] and getting getting it done to actually even starting the task. The one thing that we started noticing was there was a lot of incremental intent that you could just capture from the way things were happening. For example, like if a customer call ends with a bunch of to-dos, those are all intent that I don't need to like copy paste and start one at a time. Um, so [clears throat] like the mere act of even like noticing, remembering and starting each one of them could just be automated. Um, [clears throat] so most teams treat

[11:28] agents like a task Q and a task Q only moves as fast to the person feeding it. But if you actually look at what's in the queue, most of it doesn't need you. The end to end plus one, that intent is already there in the codebase, the alert or the transcript. It doesn't need a genius to start it. you can you can sort of figure out from the customer transcript this is what you want to start. You can figure out from a production alert um what you need to solve. Those things need to be on autopilot. It just needs an owner um and it needs to be like multiplayer and

[12:01] collaborative with the rest of the team who where the ownership might be distributed to make sure all these sort of parallel sessions actually land. This is the next phase where of Warflex um and even um coding agents in general where things are moving from single player to like truly multiplayer and moving from um reactive to proactive where the intents that are already in there are being captured and used. So I would say like you know there are two kinds of work there is z truly 0ero to1 work that's like the truly creative

[12:33] stuff where the customer can't really even ask for it. it takes taste or judgment. That's the part that's still human and uh you know I I like doing that stuff and the part that's going into the autobots is the end to end plus one stuff where uh the intents are sufficiently present as a part of the signals that the company is getting. So that's the new bottleneck and that's what Warflex 2.0 um is all about solving. Now people have tried to automate it and have had scars um doing something fairly simple. So for example,

[13:06] you know, people have set up automations to solve all sentries. You tell it to solve all the centuries and it goes crazy. Like a flood of PRs just hit you that nobody has times to time to merge. It pings you all day like one at a time and it's noisy. It often just silences the alert and leaves out the root cause. Um and a token bill that bursts u while the agent runs for hours on something nobody wanted. It's a black box. You can't trust it with anything that matters, right? You know, these are all the fears that uh that uh people end up with when they just like point um a fire

[13:42] hose of incoming events, company events on on an agent and or an automation. That doesn't really work. People have burnt their fingers. What you what what you need is a bot which actually has common sense. Um think about a new hire you don't fully trust yet. You give them important things first. You expect them to check in a lot early. You give them more as their work holds up and less when it doesn't. They work inside a budget and you can see what they do. Nobody hires a person and says solve everything. That's the bar that we built

[14:17] um for flex 2.0 and it's the next rung on the ladder. 1.0 finishes the work that you start. 2.0 starts it. It gives you Autobots 24 + 7 co-workers that live in. You give an Autobot a goal um and a home channel. it stays plugged into your web hooks and starts the work itself. Um, we even built a directory of opinionated bots, right? And you can, you know, start from there and change it. Um, that's the big uh thing, you know, pe people can't imagine these bots. So, we've built a directory and we've sort of made sure um um the ones

[14:51] that we like and works for us, it's uh available out of the box with my taste and judgment to you. Um so so one [snorts] of some of the most you know I'll just walk you through some of the most uh wellused bots. Um we have an on on call bot that triages sentry and page your duty alerts and investigates before an engineer is looped in. A CI bot that keeps speeding up your builds. A project manager bot which we started using a lot which holds a whole project in one channel and reports progress and blockers every day. Um this is super

[15:25] cool because it can it can make progress on things. It can tag people for reviews once uh some work needs to be reviewed. It can make your project run on um on insane speed. One of the nice Autobots that we have we have is like uh it it watches customer calls. Um for example, you know, I was rolling out uh our beta to a friendly customer and the bot had a bug. It didn't respond back in the Slack channel right after. So you know normally I would have taken a screenshot and tagged Warflex um to make it make it go work on the bug. This time I just you

[16:00] know after the call ended the Autobot just read the transcript and found my to-do located on the screen at that time stamp because you know it also has the you know video alongside the screen share alongside and uh it it checked with me whether it wants me to fix it and I said yes. It tagged the right engineer who who had owned the fix and uh you know came back with the PR. The engineer approved it. It uh it got merged. Um it got deployed. It closed the item and it even drafted a follow-up to the customer. Um I approved the

[16:34] follow-up and u it went it went to the customer that it was fixed right. So that that's the kind of leverage you know you just like I think the future is just like approve approve approve. lot of these routine stuff is like you you just approve it and even there like a bot sort of like learns um how much confidence it has and like keeps moving forward and over time it gets better and better like an employee. So um [clears throat] one one thing for this room on why it works now the latest model training runs focused on orchestration a main agent that plans and keeps track with heavy

[17:06] lifting pushed down to sub agents. Most frontier models can now solve a well-defined task and their output is hard to tell apart. The next level up is a manager. An agent that starts sessions and keeps track of them. That's an autobot. It also runs on what you already have. Most uh teams bring their cloud code or codec subscriptions. Larger API users can route the well specified work to open models and keep the frontier models for judgment and communication. That way you can save a lot of money. Obviously the subscriptions save you a lot of money or if you're not eligible for it, the open

[17:39] source models save you a lot of money. What we built is an agent that decides what to work on next inside the limits you set and shows you why. Ultimately, if you follow maximizing the leverage per person to its end, you get a company that runs on loops. A customer call ends and the product gets better. An alert fires and someone already knows why. CA slows down and a tested fix is waiting for review. The people spend their day on 0 to1 and on building the next loop. Our northstar is a zero employee

[18:12] company. A northstar tells you which way to walk. Um it doesn't say that you arrive. 10 people driving a huge business rounds down to zero. We're early. Autobots will get things wrong. some responsibilities aren't ready to hand over um but we're building the next Lego block um you know the larger Lego block which is assembled with the underlying models Tesla took ground one intervention at a time where uh the way they solved autopilot is by profiling which uh which areas or scenarios the model made mistake and that's what we do

[18:48] we profile where humans spend their time and what the bottlenecks are and figure out how to throw tokens and intelligence at the problem. We climb the leverage one rung at a time as a new bottleneck shows up. We try to we are probably in a super intelligence take off and uh the opportunities to rewrite much of how the world runs are like insanely high. Companies build record revenue in super small amount of time. The growth rates are incredible. Something that I've never seen all my life. But also it's

[19:21] like one of the most competitive spaces ever. Um um the teams that tend to win tend to be like really small with uh everyone having a lot of ownership and leverage. It's it's not the traditional incumbents are not able to adapt and like um and compete. The this is a land grab and it goes to small teams with taste, judgment and an insane amount of leverage per person. Own the 0ero to one and take as much ground as you can in this land grab. Thank you so much guys.

[19:54] Really appreciate the opportunity speaking with all of you guys today. Thank you.
