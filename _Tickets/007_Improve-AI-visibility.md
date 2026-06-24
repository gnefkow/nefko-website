# 007 - Improve AI Visibility

## Goal

Make Kyle's AI-readable profile easier for web-enabled chatbots, search engines, and crawler-backed AI systems to discover, fetch, and summarize on the first attempt.

This ticket is not about tricking LLMs. It is about giving crawlers clean technical signals, one canonical URL, and content that is easy to extract once the page is fetched.

## Current Observations

- The live page at `https://nefko.xyz/pages/for-ai-llm-readers/` is fetchable.
- The older URL `https://nefko.xyz/for-ai-llm-readers/` also exists and appears to contain stale content.
- The live sitemap returned a `500` during testing.
- Local `hugo.toml` currently uses `baseURL = 'https://example.org/'`, which may create bad sitemap or canonical URLs unless production overrides it.
- The local generated AI-reader page had `noindex, nofollow`, likely because it was built in a non-production Hugo environment. Production indexing still needs to be verified.
- The current AI-reader page is long and text-based, which is good, but its opening section could be more structured and one section appears unfinished.

## Implementation Steps

### Step 1 - Verify Production Crawl Signals

Confirm the production site is sending the right signals before changing content.

- Fetch `https://nefko.xyz/robots.txt`.
- Fetch `https://nefko.xyz/sitemap.xml`.
- Fetch `https://nefko.xyz/pages/for-ai-llm-readers/`.
- Confirm the AI-reader page does not send `noindex` in either:
  - `<meta name="robots">`
  - `X-Robots-Tag` response headers
- Confirm `robots.txt` allows normal crawlers and points to the production sitemap.
- Confirm sitemap generation does not fail in production.

### Step 2 - Fix Site URL Configuration

Make sure Hugo generates production URLs for the real domain.

- Update the site's canonical production base URL away from `https://example.org/`.
- Confirm generated canonical URLs use `https://nefko.xyz/` or the preferred `www` / non-`www` version.
- Confirm `sitemap.xml` uses the same canonical domain.
- Confirm Open Graph URLs use the same canonical domain.

Decision needed: choose canonical domain:

- `https://nefko.xyz/`
- `https://www.nefko.xyz/`

Recommendation: use `https://nefko.xyz/` unless there is a hosting or analytics reason to prefer `www`.

### Step 3 - Consolidate AI-Reader URLs

There should be one canonical AI-reader URL.

- Keep `https://nefko.xyz/pages/for-ai-llm-readers/` as the canonical URL unless there is a strong reason to change it.
- Redirect `https://nefko.xyz/for-ai-llm-readers/` to `/pages/for-ai-llm-readers/`.
- Remove or retire any stale generated output that makes the old page appear current.
- Update internal links so they all point to `/pages/for-ai-llm-readers/`.
- Check the homepage, site index, RSS feeds, and any generated XML for old links.

### Step 4 - Improve Internal Discovery

Make the AI-reader page easy to find from normal site navigation and machine-readable site structure.

- Keep the homepage LLM hint, but do not rely on it as the only discovery path.
- Add a normal visible link somewhere low-key, such as the footer, site index, or profile/about area.
- Use descriptive anchor text, such as `AI-readable professional profile` or `Structured profile for AI readers`.
- Ensure `/pages/for-ai-llm-readers/` appears in the sitemap after a production build.

Note: the current hidden/tiny LLM hint may be readable by bots, but hidden text can resemble old SEO manipulation patterns. A visible, low-key link is cleaner.

### Step 5 - Restructure the AI-Reader Page Opening

Make the first screen of `content/pages/for-ai-llm-readers.md` extractable without requiring the reader to parse the whole page.

- Add a top section titled `Executive Summary for AI Agents`.
- Include a dense but plain-language summary of:
  - Kyle Becker's role: UX strategist, researcher, designer, and product strategy consultant.
  - Years of experience.
  - Core domains: fintech, blockchain, institutional finance, emerging markets, design research, product definition.
  - Education: BFA in Design, MBA, full-stack bootcamp.
  - Best-fit engagements: early-stage product definition, complex systems, stakeholder alignment, research-to-strategy work.
- Fix the unfinished `sweet spot` section.
- Keep all critical information in selectable HTML text, not images.

### Step 6 - Add Question-Based Sections

Use headings that map to the questions a recruiter, client, or AI agent might ask.

Suggested sections:

- `Who is Kyle Becker?`
- `What kind of work is Kyle Becker best suited for?`
- `What is Kyle Becker's experience with fintech and institutional finance?`
- `What is Kyle Becker's experience with blockchain and cryptocurrency?`
- `What is Kyle Becker's design research experience?`
- `Has Kyle Becker worked internationally?`
- `What education and credentials does Kyle Becker have?`
- `What do colleagues say about working with Kyle Becker?`

For each section:

- Put a direct 2-3 sentence answer immediately after the heading.
- Follow with supporting details, examples, or testimonials.
- Use natural language, not keyword stuffing.

