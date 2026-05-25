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
    result = await asyncio.to_thread(client.embed, texts, model="voyage-3")
    return result.embeddings


async def ingest_document(document_id: int, filename: str, text: str) -> int:
    chunks = chunk_text(text)
    if not chunks:
        return 0

    embeddings = await embed_texts(chunks)
    qdrant = get_qdrant()

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

    await qdrant.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(chunks)


async def search_documents(query: str, limit: int = 5) -> List[dict]:
    embeddings = await embed_texts([query])
    query_vector = embeddings[0]

    qdrant = get_qdrant()
    hits = await qdrant.search(
        collection_name=settings.qdrant_collection,
        query_vector=query_vector,
        limit=limit,
    )

    return [
        {
            "text": hit.payload["text"],
            "filename": hit.payload["filename"],
            "score": round(hit.score, 4),
        }
        for hit in hits
    ]
