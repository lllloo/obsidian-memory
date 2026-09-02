---
title: OpenClaw 2.0 Release Notes
description: OpenClaw v2026.8.1 官方發布說明，涵蓋安裝、Web UI、記憶、skill、模型、自動化、瀏覽器、外掛與安全的使用者面改動
created: 2026-09-02
updated: 2026-09-02
source: "https://docs.openclaw.ai/releases/2026.8.1"
published: 2026-08-30
tags:
  - clippings
---

> 落地說明：本檔為官方 release notes 的敘述段落，已濾除逐條 PR／commit 清單（原文約 19,500 行）；完整變更記錄回官方頁面查。發布日期以 InfoQ／Decrypt 報導的「2026 年 8 月底週末」推得，官方頁未標明確日期。

For the story behind this release, read [OpenClaw 2.0, Accidentally](https://openclaw.ai/blog/openclaw-2-accidentally).

This update touches every part of OpenClaw, including installation, messaging, memory, skills, models, automations, the browser and native apps, plugins, security, and many smaller fixes.

The sections below describe the user-facing result, with the complete PR and commit record available inside each subsection when someone wants to dig into it.

**Release scale:** 16,977 pull requests, 698 direct commits, and 987 contributors.

## Installation and Onboarding

> [!note] Note
> **Warning**
> 
> **Storage and downgrade warning**
> 
> This release changes how sessions and transcripts are stored by moving them into SQLite. Before downgrading to an older file-backed release, use the current CLI to restore archived legacy transcript artifacts; sessions created after the migration will not appear in older releases.
> 
> Create a [verified backup](https://docs.openclaw.ai/install/updating#before-updating%3A-create-a-verified-backup) before upgrading to protect broader OpenClaw state, and review [downgrading across the session SQLite migration](https://docs.openclaw.ai/install/updating#downgrading-across-the-session-sqlite-migration) before rolling back.

OpenClaw now gives new [Mac, Linux, and Windows installs](https://docs.openclaw.ai/install) a clearer path from download to a first useful conversation, while iPhone, iPad, and Android put pairing and permissions where people need them. Guided setup can reuse supported subscriptions, API keys, and [local models](https://docs.openclaw.ai/gateway/local-models) already available, verifies the chosen model before saving it, and hands off to the web app or terminal when the connection is ready.

Installing OpenClaw

The [supported install path](https://docs.openclaw.ai/install) now keeps the app or command available after setup. A Mac app opened from Downloads or a disk image can offer to move itself into Applications, where updates and launch at login work properly. On Linux and other Unix systems, the installer makes `openclaw` available in new terminal sessions without asking you to edit shell startup files by hand.

Network installations that would expose OpenClaw without authentication are stopped before anything changes. Reinstalling also protects an existing working setup when preparation is cancelled or fails, and gives OpenClaw time to start before reporting whether it is reachable.

Connecting a subscription, API key, or local model

[Guided setup](https://docs.openclaw.ai/start/wizard) now starts by looking for AI access you may already have. It can reuse verified Codex, ChatGPT, or Claude CLI sign-ins, accept an API key, run a supported provider's own sign-in, or find qualifying Ollama and LM Studio models, then prove that the exact choice can answer before it keeps that model and credential. Access already working on the machine can become part of setup instead of another thing to configure.

For OpenAI accounts, setup uses the models the signed-in account can actually access while preserving routes you configured yourself, and administrators can prepare supported [local models](https://docs.openclaw.ai/gateway/local-models) with live progress. Finding or downloading a local model is only the start, so the supported local-model screens do not show Start chatting until that exact choice passes activation.

Starting your first conversation

Successful setup now hands off directly to a [first conversation](https://docs.openclaw.ai/start/wizard). Graphical Mac, Linux, and Windows sessions can open the web app, while SSH and other headless setups provide an authenticated link with port-forward instructions and keep terminal chat available.

From there, the setup conversation can finish supported skill and web-search configuration, then offer an external channel as an optional next step instead of another prerequisite for first use. The classic wizard can still continue without AI because its live model check remains optional.

Setting Up OpenClaw on Mac, Windows, and Linux

On [Mac](https://docs.openclaw.ai/platforms/macos), the main guide points directly to the app, and the local or remote Gateway you choose stays selected even if older startup or cleanup work finishes late. The app waits through the Local Network prompt and legitimate first-run data upgrades, authenticates the exact remote Gateway before moving on, and opens the dashboard only when the connection is ready.

On [Windows](https://docs.openclaw.ai/platforms/windows), the guide points to the latest signed x64 and Arm64 Hub installers. The PowerShell installer now recognizes a supported Node runtime correctly and can continue in the same session after Winget installs Node.js. Windows Hub updates independently, so its standalone stable build can be newer than the mirror included with an OpenClaw release.

On [Linux](https://docs.openclaw.ai/platforms/linux), desktop setup can repair or reinstall OpenClaw, connect to a local or remote Gateway directly or through SSH, verify eligible AI access already on the machine, and resume an interrupted activation. Direct certificate-pinned connections remain unavailable inside the desktop app.

Setting Up OpenClaw on iPhone, iPad, and Android

Mobile setup now puts QR and setup-code pairing first because that is what most people were trying to find anyway, while discovered Gateways and manual host and credential entry remain available. Secure official pairing shows whether the phone has Full or Limited access, and an unencrypted connection to another machine is automatically kept Limited.

On [iPhone and iPad](https://docs.openclaw.ai/platforms/ios), a valid setup QR can now pair and open the main UI in one scan when the connection is already trusted or matches the code, while untrusted connections still stop for approval. OpenClaw explains pairing before asking for Local Network access, lets you decide on optional permissions one at a time, and gives eligible administrators a dedicated Settings conversation for Gateway setup and repair without exposing that privileged assistant in ordinary Chat.

On [Android](https://docs.openclaw.ai/platforms/android), pairing stays usable in landscape, on narrow screens, and with larger system text. Public Gateways can use normal certificate checks while LAN and IP connections keep explicit pinning, and pairing again preserves saved location and notification choices instead of quietly changing consent; revoked permissions remain revoked, and Google Play builds still use foreground location only.

Moving, Importing, or Resetting an Existing Setup

[Imports from Claude, Codex, and Hermes](https://docs.openclaw.ai/install/migrating) now happen in a temporary staging area, where OpenClaw verifies or repairs the model route before making the new setup active. If the source, import plan, or destination changes along the way, promotion stops rather than replaying a half-finished import against different data.

Rerunning onboarding keeps the workspace you already use unless you approve a move, and named agents keep the credentials they own through supported creation and configuration-only resets. OpenClaw validates the provider, Gateway, migration, and workspace choices before a reset can move existing data to Trash, but a valid confirmed reset is still destructive.

Automating Setup and Recovering from Interruptions

[Non-interactive onboarding](https://docs.openclaw.ai/start/wizard-cli-automation) now rejects invalid provider, authentication, Gateway, workspace, and conflicting flow choices before it creates an agent or writes configuration. When `--json` is requested, failures return one machine-readable result instead of empty or mixed output, and a concurrent setup for the same profile fails quickly with the current holder when known instead of sitting there looking frozen.

Cancelled or interrupted setup revokes stale work, while failed provider sign-in or local-model preparation can be retried without cancelling a newer attempt. Gateway health failures stay inside setup with the original diagnostic and recovery hints, but `--json` does not waive risk acknowledgement, and deliberately skipping service startup can still finish without a reachable Gateway, so automation must inspect the reported health instead of trusting exit status alone.

## The New Web UI

The rebuilt [Control UI](https://docs.openclaw.ai/web/control-ui) puts conversations at the centre of OpenClaw, with files, approvals, settings, and live work close to the conversation so you can set up a Claw, follow what it is doing, and keep working without bouncing between separate tools.

Navigation and sidebar

The [web-based experience](https://docs.openclaw.ai/web/control-ui) in OpenClaw now feels more familiar to anyone who uses apps like ChatGPT, Claude, Gemini, or Perplexity, with conversations in the sidebar and the one you are working in at the centre instead of opening on a separate Overview page. Settings and Inbox keep setup details and alerts out of the way until you need them, while conversations and new-session drafts can open in real browser tabs or windows.

The sidebar can stay completely flat or group conversations by project, person, or your own custom groups, folds worktrees back into their original project, and remembers its width, which makes it feel a lot less like developer tooling when you are moving between a lot of work.

Starting and managing conversations

Starting a [new conversation](https://docs.openclaw.ai/concepts/session) is now a proper setup screen instead of a blank chat that inherits whatever defaults happen to be active. Before anything begins, you can choose the agent, model, reasoning level, opening message or image, workspace, and the computer that should run it, then use groups, transcript search, status, and batch actions to manage the work later.

Worktree conversations open immediately with the original message while naming, checkout, and setup continue. If a remote start fails, the submitted prompt and attachments stay visible with a same-session Retry or a read-only Check delivery action, and later messages wait until OpenClaw knows what happened instead of risking a duplicate or sending out of order.

Supported Codex conversations can branch from an earlier message without changing the original, and explicit forks can use more than 100,000 tokens when the selected child model can safely accept that context. Automatic thread and subagent forks keep the 100,000-token limit.

Chat and history

[Chat](https://docs.openclaw.ai/web/webchat) now feels much more alive while a Claw is working. Replies render as Markdown while they stream, older messages load without knocking you out of place, and recent conversations can appear before the Gateway finishes refreshing.

The composer is easier to use during long-running work. You can change the model, reasoning, or speed before sending, edit and reorder queued follow-ups, and use dictation without accidentally sending the result.

One of the more useful additions is `/btw`, which opens a separate multi-turn conversation so you can ask a side question without derailing the work or filling the main history. Faster initial history uses a bounded transcript snapshot stored unencrypted in the browser profile.

Follow the Work and Approve Actions

Following a Claw while it works is much easier. Tool calls now pair clearly with their results, command activity is easier to read, file changes show focused diffs, and larger screens can keep running background tasks beside the conversation with elapsed time and recent activity. People with permission to change the conversation can stop work there, while the full [Tasks page](https://docs.openclaw.ai/automation/tasks) covers work across conversations.

Goals now begin from a normal composer mode and stay manageable through Edit, Pause, Resume, and Clear instead of filling the conversation with slash commands. Drafts survive reloads and session switches, and the card remains usable on a phone even when the objective is long. Older Gateways keep the textual /goal workflow rather than these structured controls. If you have used [approval gates](https://docs.openclaw.ai/tools/exec-approvals) in ChatGPT or Claude Desktop, the approval flow should also feel familiar, with requests inside the conversation that triggered them and a quiet indicator elsewhere when something needs attention.

Once a turn finishes, intermediate commentary and tools fold into a **Worked for** summary you can reopen. Live activity, search results, attachment-only replies, unresolved errors, and pending approvals stay visible instead of being tidied away before they are actually finished, and closing the approval queue leaves a request pending rather than deciding it for you.

Files, Git, browser, and terminal

OpenClaw can now keep the work beside the conversation instead of making you bounce between tools. On supported administrator connections, you can open and edit eligible existing text or Markdown files from Chat, and if a Claw changes the same file while you are working, the editor stops with a conflict instead of overwriting the newer version. The Changes panel shows branch commits and working-tree edits, while eligible GitHub checkouts add pull-request status, CI summaries, and a link to start a pull request on GitHub.

A [docked Browser panel](https://docs.openclaw.ai/tools/browser) can navigate, click, type, scroll, inspect elements, and mark up a screenshot before attaching that screenshot and page context to the conversation, but it requires advertised browser support and an administrator connection, and whatever appears in the page or capture may be sensitive.

Chat, Details, and Discussion can sit in resizable columns or merge into tabs, while the dashboard, [terminal](https://docs.openclaw.ai/tools/exec), and desktop can open in focused views when you need more room. The file editor still cannot create or delete files, Changes stays read-only, and Create PR hands off to GitHub rather than submitting inside OpenClaw.

Settings and connected services

[Settings](https://docs.openclaw.ai/gateway/configuration) is now easier to navigate. It has its own full-page workspace, searches both destinations and individual controls, separates common from advanced options, and keeps panel URLs bookmarkable. If a value is incomplete or invalid, the draft stays on screen so you can fix it, and settings the normal form cannot represent safely open in Raw mode instead of being silently lost.

Major controls also have clearer homes. Connection details, agent identity and memory, Plugins, MCP servers, devices, channels, and pairing are organized around where you actually manage them, while Model Providers brings together the credential health, available models, quota, balance, budget, and spending data each provider reports. That provider view is read-only, and guided MCP management still lives in Plugins while Settings keeps diagnostics and raw editing.

A browser with limited access can request administrator scope, but another administrator still has to approve the signed request from that device. Trusted dashboard links and the native pairing flow can help eligible administrators recover access without turning a shared token into a bypass.

Sharing and Incognito

On a [multi-user Gateway](https://docs.openclaw.ai/concepts/multi-user), a conversation now keeps its creator and each identified person's prompts visible, while owners or administrators can choose whether someone else may read, suggest changes, work in a draft, or participate directly. Drafts can be created and published without a race, suggestions keep their author, and lightweight presence and typing cues make it easier to tell who is there without cluttering a solo setup.

People can manage their own display name and avatar, and permitted Online cards can show what someone is working on without exposing IP addresses or conversations the viewer cannot open. These controls make collaboration understandable, but they are not tenant isolation or a security boundary, and revoked access can briefly look available until the UI refreshes or the Gateway rejects the action.

Incognito is off by default and deliberately narrower. Its conversation stays in process memory, does not write the normal transcript or automatic OpenClaw memory to disk, and disappears when the Gateway restarts, but the model provider still receives the messages, tools can still write files or affect external services, content-free audit metadata remains, and whoever operates the Gateway can see live work.

Appearance, language, accessibility, and mobile

The [Control UI](https://docs.openclaw.ai/web/control-ui) is easier to navigate without a mouse. Keyboard and focus behavior is more consistent across navigation, dialogs, tabs, Settings, plugins, skills, Usage, Workboards, the terminal, and the browser, with skip links, clearer assistive-technology labels, and focus returning to the right place after menus and dialogs close.

On phones and tablets, text sizing now reaches navigation and sidebar content. Inputs no longer trigger iOS zoom, touch devices avoid desktop-style hover highlights, and Send or Stop responds to the first tap on the documented Android Chrome and installed-PWA layouts while desktop hover behavior stays intact.

Appearance now includes seven built-in themes and separate Interface and Chat prose font pickers. You can mix any of nine self-hosted typefaces, or the system stack, with any theme while JetBrains Mono remains the code face. Authenticated profile choices can follow you across browsers, connections without a writable profile keep them browser-local, and all 20 maintained non-English Control UI locales load only when selected and fill previously missing strings.

Control UI Latency and Responsiveness

The [Control UI](https://docs.openclaw.ai/web/control-ui) now reaches Chat faster. In a simulated default-chat test with a mocked Gateway and 50 millisecond HTTP/1.1 latency, JavaScript requests fell from 140 to 45 and startup fell from about 1.6 seconds to 575 milliseconds.

It also stays lighter the longer you leave it open. Hidden panels stop fetching data they do not show, retained state is bounded, and returning to a conversation repeats less rendering.

Reconnects reject stale responses and keep the right conversation selected as the connection changes. If the page bundle loads but never renders, OpenClaw now shows recovery guidance and a Try again action, while interrupted updates reconcile with the replacement Gateway and confirm success only after it reports the expected version.

## Updates and Maintenance

Users could sometimes experience instability after updating OpenClaw. [Supported update paths](https://docs.openclaw.ai/install/updating) now inspect the installation before replacing it and stop unsafe candidates while leaving the previous CLI runnable. In the Control UI, updates identify the target, ask for confirmation, and keep progress and the final outcome visible.

Maintenance tools now provide clearer recovery paths. Configuration errors point to the setting that needs attention, Doctor focuses on problems and the next action, new backups are checked against the guarded restore path, destructive cleanup stops when ownership is unclear, and supported restarts give tracked work time to finish before handoff.

Installing OpenClaw Updates

Gateway updates started in the [Control UI](https://docs.openclaw.ai/install/updating) now identify the target, require confirmation, show progress through the update and restart, and report the final outcome. On eligible signed Mac apps, that flow updates the app first and then only the app-managed local Gateway; browser and user-managed installs keep their Gateway-only path.

[Supported CLI updates](https://docs.openclaw.ai/cli/update) check Node compatibility, package-manager lifecycle rules, and whether npm, pnpm, or Bun owns the installation before replacement. An unsafe candidate stops while leaving the previous CLI runnable, and an exact `openclaw update --dry-run` previews the path without changing configuration, handoff, cleanup, or restart state.

On Linux, code updates can preserve an administrator-owned service definition instead of trying to rewrite it, while an unsafe or uninspectable service handoff still fails visibly. If a plugin replacement asks for new capabilities, OpenClaw keeps the known-good plugin available while the replacement waits for review; `openclaw update --accept-capabilities` or `openclaw update repair --accept-capabilities` approves only the staged artifact for that invocation, and `--yes` does not.

One upgrade path still needs a manual repair. If you are on OpenClaw 2026.7.1 with pnpm 11, run `pnpm add -g openclaw@latest` once. OpenClaw does not upgrade Node for you.

Configuration Errors and Service Repairs

Bad [configuration](https://docs.openclaw.ai/gateway/configuration) now stops with a useful answer instead of quietly starting OpenClaw with something else. Packaged builds, CLI checks, service preflight, and Gateway startup show the file, line, full setting path, allowed values when available, and a safe version of what was received; malformed top-level scalar files fail closed instead of loading defaults.

If you are upgrading a configuration that still contains retired keys, run `openclaw doctor --fix` before September 18, 2026. [Doctor](https://docs.openclaw.ai/cli/doctor) keeps canonical values when old and new keys conflict and removes settings that no longer do anything, although explicitly retired tuning values return to the built-in defaults.

Supported Gateway service repairs preserve the installed state directory, config path, port, managed environment, and eligible file-backed credentials instead of silently retargeting the service. Changing those targets intentionally requires `openclaw gateway install --force`; on Linux, service commands also refuse conflicting user and system units and show which unit owns the Gateway.

OpenClaw Restarts and Running Work

Before a supported snapshot or [targeted restart](https://docs.openclaw.ai/gateway/restart-recovery), Gateway suspend and resume can pause new ordinary work, report blockers, and drain the agent runs, deliveries, scheduled jobs, queues, sessions, and background commands OpenClaw already tracks. Failed configuration reloads keep the prior coherent state, and rapid configuration writes retain pending restart intent instead of dropping it.

After restart, health checks, the agent list, and core controls become usable before optional catalog, plugin, and migration work finishes. That work is deferred rather than removed, so the first explicit catalog request can still take longer.

The wait covers work OpenClaw tracks. New channel or external ingress, existing plugin connections, unregistered background work, and durable receipt of incoming messages remain outside it, and externally supervised installations must consume the handoff and complete their own restart.

Troubleshooting, System Health, and Logs

[Doctor](https://docs.openclaw.ai/cli/doctor) now spends less time reciting healthy inventory and more time showing what broke and what to do next. A recoverable interactive startup failure can offer one confirmed `doctor --fix` attempt, while an unrecoverable configuration stays unchanged with exact instructions to inspect, edit, or move it aside. Bare `openclaw doctor --json` is a read-only advisory check; use `openclaw doctor --lint --all` when you need the advisory checks omitted from the default run.

[Logs](https://docs.openclaw.ai/cli/logs) now fill their bounded tail window across short reads, preserve Unicode at file boundaries, distinguish line and byte truncation from rollover, and report unavailable storage instead of an empty success. Status keeps its base report when optional health details fail, so missing information remains unknown rather than being shown as healthy.

In the admin Control UI, Ask OpenClaw can turn consequential health state into a diagnostic question and keep the system-care conversation docked as you move around, while the System overlay shows a short history of scheduler pressure, CPU, memory, event-loop delay, and optional disk activity. These controls require admin or operator access and do not appear during onboarding or to read-scoped clients.

Command-Line Output and Shell Completion

Commands used by scripts now have a more predictable machine interface. The named JSON and JSONL commands keep terminal-reset bytes out of stdout and return a consistent structured error when an invocation fails, so automation no longer has to special-case them.

[Shell completion](https://docs.openclaw.ai/cli) installation and refresh preserve unrelated profile content and permissions while publishing profiles and caches atomically across Bash, Zsh, Fish, and PowerShell. Remote Gateway turns and common read-only commands also skip startup work they do not need, while local probes and human output keep fuller validation; mistyped commands now point to the command tree that rejected them, nearby commands, and the correct help.

The predictable machine-output contract covers the named command paths. Human diagnostics can still appear on stderr, successful degraded results remain command-specific, and raw lifecycle-error redaction is not yet universal.

Backup, restore, reset, and uninstall

[Reset and uninstall](https://docs.openclaw.ai/cli/reset) now refuse to remove data until the Gateway service is torn down and OpenClaw can establish that no other process owns the state. If teardown or ownership checks fail, the state stays put, and a state-only uninstall leaves configured workspaces alone.

New [full backups](https://docs.openclaw.ai/cli/backup) preserve configured agent state roots and safe relative links, avoid mistaking active archive work for a stall, and restore default or custom layouts through the same guarded flow. Managed `dev/` checkouts and local source edits still need a separate backup, while older archives containing absolute generated `plugin-skills/` links remain rejected.

Known-vulnerable Node and SQLite combinations now stop before state opens, with guidance for whether the embedded Node runtime or shared system SQLite library needs upgrading.

## Messaging

Messaging now keeps more of a conversation intact across the places people already talk to their Claw. [Telegram](https://docs.openclaw.ai/channels/telegram) gains richer messages and media, [Slack](https://docs.openclaw.ai/channels/slack) keeps live progress and the final answer together, [Discord](https://docs.openclaw.ai/channels/discord) adds opt-in Activities and voice rooms that understand who is present, and the native apps keep media and pending sends inside the conversation where they belong.

Across supported channels, OpenClaw now holds accepted messages through managed restarts, reports whether a connection is usable, recovering, or blocked, and preserves an uncertain send instead of blindly sending it again. Recovery starts once OpenClaw has accepted the message, and each service still controls what it can confirm beyond that point.

Message Delivery and Recovery

On supported channels, [messages OpenClaw has accepted](https://docs.openclaw.ai/concepts/messages) now stay pending through a managed restart, and channel status shows whether a connection is usable, recovering, or blocked. When a send times out without a confirmed result, OpenClaw keeps that outcome uncertain and can warn on the next contact rather than creating a likely duplicate. Recovery begins after local acceptance.

Eligible single-choice questions can use native controls on Telegram, Discord, and Slack, while longer Telegram and Discord turns can show a short status headline with compact tool activity. Multi-select and free-text questions continue through the supported client or text path, and Telegram partial-answer streaming remains a separate opt-in mode.

Telegram

On rich-enabled [Telegram](https://docs.openclaw.ai/channels/telegram) accounts, agents can send native details, tables, checklists, math, maps, file references, locations, venues, and a compatible round video note. Large nested replies paginate within Telegram's limits, and rejected rich structures fall back to the complete plain-text answer instead of dropping the useful part.

Busy conversations hold together better too. Follow-ups stay ordered during active work, accepted updates can resume after a restart, abandoned delivery claims stop freezing the chat, and verified public poll activity returns to the chat or forum topic where it began. Anonymous polls remain display-only, and quoted text reaches the agent as attributed quotation rather than active instructions.

Discord

[Discord](https://docs.openclaw.ai/channels/discord) now supports opt-in [Activities](https://docs.openclaw.ai/channels/discord-activities) that open configured OpenClaw widgets directly inside Discord. Voice agents can also see who is in the room, use different wake-name rules for one-on-one and group conversations, and optionally join only while a human is present. Activities require explicit channel configuration, a Discord client secret, and a public HTTPS route; occupied-room auto-join is a separate option and does not change the existing always-on default.

Message retries now reuse their identity to reduce duplicates, interaction replies settle in order, stale reply context is discarded, and repeated resume failures can recover without restarting all of OpenClaw. Forum-thread sends still remain uncertain when retrying them could produce a duplicate.

Slack

[Slack](https://docs.openclaw.ai/channels/slack) progress now stays in one conversation from the first status through the final answer, keeping the running commentary, work steps, and answer inside one streamed message unless an operator chooses the more compact alternative. Charts and tables can render natively too, with readable text preserved when Slack cannot use the native form.

One organization-installed app can also serve the Enterprise Grid workspaces Slack grants it, with messages, actions, approvals, and proactive delivery bound to the right workspace. Destinations outside the current conversation require an explicit workspace, requests without verified workspace identity are rejected, and relay mode plus org-wide surfaces remain unsupported.

WhatsApp

[WhatsApp](https://docs.openclaw.ai/channels/whatsapp) can now list groups from the linked account without making someone hunt through logs or invite links, and it avoids opening a competing connection while OpenClaw already owns that account. If OpenClaw restarts after accepting an incoming message, the pending work can continue without later events jumping ahead, while multipart replies keep the parts and receipts that actually succeeded instead of replaying the entire response after one part fails.

Signal

[Signal](https://docs.openclaw.ai/channels/signal) replies now keep their native quote block through ordinary, chunked, media, and durable delivery when quoting is enabled. Messages received just before a crash can resume from local storage, and a failed recipient is reported instead of disappearing into a false success. Group sends remain conservative after any member receives the message, so one failed recipient does not cause the whole reply to be repeated to everyone else.

iMessage and BlueBubbles

[iMessage](https://docs.openclaw.ai/channels/imessage) is now an official installable plugin that carries existing configuration and state through the move out of core. Eligible approval requests can use native Messages polls, while older bridges, SMS, and failed poll sends keep the existing text, reaction, or command fallback.

Remote Mac setups also keep attachments with the correct existing chat and can use supported remote paths and actions without sharing a filesystem with the machine running OpenClaw, while incoming messages already stored before a crash can replay. New setups still need the plugin and `imsg` on a signed-in Mac, and this remains separate from the iOS and macOS OpenClaw chat apps.

Feishu and Lark

In [Feishu](https://docs.openclaw.ai/channels/feishu), an agent can resend a sticker previously received by that bot account and, when an operator adds labels, find the right sticker by keyword. Accepted Feishu messages and comments can also resume after a restart, streaming cards keep the latest accepted version, and unsupported image formats remain available as file attachments instead of being discarded. Sticker actions and labels are opt-in and do not retroactively organize an existing collection; the sticker and comment work is specifically verified for Feishu rather than every Lark path.

Mattermost

[Mattermost](https://docs.openclaw.ai/channels/mattermost) can now read bounded, paginated history from channels the bot can already access once an operator enables the feature. Integrations that rewrite or cancel replies now complete that work before delivery, preventing an early preview from exposing content that the hook removes or changes. Completed sends also keep the real Mattermost post identity across previews, actions, media, and durable paths.

Matrix

[Matrix](https://docs.openclaw.ai/channels/matrix) replies can now use native spoilers, underline, tables, and up to 100 discoverable room or personal custom emotes. More importantly, an encrypted room now fails visibly when encryption is unavailable instead of quietly falling back to plaintext text, attachments, filenames, or media metadata. Large tables can still choose their own readable formatting fallback without weakening the room's confidentiality boundary.

Microsoft Teams

Configured [Microsoft Teams](https://docs.openclaw.ai/channels/msteams) approvers can approve or deny eligible exec and plugin requests from a native Adaptive Card in the chat or channel thread where the request began, then see the recorded outcome on that same card. Quoted replies, attachments, streaming results, and duplicate handling also stay bound to the originating conversation. The cards cover configured exec and plugin requests only and require valid authentication, permissions, tenant authorization, and routing.

Google Chat

[Google Chat](https://docs.openclaw.ai/channels/googlechat) webhook events accepted by OpenClaw now remain queued through restarts, keep their order within each space, and recognize Google's retries before they create duplicate work. Recovery begins when the Gateway admits the event; events Google never delivered remain outside that recovery path.

LINE

[LINE](https://docs.openclaw.ai/channels/line) keeps mixed rich replies, their quick actions, and media together, using the reply path for as many as five messages when the response fits instead of consuming Push API quota unnecessarily. Long code that will not fit a Flex card falls back to ordinary chunks, unsupported media remains visible as a link, and blank or rejected rich structures no longer take the whole reply with them.

In groups that require a mention, slash commands addressed to the bot now run as commands, and quoting one of its recent Gateway-sent messages can address it without a second mention. Date, time, and rich-menu selections reach the agent, while supported actions and choices return as native controls with visible text for anything LINE cannot render.

A bot can also post one room-specific introduction when it actually joins an allowed group, while respecting both channel-wide and per-account opt-outs. Webhook events are stored before acknowledgement so work OpenClaw already admitted can continue after a restart. Affected installations that passed through the brief pre-drain queue transition migrate eligible accepted rows before delivery resumes, while genuinely mismatched rows remain quarantined and messages for removed accounts wait until that account is restored.

SMS, MMS, and RCS with Twilio

The [Twilio-backed channel](https://docs.openclaw.ai/channels/sms) can now send and receive MMS and show recent provider or carrier states such as sent, delivered, failed, or conflicted without retaining message bodies or phone-number addresses. SMS and RCS messages OpenClaw has already accepted can survive a restart in sender order, while replay protection fails closed instead of accepting work it can no longer protect from duplication.

Delivery observations are kept for 30 days and reflect the latest state reported by Twilio or a carrier, which can differ from recipient-visible delivery. If the replay cache fills, new events are rejected rather than accepted without duplicate protection, and Twilio does not retry that response by default.

ClickClack

[ClickClack](https://docs.openclaw.ai/channels/clickclack) can place a team discussion beside an OpenClaw session, giving people somewhere to coordinate around the work without turning the agent's main transcript into a meeting room. Guided and command-line setup, readable discussion names, native command menus, attachments, optional group mention rules, and opt-in progress make that room easier to use while keeping the final answer visible.

Opening a discussion still requires an authorized operator and a reachable ClickClack deployment. Generated names remain best effort, and mention-gated or bot-to-bot conversations have to be enabled deliberately.

Reef

Trusted Claws can talk directly through [Reef](https://docs.openclaw.ai/channels/reef), OpenClaw's bundled end-to-end encrypted agent channel, using friend-code pairing, terminal registration and friendship controls, and discovery that keeps an external peer distinct from a local thread. Operators can now add plain-language inbound and outbound sharing rules for their own sensitive topics and named friends, while deterministic denials for secrets and credentials remain in force and changing the rules invalidates pending approvals from the old policy.

When an inbound message needs owner review, that recorded decision now owns later redelivery instead of rerunning the guard until the answer changes, and later inbox messages can keep moving while it waits. Temporary inbound guard failures leave the item parked for another attempt rather than rejecting it, with approved delivery receiving one final guard check and outbound sends still failing fast.

When a peer rejects a message, the sending agent gets bounded feedback and one controlled chance to rephrase before it stops for owner guidance instead of arguing in a loop.

Agent-to-Agent Messaging with A2A

OpenClaw can now expose selected agents to explicitly trusted external agent systems through the [A2A v1.0 protocol](https://docs.openclaw.ai/channels/a2a). Configured peers can discover those agents, submit and poll authenticated tasks, receive replies as artifacts, and exchange text or structured data, while an unconfigured plugin registers no discovery or task routes at all.

This first version supports one account, keeps tasks in memory, and does not yet provide streaming, push notifications, or cancellation. Authenticated peers currently operate as trusted callers rather than passing through the normal command-policy decision, so this is a deliberate interoperability path for known peers rather than a public agent endpoint.

Buzz

[Buzz](https://docs.openclaw.ai/channels/buzz) is now an official OpenClaw channel for team rooms, with guided setup that can route different rooms to different agents and live directories that give those agents current room and member names without replacing the stable UUIDs used for automation. One Gateway can now run named Buzz accounts with separate bot identities, credentials, rooms, routing, and lifecycles while preserving the legacy root account and environment fallback, and updating one account does not unnecessarily disconnect healthy siblings.

Replies can use native mentions and threads, and operators can choose flat automatic replies and typing while explicit message-tool and CLI targets remain explicit. Mention-gated rooms can carry a small amount of recent authorized context into the next turn without running the model on every background message.

Setup finishes only after Bot-role membership is verified, a room name must resolve uniquely before it can be used safely, native mentions cap at 50, and passive context remains opt-in and tightly bounded.

QQ Bot

[QQ Bot](https://docs.openclaw.ai/channels/qqbot) has moved to Tencent's integrity-pinned external plugin while keeping the public `qqbot` channel ID and carrying existing credentials, account selection, allowlists, approval restrictions, streaming behavior, and group tool policy when Tencent 2.0 can represent them safely. If an older policy cannot be translated without weakening it, Doctor stops for an explicit repair instead of quietly changing the rules. Inbound envelopes already accepted into the local queue can also resume after a restart.

Zalo and Zalo Personal

[Zalo Bot](https://docs.openclaw.ai/channels/zalo) and [Zalo Personal](https://docs.openclaw.ai/channels/zalouser) now keep accepted messages through restarts using separate recovery paths. Zalo Bot records a webhook before acknowledging it, while Zalo Personal resumes accepted socket messages from its account queue without one delayed conversation holding up unrelated chats. Polling and webhook modes remain mutually exclusive, and targeting, reactions, formatting, delivery errors, and partial receipts remain specific to the path that handled the message.

Tlon and Urbit

[Tlon](https://docs.openclaw.ai/channels/tlon) now saves an accepted Urbit message before acknowledging it, so work already admitted to OpenClaw can resume after a restart without immediately abandoning the server cursor. Replies gain native Markdown lists, and oversized SSE events or JSON payloads stop before they can grow in memory without bound.

There is one hard recovery limit. If Eyre has definitively deleted a channel, OpenClaw can create and subscribe to another one, but the old cursor and its server-side history are gone.

Nextcloud Talk

[Nextcloud Talk](https://docs.openclaw.ai/channels/nextcloud-talk) can now process different rooms concurrently while preserving message order within each room. Up to 32 deliveries can be active at once, with excess work queued, and sends or reactions to an unresponsive self-hosted or remote server now fail within a bounded time instead of hanging indefinitely.

Nostr

A [Nostr](https://docs.openclaw.ai/channels/nostr) direct message can move to the next configured relay when one cannot connect, return the real connection error when every relay fails, and expose the successful relay's real event ID instead of a synthetic timestamp. Named accounts, protected keys, profile imports, reply targets, and ordered encrypted chunks also stay attached to the selected account more consistently.

Synology Chat

[Synology Chat](https://docs.openclaw.ai/channels/synology-chat) now records inbound webhook work before returning success, allowing accepted messages to resume after a restart. If the local write fails, OpenClaw returns an error so the sender can redeliver, while the upstream retry remains controlled by Synology. Long Unicode replies keep their order, lookups and responses are bounded, and uncertain outbound sends remain unresolved instead of being replayed into a duplicate.

Twitch

[Twitch](https://docs.openclaw.ai/channels/twitch) chat already accepted into OpenClaw's local queue can continue after a process crash. Stalled user lookups can be cancelled, stopped accounts stay stopped even when an earlier connection attempt finishes late, and ordinary replies keep normalized attachment links while internal tool traces and XML scaffolding are removed before they reach chat.

IRC

[IRC](https://docs.openclaw.ai/channels/irc) channel messages already admitted to OpenClaw can resume in order after a restart without echoing the bot's own replies back into the room. Direct-message recovery stays tied to the connection that accepted it and stops if that identity changes, while mentions follow IRC nickname rules, Markdown becomes readable plain text, and internal tool traces stay out of the channel.

Android Chat

[Android](https://docs.openclaw.ai/platforms/android) now writes text, images, and voice notes to its outbox before using the network, keeping them through offline periods and restarts until conversation history confirms delivery. If the outcome remains uncertain, the item stays visible with explicit Retry and Delete controls and is not sent again automatically.

Supported audio and video play inline, video uses the native upload flow, and notification replies return to the exact saved conversation or fail. Older 2026.7.x OpenClaw installations use a reduced compatibility path.

iOS and macOS Chat

The [iOS](https://docs.openclaw.ai/platforms/ios) and [macOS](https://docs.openclaw.ai/platforms/macos) OpenClaw apps can play supported managed audio and video inside chat, upload video from the native composer, and hand the active attachment to system Now Playing controls. A slow accepted reply stays visibly pending while live state and saved history reconcile, so late history cannot clear a newer turn just because it arrived second.

A run that truly produces no output eventually releases the composer without inventing a reply. Native video uploads retain the 20 MB limit, and these chat apps remain separate from the iMessage channel plugin.

Control UI, WebChat, and TUI

[Control UI chat](https://docs.openclaw.ai/web/webchat) now gives supported generated documents and managed audio and video their own named cards instead of exposing raw attachment instructions or treating every file like a download. Ready video can expand over the conversation, compatible delivered media can play inline, and every attempted attachment keeps a visible named outcome with actionable failure guidance. Active or unknown file formats remain unavailable rather than becoming downloadable, while media the browser cannot prepare keeps its download action.

Across Control UI, WebChat, and TUI, prompts, live work, attachments, and replies stay aligned when several clients share a conversation or reconnect at different times. Delayed prompts no longer jump below their live replies, and terminal users keep a privacy-safe attachment warning beside the answer and after history reload.

These are OpenClaw's own chat clients rather than external messaging services, and the saved conversation remains the final record when a live update and refreshed history disagree.

Voice calls

[Voice Call](https://docs.openclaw.ai/plugins/voice-call) can opt into an agent's main transcript when an operator wants phone and desktop conversations to share history, while the default remains one session per phone. Realtime agents can speak their final words and request a hangup, and failed startup, carrier hangup, or media silence now closes the unusable session instead of leaving it active until the maximum duration.

Choosing the main transcript places raw call turns in primary history. A carrier can still reject a requested hangup, and carrier, provider-media, Discord, Talk, and Meet calls keep their own credentials and lifecycle rather than being treated as one interchangeable voice system.

Raft

[Raft](https://docs.openclaw.ai/channels/raft) setup now says clearly when the machine running OpenClaw cannot find the Raft executable instead of presenting a configured channel as healthy. A passing probe means the command-line tool was available at that moment, not that a later connection or message has already succeeded.

## Memory

[Memory](https://docs.openclaw.ai/concepts/memory) now lets an eligible personal Claw recall relevant context from that agent's other private conversations, including what mattered immediately before a reset, while visible workflows let you search indexed sources, inspect how memory is working, import supported history, and remove attributable derived memory. Recall stays within the same agent's private conversations and respects explicit isolation and access policy.

Built-in Memory owns the core search and recall path, with a supported Doctor migration from QMD. LanceDB, Memory Wiki, external embedding services, `MEMORY.md`, and `USER.md` still have distinct roles, and forgetting derived memory does not erase the original conversation or copies outside OpenClaw.

Upgrading to built-in Memory

[Built-in Memory](https://docs.openclaw.ai/concepts/memory-builtin) now owns the core search and recall path. If you use [QMD](https://docs.openclaw.ai/concepts/memory-builtin#migrating-from-qmd), run `openclaw doctor --fix` to remove retired QMD settings, carry forward supported extra paths and any session indexing you explicitly enabled, preserve compatible rows already in the agent database, and rebuild the index from canonical Markdown.

The migration carries supported data into a different core, so QMD-only reranking, query expansion, and cross-agent transcript search are retired. Malformed structures, incompatible vector dimensions, and data without a safe owner remain stopped for repair.

Finding and recalling past context

On eligible personal setups, your Claw can recall relevant context from that same agent's other private conversations by default, including what mattered immediately before you reset the session. Recall remains limited to that agent's private conversations; groups, channels, shared aliases, other agents, deleted history, and policy-blocked sources stay out, and an explicit direct-message isolation setting still wins.

[Built-in search](https://docs.openclaw.ai/concepts/memory-search) now understands filenames, full and partial Unicode paths, and configured extra paths, broadens thin strict matches, and keeps keyword results available when an optional embedding provider cannot start. While memory or session content is being rebuilt, each search stays on one stable published index, and later searches use its replacement only after publication instead of waiting behind routine maintenance or mixing generations. Search stays within the configured roots and agent boundaries, while required embedding providers fail closed.

Sessions without a configured reset policy now remain open across days, and durable reset or compaction markers explain visible history changes. SQLite-backed chats on web, macOS, iOS, and Android can rewind to a user message, [fork the conversation](https://docs.openclaw.ai/concepts/session), and switch among preserved branches. Rewinding changes the transcript branch, but it does not undo files, sent messages, or other tool side effects.

Importing memories and conversation history

Importing is separate from the QMD-to-built-in upgrade. You can [bring supported memory](https://docs.openclaw.ai/install/migrating) from Codex, Claude Code, or Hermes into an agent workspace through the Control UI, first-run setup, or Ask OpenClaw while leaving the source alone and not sweeping in credentials, settings, skills, or arbitrary provider files. If the destination already contains conflicting content, replacement has to be reviewed explicitly.

Old conversations follow their own preview-first path. The CLI shows what it would stage before it writes, the Control UI reports bounded-batch progress, and material owned by that import can be rolled back and applied again. Large histories use bounded or indexed processing, Memory Wiki preserves human notes through supported imports, and older history without complete ownership tracking may need to be rescanned. Staged material still does not become durable memory until dreaming or an explicit promotion chooses it.

Reviewing, creating, and forgetting memories

Settings now has a [Memory destination](https://docs.openclaw.ai/concepts/memory) for live status, Dreams, configuration, indexed-source search and browsing, add-on controls, and embedding readiness, so you can see what your Claw has available and open safe workspace memory files. Memory Wiki overview and Imported Insights dashboards now read published snapshots instead of reparsing the whole vault for every request, keeping large views responsive and showing when a rebuild is running or a manual compile is required. Session and legacy sources remain snippet-only, and add-on changes remain read-only unless the connection has admin authorization.

Eligible observations can be consolidated into `MEMORY.md`, durable directives can live in `USER.md`, standing intents can wait for the right event, and project memories stay scoped to the project that produced them. Automatic memory remains bounded and provenance-gated, so content derived from network or restricted sessions keeps an untrusted origin and stays out of automatic context even though an explicit search can still surface it. This provenance protection applies to newly tracked material, while older untracked files retain their existing classification.

[`openclaw memory forget`](https://docs.openclaw.ai/cli/memory) lets you preview a purge by session, hook source, or participant, then remove attributable derived memory and stop the selected session from being pulled back in by backfill, indexing, or dreaming. An interrupted purge can be retried, and newly attributable consolidation or backfill diary claims are removed with the selected session. The purge follows recorded provenance, so the original transcript, older lineage-free notes, other agents' stores, direct or external writes, exports, and backups may remain. Review the preview before applying it.

## Skills

[Skills](https://docs.openclaw.ai/tools/skills) turn the way you work into reusable instructions your Claw can follow again, and this release connects the entire path. You can create and validate a skill, find or install it, call it directly from a conversation, review proposed changes, and have supported edits ready on the next turn of a persistent session. Invalid skills are reported individually, so the rest of the catalog remains available.

Skill Workshop brings proposals, checks, decisions, and applied history into one workflow. Self-learning can turn substantial work and durable corrections into proposed improvements, or maintain skills created through Workshop when automatic learning is enabled, while skills owned by you or someone else stay under their owner's control.

Creating and checking skills

[Creating a skill](https://docs.openclaw.ai/tools/creating-skills) now follows one guided path from choosing how it should be invoked through adding supporting files, saving it, and validating the result. The checker understands supported invocation metadata and catches problems such as an overlong description before anything is written.

OpenClaw now reports malformed metadata, unreadable files, oversized instructions, and shadowed copies against the skill that caused them, while continuing to load valid skills around it. In a persistent Gateway session, edits to canonical and managed-worktree skills are available on the next turn, and required skill instructions are read in full.

Finding, Installing, and Using Skills

[Installed skills](https://docs.openclaw.ai/tools/skills), ClawHub discovery, skill settings, and Skill Workshop now share one Plugins hub, giving you one place to find a skill, install it, configure it, and confirm its current status. Skills and plugins keep their separate lifecycles, while reconnecting or switching the active agent, model, or connectors refreshes the lists from the current Gateway.

When a skill is available to you and the active agent, you can choose it in chat or name up to eight with `$skill-name` across supported chat and agent entry points, including eligible skills hidden from automatic model selection. The chat picker adds references to your draft without sending it, and Code Mode can list and read eligible skills within its existing sandbox and allowlist. Large model-visible catalogs can still be compacted, so `openclaw skills check` remains the complete inventory.

Reviewing Changes in Skill Workshop

[Skill Workshop](https://docs.openclaw.ai/tools/skill-workshop) gives you one place to turn an idea or a reusable lesson from substantial past work into a reviewable skill change. You can inspect the proposed instructions and supporting files, see results from plugin-provided scanners, benchmarks, and graders, revise the proposal, and then apply, reject, or quarantine it. Past-work scans produce pending proposals rather than editing live skills, and Android users can search and inspect them before an authenticated administrator makes a change.

Every decision stays bound to the exact proposal revision you reviewed, so a later revision returns for review. Critical prompt-injection findings block application, interrupted applies can recover without overwriting a target changed elsewhere, and an explicitly selected remote Gateway remains the authority for the change. Applied revisions are grouped by skill with newest-first history and comparisons that say when the visible diff is incomplete.

How Skills Improve Over Time

OpenClaw can turn substantial work and durable corrections into reusable skills, then improve the Workshop-created skills that actually shaped a run. New and unconfigured installations start in `auto`, while upgrades keep their existing choice. `off` disables automatic repair, `propose` queues changes for review, and `auto` can create or update Workshop-owned skills with targeted patches or a same-turn repair. The conversation already in progress keeps the version it loaded until the next turn.

Skills you wrote and shared skills owned elsewhere remain yours. [Automatic learning](https://docs.openclaw.ai/tools/self-learning) can suggest improvements to them, but it cannot rewrite or remove them on its own, and explicit `/learn` or past-work scans also produce proposals for review.

On supported agent runtimes, optional background review runs separately without interrupting or posting into chat. When both the learning mode and scheduled-job settings allow it, a visible weekly job reviews the collection, records usage and outcomes, preserves specialized skills, and creates recoverable backups. Restoring a backup remains an explicit choice.

## Native Apps

This release makes the [native apps](https://docs.openclaw.ai/platforms) useful for more of the work around a conversation. iPhone, iPad, and Android bring voice, attachments, model choices, and conversation controls into Chat, macOS adds Quick Chat from the menu bar or a global shortcut, and Wear OS brings transcripts, replies, Talk, and session controls to a paired watch. Apple Watch retains wrist actions through relaunches and retries, while the Linux desktop companion work now covers a tray, an embedded Control UI, and Quick Chat.

Progress cards and assistant-created widgets also bring more of the Claw's active work into supported native conversations, with translations, profile accents, waveforms, and file diffs appearing on the specific clients covered below.

iPhone, iPad, and Apple Watch

On [iPhone and iPad](https://docs.openclaw.ai/platforms/ios), one Chat surface now handles typing, dictation, voice notes, attachments, realtime Talk, and the session, model, reasoning, and tool-activity controls around a conversation. The sidebar makes it easier to switch agents, search and manage recent conversations, see what needs attention, and pin the destinations used most often.

Sharing into OpenClaw now previews supported attachments and shows their progress from preparation through completion or failure. Completed shares in this release support text, links, or one to three images, and Send stays unavailable when an unsupported, excess, or unloadable attachment would otherwise be left out.

Apple Watch retains messages, approvals, replies, and commands through relaunches, Gateway changes, navigation, and retries, then reconciles the result across the phone and Watch so the same wrist action is less likely to be lost or repeated.

Android and Wear OS

[Android](https://docs.openclaw.ai/platforms/android) puts dictation, voice notes, realtime Talk, model and thinking choices, context use, attachments, and the current Talk, Send, or Stop action into one compact composer, with Photos, Videos, and Files behind one plus menu. Text, links, images, supported audio, and common documents received from the system Sharesheet become drafts for review, and unsupported, oversized, or excess items are shown before anything sends.

Search can reach Gateway-backed sessions beyond cached recents while Android is connected, and Threads can expand related parent and child work with descendant status. When the app is offline, search uses the active sessions already in its cache. Eligible capped assistant replies can now open inline so the ending, formatting, attachments, and full code remain available to read or copy, while unavailable, failed, or oversized results remain explicit instead of silently ending the answer.

The Wear OS companion uses its paired Android phone for the connection and stores no Gateway credentials on the Watch. It can show recent transcripts, send typed or dictated replies, stop a run, notify when a reply arrives, use continuous realtime Talk, and switch agents, sessions, and models when the phone advertises those controls. Supported phones also add Agent Pulse as a read-only view of bounded background work and pending attention, with no approval or mutation actions on the Watch.

macOS app

[macOS Quick Chat](https://docs.openclaw.ai/platforms/macos) opens from the menu bar or a global shortcut over the app already in use, with a picker for the five most recently updated conversations. It streams the reply in place, switches agents, accepts dictation, and selects a model and reasoning level. Screen Recording permission adds window or region capture, while Accessibility permission adds bounded text from the focused app and lets a final answer paste back where the user was working. Captured context clears after the send or when Quick Chat hides.

Full-window native chat now centers wide conversations, grows with longer drafts, searches loaded user and assistant messages with Command-F and Command-G, and puts Copy, Reply, Listen, and other message actions directly on the conversation. A failed queued send can be retried immediately, while a send whose outcome is uncertain remains under user control. Search stays within loaded visible message text and does not fetch older history or inspect hidden reasoning and tool payloads.

Native chat can rename, fork, pin, archive, mark read or unread, and organize conversations in parent-child trees and groups, with batch actions, inspection, and worktree-backed creation. A worktree request stops when the chosen agent, parent, worktree, or base reference cannot be honored.

The Dashboard returns to its remembered frame, Space, and eligible route through reconnects, and the status menu keeps live session cards, selection, and Gateway or device diagnostics stable and readable.

Linux app

The [Linux desktop companion](https://docs.openclaw.ai/platforms/linux) work now includes first-run setup, tray and service controls, an embedded Control UI, reconnect handling, deep links, autostart, window restoration, update notices, and native alerts for pending requests. Quick Chat switches agents, keeps one Gateway connection open, streams replies in the bar, and shows whether a send was accepted, failed, or is waiting for reconnection.

The build and publication path supports.deb and AppImage packages, although their availability as v2026.8.1 downloads has not yet been verified. The summon shortcut works on X11, Wayland keeps the tray entry, and approval decisions remain in the Dashboard or command line.

Progress and Presentation by Native App

On iOS, macOS, and Android, rich [progress cards](https://docs.openclaw.ai/tools/progress-card) can remain above the composer after a run and return through a relaunch or reconnect when the connected Gateway supports saved cards. Those clients also show a working Claw, elapsed time, and long-wait status while a turn runs, then add a duration and token recap when it completes successfully and unambiguously. Older Gateways can still show live fallback cards, but they cannot restore those cards after relaunch, and Android's fallback can sometimes retain a stale completed status.

[Assistant-created widgets](https://docs.openclaw.ai/web/dashboards) can render inline on iOS, Android, macOS, and Linux Quick Chat when the client advertises support, and an eligible connected Mac can also present one in its native Canvas panel. Linux Quick Chat remains text-only when it uses a custom Gateway TLS leaf pin. Expandable file-edit diffs cover a narrower set of clients and appear on iPhone, iPad, and Mac.

Runtime translations now reach Android's main workflows and named iPhone, iPad, Live Activity, Apple Watch, and Wear status surfaces, with a per-app language picker on Android. Identity-bound iOS, macOS, and Android connections follow the user's profile accent as it changes across devices, and voice surfaces on iOS, watchOS, macOS, and Android share the same phase-based waveform, using synthetic motion where live metering is unavailable.

## Models and Providers

Chat and the [Models page](https://docs.openclaw.ai/concepts/models) now open from the catalog OpenClaw already has, so choosing a model no longer waits for a full provider scan. Live discovery runs only when you open a model screen or explicitly refresh it, keeps the last useful list when a lookup fails, and `/model` can change only the current conversation or deliberately update one agent or the shared default.

Once a model is selected, OpenClaw keeps the request inside the intended provider and authorized account order, preserves the real order and outcome of streamed replies and tool calls, carries reasoning and context settings with the model and runtime, and reports plan windows, token use, context pressure, and estimated cost more clearly.

Finding and choosing models

Chat and the [Models page](https://docs.openclaw.ai/concepts/models) now start from the catalog OpenClaw already has, with supported providers looking for newer chat and text models when you open a picker or request a refresh. If that lookup fails, the built-in entries and last working list remain available.

A `/model` change can stay with the current conversation or deliberately apply to one agent or the shared default, with persistent changes requiring the right authority. Aliases and fallback keep the provider and account attached to the selected model.

The list shows models OpenClaw can identify, while the provider, account, region, endpoint, plan, limits, and pricing determine which ones you can use.

Provider accounts and sign-in

OpenClaw now keeps model requests inside the [provider accounts](https://docs.openclaw.ai/concepts/model-failover) and credential order you configured. If one account hits an authentication or quota cooldown, the next authorized account for that provider can take over without changing the selected provider or model, and the saved preference resumes when it recovers. Environment keys remain available when no explicit account list is configured.

OAuth registration stays with the setup conversation where it began, failed credential writes surface as failures, and a successful login applies only to the model route that authenticated. Tenant and custom-endpoint credentials stay on the account and origin they were configured for.

New GitHub Copilot device logins place the token in OpenClaw's protected local secret store by default and keep a reference in the auth profile. The store depends on state-directory permissions rather than encryption at rest, existing inline profiles are not migrated, and operators can still choose the prior plaintext mode explicitly.

Streaming Replies and Tool Calls

OpenClaw now distinguishes a complete [streamed reply](https://docs.openclaw.ai/concepts/streaming) from one that stopped partway through. On supported Responses paths, reasoning, text, tool output, and available usage remain in order; if a stream fails, valid work that already arrived is preserved, and OpenClaw retries or moves to an authorized fallback only when replay is safe. With no safe recovery path, the partial reply remains attached to the error.

Tool calls wait for a complete name and arguments before they can run, including large streamed arguments and calls whose provider item IDs change along the way. Unmanaged native OpenAI Responses conversations on the official endpoint with storage enabled can continue by sending only new input after the first turn, then recover with full history if that upstream continuation state expires.

Reasoning and context limits

[Reasoning settings](https://docs.openclaw.ai/concepts/context) now stay attached to the selected model and runtime when a conversation is restored or its authentication route is rebuilt. Native Codex supports Ultra for Sol and Terra and Max for Luna; embedded OpenClaw maps Ultra to the provider's highest supported effort and adds guidance for delegated work, which is a different behavior from native Codex Ultra.

Supported GPT and Claude routes expose larger context options. Normal GPT-5.5 and GPT-5.6 runs use a 272,000-token budget with an opt-in 922,000-token input window, and the Control UI can choose 200K or 1M for supported Claude 5 CLI conversations. These options remain limited to the routes, interfaces, and accounts that support them.

[Compaction](https://docs.openclaw.ai/concepts/compaction) now uses the latest trustworthy context count rather than accumulated cache billing or duplicated history, preserves tool output across supported Responses checkpoints, and falls back to full history when a stored checkpoint is rejected. Context limits are now configured per model, and Doctor can migrate supported provider-level settings tied to explicit model entries.

Usage, limits, and pricing

OpenClaw now separates subscription-plan information from estimated API cost. Chat can show plan windows, reset times, credits, and the account email attached to a snapshot, while completed iOS replies can show supported input, output, cache, cost, and context-pressure details. These figures are snapshots or estimates, not provider invoices, and in mixed API-key and subscription setups the account label identifies the plan snapshot rather than every run.

The Control UI adds a Profile page for lifetime activity recorded by OpenClaw, with [Usage](https://docs.openclaw.ai/concepts/usage-tracking) and Profile views grouped in the selected time zone, and plugin-initiated model calls now contribute to aggregate totals. OpenClaw cannot reconstruct activity it never recorded.

Supported failed or incomplete turns can retain the provider's token and cost data without being marked successful. Permanent authentication, model, media, and long-window quota failures stop retrying, while transient rate limits and retryable server errors keep their existing retry or authorized same-provider fallback behavior; Codex subscription runs do not silently switch to pay-as-you-go API keys.

## Automations and Scheduling

[Automations](https://docs.openclaw.ai/automation) now bring scheduled work together under one name across the agent, Control UI, command line, docs, and supported native apps, while existing Cron commands, settings, jobs, and schedule syntax continue to work.

History separates whether an automation ran, whether its result was delivered, and whether the whole request completed. Work genuinely missed during a restart or clock change can return without reviving completed or retired jobs, and connected tools keep only the authority captured when the automation was created or reauthorized, checked against current policy and availability each time it runs.

Creating and managing automations

[Automations](https://docs.openclaw.ai/automation/cron-jobs) is now the user-facing name in the agent tool, Control UI, command line, and docs, while `openclaw automations` offers the same command family as `openclaw cron`. The old command, `/cron` route, `cron.*` settings and RPC names, schedule expressions, identifiers, and stored jobs continue to work.

The Control UI is the fullest place to search, filter, create, clone, inspect, edit, run, pause, and remove automations, including advanced delivery and failure routing. New Quick Create and starter automations stay internal unless you explicitly choose an Announce summary and its destination. iOS and Android expose the fields and actions each client supports, Android changes require administrator scope while read-scoped connections remain inspection-only, and script automations remain visible but read-only on clients that cannot replace their payload.

Schedules and runs

An owner can turn the current conversation into a [`/loop`](https://docs.openclaw.ai/automation/cron-jobs) or eligible reminder that checks a small amount of recent context when it runs and returns one final answer to the same chat. It starts as a fresh run rather than continuing the original transcript, and work created without a conversation stays isolated.

Recurring schedules, one-time jobs, manual starts, queued work, restart catch-up, on-exit work, commands, and bounded scripts now share one configured capacity limit. Waiting work starts as room becomes available, while successful scripts can retain a small amount of state, notify a destination, wake the main conversation, or ask to be checked again later. Scripts still have time, tool-call, pacing, and state limits, and can be disabled entirely.

Force runs and edits no longer pull recurring work away from its natural schedule. Timezone-aware schedules skip local times that never occur, choose the first real occurrence when a local time repeats, and continue to respect explicit offsets after a restart.

Triggers and connected tools

An automation can now wait for a [condition or monitored event stream](https://docs.openclaw.ai/automation/cron-jobs) and run when something changes. Conditions can be created, filtered, edited, and inspected in the Control UI, are checked before they are saved, and record checks and matches without creating a run for every non-match. Stream schedules are created through the command line or agent and remain read-only in the Control UI, with bounded buffering, batching, and restart backoff. Triggers can still be disabled entirely, and condition intervals must be at least 30 seconds.

New or reauthorized Codex jobs can keep the app permissions and eligible connected-tool access they were created with across restarts. That captured authority is a ceiling checked on every run against current accounts, configuration, policy, approvals, and availability. Tools requiring someone present to approve them stay excluded, existing limits do not expand automatically, and some older jobs need a one-time edit or reauthorization before they can retain this access.

Heartbeats and email watchers

[Heartbeat schedules](https://docs.openclaw.ai/automation) are now managed as Automations, with failed work and alerts remaining visible and retryable and queued wakes surviving busy periods, handler replacement, and clock changes. Disabling Cron stops scheduled heartbeats while manual and event-driven wakes remain available. Existing installations using `HEARTBEAT.md` must run `openclaw doctor --fix` to migrate valid work because OpenClaw no longer reads that file at runtime.

[Gmail](https://docs.openclaw.ai/automation/cron-jobs) can split an accepted batch into one isolated run per message when its mapping opts in, filter Sent and Draft mail, and keep forwarding through watcher restarts without overlapping renewals or repeated restart loops. Ordinary custom mappings keep their existing behavior, and expired-OAuth renewal health is unchanged.

The bundled IMAP watcher lets authenticated new mail from an existing mailbox start a restricted reader agent without exposing an HTTP hook. It is disabled by default and inbound-only, requires sender allowlisting and authentication, and cannot send or modify mail. After three temporary admission failures, the message is recorded as skipped.

History, alerts, and delivery

[Automation history](https://docs.openclaw.ai/automation/cron-jobs) now treats running the work, delivering its result, and completing the whole request as separate facts. A job can execute successfully while the request still fails because requested delivery did not settle, and delivery is required unless best-effort is explicitly selected. Current-session work on a web-only Gateway counts the durable conversation result as completion when there is no external route, while an unavailable named route remains a delivery error without rerunning work that already completed. A successful delivery retry clears an earlier transient error, and intentional suppression is shown with its recorded reason in the command line and Control UI instead of looking like a failed delivery. Primary webhooks record accepted or failed outcomes before finalization, while secondary completion webhooks remain detached fan-out.

History can show duration, token totals, cache counters, condition checks and fires, delivery traces, cancellation or failure reasons, and direct Inspect links from eligible visible notifications. Inspect links require `gateway.publicOrigin`, historical rows may not have every optional counter, and condition activity belongs to the job's history rather than the global feed.

Failure alerts use configurable routes, thresholds, and cooldowns, with route-backed alerts defaulting to two consecutive failures and a one-hour cooldown. Recurring `cron` or `every` jobs disable themselves after ten consecutive execution failures and explain how to re-enable them, while delivery-only failures do not advance that streak and a successful run or manual re-enable resets it.

Automations After a Restart

[Restart recovery](https://docs.openclaw.ai/gateway/restart-recovery) now distinguishes work that was genuinely missed from work that already finished or no longer belongs to the current automation. Queued and deferred runs, rescheduled one-time reminders, schedule times missed during a restart or clock change, and interrupted one-shot jobs without a terminal result can return under normal catch-up pacing. Attempts with a durable terminal result do not replay, and completed slots, deleted or retired jobs, old schedules, and work from a replaced scheduler stay retired.

Current edits, self-removal, and rescheduling are preserved during startup, concurrent scheduler work no longer overwrites sibling jobs, and damaged older rows remain available for Doctor. Failed or skipped one-shot recovery remains disabled for inspection, while a successful job configured with `deleteAfterRun` is removed normally. Legacy running markers still remain interrupted when they cannot establish whether an outside side effect happened, so exactly-once execution in external systems remains outside the scheduler's recovery boundary.

## Browser and Computer Use

OpenClaw can now use [signed-in browser sessions](https://docs.openclaw.ai/tools/browser-login) through an isolated managed profile or the exact Chrome tabs you choose to share. On macOS, supported cookies can be imported locally or synced to a remote managed browser for an allowlist of sites you choose, while the official Chrome extension keeps live access scoped to shared tabs. Browser actions, downloads, and desktop input also stay attached to their intended tab, page state, and machine, with cancellation and timeouts reaching more of the local and remote work they own.

[Computer Use](https://docs.openclaw.ai/nodes/computer-use) can work with supported apps and windows on paired Macs and explicitly enabled Windows machines, and the Desktop panel can open the machine that owns a session. Control still requires the applicable pairing, policy, and operating-system permissions, view-only sessions reject input, and Linux control remains experimental.

Browser setup

On a Mac, you can explicitly copy compatible cookies from Chrome, Brave, Edge, or Chromium into an [isolated managed browser](https://docs.openclaw.ai/tools/browser) after approving Keychain or Touch ID access. If that browser runs on another OpenClaw machine, a separate opt-in sync can send cookies once or continuously for only the sites you allow. Neither path copies local storage or IndexedDB, and device-bound sessions can still ask you to sign in again.

For a browser you already have open, the Apps page now points to the official [Chrome extension](https://docs.openclaw.ai/tools/chrome-extension) and the command line can prepare its local connection. You decide which tabs to share, each shared tab can have its own copilot, and sending a page, supported document or thread, or selected text to the main conversation is a one-time handoff rather than continuing access to the rest of your browser.

Browsing and page actions

Navigation now returns a compact fresh view of the page for the next action, and snapshot references stay aligned with the content that appears in the final bounded snapshot. Multi-action batches pause after moving to a new document or closing a page so the next step can use fresh state, while new tabs can open in the background and the chosen locale, timezone, and device settings remain attached to the controlled page. Agents can also read bounded visible text, inspect recent network requests and uncaught page errors, and find matching controls in a snapshot without custom page evaluation. Page-controlled text and diagnostics remain untrusted, and existing-session profiles cannot collect the page-error log.

Command-line users can run a [repeatable JSON plan](https://docs.openclaw.ai/cli/browser) against one tab, keep ordered results, and choose whether a failure stops the batch or allows the remaining actions to finish. The conversation can show the active tab's title, URL, and latest thumbnail, then open the matching page in the Browser panel while keeping its session profile and machine attached. Cancelled or timed-out downloads stop without claiming a later request's file or publishing unwanted partial output, although a download already in its final save can still finish.

Computer Use

On a paired Mac, [Computer Use](https://docs.openclaw.ai/nodes/computer-use) can capture the desktop and work with supported apps, windows, and elements through pointer, keyboard, scroll, drag, and wait actions. Settings now shows the selected provider, Accessibility and Screen Recording state, and whether its supporting service is ready. Using those controls still requires pairing, the applicable command and tool policy, required arming, and the macOS permissions OpenClaw reports but cannot grant.

Explicitly enabled Windows machines now use the packaged Computer Use driver without a separately installed service. Linux uses the packaged route too and remains experimental, with complete live click-and-type behavior still unverified in this release. Codex Computer Use remains a separate macOS integration with its own readiness and recovery checks.

The Desktop panel can show the main OpenClaw machine, a Labs headless Linux desktop, or an explicitly enabled paired Mac, Windows, or Linux machine, and session buttons can open the computer that owns the work. Paired streaming is off by default, and view-only sessions keep keyboard, pointer, and clipboard input blocked.

Remote screens and devices

OpenClaw now keeps browser and computer work on the explicitly selected eligible [paired machine](https://docs.openclaw.ai/gateway/cloud-sessions). A disconnected, ambiguous, or ineligible selector returns an actionable error for that device, while unpinned automatic browser routing can still use the main machine when policy permits.

Browser uploads and downloads can move between the main machine and a remote Browser node without a shared filesystem, and completed downloads return as readable local files. Terminal uploads can place safely quoted remote paths into the active shell without pressing Enter. Transfer size and authorization limits remain in force, malformed screenshots and Canvas data stop before dispatch, and Android accessibility control remains an opt-in local foundation for third-party builds that a Gateway or agent cannot invoke yet.

Browser Targeting, Privacy, and Timeouts

Tab handles, page references, screenshots, and desktop actions now remain bound to the tab, page, display, request, and provider that created them. Stale or ambiguous state stops with an error, cancellation and timeouts reach more of the local and remote work they own, and relay reconnects restore only tabs that are still shared.

Remote browser connections are validated and remain pinned to their configured endpoint, connection credentials are redacted on the supported paths, and page-controlled text enters model context as untrusted input. [Browser](https://docs.openclaw.ai/tools/browser) and Canvas screenshots remain available to the inspecting agent but are no longer attached automatically to outbound replies. Cleanup stays limited to browsers and tabs OpenClaw owns, and older extension clients may need an upgrade or fresh pairing for the newer relay protections.

## Plugins and Integrations

Admins can now browse, search, install, enable, disable, and remove [plugins](https://docs.openclaw.ai/plugins/manage-plugins) from the Control UI, while the same hub can install curated ClawHub skills and add vetted [MCP connectors](https://docs.openclaw.ai/cli/mcp). Managed installs pause for source review where needed, roll failed changes back to a retryable state, and repair stale or incomplete records without throwing away healthy configuration. Plugin updates also keep work already in flight on the version it started with, then move later work to the replacement only after it loads successfully.

ClawHub installs carry the selected publisher, version, scan state, and source across desktop and mobile, MCP servers recover independently when a connection or catalog changes, and plugin authors get typed Gateway and SDK contracts for building against OpenClaw. Vendor-neutral Agent Plugins can bring skills and supported MCP servers together with scoped storage, giving integrations a clearer path from package to running system.

Installing and managing plugins

Admins can now browse and search [installed plugins](https://docs.openclaw.ai/plugins/manage-plugins) in the Control UI, see what each one provides, enable or disable it, remove external plugins, install curated ClawHub results, and add vetted MCP connectors. Read-only operators can inspect the same inventory, while advanced sources, updates, and configuration that the web form cannot safely represent remain available through the command line.

The first install from an arbitrary package, repository, archive, local path, or marketplace source stops for explicit review. A plugin that still needs setup can stay disabled, and a failed managed install rolls partial changes back so it can be retried normally. Repair can recover stale or incomplete install generations while preserving healthy configuration, with integrity or version drift still requiring review.

Plugin lists and diagnostics now distinguish disabled plugins, discovery or validation failures, active runtime failures, and background-service failures. Use `plugins doctor` for local discovery and configuration checks, and `openclaw health` for the plugin and service state of the running system. Some installs and removals still require a restart before the change becomes active.

ClawHub, Claws, and sharing skills

[ClawHub](https://docs.openclaw.ai/tools/skills) now carries the selected publisher, version, scan result, and exact source through review and installation, including when two skills share a name. Before a skill or plugin is installed, its ClawHub Security Audit shows the exact release, a Safe, Review, or Blocked result, ClawHub's overview, and the audit link. A Review result gives you that context and continues through the ordinary confirmation instead of a second risk gate, while a Blocked release still cannot be installed. Mac, iPhone, iPad, and Android users use the same publisher, version, and audit contract, while external skills.sh results keep their pinned source identity and are clearly marked as outside ClawHub scanning.

Skill updates protect local and concurrent edits unless an operator explicitly forces the overwrite. Direct downloads verify a declared digest and inspect the complete archive within the supported size limit, and older tracked installs without fingerprints need one forced update to establish that baseline.

[Experimental Claws](https://docs.openclaw.ai/cli/claws) can package an agent with managed workspace files, skills, plugins, MCP servers, and scheduled work. You preview the exact plan before applying it, updates and removal act on resources the Claw owns, and shared resources remain in place unless you deliberately choose conflict-aware cleanup. Recreating a Claw with the same ID now waits until the old Claw's cleanup is complete, so interrupted removal remains fenced and retryable instead of deleting replacement state. Claws remain behind `OPENCLAW_EXPERIMENTAL_CLAWS=1`, uncertain outside actions can leave visible partial state that needs a fresh plan, and the package does not carry credentials, providers, bindings, arbitrary local paths, executable configuration, sessions, or host state it does not own.

Loading and updating plugins

[Plugin updates](https://docs.openclaw.ai/plugins/architecture) now preserve one runtime generation for work already underway. Accepted messages, completions, and workers finish with the plugin version they started with, and later work moves to the replacement only after it has loaded successfully. If a live reload fails, OpenClaw restores the last active commands, providers, hooks, memory, and other registrations.

OpenClaw also reuses prepared plugin metadata and runtimes across turns instead of rebuilding the same setup each time, while health shows failed activation, cleanup, or background services directly. A known plugin-owned failure can be quarantined without taking healthy plugins or all of OpenClaw offline, while invalid configuration, failed migrations, ambiguous ownership, and unverifiable state still stop activation.

Context-engine plugins remain selected on fresh turns and can advance durable state through long sessions by applying limits to the accepted turn instead of all accumulated history. Existing v1 engines keep their full-history contract until they adopt the newer interface, and a single accepted turn above 8 MiB or 20,000 events still stops.

MCP servers and apps

[MCP servers](https://docs.openclaw.ai/cli/mcp) can now recover their connection and catalog after late startup, transport loss, a server restart, or a changed tool list without restarting OpenClaw or taking healthy servers down with them. Tool results retain structured data, screenshots, audio, resources, recovery guidance, and real error state. A call that first discovers an expired stateful session still fails once without replay because it may already have changed something.

Local MCP sign-in can finish in the browser, save and verify the credential, and resume a newly started authorization after a process restart. Shared operator sign-in remains the default, while supported HTTP MCP servers can opt into per-person OAuth that keeps each credential attached to the trusted channel, bot account, and sender. Remote and headless operators keep the manual code path, and this first per-person mode does not add private sign-in delivery, automatic turn resumption, or Control UI account management.

MCP Apps remain opt-in and can show supported interactive server interfaces after the required configuration and restart. They extend trust to UI code supplied by the server, reconstructed conversation views stay read-only, and app context enters the next turn as untrusted input. Headless nodes can publish request-response MCP tools into Code Mode, while OAuth, streaming, notifications, sampling, and mobile publication remain outside this first node-hosted version.

Building plugins and integrations

Developers [building a Gateway client](https://docs.openclaw.ai/gateway/protocol) or embedding OpenClaw now have typed protocol schemas, runtime validation, authentication, reconnect, readiness, timeout, and browser or Node entry-point guidance. The Gateway protocol and reference client are prepared as calendar-versioned npm packages and become installable when the release train publishes them.

[Plugin authors](https://docs.openclaw.ai/plugins/building-plugins) also get focused contracts for requester-aware hooks, channel setup, CLI backends, bounded provider streams, read-only secret references, and browser meeting adapters. Hook policy remains underneath channel admission, sandboxing, approvals, owner-only tools, and other host policy, and the timeout cleanup for Codex hook relays applies to POSIX hosts rather than Windows.

The contract cleanup removes retired July and August SDK paths and replaces the `deactivate` alias with `gateway_stop`, while the beta.5 session-store bridge remains available through October 12, 2026. Clients using the v2026.7.2 beta question, worker, or session-catalog shapes need to move to the renamed and flattened contracts. Custom `agents.defaults.cliBackends` commands, arguments, environment, aliases, and parsers now belong in a backend plugin whose executable is available to the OpenClaw service.

**Maintenance**

Plugin Packages and Host Compatibility

OpenClaw can now install vendor-neutral [Agent Plugins](https://docs.openclaw.ai/plugins/bundles) from directories, archives, or Git sources, load their immediate-child skills and valid stdio, HTTP, or SSE MCP servers, and give them scoped bundle and persistent data paths. The OpenClaw extension can add activation hints, while providers, channels, configuration schemas, and runtime entry points stay outside this portable bundle contract. An invalid MCP entry is skipped without blocking valid siblings.

Cohere, Meta, BytePlus, ComfyUI, OpenCode, Voyage, Vydra, Volcengine, Mistral, NovitaAI, Teams meetings, and Zoom meetings now ship as separately installed [official packages](https://docs.openclaw.ai/plugins/plugin-inventory). New setups install the relevant package and restart OpenClaw, and an existing enabled setup relocates when the external artifact is available. OpenCode Go remains bundled because its external placeholder was not usable.

Plugin loading now handles the specific npm 10 through 12 metadata and lock behavior, direct and peer OpenClaw dependencies, packed host-runtime imports, and concurrent Node ESM cases that had prevented successful installs from activating. Canvas is now focused on the macOS presenter and session-board A2UI path, with its standalone workspace, eval and snapshot surfaces, native push and reset commands, and iOS, Android, and Linux clients removed. Dashboard and A2UI actions remain explicitly granted and sandboxed.

## Security and Privacy

Sensitive work now carries more of its authority with it. [Approvals](https://docs.openclaw.ai/tools/exec-approvals) stay attached to the exact request, command, session, and person that received them, removing or pairing a device again retires its old access, and [protected credentials](https://docs.openclaw.ai/gateway/secrets) can reach supported destinations without entering model-visible text. Sandboxes, network requests, browser actions, and plugin installs also recheck the workspace, destination, document, publisher, version, or artifact they depend on, so stale or mismatched authority stops or asks again instead of being reused.

Approvals and permissions

An [approval request](https://docs.openclaw.ai/tools/exec-approvals) now has one durable record shared by authorized browser and supported mobile surfaces. The first valid answer settles it, reconnecting cannot revive a completed request, abandoned requests are cancelled, and aborting a run clears the approvals it left pending. Operators can also opt in to installed Control UI PWA approval alerts that open the authenticated request, with the subscribed device, person, current role and scopes, preferences, and request visibility checked again before delivery. Resolved or expired requests replace stale actionable alerts, while optional agent and task alerts remain off by default.

Recurring automations can now show their standing grants in the approvals page and CLI, including the owning automation, exact command, use count, and current state. Revoking an active grant takes effect at the next spawn boundary so the next occurrence asks again, and managed deployments can set the default lifetime used for future grants. Reusable command [permission](https://docs.openclaw.ai/gateway/permission-modes) can still bind to exact arguments and a working directory, while script-backed commands recheck the bytes that were reviewed before they run. The binding covers the reviewed command and script bytes, while interpreters and changing dependencies can introduce separate behavior; opaque wrappers and commands that can launch something else may ask again.

Each session can choose read-only, guarded, workspace, or full access and override MCP servers, skills, or web search where the client exposes those controls, with full access reserved for administrators. Per-turn exec restrictions can tighten that session policy but cannot loosen it, and Doctor provides a migration path for the older persistent exec fields. Scheduled and delegated work retains its originating policy, and an uncertain result from another machine is reported as unknown instead of being retried on a guess.

Per-session controls are nonretroactive, so existing sessions without a permission mode keep the previous global posture. Opt-in roles limit collaboration inside one trusted OpenClaw installation rather than creating isolation between hostile tenants.

People, devices, and pairing

[Pairing](https://docs.openclaw.ai/gateway/pairing) authority now lives on the device record. Removing or pairing a device again retires its old connection and worker access, non-admin device tokens can manage only their own pairing, macOS and Android can review pairing state, and administrators can create a short-lived one-paste command for joining a machine.

Automatic browser enrollment behind a trusted proxy remains off until enabled and stays within configured role and access limits. Verified proxy or Tailscale identity applies only to the current connection instead of rewriting durable pairing. The separate SSH identity check for private-network machines is on by default and follows normal OpenSSH HostName rules, so operators who want manual-only pairing must disable it and leave CIDR auto-approval unset.

Participant, session, agent, and requester identity now travels with more of the work for attribution without widening access. Managed GitHub identities apply to local command-line and API work and author metadata, while Git transport, sandboxes, remote machines, and cloud workers continue to use their own identity paths.

Secrets and private data

The new team-scoped local [Secret Store](https://docs.openclaw.ai/gateway/secrets) separates Protected values from Agent-readable environment values. Supported masked requests, Vault or [1Password](https://docs.openclaw.ai/gateway/1password) references, and destination-bound substitution can keep a protected credential out of plaintext configuration and model-visible text while placing it into an approved Gateway-hosted HTTPS request. Masked credential requests on the web, iOS, and Android now preserve the exact entered value and operator-edited destination, refresh affected providers after the value is saved, and close the request and its protected connection with the run that owns them. Agent-readable values are a separate grant for Gateway-hosted commands and can still be printed or transmitted by the command that receives them.

Changing a Control UI Gateway URL to a different credential scope now clears the previous endpoint's password and bootstrap credentials before connecting, while credentials explicitly supplied for the destination still take precedence. A query-only scope change can retain the origin-scoped token but requires the password to be entered again.

Secret Store values are not encrypted at rest and depend on the filesystem permissions of OpenClaw's state directory. Destination-bound substitution applies only to Gateway-hosted HTTPS commands whose subprocess honors its proxy settings. Raw sockets, containers, remote nodes, provider-native harnesses, plain HTTP, and WebSockets stay outside that path.

Common credential and signed-parameter patterns are now redacted across covered logs, diagnostics, agent errors, and Control UI failures, while chat history removes inline media bytes, local paths, private shell rows, copied prompt context, and failed-delivery payloads on the covered paths. Extra feature statistics, Android installed-app details, and iOS Health summaries require explicit choices, with Health behind two disabled-by-default gates. Update checks remain on unless disabled, while approximate Activity location is enabled by default for routable addresses and may download its local city database on first use.

Sandbox and file access

Contributor-controlled code is now prepared inside the designated untrusted-code [sandbox](https://docs.openclaw.ai/gateway/sandboxing), and managed worktrees suppress repository Git hooks unless an administrator deliberately runs the separate setup script. Repositories that relied on implicit hooks will need to move that setup into the explicit path.

Sandbox identity now includes the workspace that owns the run. Newly created guest sessions that require a sandbox receive a separate identity for each authenticated guest and can share a workspace only read-only, while worker sessions on another machine can opt into per-session containers. Direct execution remains the default, and the same per-guest boundary is not established for child sessions they create.

[File checks](https://docs.openclaw.ai/gateway/security/secure-file-operations) catch more attempts to escape through the named root, denied directories, oversized reads, and POSIX symlink parents. Symlink containment is checked before the filesystem operation rather than atomically beneath the approved root, leaving a remaining window for a path to change between the check and use.

Network Access and Untrusted Content

[Network policy](https://docs.openclaw.ai/gateway/security) now blocks unspecified and local-use NAT64 targets by default, validates guarded redirects and no-auth browser origins, and stops telemetry when its configured proxy is invalid instead of bypassing it. Private automation webhook destinations require an exact-host exception or a broader private-network switch, with the broader setting widening trust across every configured cron webhook.

Text returned by search, fetch, MCP, plugins, Browser, and other network-backed tools is bounded, normalized, and marked as untrusted external content before the model sees it. This makes the source and boundary explicit, while the model can still be influenced by hostile material it reads.

Terminal and CSV output neutralize covered control-sequence and formula injection forms, configuration rejects prototype-polluting paths, and browser references, executable waits, navigation, and MCP App grants are rechecked against the document and live authority that produced them. Browser navigation enforcement covers selected-page document traffic during managed actions and a bounded grace period, leaving popups, Service Workers, background requests, some redirects, and remote backends outside that boundary.

Plugin Permissions and Installation Checks

Managed external plugin installs now show one [capability review](https://docs.openclaw.ai/plugins/plugin-permission-requests) bound to the artifact being installed and ask again when an update requests more authority. Skill security verdicts stay attached to the exact publisher and version, ClawHub GitHub installs require a full commit SHA instead of a mutable branch or tag, and managed Homebrew or NodeSource installers stop when a response fails, is empty, redirects, or lacks a shebang.

The capability prompt applies to managed external installs. Bundled plugins skip it, already-enabled legacy plugins keep their existing access, and bundled execution retains named compatibility exceptions. The review shows what a plugin is asking to do, while authenticity and code safety continue to depend on [artifact integrity](https://docs.openclaw.ai/gateway/security/dependency-locking), registry identity, and code review. A full commit SHA pins the downloaded archive bytes while source metadata still depends on the resolver, and the installer response check only confirms that the download looks like a script.

## Quality-of-Life Improvements

Everyday work in OpenClaw now takes less effort to find, follow, move, and protect. [Past conversations](https://docs.openclaw.ai/concepts/session-search) are easier to return to, long jobs keep useful progress visible, portable snapshots can be checked before they are needed, and eligible work can run on a [cloud worker](https://docs.openclaw.ai/gateway/cloud-workers) or [paired computer](https://docs.openclaw.ai/gateway/cloud-sessions), with cloud sessions later reclaimed to the main machine. Voice, video, meeting capture, agent tools, keyboard access, maintained translations, interface polish, and documentation also pick up changes that make the product easier to use across ordinary work.

Past Conversations and Long-Running Work

[Past conversations](https://docs.openclaw.ai/concepts/session-search) and long-running work are easier to find and follow. The session catalog groups and opens Codex, Claude Code, OpenCode, and Pi work from the main OpenClaw computer or an eligible paired one, and each session can carry one of eight colors across the Control UI, macOS, iOS, and Android. An eligible Claude Code continuation also brings its chosen color and renamed title into OpenClaw without replacing later edits. Durable [progress cards](https://docs.openclaw.ai/tools/progress-card) survive reloads and reconnects, and background-task history is available on the web, iOS, and Android. An optional observer can summarize a conversation, answer questions about it, show its timeline, and alert an operator when attention is needed.

Resume support depends on the runtime that owns the session. OpenCode and Pi catalogs are view-only, paired-computer actions need an opted-in capable host and an eligible session, and external transcripts remain with their original runtime. The observer can be disabled and requires an available utility model.

Stored Data and Backups

Sessions and transcripts, selected device and authentication records, meeting capture, and runtime journals now use SQLite-backed stores, and [portable snapshots](https://docs.openclaw.ai/cli/backup) can be created, verified, and restored through the same toolset. This gives backup and recovery a checkable path before an incident.

Some legacy stores require the owning process to be stopped before `openclaw doctor --fix` can migrate them. Pending pairing requests and bootstrap codes are not imported, the macOS tunnel migration cannot be read by older JSON-only builds, and restore refuses to write over an existing target.

Remote computers and devices

Work no longer has to stay on the main machine running OpenClaw. A configured [cloud worker](https://docs.openclaw.ai/gateway/cloud-workers) can start a session in a selected repository and later return it to the main machine, and the Control UI now identifies the service and profile behind a placement when that identity can be resolved safely. Crabbox profiles can leave machine sizing to the service or choose it for one session. An explicitly opted-in [paired computer](https://docs.openclaw.ai/gateway/cloud-sessions), including an eligible native Mac, can run a complete turn using a worker bundle verified and supplied by OpenClaw rather than whatever code happens to be installed there.

Those are two different paths with different requirements. Cloud workers need a configured profile and the OpenClaw runtime, while paired computers need compatible versions, consent, available capacity, and support for the requested commands. The portable worker bundle does not include the destination machine's native terminal module, so work that depends on a truly interactive terminal still has a real boundary.

Voice, meetings, and media

[Talk](https://docs.openclaw.ai/nodes/talk) can use GPT-Live and GA Realtime voice through supported direct-browser and Gateway-relay paths, including eligible ChatGPT or Codex sign-ins. The routes are not interchangeable though, because credentials and transports vary across clients, Android relay remains gated, and Azure configurations are excluded from the ChatGPT OAuth relay path.

Supported OpenAI and Gemini Live calls can add video, remember whether you use the camera, and switch cameras without restarting voice. Those controls only appear on supported browser and provider transports, permission and capture stay on the device, and an unsupported or fallback relay can omit or reject video.

Enabled [Google Meet, Microsoft Teams, and Zoom bots](https://docs.openclaw.ai/plugins/meeting-plugins) can also retain speaker-attributed transcripts and summaries in SQLite. Google Meet's bounded live-caption buffer is a separate path from that durable archive, and meeting retention can still be disabled globally.

Code Mode and agent tools

[Code Mode](https://docs.openclaw.ai/tools/code-mode) remains experimental and off by default. Its Labs switch selects automatic use for preferred models, while Agent Defaults can inherit or override that choice for one exact model. When active, Code Mode can treat authorized tools like ordinary asynchronous functions, letting an agent combine trusted results from conversations, files, and sessions in one program or run independent calls together. This is the final interface rather than another layer beside the old one, so the previous `tools` object, `ALL_TOOLS`, exact-ID calls, and raw call envelopes are gone. What a program can compose still stops at the tools it is authorized to use and the structured results those tools declare.

[Tool Search](https://docs.openclaw.ai/tools) also does a better job of turning a natural request into a discoverable capability, can search several capability groups in one structured request, and now exposes existing session archive and pin actions. Policy can still hide tools and a request with no valid answer can return nothing, while existing single-query request and response shapes continue to work.

Accessibility and language support

Keyboard users can open plugin details and select Usage sessions again. The 20 maintained non-English [Control UI](https://docs.openclaw.ai/web/control-ui) catalogs also include refreshed text for prompts, devices, activity, catalogs, and other expanded surfaces. These catalog updates keep the existing language set aligned with the current interface; they do not add languages or change application logic.

Android also has an experimental `mobile_ui` path that lets an authorized agent observe and interact with apps on a supported paired device. It is owner-only, off by default, limited to third-party builds, unavailable through Gateway HTTP and Play builds, and requires both dangerous commands to be armed explicitly.

Interface polish and compatibility

Startup and several messaging paths now skip unnecessary work, while smaller fixes across onboarding, Tasks, Worktrees, Activity, dashboards, generated titles, durations, phone numbers, and themes make [familiar screens](https://docs.openclaw.ai/web/control-ui) easier to read and use.

The optional [Control UI lobster](https://docs.openclaw.ai/web/lobster) now reacts to status changes and adds seasonal or rare variants, visitors, collection rewards, and controls to dismiss one visit or disable visits. These additions are cosmetic, many appearances remain rare or session-seeded, reduced-motion preferences are preserved, and related CLI flourishes stay inside interactive use so automated output is unchanged.

Documentation

Setup, migration, recovery, and feature guidance now covers [cloud workers](https://docs.openclaw.ai/gateway/cloud-workers), [meetings and media](https://docs.openclaw.ai/plugins/meeting-plugins), [Code Mode](https://docs.openclaw.ai/tools/code-mode), Swarm, portals, sandboxes, local speech, [SQLite migrations](https://docs.openclaw.ai/reference/database-schemas), [backups](https://docs.openclaw.ai/install/backups), and downgrade recovery more clearly. Mobile readers get better top-level links, and the Release and CI pages lose a redundant navigation layer. These are documentation and QA updates; runtime behaviour continues to follow the referenced product and platform contracts.

Two cloud-worker details remain out of sync. The Cloud Workers settings guide overstates profile information shown for providers other than Crabbox, and the Daytona guide says `settings.class` can be omitted even though profile validation still requires it, so Daytona profiles should keep the class explicit until the guide and product contract agree.

## Other Bug Fixes

OpenClaw now preserves completed Codex delegation results through the covered handoffs, keeps accepted user turns from being stored twice, stops cancelled commands before they start, and retains Canvas widget identity and pin state after reload. The rest of this section covers scoped fixes across browser Talk, Copilot and xAI replay, [Doctor](https://docs.openclaw.ai/cli/doctor) recovery, plugin upgrades, meeting audio, and the [terminal app](https://docs.openclaw.ai/web/tui).

Agent Work and Handoffs

In the repaired [Codex delegation](https://docs.openclaw.ai/tools/subagents) and `sessions_yield` paths, completed subagent results now survive cleanup and handoff, yielded jobs launch once, and the parent resumes after fan-out finishes.

Conversations, history, and stored data

One accepted user turn now stays one turn across the repaired retry and restart paths instead of being written twice. `/new` and `/reset` also preserve the underlying transcript position while clearing the visible conversation, so resetting what you see does not lose OpenClaw's place in the [saved history](https://docs.openclaw.ai/concepts/session).

Agent tools and code execution

[Code Mode](https://docs.openclaw.ai/tools/code-mode) can keep an eligible task moving when it fails before taking action or while discovering tools and skills, and nested tool calls now finish or cancel cleanly instead of hanging. Once a write may have happened, recovery is limited to checking what changed rather than replaying an uncertain action, while cancellation, policy denial, and other final outcomes still stop the task.

Processes and background commands

Cancelling a queued command now keeps it from starting, cancellation during startup reaches the process once it exists, and an explicit replacement retires the command it replaced without killing ordinary work that happens to be running at the same time. Commands already running in the background keep their existing lifetime.

[Process output](https://docs.openclaw.ai/tools/exec) also stays in the order OpenClaw observed it, completion remains attached to the exact process that finished, and polling says when earlier output was omitted. The full history remains available through paged process logs rather than one response that can grow without bound.

Automations and task boards

[Workboard](https://docs.openclaw.ai/plugins/workboard) now keeps an accepted worker attached to its card, rolls back a failed operation without overwriting someone else's edits, and reconnects launches interrupted by a restart. If OpenClaw does not have a complete view of the running workers, it waits instead of guessing whether one still belongs to the card, and stale launch attempts remain blocked.

Web and dashboard interfaces

[Canvas](https://docs.openclaw.ai/platforms/mac/canvas) now keeps generated widgets distinct when their names collide, remembers which widget was pinned after reload, and shows a bounded error when pinning fails instead of making the action disappear. When a stored widget identity is invalid or an occupied name is ambiguous, Canvas still refuses to guess which widget you meant.

Terminal App

The [terminal app](https://docs.openclaw.ai/web/tui) now stays on the conversation you most recently selected during rapid switching and preserves the active answer and chosen tool visibility when you return to it. It retries one temporary live-update failure, while a second failure remains visible and full verbosity continues to show stored tool output.

Voice and Talk

Browser [Realtime Talk](https://docs.openclaw.ai/nodes/talk) now limits stalled microphone uploads, queued playback, replacement work, and abandoned voice sessions instead of letting them grow without bound. A malformed audio frame can be dropped without ending healthy playback, while Google Live ends the current voice session when it cannot safely cancel only the response that overflowed.

Models and providers

Specific [GitHub Copilot](https://docs.openclaw.ai/plugins/reference/github-copilot) and xAI replay failures now recover without resetting the conversation. Copilot preserves valid same-run reasoning through active tool calls, and affected post-compaction or encrypted-reasoning failures receive one bounded sanitized retry under the matching transport, model family, or xAI decrypt signature.

Speech and media providers

Across the affected shared and OpenAI [transcription](https://docs.openclaw.ai/nodes/audio) paths, repeated short-lived connections now back off and stop at the configured retry limit, OpenAI turns stay in order, more eligible final words survive microphone close, and a large backlog keeps the newest audio so the session remains responsive.

Local CLI text-to-speech now caps output memory, handles a broken audio stream safely, and preserves a valid output file when only unused stdout fails. Output metadata from Local CLI and ElevenLabs also reports the audio format that was actually produced.

Command line and diagnostics

[Doctor](https://docs.openclaw.ai/cli/doctor) now stops a stale build before repair, safely migrates the covered legacy agent databases without following unrelated state, and gives operators a concrete recovery path when the shared database is corrupt. Corrupt shared state is diagnosed and left unchanged for manual restoration or repair.

Security and permissions

Doctor's legacy [authentication migration](https://docs.openclaw.ai/gateway/authentication) now preserves complete credentials, credentials already stored in SQLite, and the selected ChatGPT account across the covered legacy-to-SQLite migrations. Ambiguous ownership, unreadable files, and unverifiable credentials continue to stop the migration.

Plugins and installation

[Plugin upgrades](https://docs.openclaw.ai/plugins/manage-plugins) now keep canonical SQLite install and state records when conflicting legacy data is provably stale, archive the old file for recovery, and allow startup to continue. Newer or ambiguous legacy state and archive failures remain blocking so Doctor can retry without discarding either copy.

Messaging and calls

Affected [Google Meet and Teams sessions](https://docs.openclaw.ai/plugins/meeting-plugins) now wait for the local audio bridge to stop before teardown completes. Google Meet also rejects malformed node-control requests before dispatch and keeps local audio diagnostics bounded and readable.

Documentation

Documentation links now reach their intended external destinations and cross-page headings, while contributor attribution follows renamed accounts correctly. The [external-link checker](https://docs.openclaw.ai/ci) reports future drift on weekly or manual runs without blocking pull requests.

## Maintainer and Internal Changes

Another 6,364 changes in this release primarily affect the people who build and maintain OpenClaw. They cover [release and CI work](https://docs.openclaw.ai/reference/RELEASING), tests, internal refactors, documentation maintenance, and narrow fixes that sit outside the user-facing product sections above.

All 6,364 Maintainer and Internal Changes

This completes the record for all 17,675 analyzed PRs and commits in v2026.8.1. The list contains 27 improvements or features, 251 bug, provider, and security fixes, 70 documentation changes, and 6,016 internal maintenance changes, preserving the original PR and commit titles below.

**Maintenance**

*Version note: The package published as `2026.9.1-beta.1` was incorrectly versioned and corresponds to `2026.8.1-beta.4`; it is not newer than stable `2026.8.1`.*
