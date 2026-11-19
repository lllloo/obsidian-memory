---
title: Stop Shipping LLM Settings That Only Win on Paper — Rohan Pandey & Balaji Varadarajan
description: AI Engineer CODE 2026 線上場官方閱讀版，DigitalOcean 示範用貝氏最佳化迴圈替模型 serving 設定找最佳 recipe，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-rohan-optimization
published: 2026-11-12
tags:
  - clippings
  - ai-agent
  - evaluation
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 serving 框架名被辨識成 VLM／BLM／VLN，DeepSeek 被辨識成 DeepSeq）。逐字稿對應 Day 2 直播 `https://www.youtube.com/watch?v=y9JtCCZP2MQ`（YouTube 影片 ID `y9JtCCZP2MQ`，本場 2:13:37–2:19:04）。演講日依大會議程頁為 2026-11-12（線上場）；議程頁講者列只列 Rohan Pandey，逐字稿中也只有他發言。

Day 2 livestream · [2:13:37–2:19:04 on YouTube](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8017s). The player starts and stops at this session’s boundaries.

## Introduction

**Rohan Pandey** demonstrates an optimization loop that tests serving configurations and returns both a report and a deployable recipe.

A model's downloaded weights do not tell an operator which serving configuration will work best for a particular machine and workload. Manually trying parameter combinations takes time, and the result can depend on whether the traffic consists of short chats, long conversations, retrieval-heavy requests, or batch classification.

Pandey's short demo starts from that practical task. He wants an optimization agent to search for a better recipe in the background, leaving the operator with a configuration they can inspect and deploy rather than a recommendation expressed only in prose.

[2:14:07 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8047s)

## Let measurements choose the next trial

