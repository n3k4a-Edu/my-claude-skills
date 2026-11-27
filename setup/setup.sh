#!/usr/bin/env bash
# Installs this skill setup on macOS or Linux. Safe to run again.
#   bash setup/setup.sh              (full setup)
#   bash setup/setup.sh --skip-plugins
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE="$HOME/.claude"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$CLAUDE/setup-backup/$STAMP"
mkdir -p "$CLAUDE/skills"

echo "== Skills"
for dir in "$REPO"/skills/*/; do
  name="$(basename "$dir")"; target="$CLAUDE/skills/$name"
  if [ -L "$target" ] && [ "$(readlink "$target")" = "${dir%/}" ]; then continue; fi
  if [ -L "$target" ]; then rm "$target"
  elif [ -e "$target" ]; then mkdir -p "$BACKUP"; mv "$target" "$BACKUP/"; echo "  backed up $name"; fi
  ln -s "${dir%/}" "$target"; echo "  linked $name"
done

echo "== CLAUDE.md"
if [ -f "$CLAUDE/CLAUDE.md" ] && cmp -s "$REPO/setup/CLAUDE.md" "$CLAUDE/CLAUDE.md"; then echo "  already current"
else [ -f "$CLAUDE/CLAUDE.md" ] && cp "$CLAUDE/CLAUDE.md" "$CLAUDE/CLAUDE.md.bak-$STAMP"; cp "$REPO/setup/CLAUDE.md" "$CLAUDE/CLAUDE.md"; echo "  installed"; fi

echo "== Project-detection hook"
HOOK="bash \"$REPO/setup/hooks/detect-project.sh\""
python3 - "$CLAUDE/settings.json" "$HOOK" <<'PY'
import json, os, shutil, sys, time
path, cmd = sys.argv[1], sys.argv[2]
s = json.load(open(path)) if os.path.exists(path) else {}
starts = s.setdefault("hooks", {}).setdefault("SessionStart", [])
present = [h for e in starts for h in e.get("hooks", []) if "detect-project" in h.get("command", "")]
if len(present) == 1 and present[0]["command"] == cmd:
    print("  already installed")
else:
    if os.path.exists(path):
        shutil.copy(path, path + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
    if present:
        for h in present:
            h["command"] = cmd
        print("  updated to new path")
    else:
        starts.append({"hooks": [{"type": "command", "command": cmd}]})
        print("  installed")
    json.dump(s, open(path, "w"), indent=2, ensure_ascii=False)
PY

if [ "${1:-}" != "--skip-plugins" ]; then
  echo "== Plugins"
  if ! command -v claude >/dev/null; then echo "  claude CLI not found: install Claude Code, then run again."
  else
    python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));[print("M",m["source"]) for m in d["marketplaces"]];[print("P",p) for p in d["plugins"]]' "$REPO/setup/plugins.json" |
    while read -r kind value; do
      if [ "$kind" = M ]; then claude plugin marketplace add "$value" >/dev/null 2>&1 || true; echo "  marketplace $value"
      else echo "  $value: $(claude plugin install "$value" 2>&1 | tail -1)"; fi
    done
  fi
fi
echo; echo "Done. Restart Claude to load the skills."
