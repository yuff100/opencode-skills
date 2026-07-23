#!/usr/bin/env python3
"""Initialize engineering-manual style repo and system wikis."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


REPO_DIRECTORIES = ["components", "flows", "apis", "runbooks", "queries", "questions", "decisions"]
SYSTEM_DIRECTORIES = ["repos", "contracts", "request-flows", "field-flows", "runbooks", "questions"]


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def index_template() -> str:
    return """# Repository Wiki

This is the persistent engineering knowledge-base entry for the current repository. The first-pass goal is not only to generate directories, but to distill verifiable knowledge from source code, IDL/source contracts, configuration, and runtime evidence for integration support, change reviews, dependency-impact analysis, and common incident troubleshooting.

## Language Policy

Wiki body content defaults to English. Keep code identifiers, file paths, API field names, config keys, log fields, metrics, alerts, service names, error codes, and exact runtime literals in their original form.

## Core Maps

- [Repository Overview](overview.md)
- [Source Map](source-map.md)
- [Schema](SCHEMA.md)
- [Maintenance Log](log.md)

## Components

- [Config and Cache Runtime](components/config-and-cache.md)
- [External Dependencies and Failure Impact](components/external-dependencies.md)

## Flows

- [Auth and Identity Flow](flows/auth-and-identity.md)
- [Business Flow Index](flows/business-flows.md)
- [Field Propagation Matrix](flows/field-propagation.md)
- [Runtime Observability](flows/runtime-observability.md)

## API

- [HTTP Endpoints](apis/http-endpoints.md)
- [Telecom Interfaces](apis/telecom-interfaces.md)

## Runbooks

- [Request Troubleshooting Runbook](runbooks/request-troubleshooting.md)

## Open Questions

- [IDL Source Location](questions/idl-source-location.md)
- [Operations Metadata Sources](questions/operations-metadata.md)

## Continuous Accumulation

- `queries/`: long-term valuable question answers and analysis.
- `decisions/`: architecture decisions and trade-offs.
"""


def schema_template() -> str:
    return """# Repo Wiki Schema

Every non-core page should start with frontmatter:

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

`related_files` is still recognized by scripts as a compatibility field. New pages should prefer `source_files` because it more directly expresses which source files support page conclusions.

Body content defaults to English; keep code symbols, paths, API fields, config keys, log fields, metrics, alerts, service names, and error codes in their original literal form.

## Page Types

- `component`: modules, handlers, clients, config objects, cache, external dependencies.
- `flow`: business flows, field propagation, request chains, auth identity, data flow, state transitions, failure paths, runtime observability.
- `api`: endpoint/interface-level API manuals.
- `runbook`: symptoms, owner, dashboard, alert, logs, fast checks, mitigation, and escalation paths.
- `question`: information not confirmable from source code or runtime, with search evidence and next checks.
- `query`: long-term valuable question answers.
- `decision`: architecture background, decision, impact, alternatives, and revisit triggers.

Keep conclusions verifiable, cite source files, and update metadata after verification.
"""


def overview_template() -> str:
    return """---
title: Repository Overview
type: overview
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - overview
---

# Repository Overview

Use this page to describe the repository's tech stack, core responsibilities, directory map, key entry points, and major architectural relationships. In the first pass, write only information that can be confirmed from source code, configuration, README, IDL, or user-provided context.

## Tech Stack

## Responsibilities

## Directory Map

## Entrypoints

## Architecture

## Runtime Notes

## Key Pages
"""


def log_template() -> str:
    today = date.today().isoformat()
    return f"""# Repo Wiki Log

- {today}: Initialized repository wiki.
"""


def source_map_template() -> str:
    return """# Source Map

Record high-level source areas and corresponding primary wiki pages.

| Source path | Wiki page | Notes |
| --- | --- | --- |
"""


def api_template() -> str:
    return """---
title: HTTP Endpoints
type: api
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - http
  - api
---

# HTTP Endpoints

## Surface

| Endpoint | Method | Handler | Purpose |
| --- | --- | --- | --- |

## IDL Source

Record source IDL/source contracts, generation entry points, and generated artifacts. If not found, write search evidence to `questions/idl-source-location.md`.

| Source | Path Or Link | Notes |
| --- | --- | --- |

## Endpoint Reference

Create a dedicated subsection for each endpoint. Field tables should document source, requiredness, and type.

### Endpoint Name

| Field | Source | Required | Type | Description |
| --- | --- | --- | --- | --- |

## Identity Sources

| Source | Field/Context | Used By | Notes |
| --- | --- | --- | --- |

## Example Request

```bash
curl '<url>'
```

## Example Response

```json
{}
```

## Errors And Status Codes

## Callers
"""


def telecom_api_template() -> str:
    return """---
