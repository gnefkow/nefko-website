This is a quote block:
https://www.figma.com/design/joXmwjmWx44fSTAAIRiHmm/Website?node-id=2040-137&t=7MIqDU69VDSeaCRf-1

Our goal is to:
1. Create this as a re-usable block in our library for ux-portfolio, and
2. Create a {{code standard}} so that we can pass in the values for this on pages of the website. 
3. Update our testimonial yaml structure so we can pull in these quotes. 

In our figma example, our code would look like:
 {{ 
    testimonial: "tricia-wang.yaml"
    quote: "cradl-onboarding-quote"
 }}



## Implementation plan

### Component naming — **PROPOSED**

| Component | Shortcode | Purpose |
|---|---|---|
| **Quote block** (this ticket) | `{{< quote-block >}}` | Single dark testimonial card with portrait, two-part quote, and attribution — for case studies and article body |
| Testimonials carousel (existing) | `{{< testimonials-carousel >}}` | Homepage filter + carousel + modal — uses `home-quote`, not quote blocks |

Shared data: `content/testimonials/*.yaml`. Shared assets: `static/images/testimonial-avatars/`.

---

### Figma source — **VERIFIED**

https://www.figma.com/design/joXmwjmWx44fSTAAIRiHmm/Website?node-id=2040-137

Node `2040:137` — `Ref-block_Tricia-Wang`. Figma MCP access confirmed.

**Note:** Figma uses Merriweather; the site uses Lato via design tokens. Typography will be approximate — map to closest existing classes, do not add Merriweather.

---

### What we're building

A reusable inline block for case study / article pages:

1. **Portrait strip** — narrow vertical crop of the testimonial photo (left)
2. **Quote column** — `big-quote` (bold lead line) + `small-quote` (italic body)
3. **Attribution** — first name, last name, job title, company

No JS required. No modal. Renders inside the page column (`measure-wide`), not full-bleed.

---

### Shortcode API — **PROPOSED**

```markdown
{{< quote-block
  testimonial="tricia-wang"
  quote="cradl-onboarding-quote"
>}}
```

| Parameter | Required | Example | Notes |
|---|---|---|---|
| `testimonial` | yes | `tricia-wang` or `tricia-wang.yaml` | Filename in `content/testimonials/` (extension optional) |
| `quote` | yes | `cradl-onboarding-quote` | Key inside the `key-quotes` list |
| `work` | no | `0` | Which `worked-together` entry to use for title/company. Default `0` (first entry). |

**Error handling:** If the YAML file, quote key, or required sub-fields (`big-quote`, `small-quote`) are missing, render nothing (or a Hugo build warning in dev) — do not fall back to `full-quote` or `home-quote`.

---

### Field mapping (Figma → YAML → template)

| UI element | YAML field | Template variable | Notes |
|---|---|---|---|
| Portrait | `photo` | `$photo` | `<img src="{{ $photo }}" alt="{{ $fullName }}">` |
| Big quote line | `key-quotes` → `{quote}` → `big-quote` | `$bigQuote` | Lead sentence; Figma shows opening curly quote in text — include in YAML string if desired |
| Small quote body | `key-quotes` → `{quote}` → `small-quote` | `$smallQuote` | Italic supporting text |
| **Tricia** | `first-name` | `$firstName` | Rendered as separate span (Figma has two text nodes) |
| **Wang** | `last-name` | `$lastName` | Same line as first name, space between |
| Title line | `worked-together[n].title` | `$work.title` | e.g. `Executive Director` — **not** the carousel's "X was a Y when…" sentence |
| Company line | `worked-together[n].company` | `$work.company` | e.g. `Crypto Research and Development Lab (CRADL)` |

**Example — Tricia Wang (`tricia-wang.yaml`):**

```yaml
first-name: Tricia          →  Tricia
last-name: Wang             →  Wang
photo: /images/...          →  portrait
worked-together[0].title   →  Executive Director
worked-together[0].company →  Crypto Research and Development Lab (CRADL)
key-quotes → cradl-onboarding-quote:
  big-quote                →  "Kyle was a key leader on our design research team."
  small-quote              →  "his ability to quickly ramp up…"
```

