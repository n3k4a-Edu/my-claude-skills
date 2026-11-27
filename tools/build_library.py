"""Build the skill library from curation.json.

Usage: uv run python -I tools/build_library.py [--sources DIR]
Reads skills from the repo's custom/ folder and from cloned upstream repos in
--sources (default ~/.claude/skill-sources), then writes:
  skills/<core-skill>/            real skills Claude Code loads directly
  skills/skill-library/library/   everything else, read on demand by the loader
"""
import argparse, glob, json, os, re, shutil, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__", ".tessl-plugin", ".venv"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4"}
DESC_MAX = 220


def frontmatter(text):
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    name = re.search(r"^name:\s*['\"]?(.+?)['\"]?\s*$", fm, re.M)
    desc = re.search(r"^description:\s*(.+?)(?=^\w[\w-]*:|\Z)", fm, re.M | re.S)
    d = re.sub(r"\s+", " ", desc.group(1)).strip().strip("\"'|> ") if desc else ""
    return (name.group(1).strip() if name else None), d


def short(d):
    return d if len(d) <= DESC_MAX else d[: DESC_MAX - 1].rsplit(" ", 1)[0] + "…"


def resolve(src_cfg, sources_dir, folder):
    base = REPO if src_cfg["root"] == "custom" else sources_dir
    if src_cfg.get("single"):
        return os.path.join(base, src_cfg["root"])
    hits = glob.glob(os.path.join(base, src_cfg["root"], folder))
    if len(hits) != 1:
        sys.exit(f"cannot resolve {src_cfg['root']}/{folder}: {hits}")
    return hits[0]


def copy_skill(src, dst, main_name):
    skill_text = open(os.path.join(src, "SKILL.md"), encoding="utf-8", errors="replace").read()
    for dp, dn, fn in os.walk(src):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        rel = os.path.relpath(dp, src)
        for f in fn:
            ext = os.path.splitext(f)[1].lower()
            # README screenshots at the skill root are not part of the instructions
            if rel == "." and ext in IMAGE_EXT and f not in skill_text:
                continue
            out_name = main_name if (rel == "." and f == "SKILL.md") else f
            os.makedirs(os.path.join(dst, rel), exist_ok=True)
            shutil.copy2(os.path.join(dp, f), os.path.join(dst, rel, out_name))


def matches(pattern, sid):
    return pattern == sid or (pattern.endswith("/*") and sid.startswith(pattern[:-1]))


