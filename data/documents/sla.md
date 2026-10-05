# Cloudify Service Level Agreement (SLA)

## Overview

This Service Level Agreement defines the uptime and service commitments for Cloudify customers on the Starter, Professional, and Enterprise subscription plans. The SLA applies to Cloudify’s hosted platform and core management services, including the Cloudify control plane and infrastructure orchestration functions.

This document should be read together with [enterprise_plan.md](enterprise_plan.md), [support_policy.md](support_policy.md), [incident_response.md](incident_response.md), and [refund_policy.md](refund_policy.md).

## 1. Service availability commitments

Cloudify commits to monthly uptime percentages as follows:

| Plan | Monthly uptime commitment | Service credit trigger |
| --- | --- | --- |
| Starter | 99.5% | 10% service credit if monthly uptime falls below 99.5% |
| Professional | 99.9% | 15% service credit if monthly uptime falls below 99.9% |
| Enterprise | 99.95% | 25% service credit for breach of 99.95%, plus 50% credit for breach below 99.9% |

### Definitions

- Monthly uptime is measured across the customer’s billing month.
- Availability is calculated on Cloudify-managed production services available to the customer and excludes scheduled maintenance windows, customer-caused outages, and known issues disclosed by the customer.
- Planned maintenance windows must be communicated at least 72 hours in advance, except for emergency security upgrades.

## 2. Service credit schedule

If Cloudify fails to meet the monthly availability commitment, customers may receive service credits according to the following schedule:

### Starter

- 10% credit if monthly uptime is below 99.5% but at or above 99.0%.
- 20% credit if uptime is below 99.0%.

### Professional

- 15% credit if monthly uptime is below 99.9% but at or above 99.5%.
- 30% credit if uptime is below 99.5%.

### Enterprise

- 25% credit if monthly uptime is below 99.95% but at or above 99.9%.
- 50% credit if uptime is below 99.9%.
- Additional credits may be applied if the agreed service commitment in the Enterprise Order Form is breached due to prolonged outage or a critical production service outage.

Service credits are applied to the next invoice for the relevant subscription period and may not be exchanged for cash unless explicitly stated in a negotiated Enterprise contract.

## 3. SLA exclusions

The SLA does not apply to:

- Customer-initiated downtime, configuration errors, or resource mis-sizing.
- Third-party provider outages outside Cloudify’s control.
- Feature previews, beta products, or pre-release functionality.
- Customer misuse, abuse, or intentional circumventing of Cloudify security controls.
- Outages caused by unsupported integrations or non-approved workloads.

## 4. Enterprise-specific service commitments

Enterprise customers receive enhanced operational commitments, including:

- 99.95% monthly uptime guarantee.
- 24x7 priority support under [support_policy.md](support_policy.md).
- Dedicated technical account management and monthly business review.
- A clear communication path for incident response and executive escalation.
- Expedited investigation of any production incident or service concern under [incident_response.md](incident_response.md).

Enterprise customers also receive the ability to request custom service commitments through their negotiated contract, which supersedes this general SLA wherever the terms conflict.

## 5. Incident response and ownership

Cloudify’s incident response process begins immediately when a production issue is detected. Severity levels are defined in [incident_response.md](incident_response.md). Critical incidents trigger engineering response, customer notification, and operational recovery. Customers are not required to request a credit to receive a service credit if the SLA thresholds are met; credits are calculated automatically based on platform telemetry and incident records.

## 6. Support and escalation path

Support response and severity handling are defined in [support_policy.md](support_policy.md). Customers who experience repeated SLA violations or prolonged unavailability may escalate through their assigned account representative or the Cloudify support escalation channel.

## 7. Service limits and exclusions

Cloudify may make maintenance windows outside a customer’s peak usage period when operationally necessary. Companies with Starter or Professional plans are expected to schedule non-critical changes during normal support windows. Enterprise customers may request advance notice windows that align to their operational needs in line with the contract and support policy.

## 8. Contractual relationship with subscriptions

This SLA forms part of the operating commitments for all plans. Refund requests are governed by [refund_policy.md](refund_policy.md), and plan entitlements are defined in [subscription_policy.md](subscription_policy.md). Where a plan states a different support level or availability commitment, the plan description controls for that customer’s account.

## Related documents

- [enterprise_plan.md](enterprise_plan.md)
- [support_policy.md](support_policy.md)
- [incident_response.md](incident_response.md)
- [refund_policy.md](refund_policy.md)
- [subscription_policy.md](subscription_policy.md)
