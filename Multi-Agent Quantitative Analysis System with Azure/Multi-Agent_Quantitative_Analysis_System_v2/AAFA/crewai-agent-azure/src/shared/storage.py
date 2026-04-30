"""
Storage Service Module.
Uploads reports to Azure Blob Storage or saves locally as fallback.
"""
import os, shutil
from src.shared.config import settings

LOCAL_REPORTS_DIR = (
    "/content/Multi-Agent Quantitative Analysis System/"
    "AAFA/crewai-agent-azure/outputs"
)


class StorageService:
    """Abstraction over Azure Blob / local file storage."""

    def __init__(self):
        self.use_azure = bool(settings.azure_blob_storage_connection_string)
        if self.use_azure:
            from azure.storage.blob import BlobServiceClient
            self.service_client = BlobServiceClient.from_connection_string(
                settings.azure_blob_storage_connection_string
            )
            self.container_name = "reports"
            self._ensure_container()
            print("[Storage] Azure Blob configured.")
        else:
            os.makedirs(LOCAL_REPORTS_DIR, exist_ok=True)
            print(f"[Storage] Local fallback: {LOCAL_REPORTS_DIR}")

    def _ensure_container(self):
        """Create Azure container if it does not exist."""
        try:
            c = self.service_client.get_container_client(self.container_name)
            if not c.exists():
                c.create_container()
        except Exception as e:
            print(f"[Storage] Container check warning: {e}")

    def upload_file(self, file_path: str, destination_name: str) -> str:
        """Upload or copy a file. Returns URL or local path."""
        return (self._upload_azure(file_path, destination_name)
                if self.use_azure
                else self._save_local(file_path, destination_name))

    def _upload_azure(self, file_path: str, name: str) -> str:
        """Upload to Azure Blob and return public URL."""
        try:
            bc = self.service_client.get_blob_client(container=self.container_name, blob=name)
            with open(file_path, "rb") as data:
                bc.upload_blob(data, overwrite=True)
            acct = self.service_client.account_name
            return f"https://{acct}.blob.core.windows.net/{self.container_name}/{name}"
        except Exception as e:
            return f"[Storage] Azure error: {e}"

    def _save_local(self, file_path: str, name: str) -> str:
        """Copy file to local outputs directory and return path."""
        try:
            dest = os.path.join(LOCAL_REPORTS_DIR, name)
            for candidate in [file_path, os.path.join(os.getcwd(), name)]:
                if os.path.exists(candidate) and candidate != dest:
                    shutil.copy2(candidate, dest)
                    break
            return f"file://{dest}"
        except Exception as e:
            return f"[Storage] Local error: {e}"