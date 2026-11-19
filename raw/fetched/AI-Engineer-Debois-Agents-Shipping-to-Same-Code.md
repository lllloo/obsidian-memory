---
title: Your Team's Agents Are All Shipping to the Same Code at Once — Patrick Debois
description: AI Engineer 演講：Patrick Debois 談多人多 agent 同時合進同一 main 的協調與 merge train，附逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/fTUinMqA1XQ-your-teams-agents-are-all-shipping-same
published: 2026-11-10
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript JSON 下載連結，原為逐句時間戳，本檔依每分鐘合併成段並標起始時間，文字未改；含辨識錯誤，如 Tessl 被辨識成 Tesla、AST 被辨識成 ASD、merge queue 被辨識成 merge cube）。對應 YouTube 單場影片 ID `fTUinMqA1XQ`（`https://www.youtube.com/watch?v=fTUinMqA1XQ`，約 22 分 49 秒，上傳日 2026-11-10 取自 yt-dlp metadata）。閱讀頁的投影片與 SVG 圖未保留圖形，僅留文字。


At a glance

### Ideas worth remembering

- A ticket claim prevents duplicate work on that ticket. Announcing intended files and edits lets agents detect overlap between different tickets.
- Two passing PRs can disagree about the meaning of a value. Follow the invoice total from calculation to report and check which unit each change assumes.
- Match the handoff to the question. A stuck experiment may need a live workspace. A decision among known options may need only a choice and a shared record of the answer.
- Choose review depth using production impact and recovery cost as well as test results. Gradual rollout limits exposure, rollback reverses a release, and data restoration addresses loss that a rollback alone may leave behind.

01 [0:00 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=0s)

### The person at the center of a solo factory

Several coding agents can work on one laptop and still leave one person with a demanding job. The developer remembers what each agent is doing, makes the decisions and merges the results. Patrick Debois of Tessl calls this a *solo factory*. Behind it sits a familiar delivery pipeline that builds, tests and takes changes through merge and release. That pipeline can automate a great deal while still moving changes in serial order.

Sharing context, skills and the loops that agents run lets colleagues reproduce a setup. The coordination problem changes when those colleagues put their setups to work at the same time. Their agents all want to merge into the same `main` branch. The people share a ticket board and need to know which changes are coming. The developer who could keep the whole plan in memory on a laptop now sees only part of it.

[0:21](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=21s) [0:24](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=24s)

02 [1:58 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=118s)

### One merge creates work for every waiting PR

Debois estimates that incoming pull request volume can rise almost tenfold when a multiplayer factory starts up. What that buys the team depends on what reaches release. Two agents can keep each other busy by undoing each other’s changes. Both produce work for the merge queue while the code goes back to where it started.

Why does landing one change make the rest of the queue more expensive? Consider two other PRs waiting when the first one merges. Each was tested against the previous state of `main`. In the pipeline Debois describes, each now has to rebase, bringing its changes onto the new base, and typically rerun its tests. The two waiting branches incur that cost independently. As the queue grows, a single successful merge can trigger more CI work and a longer wait for release.

Features also compete for approval with fixes for agent incidents and maintenance of the factory itself. Someone has to review changes to the skills and loops that produce the next round of PRs. Debois uses *concurrent delivery* for the design problem this creates. Simultaneous work is frequent enough to plan for it before coding begins.

### What happens to two waiting PRs when main advances?

<svg width="460" height="451" aria-hidden="true"><defs><marker id="_R_3f9ajalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 298.7012987012987 100 L 345 131 L 345 162" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="345" y="135" text-anchor="middle"><tspan x="345" dy="0">B’s base advances</tspan></text></g> <g><path d="M 161.2987012987013 100 L 115 131 L 115 162" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="115" y="135" text-anchor="middle"><tspan x="115" dy="0">C’s base advances</tspan></text></g> <g><path d="M 345 273 L 345 312 L 345 351" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="345" y="308" text-anchor="middle"><tspan x="345" dy="0">typically reruns</tspan> <tspan x="345" dy="16">checks</tspan></text></g> <g><path d="M 115 273 L 115 312 L 115 351" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9ajalm_)"></path><text x="115" y="308" text-anchor="middle"><tspan x="115" dy="0">typically reruns</tspan> <tspan x="115" dy="16">checks</tspan></text></g></svg>

