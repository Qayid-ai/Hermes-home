---
name: claude-code
description: "Delegate coding to Claude Code CLI (features, PRs)."
version: 2.2.0
author: Hermes Agent + Teknium
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Anthropic, Code-Review, Refactoring, PTY, Automation]
    related_skills: [codex, hermes-agent, opencode]
---

# Claude Code — Hermes Orchestration Guide

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the Hermes terminal. Claude Code v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## Prerequisites

- **Install:** `npm install -g @anthropic-ai/claude-code`
- **Auth:** run `claude` once to log in (browser OAuth for Pro/Max, or set `ANTHROPIC_API_KEY`)
- **Console auth:** `claude auth login --console` for API key billing
- **SSO auth:** `claude auth login --sso` for Enterprise
- **Check status:** `claude auth status` (JSON) or `claude auth status --text` (human-readable)
- **Health check:** `claude doctor` — checks auto-updater and installation health
- **Version check:** `claude --version` (requires v2.x+)
- **Update:** `claude update` or `claude upgrade`

## Two Orchestration Modes

For Rawan/Qayid, there are now two valid workflows:

1. **Print mode (`claude -p`)** when Anthropic subscription-based charging supports it and the task fits one-shot file or text output.
2. **Interactive Claude Code through tmux with a file-output contract** as the fallback/control-plane workflow, and for long-running, approval-heavy, or multi-turn work.

Do not delete or deprecate the tmux/file-output workflow. Anthropic may revert charging or TUI/print behaviour again.

### Default Mode: Interactive PTY via tmux + File Output

Interactive mode uses the Claude Code subscription/TUI path, keeps Claude in a real session, and avoids treating terminal-visible output as the answer channel. Hermes controls the TUI through tmux, watches the pane only for status or approval prompts, and reads the final answer from a markdown file Claude writes.

```bash
# Start a tmux session in the project or working directory
tmux new-session -d -s claude-work -x 160 -y 50 'mkdir -p /path/to/project/outputs && cd /path/to/project && claude'

# Submit work with C-m, not literal Enter, after startup/trust handling
tmux send-keys -t claude-work '<prompt with file-output contract>' C-m

# Use pane capture only for control-plane status
tmux capture-pane -t claude-work -p -S -120

# Read Claude's final output from the contracted file
# e.g. ./outputs/<slug>.md
```

**Use this for:**
- All Qayid-controlled Claude Code delegation by default
- High-context review, synthesis, coding, or planning
- Multi-turn iterative work
- Human-in-the-loop decisions
- Exploratory coding sessions
- Claude slash commands such as `/compact`, `/review`, `/model`, `/context`

**Required prompt contract:**
```text
You are being controlled through interactive Claude Code.
Do not rely on terminal-visible output as the final answer.
Write your complete final answer to ./outputs/<slug>.md.
Rules:
- Create or overwrite that file.
- The markdown file is the source of truth.
- Do not include ANSI/UI text.
- If you need to ask a question, write it to the file under "Question".
- After writing the file, reply in the terminal only: WRITTEN ./outputs/<slug>.md
```

### Print Mode (`claude -p`)

`claude -p` is allowed again for Rawan/Qayid workflows when Anthropic subscription-based charging supports it and the task is bounded enough for one-shot output.

Use print mode for:
- sealed-context analysis
- bounded synthesis passes
- code review where the diff/context is supplied explicitly
- automation where stdout or a contracted output file is acceptable

Do **not** use print mode when you need TUI-only features such as `/effort ultracode`, multi-turn interactive control, approval handling, long-running autonomous edits, or fragile tool supervision. Use interactive tmux with a file-output contract for those.

## PTY Dialog Handling (CRITICAL for Interactive Mode)

Claude Code presents up to two confirmation dialogs on first launch. You MUST handle these via tmux send-keys:

### Dialog 1: Workspace Trust (first visit to a directory)
```
❯ 1. Yes, I trust this folder    ← DEFAULT (just press Enter)
  2. No, exit
```
**Handling:** `tmux send-keys -t <session> Enter` — default selection is correct.

### Dialog 2: Bypass Permissions Warning (only with --dangerously-skip-permissions)
```
❯ 1. No, exit                    ← DEFAULT (WRONG choice!)
  2. Yes, I accept
```
**Handling:** Must navigate DOWN first, then Enter:
```
tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter
```

