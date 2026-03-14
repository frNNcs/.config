# Debugging and Caveats

## Fast triage

1. Validate YAML indentation (spaces-only).
2. Check chart type spelling (`polarArea`, `doughnut`, `sankey`).
3. Check labels/data alignment.
4. Check modifier compatibility with chart type.
5. Check source references (`id`, `file`, table block ID).
6. Check DataviewJS availability and plugin enabled state.

## Common failures and fixes

### Failure: Chart not rendering
- Cause: malformed YAML or missing required keys.
- Fix: start from minimal template; reintroduce modifiers incrementally.

### Failure: Values misaligned
- Cause: `labels` count does not match each `series.data` count.
- Fix: normalize arrays before rendering.

### Failure: Table-linked chart blank
- Cause: wrong block ID or layout mismatch.
- Fix: verify `^blockId`, `id`, `layout` (`rows|columns`), and optional `file` name.

### Failure: DataviewJS chart missing
- Cause: using `dataview` instead of `dataviewjs`, or no query results.
- Fix: run in `dataviewjs`, add fallback or empty-state handling.

### Failure: Sankey node mismatch
- Cause: inconsistent source/target labels across edges and maps.
- Fix: normalize node strings and keep maps keyed to exact names.

## Structural caveats from docs

- Some documentation snippets have indentation inconsistencies.
- Dataview integration is specifically `dataviewjs`.
- Export to image is command-based post-processing, not inline YAML config.

## Reliability checklist

- Keep templates versioned.
- Reuse a linter-like manual check before final output.
- Prefer deterministic source paths and naming conventions.