**A PR lands on main** The base changes for the remaining PRs.

**Rebase B** Waiting PR B — Bring B’s changes onto the updated main.

**Retest B** Waiting PR B — Run B’s checks on that combination.

**Rebase C** Waiting PR C — Bring C’s changes onto the same updated main.

**Retest C** Waiting PR C — Run C’s checks on its combination.

Both paths start at the same merge. Each waiting PR checks its own changes against the updated base, so CI can repeat work even when neither author adds a feature.

Read the diagram as text
- **A PR lands on main.** The base changes for the remaining PRs.
- **Rebase B.** Waiting PR B — Bring B’s changes onto the updated main.
- **Retest B.** Waiting PR B — Run B’s checks on that combination.
- **Rebase C.** Waiting PR C — Bring C’s changes onto the same updated main.
- **Retest C.** Waiting PR C — Run C’s checks on its combination.
- A PR lands on main → Rebase B: B’s base advances.
- A PR lands on main → Rebase C: C’s base advances.
- Rebase B → Retest B: typically reruns checks.
- Rebase C → Retest C: typically reruns checks.

[2:00](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=120s) [2:04](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=124s)

03 [3:50 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=230s)

### Claim the ticket, announce the files, isolate the work

Authentication and payments suggest a natural split between two agents. A graph of the code can help identify pieces that actually separate well. Where two tasks come close together, the assignment can get more precise, down to a file, a function or even individual edits within a file. Doing this during planning reveals how much independent work there is before the agents start.

An agent claims a ticket on the board so another agent leaves that task alone. It also announces which files it expects to touch and what it plans to change. The announcement serves a different purpose from the claim. Two agents can each own a different ticket and still discover that their plans involve the same function. Publishing the intended edits gives them a chance to spot that overlap while they can still adjust the work.

Separate Git worktrees give agents their own working files. Isolation can extend to the things those files depend on. An agent can have its own machine and context, a fixed API version, a database snapshot and its own test data. Mocks or digital twins can stand in for outside systems. An agent can then run an experiment without another agent changing the data underneath it or the experiment affecting the outside world. The resulting code will still need to meet everyone else’s changes on `main`.

[4:01](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=241s) [4:11](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=251s)

04 [5:57 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=357s)

### When two agents reach the same code

