from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document


class ChunkingInterface(ABC):

    @abstractmethod
    def chunk(
        self,
        documents: List[Document],
        chunk_size: int,
        chunk_overlap: int
    ) -> List[Document]:
        pass