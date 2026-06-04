
from __future__ import annotations
import pickle, re
from pathlib import Path
import numpy as np, faiss
from sentence_transformers import SentenceTransformer
from core.settings import Settings

class CustomerMemoryStore:
    """Per-customer FAISS memory. Replaces mem0+ChromaDB."""
    def __init__(self, settings: Settings):
        self._base=Path(settings.faiss_mem_dir)
        self._base.mkdir(parents=True,exist_ok=True)
        self._model=SentenceTransformer(settings.embedding_model)

    def add_resolution(self,user_id,ticket_subject,ticket_description,accepted_draft,entity_links=None):
        """Store an accepted draft as searchable memory."""
        ent=(" | entities: "+", ".join(entity_links)) if entity_links else ""
        text=f"Ticket: {ticket_subject} | Issue: {ticket_description[:200]} | Resolution: {accepted_draft[:300]}{ent}"
        self._add(user_id,text,{"type":"resolution","subject":ticket_subject})

    def add_interaction(self,user_id,user_input,assistant_response,metadata=None):
        self._add(user_id,f"User: {user_input[:200]} | Asst: {assistant_response[:300]}",metadata or {})

    def search(self,query,user_id,limit=5)->list:
        """Semantic search; returns [{memory,score,metadata}]."""
        idx,docs,metas=self._load(user_id)
        if idx is None or idx.ntotal==0: return []
        k=min(limit,idx.ntotal)
        dists,idxs=idx.search(self._model.encode([query]).astype("float32"),k)
        return [{"memory":docs[i],"score":round(1/(1+float(d)),4),"metadata":metas[i]}
                for d,i in zip(dists[0],idxs[0]) if i>=0]

    def list_memories(self,user_id,limit=20)->list:
        _,docs,metas=self._load(user_id)
        return [{"memory":d,"score":None,"metadata":m}
                for d,m in list(zip(reversed(docs),reversed(metas)))[:limit]]

    def _safe(self,uid): return re.sub(r"[^\w\-]","_",uid)[:80]
    def _paths(self,uid):
        s=self._safe(uid)
        return self._base/f"{s}.faiss",self._base/f"{s}.pkl"
    def _load(self,uid):
        ip,mp=self._paths(uid)
        if not ip.exists() or not mp.exists(): return None,[],[]
        try:
            idx=faiss.read_index(str(ip))
            p=pickle.load(open(mp,"rb"))
            return idx,p.get("docs",[]),p.get("metas",[])
        except: return None,[],[]
    def _save(self,uid,idx,docs,metas):
        ip,mp=self._paths(uid)
        faiss.write_index(idx,str(ip))
        pickle.dump({"docs":docs,"metas":metas},open(mp,"wb"))
    def _add(self,uid,text,meta):
        idx,docs,metas=self._load(uid)
        emb=self._model.encode([text]).astype("float32")
        if idx is None: idx=faiss.IndexFlatL2(emb.shape[1])
        idx.add(emb); docs.append(text); metas.append(meta)
        self._save(uid,idx,docs,metas)
