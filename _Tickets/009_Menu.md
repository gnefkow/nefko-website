Let's create a menu so we can navigate around.

## Goal

Create a full-screen site menu that is useful to human visitors and legible to crawlers / AI readers as a clear map of the site.

This should follow the Figma menu designs, but implementation should match the existing Hugo + semantic CSS token system. Do not introduce Tailwind, React, or raw Figma hex values.

## Designs

Note that we have different states for the list item buttons, and there are different ones for desktop vs mobile.

- Desktop: https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2134-31843&t=FXNWKD7RhouXRNcI-1
- Mobile: https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2134-31886&t=FXNWKD7RhouXRNcI-1
- List items: https://www.figma.com/design/Re2xNaGCq70kuUzbNSTdgd/NEW---Portfolio--Blog--Resume?node-id=2134-31902&t=FXNWKD7RhouXRNcI-1

Figma observations:

- Menu overlay background is black.
- Desktop close button sits near the top-left of the overlay.
- Mobile close button is centered and fixed to the bottom of the screen, with a margin of `2em` between it and the bottom of the screen.
- Menu items are 64px / 4em tall with 16px / 1em horizontal padding.
- Menu label text is 28px. This maps to the existing `.h3` size (`--font-size-h3: 1.75rem`) rather than a new arbitrary type size.
- List items have separate visual states for default, current page, pointer-down, and selected.

## Existing site context

The site already has a minimal sticky header:

- `themes/nefkoPortfolio/layouts/_partials/site-header.html`
- `themes/nefkoPortfolio/layouts/_partials/site-navigation.html`
- `themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css`

Current behavior:

- Home pages show the logo + name.
- Child pages show a back link to the homepage.
- There is not yet a full menu component to modify, so this should be built as a new menu layer integrated into the existing header partial.

## Semantic color mapping

Architecture rule: never use raw hex codes in component CSS. Map Figma colors to tokens in `themes/nefkoPortfolio/assets/nefkoPortfolio/css/_styles.css`.

| Figma color | Figma role | Existing token mapping | Notes |
|---|---|---|---|
| `#000000` | Full-screen menu background | `var(--bg-inverse-primary)` | Exact match. |
| `#ffffff` | Current-page text, active text, close icon, current-page left border | `var(--text-inverse-primary)` | Exact match. For border use this same inverse text token unless a future inverse-border token is added. |
| `#cacaca` | Default inactive menu item text | `var(--text-inverse-secondary)` | Existing token is `#cccccc`, close visual match. Prefer token over adding a near-duplicate. |
| `#191919` | Pointer-down / selected item background | No exact existing token | Decision needed. Closest semantic family would be a new inverse surface token, but if we must only use existing tokens, use `var(--bg-inverse-primary)` and accept that the dark hover surface will not be visible against the overlay. |
| `#7e7e7e` | Mobile close button border | No exact existing token | Decision needed. Closest existing semantic role is `var(--border-tertiary)` (`#666666`), but it is darker than Figma. |
| `#8f8f8f` | Selected item border | No exact existing token | Decision needed. Closest existing semantic role is also `var(--border-tertiary)` (`#666666`), but it is darker than Figma. |

Recommended conservative choice for this ticket:

- Use existing tokens where exact or near-exact: `--bg-inverse-primary`, `--text-inverse-primary`, `--text-inverse-secondary`.
- Use `--border-tertiary` for inverse borders only if Nefko accepts the darker border.
- Do not add new color tokens unless visual fidelity to `#191919`, `#7e7e7e`, and `#8f8f8f` is more important than keeping the current token set small.

## Spacing / sizing mapping

Follow Tachyons scale / em equivalents rather than raw px.

| Figma value | Role | Implementation mapping |
|---|---|---|
| `16px` | Menu item horizontal padding, mobile close button padding | `1em` / Tachyons `pa3` equivalent where appropriate |
| `28px` | Menu item label size | Existing `.h3` / `var(--font-size-h3)` |
| `45px` | Close icon size | `2.8125rem`; consider whether `3rem` is close enough for maintainability |
| `64px` | Menu item height | `4em` |
| `31px` | Left inset in Figma | Map to `2em` unless matching the existing `page-gutter` (`1rem`) is preferred |
| `35px` mobile top inset | Map to `2em` |
| `2px` | Selected item radius | `2px` is acceptable if no Tachyons radius utility matches cleanly |
| `999px` | Mobile close button pill radius | `border-radius: 999px` is acceptable for a circle / pill pattern |
| `2em` | Mobile close button bottom margin | Use exactly `bottom: 2em` per ticket requirement |

