
from core.settings import Settings
from integrations.rag.faiss_kb import KnowledgeBaseService

class KnowledgeService:
    def __init__(self,settings:Settings): self._s=settings
    def ingest(self,clear_existing=False)->dict:
        """Ingest all KB files from knowledge_base_dir."""
        return KnowledgeBaseService(settings=self._s).ingest_directory(
            self._s.knowledge_base_dir,clear_existing=clear_existing)
