---
ticket: 006_git-hygiene
status: planned
type: infrastructure
keywords:
  - gitignore
  - public/
  - resources/_gen
  - Hugo build output
  - repo hygiene
  - Netlify
  - commit cleanup
  - generated files
  - stale build artifacts
  - test files
scope:
  - .gitignore
  - public/
  - resources/_gen/
  - content/_index-test-snippet.md
  - content/pages/for-ai-llm-readers-2.md
depends-on: []
blocks: []
---

# 006: Git & Build Output Hygiene

Clean up repository tracking so day-to-day commits only include **source** files (content, theme, static assets, config) — not Hugo build output, cache, or accidental junk.

**Status: planned**

---

## Problem

Commit `18d634b` (*added block for messaging to bots*) changed **105 files** with **276k+ insertions**, even though the llm-hint feature itself was only ~4 source files:

| Intended change | File |
|---|---|
| New shortcode | `themes/nefkoPortfolio/layouts/_shortcodes/llm-hint.html` |
| Styles | `themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css` |
| Homepage usage | `content/_index.md` |
| Documentation | `_readme-architecture.md` |

Everything else in that commit was noise:

1. **Full Hugo rebuild of `public/`** — dozens of HTML/XML/CSS files regenerated locally and staged.
2. **Hugo asset cache** — `resources/_gen/` updates.
3. **Debug/test artifacts** left over from shortcode troubleshooting:
   - `content/_index-test-snippet.md`
   - `public/_index-test-snippet/index.html`
   - `public/test-index/index.html`
4. **Junk files in `public/`** (not site content — macOS/app temp files):
   - `public/AlTest1.err`, `public/AlTest1.out`
   - `public/adobegc.log`, `public/oobelib.log`
   - `public/CalNotificationsAvailable`
   - `public/MozillaUpdateLock-2656FF1E876E9973`
   - `public/com.brave.Browser.Sparkle.pid`
   - `public/com.creatie.font.err`, `public/com.creatie.font.out`
5. **Unrelated content bundled in the same commit** (review before reverting):
   - `_Tickets/005_Nav-Bar/005_Nav-Bar.md` edits
   - `content/pages/for-ai-llm-readers.md` edits
   - **Deletion** of `content/pages/for-ai-llm-readers-2.md` (existed in `4ba2edd`, removed in `18d634b`)

Commit is **already pushed** to `origin/main`. The llm-hint work ships as-is; **this ticket is follow-up cleanup** — it does not amend `18d634b`. Expect at least one new commit (likely a large deletion diff when `public/` is untracked).

---

## Root Cause

| Factor | Detail |
|---|---|
| **No root `.gitignore`** | The theme has `themes/nefkoPortfolio/.gitignore` (includes `/public/`, `/resources/_gen/`), but the **project root does not**. Git tracks build output at the repo root. |
| **`public/` historically committed** | Netlify runs `hugo` on deploy (`netlify.toml` → `publish = "public"`). Local `public/` does not need to be in git. |
| **Hugo does not clean `public/`** | Stale files (old CSS hashes, test pages, junk) persist until manually deleted. |
| **Broad staging** | `git add .` (or equivalent) staged rebuild output alongside real source changes. |

---

## Goal

After this ticket:

- Only **source** is tracked: `content/`, `themes/`, `static/`, `hugo.toml`, `netlify.toml`, tickets, docs, etc.
- `public/` and `resources/_gen/` are **ignored** and **removed from git index** (files may remain locally for preview).
- Test/junk artifacts are **deleted** from disk and repo.
- Future commits for features like llm-hint stay small and reviewable.

---

## Proposed Implementation

### 1. Add root `.gitignore`

Create `Websites/ux-portfolio/.gitignore`. Start from the Hugo section of `themes/nefkoPortfolio/.gitignore`:

```gitignore
# Hugo build output & cache
/public/
/resources/_gen/
/assets/jsconfig.json
hugo_stats.json
/.hugo_build.lock

# OS & editor noise
.DS_Store
```

Keep it minimal — do not copy the entire theme's 360-line gitignore unless needed later.

### 2. Delete artifacts from disk

| Path | Action |
|---|---|
| `content/_index-test-snippet.md` | Delete |
| `public/_index-test-snippet/` | Delete |
| `public/test-index/` | Delete |
| `public/AlTest1.err`, `.out`, etc. | Delete (full list in Problem section) |

Then run `hugo` locally and confirm `public/` contains only legitimate site output.

### 3. Stop tracking generated folders

```bash
git rm -r --cached public/
git rm -r --cached resources/_gen/
```