title: Telecom Interfaces
type: api
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - telecom
  - sip
  - diameter
  - rtp
  - tmsg
  - api
---

# Telecom Interfaces

## Protocol Profile

| Protocol | Interface Type | Transport | Default Ports | Notes |
| --- | --- | --- | --- | --- |

## Surface

| Interface | Operation | Handler | Purpose |
| --- | --- | --- | --- |

## IDL Source

| Source | Path Or Link | Notes |
| --- | --- | --- |

## Endpoint Reference

### Interface Or Message Name

| Field | Source | Required | Type | Description |
| --- | --- | --- | --- | --- |

## Protocol-Specific Fields

### SIP Headers

| Header | Source | Required | Validation | Notes |
| --- | --- | --- | --- | --- |

### Diameter AVPs

| AVP | Code | Source | Required | Notes |
| --- | --- | --- | --- | --- |

### RTP/RTCP Attributes

| Attribute | Source | Required | Runtime Use | Notes |
| --- | --- | --- | --- | --- |

### tMsg Envelope

| Field | Source | Required | Delivery Impact | Notes |
| --- | --- | --- | --- | --- |

## Example Request

```text
# SIP example
INVITE sip:user@example.com SIP/2.0
Call-ID: <call-id>
```

```text
# Diameter example (textual form)
Command-Code: <code>
AVP: <name>=<value>
```

```text
# RTP/RTCP example
ssrc=<ssrc> payloadType=<pt>
```

```text
# tMsg example
topic: <topic>
correlationId: <id>
payload: <json-or-binary>
```

## Example Response

```json
{}
```

## Errors And Status Codes

| Protocol | Error/Status | Meaning | Typical Root Cause |
| --- | --- | --- | --- |

## Callers And Peers
"""


def config_cache_template() -> str:
    return """---
title: Config And Cache Runtime
type: component
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - config
  - cache
---

# Config And Cache Runtime

## Responsibility

## Config Sources

| Config | Source | Reader | Runtime Impact |
| --- | --- | --- | --- |

## JSON Shapes

```json
{}
```

## Defaults

| Config | Default | Source | Notes |
| --- | --- | --- | --- |

## Runtime Impact

## Cache Keys And TTL

| Cache | Key Shape | TTL | Invalidation |
| --- | --- | --- | --- |

## Test Or Lane Behavior

## Failure Modes
"""


def external_dependencies_template() -> str:
    return """---
title: External Dependencies And Failure Impact
type: component
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - external-dependencies
  - dependencies
---

# External Dependencies And Failure Impact

## Responsibility

This page centrally documents external services, config centers, caches, message queues, object storage, metrics, and shared libraries accessed by the current repository, plus failure propagation and user-visible impact within this service.

## Dependency Matrix

| Dependency | Kind | Protocol | Peer Or Broker | Client/Source Files | Hard Or Degradable | Timeout/Error Handling | User-Visible Impact |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Telecom Protocol Coverage

| Protocol | Role | Key Config | Failure Signal | Fallback |
| --- | --- | --- | --- | --- |

- SIP: proxy/registrar/media-edge dependencies.
- Diameter: peer realm/application-id dependencies.
- RTP: media relay/mixer/transcoder dependencies.
- tMsg: broker/topic/subscription dependencies.

## Failure Impact

## Fallbacks And Degradation

## Logs And Metrics

## Owners And Escalation

## Change Notes
"""


def auth_identity_template() -> str:
    return """---
title: Auth And Identity Flow
type: flow
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - auth
  - identity
---

# Auth And Identity Flow

## Entry Points

## Middleware Or Handler Sequence

## Identity Sources

| Source | Field/Context | Used By | Failure Signal |
| --- | --- | --- | --- |

## Tenant And Partner Resolution

## Token Or User Resolution

## Region Or Runtime Context

## Failure Modes

## Verification Notes
"""


def business_flows_template() -> str:
    return """---
title: Business Flow Index
type: flow
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - business-flow
---

# Business Flow Index

This page organizes flows by business questions rather than only by code modules. The goal is for the wiki to explain how a specific request, field, state, or policy works in business terms.

## Business Context

| Business Question | Flow Page | Main Entry | Runtime Evidence |
| --- | --- | --- | --- |

## Core Flows

| Flow | Entry Point | Main Components | Downstream Dependencies | State Side Effects |
| --- | --- | --- | --- | --- |

## Field Hotspots

| Field Or State | Why It Matters | Source | Downstream Use | Details |
| --- | --- | --- | --- | --- |

## Runtime Observability

| Flow | Metrics | Logs | Alerts | Dashboard |
| --- | --- | --- | --- | --- |

## Open Questions
"""


def field_propagation_template() -> str:
    return """---
title: Field Propagation Matrix
type: flow
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - field-propagation
---

# Field Propagation Matrix