### Robust Dialog Handling Pattern
```
# Launch with permissions bypass
terminal(command="tmux send-keys -t claude-work 'claude --dangerously-skip-permissions \\"your task\\"' Enter")

# Handle trust dialog (Enter for default "Yes")
terminal(command="sleep 4 && tmux send-keys -t claude-work Enter")

# Handle permissions dialog (Down then Enter for "Yes, I accept")
terminal(command="sleep 3 && tmux send-keys -t claude-work Down && sleep 0.3 && tmux send-keys -t claude-work Enter")

# Now wait for Claude to work
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -60")
```

**Denying tool approval prompts:** Do not use blind `Down`/`Enter` sequences when the goal is denial. Claude Code approval menus vary (`Yes`, `Yes always`, `No`, sometimes defaults shift after a failed command). Capture the pane, verify the exact option order, and prefer `Ctrl+C`/`Esc` to interrupt the pending tool call when denial matters. If you must select `No`, use the visible option order and re-capture immediately to confirm the command did not run.

**Note:** After the first trust acceptance for a directory, the trust dialog won't appear again. Only the permissions dialog recurs each time you use `--dangerously-skip-permissions`.

## CLI Subcommands

| Subcommand | Purpose |
|------------|---------|
| `claude` | Start interactive REPL |
| `claude "query"` | Start REPL with initial prompt |
| `claude -p "query"` | Print mode; allowed for bounded Rawan/Qayid workflows when subscription charging supports it |
| `cat file \| claude -p "query"` | Stdin print-mode pattern; allowed for bounded sealed-context workflows |
| `claude -c` | Continue the most recent conversation in this directory |
| `claude -r "id"` | Resume a specific session by ID or name |
| `claude auth login` | Sign in (add `--console` for API billing, `--sso` for Enterprise) |
| `claude auth status` | Check login status (returns JSON; `--text` for human-readable) |
| `claude mcp add <name> -- <cmd>` | Add an MCP server |
| `claude mcp list` | List configured MCP servers |
| `claude mcp remove <name>` | Remove an MCP server |
| `claude agents` | List configured agents |
| `claude doctor` | Run health checks on installation and auto-updater |
| `claude update` / `claude upgrade` | Update Claude Code to latest version |
| `claude remote-control` | Start server to control Claude from claude.ai or mobile app |
| `claude install [target]` | Install native build (stable, latest, or specific version) |
| `claude setup-token` | Set up long-lived auth token (requires subscription) |
| `claude plugin` / `claude plugins` | Manage Claude Code plugins |
| `claude auto-mode` | Inspect auto mode classifier configuration |

## Print Mode Reference (`claude -p`)

Use `claude -p` for bounded one-shot tasks when subscription charging is available. Keep prompts sealed and explicit. For final artifacts, either capture stdout directly or require Claude to write to a named file.

Use interactive tmux with a file-output contract when you need TUI-only controls, `/effort ultracode`, approvals, multi-turn supervision, or a resilient fallback if print mode regresses.

## Complete CLI Flags Reference

### Session & Environment
| Flag | Effect |
|------|--------|
| `-p, --print` | Non-interactive one-shot mode (exits when done) |
| `-c, --continue` | Resume most recent conversation in current directory |
| `-r, --resume <id>` | Resume specific session by ID or name (interactive picker if no ID) |
| `--fork-session` | When resuming, create new session ID instead of reusing original |
| `--session-id <uuid>` | Use a specific UUID for the conversation |
| `--no-session-persistence` | Don't save session to disk (print mode only) |
| `--add-dir <paths...>` | Grant Claude access to additional working directories |
| `-w, --worktree [name]` | Run in an isolated git worktree at `.claude/worktrees/<name>` |
| `--tmux` | Create a tmux session for the worktree (requires `--worktree`) |
| `--ide` | Auto-connect to a valid IDE on startup |
| `--chrome` / `--no-chrome` | Enable/disable Chrome browser integration for web testing |
| `--from-pr [number]` | Resume session linked to a specific GitHub PR |
| `--file <specs...>` | File resources to download at startup (format: `file_id:relative_path`) |

### Model & Performance
| Flag | Effect |
|------|--------|
| `--model <alias>` | Model selection: `sonnet`, `opus`, `haiku`, or full name like `claude-sonnet-4-6` |
| `--effort <level>` | Reasoning depth: `low`, `medium`, `high`, `max`, `auto` | Both |
| `--max-turns <n>` | Limit agentic loops (print mode only; prevents runaway) |
| `--max-budget-usd <n>` | Cap API spend in dollars (print mode only) |
| `--fallback-model <model>` | Auto-fallback when default model is overloaded (print mode only) |
| `--betas <betas...>` | Beta headers to include in API requests (API key users only) |

