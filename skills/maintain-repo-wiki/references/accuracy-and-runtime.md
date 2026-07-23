# Accuracy and Runtime Evidence Supplement

Use this reference when the first wiki version needs more trustworthy API information or a more realistic representation of runtime behavior.

## Locate Source IDL / Source Contract

Before finalizing API fields, search for contract sources first:

```bash
rg --files -g '*.thrift' -g '*.proto' -g '*.idl' -g '*openapi*' -g '*swagger*'
rg -n "idl|thrift|proto|openapi|swagger|kitex|hertz|generate|gen" .
```

Also inspect build files, generation scripts, `go:generate` comments, CI config, `go.mod`, `.gitmodules`, README/deploy docs, and generated-code headers.

After finding the source, update API pages:

- `## IDL Source`: record path, generator, generated output path, and latest verified commit.
- Endpoint field table: record field name, source, requiredness, type, default, validation logic, and response shape.

If source is not found, update or create `questions/idl-source-location.md` and record:

- Executed search commands
- Checked paths
- Possible external repository or package clues
- Fields still unverified

Do not infer missing fields from handler names only. The point of locating IDL/source contract is to make generated API information accurate and trustworthy.

## Reflect Real Runtime

Before writing business-flow, field-propagation, runbook, or runtime pages, search repository docs, deployment/config files, monitoring metadata, and test fixtures:

```bash
rg -n "owner|oncall|dashboard|grafana|argos|metrics|alarm|alert|log|SLO|SLA" .
```

Only write the following into runbooks when confirmed from repository files, monitoring config, deployment metadata, or user-provided context:

- Service owner or oncall group
- Metrics dashboard name or link
- Alert names and trigger meanings
- Common error-log samples
- Request identifiers required for trace/debug
- Fast checks and mitigation steps

If confirmation is unavailable, create `questions/operations-metadata.md`, list missing owner/dashboard/alert/log-source information, and ask the user where to get it. Do not fabricate operations metadata; the goal is to reflect real runtime.

## Business Flows and Field Propagation

When users ask “is this field passed downstream?”, “where does this business policy take effect?”, or “why does production behavior differ from request parameters?”, prioritize updating `flows/field-propagation.md` and related business-flow pages:

- Start from API/IDL fields and record field source, requiredness, default, and validation.
- Track fields through handler/adapter/request builder/provider/filter/packer/recorder.
- For each downstream RPC/event/cache/search/sort request, record whether fields are passed, renamed, mapped by config, or overridden.
- Record how metrics/logs verify whether a field or stage takes effect, such as request IDs, metric names/tags, and log patterns.
- If unconfirmed, write `unknown` plus next checks; do not replace verified conclusions with assumptions like “should be passed through.”
