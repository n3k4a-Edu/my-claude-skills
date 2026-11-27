---
name: skill-library
description: Use when starting any project or task, when the work enters a new phase (planning, building, testing, securing, shipping, marketing), or when no loaded skill clearly fits. Covers frontend and UI, web frameworks, backend languages, mobile, databases, DevOps and networking, testing, security and pentesting, reverse engineering, games and 3D, AI agents and ML, marketing and SEO, business and product, video, documents, and writing. Use also when the user asks which skill fits, or names a skill that is not loaded.
---

# Skill Library

This is a library of 270 curated skills, plus an index of the plugin and account skills. Nothing loads until you pick it. Picking well matters more than picking many: one skill that names the user's exact stack and goal beats five generic ones.

Every path below starts at `library/` inside this skill's base directory. For example, a skill's instructions live at `<base>/library/skills/<name>/INSTRUCTIONS.md`.

## The recipe

### 1. Frame the task in four facts

Write these down for yourself before opening any file:

- **Goal:** the user's verb and object. For example: redesign homepage, fix conversion, edit save file, harden API.
- **Stack:** the frameworks and languages, from the request and from project signals (table below).
- **Phases:** the stages the work will pass through. For example: design → build → secure → launch.
- **Environment:** are you in Claude Code with a shell, or in a chat without one? Is a needed tool installed?

| Signal in the project folder | Stack | Category file |
|---|---|---|
| `wp-config.php`, `wp-content/`, theme `style.css` with `Theme Name:` | WordPress | `frontend-design.md` |
| `package.json` with react / next / vue / nuxt / angular / vite / svelte | JS web app | `web-frameworks.md` |
| `composer.json` with laravel, `artisan` | Laravel | `backend-languages.md` |
| `manage.py` / `pyproject.toml` / `requirements.txt` | Python (Django, FastAPI…) | `backend-languages.md` |
| `pom.xml`, `build.gradle(.kts)` | Java / Kotlin | `backend-languages.md` |
| `*.csproj`, `*.sln` | .NET | `backend-languages.md` |
| `go.mod` / `Cargo.toml` / `Gemfile` | Go / Rust / Ruby | `backend-languages.md` |
| `pubspec.yaml`, `*.xcodeproj`, `Package.swift`, `AndroidManifest.xml`, expo in `app.json` | Mobile | `mobile.md` |
| `project.godot`, `*.uproject`, Unity `Assets/` or `*_Data/Managed/`, `*.blend` | Game / 3D | `reverse-engineering-games-3d.md` |
| A target binary to analyse (`*.exe`, `*.dll`, `*.apk`, `*.so`, firmware) | Reverse engineering | `reverse-engineering-games-3d.md` |
| `Dockerfile`, `docker-compose.yml`, `*.tf`, k8s YAML, CI workflows | Infra | `devops-infra.md` |
| `prisma/`, `migrations/`, `*.sql` | Database | `data-databases.md` |

If there is no project folder, take the stack and goal from the request alone. If the folder is empty and the request does not say what is being built, ask the user one question about it.

### 2. Map each phase to a category file

| Phase or goal | Category file |
|---|---|
| Planning a new project or a big feature (always the first phase for those) | `engineering-process.md` |
| UI, design, landing page, redesign | `frontend-design.md` |
| Building with a framework | the stack's file from step 1 |
| Database work: schema, slow queries, indexes, migrations, auth with Supabase | `data-databases.md` |
| Payments (Stripe), email sending, third-party APIs, Slack apps | `backend-languages.md` |
| Architecture, debugging approach, onboarding to a codebase | `engineering-process.md` |
| Writing or fixing tests, QA, performance | `testing-quality.md` |
| Security, pentest, hardening, or anything about to go online | `security.md` |
| Marketing, SEO, ads, copy, conversion, launch, pricing | `marketing-growth.md` |
| Strategy, finance, fundraising, PRD, roadmap, research | `business-product.md` |
| AI agents, LLM features, MCP servers, ML | `ai-agents-ml.md` |
| Video, demos, watching a video | `media-video.md` |
| Documents (docx, pptx, xlsx, pdf), writing quality | `writing-thinking.md` |

