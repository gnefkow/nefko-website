---
ticket: 004_home-case-studies-block
status: built
type: component
keywords:
  - featured-case-studies
  - featured-block
  - case studies
  - home page
  - case study cards
  - card-surface
  - tag badges
  - tags
  - shortcode
  - vertical card layout
  - 2-column grid
  - hover shadow
  - page-gutter
  - measure-wide
  - Option 4 layout
  - ph5-l
  - box-sizing
  - 960px breakpoint
  - Tachyons height collision
  - h5 height utility
  - design tokens
  - typography classes
  - GetFeaturedImage
  - YAML front matter tags
scope:
  - themes/nefkoPortfolio/layouts/_shortcodes/featured-case-studies.html
  - themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css
  - themes/nefkoPortfolio/layouts/home.html
  - themes/nefkoPortfolio/layouts/list.html
  - themes/nefkoPortfolio/layouts/post/list.html
  - themes/nefkoPortfolio/layouts/taxonomy.html
  - themes/nefkoPortfolio/layouts/terms.html
  - themes/nefkoPortfolio/layouts/404.html
  - content/case-studies/*/index.md
  - content/_index.md
  - _readme-architecture.md
depends-on:
  - 002_css-semantic-tokens
blocks: []
---

# 004: Home Case Studies Block

Rework the home-page case study block to match Figma **CaseStudyEntrypointBlock** layout. Also fixed a site-wide layout bug (Option 4 `page-gutter`) discovered during QA.

**Status: built**

---

## Figma Source

| Frame | URL | What it shows |
|---|---|---|
| **Case Studies section** (mobile) | [node 2096:32472](https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2096-32472) | Section heading + vertical stack of case study cards |
| **CaseStudyEntrypointBlock** (component) | [node 2096:32414](https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2096-32414) | Single card anatomy: image → title → subtitle → tag row |

Figma is **mobile-width** (~321px content column). Desktop uses a **2-column CSS grid** at `30em`+ within the page's `measure-wide` column.

---

## What We Built

### Shortcode: `{{< featured-case-studies >}}`

Renders optional section `title` + `text`, then a grid of case study cards pulled from the `pages` param. Each card links to the case study page.

**Shortcode does not own page layout** — no `measure-wide`, `ph3`, or `ph5-l` on the shortcode wrapper. The parent layout (`home.html` etc.) provides `.page-gutter` + `measure-wide`.

### Sub-components

1. **Section header** — Optional `title` + `text` from shortcode params (Nefko edits in `_index.md`).
2. **Case study card** — vertical stack inside a liftable white surface.
3. **Tag badges** — reusable `.tag` element (uppercase pills).

---

## Card DOM Structure (as built)

```
featured-block__list          (CSS grid, gap: 0)
  └── featured-block__item    (<li>, padding: 0)
        └── featured-block__card          (<a> link — hover trigger, no visual styles)
              └── featured-block__card-surface   (white mat + hover border/shadow)
                    ├── featured-block__card-image
                    │     └── featured-block__card-img
                    └── featured-block__card-body
                          ├── featured-block__card-title
                          └── featured-block__card-meta
                                ├── featured-block__card-description
                                └── featured-block__tags
                                      └── .tag (×n)
```

**Which element lifts on hover?** `featured-block__card-surface` — triggered by `:hover` / `:focus` on the parent `<a class="featured-block__card">`. No `dim` class (no opacity fade).

---

## Card Styling (final values)

### `featured-block__card-surface`
| Property | Value |
|---|---|
| Padding | `0.6em` all sides |
| Background | `var(--bg-primary)` (white) |
| Default border | `1px solid transparent` |
| Hover border | `var(--bg-primary)` (white edge against shadow) |
| Hover shadow | `0 4px 12px rgba(0, 0, 0, 0.08)` |

### `featured-block__card-body`
| Property | Value |
|---|---|
| Padding top | `0.5rem` |
| Padding left/right | `0.25rem` |
| Padding bottom | `1rem` |

### Internal spacing
| Between | Value |
|---|---|
| Title → subtitle | Tachyons `mb1` (`0.25rem` / ~4px) on title |
| Subtitle → tags | `gap: 0.75rem` on `.featured-block__card-meta` |
| Tag → tag | `gap: 0.25rem` on `.featured-block__tags` |

### Grid
| Property | Value |
|---|---|
| Mobile | Single column |
| `30em`+ | 2 columns |
| Grid gap | `0` (spacing comes from `card-surface` padding only) |
| `featured-block__item` padding | `0` |

### Image
| Property | Value |
|---|---|
| Container height | `12.4375rem` (~199px) |
| Image border | **None** (removed gray `2px` border) |
| `object-fit` | `cover` |

---

## Typography (as built)

| Element | Implementation |
|---|---|
| Section heading | `.h3-heavy` |
| Card title | `.h4-heavy` + `mb1` (22px — 2px under Figma's 24px) |
| Card subtitle | `.p` + `.text-tertiary` (16px — paragraph, not `.h5`) |
| Tag label | `.tag` + Tachyons `f7` (12px, uppercase via CSS) |

**Why not `.h5` on subtitle:** Tachyons `.h5` is a **height** utility (`height: 16rem`), not font size. Caused a 256px gap bug. Site-wide fix: `height: auto` on typography `.h1`–`.h6` in `_styles.css`.

---

## Hex-to-Token Mapping

| Figma Value | Design Token | Usage |
|---|---|---|
| `#000000` | `--text-primary` | Section heading, card title |
| `#7c7c7c` | `--text-tertiary` | Card subtitle |
| `#f1f1f1` | `--bg-secondary` | Tag background |
| `#5f5f5f` | `--border-tertiary` | Tag text |

---

## Data Architecture

### Case study front matter fields

| Field | Used for |
|---|---|
| `title` | Card title |
| `description` | Card subtitle |
| `featured_image` | Hero image (via `GetFeaturedImage` partial) |
| `tags` | Tag pill row (YAML array or comma-separated string) |

Tags added to: `cradl-onboarding`, `cradl-ux-in-cryptocurrency`, `jpm-onyx`. **`yoma-digital-transformation` still has no tags.**

Tags are display-only — not filterable (unlike testimonials carousel).

---

## Page Layout — Option 4 (site-wide fix)

Discovered during this ticket: at `60em` (960px), content snapped narrower because `ph3 ph5-l` + `measure-wide` were on the **same element** under `box-sizing: border-box`.

**Fix:** Separated gutter from reading column.

```html
<div class="page-gutter pv3 pv4-l">
  <article class="measure-wide center ...">
    {{ .Content }}   <!-- shortcodes live here, no duplicate wrappers -->
  </article>
</div>
```

| Layer | Class | Job |
|---|---|---|
| Outer | `.page-gutter` | Horizontal inset (`1rem`; `4rem` at `60em`) |
| Inner | `.measure-wide` | Max-width `34em` — **no horizontal padding** |

Applied to: `home.html`, `list.html`, `post/list.html`, `taxonomy.html`, `terms.html`, `404.html`.

Documented in `_readme-architecture.md` under **Page column layout**.

**Not changed:** `single.html`, `page/single.html` (`mw7`/`mw8` layout).

---

## Files Changed

```
ux-portfolio/
├── content/
│   ├── _index.md
│   └── case-studies/*/index.md
├── _readme-architecture.md              # page-gutter rule + typography collision note
└── themes/nefkoPortfolio/
    ├── layouts/
    │   ├── home.html
    │   ├── list.html
    │   ├── post/list.html
    │   ├── taxonomy.html
    │   ├── terms.html
    │   ├── 404.html
    │   └── _shortcodes/
    │       └── featured-case-studies.html
    └── assets/nefkoPortfolio/css/
        └── _styles.css                  # .page-gutter, .featured-block__*, .tag, h1–h6 height fix
```

---

## Bugs Fixed During Build

### BUG: Huge gap between subtitle and tags — **FIXED**
Tachyons `.h5` height utility (`16rem`) collided with typography `.h5` on subtitle `<p>`. Fixed with `height: auto` on typography classes + switched subtitle to `.p`.

### BUG: Content width snap at 960px — **FIXED**
Option 4 `page-gutter` site-wide. See above.

### BUG: Hover appeared to apply to wrong element — **FIXED**
Removed Tachyons `dim` (opacity fade). Added `featured-block__card-surface` wrapper; border + shadow apply to the whole card unit on link hover.

---

## Decisions Log

| Topic | Decision |
|---|---|
| Section copy | Nefko edits `_index.md`; shortcode API unchanged |
| Desktop layout | 2-column grid at `30em`+ |
| Card count | All pages in `pages` param (currently 4) |
| Hover | No opacity fade; white border + shadow on `card-surface` |
| Typography | Approximate with existing tokens; subtitle is `.p` |
| Grid gap | `0` — card spacing from `card-surface` padding only |
| Image border | Removed — white mat from surface padding is enough |
| Page layout | Option 4 site-wide via `.page-gutter` |

---

## Open Questions

*(none remaining)*
