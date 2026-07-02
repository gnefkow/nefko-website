This document is an outline of the strategies the UX Portfolio site uses for AI routing (sometimes called Generative Engine Optimization, or GEO). It is a **living document**: high-level architecture, update workflows, Hugo build behavior, and go-live checks — not an exhaustive file inventory.

Related work is tracked under ticket **007** (AI visibility) and sub-ticket **7.6** (Person JSON-LD).

---

## What is in place

The site exposes Kyle's professional identity to crawlers and AI agents through **layered, machine-readable surfaces**:

| Layer | Purpose | Primary URL |
|---|---|---|
| **Discovery hints** | Tell agents where to start | `/llms.txt`, `/robots.txt` |
| **Unified catalog** | Lightweight index of all structured resources | `/ai/index.json` |
| **Profile JSON** | Structured identity record | `/ai/profile.json` |
| **Experience index** | Scan list of work episodes (cards + pointers) | `/ai/experiences.json` |
| **Experience payloads** | Long narrative per episode | `/experiences/<slug>/index.json` |
| **Testimonial index** | Scan list of collaborator testimonials | `/ai/testimonials.json` |
| **Testimonial payloads** | Full quote + attribution per person | `/testimonials/<slug>/index.json` |
| **Conversation index** | Scan list of published conversations | `/ai/conversations.json` |
| **Conversation payloads** | Full transcript per article | `/blog/conversations/<slug>/conversation.json` |
| **Long-form prose** | Narrative bio for LLMs that fetch a page | `/pages/for-ai-llm-readers/` |
| **JSON-LD** | Schema.org entities embedded in HTML `<head>` | Homepage + AI-reader page (view source) |
| **Topic slices** | Conversation groupings by topic (Python-generated) | `/ai/topics/<topic>.json` |

**Design principle:** The catalog is a **table of contents**, not a dump. Heavy data lives in dedicated JSON endpoints; the catalog points to them via `json_url` or `canonical_url`.

**Current catalog shape (5 resources):**

1. `for_ai_llm_readers` → long-form prose at `/pages/for-ai-llm-readers/` (`canonical_url`)
2. `profile` → structured identity at `/ai/profile.json` (`json_url`)
3. `experience_index` → `/ai/experiences.json` (with `count`)
4. `conversation_index` → `/ai/conversations.json` (with `count`)
5. `testimonial_index` → `/ai/testimonials.json` (with `count`)

Individual conversations, topic indexes, and per-testimonial payloads are **not** listed as top-level catalog rows — the catalog points to each section index; agents follow `json_url` hops from there.

---

## High-level architecture

```
YOU EDIT                         BUILD STEP                    LIVE OUTPUT
────────                         ──────────                    ───────────

data/profile/person.yaml         ──┐
content/experiences/*.md         ──┤
content/testimonials/*/          ──┼──►  hugo --environment production
  testimonial.yaml               ──┤         │
data/ai/endpoints.yaml           ──┤         ├──► /ai/index.json               (catalog)
data/conversations/*.yaml        ──┘         ├──► /ai/profile.json              (profile payload)
data/profile/experience_order.yaml           ├──► /ai/experiences.json          (experience cards)
                                             ├──► /experiences/<slug>/            (quiet HTML page)
                                             ├──► /experiences/<slug>/index.json  (experience payload)
                                             ├──► /ai/testimonials.json           (testimonial cards)
                                             ├──► /testimonials/<slug>/           (quiet HTML page)
                                             ├──► /testimonials/<slug>/index.json (testimonial payload)
                                             ├──► /ai/conversations.json          (conversation cards)
                                             ├──► JSON-LD in HTML head            (Person, OrganizationRole)
                                             └──► /llms.txt, sitemap, etc.

data/conversations/*.yaml    ──┐
content/blog/conversations/  ──┼──►  Python Phase 2 (conversations only)
                               │
                               ├──► conversation.json per article
                               └──► static/ai/topics/*.json
```

**Ingredients / oven / cake:**

| Folder | Role |
|---|---|
| `data/`, `content/` | Ingredients — what you edit |
| `layouts/` | Oven — Hugo templates that bake JSON, HTML, JSON-LD |
| `public/` | Cake — build output; never hand-edit |

**Single owner for the catalog and section indexes:** Hugo. Do not hand-edit `public/ai/index.json` or recreate `static/ai/index.json` — those are build output.

**Stable Person identity:** JSON-LD and conversation metadata share `@id: https://nefko.xyz/#kyle-becker` so crawlers can link authorship across pages.

---

## Source data (what humans edit)

### Profile identity — `data/profile/person.yaml`