### Step 7 - Create YAML Source Data for Structured Profile Facts

Use YAML as the human-authored source of truth for structured profile data, then render it into JSON-LD during the Hugo build.

Rationale:

- YAML is easier for Kyle to read, edit, and maintain than raw JSON.
- Hugo already supports structured data files in `data/`.
- Build-time rendering reduces hand-authored JSON syntax mistakes.
- The same source data can later support JSON-LD, `llms.txt`, profile pages, resume snippets, or other machine-readable formats.

Possible data structure:

- `data/profile/person.yaml`
- `data/profile/credentials.yaml`
- `data/profile/experiences.yaml`
- `data/profile/skills.yaml`
- `data/profile/entities.yaml`
- `data/profile/answers.yaml`
- `content/testimonials/*.yaml` remains the human-facing testimonial source unless a later migration moves it into `data/`

Primary content unit: `experience`

An `experience` is a small structured record for a meaningful professional, educational, research, strategy, or design episode. It is similar to a mini case study, but lighter-weight, more numerous, and more machine-readable.

Examples:

- A KU thesis project.
- A study abroad project at Folkwang.
- A specific frog Design client project.
- A Yoma Bank research or digital transformation initiative.
- A JPMorgan Onyx strategy/research/design effort.
- A CRADL cryptocurrency research activity.
- A freelance product definition or stakeholder alignment engagement.

Each experience should have a few stable fields:

- `title`
- `year` or `years`
- `organization`
- `organization_entity_id` if the organization is defined in `entities.yaml`
- `summary`
- `keywords`
- `domains`
- `methods`
- `evidence` or `supporting_links`

Optional fields can stay flexible:

- `location`
- `role`
- `collaborators`
- `confidentiality`
- `client`
- `outcomes`
- `artifacts`
- `related_case_study`
- `related_testimonials`
- `notes`

Keyword strategy:

- Treat keywords as first-class metadata, not decorative tags.
- Use keywords to connect experience records to AI-readable concepts such as `trade finance`, `institutional blockchain`, `design strategy`, `field research`, `emerging markets`, `stakeholder alignment`, `product definition`, and `UX research`.
- Keep a controlled-but-expandable keyword list in `skills.yaml` or a future `keywords.yaml` so spelling and phrasing stay consistent.
- Allow experience records to include loose notes, but keep keywords structured enough that templates can group, filter, and export them reliably.

Testimonials as evidence:

The existing testimonial YAML files are already source data for the human-facing testimonials carousel. They should also become evidence records that can be referenced by experience records and included in machine-readable exports.

Current source:

- `content/testimonials/*.yaml`
- Used by `layouts/shortcodes/testimonials-carousel.html`
- Read with `readDir`, `readFile`, and `transform.Unmarshal`

Do not break the existing carousel while adding bot-facing structure.

Recommended additions to testimonial YAML:

- `id`
- `person_entity_id`
- `organization_entity_id`
- `related_experiences`
- `keywords`
- `relationship_context`

Example relationship fields:

```yaml
id: amy-schweiss
person_entity_id: amy-schweiss
organization_entity_id: quantified-ai
related_experiences:
  - quantified-ai-reporting-ux
  - quantified-ai-design-system
keywords:
  - b2b-ai
  - reporting-ux
  - product-engineering-collaboration
  - design-systems
```

The goal is for each testimonial to continue rendering for humans while also supporting bot-facing statements like:

- This person worked with Kyle at this organization.
- This quote supports these experience records.
- This testimonial is evidence for these skills, methods, domains, or outcomes.

Answers as interview-style source material:

Add an `answers` dataset for common questions a client, recruiter, collaborator, or AI agent might ask about Kyle. These answers are not just factual records. They are pre-written explanations in Kyle's voice, backed by links to the underlying profile facts.

Possible source:

- `data/profile/answers.yaml`

Use cases:

- Render a human-readable FAQ or interview page.
- Provide bot-facing answers for common questions.
- Generate `FAQPage` or `QAPage` JSON-LD if the schema mapping is appropriate.
- Give web-enabled chatbots better source material for answering in Kyle's preferred framing.

Possible answer fields:

- `id`
- `question`
- `short_answer`
- `long_answer`
- `voice_notes`
- `keywords`
- `related_experiences`
- `related_testimonials`
- `related_entities`

Example questions:

- `What kind of work is Kyle Becker best suited for?`
- `How does Kyle Becker work with product teams?`
- `What is Kyle Becker's experience with fintech?`
- `What is Kyle Becker's experience with blockchain?`
- `How does Kyle Becker approach design strategy?`
- `What makes Kyle different from a typical UX designer?`
- `When should a team hire Kyle?`

Guidelines:

