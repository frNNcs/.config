# Data Sources Recipes

## 1) Inline arrays

Use for quick static insights.

```chart
type: bar
labels:
  - Backlog
  - In Progress
  - Done
series:
  - title: Tasks
    data:
      - 31
      - 12
      - 44
beginAtZero: true
```

## 2) Chart from Markdown table

### Source table

```md
| Month | Sales | Returns |
| ----- | ----- | ------- |
| Jan   | 120   | 8       |
| Feb   | 140   | 11      |
| Mar   | 132   | 9       |
^sales-table
```

### Linked chart (same note)

```chart
type: bar
id: sales-table
layout: rows
beginAtZero: true
```

### Linked chart (other note)

```chart
type: line
file: KPI Source
id: sales-table
layout: rows
time: month
```

## 3) DataviewJS with direct API rendering

```dataviewjs
const pages = dv.pages('#project').where(p => p.mark);
const labels = pages.map(p => p.file.name).array();
const marks = pages.map(p => p.mark).array();

const chartData = {
  type: 'bar',
  data: {
    labels,
    datasets: [{
      label: 'Mark',
      data: marks,
      borderWidth: 1
    }]
  },
  options: { scales: { y: { beginAtZero: true } } }
};

window.renderChart(chartData, this.container);
```

## 4) DataviewJS generating chart YAML block

```dataviewjs
const pages = dv.pages('#project').where(p => p.mark);
const labels = pages.map(p => p.file.name).array();
const marks = pages.map(p => p.mark).array();

const chart = [
  '```chart',
  'type: bar',
  'labels:',
  ...labels.map(v => `  - ${JSON.stringify(v)}`),
  'series:',
  '  - title: Mark',
  '    data:',
  ...marks.map(v => `      - ${v}`),
  'beginAtZero: true',
  '```'
].join('\n');

dv.paragraph(chart);
```

## Source strategy guidance

- Prefer inline for one-off notes.
- Prefer table-link when humans edit table first and chart second.
- Prefer DataviewJS for dashboards fed by vault metadata and query transforms.
