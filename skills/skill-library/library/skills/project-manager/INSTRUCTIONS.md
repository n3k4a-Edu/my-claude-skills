---
name: project-manager
description: "Project management, Agile, Scrum, sprint planning, and team coordination. Use when the user asks about project planning, sprint management, Kanban, task breakdown, estimations, standups, retrospectives, project timelines, resource allocation, risk management for projects, or any project delivery question."
metadata:
  version: "1.0.0"
---

# Project Manager

Practical project management. No ceremony for ceremony's sake.

## Sprint Planning

### User Story Format
```
As a [role], I want [capability] so that [benefit].

Acceptance Criteria:
- Given [context], when [action], then [result]
- ...

Definition of Done:
- Code reviewed and merged
- Tests passing (unit + integration)
- Documentation updated
- Deployed to staging and verified
```

### Estimation (Story Points)
| Points | Meaning | Example |
|---|---|---|
| 1 | Trivial, < 2 hours | Copy change, config update |
| 2 | Small, half day | Simple bug fix, add a field |
| 3 | Medium, 1-2 days | New API endpoint, component |
| 5 | Large, 3-5 days | Feature with multiple parts |
| 8 | Very large, 1-2 weeks | Complex feature, refactor |
| 13 | Epic-sized, break it down | Too big for one sprint |

If it's 13+, decompose it. If the team disagrees by >2x, discuss — someone sees complexity others don't.

### Sprint Cadence (2-week default)
- **Day 1**: Sprint planning (2h max). Pick from prioritized backlog. Commit to sprint goal.
- **Daily**: Standup (15 min). What did I do? What will I do? Any blockers?
- **Day 9**: Code freeze. Only bug fixes after this.
- **Day 10**: Sprint review (demo to stakeholders) + retrospective.

### Velocity Tracking
- Track points completed per sprint (last 3-5 sprints)
- Plan at 70-80% of average velocity (leave buffer)
- If velocity drops 2 sprints in a row: investigate (scope creep? technical debt? team issues?)

## Task Breakdown

For any feature, decompose into:
1. **Research/Spike** (if needed): Time-boxed learning. Output is a decision, not code.
2. **Backend**: Data model → API → business logic → tests
3. **Frontend**: Component → integration → UI tests
4. **Infrastructure**: Deploy config, monitoring, alerts
5. **Documentation**: API docs, user docs, runbook

Each task should be completable in 1-2 days. If not, break it smaller.

## Risk Management

For every project, maintain a risk register:

| Risk | Probability | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Key person leaves | M | H | Document everything, cross-train | Tech Lead |
| Third-party API changes | L | H | Abstract behind interface, pin versions | Backend Lead |
| Scope creep | H | H | Written requirements, change request process | PM |

Review weekly. Update as risks materialize or new ones appear.

## Meeting Templates

### Standup (async or 15 min sync)
```
✅ Yesterday: [completed items]
🔄 Today: [planned items]
🚫 Blocked: [blockers + who can unblock]
```

### Retrospective
```
😊 What went well? (keep doing)
😤 What didn't go well? (stop doing)
💡 What should we try? (start doing)
→ Pick top 2 action items with owners
```

### Project Status Update
```
🎯 Goal: [sprint/project goal]
📊 Progress: [X/Y stories done, Z% complete]
🟢 On track / 🟡 At risk / 🔴 Blocked
⚠️ Risks: [top 2-3]
📅 Next milestone: [date + deliverable]
🙋 Needs: [decisions or resources needed]
```

## Common Anti-Patterns to Flag

- Sprint scope changes mid-sprint without trade-offs
- No definition of done → "done" means different things
- Skipping retrospectives → same mistakes repeat
- Estimates treated as commitments → padding and stress
- Too many meetings → no time for actual work
- No single owner per task → diffused responsibility
