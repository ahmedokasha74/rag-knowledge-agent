# Cloudify API Usage Policy

## Overview

This API Usage Policy defines the rules for using Cloudify’s APIs and related automation interfaces. It applies to all Cloudify customers across Starter, Professional, and Enterprise plans and is designed to protect platform stability, service quality, and security boundaries.

This document must be read together with [acceptable_use_policy.md](acceptable_use_policy.md), [security_policy.md](security_policy.md), [subscription_policy.md](subscription_policy.md), and [support_policy.md](support_policy.md).

## 1. API access model

Customers may access the Cloudify API using:

- User-issued API keys.
- Service-level credentials for automation workflows.
- Short-lived tokens when the platform or integration supports them.

All API credentials are linked to a user or service account and must be stored securely. API tokens must be rotated according to the account’s security settings and the rule set in [security_policy.md](security_policy.md).

## 2. Rate limits and quotas

Cloudify applies usage limits based on plan type. Rate limits are enforced to protect service reliability and fair usage across customers.

| Plan | Request limit | Burst capacity | Additional notes |
| --- | --- | --- | --- |
| Starter | 1,000 requests/minute | 2x burst for short intervals | Intended for development and light usage |
| Professional | 5,000 requests/minute | 3x burst for short intervals | Suitable for operational workloads |
| Enterprise | 25,000 requests/minute plus negotiated custom limits | 4x burst with approval | Custom limits may be negotiated in the contract |

### Important notes

- Rate limits apply per API key or service account.
- Cloudify may temporarily reduce throughput during service degradation or abuse investigation.
- Customers with sustained high usage may be required to move to a larger plan or a contract-specific arrangement.

## 3. Acceptable API use

Customers may use the API to:

- Manage infrastructure and deployment actions.
- Retrieve operational metrics and environment status.
- Automate provisioning, rollback, or health checks.
- Integrate with approved tooling and internal developer workflows.

Customers may not use the API to:

- Circumvent rate limits, quotas, or account controls.
- Generate abusive traffic, data exfiltration, or spam.
- Scrape or enumerate unrelated customer environments.
- Perform high-volume scanning or brute force activity.
- Exploit authentication weaknesses or insecure secret handling.

## 4. Security requirements

API users must:

- Store credentials in a secure secret manager or environment variable store.
- Restrict keys to the minimum necessary permissions.
- Revoke keys when no longer required.
- Use only approved endpoints and avoid sharing credentials across teams or external parties.

Security events involving API abuse, data leakage, or suspicious activity are handled under [security_policy.md](security_policy.md) and [incident_response.md](incident_response.md).

## 5. Abuse detection and enforcement

Cloudify monitors API activity for abnormal patterns, including spikes, excessive requests, unauthorized access attempts, suspicious credential reuse, and compromised tokens. Where abuse or misuse is detected, Cloudify may:

- Temporarily throttle requests.
- Disable API permissions.
- Suspend the relevant user or account.
- Require remediation before service is restored.

## 6. Enterprise API features

Enterprise customers may be eligible for:

- Customized rate limits or quotas.
- Dedicated service accounts and governance controls.
- Higher burst allowances subject to contract review.
- Expanded observability and audit access.

These features are subject to the signed enterprise agreement and security review under [enterprise_plan.md](enterprise_plan.md).

## 7. API support

Cloudify provides support for API issues according to [support_policy.md](support_policy.md). For account or billing questions tied to API usage overages or plan limits, customers should contact the Cloudify billing or admin team. For security abuse or credentials compromise, customers should escalate through Cloudify security or support channels immediately.

## Related documents

- [acceptable_use_policy.md](acceptable_use_policy.md)
- [security_policy.md](security_policy.md)
- [subscription_policy.md](subscription_policy.md)
- [support_policy.md](support_policy.md)
- [enterprise_plan.md](enterprise_plan.md)
