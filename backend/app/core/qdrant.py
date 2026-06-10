from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings

EMBEDDING_DIM = 1024  # voyage-3

_client: AsyncQdrantClient | None = None


def get_qdrant() -> AsyncQdrantClient:
    global _client
    if _client is None:
        if settings.qdrant_url:
            _client = AsyncQdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key or None,
            )
        else:
            _client = AsyncQdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port,
            )
    return _client


async def ensure_collection() -> None:
    await ensure_tenant_collection(settings.qdrant_collection)


async def ensure_tenant_collection(collection_name: str) -> None:
    from qdrant_client.models import PayloadSchemaType
    client = get_qdrant()
    exists = await client.collection_exists(collection_name)
    if not exists:
        await client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )
    # Ensure payload index exists (safe to call even if already indexed)
    try:
        await client.create_payload_index(
            collection_name=collection_name,
            field_name="document_id",
            field_schema=PayloadSchemaType.INTEGER,
        )
    except Exception:
        pass
