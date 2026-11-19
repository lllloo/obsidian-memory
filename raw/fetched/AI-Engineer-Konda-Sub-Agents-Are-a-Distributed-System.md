---
title: Your Sub-Agents Are a Distributed System. Treat Them Like One. — Girish Konda
description: AI Engineer 官方閱讀版，Girish Konda 以分散式系統概念看 sub-agent 交接並提出 SAFE handoffs，附官方機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/DxP5aW4VknQ-your-sub-agents-are-distributed-system-treat
published: 2026-11-10
tags:
  - clippings
  - ai-agent
  - agent-framework
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（取自閱讀頁的 transcript JSON 端點 `https://ai.engineer/api/data/transcript?slug=youtube-ee510e640dfcbed05b42&format=json`，按時間戳約每 12 段合併成一段，文字未改；機器辨識有錯，如 Girish 被辨識成 Gish、MCP Pacemaker 被辨識成 FCP pacemaker／MCPmaker、Byzantine 被辨識成 Baantine、asynchronous 被辨識成 a synchronous、idempotency 被辨識成 item potency）。對應 YouTube 影片 ID `DxP5aW4VknQ`（`https://www.youtube.com/watch?v=DxP5aW4VknQ`，AI Engineer 頻道，2026-11-10 上傳，約 23 分鐘）。

Loading slides…

At a glance

### Ideas worth remembering

- A deadline tells the orchestrator that a reply is late. Preserve any known process exit cause, and resolve an uncertain write by reading back its effect.
- Trace apparent agreement back to its observations. Three artifacts can repeat one guess, and a once-valid observation can expire before the next decision.
- Choose the deadline behavior per operation. Pacemaker lets a package-manager cold start proceed after 15 seconds of waiting, but refuses a new session if the session cap is still full after 10 seconds.

01 [0:00 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=0s)

### Three workers behind one function call

An orchestrator splits a task among three sub-agents. They run concurrently, read shared state from memory files, repository working trees, issues, or vector stores, and call tools that reach databases, APIs, CI systems, and deployment pipelines. The orchestrator merges their replies into one answer. To its caller, the whole operation can look like a function that takes a string and returns a string.

Girish Konda, a principal software engineer at Microsoft and the creator of **MCP Pacemaker**, encountered the consequences in engineering work and in his open-source bridge for keeping MCP servers running. Half-finished work can return fluent prose. One worker can read another’s guess. A service can signal overload while the orchestrator keeps starting workers. If a reply goes missing, retrying the worker can repeat every write it made on the first attempt. The string-returning interface leaves all four decisions to the caller.

[0:47](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=47s) [0:50](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=50s)

02 [3:08 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=188s)

### Three ways to classify an alert as benign

In a crash-stop failure, a process that was running correctly stops and stays stopped. A worker that throws an error gives the caller an explicit failure to handle. Silence is harder to interpret. A fluent but wrong reply is harder still. Konda draws an analogy to a Byzantine failure from the caller’s point of view. An entirely well-intentioned worker can report success after an incomplete investigation, using the same return type it would use for a completed one.

How much investigation went into a benign alert verdict? In Konda’s illustration, three paths produce the same classification at the same confidence level.

- **Telemetry comparison.** The worker retrieved telemetry and performed a comparison before classifying the alert.
- **Familiar title.** The worker recognized an alert title it had seen before and returned the associated answer.
- **Unsupported verdict.** The worker performed no investigation and generated the answer anyway.

The next decision might depend on whether anyone inspected *this alert’s* telemetry. Even retaining the confidence alongside the label gives the orchestrator no way to recover that information.

[3:13](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=193s) [3:16](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=196s)

03 [4:54 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=294s)

### What a 30-second timeout can hide

When a deadline expires, the orchestrator knows how long it waited. The worker might still be running, it might have crashed, or it might have finished and lost the reply. The 1985 FLP result concerns the limits of reaching agreement when a process may fail and messages may be delayed. The practical connection is the difficulty of telling a delayed process from a dead one. A timeout-based failure detector can raise a suspicion and be wrong.

