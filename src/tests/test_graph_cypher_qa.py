from helpers.config import get_settings
from controllers.GraphRag.graph_cypher_qa import GraphCypherQA


def main():

    settings = get_settings()

    graph_qa = GraphCypherQA(
        config=settings
    )

    queries = [
        "What plans does Cloudify offer?",
        "What is the relationship between Cloudify and Professional?",
        "What is connected to Cloudify?",
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print("USER:")
        print(query)

        result = graph_qa.ask(query)

        print("\nRESULT:")
        print(result)


if __name__ == "__main__":
    main()