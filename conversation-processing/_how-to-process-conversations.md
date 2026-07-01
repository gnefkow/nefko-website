# How to Process Conversations

This guide explains how to turn a raw AI interview transcript into a human-readable conversation page and an AI-readable JSON payload.

The process has two phases because Kyle should review the human `.md` page before the JSON is generated.

After running a process, remind Kyle what he needs to do next.

## Folder Structure

Raw transcript inputs go here:

```txt
conversation-processing/raw-transcripts/
```

Processing scripts live here:

```txt
conversation-processing/scripts/
```

Generated conversation pages and JSON payloads go here:

```txt
content/blog/conversations/<slug>/
content/blog/conversations/<slug>/index.md
content/blog/conversations/<slug>/conversation.json
```

Reviewed metadata lives here:

```txt
data/conversations/<slug>.yaml
```

AI discovery indexes:

```txt
/ai/index.json                         # Hugo build — unified catalog
/ai/experiences.json                   # Hugo build — full experience payloads
static/ai/topics/<topic>.json          # Phase 2 Python — topic slices
```

The shared tag codebook lives here:

```txt
_Work-utilities/codebook.yaml
```

Use the codebook when selecting conversation topics, tags, keywords, and AI-routing metadata. It is the living taxonomy for recruiter-facing and bot-readable themes across the portfolio.

## Important Rule

Do not edit raw transcripts in `conversation-processing/raw-transcripts/`.

The scripts read raw transcripts as immutable source inputs. They may create website pages, metadata, JSON, indexes, and links, but they should not modify raw transcript files.

## Phase 1: Generate the Human Page

Run Phase 1 after placing a raw transcript in `conversation-processing/raw-transcripts/`.

Example:

```bash
python3 conversation-processing/scripts/phase1_generate_conversation_page.py crypto-industry-today.md \
  --slug crypto-industry-today \
  --title "Crypto's Real Design Problem Is Not Usability" \
  --description "A conversation with Kyle Becker about crypto UX, institutional finance, and why blockchain design needs to focus on systems strategy." \
  --topic crypto \
  --topic ux-strategy \
  --topic fintech \
  --tag blockchain \
  --tag systems-design
```

Phase 1 creates:

```txt
content/blog/conversations/crypto-industry-today/index.md
data/conversations/crypto-industry-today.yaml
```

It does not create `conversation.json`.

## Human Review Checkpoint

Before running Phase 2, review:

```txt
content/blog/conversations/<slug>/index.md
data/conversations/<slug>.yaml
```

Check that:

- Speaker labels are correct, usually `Herb` and `Kyle`.
- Conversation turns are in the right order.
- The transcript text has not been rewritten by the script.
- Title, description, topics, keywords, summary, claims, and notable quotes are acceptable.
- The page should remain `draft: true` until it is ready to publish.

If you manually edit the transcript text in `index.md`, run Phase 2 afterward so the JSON reflects the reviewed page.

## Phase 2: Generate JSON and Indexes

Run Phase 2 only after the human page and metadata have been reviewed.

Example:

```bash
python3 conversation-processing/scripts/phase2_generate_json.py crypto-industry-today
```

Phase 2 creates or updates:

```txt
content/blog/conversations/crypto-industry-today/conversation.json
static/ai/topics/<topic>.json
```

Run `hugo --environment production` after Phase 2 so `/ai/index.json` picks up the published conversation from `data/conversations/<slug>.yaml`.

It also updates:

```txt
content/blog/conversations/crypto-industry-today/index.md
```

Specifically, it writes the public JSON URL into the `ai_json` frontmatter field and adds a visible `conversation.json` link to the page.

## Validate the Output

After Phase 1, you can validate the human page and metadata:

```bash
python3 conversation-processing/scripts/validate_conversation.py crypto-industry-today
```

After Phase 2, require JSON and index validation:

```bash
python3 conversation-processing/scripts/validate_conversation.py crypto-industry-today --require-json
```

Validation checks:

- `index.md` exists.
- Metadata YAML exists.
- `conversation.json` exists after Phase 2.
- The raw transcript still matches the hash recorded during Phase 1.
- The human page and JSON use predictable canonical URLs.
- The JSON turns match the reviewed `index.md` turns.
- The human page links to `conversation.json` after Phase 2.
- After a Hugo build, `/ai/index.json` includes the conversation when `data/conversations/<slug>.yaml` has `status: published`.

## Build Check

After validation, run the normal Hugo build process for the site.

Confirm these URLs exist in the generated site:

```txt
/blog/conversations/<slug>/
/blog/conversations/<slug>/conversation.json
/ai/index.json
```

Also confirm relevant topic indexes exist, for example:

```txt
/ai/topics/crypto.json
/ai/topics/ux-strategy.json
```

## Final "Check It" Step

Before considering a conversation ready to push or publish, do the final check.

Important instruction for bots/agents:

If Kyle starts talking about pushing, deploying, publishing, or checking the build, ask him whether he wants you to run the final check. Do not assume. The check may require building the site or inspecting generated output, so it should be treated as a distinct approval step.

The final check should happen after:

- Phase 1 has generated `index.md`.
- Kyle has reviewed the human-readable page and metadata.
- Phase 2 has generated `conversation.json`.
- The page is intended to be publishable, usually meaning `draft: false`.
- The Hugo site has been built.

Run:

```bash
python3 conversation-processing/scripts/validate_conversation.py crypto-industry-today --require-json --check-build
```

The final check validates:

- The generated `index.md` exists.
- The generated `conversation.json` exists.
- `index.md` links visibly to the JSON payload.
- The JSON turns match the reviewed `index.md` turns.
- The raw transcript still matches the Phase 1 source hash.
- The built `/ai/index.json` catalog includes the conversation after Hugo build.
- The built human page exists in `public/blog/conversations/<slug>/`.
- The built JSON payload exists in `public/blog/conversations/<slug>/conversation.json`.
- The built AI index exists in `public/ai/index.json`.
- `public/sitemap.xml` includes the human conversation URL.

Note: the sitemap is expected to include the human HTML page, not necessarily the JSON payload. The JSON payload is discovered through the human page link and the AI indexes.

## What the Scripts Do Not Do

The scripts do not:

- Rewrite Kyle's answers.
- Clean up typos inside conversation turns.
- Convert the transcript into a new article.
- Publish the page automatically.
- Modify files in `conversation-processing/raw-transcripts/`.

If transcript wording needs editorial correction, make that as a deliberate manual edit in the generated `index.md`, then rerun Phase 2 so `conversation.json` matches the reviewed page.