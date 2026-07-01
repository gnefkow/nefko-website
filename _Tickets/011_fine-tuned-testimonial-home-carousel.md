---
ticket: 011_fine-tuned-testimonial-home-carousel
status: built
type: refactor
keywords:
  - testimonials
  - testimonials-carousel
  - manual curation
  - inner content
  - shortcode
  - home-quote
  - tag filtering
depends-on:
  - 003_testimonials-carousel
scope:
  - layouts/shortcodes/testimonials-carousel.html
  - content/_index.md
blocks: []
---

# 011: Fine-tuned Testimonial Home Carousel

## Why

The carousel is currently populated by logic: it loads every file in `content/testimonials/`, hardcodes four filter tabs, and uses YAML `tags` to decide which slides appear under each tab. That wiring is hard to reason about and does not support hand-picking a specific quote version per tab (e.g. Charla under **Leadership** with `ambidexterity` and under **Engineers** with `engineering`).

The homepage will always show at most ~20 testimonials, and Kyle will hand-pick them. Manual configuration in `_index.md` is more legible than tag-matching logic.

---

## What we're building

Replace automatic population with **inner-content configuration** on the shortcode call. Tab labels, testimonial roster, quote version, and display order are all declared explicitly in `_index.md`.

### Authoring format (decided)

Use `{{<` / `{{< /` (not `{{%`) so inner content is not processed as Markdown. Indentation is allowed — the parser trims each line (same pattern as `case-study-summary`).

```markdown
{{< testimonials-carousel >}}
  [Leadership]
    john-dubuque | ambidexterity
    john-lees | enthusiasm
    charla-kunkel | ambidexterity
  [Engineers]
    charla-kunkel | engineering
{{< /testimonials-carousel >}}
```

| Syntax element | Meaning |
|---|---|
| `[Tab Label]` | Starts a filter tab. Tab label text is exactly what appears in the filter bar. Only tabs listed here are rendered — no hardcoded tab set. |
| `testimonial-slug \| version` | One carousel slide. Slug matches filename in `content/testimonials/` (without `.yaml`). `version` is a key inside that file's `key-quotes` list. |
| Line order | Display order within the tab. No separate `index` field needed. |
| Leading whitespace | Ignored (`strings.TrimSpace` per line). |

**Optional future extension:** allow `john-dubuque` without a version (fallback to `home-quote`). Not required for v1 if every slide always specifies a version.

### Data lookup (unchanged source files)

- Testimonial content still lives in `content/testimonials/*.yaml`.
- Carousel slide excerpt: `key-quotes` entry matching `version` (plain string value — not `big-quote`/`small-quote` pairs used by `testimonial-block`).
- Modal content: still `full-quote` from the same YAML file.
- Attribution: still first `worked-together` entry + `"X was a Y when I worked with them at Z"` context line.

---

## Implementation steps

| # | Task | File |
|---|---|---|
| 1 | Parse `.Inner` into a slice of tabs, each with ordered slides `{ testimonial, version }` | `layouts/shortcodes/testimonials-carousel.html` |
| 2 | Replace `readDir` bulk load with per-slide `readFile` for the referenced YAML only | same |
| 3 | Replace `home-quote` extraction with `version` key lookup in `key-quotes` | same |
| 4 | Generate filter tabs from parsed tab labels (first tab = active default) | same |
| 5 | Render one slide per configured row; set `data-tab` to the tab label (not `data-tags`) | same |
| 6 | Update JS tab filtering to match `data-tab` instead of YAML tags | same (inline `<script>`) |
| 7 | Update shortcode header comment with new usage docs | same |
| 8 | Remove duplicate empty shortcode call; keep single configured call | `content/_index.md` |
| 9 | Build + verify: tab switching, carousel drag/arrows, modal, responsive layout | — |

### Inner-content parsing spec

Mirror `themes/nefkoPortfolio/layouts/_shortcodes/case-study-summary.html`:

1. Split `.Inner` on `\n`.
2. `strings.TrimSpace` each line; skip empty lines.
3. Line matching `^\[(.+)\]$` → start new tab (capture label).
4. Line matching `^(.+?)\s*\|\s*(.+)$` → append slide to current tab.
5. Line with no `|` and no brackets → `warnf` and skip (or error in build).

If a tab header appears with no slides, omit the tab or warn. If a slide references a missing YAML file or missing `version` key, `warnf` at build time.

---

## Code to remove (old logical wiring)

### Hugo template — remove entirely

**1. Bulk directory scan** — loads every testimonial regardless of homepage intent:

