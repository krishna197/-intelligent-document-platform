#!/usr/bin/env python3
"""Test lazy imports from storage module."""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Attempting to import src.storage (should not load concrete implementations)...")
try:
    import src.storage
    print("Success! Imported src.storage module")

    # Test accessing base classes
    print("Testing access to BaseStorage and StorageFactory...")
    BaseStorage = src.storage.BaseStorage
    StorageFactory = src.storage.StorageFactory
    print("Success! Accessed BaseStorage and StorageFactory")

    # Test accessing concrete implementations (should trigger lazy loading)
    print("\nTesting access to S3Storage (should trigger lazy loading)...")
    try:
        S3Storage = src.storage.S3Storage
        print("Success! Accessed S3Storage (this would fail if boto3 not installed)")
    except Exception as e:
        print(f"Expected failure accessing S3Storage: {e}")

    print("\nTesting access to GCPStorage (should trigger lazy loading)...")
    try:
        GCPStorage = src.storage.GCPStorage
        print("Success! Accessed GCPStorage (this would fail if google.cloud not installed)")
    except Exception as e:
        print(f"Expected failure accessing GCPStorage: {e}")

except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()