This page is organized by key fields and explains propagation paths from entry points to downstream dependencies, cache, events, and responses.

## Scope

Describe covered interfaces, RPCs, events, cache paths, telecom protocols (SIP/Diameter/RTP), internal message interfaces (tMsg), or business flows.

## Field Matrix

| Field | Source | Validation Or Mapping | Internal Object | Downstream | Runtime Use | Missing Or Error Behavior |
| --- | --- | --- | --- | --- | --- | --- |

## Telecom Protocol Field Matrix

| Protocol | Field | Source | Mapping | Downstream Use | Runtime Check |
| --- | --- | --- | --- | --- | --- |

- SIP examples: Call-ID, From/To tags, Via, CSeq, SDP attributes.
- Diameter examples: Session-Id, Origin-Host, Destination-Realm, Result-Code, AVPs.
- RTP examples: SSRC, payload type, sequence number, timestamp, RTCP stats.
- tMsg examples: message type, correlation id, tenant id, retry count.

## Downstream Request Mapping

| Downstream | Request Builder | Source Fields | Renamed Fields | Dropped Or Defaulted Fields | Evidence |
| --- | --- | --- | --- | --- | --- |

Include protocol-to-protocol mapping when applicable, such as SIP header to tMsg field or Diameter AVP to internal RPC field.

## Config And Defaults

| Field | Config | Default | Runtime Impact |
| --- | --- | --- | --- |

## Observability

| Field Or Stage | Metric | Log Pattern | Dashboard/Alert | How To Check |
| --- | --- | --- | --- | --- |

## Open Questions
"""


def runtime_observability_template() -> str:
    return """---
title: Runtime Observability
type: flow
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - runtime
  - observability
---

# Runtime Observability

This page connects business flows with metrics, logs, alerts, dashboards, and request IDs to explain production behavior and support troubleshooting.

## Business Context

| Flow Or Feature | Why It Matters | Primary Symptoms |
| --- | --- | --- |

## Runtime Signals

| Signal | Metric/Log/Alert | Source | Tags Or Fields | Meaning |
| --- | --- | --- | --- | --- |

## Request Correlation

| Identifier | Source | Propagates To | How To Search |
| --- | --- | --- | --- |

## Flow To Signal Map

| Flow Stage | Expected Metric | Key Logs | Failure Signal | First Check |
| --- | --- | --- | --- | --- |

## Dashboards And Alerts

| Dashboard/Alert | Scope | Owner | Link Or Source |
| --- | --- | --- | --- |

## Open Questions
"""


def runbook_template() -> str:
    return """---
title: Request Troubleshooting Runbook
type: runbook
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - runbook
  - troubleshooting
---

# Request Troubleshooting Runbook

## Symptoms

## Owners

If owner information cannot be confirmed from the repository, record it in `questions/operations-metadata.md` and do not guess.

## Fast Checks

## Metrics Dashboards

## Alerts

## Common Error Logs

## Identity Sources

| Source | Field/Context | Fast Check | Failure Signal |
| --- | --- | --- | --- |

## Defaults

## Runtime Impact

## Mitigations

## Escalation
"""


def idl_question_template() -> str:
    return """---
title: IDL Source Location
type: question
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - idl
  - contract
---

# IDL Source Location

## Question

Where is the source IDL/source contract for the current repository maintained, what is the generation workflow, and which generated files must stay aligned with it?

## Search Evidence

| Checked Path Or Command | Result | Notes |
| --- | --- | --- |

## Current Best Answer

## Next Checks
"""


def operations_question_template() -> str:
    return """---
title: Operations Metadata Sources
type: question
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - operations
  - runtime
---

# Operations Metadata Sources

## Question

Where should service owner, oncall group, metrics dashboard, alert names, log retrieval entry points, and common error samples be confirmed?

## Search Evidence

| Checked Source | Result | Notes |
| --- | --- | --- |

## Confirmed Runtime Metadata

| Item | Value | Source |
| --- | --- | --- |

## Next Checks
"""


def system_index_template() -> str:
    return """# System Wiki

Use this page as the entry point for a cross-repository microservice knowledge base.

## Core Maps

- [Service Catalog](service-catalog.md)
- [Dependency Graph](dependency-graph.md)
- [Maintenance Log](log.md)

## Knowledge Areas

- `repos/`: summary and local wiki links for each repository.
- `contracts/`: cross-service contracts, IDL/source contracts, producer/consumer mappings.
- `request-flows/`: end-to-end request chains.
- `field-flows/`: key cross-service field propagation.
- `runbooks/`: cross-service troubleshooting manuals.
- `questions/`: cross-repo information that cannot yet be confirmed.
"""


def service_catalog_template() -> str:
    return """# Service Catalog

| Service | Repo | Role | Owner | Protocols Supported | Wiki | Runtime |
| --- | --- | --- | --- | --- | --- | --- |
"""


def dependency_graph_template() -> str:
    return """# Dependency Graph

