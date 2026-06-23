---
ticket: 002_css-semantic-tokens
status: complete
type: infrastructure
keywords:
  - CSS
  - design tokens
  - semantic tokens
  - CSS custom properties
  - CSS variables
  - color system
  - typography system
  - styling
  - theming
  - _styles.css
  - :root
  - bg-primary
  - text-primary
  - token utility classes
scope:
  - themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css
  - themes/nefkoPortfolio/layouts/
depends-on: []
blocks:
  - 002_Testimonials-Block
---

# 002: CSS Semantic Token System

## What was done

Established a centralized semantic token system using CSS custom properties (`:root` variables) and matching utility classes. Replaced all hardcoded Tachyons color classes across every layout template with token-based equivalents.

### Also: renamed `assets/ananke/` → `assets/nefkoPortfolio/`

The CSS assets directory still carried the upstream Ananke theme name. Renamed it to `nefkoPortfolio` and updated the one functional reference in `GetResource.html`. The output path was already `nefkoPortfolio/css/main.css`, so this was invisible to the built site.

---

## Token Definitions

All tokens live in `:root` at the top of `_styles.css`.

### Color Tokens

| Token | Value | Usage |
|---|---|---|
| `--bg-primary` | `#ffffff` | Page body, card backgrounds |
| `--bg-secondary` | `#f4f4f4` | Secondary sections (available but not default) |
| `--bg-tertiary` | `#e9e9e9` | Input fields, TOC, related content, button fills |
| `--bg-inverse-primary` | `#000000` | Header, footer, dark sections |
| `--text-primary` | `#000000` | Headings, body text, links |
| `--text-secondary` | `#333333` | Summary body text, list content |
| `--text-tertiary` | `#777777` | Labels, section tags, muted text |
| `--text-inverse-primary` | `#ffffff` | Text on dark backgrounds |
| `--text-inverse-secondary` | `#cccccc` | Secondary text on dark backgrounds |
| `--text-inverse-tertiary` | `#a4a4a4` | Muted text on dark backgrounds |
| `--border-primary` | `#eeeeee` | Card borders |
| `--border-secondary` | `#cccccc` | Button borders, blockquote borders |
| `--border-tertiary` | `#666666` | Heavier dividers |

### Typography Tokens

| Token | Value |
|---|---|
| `--font-family-body` | `'Lato', -apple-system, BlinkMacSystemFont, sans-serif` |
| `--font-family-heading` | same as body |
| `--font-size-h1` through `--font-size-h6` | `3rem` down to `1rem` |
| `--font-size-p` | `1rem` |
| `--font-size-sm` | `0.875rem` |
| `--font-weight-regular` | `400` |
| `--font-weight-heavy` | `700` |

### Typography Classes

`.h1` through `.h6` (regular weight), `.h1-heavy` through `.h6-heavy` (bold), `.p`, `.p-heavy`, `.p-sm`, `.p-sm-heavy`.

**Note:** Tachyons defines `.h1`–`.h6` as *height* classes. Our typography classes override those. If you need Tachyons heights, use the explicit Tachyons classes (`h1` = `height: 1rem`) sparingly or rename the typography classes.

### Utility Classes

| Class | Maps to |
|---|---|
| `.bg-primary` | `var(--bg-primary)` |
| `.bg-secondary` | `var(--bg-secondary)` |
| `.bg-tertiary` | `var(--bg-tertiary)` |
| `.bg-inverse-primary` | `var(--bg-inverse-primary)` |
| `.text-primary` | `var(--text-primary)` |
| `.text-secondary` | `var(--text-secondary)` |
| `.text-tertiary` | `var(--text-tertiary)` |
| `.text-inverse-primary` | `var(--text-inverse-primary)` |
| `.text-inverse-secondary` | `var(--text-inverse-secondary)` |
| `.text-inverse-tertiary` | `var(--text-inverse-tertiary)` |
| `.border-primary` | `var(--border-primary)` |
| `.border-secondary` | `var(--border-secondary)` |
| `.border-tertiary` | `var(--border-tertiary)` |

---

## Files Changed

| File | What changed |
|---|---|
| `assets/nefkoPortfolio/css/_styles.css` | Added `:root` tokens, typography classes, utility classes. Updated existing component styles to use tokens. |
| `layouts/_partials/func/style/GetResource.html` | Path changed from `/ananke/css/` to `/nefkoPortfolio/css/` |
| `layouts/baseof.html` | Body classes: `bg-near-white` → `bg-primary text-primary` |
| `layouts/_partials/site-header.html` | `bg-black` → `bg-inverse-primary` |
| `layouts/_partials/site-footer.html` | `bg-black` → `bg-inverse-primary` |
| `layouts/_partials/page-header.html` | `bg-black` → `bg-inverse-primary`, `bg-black-60` → `bg-inverse-primary o-60` |
| `layouts/_partials/summary.html` | `bg-white` → `bg-primary`, `gray` → `text-tertiary`, `near-black` → `text-primary` |
| `layouts/summary.html` | Same as above, plus button: `bg-light-gray` → `bg-tertiary` |
| `layouts/_partials/summary-with-image.html` | `dark-gray` → `text-secondary`, button tokens |
| `layouts/summary-with-image.html` | Same as partial version |
| `layouts/list.html` | `bg-white` → `bg-primary`, `mid-gray` → `text-secondary` |
| `layouts/post/list.html` | Same as list.html |
| `layouts/taxonomy.html` | Same as list.html |
| `layouts/post/summary.html` | `near-black` → `text-primary`, `mid-gray` → `text-secondary`, button tokens |
| `layouts/_shortcodes/form-contact.html` | `black-80` → `text-primary`, `bg-light-gray` → `bg-tertiary`, `bg-black` → `bg-inverse-primary` |
| `layouts/_partials/menu-contextual.html` | `bg-light-gray` → `bg-tertiary` (both TOC and related content blocks) |

---

## How to use in new components

In CSS within shortcodes or partials:

```css
.my-component {
  background-color: var(--bg-inverse-primary);
  color: var(--text-inverse-primary);
  border: 1px solid var(--border-tertiary);
}
```

Or as utility classes in HTML:

```html
<div class="bg-inverse-primary text-inverse-primary">
  Dark section content
</div>
```
