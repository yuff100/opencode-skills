---
name: maintain-repo-wiki
description: Build and maintain persistent Markdown knowledge bases for code repositories and microservice systems. Supports single-repo Repo Mode, centralized Knowledge Repo Mode, and cross-repo System Mode. Requires broad-to-deep coverage across architecture, service boundaries, business flows, field propagation, state side effects, dependency-failure impact, trusted API references, IDL/source contracts, telecom protocols (SIP, Diameter, RTP), internal message interfaces (tMsg), config/cache, runtime metrics/logs/alerts/owners, troubleshooting runbooks, historical context, and reusable business Q&A so the knowledge base can answer integration, history, change-impact, and troubleshooting questions reliably.
---

# Maintain Repo Wiki

Use this skill to build persistent knowledge bases for a single code repository or a set of microservice repositories. The default style is a broad-to-deep engineering manual: establish system architecture, service boundaries, and source map first, then drill down into business flows, field propagation, state side effects, interface contracts, dependency-failure impact, and runtime troubleshooting evidence.

Core goal: make the wiki serve onboarding, integration, business consultation, historical context, requirement changes, cross-service impact analysis, and production troubleshooting. For business questions, the wiki should explain where a field/state/request comes from, who rewrites it, where it is passed, what it affects, and which metrics/logs to check when abnormal behavior appears. Long-term Q&A accumulation in the Karpathy Project Wiki style remains in `queries/`, while single-repo default output focuses on engineering and business-flow manuals.

## Three Modes

### Repo Mode (Single Repository)

For the current repository’s own wiki. Default output:

```text
wiki/
├── index.md
├── log.md
├── SCHEMA.md
├── overview.md
├── source-map.md
├── components/
│   ├── config-and-cache.md
│   └── external-dependencies.md
├── flows/
│   ├── auth-and-identity.md
│   ├── business-flows.md
│   ├── field-propagation.md
│   └── runtime-observability.md
├── apis/
│   ├── http-endpoints.md
│   └── telecom-interfaces.md
├── runbooks/
│   └── request-troubleshooting.md
├── queries/
├── questions/
│   ├── idl-source-location.md
│   └── operations-metadata.md
└── decisions/
```

Run:

```bash
python3 <skill>/scripts/init_repo_wiki.py <repo-root>
```

### System Mode (Cross-Repository System Wiki)

For maintaining cross-service global knowledge only, without full per-repo wikis. Default output is `system-wiki/`:

```bash
python3 <skill>/scripts/init_repo_wiki.py <root> --mode system
```

### Knowledge Repo Mode (Centralized Knowledge Repository)

For creating a dedicated knowledge repository that stores per-input-repo wikis and a global system wiki. Default output:

```text
knowledge-repo/
├── sources.yaml
├── repos/
│   └── <repo-name>/wiki/
└── system/
    └── wiki/
```

Run example:

```bash
python3 <skill>/scripts/init_repo_wiki.py <knowledge-repo-root> --mode knowledge \
  --repo https://code.example.com/example/mock_feed_service \
  --repo /abs/path/to/local/repo
```

## Recommended Strategy for Multi-Repo, Multi-Component Systems

For communication platforms with many repositories and dozens of components per repository, use a layered and incremental strategy:

1. **System layer first (`system/wiki/`)**
   - Build service catalog, dependency graph, cross-repo request flows, field flows, and system-level runbooks.
   - Prioritize high-impact chains such as SIP signaling path, Diameter policy/charging path, RTP media path, and tMsg event path.

2. **Repository layer second (`repos/<repo>/wiki/`)**
   - For each repository, fill `overview.md`, `source-map.md`, `components/external-dependencies.md`, `flows/field-propagation.md`, and highest-risk runbooks before deep component coverage.

3. **Component layer third (within each repo wiki)**
   - Split each repository into bounded component pages (`components/<component>.md`) and related flow pages (`flows/<component>-*.md`).
   - Keep one page per clear boundary. If a page grows too large, split by write path, read path, or dependency segment.

4. **Incremental deepening instead of one-shot full generation**
   - Do not try to fully document all components in one pass.
   - Start with critical paths and frequently changed components, then expand by priority.

5. **Diff-driven maintenance**
   - After each code change, use `changed_files.py` to update only impacted pages and linked system pages.

6. **Quality gate as ongoing policy**
   - Run `wiki_lint.py` for structure and `wiki_lint.py --quality` for operational depth.
   - Track unresolved facts in `questions/` with evidence and owners for follow-up.

## Core Rules

