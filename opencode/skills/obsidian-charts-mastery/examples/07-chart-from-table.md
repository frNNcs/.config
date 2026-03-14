# Example 07 — Chart from markdown table

Source table:

```md
| Month | MRR | Churn |
| ----- | --- | ----- |
| Jan   | 100 | 5     |
| Feb   | 108 | 6     |
| Mar   | 115 | 4     |
^mrr-table
```

Linked chart:

```chart
type: line
id: mrr-table
layout: rows
time: month
legend: true
legendPosition: bottom
```

Why:
- Keep table as editable source-of-truth.
- Derive chart without duplicating numbers.
