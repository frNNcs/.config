# Chart Types Playbook

## Decision matrix

Use this matrix to map analytical intent to chart type.

- Compare categories at one point: **bar**
- Observe trend over time: **line**
- Show part-to-whole (few categories): **doughnut** or **pie**
- Show radial weighted categories: **polarArea**
- Compare profiles across many dimensions: **radar**
- Show transitions or movement between states: **sankey**

## Type-by-type guidance

### bar
Prefer for ranking and category comparison. Handle negative values naturally.

Use when:
- Comparing entities (teams, tags, projects)
- Showing snapshots by period without continuity emphasis

Avoid when:
- Need flow semantics (prefer sankey)
- Need strong temporal continuity (prefer line)

### line
Prefer for temporal sequence and progression.

Use when:
- Daily/weekly trends
- Forecast overlays
- Gapped series (with optional `spanGaps`)

Useful modifiers:
- `fill`, `tension`, `spanGaps`, `bestFit`, `time`, `beginAtZero`

### doughnut / pie
Prefer for concise composition.

Use when:
- 3–7 categories
- Single point-in-time composition

Guidelines:
- Set explicit width (`40%` often works)
- Use `labelColors: true`

Avoid when:
- Too many slices
- Fine-grained comparisons are needed (prefer bar)

### polarArea
Prefer for proportional categories with radial impact.

Use when:
- Visual emphasis on magnitude by sector area

Guidelines:
- Set explicit width
- Use `labelColors: true`

### radar
Prefer for multi-axis profile comparison.

Use when:
- Capability or metric vectors across fixed dimensions

Guidelines:
- Keep dimensions moderate (5–10)
- Use explicit width

### sankey
Prefer for flow structure and weighted transitions.

Data model:
- `series[0].data`: list of triplets `[source, value, target]`
- Optional node maps: `priority`, `colorFrom`, `colorTo`

Use when:
- Movement among stages matters more than absolute totals

Avoid when:
- Only static category totals are needed (bar/doughnut better)

## Common anti-patterns

- Using pie/doughnut with high category counts
- Using line charts for unordered categories
- Using sankey without consistent node naming
- Mixing many design styles in one dashboard
