---
title: Your Agent Hates Your CLI — Ayush Bhardwaj
description: AI Engineer CODE 2026 官方閱讀版，Bhardwaj 談把 agent 的 pipe 繞路當成 CLI 的 bug report，附機器逐字稿
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-ayush-cli
published: 2026-11-12
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 AI Engineer 官方閱讀頁，正文後附官方機器逐字稿（原註明含辨識錯誤，如 Claude Code 被辨識成 CloudCode／cloud code、grep 被辨識成 grab／Crap、sed 被辨識成 Sad／set、Sanity 的 `give_feedback` 被辨識成「GIF feedback」、DuckDB 被辨識成 DougDB）。逐字稿對應 Day 2 直播 `https://www.youtube.com/watch?v=y9JtCCZP2MQ`（YouTube 影片 ID `y9JtCCZP2MQ`，本場位於 1:46:46–1:59:04）；`published` 取該直播的 release date。

Day 2 livestream · [1:46:46–1:59:04 on YouTube](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6406s). The player starts and stops at this session’s boundaries.

## Introduction

**Ayush Bhardwaj** treats the shell commands around a tool invocation as usability feedback from an agent that rarely files a bug report.

One agent downloads a documentation page and keeps forty lines. Another parses a dependency report and keeps the tail because that is where the totals happen to live. A third runs a test suite and truncates the output. Each gets an answer by writing a small program around the program it was asked to use.

Bhardwaj's observation is that these workarounds conceal product friction. A pipe can be a perfectly sensible one-off choice. The same cut-down command appearing repeatedly suggests that the underlying tool is missing a useful way to request the information.

[1:48:27 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6507s)

## A successful pipeline can hide a failed command

At [01:48:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6507s), Bhardwaj describes an audit of his own agent calls across common CLIs. Output filtering was frequent, particularly for read-heavy commands. He treats the sample as evidence about the tools and workflows he uses, rather than a census of all agent behavior.

Some filters create a correctness problem. Without `pipefail`, a Bash pipeline normally reports the status of its last command. Piping a failing test command into a successful output filter can therefore leave a success status attached to a failed operation. If the remaining text still contains the error, the agent may notice. If the filter also removes it, both the status and the visible output can mislead it.

This motivates a small interface improvement: make failures hard to miss. Put a concise error summary at the end of the output, preserve the failure status, and point to a full log. An agent that reaches for `tail` should not accidentally erase the only evidence that the operation failed.

[1:50:43 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6643s)

## Read the command after your command

Bhardwaj built a tool for searching previous coding-agent sessions. His users were agents trying to recover context from earlier work. Opening a long session could return an enormous body of text when the useful result was only a few messages around a match.

At [01:50:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6643s), he addresses the obvious objection: agents already know how to use `grep`, `head`, and `tail`. Why interfere?

The issue is repeated guessing. A size cap limits volume but does not identify relevance. A positional assumption can break when the output changes. A selection flag lets the caller state the thing it wants, and lets the tool implement that request consistently.

