---
title: "Mem0 × Claude Code Integration"
description: Mem0 官方 Claude Code 整合文件：plugin marketplace／MCP-only／手動 .mcp.json 三種安裝路徑、9 個 MCP 工具與 lifecycle hooks 對照
created: 2026-07-21
updated: 2026-07-21
source: "https://docs.mem0.ai/integrations/claude-code"
published:
tags:
  - mcp
  - claude-code
  - coding-agent
  - memory
---

Add persistent memory to [**Claude Code**](https://docs.anthropic.com/en/docs/claude-code) (CLI) and **Claude Cowork** (desktop app) with the Mem0 plugin. Your agent forgets everything between sessions. This plugin fixes that by connecting to Mem0’s cloud memory layer via MCP, automatically capturing learnings at key lifecycle points, and retrieving relevant context before every response.

## Prerequisites

Before setting up Mem0 with Claude Code, ensure you have:

1. A Mem0 Platform account and API key:
	- [Sign up at app.mem0.ai](https://app.mem0.ai/?utm_source=oss&utm_medium=integration-claude-code)
		- [Get your API key](https://app.mem0.ai/dashboard/api-keys?utm_source=oss&utm_medium=integration-claude-code) (starts with `m0-`)
2. Claude Code CLI or Claude Cowork desktop app installed
3. Your API key added to your shell profile (persists across sessions):

```shellscript
echo 'export MEM0_API_KEY="m0-your-api-key"' >> ~/.zshrc
source ~/.zshrc
```

```shellscript
echo 'export MEM0_API_KEY="m0-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

Confirm it’s set:

```shellscript
echo $MEM0_API_KEY
# Should print: m0-your-api-key
```

## Installation

### Option A: Plugin Marketplace (Recommended)

Install the full plugin including MCP server, lifecycle hooks, and SDK skill.

1. Add the Mem0 marketplace:
	```shellscript
	claude plugin marketplace add mem0ai/mem0
	```
2. Install the plugin:
	```shellscript
	claude plugin install mem0@mem0-plugins
	```

**Claude Cowork desktop app:** Open the Cowork tab, click **Customize** in the sidebar, click **Browse plugins**, and install Mem0.

### Option B: MCP Only

Add the Mem0 MCP server directly with a single command:

```shellscript
npx mcp-add \
  --name mem0-mcp \
  --type http \
  --url "https://mcp.mem0.ai/mcp/" \
  --clients "claude code"
```

This gives you the MCP tools but not the lifecycle hooks or SDK skill.

### Option C: Manual MCP Configuration

Add to your Claude Code MCP config (`.mcp.json`):

```json
{
  "mcpServers": {
    "mem0": {
      "type": "http",
      "url": "https://mcp.mem0.ai/mcp/",
      "headers": {
        "Authorization": "Token ${MEM0_API_KEY}"
      }
    }
  }
}
```

### Managing the Plugin

```shellscript
claude plugin update mem0@mem0-plugins         # update the plugin to the latest version (restart to apply)
claude plugin marketplace update mem0-plugins  # refresh the marketplace catalog
claude plugin uninstall mem0@mem0-plugins      # uninstall the plugin (keeps the marketplace)
claude plugin marketplace remove mem0-plugins  # unregister the marketplace entirely
```

Start a new session and ask: *“List my mem0 entities”* or *“Search my memories for hello”*. If the `mem0` tools appear and respond, you’re all set.

## Post-Installation: Run /mem0:onboard

After installing the plugin, start a new Claude Code session and run:

```text
/mem0:onboard
```

This runs the setup wizard which:

1. Verifies your API key and MCP connection
2. Detects and imports project files (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`)
3. Installs coding-optimized memory categories
4. Shows your identity (user ID, project scope, branch)

The onboarding is idempotent and safe to re-run anytime. It auto-triggers on first session in a new project, but you can always invoke it manually.

## What’s Included

| Component | Plugin Install | MCP Only |
| --- | --- | --- |
| MCP Server (9 memory tools) | Yes | Yes |
| Lifecycle Hooks | Yes | No |
| Mem0 SDK Skill | Yes | No |

## Available MCP Tools

Once installed, the following tools are available in every Claude Code session:

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

When installed via the plugin marketplace, Mem0 hooks into Claude Code’s lifecycle to automatically manage memory:

| Hook | Event | What it does |
| --- | --- | --- |
| **Setup** | `Setup` | Installs the mem0 SDK and dependencies (runs on init and maintenance) |
| **Session start** | `SessionStart` | Loads prior memories and displays status banner |
| **User prompt** | `UserPromptSubmit` | Searches relevant memories before each message; skips short prompts |
| **Pre-tool (3 handlers)** | `PreToolUse` | Blocks MEMORY.md writes; enforces `user_id` / `app_id` on mem0 tool calls; scans files being read for relevant memory context |
| **Post-tool** | `PostToolUse` | Tracks stats, scans bash errors for related memories |
| **Stop** | `Stop` | Stores a session summary at the end of every assistant turn (not just at session end) |
| **Pre-compact** | `PreCompact` | Stores a summary before the context is compacted |

What you type is stored as yours. What Claude produces — session summaries and compaction summaries — is stored as the assistant’s, so its suggestions never become your stated preferences.

## Example Workflow

```text
# Session 1: Working on a feature
You: Let's refactor the auth module to use JWT tokens instead of sessions.

# Claude searches memories, finds nothing relevant, proceeds with the work.
# Mem0 stores what you said as yours:
#   - Your preference: "Prefers TypeScript, uses ESLint"
# ...and what Claude did as the assistant's, in the session summary:
#   - Decision: "Migrated auth from sessions to JWT tokens"
#   - Files modified: auth/middleware.ts, auth/token.ts

# Session 2 (days later): Related work
You: Add refresh token rotation to the auth system.

# Claude searches memories, retrieves the JWT migration context.
# Knows the file structure, decisions made, and your stated preferences.
# Continues seamlessly without re-explaining the codebase.
```

## Troubleshooting

- **“Connection failed”**: Verify `MEM0_API_KEY` is set in your shell: `echo $MEM0_API_KEY`. If empty, add it to your shell profile (see Prerequisites)
- **No tools appearing**: Restart your Claude Code session after installation
- **Memories not being captured**: Ensure you installed via the plugin marketplace (Option A) for lifecycle hooks. MCP-only installs require manual memory operations
- **“Mem0 Inactive” banner every session**: Your API key isn’t persisting. Add `export MEM0_API_KEY="m0-..."` to your `~/.zshrc` (or `~/.bashrc`) and run `source ~/.zshrc`

## Mem0 MCP Setup

Detailed MCP configuration for all clients

![](https://mintcdn.com/mem0/QK-8_hblyHgAr7vt/images/provider-icons/openai.svg?fit=max&auto=format&n=QK-8_hblyHgAr7vt&q=85&s=c053d899474ab098eb247707fcbabb56)

## Codex Integration

Add Mem0 memory to OpenAI Codex workflows

**Using Mem0?** [Star us on GitHub](https://github.com/mem0ai/mem0) to help more developers discover memory for AI apps.