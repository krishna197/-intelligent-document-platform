"""GCP Cloud Storage implementation."""

from google.cloud import storage
from google.api_core import exceptions
from typing import BinaryIO, Optional, List
import logging
import os

from .base import BaseStorage, StorageFactory

logger = logging.getLogger(__name__)


class GCPStorage(BaseStorage):
    """GCP Cloud Storage implementation."""

    def __init__(self, bucket_name: str, project_id: Optional[str] = None,
                 credentials_path: Optional[str] = None):
        """
        Initialize GCP Cloud Storage.

        Args:
            bucket_name: Name of the GCS bucket
            project_id: GCP project ID (optional, uses default if not provided)
            credentials_path: Path to service account key file (optional, uses default credentials if not provided)
        """
        super().__init__(bucket_name)
        self.project_id = project_id

        try:
            if credentials_path and os.path.exists(credentials_path):
                # Use explicit credentials
                self.storage_client = storage.Client.from_service_account_json(
                    credentials_path, project=project_id
                )
            else:
                # Use default credentials (from environment, gcloud auth, or metadata server)
                self.storage_client = storage.Client(project=project_id)

            # Get or create the bucket
            self.bucket = self._get_or_create_bucket()
            self.logger.info(f"GCP storage initialized for bucket: {bucket_name}")

        except Exception as e:
            self.logger.error(f"Failed to initialize GCP storage: {e}")
            raise

    def _get_or_create_bucket(self) -> storage.Bucket:
        """Get the bucket if it exists, create it if it doesn't."""
        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)
            self.logger.debug(f"Bucket {self.bucket_name} already exists")
            return bucket
        except exceptions.NotFound:
            # Bucket doesn't exist, create it
            self.logger.info(f"Bucket {self.bucket_name} does not exist, creating...")
            try:
                bucket = self.storage_client.create_bucket(self.bucket_name)
                self.logger.info(f"Bucket {self.bucket_name} created successfully")
                return bucket
            except Exception as create_error:
                self.logger.error(f"Failed to create bucket {self.bucket_name}: {create_error}")
                raise
        except Exception as e:
            self.logger.error(f"Error accessing bucket {self.bucket_name}: {e}")
            raise

    def upload_file(self, file_path: str, object_key: Optional[str] = None) -> bool:
        """
        Upload a file to GCS.

        Args:
            file_path: Local path to the file to upload
            object_key: Optional key/object name in GCS (defaults to filename)

        Returns:
            True if upload successful, False otherwise
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False

        if object_key is None:
            object_key = os.path.basename(file_path)

        try:
            blob = self.bucket.blob(object_key)
            blob.upload_from_filename(file_path)
            self.logger.info(f"Uploaded {file_path} to gs://{self.bucket_name}/{object_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload {file_path} to GCS: {e}")
            return False

    def download_file(self, object_key: str, file_path: str) -> bool:
        """
        Download a file from GCS.

        Args:
            object_key: Key/object name in GCS
            file_path: Local path where file should be saved

        Returns:
            True if download successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

            blob = self.bucket.blob(object_key)
            blob.download_to_filename(file_path)
            self.logger.info(f"Downloaded gs://{self.bucket_name}/{object_key} to {file_path}")
            return True
        except exceptions.NotFound:
            self.logger.error(f"File not found in GCS: gs://{self.bucket_name}/{object_key}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to download from GCS: {e}")
            return False

    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from GCS.

        Args:
            object_key: Key/object name in GCS

        Returns:
            True if deletion successful, False otherwise
        """
        try:
            blob = self.bucket.blob(object_key)
            blob.delete()
            self.logger.info(f"Deleted gs://{self.bucket_name}/{object_key}")
            return True
        except exceptions.NotFound:
            self.logger.warning(f"File not found in GCS (already deleted?): gs://{self.bucket_name}/{object_key}")
            return True  # Consider it successful if it's already gone
        except Exception as e:
            self.logger.error(f"Failed to delete from GCS: {e}")
            return False

    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """
        List files in GCS bucket.

        Args:
            prefix: Optional prefix to filter objects

        Returns:
            List of object names
        """
        try:
            blobs = self.storage_client.list_blobs(self.bucket_name, prefix=prefix)
            names = [blob.name for blob in blobs]
            self.logger.debug(f"Listed {len(names)} objects from bucket {self.bucket_name}")
            return names
        except Exception as e:
            self.logger.error(f"Failed to list objects from GCS: {e}")
            return []

    def file_exists(self, object_key: str) -> bool:
        """
        Check if a file exists in GCS.

        Args:
            object_key: Key/object name in GCS

        Returns:
            True if file exists, False otherwise
        """
        try:
            blob = self.bucket.blob(object_key)
            return blob.exists()
        except Exception as e:
            self.logger.error(f"Error checking file existence in GCS: {e}")
            return False

    def get_file_url(self, object_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Get a signed URL for accessing a file in GCS.

        Args:
            object_key: Key/object name in GCS
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Signed URL string or None if not supported
        """
        try:
            blob = self.bucket.blob(object_key)
            if not blob.exists():
                self.logger.warning(f"File does not exist: gs://{self.bucket_name}/{object_key}")
                return None

            url = blob.generate_signed_url(expiration=expiration)
            self.logger.debug(f"Generated signed URL for gs://{self.bucket_name}/{object_key}")
            return url
        except Exception as e:
            self.logger.error(f"Failed to generate signed URL: {e}")
            return None

    def upload_fileobj(self, file_obj: BinaryIO, object_key: str) -> bool:
        """
        Upload a file-like object to GCS.

        Args:
            file_obj: File-like object to upload
            object_key: Key/object name in GCS

        Returns:
            True if upload successful, False otherwise
        """
        try:
            blob = self.bucket.blob(object_key)
            blob.upload_from_file(file_obj)
            self.logger.info(f"Uploaded fileobj to gs://{self.bucket_name}/{object_key}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload fileobj to GCS: {e}")
            return False

    def download_fileobj(self, object_key: str, file_obj: BinaryIO) -> bool:
        """
        Download a file from GCS to a file-like object.

        Args:
            object_key: Key/object name in GCS
            file_obj: File-like object to write to

        Returns:
            True if download successful, False otherwise
        """
        try:
            blob = self.bucket.blob(object_key)
            blob.download_to_file(file_obj)
            self.logger.info(f"Downloaded gs://{self.bucket_name}/{object_key} to fileobj")
            return True
        except Exception as e:
            self.logger.error(f"Failed to download fileobj from GCS: {e}")
            return False