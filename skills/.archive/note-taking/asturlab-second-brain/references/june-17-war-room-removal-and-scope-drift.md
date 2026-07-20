# June 17 scope-drift correction — War Room removal

Session learning for the AsturLAB Second Brain skill.

## What happened

During the second-brain build, Qayid accidentally treated later War Room sequencing discussion as part of the original June 15 second-brain brief. That caused War Room OS Slice 1/2 work to be committed and Slice 3 work to be created/parked.

Rawan corrected the scope:

- The June 15 22:06 source message governed the build.
- That brief was for the AsturLAB second brain / Karpathy LLM Wiki system.
- War Room OS was not part of that original build.
- War Room should be started fresh later.
- War Room artifacts created from the mistaken merged scope should be removed, not treated as progress to preserve.

## Operational rule

When the active task is the second-brain build and War Room artifacts exist because of previous scope bleed:

1. Stop War Room continuation immediately.
2. Identify committed and uncommitted War Room artifacts separately.
3. Preserve evidence only long enough to show the user what will be deleted.
4. Ask explicit confirmation before destructive removal of committed files.
5. Prefer `git rm -r asturlab/operations/asturlab-os` for committed War Room OS files on the active branch.
6. Remove parked/untracked War Room drift after confirmation.
7. Continue only the second-brain build from the June 15 brief.

## Exact safety phrasing used

If committed War Room files exist, say what will be removed and require explicit confirmation, e.g.

`confirm remove War Room OS`

Do not silently delete committed files or parked artifacts.

## Pitfall

Do not convert user correction into another parking/archive workflow by default. If the user says they will start War Room fresh later, the active branch should not carry mistaken War Room scaffold as future work unless they explicitly ask to keep it.
