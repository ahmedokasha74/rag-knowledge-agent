from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums

from models.db_schemes import RetrievedDocument

from typing import List, Optional
from uuid import NAMESPACE_URL, UUID, uuid5
import logging


class QdrantDBProvider(VectorDBInterface):

    def __init__(
        self,
        db_client: str,
        default_vector_size: int = 1024,
        distance_method: str = DistanceMethodEnums.COSINE.value,
        index_threshold: int = 100,
    ):
        self.db_client = db_client
        self.default_vector_size = default_vector_size
        self.index_threshold = index_threshold

        self.client: Optional[QdrantClient] = None

        self.distance_method = self._get_distance_method(
            distance_method
        )

        self.logger = logging.getLogger("uvicorn")

    @staticmethod
    def _normalize_record_id(record_id):
        if isinstance(record_id, (int, UUID)):
            return record_id

        return uuid5(NAMESPACE_URL, str(record_id))

    def _get_distance_method(self, distance_method: str):

        if distance_method == DistanceMethodEnums.COSINE.value:
            return models.Distance.COSINE

        if distance_method == DistanceMethodEnums.DOT.value:
            return models.Distance.DOT

        if distance_method == DistanceMethodEnums.EUCLID.value:
            return models.Distance.EUCLID

        raise ValueError(
            f"Unsupported distance method: {distance_method}"
        )

    async def connect(self):

        if self.client is None:
            self.client = QdrantClient(
                path=self.db_client
            )

    async def disconnect(self):

        if self.client:
            self.client.close()
            self.client = None

    def _ensure_connected(self):

        if self.client is None:
            raise RuntimeError(
                "Qdrant client is not connected."
            )

    async def is_collection_existed(
        self,
        collection_name: str
    ) -> bool:

        self._ensure_connected()

        return self.client.collection_exists(
            collection_name=collection_name
        )

    async def list_all_collections(self) -> List:

        self._ensure_connected()

        return self.client.get_collections()

    async def get_collection_info(
        self,
        collection_name: str
    ) -> dict:

        self._ensure_connected()

        return self.client.get_collection(
            collection_name=collection_name
        )

    async def delete_collection(
        self,
        collection_name: str
    ):

        self._ensure_connected()

        if await self.is_collection_existed(
            collection_name
        ):
            self.logger.info(
                f"Deleting collection: {collection_name}"
            )

            return self.client.delete_collection(
                collection_name=collection_name
            )

        return False

    async def create_collection(
        self,
        collection_name: str,
        embedding_size: int = None,
        do_reset: bool = False,
    ):

        self._ensure_connected()

        if do_reset:
            await self.delete_collection(
                collection_name=collection_name
            )

        if await self.is_collection_existed(
            collection_name
        ):
            return False

        embedding_size = (
            embedding_size
            or self.default_vector_size
        )

        self.logger.info(
            f"Creating Qdrant collection: {collection_name}"
        )

        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=embedding_size,
                distance=self.distance_method,
            ),
        )

        return True

    async def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ) -> bool:

        self._ensure_connected()

        if not await self.is_collection_existed(
            collection_name
        ):
            self.logger.error(
                f"Collection does not exist: {collection_name}"
            )
            return False

        try:

            record_id = self._normalize_record_id(record_id or 1)

            self.client.upload_points(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=record_id,
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata or {},
                        },
                    )
                ],
            )

            return True

        except Exception as e:

            self.logger.exception(
                f"Error inserting record: {e}"
            )

            return False

    async def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50,
    ) -> bool:

        self._ensure_connected()

        if not await self.is_collection_existed(
            collection_name
        ):
            self.logger.error(
                f"Collection does not exist: {collection_name}"
            )
            return False

        if len(texts) != len(vectors):
            raise ValueError(
                "texts and vectors must have the same length."
            )

        metadata = metadata or [{} for _ in texts]

        record_ids = (
            record_ids
            or list(range(len(texts)))
        )

        if len(metadata) != len(texts):
            raise ValueError(
                "metadata length must match texts length."
            )

        if len(record_ids) != len(texts):
            raise ValueError(
                "record_ids length must match texts length."
            )

        try:

            for i in range(
                0,
                len(texts),
                batch_size
            ):

                batch_texts = texts[
                    i:i + batch_size
                ]

                batch_vectors = vectors[
                    i:i + batch_size
                ]

                batch_metadata = metadata[
                    i:i + batch_size
                ]

                batch_record_ids = record_ids[
                    i:i + batch_size
                ]

                batch_record_ids = [
                    self._normalize_record_id(record_id)
                    for record_id in batch_record_ids
                ]

                records = [
                    models.PointStruct(
                        id=batch_record_ids[x],
                        vector=batch_vectors[x],
                        payload={
                            "text": batch_texts[x],
                            "metadata": batch_metadata[x],
                        },
                    )
                    for x in range(len(batch_texts))
                ]

                self.client.upload_points(
                    collection_name=collection_name,
                    points=records,
                )

            return True

        except Exception as e:

            self.logger.exception(
                f"Error inserting batch: {e}"
            )

            return False

    async def search_by_vector(
        self,
        collection_name: str,
        vector: list,
        limit: int = 5,
    ) -> List[RetrievedDocument]:

        self._ensure_connected()

        if not await self.is_collection_existed(
            collection_name
        ):
            self.logger.error(
                f"Collection does not exist: {collection_name}"
            )
            return []

        try:

            results = self.client.query_points(
                collection_name=collection_name,
                query=vector,
                limit=limit,
            ).points

            return [
                RetrievedDocument(
                    score=result.score,
                    text=result.payload.get(
                        "text",
                        ""
                    ),
                )
                for result in results
            ]

        except Exception as e:

            self.logger.exception(
                f"Error searching Qdrant: {e}"
            )

            return []