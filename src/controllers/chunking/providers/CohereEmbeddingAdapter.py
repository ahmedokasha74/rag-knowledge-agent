from langchain_core.embeddings import Embeddings


class CohereEmbeddingAdapter(Embeddings):

    def __init__(self, embedding_provider):
        self.embedding_provider = embedding_provider

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.embedding_provider.embed_texts(
            texts=texts
        )

    def embed_query(self, text: str) -> list[float]:
        return self.embedding_provider.embed_text(
            text=text
        )