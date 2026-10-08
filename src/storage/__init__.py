# Storage abstractions

from .base import BaseStorage, StorageFactory

# Lazy imports for concrete implementations to avoid dependency issues
def __getattr__(name):
    if name == "S3Storage":
        from .aws_s3 import S3Storage
        return S3Storage
    if name == "GCPStorage":
        from .gcp_storage import GCPStorage
        return GCPStorage
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ["BaseStorage", "StorageFactory", "S3Storage", "GCPStorage"]