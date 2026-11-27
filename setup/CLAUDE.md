# Global Instructions

These instructions apply to every project on this machine. Project-level CLAUDE.md files can override them.

## UI / Frontend Work

For **any** task that involves UI, UX, frontend code, design, visual layout, components, pages, styling, or user-facing interfaces, invoke the design skill that **best fits the type of site or task** before writing or proposing code. Do not ask for confirmation; just use it.

This applies whenever the request involves any of:
- Building or modifying pages, components, layouts, or screens
- Styling, theming, colors, typography, spacing
- Forms, buttons, modals, cards, hero sections, navigation
- Landing pages, dashboards, admin panels, marketing sites
- WordPress themes, block templates, Gutenberg blocks
- React/Vue/Svelte components and their CSS
- Any HTML/CSS/Tailwind/shadcn work

### How to pick the skill

1. Look at the skills available in the current session (new ones get installed over time) and pick the one whose description matches the site/task most specifically. A specialised skill beats a general one.
2. Use the table below as the default when those skills are installed. If a newly installed skill fits the task better than the table's choice, use the new one.
3. Combining is fine: a platform skill (e.g. WordPress) plus a design skill for the visual decisions.
4. Say in one line which skill you picked and why.

| Site / task type | Default skill |
|---|---|
| WordPress site, theme, Gutenberg blocks | `build-with-wordpress` + `ui-ux-pro-max` for design decisions |
| Landing page, portfolio, marketing site, redesign | `design-taste-frontend` |
| Dashboard, admin panel, web app UI (React / shadcn / Tailwind) | `ui-ux-pro-max` + `ui-ux-pro-max:ui-styling` |
| Design system, design tokens | `ui-ux-pro-max:design-system` |
| Brand identity, logo | `ui-ux-pro-max:brand` / `ui-ux-pro-max:design` |
| Banners, social ads, hero visuals | `ui-ux-pro-max:banner-design` |
| Presentations / slides | `ui-ux-pro-max:slides` |
| Polish, audit or critique an existing UI | `impeccable` |
| Exploring and comparing several design variants | `superdesign` |
| Cinematic/motion-rich hero sections and landing pages | `motionsites-web-builder` |
| Anything not covered above | `ui-ux-pro-max`, else `frontend-design` |

## Skill Library (picks the skills for every project)

Beyond the skills loaded in the session, ~270 curated skills live in the **`skill-library`** skill and load only when needed. For any project or task that is more than a one-line change, and again whenever the work moves to a new phase (plan → build → test → secure → launch), invoke `skill-library` and follow its recipe. It reads the project's stack, maps each phase to skills, and loads the best ones. The tables below say who leads each job; the library fills everything they do not cover (framework patterns, databases, mobile, DevOps, marketing detail, and more).

## Security & Code Quality

Before shipping ANY project, invoke the most relevant security skill:
- Web app / API security testing → `security-audit`; with the Strix CLI installed, `penetration-testing-with-strix` (library)
- Code vulnerability scanning → trailofbits `static-analysis`; with Strix, `find-security-vulnerabilities-in-code` (library)
- Framework-specific hardening → the library's `laravel-security`, `django-security`, `rails-security`, `springboot-security`…
- Supply chain / dependency risks → `supply-chain-risk-auditor`
- OWASP Top 10 → `security-audit`; with Strix, `owasp-top-10-testing` (library)
- General code review → `second-opinion` or `code-review`

For CI/CD pipelines, suggest adding `ci-security-scanning-with-strix` (library).

## Engineering Workflows

| Task | Skill |
|---|---|
| Planning a new project or feature | `superpowers:brainstorming`, then `plan-critic` to stress-test the plan |
| Test-driven development | `superpowers:test-driven-development` |
| Bug diagnosis | `superpowers:systematic-debugging` |
| Prototyping, deep-module design, domain modeling | library: `prototype`, `codebase-design`, `domain-modeling` |
| Writing less code, reviewing a change for necessity | library: `ponytail`, `ponytail-review` |

## Business & Strategy

For business questions, invoke the matching skill without asking:

| Topic | Skill |
|---|---|
| Business strategy, company operations, executive decisions | `ceo-advisor` |
| Marketing plans, SEO, campaigns, growth, funnels | `marketing-strategist` for the overall plan; the library's marketing skills for each specific job (`seo-audit`, `copywriting`, `cro`, `launch`, `pricing`, `cold-email`…) |
| Reviewing any plan, proposal, roadmap, or architecture | `plan-critic` |
| IT infrastructure, servers, networking, DevOps, cloud | `it-infrastructure` |

## Creative & Research

| Topic | Skill |
|---|---|
| Blender, 3D modeling, game assets, animation | `blender-3d` |
| Game modding, memory analysis, Cheat Engine, game internals | `game-research` |
| Binary analysis, malware research, CTF, firmware, decompilation | `advanced-re` (+ `reverse-engineer-anything` for the REA workflow) |
| Reverse engineering with IDA Pro | Use IDA MCP tools directly |

## General Rules

- **Skill selection**: Always pick the MOST SPECIFIC skill for the task. A specialized skill beats a general one. Check all installed skills' descriptions before defaulting to a general approach.
- **Combining skills**: Use multiple skills when the task spans domains (e.g. `build-with-wordpress` + `ui-ux-pro-max` + `security-audit`).
- **Speed**: Execute immediately after selecting the skill. No unnecessary confirmation rounds. If the skill gives clear instructions, follow them.
- **New skills**: When a newly installed skill covers the task better than these tables, use it. These tables are defaults, not restrictions.

## Skill Auto-Use Policy

Skills configured for auto-use should fire **without asking** the user for permission. The user has already pre-approved them by installing them at the user level.
