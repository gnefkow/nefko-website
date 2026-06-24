---
ticket: 005_nav-bar
status: built
type: component
keywords:
  - site-header
  - site-navigation
  - nav bar
  - scroll state
  - home header
  - child page header
  - back button
  - logo mark
  - sticky header
  - design tokens
  - GSAP Observer
scope:
  - themes/nefkoPortfolio/layouts/_partials/site-header.html
  - themes/nefkoPortfolio/layouts/_partials/site-navigation.html
  - themes/nefkoPortfolio/layouts/_partials/page-header.html
  - themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css
  - layouts/_partials/site-nav-scroll.js
  - static/images/logo-mark.svg
depends-on:
  - 002_css-semantic-tokens
blocks: []
---

# 005: Simple, Clean Header

Replace the current black inverse header with a minimal white header that matches Figma. Four visual states driven by **page type** (home vs child) and **scroll position** (≥ 40px).

**Status: built**

---

## Figma Source

| Frame | URL | What it shows |
|---|---|---|
| **Header** (component set) | [node 2100:32904](https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2100-32904) | All four nav variants in one component |

### Four variants (mobile, 390px wide)

| Variant | Figma symbol | Background | Horizontal padding | Shadow | Left content |
|---|---|---|---|---|---|
| **Home, not scrolled** | `State=home, Scoll=no` | White | 24px | None | Logo mark only (24×24) |
| **Home, scrolled** | `State=home, Scoll=yes` | White | 24px | Yes | Logo mark + “Kyle Becker” |
| **Child, not scrolled** | `State=child, Scoll=no` | White | 16px | None | Back button: arrow + page short title |
| **Child, scrolled** | `State=child, Scoll=yes` | White | 16px | Yes | Back button: arrow + page short title |

**Bar height:** 66px total (20px vertical padding + content).

**Out of scope for this ticket** (per Nefko):
- Large breakpoints / desktop nav layout
- Other navigation tabs (Contact, What is UX Strategy?, social icons)

---

## Current State (what we’re replacing)

The header today is an Ananke-era black bar:

```
site-header.html
  └── div.bg-inverse-primary          ← black background
        └── site-navigation.html
              ├── Site title link (white text, f3 fw2)
              ├── menu.main links     ← Contact, What is UX Strategy?
              └── social/follow.html  ← LinkedIn etc.
```

Problems:
- Black bar fights the rest of the site, which is white/light
- Case study pages embed the same black nav inside the hero cover (`page-header.html`), with white text over a dimmed photo
- No scroll-aware behavior
- Menu items and socials are in Figma’s future-state nav, not this ticket

**Body classes already available** (`baseof.html`):
- `is-home` on `/`
- `is-page`, `is-section`, `page-{slug}` on other pages

---

## Target Behavior

### Page-type detection

| Condition | Variant family |
|---|---|
| `.IsHome` (body has `is-home`) | **Home** variants |
| Everything else (pages, case studies, lists, taxonomies, 404…) | **Child** variants |

### Scroll detection

- Toggle scrolled state when `window.scrollY >= 40`
- Class on `<header>`: `.site-header.is-scrolled`
- Use **GSAP Observer** (already loaded globally) per site architecture — not a raw scroll listener

### Home variant logic

| State | Logo mark | “Kyle Becker” text |
|---|---|---|
| Not scrolled | Visible, links to `/` | Hidden |
| Scrolled | Visible, links to `/` | Visible beside logo |

The name appearing on scroll is the main home-page affordance — no separate menu needed in this ticket.

### Child variant logic

| State | Back control |
|---|---|
| Not scrolled | Arrow + short title |
| Scrolled | Same content + shadow |

**Back button** (Figma “Button” frame):
- White pill: 8px padding, 4px border-radius, 4px gap between icon and label
- Left arrow icon: 18×18
- Label: page short title (see open question Q1)
- **Proposed default:** links to `/` (home). Alternative: `history.back()` — needs Nefko’s call.

### Sticky / elevation

Figma’s scrolled variants add a bottom shadow, which implies the bar stays at the top while content scrolls beneath it.

**Proposed:** `position: sticky; top: 0; z-index: 100` on `.site-header`, with shadow applied via `.site-header.is-scrolled`.

### Case study hero pages

Today `page-header.html` renders nav *inside* the cover image with a dark overlay. The new design is a **white bar**, which cannot sit on the dimmed hero the same way.

**Proposed:** Extract nav out of the hero cover. Structure becomes:

