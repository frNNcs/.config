# Example 01 — Bar basic

```chart
type: bar
labels:
  - Sprint 1
  - Sprint 2
  - Sprint 3
series:
  - title: Completed
    data:
      - 24
      - 29
      - 32
  - title: Carryover
    data:
      - 6
      - 4
      - 3
beginAtZero: true
legend: true
legendPosition: bottom
```

Why:
- Compare category totals clearly.
- Keep baseline at zero for fair comparison.