![An arrow leads from shared resources to nested boxes for one agent’s machine snapshot, API twins, database branch, test data and private context. A return arrow requires review through a pull request.](https://ai.engineer/api/talk-essay-media/b6108e4a5b077507b848171284d0f826363a5db9d7970e14aea20b90bcf042fd)

Separate Git branches still leave agents with different views of shared task state.

A collision during execution leaves a choice about the plan already in flight.

- **Wait and retry.** Let one agent finish the contested work, then give the other another attempt.
- **Requeue the task.** Return the waiting work to the queue until the work it depends on is done.
- **Renegotiate the split.** Change who does what while the agents are working. If they can agree on separate edits, both can continue.

If the overlap survives until merge time, one option is to rerun the work and try the merge again. An agent could also inspect the whole function containing the conflicting lines and attempt a repair that accommodates both edits. An agent that can see a neighboring change coming could go further and adapt its own code while the other change is still in progress. That possibility depends on knowing what the other agent intends to do.

[5:57](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=357s) [6:01](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=361s)

05 [7:21 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=441s)

### The invoice that merges cleanly and reports the wrong unit

What unit does the report expect to receive? One PR changes the function that calculates an invoice total so it returns cents. At the same time, another PR changes how the total is reported. The reporting change still expects dollars. The edits can touch different lines and their tests can pass, yet the output of the calculation is the input to the report. A number calculated in cents would be read as a number of dollars.

Debois proposes having an agent compare the intents of the incoming PRs. For this pair, the agent would need to follow the total across the two changes and ask where the conversion to the report’s intended unit takes place. If the changes disagree about that responsibility, the agent has something specific to flag for a person or to correct in a PR.

[7:30](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=450s) [7:38](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=458s)

06 [8:20 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=500s)

### Check which changes can travel together

![A queue tests A, A+B and A+C in parallel. A+B fails, sending B back to rerun. A and C land on main, and a release train takes the batch through a deployment gate to production.](https://ai.engineer/api/talk-essay-media/03fc124ebd17f8e68e79bc38ed84527e838452649f3138542f9a954c0cc96098)

The train tests possible combinations in parallel while earlier changes wait to land.

If one PR fails to land, which others actually have to wait? A queue that processes each candidate in turn can leave the rest rebasing and redoing work after a failure. A *speculative merge train* looks ahead at the incoming PRs and checks candidates in pairs for compatibility. If one candidate drops out, the queue already has information about which other changes can go through together. Those candidates can advance while the troublesome one waits.

The train spends effort checking combinations ahead of time to reduce waiting later. What those checks establish depends on what they test. A train that only checks whether the invoice edits merge and pass their existing tests could carry the unit error straight through. Debois expects planning, merge handling and analytics for concurrent changes to become developer infrastructure in their own right as teams outgrow simple agent loops.

[8:29](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=509s) [8:35](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=515s)

07 [9:40 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=580s)

### A conversation becomes a ticket the team can execute

![Three answers become checks on the ticket. The export must contain the columns finance needs, cover only the last 90 days and list refunds as negative rows.](https://ai.engineer/api/talk-essay-media/60e5954e5e644e1ae8f489290f83e061d66c36a9ea0f36fda3c6fef068f73e84)

Questions raised during planning become acceptance checks on the same ticket.

One shared board makes incoming changes and work in progress visible beyond the developer who started each task. Visibility also exposes a bottleneck. Several agents can ask for attention at once, and moving all their questions onto a board still leaves people answering them.

One way to put that attention to better use is to invite an agent into a conversation the team is already having. Several people can clarify the same request while the agent refines the ticket. The agent can ask what behavior they want, which requirements apply and what test would show that the work is done. The answers turn the ticket into something like a coding agent’s plan, available on the board for everyone to inspect.

Consider the old path for a request from sales, marketing or support. A colleague filed a ticket and could wait weeks for an engineer to pick it up. Building a quick version independently brought another problem when the result didn’t fit engineering practice. At Tessl, colleagues bring the agent into their organizational chat. They can experiment, refine the feature or start building it using engineering’s pipeline, knowledge, skills and loops. The support colleague who knows the original requirement can help settle what the feature should do while the idea is still taking shape.

[9:48](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=588s) [9:51](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=591s)

08 [12:54 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=774s)

### Step into the stuck agent’s workspace

What would you need in front of you to unblock an agent? When a ticket calls for rapid experimentation, another round of comments can be slow. In the handoff Debois describes, the stuck agent opens an IDE with its working context and files already available. A person can try an experiment there, make the missing choice and hand the work back. The agent resumes with the result of that intervention.

Some tasks only need a decision. The agent can present a few options, let a person pick one or override them, then continue. That saves the person from having to reconstruct the problem and write the next prompt from scratch. The choice goes into a shared decision log. A colleague can trace who decided what, and an agent in a later session can query the same decision when it needs that context.

[12:57](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=777s) [13:03](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=783s)

09 [15:06 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=906s)

### Size the change for its reviewer and its production risk

There is a second reason to divide the work. A change can be isolated from other agents and still be too large for a person to review well. Smaller PRs can move through merge trains in pieces that reviewers can understand. Better context and tools can reduce failures before review, and another agent can challenge the code before a person sees it. Screenshots of a flow, video and test results give the reviewer a way to inspect what the change actually did.

When developers tell Debois they have stopped reading the code, his follow-up is about the impact of sending that change to production. An application with no customers has a different exposure from a service people rely on. Even within one application, the review decision can vary by change.

- **Documentation.** A limited-impact edit may go through after the applicable checks.
- **Authentication.** A mistake can have enough impact to justify closer human review before release.
- **A feature that can roll out gradually.** Release it in stages and inspect the output and errors as it reaches users.

Recovery changes that calculation too. If a release could lose data, how quickly could the team restore it? If one node fails, what happens to the service? How quickly could the team roll back a bad release? Review and testing can lower the likelihood of failure. Architectural choices about node failure, rollback and data restoration help determine how costly a failure will be once it happens.

[15:08](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=908s) [15:15](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=915s)

10 [18:03 ↗](https://www.youtube.com/watch?v=fTUinMqA1XQ&t=1083s)

### Who keeps up with the changes, and who owns the factory?

Debois works remotely while most of his team gathers in London. He already had trouble catching up on changes discussed in the room. With several agents producing code, marketing and support can find themselves in much the same position. A list of merged PRs leaves them to work out the implications. Communicating a change in the language of each group’s work becomes part of delivering it.

The more routine work the agents handle, the more valuable it becomes to route an exception to someone who can decide it. Someone also has to maintain the system doing the routing. Debois sees a *factory team* emerging, much as a platform team might look after a cluster. Its responsibilities include establishing who owns each skill, keeping shared context up to date, connecting agents to the right components and monitoring the factory. An outdated instruction shared by the whole team has a different reach from one sitting on a single developer’s laptop.

The shared log gives an agent a way to recover a decision someone has already made. Debois’s team is exploring what happens when the board needs a new decision. A personal agent working there on someone’s behalf could answer another agent’s question and exercise the judgment that person has delegated to it.

[Transcript download](https://ai.engineer/api/data/transcript?slug=youtube-2845a3cf72610a8ad7ae&format=json)

Full transcript


[0:00] Welcome to our session on multiplayer software factories where I'll walk you through what the tensions are, what the solutions are when multiple people and multiple agents are working on the same software delivery pipeline. Software delivery pipelines are of course not new and existed before uh uh AI and you know we have the typical build test and then kind of wait for the release and the merge to go out into main. uh this is pretty much a serial flow and it has helped us automate and be more robust in the delivery. At the same time, people are building factories and I call them solo factories on their laptops on their kind of systems uh within their coding agents and increasingly they're using multiple agents and doing kind of delivery with agents. Now they often have to still make the decisions and they also have to do the merges and they kind of are a little bit of this central piece or almost like they have to keep

[1:01] the memory what they're doing and so on. I'm talking not single player of not solo player but uh multiplayer and there's probably a gradation in between currently people doing it on our laptops then people sharing their setups like their context their skills their loops within their factories pretty much the state of many factories out there and then the multiplayer factories of people collaborating at the same time uh in the same kind of uh kind of ticket board uh on their same code base And that's what I'll work you through today. Now on the left, the tension is everybody wants to merge into main. On the right, there's multiple people on the board and they have to collaborate and work together. So that's kind of the two parts of this talk. Let's start with the first part, the code, and how to make that like a central piece of agents being able to work together. You know, one of the first things when you turn on a factory or multiplayer

[2:02] factory, you'll see that there's definitely an increase in pull requests, you know, it almost like a factor 10 uh of more and more pull requests landing. Uh that's good because we're being more productive. We get more changes done and but that also builds up some of the tension. For example, um we have a lot more merges and they have to make sure that they're not conflicting and if we're unlucky, the agents also spend time of going rounds around us. Uh you know, one agent changing something then the other agent changing it back. These conflicts are real when you turn on a multiplayer factory. And one of the most noticeable things is we start to wait more for releases because when we merge a change all the other PRs need to rebase and they typically rerun their tests uh and you'll have to wait and at the same time that means actually your CI/CD system is becoming a lot lot slower because of

[3:04] that multi- thing and also more costly but that's a side effect. Now the PRQ is kind of building up not just with features. There's also the agent incidents that we have to solve as I mentioned and then there's factory maintenance on their own like the improvement of the skills the improvement of the loops that we've been using all more more and more work that needs to get approved by us. So why can't we flip this from being this concurrency and it being an exception to becoming the routine? And this is what I call conc concurrent delivery and going from continuous delivery to concurrent delivery and design for people to work and agents to work together on the same codebase. Now one of the simple things that we uh can do is instead of just running and running agents just in parallel we can get smarter about this uh almost like splitting up the work like we would do with units like you get to do this task

[4:05] you get to do that task and there's different ways of splitting this in a way that we can say well you work on authentication I work on payment I work on other parts and we can use even the ASD graph to determine which pieces are like able to split quite well and then we can go have the agents go on more granular level and they would do like hey this file this function and even they would go on certain keystrokes like in certain files doing together. So this is a way of kind of dealing with kind of more uh splitting of the work before you actually do uh the actual coding. This is a better way of planning the changes. And then once uh you start planning and you start actually executing the plan uh much like you would do on your uh scrum board, you would say I'm going to take care of this and the agent writes and says it claims the ticket. It says I want to do that ticket. So no other agent can actually step in at the same time. And it also announces which files

[5:06] and which changes it's going to make. So this is something that is helpful for other agents to see that they're not starting to overlap during the planning and the execution. Now to make sure that they can keep executing um a lot of people use work trees to kind of separate them. When you kind of think about this broader there is a lot more splitting that you could do. You basically are phrasing the world of an agent. You give them their own kind of machine. You give their their own phrase of the context. to give them their own version of the API that's being locked and even the database gets their snapshot their test data and even outside world like digital twins and uh kind of making sure that everything's mocked and that they can do these things without having to deal with any impact of the outside world. Now when two agents do collide during the work there's a couple of strategies they can either start like waiting for each other um one after the other they

[6:06] can retry after the wait they can say like okay I'm going to wait but I'll recue and I'll wait until it's done or they can start changing and optimizing the plan like you do this I do that and that's renegotiation uh in the end so they're changing actually the planning while they're doing the execution to make sure that they don't interfere with each other. Now on a conflict you could rerun it. Um and within get you're merging today and you say okay there's a conflict. What do I do? You rerun and see if it merges on the rerun which was typically our PR uh change or you could just kind of make sure that the agents do that for you instead. So they can see whether they can merge instead of just by code lines. they can merge by function and it becomes smarter and then the agent maybe can fix [clears throat] the merge so you don't have to do that again and ultimately it can even start seeing changes coming so hey this agent is

[7:07] probably going to change this I'm going to see this coming and I'm already kind of adapting my code uh at the same time so this is thinking in concurrency instead of being kind of serial in the changes now one of the things you can see is that you agents have been optimized to merge stuff, right? Like with the merging of code, this is clear. But what if two changes land at the same time? In this case, you're calculating and changing the function of calculating the the total for an invoice and say it's not just in dollars, but it in dollar cents. Now, at the same time, there is another PR that changes the fact of reporting out. Now two mergers that consistently could merge with the test succeeding but at the same time it was a different intent. The report don't want to have it in euro cents or in dollar cents. Right? So they're not conflicting in code but they're conflicting on

[8:08] intent. So we could have agents actually look at the intent whether they're still consistent across the multiple mergers and warn us or change the PR accordingly. Now, if you want to kind start merging, um the PRs are able to merge, they're good to merge. Um but what if one of those mages uh merges doesn't uh merge well, right? Then you'll have typically rebase all the others, they'll have to do rework and so on. Now, there's a better way of dealing with these merge trains is by looking uh in a concept called speculative merge trains. And it looks at all the PRs coming in and it sees which ones are compatible with each other and it kind of already checks them in pairs. And then it says like when that is landing and this one isn't landing, but you could still do the others, it goes faster because all the others that can go through already go through in the merge cube. Uh these are just some examples of kind

[9:09] of new strategies of dealing with merges and conflicts and reviews and better planning. I think in general there's a new kind of infra layer coming and you see that almost from the vendors you know it's a new developer infrastructure mergers are going to be handled differently there's now an analytics there's now a better planning there's now a better tool for anything and that's kind of what we're building up uh right now a lot of the factories are just glorified loops as we would do with the SCD but the concurrency will only increase now I told you there was a flip side to this there's also the humans working together, not just the agents. And the typically the change is that you're working together in one kind of task board, right? And all the humans are being able to see what changes are coming, what tasks are being done. And this creates the visibility where in your solo factory, you would have that doing that all alone, but it wouldn't be a central kind of board that you're working on. Now, they all need your attention, and that's probably the easy

[10:11] part, right? So we want to reduce also that attention uh from the agents having to call you all the time. So this is a side effect of having multiple agents working at the same time. Now one of the nice features is and uh it's been kind of interesting to see that agents can join your chat and this is a different way of coding. It is not you prompting but it's you kind of pulling an agent into a conversation. Uh and that's really powerful because the agent is picking up clues not just from you from your team members at the same time. And what it's actually doing it is refining the ticket from all the input. And that is really powerful because you actually not only had like adversarial review by agents, but you also get multiple input by humans on the same ticket while during the conversation. And what it's really good at is prompting you with questions instead of having to ask everything over and over again. So one thing that helpful is that

[11:14] it clarifies what is the test, what should it do, what are the requests uh requirements that it needs to do. And the ticket actually becomes almost like a plan the plan mode in your coding agent but now as a share feature within your board um of looking at all the requirements. Now what's even more powerful is that it doesn't only have to be engineers. Think of this as in the past sales marketing support they were kind of filing tickets to the engineering that would get somewhere on a board and they all have to wait until an engineering comes that could have taken weeks. Right now what we see in our factory at Tesla is that people are just sharing and doing a chat within kind of the uh organization and the agent is there. Now they don't need to build um the uh uh the code all the time and before [clears throat] they were maybe doing vibe coding but one of

[12:16] the problems with the vibe coding is it didn't fit according to engineering practices. Now with a multiplayer factory people are using the same pipeline the same knowledge the same skills the same loops to actually already fit into that flow of engineering itself. So they can experiment, they can refine the feature and they can also even build the feature where before we would wait they can just kickstart it and engineering refused that. That's a very powerful flow of getting everybody on board and being in the flow of that one multiplayer factory. Now sometimes the agent while executing is unsure and you might have the same feeling that sometimes the ticket mode within a factory is slow and you want to do fast iteration. Now there's a way to do this hybridly when for example your agent is is stuck. Uh there was a very interesting ID from Helix ML where when

[13:16] your agent is stuck is actually starts a new kind of coding IDE with the exact context that the agent was working on you as a human almost jump in uh to help the agent figure out like with all the context available with all kind of the files available and then when you made the right choices when you did the right experiments you hand it actually back to the agent and the factory to continue. So this is a nice way of finding the middle ground between a personal coding agent fast iterations and still doing the factory uh and the agent can use it as well to kind of clarify and help uh and ask for help. Now what we really want to do is reduce kind of the choices uh that it has to kind of make and what is really powerful is that it represents actually questions to us for decisions not just what should I do and open questions you know you see that in coding agents as well it gives

[14:16] you a couple of options that you can choose for and then it goes off this is really powerful and it is less trained on like having to tell the agent all the time what to do by presenting options there as well. Of course, you can override, but this is really a powerful multiplayer thing. Now, every decision that people make actually goes onto a ledger. This is like your context locally maybe that you have in your coding agent. But if you are in a multiplayer factory, this is shared somewhere on a decision log and that can be used either by agents, it could be used by humans to find and you can trace things back like who made what decision uh and when that context is being used in the next session, you can also query that as well. Now we want that to be small because big changes uh they are not very readable. So while I said in the beginning you could optimize for agent not being conflicting. There is also another kind

[15:18] of thing you have to think about which is the human review. How much change can a human review but you can build like separate Pars in multiple main merge trains for people to do fast reviewing of those things. Now a lot of people are focused on kind of you know when the PR and we want to reduce the number of PR reviews is that there is some kind of automated review. Now the first part is typically to reduce the failures which is great right like we we want to provide better context better tools we have adversarial agents look at the code before it comes to us that is a good way of reducing kind of the risk uh by it being better quality now at the same time we're optimizing that we can actually see what it did we are asking for screen flow uh shots for videos for proof for testing all the things that could help a reviewer and then ultimately how far do

[16:20] you go several people tell me like hey I'm not looking at the code anymore and I asked them okay you know but what is the impact of this going to production some documentation that is limited impact maybe you know some don't have real customers which is also great right like the impact is not a lot but if you really start thinking about what you're doing is you're selecting by what risk you can take. So some of the tests will kind of say well if it's maybe in the documentation part you can go ahead if it's like a a more impact fail change like within authentication you kind of do more kind of review by human and sometimes there's a middle ground hey this feature can just roll out we'll check what the output is whether there's any errors like gradual releases. So instead of only optimizing for quality and reducing of the likelihood, you also kind of have

[17:21] a way of looking at it from a risk perspective. And when it moves out of production, you know, you can also see how you can mitigate the risk, right? Because if the impact is that you uh lose data, do you have a fast restore strategy? uh or you can think about this like what if one node fails or can I fast roll back those are architectural decisions as well. So what you want to do is when things go wrong you want to have it being cheap to restore or to fix and that is important in not only optimizing but there's multiple ways of kind of dealing with the risk on the PR review. Now, one of the funny things when you work in a multiplayer factory is that um you know before people were chatting and I personally for example work remote where most of the team is in a central place in London. Now they get together they do a lot of chats and so on and me sometimes from remote I had a hard time

[18:23] catching up what has changed. Now, when you turn on the multiplayer factory, everybody needs to keep up, right? There's so much code being produced that maybe marketing support and other places can't keep up. They need to have a translation in their changes that have happened in their language. So, communication and radiating change is actually a very important feature in a multiplayer factory. How do you keep up within your domain within your understanding for your part of the job? Now in a nutshell you can do a lot of automation and you will use a lot of skills uh and that like context and better improvement uh on those pieces and you kind of reserve the people for the exceptions and that's the way that I want you to think about is automate what you can but make sure you are able to route to a human to make the right decision with all that infrastructure with all

[19:24] those kind of ways of working together. Um there is kind of a new team that is forming which is almost like the factory team uh similar to a platform team that was dealing with a kubernetes or with a cluster or with the cloud but right now this is they are dealing with the coding agents and the coding fabric of working all together. They make sure that who owns the skills the context is up to date. they make sure that things are connected to the right pieces uh and that the whole factory also itself is being maintained uh and being monitored as well. So this is a nutshell. There's a lot more to it, but this was in a nutshell two things like the pressure is building up on agents working more together in the codebase and then the humans also kind of working with the agents more and more together in a concurrent way and delivering more output at the same time. And for that there needs to be a lot of

[20:24] change. Now one of the things that we're playing now with is they're not just the coding agents. They're not just the people that do things in the board. Now they're being those personal agents and they will work in the uh board. They will make decisions for you. They will provide answers to other agents as well. This is a new way of building. This is a new way of kind of delegating some of the tasks that you are doing in the factory. So my advice is brace yourself. We're not there yet. like the coding agent were a good step on your solo factories. Multiplayer factories will bring new dynamics both to the agents coding and both to the organizational working together. And that's it and thank you very much for listening. You can kind of find the slides by asking uh to me in DM on LinkedIn. I happily send you in exchange for some feedback. Um and you know you can of course try the Tesla

[21:24] factory where we implement and uh are working on kind of loops factories and skills uh for you uh being in a multiplayer mode and I'd also uh shared the research at a site on concurrent.cd where I find like people and uh tools and techniques that people are solving uh this concurrency all together. Thank you very very much for listening and I hope you learned some of the new things today and feel free to leave uh some comments and I'll happily have a look and respond to that. Thank you very much.
