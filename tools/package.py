"""Zip the skill-library for upload to claude.ai: uv run python -I tools/package.py

dist/skill-library.zip         a bare skill (for a "Upload skill" button)
dist/skill-library-plugin.zip  the same skill wrapped as a plugin (for "Upload plugin")
"""
import json, os, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(REPO, "skills", "skill-library")
dist = os.path.join(REPO, "dist")
os.makedirs(dist, exist_ok=True)

manifest = {
    "name": "skill-library",
    "version": "1.0.0",
    "description": "Picks the best skills for any project from a curated on-demand library of 350 skills (frontend, backend, mobile, databases, DevOps, security, reverse engineering, games, AI agents, marketing, business, research).",
    "author": {"name": "n3k4a"},
}


def add_tree(z, prefix):
    for dp, _, files in os.walk(src):
        for f in files:
            full = os.path.join(dp, f)
            # forward slashes so the archive opens the same everywhere
            z.write(full, prefix + os.path.relpath(full, src).replace(os.sep, "/"))


def write(name, build):
    out = os.path.join(dist, name)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        build(z)
    print(f"{out}: {os.path.getsize(out) / 1e6:.1f} MB")


write("skill-library.zip", lambda z: add_tree(z, "skill-library/"))


def plugin(z):
    z.writestr(".claude-plugin/plugin.json", json.dumps(manifest, indent=2))
    z.writestr("README.md", "# skill-library\n\nOne skill that picks the right skills for any project. It reads the project's stack and the task's goal, maps each phase (plan, build, test, secure, launch) to a category, scores the candidates, and loads the best one to three skills from a curated on-demand library of 350 skills. Third-party skills keep their own MIT or Apache-2.0 licenses, listed in `skills/skill-library/library/LICENSES/`.\n")
    add_tree(z, "skills/skill-library/")


write("skill-library-plugin.zip", plugin)


def web_plugin(z):
    # no library/ folder, so the skill reads the latest library from GitHub
    z.writestr(".claude-plugin/plugin.json", json.dumps(manifest, indent=2))
    z.write(os.path.join(src, "SKILL.md"), "skills/skill-library/SKILL.md")


write("skill-library-web.zip", web_plugin)
