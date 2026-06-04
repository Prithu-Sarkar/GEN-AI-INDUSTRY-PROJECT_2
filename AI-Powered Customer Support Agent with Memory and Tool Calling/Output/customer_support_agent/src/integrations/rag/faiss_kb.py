
from __future__ import annotations
import hashlib, pickle
from pathlib import Path
import numpy as np, faiss
from sentence_transformers import SentenceTransformer

# LangChain 1.2+ text-splitter import path (separate package since LC 1.x)
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.settings import Settings

class KnowledgeBaseService:
    """FAISS-backed RAG service. Replaces chromadb from original project."""
    _IDX="faiss_rag.index"; _META="faiss_rag_meta.pkl"

    def __init__(self, settings: Settings):
        self._s=settings
        self._ip=Path(settings.faiss_rag_dir)/self._IDX
        self._mp=Path(settings.faiss_rag_dir)/self._META
        self._model=SentenceTransformer(settings.embedding_model)
        # LangChain 1.2+ splitter
        self._splitter=RecursiveCharacterTextSplitter(
            chunk_size=settings.rag_chunk_size,
            chunk_overlap=settings.rag_chunk_overlap)
        self._index=None; self._docs=[]; self._metas=[]
        self._load()

    def ingest_directory(self, directory: Path, clear_existing=False)->dict:
        """Chunk and embed all .md/.txt files; persist FAISS index to disk."""
        if clear_existing: self._index,self._docs,self._metas=None,[],[]
        srcs=sorted(list(directory.glob("*.md"))+list(directory.glob("*.txt")))
        chunks,metas=[],[]
        for fp in srcs:
            for i,ch in enumerate(self._splitter.split_text(fp.read_text(encoding="utf-8"))):
                chunks.append(ch)
                metas.append({"source":fp.name,"chunk_index":i,
                               "hash":hashlib.sha1(ch.encode()).hexdigest()[:8]})
        if not chunks: return {"files_indexed":0,"chunks_indexed":0,"total_in_index":0}
        emb=self._model.encode(chunks,show_progress_bar=False)
        if self._index is None: self._index=faiss.IndexFlatL2(emb.shape[1])
        self._index.add(emb.astype(np.float32))
        self._docs.extend(chunks); self._metas.extend(metas)
        self._save()
        return {"files_indexed":len(srcs),"chunks_indexed":len(chunks),
                "total_in_index":self._index.ntotal}

    def search(self, query: str, top_k=None)->list:
        """Semantic search over indexed KB. Returns [{content,source,distance}]."""
        if self._index is None or self._index.ntotal==0: return []
        k=min(top_k or self._s.rag_top_k,self._index.ntotal)
        dists,idxs=self._index.search(self._model.encode([query]).astype(np.float32),k)
        return [{"content":self._docs[i],"source":self._metas[i].get("source","?"),
                 "distance":float(d)} for d,i in zip(dists[0],idxs[0]) if i>=0]

    def _save(self):
        if self._index is None: return
        faiss.write_index(self._index,str(self._ip))
        pickle.dump({"documents":self._docs,"metadatas":self._metas},open(self._mp,"wb"))

    def _load(self):
        if self._ip.exists() and self._mp.exists():
            try:
                self._index=faiss.read_index(str(self._ip))
                p=pickle.load(open(self._mp,"rb"))
                self._docs=p.get("documents",[]); self._metas=p.get("metadatas",[])
            except: self._index,self._docs,self._metas=None,[],[]
