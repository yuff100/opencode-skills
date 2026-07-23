# maintain-repo-wiki
Production-grade LLM wiki workflows for single-repo and multi-repo systems, with continuous evolution for business knowledge, troubleshooting, and shared understanding.

`maintain-repo-wiki` builds long-lived Markdown knowledge bases for code repositories, microservice systems, or centralized knowledge-repo setups.

It does more than generating a README or directory index. It consolidates source code, IDL/source contracts, configs, dependencies, business flows, field propagation, metrics/logs/alerts, troubleshooting experience, and long-term Q&A into an engineering knowledge base. The goal is for the wiki to answer onboarding, integration, business consultation, historical context, change impact, and production troubleshooting questions.

## Use Cases

- Complete `wiki/` for a single repository so future contributors can quickly understand architecture, entry points, module boundaries, and core flows.
- Build a centralized knowledge base for multiple repositories, separating per-repo facts from cross-service system facts.
- Deepen an existing wiki from “good for onboarding” to “good for integration, change assessment, and troubleshooting.”
- Refresh relevant wiki pages after code changes, PRs, IDL changes, or production incidents.
- Turn repeatedly asked business questions into reusable answers to avoid repeated analysis.

## Agent Prompt Examples

Send the following prompts to any agent that supports this skill. Execution details and quality requirements are defined in `SKILL.md`, so you do not need to repeat them in the prompt.

### Initialize

```text
Use maintain-repo-wiki to initialize and populate an engineering wiki for the following repositories. Repo 1: xxx; Repo 2: xxx (can be absolute local paths or GitHub links).
```

### Ingest

```text
Use maintain-repo-wiki to ingest the following code change / design doc / troubleshooting conclusion into the current repository wiki:

<paste diff, PR link, design doc, log conclusion, or change notes>
```

### Query

```text
Use maintain-repo-wiki to answer this question based on the current repository wiki:

<write a concrete business question, field propagation question, integration question, change-impact question, or troubleshooting question>
```

## Core Principles

- Treat source code, IDL/source contracts, repository docs, configs, logs, and user-provided facts as ground truth. Do not guess.
- Organize knowledge from broad to deep: system architecture and service boundaries first, then source map, business flows, field propagation, APIs, config/cache, and runbooks.
- Flows are not limited to auth paths. Every core business entry should include business flow, field origins, state side effects, failure modes, and verification methods.
- Do not copy large code blocks. Record only verifiable conclusions, source references, API contracts, runtime relationships, and open questions.
- Put uncertain information in `questions/`; never present it as a conclusion.
- When adding or significantly changing pages, update `index.md` and `log.md` together.

## Three Modes

### Repo Mode

For a single repository wiki. Default output path is `wiki/`.

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/init_repo_wiki.py <repo-root>
```

Typical output:

```text
wiki/
├── index.md
├── log.md
├── SCHEMA.md
├── overview.md
├── source-map.md
├── components/
├── flows/
├── apis/
├── runbooks/
├── queries/
├── questions/
└── decisions/
```

### System Mode

For cross-repo, cross-service system knowledge only. It does not store full per-repo wikis. Default output path is `system-wiki/`.

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/init_repo_wiki.py <root> --mode system
```

Suitable for service catalog, dependency graph, cross-service request flow, field flow, contracts, and cross-service runbooks.

### Knowledge Repo Mode

For a dedicated knowledge repository that stores both per-repo wikis and a global system wiki.

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/init_repo_wiki.py <knowledge-repo-root> --mode knowledge \
  --repo https://code.byted.org/mercury/oversea_open_stream \
  --repo /abs/path/to/local/repo
```

Typical output:

```text
knowledge-repo/
├── sources.yaml
├── repos/
│   └── <repo-name>/wiki/
└── system/
    └── wiki/
