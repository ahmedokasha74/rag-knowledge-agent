# Cloudify Security Policy

## Overview

This Security Policy defines Cloudify’s security requirements, controls, and responsibilities for hosted infrastructure, customer data, and administrative access. It applies to all Cloudify environments and to all subscription plans, including Starter, Professional, and Enterprise. Cloudify’s security model is designed to balance secure operations with ease of onboarding and rapid customer support.

This policy should be read together with [privacy_policy.md](privacy_policy.md), [incident_response.md](incident_response.md), [api_usage_policy.md](api_usage_policy.md), and [enterprise_plan.md](enterprise_plan.md).

## 1. Security principles

Cloudify follows these operating principles:

- Secure by default for all accounts and environments.
- Least-privilege access for internal users and customer administrators.
- Encryption for data in transit and at rest.
- Multi-factor authentication (MFA) on all administrative access.
- Continuous logging and auditability for privileged actions.
- Timely detection and response to outages, abuse, and security incidents.

## 2. Tenant isolation and infrastructure controls

Cloudify segregates customer environments through service-level isolation and environment-specific access controls. Each customer account has a separate administrative boundary, and production workloads are isolated from one another using provider-side controls, role boundaries, and network segmentation policies.

### General controls

- Data is encrypted in transit using TLS 1.2 or later.
- Data at rest uses AES-256 encryption or equivalent provider-managed encryption at the storage layer.
- Operational system secrets are stored in managed secret stores and rotated regularly.
- Network security groups, firewall rules, and private routing apply to production services.

### Plan-specific controls

- Starter: encryption, MFA for account admins, and secure default environment controls.
- Professional: all Starter controls plus environment-level role separation and deeper operational logging.
- Enterprise: all Professional controls plus private networking options, enhanced identity integration, and customer-specific security review workflows.

## 3. Identity and access management

Cloudify requires MFA for all account owners and administrators. Users with billing, support, or technical administrative access must authenticate through an approved identity provider or through Cloudify’s platform identity controls.

### Access model

- Account owners can manage billing and invite users.
- Administrators can provision access, manage environments, and configure policies.
- Developers and operators may access only the projects and resources assigned to them.
- Support personnel may access customer data only when explicitly authorized for a support or incident case.

### Session and credential rules

- API keys are rotated at least every 365 days for customers unless otherwise required by contract.
- Temporary credentials expire automatically after a short TTL.
- Enterprise customers may use SSO and SCIM integrations where the contract requires them.
- Shared credentials are prohibited for production or administrative accounts.

## 4. API and integration security

Customer API access is governed by [api_usage_policy.md](api_usage_policy.md). Cloudify sets hard rate limits, validates API keys, and monitors abuse for automated misuse or suspicious behavior.

Additional API security requirements include:

- API tokens must be stored in secure secret management systems.
- Tokens must not be embedded in client-side code except where the application’s architecture explicitly requires them.
- Account owners must revoke any tokens that are no longer needed.
- Cloudify may disable tokens without notice if abuse or suspected compromise is detected.

## 5. Vulnerability management

Cloudify maintains a vulnerability management program that includes:

- Dependency scanning for platform and customer-facing software components.
- Patch prioritization based on asset criticality and exploitability.
- Quarterly review of infrastructure vulnerabilities and exposure remediation.
- Emergency patching for actively exploited critical vulnerabilities.

## 6. Incident, abuse, and escalation response

Security incidents are handled under [incident_response.md](incident_response.md). Cloudify classifies incidents by severity and follows prescribed communication, investigation, and remediation steps. Customer notifications are required for security events that materially affect customer data, product security, or service availability.

## 7. Customer responsibilities

Customers are responsible for:

- Managing user identities within their organization.
- Configuring least-privilege access for team members.
- Securing their own application secrets and internal developer workflows.
- Meeting the requirements for their selected plan and any contractual security commitments.

Cloudify does not guarantee the security of a customer environment where the customer has deliberately disabled controls, exposed secrets in public repositories, or bypassed the approved access model.

## 8. Compliance and auditability

Cloudify maintains logs for access, changes, and security-relevant events. Logs are retained according to the schedule in [data_retention.md](data_retention.md). Enterprise customers may request formal audit reports and higher assurance controls in accordance with their contract.

## 9. Security exceptions

Any temporary deviation from this policy requires written approval from Cloudify security leadership and explicit risk acceptance. Temporary exceptions must include an expiration date, compensating controls, and a remediation plan.

## 10. Enforcement

Failure to meet security requirements may result in warnings, account restrictions, temporary suspension, or termination under [acceptable_use_policy.md](acceptable_use_policy.md) and [subscription_policy.md](subscription_policy.md).

## Related documents

- [privacy_policy.md](privacy_policy.md)
- [incident_response.md](incident_response.md)
- [api_usage_policy.md](api_usage_policy.md)
- [acceptable_use_policy.md](acceptable_use_policy.md)
- [enterprise_plan.md](enterprise_plan.md)