## Menu content management

Menu contents should be managed in one explicit, human-editable data file:

- `data/site-menu.yaml`

Do not infer menu items from Hugo sections, page frontmatter, taxonomies, weights, or `hugo.toml` menu config. The whole point is that Nefko can open one small file and see exactly what appears in the menu.

Recommended first version:

```yaml
primary:
  - label: Home
    url: /

  - label: About
    url: /pages/about/

  - label: Contact
    url: /pages/contact/

  - label: For AI Readers
    url: /pages/for-ai-llm-readers/
```

The `primary` group is the human-facing menu. A `utility` group can be added later if Nefko wants a secondary area for administrative or AI-readable pages.

Implementation recommendation: include the utility links either in a visually secondary group near the bottom of the menu or in semantic HTML that is still crawlable. The menu should not become a complete sitemap unless we intentionally want it to feel like one for humans.

## Implementation plan

1. Add the explicit menu data file.
   - Create `data/site-menu.yaml`.
   - Put `primary` and optional `utility` link groups in this file.
   - Render links in file order.
   - Do not use `site.Menus.main` for this feature.

2. Build a new menu partial.
   - Add `themes/nefkoPortfolio/layouts/_partials/site-menu.html`.
   - Render links from `.Site.Data.site_menu.primary`.
   - If `utility` links exist, render `.Site.Data.site_menu.utility` as a secondary group.
   - Use semantic `<nav aria-label="Main menu">` and a real list (`ul` / `li`) so the structure is readable to humans, crawlers, and AI.
   - Mark the current page using `aria-current="page"` and a current-page CSS class.

3. Integrate the menu into the existing header.
   - Update `themes/nefkoPortfolio/layouts/_partials/site-navigation.html`.
   - Keep the existing home logo / child back-link behavior.
   - Add a menu open button to the header.
   - Include the menu overlay once per page.

4. Add menu CSS to `_styles.css`.
   - Add styles near the existing `Site header` section.
   - Use `var(--bg-inverse-primary)`, `var(--text-inverse-primary)`, `var(--text-inverse-secondary)`, and `var(--border-tertiary)` as decided above.
   - Use `.h3` / `var(--font-size-h3)` for menu link text.
   - Keep layout values in em/rem terms and document any unavoidable one-off values.

5. Add a small menu script.
   - Create something like `assets/nefkoPortfolio/js/site-menu.js` or put it wherever the existing asset pipeline expects local JS.
   - Toggle the overlay open / closed.
   - Toggle `aria-expanded` on the menu button.
   - Hide the menu from assistive tech when closed.
   - Close on Escape.
   - Return focus to the opener after closing.
   - Prevent background scroll while open.

6. Wire the script into the page.
   - Current `site-scripts.html` is empty.
   - Follow the existing `site-nav-scroll.js` loading pattern from `head-additions.html` if that is where local scripts are currently loaded.

7. Implement responsive layout.
   - Desktop: close button top-left, menu items start lower in the overlay.
   - Mobile: menu items start near the top; close button is centered, fixed to bottom, `bottom: 2em`.
   - Avoid duplicate desktop/mobile markup unless the behavior truly requires it.

8. Implement list item states.
   - Default inactive: inverse secondary text.
   - Current page default: inverse primary text + left border.
   - Pointer-down / active: inverse primary text and dark surface if token decision permits.
   - Selected / focus-visible: visible border and accessible outline.
   - Ensure keyboard focus is at least as visible as hover / pointer states.

9. Test.
   - Run the Hugo dev server.
   - Check home, a case study, a blog post, and a page.
   - Confirm current-page state works for sections and individual pages.
   - Confirm mobile close button position.
   - Confirm keyboard behavior: Tab, Shift+Tab, Enter/Space, Escape.
   - Confirm no raw Figma hex colors were added to component CSS.

## Open decisions before build

- Should utility links (`SiteIndex`, `For AI/LLM Readers`, `Links`) be visible in the menu, visually secondary, or only present in the existing site index / AI-readable files?
- Should we add new semantic tokens for inverse interactive surfaces and inverse borders, or accept the closest existing tokens?
- Should the child-page back link remain when the menu button is added, or should the header become logo + menu everywhere?