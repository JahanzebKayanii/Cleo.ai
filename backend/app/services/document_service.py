import asyncio
from typing import List

import voyageai
from qdrant_client.models import PointStruct

from app.core.config import settings
from app.core.qdrant import get_qdrant

CHUNK_SIZE = 500
CHUNK_OVERLAP_WORDS = 5

_voyage_client: voyageai.Client | None = None


def _get_voyage() -> voyageai.Client:
    global _voyage_client
    if _voyage_client is None:
        _voyage_client = voyageai.Client(api_key=settings.voyage_api_key)
    return _voyage_client


def chunk_text(text: str) -> List[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for para in paragraphs:
        if len(para) <= CHUNK_SIZE:
            chunks.append(para)
        else:
            words = para.split()
            current: List[str] = []
            current_len = 0
            for word in words:
                if current_len + len(word) + 1 > CHUNK_SIZE and current:
                    chunks.append(" ".join(current))
                    current = current[-CHUNK_OVERLAP_WORDS:] + [word]
                    current_len = sum(len(w) + 1 for w in current)
                else:
                    current.append(word)
                    current_len += len(word) + 1
            if current:
                chunks.append(" ".join(current))
    return chunks


async def embed_texts(texts: List[str]) -> List[List[float]]:
    client = _get_voyage()
    for attempt in range(3):
        try:
            result = await asyncio.to_thread(client.embed, texts, model="voyage-3")
            return result.embeddings
        except voyageai.error.RateLimitError:
            if attempt == 2:
                raise
            await asyncio.sleep(20)
    raise RuntimeError("embed_texts: unreachable")


async def ingest_document(document_id: int, filename: str, text: str, collection: str | None = None) -> int:
    chunks = chunk_text(text)
    if not chunks:
        return 0

    collection = collection or settings.qdrant_collection
    embeddings = await embed_texts(chunks)
    qdrant = get_qdrant()

    from app.core.qdrant import ensure_tenant_collection
    await ensure_tenant_collection(collection)

    points = [
        PointStruct(
            id=document_id * 10_000 + i,
            vector=embedding,
            payload={
                "document_id": document_id,
                "filename": filename,
                "chunk_index": i,
                "text": chunk,
            },
        )
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
    ]

    await qdrant.upsert(collection_name=collection, points=points)
    return len(chunks)


async def delete_document_vectors(document_id: int, collection: str | None = None, chunk_count: int = 500) -> None:
    from qdrant_client.models import PointIdsList
    collection = collection or settings.qdrant_collection
    qdrant = get_qdrant()
    # Point IDs are stored as document_id * 10_000 + chunk_index
    point_ids = list(range(document_id * 10_000, document_id * 10_000 + chunk_count))
    await qdrant.delete(
        collection_name=collection,
        points_selector=PointIdsList(points=point_ids),
    )


async def search_documents(query: str, limit: int = 5, collection: str | None = None) -> List[dict]:
    collection = collection or settings.qdrant_collection
    embeddings = await embed_texts([query])
    query_vector = embeddings[0]

    qdrant = get_qdrant()
    try:
        hits = await qdrant.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=limit,
        )
    except Exception:
        return []

    return [
        {
            "text": hit.payload["text"],
            "filename": hit.payload["filename"],
            "score": round(hit.score, 4),
        }
        for hit in hits
    ]
