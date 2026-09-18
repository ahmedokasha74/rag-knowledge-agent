# Cloudify Subscription Policy

## Overview

This policy defines the subscription terms for Cloudify’s three plan tiers: Starter, Professional, and Enterprise. It covers plan features, billing cadence, plan changes, cancellations, and the relationship between plan entitlements and other Cloudify policies.

This document should be read together with [billing_guide.md](billing_guide.md), [refund_policy.md](refund_policy.md), [sla.md](sla.md), and [enterprise_plan.md](enterprise_plan.md).

## 1. Plan summary

| Plan | Ideal fit | Billing model | Support tier | SLA commitment |
| --- | --- | --- | --- | --- |
| Starter | Solo developers and small teams | Monthly or annual | Standard business-hours support | 99.5% uptime |
| Professional | Growing engineering organizations | Monthly or annual | Priority support | 99.9% uptime |
| Enterprise | Large organizations with production requirements | Annual, contract-based | 24x7 priority support | 99.95% uptime |

## 2. Product entitlements

### Starter

Starter is designed for early-stage customers and small teams. Features include:

- Up to 3 projects.
- One production environment.
- Basic monitoring and alerting.
- Standard business-hours support.
- API access subject to rate limits.
- Encryption, MFA, and secure default controls.

### Professional

Professional is designed for growing organizations that need higher operational visibility and more account flexibility. Features include:

- Up to 20 projects.
- Multiple environment tiers and role-based access controls.
- Enhanced observability and retention windows.
- Priority support and faster incident triage.
- Higher API rate limits than Starter.
- Advanced admin controls and user provisioning support.

### Enterprise

Enterprise is designed for medium and large organizations with strict production requirements. Features include:

- Contracted project and environment allocations based on customer needs.
- 24x7 support.
- 99.95% SLA commitment.
- Advanced security controls, SSO, and security review support.
- Expanded retention, audit access, and executive communication pathways.
- Custom API rate limits, governance, and dedicated onboarding.

## 3. Billing cadence

Cloudify bills subscriptions on either a monthly or annual basis depending on the plan and contract. Monthly plans renew automatically each billing cycle. Annual plans also renew automatically unless a valid cancellation notice is submitted before the renewal date.

### Monthly plans

- Billed in advance at the start of each month.
- Can be changed or canceled with effect at the next billing cycle.
- Upgrade charges are prorated as described in [billing_guide.md](billing_guide.md).

### Annual plans

- Billed annually in advance.
- Require a 14-day refund window from initial activation or first invoice date.
- Subject to the cancellation rules described in [refund_policy.md](refund_policy.md).

## 4. Plan changes and cancellations

Customers may change plans through the Cloudify account portal. A plan change may result in:

- Immediate access to higher-tier features when an upgrade is applied.
- Credit for the unused portion of a lower-tier subscription when a downgrade is processed, applied as account credit against future invoices.
- A new billing date or adjustment at the next renewal if the change occurs on an annual term.

Cancellation of a plan requires an account owner or authorized administrator to submit the request through the billing portal or support process. Cancellation does not immediately erase account data; retention follows [data_retention.md](data_retention.md).

## 5. Eligibility and contract terms

Customers must meet basic account criteria to sign up for a plan, including valid business identity, billing contact information, and authorization to use the service. Enterprise plans require a negotiated contract and may include custom operational, support, and security commitments not reflected in the general public documentation.

## 6. Policy and service relationship

This policy is connected to other operational policies:

- [billing_guide.md](billing_guide.md): detailed invoice and charge handling.
- [refund_policy.md](refund_policy.md): refund eligibility and process.
- [sla.md](sla.md): uptime commitments and service credits.
- [support_policy.md](support_policy.md): support commitments by plan.
- [enterprise_plan.md](enterprise_plan.md): enterprise-only terms and guarantees.

## Related documents

- [billing_guide.md](billing_guide.md)
- [refund_policy.md](refund_policy.md)
- [sla.md](sla.md)
- [enterprise_plan.md](enterprise_plan.md)
- [support_policy.md](support_policy.md)