```
site-header (white, sticky)     ← always on top
main
  └── page-header (hero image only, no nav inside)
```

This is a visible layout change on case studies — the hero starts below the white nav instead of behind it.

---

## Color Mapping (Figma → design tokens)

| Figma value | Token / class | Notes |
|---|---|---|
| `#FFFFFF` background | `var(--bg-primary)` / `.bg-primary` | Exact match |
| `#000000` text & icons | `var(--text-primary)` / `.text-primary` | Exact match |
| Shadow `0px 14px 5.9px -12px rgba(0,0,0,0.25)` | **New token** `--shadow-header-scrolled` | No existing shadow token. Add to `:root` in `_styles.css`. |

No raw hex in component CSS.

---

## Typography Mapping

Nefko OK’d approximate typography. Map to existing system where close enough.

| Figma | Size | Weight | Proposed implementation |
|---|---|---|---|
| “Kyle Becker” (home scrolled) | ~19.7px | Lato Light (300) | `.h5` + `fw3` (Tachyons light). Close to 18px h5; weight 300 not in tokens today — use Tachyons `fw3` rather than new token unless we want `--font-weight-light`. |
| Page short title (child) | 18px | Lato Medium (500) | `.h5` + `fw5` (Tachyons medium) |

Both use `--font-family-heading` (Lato) via `.h5`.

---

## Spacing Mapping (Figma px → Tachyons / custom)

Ticket scope is mobile-first; large breakpoints deferred.

| Figma value | Closest Tachyons | Plan |
|---|---|---|
| Bar height 66px | — | Custom `.site-header { min-height: 66px }` — no Tachyons height match |
| Vertical padding 20px | `pv4` = 32px, `pv3` = 16px | Custom `padding-top/bottom: 1.25rem` (20px) on `.site-header__inner` — note in ticket, not silent hardcode elsewhere |
| Home horizontal 24px | `ph3` = 16px, `ph4` = 32px | Custom `1.5rem` on home variant — or accept `ph3` (16px) as close enough |
| Child horizontal 16px | `ph3` = 1rem | `.site-header--child .site-header__inner { padding-left/right: 1rem }` ✓ |
| Back button padding 8px | `pa2` | ✓ |
| Back button radius 4px | — | Custom `border-radius: 4px` on `.site-header__back` |
| Icon gap 4px | — | Custom `gap: 0.25rem` |
| Logo mark 24×24 | — | Fixed SVG dimensions |
| Arrow icon 18×18 | — | Fixed SVG dimensions |

---

## Assets Needed

**Nefko does not need to export SVGs.** Web Team handles both during implementation.

| Asset | Figma node | How we get it |
|---|---|---|
| **Back arrow** | `2100:32974` (icon/arrow-narrow-left) | Figma MCP returns a downloadable SVG asset URL. Save to `static/images/icon-arrow-left.svg`. Use `currentColor` fill. |
| **Logo mark** | `2100:32695` (Frame49) | Not a vector export — Figma describes it as two black rectangles with known proportions. Hand-write a 24×24 SVG from Figma inset values (or inline in the partial). Store at `static/images/logo-mark.svg`. |

Figma MCP asset URLs expire after ~7 days; assets must be committed to the repo during implementation, not hot-linked.

---

## Proposed DOM Structure

```html
<header class="site-header site-header--home|child [is-scrolled]">
  <nav class="site-header__inner" role="navigation" aria-label="…">
    {{ if .IsHome }}
      <a class="site-header__brand" href="/">
        <img class="site-header__logo" src="…/logo-mark.svg" alt="Kyle Becker" />
        <span class="site-header__name h5 fw3">Kyle Becker</span>
      </a>
    {{ else }}
      <a class="site-header__back pa2 …" href="/">
        <svg class="site-header__back-icon" …></svg>
        <span class="site-header__back-label h5 fw5">{{ $shortTitle }}</span>
      </a>
    {{ end }}
  </nav>
</header>
```

**Removed from this ticket’s markup:** `menu.main` loop, `social/follow.html`, i18n list. Keep the partials/files intact — just stop including them in `site-navigation.html` for now so a future nav ticket can re-wire them.

---

## Files to Change

