---
title: Uncle Bob 用約束取代讀 AI 產碼
description: Robert C. Martin 宣告不讀 agent 寫的程式碼、改用大量測試與度量閘門包圍 agent 的推文串，含一個月前自我打折的前串
created: 2026-08-09
updated: 2026-08-09
source: https://x.com/unclebobmartin/status/2080257779395154409
published: 2026-07-23
tags:
  - coding-agent
  - ai-agent
  - testing
  - clean-code
---

擷取自 X（Twitter），2026-08-09 以 defuddle 取得。含主串與同一作者一個月前的相關前串。

## 主串（2026-07-23，5M views）

**@ori_pomerantz（提問者）：**

> I am trying to use Claude to help me write something, but I just don't feel comfortable letting it edit my files. Does anybody else feel the same? If I am responsible for code, I NEED to understand it, psychologically if for no other reason.
>
> Started programming in 1983. Old?

**@unclebobmartin（Robert C. Martin）回覆：**

> I'm significantly older than you. I started coding in the late 60s. My current strategy is to not read any of the code written by my agents. That's the only way I can take advantage of their productivity. What I do instead is to surround the agents with extreme constraints. Unit tests, gherkin tests, QA procedures, quality metrics, mutation testing, test coverage, and a plethora of others. In the end, I have very high confidence in the code they produce because they've had to run the gauntlet of all of my constraints and tests.

### 串內回應

**@rfleury：**

> Oh, okay. What did you build with this setup?

**@repojournal（2026-07-23）：**

> If we cannot trust the outcome of what AI makes and AI has proven over and over again that it will not listen to us at all times what gives us the confidence that it will stay within the guardrails of our constraints just because we asked it to?

**@GeoffreyHuntley（2026-07-24）：**

> 🎯 we need to engineer the constraint's.

## 前串（2026-07-02，22.6K views）

同一作者，[status/2072736888478175413](https://x.com/unclebobmartin/status/2072736888478175413)：

> I've been pushing very hard on overloading with tests. Gherkin test unit test QA test mutation test gherkin mutation test. It's easy to make the AI's do these things. But just because we can do them doesn't mean we actually should.
>
> Lots of times I just use unit tests and crap evaluation. That seems to work pretty well. For larger projects I can imagine that gherkin testing is pretty useful and so is QA testing. I'm checking that now.

### 串內回應

**@karlprosser：**

> I think the Gerkin in the ends becomes the living spec, while the code either proves that spec to honest or not, while your prompt history is the journey to both. I like to have 2 laveea of gherkin once that really captures the functional scenario and another that fleshes it out

**@it_is_Randy：**

> +1 on the larger projects. If its a new project easier to do mutation testing and low crap score. On larger projects I try and just stick to gherkin testing and now trying to get e2e testing with playwright going. Do you have a repo that has agents architected to achieve your Clean Code standards that I can leverage?
