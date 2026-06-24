# 008 - Conversation Publishing Process

## Goal

Create a repeatable system for publishing Kyle's long-form AI interview conversations as faithful, readable website content with machine-readable metadata.

The end goal: when people ask about Kyle in a generic AI interface like ChatGPT, Gemini, Perplexity, or Claude, the bot can find Kyle's website and discover rich, topic-specific discussions that represent his views in his own language.

This ticket starts with a conversation between Kyle and "Herb", an AI interviewer, about the crypto industry in 2026. Raw transcript files now live in `conversation-processing/raw-transcripts/`.

Important boundary:

- This is not a system for creating new thought-leadership articles from the conversations.
- This is a system for preserving the conversation content, presenting it clearly, and decorating it with enough structure, tags, summaries, and indexes that humans and machines can find and understand it.
- Scripts should not edit the actual words inside the conversation turns. They may change labels, routing, frontmatter, metadata, indexes, and presentation structure.
- Raw transcripts are inputs only. The process must not modify files in `conversation-processing/raw-transcripts/`.

## What Good Looks Like

- Conversations are parsed, labeled, routed, and presented in a readable page format.
- Each conversation becomes a human-readable conversation page on the website.
- Each conversation also produces structured metadata and JSON files for AI readers.
- JSON files are tagged with topics, keywords, people, industries, and concepts so they are easy for crawlers and AI systems to index.
- AI readers can discover the relevant JSON files from a topic index, sitemap, or other plain, crawlable entry point.
- The system keeps Kyle's voice, ideas, ordering, examples, and claims intact.
- The workflow is understandable and repeatable for future conversations, not just this one file.
- The process includes review points for metadata and publishing status, but not automated rewriting of the transcript.
- The process is documented in `conversation-processing/_how-to-process-conversations.md` so Kyle can run it step by step.

## Source Conversation Summary

The crypto conversation currently used as the first test case contains a strong conversation candidate.

Core argument:

Crypto's mature design problem is not simply making wallets easier to use. The deeper question is whether blockchain is being applied to markets with real coordination, accounting, trust, and adoption problems. Retail crypto often mistakes usability improvements for demand, while institutional and multi-party systems may be a more natural fit for distributed accounting technology.

Potential conversation title:

`Crypto's Real Design Problem Is Not Usability`

Important themes:

- Stablecoins may transform institutional rails while remaining invisible to ordinary consumers.
- Retail crypto startups often chase wealthy markets where existing financial infrastructure already works well.
- Crypto "tribes" shape the industry: Bitcoin sovereignty advocates, DeFi traders, ReFi, NFT communities, institutional finance, payments/remittance builders, and others.
- Many retail crypto products start with a fixed crypto-native feature set and then search for a user.
- Lowering usability barriers does not create demand when people do not want the destination.
- Founders need to match their technical interests with markets they actually want to serve.
- Blockchain's strongest fit may be complex multi-party accounting systems rather than consumer novelty.
- UX strategy in crypto should emphasize ecosystem mapping, incentives, governance, auditability, trust boundaries, and existing software ecology.

## Recommended Output Model

For each raw conversation, generate one conversation folder that contains both the human page and the AI-readable payload.

Canonical folder structure:

- `content/blog/conversations/<slug>/`
- `content/blog/conversations/<slug>/index.md`
- `content/blog/conversations/<slug>/conversation.json`

Expected public URLs after Hugo builds:

- Human page: `https://nefko.xyz/blog/conversations/<slug>/`
- JSON payload: `https://nefko.xyz/blog/conversations/<slug>/conversation.json`

Working input and script locations:

- Raw transcript inputs: `conversation-processing/raw-transcripts/`
- Processing scripts: `conversation-processing/scripts/`
- Step-by-step operator guide: `conversation-processing/_how-to-process-conversations.md`

Raw transcripts should be treated as immutable source inputs. Scripts may read them, but should never overwrite, format, rename, or otherwise modify them.

### 1. Human-Readable Conversation Page