| File | Change |
|---|---|
| `site-header.html` | Replace `bg-inverse-primary` wrapper with `.site-header` BEM block; pass page context |
| `site-navigation.html` | Rewrite to home/child markup above; drop menu + socials |
| `page-header.html` | Remove nav from inside hero cover; hero becomes image-only |
| `_styles.css` | Add `.site-header*` component styles + `--shadow-header-scrolled` token |
| `layouts/_partials/site-nav-scroll.js` | New — GSAP Observer toggles `.is-scrolled` at 40px |
| `site-scripts.html` (theme) or project override | Include scroll script globally |
| `static/images/logo-mark.svg` | New asset |

**Optional content work** (if Q1 answer is custom field):
- Add `short_title` to page/case-study front matter where `.Title` is too long

---

## Scroll Script (sketch)

```javascript
document.addEventListener('DOMContentLoaded', function () {
  var header = document.querySelector('.site-header');
  if (!header || typeof Observer === 'undefined') return;

  var threshold = 40;

  function setScrolled(scrolled) {
    header.classList.toggle('is-scrolled', scrolled);
  }

  setScrolled(window.scrollY >= threshold);

  Observer.create({
    target: window,
    type: 'scroll',
    onChange: function (self) {
      setScrolled(self.scrollY() >= threshold);
    }
  });
});
```

Shadow transition: CSS `transition: box-shadow 0.2s ease` on `.site-header` — no GSAP tween needed for a binary class toggle.

---

## CSS Sketch (key rules)

```css
:root {
  --shadow-header-scrolled: 0 14px 5.9px -12px rgba(0, 0, 0, 0.25);
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: var(--bg-primary);
  transition: box-shadow 0.2s ease;
}

.site-header.is-scrolled {
  box-shadow: var(--shadow-header-scrolled);
}

.site-header__inner {
  display: flex;
  align-items: center;
  min-height: 66px;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
}

.site-header--home .site-header__inner {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.site-header--child .site-header__inner {
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Home: name hidden until scroll */
.site-header__name {
  display: none;
  color: var(--text-primary);
}
.site-header.is-scrolled .site-header__name {
  display: inline;
}

.site-header__back {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem;
  border-radius: 4px;
  background: var(--bg-primary);
  color: var(--text-primary);
  text-decoration: none;
}
```

(Flesh out brand link layout, logo sizing, focus states during implementation.)

---

## Decisions (resolved)

| # | Question | Decision |
|---|---|---|
| **Q1** | Page short title source | Nefko will add `short_title` to page front matter. Template reads `Params.short_title`, falls back to `.Title` until every page has one. |
| **Q2** | Back button destination | Link to home: `href="/"` |
| **Q3** | Case study hero layout | White bar above hero (matches Figma). Nav extracted from cover in `page-header.html`. |

### Front matter convention

```yaml
---
title: A Digital Transformation in a Burmese Bank
short_title: Yoma Bank
---
```

Nefko owns the content pass. Implementation can ship before all pages have `short_title`; fallback keeps things working.

---

## Trade-offs

| Choice | Why | Cost |
|---|---|---|
| Hide menu + socials now | Matches Figma scope; simplifies first ship | Contact / social temporarily unreachable from nav until a follow-up ticket |
| Sticky header | Shadow-on-scroll implies fixed top bar | Reserves 66px vertical space at all times; content scrolls under shadow |
| GSAP Observer for scroll | Architecture convention | Slightly heavier than 5 lines of vanilla JS for a class toggle |
| Custom px for bar height/padding | Figma values don’t land on Tachyons scale | Documented in ticket; acceptable per mobile-first scope |
| `short_title` front matter | Clean child nav labels | One-time content pass on long-titled pages |

---

## Test Plan (for implementation phase)

- [ ] **Home `/`:** logo only at top; after scrolling 40px, name appears + shadow
- [ ] **Child page** (e.g. `/pages/contact/`): back control + title; shadow after 40px
- [ ] **Case study with hero:** white nav above hero image; no black overlay nav
- [ ] **Case study without hero / plain page:** same child variant
- [ ] **Scroll back to top:** shadow and home name hide again
- [ ] **Keyboard:** back link and logo link focus-visible
- [ ] **No regressions:** page content still uses `.page-gutter` / `measure-wide` below header

---

## Implementation Order (when approved)

1. Add CSS tokens + `.site-header` styles to `_styles.css`
2. Add logo + arrow SVG assets
3. Rewrite `site-navigation.html` + `site-header.html`
4. Update `page-header.html` (extract nav from hero)
5. Add scroll script + wire into global scripts
6. Visual QA against Figma mobile frames (Nefko adds `short_title` to content on his own schedule)
