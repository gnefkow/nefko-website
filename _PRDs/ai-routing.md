This document is an outline of the strategies the UX Portfolio site uses for AI routing (sometimes called Generative Engine Optimization, or GEO). It is a **tomorrow document**: high-level architecture, update workflows, Hugo build behavior, and go-live checks — not an exhaustive file inventory.

Related work is tracked under ticket **007** (AI visibility) and sub-ticket **7.6** (Person JSON-LD).

---

## What is in place

The site exposes Kyle's professional identity to crawlers and AI agents through **layered, machine-readable surfaces**:

| Layer | Purpose | Primary URL |
|---|---|---|
| **Discovery hints** | Tell agents where to start | `/llms.txt`, `/robots.txt` |
| **Unified catalog** | Lightweight index of all structured resources | `/ai/index.json` |
| **Full payloads** | Detailed records agents fetch after reading the catalog | `/ai/experiences.json`, `/blog/.../conversation.json` |
| **Long-form prose** | Narrative bio for LLMs that fetch a page | `/pages/for-ai-llm-readers/` |
| **JSON-LD** | Schema.org entities embedded in HTML `<head>` | Homepage + AI-reader page (view source) |
| **Topic slices** | Conversation groupings by topic | `/ai/topics/<topic>.json` |

**Design principle:** The catalog is a **table of contents**, not a dump. Heavy data lives in dedicated JSON endpoints; the catalog points to them via `json_url` or `canonical_url`.

---

## High-level architecture

```
YOU EDIT (YAML, markdown)          BUILD STEP              LIVE OUTPUT
─────────────────────────          ──────────              ───────────

data/profile/person.yaml     ──┐
data/profile/experiences/*   ──┼──►  hugo --environment production
data/conversations/*.yaml    ──┘         │
                                         ├──► /ai/index.json          (catalog)
                                         ├──► /ai/experiences.json    (full work history)
                                         ├──► JSON-LD in HTML head     (ProfilePage, Person, OrganizationRole)
                                         └──► /llms.txt, pages, sitemap (unchanged pattern)

data/conversations/*.yaml    ──┐
content/blog/conversations/  ──┼──►  Python Phase 2 (conversations only)
                                 │
                                 ├──► conversation.json per article
                                 └──► static/ai/topics/*.json
```

**Single owner for the catalog:** Hugo. Do not hand-edit `public/ai/index.json` or recreate `static/ai/index.json` — those are build output.

**Stable Person identity:** JSON-LD and conversation metadata share `@id: https://nefko.xyz/#kyle-becker` so crawlers can link authorship across pages.

---

## Source data (what humans edit)

### Profile identity — `data/profile/person.yaml`

Lean identity card: name, job title, description, `knowsAbout`, `worksFor`, education (`alumniOf`), certifications (`hasCredential`), `sameAs`.

**Not a CV.** Degrees/certs live here; work episodes live in `experiences/`.

### Work history — `data/profile/experiences/` + `experience_order.yaml`

- **One YAML file per episode** (tenure or, later, client project).
- **`experience_order.yaml`** — optional explicit display order; anything omitted sorts by `start_year` descending.
- **`status: draft`** excludes a record from all Hugo output until set to **`published`**.

**Tenure vs project (future):** Keep both in the same folder. Tenures use `type: employment`; client projects use `type: project` + `parent_experience_id` pointing at the tenure (e.g. `frog-austin-ey` → `frog-austin`).

### Conversations — `data/conversations/<slug>.yaml`

Metadata for blog conversations: title, summary, topics, keywords, URLs, `status`. Must be **`published`** to appear in `/ai/index.json`.

Human-readable page + full transcript payload live under `content/blog/conversations/<slug>/`.

### Not yet implemented (ticket 007 backlog)

- `data/profile/credentials.yaml`, `entities.yaml`, `answers.yaml` — planned; some fields are inlined in `person.yaml` for now.

---

## What Hugo does at build time

Run: `hugo --environment production`

### 1. Unified catalog — `/ai/index.json`

- **Trigger:** `content/ai/index.md` → layout `layouts/ai-index.json.json`
- **Logic:** `layouts/_partials/func/get-ai-catalog-resources.html`
- **Assembles:** profile entry, experience index entry, published conversations, topic index links (only if `static/ai/topics/<topic>.json` exists)

### 2. Experience payload — `/ai/experiences.json`

- **Trigger:** `content/ai/experiences.md` → layout `layouts/experiences.json.json`
- **Logic:** `layouts/_partials/func/get-profile-experiences.html` (sort/filter published records)

### 3. JSON-LD in HTML `<head>`

- **Wiring:** `layouts/_partials/head-additions.html` (homepage + `/pages/for-ai-llm-readers/` only)
- **Profile:** `json-ld-profile.html` → `ProfilePage` + `Person` from `person.yaml`
- **Work history:** `json-ld-experiences.html` → `@graph` of `OrganizationRole` nodes linked to Person `@id`

