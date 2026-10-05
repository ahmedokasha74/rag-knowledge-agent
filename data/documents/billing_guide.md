# Cloudify Billing Guide

## Overview

This guide explains how Cloudify charges for services, handles invoices, processes changes in plan tiers, and manages account billing across the Starter, Professional, and Enterprise plans. The guide is intended for account owners, administrators, and finance-related contacts.

This guide should be read with [subscription_policy.md](subscription_policy.md), [refund_policy.md](refund_policy.md), [account_management.md](account_management.md), and [enterprise_plan.md](enterprise_plan.md).

## 1. Billing model

Cloudify offers both monthly and annual billing for the Starter and Professional plans. Enterprise plans are generally annual and contract-based, with the billing schedule specified in the customer agreement.

### Billing phases

- Initial activation billing.
- Recurring monthly or annual billing.
- Overage and usage charges, if applicable.
- Adjustments for plan changes or prorations.
- Credits and service credits applied to future invoices.

## 2. Invoice schedule

Invoices are issued in the following cadence:

- Starter monthly: billed on the first day of each month.
- Professional monthly: billed on the first day of each month.
- Starter annual: billed once annually at activation, then renewed annually.
- Professional annual: billed once annually at activation, then renewed annually.
- Enterprise annual: billed according to the negotiated contract schedule.

Customers receive invoices by email and in the Cloudify billing portal. Invoices remain accessible for 7 years under [data_retention.md](data_retention.md) and [privacy_policy.md](privacy_policy.md).

## 3. Payment terms

Cloudify accepts payment by credit card or approved invoicing arrangements. Payment is due according to the billing schedule. If a payment fails, Cloudify attempts a retry request and may temporarily restrict access to production features until the payment issue is resolved.

### Delinquency policy

If an invoice remains unpaid beyond the grace period:

- Access to paid features may be limited or suspended.
- Support services may be restricted to billing and account issues only.
- Renewal may be delayed until the account is brought current.
- Cloudify may pursue collections or chargeback remedies if the account remains overdue.

## 4. Plan changes and proration

Customers may upgrade or downgrade plans at any time. The following rules apply:

- Upgrades are prorated from the date of change.
- Downgrades receive a credit for the unused portion of the current cycle, applied to the next invoice rather than as cash.
- Annual changes may take effect at the next renewal date unless otherwise specified in the contract.

### Examples

- A Professional customer upgrades to Enterprise midway through the month. The enterprise charge is prorated from the upgrade date.
- A Starter customer downgrades to a lower tier during a monthly cycle. The reduction is applied as account credit on the next invoice.

## 5. Service credits and account credits

Cloudify may apply service credits under [sla.md](sla.md) and account credits for downgraded plans or promo adjustments. Credits are applied as invoice reductions and do not grant a cash refund unless a refund is approved under [refund_policy.md](refund_policy.md).

## 6. Refunds and billing disputes

Refund eligibility is governed by [refund_policy.md](refund_policy.md). Refund requests related to billing disputes are reviewed by the Cloudify finance team and may require confirmation of account ownership and invoice status. Disputes should be raised before a chargeback is initiated to allow Cloudify to resolve the issue internally.

## 7. Enterprise billing

Enterprise customers have negotiated billing arrangements, including contract pricing, annual commitments, and custom service add-ons. Price adjustments may occur only under the terms of the signed agreement. Enterprise customers may receive a separate billing contact and an invoice approval workflow.

## 8. Account ownership and invoice authority

Only account owners or authorized administrators can change billing methods, submit plan changes, or request invoice adjustments. Cloudify may require additional validation for changes involving high-value contracts or account ownership transfers.

## 9. Tax and compliance

Cloudify may apply taxes, VAT, or other legal obligations according to the customer’s billing address and regional tax rules. Customers are responsible for providing accurate legal entity and tax information for invoicing and compliance purposes.

## Related documents

- [subscription_policy.md](subscription_policy.md)
- [refund_policy.md](refund_policy.md)
- [account_management.md](account_management.md)
- [enterprise_plan.md](enterprise_plan.md)
- [data_retention.md](data_retention.md)
