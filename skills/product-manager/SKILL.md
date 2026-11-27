---
name: product-manager
description: "Product management, PRDs, user stories, roadmaps, feature prioritization, and product strategy. Use when the user asks about writing PRDs, defining product requirements, feature prioritization, product roadmaps, user research insights, A/B testing, product metrics, or any product decision-making question."
metadata:
  version: "1.0.0"
---

# Product Manager

Build what matters. Ship fast. Measure everything.

## PRD Template (Product Requirements Document)

```markdown
# [Feature Name]

## Overview
One paragraph: What is it? Why now? What's the expected impact?

## Problem Statement
- Who has this problem? (specific user segment)
- What pain are they experiencing? (with data if available)
- How are they solving it today? (current workaround)

## Goals & Success Metrics
| Metric | Current | Target | Timeline |
|---|---|---|---|
| [Primary metric] | X | Y | 30 days post-launch |
| [Secondary metric] | X | Y | 90 days post-launch |

## User Stories
1. As a [role], I want [capability] so that [benefit]
   - Acceptance criteria: ...

## Scope
### In Scope
- ...
### Out of Scope (and why)
- ...
### Future Considerations
- ...

## Design
[Link to Figma/mockups]

## Technical Considerations
- Dependencies, APIs, infrastructure changes
- Performance requirements
- Security considerations

## Launch Plan
- [ ] Feature flag for gradual rollout
- [ ] Analytics events implemented
- [ ] Documentation updated
- [ ] Support team briefed

## Risks & Mitigations
| Risk | Mitigation |
|---|---|
| ... | ... |

## Timeline
| Phase | Dates | Deliverable |
|---|---|---|
| Design | Week 1-2 | Approved mockups |
| Build | Week 3-5 | Feature complete |
| QA | Week 6 | Bug-free |
| Launch | Week 7 | 10% → 50% → 100% rollout |
```

## Feature Prioritization

### RICE Scoring
| Factor | How to score |
|---|---|
| **Reach**: How many users affected per quarter? | Number of users |
| **Impact**: How much does it move the metric? | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal |
| **Confidence**: How sure are you? | 100%=high, 80%=medium, 50%=low |
| **Effort**: Person-months to build | Smaller = better |

RICE Score = (Reach × Impact × Confidence) / Effort

### ICE Scoring (simpler)
- **Impact** (1-10): How much does this move the needle?
- **Confidence** (1-10): How sure are we this will work?
- **Ease** (1-10): How easy is this to implement?

Score = Impact × Confidence × Ease

### MoSCoW for Scope
- **Must have**: Ship will fail without it
- **Should have**: Important but not critical for this release
- **Could have**: Nice if time permits
- **Won't have**: Explicitly not this release (but maybe later)

## Product Metrics

### North Star Metric
One metric that captures core value delivery:
- **Marketplace**: Transactions per week
- **SaaS**: Weekly active users or tasks completed
- **Social**: Daily active users
- **E-commerce**: Purchase frequency

### AARRR (Pirate Metrics)
| Stage | Metric | Example |
|---|---|---|
| **Acquisition** | How do users find us? | Signups, landing page conversion |
| **Activation** | Do they have a good first experience? | Completed onboarding, first action |
| **Retention** | Do they come back? | D7/D30 retention, weekly active |
| **Revenue** | Do they pay? | Conversion to paid, ARPU, MRR |
| **Referral** | Do they tell others? | NPS, referral rate, viral coefficient |

### Measuring Impact
- Define the metric BEFORE building the feature
- Set up tracking events BEFORE launch
- Run A/B test if possible (not everything needs one)
- Wait for statistical significance (usually 1-2 weeks minimum)
- Look at secondary metrics too (did we help one metric but hurt another?)

## User Research (Quick Methods)

| Method | Time | Best for |
|---|---|---|
| User interviews (5) | 1 week | Understanding motivations and pain |
| Usability test (5) | 3 days | Finding UX problems |
| Survey (100+) | 1 week | Quantifying preferences |
| Analytics deep-dive | 1 day | Understanding behavior at scale |
| Session recordings | 2 days | Seeing where users struggle |
| A/B test | 2 weeks | Validating specific changes |

5 user interviews catch ~85% of usability issues.

## Roadmap Communication

### For the team (detailed)
- Sprint-level, with specific stories and owners
- Updated weekly

### For stakeholders (strategic)
- Quarterly themes, not specific features
- "Now / Next / Later" format
- Updated monthly

### For external/customers
- High-level themes only
- No specific dates (say "Q2" not "March 15")
- Updated quarterly

## Common Product Traps

- Building what customers ask for instead of solving their actual problem
- Shipping features without measuring if they worked
- Roadmap driven by loudest voice instead of data
- Not talking to users regularly (minimum: 5 interviews/month)
- Feature factory: shipping features without retirement plan
- Ignoring technical debt until it blocks everything
