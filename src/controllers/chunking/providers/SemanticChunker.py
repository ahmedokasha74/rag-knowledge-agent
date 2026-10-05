from controllers.chunking.ChunkingInterface import ChunkingInterface
from controllers.chunking.providers.CohereEmbeddingAdapter import (
    CohereEmbeddingAdapter
)

from langchain_experimental.text_splitter import (
    SemanticChunker as LangChainSemanticChunker
)
from langchain_core.documents import Document

from typing import List


class SemanticChunker(ChunkingInterface):

    def __init__(self, embedding_provider):

        self.embedding_provider = CohereEmbeddingAdapter(
            embedding_provider
        )

        self.splitter = LangChainSemanticChunker(
            embeddings=self.embedding_provider
        )

    def chunk(
        self,
        documents: List[Document],
        chunk_size: int,
        chunk_overlap: int
    ) -> List[Document]:

        return self.splitter.split_documents(documents)