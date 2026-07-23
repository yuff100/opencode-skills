# Quality Gates

When the first wiki version is already useful for onboarding but still needs to support integration, requirement changes, cross-service understanding, or troubleshooting, use these gates to decide what to deepen next.

## Completion Levels

### Level 1: Orientation

- Single-repo `wiki/index.md` links all important pages.
- `overview.md` explains responsibilities, tech stack, directory map, and major architecture.
- `source-map.md` maps major source areas to wiki pages.
- Covers key entities and core concepts/request flows.
- Unknown information is tracked in `questions/`.
- `wiki_lint.py` passes.

### Level 2: Integration and Change Work

- API pages are documented per endpoint or interface.
- Each endpoint includes method/route, handler, IDL source, field table, field source, requiredness, response shape, error behavior, and examples.
- Telecom interfaces include protocol profile and protocol-specific field coverage where applicable:
  - SIP header semantics
  - Diameter command/AVP semantics
  - RTP/RTCP media attributes
  - tMsg envelope and delivery semantics
- Config/cache pages include JSON structure, defaults, runtime impact, and test toggles.
- Dependency pages distinguish hard dependencies from degradable dependencies.
- Auth/identity flows explain where tenant, user, signature, token, region, or request context comes from.
- Core business entries have business-flow pages, not only auth/identity pages.
- Key business fields have field-propagation matrices answering whether fields are sent to downstream dependencies, where they are mapped/defaulted/dropped, and behavior on abnormal inputs.
- `wiki_lint.py --quality` passes, or every remaining issue has explicit justification.

### Level 3: Operations and Troubleshooting

- Runbooks cover common failures, logs, metrics, fast checks, mitigation, and escalation.
- For telecom systems, runbooks include protocol-specific checks (for example SIP signaling steps, Diameter peer status, RTP quality counters, tMsg delivery/retry state).
- External dependency pages describe timeout behavior, empty responses, error propagation, fallback, and user-visible impact.
- When confirmable, runbooks include service owner, metrics dashboards, alert names, and common error-log samples.
- Business-flow and runtime-observability pages map metrics/logs back to business stages, components, and dependencies.
- For common business/historical questions, `queries/` contains reusable answers linking to flow/API/config/runbook pages.
- `log.md` states current policy and marks outdated records as superseded.
- Wiki is tracked in git, unless user explicitly chooses local-only draft mode.

### Level 4: System Knowledge (Cross-Repository)

- `sources.yaml` records all input repositories, source_type, url/path, branch, role, owner, and scan_mode.
- `repos/<repo-name>/wiki/` stores per-repository local knowledge.
- `system/wiki/service-catalog.md` covers all services.
- `system/wiki/dependency-graph.md` records upstream/downstream, protocol, contract, and failure impact.
- `system/wiki/contracts/` maps IDL/source contracts to producer/consumer.
- `system/wiki/request-flows/` records end-to-end request chains.
- `system/wiki/field-flows/` records key cross-service field propagation and downstream usage.
- Missing cross-service facts are tracked in `system/wiki/questions/`.

## Page-Specific Checks

API page:

- A route-only table is only a starting point, not the final state.
- Each endpoint/interface should have its own section.
- Source IDL path must be explicit, or field origin must be explained.
- Examples must be verifiable from code, tests, IDL, or docs.
- If IDL cannot be found, create or update a question page instead of guessing fields.
- If the interface is SIP, Diameter, RTP, or tMsg, include verifiable protocol-specific examples and field mapping evidence.

Dependency page:

- Include dependency name, client code, purpose, hard/degradable classification, timeout/error behavior, fallback, and user-visible impact.
- Write owner or escalation path only if confirmed from repo or user context.

System page:

- Do not copy downstream internal implementations. Record only cross-service boundaries, contracts, call direction, and failure impact.
- Link internal details to `repos/<repo-name>/wiki/`.
- For cross-service business questions, there must be a request flow or field flow connecting fields, state, dependencies, and runtime evidence.

Business-flow page:

- Do not only list call chains; explain business semantics: input meaning, why each step exists, how fields change, and what outputs affect.
- Include key-field tables, branch conditions, downstream request construction, state side effects, failure modes, metrics/logs, and verifiable source files.
- If a business question was asked before and wiki could not answer, prioritize flow/field-propagation updates before adding query entries.

Field-propagation page:

- Organize by fields, not by code functions.
- At minimum cover key fields from major entries: tenant, identity, region, language/country/device, business category, content ID, state/dedup/experiment, etc.
- For each field, state whether it enters downstream RPC/event/cache/search/sort; if unconfirmed, explicitly write `unknown` and list next checks.
- For telecom/message workflows, also state whether each protocol field is preserved, transformed, or dropped between SIP, Diameter, RTP, tMsg, and internal objects.

Runbook:

- Include owners, metrics dashboards, alert names, common error-log samples, fast checks, mitigation, and escalation.
- If operations metadata is unavailable in the repository, record gaps in `questions/` and ask users where owner/dashboard/alert sources come from. Do not fabricate.
- Include protocol-level troubleshooting evidence where applicable (SIP signaling traces, Diameter command/result patterns, RTP/RTCP metrics, tMsg retry/dead-letter indicators).

Maintenance log:

- Keep historically valuable records.
- Mark outdated policy as superseded and note current policy nearby.
- Keep records concise and date-stamped.