Location:

- `content/blog/conversations/<slug>/index.md`

Purpose:

- A readable presentation of the actual conversation.
- Should read like a published Q&A transcript, not a transformed article.
- Should preserve the conversation's questions, answers, order, examples, and argument.

Recommended structure:

- Frontmatter with title, description, date, participants, categories, tags, draft status, source conversation path, and AI JSON path.
- Before JSON generation, `ai_json` may be empty, omitted, or set to a clear placeholder such as `pending`.
- After JSON generation, the page generator or JSON script should update `ai_json` to the public JSON URL.
- Short contextual note explaining what the conversation is about.
- Optional table of contents generated from topics or section breaks.
- Q&A transcript with original turn content preserved.
- Speaker labels normalized to `Herb` and `Kyle`.
- Optional "Key Themes" block derived from metadata.

Content preservation rule:

- The system must not change the text inside any `Herb` or `Kyle` conversation turn.
- The system may change speaker labels, for example `Cursor` to `Herb` and `User` to `Kyle`.
- The system may add frontmatter, headings, anchors, tags, summaries, descriptions, JSON fields, and topic indexes around the conversation.
- The system should not reorder the conversation unless the raw export itself is malformed.
- The system should not synthesize Kyle's answers into new prose inside the transcript.
- If a typo, transcription artifact, or unclear phrase needs correction, that should be a manual editorial change to the source or generated page, not an automated script behavior.

### 2. Human-Editable Metadata

Location:

- Proposed: `data/conversations/<slug>.yaml`

Purpose:

- A reviewable source of truth for tags, summaries, topics, claims, and discovery metadata.
- Easier for Kyle to edit than JSON.
- Feeds both `index.md` and `conversation.json` in the generated conversation folder.

Recommended fields:

- `id`
- `title`
- `slug`
- `description`
- `date`
- `participants`
- `source_path`
- `source_sha256`
- `conversation_path`
- `status`
- `topics`
- `keywords`
- `industries`
- `concepts`
- `audiences`
- `summary`
- `key_claims`
- `notable_quotes`
- `canonical_url`
- `json_url`

### 3. Machine-Readable JSON

Location:

- Primary payload: `content/blog/conversations/<slug>/conversation.json`
- Proposed master index: `static/ai/index.json`
- Proposed topic indexes: `static/ai/topics/<topic-slug>.json`

Purpose:

- Give AI crawlers compact, structured material that is easier to fetch, parse, and cite than a long HTML page.
- Keep the AI-readable payload next to the human-readable page so the relationship is obvious in source control.
- Use master and topic indexes as discovery files that point to each conversation folder's JSON payload.

Recommended JSON fields:

```json
{
  "id": "crypto-industry-today",
  "title": "Crypto's Real Design Problem Is Not Usability",
  "canonical_url": "https://nefko.xyz/blog/conversations/crypto-industry-today/",
  "json_url": "https://nefko.xyz/blog/conversations/crypto-industry-today/conversation.json",
  "source_type": "ai_interview",
  "participants": ["Kyle Becker", "Herb"],
  "summary": "",
  "topics": [],
  "keywords": [],
  "industries": [],
  "concepts": [],
  "audiences": [],
  "key_claims": [],
  "notable_quotes": [],
  "conversation_turns": [],
  "source_files": {
    "raw_conversation": "conversation-processing/raw-transcripts/crypto-industry-today.md",
    "raw_conversation_sha256": "",
    "conversation": "content/blog/conversations/crypto-industry-today/index.md",
    "json_payload": "content/blog/conversations/crypto-industry-today/conversation.json",
    "metadata": "data/conversations/crypto-industry-today.yaml"
  },
  "last_updated": ""
}
```

## Proposed Script System

Keep the scripts small and explicit. Kyle should be able to understand what each script does without treating the pipeline as a black box.

Scripts should live in `conversation-processing/scripts/`.

The process should be split into two human-readable phases:

