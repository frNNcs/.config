---
name: obsidian-charts-mastery
description: This skill should be used when the user asks to "crear un chart en Obsidian", "generar dashboard con Obsidian Charts", "usar dataviewjs para gráficos", "convert chart to image", "build charts for my vault", "design consistent charts", "chart from markdown table", or "debug chart yaml".
version: 0.1.0
---

# Obsidian Charts Mastery

Generate high-quality charts for Obsidian notes using robust YAML, clear data modeling, and consistent visual design.

## Objetivo

Produce charts that are:
- Correct (valid YAML, aligned data lengths, compatible modifiers)
- Readable (titles, legends, axis labeling, balanced density)
- Reusable (templates, repeatable structure)
- Maintainable (clear data source strategy and troubleshooting path)

## Flujo operativo

1. Identify chart intent (comparison, trend, composition, flow, distribution).
2. Choose source strategy:
   - Inline YAML arrays
   - Markdown table (`id`, optional `file`, `layout`, `select`)
   - DataviewJS extraction (`dv.current()`, `dv.pages()`)
3. Select chart type and preset.
4. Apply modifiers for readability and semantics.
5. Validate structure and run caveat checks.
6. Export as image when immutable sharing is needed.

## Selección rápida de tipo de chart

- **bar**: category comparison (rankings, month-to-month counts)
- **line**: temporal trend and continuity
- **doughnut/pie**: proportion at one point in time
- **polarArea**: weighted categories with radial emphasis
- **radar**: profile/competency vectors across dimensions
- **sankey**: flow from source to target with volume

Consult `references/chart-types-playbook.md` for decision heuristics and anti-patterns.

## Patrones YAML canónicos

Use this baseline for most charts:

```chart
type: bar
labels:
  - Jan
  - Feb
  - Mar
series:
  - title: Team A
    data:
      - 12
      - 18
      - 15
```

For robust authoring and modifier compatibility, consult `references/yaml-patterns-and-modifiers.md`.

## Estrategias de fuente de datos

### 1) Inline
Use for static or ad-hoc insight snapshots.

### 2) Chart from Table
Use when table readability in Markdown must stay primary.
- Require block id (`^tableId`) in source table
- Set `id` in chart block
- Use `layout: rows|columns`
- Use `file` for cross-note table sources

### 3) DataviewJS / API
Use for dynamic vault analytics.
- Build arrays with `dv.pages()` and transforms
- Render via `window.renderChart(chartData, this.container)`
- Or generate `chart` codeblocks with `dv.paragraph(...)`

Full recipes: `references/data-sources-recipes.md`.

## Reglas de diseño

- Keep one palette per dashboard.
- Preserve semantic color mapping across all charts.
- Prefer `legend: true` unless labels are directly encoded.
- Limit category count per chart to avoid visual overload.
- For radial charts (`pie`, `doughnut`, `radar`, `polarArea`), set explicit width (commonly `40%`).
- Prefer `labelColors: true` in radial distributions.

Detailed style system: `references/design-and-dashboard-guidelines.md`.

## Debugging y validación

Always verify:
- YAML indentation is consistent (spaces only)
- `labels.length` matches each `series[n].data.length` (except sankey edge format)
- Table `id` exists and `layout` matches shape
- DataviewJS context and plugin availability
- Modifier/type compatibility (line-only options not applied to pie, etc.)

See full checklist and error map in `references/debugging-and-caveats.md`.

## Exportación a imagen

When reproducible static output is required, use plugin command:
- **Create image from Chart**

Tune image quality/format in plugin settings.

## Additional Resources

### Reference Files
- `references/chart-types-playbook.md`
- `references/yaml-patterns-and-modifiers.md`
- `references/data-sources-recipes.md`
- `references/design-and-dashboard-guidelines.md`
- `references/debugging-and-caveats.md`

### Example Files
- `examples/01-bar-basic.md`
- `examples/02-line-time-bestfit.md`
- `examples/03-radar-competency.md`
- `examples/04-doughnut-distribution.md`
- `examples/05-polar-area-priority.md`
- `examples/06-sankey-flow.md`
- `examples/07-chart-from-table.md`
- `examples/08-dataviewjs-integration.md`

### Scripts
- `scripts/README.md` (documents script strategy and optional automation points)
