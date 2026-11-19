---
title: Your Self-Hosted LLM Needs to Say No — Harshul Jain & Parv Khatri
description: AI Engineer 官方閱讀版，談自架 LLM 被 coding agent 爆量時於 ingress 做 admission control，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/ntVpbyDTYaQ-your-self-hosted-llm-needs-say-no
published: 2026-11-09
tags:
  - clippings
  - ai-agent
  - evaluation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，附官方機器逐字稿（閱讀頁的逐字稿區塊以 JS 載入，改由頁面上的 Transcript download 端點 `https://ai.engineer/api/data/transcript?slug=youtube-fc6cd645b9e992bf9b2e&format=json` 取得，僅將逐句片段依約 30 秒合併並加時間連結，文字未改）。對應單場 YouTube 影片 ID `ntVpbyDTYaQ`（`https://www.youtube.com/watch?v=ntVpbyDTYaQ`，約 52 分鐘）；published 為 YouTube 上傳日。逐字稿含辨識錯誤，如講者名 Harshul Jain／Parv 被辨識成 Hershel Jan／Pearl／Perv，vLLM 被辨識成 VLM／BLLM，AdmitPerf 被辨識成 admin perf／admit puff，Anthropic 被辨識成 Enthropic。

Loading slides…

At a glance

### Ideas worth remembering

- Make the admission decision before prefill commits GPU memory. A request that fits now can still put pressure on the batch as its answer and KV cache grow.
- Choose the admission unit around what must finish. Splitting capacity evenly across two dependent sets of calls can leave both agent tasks waiting.
- Give the agent an action it can take. `Retry-After` with jitter spreads returning traffic out. A caller-specific limit calls for lower concurrency. Pool-wide overload calls for a longer wait, another provider or parking the task.
- Check whether the signal moves under load, then score the policy across all arriving requests. On the A10, KV occupancy peaked at 0.5%. Capping the queue at two waiting requests cut p95 time to first token from about 2.5 seconds to about one second at the same reported goodput.

01 [0:05 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=5s)

### The prompt arrives before anyone knows the cost of the answer

Ask a model to fix a failing test. The serving system can count the input tokens when the prompt arrives. The answer takes shape one token at a time, with each token becoming part of the context for the next. By the time the system knows the output length, it has already generated the answer. Admission control has to decide whether to start much earlier, while the GPU time this request will need is still uncertain.

Follow the request through a self-hosted deployment. The API gateway checks the key and counts calls. A router picks a replica, one running copy of the model. Its inference engine loads the weights onto the GPU and batches requests so several answers can advance together. Each active request also accumulates a key-value (KV) cache, the model state it keeps for the context it has already processed. A longer answer adds more state.

How much work the deployment can take depends on what the product promises. In interactive chat, people notice both a poor answer and a long wait for the next token. An asynchronous agent can tolerate delay, but a poor answer may mean rerunning an expensive task, so quality and throughput matter. Autocomplete needs to return many suggestions quickly and can use a less expensive model. Suppose a deployment can sustain eight concurrent requests while meeting its service-level objective (SLO). What happens when 40 arrive in two seconds?

Two incidents in Jain and Khatri's review show what can give way first. On November 8, 2023, heavy traffic at OpenAI exhausted memory on routing servers. Health checks began failing. The team added replicas, rolled them back, then cut incoming traffic and restored it gradually. An Anthropic model tier slowed down during a January 21, 2026 incident and began returning errors over roughly 90 minutes. The reported cause was insufficient compute for demand. OpenAI's follow-up emphasized shedding load gracefully. Anthropic's emphasized detecting the capacity limit earlier.

[0:16](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=16s) [0:22](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=22s)

02 [8:49 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=529s)

### What the engine commits when it starts a request

