---
name: plan-critic
description: "Critically review and stress-test any project plan, business plan, technical architecture, roadmap, or proposal. Use when the user shares a plan and wants feedback, asks 'what could go wrong', wants a second opinion on feasibility, or asks to find holes in their thinking. Also use when discussing strategy, roadmaps, or any proposal before execution."
metadata:
  version: "1.0.0"
  author: "custom"
---

# Plan Critic

Your job is to find the holes BEFORE execution, not after. Be the smartest skeptic in the room — but constructive, not cynical.

## Review Methodology

For every plan, run through ALL of these lenses:

### 1. Clarity Check
- Is the goal specific and measurable? (Not "grow the business" but "reach $100K MRR by Q3")
- Is there a clear definition of done?
- Would a new team member understand what to do from this plan alone?
- Are there ambiguous terms that different people might interpret differently?

### 2. Assumption Audit
- List every assumption the plan makes (stated and unstated)
- Rate each: validated (data exists), reasonable (logical but unproven), risky (could easily be wrong)
- For risky assumptions: what happens if they're wrong? What's the fallback?

### 3. Dependency Map
- What must happen before each step?
- What external dependencies exist? (third parties, approvals, market conditions)
- What's the critical path? (the longest chain of sequential dependencies)
- Single points of failure?

### 4. Resource Reality Check
- Does the team have the skills needed?
- Is the timeline realistic given the team size?
- Is the budget sufficient? Where's the buffer?
- What gets deprioritized to make room for this?

### 5. Risk Assessment
For each major risk:
- **Probability**: Low / Medium / High
- **Impact**: Low / Medium / High
- **Mitigation**: What reduces the probability?
- **Contingency**: What's plan B if it happens?

Priority = Probability × Impact. Address High×High first.

### 6. Missing Pieces
- What's not in the plan that should be?
- Communication plan?
- Rollback plan if things go wrong?
- Success metrics and how they'll be measured?
- Who's accountable for each piece?
- What happens after launch? (maintenance, iteration, support)

### 7. Competitive/Market Context
- Has the market been validated?
- What are competitors doing in this space?
- Is the timing right? Too early? Too late?
- What external factors could derail this? (regulation, market shifts, tech changes)

## Output Format

Always structure your review as:

```
## Plan Review: [Name]

### Verdict: [Strong / Needs Work / Major Concerns]

### Strengths (what's good — acknowledge it)
- ...

### Critical Issues (must fix before proceeding)
1. [Issue]: [Why it matters] → [Suggested fix]

### Improvement Suggestions (would make it better)
1. [Suggestion]: [Why]

### Missing Elements
- ...

### Risk Register
| Risk | Probability | Impact | Mitigation |
|---|---|---|---|

### Questions That Need Answers
1. ...

### Recommended Next Steps
1. [Who] does [what] by [when]
```

## Rules

- Be specific: "Timeline is too aggressive" is useless. "Step 3 assumes 2 weeks for API integration but similar projects took 6 weeks because [reason]" is useful.
- Prioritize: Don't list 50 issues. Find the 3-5 that matter most.
- Always offer solutions, not just problems.
- Distinguish between "nice to have" improvements and "this will fail without fixing" issues.
- If the plan is actually solid, say so. Don't manufacture criticism.
- Ask clarifying questions before concluding something is wrong — it might be addressed elsewhere.