At [02:14:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8047s), Pandey describes the search strategy as Bayesian optimization. Instead of exhaustively trying every combination, the loop uses the results of earlier trials to guide what to try next. [Optuna](https://optuna.org/) supplies the optimization machinery in the demonstration.

The loop starts with a recipe, tests it, assigns a score, proposes another configuration, and repeats until its trial budget is exhausted. That makes the objective important. An optimizer can search efficiently while still improving the wrong quantity if the score does not represent the intended service.

Pandey's workload includes four traffic regimes: short chat, long chat, retrieval-augmented generation, and batch classification. Each has its own input and output lengths. The mix is configurable, so the best result is conditional on the chosen traffic and hardware rather than a universal setting for the model.

[2:16:26 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8186s)

## Make the experiment reproducible

The demo runs on a machine with **GPT-OSS 120B** already available. At [02:16:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8186s), Pandey walks through a command that selects the weights, activates an environment, and runs a tuner script.

The important inputs are the study name, starting YAML configuration, hardware specification, and number of trials. Together they identify the experiment and constrain the search. The displayed command is an example of launching a study; the report he later opens comes from a completed run with its own trial count.

That distinction prevents a misleading reading of the demo as an instantaneous optimization. Pandey says these studies take hours. The automation removes repeated manual tuning work; it does not make serving benchmarks free.

[2:17:55 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8275s)

## Return the evidence with the configuration

[![The configuration optimizer report shows a selected trial, an improvement figure, and the resulting serving configuration.](https://ai.engineer/reading/code-2026/images/online-rohan-optimization-8275.jpg)](https://ai.engineer/reading/code-2026/images/online-rohan-optimization-8275.jpg)

*The [report at 2:17:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8275s) displays a 17.5% improvement for this study and a selected configuration. The result belongs to this workload and test setup; it is not an accuracy improvement in the language model.*

The completed run produces two artifacts. The YAML file contains the selected serving parameters. The HTML report shows how trials performed and which configuration won. Keeping both lets an operator distinguish the deployable result from the measurements that justify choosing it.

Pandey describes the objective in terms of goodput: useful generated-token performance under the workload's service constraints. He also opens a second experiment on a **DeepSeek R1 distilled model**, reporting higher throughput and lower inter-token latency than its starting configuration. The recording does not establish that those gains transfer to a different deployment.

The useful outcome is the workflow itself. Define the traffic you care about, choose a scoring objective, let the optimizer run bounded experiments, and retain the winning recipe alongside the trial history. An agent can make the tuning process less laborious while leaving the evidence visible to the person responsible for deploying it.

Full transcript 69 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[2:13:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8017s) All right. Hello, everyone. So my name is Rohan, and this is a quick demo on the optimization

[2:13:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8023s) agent that has been recently built. So a quick intro into what the purpose is and what the

[2:13:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8030s) goal is of this agent, and then I'll get into a brief demo and results from a previous

[2:13:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8035s) run that we just did. So what the goal is here is to build an agent that helps find

[2:14:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8043s) the best VLM serving config for any given model.

[2:14:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8047s) The purpose is to reduce the time it takes

[2:14:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8050s) to manually find the best configs

[2:14:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8054s) and the VLM serving recipe.

[2:14:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8056s) And if we can automate this

[2:14:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8057s) and have it run in the background

[2:14:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8059s) and have the agent find the recipes

[2:14:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8062s) and the optimized parameters faster,

[2:14:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8064s) then it will save a lot of time.

[2:14:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8066s) So that's the goal of the agent

[2:14:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8068s) and a little bit more into how the agent actually does this.

[2:14:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8071s) So the strategy that the agent uses is called Bayesian optimization.

[2:14:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8076s) And Bayesian optimization is a technique that's used to find the most optimal numbers in any given situation.

[2:14:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8085s) So in our situation, it's to find the optimal numbers in this VLN recipe.

[2:14:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8090s) It uses mathematical steps that essentially minimizes the search space.

[2:14:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8095s) So by minimizing the search space, it reduces a lot of the time that it takes in finding the optimized numbers in this recipe during the run.

[2:15:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8105s) So Bayesian optimization is a strategy that is used, but Optuna is the tool that uses a strategy in the search loop.

[2:15:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8114s) So Optuna uses Bayesian optimization.

[2:15:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8116s) It feeds it the current recipe, the starting recipe.

[2:15:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8120s) Vision Optimization runs on that, and over many iterations or many trials, it eventually

[2:15:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8126s) finds the optimized recipe.

[2:15:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8128s) And Optuna basically takes each recipe after every trial, assesses it, gets a score, uses

[2:15:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8134s) the strategy to change the recipe, improve it, and then it reruns it within the search

[2:15:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8139s) loop until the trials is done.

[2:15:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8141s) So let's go a little bit into how we do this.

[2:15:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8145s) So I'm currently in a droplet here, and this droplet, for example, has GPT OSS 120b model loaded up.

[2:15:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8154s) So what we can do is we can look at the current recipe.

[2:16:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8162s) So what we see here is four regimes, right, that we're testing it on.

[2:16:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8165s) So there's chat short, there's chat long, there's rag and batch classify.

[2:16:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8170s) They have their own set of ISL OSL tokens that we're feeding it through.

[2:16:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8173s) All these can be changed depending on what we want to see.

[2:16:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8178s) But essentially this is the starting config, starting recipe that you would get when you download the weights of the model.

[2:16:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8186s) So moving on, once you have the model downloaded in your droplet and you're ready to run this agent,

[2:16:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8193s) you paste in this command, which essentially tells you where the weights are coming from,

[2:16:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8199s) to activate a virtual environment and have, or not have, but run the script called tuner.py.

[2:16:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8208s) This script essentially tells you, or it has a couple of things you have to tell it.

[2:16:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8211s) So you want to give it the name of the study.

[2:16:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8214s) You want to tell it the starting YAML file, which we just saw above here.

[2:17:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8220s) You want to tell it the hardware that it's running on.

[2:17:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8222s) And you want to tell it the number of trials that you want.

[2:17:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8225s) So in this example, we have 24.

[2:17:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8228s) Briefly, I'll show you another example of a past run that was run that had only nine

[2:17:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8233s) trials.

[2:17:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8234s) So anyway, this is the command that's run.

[2:17:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8240s) Typically these commands take a couple hours to run.

[2:17:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8245s) I think for the GPT-O, it says it took about four or five hours.

[2:17:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8248s) And then for the other model, it took a couple hours as well.

[2:17:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8252s) So we can go into the HTML report that's generated after the agent finishes its work.

[2:17:41](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8261s) So this one is for the GPT-OSS model that I mentioned.

[2:17:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8264s) What we see in the HTML report is which trial number was the best trial out of the total of how many trials.

[2:17:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8270s) So in this case, it was 50 trials.

[2:17:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8272s) So at the end of the run, you get an optimized YAML file, which includes all the numbers that we currently look for in the BLM serving recipe.

[2:18:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8281s) So in this case, we found, or the agent found that 256 was the optimized number, so on and so forth.

[2:18:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8287s) And the way that it's getting the accuracy is the amount of good put tokens that's being generated.

[2:18:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8292s) So overall, we found that from the first config, we had an improvement of 17.5% in terms of tokens generated.

[2:18:21](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8301s) And this one, as I mentioned, is for GPT-OSS.

[2:18:24](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8304s) We have another HTML report here, which is for the DeepSeq R1 distill model.

[2:18:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8309s) In here we found that, or in here we had nine trials that was run, and out of the nine,

[2:18:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8316s) the ninth one was the best.

[2:18:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8317s) We found that token throughput doubled, and ITL was improved by almost half, aka it was

[2:18:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8323s) reduced by almost half.

[2:18:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8325s) So this is a quick intro and brief demo on the commands you run and what the output looks

[2:18:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8331s) like.

[2:18:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8331s) In general, you get an HTML report that tells you how each trial went, and then you also

[2:18:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=8337s) get a YAML file that has the optimized recipe at the end of the day. So hopefully that was helpful.