**Figma vs YAML content drift:** Figma shows title **"Founder & Executive Director"** and company **"Crypto Research & Design Lab"**. YAML currently has **"Executive Director"** and **"Crypto Research and Development Lab (CRADL)"**. The component renders YAML as source of truth; update YAML separately if copy should match Figma.

---

### YAML structure — **DECIDED** (Tricia); pattern for others

Nested quote entries inside `key-quotes` use a **mapping** with `big-quote` and `small-quote` — not a block scalar (`|`):

```yaml
key-quotes:
  - home-quote: |
      (carousel excerpt — unchanged)
  - cradl-onboarding-quote:
      big-quote: "Lead sentence."
      small-quote: "Supporting paragraph."
```

**Data prep:** `tricia-wang.yaml` — done. Other testimonials get quote-block entries only when a page needs them (no bulk migration required for this ticket).

**Hugo lookup pattern** (mirror carousel's `home-quote` extraction, but keyed by `quote` param):

```go
{{ range index $t "key-quotes" }}
  {{ with index . $quoteKey }}
    {{ $bigQuote = index . "big-quote" }}
    {{ $smallQuote = index . "small-quote" }}
  {{ end }}
{{ end }}
```

---

### Hex-to-token mapping

All component colors must use `var(--token-name)` from `_styles.css`. No raw hex in component CSS.

| Figma value | Closest token | Usage |
|---|---|---|
| `#222222` card background | `var(--bg-inverse-primary)` | Figma is slightly lighter than `#000`; acceptable approximation |
| `#ffffff` quote + name | `var(--text-inverse-primary)` | Big quote, small quote, name |
| `#dddddd` title + company | `var(--text-inverse-secondary)` | Muted attribution lines (`#ddd` ≈ `#ccc`) |
| White page padding area | (none — inherits page) | Block sits on normal article background |

**Shadow:** Figma uses a multi-layer drop shadow. Closest existing token: `var(--shadow-callout-block)`. If the visual is too flat, add `--shadow-quote-block` to `:root` in `_styles.css` — document in ticket before hardcoding rgba values in the component.

**Image shadow:** Figma adds a separate shadow on the portrait crop. No matching token today. Options: (a) reuse `--shadow-callout-block` at reduced opacity via a single component rule, or (b) add `--shadow-quote-block-portrait` — decide at build time.

---

### Typography mapping (Figma → design system)

Figma specifies Merriweather; site uses Lato. Use semantic classes from `_styles.css` + inverse color overrides on the dark card.

| Figma | Size | Weight / style | Proposed implementation |
|---|---|---|---|
| Big quote | 16px | Black / heavy | `.h6-heavy` + `color: var(--text-inverse-primary)` on `.quote-block__big-quote` |
| Small quote | 12px | Light italic | `.p-sm` + `font-style: italic` + inverse primary color — **12px has no token**; `--font-size-sm` is 14px (closest) |
| Name | 12px | Black / heavy | `.p-sm-heavy` + inverse primary — same 12px → 14px approximation |
| Title + company | 8px | Regular | `.p-sm` + inverse secondary — **8px has no token**; 14px is closest readable minimum |

**Decision:** Accept ~2px size drift on small text rather than introducing one-off pixel font sizes. Do **not** load Merriweather.

**Utility classes in markup:** Prefer semantic BEM classes (`.quote-block__*`) with token references in CSS — same pattern as `.callout-block`. Typography base can `@extend` or duplicate token vars, not Tachyons font-size utilities mixed ad hoc.

---

### Spacing & layout mapping (Figma px → Tachyons / tokens)

Per `_readme-architecture.md`: map Figma dimensions to Tachyons scale or documented custom values in component CSS only.

| Figma | Value | Proposed implementation |
|---|---|---|
| Card max width | 474px | `max-width: 30em` — Tachyons `measure` (~480px) |
| Outer wrapper padding | 24px × 36px | Block margin `2rem 0` (matches `.callout-block`); no extra outer padding — page gutter handles horizontal inset |
| Card inner padding | 16px | `padding: 1rem` — Tachyons `pa3` equivalent |
| Gap: image ↔ text | 25px | `gap: 1.5rem` (~24px) |
| Gap: big ↔ small quote | 6px | `gap: 0.375rem` or `margin-bottom: 0.375rem` on big quote |
| Gap: quote block ↔ attribution | 25px | `gap: 1.5rem` on text column flex |
| Gap: name parts | 2px | `gap: 0.125rem` on name row |
| Gap: title ↔ company | 2px | `gap: 0.125rem` on attribution meta |
| Portrait column width | 71px | `width: 4.5rem` — no Tachyons width match; scoped to `.quote-block__photo` |
| Portrait column height | 185px | `height: 11.5rem` — scoped custom; `object-fit: cover` + overflow hidden |
| Border radius | 1px | `border-radius: 1px` — decorative micro-radius, acceptable one-off |

**Layout:** `display: flex; flex-direction: row; align-items: flex-start` on card. Text column `flex: 1; min-width: 0` for wrapping.

**Responsive (proposed):** Below ~30em card width, stack portrait above text OR shrink portrait — decide at build; mobile Figma frame not provided.

---

### File structure — **PROPOSED**

Follow `callout-block` (theme shortcode + CSS in `_styles.css`) and `testimonials-carousel` (YAML read via `readFile` + `transform.Unmarshal`):

```
ux-portfolio/
├── content/
│   └── testimonials/
│       └── tricia-wang.yaml          # cradl-onboarding-quote — done
├── layouts/
│   └── shortcodes/
│       └── quote-block.html          # Shortcode template + YAML load logic
└── themes/nefkoPortfolio/assets/nefkoPortfolio/css/
    └── _styles.css                   # .quote-block, .quote-block__* rules (after .callout-block)
```

CSS class prefix: `quote-block` (e.g. `.quote-block__card`, `.quote-block__big-quote`).

Update `_readme-architecture.md` **Our Blocks** table with `quote-block` row after implementation.

---

### Implementation steps

| Step | Task | Files |
|---|---|---|
| 0 | ~~YAML structure for nested quotes~~ | `content/testimonials/tricia-wang.yaml` — **done** |
| 1 | Create `quote-block` shortcode — load YAML by `testimonial` param, extract `quote` key from `key-quotes`, map fields per table above | `layouts/shortcodes/quote-block.html` |
| 2 | Add component CSS using design tokens only; BEM prefix `quote-block__*` | `themes/.../css/_styles.css` |
| 3 | Portrait crop + shadow (CSS `overflow: hidden`, `object-fit: cover`, optional shadow token) | `_styles.css` |
| 4 | Add shortcode to a test page (e.g. CRADL onboarding case study) | `content/case-studies/cradl-onboarding/index.md` (or rocketbook stub) |
| 5 | Document shortcode in ticket + `_readme-architecture.md` | this ticket, architecture readme |
| 6 | Visual QA against Figma screenshot — spacing/typography approximate, not pixel-perfect | — |

---

### Decisions log

| Topic | Status | Proposal |
|---|---|---|
| Font family | **Decided** | Lato via tokens — no Merriweather |
| Attribution format | **Decided** | Direct title + company lines from `worked-together` — not carousel context sentence |
| Data location | **Decided** | `content/testimonials/` via `readFile` (same as carousel) |
| CSS location | **Proposed** | `_styles.css` component section (like `callout-block`), not inline in shortcode |
| Card background `#222` | **Proposed** | Approximate with `--bg-inverse-primary` |
| 8px / 12px Figma type | **Proposed** | Use `--font-size-sm` (14px) — note drift in QA |
| Multi-layer shadow | **Open** | Start with `--shadow-callout-block`; add token if insufficient |
| `worked-together` index | **Proposed** | Default first entry; optional `work` param for testimonials with multiple roles |
| Multiple quote blocks per page | **Decided** | Supported — each shortcode invocation is independent |

---

### Test plan

- [ ] `hugo server` builds with no template errors
- [ ] Shortcode with `testimonial="tricia-wang"` + `quote="cradl-onboarding-quote"` renders all fields
- [ ] Missing `quote` key or bad filename renders safely (no broken layout)
- [ ] Inspect computed styles — no raw hex except documented micro-radius
- [ ] Name renders as `{first-name} {last-name}` with correct photo alt text
- [ ] Title and company come from `worked-together[0]`
- [ ] Block width respects `measure` (~30em) inside article column
- [ ] Compare side-by-side with Figma screenshot — layout hierarchy matches (portrait left, quote stack, attribution below)