MCP Pacemaker needed two different fixes for calls that appeared to time out.

- **Slow first start.** A server downloaded itself on its first run and exceeded the ordinary 30-second call timeout. A working installation looked broken. Giving `initialize` its own timeout let startup have a different deadline from routine calls.
- **Crash during a call.** A server exited while a call was outstanding. When the call later timed out, the bridge overwrote the exit code that explained the crash. Pacemaker now records the timeout only if the server is still alive. When the process has exited, the caller keeps the more informative cause.

A handoff can represent uncertainty directly. The worker returns a status, the work it completed, the work still outstanding, its evidence, and any side effects. `partial` is an ordinary result. An unresolved timeout yields `unknown`, with any underlying diagnostic preserved. A2A already lets a task complete, fail, be canceled or rejected, or pause for input. An MCP tool result can set `isError` to `true`. The orchestrator still has to read those signals. A worker can mark a task complete while its account of the work says otherwise.

Konda’s individual Internet-Draft on evaluation states makes a further distinction. A check that ran and returned false establishes something about the condition. A check that could not run leaves the condition open. Collapsing both into a negative result changes which operation gets retried, who gets paged, and what a later audit says was checked.

[4:54](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=294s) [5:00](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=300s)

04 [7:28 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=448s)

### How one guessed percentage becomes three agreeing artifacts

![Among five circles, a read quorum of three and a write quorum of three overlap at one circle. Alongside, three sub-agents vote unanimously using the same guess from shared context.](https://ai.engineer/api/talk-essay-media/f3bfa2dc9ca53bf61986982e68ad53debb2e2add1816d7b300d3a4c39b7bc7a7)

Three agents reading the same incorrect context can all agree. The comparison shows why three such answers offer no independent confirmation.

Where did the apparent corroboration come from? In a hypothetical incident, a worker writes into shared context that the error rate fell by 80%. It inferred the change. A second worker picks up the sentence for a review note. A third reads the same context and uses the drop to justify proceeding in a runbook. When the orchestrator merges the three artifacts, the percentage appears in an investigation, a review, and an operational decision. Tracing either downstream branch leads straight back to the first worker.

The database analogy is a **dirty read**. A reader sees a value before the writer commits or rolls back. In shared agent context, a sentence becomes readable the moment a worker writes it. Without a marker for unchecked material, another worker can act on a guess before anyone has established where it came from.

Would asking three agents for a quorum help? In the 1979 weighted-voting scheme Konda invokes, the read quorum weight plus the write quorum weight exceeds the total voting weight. That inequality forces every read quorum to overlap the latest write quorum. Counting agreeing agent answers supplies no comparable guarantee. Here, all three answers inherit one unsupported sentence.

### Where do the three accounts of an 80% drop get their evidence?

<svg width="593" height="451" aria-hidden="true"><defs><marker id="_R_3faajalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 353 106.6413043478261 L 478 158 L 478 206.5" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="478" y="154" text-anchor="middle"><tspan x="478" dy="0">Read from shared</tspan> <tspan x="478" dy="16">context</tspan></text></g> <g><path d="M 248 119 L 248 158 L 248 197" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="248" y="154" text-anchor="middle"><tspan x="248" dy="0">Read from shared</tspan> <tspan x="248" dy="16">context</tspan></text></g> <g><path d="M 143 118.625 L 68 158 L 68 243 L 68 320 L 143 352.0833333333333" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="68" y="247" text-anchor="middle"><tspan x="68" dy="0">Original finding</tspan></text></g> <g><path d="M 478 279.5 L 478 320 L 353 361.8478260869565" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="478" y="324" text-anchor="middle"><tspan x="478" dy="0">Review artifact</tspan></text></g> <g><path d="M 248 289 L 248 320 L 248 351" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3faajalm_)"></path><text x="248" y="324" text-anchor="middle"><tspan x="248" dy="0">Runbook artifact</tspan></text></g></svg>