Read `INDEX.md`, then open only the files this mapping points to. Each file lists library skills first, then plugin skills and account skills for the same area.

### 3. Score the candidates

For every skill in the open files that could apply, check four things:

1. **Stack fit.** Does the description name the user's exact framework or platform? `laravel-security` scores higher than `security-review` for a Laravel app.
2. **Goal fit.** Does its "use when" match the user's verb? Build, fix, audit, plan, and launch are different jobs.
3. **Depth.** A skill that specialises in the job beats a general one.
4. **Availability.** Check the tags:
   - `needs: …` means a tool, account, or MCP server must be present.
   - `Claude Code only` means it needs a shell.
   - A plugin skill needs the Skill tool to list it in this session.

List the jobs in the current phase, then pick **one skill per job**, the top scorer. Typical jobs are UI, framework, database and auth, payments, security, and marketing. Most phases have one to three jobs. A full-stack build phase can have up to five. Never load two skills for the same job. You may name one backup per job without loading it.

When a plugin is a bundle (`build-with-wordpress:*`, `ui-ux-pro-max:*`, `vercel:*`), choose the sub-skill whose description matches the job. For example: `quick-build` to build, `site-specification` to plan.

To check `needs:` when you have a shell, run a quick probe such as `where strix` (Windows) or `command -v strix` (macOS, Linux). Without a shell, treat the tool as missing.

### 4. Apply the user's own routing

The user's CLAUDE.md may name a skill for this task type, for example "WordPress → build-with-wordpress + ui-ux-pro-max".

- If the named skill is available, it leads that job. A pairing like "X + Y" counts as one job.
- If CLAUDE.md matches two rows, the row that names the platform ("WordPress") beats the generic one ("landing page").
- If a library skill names the user's exact stack for that same job and the CLAUDE.md skill is generic, load both. CLAUDE.md's skill leads, and the stack skill adds the framework details. Example: `security-audit` leads, `laravel-security` adds the Eloquent specifics.
- If the named skill is not available, use the library skill that does the same job, and continue.

### 5. Confirm by reading, then commit

Open each pick's `skills/<name>/INSTRUCTIONS.md` and read the first ~30 lines.

- If what you read does not fit the task, drop the skill and take the next-best candidate.
- If it fits, read the whole file and follow it as if that skill had been invoked directly.
- For a plugin or account skill, invoke it with the Skill tool instead. If what loads does not fit, set it aside and take the next candidate.
- When the Skill tool lists a skill that also exists in the library, use the Skill tool. That copy is the installed, current one.

Paths inside a skill, such as `references/x.md` or `scripts/y.py`, are relative to `skills/<name>/`. Open or run them only when its instructions call for them.

### 6. Handle what is missing

- **A skill asks for a context file that does not exist** (many marketing skills read a product-marketing context first). Run the skill that creates it, `product-marketing`, or ask the user for those facts, before continuing.
- **A `needs:` tool is missing.**
  - If the tool is central to the skill (Strix for the strix-* skills), take the next-best skill and tell the user in one line what installing it would add.
  - If only part of the skill uses the tool (game-research without Cheat Engine), keep the skill and do the parts that work without it.
- **A plugin skill is not listed by the Skill tool.** Pick the best library skill for that job. Tell the user which plugin would cover it better.

### 7. Announce, in one or two lines

Name the skills, why each one, and, for multi-phase work, what comes next. For example:

> Using ui-ux-pro-max + design-taste-frontend for the homepage redesign (WordPress theme), then security-audit before it goes online.

### 8. Come back at each phase change

When the work moves on (design done, now build; built, now secure; shipped, now market), repeat steps 2–7 for the new phase. Drop the skills that are no longer needed.

## Quick reference

| Situation | Do this |
|---|---|
| The user names a skill that is not loaded | Search the category files for that name, then step 5 |
| Two candidates tie | Take the one whose description names the exact stack or goal. If still tied, take the one with fewer `needs:` |
| Nothing fits well | Say so and work without one. A weak match misleads more than it helps |
| A tiny task (rename, typo, one-line answer) | Skip the library |
| Unsure which category | Open `INDEX.md` and pick by its "What it covers" column |
