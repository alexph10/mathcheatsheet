"""Validate frontmatter and cross-links across all cheat sheets.

Checks:
  1. Every .md (except TEMPLATE / top-level docs) has YAML frontmatter.
  2. Required frontmatter fields are present and well-typed.
  3. `id` is globally unique and matches filename stem.
  4. `domain` matches the file's folder path.
  5. Every id in `prerequisites` / `used_by` resolves to an existing sheet.
  6. `notebook:` field, if present, points to a real .ipynb next to the .md.
  7. Relative .md links in the body resolve.

Exits non-zero on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TOP_LEVEL_DOCS = {"readme.md", "template.md", "taxonomy.md", "contributing.md"}
REQUIRED_FIELDS = {"id", "title", "domain", "difficulty", "status"}
VALID_STATUS = {"draft", "reviewed", "stable"}
VALID_DIFFICULTY = {1, 2, 3}

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]*)?\)")


def iter_sheets() -> list[Path]:
    sheets = []
    for p in ROOT.rglob("*.md"):
        if any(part.startswith("_") or part.startswith(".") for part in p.relative_to(ROOT).parts):
            continue
        if p.name in TOP_LEVEL_DOCS and p.parent == ROOT:
            continue
        sheets.append(p)
    return sheets


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return yaml.safe_load(m.group(1)) or {}


def main() -> int:
    sheets = iter_sheets()
    errors: list[str] = []
    by_id: dict[str, Path] = {}

    # Pass 1: parse + per-sheet checks
    parsed: dict[Path, dict] = {}
    for sheet in sheets:
        fm = parse_frontmatter(sheet)
        if fm is None:
            errors.append(f"{sheet}: missing YAML frontmatter")
            continue
        parsed[sheet] = fm

        missing = REQUIRED_FIELDS - fm.keys()
        if missing:
            errors.append(f"{sheet}: missing required fields {sorted(missing)}")

        sid = fm.get("id")
        if sid and sid != sheet.stem:
            errors.append(f"{sheet}: id '{sid}' does not match filename stem '{sheet.stem}'")
        if sid:
            if sid in by_id:
                errors.append(f"{sheet}: duplicate id '{sid}' (also in {by_id[sid]})")
            else:
                by_id[sid] = sheet

        domain = fm.get("domain")
        expected_domain = sheet.parent.relative_to(ROOT).as_posix()
        if domain and domain != expected_domain:
            errors.append(f"{sheet}: domain '{domain}' != folder path '{expected_domain}'")

        if fm.get("difficulty") not in VALID_DIFFICULTY:
            errors.append(f"{sheet}: difficulty must be one of {sorted(VALID_DIFFICULTY)}")
        if fm.get("status") not in VALID_STATUS:
            errors.append(f"{sheet}: status must be one of {sorted(VALID_STATUS)}")

        nb = fm.get("notebook")
        if nb and not (sheet.parent / nb).exists():
            errors.append(f"{sheet}: notebook '{nb}' does not exist")

    # Pass 2: cross-reference checks
    for sheet, fm in parsed.items():
        for field in ("prerequisites", "used_by"):
            for ref in fm.get(field, []) or []:
                if ref not in by_id:
                    errors.append(f"{sheet}: {field} references unknown id '{ref}'")

        text = sheet.read_text(encoding="utf-8")
        body = text[text.find("---", 3) + 3 :] if text.startswith("---") else text
        for link in MD_LINK_RE.findall(body):
            if link.startswith("http"):
                continue
            target = (sheet.parent / link).resolve()
            if not target.exists():
                errors.append(f"{sheet}: broken link -> {link}")

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(sheets)} sheets validated, {len(by_id)} unique ids.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
