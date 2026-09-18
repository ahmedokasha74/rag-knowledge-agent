# Phase 0 — Knowledge Base Design

## Scope

This phase covers the completed knowledge-base portion of the Cloudify domain definition. It includes the fictional company model, business rules, policy documents, and the knowledge structure that a future retrieval-augmented generation system can use.

Database design and implementation are intentionally left for a later step and are not part of this phase.

## Domain definition

Cloudify is a fictional SaaS company that provides cloud infrastructure and developer operations services. It serves engineering organizations that need dependable infrastructure management, secure deployment workflows, and operational support across development, staging, and production environments.

## Cloudify business model

Cloudify offers three subscription plans:

1. Starter
   - Suitable for small teams and early deployments.
   - Includes standard support and a 99.5% monthly uptime commitment.

2. Professional
   - Suitable for growing engineering organizations.
   - Includes priority support and a 99.9% monthly uptime commitment.

3. Enterprise
   - Suitable for production-critical organizations.
   - Includes 24x7 support, enhanced governance, and a 99.95% monthly uptime commitment.

## Important business rules

The documentation set intentionally keeps these rules consistent across the knowledge base:

- All plans have a 14-day refund window for new subscriptions, subject to exceptions and policy violations.
- Annual subscriptions are generally non-refundable after the 14-day cooling-off period.
- Starter has a 99.5% uptime SLA.
- Professional has a 99.9% uptime SLA.
- Enterprise has a 99.95% uptime SLA.
- Enterprise customers receive priority support and 24x7 coverage.
- API rate limits differ by plan and are governed by the API Usage Policy.
- Data retention schedules differ by class and plan.
- Security, privacy, and support obligations are explicitly cross-linked across documents.

## Document inventory

The knowledge base includes these 14 documents:

- refund_policy.md
- privacy_policy.md
- security_policy.md
- sla.md
- onboarding_guide.md
- support_policy.md
- subscription_policy.md
- billing_guide.md
- acceptable_use_policy.md
- account_management.md
- enterprise_plan.md
- incident_response.md
- data_retention.md
- api_usage_policy.md

## Cross-document relationships

The knowledge base is intentionally interconnected. For example:

- refund_policy.md connects to subscription_policy.md and billing_guide.md.
- sla.md connects to enterprise_plan.md, support_policy.md, and incident_response.md.
- privacy_policy.md connects to data_retention.md and security_policy.md.
- api_usage_policy.md connects to acceptable_use_policy.md and security_policy.md.
- onboarding_guide.md connects to account_management.md and support_policy.md.

These relationships are designed so future questions can require reasoning across multiple documents, not just a single policy.

## Example future RAG questions

The knowledge base is designed to support queries such as:

- What is Cloudify’s refund policy for Enterprise customers?
- What uptime does the Enterprise plan guarantee?
- How long does Cloudify retain customer data?
- What support response time does an Enterprise customer receive?
- What happens if Cloudify experiences a service outage?
- Can a customer cancel an annual subscription and receive a refund?
- What are the API rate limits for Enterprise customers?
- What security requirements apply to API access?
- What compensation is available when SLA commitments are not met?

## Result

The completed Phase 0 knowledge base provides a realistic, internally consistent fictional business domain for future work. The next implementation phases can later connect this documentation to structured data and operational systems without changing the underlying Cloudify domain model.
