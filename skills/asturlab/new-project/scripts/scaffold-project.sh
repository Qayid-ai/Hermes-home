#!/bin/bash
# scaffold-project.sh
# Scaffolds a new project under ~/Vaults/asturlab/projects/ with full structure.
# Usage: bash scaffold-project.sh <project-name>
# Refuses to overwrite existing projects. Validates name format.

set -e

PROJECT="$1"
VAULT="$HOME/Vaults/asturlab"
PROJECT_DIR="$VAULT/projects/$PROJECT"
TODAY=$(date +%Y-%m-%d)

# --- Validation ---

if [ -z "$PROJECT" ]; then
  echo "ERROR: project name required."
  echo "Usage: bash $0 <project-name>"
  exit 1
fi

if ! [[ "$PROJECT" =~ ^[a-z][a-z0-9-]*$ ]]; then
  echo "ERROR: project name '$PROJECT' is invalid."
  echo "Names must match ^[a-z][a-z0-9-]*$ — lowercase letters, digits, hyphens only. Must start with a letter."
  exit 1
fi

if [ ! -d "$VAULT" ]; then
  echo "ERROR: vault not found at $VAULT"
  echo "Vault setup is broken or VAULT path has changed."
  exit 1
fi

if [ -d "$PROJECT_DIR" ]; then
  echo "ERROR: project '$PROJECT' already exists at $PROJECT_DIR"
  echo "Refusing to overwrite. Choose a different name or remove the existing folder manually."
  exit 1
fi

# --- Folder structure ---

echo "Scaffolding project: $PROJECT"
echo ""

mkdir -p "$PROJECT_DIR/notes"
mkdir -p "$PROJECT_DIR/sessions"
mkdir -p "$PROJECT_DIR/research"
mkdir -p "$PROJECT_DIR/communications/client"
mkdir -p "$PROJECT_DIR/communications/partners"
mkdir -p "$PROJECT_DIR/communications/meetings"
mkdir -p "$PROJECT_DIR/planning"

echo "  CREATED: folder structure (notes, sessions, research, communications/{client,partners,meetings}, planning)"

# --- README.md stub ---

cat > "$PROJECT_DIR/README.md" <<README_EOF
---
project: $PROJECT
status: active
created: $TODAY
last-updated: $TODAY
---

# $PROJECT

## Overview

<!-- One-paragraph description of what this project is. -->

## Status

<!-- Current state — what's been done, what's in progress, what's next. -->

## Key files

- [Brief](planning/brief.md)
- [Scope](planning/scope.md)
- [Roadmap](planning/roadmap.md)
- [Kanban](planning/kanban.md)
- [Decisions](planning/decisions.md)
README_EOF

echo "  CREATED: README.md"

# --- Planning scaffold (8 files) ---

PLANNING="$PROJECT_DIR/planning"

write_planning() {
  local filename="$1"
  local content="$2"
  echo "$content" > "$PLANNING/$filename"
  echo "  CREATED: planning/$filename"
}

write_planning "brief.md" "---
project: $PROJECT
type: brief
status: draft
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->
<!-- Brief is typically locked once agreed with client. Update last-updated when edited. -->

# Brief

## The ask

<!-- What was originally requested. Quote or paraphrase the client's words. -->

## Context

<!-- Background — who is asking, what problem they have, why now. -->
"

write_planning "scope.md" "---
project: $PROJECT
type: scope
status: draft
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->
<!-- Living document — update last-updated whenever scope changes. -->

# Scope

## In scope

<!-- What we're delivering. Be specific. -->

## Out of scope

<!-- What we're explicitly NOT delivering. Equally important. -->

## Success criteria

<!-- How we know it's done. -->
"

write_planning "requirements.md" "---
project: $PROJECT
type: requirements
status: draft
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->

# Requirements

## Functional

<!-- What the system must do. Behaviour, not implementation. -->

## Non-functional

<!-- Performance, security, accessibility, scaling expectations. -->

## Constraints

<!-- Hard constraints — tech stack mandates, budget caps, deadlines, integrations. -->
"

write_planning "tech-plan.md" "---
project: $PROJECT
type: tech-plan
status: draft
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->
<!-- Living document — update as the build evolves. -->

# Technical plan

## Stack

<!-- Languages, frameworks, hosting, key services. -->

## Architecture

<!-- High-level structure. Components and how they relate. -->

## Approach

<!-- Build order, what comes first, dependencies. -->
"

write_planning "roadmap.md" "---
project: $PROJECT
type: roadmap
status: active
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->
<!-- Living document — update as milestones shift. -->

# Roadmap

## Milestones

<!-- Format:
### YYYY-MM-DD — Milestone title
**Owner:** who
**Status:** todo | doing | done | blocked
**Notes:** brief context
-->
"

write_planning "kanban.md" "---
project: $PROJECT
type: kanban
status: active
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->
<!-- Tasks move between sections. New tasks default to Todo. -->

# Kanban

## Todo

## Doing

## Done
"

write_planning "decisions.md" "---
project: $PROJECT
type: decisions
status: active
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->

# Decisions

Append-only log. New entries at the bottom. Never edit prior entries.

<!-- Template for new entries:
## YYYY-MM-DD — Decision title
**Context:** What prompted the decision.
**Decision:** What was decided.
**Reasoning:** Why this over alternatives.
-->
"

write_planning "risks.md" "---
project: $PROJECT
type: risks
status: active
last-updated: $TODAY
---

<!-- Frontmatter: status must be one of: draft | active | locked -->

# Risks

<!-- Format:
## Risk title
**Severity:** low | medium | high
**Surfaced:** YYYY-MM-DD
**Status:** open | mitigated | accepted | closed
**Description:** What the risk is and what it threatens.
**Mitigation:** What we're doing about it (if anything).
-->
"

# --- Final summary ---

echo ""
echo "Done. Project '$PROJECT' scaffolded at $PROJECT_DIR"
echo ""
echo "Structure:"
find "$PROJECT_DIR" -type d -o -type f | sort | sed "s|$PROJECT_DIR|  $PROJECT|"
echo ""
echo "Next steps:"
echo "  1. Create matching Telegram channel/topic named '$PROJECT' (for Rule 4 channel mapping)"
echo "  2. Open planning/brief.md and document the original ask"
echo "  3. Set status: locked on brief.md once it's agreed"
