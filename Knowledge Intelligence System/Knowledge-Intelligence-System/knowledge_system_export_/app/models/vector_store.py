"""FAISS vector store wrapper."""

import os

from typing import (
    List,
    Dict
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_core.documents import (
    Document
)


class VectorStore:

    def __init__(self, config):

        self.cfg = config

        self.embeddings = HuggingFaceEmbeddings(

            model_name=config.embedding_model,

            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        if os.path.exists(config.vector_db_path):

            self.db = FAISS.load_local(
                config.vector_db_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

        else:

            self.db = None


    def add_documents(
        self,
        docs: List[Document]
    ) -> Dict:

        if not docs:

            return {
                "inserted": 0,
                "status": "no documents"
            }

        if self.db is None:

            self.db = FAISS.from_documents(
                docs,
                self.embeddings
            )

        else:

            self.db.add_documents(docs)

        self.db.save_local(
            self.cfg.vector_db_path
        )

        return {
            "inserted": len(docs),
            "status": "ok"
        }


    def similarity_search(
        self,
        q: str,
        k: int = None
    ):

        if self.db is None:
            return []

        return self.db.similarity_search(
            q,
            k=k or self.cfg.similarity_k
        )


    def as_retriever(self):

        if self.db is None:
            raise ValueError(
                "Vector database is empty."
            )

        return self.db.as_retriever(
            search_kwargs={
                "k": self.cfg.similarity_k
            }
        )


    def stats(self):

        if self.db is None:

            return {
                "doc_count": 0
            }

        return {
            "doc_count":
            len(self.db.index_to_docstore_id)
        }