Lean identity card: name, job title, description, `knowsAbout`, `worksFor`, education (`alumniOf`), certifications (`hasCredential`), `sameAs`.

**Not a CV.** Degrees/certs live here; work episodes live in `content/experiences/`.

### Work history — `content/experiences/*.md` + `data/profile/experience_order.yaml`

**One markdown file per episode.** Everything is an "experience" — employment, freelance, advisory, research, teaching. Use `type:` as a loose label, not a routing bucket.

**Front matter (card fields — scannable metadata):**

- `id`, `title`, `role`, `organization`, `years`, `start_year`, `end_year`
- `summary`, `domains`, `keywords`, `methods`
- `related_case_study` (optional link to a polished portfolio case study)
- `related_testimonials` (optional list of testimonial slugs — resolved to pointer records with `json_url` at build time)
- `status: published` | `draft` — draft records are excluded from all AI output

**Markdown body (narrative — optional, can grow over time):**

- Write long-form prose under `##` headings (e.g. `## Project overview`, `## Outcome`, `## Worldview`)
- Hugo parses headings into structured `narrative` keys in JSON — **do not duplicate narrative in front matter**
- Stub episodes can use `...coming soon` as body until narrative is written

**`data/profile/experience_order.yaml`** — optional explicit display order; anything omitted sorts by `start_year` descending.

**`content/experiences/_index.md`** — section config only (`build.render: never`, `build.list: never`). Cascades `html` + `json` outputs to child pages. There is **no public `/experiences/` listing page** — episodes are quiet, crawlable pages.

### Endpoint copy — `data/ai/endpoints.yaml`

Human-edited titles and descriptions for Hugo-generated JSON feeds (`catalog`, `profile`, `experiences`, `testimonials`, `conversations`). Layouts read from `site.Data.ai.endpoints`.

### Testimonials — `content/testimonials/<slug>/`

**One leaf bundle per collaborator.** The quote data lives in a single YAML file; Hugo publishes quiet HTML + JSON from the same source.

**Bundle structure:**

```
content/testimonials/tricia-wang/
  index.md           # minimal stub (status: published)
  testimonial.yaml   # single source of truth — names, roles, quotes, tags
```

**`testimonial.yaml` fields (human-edited):**

- `first-name`, `last-name`, `photo`
- `worked-together` (title, company, relationship)
- `tags`
- `full-quote`
- `key-quotes` (versioned excerpts for carousel and case-study quote blocks)

**Optional publish gate:** `status: published` on `index.md`. Default: published if absent.

**`content/testimonials/_index.md`** — section config only (`build.render: never`, `build.list: never`). Cascades `html` + `json` outputs to child pages. There is **no public `/testimonials/` listing page**.

**Human UI:** Homepage carousel and case-study quote blocks read the same `testimonial.yaml` via `layouts/_partials/func/read-testimonial-data.html`. No quote copy-paste into experiences or case studies.

**Cross-references (build-time, no duplicate maintenance):**

- Experience `related_testimonials: [tricia-wang]` → resolved to `{ id, name, canonical_url, json_url }` pointers in experience JSON
- Testimonial payloads include derived `related_experiences` — reverse lookup from all published experiences that list this slug

### Conversations — `data/conversations/<slug>.yaml`

Metadata for blog conversations: title, summary, topics, keywords, URLs, `status`. Must be **`published`** to appear in `/ai/conversations.json`.

Human-readable page + full transcript payload live under `content/blog/conversations/<slug>/`.

### Not yet implemented (ticket 007 backlog)

- `data/profile/credentials.yaml`, `entities.yaml`, `answers.yaml` — planned; some fields are inlined in `person.yaml` for now.

---

## What Hugo does at build time

Run: `hugo --environment production` (use `guest` locally only if you intentionally mirror dev behavior).

### 1. Unified catalog — `/ai/index.json`

- **Trigger:** `content/ai/catalog/index.md` → layout `layouts/ai-index.json.json`
- **Logic:** `layouts/_partials/func/get-ai-catalog-resources.html`
- **Assembles:** for-ai-llm-readers entry, profile entry, experience index entry, conversation index entry, testimonial index entry

### 2. Profile JSON — `/ai/profile.json`

- **Trigger:** `content/ai/profile/index.md` → layout `layouts/profile.json.json`
- **Logic:** `layouts/_partials/func/profile-json-payload.html` (reads `data/profile/person.yaml`)

### 3. Experience index — `/ai/experiences.json`

- **Trigger:** `content/ai/experiences/index.md` → layout `layouts/experiences.json.json`
- **Logic:** `layouts/_partials/func/get-profile-experiences.html`
- **Each row includes:** card fields + `canonical_url` + `json_url` pointing at the per-episode payload

