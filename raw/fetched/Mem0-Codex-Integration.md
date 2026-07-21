---
title: "Mem0 × Codex Integration"
description: Mem0 官方 Codex 整合文件：plugin marketplace 與 direct MCP 兩種安裝、config.toml 設定、9 個 MCP 工具與 hooks 對照與衝突排除
created: 2026-07-21
updated: 2026-07-21
source: "https://docs.mem0.ai/integrations/codex"
published:
tags:
  - mcp
  - claude-code
  - coding-agent
  - memory
---

Add persistent memory to [**OpenAI Codex**](https://openai.com/index/codex/) with the Mem0 plugin. Codex forgets everything between tasks. This plugin fixes that by connecting to Mem0’s cloud memory layer via MCP, automatically capturing learnings at key lifecycle points, and retrieving relevant context before every response.

## Prerequisites

Before setting up Mem0 with Codex, ensure you have:

1. A Mem0 Platform account and API key:
	- [Sign up at app.mem0.ai](https://app.mem0.ai/?utm_source=oss&utm_medium=integration-codex)
		- [Get your API key](https://app.mem0.ai/dashboard/api-keys?utm_source=oss&utm_medium=integration-codex) (starts with `m0-`)
2. OpenAI Codex access
3. Your API key added to your shell profile (persists across sessions):

```shellscript
echo 'export MEM0_API_KEY="m0-your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

```shellscript
echo 'export MEM0_API_KEY="m0-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

## Installation

### Option A: Plugin Marketplace (Recommended)

Install the full plugin including MCP server, lifecycle hooks, and SDK skill.

1. Add the Mem0 marketplace:
	```shellscript
	codex plugin marketplace add mem0ai/mem0
	```
2. Install the plugin:
	```shellscript
	codex plugin add mem0@mem0-plugins
	```
	Or, in the app: restart Codex, open the Plugin Directory, browse the **Mem0 Plugins** marketplace, and install **Mem0**.

Step 1 is required for the app UI. Mem0 isn’t in OpenAI’s curated directory yet, so **without `codex plugin marketplace add`, Mem0 won’t appear in the Codex app’s Plugin Directory**: searching for it returns nothing. Adding the marketplace surfaces it (under **Created by you**) and makes it installable.

Do not combine with Option B. The plugin manifest auto-registers the `mem0` MCP server, so adding both will create a duplicate registration.

### Option B: Direct MCP

The fastest way to connect Codex to Mem0 needs no plugin or marketplace. Add the MCP server with a single command:

```shellscript
codex mcp add mem0 --url https://mcp.mem0.ai/mcp/ --bearer-token-env-var MEM0_API_KEY
```

Or add it manually to `~/.codex/config.toml`:

```toml
[mcp_servers.mem0]
url = "https://mcp.mem0.ai/mcp/"
bearer_token_env_var = "MEM0_API_KEY"
```

Make sure `MEM0_API_KEY` is exported in the shell you launch Codex from, then restart Codex.

This gives you the MCP tools but not the lifecycle hooks or SDK skill.

### Managing the Plugin

```shellscript
codex plugin marketplace upgrade               # pull latest plugin versions
codex plugin remove mem0@mem0-plugins          # uninstall the plugin (keeps the marketplace)
codex plugin marketplace remove mem0-plugins   # unregister the marketplace entirely
```

To update, run `codex plugin marketplace upgrade` to pull the latest from the Mem0 repo.

After either option, start a new Codex task and ask: *“List my mem0 entities”* or *“Search my memories for hello”*. If the `mem0` tools appear and respond, you’re all set.

## What’s Included

| Component | Plugin Install | MCP Only |
| --- | --- | --- |
| MCP Server (9 memory tools) | Yes | Yes |
| Lifecycle Hooks | Yes | No |
| Mem0 SDK Skill | Yes | No |

## Available MCP Tools

Once installed, the following tools are available in every Codex session:

| Tool | Description |
| --- | --- |
| `add_memory` | Save text or conversation history for a user/agent |
| `search_memories` | Semantic search across memories with filters |
| `get_memories` | List memories with filters and pagination |
| `get_memory` | Retrieve a specific memory by ID |
| `update_memory` | Overwrite a memory’s text by ID |
| `delete_memory` | Delete a single memory by ID |
| `delete_all_memories` | Bulk delete all memories in scope |
| `delete_entities` | Delete a user/agent/app/run entity and its memories |
| `list_entities` | List users/agents/apps/runs stored in Mem0 |

## Lifecycle Hooks

When installed via the plugin marketplace, Mem0 hooks into Codex’s lifecycle to automatically manage memory:

| Hook | Event | What it does |
| --- | --- | --- |
| **Session start** | `SessionStart` | Loads prior memories and displays status banner |
| **User prompt** | `UserPromptSubmit` | Searches relevant memories before each message |
| **Pre-tool (3 handlers)** | `PreToolUse` | Blocks MEMORY.md writes; enforces `user_id` / `app_id` on mem0 tool calls; scans files being read for relevant memory context |
| **Post-tool** | `PostToolUse` | Tracks stats, scans bash errors for related memories |
| **Stop** | `Stop` | Stores a session summary at the end of every assistant turn (not just at session end) |
| **Pre-compact** | `PreCompact` | Stores a summary before the context is compacted |

What you type is stored as yours. What Codex produces — session summaries and compaction summaries — is stored as the assistant’s, so its suggestions never become your stated preferences.

## Example Workflow

```text
# Task 1: Setting up a new service
You: Create a REST API for the notifications service using Express and TypeScript.

# Codex searches memories, finds your preferences from prior tasks.
# Mem0 stores what you said as yours:
#   - Your preference: "Prefers explicit error types over generic catch-all"
# ...and what Codex did as the assistant's, in the session summary:
#   - Decision: "Notifications service uses Express + TypeScript + Zod validation"
#   - Convention: "All API routes follow /api/v1/{resource} pattern"

# Task 2 (days later): Extending the service
You: Add WebSocket support for real-time notification delivery.

# Codex searches memories, retrieves the architecture decisions and conventions.
# Follows the same patterns established in the first task.
```

## Troubleshooting

- **“Connection failed”**: Verify `MEM0_API_KEY` is set: `echo $MEM0_API_KEY`
- **No tools appearing**: Restart your Codex session after installation
- **Duplicate `mem0` MCP / “tool collision” errors**: You combined Option A with Option B. Remove the `[mcp_servers.mem0]` block from `~/.codex/config.toml`; the plugin registers it automatically
- **Hooks not firing**: Ensure the plugin is installed via the marketplace (Option A). MCP-only installs do not include hooks

## Mem0 MCP Setup

Detailed MCP configuration for all clients

![](https://mintcdn.com/mem0/QK-8_hblyHgAr7vt/images/provider-icons/anthropic.svg?fit=max&auto=format&n=QK-8_hblyHgAr7vt&q=85&s=d2a2af9f60f53e9f21d741fe237af0f5)

## Claude Code Integration

Add Mem0 memory to Claude Code workflows

**Using Mem0?** [Star us on GitHub](https://github.com/mem0ai/mem0) to help more developers discover memory for AI apps.