### Permission & Safety
| Flag | Effect |
|------|--------|
| `--dangerously-skip-permissions` | Auto-approve ALL tool use (file writes, bash, network, etc.) |
| `--allow-dangerously-skip-permissions` | Enable bypass as an *option* without enabling it by default |
| `--permission-mode <mode>` | `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` |
| `--allowedTools <tools...>` | Whitelist specific tools (comma or space-separated) |
| `--disallowedTools <tools...>` | Blacklist specific tools |
| `--tools <tools...>` | Override built-in tool set (`""` = none, `"default"` = all, or tool names) |

### Output & Input Format
| Flag | Effect |
|------|--------|
| `--output-format <fmt>` | `text` (default), `json` (single result object), `stream-json` (newline-delimited) |
| `--input-format <fmt>` | `text` (default) or `stream-json` (real-time streaming input) |
| `--json-schema <schema>` | Force structured JSON output matching a schema |
| `--verbose` | Full turn-by-turn output |
| `--include-partial-messages` | Include partial message chunks as they arrive (stream-json + print) |
| `--replay-user-messages` | Re-emit user messages on stdout (stream-json bidirectional) |

### System Prompt & Context
| Flag | Effect |
|------|--------|
| `--append-system-prompt <text>` | **Add** to the default system prompt (preserves built-in capabilities) |
| `--append-system-prompt-file <path>` | **Add** file contents to the default system prompt |
| `--system-prompt <text>` | **Replace** the entire system prompt (use --append instead usually) |
| `--system-prompt-file <path>` | **Replace** the system prompt with file contents |
| `--bare` | Skip hooks, plugins, MCP discovery, CLAUDE.md, OAuth (fastest startup) |
| `--agents '<json>'` | Define custom subagents dynamically as JSON |
| `--mcp-config <path>` | Load MCP servers from JSON file (repeatable) |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config`, ignoring all other MCP configs |
| `--settings <file-or-json>` | Load additional settings from a JSON file or inline JSON |
| `--setting-sources <sources>` | Comma-separated sources to load: `user`, `project`, `local` |
| `--plugin-dir <paths...>` | Load plugins from directories for this session only |
| `--disable-slash-commands` | Disable all skills/slash commands |

### Debugging
| Flag | Effect |
|------|--------|
| `-d, --debug [filter]` | Enable debug logging with optional category filter (e.g., `"api,hooks"`, `"!1p,!file"`) |
| `--debug-file <path>` | Write debug logs to file (implicitly enables debug mode) |

### Agent Teams
| Flag | Effect |
|------|--------|
| `--teammate-mode <mode>` | How agent teams display: `auto`, `in-process`, or `tmux` |
| `--brief` | Enable `SendUserMessage` tool for agent-to-user communication |

### Tool Name Syntax for --allowedTools / --disallowedTools
```
Read                    # All file reading
Edit                    # File editing (existing files)
Write                   # File creation (new files)
Bash                    # All shell commands
Bash(git *)             # Only git commands
Bash(git commit *)      # Only git commit commands
Bash(npm run lint:*)    # Pattern matching with wildcards
WebSearch               # Web search capability
WebFetch                # Web page fetching
mcp__<server>__<tool>   # Specific MCP tool
```

## Settings & Configuration

### Settings Hierarchy (highest to lowest priority)
1. **CLI flags** — override everything
2. **Local project:** `.claude/settings.local.json` (personal, gitignored)
3. **Project:** `.claude/settings.json` (shared, git-tracked)
4. **User:** `~/.claude/settings.json` (global)

### Permissions in Settings
```json
{
  "permissions": {
    "allow": ["Bash(npm run lint:*)", "WebSearch", "Read"],
    "ask": ["Write(*.ts)", "Bash(git push*)"],
    "deny": ["Read(.env)", "Bash(rm -rf *)"]
  }
}
```

### Memory Files (CLAUDE.md) Hierarchy
1. **Global:** `~/.claude/CLAUDE.md` — applies to all projects
2. **Project:** `./CLAUDE.md` — project-specific context (git-tracked)
3. **Local:** `.claude/CLAUDE.local.md` — personal project overrides (gitignored)

Use the `#` prefix in interactive mode to quickly add to memory: `# Always use 2-space indentation`.

