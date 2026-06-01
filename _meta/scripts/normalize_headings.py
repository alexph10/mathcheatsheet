"""One-shot: rewrite every markdown heading (# .. ######) as #### across the repo.

Touches *.md (respecting fenced code blocks) and markdown cells inside *.ipynb.
Leaves code cells, frontmatter YAML, and code-fenced content untouched.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEADING_RE = re.compile(r"^(#{1,6})(\s+)")
FENCE_RE = re.compile(r"^```")


def rewrite_md_text(text: str) -> str:
    out, in_fence = [], False
    for line in text.splitlines(keepends=True):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        out.append(HEADING_RE.sub(r"#### \2".replace("\\2", ""), line) if False else HEADING_RE.sub(lambda m: "#### ", line, count=1) if HEADING_RE.match(line) else line)
    return "".join(out)


def rewrite_md_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    new = rewrite_md_text(original)
    if new != original:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def rewrite_ipynb_file(path: Path) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", "")
        if isinstance(src, list):
            joined = "".join(src)
            new = rewrite_md_text(joined)
            if new != joined:
                cell["source"] = new.splitlines(keepends=True)
                changed = True
        else:
            new = rewrite_md_text(src)
            if new != src:
                cell["source"] = new
                changed = True
    if changed:
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    md_changed = nb_changed = 0
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts:
            continue
        if rewrite_md_file(p):
            md_changed += 1
    for p in ROOT.rglob("*.ipynb"):
        if ".git" in p.parts or ".ipynb_checkpoints" in p.parts:
            continue
        if rewrite_ipynb_file(p):
            nb_changed += 1
    print(f"Rewrote headings in {md_changed} .md files and {nb_changed} .ipynb files.")


if __name__ == "__main__":
    main()
