# Claude Code for analysis/deep-mode routing

Use this when Claude Code is being used as a high-context reasoning backend rather than as a coding agent.

## Pattern

1. Gather context in Hermes first.
   - Use `read_file`, `search_files`, `session_search`, or QMD from Hermes.
   - Keep the context small and explicit.
   - Treat missing or empty project docs as signal, but say so.

2. Start Claude Code in an isolated scratch directory.
   - Example: `/tmp/qayid-deep`.
   - Require output to `./outputs/<slug>.md`.

3. Use a sealed-context prompt.
   - Say: "Use only the context below. Do not inspect other project folders or run discovery commands. If context is insufficient, write the missing question to the output file."
   - This matters because Claude Code may otherwise behave like a coding agent and start broad filesystem inspection.

4. Monitor the pane only for control-plane state.
   - Approve safe writes to `outputs/`.
   - Do not approve broad vault reads unless the task genuinely needs them and the user has not constrained scope.
   - If Claude drifts into extra discovery, deny/interupt and redirect: "Proceed using only the provided context and write the final output now."

5. Read the markdown output file back into Hermes and use that as source of truth.

## Pitfall from strategy sessions

For strategic modes like pre-mortem, blindspot, and interview, the failure mode is over-research. Claude Code sees a filesystem and tries to inspect adjacent folders. That can violate AsturLAB's smallest-sufficient-context rule and wastes time. Seal the context before submission and actively stop extra discovery.