**First worker’s finding** Writes an inferred 80% error-rate drop into shared context.

**Review note** Repeats the sentence.

**Runbook step** Uses the drop as a reason to proceed.

**Orchestrator’s merge** Receives three agreeing artifacts with one source.

Follow the arrows into the merge. The review and runbook each inherit the first worker’s inference. Neither branch adds a measurement.

Read the diagram as text
- **First worker’s finding.** Writes an inferred 80% error-rate drop into shared context.
- **Review note.** Repeats the sentence.
- **Runbook step.** Uses the drop as a reason to proceed.
- **Orchestrator’s merge.** Receives three agreeing artifacts with one source.
- First worker’s finding → Review note: Read from shared context.
- First worker’s finding → Runbook step: Read from shared context.
- First worker’s finding → Orchestrator’s merge: Original finding.
- Review note → Orchestrator’s merge: Review artifact.
- Runbook step → Orchestrator’s merge: Runbook artifact.

[7:31](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=451s) [7:39](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=459s)

05 [9:09 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=549s)

### Choose what the orchestrator can promise

A consistency model says what a reader may rely on when operations overlap. **Linearizability** makes each operation appear to occur at one point in real-time order. **Sequential consistency** gives everyone one total order that respects each process’s own order. **Causal consistency** preserves the order of operations that depend on each other. **Session guarantees** can let a client read its own writes and avoid moving backward on successive reads. **Eventual consistency** promises convergence after updates stop. Giving workers a shared context leaves all of these questions open.

Requiring a single real-time order has an availability cost when the network splits. Causal and session guarantees leave room for a client to keep working if it stays attached to one place. In Konda’s design, that place is the orchestrator. His **SAFE handoffs** draw on Pacemaker, his other engineering work, and his individual draft.

- **S — Source reads.** A worker passes on the source, version, and time behind a fact. The decision that uses it checks whether it is still fresh.
- **A — At-most-once effects.** Each write has an identity and a single-use approval for that action. If its outcome is uncertain, the caller reads it back.
- **F — Fan-out budgets.** Each downstream dependency gets a limit and a bounded wait. When the system refuses work, the refusal counts as a failure.
- **E — Explicit outcomes.** Each handoff ends in a named state. A timeout can leave the outcome `unknown`, and a known cause survives for diagnosis.

[9:16](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=556s) [9:19](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=559s)

06 [11:35 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=695s)

### S · Check the source at decision time

A worker handing on a fact supplies a record of the observation. The record names the claim and its revision, the source and its version, and the scope over which the claim applies. It also distinguishes three times that a single timestamp would conflate. When was the source data current? When did the worker read it? When did a decision use it?

How long can the next worker rely on that read? In Konda’s example, the data covers events through 9:05. A worker reads it at 9:06, and a decision uses it at 9:07. The data is two minutes old at the decision, within the chosen five-minute limit. At 9:15 the same data is ten minutes old. The orchestrator rejects the stale record and requires another read before the next decision.

Copying the claim into a new note does nothing to advance the time through which the data was current. The same record requirement exposes the problem with the earlier 80% drop. A worker that observed the drop could identify the source and when it read it. The worker that guessed has no such observation to hand on.

[11:47](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=707s) [11:52](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=712s)

07 [13:09 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=789s)

### A · Recover a write by its identity

