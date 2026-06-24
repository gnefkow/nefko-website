# UX Portfolio — Architecture & Design Guidelines

This document tracks the principles and systems we use when building components for this site. Reference it during ticket planning and implementation.

---

## Colors & Design Tokens

**Never use raw hex codes.** All colors must reference CSS custom properties (design tokens) defined in the site's core style files. If a Figma design or any source provides hex values, cross-check them against the existing tokens and use the matching `var(--token-name)` instead.

### Core CSS files

| File | Purpose |
|---|---|
| `themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css` | Design tokens — colors, typography, semantic variables |
| `themes/nefkoPortfolio/assets/nefkoPortfolio/css/_tachyons.css` | Tachyons utility classes — widths, spacing, layout |

### Ticket process — handling hex codes

When a new ticket includes hex color values from Figma:
1. Look up each hex value in `_styles.css` and find the corresponding design token.
2. Document the hex-to-token mapping in the ticket.
3. If no existing token is a reasonable match, note it as a decision to discuss — do not silently hardcode a hex value.

---

## Widths, Spacing & Layout — Tachyons

This site uses [Tachyons](https://tachyons.io/), a functional CSS framework that provides a predefined scale for widths, spacing, typography, and layout. **We do not use arbitrary pixel values.** Everything should map to a Tachyons class or its equivalent `em` value.

### Key width classes

| Class | Value | Typical use |
|---|---|---|
| `measure-narrow` | `20em` (~320px) | Narrow text columns |
| `measure` | `30em` (~480px) | Default readable text width |
| `measure-wide` | `34em` (~544px) | Wider content areas (e.g. filter bars, article columns) |

### Spacing scale

Tachyons uses a numbered spacing scale (`pa0`–`pa7`, `ma0`–`ma7`, etc.) for padding and margin. The scale is exponential, not linear. Use these classes rather than custom pixel/rem values.

### Ticket process — handling arbitrary pixel values

When a new ticket comes in from Figma or any other source, **the planning step must include mapping any arbitrary pixel widths or spacing values to the closest Tachyons class.** Do not carry raw pixel values into the implementation.

Checklist for every new ticket:
1. Extract all pixel-based dimensions from the design (widths, padding, margins, gaps).
2. For each value, identify the appropriate Tachyons class or `em`-based equivalent.
3. Document the mapping in the ticket before building.
4. If no Tachyons class is a reasonable fit, note that in the ticket as a decision to discuss — do not silently hardcode a pixel value.

### When Tachyons classes are used in component CSS

Some components use inline `<style>` blocks (e.g. shortcodes). In these cases, reference the Tachyons `em` values directly rather than inventing pixel widths:

```css
/* Good — uses the Tachyons measure-wide equivalent */
max-width: 34em;

/* Bad — arbitrary pixel value */
max-width: 550px;
```

### Page column layout (gutter + reading width)

Tachyons sets `box-sizing: border-box` on most elements. **Do not put horizontal padding and `measure-wide` on the same element** — at the `60em` (960px) breakpoint, `ph5-l` padding eats into the `34em` cap and the content column suddenly narrows.

**Use two layers instead:**

```html
<div class="page-gutter pv3 pv4-l">
  <article class="measure-wide center ...">
    <!-- content -->
  </article>
</div>
```

| Layer | Class | Job |
|---|---|---|
| Outer | `.page-gutter` | Horizontal inset only (`1rem`; `4rem` at `60em`) — full viewport width |
| Inner | `.measure-wide` | Reading column max-width (`34em`) — **no horizontal padding** |

**Rules:**
- Layout templates (`home.html`, `list.html`, etc.) own the page column — not shortcodes.
- Shortcodes render content only; do not duplicate `measure-wide` or `ph3 ph5-l` wrappers.
- Full-bleed sections (e.g. testimonials carousel) break out of the article with `width: 100vw; margin-left: calc(-50vw + 50%)` and manage their own inner padding.

`.page-gutter` is defined in `_styles.css` and mirrors the `ph3` / `ph5-l` scale.

---

## Typography

Semantic heading and paragraph classes (`.h1`–`.h6`, `.p`, etc.) live in `_styles.css`.

**Tachyons name collision:** In Tachyons, `.h1`–`.h6` are **height** utilities (e.g. `.h5` = `height: 16rem`). Our typography classes reuse those names for **font size**. `_styles.css` sets `height: auto` on `.h1`–`.h6` to override the Tachyons heights — but prefer `.p` / `.p-sm` for body text and subtitles rather than `.h5` on a `<p>` when a paragraph is what you mean.

---

## Animations — GSAP

This site uses [GSAP (GreenSock Animation Platform)](https://gsap.com/) as its animation library. It is loaded globally via CDN in `layouts/_partials/head-additions.html` and is available on every page.

### Currently loaded plugins

| Package | Purpose |
|---|---|
| GSAP Core | Tweens, timelines, easing |
| Observer | Touch/pointer/scroll gesture detection |
| Draggable | Finger-tracking drag interactions (carousels, sliders, cards) |
| InertiaPlugin | Momentum/velocity-based snap after drag release |

Additional GSAP plugins (ScrollTrigger, Flip, etc.) can be added to `head-additions.html` as needed. All GSAP plugins are 100% free (including commercial use) since Webflow's acquisition in April 2025.

### Script loading — DOMContentLoaded required

GSAP is loaded via `<script defer>` in `<head>`. Deferred scripts execute after the document finishes parsing but before `DOMContentLoaded`. Shortcode components use inline `<script>` tags in the body, which run immediately when the browser encounters them during parsing — **before** deferred scripts have loaded.

**Rule:** Any inline `<script>` in a shortcode that references GSAP (or any other deferred library) must wrap its initialization in `document.addEventListener('DOMContentLoaded', function () { ... })`. Without this, GSAP globals will be `undefined` and the code will silently fail.

### Guidelines

- **Use GSAP for all animations.** Do not write custom CSS `@keyframes` or vanilla JS `requestAnimationFrame` loops. GSAP handles cross-browser performance, easing, and sequencing better than hand-rolled solutions.
- **Use GSAP Draggable + InertiaPlugin for drag/swipe interactions** rather than manual touch event listeners. Draggable provides finger-tracking and InertiaPlugin handles momentum-based snapping.
- **Use GSAP Observer for simpler gesture detection** (scroll-triggered behavior, non-drag swipe events) where full Draggable is overkill.
- When a ticket calls for animation, the implementation should use `gsap.to()`, `gsap.fromTo()`, `gsap.timeline()`, `Draggable.create()`, or the appropriate GSAP API — not a one-off approach.
- Keep animation durations and easing consistent across the site. Prefer GSAP's built-in eases (`power2.out`, `power2.inOut`, etc.) over custom cubic-bezier values.

### First consumer

The **testimonials carousel** (`layouts/shortcodes/testimonials-carousel.html`) is the first component using GSAP. It uses:
- `Draggable.create()` for finger-tracking push interaction on the slide strip
- `InertiaPlugin` for momentum-based snap to the nearest slide on release
- `gsap.to()` for arrow/keyboard-triggered push animations
