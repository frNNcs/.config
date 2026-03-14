# Example 08 — DataviewJS integration

```dataviewjs
const notes = dv.pages('#project').where(p => p.status);

const grouped = notes
  .groupBy(p => p.status)
  .map(g => ({ label: g.key, count: g.rows.length }))
  .array();

const chartData = {
  type: 'doughnut',
  data: {
    labels: grouped.map(x => x.label),
    datasets: [{
      label: 'Items by status',
      data: grouped.map(x => x.count)
    }]
  },
  options: {
    plugins: {
      legend: { position: 'right' }
    }
  }
};

window.renderChart(chartData, this.container);
```

Why:
- Build dynamic charts from vault metadata.
- Avoid manual updates when note set changes.
