from .BaseController import BaseController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessingEnum
from typing import List
from dataclasses import dataclass
# from langchain.schema import Document
from langchain_core.documents import Document
class BaseReader(BaseController):
    def __init__(self):
        super().__init__()
        self.allowed_types = self.app_settings.FILE_ALLOWED_TYPES
        self.max_size = self.app_settings.FILE_MAX_SIZE
        self.default_chunk_size = self.app_settings.FILE_DEFAULT_CHUNK_SIZE

    def get_file_extension(self, file_path: str) -> str:
        return os.path.splitext(file_path)[-1]

    def is_file_type_allowed(self, file_path: str) -> bool:
        file_extension = self.get_file_extension(file_path)
        return file_extension.lower() in self.allowed_types

    def is_file_size_allowed(self, file_path: str) -> bool:
        file_size = os.path.getsize(file_path)
        return file_size <= self.max_size
    def get_file_loader(self, file_path: str):
        file_extension = self.get_file_extension(file_path)

        if file_extension.lower() in [".txt", ".md"]:
            return TextLoader(file_path)

        elif file_extension.lower() == ".pdf":
            return PyMuPDFLoader(file_path)

        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

    def get_file_content(self, file_path: str):
        loader =self.get_file_loader(file_path=file_path)
        if loader:
            return loader.load()
        return None
    def process_file_content(self,file_content: List[Document],chunk_size: int=100, overlap_size: int=20):
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]
        chunks = self.process_simpler_splitter(
            texts=file_content_texts,
            metadatas=file_content_metadata,
            chunk_size=chunk_size,
        )

        return chunks
    def process_simpler_splitter(
    self,
    texts: List[str],
    metadatas: List[dict],
    chunk_size: int = 100
        ):
        chunks = []

        for text, metadata in zip(texts, metadatas):

            text_length = len(text)
            start_index = 0

            while start_index < text_length:

                end_index = min(
                    start_index + chunk_size,
                    text_length
                )

                chunk_text = text[start_index:end_index]

                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_start"] = start_index
                chunk_metadata["chunk_end"] = end_index

                chunks.append({
                    "text": chunk_text,
                    "metadata": chunk_metadata
                })

                start_index += chunk_size

        return chunks
