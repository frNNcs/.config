# YAML Patterns and Modifiers

## Canonical base structure

```chart
type: line
labels:
  - 2026-01
  - 2026-02
  - 2026-03
series:
  - title: Revenue
    data:
      - 120
      - 135
      - 128
```

## Modifier catalog (high-value)

### Layout and visibility
- `width`: CSS width, default `100%`; strongly useful for radial charts
- `legend`: true/false
- `legendPosition`: `top|left|bottom|right`
- `beginAtZero`: force numeric baseline

### Line-specific
- `fill`: area under line
- `tension`: 0–1 smoothing
- `spanGaps`: connect points through nulls
- `bestFit`: trend line
- `bestFitTitle`: custom trend label
- `bestFitNumber`: index of target series for trend

### Axis and orientation (bar/line)
- `indexAxis`: `x|y`
- `stacked`: stack series
- `xTitle`, `yTitle`
- `xReverse`, `yReverse`
- `xMin`, `xMax`, `yMin`, `yMax`
- `xDisplay`, `yDisplay`
- `xTickDisplay`, `yTickDisplay`

### Radial and transparency
- `labelColors`: link label colors to segments
- `rMax`: max radial scale (radar/polar)
- `transparency`: global alpha override (0.0–1.0)

### Time axis
- `time`: enable date/time axis treatment (`day|week|month|year|...`)

## Compatibility hints

- Apply line modifiers (`fill`, `tension`, `bestFit`) only to `line`.
- Apply `indexAxis` and stack orientation primarily to `bar`/`line`.
- Use radial width controls for `pie`, `doughnut`, `radar`, `polarArea`.

## Safe defaults

- Keep `legend: true` by default.
- Set radial chart `width: 40%` unless layout demands otherwise.
- Enable `beginAtZero` for count-like metrics.
- Use `time` when labels are dates.

## Validation checklist before final output

1. Ensure spaces-only indentation.
2. Ensure every series has aligned data length with labels.
3. Ensure modifier belongs to chart type.
4. Ensure strings with spaces are quoted if needed.
5. Ensure negative values are expected and meaningful.
