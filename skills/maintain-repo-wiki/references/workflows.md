# Workflows

## Repo Mode (Single Repository)

1. Run `python3 <skill>/scripts/init_repo_wiki.py <repo-root>`.
2. Use `rg --files` to understand repository structure.
3. Read README, CLAUDE.md, package manifest, build config, route definitions, service entry points, handler/client code, config, IDL/source contracts, protocol dictionaries/specs (for SIP/Diameter/RTP), message-interface definitions (for tMsg), and tests.
4. Substantially fill default engineering-manual pages: `overview.md`, `source-map.md`, `components/config-and-cache.md`, `components/external-dependencies.md`, `flows/auth-and-identity.md`, `apis/http-endpoints.md`, `apis/telecom-interfaces.md` (if telecom protocols or message interfaces exist), and `runbooks/request-troubleshooting.md`.
5. Add repository-specific pages based on actual structure, such as `components/request-middleware.md`, `components/<domain>-adapter.md`, `flows/<domain>-request.md`, `flows/<write-path>.md`.
6. Put unknown facts into `questions/` with search evidence. Do not guess owner, dashboard, alert, IDL source, or external callers.
7. Run `git status --short wiki` and report status.

## Knowledge Repo Mode (Centralized Knowledge Repository)

1. Run `python3 <skill>/scripts/init_repo_wiki.py <knowledge-root> --mode knowledge --repo <url-or-path> ...`.
2. Check `sources.yaml` and fill each repo’s role, owner, branch, and scan_mode.
3. For each input repo, generate or update `repos/<repo-name>/wiki/` using the same engineering-manual depth as single-repo mode.
4. For each repository, at minimum fill API, core flows, external dependencies, config/cache, runbooks, and questions.
5. Generate `system/wiki/` based on each repository wiki plus source code/IDL.
6. `system/wiki/` records cross-service facts only. Do not copy downstream internal implementations; link internal details to `repos/<repo-name>/wiki/`.
7. `.kb-cache/` may be used to clone/cache input repos but should not be committed.

### Layered Generation for Multi-Repo, Multi-Component Systems

When each repository contains many subcomponents, use phased generation to avoid shallow or stale wiki pages:

1. **Phase A - System skeleton**
   - Fill `system/wiki/service-catalog.md`, `dependency-graph.md`, key `contracts/`, and core cross-service request/field flows.
   - Ensure SIP, Diameter, RTP, and tMsg paths are represented in system-level flow pages when applicable.

2. **Phase B - Repository skeletons**
   - For each `repos/<repo-name>/wiki/`, fill only high-value base pages first:
     - `overview.md`
     - `source-map.md`
     - `components/external-dependencies.md`
     - `flows/field-propagation.md`
     - highest-risk `runbooks/`

3. **Phase C - Component expansion**
   - Add component pages and dedicated flows incrementally:
     - `components/<component>.md`
     - `flows/<component>-request.md`
     - `flows/<component>-pipeline.md`
   - Prioritize by runtime impact, failure frequency, and change frequency.

4. **Phase D - Diff-driven refresh**
   - Use `changed_files.py` after PRs/incidents and refresh only affected pages.
   - If component-level changes impact cross-service behavior, update `system/wiki/` in the same cycle.

## System Wiki (Cross-Repository Layer)

Prioritize generating:

- `service-catalog.md`: services, repos, roles, owners, wiki links, runtime.
- `dependency-graph.md`: upstream, downstream, protocol, contract, failure impact.
- `contracts/`: IDL/source contract, producer/consumer, compatibility notes.
- `request-flows/`: end-to-end request chains and service hops.
- `runbooks/`: cross-service troubleshooting manuals.
- `questions/`: missing IDL, owner, dashboard, alert, and log samples.

## Ingest (Ingest Changes)

1. Define scope clearly: files, modules, diff, PR, issue, design docs, IDL/source contracts, or user-provided material.
2. Read original source/contract/material.
3. Update the minimum relevant pages.
4. Reference `source_files` in frontmatter; keep `related_files` only when needed for legacy compatibility. Use repository-relative paths only in these evidence fields; never use local temporary absolute paths.
5. Link new pages from `index.md`.
6. Append a record to `log.md`.

Do not paste large code blocks into the wiki. Prefer verifiable summaries, file references, and cross-page links.

If environment context is necessary (for example runtime host or workspace notes), place it in `log.md` narrative text rather than in evidence path fields.

## Query (Answer and Accumulate)

1. Read `index.md` at the relevant level.
2. Read candidate pages.
3. For strong conclusions, verify against source code, IDL/source contracts, or repo wiki pages.
4. If wiki and code conflict, trust code. When users request wiki maintenance, update the wiki accordingly.
5. Write long-term valuable answers into `queries/`.

## Refresh After Diff

1. Run `python3 <skill>/scripts/changed_files.py --wiki wiki` or target `repos/<repo>/wiki`.
2. Check related source files and nearby tests for impacted pages.
3. If behavior, responsibility, interface, or dependencies changed, update pages.
4. If changes affect cross-service contracts, dependency graph, or request flow, update `system/wiki/`.
5. Run `wiki_lint.py`.

## Deepen

1. Upgrade endpoint summaries into API references with route, method, handler, request fields, field sources, requiredness, response shape, error behavior, IDL source, and examples.
2. Search for source IDL before finalizing API fields. See `references/accuracy-and-runtime.md`. If source IDL is outside the repository, update a question page with search commands and evidence.
3. Add external dependency pages for runtime-impacting RPCs, caches, config services, queues, object storage, collectors, SIP peers, Diameter peers, RTP media services, or tMsg brokers.
4. Add config/cache runtime details: JSON shapes, defaults, test-only flags, runtime impact, reload behavior, cache-key shapes, TTL, and invalidation paths.
5. Add runbooks for likely incidents or interface failures, including owners, metrics dashboards, alerts, and common error-log samples. For telecom/message systems, include SIP signaling checks, Diameter peer/result-code checks, RTP quality checks, and tMsg delivery checks. If unavailable in repo/user context, create question pages instead of guessing.
6. Mark noisy but historically valuable log entries as superseded; do not delete directly.

## First-Pass Content Standard

Do not make the first wiki pass an empty shell with headings only. Even when information is incomplete, extract these verifiable items from source code:

- Routes, handlers, middleware, clients, config getters, cache keys, metric keys, and log prefixes.
- Protocol/message artifacts when applicable: SIP methods/headers, Diameter commands/AVPs, RTP/RTCP attributes, tMsg envelope fields.
- Field source, requiredness, response shape, and error behavior for each core endpoint.
- Caller source files, hard/degradable classification, failure propagation, and user-visible impact for each external dependency.
- Execution sequence, identity source, context writes, state side effects, and failure modes for each core flow.
- If operations metadata is missing, record it in `questions/operations-metadata.md` and distinguish “metrics/logs confirmed in code” from “production dashboard/alert pending confirmation.”