- **Phase 1:** Generate the human `.md` page from the raw transcript for Kyle to review.
- **Phase 2:** After Kyle approves the `.md` page, generate `conversation.json`, update discovery indexes, and write the JSON URL back into `index.md`.

### Script 1 - Parse Raw Conversation

Input:

- `conversation-processing/raw-transcripts/<conversation>.md`

Output:

- Intermediate structured data, probably JSON, in a generated or working directory.

Responsibilities:

- Parse exported conversation markdown.
- Identify speaker turns.
- Normalize speaker labels from `Cursor` and `User` to configured names like `Herb` and `Kyle`.
- Preserve turn order.
- Remove export metadata.
- Flag unclear or malformed sections rather than silently guessing.
- Do not modify the raw transcript file.

### Script 2 - Normalize Conversation Structure

Input:

- Parsed conversation data.

Output:

- Normalized conversation markdown or structured data.

Responsibilities:

- Replace exported speaker labels with configured public names, such as `Cursor` to `Herb` and `User` to `Kyle`.
- Preserve the exact text inside each conversation turn.
- Add stable turn IDs or anchors if useful.
- Add section breaks only if they are presentation wrappers, not reordering or rewriting.
- Produce a report showing counts of turns, speakers, and any malformed sections.

Important constraint:

- This script should be deterministic and should not use AI to rewrite transcript content.
- If the parser cannot confidently identify a turn, it should fail or flag the issue rather than guessing.

### Script 3 - Draft Metadata

Input:

- Normalized conversation.

Output:

- Human-editable YAML metadata.

Responsibilities:

- Generate a proposed title, description, summary, topics, keywords, industries, concepts, audiences, key claims, and notable quotes.
- Identify a recommended slug.
- Keep all summaries clearly separate from the conversation itself.
- Use canonical tag IDs from the shared taxonomy once that taxonomy exists.

Important constraint:

- Tags, claims, summaries, and quotes should be reviewable and editable.
- Metadata should help people and machines find the conversation. It should not become a substitute for the conversation.

### Script 4 - Generate Conversation Page

Input:

- Normalized conversation and reviewed metadata.

Output:

- `content/blog/conversations/<slug>/index.md`

Responsibilities:

- Create Hugo-compatible frontmatter.
- Generate a readable Q&A page.
- Preserve every speaker turn.
- Add a short contextual intro from metadata.
- Add tags and topics.
- In Phase 1, either omit the JSON link or mark it as pending.
- In Phase 2, after `conversation.json` exists, add a visible link to `conversation.json` and set the `ai_json` frontmatter field to the public JSON URL.

Frontmatter should include:

- `title`
- `description`
- `type: post`
- `date`
- `lastmod`
- `categories`
- `tags`
- `draft`
- `source_conversation`
- `ai_json`

### Script 5 - Generate AI JSON Files

Input:

- Reviewed metadata, normalized conversation, and Kyle-approved conversation page path.

Output:

- `content/blog/conversations/<slug>/conversation.json`
- Updated `static/ai/index.json`
- Updated topic files in `static/ai/topics/`

Responsibilities:

- Write one structured JSON payload inside each conversation folder.
- Maintain a master index of all AI-readable files.
- Maintain topic-level indexes so crawlers can find relevant discussions by theme.
- Include canonical URLs to the human-readable conversation page.
- Include the public URL of the colocated `conversation.json` payload.
- Include stable IDs and last-updated timestamps.
- Update `content/blog/conversations/<slug>/index.md` so the human page links to the JSON payload after it exists.

### Script 6 - Validate Outputs

Input:

- Generated markdown and JSON files.

Output:

- Terminal report.

Responsibilities:

- Confirm generated JSON parses.
- Confirm required fields exist.
- Confirm all referenced files exist.
- Confirm generated conversation frontmatter parses.
- Confirm canonical URLs and local paths are consistent.
- Warn if tags or topics are empty.
- Confirm `index.md` links to `conversation.json` after Phase 2.
- Confirm raw transcript files were not modified.
- Support a final build-output check that confirms the human page appears in `public/sitemap.xml` after Hugo builds.

