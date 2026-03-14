---
name: obsidian-doc-manager
description: This skill should be used when the user asks to "create a new note", "update kanban tasks", "organize the vault", "fix frontmatter", "manage documentation", or mentions PARA structure, Obsidian tags, or task management workflows in the obsidian-personal repository.
version: 0.1.0
---

# Obsidian Document Manager

This skill provides workflows and strict standards for managing the personal Obsidian vault using the PARA methodology, Kanban task tracking, and Infrastructure-as-Code (IaC) documentation.

## Core Workflows

### 1. Creating and Managing Notes (PARA Structure)
1. Determine the correct PARA directory:
   - `000 Inbox`: Unsorted quick captures.
   - `001 Projects`: Short-term efforts with specific goals.
   - `002 Areas`: Long-term responsibilities.
   - `003 Resources`: Ongoing topics of interest.
   - `004 Archive`: Inactive items.
   - `005 Templates`: Base files for new notes.
2. Apply the standard YAML frontmatter to the top of the file.
3. Set the `created` and `updated` timestamps to the current date (YYYY-MM-DDThh:mm).
4. Assign an initial `status` (e.g., `todo`, `in-progress`, `done`, `blocked`).

### 2. Managing Kanban Tasks
1. Locate the relevant Kanban note (e.g., `YYYY-MM-DD project kanban.md`). **Never** put TODO lists in `README.md`.
2. Use the standard task format: `- [ ] Description #tag1 #tag2 #todo 📅 YYYY-MM-DD`
3. Move tasks progressively between `## todo`, `## doing`, and `## done` headers.
4. Ensure all subtasks are indented with exactly **2 spaces**.
5. Mark completed subtasks with `[x]` and `✅ YYYY-MM-DD`.
6. Never leave subtasks orphaned without a parent task.
7. When a main task is completed, update the main note's `updated` and `status` fields in the frontmatter.

### 3. Diagram Standards (Excalidraw/Mermaid)
1. Use a single object with internal text (avoid separate shape + text).
2. Ensure arrows are explicitly **bound/connected** to nodes, not just visually positioned.

### 4. Git & Documentation Integrity
1. Use Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).
2. Update `CHANGELOG` in `README.md` only for significant project-level changes.
3. Ensure no duplicate tasks exist between Kanban and documentation.

## Additional Resources

### Reference Files
For detailed structural rules and schemas, consult:
- **`references/frontmatter-schema.md`** - Complete list of allowed YAML fields, statuses, and standard tags.

### Example Files
Working templates available in `examples/`:
- **`examples/kanban-template.md`** - Standard format for task tracking.
- **`examples/standard-note.md`** - Boilerplate for standard documentation.