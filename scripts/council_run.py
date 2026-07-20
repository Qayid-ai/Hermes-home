#!/usr/bin/env python3
"""Council forum runner for Qayid.

Runs Codex + Opus + Antigravity into a shared forum with validation gates,
then runs a fresh Opus synthesiser from the finished forum.

The runner is deliberately conservative:
- voices write per-engine outputs only
- Qayid/runner is the only forum writer
- Antigravity is stdout-only through the no-fallback host wrapper
- bad output is marked DEGRADED/UNAVAILABLE instead of silently accepted
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import shutil
import shlex
import subprocess
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path('/tmp/qayid-council')
AGY_WRAPPER = Path.home() / 'agy-container' / 'antigravity_ask_host.sh'

VOICE_NAMES = {
    'codex': 'Codex',
    'opus': 'Opus',
    'antigravity': 'Google Antigravity',
}

ENGINE_NAMES = {
    'codex': 'openai-codex',
    'opus': 'claude-opus via claude-code',
    'antigravity': 'antigravity-host',
}

TOOL_NARRATION_RE = re.compile(r"^\s*I will (read|check|list|write|view|start|run|explore|inspect)\b", re.I | re.M)
VERDICT_RE = re.compile(r"\b(verdict|recommendation|recommend|thesis|position|prioriti[sz]e|should)\b", re.I)
UNCERTAINTY_RE = re.compile(r"\b(uncertain|uncertainty|risk|caveat|depends|evidence|source quality|confidence)\b", re.I)
# Process-failure gate. Keep this narrow and line-oriented.
# A strategic answer may legitimately discuss "failed" products or market errors;
# that is not a runner failure. Only terminal/tool failure phrasing should trip it.
FAILURE_RE = re.compile(
    r"(?im)^\s*(?:"
    r"blocked\b|failed\s+(?:to|because|due to)\b|error\b|exception\b|traceback\b|"
    r"permission denied\b|read-only sandbox\b|not logged in\b|model unreachable\b"
    r")"
)

@dataclasses.dataclass
class ValidationResult:
    quality: str  # PASS | FAIL
    status: str   # AVAILABLE | DEGRADED | UNAVAILABLE
    failure_class: str
    reasons: list[str]
    chars: int

@dataclasses.dataclass
class VoiceResult:
    voice: str
    round_no: int
    output_path: Path
    log_path: Path
    validation: ValidationResult
    engine: str
    attempts: int = 1


def sh(cmd: str, cwd: Path | None = None, timeout: int = 30, check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, shell=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=check)


def slugify(s: str, max_len: int = 64) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip('-')
    return s[:max_len].strip('-') or 'question'


def read(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='replace')
    except FileNotFoundError:
        return ''


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def append(path: Path, text: str) -> None:
    with path.open('a', encoding='utf-8') as f:
        f.write(text)


def non_ws_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text or ''))


def validate_voice(voice: str, output: str, log: str = '') -> ValidationResult:
    reasons: list[str] = []
    n = non_ws_len(output)

    if not output.strip():
        return ValidationResult('FAIL', 'UNAVAILABLE', 'blank-output', ['output file missing or blank'], n)

    if FAILURE_RE.search(output):
        reasons.append('output contains failure language')

    if n < 800:
        reasons.append(f'output too short: {n} non-whitespace chars < 800')

    if not VERDICT_RE.search(output):
        reasons.append('missing clear verdict/recommendation/thesis language')

    if not UNCERTAINTY_RE.search(output):
        reasons.append('missing uncertainty/risk/evidence-quality language')

    if voice == 'antigravity':
        if '[ENGINE: antigravity-host]' not in log:
            reasons.append('missing antigravity-host provenance marker in stderr log')
        narration = TOOL_NARRATION_RE.findall(output)
        narration_lines = len(TOOL_NARRATION_RE.findall(output))
        total_lines = max(1, len([ln for ln in output.splitlines() if ln.strip()]))
        if narration_lines >= 3 or narration_lines / total_lines > 0.25:
            reasons.append('output is dominated by tool-use narration')
        if re.search(r"\bWRITTEN\b", output) and n < 1200:
            reasons.append('contains WRITTEN/status text with too little substantive content')
        if output.lstrip()[:1].islower():
            reasons.append('appears to start mid-sentence/truncated')

    if not reasons:
        return ValidationResult('PASS', 'AVAILABLE', 'none', [], n)

    # Some output exists but fails quality. Preserve it as degraded evidence.
    return ValidationResult('FAIL', 'DEGRADED', 'quality-gate', reasons, n)


def base_voice_prompt(voice: str, question: str, sealed_context: str, forum_so_far: str, output_path: str, round_no: int) -> str:
    return textwrap.dedent(f"""
    You are {VOICE_NAMES[voice]}, one independent research-capable voice in the Council forum.

    You are not Qayid. You are not the final synthesiser.

    Task:
    Investigate the question below and write your grounded position for round {round_no}.
    Use your own research capability. Spawn multiple internal agents/subagents where your CLI supports that.
    If your CLI cannot spawn subagents, run at least three separate research tracks yourself and label them before giving your final position.
    Run this as deep research, not a quick opinion. Minimum tracks:
    - demand/revenue evidence
    - competition/substitution risk
    - execution/distribution/solo-operator fit
    Add extra tracks when the question warrants it.

    Rules:
    - Reason from the supplied question, sealed context, and full forum-so-far.
    - You may use web/research tools available inside your own CLI session.
    - Do not edit the shared forum file.
    - In rebuttal rounds, engage the strongest opposing arguments from the forum, not straw men.
    - State uncertainties and source quality plainly.
    - Separate primary evidence, secondary reporting, and inference.
    - Prefer official sources, market/category data, competitor docs, and concrete buyer/workflow evidence over vibes.
    - Do not defer to consensus.
    - Include a clear thesis/verdict near the top.
    - Include concrete implications or next actions.

    QUESTION:
    {question}

    SEALED CONTEXT:
    {sealed_context}

    FULL FORUM SO FAR:
    {forum_so_far}

    OUTPUT CONTRACT:
    Write your complete answer to {output_path}.
    After writing, reply in the terminal only: WRITTEN {output_path}
    """).strip() + "\n"


def antigravity_prompt(question: str, sealed_context: str, forum_so_far: str, round_no: int) -> str:
    return textwrap.dedent(f"""
    You are Google Antigravity, one independent research-capable voice in the Council forum.

    You are not Qayid. You are not the final synthesiser.

    Task:
    Investigate the question below and write your grounded position for round {round_no}.
    Use your own research capability. If you cannot spawn subagents, run at least three separated research tracks and label the resulting evidence before giving your final position.
    Run this as deep research, not a quick opinion. Minimum tracks:
    - demand/revenue evidence
    - competition/substitution risk
    - execution/distribution/solo-operator fit
    Add extra tracks when the question warrants it.

    Rules:
    - Reason from the supplied question, sealed context, and full forum-so-far.
    - Do not defer to consensus.
    - State uncertainties and source quality plainly.
    - Separate primary evidence, secondary reporting, and inference.
    - Prefer official sources, market/category data, competitor docs, and concrete buyer/workflow evidence over vibes.
    - Include a clear thesis/verdict near the top.
    - Include concrete implications or next actions.

    QUESTION:
    {question}

    SEALED CONTEXT:
    {sealed_context}

    FULL FORUM SO FAR:
    {forum_so_far}

    OUTPUT CONTRACT:
    Return ONLY your complete Council position in markdown on stdout.
    Do not inspect the filesystem.
    Do not write files.
    Do not describe your plan.
    Do not say WRITTEN.
    Do not include tool-use narration such as "I will read...".
    The Council wrapper will save your stdout to ./outputs/antigravity-r{round_no}.md.
    """).strip() + "\n"


def synthesis_prompt(forum: str) -> str:
    return textwrap.dedent(f"""
    You are the Council synthesiser.

    Read ONLY the finished forum below. Do not inspect any files. Do not use web. Do not use raw voice output files. Do not re-derive from scratch.

    Produce:
    1. Points of consensus.
    2. Genuine disagreements and what drives each.
    3. The strongest dissenting insight worth preserving.
    4. Evidence-quality notes.
    5. Verdict.
    6. Concrete next action.

    If a voice or round is marked UNAVAILABLE, DEGRADED, or Quality: FAIL, state the gap and how it limits confidence.

    Write your complete verdict to ./outputs/synthesis.md.
    After writing, reply only: WRITTEN ./outputs/synthesis.md

    FINISHED FORUM:
    {forum}
    """).strip() + "\n"


def init_run(question: str, mode: str, rebuttal_rounds: int, hard_cap: str, sealed_context: str) -> Path:
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    run_dir = ROOT / f"{stamp}-{slugify(question)}"
    for sub in ['outputs', 'logs', 'prompts']:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    sh('git init -q', cwd=run_dir, timeout=10)
    forum = textwrap.dedent(f"""
    # Council Forum — {question}

    Mode: {mode}
    Rebuttal rounds requested: {rebuttal_rounds}
    Hard cap: {hard_cap}

    ## Sealed context
    {sealed_context}

    ## Round 0 — Opening positions
    """).lstrip()
    write(run_dir / 'forum.md', forum)
    return run_dir


def wait_for_file(path: Path, timeout: int) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists() and path.stat().st_size > 0:
            return True
        time.sleep(2)
    return False


def tmux_capture(session: str) -> str:
    res = sh(f"tmux capture-pane -t {session} -p -S -120 2>/dev/null || true", timeout=5)
    return res.stdout or ''


def tmux_send(session: str, keys: str) -> None:
    sh(f"tmux send-keys -t {session} {keys} 2>/dev/null || true", timeout=5)


def tmux_select_option(session: str, option: str) -> None:
    """Select an interactive Claude Code menu option reliably.

    Claude Code subagent approval prompts sometimes treat `tmux send-keys '1 C-m'`
    as queued text instead of a submitted menu choice. Send the digit literally,
    then send Enter as a separate keypress, then send one extra Enter if the UI
    still has the queued digit focus. This is still narrow: callers decide which
    prompts are safe to approve.
    """
    sh(f"tmux send-keys -t {session} -l {shlex.quote(option)} 2>/dev/null || true", timeout=5)
    time.sleep(0.4)
    tmux_send(session, 'C-m')
    time.sleep(0.8)
    pane = tmux_capture(session)
    if f'❯ {option}' in pane or 'Press up to edit queued messages' in pane:
        tmux_send(session, 'C-m')


def is_safe_tmp_bash_prompt(pane: str) -> bool:
    """Allow only read/research Bash approvals inside Council scratch/tmp.

    This covers Claude Code inspecting downloaded public data under /tmp with
    python/openpyxl. It deliberately excludes destructive shell, credential reads,
    network posting, git mutation, and writes outside /tmp/qayid-council or /tmp.
    """
    if 'Bash command' not in pane or 'Do you want to proceed?' not in pane:
        return False
    if '/tmp' not in pane and '/private/tmp' not in pane and '/tmp/qayid-council' not in pane:
        return False
    safe_markers = ['python3 -c', 'openpyxl', 'head -', 'tail -', 'List sheet names', 'Read Contents sheet', 'Dump Section']
    if not any(marker in pane for marker in safe_markers):
        return False
    banned = ['rm ', 'rm -', 'mv ', 'cp ', 'curl ', 'wget ', 'ssh ', 'scp ', 'git ', 'chmod ', 'chown ', '.env', 'auth.json', 'token', 'password', 'kill-session']
    return not any(bad in pane for bad in banned)


def wait_for_opus_file(session: str, output_path: Path, timeout: int, allow_deep_research: bool = True) -> bool:
    """Wait for an Opus output file while handling narrow interactive prompts.

    This is intentionally not YOLO. It only approves:
    - Claude trust prompt for the isolated /tmp/qayid-council scratch dir.
    - Claude Code's deep-research Skill prompt, when enabled.

    Anything else remains visible/stuck so the run fails loudly instead of
    granting broad permissions.
    """
    deadline = time.time() + timeout
    approved_trust = False
    approved_deep_research = False
    while time.time() < deadline:
        if output_path.exists() and output_path.stat().st_size > 0:
            return True

        pane = tmux_capture(session)
        if not approved_trust and 'Yes, I trust this folder' in pane and ('/tmp/qayid-council' in pane or '/private/tmp/qayid-council' in pane):
            tmux_send(session, 'C-m')
            approved_trust = True
        elif allow_deep_research and not approved_deep_research and 'Use skill "deep-research"?' in pane:
            # Option 2 = Yes, and don't ask again for this scratch directory.
            tmux_select_option(session, '2')
            approved_deep_research = True
        elif allow_deep_research and 'Web Search' in pane and 'Do you want to proceed?' in pane and ('/tmp/qayid-council' in pane or '/private/tmp/qayid-council' in pane):
            # Option 2 = Yes, and don't ask again for Web Search commands in this scratch directory.
            tmux_select_option(session, '2')
        elif allow_deep_research and (
            'Fetch' in pane
            or 'Claude wants to fetch content from' in pane
            or 'Do you want to allow Claude to fetch this content?' in pane
        ) and (
            'Do you want to allow Claude to fetch this content?' in pane
            or 'Do you want to proceed?' in pane
            or 'Claude wants to fetch content from' in pane
        ):
            # Option 1 is safest: approve only this fetch prompt, not a broad per-domain grant.
            # Claude Code versions vary the wording, so match the permission prompt rather than
            # only the tool title.
            tmux_select_option(session, '1')
        elif allow_deep_research and is_safe_tmp_bash_prompt(pane):
            # Narrowly approve read-only /tmp data inspection used by Opus research agents.
            tmux_select_option(session, '1')
        time.sleep(3)
    return False


def launch_codex(run_dir: Path, prompt_path: Path, round_no: int, timeout: int) -> None:
    session = f"council-codex-r{round_no}"
    cmd = (
        f"tmux kill-session -t {session} 2>/dev/null || true; "
        f"tmux new-session -d -s {session} -x 160 -y 50 "
        f"'cd {run_dir} && codex --search exec --sandbox workspace-write "
        f"--output-last-message outputs/codex-r{round_no}.last.md \"$(cat {prompt_path})\" "
        f"> logs/codex-r{round_no}.log 2>&1'"
    )
    sh(cmd, timeout=10)


def launch_antigravity(run_dir: Path, prompt_path: Path, round_no: int, timeout: int) -> None:
    session = f"council-antigravity-r{round_no}"
    cmd = (
        f"tmux kill-session -t {session} 2>/dev/null || true; "
        f"tmux new-session -d -s {session} -x 160 -y 50 "
        f"'cd {run_dir} && ANTIGRAVITY_TIMEOUT_SECS={timeout} {AGY_WRAPPER} "
        f"\"$(cat {prompt_path})\" council-antigravity-r{round_no} "
        f"> outputs/antigravity-r{round_no}.md 2> logs/antigravity-r{round_no}.log'"
    )
    sh(cmd, timeout=10)


def launch_opus(run_dir: Path, prompt_path: Path, round_no: int | str, timeout: int, allow_deep_research: bool = True) -> str:
    session = f"council-opus-r{round_no}" if isinstance(round_no, int) else 'council-synth'
    # Initial-argument launch is more reliable than paste-buffer for this workflow.
    cmd = (
        f"tmux kill-session -t {session} 2>/dev/null || true; "
        f"tmux new-session -d -s {session} -x 160 -y 50 "
        f"'cd {run_dir} && claude --model opus --effort max --permission-mode acceptEdits \"$(cat {prompt_path})\"'"
    )
    sh(cmd, timeout=10)
    return session


def harvest(run_dir: Path, voice: str, round_no: int, attempts: int = 1) -> VoiceResult:
    out = run_dir / 'outputs' / f'{voice}-r{round_no}.md'
    log_name = 'antigravity-r%d.log' % round_no if voice == 'antigravity' else f'{voice}-r{round_no}.log'
    log = run_dir / 'logs' / log_name
    validation = validate_voice(voice, read(out), read(log))
    return VoiceResult(voice, round_no, out, log, validation, ENGINE_NAMES[voice], attempts)


def append_voice(run_dir: Path, result: VoiceResult) -> None:
    forum = run_dir / 'forum.md'
    output_rel = result.output_path.relative_to(run_dir)
    body = read(result.output_path).strip()
    if not body:
        body = '(No usable output captured.)'
    v = result.validation
    append(forum, textwrap.dedent(f"""

    ### {VOICE_NAMES[result.voice]} — Round {result.round_no}

    Status: {v.status}
    Quality: {v.quality}
    Failure class: {v.failure_class}
    Engine: {result.engine}
    Output file: {output_rel}
    Attempts: {result.attempts}
    Validation notes: {'; '.join(v.reasons) if v.reasons else 'none'}

    {body}
    """))


def write_quality_report(run_dir: Path, results: list[VoiceResult]) -> None:
    forum = read(run_dir / 'forum.md')
    data = {
        'forum_path': str(run_dir / 'forum.md'),
        'forum_sha256': hashlib.sha256(forum.encode('utf-8')).hexdigest(),
        'voices': [
            {
                'voice': r.voice,
                'round': r.round_no,
                'status': r.validation.status,
                'quality': r.validation.quality,
                'failure_class': r.validation.failure_class,
                'reasons': r.validation.reasons,
                'chars_non_ws': r.validation.chars,
                'output_path': str(r.output_path),
                'log_path': str(r.log_path),
                'engine': r.engine,
                'attempts': r.attempts,
            } for r in results
        ],
    }
    write(run_dir / 'run.json', json.dumps(data, indent=2))
    lines = ['# Council Quality Report', '', f"Forum SHA256: `{data['forum_sha256']}`", '']
    for r in results:
        lines += [
            f"## {VOICE_NAMES[r.voice]} r{r.round_no}",
            f"- Status: {r.validation.status}",
            f"- Quality: {r.validation.quality}",
            f"- Failure class: {r.validation.failure_class}",
            f"- Attempts: {r.attempts}",
            f"- Reasons: {'; '.join(r.validation.reasons) if r.validation.reasons else 'none'}",
            '',
        ]
    write(run_dir / 'quality_report.md', '\n'.join(lines))


def run_round(run_dir: Path, question: str, sealed_context: str, round_no: int, timeout: int, dry_run: bool = False) -> list[VoiceResult]:
    forum = read(run_dir / 'forum.md')
    prompts = {
        'codex': base_voice_prompt('codex', question, sealed_context, forum, f'./outputs/codex-r{round_no}.md', round_no),
        'opus': base_voice_prompt('opus', question, sealed_context, forum, f'./outputs/opus-r{round_no}.md', round_no),
        'antigravity': antigravity_prompt(question, sealed_context, forum, round_no),
    }
    for voice, prompt in prompts.items():
        write(run_dir / 'prompts' / f'{voice}-r{round_no}.txt', prompt)

    if dry_run:
        return []

    launch_codex(run_dir, run_dir / 'prompts' / f'codex-r{round_no}.txt', round_no, timeout)
    launch_antigravity(run_dir, run_dir / 'prompts' / f'antigravity-r{round_no}.txt', round_no, timeout)
    opus_session = launch_opus(run_dir, run_dir / 'prompts' / f'opus-r{round_no}.txt', round_no, timeout, allow_deep_research=True)

    # Wait concurrently. Opus may need interactive approvals while Codex/Antigravity run,
    # so do not wait for other voices first or Opus can sit blocked for minutes.
    deadline = time.time() + timeout
    while time.time() < deadline:
        codex_done = (run_dir / 'outputs' / f'codex-r{round_no}.md').exists() and (run_dir / 'outputs' / f'codex-r{round_no}.md').stat().st_size > 0
        ag_done = (run_dir / 'outputs' / f'antigravity-r{round_no}.md').exists() and (run_dir / 'outputs' / f'antigravity-r{round_no}.md').stat().st_size > 0
        opus_done = (run_dir / 'outputs' / f'opus-r{round_no}.md').exists() and (run_dir / 'outputs' / f'opus-r{round_no}.md').stat().st_size > 0
        if codex_done and ag_done and opus_done:
            break
        if not opus_done:
            wait_for_opus_file(opus_session, run_dir / 'outputs' / f'opus-r{round_no}.md', 3, allow_deep_research=True)
        time.sleep(2)

    # Claude Code can finish its research agents and write slightly after the main
    # concurrent loop, especially when Codex/Antigravity finish much earlier.
    # Do not mark Opus blank while the interactive session is still alive and
    # close to producing the contracted file.
    opus_output = run_dir / 'outputs' / f'opus-r{round_no}.md'
    if not (opus_output.exists() and opus_output.stat().st_size > 0):
        wait_for_opus_file(opus_session, opus_output, min(180, max(30, timeout // 3)), allow_deep_research=True)

    results = [harvest(run_dir, v, round_no) for v in ['codex', 'opus', 'antigravity']]

    # Repair Antigravity once if it returned narration/truncated output but the engine path worked.
    ag = next(r for r in results if r.voice == 'antigravity')
    if ag.validation.quality == 'FAIL' and ag.validation.status == 'DEGRADED' and '[ENGINE: antigravity-host]' in read(ag.log_path):
        repair_prompt = antigravity_prompt(question, sealed_context, forum, round_no) + "\nYour previous output failed because it contained tool narration or was truncated. Return only the final substantive markdown answer.\n"
        repair_path = run_dir / 'prompts' / f'antigravity-r{round_no}-repair.txt'
        write(repair_path, repair_prompt)
        launch_antigravity(run_dir, repair_path, round_no, timeout)
        wait_for_file(run_dir / 'outputs' / f'antigravity-r{round_no}.md', timeout)
        repaired = harvest(run_dir, 'antigravity', round_no, attempts=2)
        results = [repaired if r.voice == 'antigravity' else r for r in results]

    for r in results:
        append_voice(run_dir, r)
    return results


def run_synthesis(run_dir: Path, timeout: int, dry_run: bool = False) -> None:
    prompt = synthesis_prompt(read(run_dir / 'forum.md'))
    prompt_path = run_dir / 'prompts' / 'synthesis.txt'
    write(prompt_path, prompt)
    if dry_run:
        return
    synth_session = launch_opus(run_dir, prompt_path, 'synth', timeout, allow_deep_research=False)
    wait_for_opus_file(synth_session, run_dir / 'outputs' / 'synthesis.md', timeout, allow_deep_research=False)


def cleanup_tmux() -> None:
    for pattern in ['council-codex-r', 'council-opus-r', 'council-antigravity-r', 'council-synth']:
        res = sh("tmux list-sessions -F '#S' 2>/dev/null || true", timeout=5)
        for sess in res.stdout.splitlines():
            if sess.startswith(pattern) or sess == pattern:
                sh(f"tmux kill-session -t {sess} 2>/dev/null || true", timeout=5)


def smoke_validate() -> int:
    good = "# Verdict\n\nRecommendation: prioritise reliability as promise and speed as method.\n\n" + ("Evidence and uncertainty: depends on client mix. " * 80)
    bad = "I will read the files.\nI will check the logs.\nI will write the answer.\nWRITTEN ./outputs/antigravity-r0.md\ne, fragment"
    assert validate_voice('antigravity', good, '[ENGINE: antigravity-host]').quality == 'PASS'
    assert validate_voice('antigravity', bad, '[ENGINE: antigravity-host]').quality == 'FAIL'
    assert validate_voice('codex', '', '').status == 'UNAVAILABLE'
    print('SMOKE_OK validators')
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--question', required=False)
    ap.add_argument('--sealed-context', default='No additional sealed context supplied.')
    ap.add_argument('--mode', default='forum', choices=['forum', 'forum_rebuttal', 'open_debate'])
    ap.add_argument('--rebuttal-rounds', type=int, default=0)
    ap.add_argument('--hard-cap', default='n/a')
    ap.add_argument('--timeout', type=int, default=420)
    ap.add_argument('--dry-run', action='store_true', help='create scratch/prompts only; do not invoke voices')
    ap.add_argument('--smoke-validate', action='store_true')
    args = ap.parse_args(argv)

    if args.smoke_validate:
        return smoke_validate()
    if not args.question:
        ap.error('--question is required unless --smoke-validate is used')

    run_dir = init_run(args.question, args.mode, args.rebuttal_rounds, args.hard_cap, args.sealed_context)
    all_results: list[VoiceResult] = []
    try:
        all_results.extend(run_round(run_dir, args.question, args.sealed_context, 0, args.timeout, args.dry_run))

        rounds = args.rebuttal_rounds
        if args.mode == 'open_debate' and rounds <= 0:
            rounds = 3
        if args.mode == 'forum':
            rounds = 0

        try:
            cap = int(args.hard_cap) if str(args.hard_cap).isdigit() else None
        except Exception:
            cap = None
        if args.mode == 'open_debate' and cap is not None:
            rounds = min(rounds, cap)

        for round_no in range(1, rounds + 1):
            append(run_dir / 'forum.md', f"\n\n## Round {round_no} — Rebuttals\n")
            all_results.extend(run_round(run_dir, args.question, args.sealed_context, round_no, args.timeout, args.dry_run))

        write_quality_report(run_dir, all_results)
        run_synthesis(run_dir, args.timeout, args.dry_run)
    finally:
        cleanup_tmux()

    print(f"FORUM={run_dir / 'forum.md'}")
    print(f"SYNTHESIS={run_dir / 'outputs' / 'synthesis.md'}")
    print(f"QUALITY={run_dir / 'quality_report.md'}")
    print(f"RUN_JSON={run_dir / 'run.json'}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
