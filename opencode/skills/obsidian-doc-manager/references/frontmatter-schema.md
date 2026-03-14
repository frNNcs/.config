# Frontmatter Schema

All main documentation files must include YAML frontmatter at the top of the file.

```yaml
---
created: YYYY-MM-DDThh:mm
updated: YYYY-MM-DDThh:mm
status: in-progress | todo | done | blocked
---
```

## Allowed Statuses
- `todo`: Pending tasks or unstarted projects.
- `in-progress`: Active efforts.
- `done`: Completed items.
- `blocked`: Tasks waiting on external dependencies.

## Standard Tags
Use these tags to categorize tasks and notes:
- `#homelab`: All homelab-related tasks.
- `#todo`: Marks pending tasks.
- `#docker`: Docker/Swarm tasks.
- `#ansible`: Ansible-specific tasks.
- `#twingate`: Twingate-specific tasks.
- `#monitoring`: Integration with Prometheus/Grafana.