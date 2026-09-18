from controllers.chunking.ChunkingEnums import ChunkingType
from controllers.chunking.providers.TokenChunker import TokenChunker
from controllers.chunking.providers.SemanticChunker import SemanticChunker
from controllers.chunking.providers.RecursiveChunker import RecursiveChunker


class ChunkingProviderFactory:

    @staticmethod
    def get_provider(
        chunking_type: ChunkingType,
        embedding_provider=None
    ):

        if chunking_type == ChunkingType.TOKEN:
            return TokenChunker()

        elif chunking_type == ChunkingType.SEMANTIC:
            return SemanticChunker(
                embedding_provider=embedding_provider
            )

        elif chunking_type == ChunkingType.RECURSIVE:
            return RecursiveChunker()

        raise ValueError(
            f"Unsupported chunking type: {chunking_type}"
        )