# Cloudify Incident Response Policy

## Overview

This Incident Response Policy describes how Cloudify identifies, triages, communicates, and resolves service incidents affecting the Cloudify platform. The policy applies to the Starter, Professional, and Enterprise plans and is designed to support operational continuity and transparent customer communication.

This document should be read together with [sla.md](sla.md), [support_policy.md](support_policy.md), [security_policy.md](security_policy.md), and [enterprise_plan.md](enterprise_plan.md).

## 1. Incident severity levels

Cloudify classifies incidents by severity as follows:

### Severity 1

- Complete or near-complete production outage affecting multiple customers or a customer’s critical production environment.
- Customer-facing functionality is unavailable or materially degraded.
- Response target: 15 minutes for Enterprise, 30 minutes for Professional, and 1 business day for Starter where the issue is a severe account-level event.

### Severity 2

- Major degradation in core functionality that impairs key workflows or customer operations.
- Response target: 1 hour for Enterprise, 4 business hours for Professional, and 1 business day for Starter.

### Severity 3

- Moderate issue with workaround available.
- Response target: 4 business hours for Enterprise and Professional; 1 business day for Starter.

### Severity 4

- Low-impact or informational issue without material customer impact.
- Response target: within 1 business day for all plans.

## 2. Detection and triage

Cloudify monitors service health through platform telemetry, uptime checks, and customer reports. Triage begins with confirmation of the issue, impact assessment, and ownership assignment. Where a security incident is suspected, the process escalates to Cloudify security leadership under [security_policy.md](security_policy.md).

## 3. Communications

During an incident, Cloudify will communicate updates to affected customers according to the issue severity and plan type. Enterprise customers receive more frequent updates and more direct communication. Communication requirements include:

- Initial acknowledgment.
- Status updates at defined intervals based on severity.
- Root cause summary once resolved.
- Preventive remediation actions where relevant.

## 4. Remediation and recovery targets

Cloudify aims to restore service according to the following expectations:

- Severity 1: restore service as quickly as possible, with emergency mitigation prioritized over normal change control.
- Severity 2: resolve within 4 hours where possible or provide mitigation within the same period.
- Severity 3: resolve within 5 business days or issue a workaround.
- Severity 4: resolve in the next normal operational cycle.

## 5. Service credit and compensation

If a production incident causes Cloudify to breach the SLA commitments in [sla.md](sla.md), affected customers may receive service credits according to the plan schedules. Enterprise customers may also be eligible for specific contractual remedies if stated in their agreement.

## 6. Customer responsibilities during an incident

During a Severity 1 or Severity 2 incident, customers are expected to:

- Provide support contact details and correct escalation points.
- Share relevant configuration changes or deployment events that may have caused the issue.
- Monitor their own application dependencies and internal communications.
- Work with Cloudify support on mitigations where the issue is related to customer-side configuration or misuse.

## 7. Security-related incidents

If an incident involves unauthorized access, malicious traffic, or a suspected platform compromise, Cloudify follows the investigation process defined in [security_policy.md](security_policy.md). Customers will be notified if the issue materially affects their data, services, or compliance posture.

## 8. Post-incident review

Cloudify conducts a post-incident review after material incidents. The review includes analysis of root cause, timeline, impact, remediation, and preventive action. Cloudify may document recurring issues for future service improvement or for customer-facing operational guidance.

## Related documents

- [sla.md](sla.md)
- [support_policy.md](support_policy.md)
- [security_policy.md](security_policy.md)
- [enterprise_plan.md](enterprise_plan.md)
- [data_retention.md](data_retention.md)