| Upstream | Downstream | Protocol | Contract | Failure Impact |
| --- | --- | --- | --- | --- |

```mermaid
graph TD
  Pending["Service dependencies pending confirmation from source code, IDL, and runtime evidence"]
```
"""


def repo_name_from_source(source: str) -> str:
    cleaned = source.rstrip("/")
    if "://" in cleaned:
        path = urlparse(cleaned).path.rstrip("/")
        name = Path(path).name
    else:
        name = Path(cleaned).name
    if name.endswith(".git"):
        name = name[:-4]
    return name.replace(" ", "-")


def source_type(source: str) -> str:
    return "git" if "://" in source or source.startswith("git@") else "local"


def sources_yaml_template(sources: list[str]) -> str:
    lines = [
        "# Input repository list. source_type supports git or local.",
        "repos:",
    ]
    for source in sources:
        name = repo_name_from_source(source)
        kind = source_type(source)
        lines.extend(
            [
                f"  - name: {name}",
                f"    source_type: {kind}",
            ]
        )
        if kind == "git":
            lines.append(f"    url: {source}")
            lines.append("    branch: master")
        else:
            lines.append(f"    path: {source}")
        lines.extend(
            [
                "    role: pending-confirmation",
                "    owner: pending-confirmation",
                "    scan_mode: source_and_wiki",
            ]
        )
    return "\n".join(lines) + "\n"


def init_repo_wiki(repo_root: Path, wiki_path: str, mode: str) -> tuple[Path, list[str]]:
    wiki_dir = repo_root / wiki_path
    created = []

    directories = SYSTEM_DIRECTORIES if mode == "system" else REPO_DIRECTORIES
    for directory in directories:
        path = wiki_dir / directory
        path.mkdir(parents=True, exist_ok=True)
        created.append(path.relative_to(repo_root).as_posix() + "/")

    if mode == "system":
        files = {
            "index.md": system_index_template(),
            "service-catalog.md": service_catalog_template(),
            "dependency-graph.md": dependency_graph_template(),
            "log.md": log_template(),
        }
    else:
        files = {
            "index.md": index_template(),
            "SCHEMA.md": schema_template(),
            "overview.md": overview_template(),
            "log.md": log_template(),
            "source-map.md": source_map_template(),
            "apis/http-endpoints.md": api_template(),
            "apis/telecom-interfaces.md": telecom_api_template(),
            "components/config-and-cache.md": config_cache_template(),
            "components/external-dependencies.md": external_dependencies_template(),
            "flows/auth-and-identity.md": auth_identity_template(),
            "flows/business-flows.md": business_flows_template(),
            "flows/field-propagation.md": field_propagation_template(),
            "flows/runtime-observability.md": runtime_observability_template(),
            "runbooks/request-troubleshooting.md": runbook_template(),
            "questions/idl-source-location.md": idl_question_template(),
            "questions/operations-metadata.md": operations_question_template(),
        }

    for name, content in files.items():
        path = wiki_dir / name
        if write_if_missing(path, content):
            created.append(path.relative_to(repo_root).as_posix())

    return wiki_dir, created


def init_knowledge_repo(repo_root: Path, sources: list[str]) -> tuple[Path, list[str]]:
    created = []
    write_if_missing(repo_root / "sources.yaml", sources_yaml_template(sources))
    created.append("sources.yaml")

    for source in sources:
        name = repo_name_from_source(source)
        wiki_dir, child_created = init_repo_wiki(repo_root / "repos" / name, "wiki", "repo")
        created.extend([f"repos/{name}/{item}" for item in child_created])

    system_dir, system_created = init_repo_wiki(repo_root / "system", "wiki", "system")
    created.extend([f"system/{item}" for item in system_created])
    return system_dir, created


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a repository wiki, system wiki, or knowledge repo.")
    parser.add_argument("repo_root", nargs="?", default=".", help="Repository root directory")
    parser.add_argument("--mode", choices=["repo", "system", "knowledge"], default="repo", help="Wiki mode to initialize")
    parser.add_argument("--wiki-path", help="Wiki path relative to repo root")
    parser.add_argument("--repo", action="append", default=[], help="Input repo git URL or absolute local path for knowledge mode")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    repo_root.mkdir(parents=True, exist_ok=True)
    if args.mode == "knowledge":
        wiki_dir, created = init_knowledge_repo(repo_root, args.repo)
    else:
        wiki_path = args.wiki_path or ("system-wiki" if args.mode == "system" else "wiki")
        wiki_dir, created = init_repo_wiki(repo_root, wiki_path, args.mode)

    print(f"repo wiki: {wiki_dir}")
    print(f"created or confirmed {len(created)} path(s)")
    for item in created:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
