# Google Workspace scoped OAuth for course resource extraction

Use this when a paid course extraction has many Google Drive, Docs, or Sheets resources and public export only captures a minority of attached files.

## Why this exists

Course worksheets and resource folders are first-class course material. If Skool lessons link to private Google Docs, Sheets, or Drive folders, do not mark the lesson extraction complete just because the links are indexed. Set up Google OAuth with the narrowest scope needed, then export/download the resources lesson-by-lesson.

For course extraction, prefer Drive + Docs + Sheets only unless the user explicitly asks for Gmail, Calendar, Contacts, or broader Workspace access.

## Scope set

Use only:

- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/documents`

Do not request Gmail, Calendar, Contacts, or full Workspace scopes for course-resource extraction.

## Setup sequence

1. Load the `google-workspace` skill before touching OAuth.
2. Save the Google Cloud Desktop OAuth client JSON through the skill setup script.
3. Generate an auth URL with `--services drive,sheets,docs` if the installed setup script supports it.
4. If the setup script in the current environment cannot generate the narrow URL correctly, generate the URL using the same client JSON and PKCE state shape rather than falling back to broader scopes.
5. Tell the user the `http://localhost:1` redirect failure is expected.
6. Ask the user to paste the entire redirected URL from the address bar, not a screenshot.
7. Exchange the code using the saved pending OAuth state.
8. Verify auth before re-running export.

## Fallback auth URL generation pattern

Use the Hermes Python environment, not system Python, when dependencies are already installed there:

```bash
${HERMES_AGENT_DIR:-$HOME/.hermes/hermes-agent}/venv/bin/python - <<'PY'
import json
from pathlib import Path
from google_auth_oauthlib.flow import Flow

home = Path.home() / '.hermes'
client = home / 'google_client_secret.json'
pending = home / 'google_oauth_pending.json'
scopes = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents',
]
flow = Flow.from_client_secrets_file(
    str(client),
    scopes=scopes,
    redirect_uri='http://localhost:1',
    autogenerate_code_verifier=True,
)
url, state = flow.authorization_url(access_type='offline', prompt='consent')
pending.write_text(json.dumps({
    'state': state,
    'code_verifier': flow.code_verifier,
    'redirect_uri': 'http://localhost:1',
}, indent=2))
print(url)
PY
```

Adjust the Hermes venv path if the installation differs.

## Resource manifest statuses

For each Google resource, keep explicit status in the course resource manifest:

- `exported` — Google-native file exported successfully.
- `downloaded` — binary file downloaded successfully.
- `folder_indexed` — folder metadata/listing captured but contents not all exported yet.
- `pending_oauth` — link captured but private access requires OAuth.
- `inaccessible` — user account lacks legitimate access.

Do not claim resources were extracted when they were only indexed.

## Pitfalls

- Do not solve private Google Drive access by broadening OAuth scope without asking.
- Do not paste OAuth client secrets, token JSON, or pending OAuth JSON into chat.
- Do not store session-specific client IDs in the skill or reference file.
- Do not treat a `ModuleNotFoundError` from system Python as a durable tool failure; try the Hermes venv or run the setup script dependency install step.
