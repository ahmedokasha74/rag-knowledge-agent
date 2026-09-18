# Cloudify Onboarding Guide

## Overview

This guide explains how a new customer sets up a Cloudify account, configures the environment, and begins using Cloudify services. Cloudify supports three plans—Starter, Professional, and Enterprise—and each plan follows a slightly different onboarding path. The onboarding flow is designed to minimize time to value while ensuring security, billing, and access management are correct from the first day.

Use this document alongside [account_management.md](account_management.md), [subscription_policy.md](subscription_policy.md), [billing_guide.md](billing_guide.md), and [support_policy.md](support_policy.md).

## 1. Pre-implementation checklist

Before the customer receives access, Cloudify verifies the following:

- A valid company profile and billing contact.
- An account owner and at least one administrator user.
- A primary plan selection: Starter, Professional, or Enterprise.
- Payment method and invoice preferences.
- Security requirements, including MFA setup and SSO if applicable.
- Project naming conventions and environment scope (production, staging, development).

## 2. Account creation

The account owner completes the following flow:

1. Create the organizational account.
2. Confirm the account email and billing contact.
3. Select the plan.
4. Add a payment method and review the billing schedule.
5. Complete the security setup, including MFA and user invitations.
6. Review the accepted policies, including [privacy_policy.md](privacy_policy.md), [acceptable_use_policy.md](acceptable_use_policy.md), and [subscription_policy.md](subscription_policy.md).

### Provisioning timeline

- Starter: access is usually provisioned within 1 business day.
- Professional: provisioned within 1 business day after verification and payment approval.
- Enterprise: provisioned within 3 business days after legal review, security questionnaire, and contract signature.

## 3. Role setup and access management

Cloudify recommends that each organization designate:

- An account owner for billing and legal inquiries.
- One or more administrators for platform configuration and permissions.
- Developers or operations users assigned to the appropriate project roles.

The account owner must ensure all users are configured according to [account_management.md](account_management.md). Cloudify requires MFA for all administrative roles and strongly recommends it for all users with production access.

## 4. Workspace and environment setup

After the account is active, the customer can create one or more workspaces. Cloudify supports the following environment model:

- Development: non-production validation and engineering use.
- Staging: pre-production validation before release.
- Production: live workloads and customer-facing systems.

### Starter

- Up to 3 projects.
- 1 production environment.
- Limited project access controls.

### Professional

- Up to 20 projects.
- 5 environments and faster operational support.
- Role-based controls across multiple teams.

### Enterprise

- Custom project limits tied to contract.
- Multiple production environments with dedicated project segmentation.
- Advanced SSO, compliance controls, and support escalation.

## 5. First deployment checklist

New customers are encouraged to complete the following before going live:

1. Configure environment budgets and alert thresholds.
2. Add administrators and developer users.
3. Create network policies and secret management workflows.
4. Connect Cloudify to the customer’s cloud provider accounts and required integrations.
5. Define support contacts and escalation routing.
6. Review the applicable SLA and incident procedures.

## 6. Support and assistance

Cloudify offers support according to the customer plan. For information on response times and escalation, see [support_policy.md](support_policy.md). Customers should open a support ticket if:

- The environment is not functioning as expected.
- A service degradation or outage is impacting business operations.
- A configuration change is required to restore service.
- A security issue or suspicious access pattern needs investigation.

## 7. Billing and plan activation

Billing starts when the account is activated and access is granted. Charges are billed according to the selected plan in [billing_guide.md](billing_guide.md). Monthly and annual billing rules are available in [subscription_policy.md](subscription_policy.md) and [refund_policy.md](refund_policy.md).

## 8. Onboarding completion

Cloudify considers onboarding complete after the following milestones are met:

- Account owner and administrators are active.
- MFA and access policies are enabled.
- A production environment is configured, if applicable.
- Billing is active and supported by a payment method.
- Support path and escalation contacts are established.

This onboarding standard applies equally to all three subscription tiers but with different support and administrative expectations based on plan level.

## Related documents

- [account_management.md](account_management.md)
- [subscription_policy.md](subscription_policy.md)
- [billing_guide.md](billing_guide.md)
- [support_policy.md](support_policy.md)
- [security_policy.md](security_policy.md)
