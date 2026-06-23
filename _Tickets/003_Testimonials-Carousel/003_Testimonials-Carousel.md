---
ticket: 003_testimonials-carousel
status: built
type: component
keywords:
  - testimonials
  - testimonials-carousel
  - carousel
  - filter tabs
  - quotes
  - modal
  - shortcode
  - GSAP
  - Draggable
  - InertiaPlugin
  - swipe
  - finger-tracking
  - drag
  - snap
  - push animation
  - wrap-around
  - full-bleed
  - YAML data
  - home-quote
  - full-quote
  - tag filtering
  - pagination dots
  - CDN defer
  - DOMContentLoaded
  - design tokens
  - Tachyons widths
scope:
  - layouts/shortcodes/testimonials-carousel.html
  - layouts/_partials/head-additions.html
  - themes/nefkoPortfolio/assets/nefkoPortfolio/css/_testimonials-carousel.css
  - content/testimonials/*.yaml
  - static/images/testimonial-avatars/
depends-on:
  - 002_css-semantic-tokens
blocks: []
---

# 003: Testimonials Carousel

## Component naming — **DECIDED**

This component is **`testimonials-carousel`** — the homepage filter + carousel + modal experience from Figma.

Other pages will need **single testimonial blocks** (same `content/testimonials/` data, different layout). Those will be separate shortcodes later (e.g. `testimonial-block` or similar). This ticket covers only the carousel.

| Component | Shortcode | Purpose |
|---|---|---|
| **Testimonials carousel** (this ticket) | `{{< testimonials-carousel >}}` | Filter tabs, card rail, pagination, modal |
| Single testimonial block (future) | TBD | One quote, different layout — case studies, etc. |

Shared data: `content/testimonials/*.yaml`. Shared assets: `static/images/testimonial-avatars/`.

## Figma Source

https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2052-32308&t=FXNWKD7RhouXRNcI-1

The Figma design is a **mobile-width** frame (390px). Desktop behavior will need to be determined.

---

## What We're Building

The **testimonials carousel** consists of 4 sub-components:

1. **Filter Bar** — "Working with" label + horizontally scrollable category tabs
2. **Testimonial Rail** — Carousel of testimonial blocks (one visible at a time)
3. **Pagination Dots** — Carousel position indicators
4. **"See Quote" Modal** — Full-quote overlay triggered by "Read Full quote" link

---

## Figma Design Breakdown

### Filter Bar
- **Left side**: "Working with" in bold white text — fixed, does not scroll.
- **Right side**: Horizontally scrollable tab strip.
- **Figma reference tabs**: Engineers, CEOs, Designers, Mentees, Researchers, Start Ups, Finance, Product
- **Initial launch tabs** (defined in the component, not Figma): **Leadership | Product | Engineers | Designers**
- **Active tab**: light background, dark text, drop shadow.
- **Inactive tabs**: muted text, right-side border dividers.
- **Bottom border** across the entire bar.

### Carousel card (single slide)
- Decorative open-quote mark (SVG/image asset).
- **Quote text**: Lato Italic, large (~30px), white. Pulled from **`home-quote`** in each YAML file — a curated excerpt for the homepage carousel, not the full quote.
- **"Read Full quote"** link: underlined, slightly muted white. Opens modal with **`full-quote`**.
- **Attribution area**:
  - Circular avatar photo (60px diameter).
  - **Name**: Lato Bold, ~22px, white.
  - **Context line**: Lato Regular, ~17px, muted gray. Template from Figma: `{name} was a {role} when I worked with them at {place}`.

### Pagination Dots
- Small circles (6px), one elongated active indicator (20px wide).
- Active dot: filled light gray.
- Inactive dots: dark fill with light gray border.

---

## Hex-to-Token Mapping

Every hex code from the Figma maps to an existing design token from `_styles.css`, except the pagination dots:

| Figma Value | Design Token | Usage |
|---|---|---|
| `#000000` (bg) | `--bg-inverse-primary` | Section background |
| `#ffffff` | `--text-inverse-primary` | Quote text, person name |
| `#a4a4a4` | `--text-inverse-tertiary` | Attribution context line |
| `#cccccc` | `--text-inverse-secondary` | Inactive tab text |
| `rgba(255,255,255,0.8)` | `--text-inverse-secondary` | "Read Full quote" link (close enough; avoid one-off opacity) |
| `#e9e9e9` | `--bg-tertiary` | Active tab background |
| `#282727` | `--text-primary` | Active tab text (≈ #000, close enough) |
| `#ebebeb` | `--border-primary` | Active tab border |
| `#666666` | `--border-tertiary` | Tab dividers, bar bottom border |
| `#d9d9d9` | **No token** | Pagination dot active fill + inactive border |
| `#2b2b2b` | **No token** | Pagination dot inactive background |

**Decision needed**: The pagination dot colors (`#d9d9d9`, `#2b2b2b`) have no existing token. Options:
- (a) Add new tokens like `--dot-active` / `--dot-inactive` in `:root`.
- (b) Hardcode them in the component CSS since they're purely decorative UI chrome unlikely to be reused.
- (c) Approximate with existing tokens (`--border-secondary` for #d9d9d9, `--bg-inverse-primary` for the dark fill).

---

## Data Architecture

### Current testimonial YAML files: `content/testimonials/*.yaml`

There are 10 testimonials. Each file has this general shape:

```yaml
first-name: Charla
last-name: Kunkel
photo: /images/testimonial-avatars/Charla-Kunkel.jpg
worked-together:
  - title: Senior Technologist
    company: frog Design
    relationship: Projects
  - title: Head of Product and Engineering
    company: Quantified AI
    relationship: Client
tags: Engineer, Product, Start Up, Leadership, AI
full-quote: |
  (long multi-paragraph quote — used in modal)
key-quotes:
  - home-quote: |
      (curated excerpt — used in testimonials carousel)
  - engineering: |
      (optional — other contexts, e.g. case studies)
```

Avatar photos live in `static/images/testimonial-avatars/`. Each YAML has an explicit `photo` path.

### Quote fields — **DECIDED**

| Field | Where it lives | Used by |
|---|---|---|
| `home-quote` | Inside `key-quotes` array | **Testimonials carousel** — the italic excerpt in each slide |
| `full-quote` | Top-level field | **Modal** — shown when user clicks "Read Full quote" |
| Other `key-quotes` entries | Inside `key-quotes` array | Not used by this component; reserved for single-block layouts, case studies, etc. |

All 10 YAML files now have a `home-quote` entry. The carousel shortcode must extract `home-quote` specifically — do not fall back to `full-quote` truncation or other `key-quotes` keys.

**Template note:** `home-quote` is nested inside the `key-quotes` list (e.g. `- home-quote: |`). Hugo template logic needs to find that entry among any sibling keys (`engineering`, `ambidexterity`, etc.).

### Filter categories vs. YAML tags — **DECIDED**

**Categories are defined in the component**, not in the YAML files. The shortcode owns the tab list:

```
Leadership | Product | Engineers | Designers
```

**YAML `tags` are separate metadata.** Each testimonial can have many tags (Startup, Web3, Finance, Design Research, etc.). That is fine — YAML tags are a superset of what appears in the filter bar. Tags that don't correspond to a filter tab are ignored by the carousel filter; they may be useful elsewhere later.

**Filter behavior:** When a tab is selected, show testimonials whose `tags` include a match for that category. Matching is case-insensitive string comparison against the category label (e.g. tag `Leadership` → Leadership tab, tag `Product` → Product tab).

**Tag alignment note:** Some current tags are close but not exact matches (e.g. `Engineer` vs tab `Engineers`, `UX Design` vs tab `Designers`). Nefko can add the canonical category names to `tags` as needed when curating who appears in each tab. No separate `filter-categories` field required.

### Data issues to resolve before building

1. ~~**Inconsistent tag field name**~~ — **Done.** All files use `tags`.

2. ~~**Carousel excerpt**~~ — **Done.** All 10 files have `home-quote` inside `key-quotes`. Carousel uses `home-quote` only.

3. ~~**Filter tab categories vs. YAML tags**~~ — **Done.** See above.

4. ~~**Avatar photos**~~ — **Done.** All 10 YAML files have `photo` fields.

5. ~~**Hugo data access**~~ — **Done.** Keep YAML files in `content/testimonials/`. Shortcode reads from there (not `data/`).

---

## File Structure (Proposed)

Following the pattern set by the logos-block:

```
ux-portfolio/
├── content/
│   └── testimonials/
│       └── *.yaml                 # Shared testimonial data
├── layouts/
│   └── shortcodes/
│       └── testimonials-carousel.html  # This component — filter + carousel + modal
└── static/
    └── images/
        └── testimonial-avatars/    # Shared avatar photos (done)
```

CSS/JS class prefix: `testimonials-carousel` (e.g. `.testimonials-carousel__filter`, `.testimonials-carousel__slide`).

Categories (`Leadership`, `Product`, `Engineers`, `Designers`) are hardcoded in the shortcode — same pattern as logos-block tabs, but without a separate `data/` file since testimonial content lives in `content/testimonials/`.

**Note**: The logos-block currently inlines its CSS within the shortcode `<style>` tag. If we want to use the design tokens from `_styles.css` via `var()`, inlining works fine since `:root` tokens are global. But if we want Hugo Pipes to bundle the CSS together, we'd use a separate file added to the asset pipeline. Either approach works — the logos-block pattern (inline) is simpler.

---

## Implementation Steps

| Step | Task | Files |
|------|------|-------|
| 0 | ~~Data prep: tags, photos, home-quote~~ | **Done** |
| 1 | Create `testimonials-carousel` shortcode — category tabs, slide rail (`home-quote`), pagination dots, modal (`full-quote`) | `layouts/shortcodes/testimonials-carousel.html` |
| 2 | Load testimonial YAML from `content/testimonials/` | shortcode template logic |
| 3 | CSS — filter bar, carousel card, pagination dots, modal. Colors via design tokens. Prefix classes `testimonials-carousel__*`. | Inline in shortcode or `_testimonials-carousel.css` |
| 4 | JS — Tab filtering (match `tags` to selected category), carousel, pagination sync, modal | Inline in shortcode |
| 5 | Add `{{</* testimonials-carousel */>}}` shortcode call to homepage | `content/_index.md` |
| 6 | Test filtering, carousel behavior, modal, responsiveness | — |

---

## Decisions Log

### Desktop layout — **DECIDED**
The carousel uses two width tiers, both from Tachyons, to match the site's global width system:

| Area | Width | Tachyons class equivalent |
|---|---|---|
| Filter bar | `34em` (~544px) | `measure-wide` — matches the homepage article column |
| Quote viewport + nav | `30em` (~480px) | `measure` — narrower for visual contrast |

On mobile: full width with **24px** horizontal padding. No top padding on the section; bottom padding retained.

### Full-bleed — **DECIDED**
The carousel's black background must stretch edge-to-edge (zero margin/padding on left and right) regardless of the parent container's max-width or padding. Implemented via the CSS full-bleed pattern (`width: 100vw; margin-left: calc(-50vw + 50%);`) to break out of the `measure-wide` + `ph3 ph5-l` article wrapper in `home.html`.

### Carousel interaction — **DECIDED**
- **Mobile:** finger-tracking drag/swipe between testimonial cards. The slide physically follows the user's thumb and snaps to the nearest slide on release (momentum-based via InertiaPlugin). Uses GSAP Draggable + InertiaPlugin on the strip element.
- **Desktop:** arrow buttons to navigate cards (push animation).
- **Category tabs:** filter which testimonials appear in the carousel — separate from swipe/arrows.
- **Wrap-around:** Arrow buttons and keyboard arrows loop. Draggable has edge resistance at boundaries (rubber-band feel) with overshoot snap-back.
- No auto-advance timer.

**Strip architecture:** Slides are laid out in a horizontal flex strip (`.testimonials-carousel__strip`) inside the viewport. Only filtered slides are visible (`display: none` on non-matching slides). Draggable translates the strip's `x` position. Snap points are at `x = -i * viewportWidth`.

**Wrap-around on arrows/keyboard:** `goToSlide()` resolves out-of-bounds positions with modular arithmetic. On drag, edge resistance provides a rubber-band effect at boundaries rather than hard wrapping.

**Previous approach (replaced):** Crossfade + x-offset via `gsap.to`/`gsap.fromTo` with Observer for swipe detection. Replaced because it didn't feel physical — slides faded rather than pushed.

### Modal — **DECIDED**
Dark background (`--bg-inverse-primary`). X button at top to close. Content is `full-quote` from the active testimonial.

### Data location — **DECIDED**
Keep YAML files in `content/testimonials/`.

---

### Animation library — **DECIDED**
**GSAP** (GreenSock Animation Platform) loaded globally via CDN for site-wide use. The carousel is the first consumer; other pages/components can use it for any standard web animation needs.

| Detail | Value |
|---|---|
| Library | GSAP 3 |
| Plugins loaded | Core, Observer, Draggable, InertiaPlugin |
| CDN | `cdn.jsdelivr.net/npm/gsap@3/dist/` |
| Load method | `<script defer>` in `layouts/_partials/head-additions.html` |
| Carousel usage | `Draggable.create()` for finger-tracking, `InertiaPlugin` for momentum snap, `gsap.to()` for arrow/keyboard push animation |

**Why GSAP over a carousel-specific library:** We need animations beyond the carousel (page transitions, scroll effects, micro-interactions). GSAP is a general-purpose animation engine — one dependency covers all use cases instead of accumulating single-purpose libraries.

**All GSAP plugins are 100% free** (including commercial use) since Webflow's acquisition in April 2025.

---

## Bugs

### BUG: Viewport height jumps during slide transition — **FIXED**

**Symptom:** When clicking an arrow, the carousel viewport momentarily doubles in height. The new slide appears stacked below the outgoing slide, then the outgoing slide disappears and the viewport snaps back to single-slide height.

**Root cause:** The `--active` CSS class toggles slides between `position: absolute` (out of flow) and `position: relative` (in flow). During the GSAP transition, both the outgoing and incoming slides had `--active` simultaneously, meaning both were `position: relative` and in normal document flow — the viewport expanded to contain them stacked vertically.

**Fix:** At the start of the exit animation, immediately force the outgoing slide to `position: absolute` via GSAP `set()` so it leaves document flow. The incoming slide is the only one with `position: relative`, so the viewport height stays stable throughout the transition. The `--active` class is still removed in `onComplete` for cleanup, but the position override happens instantly.

### BUG: GSAP not available in inline shortcode scripts — **FIXED**

**Symptom:** Swipe/drag did not work on mobile. Arrow buttons worked fine. No console errors because the code silently skipped the GSAP Observer setup via a `typeof` guard.

**Root cause:** GSAP is loaded in `<head>` with `defer`, which means the scripts execute after the document finishes parsing. But the inline `<script>` inside the shortcode runs immediately when the browser encounters it during parsing — before the deferred scripts have loaded. At that point, `gsap`, `Observer`, `Draggable`, etc. are all `undefined`.

**Fix:** Wrapped the entire carousel init in `document.addEventListener('DOMContentLoaded', function () { ... })`. The `DOMContentLoaded` event fires after all `defer` scripts have executed, guaranteeing GSAP globals are available.

**General rule:** Any inline `<script>` in a shortcode that uses GSAP must wrap its init in `DOMContentLoaded`. This applies to all future components, not just the carousel. See the architecture readme for this guideline.

### BUG: Filter tabs use exact string match against tags — **NOTED**

**Symptom:** A testimonial with tag `Engineer` did not appear under the `Engineers` tab.

**Root cause:** The filter does a case-insensitive but otherwise exact match of the tab label against each tag in the YAML `tags` field. `"engineer" !== "engineers"`.

**Resolution:** The YAML tags must use the exact canonical tab label. This is by design — no fuzzy matching. When curating which testimonials appear under each tab, ensure the tag string matches the tab label exactly (e.g. `Engineers` not `Engineer`, `Designers` not `UX Design`). The ticket's "Tag alignment note" under Filter Categories documents this.

---

## Open Questions

*(none remaining for initial build)*