### 4. Per-experience outputs (same source file)

- **Trigger:** each `content/experiences/<slug>.md` (cascade from `_index.md`)
- **HTML:** `layouts/experiences/single.html` → `/experiences/<slug>/`
- **JSON:** `layouts/experiences/single.json.json` → `/experiences/<slug>/index.json`
- **Payload logic:** `layouts/_partials/func/experience-json-payload.html`
- **Narrative parsing:** `layouts/_partials/func/experience-narrative-from-content.html` (splits body on `##` headings)

### 5. Testimonial index — `/ai/testimonials.json`

- **Trigger:** `content/ai/testimonials/index.md` → layout `layouts/testimonials.json.json`
- **Logic:** `layouts/_partials/func/get-testimonials.html`
- **Each row includes:** name, organization, tags, summary excerpt, `canonical_url`, `json_url`

### 6. Per-testimonial outputs (same bundle)

- **Trigger:** each `content/testimonials/<slug>/index.md` (cascade from `_index.md`)
- **HTML:** `layouts/testimonials/single.html` → `/testimonials/<slug>/`
- **JSON:** `layouts/testimonials/single.json.json` → `/testimonials/<slug>/index.json`
- **Payload logic:** `layouts/_partials/func/testimonial-json-payload.html` (reads `testimonial.yaml` in bundle)
- **Data reader:** `layouts/_partials/func/read-testimonial-data.html` (shared with shortcodes)

### 7. Conversation index — `/ai/conversations.json`

- **Trigger:** `content/ai/conversations/index.md` → layout `layouts/conversations.json.json`
- **Logic:** `layouts/_partials/func/get-profile-conversations.html` (reads `data/conversations/*.yaml`)

### 8. JSON-LD in HTML `<head>`

- **Wiring:** `layouts/_partials/head-additions.html` (homepage + `/pages/for-ai-llm-readers/` only)
- **Profile:** `json-ld-profile.html` → `ProfilePage` + `Person` from `person.yaml`
- **Work history:** `json-ld-experiences.html` → `@graph` of `OrganizationRole` nodes from published experience pages

**Hugo 0.157 quirk:** JSON placed directly inside `<script type="application/ld+json">` gets double-encoded. Partials emit the full script tag via `printf` + `safeHTML` — do not remove that workaround without re-testing view-source output.

**Hugo leaf-bundle quirk:** Do not put multiple sibling `.md` files directly under `content/ai/` (e.g. `content/ai/index.md` + `content/ai/experiences.md`). A leaf `index.md` swallows siblings. AI endpoint triggers live in separate subfolders: `content/ai/catalog/`, `content/ai/profile/`, `content/ai/experiences/`, `content/ai/testimonials/`, `content/ai/conversations/`.

**Testimonial bundle quirk:** Flat `content/testimonials/<slug>.yaml` files do not become Hugo pages in this setup. Each testimonial must be a leaf bundle (`<slug>/index.md` + `<slug>/testimonial.yaml`) for HTML and JSON routing to work.

### 9. Everything else

Normal Hugo: markdown pages, case studies, sitemap, `static/llms.txt`, etc.

---

## Conversation pipeline (Python, not Hugo)

For new conversation articles only. Full process: `conversation-processing/_how-to-process-conversations.md`.

| Phase | Script | Creates |
|---|---|---|
| 1 | `phase1_generate_conversation_page.py` | Human markdown page + `data/conversations/<slug>.yaml` |
| 2 | `phase2_generate_json.py` | `conversation.json` + `static/ai/topics/*.json` |

Phase 2 **does not** write the catalog or conversation index. After Phase 2, run Hugo so `/ai/index.json` and `/ai/conversations.json` pick up the conversation.

**Validate:**

```bash
python3 conversation-processing/scripts/validate_conversation.py <slug> --require-json --check-build
```

(`--check-build` requires a Hugo build first and confirms the slug appears in `public/ai/conversations.json`.)

---

## How to update things

### Change positioning, credentials, or expertise tags

1. Edit `data/profile/person.yaml`
2. `hugo --environment production`
3. Verify JSON-LD in view-source on `/` and profile entry in `/ai/index.json`

### Add or edit a work episode

1. Add/edit `content/experiences/<slug>.md`
   - Front matter: card fields + `status: published`
   - Body: narrative under `##` headings (optional)
2. Optionally add `<id>` to `data/profile/experience_order.yaml`
3. Hugo build → check:
   - `/ai/experiences.json` row count
   - `/experiences/<slug>/index.json` payload
   - catalog `kyle-becker-experiences` `count`

### Add or edit a testimonial

