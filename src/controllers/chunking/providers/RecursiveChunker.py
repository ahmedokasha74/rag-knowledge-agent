from controllers.chunking.ChunkingInterface import ChunkingInterface
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


class RecursiveChunker(ChunkingInterface):

    def chunk(
        self,
        documents: List[Document],
        chunk_size: int,
        chunk_overlap: int
    ) -> List[Document]:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        return splitter.split_documents(documents)