![The initialize handshake is safe to replay. An uncertain tool call may already have executed, and resuming can repeat a write. The flow assigns the effect an identity, approves the exact action once and reads it back by identity to confirm it.](https://ai.engineer/api/talk-essay-media/0d0f37636a47bd8ddd31f88c734ce9be53c668bcc3f4735778efecbca3409125)

A restarted worker can repeat the initial handshake. It needs a stable action ID and a readback to establish whether a write already happened.

Suppose a sub-agent calls a tool to create a pull request. The tool makes the write, but the reply is lost. From the orchestrator’s point of view the outcome is `unknown`. If it delegates the whole task again, the worker reaches the creation step a second time. The first pull request can already exist while the orchestrator is still waiting to learn whether anything happened.

The 1984 remote procedure call example makes the ambiguity precise. Under its semantics, a normal return means the procedure ran once. An exception leaves two possibilities, zero executions or one. Forgoing a retry preserves at-most-once execution at the cost of possibly losing the operation. Retrying for at-least-once execution admits duplicates. Getting exactly one observable effect requires both eventual execution and a way for the receiver to recognize duplicate attempts, for example with an idempotency key. MCP’s idempotency hint describes a tool property. The tool implementation has to supply the behavior.

Pacemaker distinguishes two operations during recovery. When a client reconnects after a restart, the bridge can replay the recorded `initialize` handshake against a fresh server. That reconnects the client without restoring tool state. When recycling a shared server, the bridge gives outstanding calls time to drain. If a tool call is still unanswered at the deadline, Pacemaker reports that it may already have run and leaves the caller to check. Replaying that call could duplicate a write.

SAFE gives each side effect an identity and binds a single-use approval to that particular action. After submission, the caller uses the identity to read back the result. For the pull request, confirmation means observing that the intended pull request exists. Remembering that the worker sent the request establishes only submission.

Resuming work creates a related problem. Consider a client holding a lease, a lock with an expiry time. The client pauses, the lease expires, and another client takes over. The first client wakes up and tries to write with its old credentials. A **fencing token** lets storage reject that late write. Each lock grant gets a higher number. Storage remembers the highest token it has seen and rejects writes carrying an older one.

For a resumed agent, the corresponding check belongs at the point that permits the write. Restoring a conversation can recover the plan. The system still needs to check whether the approval covers this action and whether it has already been used. Pacemaker fixed a related session bug in which an old exit or resume event could interfere with a replacement session.

[13:21](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=801s) [13:24](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=804s)

08 [16:43 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1003s)

### F · Budget concurrency at the resource workers share

![Arrows from many sessions launched via npx converge on one shared package cache. A callout beneath the cache says its lock was compromised and every session failed.](https://ai.engineer/api/talk-essay-media/0d9b5fe4ac0a4b54f41fbd794f02bec3b0d8db043907828308b79e46eb87cd12)

Many workers converge on one shared package cache. Adding a worker also adds another contender for the same lock.

Before Pacemaker limited cold starts, many sessions launched servers through `npx` at the same time. They all used one package cache. Every start in that burst failed with npm’s lock-compromised error, even though each individual request was valid. To schedule the next start, the bridge needed to know how many others were already using the cache.

A downstream service can also report that it is overloaded. It might return HTTP `429` or `503`. In the MCP tool-error example, the model receives a rate limit as a sentence. If the code that starts workers never inspects that result, the model can read the explanation while the orchestrator sends the next worker straight into the same limit.

Pacemaker uses two different admission policies, each with an explicit decision at the deadline.

- **Package-manager cold starts.** By default, two starts at a time pass through the gate. Other starts wait up to 15 seconds. Once that wait expires, a start proceeds without the gate. Konda accepted the risk of cache corruption so a stuck gate could not hang a client indefinitely.
- **Session capacity.** At the session cap, a new session waits up to 10 seconds for room. If capacity is still unavailable, the bridge refuses the session and counts the refusal as a failure in its health reporting.

Enforcing the session cap requires reserving capacity before starting a session. If queued starts each check that space exists and record their use only after startup, several can claim the same remaining slot. A limit of the right size can still fail through this check-then-act race. Reserving the slot makes the next admission decision account for work already committed to start.

[16:53](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1013s) [16:55](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1015s)

09 [18:42 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1122s)

### E · Let code decide whether the claim passes

A worker can propose a status as readily as it can propose a conclusion. To make states such as `stale` and `unknown` meaningful, the orchestrator treats the result like a request body received over the internet. Code checks the schema, looks for the evidence, checks its freshness, and recomputes numbers where possible. If a check fails, the step returns a refusal with a reason. That keeps the failed claim out of the next worker’s inputs, where a warning attached underneath it would be easy to lose.

Did the error rate fall when the error count went from ten to six? In Konda’s worked example, the first period had 10 errors per 1,000 requests. The second had 6 errors per 600 requests. Dividing each count by its own request volume gives `10 / 1,000 = 1%` and `6 / 600 = 1%`. The count fell along with traffic. The rate held steady.

Recomputing the rates gives the orchestrator a specific reason to refuse the claimed improvement. The worker can return the supported finding that both rates were 1%, or hand the decision to a person. Either outcome lets the investigation continue without passing a spurious improvement into the runbook.

[18:46](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1126s) [18:49](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1129s)

10 [20:01 ↗](https://www.youtube.com/watch?v=DxP5aW4VknQ&t=1201s)

### What SAFE costs, and where it fits

Provenance makes a claim checkable. The source itself can still be wrong. At-most-once effects leave room for zero executions, and a lost reply leaves the outcome open until read-back. If a multi-step task changed the world before failing, undoing those changes requires a compensation step designed for that action, as in the 1987 Sagas work. Ordering is similarly scoped. A reader can trace the causal history of a particular fact while independent workers’ operations have no single global order.

CAP describes the trade between consistency and availability during a network partition. Konda makes the practical choice operation by operation. Pacemaker lets a cold start through after a bounded wait because the client needs progress. For a write whose safety the orchestrator cannot establish, SAFE accepts the availability cost of refusal. Even on a healthy network, checking freshness can add another read to the decision path. Someone also has to own the work a refusal leaves outstanding.

The intended setting is one orchestrator delegating work to agents that touch production systems. If a worker only drafts text and a person reads it before anything happens, much of this machinery is overhead. Multiple orchestrators or peer agents need another way to coordinate because they lack the single place SAFE assumes for enforcing decisions.

For one orchestrator, a useful starting question is what its code will do when a worker returns `partial`, `stale`, or `unknown`. Each state calls for a different next step. Inspect what remains unfinished, refresh the evidence, or find out whether the write already happened. Giving the caller those choices lets a handoff end honestly while the task itself is still open.

[Transcript download](https://ai.engineer/api/data/transcript?slug=youtube-ee510e640dfcbed05b42&format=json)

Full transcript

Loading transcript…


## Official machine transcript

[0:00] Hey folks, this is Gish, a principal software engineer at Microsoft. Outside my job, I build open source tools for AI agents. One of them is MCP pacemaker, a supervised bridge that keeps MCP servers running. Before we start, a small disclosure. The views in this talk are my own and doesn't represent my employer. So, sub agents are a distributed system. Over the past year, I have been using agents and sub agents on real

[0:30] engineering work, dev sessions, code reviews, instant trashing, whatnot. This talk is about what happens when one agent hands work to another. So, here's an architecture. The orchestrator splits a task and hands the pieces to three different sub aents. They all run at the same time. They all read from the same shared state. Consization, memory files, repo, working trees, issues, vector stores.

[1:08] And they don't just think, they make tool calls to real systems which touch databases, APIs, CI tools, deployment pipelines and the results come back and orchestrator merges them into a single answer. An orchestrator workers shared mutable state and results merge from concurrent executions. This represents a classic distributed system. I have known how to reason with dispute

[1:39] systems for decades, but none of the setup came with it. What you get is a function that takes a string and returns a string. Failures we hit are not new, are not specific to a agents. They're classic distributed system failures. partial failure, a normal call that fails halfway through and returns an exception error code. In a sub agent case, it returns text that looks like a success.

[2:13] Dirty reads normally we have isolations versions. Here every worker reads one shade context including things other worker only guessed. Unbounded fan out. A busy service pushes [clears throat] back with the cues 429's 503s. In agents, orchestrator does not see any of this. It just starts in the worker. Retries. In normal distute systems, we build potency to make retries reliable.

[2:48] in agents a reiterate sub agent runs the whole task again with side effects included for each of these case I'll name the concept it already is then I'll put them together as a [clears throat] consistency model I'm proposing and walk through why each part is there start with the failure model because everything else depends on it a friendly case is a crash stop a process it was

[3:16] running correctly stops and stays is stopped. The subway agent that throws an error in this box. It's easy to handle. Next, no reply. The call is lost or it's very late. We'll come back to this soon. The hot case is the one from Baantine general sniper. A component that gives conflicting information. The process answers and the answer is wrong. A half finished sub agent sits closest to the box. It is not malicious but from the outside it looks the same. It does

[3:50] not crash. It answers fluently. Let's jump into this. A sub agent that half finished does not raise. It returns normal looking text with the same type signature as success. I talked about one version of this in one of my talks. We pointed an agent at an LQ. Here's an illustration I used there with three different paths which gave the same answer. The first one

[4:20] it pulled the telemetry and compared with a nonbrand set. It actually did the work. The second one it matched against the title. It it has seen before and gave the response. The third alert it didn't do anything. It just hallated. All three are categorized as benign with the same level of confidence and nothing downstream can tell these apart. The orchestrator can read the

[4:50] conclusion. It cannot read how much work was behind it. Now the call gets no reply. The orchestrator send work and the timeout fired. From here three volts look the same. The sub agent is still working. It crashed and the reply was lost. It's a hall limit, not a tooling gap. The FLP paper from 1985 showed that in a synchronous system with even one faulty process, agreement can fail to finish.

[5:22] Chundra and 2x answer in 1996 was failure detectors that can make mistakes. They suspect did not know. I hit both directions in my own open source project MCP pacemaker supervised bridge a server whose first run downloads itself hit the 30 secondond call timeout and look broken it was slow not dead we fixed it by giving initialize its own timeout now the other way the server crashed during a call the call then

[5:57] timed out and the timeout overrode the exit code that explained the crash. We fixed it by recording the time out only when it was alive. So time out is a suspicion. Record it as unknown and keep the real cause. And now make failure a value. Let's take this illustration. A sub agent returns a status. what it did, what it did not do, the evidence, and any side effects. Partial is a

[6:33] normal answer here. The protocols already have a slot for this. In A2A, a task can end as completed, failed, cancelled, or rejected or stop and ask for input. In MCP, a dual result can say is error true. But a sub agent can still say completed while its text says something else. And a loop that only reads the text never sees the difference. Another split. Checking a condition and getting no is a

[7:08] different fact from not being able to check at all. My own individual internet draft on evaluation states talks about this. Collapse the two and you change what gets retrieded and who gets ped and what the audit says later. Next dirty reads. Let's take this madeup example from one of my talk. The sub agent the trash it writes into a

[7:39] shade context saying that error rate fell by 80%. It did not measure that it inferred it. Now two other sub aents read from the same shade context. The second sub aent writes a review note and picks the same sentence up. The third agent writes a runbook step and uses it as a reason to proceed. The orchestrator merges all the all these three three artifacts agree. It is

[8:11] once unsupported sentence read three different times. The 1995 critique of SQL isolation levels define a dirty read as you read a value before the writer commits or rolls back. In a shared context, a guess is readable the moment it is written and nothing marks it as unchecked. A regular fix to is to ask three sub agents and get a quorum. Corums do work for a specific reason. In

[8:43] weighted voting from 1979, the read corum plus right corum is greater than total. So every read overlaps the latest right. The overlap is the guarantee. In sub aent's case, the three sub aents that read the same shared context does not give you that. They are not independent copies. They read the same guess. Their agreement is one source counted three different times. Let's pick a consistency model.

[9:12] In databases, we have vocabulary for this. Linearizable. Every operation appears to happen at one point in real time order. Sequential. One total order that respects each process own order. Causal operations that are causally related appear in the same order everywhere. Session guarantees. There are promises to one client like read your rights and monotonic reads

[9:42] eventual. If no new updates are made, reads eventually return the last value. A shared context gives you none of these. There's no stated guarantee at all. And you don't need the top consistency models. The strongest models cannot stay available when the network splits. Causal end session guarantees can as long as each clients stick to one place for sub agents that place the

[10:12] orchestrator. So here's a consistency model I use for sub agents. I call it safe handoffs. S stands for source feeds. Every fact a worker hands on carries its source version as of time and revision and decisions read only fresh source facts. A at most once effects every right has an identity and a single use approval for that exact action. An outcome [clears throat] is read back

[10:49] never replayed. F fan out budgets. Each downstream gets a gate and a bounded weight and refusal counts as a failure. E stands for explicit outcomes. Every handoff ends in a named state and a timeout is unknown with its cost kept. This consistency model is the one I use for my own sub agents. It's not a universal model. It's based off my own public work. Some of it is in my FCP pacemaker bridge and some are based on

[11:24] my other docs and my own internet draft. Now let's see what's behind each letter. Yes, source reads. It's the answer to that reads where one worker's guess becomes another worker's fact. What helps is to treat every fact as a record, not a sentence. Lampot's 1978 paper define when one event happened before another. A fact's provenence is that record. What it was read from and when. Let's take this madeup example.

[12:04] the record names, the claim and its revision, the source and its version, the scope and three different times, when the data was current, when we read it and when we used it. Freshness is checked where the fact is used. In this illustration, the data ends at 9:05. We read it at 9:06 and we decided at 9:07. In this case, we picked a 5 minute limit. So the data

[12:41] decision at 9:07, it's fine. Now at 9:15, the second edition came in because our freshness limit is five. This is a stale record. We reject it and we say that the next station needs another read. This is how you separate an observation from an inference. An observation has a source and a read time. An inference has none. A most of it is about retries.

[13:13] This is an illustration from my article about MCPmaker bridge. The orchestrator delegates a task. The sub agent calls a tool which does a real right. like creating a PR the reply is lost. The orchestrator knows one thing the outcome is unknown. So it retries the whole task the right happens again.

[13:45] This is a classic problem. In 1984 RPC paper it says that if the call returns [snorts] the procedure ran precisely once. If you get an exception, it ran once or not at all. And you are not told which. So you pick a delivery semantic. At most once don't retry and accept the fact that it may be lost. At least once. Retry and accept that duplicates are possible.

[14:20] Exactly once. It happened at least once. And there's a way we can dduplicate maybe by using an item potency key. In MCP item potent hint is only a hint and da or false. If you need it, you build it. Here's a small design from my bridge on how I handle it. When a client comes back after restart, the bridge replace the client's record initialize against a fresh server. That's safe. It's just a handshake and

[14:52] it does not restore tool state. What it never replace is an uncertain tool call. When a shared server is recycled, the bridge drains it and calls till unanswered at the deadline fail as potentially excluded. That status is honest. It tells the caller to go and check. What helped is giving every side effect an identity. Approval binds to that exact action. It's only used once. After the call, read back by that

[15:27] identity. Submitted is not confirmed. Confirmed means you observe the effect. The last part of a it shows up when work passes and resumes. A lease is a lock with a timeout. Martin Clipman's post about distributed locking shows this problem. A client passes while holding it. The lease expense. Someone else takes over and the first client wakes up and writes anyway. The fix he proposed is a fencing token.

[16:00] A number that goes up every time the lock is granted. The storage remembers the highest token it has seen and rejects any right with the old one. Sub agents pause and resume all the time. In my other talk, as I put it, restore context, not side effects. So treat an approval like a fencing token. One action, one use. Checked at the gate, not remembered in the prompt or conversation.

[16:33] My bridge fixed the same class of bug. A stale exit or a deleted resume can no longer remove or bring back a replacement session. Fan out budgets is about unbounded fan out. This is flow control or the lack of it. I hit this issue in my own MCP bridge before it had a limit on cold starts. Many sessions start their service at the same time through npx. They share one package cache. Every one

[17:06] of them failed with npm's lock compromised error. Nothing in any single request was wrong. The failures was the concurrency itself. And when a downstream does push back, it can arrive as a plain text. This is MCP specs one example of a tool execution error. limit as one sentence. The model reads a sentence. The orchestrator code may never look and the next worker starts anyway.

[17:34] So I introduce a kota budget in my bridge. Coal starts that use a package manager go through a gate two at a time by default. Everyone else waits and the weight is born at 15 seconds. Past that the start goes ahead without a gate. And I documented why a corrupted cache is a risk while a hung client request is certainity. There is a choice for availability made on purpose and written down.

[18:07] And I also built a cap on sessions. At the cap, a new a new session waits up to 10 seconds and then it's refused. That refusal now counts as a failure in health. Another book capacity has to be reserved before the synchronous start not after otherwise cued starts or book the cap that is a check then act race for sub agents give the orchestrator a number per downstream a bounded weight and a refused cancel. Now

[18:42] e the an explicit outcomes every hand of ends in a named state like stale or unknown not just text. The last piece is who decided that state treats agent output as untrusted input the same way you treat request body from the internet. The orchestrator also checks in code. Does the result match the schema? Is the evidence there? Is it fresh enough? to the numbers hold when you recmp compute them. If a check fails, the step returns

[19:15] a refusal with a reason. It does not pass the text along with a warning paragraph underneath. If the same model can skip a check and declare it past, you have a request, not a boundary. Here's a madeup example from another talk. A sub agent says that a rate fell. Before it was 10 errors in,000 requests. after it was six errors with 600 requests. It went from 10 to six and it claimed that our rate fell. But when we computed the rate, it's both 1%.

[19:50] We recomputed it and then the claim is refused. A supported answer is fine. A deliberate handoff to a person is fine. A confident guess it's not. So limitations because a consistency model is only useful when you know where we should stop. So here's what safe model does not do. It does not make facts true. A source fact is checkable, not correct. It does not give you exactly once delivery.

[20:23] A lost reply stays unknown until you read back. It does not roll anything back. Undoing a partial task is a compensation step you design. like the Saga paper from 1987. And finally, there's no global order across workers, only causal order per fact. And it has a price. CAP theorem says that when the network splits, you trade off availability

[20:53] against consistency. My bridge chose availability for cold starts on purpose. For rights, safe picks consistency over availability. It refuses rather than guesses. Packlac adds that even without failures, you trade latency for consistency. Every freshness check is another read and and every refusal needs an owner. So where does not fit? If a sub agent only drafts text that a

[21:29] person reads before anything happens, most of this is is a overhead. It also assumes that there's one single orchestrator. If you have more, this does not fit. Pure agents with no single place to stick to need something else. This is the consistency model I use for my own agents that touch actual real production systems. It's not universal. So wrapping up, here's three key takeaways.

[22:00] Treat every handoff to a sub agent as a network call. It can fail halfway. It can be slow and it can come back twice. Written a status, not just text. If the result cannot say partial, stale or unknown, the orchestrator will read it as done and start with our safe consistency model and enforce it in code. Keep what fits and change what does not. We already know how to build distribute systems. We just have to notice that we are building

[22:31] one. So these are some of the sources behind this talk. On the left side it's my own work, my open source projects, my articles, internet drafts and my talks. On the right side specs and standards and bunch of papers behind each concept. Thank you.