1. Edit `content/testimonials/<slug>/testimonial.yaml` (quote text, attribution, tags, key-quotes)
2. Ensure `content/testimonials/<slug>/index.md` has `status: published` (or omit status to default to published)
3. Hugo build → check:
   - `/ai/testimonials.json` row count
   - `/testimonials/<slug>/index.json` payload
   - catalog `kyle-becker-testimonials` `count`
4. To link a testimonial to a work episode, add the slug to `related_testimonials` on the experience front matter — pointers resolve automatically at build time

### Publish a conversation

1. Complete Phase 1 + Phase 2 (conversation pipeline)
2. Ensure `data/conversations/<slug>.yaml` has `status: published`
3. Hugo build → slug appears in `/ai/conversations.json`; catalog includes `conversation_index` if count > 0

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
| Catalog shape | `count: 5` — types: `for_ai_llm_readers`, `profile`, `experience_index`, `conversation_index`, `testimonial_index` |
| Profile JSON | `public/ai/profile.json` parses as JSON |
| Experience index | `public/ai/experiences.json` — `count` matches published experience pages |
| Per-experience JSON | `public/experiences/<slug>/index.json` exists for each published episode |
| Testimonial index | `public/ai/testimonials.json` — `count` matches published testimonial bundles |
| Per-testimonial JSON | `public/testimonials/<slug>/index.json` exists for each published testimonial |
| Cross-ref resolution | Experience rows with `related_testimonials` emit pointer objects (not bare slugs); testimonial payloads include derived `related_experiences` |
| Conversation index | `public/ai/conversations.json` — each published slug in `data/conversations/` listed |
| No section list pages | `public/experiences/index.html` and `public/testimonials/index.html` should **not** exist |

Quick Python spot-check:

```bash
python3 -c "import json; d=json.load(open('public/ai/index.json')); print(d['count'], [r['type'] for r in d['resources']])"
python3 -c "import json; d=json.load(open('public/ai/experiences.json')); print(d['count'], d['experiences'][0].get('json_url'))"
python3 -c "import json; d=json.load(open('public/ai/testimonials.json')); print(d['count'], d['testimonials'][0].get('json_url'))"
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
| `https://nefko.xyz/ai/profile.json` | 200, structured identity payload |
| `https://nefko.xyz/ai/experiences.json` | 200, published experiences with `json_url` per row |
| `https://nefko.xyz/ai/testimonials.json` | 200, published testimonials with `json_url` per row |
| `https://nefko.xyz/ai/conversations.json` | 200 when conversations published |
| `https://nefko.xyz/experiences/<slug>/index.json` | 200 for published episodes |
| `https://nefko.xyz/testimonials/<slug>/index.json` | 200 for published testimonials |
| `https://nefko.xyz/pages/for-ai-llm-readers/` | 200, no `noindex` in production |
| `https://nefko.xyz/robots.txt` | Allows crawl, references sitemap |

---

## Mental model for future work

| Question | Answer |
|---|---|
| Where do I edit structured facts? | `data/profile/person.yaml`, `data/conversations/*.yaml`, `data/ai/endpoints.yaml` |
| Where do I edit work episodes? | `content/experiences/<slug>.md` (one file: front matter + body) |
| Where do I edit testimonials? | `content/testimonials/<slug>/testimonial.yaml` |
| Where is the agent entry point? | `/llms.txt` → `/ai/index.json` |
| How does an agent get profile depth? | Catalog `profile` row → `/ai/profile.json` |
| How does an agent get episode depth? | `/ai/experiences.json` → follow `json_url` → `/experiences/<slug>/index.json` |
| How does an agent get testimonial depth? | `/ai/testimonials.json` → follow `json_url` → `/testimonials/<slug>/index.json`; or hop from experience `related_testimonials` pointers |
| How does an agent get conversation depth? | `/ai/conversations.json` → follow `json_url` → `/blog/conversations/<slug>/conversation.json` |
| What generates the catalog and indexes? | Hugo only |
| What still uses Python? | Conversation `conversation.json` + topic indexes |
| What ships in HTML for Google? | JSON-LD on homepage + AI-reader page |
| How do I hide incomplete data? | `status: draft` on experience, testimonial stub, or conversation metadata |
| Polished portfolio stories vs quiet episodes? | Case studies at `/case-studies/`; optional `related_case_study` link on experience row |
| How do testimonials connect to episodes? | `related_testimonials` on experience front matter; reverse `related_experiences` derived in testimonial JSON |

When in doubt: **edit markdown or YAML → Hugo build → fetch `/ai/index.json`**.

See also: `_PRDs/Experiences.md` for the product rationale behind the experiences layer.
