# Example 02 — Line with time and trend

```chart
type: line
labels:
  - 2026-01-01
  - 2026-02-01
  - 2026-03-01
  - 2026-04-01
series:
  - title: Throughput
    data:
      - 102
      - 111
      - 120
      - 124
time: month
bestFit: true
bestFitTitle: Trend
tension: 0.25
fill: false
beginAtZero: true
legendPosition: top
```

Why:
- Emphasize trend over time with fitted line.
- Keep smoothing moderate to avoid distortion.
