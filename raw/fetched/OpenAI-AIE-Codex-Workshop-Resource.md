---
title: OpenAI AIE Codex Workshop Resource
description: OpenAI 為 AI Engineer CODE Summit 2026 Codex 場次製作的配套資源頁，逐項附功能說明、官方文件連結、範例 prompt 與 coordinate skill 全文
created: 2026-11-19
updated: 2026-11-19
source: https://aie-codex-workshop.openai.chatgpt.site/
published:
tags:
  - clippings
  - coding-agent
  - ai-agent
---

> 本檔以 defuddle 取自 OpenAI 官方的 workshop 資源頁（ChatGPT Sites 託管），即 YouTube 影片 `IPh9YsWvDQk`（Kundel & Guo, "New Ways of Working with Codex"）描述中的 Workshop resource 連結；演講字幕見 `raw/fetched/AI-Engineer-Kundel-Guo-New-Ways-of-Working-with-Codex.md`。頁面為廠商自寫的教學材料，內容照貼不改寫；嵌入影片只保留 HTML 標籤。

![Codex Micro keyboard](https://aie-codex-workshop.openai.chatgpt.site/media/codex-micro.webp)

## Enter to win a Codex Micro at the OpenAI booth

We’re raffling off three [Codex Micro](https://developers.openai.com/codex/features/codex-micro) devices on Thursday at 1 p.m. at the OpenAI booth.

You must be present at the booth to win.

Jump to **Introduction**

### Install the desktop app

The ChatGPT desktop app is available for macOS, Windows, and Linux.

#### Workshop tip

You can also use the Codex CLI or web app. We’ll use the desktop app for most of the workshop.

[Download the desktop app](https://chatgpt.com/desktop/)
1. Install and open the ChatGPT desktop app.
2. Sign in with your ChatGPT account or use an OpenAI API key. Some features require a ChatGPT account.
3. Switch to Codex mode. Start a chat, create a project, or open the folder you want Codex to work in.

#### Additional resources

- [Read the Codex quickstart](https://developers.openai.com/codex/quickstart)

### What is Codex?

At its core, Codex is a coding agent built on an open-source agent harness. The harness gives models the tools to read files, edit code, and run commands. The same harness powers [Codex mode in the ChatGPT desktop app](https://developers.openai.com/codex/app), the [Codex CLI](https://developers.openai.com/codex/cli), [Dots](https://developers.openai.com/codex/dots), [ChatGPT Work](https://developers.openai.com/codex/get-started-with-work), [`@ChatGPT` in Slack](https://developers.openai.com/codex/third-party/slack), and the [Agents API](https://developers.openai.com/api/docs/guides/agents-api/overview). If you’re building your own app, you can also use the [App Server protocol](https://developers.openai.com/codex/app-server) to bring the Codex experience into it.

[**Explore Codex on GitHub** openai/codex](https://github.com/openai/codex)

### Repository context

Keep the information needed to contribute to the codebase in the repo itself. Use `AGENTS.md` to point Codex to architecture decisions, coding conventions, and the commands your team uses to build and test. Keep the configuration for linters, formatters, and other checks in the repo so Codex can run the same checks your team uses to enforce those conventions.

#### Additional resources

- [Write an AGENTS.md](https://developers.openai.com/codex/guides/agents-md)

### Plugins

Much of the context for a change lives outside the repo. Connect plugins to pull in decisions from Slack, requirements from Linear or Jira, docs from Notion or Google Docs, related emails, and design mocks from Figma.

A plugin can bundle MCP tools, reusable skills, and supporting resources. Connect services through your ChatGPT account and use those connections across supported desktop, web, mobile, and CLI experiences. Individual capabilities vary by surface.

Install plugins from the marketplace, or share your own through a team marketplace, a GitHub repository, or a marketplace checked into your project. That gives teammates the same tools and workflows alongside the code.

### Plugin extensions

Extensions bring your team’s tools into the interface. Add a sidebar entry, let people find content through @mentions in the desktop composer, or give an app a full-page view on supported surfaces.

A design system plugin could autocomplete component names in the composer or open a gallery where teammates preview and configure components, then send their selection to Codex to implement.

![Plugin extension surfaces highlighted in the sidebar, a chat message, the composer’s @mention field, and the right-hand panel.](https://aie-codex-workshop.openai.chatgpt.site/media/plugin-extensions.png)

#### Additional resources

- [Build plugin extensions](https://developers.openai.com/plugins/build/extensions)
- [See the workshop diagram](https://docs.google.com/presentation/d/1wOjktTTgm6v9D6FFlbW8917pr_NyPi7IBwWN3P-A7Uk/edit#slide=id.h3ad1d494c04d892d_0_1491)

### Appshots

An appshot attaches an image of the active window and any text the app exposes through accessibility. That can include text below the fold, outside the screenshot.

- macOS: Press Left Command + Right Command together.
- Windows: Press Left Alt + Right Alt together.

In Settings, change the shortcut or choose whether appshots go to the current chat, a new chat, or a chat selected automatically.

#### Additional resources

- [Read the Appshots guide](https://developers.openai.com/codex/appshots)

<video controls="" width="1280" height="720" aria-label="Appshots workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/appshots.mp4" type="video/mp4"></video>

Press both Command keys. The active website appears as an attachment above your prompt.

### Computer use

Use Computer Use to gather context from apps without a dedicated plugin or to test an interface directly.

Desktop apps

Install the Computer Use plugin and review app access in **Settings → Computer Use**. On macOS, grant Screen Recording and Accessibility permissions. Codex can run a task in the background while you keep working. On Windows, keep the target app visible on the active desktop.

Chrome

In **Settings → Computer Use**, select Chrome and install the ChatGPT browser extension. On macOS, Windows, and Linux, Codex can use sites you’re already signed in to and work in its own tabs while you keep using yours.

#### Additional resources

- [Set up Computer Use](https://developers.openai.com/codex/computer-use)
- [Set up the browser extension](https://developers.openai.com/codex/chrome-extension)

<video controls="" width="1280" height="720" aria-label="Computer use workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/computer-use.mp4" type="video/mp4"></video>

Turn on Computer Use, add the Computer chip, and send “test this app.” Codex opens Photos in the iOS simulator and reports whether it can open a photo after declining notifications.

### Computer history

Plugins and Computer Use help Codex find what you’re working on. Computer History adds context about how you work across apps. Opt in under Settings → Computer History in the macOS app, then ask Codex to help you pick up something you looked at recently.

With Memory enabled, Codex can use that context to remember preferences, like drafting blog posts in Google Docs. In Settings, review what was recorded, pause collection, clear recent history, or exclude specific apps and websites.

<video controls="" width="1280" height="720" aria-label="Computer history workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/computer-history.mp4" type="video/mp4"></video>

Select Computer History in Settings and turn on the toggle to start recording recent activity.

### ChatGPT Space

Plugins can pull context from across your tools. When teammates, ChatGPT, Codex, and Dots need to work from the same plan, use a shared Page in ChatGPT Space. It gives decisions and feedback a home alongside the plan, while the implementation stays in the repo.

To move a plan from a thread into Space, ask Codex to create a Page.

Try this prompt

Move this plan into a Page.

<video controls="" width="1280" height="720" aria-label="ChatGPT Space workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/plan-to-page.mp4" type="video/mp4"></video>

Send “Turn this plan into a page.” Select Open on the returned Page card to see the editable plan in Space.

#### Ask about a specific passage

Select a paragraph and mention ChatGPT to ask a question about it. Mention a teammate when you want their input on a decision.

<video controls="" width="1280" height="720" aria-label="Mentions on a Page workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/page-mentions.mp4" type="video/mp4"></video>

Highlight the database decision and mention ChatGPT. The question stays attached to the selected paragraph.

#### Automatically update Pages

Add an Instructions block to tell ChatGPT how to update a Page. Think of it like an `AGENTS.md` for the Page. You can specify which sources to check, what to add, and how to format it. To keep the Page up to date automatically, tell ChatGPT when to run the update and turn on the schedule. For example, have it add new feedback from `#alpha-feedback` to your bug tracker every evening.

<video controls="" width="1280" height="720" aria-label="Assistant instructions workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/page-instructions.mp4" type="video/mp4"></video>

Add an Instructions block to the bug tracker Page and tell ChatGPT to pull in the latest feedback every day at 9 p.m.

#### Additional resources

- [Explore ChatGPT Space](https://developers.openai.com/codex/space)

### Ultrafast

Ultrafast can generate tokens up to 8× faster in Codex with GPT-6 Astra or GPT-6.1 Sol. On eligible plans that bill in credits, it uses 6× the model’s Standard credit rate.

Use Ultrafast when you can verify each change quickly, either with a fast check or by reviewing the result yourself. If builds or tests take up most of the time between turns, you may barely notice the speedup.

Set reasoning effort to Low and ask Codex for one small change at a time. For a web app, open a local preview with hot reload so you can inspect each change as it appears and give feedback right away. That keeps you focused on shaping the result while you’re still figuring out what looks or feels right.

#### Additional resources

- [Check Ultrafast availability and usage](https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex)

### Browser annotations

When you want to show Codex exactly what to change, use annotations in the ChatGPT desktop app’s built-in browser. Click the annotation button, select the elements you want to give feedback on, and describe the change. For example, select a heading and ask Codex to align it with the paragraph below.

Click the settings button in the annotation popover to try changes directly on the page. You can preview adjustments like text color, font size, or opacity before sending your feedback.

<video controls="" width="1280" height="720" aria-label="Browser annotations workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/annotations.mp4" type="video/mp4"></video>

Select the Components heading and click Ask ChatGPT. The selection becomes context for your feedback.

By default, the browser selects elements from the page’s DOM. If you maintain the site, use the Browser Annotation API to define selectable regions and add controls that let people preview changes. In a design-system gallery, mark each component preview as one target so feedback identifies the exact variant.

```shell
<section aria-label="Button previews" oai-annotation-container>
  <div oai-annotatable="Button / Primary">
    <button class="button-primary" type="button">Save changes</button>
  </div>
  <div oai-annotatable="Button / Secondary">
    <button class="button-secondary" type="button">Cancel</button>
  </div>
</section>
```

To add annotation support to your own site, install the Annotations Extensibility plugin and give Codex a prompt like this.

Try this prompt

Add browser annotations to my design-system gallery using the Browser Annotation API. Make each component preview selectable as a whole and label it with the component name and variant. Show me how to verify the targets in annotation mode.

### Remote hosts

Use Codex Remote with your ChatGPT account to start, steer, and review work on a connected machine. You can also connect to a development host over SSH. Pick a host with the tools and access the task needs, such as a Mac mini for an iOS simulator.

With your own host, you choose the hardware and keep a persistent setup. Your files, installed tools, and local services stay on the machine between tasks. You manage updates, connectivity, and capacity.

#### Additional resources

- [Get started with Codex Remote](https://developers.openai.com/blog/mastering-codex-remote-for-engineering)

### Remote control in the CLI

You can use the Codex CLI to set up Remote on a computer without installing the ChatGPT desktop app there. Once the host is connected, use the ChatGPT mobile app to start or continue work on it.

1. On the remote computer, install the Codex CLI and make sure the project and its dependencies are available. You can use SSH to run these steps on the host.
2. Run `codex login` on the host and sign in with the ChatGPT account you use on your phone. On a host without a browser, use `codex login --device-auth`.
3. Run the command below on the host to start Remote in the background. Keep the host awake and connected.
4. Open Remote in the ChatGPT mobile app, select the host and your project, and start a chat.

```shell
codex remote-control start
```

For a foreground session, run `codex remote-control` and leave the terminal open. To stop the background service, run `codex remote-control stop` on the host.

#### Additional resources

- [Read the Remote control command reference](https://developers.openai.com/codex/cli/reference#codex-remote-control)

### Codex Cloud

Codex Cloud runs tasks in hosted, isolated workspaces. Choose Work in → Cloud in the desktop app or on the web, then select a published environment. You can also start cloud work from mobile.

To create an environment, select your GitHub repositories and let Codex inspect them, install dependencies, and test the setup. Review the report, add any missing access or build and test commands, then publish the environment. Each new task gets a fresh workspace from that setup. To continue work, follow up in the same task so Codex can resume from its saved state. Enterprise teams can share prepared environments across the workspace.

If a task needs an internal API or database, connect the environment to your private network with Tailscale. For supported cloud services, use OpenID Connect (OIDC) to give tasks short-lived credentials scoped to the resources they need.

### ChatGPT Sites

With an eligible ChatGPT subscription, you can build and host websites and full-stack web apps in Sites. Deploy frontend and backend code together, with hosting features built in.

- **Database and file storage.** Use D1 to store records in a managed relational database and R2 for file uploads such as images and documents.
- **Environment variables and secrets.** Manage runtime configuration and credentials in Site settings.
- **Analytics.** Track page views and unique visitors where analytics is available.
- **Custom domains.** Connect a domain you own where custom domains are available.
- **Authentication.** Use Sign in with ChatGPT to identify visitors and protect features that need an account.

#### Sign in with ChatGPT

Use sharing settings in ChatGPT to control who can view or edit your Site. On a public Site, you can keep pages open to everyone and require sign-in for specific features, such as submitting an RSVP or opening an admin dashboard. Sites provides a signed-in visitor’s email address and full name when available. Check sign-in and permissions on the server before granting access to protected features.

Ask ChatGPT to add sign-in to your Site. Try this prompt from the Sites docs.

Try this prompt

Add Sign in with ChatGPT to this public Site. Keep the Site available to signed-out visitors. Show a Sign in with ChatGPT action when someone is signed out. After they sign in, greet them with their full name when available, or their email address otherwise. Add a Sign out action, and keep authorization decisions in server-side code.

#### Plugins in Sites

Plugins can load data from each visitor’s own connected apps. For example, build a Linear dashboard that shows the issues assigned to you. When a teammate signs in to the same Site and connects Linear, they see their assigned issues. Each visitor’s Linear permissions determine what the Site can access.

Plugins in Sites require a Site that’s private to a workspace where the feature is enabled.

### Code Review

As agents help write more code, you have more changes to review. In the ChatGPT desktop app, open **Code Review** to find pull requests you opened or were asked to review. You can read the summary, inspect the diff and checks, see comments from Codex and other review tools, and leave feedback or approve the PR directly in the app.

If you’re missing context, start a chat with Codex from the PR view. Ask what the change is meant to fix, why it takes a particular approach, or which files and tests matter most. You can also ask about a specific risk, such as whether a checkout change could create duplicate orders on a retry.

#### Additional resources

- [Review pull requests with Codex](https://help.openai.com/en/articles/20001552-review-pull-requests-with-codex)

### Codex Voice

Use Codex Voice to delegate new tasks and keep several threads moving in one conversation. Ask it to start a thread for a new task, check progress on another, or steer work that’s already underway.

You can talk while Codex shows information on screen. For example, ask it to pull up the status of your open tasks, then say which one you want to work on next. You can also ask it to keep replies brief or show the details without speaking.

Once you’ve set up [Codex Remote](#codex-everywhere-remote-hosts), open Remote in the ChatGPT mobile app, choose your device, and tap Voice. From there, you can start threads and steer tasks running on that device.

#### Additional resources

- [Use Codex with ChatGPT Voice](https://developers.openai.com/codex/features/voice)

### Using Dots to keep up with your work

Use your Dot as a personal agent that can start new coding tasks, track work already underway, and steer tasks as they progress. Your Dot can run tasks on its own computer, in a Codex Cloud environment, or on a computer you connect to it. Tell it which environment to use by default.

As your Dot learns what you’re working on and what matters to you, it can flag issues before you ask. It might spot a pull request that contradicts a decision in Slack or flag a teammate’s PR that overlaps with yours. With the right access, you can also ask it to shepherd a PR through CI/CD to production and notify stakeholders at each step.

### Dots across channels

You can reach the same Dot across channels. Each channel has its own interface and conversation history, and your Dot carries shared context and memory across them.

For example, forward a task to your Dot in Slack and ask it to make the change in Codex Cloud and open a pull request. Call your Dot on your way to work to check on the PR, or follow up by text or RCS. When you check in later, your Dot can bring up new developments that matter to you.

#### Additional resources

- [Connect ways to message or call your dot](https://developers.openai.com/codex/dots/channels)

### The Agents API

The Agents API runs the same open-source Codex harness as a managed service. It handles sessions, context compaction, and routing work to subagents. You choose the model, instructions, and tools, including [computer use](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use) for browser tasks.

Use the Agents API to build a custom interface or run a background automation. OpenAI can host the sandbox, or you can bring your own execution environment while OpenAI manages the harness. If you want to own the orchestration too, you can build your own harness with the [Responses API](https://developers.openai.com/api/docs/guides/agents). [Codex App Server](https://developers.openai.com/codex/app-server) is designed for clients that embed the Codex experience, with conversation history, approvals, and streamed events.

This JavaScript example starts an agent in an OpenAI-hosted sandbox and streams its progress. Install the SDK with `npm install openai@latest`, set `OPENAI_API_KEY` to a project key with the permissions listed in the quickstart, and save the example as `quickstart.mjs`. Run it with `node quickstart.mjs`.

Run a task in an OpenAI-hosted sandbox

```shell
import OpenAI from "openai";

const client = new OpenAI();
const events = await client.beta.agents.sessions.create({
  agent: { model: "gpt-6-astra" },
  environment: { type: "openai_hosted" },
  input:
    "Write and run a Python script that prints a Celsius-to-Fahrenheit table.",
  stream: true,
});

try {
  for await (const event of events) {
    console.log(JSON.stringify(event));
  }
} finally {
  events.controller.abort();
}
```

#### Additional resources

- [Follow the Agents API quickstart](https://developers.openai.com/api/docs/guides/agents-api/quickstart)

### Turn down reasoning effort

Start with Medium or High reasoning effort and adjust as you work. Try Low for a straightforward change you can verify quickly. Increase effort if Codex gets stuck or misses important constraints. For simple tasks, higher effort can spend more of your usage limit on reasoning and lead to a more complicated solution than you need.

Use the [Codex model guide](https://developers.openai.com/codex/models) to choose a model that fits the work. For example, try GPT-6.1 Terra for computer use tasks like automating a workflow across apps.

<video controls="" width="960" height="440" aria-label="Turn down reasoning effort workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/reasoning-effort.mp4" type="video/mp4"></video>

Drag the reasoning-effort slider to the left. The label above it updates to show the selected effort.

### Have an agent ask for help

Start with GPT-6.1 Sol at Medium. Save the skill below as `coordinate/SKILL.md` in your skills directory, then invoke `$coordinate` when you want Codex to delegate work.

View “coordinate” skill

```shell
---
name: coordinate
description: Work with focused helpers.
---

# Coordinate

Do the main work yourself, using Luna for scouting or bounded tasks and Astra for advice.

## Luna: `gpt-6-luna`, high

Use Luna for well-defined work or substantial investigations that require synthesizing information across sources. Handle narrow lookups directly. For scouting, give it a concrete question and sources; ask for concise findings with evidence. Use the findings directly and send gaps back to Luna instead of repeating its reads or searches. For changes, specify the files and expected behavior; have Luna implement and check them. Tell Luna not to spawn agents.

## Astra: `gpt-6-astra`, high

Consult Astra when the approach is unclear, repeated attempts fail, or the task needs cross-cutting design or aesthetic judgment. Share the question, relevant findings, constraints, and what you have tried. Use its guidance to continue implementation.

## Coordinate

Start helpers with `fork_turns: "none"`. Give them their assignment and needed context.

Ask helpers to report only to you, with updates that unblock work or change the plan; otherwise report on completion. Relay dependencies between helpers.

After dispatching helpers, wait for completion using `collaboration.wait_agent` with `timeout_ms: 120000`; extend to five minutes for slow helpers. Answer questions or resolve blockers they raise, then resume waiting. After a quiet timeout, wait again without status pings or transcript polling. Continue implementation once helpers finish.

When the user adds follow-up guidance, keep a compact worklog file of the goal, current instructions, assignments, decisions, and completed work. Update entries in place; consult it after compaction or handoff.
```

This saves you from choosing a model for every subtask. Delegation can add time and token usage, and even Astra can misjudge which tasks would benefit from a different model.

#### Additional resources

- [Create a reusable skill](https://developers.openai.com/codex/build-skills)

### Collaborating agents

Pair two agents when they own different parts of the same outcome and their decisions affect each other. For example, one agent can own the web app’s frontend and backend while another owns the mobile app. If either agent needs to change the shared API, have them discuss the change before implementing it.

Give each agent a clear area to edit. Tell them what to coordinate directly, when to escalate a decision, and who will assemble the result. Ask Codex where a pair would help on your task, then use this prompt from the Collaborate skill to set it up.

Try this prompt

Give two peers one concrete outcome, shared constraints, complementary responsibilities, and an initial write split. Both do substantive work; name one to assemble the result. Have them coordinate directly and adjust their split within the authorized subsystem without overlapping edits. Escalate changes to the outcome, protected boundaries, or another lane’s ownership.

### Child threads and worktrees

Codex can use subagents to parallelize parts of a task. The thread that starts them manages their lifecycle. For independent tasks, ask Codex to start child threads. For example, ask it to start five threads in parallel, one to review each pull request.

Each child thread runs independently and can communicate with its parent and sibling threads. Open any child thread to give it feedback or take over, or let the parent keep coordinating the work. This is a thread of threads.

Ask Codex to start a child thread on the same machine, in a new worktree for a separate checkout, or in a remote environment.

#### Additional resources

- [Use subagents in Codex](https://developers.openai.com/codex/agent-configuration/subagents)
- [Run chats in parallel with Git worktrees](https://developers.openai.com/codex/environments/git-worktrees)

### What’s new in the CLI

Recent updates bring the Codex CLI closer to the desktop app. The new Agent command center shows your tasks and their status, and voice mode lets you talk to Codex from the terminal.

On macOS or Linux, run this to install or update to the latest Codex CLI. See the [CLI guide](https://developers.openai.com/codex/cli) for other install options.

Install or update the Codex CLI

```shell
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

#### Open the Agent command center

Run `/agents` to see your tasks and their status. Press Tab to cycle through status filters. Use the arrow keys to select a task and Enter to open it.

<video controls="" width="1280" height="720" aria-label="Open the Agent command center workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/cli-agent-command-center.mp4" type="video/mp4"></video>

Open the command center, move between tasks, then filter to tasks that need your input or are still working.

#### Talk to Codex

Where experimental CLI voice is available, run `/voice` and speak when the terminal shows **listening**. Use `/voice mute` to mute the mic, `/voice stop` to end the session, or `/voice settings` to choose a voice and sound devices.

<video controls="" width="1280" height="720" aria-label="Start voice in the CLI workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/cli-voice.mp4" type="video/mp4"></video>

Start a voice conversation, watch the microphone meter respond, then mute the mic and stop the session.

#### Additional resources

- [Explore Codex CLI slash commands](https://developers.openai.com/codex/cli/slash-commands)

### Shortcuts

Customize keyboard shortcuts in the ChatGPT desktop app’s Settings. Set a shortcut for the command palette so you can quickly jump between threads, and adjust shortcuts for the built-in browser to fit how you work.

You can also set a global shortcut for voice dictation. Press it from another app to dictate text while you work there.

#### Additional resources

- [Customize desktop keyboard shortcuts](https://developers.openai.com/codex/app/settings#keyboard-shortcuts)

### Daybreak Blue

Daybreak Blue gives approved users access to OpenAI models for authorized defensive cybersecurity work, such as reviewing code for security issues and recommending fixes. You can [apply as an individual](https://chatgpt.com/cyber) with an eligible paid plan. To get access, verify your identity and enable Advanced Account Security with at least one compatible physical FIDO2 security key, such as a YubiKey.

#### Workshop tip

If you need a hardware key, OpenAI partners with Yubico to offer preferred pricing on a two-key bundle. [See the OpenAI + Yubico offer](https://www.yubico.com/openai-and-yubico/).

<video controls="" width="760" height="720" aria-label="Enable Daybreak in Codex workshop demonstration"><source src="https://aie-codex-workshop.openai.chatgpt.site/media/daybreak-toggle.mp4" type="video/mp4"></video>

Switch on Daybreak in the model picker. The composer shows GPT-6 Sol High.
