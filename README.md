# my-claude-skills

My Claude setup in one repo: my own skills, a curated library of 270 skills that loads on demand, global CLAUDE.md routing, a project-detection hook, and the list of plugins to install.

## New machine

1. Install Claude Code and Git, and sign in to GitHub (`gh auth login`).
2. Clone and run setup:

   Windows:
   ```powershell
   git clone https://github.com/n3k4a-Edu/my-claude-skills.git $HOME\my-claude-skills
   powershell -ExecutionPolicy Bypass -File $HOME\my-claude-skills\setup\setup.ps1
   ```
   macOS / Linux:
   ```bash
   git clone https://github.com/n3k4a-Edu/my-claude-skills.git ~/my-claude-skills && bash ~/my-claude-skills/setup/setup.sh
   ```
3. Restart Claude. Re-authorize MCP servers that need a sign-in with `/mcp`, and install any desktop tools you use there (IDA, Cheat Engine, Blender, Strix CLI).

## Staying up to date

- On any machine: `setup\update.ps1` (or `git pull` + `bash setup/setup.sh --skip-plugins`).
- To pull new versions of the upstream skill repos and rebuild the library: `tools\refresh-upstream.ps1`, review the diff, commit, push.
- To add or drop a library skill: edit `tools/curation.json`, run `uv run python -I tools/build_library.py`, commit.

## claude.ai (web and mobile)

Upload `dist/skill-library.zip` (built by `uv run python -I tools/package.py`) in Settings → Capabilities → Skills. It carries the whole library, so it works without network access. Skills tagged "Claude Code only" need a shell and will not run there.

## Layout

| Path | What |
|---|---|
| `custom/` | Source of my own skills |
| `skills/` | What gets linked into `~/.claude/skills` (built; do not edit by hand except `skill-library/SKILL.md`) |
| `skills/skill-library/library/` | The on-demand library: `INDEX.md`, one file per category, `skills/<name>/INSTRUCTIONS.md` |
| `tools/curation.json` | Which upstream skills are in, by category, with tool requirements |
| `setup/` | Setup and update scripts, global `CLAUDE.md`, hook, plugin list |

Third-party skills keep their licenses (MIT / Apache-2.0): see `skills/skill-library/library/LICENSES/`.
