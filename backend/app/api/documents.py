from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.document import Document
from app.services.document_service import ingest_document, search_documents

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename.endswith((".txt", ".md")):
        raise HTTPException(status_code=400, detail="Only .txt and .md files are supported")

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text")

    if not text.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    doc = Document(filename=file.filename, content=text, status="processing")
    db.add(doc)
    await db.flush()

    chunk_count = await ingest_document(doc.id, file.filename, text)

    doc.chunk_count = chunk_count
    doc.status = "ready"

    return {"id": doc.id, "filename": file.filename, "chunks": chunk_count, "status": "ready"}


@router.get("/search")
async def search(q: str, limit: int = 5):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    results = await search_documents(q, limit)
    return results
