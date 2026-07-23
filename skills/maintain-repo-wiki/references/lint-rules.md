# Lint Rules

`scripts/wiki_lint.py` detects structural issues that reduce wiki trustworthiness. It supports preferred field `source_files` and legacy compatibility field `related_files`.

When the wiki must support integration, runtime understanding, or troubleshooting, use `--quality`:

```bash
python3 <skill>/scripts/wiki_lint.py wiki --quality
python3 <skill>/scripts/wiki_lint.py repos/<repo-name>/wiki --quality
```

## Must-Fix Issues

- Missing `index.md`.
- Missing frontmatter on non-core pages.
- Missing `title`, `type`, or `status` in frontmatter.
- Broken relative Markdown links.
- Pages not referenced by `index.md`.
- `source_files` or `related_files` paths that do not exist.
- `source_files` or `related_files` containing local temporary absolute paths (for example `/tmp/...`, `/Users/...`, `/home/...`) instead of repository-relative paths.
- Leftover `TODO`, `TBD`, or `FIXME` in page bodies.

## Quality Issues

The following are checked only in `--quality` mode:

- API pages missing `Field | Source | Required` field table.
- API pages missing `IDL Source` section.
- API pages missing request or response examples.
- API pages missing error-behavior description.
- Dependency pages missing dependency matrix or failure impact.
- Config/cache pages missing defaults or runtime impact.
- Auth/identity pages missing identity sources.
- Business-flow pages missing business context, field propagation, runtime observability, or failure modes.
- Field-propagation pages missing field matrix, downstream mapping, config/defaults, or observability.
- Runbooks missing owners, metrics dashboards, alerts, or common error logs.

## Acceptable Exceptions

- `questions/` pages may use `status: draft` while investigation is incomplete.
- Historical `decisions/` pages may reference removed source files, but must use `status: retired` and explain why the source is gone.
- External links are not checked by lint scripts.
- Cross-repo pages in `system/wiki/` may lack direct `related_files`, but must link to repo wiki, contract, or question pages.

If an exception is intentionally kept, document the reason in the page body to avoid accidental “fixes” by later agents.

Environment metadata is not an exception to path rules: keep it in `log.md` narrative text, not in evidence path fields.
