# Page Schemas

These schemas apply to `wiki/`, `repos/<repo>/wiki/`, and `system/wiki/`. The default style is engineering-manual pages: machine-readable frontmatter and detailed, traceable English body content.

## Common Frontmatter

Single-repo page:

```yaml
---
title: Human readable title
type: overview | component | flow | api | runbook | query | question | decision
status: active | draft | retired
source_files:
  - path/from/repo/root.ext
last_verified_commit: commit-or-unknown
last_verified: YYYY-MM-DD
tags:
  - short-tag
---
```

Compatibility rules:

- `source_files` is the preferred field for new pages and represents source files directly verified for page conclusions.
- `related_files` is still supported and recognized by scripts, mainly for compatibility with Karpathy Project Wiki style pages.
- If a page records only external runtime information or cross-repo relationships, source files are optional, but links to repo wiki, contract, or question pages are required.

Additional fields for repository pages inside a centralized knowledge repository:

```yaml
repo: mock_feed_service
repo_url: https://code.example.com/example/mock_feed_service
verified_commit: commit-or-unknown
```

Rules:

- Use paths relative to the corresponding source repository root in `source_files`/`related_files`.
- Do not use local temporary absolute paths in evidence path fields (for example `/tmp/...`, `/Users/...`, `/home/...`).
- If environment details must be recorded, keep them in `log.md` narrative text, not in `source_files`/`related_files`.
- Use `status: draft` when unresolved facts remain on the page.
- Use `status: retired` only for historical knowledge.
- Each page should describe exactly one clearly bounded concept.
- Default body language is English; keep code symbols, paths, field names, config keys, log fields, metrics, alerts, and error codes in their original literal form.

## Repo Wiki Page Types

- `overview`: repository responsibilities, tech stack, directory map, architecture overview.
- `component`: modules, services, handlers, clients, config objects, cache, external dependencies.
- `flow`: business flow, field propagation, authentication, data flow, request paths, error handling, region behavior, cache strategy, architecture patterns, runtime observability.
- `api`: endpoint/interface-level interface docs including `IDL Source`, field table, examples, and error behavior, with support for HTTP/RPC/CLI/event/schema plus telecom protocols such as SIP, Diameter, RTP, and internal message interfaces such as tMsg.
- `runbook`: symptoms, owner, dashboard, alert, log samples, fast checks, mitigation, escalation path.
- `query`: long-term valuable question answers.
- `question`: unconfirmed information and next checks.
- `decision`: architecture background, decision, impact, alternatives, and revisit triggers.

## Default Repo Wiki Pages

First-pass initialization should create and substantially populate these pages after scanning source code, instead of leaving empty folders:

- `index.md`: entry page and links to all important pages.
- `overview.md`: repository responsibilities, tech stack, directory map, entry points, architecture, runtime notes.
- `source-map.md`: source areas, corresponding wiki pages, and notes.
- `components/config-and-cache.md`: config sources, JSON shape, defaults, runtime impact, test-lane switches, cache key, TTL, invalidation path.
- `components/external-dependencies.md`: dependency matrix, hard/degradable classification, timeout/error handling, failure impact, degradation, logs/metrics, escalation.
- `flows/auth-and-identity.md`: entry points, middleware/handler sequence, identity sources, tenant/user/token/region sources, failure modes.
- `flows/business-flows.md`: core business entries and business-flow index organized by business questions, not only by code directories.
- `flows/field-propagation.md`: propagation matrix from entry fields to internal objects, config, downstream dependencies, cache/event/response.
- `flows/runtime-observability.md`: metrics, logs, request IDs, dashboards, alerts, and troubleshooting entries mapped to business flows.
- `apis/http-endpoints.md`: route table, IDL/source contract, endpoint field table, examples, error codes, callers.
- `apis/telecom-interfaces.md`: protocol profile, interface/operation table, SIP header mapping, Diameter AVP mapping, RTP/RTCP attributes, tMsg envelope fields, protocol error/status references.
- `runbooks/request-troubleshooting.md`: symptoms, owner, fast checks, metrics dashboard, alerts, common error logs, mitigations, escalation.
- `questions/idl-source-location.md`: IDL/source contract search evidence and current best conclusion.
- `questions/operations-metadata.md`: search evidence and gaps for owner/dashboard/alert/log sources.

## Section Requirements

API page:

- `Protocol Profile` (required when documenting SIP/Diameter/RTP/tMsg)
- `Surface`
- `IDL Source`
- `Endpoint Reference`
- Field table: `Field | Source | Required | Type | Description`
- `Protocol-Specific Fields` for applicable protocols:
  - SIP headers
  - Diameter AVPs
  - RTP/RTCP attributes
  - tMsg envelope fields
- `Identity Sources` if auth/tenant/token/request context is involved
- `Example Request`
- `Example Response`
- `Errors And Status Codes`
- `Callers`

Component page:

- `Responsibility`
- `Key Files`
- `Public Interfaces`
- `Dependencies`
- `Failure Impact`
- `Change Notes`

Flow page:

- `Entry Points`
- `Middleware Or Handler Sequence` or `Sequence`
- `Business Context` explaining which business questions, historical context, or requirement scenarios this flow addresses
- `Field Propagation` if important request/config/state/downstream fields are involved
- `Identity Sources` if auth/identity/tenant is involved
- `Runtime Observability` describing metrics/logs/request IDs/dashboard/alerts
- `State And Side Effects`
- `Failure Modes`
- `Verification Notes`

Field-propagation page:

- `Scope`
- Field matrix: `Field | Source | Validation Or Mapping | Internal Object | Downstream | Runtime Use | Missing Or Error Behavior`
- `Downstream Request Mapping` describing whether fields enter RPC/event/cache/search/sort downstream requests
- `Config And Defaults`
- `Observability`
- `Open Questions`
- For telecom/message systems, include protocol-field mapping coverage for SIP, Diameter, RTP, or tMsg where relevant.

Runbook:

- `Symptoms`
- `Owners`
- `Fast Checks`
- `Metrics Dashboards`
- `Alerts`
- `Common Error Logs`
- `Mitigations`
- `Escalation`

Question page:

- `Question`
- `Search Evidence`
- `Current Best Answer`
- `Next Checks`

## System Wiki Pages

- `service-catalog.md`: service list, repo, role, owner, wiki links, runtime.
- `dependency-graph.md`: upstream, downstream, protocol, contract, failure impact, and Mermaid graph.
- `contracts/`: cross-service API/RPC/IDL/source contracts, producer/consumer, compatibility notes.
- `request-flows/`: end-to-end request paths with behavior and failure impact by service hop.
- `field-flows/`: cross-service field propagation by key business field, including source, mapping, downstream use, runtime evidence, and gaps.
- `runbooks/`: cross-service troubleshooting manuals.
- `questions/`: missing cross-repo facts such as owner, dashboard, alert, and IDL source.

System wiki records only cross-service boundaries and global runtime facts. It does not replace repository-internal details in `repos/<repo-name>/wiki/`.
