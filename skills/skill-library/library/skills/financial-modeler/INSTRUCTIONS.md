---
name: financial-modeler
description: "Financial modeling, projections, unit economics, P&L, cash flow, fundraising, valuation, and budgeting. Use when the user asks about financial projections, revenue models, pricing strategy, unit economics, burn rate, runway, cap tables, fundraising, ROI analysis, budget planning, or any financial analysis question for startups and businesses."
metadata:
  version: "1.0.0"
---

# Financial Modeler

Numbers tell the story. Build models that are useful, not just impressive.

## Unit Economics

### SaaS
| Metric | Formula | Healthy benchmark |
|---|---|---|
| MRR | Sum of monthly recurring revenue | Growing >10% m/m early stage |
| ARR | MRR × 12 | Use for annual contracts |
| CAC | Total sales+marketing spend / New customers | - |
| LTV | ARPU × Gross Margin × (1 / Churn Rate) | LTV/CAC > 3 |
| LTV/CAC | LTV / CAC | > 3x |
| Payback | CAC / (ARPU × Gross Margin) | < 12 months |
| Churn | Lost customers / Total customers per month | < 5% monthly |
| NRR | (Start MRR + Expansion - Contraction - Churn) / Start MRR | > 110% |
| Gross Margin | (Revenue - COGS) / Revenue | > 70% for SaaS |

### E-commerce
| Metric | Formula |
|---|---|
| AOV | Total revenue / Number of orders |
| CAC | Marketing spend / New customers |
| Repeat rate | Returning customers / Total customers |
| COGS | Product cost + shipping + packaging + returns |
| Contribution margin | Revenue - COGS - Variable costs per order |

### Marketplace
| Metric | Formula |
|---|---|
| GMV | Total transaction volume on platform |
| Take rate | Platform revenue / GMV |
| Liquidity | % of listings that result in transactions |

## Revenue Projection (Bottom-Up)

```
Month 1:
  Existing customers: 100
  New customers: 20 (from X leads × Y% conversion)
  Churned: 5 (5% churn)
  End customers: 115
  Revenue: 115 × $50 ARPU = $5,750

Month 2:
  Existing: 115
  New: 25 (marketing spend increase)
  Churned: 6
  End: 134
  Revenue: 134 × $50 = $6,700
```

Build 3 scenarios: **Conservative** (50% of optimistic), **Base** (realistic), **Optimistic** (everything works).

## P&L Structure

```
Revenue
  - COGS (hosting, payment processing, direct costs)
= Gross Profit (target: >70% for SaaS, >40% for e-commerce)
  - Operating Expenses
    - Engineering (salaries, tools, infrastructure)
    - Sales & Marketing (ads, events, sales team)
    - General & Admin (rent, legal, accounting, insurance)
= EBITDA
  - Depreciation & Amortization
= Operating Income
  - Interest, Taxes
= Net Income
```

## Cash Flow Basics

```
Cash at start of month
  + Cash received (revenue collected, not just invoiced)
  - Cash paid out (salaries, rent, vendors, taxes)
  = Cash at end of month

Burn rate = Monthly cash decrease (when losing money)
Runway = Cash / Monthly burn rate = months until zero
```

**Rule**: Always maintain 6+ months runway. Start fundraising at 9-12 months.

## Fundraising Math

### Valuation Methods (Early Stage)
- **Pre-revenue**: Comparable deals, team quality, market size
- **Revenue multiple**: ARR × industry multiple (5-15x for SaaS)
- **DCF**: Discounted cash flows (more useful post-Series A)

### Round Structure
```
Pre-money valuation: $10M
Investment: $2M
Post-money valuation: $12M
Investor ownership: $2M / $12M = 16.7%
Founder dilution: from 100% to 83.3%
```

### Cap Table Example
| Shareholder | Pre-Round | Shares | Post-Round |
|---|---|---|---|
| Founders | 80% | 800K | 66.7% |
| Seed investors | 20% | 200K | 16.7% |
| Series A | 0% | 200K | 16.7% |
| **Total** | 100% | 1.2M | 100% |

## Budget Template (Monthly)

| Category | Budget | Actual | Variance |
|---|---|---|---|
| **Revenue** | $X | $Y | +/- Z% |
| Engineering | | | |
| - Salaries | | | |
| - Tools/SaaS | | | |
| - Infrastructure | | | |
| Marketing | | | |
| - Paid ads | | | |
| - Content/SEO | | | |
| - Events | | | |
| Sales | | | |
| G&A | | | |
| **Total Expenses** | | | |
| **Net** | | | |

Review monthly. Investigate any line >10% over budget.

## Pricing Strategy

### Cost-Plus
Price = Cost × (1 + Margin%). Simple but ignores value.

### Value-Based (preferred)
1. What's the customer's alternative? (competitor price, manual cost)
2. What value does your product create? (time saved × hourly rate, revenue generated)
3. Price at 10-30% of value created

### Pricing Tiers (SaaS)
- **Free/Freemium**: Acquisition tool. Limited features. Convert 2-5% to paid.
- **Starter**: $X/mo. Core features. Individual users.
- **Pro**: $3-5X/mo. Full features. Teams. This is where most revenue comes from.
- **Enterprise**: Custom pricing. SLA, SSO, audit logs, dedicated support.

## Red Flags in Financial Models

- Hockey stick projections with no explanation of what drives the inflection
- CAC not increasing as market saturates
- Zero churn assumption
- Revenue growing but no corresponding cost increases
- No sensitivity analysis (what if growth is 50% lower?)
- Mixing up revenue and cash collection
- Forgetting one-time costs (legal, equipment, setup fees)
