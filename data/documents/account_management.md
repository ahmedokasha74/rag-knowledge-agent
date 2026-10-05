# Cloudify Account Management Policy

## Overview

This policy defines how Cloudify customer accounts are created, administered, updated, and terminated. It covers account ownership, user roles, administrative access, billing contact change management, and escalation for account security concerns.

This policy relates to [onboarding_guide.md](onboarding_guide.md), [subscription_policy.md](subscription_policy.md), [billing_guide.md](billing_guide.md), [privacy_policy.md](privacy_policy.md), and [support_policy.md](support_policy.md).

## 1. Account ownership

Each Cloudify organization has an account owner, who is the primary contact for:

- Billing and invoicing.
- Contract and plan changes.
- Security escalation and account verification.
- Legal and administrative notices.

The account owner must maintain a valid email address and secure authentication method. Cloudify may require re-verification for account changes involving payment details, billing status, or plan upgrades.

## 2. User and role model

Cloudify accounts may include multiple users with role-based access. Standard roles include:

- Account owner.
- Administrator.
- Developer.
- Read-only viewer.
- Support liaison.

### Access rules

- Account owners may manage billing, users, and plan changes.
- Administrators can manage project access and environment configuration.
- Developers may deploy and operate workloads within the environments assigned to them.
- Read-only users may view dashboards but cannot modify settings.
- Support liaison users may coordinate support cases but are not automatically granted technical or billing authority.

## 3. Invitation and onboarding process

New users are invited to an account by an existing administrator or account owner. Cloudify requires MFA for administrative accounts and recommended MFA for all users with production access. New users must accept the Cloudify terms and relevant policies before being granted access.

## 4. Change management for accounts

Customers are responsible for notifying Cloudify of:

- Changes to billing contact information.
- Ownership changes or legal entity updates.
- User additions or removals.
- Security incidents affecting account access.
- Changes to SSO, MFA, or identity configuration.

Cloudify may place a review hold when there is unusual account activity, such as sudden plan changes, payment disputes, or unauthorized user invites.

## 5. Billing and plan changes

Only account owners and authorized administrators may approve payment updates or change subscription tiers. A plan change may alter support entitlements, usage limits, and retention windows. Billing and plan decisions are governed by [subscription_policy.md](subscription_policy.md) and [billing_guide.md](billing_guide.md).

## 6. Suspension and termination

Cloudify may suspend or terminate an account if:

- The customer fails to pay fees according to the billing schedule.
- The account violates [acceptable_use_policy.md](acceptable_use_policy.md) or [security_policy.md](security_policy.md).
- There is fraud, account takeover, or suspected abuse.
- The customer materially breaches the agreement or an enterprise contract.

When an account is suspended or terminated, customer data is handled according to [data_retention.md](data_retention.md). Certain data may be retained for legal, tax, security, or contractual reasons even after the account is no longer active.

## 7. Support access and customer contact

Support cannot disclose details of the account to unauthorized users. Customers must establish a verified support identity before Cloudify will provide account-specific details, especially in cases involving code, security incidents, or billing disputes.

## 8. Enterprise-specific administration

Enterprise customers may have additional roles, custom user group mappings, and delegated administrative responsibilities. Their account structure may include domain-based SSO, a dedicated technical account manager, and broader support and audit review requirements.

## Related documents

- [onboarding_guide.md](onboarding_guide.md)
- [subscription_policy.md](subscription_policy.md)
- [billing_guide.md](billing_guide.md)
- [privacy_policy.md](privacy_policy.md)
- [support_policy.md](support_policy.md)
- [data_retention.md](data_retention.md)