def plugin_skills():
    path = os.path.expanduser("~/.claude/plugins/installed_plugins.json")
    if not os.path.exists(path):
        return []
    data = json.load(open(path, encoding="utf-8"))
    out = []
    for key, entries in sorted(data.get("plugins", {}).items()):
        root = entries[0]["installPath"]
        manifest = os.path.join(root, ".claude-plugin", "plugin.json")
        dirs = ["skills"]
        if os.path.exists(manifest):
            declared = json.load(open(manifest, encoding="utf-8")).get("skills")
            if declared:
                dirs = declared if isinstance(declared, list) else [declared]
        items = []
        found = []
        for d in dirs:
            found += glob.glob(os.path.join(root, d, "*", "SKILL.md"))
        for p in sorted(found):
            n, d = frontmatter(open(p, encoding="utf-8", errors="replace").read())
            items.append((n or os.path.basename(os.path.dirname(p)), short(d)))
        if items:
            out.append((key, items))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default=os.path.expanduser("~/.claude/skill-sources"))
    args = ap.parse_args()
    cur = json.load(open(os.path.join(REPO, "tools", "curation.json"), encoding="utf-8"))
    skills_dir = os.path.join(REPO, "skills")
    lib = os.path.join(skills_dir, "skill-library", "library")

    shutil.rmtree(lib, ignore_errors=True)
    for d in glob.glob(os.path.join(skills_dir, "*")):
        if os.path.basename(d) != "skill-library":
            shutil.rmtree(d)
    os.makedirs(os.path.join(lib, "skills"))

    plugins = plugin_skills()
    plugin_cat = {p: c for c, ps in cur.get("plugin_categories", {}).items() for p in ps}
    seen, cats = {}, []
    for cat_id, cat in cur["categories"].items():
        rows = []
        for sid in cat["skills"]:
            src_name, folder = sid.split("/", 1)
            src = resolve(cur["sources"][src_name], args.sources, folder)
            name, desc = frontmatter(open(os.path.join(src, "SKILL.md"), encoding="utf-8", errors="replace").read())
            name = name or folder
            if name in seen:
                sys.exit(f"duplicate skill name {name}: {seen[name]} and {sid}")
            seen[name] = sid
            copy_skill(src, os.path.join(lib, "skills", name), "INSTRUCTIONS.md")
            if any(matches(p, sid) for p in cur["core"]):
                copy_skill(src, os.path.join(skills_dir, name), "SKILL.md")
            needs = next((v for k, v in cur["requires"].items() if matches(k, sid)), None)
            code_only = any(matches(p, sid) for p in cur["code_only"])
            rows.append((name, short(desc), needs, code_only, src_name))
        cats.append((cat_id, cat["title"], rows))
        with open(os.path.join(lib, f"{cat_id}.md"), "w", encoding="utf-8") as f:
            f.write(f"# {cat['title']}\n\nOpen a skill with `skills/<name>/INSTRUCTIONS.md` (relative to this folder).\n\n")
            for name, desc, needs, code_only, src_name in rows:
                tags = []
                if needs:
                    tags.append(f"needs: {needs}")
                if code_only:
                    tags.append("Claude Code only")
                tag = f" _({'; '.join(tags)})_" if tags else ""
                f.write(f"- **{name}** — {desc}{tag}\n")
            extra = [(k, items) for k, items in plugins if plugin_cat.get(k.split("@")[0]) == cat_id]
            if extra:
                f.write("\n## Plugin skills (Claude Code: invoke with the Skill tool when it lists them)\n\n")
                for key, items in extra:
                    for n, d in items:
                        f.write(f"- **{key.split('@')[0]}:{n}** — {d}\n")
            acct = cur.get("account_skills", {}).get(cat_id, [])
            if acct:
                f.write("\n## Account skills (available wherever the user is signed in)\n\n")
                for n, d in acct:
                    f.write(f"- **{n}** — {d}\n")

    with open(os.path.join(lib, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("# Skill library index\n\nPick the categories that fit the task, then read only those files.\n\n")
        f.write("| Category file | What it covers | Skills |\n|---|---|---|\n")
        for cat_id, title, rows in cats:
            f.write(f"| `{cat_id}.md` | {title} | {len(rows)} |\n")
        f.write("\nEach category file lists library skills first, then the matching plugin and account skills. `plugins.md` has the few plugin skills that fit no category.\n")

    with open(os.path.join(lib, "plugins.md"), "w", encoding="utf-8") as f:
        f.write("# Other plugin skills\n\nPlugin skills not filed under a category. Invoke with the Skill tool as `<plugin>:<skill>` when the plugin is installed.\n\n")
        for key, items in plugins:
            if key.split("@")[0] in plugin_cat:
                continue
            f.write(f"## {key}\n")
            for n, d in items:
                f.write(f"- **{key.split('@')[0]}:{n}** — {d}\n")
            f.write("\n")

    lic_dir = os.path.join(lib, "LICENSES")
    os.makedirs(lic_dir)
    for src_name, cfg in cur["sources"].items():
        if cfg.get("license"):
            shutil.copy2(os.path.join(args.sources, cfg["license"]), os.path.join(lic_dir, f"{src_name}.txt"))
    with open(os.path.join(lic_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("Third-party skills keep their original licenses (MIT or Apache-2.0):\n\n")
        for src_name, cfg in cur["sources"].items():
            if cfg.get("upstream"):
                f.write(f"- {src_name}: {cfg['upstream']} — `{src_name}.txt`\n")

    total = sum(len(r) for _, _, r in cats)
    print(f"library: {total} skills in {len(cats)} categories; core skills: {len(os.listdir(skills_dir)) - 1}")


if __name__ == "__main__":
    main()
