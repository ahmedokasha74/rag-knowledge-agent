# Cloudify Data Retention Policy

## Overview

This Data Retention Policy describes how Cloudify stores, archives, and deletes customer and operational data for the Starter, Professional, and Enterprise plans. Cloudify retains data only for as long as necessary to provide the service, comply with legal and regulatory requirements, maintain operational continuity, and support customer account and billing obligations.

This policy should be read alongside [privacy_policy.md](privacy_policy.md), [security_policy.md](security_policy.md), [account_management.md](account_management.md), and [subscription_policy.md](subscription_policy.md).

## 1. Retention principles

Cloudify follows these principles for data handling:

- Data is stored only for approved service, legal, or contractual purposes.
- Retention is tied to a documented business purpose.
- Backups and logs are retained for a limited period and then rotated or deleted.
- Enterprise customers may have longer retention windows under contract.
- Customers may request deletion of data where allowed by law and contract, subject to retention exceptions.

## 2. Data categories and retention windows

| Data category | Starter | Professional | Enterprise |
| --- | --- | --- | --- |
| Billing records | 7 years | 7 years | 7 years or contract term + 7 years |
| Support tickets and case notes | 3 years | 3 years | 5 years |
| Product telemetry and logs | 90 days | 180 days | 1 year or contract-defined |
| Backups | 30 days | 30 days | 30-90 days depending on agreement |
| Security event records | 1 year | 1 year | 2 years or contract-specified |
| Customer account and admin data | Duration of service + 30 days post-close | Duration of service + 30 days post-close | Duration of service + 90 days post-close |

## 3. Exceptions and legal hold

Cloudify may retain data longer than the standard period when required by:

- Legal process or investigation.
- Tax, accounting, or fraud review obligations.
- Security incident analysis and remediation.
- Contractual or negotiation obligations.

When an exception applies, Cloudify marks the data as subject to legal hold and logs the reason for extended retention. Legal hold and retention exceptions are reviewed periodically by Cloudify compliance and security teams.

## 4. Deletion and archival

Customers may request deletion or export of their account data according to [privacy_policy.md](privacy_policy.md) and [account_management.md](account_management.md). Cloudify may delete or archive data as follows:

- Active records are removed when no longer required.
- Logs are rotated according to the retention schedule.
- Backups are restored only for recovery operations and deleted according to the standard backup schedule.
- Customer data is removed from active systems within 30 days of account closure unless a legal or contractual exception applies.

## 5. Enterprise retention and audit support

Enterprise customers may request additional retention or audit support through their contract. Cloudify may store higher volumes of telemetry and support records for Enterprises when required for production assurance, compliance review, or security investigations.

## 6. Customer responsibilities

Customers are responsible for:

- Providing accurate account and billing data.
- Managing their own data classification and retention requirements in their internal systems.
- Reviewing whether their workloads require longer retention periods than the standard defaults.

## Related documents

- [privacy_policy.md](privacy_policy.md)
- [security_policy.md](security_policy.md)
- [account_management.md](account_management.md)
- [subscription_policy.md](subscription_policy.md)
- [enterprise_plan.md](enterprise_plan.md)