```

## Recommended Workflow

### 1. Bootstrap

After initialization, read real repository context first:

```bash
rg --files
```

Prioritize README, AGENTS/CLAUDE docs, package/build config, service entry points, route definitions, configs, IDL/source contracts, and tests. Fill these first:

- `overview.md`
- `source-map.md`
- `components/config-and-cache.md`
- `components/external-dependencies.md`
- `flows/auth-and-identity.md`
- `flows/business-flows.md`
- `flows/field-propagation.md`
- `flows/runtime-observability.md`
- Main `apis/`
- Highest-risk `runbooks/`

### 2. Ingest

When ingesting code, diffs, PRs, issues, design docs, or IDL/source contracts:

- Read source material first, then write wiki content.
- Update only the minimum relevant pages.
- Use `source_files` in frontmatter to record source references.
- In centralized knowledge repos, also record `repo`, `repo_url`, and `verified_commit`.
- Write high-value Q&A into `queries/`.

### 3. Deepen

When the wiki is only sufficient for onboarding but not troubleshooting or change assessment, keep adding:

- API field tables, field origins, requiredness, response shape, error behavior, and examples.
- Business flow, field propagation, external dependency failure impact, and config/cache runtime impact.
- Metric names/tags, log patterns, request IDs, dashboards, alerts, owners, and common error logs.
- Missing contracts, owners, dashboards, alerts, or log entry points should go into `questions/` with search evidence.

### 4. Query

When answering questions, read the current wiki `index.md` first, then route by question type:

- Single-repo questions: read `wiki/` or `repos/<repo>/wiki/`.
- Cross-service questions: read `system/wiki/` first, then jump to repo wiki pages and source code.
- Field/flow questions: prioritize `flows/field-propagation.md`, related business flows, API field tables, config/cache pages, and runbooks.

If the wiki cannot answer, fill missing pages or add `queries/<question>.md` so the next answer does not restart from zero.

### 5. Refresh

After code changes, use the changed-files tool to locate impacted pages:

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/changed_files.py --wiki wiki
```

You can also pass changed files explicitly:

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/changed_files.py \
  --wiki wiki \
  --changed biz/handler/foo.go biz/domain/bar.go
```

Then re-read impacted source files and refresh related wiki pages. If cross-service contracts, dependency graph, or request flow are affected, update `system/wiki/` as well.

## Quality Checks

Basic lint:

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/wiki_lint.py wiki
```

Quality lint:

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/wiki_lint.py wiki --quality
```

`--quality` checks whether API, dependency, config, auth/identity, runbook, and other pages are sufficient for integration, runtime understanding, and troubleshooting.

Output page metadata:

```bash
python3 /Users/bytedance/.codex/skills/maintain-repo-wiki/scripts/wiki_inventory.py wiki
```

## Expected Wiki Depth

A qualified engineering wiki should answer:

- What this repository is responsible for, and where its core entry points are.
- For an HTTP/RPC/event interface, what the contract, field origins, requiredness, and error behavior are.
- How a business field propagates from entry point to downstream dependencies, and where it is defaulted, rewritten, filtered, or persisted.
- What side effects are produced by a state change.
- User-visible impact when dependencies fail, timeout, or return invalid responses.
- Which metrics, logs, alerts, dashboards, and request IDs to use during incidents.
- Which flows, APIs, config/cache pages, runbooks, or cross-service contracts are impacted by code changes.

If the wiki cannot answer these questions, deepen it instead of keeping only directory-level descriptions.

## Script Quick Reference

- `scripts/init_repo_wiki.py`: initialize Repo/System/Knowledge Repo modes.
- `scripts/wiki_lint.py`: check wiki health and quality gates.
- `scripts/changed_files.py`: map changed source files to wiki pages that reference them.
- `scripts/wiki_inventory.py`: export page metadata JSON for audits or automation.

## References

- `SKILL.md`: full behavior rules and workflow.
- `references/lint-rules.md`: lint and quality check rules.
- `references/page-schemas.md`: page schema and frontmatter conventions.
- `references/quality-gates.md`: quality gates for engineering knowledge bases.
- `references/workflows.md`: detailed maintenance workflows.
- `references/accuracy-and-runtime.md`: accuracy and runtime evidence requirements.
