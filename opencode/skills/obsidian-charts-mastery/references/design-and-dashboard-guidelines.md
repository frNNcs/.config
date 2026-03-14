# Design and Dashboard Guidelines

## Visual system rules

1. Define one palette and keep it stable.
2. Preserve semantic colors across charts (e.g., red always = blocked).
3. Keep text hierarchy consistent: title > subtitle > footnote.
4. Avoid clutter: too many categories, too many legends, too many effects.

## Color and theming

Use plugin theming or CSS variables (with theming enabled):

```css
:root {
  --chart-color-1: #4F46E5;
  --chart-color-2: #0EA5E9;
  --chart-color-3: #22C55E;
  --chart-color-4: #F59E0B;
  --chart-color-5: #EF4444;
}
```

## Dashboard composition

- Start with one KPI summary chart.
- Add one trend chart.
- Add one composition chart.
- Add one diagnostic detail chart.

Use balanced widths and predictable section order to improve scanability.

## Readability tactics

- Use concise labels.
- Use axis titles where ambiguity exists.
- Use `legendPosition: bottom` when horizontal space is constrained.
- For radial charts, set width to avoid oversized dominance.

## When to export as image

Export chart to image when:
- Sharing immutable snapshots
- Archiving release reports
- Preventing drift from live Dataview-backed data