## Interactive Session: Slash Commands

### Session & Context
| Command | Purpose |
|---------|---------|
| `/help` | Show all commands (including custom and MCP commands) |
| `/compact [focus]` | Compress context to save tokens; CLAUDE.md survives compaction. E.g., `/compact focus on auth logic` |
| `/clear` | Wipe conversation history for a fresh start |
| `/context` | Visualize context usage as a colored grid with optimization tips |
| `/cost` | View token usage with per-model and cache-hit breakdowns |
| `/resume` | Switch to or resume a different session |
| `/rewind` | Revert to a previous checkpoint in conversation or code |
| `/btw <question>` | Ask a side question without adding to context cost |
| `/status` | Show version, connectivity, and session info |
| `/todos` | List tracked action items from the conversation |
| `/exit` or `Ctrl+D` | End session |

### Development & Review
| Command | Purpose |
|---------|---------|
| `/review` | Request code review of current changes |
| `/security-review` | Perform security analysis of current changes |
| `/plan [description]` | Enter Plan mode with auto-start for task planning |
| `/loop [interval]` | Schedule recurring tasks within the session |
| `/batch` | Auto-create worktrees for large parallel changes (5-30 worktrees) |

### Configuration & Tools
| Command | Purpose |
|---------|---------|
| `/model [model]` | Switch models mid-session (use arrow keys to adjust effort) |
| `/effort [level]` | Set reasoning effort: `low`, `medium`, `high`, `max`, or `auto` |
| `/init` | Create a CLAUDE.md file for project memory |
| `/memory` | Open CLAUDE.md for editing |
| `/config` | Open interactive settings configuration |
| `/permissions` | View/update tool permissions |
| `/agents` | Manage specialized subagents |
| `/mcp` | Interactive UI to manage MCP servers |
| `/add-dir` | Add additional working directories (useful for monorepos) |
| `/usage` | Show plan limits and rate limit status |
| `/voice` | Enable push-to-talk voice mode (20 languages; hold Space to record, release to send) |
| `/release-notes` | Interactive picker for version release notes |

### Custom Slash Commands
Create `.claude/commands/<name>.md` (project-shared) or `~/.claude/commands/<name>.md` (personal):

```markdown
# .claude/commands/deploy.md
Run the deploy pipeline:
1. Run all tests
2. Build the Docker image
3. Push to registry
4. Update the $ARGUMENTS environment (default: staging)
```

Usage: `/deploy production` — `$ARGUMENTS` is replaced with the user's input.

### Skills (Natural Language Invocation)
Unlike slash commands (manually invoked), skills in `.claude/skills/` are markdown guides that Claude invokes automatically via natural language when the task matches:

```markdown
# .claude/skills/database-migration.md
When asked to create or modify database migrations:
1. Use Alembic for migration generation
2. Always create a rollback function
3. Test migrations against a local database copy
```

## Interactive Session: Keyboard Shortcuts

### General Controls
| Key | Action |
|-----|--------|
| `Ctrl+C` | Cancel current input or generation |
| `Ctrl+D` | Exit session |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+B` | Background a running task |
| `Ctrl+V` | Paste image into conversation |
| `Ctrl+O` | Transcript mode — see Claude's thinking process |
| `Ctrl+G` or `Ctrl+X Ctrl+E` | Open prompt in external editor |
| `Esc Esc` | Rewind conversation or code state / summarize |

### Mode Toggles
| Key | Action |
|-----|--------|
| `Shift+Tab` | Cycle permission modes (Normal → Auto-Accept → Plan) |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle thinking mode |
| `Alt+O` | Toggle Fast Mode |

### Multiline Input
| Key | Action |
|-----|--------|
| `\` + `Enter` | Quick newline |
| `Shift+Enter` | Newline (alternative) |
| `Ctrl+J` | Newline (alternative) |

### Input Prefixes
| Prefix | Action |
|--------|--------|
| `!` | Execute bash directly, bypassing AI (e.g., `!npm test`). Use `!` alone to toggle shell mode. |
| `@` | Reference files/directories with autocomplete (e.g., `@./src/api/`) |
| `#` | Quick add to CLAUDE.md memory (e.g., `# Use 2-space indentation`) |
| `/` | Slash commands |

