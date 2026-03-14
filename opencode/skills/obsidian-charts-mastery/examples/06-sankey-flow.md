# Example 06 — Sankey flow

```chart
type: sankey
labels:
  - Backlog
  - In Progress
  - Review
  - Done
series:
  - title: Workflow
    data:
      - [Backlog, 24, In Progress]
      - [In Progress, 19, Review]
      - [Review, 16, Done]
      - [Backlog, 5, Done]
    priority:
      Backlog: 1
      In Progress: 2
      Review: 3
      Done: 4
    colorFrom:
      Backlog: "#EF4444"
      In Progress: "#F59E0B"
      Review: "#3B82F6"
      Done: "#22C55E"
    colorTo:
      Backlog: "#EF4444"
      In Progress: "#F59E0B"
      Review: "#3B82F6"
      Done: "#22C55E"
legend: false
```

Why:
- Encode weighted transitions between workflow stages.
- Keep node naming consistent across edges and color maps.
