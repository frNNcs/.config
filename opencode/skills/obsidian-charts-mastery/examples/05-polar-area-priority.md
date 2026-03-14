# Example 05 — Polar area priorities

```chart
type: polarArea
labels:
  - Critical
  - High
  - Medium
  - Low
series:
  - title: Open items
    data:
      - 18
      - 29
      - 34
      - 12
width: 40%
labelColors: true
rMax: 40
```

Why:
- Highlight weighted categories with radial encoding.
- Cap radial max to preserve interpretability.