### Pro Tip: "ultrathink"
Use the keyword "ultrathink" in your prompt for maximum reasoning effort on a specific turn. This triggers the deepest thinking mode regardless of the current `/effort` setting.

## PR Review Pattern

### Quick Review (Interactive tmux)
Use the default interactive tmux workflow. Ask Claude to review the diff and write findings to `./outputs/pr-review.md`. Do not pipe the diff through `claude -p`.

### Deep Review (Interactive + Worktree)
```
terminal(command="tmux new-session -d -s review -x 140 -y 40")
terminal(command="tmux send-keys -t review 'cd /path/to/repo && claude -w pr-review' Enter")
terminal(command="sleep 5 && tmux send-keys -t review Enter")  # Trust dialog
terminal(command="sleep 2 && tmux send-keys -t review 'Review all changes vs main. Check for bugs, security issues, race conditions, and missing tests.' Enter")
terminal(command="sleep 30 && tmux capture-pane -t review -p -S -60")
```

### PR Review from Number
Use interactive Claude Code in the repository and include the PR number in the prompt. Require output at `./outputs/pr-<number>-review.md`. Do not use `claude -p --from-pr`.

### Claude Worktree with tmux
```
terminal(command="claude -w feature-x --tmux", workdir="/path/to/repo")
```
Creates an isolated git worktree at `.claude/worktrees/feature-x` AND a tmux session for it. Uses iTerm2 native panes when available; add `--tmux=classic` for traditional tmux.

## Parallel Claude Instances

Run multiple independent Claude tasks simultaneously by starting separate tmux-backed interactive Claude Code sessions. Each session must receive its own file-output contract.

```bash
# Task 1: backend
tmux new-session -d -s task1 -x 160 -y 50 'cd ~/project && claude'
tmux send-keys -t task1 '<backend task + write final output to ./outputs/backend.md>' C-m

# Task 2: tests
tmux new-session -d -s task2 -x 160 -y 50 'cd ~/project && claude'
tmux send-keys -t task2 '<tests task + write final output to ./outputs/tests.md>' C-m

# Task 3: docs
tmux new-session -d -s task3 -x 160 -y 50 'cd ~/project && claude'
tmux send-keys -t task3 '<docs task + write final output to ./outputs/docs.md>' C-m

# Monitor status only
for s in task1 task2 task3; do tmux capture-pane -t "$s" -p -S -20; done
```


## CLAUDE.md — Project Context File

Claude Code auto-loads `CLAUDE.md` from the project root. Use it to persist project context:

```markdown
# Project: My API

## Architecture
- FastAPI backend with SQLAlchemy ORM
- PostgreSQL database, Redis cache
- pytest for testing with 90% coverage target

## Key Commands
- `make test` — run full test suite
- `make lint` — ruff + mypy
- `make dev` — start dev server on :8000

## Code Standards
- Type hints on all public functions
- Docstrings in Google style
- 2-space indentation for YAML, 4-space for Python
- No wildcard imports
```

**Be specific.** Instead of "Write good code", use "Use 2-space indentation for JS" or "Name test files with `.test.ts` suffix." Specific instructions save correction cycles.

### Rules Directory (Modular CLAUDE.md)
For projects with many rules, use the rules directory instead of one massive CLAUDE.md:
- **Project rules:** `.claude/rules/*.md` — team-shared, git-tracked
- **User rules:** `~/.claude/rules/*.md` — personal, global

Each `.md` file in the rules directory is loaded as additional context. This is cleaner than cramming everything into a single CLAUDE.md.

### Auto-Memory
Claude automatically stores learned project context in `~/.claude/projects/<project>/memory/`.
- **Limit:** 25KB or 200 lines per project
- This is separate from CLAUDE.md — it's Claude's own notes about the project, accumulated across sessions

## Custom Subagents

Define specialized agents in `.claude/agents/` (project), `~/.claude/agents/` (personal), or via `--agents` CLI flag (session):

### Agent Location Priority
1. `.claude/agents/` — project-level, team-shared
2. `--agents` CLI flag — session-specific, dynamic
3. `~/.claude/agents/` — user-level, personal

### Creating an Agent
```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Security-focused code review
model: opus
tools: [Read, Bash]
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication/authorization flaws
- Secrets in code
- Unsafe deserialization
```

Invoke via: `@security-reviewer review the auth module`

