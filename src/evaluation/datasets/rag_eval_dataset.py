from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class EvaluationCase:
    user_input: str
    reference: str
    category: str


EVALUATION_CASES = [
    EvaluationCase(
        user_input="What plans does Cloudify offer?",
        reference=(
            "Cloudify offers Starter, Professional, and Enterprise plans."
        ),
        category="simple factual, graph-friendly",
    ),
    EvaluationCase(
        user_input="What is Cloudify?",
        reference=(
            "Cloudify is a SaaS company offering infrastructure and developer "
            "operations services to customers."
        ),
        category="entity-based",
    ),
    EvaluationCase(
        user_input="What is the relationship between Cloudify and Professional?",
        reference="Cloudify has a Professional plan.",
        category="relationship, graph-friendly",
    ),
    EvaluationCase(
        user_input="What uses of Cloudify are permitted?",
        reference=(
            "Customers may deploy and manage cloud infrastructure and application "
            "environments, support internal engineering, DevOps, and infrastructure "
            "workflows, operate workloads consistent with their plan and contract, "
            "and use Cloudify APIs and interfaces for authorized administrative tasks."
        ),
        category="policy, vector-friendly",
    ),
    EvaluationCase(
        user_input="What is the uptime commitment for the Professional plan?",
        reference="The Professional plan has a 99.9% monthly uptime commitment.",
        category="simple factual, vector-friendly",
    ),
    EvaluationCase(
        user_input=(
            "What uptime does Professional promise, and what service credit "
            "applies if monthly uptime falls below 99.9%?"
        ),
        reference=(
            "Professional promises 99.9% monthly uptime. If uptime is below 99.9% "
            "but at or above 99.5%, the service credit is 15%; if uptime is below "
            "99.5%, the service credit is 30%."
        ),
        category="combined-context, multi-hop",
    ),
    EvaluationCase(
        user_input="Can an annual subscription be refunded after 14 days?",
        reference=(
            "Annual subscriptions are generally non-refundable after the 14-day "
            "cooling-off period, except for qualifying material service issues or "
            "terms explicitly provided in an Enterprise contract."
        ),
        category="policy, vector-friendly",
    ),
    EvaluationCase(
        user_input="What API request limit applies to the Professional plan?",
        reference=(
            "Professional allows 5,000 API requests per minute, with a 3x burst "
            "capacity for short intervals."
        ),
        category="specific factual, vector-friendly",
    ),
    EvaluationCase(
        user_input=(
            "How does the Enterprise plan differ from Professional in uptime "
            "and support?"
        ),
        reference=(
            "Enterprise has a 99.95% monthly uptime commitment and 24x7 priority "
            "support. Professional has a 99.9% monthly uptime commitment and "
            "priority support."
        ),
        category="hybrid, comparative",
    ),
]


def build_reference_dataset() -> list[dict[str, str]]:
    """Return RAGAS-independent user inputs and grounded references."""
    return [
        {
            "user_input": case.user_input,
            "reference": case.reference,
            "category": case.category,
        }
        for case in EVALUATION_CASES
    ]


def serialize_case(case: EvaluationCase) -> dict[str, str]:
    return asdict(case)