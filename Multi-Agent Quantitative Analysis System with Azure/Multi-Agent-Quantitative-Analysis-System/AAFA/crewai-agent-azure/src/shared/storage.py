"""
Storage Service Module.

Responsible for persisting generated Markdown reports.
Primary target: Azure Blob Storage (cloud-permanent).
Fallback: Local file system inside outputs/ directory (Colab-safe).
"""

import os
import shutil
from src.shared.config import settings

# Local directory for storing reports in Colab
LOCAL_REPORTS_DIR = (
    '/content/Multi-Agent Quantitative Analysis System/AAFA/crewai-agent-azure/outputs'
)


class StorageService:
    """
    Abstraction layer over cloud/local storage for report files.

    Behaviour:
        - If Azure Blob credentials are set: uploads to Azure and returns the blob URL.
        - Otherwise: copies the file to outputs/ and returns a local file:// URL.
    """

    def __init__(self):
        # Determine storage backend based on credential availability
        self.use_azure = bool(settings.azure_blob_storage_connection_string)

        if self.use_azure:
            # Lazy import: only needed when Azure is configured
            from azure.storage.blob import BlobServiceClient
            self.service_client = BlobServiceClient.from_connection_string(
                settings.azure_blob_storage_connection_string
            )
            self.container_name = 'reports'
            self._ensure_container_exists()
            print('[Storage] Azure Blob Storage configured.')
        else:
            # Ensure local fallback directory exists
            os.makedirs(LOCAL_REPORTS_DIR, exist_ok=True)
            print(f'[Storage] Using local storage: {LOCAL_REPORTS_DIR}')

    def _ensure_container_exists(self):
        """
        Creates the Azure Blob container if it does not already exist.
        Silently swallows errors (e.g., container already exists).
        """
        try:
            container_client = self.service_client.get_container_client(self.container_name)
            if not container_client.exists():
                container_client.create_container()
                print(f'[Storage] Created Azure container: {self.container_name}')
        except Exception as e:
            print(f'[Storage] Warning checking container: {e}')

    def upload_file(self, file_path: str, destination_name: str) -> str:
        """
        Uploads or copies a report file to the configured storage backend.

        Args:
            file_path (str): Local path to the file to upload.
            destination_name (str): Target filename (used in URL / output path).

        Returns:
            str: A URL or local path string pointing to the stored file.
        """
        if self.use_azure:
            return self._upload_to_azure(file_path, destination_name)
        else:
            return self._save_locally(file_path, destination_name)

    def _upload_to_azure(self, file_path: str, destination_name: str) -> str:
        """
        Uploads a file to the Azure Blob container.

        Returns:
            str: Public HTTPS URL of the uploaded blob.
        """
        try:
            blob_client = self.service_client.get_blob_client(
                container=self.container_name, blob=destination_name
            )
            with open(file_path, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
            account = self.service_client.account_name
            return f'https://{account}.blob.core.windows.net/{self.container_name}/{destination_name}'
        except Exception as e:
            return f'[Storage] Azure upload error: {str(e)}'

    def _save_locally(self, file_path: str, destination_name: str) -> str:
        """
        Copies the file to the local outputs directory.

        Returns:
            str: Local file:// path of the saved report.
        """
        try:
            dest = os.path.join(LOCAL_REPORTS_DIR, destination_name)
            if file_path != dest and os.path.exists(file_path):
                shutil.copy2(file_path, dest)
            elif not os.path.exists(file_path):
                # If CrewAI wrote the file to CWD, check there too
                cwd_path = os.path.join(os.getcwd(), destination_name)
                if os.path.exists(cwd_path):
                    shutil.copy2(cwd_path, dest)
            return f'file://{dest}'
        except Exception as e:
            return f'[Storage] Local save error: {str(e)}'