```go-html-template
{{ $dir := "content/testimonials" }}
{{ $testimonials := slice }}
{{ range readDir $dir }}
  {{ if and (not .IsDir) (strings.HasSuffix .Name ".yaml") }}
    {{ $raw := readFile (printf "%s/%s" $dir .Name) }}
    {{ $data := $raw | transform.Unmarshal }}
    {{ $testimonials = $testimonials | append $data }}
  {{ end }}
{{ end }}
```

**2. Hardcoded category list** — tabs become author-defined via `[Brackets]`:

```go-html-template
{{ $categories := slice "Leadership" "Product" "Engineers" "Designers" }}
```

**3. `home-quote`-only extraction** — replace with lookup by configured `version`:

```go-html-template
{{ $homeQuote := "" }}
{{ with index $t "key-quotes" }}
  {{ range . }}
    {{ with index . "home-quote" }}
      {{ $homeQuote = strings.TrimSpace . }}
    {{ end }}
  {{ end }}
{{ end }}
```

**4. Tag-based slide attributes** — slides no longer carry YAML tags for filtering:

```go-html-template
data-tags="{{ index $t "tags" }}"
```

**5. Tab bar loop over `$categories`** — replace with loop over parsed tabs:

```go-html-template
{{ range $i, $cat := $categories }}
  <button class="testimonials-carousel__tab{{ if eq $i 0 }} testimonials-carousel__tab--active{{ end }}"
          data-category="{{ $cat }}"
          ...>
    {{ $cat }}
  </button>
{{ end }}
```

**6. Slide loop over all `$testimonials`** — replace with nested loop: tabs → configured slides → load YAML per slide.

### JavaScript — replace (do not delete carousel behavior)

**Tag-matching filter** — the core logic to strip; replace with exact tab-label match on `data-tab`:

```javascript
function getFiltered(category) {
  var result = [];
  var cat = category.toLowerCase();
  allSlides.forEach(function (slide, i) {
    var tags = slide.getAttribute('data-tags')
      .split(',')
      .map(function (t) { return t.trim().toLowerCase(); })
      .filter(function (t) { return t !== ''; });
    if (tags.indexOf(cat) !== -1) {
      result.push(i);
    }
  });
  return result;
}
```

**Replacement shape:**

```javascript
function getFiltered(category) {
  var result = [];
  var cat = category.toLowerCase();
  allSlides.forEach(function (slide, i) {
    if (slide.getAttribute('data-tab').toLowerCase() === cat) {
      result.push(i);
    }
  });
  return result;
}
```

Keep unchanged: GSAP Draggable, strip layout, pagination dots, arrow wrap-around, modal open/close, keyboard nav, resize handler, `DOMContentLoaded` wrapper.

### Shortcode header comment — update

Remove references to:
- `readDir` data loading
- Hardcoded categories `(Leadership, Product, Engineers, Designers)`
- Implicit "all YAML files" behavior

---

## What stays the same

| Area | Notes |
|---|---|
| CSS | All `.testimonials-carousel__*` styles — no design changes |
| Modal | Still shows `full-quote` from YAML |
| Attribution template | Unchanged context-line format |
| GSAP / Draggable / InertiaPlugin | Unchanged |
| `content/testimonials/*.yaml` | Still the data store; `tags` field remains for other uses but carousel ignores it |
| `testimonial-block` shortcode | Unaffected — case studies keep using `quote` param with `big-quote`/`small-quote` pairs |
| Filter bar UI | "Working with" label + scrollable tabs — only tab *source* changes |

---

## `_index.md` cleanup

Current file has a duplicate call — remove the empty self-closing shortcode on line 18 and keep only the configured block:

```markdown
{{< testimonials-carousel >}}
  [Leadership]
    john-dubuque | ambidexterity
    john-lees | enthusiasm
    charla-kunkel | ambidexterity
  [Engineers]
    charla-kunkel | engineering
{{< /testimonials-carousel >}}
```

---

## Acceptance criteria

- [ ] Carousel renders only the testimonials listed in `_index.md` inner content — not all YAML files
- [ ] Filter tabs match `[Bracket]` labels in inner content, in listed order
- [ ] Each slide shows the quote from the specified `version` key
- [ ] Same person can appear on multiple tabs with different `version` values
- [ ] Tab click shows only that tab's slides; carousel resets to slide 1
- [ ] Drag, arrows, dots, modal, and keyboard nav still work
- [ ] Build warns (does not silently fail) on missing YAML file or missing version key
- [ ] No references to hardcoded four-tab list or YAML `tags` filtering remain in the shortcode

---

## Out of scope

- Changing testimonial YAML schema (`tags`, `home-quote`, etc. can stay for other consumers)
- `work` param for alternate `worked-together` entries (always use index 0, same as today)
- Moving config to `data/home-testimonials.yaml` (inner content was chosen for legibility on the homepage)
- Updates to ticket 003 documentation (optional follow-up)
