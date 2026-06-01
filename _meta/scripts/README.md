# Scripts

| Script | Purpose |
| ------ | ------- |
| `validate.py`    | Lints frontmatter, checks ids/domains, verifies prerequisite + link targets. Run before committing. |
| `build_index.py` | Rewrites the README status table and emits per-folder `_index.md` tables of contents. |

Both scripts are pure stdlib + `pyyaml`. No notebook execution required.