This removes them from git **without deleting** local copies (needed for `hugo server` preview). After `.gitignore` is in place, they will not be re-staged.

### 4. Restore `for-ai-llm-readers-2.md`

**Decision (Nefko): yes — restore.** This page was accidentally removed in `18d634b` while unrelated files were staged. It existed in `4ba2edd` and should come back:

```bash
git show 4ba2edd:content/pages/for-ai-llm-readers-2.md > content/pages/for-ai-llm-readers-2.md
```

Include the restore in the hygiene commit (or an immediately adjacent follow-up commit if preferred). After restore, confirm whether both AI reader pages (`for-ai-llm-readers.md` and `for-ai-llm-readers-2.md`) should remain long-term — that consolidation can be a **separate content ticket** if needed.

### 5. Commit hygiene message

Single focused commit, e.g.:

> Stop tracking Hugo build output; remove test artifacts and junk from public/

Do **not** mix unrelated feature work into this commit.

---

## Out of Scope (for now)

| Item | Why defer |
|---|---|
| Rewriting git history (`git filter-repo`, force-push) | Commit already on `origin/main`; history rewrite is high risk for little gain if index cleanup is sufficient. |
| Removing old hashed CSS files from remote history | Addressed going forward by untracking `public/`. |
| Changing Netlify deploy config | Already correct — builds fresh on each deploy. |
| Pre-commit hooks / CI lint for repo hygiene | Nice follow-up; not required for this ticket. |

---

## Tradeoffs

| Choice | Pros | Cons |
|---|---|---|
| **Untrack `public/`** (recommended) | Small commits; matches Netlify workflow; matches standard Hugo practice | Local preview still needs `hugo`; cannot browse built site directly from GitHub without CI |
| **Keep tracking `public/`** | Built site visible in repo | Every local build pollutes git; stale files accumulate forever |
| **Restore `for-ai-llm-readers-2.md`** | No accidental content loss (**confirmed — do this**) | Two AI reader pages until a future content ticket consolidates them |

---

## Follow-up required

This ticket is **explicitly follow-up work** triggered by commit `18d634b`. It is not part of the original llm-hint feature.

| Follow-up | When | Notes |
|---|---|---|
| **Hygiene commit** | During 006 implementation | Untrack `public/` + `resources/_gen/`, delete junk/test files, add `.gitignore`, restore `for-ai-llm-readers-2.md`. Will produce a large diff (mostly deletions from git index). Push to `origin/main`. |
| **Verify Netlify deploy** | After hygiene commit | Build command unchanged; confirm deploy still succeeds. |
| **AI reader page consolidation** | Future content ticket (optional) | Nefko now has two pages: `for-ai-llm-readers.md` and `for-ai-llm-readers-2.md`. Decide canonical URL, redirects, and whether to retire one. Out of scope for 006. |
| **Repo hygiene docs** | Same session or immediately after 006 | Short note in `_readme-architecture.md` (see Optional doc update). |
| **Pre-commit / CI guardrails** | Future infrastructure ticket (optional) | Warn if `public/` or `resources/_gen/` are staged. Not required to close 006. |

**Do not amend or force-push `18d634b`.** Leave that commit in history; fix forward.

---

## Verification Checklist

- [ ] Root `.gitignore` exists and ignores `/public/` and `/resources/_gen/`
- [ ] No junk files remain at top level of `public/` (`.err`, `.log`, `.pid`, lock files)
- [ ] `content/_index-test-snippet.md` gone
- [ ] `git status` after `hugo` shows **no** changes under `public/` or `resources/_gen/`
- [ ] `hugo server` still serves homepage with llm-hint block
- [ ] Netlify deploy still succeeds (unchanged build command)
- [ ] `content/pages/for-ai-llm-readers-2.md` restored from `4ba2edd`
- [ ] Follow-up commit pushed; Netlify deploy verified

---

## Optional doc update

Add a short **Repo hygiene** note to `_readme-architecture.md`:

- Do not commit `public/` or `resources/_gen/`
- Run `hugo` locally for preview; Netlify builds on deploy
- Stage source files intentionally — avoid `git add .` before reviewing `git status`

---

## Implementation order

1. Add root `.gitignore`
2. Restore `for-ai-llm-readers-2.md` from `4ba2edd`
3. Delete junk + test files from disk
4. `git rm -r --cached public/ resources/_gen/`
5. Commit + push (follow-up commit on `main`)
6. Verify Netlify deploy
7. Optional: architecture readme repo-hygiene note
8. Later (optional): content ticket to consolidate AI reader pages
