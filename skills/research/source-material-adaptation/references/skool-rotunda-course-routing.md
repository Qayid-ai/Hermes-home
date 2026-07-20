# Skool + Rotunda course route discovery

Use when Rawan has logged into Skool through a Rotunda browser profile and the course cards do not click cleanly through automation.

## Pattern

1. List pages for the authenticated profile:

```bash
uvx rotunda agent pages <profile-id-or-name>
```

2. Reload and describe the classroom page:

```bash
uvx rotunda agent reload <page>
uvx rotunda agent wait <page> load
uvx rotunda agent describe <page>
```

Authenticated Skool classroom pages should show member navigation such as Community, Classroom, Calendar, Members, Leaderboards, and course cards. Public pages show LOG IN/JOIN.

3. If a course card appears disabled or click times out, do not assume no access. Skool may render course cards as sortable/disabled DOM nodes while still exposing access in page data.

4. Extract rendered HTML:

```bash
mkdir -p /tmp/skool-map
uvx rotunda agent extract --format html --output /tmp/skool-map/classroom.html <page>
```

5. Parse `#__NEXT_DATA__` rather than scraping only visible text.

Useful fields:

- `props.pageProps.allCourses[]` on classroom index pages.
- `props.pageProps.course.course` on a course route.
- `props.pageProps.course.children[]` for sets/phases and modules.
- Course route slug is usually `course.name`, not the title.
- Module route uses `?md=<module-id>`.

Route shape:

```text
https://www.skool.com/<group-slug>/classroom/<course-name>?md=<module-id>
```

Example:

```text
https://www.skool.com/im-not-you-6521/classroom/5e03fcb0?md=<module-id>
```

## Sanitisation rule

Never write raw `__NEXT_DATA__` into the course map.

It can include:

- user email;
- payment metadata;
- joined groups;
- public API keys;
- irrelevant community metadata;
- owner/member records.

Durable course maps should keep only:

- course/community name;
- course slug/id;
- phase/set titles;
- lesson/module titles;
- module IDs;
- legitimate Skool URLs;
- pending extraction fields for content type, transcript/captions, resources, and exercises.

## Pitfall

A failed click on a Skool course card is not enough evidence that access is blocked. Check the page data for `hasAccess`, `course.name`, and module children before asking Rawan to troubleshoot login again.