![Stacks of KV-cache blocks approach a dashed GPU memory limit over time. Three panels describe evicting the cache and recomputing later, swapping it to CPU or disk, and preempting the request with an error.](https://ai.engineer/api/talk-essay-media/ba7b9db401783022ab333e247e8ffa0ff791a9356eb07eba5a72aa4aa702c5cf)

Generation adds KV pages after admission, so the memory needed by a running request can continue to grow.

Before a request takes GPU memory, an admission layer can start it, defer it or refuse it. Starting it commits the engine to two phases of work. During **prefill**, the engine reads the prompt and builds its KV cache. During **decode**, it extends the answer and the cache one token at a time. That memory stays occupied as long as the request is running.

What does a short request inherit from the calls ahead of it? Consider A, which produces a short answer, followed by B, which produces a long one. When short request C arrives, B is still in memory and its cache can keep growing. C may need little work of its own and still miss its latency target. The decision about C depends partly on a commitment the engine made to B.

If active caches fill memory, the engine can evict work, swap a request out to wait, or return an error after spending resources on it. Any of those can cost the service its latency target. Teams that self-host for privacy or cost own those decisions along with the GPUs.

A person chatting with a model leaves gaps to read the replies. A coding agent can spend those same seconds issuing calls, retrying them and starting more work. In Jain's test-fix example, the agent might read about 14 files and run about 10 tests. Across the task, tool use and follow-up reasoning can generate 40–50 calls, some quick and some long-running. At the cluster, one user's task has become a burst of related requests with different costs.

[9:22](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=562s) [9:25](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=565s)

03 [15:32 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=932s)

### Bring the request and the engine state together at ingress

![Arrows point into a policy that can admit, defer, or reject. Request inputs are input length, client or tenant, agent session, and an optional deadline. Engine inputs are KV cache use, queue age, cache hit rate, and load per pool.](https://ai.engineer/api/talk-essay-media/99f12c76d7dd76cd5dbbeb70c5b040c772be9c7807eff3b049750485160e4696)

The ingress policy combines properties of the incoming request with live queue, cache and load signals.

Which component can decide whether there is room? The agent sees its own call and controls retries. The gateway knows the API key and its rate limit. The router knows which replicas are healthy. The engine sees its batch and cache and can decide what to run or evict. In this arrangement, the component with the best view of pressure discovers the cost after the request has entered.

Placement changes both visibility and maintenance cost. A proxy at **ingress** can inspect the incoming request and whatever metrics the engine exports. At the **queue boundary**, the scheduler can intervene as it chooses the next batch. **During decode**, it can pause a running request or reclaim its cache halfway through an answer. Those later interventions have more information, but changing the scheduler can leave the team maintaining an engine fork through upstream releases. Jain and Khatri choose ingress so the policy can run against a stock engine.

What reaches that proxy, and which decision sends work onward? The request supplies input length, tenant, agent session and, when available, a deadline. The engine supplies cache occupancy, the age of the oldest queued request, prompt-cache hits and load across replica pools. The proxy can now ask whether the deployment has room for *this* caller's work. Only an admission sends the request onward to acquire GPU memory.

These inputs suggest different actions. Defer a prompt that exceeds current memory headroom or the extra calls from a session with too much work in flight. Refuse a tenant that exceeds its share, or a request whose deadline would expire in the queue. Spare KV capacity favors admission. A long wait for the oldest queued request favors deferral. A cached prompt can go first because some of its processing is already paid for. When every pool is full, refuse the arrival. For any of these rules, the observation has to be timely. A one-minute average can wash out 40 calls in two seconds.

### Which path commits GPU memory?

<svg width="690" height="454" aria-hidden="true"><defs><marker id="_R_3f9qjalm_" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M 0 0 L 8 4 L 0 8 z" fill="currentColor"></path></marker></defs><g><path d="M 460 119 L 460 150 L 413.7012987012987 181" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="460" y="154" text-anchor="middle"><tspan x="460" dy="0">Request attributes</tspan></text></g> <g><path d="M 230 119 L 230 150 L 276.2987012987013 181" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="230" y="154" text-anchor="middle"><tspan x="230" dy="0">Exported state</tspan></text></g> <g><path d="M 450 262.1521739130435 L 575 304 L 575 344.5" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="575" y="308" text-anchor="middle"><tspan x="575" dy="0">Admit</tspan></text></g> <g><path d="M 345 273 L 345 304 L 345 335" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="345" y="308" text-anchor="middle"><tspan x="345" dy="0">Defer</tspan></text></g> <g><path d="M 240 262.1521739130435 L 115 304 L 115 344.5" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#_R_3f9qjalm_)"></path><text x="115" y="308" text-anchor="middle"><tspan x="115" dy="0">Reject</tspan></text></g></svg>

**Incoming request** Inputs — Input length, tenant, session and deadline

**Engine metrics** Inputs — KV occupancy, queue age, cache hits and replica load

**Ingress policy** Decides before the request acquires a KV cache

**Start on the engine** Outcomes — Allocate cache and join the running batch

**Try later** Outcomes — Give the client a delay while capacity returns

**Refuse this attempt** Outcomes — Return a reason the caller can act on

Engine metrics travel back to ingress as information. Of the three decisions the proxy can make with that information, only admission sends work to the engine.

Read the diagram as text
- **Incoming request.** Inputs — Input length, tenant, session and deadline
- **Engine metrics.** Inputs — KV occupancy, queue age, cache hits and replica load
- **Ingress policy.** Decides before the request acquires a KV cache
- **Start on the engine.** Outcomes — Allocate cache and join the running batch
- **Try later.** Outcomes — Give the client a delay while capacity returns
- **Refuse this attempt.** Outcomes — Return a reason the caller can act on
- Incoming request → Ingress policy: Request attributes.
- Engine metrics → Ingress policy: Exported state.
- Ingress policy → Start on the engine: Admit.
- Ingress policy → Try later: Defer.
- Ingress policy → Refuse this attempt: Reject.

[16:17](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=977s) [16:21](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=981s)

04 [22:08 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1328s)

### What the agent should do with each response

![Client pseudocode waits for the Retry-After delay plus jitter before retrying. The diagram shows ten retries clustered together in the upper panel and spread across time in the lower panel.](https://ai.engineer/api/talk-essay-media/8817144544783d4554adcb80850a130da334708a6a1ef87941a8e30b0a7b554c)

Waiting exactly the suggested interval makes clients retry together. Jitter spreads their retries out.

**Admit.** A `200` opens a stream. The engine has committed cache for the prompt, and the request decodes alongside its batch, one token per step. On the client, distinguish the wait for the first token from time spent streaming. Prefill alone can take seconds under load, so Khatri starts the streaming timeout at the first token. If the agent abandons the answer, close the connection. A local timeout that leaves it open can leave the engine generating tokens and holding memory. A stream can also break after the headers have arrived. The agent then has a partial answer and must decide whether it can continue or needs another attempt.

**Defer.** For a temporary burst, the proposed server returns `503` with `Retry-After`. It can estimate the delay from when running work is likely to free enough cache. A rising queue age with capacity due back soon is a reason to ask the client to wait. Under sustained saturation, repeatedly issuing short deferrals just reschedules the same demand.

When do ten deferred clients come back? If all ten retry immediately, they create another spike while the server is still busy. Across the original burst, one retry per call can turn 40 attempts into 80. Honoring `Retry-After` gives the engine time to make progress. Adding a small random delay, or jitter, spreads the returning clients out even when they all received the same suggested wait.

**Reject.** The reason determines what the agent can change.

- **Caller over its share (`429`).** The policy may have seen a quota violation or too many concurrent calls from this tenant or session. Reduce the agent's load by capping its in-flight calls.
- **Provider overloaded (`529` in the example).** All replica pools are busy. Wait longer, switch to another model or provider, or park the task for later.

In either case, give retries a budget. Use exponential backoff with jitter and tell the user what happened once the budget runs out. Otherwise a refusal at ingress can immediately become another arrival.

[22:21](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1341s) [22:24](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1344s)

05 [27:33 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1653s)

### Twenty successful calls can still leave two tasks unfinished

A fixed allowance per API key helps tenants share the service, but it stays fixed as GPU load changes. A proxy that caps concurrent requests per replica gets closer to the hardware. Its blind spot is cost. A quick lookup and a long planning call each occupy one slot, even though their token counts, cache use and lifetimes differ. Once the queue grows, the client's timeout can end up making the refusal. A cost-aware policy estimates the incoming work in tokens and KV memory against the engine's current state.

Specifying a policy takes four choices. The **unit** says what gets admitted, such as a request, an agent session or a tenant. The **signal** is what the policy observes as the system gets busy. The **rule** converts that observation into a decision and takes time to run. The **action** determines what happens to the caller. These choices constrain each other. A deadline rule, for instance, needs the caller to supply a deadline.

What changes if the unit is a session? Imagine two agent tasks with 20 calls each and room for about half the calls. Split admissions evenly and each task gets roughly ten calls through. Both still depend on calls that failed to get in. All the capacity has been used, and neither task can finish. In the session-level alternative, A gets its full set of calls and finishes. B gets one clear deferral. A count of successful calls would miss the difference between zero completed tasks and one.

Choose the signal by the failure you need to detect. KV occupancy can reveal impending cache exhaustion. Pair occupancy with cache-hit rate when the cost is recomputation, since even a full cache may be doing valuable work by reusing prompt prefixes. Queue depth exposes accumulating waits. Deadline slack tells you how much delay a request can still tolerate. An estimate of output length helps plan for long answers. Cache pressure, for example, will miss overload on a deployment where the cache never comes close to filling.

[28:32](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1712s) [28:38](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1718s)

06 [34:01 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2041s)

### Four ways to turn a signal into a decision

The rule itself has to fit inside the time available for a decision. For the agent sending 40 calls in two seconds, a planner that takes five seconds can finish after the entire burst has arrived. Four research designs illustrate what that planning time buys and what cheaper rules can see.

- **Single threshold.** Compare KV occupancy with one limit for each incoming request. The example takes tens of microseconds per decision. It can respond quickly on each arrival, provided cache pressure actually rises under load.
- **Dual gate.** Require two signals, KV use and cache hits, to agree before acting. The example admits whole agent sessions and checks the signals in under 100 microseconds. It reported roughly four times SGLang's throughput in an offline test. That result leaves performance under live arrivals and retries open.
- **Fleet optimizer.** QLM plans across queues together to decide which requests to admit. It can account for work elsewhere in the fleet, at a reported cost of about five seconds per decision.
- **Formal deadline bound.** Calculate whether a request can still meet its time-to-first-token deadline in the worst case covered by the bound. The example makes a microsecond-scale decision and reported a drop in deadline misses from 99% to zero in its evaluation.

The papers used different models, engines and workloads, so their gains cannot establish a ranking. Jain compares them along two axes. Does the policy optimize deadlines or throughput? Does it admit individual requests or whole sessions? For a coding agent, Jain wants to admit sessions as live traffic arrives, using an engine he can deploy as shipped. The session-aware dual gate comes close because it can run without an engine fork. Its offline evaluation leaves that combination unproven.

Which rule would you try first on your own deployment? If requests carry deadlines, try a deadline bound. Otherwise, observe the deployment at peak load. If KV memory fills, try an occupancy threshold, or add a second gate when prefix reuse affects the cost of admission. If the cache has room while calls pile up, try a queue threshold. You can find out which branch applies before spending time tuning a threshold.

[34:07](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2047s) [34:12](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2052s)

07 [38:35 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2315s)

### Replay the burst and count every arrival

Start by measuring the load the replicas can sustain with admission control disabled. That establishes what 1× capacity means on this deployment. Specify the candidate policy's inputs, limits and refusal behavior. Then replay the same traffic trace with the policy enabled and disabled, sweeping offered load from 0.5× to 2× measured capacity. Below capacity a policy can appear to work simply because it has never had to refuse anything.

What score makes the cost of a refusal visible? Khatri's **goodput under admission** divides the number of requests meeting the SLO by the number of requests that arrived. For the streaming SLO here, the answer must start on time and avoid excessive gaps between tokens. Suppose the policy refuses 95 of 100 requests and serves the other five perfectly. Attainment among admitted requests is five out of five, or 100%. Goodput under admission counts all 100 in the denominator. Five percent of all arriving requests met the latency target.

The trace needs to preserve the behavior that creates pressure in the first place. Keep agent fan-out, retries and session membership. Uniform random arrivals discard the timing and dependencies the policy must handle. Set the deadline relative to latency measured without load so readers can tell how much slowdown the experiment allowed.

Khatri asks for seven disclosures alongside an admission result.

- **Load.** Give offered load as a multiple of measured capacity.
- **Deadline.** Express it relative to unloaded latency.
- **Signal liveness.** Show whether the metric the policy watches actually moved under stress.
- **Variation.** Give the repeat count and how much the runs differed.
- **Parameters.** Identify which values were tuned locally, borrowed or left at their defaults.
- **Denominator.** Say whether refusals counted toward goodput.
- **Configuration.** Record the model, engine and version, hardware, workload, SLO and baseline.

[39:29](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2369s) [39:33](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2373s)

08 [43:51 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2631s)

### Benchmark the same decision function that handles live traffic

Jain and Khatri built **AdmitPerf** to compare policies on a common deployment. Its ingress library sits in front of an inference engine such as vLLM or SGLang and makes a decision for each arrival. Its benchmark harness exercises a policy against an engine on a real GPU. Both call the same decision function, so a benchmarked rule can go into the serving path without being reimplemented. Among the 16 papers they compared on evaluation setup, no two shared the same combination of baseline, engine, workload and SLO.

The harness has five operations. Bring up the GPU-backed engine, smoke-test that it serves requests, run each policy several times, compare the results and the size of the differences, then tear the infrastructure down to stop paying for it. Provisioning sits outside the benchmark. Loading the model takes minutes, and reprovisioning between candidates would change the deployment being used as the control.

How can the harness tell an empty cache from a missing metric? Each policy declares the signals it needs. A KV-threshold policy requires the fraction of KV cache in use. If the engine cannot supply it, the harness stops at startup. Without that check, a missing value could read as zero. The policy would admit every request and produce a plausible-looking benchmark of the admit-all baseline.

For a run that proceeds, the harness records each decision with the state the policy saw. The run directory contains four JSON artifacts covering the manifest, summary, decisions and outcomes. An engineer can inspect what triggered a refusal on a particular arrival as well as what changed over the whole run.

[43:54](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2634s) [44:09](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2649s)

09 [47:48 ↗](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2868s)

### On the A10, the queue grew while the KV cache had room

The GPU comparison used a half-billion-parameter model on an A10, with the engine capped at four simultaneous sequences. The arrival rate was 14 requests per second, with two repeats. With admission control disabled, p95 time to first token was about 2.5 seconds, with variation of roughly 700 milliseconds either way. That percentile describes the wait near the slow end of the observed requests.

What did a shorter queue buy? A policy allowing at most two waiting requests admitted about 63% of arrivals and shed about 37%. Its p95 time to first token fell to about one second. Goodput under admission stayed the same in this comparison. Admitted requests saw a shorter tail wait while the fraction of *all arrivals* served within the SLO held steady.

The engine metrics explain why queue depth worked here. KV occupancy peaked at about 0.5%. Four short active sequences left ample cache even as work accumulated outside the batch. A policy waiting for high KV occupancy would have kept admitting work. The waiting-request cap had an effect because the queue was where this deployment registered overload.

There is a laptop path for trying the mechanism. AdmitPerf includes a small fake engine that implements the three endpoints the harness uses and gets busy under load. A developer can exercise the policy there, then measure its behavior on the target GPU. AdmitPerf can also discover a policy packaged separately from its repository. The tool grew out of the *LLM Inference at Scale* handbook survey. Jain points readers to both projects on the [AdmitPerf source-code slide](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=3084s).

[Transcript download](https://ai.engineer/api/data/transcript?slug=youtube-fc6cd645b9e992bf9b2e&format=json)

## Full transcript

Machine-generated source transcript; recognition errors remain.

[0:05](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=5s) Good morning everyone. My name is Hershel Jan and I have here with me Pearl. Today we are going to talk about saying no. It's called as admission control. How our system decides which request to get in when your coding agents overwhelm the LLMs you host yourself. Uh before we move on a quick intro about us. So I am a senior software engineer at Audible where I lead some of the MLAI

[0:37](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=37s) infrastructure. Uh I am also writing an open-source handbook called as LLM inference at scale. It has received over 300 plus stars by now. I am also maintaining an open-source framework called agentship which helps you ship reliable and secure agentic harnesses in an ultra fast speed. Uh perv would you like to introduce yourself? Sure. Hi everyone. I'm Perv. I'm a senior software developer at SAP. I work on like cloud application and LLM

[1:09](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=69s) infrastructure. I wrote an LLM fine-tune guide. I contribute to agentship and I'm like building a task tracker which is a local post task board for you and your agent. Uh apart from this if you would like to connect with us our LinkedIn QR codes are right there on this slide. Now back to you Hershel. Great. So here is the plan. We are going to start with understanding the motivation why

[1:41](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=101s) any serving stack can admit so much of a traffic. Second, we try to dive into admission control where the decision to say no lives and what it needs to see. Third, we will go through some of the proven strategies, the different ways a system can actually make the admission decision. And fourth, we will try to dive into the benchmarking where you will learn how to prove that your policy

[2:11](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=131s) for admission is working or it's not working. So let's get started with the motivation. Um and for this everything today uh let's try to understand what is inference. Everything today happens during this inference itself. So inference is simply a moment when someone sends a prompt to the model and gets back an answer.

[2:43](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=163s) So the step one is like a user prompt comes in. It's a sequence of words. Uh for example, it could be like failing a fix a failing test. The model which is running on your GPUs writes the answer one token at a time. A token is roughly like a word as I mentioned. Uh it writes the first word then uses that word to pick the second uh then it uses both to pick the third and it keeps on continuing like that and it cannot write

[3:16](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=196s) all of them at once because every word depends on the previous one. So those once all the words are generated they stream back to the user uh who ask for the result and that volt prompt and the answer out is like that one request. Now I want you to hold on to one small detail like model has no idea how long this answer is going to be. It only finds out whether it writes when it only

[3:49](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=229s) finds out when it writes the first last token. Keep that in mind. It will matter in the few minutes. So a model never sits on the internet itself. Every request travels through a short pipeline. It starts in your app or your agent. Then it reaches your API gateway which checks your API key counts how many requests you are sending. Then a

[4:21](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=261s) router picks a replica which which is just one running copy of the model and finally the requests land on the inference engine. The common some of the common inference engines are the VLMs, SGLAN, Tensor RT etc. engine is what actually hosts your model. It actually serves your model uh and it loads the model weights into your GPUs. It groups many requests into one batch so the GPU stays busy and for every

[4:53](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=293s) request it keeps something called as a KV cache. In plain words, the KV cache is the memory the request builds up when it try when its answer is being written. Longer the answer, bigger this memory gets. Keep this picture in your head. Every box here makes some decision but one decision is missing and we will find it out in the few minutes. First, how much an engine can actually hold.

[5:26](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=326s) Every deployment has a ceiling and it comes from the three targets that pull against each other. Quality is how big your and precise your model is. Latency is how fast the first token arrives and every token after it. Throughput is how many requests your GPUs can serve at a same time. You know the old saying good, fast, cheap, but you have to pick two. It's the same here. You cannot pick all the three. You cannot prioritize all the three. So you can't So every product has

[5:59](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=359s) to pick two. For an example like an interactive chat, you would want to go with the quality and the latency because users are more sensitive to that. It's quite obvious to the users if the quality is down or the latency is high. For something like an async agents, you would want to go with a higher throughput as well as quality. If quality is less, you will have to redo the task and redoing is very very expensive because these are the background and the asynchronous tasks.

[6:30](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=390s) And the high volume real-time systems such as the autocompletes they would try to favor latency as well as and the throughput in favor of the quality because you don't need an expensive model for doing the autocompletes for you. But whichever corner you give up there is still a maximum load you can carry while hitting your SLO your service level objective. Let's say that on this deployment it's eight requests at once. In a normal minute,

[7:00](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=420s) you never notice that limit. Now, picture the 40 requests arriving in the same two seconds. It's such a high load. And this is not like hypothetical. It has happened to like biggest providers in the world. Here are the two public postmortms two years apart. On November 8, 2023, OpenAI after a day of unusual heavy traffic, maybe not 40

[7:31](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=451s) requests, it would be some million requests, their routing servers ran out of the memory. They started failing their health checks. They added more replicas, then had to roll them back. The way out was to cut incoming traffic and ramp it up slowly. In January 21 2026 enthropic the sonnet 4.5 tire gear got slow first then it started returning errors over about 90 minutes. The cause

[8:02](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=482s) they gave was simple not enough compute for the demand. And now let's look at what each team decided as their next set of the action item. Neither of them says we need a faster engine. Open AI's followup is graceful load shedding. Enthropics is detecting capacity limits earlier. It's the same idea in the different words which is decide on your request

[8:32](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=512s) sooner to make sure which request gets in. And there are more incidents which we have linked in the appendix. If you are interested definitely go and read through them. So if you walk backward from those follow-ups, they both point at the same place, the front door. Here is the pipeline again with the missing step filled in.

[9:05](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=545s) We have a client, we have an admit layer, the Q router, and then the engine. It's never the client talking directly to your engine or client talking to your queue directly. There is an admission phase in between. Admission is a decision made before a request takes any GPU memory and it only has three possible answers. Admission decides

[9:36](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=576s) whether to start now or you want to hold the request. You want to accept it but make it wait. Third is the reject. That means not right now. It can throw different amount of errors here such as 429s and we will dive into this bit more deeper in the second part. this that is the decision that was missing from our pipeline.

[10:06](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=606s) So why does it have to happen before the engine and what would happen if you will actually accept the request what would be the cost of that yes so let's try to take a look at this like two phases of the inference like prefill and the decode. So first comes the prefill. That's the engine reading the W prompt, building the request KV cache. And then comes the decode. That's the engine writing the answer one token at a time. With every token, the cash grows a

[10:38](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=638s) little more. All of that memory stays reserved until the request finishes. So a yes is not a moment. It's a commitment that lasts the request whole life. And here you can look at the example. There is a request A, there is a request B. Once you admit a request A which is a short answer request and then you admit a request B which is a long answer request. Now when you admit a request C which is again a short answer request,

[11:09](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=669s) we don't know how longer it would take because there is a longer request which was already in the memory. Should we even take that request C or should we not even take the request C. So there is a cost associated of like admitting every request because admission could still result in missing out your SLOs's. Another impact apart from the SLOs's is your memory.

[11:40](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=700s) Here is what it does to your GPU. So every running request it keeps growing your cache as it writes. So your total memory keeps climbing. When the memory gets to the full engine has three ways to cut. Either it will aait or like throw away your request. Either it will put it to your waiting state that means it will swap or it will just say okay I won't be able to serve and I I will probably return you an error. Every one of those throws I mean every

[12:12](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=732s) one of those causes a certain delay in processing of the request. and missing out your SLOs's again while also wasting your memory. So why is it like our problem like we have con servers from open AI anthropic bold teams which are serving their own infrastructure for the inference.

[12:44](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=764s) So it's a problem for us because there are teams who want privacy. They want to have their own models hosted on their own GPUs and they want it to be hosted on their own GPUs due to the cost perspectives but they have to also protect the burndown on those GPUs. So they need to effectively decide which request to serve across their inference

[13:14](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=794s) ecosystem. On top of and on top of that like the traffic arriving at the door has also changed. Earlier there used to be a person that was chatting. He would send one request at a time. There would be a seconds of reading in between and then there would be a slow answer. But now coding agents they have taken over. There are tons of calls that these coding agents they send

[13:45](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=825s) along with the retries, pauses, um like the undo calls as well and it there is such a overwhelming traffic that your cluster has to handle and what that means is cluster has a responsibility to take a wise decision of which requests to accept and which uh requests to reject.

[14:15](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=855s) And this is exactly that visualization. You ask your agent that fix an o test. It runs all your it tries to run multiple tool calls that is reading of the files like around there could be like 14 files. There could be like around 10 tests that it has to run and it would combine together to make 40 50 calls for just one request and all these 40 requests they require like reaching out to the LLM getting back the

[14:46](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=886s) response. Uh and in between some of these requests would be long running some of the requests would be short prompt request. So we need to decide effectively where which one to pick and which one not to pick. Yeah. And that was the like reason why we need to worry about admission control. Why we need to worry

[15:18](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=918s) about handling the traffic right way across our infancy ecosystem. Okay. So this brings us to the admission control. Uh now moving on to the next slide. Uh that is slide number 18. So in this slide we will be covering three questions. Where does this decision

[15:50](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=950s) from? which request to admit and which to reject sits back at your stack and the another question is what does it need to see to make a good call or judgment on the request and what does it returns back to the client. Moving on to the next slide. So here uh we see the pipeline again which each layer's jobs is written out. The agent sees its own

[16:21](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=981s) call and decides when to retry. The gateway sees API key and request count and enforces a rate limit rate limiter for each and the router which sees replicas or healthy and which one to pick. Now the engine sees its KV cache and the current batch and decides the order of request to run and what to evict and print. So every layer decides something. Now

[16:54](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1014s) ask each of them one question. Is the room for this request? The agent says not my job. The gateway says I cannot see it. And the router say not my job and the engine says I only find out when I have already said yes. The admission box is missing in in between. So now moving on to the next slide. Um so where to put this decision change

[17:28](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1048s) what it can see and what it cost you to run. So there are three possible moments. The first is an invoice right in front of the engine. Here the policy sees the request itself plus whatever metrics the engine exposes. All you need is proxy or gateway. The engine stays exactly as it is. The second one is the Q boundary. Now the decision happens inside the engineuler

[17:58](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1078s) as it picks the next batch to run. The third is during decoding when the scheduleuler can pause a request or take back its cache halfway through an answer. Those later movement can see more but they mean changing the engineuler. That means keeping your own modified copy of BLLM or SG lang and updating it every time original changes forever. So

[18:28](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1108s) an ingress is the only movement that works with the engine exactly as it ships. So that's where we will stay for the rest of the talk. So now moving on to the next slide. Uh so what actually sits in ingress, right? Uh so you you you can think of it as a function. It can take in what it knows about the request and current state of the system and it returns one

[18:58](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1138s) of the three answers like if we have to admit the request. So the admit is the request enters the engine now and memory is committed for this moment. If it's deferred with a time we can call toao hold on like uh hold on and come back after some time and there is another decision which is with uh reject with a code that no here is the reason why and until the policy

[19:29](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1169s) says admit the request cost you nothing. It holds no GPU memory at all. Now moving on to the next slide. uh to make the call well the policy needs two views at the same time from the request and from the engine. So from the request how long the input is, which client or tenant sends it, which agent

[19:59](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1199s) session it belongs to, and a deadline. And from the engine point of view, how long uh KV cache is, how long the oldest request has been waiting in the queue, how often the prompt is already cached, and how how loaded each pool of replica is. Now look back at the ST. The gateway has left side and the engine has the right side. Nobody has the both.

[20:30](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1230s) And that's really why admission has to be its own layer. Now moving on to the next slide. Here are those eight signals turned into simple rule. Each one is compared to threshold and when it crosses it pushes towards the outcome in the colored pale from the request side. If the input is too big to fit in the memory headroom just refer it. If a client or tenant is over

[21:02](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1262s) it share reject it with 429. If one agent session has too many calls in flight defer with extras. If waiting would make a request miss its deadline anyway reject it from the engine side. Uh you can see at the bottom half of bottom half side. While KB cache is under high water mark admit it. When the oldest request has waited longer than

[21:33](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1293s) your target defer it. If the prompt is already cached admit it first because it's cheap to serve. And when every pool is full, reject it with 529. One rule of thumb, pick the signal that changes in second, like a QH, not a one minute average. A coding agent sends 40 calls in 2 seconds. A minute average won't even notice. So that's what the policy reads. Now what

[22:03](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1323s) does it say back? Now moving on to the next slide. We will take the three answers one at a time and look at each from both sides. What the server sends and what your agent should do with it. First, yes, the server sends back a 200 and the response starts streaming. At that moment, three things happens inside the engine. It commits KV cache from the whole prompt and the request joins the running batch

[22:34](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1354s) and decode one token per step alongside everyone else and it holds that memory until it finishes or until the client disconnects. That's the commitment from part one just in the form of an HTTP response which is why the admission decision has to happen before 200 never after it. Now the client side if we are writing the agent here is how to handle 200.

[23:06](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1386s) Watch the stream not the status code. First time is properly start your timeout clock when the first token arrives not when you send the request under the heavy load prefill alone can take few seconds. Second, if you decide to give up, actually close the connection. The server only frees the KV cache when the request finishes or the client disconnects. An agent that times out but leaves the connection open is

[23:36](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1416s) still holding the GPU memory. And the third one, uh, a stream can fail halfway through, right? And that that's no status for that, right? and you're you're left with partial answer and you have to decide whether to retry or carry on. In short, 200 promise to start. It's not a promise to finish. Right? The second answer is dipper which basically means not yet. The server

[24:07](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1447s) sends back 503 with retry header. The header tells the client how many seconds to wait. The policy picks that number from the engine. For example, how long until the running batch finishes and freeze the enough cash and you differ when capacity is coming back soon? It's a burst, not so not a trend, right? And for example, like if you think about it like Q age is rising but the system isn't saturated.

[24:39](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1479s) If the capacity isn't coming back anytime soon, a dipper just kicks kicks the can down the road, right? And in that case, we can just reject it with the honest answer. Moving on to the next slide. On the agent side, handling a defer is simple. Sleep for retry after time and a little random jitter, then retry again. The jitter just means a small random extra delay. So client don't like don't call

[25:11](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1511s) or like don't at all come back at the exact same moment. They will have to wait. Look what the server sees from 10 retries without retry after every agent picks its own delay. And that's usually that's usually zero. So they all come back at once. That's how 40 calls turns into 80. With retry after and jitter the retry

[25:41](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1541s) spreads out across the window serves asked for. Okay. So if if we see the uh reject reject returns 429 or 529 the third answer is no. Uh and there there are two different codes for it because there are two different reasons. A 429s means too many requests. This particular client or agent session

[26:13](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1573s) is using more than its share. The policy saw something like per client load, the number of concurrent calls or a kota. The problem is the caller and then the 529 means the provider is overloaded. Enthropic uses this code. Every replica is sold. So nobody is getting in right now. The problem is pool not the caller. Now uh handling a reject. So how should

[26:44](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1604s) agent react on 429? Reduce your own load. Cap how many calls that agent has in flight at once. And on 529 retrying harder only makes this worse. Waiting longer switching to different model provider or park the task for later. and one either and on either one keep a retry budget. Use expansion exponential back off with jitter which means waiting longer after

[27:15](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1635s) each failed try and after few tries tell the user what's going on because a reject that gets retrieded at full speed is how you end up in one of the postmodm from the talk at we described at the starting. Now over to you Hershel three. Thank you P. Uh so this is the module three where we will try to learn about

[27:46](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1666s) the different strategies uh that have been rolled out for the admission control. So far we have seen that no layer in the today's stack asks where uh whether there is a room and that layer is ours to add and now we give it a brain. So we will look at why counting requests isn't enough. Breaking a policy down into four different choices. See what four different research paper chose and finish with a decision tree that you can use onto your own ecosystem.

[28:20](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1700s) So let's start with what most team already have which is counting. Yes. Counting the number of the requests. A simple idea is to rate limit at the gateway which gives API key a fixed allowance set in advance. It's great for keeping the clients fair, keeping your tenants fair with each other, but it does nothing to protect your GPUs because it doesn't change with the load

[28:50](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1730s) that is happening onto your GPUs or your cluster. A fixed cap at the proxy gets closer. It counts how many requests are in flight on each replica. The problem is that the quick crep and a long planning to call count exactly the same while the real capacity of the GPU changes with every batch. So in practice it mostly cues and clients timeout ends up doing the

[29:20](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1760s) refusing. Neither one knows whether our 40 calls are cheap or expensive. The cost of air policy does though and it estimates each request will actually cost what each request will cost in the KV memory and the tokens using the live state from your engine. And it says no before the request actually takes up the memory. So the short version is count is

[29:50](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1790s) not a cost. How do you build your own policy? So there are four choices here. The first is the unit which tells you what you are actually admitting. Are you admitting a single request? Are you admitting an agent session or are you admitting a tenant? The two second is the signal which means what is that the policy is

[30:20](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1820s) watching for taking an admission decision. This could be as simple as your memory pressure which is your KB pressure. It could be your Q depth. It could be your deadline slack. That means whether your request is able to meet your SLOs's or not. And whatever it is, it has to actually move when the system gets busy. So three is the rule which means how does the signal gets turned into a decision.

[30:50](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1850s) So rule is used for that and that can be anything from a simple threshold that takes microscond to a full optimizer that takes seconds. Fourth is the action. Once you have the rule that gives you a decision what do you do with it? What does your how does your client gets impacted through those actions? That's the admit defer and the reject that per just talked about in the module

[31:20](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1880s) two. Each choice limits the next one. For example, a deadline signal only works if your request actually carry the deadlines. So let's go through the first three. Choice one. Do you admit a single request or do you admit a poll sessions? Say you have two agent task 20 calls each room for almost half of them.

[31:50](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1910s) You can uh point you can see the top row. So if you admit per request about half of each task gets in but neither task can finish because each one is stuck waiting on the calls that didn't make it. You have used all the capacity and completed nothing. If you admit per session, session A gets all of its call and finishes. Session B gets one clear answer. Come back later. And this

[32:20](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1940s) picture is illustrative, but the logic holds. Our 40 calls are one session. Coding agents send sessions and yet most published policies admit only the single requests. So which metric do you watch for what particular problem? This is the question that we are trying to answer. It depends on the problem that you are

[32:51](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=1971s) trying to prevent. If you are if you want to keep the cash from overflowing, you definitely have to watch your KV pressure. If you want to avoid your wasted recomputee, you have to watch out the KV used together with the cash hit rate. A full cache is fine if it's being reused. If you want to keep your weights to be shorter, you have to watch for your queue depth and you have to take actions

[33:22](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2002s) based on that. If you want to meet your latency targets, you need to watch your deadline slack. Take actions based on that. If you need to plan for your long answers, you need to predict for the output length. And look at the last column fails when it tells you when each signal stops working. Look at the first row. KV pressure fails when the cache never fills up.

[33:52](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2032s) Remember that row? It comes back to bite someone in the part four. So what are the four ways to take that decision? That is how do you convert your signal into a decision from the cheapest to the most expensive. Here are the ways a threshold just compares one number to the one limit. Example is a policy named

[34:23](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2063s) clued weight that was uh created somewhere in 2026. It takes tens of microsconds per decision. Second is a dual gate which needs two signals to agree before it acts. Example is a paper called concour uh which checks like KVUs and the cash hits under 100 microsconds. Third is an optimizer which solves like one big planning problem across all the

[34:54](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2094s) cues at once. Example is a QLM. It's thorough but it takes about 5 seconds per decision. And the fourth is the formal bound uh which does the math on the worst case. Can this request still meets its deadline? The example is the Kronos on which uses the like time to first token and it uh provides you like a microcond level latency. And now hold that cost column up against

[35:26](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2126s) our agent. It sends 40 calls in 2 seconds. A 5-second decision shows up after every party is over. So what the four papers did as the complete policy fluid weight admits single request uses the threshold on your KV use and reports 10 to 25% improvement. Conqueror is the one that admits your VO agents. It uses your dual

[35:56](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2156s) gate and reports four to 4x uh the throughput of the SG lang but it was tested offline. Uh QLM admits the request plans across the W feed and reports 40 to 90% gains at about 5 seconds per decision. Kronos admits requests against their deadline slack with a formal bound and takes deadline misses from 99% down to zero. Definitely very amazing accomplishments.

[36:29](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2189s) So each purper used a different model engine and a workload. So please don't read this as a leaderboard. The question that matters for this room is does any of them fit a coding agent and the answer is no. We placed every paper on the two axises. One axis is what it optimizes deadlines or the throughputs. Other is what it admits single request or the VO agent sessions.

[37:01](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2221s) A coding agent needs a policy that admits bold sessions, works online with live traffic and runs engine you haven't fought and nothing sits there cleanly. Conc doesn't need a for but it was only tested offline. So in practice you will pick the closest match and build just build your own. And here is how you can choose which polic like which kind of a policy you want to try it out.

[37:31](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2251s) So here is that decision tree. First the question that you have to answer is does your request carry any deadlines? If yes, set up a some sort of a formal bound on that deadline. This will take some microsconds level of latency. If there is no deadline requirement, the second question that you can ask is does the KV cache fill at the peak load? If your KV cache fills at the peak load,

[38:05](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2285s) then you would want something like a way to detect the cache prefixes used. So you can use some sort of a dual gate mechanism or a KV threshold mechanism. Um and then if your KV cache gets filled at the peak load, it does not gets filled at the peak load, then you what you could do is you can set up a Q level of threshold on it.

[38:35](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2315s) And that gets us to the benchmarking like once you have a policy, how do you benchmark? So I will be handing it over to pop. Thank you. So now moving on to part four which is benchmarking. As we just saw no publish policy fit a coding agent cleanly. So you are going to adopt one or you you will have to build your own

[39:05](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2345s) and then you have to prove if it's actually working or not. So to now moving on to the next slide you would have to test your policies right so for that you need four things first is your cluster your policy and trace and score. So let's dig deeper into each. So your cluster of the first measure it it is capacity with no admission control at all. The load your

[39:35](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2375s) replica can sustain on their own. Every load level at after this is described as multiple of your number like multiple of that number and uh about the policy u which signals it reads what limit it uses and what it does when it says no. The third one is trace which is a record of real traffic that you replay using code coding agent traffic ramping from half your capacity up to twice your

[40:08](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2408s) capacity. Four is a score. Then they run the same trace twice. Once with the policy and once without and then you can compare your result. The score is where the most people go wrong. So let's look look at that. Now moving on to the next slide which is uh how how you score. The score we recommend is called goodput under admission. So you can see the formula on

[40:38](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2438s) the screen. The top of the fraction is the request that met their SLO their latency target. That means the answer started on time and it never stalled for too long between tokens. The bottom of the fraction is every request that arrived including the one which got rejected. Why does the bottom matter so much? So try this. Uh refuse 95% of your

[41:09](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2469s) traffic and serve the remaining 5% perfectly. If you only count what you admitted, your SLO attainment is 100%. Looks amazing, right? Just ship it. But no like good put under admission says 5%. Shedding looks three when you only account the request you kept. It isn't. So moving on to slide 42.

[41:39](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2499s) The second thing to get right is the workload. A benchmark only tell you something if it looks like your real traffic. So replay agent traces with their fan out retries session not uniform random arrival. Describe load as multiple of the capacity you measured and sweep from half of it to double it. Set your guideline as multiple of your

[42:11](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2531s) latency with no load. And remember a benchmark that never goes past capacity never actually tests the policy because the policy never has to say no. So you have to make sure that you reach at that point. Now move moving on to the seven uh seven things every admission result should disclose. Signal liess is one of the seven things every admission result should disclose.

[42:42](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2562s) Here is the full full list that you can see on your screen. The load as a multiple of measured capacity deadline sets relative to latency with no load. Signal liveless which is no paper report. How many times you repeated the run and how much the result varied not one lucky run. Where each parameters comes from, turned on this setup, borrowed from

[43:12](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2592s) somewhere else or left at the default. Whether the rejected request count in a good put denominator and the full configuration and the full configuration is model, engine, version, hardware, workload, SLOs's and baseline. None of this ask anyone to change how they evaluate. It just ask them to say what they did. Use it as a checklist when you read on on a

[43:44](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2624s) paper and when your benchmark and when you benchmark your own policy. Doing all seven by hand is painful. So we built a tool that records all of this uh as as a default. So uh the tool is admin perf and it's it it's two things in one repository. So in production if you see it's a library you put in front of VLLM or SG lang it

[44:16](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2656s) decides admit defer or reject for every request that's ingress layer from part two. So if you also see we on the right side uh it's uh in in a benchmark it's a harness that runs any policy against a real engine on a real GPU and reports what the policy cost both sides calls the same function policy decide. So the policy you

[44:49](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2689s) benchmark is exactly the policy you deploy. We build it because across those 16 paper no two share the same baseline engine workload or SLO admitf makes a head-to-head comparison possible. Now moving on to the next slide. So using its pive command. So you can see on the screen we have five commands. So infra up starts a real VLM on a real

[45:22](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2722s) GPU. Infra smoke checks that it's actually serving. Then we have bench runs every policy several times each. Then we have bench computer tell you which policy won and how by how much. And then we have infraown which which basically means it should shuts all all off so you stop paying. And that's my favorite one. Uh and so now provisioning and benchmarking are separate commands on

[45:52](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2752s) purpose. Loading a model takes minutes and every policy has to face exactly same deployment. If you are reprovisioned between policy, you would change the very thing you are trying to hold a constant. The deployment is constant. The policy is variable. So now uh here a policy must declare the signal it reads. This is how admit perf

[46:22](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2782s) deals with the trap I just showed you. Every policy has to declare the signal it needs. This KV cache threshold policy says I require KV used correction which is the share of the KV cache in use. If the engine cannot report that signal, the run stops at the startup with an error. You can actually read without the check a missing signal reads as a zero and KV cache threshold that always sees

[46:54](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2814s) zero admits everything. It's quietly turned into the no admit baseline while your results looks completely normal. So policy that cannot see its signal should fail loudly and not just fail silently. Um so here what we did is every decision is recorded with the state it saw. Every run leaves behind a folder you can open

[47:25](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2845s) inspect. There would be four files as you can see on the screen. Those are manifest JSON summary JSON decision JSON and uh out outcome JSON. So what each does is uh you can take a look deeply once you run the results. Now we we will be looking at the shading cut. So shade shading 37% cut tail latency. So here

[47:55](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2875s) are the four results how they will look like on a real GPU. The setup small model we used quen 2.5 uh and it's a half billion model on a A10 GPU. The engine was kept out at four sequ sequences at a time. Eight request at 14 per second two repeats. If you look at the first row with no admission control, the P95 time to first

[48:27](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2907s) token was about two two and two and a half around 2 and a half seconds and P 45 sorry P95 means 95% of the requests were faster than that and it swung by about 700 milliseconds either way. Now the last row if you see with a queue up policy that allows at most two request waiting 60 63% of requests were admitted and the P95 dropped to about

[48:58](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2938s) around 1 second that's 2.5 times better with the exact the good same put now if we look at the signal matter more than the threshold but this This is the result I love most. Same run. KV cache usage peaked at half a percent. The queue got 24 requests deep on a small model. KV cache is huge compared to the four short sequences. So

[49:28](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2968s) it never comes close to filling. All of the pressure showed up in the queue. Instead, a KV cache pressure policy would have botched a flat line and admitted everything. that that's the row of choice from two. So now here and you you can try it today. You don't need a GPU. There is a small fake engine that speaks the three endpoints admit puff uses and it gets

[49:58](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=2998s) busy under load just like a real one. So you can test the whole setup on your laptop. If your right policy is your own package, admit perf discovers it automatically. No change to the repo and contribute contributions are very welcome. New policies, workload, engine adapter or matrices. Okay.

[50:29](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=3029s) So if you want to remember like one slide just make it this one that when you are accepting the request in your inference clusters you need to have a mechanism to say no early something that works at the ingress something before saying yes to the request before that request goes into the GPU before that request takes up your memory.

[51:00](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=3060s) and per added clearly. There are a couple of error codes that your admission policies return. You need to handle those requests and those errors. And with that we would like to come to the closure. We would like to thank you all for your patience, for your time. And here are like two of our projects. It all started as part of the LLM

[51:30](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=3090s) inference at scale handbook. We and when we were doing the survey, we found the gaps and we prepared admit puff. So here is the source code for it. Feel free to go to it and like experiment with it. Raise the issues, contribute to it. idea is to build your admission policies, benchmark them and be confident that it uh helps you keep your cluster stable. Yeah.

[52:01](https://www.youtube.com/watch?v=ntVpbyDTYaQ&t=3121s) Thank you everyone. Thank you everyone.
