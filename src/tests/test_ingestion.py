import asyncio

from helpers.config import get_settings
from controllers.ingestion.IngestionController import IngestionController


async def main():
    settings = get_settings()

    ingestion = IngestionController(
        config=settings
    )

    await ingestion.ingest_directory(
        directory_path="data/documents",
        collection_name="cloudify_documents",
        do_reset=True
    )


if __name__ == "__main__":
    asyncio.run(main())