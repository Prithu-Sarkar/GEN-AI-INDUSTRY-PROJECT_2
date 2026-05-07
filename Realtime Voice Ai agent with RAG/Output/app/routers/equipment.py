import os, uuid, tempfile
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from loguru import logger
from bson import ObjectId
from app.services.text_extraction import TextExtractionService
from app.services.embeddings import EmbeddingService
from app.database import get_database
from app.models.equipment import Equipment
from app.config import settings

router = APIRouter()

def _serialize(doc: dict) -> dict:
    out = dict(doc)
    for key in ("_id", "equipment_id", "document_id"):
        if key in out and isinstance(out[key], ObjectId):
            out[key] = str(out[key])
    for key in ("created_at", "updated_at"):
        if key in out and isinstance(out[key], datetime):
            out[key] = out[key].isoformat()
    return out

@router.post("/", response_model=Equipment, status_code=status.HTTP_201_CREATED)
async def create_equipment(equipment: Equipment):
    db = get_database()
    existing = await db.equipment.find_one({"name": equipment.name, "tenant_id": equipment.tenant_id})
    if existing:
        raise HTTPException(status_code=409, detail="Equipment with this name already exists")
    now = datetime.utcnow()
    eq_dict = equipment.model_dump(exclude={"id"}, exclude_none=True)
    eq_dict.update({"created_at": now, "updated_at": now})
    result = await db.equipment.insert_one(eq_dict)
    resp = equipment.model_dump(exclude={"id"}, exclude_none=True)
    resp["_id"] = str(result.inserted_id)
    return Equipment(**resp)

@router.get("/", response_model=List[Equipment])
async def get_equipment():
    db = get_database()
    items = await db.equipment.find({}).to_list(length=None)
    return [Equipment(**_serialize(i)) for i in items]

@router.get("/{equipment_id}", response_model=Equipment)
async def get_one_equipment(equipment_id: str):
    db = get_database()
    item = await db.equipment.find_one({"_id": ObjectId(equipment_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return Equipment(**_serialize(item))

@router.post("/{equipment_id}/documents", status_code=201)
async def upload_equipment_documents(
    equipment_id: str,
    files: List[UploadFile] = File(...),
    description: Optional[str] = Form(None),
):
    db = get_database()
    equipment = await db.equipment.find_one({"_id": ObjectId(equipment_id)})
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    text_extractor = TextExtractionService()
    embedding_service = EmbeddingService()
    tenant_id = settings.TENANT_ID
    created_docs = []
    for file in files:
        try:
            data = await file.read()
            original_name = file.filename or "upload.bin"
            content_type = file.content_type or "application/octet-stream"
            logger.info(f"Processing: {original_name} ({len(data)} bytes)")
            if not text_extractor.is_supported(content_type, original_name):
                logger.warning(f"Unsupported format: {content_type}")
                continue
            temp_path = None
            try:
                _, ext = os.path.splitext(original_name)
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                    tmp.write(data)
                    temp_path = tmp.name
                extracted_text = text_extractor.extract_text(temp_path, content_type)
                if not extracted_text or not extracted_text.strip():
                    logger.warning(f"No text extracted from {original_name}")
                    continue
                chunks = embedding_service.split_text(extracted_text)
                logger.info(f"Split into {len(chunks)} chunks")
                if not chunks:
                    continue
                storage_key = f"{tenant_id}/equipment/{equipment_id}/{uuid.uuid4().hex}-{original_name}"
                now = datetime.utcnow()
                doc_dict = {
                    "equipment_id": ObjectId(equipment_id),
                    "tenant_id": tenant_id,
                    "file_name": original_name,
                    "content_type": content_type,
                    "size": len(data),
                    "storage_key": storage_key,
                    "uploaded_by": settings.USER_ID,
                    "description": description,
                    "embedding_status": "processing",
                    "created_at": now,
                    "updated_at": now,
                }
                doc_result = await db.documents_metadata.insert_one(doc_dict)
                document_id = doc_result.inserted_id
                chunk_docs = []
                for idx, chunk_text in enumerate(chunks):
                    try:
                        vec = embedding_service.embed_text(chunk_text)
                        chunk_docs.append({
                            "document_id": document_id,
                            "equipment_id": ObjectId(equipment_id),
                            "tenant_id": tenant_id,
                            "file_name": original_name,
                            "chunk_id": str(uuid.uuid4()),
                            "chunk_index": idx,
                            "text": chunk_text,
                            "embedding": vec,
                            "is_disabled": False,
                        })
                    except Exception as e:
                        logger.warning(f"Chunk {idx} embedding failed: {e}")
                if chunk_docs:
                    await db[settings.DOCUMENT_CHUNKS_COLLECTION].insert_many(chunk_docs)
                    await db.documents_metadata.update_one(
                        {"_id": document_id},
                        {"$set": {"embedding_status": "completed", "updated_at": datetime.utcnow()}}
                    )
                    logger.success(f"✅ {original_name} - {len(chunk_docs)} chunks stored")
                    doc_dict["_id"] = str(document_id)
                    doc_dict["equipment_id"] = str(doc_dict["equipment_id"])
                    doc_dict["created_at"] = doc_dict["created_at"].isoformat()
                    doc_dict["updated_at"] = doc_dict["updated_at"].isoformat()
                    created_docs.append(doc_dict)
                else:
                    await db.documents_metadata.update_one(
                        {"_id": document_id},
                        {"$set": {"embedding_status": "failed", "updated_at": datetime.utcnow()}}
                    )
            finally:
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {e}", exc_info=True)
    return {"documents": created_docs, "count": len(created_docs)}

@router.get("/{equipment_id}/documents")
async def list_equipment_documents(equipment_id: str):
    db = get_database()
    if not await db.equipment.find_one({"_id": ObjectId(equipment_id)}):
        raise HTTPException(status_code=404, detail="Equipment not found")
    docs = await db.documents_metadata.find({
        "equipment_id": ObjectId(equipment_id),
        "is_disabled": {"$ne": True},
    }).to_list(length=1000)
    return {"documents": [_serialize(d) for d in docs], "count": len(docs)}
