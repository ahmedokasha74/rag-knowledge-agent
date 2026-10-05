from controllers.GraphRag.retrieval.graph_context_builder import (
    GraphContextBuilder,
)


def main():

    results = [
        {
            "source": "Cloudify",
            "relation": "HAS_PLAN",
            "target": "Professional",
        },
        {
            "source": "Cloudify",
            "relation": "OFFERS",
            "target": "Enterprise Plan",
        },
    ]

    builder = GraphContextBuilder()

    context = builder.build(results)

    print("\nGraph Context:")
    print("=" * 50)
    print(context)


if __name__ == "__main__":
    main()