

I have a bunch of logo assets for the different places I've worked. We're going to present it as a grid with the most important logos largest. When you click the tabs, it will enphasize the logos that fit that tab. (So clicking "AI" will enlarge the logos for the AI companies I've worked for, "Finance" will enlarge the finance companies that I've worked for, etc...)



Clarification Questions:

**Q1**: Where are the logo assets stored? I couldn't find them in the project's `static/` or `assets/` folders. Do you need to add them, or are they in a different location?
*A:* I haven't put them in yet. THis is a question for you: where SHOULD I store them?

**Q2**: Can you provide a list of all the companies/logos and their categories? For example:
- JPMorgan → Finance
- Frog Design → (which category?)
- etc.
*A:* No. We're not at that point yet. I'm asking you how to design the component, I'll put in the assets later. I'll also classify them for what tabs they need to be a part of. 

**Q3**: Can a single logo belong to multiple categories? (e.g., a fintech company that's both "Finance" and "AI")
*A:* Yes. 

**Q4**: How should "importance" be determined for the default (ALL) view? Options:
- Recency (most recent work = largest)
- Duration of engagement
- Brand recognition
- Manual ranking you provide
*A:* I will manually determine what is important.

**Q5**: When a tab is selected, what should happen to non-matching logos?
- Stay visible but shrink/fade
- Completely hide
- Gray out but stay same size
*A:* Shrink/fade

**Q6**: Do you want animation/transitions when switching tabs, or instant changes?
*A:* Animations

**Q7**: Should the logos link anywhere when clicked? (e.g., to a case study, external site, or nothing)
*A:* No, they should not link anywhere. 


**Implementation Plan**

---

## Architecture Overview

The Logos Block will use Hugo's data-driven approach: a YAML data file defines the logos and their metadata, a Hugo partial renders the HTML, CSS handles sizing and transitions, and vanilla JS handles tab interactions.

---

## 1. File Structure

```
ux-portfolio/
├── data/
│   └── logos.yaml          # Logo definitions with categories & importance
├── layouts/
│   └── partials/
│       └── logos-block.html  # Hugo partial for rendering
├── assets/
│   └── css/
│       └── logos-block.css   # Styles (processed by Hugo Pipes)
├── assets/
│   └── js/
│       └── logos-block.js    # Tab interaction logic
└── static/
    └── images/
        └── logos/            # Your logo image files go here
            ├── jpm.svg
            ├── frog.svg
            └── ...
```

**Why `static/images/logos/`?** Hugo serves files from `static/` directly without processing. SVG logos don't need resizing, so this is simpler. If you later want Hugo to auto-generate multiple sizes (for responsive images), we'd move them to `assets/`.

---

## 2. Data Model (`data/logos.yaml`)

```yaml
tabs:
  - id: all
    label: "All"
  - id: ai
    label: "AI"
  - id: web3
    label: "Web3"
  - id: finance
    label: "Finance"

logos:
  - id: jpm
    name: "JPMorgan"
    image: "/images/logos/jpm.svg"
    importance: 1          # 1 = largest, higher = smaller
    categories:
      - finance

  - id: frog
    name: "Frog Design"
    image: "/images/logos/frog.svg"
    importance: 2
    categories:
      - ai
      - web3

  - id: example-fintech
    name: "Example Fintech"
    image: "/images/logos/example.svg"
    importance: 3
    categories:
      - finance
      - ai            # Can belong to multiple categories
```

**Importance scale**: You define this. Could be 1-5, or 1-10. The CSS will map importance values to sizes.

---

## 3. Hugo Partial (`layouts/partials/logos-block.html`)

The partial will:
- Read from `data/logos.yaml`
- Render tab buttons with data attributes
- Render logo grid items with `data-categories` and `data-importance` attributes
- Include the CSS and JS assets

---

## 4. CSS Behavior (`assets/css/logos-block.css`)

**Sizing by importance:**
- Importance 1 → largest (e.g., 150px)
- Importance 2 → medium (e.g., 100px)
- Importance 3+ → smaller (e.g., 70px)

**Tab filtering states:**
- `.logo-item` (default): full size based on importance, full opacity
- `.logo-item.emphasized`: full size, full opacity (matches active tab)
- `.logo-item.de-emphasized`: shrunk to ~50% size, opacity 0.3

**Transitions:**
- `transition: transform 0.3s ease, opacity 0.3s ease;`

---

## 5. JavaScript Behavior (`assets/js/logos-block.js`)

Vanilla JS (no dependencies). On tab click:
1. Update active tab styling
2. If "All" tab: remove all `.emphasized` / `.de-emphasized` classes
3. If category tab: 
   - Add `.emphasized` to logos whose `data-categories` includes the selected category
   - Add `.de-emphasized` to logos that don't match

---

## 6. Implementation Steps

| Step | Task | Files |
|------|------|-------|
| 1 | Create data file with placeholder entries | `data/logos.yaml` |
| 2 | Create Hugo partial | `layouts/partials/logos-block.html` |
| 3 | Create CSS with sizing tiers and transitions | `assets/css/logos-block.css` |
| 4 | Create JS for tab interactions | `assets/js/logos-block.js` |
| 5 | Add shortcode or direct partial call to homepage | `content/_index.md` |
| 6 | Test with placeholder logos | — |
| 7 | You add real logo assets and update `data/logos.yaml` | `static/images/logos/`, `data/logos.yaml` |

---

## 7. What You'll Need to Provide Later

1. **Logo image files** → place in `static/images/logos/`
2. **Update `data/logos.yaml`** with:
   - Each logo's filename
   - Categories it belongs to
   - Importance ranking (1 = most important)
3. **Tab labels** if different from All/AI/Web3/Finance

---

Ready to proceed with implementation?