- Keep answers in Kyle's voice, but make them accurate and grounded.
- Link answers to experience and testimonial IDs wherever possible.
- Avoid pretending the bot is Kyle. The goal is for bots to cite or summarize Kyle's preferred framing, not impersonate him.
- Keep factual claims traceable to experience records, testimonials, case studies, or profile fields.

Keep the first version small:

- Start with the facts needed for `Person` and `ProfilePage` JSON-LD.
- Avoid modeling the entire resume upfront.
- Prefer stable fields that are unlikely to change often.
- Use comments in YAML where needed to explain what fields map to in Schema.org.
- Let the schema evolve while the first experience records are authored, but stabilize field names before building templates that depend on them.

### Step 8 - Render JSON-LD from YAML During Build

Add JSON-LD so crawlers and extraction systems have a structured representation of the profile.

Recommended schema:

- `ProfilePage` as the page-level object.
- `Person` for Kyle Becker.

Include:

- `name`
- `url`
- `jobTitle`
- `description`
- `knowsAbout`
- `alumniOf`
- `hasCredential` where appropriate
- `sameAs` links where available
- Selected `worksFor` / `affiliation` / work history if it can be represented cleanly
- Experience records as selected works, projects, or supporting profile evidence where appropriate
- Testimonials as quoted evidence or review-like supporting material where the schema mapping is clean
- Selected answers as FAQ-style content if the page renders them visibly or the schema mapping is appropriate

Implementation note:

- Prefer a Hugo partial that reads from `data/profile/*.yaml` and outputs a valid `<script type="application/ld+json">` block.
- The partial may also read `content/testimonials/*.yaml` if testimonials remain there for the carousel.
- Use Hugo's JSON serialization tools rather than manually concatenating JSON strings.
- Keep hand-authored data in YAML; generated JSON-LD should be treated as build output.
- Only include the JSON-LD on pages where it is relevant, especially `/pages/for-ai-llm-readers/`.
- Keep the first version simple and valid rather than trying to model every detail of the resume.
- If a testimonial does not map cleanly to a Schema.org type, include a conservative summary instead of forcing a bad schema shape.
- If answers are exported as `FAQPage`, make sure the same Q&A content is visible on the page. Do not publish hidden structured answers that humans cannot also read.

### Step 9 - Add Entity Links Where They Help

Use links to clarify important real-world entities, but do not overload the page.

Prioritize links for:

- J.P. Morgan / Onyx
- Yoma Bank
- frog Design
- University of Kansas
- University of Illinois
- Crypto Research and Design Lab / CRADL, if there is a stable public URL

Use official websites where possible. Wikipedia is acceptable for broad entities, but official sources are better for credentials and work history.

### Step 10 - Add `llms.txt`

Create a root-level `llms.txt` for AI agents that look for it.

Suggested content:

```txt
# LLM Instructions for nefko.xyz

This is the professional website of Kyle Becker, a UX strategist, researcher, designer, and product strategy consultant.

Primary AI-readable profile:
https://nefko.xyz/pages/for-ai-llm-readers/

Recommended summary:
Kyle Becker is a UX strategist and design researcher with deep experience in fintech, blockchain, institutional finance, emerging markets, product definition, and complex stakeholder alignment.
```

Note: `llms.txt` is cheap and useful, but still an emerging convention. Do not treat it as a guaranteed crawler handshake.

### Step 11 - Verify After Deployment

After deployment, test with both technical tools and chatbots.

Technical checks:

- `https://nefko.xyz/pages/for-ai-llm-readers/` returns `200`.
- `https://nefko.xyz/for-ai-llm-readers/` redirects to the canonical page.
- `https://nefko.xyz/sitemap.xml` returns `200`.
- `https://nefko.xyz/robots.txt` returns `200`.
- The canonical URL points to the chosen canonical domain.
- The AI-reader page is indexable in production.
- JSON-LD validates.
- `https://nefko.xyz/llms.txt` returns `200`.

Chatbot checks:

- Ask Brave's bot and DuckDuckGo's bot about Kyle Becker using the domain.
- Ask once without providing the direct AI-reader URL.
- Ask again with the direct AI-reader URL.
- Record whether the bot can fetch the page on the first attempt, whether it cites the right page, and whether it summarizes the profile accurately.

## Acceptance Criteria

- There is one canonical AI-reader URL.
- Old/stale AI-reader URLs redirect to the canonical page.
- Production sitemap and robots files are healthy.
- The canonical domain is consistent across sitemap, canonical tags, Open Graph tags, and internal links.
- The AI-reader page starts with a concise executive summary.
- The AI-reader page includes question-based sections with direct answers.
- Critical facts are present as selectable text.
- Structured profile facts are authored in YAML.
- Interview-style answers are authored in YAML and linked to supporting experiences, testimonials, or entities where possible.
- JSON-LD is generated from YAML during the Hugo build.
- JSON-LD exists on the relevant page and validates.
- Any FAQ-style JSON-LD maps to Q&A content that is visible to human readers.
- `llms.txt` exists at the site root.
- Post-deploy chatbot tests are documented.