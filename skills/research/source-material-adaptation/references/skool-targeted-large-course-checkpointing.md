# Skool targeted large-course checkpointing

Use this when Rawan asks to extract a selected subset of courses from a large Skool classroom.

## Pattern

1. Preserve the exact requested course list first.

Write a `source/target-courses.md` file before extraction starts. This prevents scope creep when the classroom has many adjacent courses.

2. Keep the workspace course-specific unless Rawan explicitly says it belongs in a broader repo.

Default shape for a named course/community extraction:

```text
~/Documents/<course-or-community-slug>/
  README.md
  source/target-courses.md
  source/course-map.md
  source/course-tree.sanitized.json
  source/resources-index.md
  extraction/lessons/
  extraction/transcripts/vtt/
  outputs/
```

If you first place it under a broader workspace and Rawan corrects it, move it immediately and verify the old path is gone.

3. Authenticate with Rotunda, then verify member classroom state.

Authenticated Skool classroom indicators include member navigation such as Community, Classroom, Calendar, Members, Map, Leaderboards, and the user's avatar. Public state indicators include `LOG IN`, `JOIN`, and redirect to `/about`.

4. Build the selected course list from `props.pageProps.allCourses`.

Match requested titles exactly against `metadata.title`. Save only sanitized fields:

- title;
- course slug/name;
- route URL;
- module/set titles;
- module IDs;
- lesson URLs;
- content signals (`videoLink`, `videoId`, description/resource presence).

Do not save raw `__NEXT_DATA__`.

5. Fetch each selected course route before lesson extraction.

Route shape:

```text
https://www.skool.com/<group>/classroom/<course-name>
```

Then parse `props.pageProps.course.course` and `props.pageProps.course.children`. Sets may contain lesson modules. Some direct modules sit at the course root and should be placed under a `(top-level lessons)` section.

6. Treat course map as phase one, not completion.

A clean course map should report:

- requested courses found / missing;
- total lessons/modules mapped;
- resource links indexed from the course tree;
- transcript/caption status as pending;
- rendered lesson-page pass as pending.

7. For large selections, run the rendered lesson-page pass with per-lesson checkpointing.

Create a deterministic script such as `extract_lesson_pages.py` in the working repo. It should:

- read `source/course-tree.sanitized.json`;
- visit each lesson URL through the authenticated Rotunda page;
- extract rendered HTML;
- parse selected module metadata from `__NEXT_DATA__`;
- parse Skool `[v2]` rich text into clean notes and links;
- write one lesson file immediately;
- update `source/lesson-page-pass-checkpoint.json` after every lesson;
- resume cleanly if interrupted;
- write a summary file at the end.

Run this as a Hermes background process with completion notification for large courses, then poll checkpoint counts rather than relying on pane output.

8. Report progress in counts, not vague status.

Example:

```text
Courses found: 21/21
Lessons mapped: 274
Rendered lesson-page pass: 35/274
Errors: 0
```

## Pitfalls

- Do not infer missing access from disabled Skool course cards. Parse authenticated page data.
- Do not treat the first course tree parse as full extraction. Many resources and rich descriptions only appear after navigating to individual lesson pages.
- Do not dump raw rich-text JSON into `course-map.md`. Convert `[v2]` lesson descriptions inside lesson files.
- Do not flatten a large Skool subset into one synthesis pass. Finish map and rendered page extraction first.
- Do not bury a course-specific extraction under a broader workspace after Rawan tells you it should be separate.