### Dynamic Agents via CLI
```
terminal(command="claude --agents '{\"reviewer\": {\"description\": \"Reviews code\", \"prompt\": \"You are a code reviewer focused on performance\"}}' -p 'Use @reviewer to check auth.py'", timeout=120)
```

Claude can orchestrate multiple agents: "Use @db-expert to optimize queries, then @security to audit the changes."

## Hooks — Automation on Events

Configure in `.claude/settings.json` (project) or `~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write(*.py)",
      "hooks": [{"type": "command", "command": "ruff check --fix $CLAUDE_FILE_PATHS"}]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -q 'rm -rf'; then echo 'Blocked!' && exit 2; fi"}]
    }],
    "Stop": [{
      "hooks": [{"type": "command", "command": "echo 'Claude finished a response' >> /tmp/claude-activity.log"}]
    }]
  }
}
```

### All 8 Hook Types
| Hook | When it fires | Common use |
|------|--------------|------------|
| `UserPromptSubmit` | Before Claude processes a user prompt | Input validation, logging |
| `PreToolUse` | Before tool execution | Security gates, block dangerous commands (exit 2 = block) |
| `PostToolUse` | After a tool finishes | Auto-format code, run linters |
| `Notification` | On permission requests or input waits | Desktop notifications, alerts |
| `Stop` | When Claude finishes a response | Completion logging, status updates |
| `SubagentStop` | When a subagent completes | Agent orchestration |
| `PreCompact` | Before context memory is cleared | Backup session transcripts |
| `SessionStart` | When a session begins | Load dev context (e.g., `git status`) |

### Hook Environment Variables
| Variable | Content |
|----------|---------|
| `CLAUDE_PROJECT_DIR` | Current project path |
| `CLAUDE_FILE_PATHS` | Files being modified |
| `CLAUDE_TOOL_INPUT` | Tool parameters as JSON |

### Security Hook Examples
```json
{
  "PreToolUse": [{
    "matcher": "Bash",
    "hooks": [{"type": "command", "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|git push.*--force|:(){ :|:& };:'; then echo 'Dangerous command blocked!' && exit 2; fi"}]
  }]
}
```

## MCP Integration

Add external tool servers for databases, APIs, and services:

```
# GitHub integration
terminal(command="claude mcp add -s user github -- npx @modelcontextprotocol/server-github", timeout=30)

# PostgreSQL queries
terminal(command="claude mcp add -s local postgres -- npx @anthropic-ai/server-postgres --connection-string postgresql://localhost/mydb", timeout=30)

# Puppeteer for web testing
terminal(command="claude mcp add puppeteer -- npx @anthropic-ai/server-puppeteer", timeout=30)
```

### MCP Scopes
| Flag | Scope | Storage |
|------|-------|---------|
| `-s user` | Global (all projects) | `~/.claude.json` |
| `-s local` | This project (personal) | `.claude/settings.local.json` (gitignored) |
| `-s project` | This project (team-shared) | `.claude/settings.json` (git-tracked) |

### MCP in Print/CI Mode
```
terminal(command="claude --bare -p 'Query database' --mcp-config mcp-servers.json --strict-mcp-config", timeout=60)
```
`--strict-mcp-config` ignores all MCP servers except those from `--mcp-config`.

Reference MCP resources in chat: `@github:issue://123`

### MCP Limits & Tuning
- **Tool descriptions:** 2KB cap per server for tool descriptions and server instructions
- **Result size:** Default capped; use `maxResultSizeChars` annotation to allow up to **500K** characters for large outputs
- **Output tokens:** `export MAX_MCP_OUTPUT_TOKENS=50000` — cap output from MCP servers to prevent context flooding
- **Transports:** `stdio` (local process), `http` (remote), `sse` (server-sent events)

### Monitoring Interactive Sessions

### Reading the TUI Status
```
# Periodic capture to check if Claude is still working or waiting for input
terminal(command="tmux capture-pane -t dev -p -S -10")
```

Look for these indicators:
- `❯` at bottom = waiting for your input (Claude is done or asking a question)
- `●` lines = Claude is actively using tools (reading, writing, running commands)
- `⏵⏵ bypass permissions on` = status bar showing permissions mode
- `◐ medium · /effort` = current effort level in status bar
- `ctrl+o to expand` = tool output was truncated (can be expanded interactively)

### File-Output Contract for Interactive Automation

When using interactive Claude Code, avoid treating `tmux capture-pane` as the final answer channel. Use the pane only as a control plane, and require Claude to write its answer to a markdown file that Hermes can read directly.