### Script 7 - Update the How-To Guide

Input:

- Finalized script names and workflow.

Output:

- `conversation-processing/_how-to-process-conversations.md`

Responsibilities:

- Document exactly where Kyle should place raw transcripts.
- Document the Phase 1 command for generating the human `.md` page.
- Document the human review checkpoint.
- Document the Phase 2 command for generating JSON and indexes.
- Document validation and build checks.
- Explain that raw transcripts are never modified.

## Proposed Workflow

1. Place raw exported conversation in `conversation-processing/raw-transcripts/`.
2. Run Phase 1 script to parse the raw transcript, normalize speaker labels, draft metadata, and generate `content/blog/conversations/<slug>/index.md`.
3. Confirm the raw transcript was not modified.
4. Kyle reviews the generated `index.md` page as the human-readable source for publication.
5. Kyle reviews or edits the metadata fields that will drive tags, topic indexes, summaries, and JSON.
6. Run Phase 2 script to generate `content/blog/conversations/<slug>/conversation.json`.
7. Phase 2 updates `index.md` with the public JSON URL and visible JSON link.
8. Phase 2 updates `static/ai/index.json` and `static/ai/topics/<topic-slug>.json`.
9. Run validation script.
10. Build the Hugo site.
11. Ask Kyle whether to run the final "check it" step before pushing, deploying, or treating the build as ready.
12. If approved, run the final check to confirm generated conversation pages, colocated JSON payloads, AI index files, and sitemap inclusion are present.
13. Update `conversation-processing/_how-to-process-conversations.md` whenever the script names or steps change.

## Implementation Steps

### Step 1 - Decide Content Locations

Confirm the final folder structure before writing scripts.

Recommended:

- Raw conversations stay in `conversation-processing/raw-transcripts/`.
- Processing scripts go in `conversation-processing/scripts/`.
- The operator guide lives at `conversation-processing/_how-to-process-conversations.md`.
- Published conversation folders go in `content/blog/conversations/<slug>/`.
- Human pages go in `content/blog/conversations/<slug>/index.md`.
- Machine-readable payloads go in `content/blog/conversations/<slug>/conversation.json`.
- Reviewed conversation metadata goes in `data/conversations/<slug>.yaml`.
- Discovery indexes go in `static/ai/`.

Decision needed:

- Should `content/blog/conversations/` be visible in normal blog navigation, presented as a separate conversation section, or excluded from blog listing while remaining directly crawlable?

### Step 2 - Define the Conversation Metadata Schema

Create a small, documented schema for conversation metadata.

Recommended fields:

- `id`
- `title`
- `slug`
- `date`
- `participants`
- `source_path`
- `source_sha256`
- `status`
- `topics`
- `keywords`
- `industries`
- `concepts`
- `audiences`
- `summary`
- `key_claims`
- `notable_quotes`
- `canonical_url`
- `json_url`

Decision needed:

- Should metadata live inside the generated JSON only, or should there also be a human-editable YAML file per conversation?

Recommendation:

- Use human-editable YAML for reviewed metadata, then generate JSON from that. This matches Kyle's preference for readable source files and avoids hand-editing JSON.

### Step 3 - Build the Parser First

Start with the least subjective script.

Acceptance criteria:

- It can parse a raw transcript in `conversation-processing/raw-transcripts/`.
- It removes export metadata.
- It produces ordered speaker turns.
- It maps `Cursor` to `Herb` and `User` to `Kyle`.
- It prepares the output path `content/blog/conversations/crypto-industry-today/`.
- It fails clearly if the markdown format changes.
- It does not write changes to the raw transcript file.

### Step 4 - Build the Markdown Output for Conversations

Acceptance criteria:

- It creates a readable Q&A page.
- It preserves every question and answer.
- It adds frontmatter.
- It does not rewrite any conversation text.
- It can be run before `conversation.json` exists.

### Step 5 - Build the Metadata Drafting Step