**Hugo 0.157 quirk:** JSON placed directly inside `<script type="application/ld+json">` gets double-encoded. Partials emit the full script tag via `printf` + `safeHTML` — do not remove that workaround without re-testing view-source output.

### 4. Everything else

Normal Hugo: markdown pages, case studies, sitemap, `static/llms.txt`, etc.

---

## Conversation pipeline (Python, not Hugo)

For new conversation articles only. Full process: `conversation-processing/_how-to-process-conversations.md`.

| Phase | Script | Creates |
|---|---|---|
| 1 | `phase1_generate_conversation_page.py` | Human markdown page + `data/conversations/<slug>.yaml` |
| 2 | `phase2_generate_json.py` | `conversation.json` + `static/ai/topics/*.json` |

Phase 2 **does not** write the catalog. After Phase 2, run Hugo so `/ai/index.json` picks up the conversation.

**Validate:**

```bash
python3 conversation-processing/scripts/validate_conversation.py <slug> --require-json --check-build
```

(`--check-build` requires a Hugo build first and confirms the slug appears in `public/ai/index.json`.)

---

## How to update things

### Change positioning, credentials, or expertise tags

1. Edit `data/profile/person.yaml`
2. `hugo --environment production`
3. Verify JSON-LD in view-source on `/` and `/ai/index.json` profile entry

### Add or edit a work episode

1. Add/edit `data/profile/experiences/<id>.yaml` (`status: published` when ready)
2. Optionally add `<id>` to `data/profile/experience_order.yaml`
3. Hugo build → check `/ai/experiences.json` and catalog `kyle-becker-experiences` count

### Publish a conversation

1. Complete Phase 1 + Phase 2 (conversation pipeline)
2. Ensure `data/conversations/<slug>.yaml` has `status: published`
3. Hugo build → conversation appears in `/ai/index.json`

### Point agents at the site

- **`static/llms.txt`** — root instructions; keep the catalog URL prominent
- **`content/pages/for-ai-llm-readers.md`** — long prose + link to catalog
- **`themes/nefkoPortfolio/layouts/robots.txt`** — comments listing catalog + llms.txt (production only)

---

## Go-live and regression testing

Run after meaningful changes, before deploy.

### Build

```bash
cd Websites/ux-portfolio
hugo --environment production
```

Build must exit 0. Use `--environment production` so robots/meta/JSON-LD match live behavior.

### Catalog and payloads (local `public/`)

| Check | Command / action |
|---|---|
| Catalog exists | `public/ai/index.json` parses as JSON |
| Resource count | `count` matches expectations (profile + experiences + conversations + topics) |
| Experience payload | `public/ai/experiences.json` — `count` matches published YAML files |
| Conversation in catalog | Each published slug in `data/conversations/` has matching `id` in catalog `resources` |

Quick Python spot-check:

```bash
python3 -c "import json; d=json.load(open('public/ai/index.json')); print(d['count'], [r['type'] for r in d['resources']])"
```

### JSON-LD (view-source or extracted JSON)

| Check | Expected |
|---|---|
| Homepage | Two JSON-LD blocks: `ProfilePage`, `@graph` with Person + OrganizationRoles |
| Person `@id` | `https://nefko.xyz/#kyle-becker` |
| AI-reader page | Same JSON-LD blocks |

Optional: paste extracted JSON into [validator.schema.org](https://validator.schema.org/).

### Conversation pipeline (when conversations changed)

```bash
python3 conversation-processing/scripts/validate_conversation.py <slug> --require-json --check-build
```

### Live URLs (after deploy)

| URL | Expect |
|---|---|
| `https://nefko.xyz/llms.txt` | 200, mentions catalog |
| `https://nefko.xyz/ai/index.json` | 200, valid JSON, current `generated_at` |
| `https://nefko.xyz/ai/experiences.json` | 200, published experiences |
| `https://nefko.xyz/pages/for-ai-llm-readers/` | 200, no `noindex` in production |
| `https://nefko.xyz/robots.txt` | Allows crawl, references sitemap |

---

## Mental model for future work

| Question | Answer |
|---|---|
| Where do I edit structured facts? | `data/profile/` and `data/conversations/` YAML |
| Where is the agent entry point? | `/llms.txt` → `/ai/index.json` |
| What generates the catalog? | Hugo only |
| What still uses Python? | Conversation `conversation.json` + topic indexes |
| What ships in HTML for Google? | JSON-LD on homepage + AI-reader page |
| How do I hide incomplete data? | `status: draft` on experience YAML |

When in doubt: **edit YAML → Hugo build → fetch `/ai/index.json`**.
