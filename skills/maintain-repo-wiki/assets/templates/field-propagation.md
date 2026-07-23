---
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

This page is organized by key fields and explains propagation from entry points to downstream dependencies, cache, events, and responses.

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