Acceptance criteria:

- It generates a proposed title, description, summary, tags, topics, claims, and quotes.
- It marks the file as a draft requiring review.
- It separates direct quotes from model-written summaries.

### Step 6 - Build the Conversation Page Generator

Acceptance criteria:

- It generates a Hugo page bundle at `content/blog/conversations/<slug>/index.md`.
- It uses frontmatter compatible with the site.
- It includes a short contextual intro and the full Q&A.
- It preserves every question and answer in order.
- In Phase 1, it does not require `conversation.json` to exist.
- In Phase 2, it links to the colocated `conversation.json` payload.
- It does not publish automatically; generated conversation pages should start as drafts.

### Step 7 - Build the AI JSON Generator

Acceptance criteria:

- It writes valid JSON.
- It writes the primary JSON payload to `content/blog/conversations/<slug>/conversation.json`.
- It includes canonical URLs and local source references.
- It updates a master index.
- It updates topic indexes.
- It updates the human `index.md` with the JSON URL.
- It avoids keyword stuffing and uses natural conceptual tags.

### Step 8 - Add Validation

Acceptance criteria:

- Invalid JSON fails validation.
- Missing referenced files fail validation.
- Empty required fields fail validation.
- The built human page URL and JSON payload URL are predictable from the same slug.
- After Phase 2, `index.md` contains the correct `conversation.json` URL.
- Raw transcript inputs remain unchanged.
- Optional build-output validation checks `public/` after Hugo builds.
- Build-output validation confirms the human conversation URL appears in `public/sitemap.xml`.
- Build-output validation confirms the built human page links to the built JSON payload URL.
- The script reports warnings in plain language.

### Step 9 - Add Site Discovery

Connect the generated AI files to crawlable site structure.

Possible options:

- Link `static/ai/index.json` from the AI-reader page.
- Link the conversation index or specific conversation pages from the AI-reader page where relevant.
- Add a low-key "AI-readable discussions" link to `content/siteindex.md`.
- Add an `llms.txt` file later that points to the AI reader page, AI JSON index, and conversation collection.
- Ensure the colocated `conversation.json` files are reachable in production.

Decision needed:

- Should AI JSON files be linked from visible pages, from machine-oriented pages only, or both?

Recommendation:

- Link them from the AI-reader page and site index in normal visible text. Avoid hidden-only discovery.
- Follow ticket 007's broader direction: one canonical domain, healthy sitemap/robots, visible internal links, and structured data that maps to human-visible content.

### Step 10 - Add Canonical Tag Taxonomy

Create a shared, controlled vocabulary so conversation metadata uses the same concepts as profile data, testimonials, case studies, and AI-reader content.

Recommended files:

- `data/taxonomy/topics.yaml`
- `data/taxonomy/industries.yaml`
- `data/taxonomy/methods.yaml`
- `data/taxonomy/audiences.yaml`

Each canonical tag should include:

- `id`
- `label`
- `aliases`
- `description`
- `related`

Acceptance criteria:

- Conversation metadata references canonical tag IDs rather than inventing new tag strings.
- Topic indexes are generated from canonical tag IDs.
- Aliases help map loose terms like `web3`, `cryptocurrency`, and `blockchain` to the intended canonical concepts.
- The taxonomy remains small and readable in the first version.

### Step 11 - Write the Step-by-Step Guide

Document the operator workflow in `conversation-processing/_how-to-process-conversations.md`.

The guide should include:

- Where raw transcripts go.
- Which scripts to run for Phase 1.
- What Kyle should review in `index.md`.
- Which scripts to run for Phase 2.
- How the JSON URL gets written back into `index.md`.
- How to validate output.
- How to confirm the build exposes both the human page and JSON payload.
- A final "check it" step that validates the built page, built JSON, built AI index, and sitemap inclusion.
- A reminder that bots/agents should ask Kyle before running the final check, especially if Kyle is talking about pushing, deploying, publishing, or checking the build.

### Step 12 - Add Final Build Check

