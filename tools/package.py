"""Zip the skill-library skill for upload to claude.ai: uv run python -I tools/package.py"""
import os, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(REPO, "skills", "skill-library")
out = os.path.join(REPO, "dist", "skill-library.zip")
os.makedirs(os.path.dirname(out), exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for dp, _, files in os.walk(src):
        for f in files:
            full = os.path.join(dp, f)
            # forward slashes so the archive opens the same everywhere
            z.write(full, "skill-library/" + os.path.relpath(full, src).replace(os.sep, "/"))
print(f"{out}: {os.path.getsize(out) / 1e6:.1f} MB")
