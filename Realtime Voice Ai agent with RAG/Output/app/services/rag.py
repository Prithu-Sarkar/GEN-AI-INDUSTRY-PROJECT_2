from typing import Any, List, Optional
import uuid
from bson import ObjectId
from loguru import logger
from app.database import get_database
from app.services.embeddings import EmbeddingService
from app.config import settings
from app.models.rag import ChunkContent, ChunkMetadata, RetrievalMetadata, RetrievalResult

embeddings_service = EmbeddingService()

class RAGService:
    def __init__(self, index_name: str = None):
        self.index_name = index_name or settings.VECTOR_INDEX_NAME

    async def retrieve(
        self,
        query: str,
        k: int = 5,
        equipment_id: Optional[str] = None,
        tenant_id: Optional[str] = None,
        extra_filters: Optional[dict] = None,
    ) -> RetrievalResult:
        """
        Retrieve top-k semantically similar chunks.
        Tries MongoDB Atlas Vector Search first.
        Falls back to in-memory cosine similarity when Atlas index is not configured.
        """
        db = get_database()
        collection = db[settings.DOCUMENT_CHUNKS_COLLECTION]

        logger.info(f"Retrieval query: {query[:60]} (k={k})")
        query_embedding = embeddings_service.embed_text(query)

        filters: dict = {"is_disabled": {"$ne": True}}
        if equipment_id:
            try:
                filters["equipment_id"] = ObjectId(equipment_id)
            except Exception:
                logger.warning(f"Invalid equipment_id; skipping filter")
        if tenant_id:
            filters["tenant_id"] = tenant_id
        if extra_filters:
            filters.update(extra_filters)

        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": self.index_name,
                        "path": "embedding",
                        "queryVector": query_embedding,
                        "numCandidates": k * 5,
                        "limit": k,
                        **({"filter": filters} if filters else {}),
                    }
                },
                {
                    "$project": {
                        "_id": 1, "chunk_id": 1, "document_id": 1,
                        "file_name": 1, "text": 1, "chunk_index": 1,
                        "equipment_id": 1, "tenant_id": 1,
                        "score": {"$meta": "vectorSearchScore"},
                    }
                },
            ]
            cursor = collection.aggregate(pipeline)
            results = await cursor.to_list(length=k)
            if not results:
                raise ValueError("Atlas returned 0 results")
            logger.info(f"Atlas vector search: {len(results)} results")
        except Exception as e:
            logger.warning(f"Atlas Vector Search unavailable ({e}). Using cosine fallback.")
            results = await self._cosine_fallback(collection, query_embedding, filters, k)

        chunk_data, chunk_meta = [], []
        for res in results:
            chunk_data.append(ChunkContent(
                text=res.get("text", ""),
                file_name=res.get("file_name"),
                score=res.get("score"),
            ))
            chunk_meta.append(ChunkMetadata(
                chunk_id=res.get("chunk_id", ""),
                document_id=str(res.get("document_id", "")),
                equipment_id=str(res.get("equipment_id", "")),
                tenant_id=res.get("tenant_id"),
                chunk_index=res.get("chunk_index", 0),
                score=float(res.get("score", 0.0)),
                file_name=res.get("file_name", ""),
            ))

        return RetrievalResult(
            data=chunk_data,
            metadata=RetrievalMetadata(
                query=query, k=k,
                chunks_retrieved=len(chunk_data),
                equipment_id=equipment_id, tenant_id=tenant_id,
                chunks=chunk_meta,
            ),
        )

    async def _cosine_fallback(self, collection, query_embedding, filters, k):
        """In-memory cosine similarity when Atlas Vector Search index is not set up."""
        import numpy as np
        docs = await collection.find(filters).to_list(length=1000)
        if not docs:
            return []
        qv = np.array(query_embedding)
        scored = []
        for doc in docs:
            ev = doc.get("embedding")
            if not ev:
                continue
            ev = np.array(ev)
            norm = np.linalg.norm(qv) * np.linalg.norm(ev)
            doc["score"] = float(np.dot(qv, ev) / norm) if norm > 0 else 0.0
            scored.append(doc)
        scored.sort(key=lambda d: d["score"], reverse=True)
        return scored[:k]