Recommended pattern:
```
# Start in a dedicated working directory Claude is allowed to write in
tmux new-session -d -s council-claude -x 160 -y 50 'mkdir -p /tmp/qayid-claude-council/outputs && cd /tmp/qayid-claude-council && claude'

# Submit prompts with C-m; it proved more reliable than literal Enter in Claude Code TUI automation
tmux send-keys -t council-claude '<prompt text>' C-m

# Detect status / approval prompts only
tmux capture-pane -t council-claude -p -S -120

# Read the actual output from the file Claude wrote
cat /tmp/qayid-claude-council/outputs/<slug>.md
```

Prompt contract:
```text
You are being controlled through interactive Claude Code.
Do not rely on terminal-visible output as the final answer.
Write your complete final answer to ./outputs/<slug>.md.
Rules:
- Create or overwrite that file.
- The markdown file is the source of truth.
- Do not include ANSI/UI text.
- If you need to ask a question, write it to the file under "Question".
- After writing the file, reply in the terminal only: WRITTEN ./outputs/<slug>.md
```

Notes:
- First write in a directory may require Claude Code's file-write approval. Capture the pane, approve the prompt with `C-m` if safe, then read the file.
- This is cleaner than scraping final answers from the TUI because line wrapping, ANSI redraws, and hidden scrollback can corrupt pane output.
- Still keep pane scraping for control-plane signals: trust prompt, permission prompt, OAuth/login handoff, `WRITTEN ...`, errors, and stuck-state detection.
- If the TUI says `Not logged in` even though `claude auth status` looks valid, treat the TUI as authoritative for that session. Run `/login` in the TUI. If it offers a copy shortcut such as `c`, copy/open the OAuth URL locally without printing it in chat; the user completes browser/keychain login, then resume the same tmux session.
- After browser OAuth/keychain login succeeds, an already-open Claude Code TUI may still show stale `Not logged in · Run /login` state. Verify auth outside the TUI with `claude auth status --text`. If the pane is still inside a `/login` prompt, send `Esc` to cancel it, confirm the normal `❯` prompt returns, then retry the contracted prompt in the same pane. If auth is valid but the TUI remains stale after that, kill and recreate the tmux session in the same workdir rather than fighting the old TUI.
- When pasting a long file-output contract into the Claude Code TUI via `tmux paste-buffer`, the paste may land at the prompt without submitting. Send an explicit second `C-m` after the paste and confirm Claude starts working before assuming the task is running.

### Context Window Health
Use `/context` in interactive mode to see a colored grid of context usage. Key thresholds:
- **< 70%** — Normal operation, full precision
- **70-85%** — Precision starts dropping, consider `/compact`
- **> 85%** — Hallucination risk spikes significantly, use `/compact` or `/clear`

### Dynamic Workflow Guardrail
Claude Code `ultracode` may propose dynamic workflows or multi-agent validation even when the task only needs a focused review. Do not approve those by default. If the user asked for a bounded review, choose `No`, or stop the workflow with `/workflows` + `x` if it already started. Then send a scope-correction prompt: stop expanding, use the grounded review already done, write the contracted output file, and do not run more workflows/agents/commands unless needed to write that file.

Exception: when Rawan explicitly asks for full source absorption, exhaustive review, or "you and Opus review all sources," dynamic workflows can be correct if they stay inside the supplied source bundle and no-write constraints. Let them finish, wait for the contracted output file, persist it outside `/tmp`, then reconcile before taking any side-effecting action.

## Environment Variables

| Variable | Effect |
|----------|--------|
| `ANTHROPIC_API_KEY` | API key for authentication (alternative to OAuth) |
| `CLAUDE_CODE_EFFORT_LEVEL` | Default effort: `low`, `medium`, `high`, `max`, or `auto` |
| `MAX_THINKING_TOKENS` | Cap thinking tokens (set to `0` to disable thinking entirely) |
| `MAX_MCP_OUTPUT_TOKENS` | Cap output from MCP servers (default varies; set e.g., `50000`) |
| `CLAUDE_CODE_NO_FLICKER=1` | Enable alt-screen rendering to eliminate terminal flicker |
| `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` | Strip credentials from sub-processes for security |

## Cost & Performance Tips

