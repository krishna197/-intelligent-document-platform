#!/usr/bin/env python3
"""Debug import issues."""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Attempting to import src.storage.base...")
try:
    from src.storage.base import BaseStorage, StorageFactory
    print("Success! Imported BaseStorage and StorageFactory")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to import src.storage.aws_s3...")
try:
    from src.storage.aws_s3 import S3Storage
    print("Success! Imported S3Storage")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()

print("\nAttempting to import src.storage.gcp_storage...")
try:
    from src.storage.gcp_storage import GCPStorage
    print("Success! Imported GCPStorage")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()