Add a final check process for the end of the workflow.

This check should run only after:

- Phase 1 has generated `index.md`.
- Kyle has reviewed the human-readable page and metadata.
- Phase 2 has generated `conversation.json`.
- The page is intended to be publishable, usually meaning `draft: false`.
- Hugo has built the site into `public/`.

Acceptance criteria:

- The generated human page exists in `public/blog/conversations/<slug>/`.
- The generated JSON payload exists in `public/blog/conversations/<slug>/conversation.json`.
- The generated AI index exists in `public/ai/index.json`.
- `public/sitemap.xml` includes the human conversation URL.
- The built human page links to the public JSON URL.
- The final check is documented as a distinct approval step.
- Bots/agents are instructed to ask Kyle before running it.

## First Conversation Recommendation

For `crypto-industry-today.md`, the published conversation should probably not be titled generically as "Crypto Industry Today."

Better title candidates:

- `Crypto's Real Design Problem Is Not Usability`
- `Crypto UX Needs to Move Beyond Wallet Onboarding`
- `The Mature Design Problem in Crypto Is Systems Strategy`
- `Blockchain Is an Accounting Technology. Design Should Treat It Like One.`

Recommended working title:

- `Crypto's Real Design Problem Is Not Usability`

Working description:

- `A UX strategist's view on why crypto's future depends less on friendlier wallets and more on finding complex markets where shared accounting creates real leverage.`

Recommended categories:

- `thoughts`

Recommended tags:

- `crypto`
- `blockchain`
- `ux strategy`
- `fintech`
- `systems design`
- `product strategy`

## Risks and Tradeoffs

- **Over-automation risk:** AI can make Kyle's thinking sound generic or alter the meaning. Do not use AI to rewrite transcript content in this pipeline.
- **Source integrity risk:** Automated transcript cleanup can accidentally change meaning. Keep raw source files untouched and keep generated turn text identical except for speaker labels.
- **SEO/AI discoverability risk:** JSON files are useful only if crawlers can find them. Add crawlable links and indexes.
- **Hugo bundle risk:** Confirm that `conversation.json` inside `content/blog/conversations/<slug>/` is published to the expected URL. If Hugo does not copy the bundled JSON as expected, document the fallback before implementation.
- **Two-phase workflow risk:** The `.md` page and JSON can drift if the page is edited after JSON generation. Validation should detect mismatches or require regenerating JSON after content changes.
- **Maintenance risk:** Too many generated artifacts can become annoying to update. Keep source-of-truth files clear.
- **Content strategy risk:** Some conversations may be rough or incomplete. The workflow should support draft status and metadata review without forcing every conversation into a polished essay format.

## Open Decisions

- Should conversation archives be public?
- Should reviewed metadata be stored as YAML before JSON generation?
- Should every conversation be published, or should the system classify some as private/source-only?
- What should the canonical public entry point be for AI-readable discussions?
- Should conversation pages appear in the normal blog list, or should templates treat `blog/conversations` as a separate content subtype?
- Should Phase 2 refuse to run if `index.md` has unreviewed placeholder metadata?
- How should validation detect whether `index.md` changed after `conversation.json` was generated?

## Suggested First Build Slice

Build the smallest useful pipeline around `crypto-industry-today.md`:

1. Raw transcript reader for `conversation-processing/raw-transcripts/`.
2. Parser script for exported markdown.
3. Conversation folder generator at `content/blog/conversations/<slug>/`.
4. Phase 1 human page generator for `index.md`.
5. Human-editable metadata YAML file.
6. Phase 2 JSON payload generator for `conversation.json`.
7. Script step that writes the JSON URL back into `index.md`.
8. Master/topic index generator under `static/ai/`.
9. Validator.
10. Step-by-step guide in `conversation-processing/_how-to-process-conversations.md`.

Then publish the first conversation page from the normalized transcript and reviewed metadata. Do not add article drafting or transcript rewriting until there is a separate reason to create authored essays from the conversation archive.