1. **Use interactive tmux sessions for Rawan/Qayid workflows** — subscription/TUI path, richer control, and fewer stdout automation failures.
2. **Use file-output contracts** — final answers belong in `./outputs/<slug>.md`, not pane capture.
3. **Use `/compact`** when context gets large.
4. **Use `/context`** to watch context pressure before output quality degrades.
5. **Start new sessions for distinct tasks** — fresh context is cheaper than dragging stale history.
6. **Use separate tmux sessions for parallel tasks** — one contracted output file per task.
7. **Clean up tmux sessions** after the work is read and verified.
8. **Use `claude -p` selectively** — it is valid again for bounded Rawan/Qayid tasks when subscription charging supports it; keep tmux/file-output as fallback.

## Analysis / Deep-Mode Routing

When using Claude Code as a reasoning backend for strategic modes, pre-mortems, blindspots, interviews, or other non-coding analysis, do not let it behave like an unconstrained coding agent. Gather the smallest sufficient context in Hermes first, then pass a sealed-context prompt and require `./outputs/<slug>.md`. See `references/analysis-deep-mode-contract.md`.

For vault-sensitive reviews, prefer launching Claude in a sealed `/tmp/<task-slug>` directory rather than inside the vault/repo. Put only the review prompt and minimal supplied context in that directory, require `./outputs/<slug>.md`, and deny broad filesystem discovery. This is especially important for AsturLAB vault work where adjacent files may contain client or cross-project context that the review does not need.

Key guardrail: if Claude starts broad filesystem discovery after you already supplied context, deny/interupt and redirect it to write the final output from the provided context. This preserves AsturLAB's smallest-sufficient-context rule and avoids cross-project bleed.

## Pitfalls & Gotchas

1. **Interactive mode REQUIRES tmux** — Claude Code is a full TUI app. Using `pty=true` alone in Hermes terminal works but tmux gives you `capture-pane` for monitoring and `send-keys` for input, which is essential for orchestration.
2. **`--dangerously-skip-permissions` dialog defaults to "No, exit"** — you must send Down then Enter to accept.
3. **`--max-budget-usd` minimum is ~$0.05** — system prompt cache creation alone costs this much. Setting lower will error immediately.
4. **`--max-turns` is print-mode only** — ignored in interactive sessions.
5. **Claude may use `python` instead of `python3`** — on systems without a `python` symlink, Claude's bash commands will fail on first try but it self-corrects.
6. **Session resumption requires same directory** — `--continue` finds the most recent session for the current working directory.
7. **`--json-schema` needs enough `--max-turns`** — Claude must read files before producing structured output, which takes multiple turns.
8. **Trust dialog only appears once per directory** — first-time only, then cached.
9. **Background tmux sessions persist** — always clean up with `tmux kill-session -t <name>` when done.
10. **Slash commands (like `/commit`) only work in interactive mode** — in `-p` mode, describe the task in natural language instead.
11. **`--bare` skips OAuth** — requires `ANTHROPIC_API_KEY` env var or an `apiKeyHelper` in settings.
12. **Context degradation is real** — AI output quality measurably degrades above 70% context window usage. Monitor with `/context` and proactively `/compact`.

## Rules for Hermes Agents

1. **Use `claude -p` selectively when subscription charging supports it; otherwise use tmux.**
2. **Use interactive tmux `claude` as the default Claude Code path** — this matches the user's subscription/TUI workflow.
3. **Use file-output contracts for final answers** — ask Claude to write `./outputs/<slug>.md`, then read the file; use `capture-pane` only for control-plane signals.
4. **Use `C-m` when submitting through tmux** — it is more reliable than literal `Enter` for Claude Code TUI prompts in Hermes-driven automation.
5. **Always set the working directory explicitly** — keep Claude focused on the right project directory.
6. **Monitor tmux sessions** — use `tmux capture-pane -t <session> -p -S -50` to check progress.
7. **Look for the `❯` prompt** — indicates Claude is waiting for input, done, or asking a question.
8. **Handle trust and permission dialogs deliberately** — do not assume the TUI started work.
9. **Do not scrape final answers from the pane** — line wrapping, ANSI redraws, and scrollback truncation corrupt output.
10. **Clean up tmux sessions** — kill them when done to avoid resource leaks.
11. **Report results to user** — summarize what Claude wrote, what changed, and where the output file lives.
12. **Don't kill slow sessions** — Claude may be doing multi-step work; check progress instead.
13. **Constrain tool access through prompt and session setup** — do not hand Claude broad write authority unless the task needs it.
