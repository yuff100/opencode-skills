---
title: API Name
type: api
status: draft
source_files: []
last_verified_commit: unknown
last_verified: YYYY-MM-DD
tags:
  - api
---

# API Name

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

## Identity Sources

| Source | Field/Context | Used By | Notes |
| --- | --- | --- | --- |

## Example Request

```bash
# HTTP example
curl '<url>'
```

```text
# SIP example
INVITE sip:user@example.com SIP/2.0
Call-ID: <call-id>
CSeq: 1 INVITE
```

```text
# Diameter example (textual form)
Command-Code: <code>
Application-Id: <app-id>
AVP: <name>=<value>
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

## Callers