- Always treat current source code, IDL/source contracts, in-repo docs, and user-provided context as factual sources.
- Single-repo facts go to `wiki/`; in centralized knowledge repos, each repository’s facts go to `repos/<repo-name>/wiki/` with the same engineering-manual depth.
- Cross-repo facts go to `system/wiki/`, such as service catalog, dependency graph, contracts, end-to-end request flows, and cross-service runbooks.
- Do not copy full source code; capture only verifiable knowledge, source references, interface contracts, runtime relationships, and open questions.
- Path policy: in documentation evidence fields (for example `source_files` and `related_files`), write only repository-relative paths (for example `/ims/...` or `src/module/file.go`). Never write local temporary absolute paths (for example `/tmp/...`, `/Users/...`, `/home/...`) in evidence path fields.
- If execution environment details are needed, record them only as explanatory text in `log.md`, not inside evidence path fields.
- Use wiki pages for fast positioning, then verify key conclusions in source code or contracts.
- Organize knowledge from broad to deep: architecture/service catalog/dependency graph first, then repo overview/source-map, then business flows, field propagation, API, config/cache, runbook, and queries.
- Flows are not limited to auth/identity. Every core business entry must have a business-flow page describing parameter entry, validation/mapping/propagation, involved components, state side effects, failure behavior, and metrics/log verification.
- For repeatedly asked user questions, accumulate in `queries/` and back-link to flow/API/runbook so the wiki can answer business consultation and historical-context questions repeatedly.
- When adding or significantly modifying pages, update `index.md` and `log.md` together.
- Put uncertain information in `questions/`. Do not guess.
- Default body language is now English; keep code identifiers, file paths, API fields, config keys, log fields, metrics, alerts, service names, and error codes in their original literal form.

## Page Organization

- `index.md`: knowledge-base entry organized by components, flows, APIs, runbooks, and open questions.
- `overview.md`: repository responsibilities, tech stack, directory map, entry points, and architecture overview.
- `source-map.md`: mapping from source areas to wiki pages to determine which pages to update after code changes.
- `components/`: engineering components such as service shell, middleware, handler/client, config/cache, and external dependencies.
- `flows/`: business flows, field propagation, auth identity, core requests, data writes, background jobs, cross-component execution sequences, runtime observability.
- `apis/`: endpoint/interface-level references for HTTP/RPC/CLI/event/schema, plus telecom protocols (SIP, Diameter, RTP) and internal message interfaces (tMsg).
- `runbooks/`: troubleshooting manuals, debug procedures, release checks, incident response.
- `queries/`: long-term valuable Q&A and analysis.
- `questions/`: items pending confirmation, such as IDL location and owner/dashboard/alert source.
- `decisions/`: architecture decisions and trade-offs.

## Engineering Manual Profile

Each repository’s first wiki pass should reach this quality:

- API pages are not route lists; they are endpoint/interface references including route, method, handler, IDL/source contract, field tables, field sources, requiredness, response shapes, error behavior, and examples. For telecom/message interfaces, include protocol profile, SIP headers, Diameter AVPs, RTP/RTCP attributes, and tMsg envelope semantics when applicable.
- Flow pages explain entry points, middleware/handler sequence, identity sources, state side effects, failure modes, and verification notes.
- Component pages explain responsibility, key source files, public interfaces, dependencies, failure impact, and change notes.
- Business-flow pages explain end-to-end logic for user/business questions: entry, field source, validation/mapping, branches, component calls, downstream request construction, state side effects, output, failure modes, metrics/logs, and troubleshooting entry points.
- Field-propagation pages explain how key business fields propagate from HTTP/RPC/event/config or telecom/message interfaces (SIP/Diameter/RTP/tMsg) to downstream dependencies, and can answer whether a parameter is passed through, where it is rewritten, and how missing values are handled.
- External-dependency pages explain dependency types, hard vs degradable classification, timeout/error handling, degradation paths, and user-visible impact.
- Config/cache pages explain config sources, JSON shapes, defaults, runtime impact, test-lane switches, cache keys, TTL, and invalidation paths.
- Runbook pages explain symptoms, owners, metrics dashboards, alerts, common error logs, fast checks, mitigations, and escalation.
- Unconfirmed IDL/source contract, owner, dashboard, alert, log entry, and related facts must be recorded in `questions/` with search evidence.

## Workflow

### Bootstrap (Initialization)

