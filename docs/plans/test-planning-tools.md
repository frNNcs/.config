---
plan name: test-planning-tools
plan description: Testing OpenCode planning toolkit features
plan status: done
---

## Idea
Verify that we can create a repo-level spec, create an actionable plan, link the spec to the plan, read the plan with expanded specs, and mark the plan as complete as described in the toolkit documentation.

## Implementation
- Create a repo-level spec using createSpec
- Append the newly created spec to this plan using appendSpec
- Read this plan using readPlan to verify the spec content is expanded
- Mark this plan as complete using markPlanDone
- Verify the status change in the plan file

## Required Specs
<!-- SPECS_START -->
- opencode-standards
<!-- SPECS_END -->