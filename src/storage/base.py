"""Base storage interface for cloud storage providers."""

from abc import ABC, abstractmethod
from typing import BinaryIO, Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseStorage(ABC):
    """Abstract base class for cloud storage providers."""

    def __init__(self, bucket_name: str):
        """
        Initialize the storage provider.

        Args:
            bucket_name: Name of the storage bucket/container
        """
        self.bucket_name = bucket_name
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"Initialized storage for bucket: {bucket_name}")

    @abstractmethod
    def upload_file(self, file_path: str, object_key: Optional[str] = None) -> bool:
        """
        Upload a file to storage.

        Args:
            file_path: Local path to the file to upload
            object_key: Optional key/object name in storage (defaults to filename)

        Returns:
            True if upload successful, False otherwise
        """
        pass

    @abstractmethod
    def download_file(self, object_key: str, file_path: str) -> bool:
        """
        Download a file from storage.

        Args:
            object_key: Key/object name in storage
            file_path: Local path where file should be saved

        Returns:
            True if download successful, False otherwise
        """
        pass

    @abstractmethod
    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from storage.

        Args:
            object_key: Key/object name in storage

        Returns:
            True if deletion successful, False otherwise
        """
        pass

    @abstractmethod
    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """
        List files in storage.

        Args:
            prefix: Optional prefix to filter objects

        Returns:
            List of object keys/names
        """
        pass

    @abstractmethod
    def file_exists(self, object_key: str) -> bool:
        """
        Check if a file exists in storage.

        Args:
            object_key: Key/object name in storage

        Returns:
            True if file exists, False otherwise
        """
        pass

    @abstractmethod
    def get_file_url(self, object_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Get a presigned URL for accessing a file.

        Args:
            object_key: Key/object name in storage
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL string or None if not supported
        """
        pass

    def upload_fileobj(self, file_obj: BinaryIO, object_key: str) -> bool:
        """
        Upload a file-like object to storage.

        Args:
            file_obj: File-like object to upload
            object_key: Key/object name in storage

        Returns:
            True if upload successful, False otherwise
        """
        # Default implementation - can be overridden by subclasses
        self.logger.warning("upload_fileobj not implemented for this storage provider")
        return False

    def download_fileobj(self, object_key: str, file_obj: BinaryIO) -> bool:
        """
        Download a file to a file-like object.

        Args:
            object_key: Key/object name in storage
            file_obj: File-like object to write to

        Returns:
            True if download successful, False otherwise
        """
        # Default implementation - can be overridden by subclasses
        self.logger.warning("download_fileobj not implemented for this storage provider")
        return False


# Storage factory for creating provider instances
class StorageFactory:
    """Factory for creating storage provider instances."""

    @staticmethod
    def create_storage(provider: str, bucket_name: str, **kwargs) -> BaseStorage:
        """
        Create a storage provider instance.

        Args:
            provider: Storage provider ('aws_s3' or 'gcp')
            bucket_name: Name of the storage bucket
            **kwargs: Additional provider-specific configuration

        Returns:
            Storage provider instance

        Raises:
            ValueError: If provider is not supported
        """
        if provider.lower() == 'aws_s3':
            from .aws_s3 import S3Storage
            return S3Storage(bucket_name, **kwargs)
        elif provider.lower() == 'gcp':
            from .gcp_storage import GCPStorage
            return GCPStorage(bucket_name, **kwargs)
        else:
            raise ValueError(f"Unsupported storage provider: {provider}. Supported providers: 'aws_s3', 'gcp'")