1. For single repo, run Repo Mode and read `rg --files`, README, CLAUDE.md, package manifest, build config, route definitions, service entry points, config, IDL/source contracts, and tests.
2. For knowledge repos, run Knowledge Repo Mode, fill `sources.yaml` first, generate `repos/<repo-name>/wiki/` for each input repo, and generate `system/wiki/`.
3. Prioritize filling `overview.md`, `source-map.md`, `components/config-and-cache.md`, `components/external-dependencies.md`, `flows/auth-and-identity.md`, `flows/business-flows.md`, `flows/field-propagation.md`, `flows/runtime-observability.md`, primary `apis/` (including `apis/telecom-interfaces.md` when SIP/Diameter/RTP/tMsg exist), and highest-risk `runbooks/`.
4. Continue with repo-specific components and core business flows based on source code, e.g., `components/request-middleware.md`, `components/<domain>-adapter.md`, `flows/<domain>-request.md`, `flows/<domain>-pipeline.md`, `flows/<dependency>-request-build.md`. Do not stop at auth flow; if the service has feed/order/payment/search/collect/impression chains, business flows are mandatory.
5. For cross-repo first pass, prioritize `system/wiki/service-catalog.md`, `dependency-graph.md`, key `contracts/`, end-to-end `request-flows/`, `field-flows/`, and cross-service runbooks, with links back to detailed `repos/<repo-name>/wiki/` pages.
6. Write only verifiable information; missing information goes to `questions/` with search path or command evidence.
7. Run `git status --short wiki system repos sources.yaml` and tell the user which knowledge-base files are still untracked.

### Ingest (Code or Document Ingestion)

1. Define target scope clearly: files, modules, diff, PR, issue, design doc, IDL/source contract, or user-provided material.
2. Read original source/contract/material before writing wiki content.
3. Update only the minimum relevant pages; avoid unrelated edits.
4. Prefer `source_files` in frontmatter for source references; keep `related_files` only when needed for legacy-page compatibility. In centralized knowledge repos, also include `repo`, `repo_url`, and `verified_commit`. For `source_files`/`related_files`, use repository-relative paths only.
5. If the result forms long-term valuable Q&A synthesis, write it into `queries/`.

### Deepen

When the wiki is good for onboarding but not yet sufficient for integration, requirement changes, or operations troubleshooting:

1. Upgrade API overviews to endpoint/interface-level references with field tables, field sources, requiredness, error behavior, IDL source, and examples. For telecom/message systems, include protocol profile and protocol-specific sections for SIP, Diameter, RTP, and tMsg.
2. Locate source IDL or generated-contract input. If not found, record search evidence in `questions/idl-source-location.md`.
3. Add external-dependency pages covering dependency type, hard/degradable classification, timeout/error handling, degradation, and user-visible impact.
4. Add JSON examples, defaults, runtime impact, test switches, dashboards, alerts, owners, common error logs, and mitigation steps to config/cache and runbook pages.
5. Add business-flow and field-propagation pages for core business entries: list source, mapping, default, internal object propagation, downstream RPC/event/cache fields, filtering/sorting/recording usage, and missing/exception behavior field by field. Include protocol-field mapping when interfaces traverse SIP, Diameter, RTP, or tMsg.
6. Add runtime observability: metric names/tags, log patterns, request IDs, dashboards/alerts, common exception samples, and symptom-to-component/dependency mapping.
7. In `system/wiki/`, add producer/consumer mappings, cross-service failure impact, end-to-end request flow, cross-repo field-propagation matrix, and cross-service troubleshooting paths.

### Query (Answer Questions)

1. Read the current-level `index.md` first.
2. For single-repo questions, read relevant pages in `wiki/` or `repos/<repo>/wiki/`.
3. For cross-service questions, read `system/wiki/` first, then jump to corresponding `repos/<repo>/wiki/` and source/contract as needed.
4. For business-field/flow questions, prioritize `flows/field-propagation.md`, related `flows/<domain>*.md`, API field tables, config/cache, and dependency/runbook pages; do not only read auth flow.
5. Verify key conclusions against source code, IDL/source contracts, metrics/logs, or user-provided facts.
6. If the wiki cannot answer, state the gap clearly and add `queries/<question>.md` or update flow/field-propagation pages; do not leave the same question unanswered next time.
7. If the answer has long-term value, store it in `queries/` and update `index.md` and `log.md`.

### Refresh (After Code Changes)

1. Run `python3 <skill>/scripts/changed_files.py --wiki wiki` or target `repos/<repo>/wiki`.
2. Re-read affected source files.
3. If responsibility, behavior, interface, dependency, or runtime impact changes, update related pages.
4. If cross-service contracts, dependency graph, or request flow are affected, update `system/wiki/` accordingly.

### Lint (Health Check)

Run:

```bash
python3 <skill>/scripts/wiki_lint.py wiki
python3 <skill>/scripts/wiki_lint.py wiki --quality
```

Basic lint detects missing frontmatter, broken links, orphan pages, missing source files, and leftover `TODO/TBD/FIXME`. `--quality` checks whether API/dependency/config/auth/runbook pages are sufficient for integration, runtime understanding, and troubleshooting. See `references/lint-rules.md` for detailed rules.

## Scripts

- `scripts/init_repo_wiki.py`: initialize Repo/System/Knowledge Repo modes.
- `scripts/wiki_lint.py`: check wiki health and quality gates.
- `scripts/changed_files.py`: map changed source files to wiki pages that reference them, supporting both `source_files` and `related_files`.
- `scripts/wiki_inventory.py`: output page metadata JSON for audit or automation.