[![The source slide translates filtering pipelines into selection flags and compact search output.](https://ai.engineer/reading/code-2026/images/online-ayush-cli-6740.jpg)](https://ai.engineer/reading/code-2026/images/online-ayush-cli-6740.jpg)

*At [01:52:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6740s), the left side is the agent's workaround; the right side moves the requested behavior into the CLI. The tool can return messages around a match instead of forcing the caller to infer line positions.*

He identifies three recurring requests:

- **Select the useful region.** Filtering session text suggests a need for messages around a match, matching messages only, or a bounded tail.
- **Return fewer fields.** A Python program that reduces a JSON result may be asking for a compact output mode rather than a richer parser.
- **Batch repeated reads.** A loop inspecting many sessions is a candidate for one command that accepts several session IDs.

The surrounding commands become a product roadmap. They show not only which operation users invoked, but what they had to do to make its result usable.

[1:53:32 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6812s)

## Documentation is part of the executable interface

A new flag cannot help if the agent never chooses it. At [01:53:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6812s), Bhardwaj describes leaving an obsolete flag in a skill after the flag had become a no-op. Agents continued using it. When sessions loaded a rewritten skill, their behavior changed.

Help text, skill instructions, and errors teach agents how the interface works. Stale guidance therefore produces recurring bad calls, even if the implementation itself is correct. Adding an efficient command and updating the instructions that point to it are one product change.

Defaults matter too. Large outputs can begin with a bounded result and explain how to retrieve the next page or request the full data. An agent-specific mode may remove terminal decoration, provide structured errors, and make truncation explicit. The design goal is to let the caller know both what it received and what it did not receive.

[1:54:09 ↗](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6849s)

## Turn transcripts into a test set

At [01:54:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6849s), Bhardwaj proposes replaying real calls through the old and new tool. The next action in the original session supplies a rough indication of what the agent wanted.

A ranking change should preserve the result the agent subsequently used. A format change should not omit necessary information. A new default should be checked against commands whose meaning it changes. Calls immediately repeated with different arguments can reveal where the first attempt failed.

That inferred answer key is imperfect, so he recommends holding back cases to evaluate the fix. Otherwise it is easy to optimize the tool for the examples that suggested the change and mistake that for a general improvement.

He also distinguishes smaller output from better task performance. A compact representation can save visible characters while barely changing total model consumption. If the agent already answered correctly, the reduced output may not move cost or runtime. The important measurements are useful answers and the turns needed to reach them, not an isolated token reduction.

Bhardwaj ends by assigning different jobs to the human and agent. The human decides what the interface should make easy. The agent can help inspect traces, replay cases, and test a proposed repair. Begin with the evidence already available: preserve the session history, find the workarounds, and read them as requests that nobody put into the issue tracker.

Full transcript 156 timestamped passages

Machine-generated source transcript; recognition errors remain. Timestamps and subtitles use the selected source recording’s clock, not clip-relative time. Section links use cited source moments; sections without a verified moment return to the talk start.

[1:46:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6406s) Hi, I am Ayush.

[1:46:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6407s) I built a CLI that lets your agent reuse context from your past session across tools.

[1:46:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6412s) While improving it, I realized why my agent secretly hated my CLI and what you can do about yours.

[1:47:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6421s) CloudCode wanted one setting from a docs page, so it downloaded the whole page,

[1:47:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6426s) grabbed it, and kept the result at 40 lines. Codex wanted to know how many dependencies

[1:47:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6432s) were vulnerable. It asked the whole JSON report and kept the last 40 lines

[1:47:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6437s) where this report puts the totals.

[1:47:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6440s) Cursor ran a test suite, found one failure, and kept the last 80 lines.

[1:47:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6445s) All three cuts kept the information shown here, each one encoded in an assumption about

[1:47:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6450s) where the answer sits in the output.

[1:47:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6452s) That can hide friction from the people who build these tools.

[1:47:35](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6455s) One pipe tells you very little, the same pipe written again and again can point to something

[1:47:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6460s) your tool is missing.

[1:47:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6462s) These are real calls from my own transcripts and the cloud code one was the agent reviewing

[1:47:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6466s) this talk and it still couldn't help itself. Agents can work around friction without filing

[1:47:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6473s) a bug report. They write a little program around your program. In June, Sanity, the

[1:48:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6480s) content platform, wrote up their MCP server. More than 20,000 agents, about 3 million tool

[1:48:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6486s) calls since launch, and not a single bug report. So they shipped a GIF feedback tool. Once

[1:48:11](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6491s) the agent had somewhere to complain, they started expressing what's wrong. But you

[1:48:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6495s) You don't need a feedback tool to start.

[1:48:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6498s) Feedback is already sitting somewhere in your transcripts.

[1:48:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6503s) I extracted about 20,000 agent calls from my same transcripts.

[1:48:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6507s) 14 CLIs appear in that sample, git, github-cli, cargo, curl, npm-docker, and others.

[1:48:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6513s) A quarter fed output into filters such as head, grab, tail, python, sort, or wc.

[1:48:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6519s) For read-heavy commands, it's more than half.

[1:48:42](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6522s) Git show and cargo test 62% each.

[1:48:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6524s) Some harnesses pipe far less, codex for example, lets the agent set an output limit on each call.

[1:48:53](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6533s) And pipes don't only cut noise. In bash, without pipe fail, a pipeline returns the exit code of its last command.

[1:49:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6541s) So let's say you pipe cargo test into head. It can report success even when the test failed.

[1:49:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6547s) Here's one example on the screen, a compile error and a green dot.

[1:49:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6553s) The status was wrong, but the agent could still read the error.

[1:49:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6558s) A pipe can also cut the error itself, which is worse.

[1:49:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6562s) In a cloud code issue on GitHub, a user reported it a script through a reference error and

[1:49:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6567s) exited with an error code.

[1:49:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6568s) Tails showed three harmless lines and Cloud reported success.

[1:49:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6572s) The error never reached the model.

[1:49:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6574s) So my advice would be to fail loudly.

[1:49:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6577s) when a tool fails, make the very last lines a short summary and a part to the full log.

[1:49:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6585s) I learned all this while tinkering with the CLI I built. It's a small tool that lets coding agents

[1:49:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6591s) search their own past sessions across cloud code, codex cursor. It shifts with a skill so the agent

[1:49:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6597s) can decide when and how to call it.

[1:50:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6600s) Agents are the users that I'm studying. My October audit recorded about 1,000 calls and that's my small case study.

[1:50:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6608s) The method works on anything your agent calls. Just look at what they do right after the call.

[1:50:15](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6615s) 80%

[1:50:17](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6617s) 4 out of 5 times an agent opened an old session with my tool. The output went straight into Crap, Sad, Head, Tail or Python.

[1:50:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6625s) I call that the pipe text.

[1:50:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6627s) A pipe keeps junk out of context, and that's fine.

[1:50:30](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6630s) The text is that the agent writing that same cutdown command by hand every single time.

[1:50:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6636s) It's small each time, and it mostly works, but each one is another guess about where the answer is.

[1:50:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6643s) The fair objection comes from a hacker news thread about designing CLS for agent that I was reading.

[1:50:49](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6649s) The command says to leave it to the agents to choose how much output to read.

[1:50:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6654s) agent can pipe through grab or head perfectly well. Well, they can and for one-off they should.

[1:51:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6661s) I'm not against that but across those everyday CLIs I found 83% of pipes fell into the pattern

[1:51:07](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6667s) seen at least 10 times the same CLI subcommand and pipe tools. The arguments past could differ

[1:51:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6673s) but the agent keep asking for the same things. I understand the output they're cutting is

[1:51:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6680s) probably big. I opened one long session with my tool two ways. The whole thing, 1.2 million

[1:51:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6687s) characters and that's why the agent spy. Just the part around the search match was about 3,000

[1:51:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6692s) characters. Harness is do-cap output but a size gap does not identify the relevant messages.

[1:51:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6699s) Selection flags on the other hand let the agent tell your tool which part it wants.

[1:51:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6705s) So based on my experience and improvements I made to my own tool, I'll give you three

[1:51:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6710s) examples.

[1:51:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6711s) Read the left column as the bug reports.

[1:51:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6714s) So starting with the first one, filtering with RG and said means let me pick the part

[1:51:58](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6718s) I want.

[1:51:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6719s) So my read command view can now written just the part around a match, only the matching

[1:52:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6725s) messages or the last few with a size gap.

[1:52:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6729s) Second example would be Python over JSON.

[1:52:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6732s) So Python over JSON means give me fewer fields. So search got a compact mode one line per hit about six times smaller than JSON with the same results.

[1:52:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6743s) Inspect command in chat history summarizes a session.

[1:52:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6746s) About a third of inspect calls came from agent looping over several sessions by hand as you can see with the for loop.

[1:52:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6753s) That means let me ask several about several at once and now it's one call.

[1:52:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6758s) As you can see, my roadmap was in the commands around my command and I had to learn from that.

[1:52:47](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6767s) InfraCost, the CloudCost tool, wrote up the same discovery in May.

[1:52:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6770s) Their agents were writing JQ and Python pipelines over JSON dumps, so they moved the filtering into the CLI and added a compact format and a skill to teach it.

[1:52:59](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6779s) Plain Cloud with none of that got 0 of 6 hard questions right in the testing and with it,

[1:53:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6785s) 6 of 6 and cost across the benchmark also fell 41%.

[1:53:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6789s) On Hacker News, the person who wrote that post said that reading those agent logs felt

[1:53:14](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6794s) like watching usability tests and I couldn't agree more.

[1:53:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6799s) This part might sound trivial and obvious.

[1:53:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6802s) Once it's in the CLI, teach your agent it's there with the skill file or the help flag.

[1:53:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6806s) But agents take their teaching literally. I made some changes that turned my deep flag

[1:53:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6812s) into a no-op. I left the skill telling the agents to use it to see what they do,

[1:53:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6817s) would they find out or not. 95 searches out of 95 still passed it. After that,

[1:53:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6824s) two sessions loaded a rewritten skill and that no longer told them to use it. None of the searches

[1:53:50](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6830s) passed deep flag and both tried new flags on their first read. So your skill.md, your help

[1:53:56](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6836s) text, your error messages are the interface. That also means stale dogs are bugs because

[1:54:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6841s) your agent will keep following them. Once the new flags reach agents, nearly every search used

[1:54:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6849s) compact output and nearly every reduced the new flags. Piped read fell from 82% to about a quarter.

[1:54:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6862s) You can get real levels and test cases for your tool easily.

[1:54:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6865s) If you use it every day, they are already in your transcripts.

[1:54:28](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6868s) The commands agent really ran are the test cases and what agent did immediately next

[1:54:32](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6872s) is a rough answer key.

[1:54:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6874s) Replay those commands through your old build and your new one.

[1:54:37](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6877s) If you change the ranking, check that result the agent went on to use still comes out on

[1:54:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6884s) the top or not.

[1:54:44](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6884s) If you change an output format, check that nothing went missing.

[1:54:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6888s) If you change the default, see which commands now behave differently.

[1:54:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6892s) And when an agent read a call with different arguments, you have probably found a failing

[1:54:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6897s) case.

[1:54:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6897s) The answer key is only a rough guess at what the agent wanted.

[1:55:01](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6901s) Keep a few cases back and use those to score your fix.

[1:55:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6906s) So after analyzing 20,000 invocation, if I were to start all over again, this is what

[1:55:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6912s) I would build first.

[1:55:13](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6913s) 55% of the measured pipelines used only head, tail, or set downstream.

[1:55:19](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6919s) That points to demand for smaller slices.

[1:55:22](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6922s) So ship ranges and limits before anything fancy.

[1:55:25](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6925s) A flag only helps if agents reach for it.

[1:55:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6929s) GitHub CLI's list command have a limit flag.

[1:55:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6931s) An agent used it 81% of the time.

[1:55:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6934s) The counter example would be cargo.

[1:55:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6936s) For cargo test, quiet mode,

[1:55:38](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6938s) prints a character per test instead of a line and still reports failures.

[1:55:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6943s) Agent passed it on about one cargo run in 10 and piped instead.

[1:55:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6948s) So teach the flag in your help test and your skill.

[1:55:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6952s) And make big outputs print less by default and say how to get more.

[1:55:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6957s) For example, end with something like showing 20 of 300, add offset flag 20 for the next wage.

[1:56:05](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6965s) One way to ship several of these at once is an agent mode.

[1:56:09](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6969s) Your CLI notices an agent is calling it and prints differently.

[1:56:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6972s) Agents like Claudecodes set an environment variable in their cells so your tool can spot them.

[1:56:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6978s) DuckDB shipped one. At a terminal you get a nicely drawn table but an agent gets a plain one that says how many rows were left out and how to get them.

[1:56:27](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6987s) A huge query stops early and says so and errors come back as JSON because agents read them better.

[1:56:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6994s) It's the same list as we have been just through and it cut the output model read by 59%.

[1:56:39](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=6999s) However, the tokens saved were nearly 0.5% of all the tokens the model read.

[1:56:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7005s) So cost and runtime didn't improve.

[1:56:48](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7008s) If you remember, InfraCost agents started getting answers right.

[1:56:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7012s) DougDBs were already there.

[1:56:54](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7014s) So measure turns and write answers, not just tokens.

[1:57:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7020s) might be thinking, I'll ask my agent to do all of this.

[1:57:04](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7024s) They are not that good at this yet.

[1:57:06](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7026s) At least not one-shotting it.

[1:57:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7028s) The design is where it goes wrong.

[1:57:10](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7030s) Ask an agent to build a tool for agent.

[1:57:12](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7032s) It probably pictures a person and then bolts the agent on.

[1:57:16](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7036s) It copies most common patterns it has seen, and most of those are poor.

[1:57:20](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7040s) A study of official MCP servers found most just rep an existing API.

[1:57:26](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7046s) Another checked tool descriptions from real MCP servers and flagged issues in 97% of them.

[1:57:33](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7053s) Docs have the same gap.

[1:57:34](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7054s) researchers at each year Zurich tested context files written by agents. They didn't help tasks

[1:57:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7060s) succeed, cost more to run, and did worse than files written by people. Agents are already good

[1:57:46](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7066s) at other half of this talk. Give one transcript and a test it can run, and it can find what's

[1:57:52](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7072s) wrong and improve the tool, sometimes past what people wrote by hand. And Tropic reported that

[1:57:57](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7077s) on its own internal tools as well. So you decide what the tool should be and let the agent check

[1:58:03](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7083s) against what really happened. You've seen the evidence for each of these so I

[1:58:08](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7088s) won't read them. Take a moment to absorb these or screenshot.

[1:58:18](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7098s) To find your own list, backup your transcript first because Cloud Code can

[1:58:23](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7103s) delete inactive once after 30 days. Then search for them for a tool's name

[1:58:29](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7109s) followed by a pipe and other similar patterns.

[1:58:31](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7111s) If you ship an MCP server, look for agent calling your tool again,

[1:58:36](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7116s) straight away with different arguments.

[1:58:40](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7120s) If you remember one thing from this talk,

[1:58:43](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7123s) if you are building a tool for your agent,

[1:58:45](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7125s) your agent transcripts are the product analytics you probably aren't reading.

[1:58:51](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7131s) The workaround is the bug report, so go read your transcripts.

[1:58:55](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7135s) And if you need any help doing that, check out Chat History on Cargo or GitHub.

[1:59:00](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7140s) It can do this for you as well.

[1:59:02](https://www.youtube.com/watch?v=y9JtCCZP2MQ&t=7142s) Thank you.
