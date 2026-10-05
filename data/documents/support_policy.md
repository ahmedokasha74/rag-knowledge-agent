# Cloudify Support Policy

## Overview

This policy explains the types of support available to Cloudify customers, response time expectations, escalation procedures, and support entitlements for the Starter, Professional, and Enterprise plans. Cloudify provides support through a ticketing workflow and direct operational channels for critical issues.

This document should be read with [sla.md](sla.md), [incident_response.md](incident_response.md), [enterprise_plan.md](enterprise_plan.md), and [account_management.md](account_management.md).

## 1. Support channels

Support is available through:

- Customer support portal.
- Email support for account and billing issues.
- Live escalation channels for Enterprise customers and urgent production incidents.

### Severity definitions

Cloudify classifies issues as follows:

- Severity 1: critical outage or complete service unavailability affecting production workloads.
- Severity 2: major degradation that materially affects functionality or customer operations.
- Severity 3: moderate issue with functional impact but workaround available.
- Severity 4: low-impact issue, feature question, or minor bug.

## 2. Response time commitments

Cloudify’s support response commitments by plan are as follows:

| Plan | Business hours | Response target | Escalation availability |
| --- | --- | --- | --- |
| Starter | 9:00-17:00 local business hours, Monday-Friday | 8 business hours for Severity 3/4; 1 business day for billing issues | Standard ticketing only |
| Professional | 24x7 for Severity 1; business hours for other severities | 30 minutes for Severity 1; 4 business hours for Severity 2; 1 business day for Severity 3/4 | High-priority ticketing |
| Enterprise | 24x7 for all severities | 15 minutes for Severity 1; 1 hour for Severity 2; 4 business hours for Severity 3; 1 business day for Severity 4 | Priority support plus named contact |

### Important notes

- Response times are measured from the time Cloudify receives or confirms the issue.
- For Enterprise contracts, a designated technical contact may request direct escalation for incidents affecting a production environment.
- Cloudify may assign a workaround or mitigation before a full resolution when a fix is not immediately available.

## 3. Service availability and issue handling

Support workflows are coordinated with the product and operations teams to ensure that service-impacting issues are routed to the correct owner under [incident_response.md](incident_response.md). Severity 1 and Severity 2 issues may require immediate engineering action, customer communication, and temporary mitigation if the underlying issue is not yet resolved.

## 4. Support exclusions

Cloudify does not provide support for:

- Unsupported third-party services connected to a customer workspace.
- Customer code defects that are outside Cloudify’s platform responsibilities.
- Support requests lacking valid customer identifiers or contact details.
- Use cases that violate the [acceptable_use_policy.md](acceptable_use_policy.md).
- Requests outside the subscription’s support scope.

## 5. Enterprise support arrangements

Enterprise customers receive:

- 24x7 support coverage.
- Named support contacts and an executive escalation route.
- Priority incident triage with faster acknowledgement and technical review.
- Access to account reviews, operational planning, and risk communication under [sla.md](sla.md).

Enterprise support may include proactive review of usage, deployment health, and security posture where the contract includes managed operations or advisory services.

## 6. Support request procedure

Customers should open a support ticket through the Cloudify portal including:

- Account and workspace identifiers.
- Environment type (production, staging, or dev).
- Severity classification and business impact.
- Relevant timestamps and issue symptoms.
- Steps taken to isolate or mitigate the issue.

Cloudify may request additional evidence, screenshots, logs, or configuration details for troubleshooting. Customers must cooperate with Cloudify support and provide any information needed to assess materially significant service issues.

## 7. Billing and account support

Billing and account support are available to all customers, with standard response times for invoice disputes, payment failures, changes to plan settings, or administrative access issues. Refund and billing issues may also be reviewed under [refund_policy.md](refund_policy.md) and [billing_guide.md](billing_guide.md).

## 8. Customer obligations

Customers are expected to:

- Notify Cloudify promptly of outages or customer-facing incidents.
- Maintain accurate administrative contacts and escalation persons.
- Provide issue details and relevant telemetry when requested.
- Avoid contacting multiple support channels for the same incident without informing Cloudify.

## Related documents

- [sla.md](sla.md)
- [incident_response.md](incident_response.md)
- [enterprise_plan.md](enterprise_plan.md)
- [account_management.md](account_management.md)
- [billing_guide.md](billing_guide.md)
