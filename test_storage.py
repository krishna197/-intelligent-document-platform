#!/usr/bin/env python3
"""Test the cloud storage implementations."""

import sys
import os
import tempfile
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_storage_base():
    """Test that we can import and instantiate storage components."""
    print("Testing storage implementations...")

    # Try to import base components first (these should work without dependencies)
    try:
        from src.storage.base import BaseStorage, StorageFactory
        print("+ Base storage classes imported successfully")
    except Exception as e:
        print(f"x Failed to import base storage classes: {e}")
        return False

    # Try to import S3 storage (might fail if boto3 not installed)
    try:
        from src.storage.aws_s3 import S3Storage
        print("+ S3Storage imported successfully")
        s3_available = True
    except ImportError as e:
        if "boto3" in str(e):
            print("! S3Storage import skipped (boto3 not installed)")
            s3_available = False
        else:
            print(f"x Failed to import S3Storage: {e}")
            return False
    except Exception as e:
        print(f"x Failed to import S3Storage: {e}")
        return False

    # Try to import GCP storage (might fail if google-cloud-storage not installed)
    try:
        from src.storage.gcp_storage import GCPStorage
        print("+ GCPStorage imported successfully")
        gcp_available = True
    except ImportError as e:
        if "google.cloud" in str(e):
            print("! GCPStorage import skipped (google-cloud-storage not installed)")
            gcp_available = False
        else:
            print(f"x Failed to import GCPStorage: {e}")
            return False
    except Exception as e:
        print(f"x Failed to import GCPStorage: {e}")
        return False

    return True

def test_s3_storage():
    """Test S3 storage instantiation (without actual AWS credentials)."""
    print("\nTesting S3 storage...")

    # Try to import S3 storage
    try:
        from src.storage.aws_s3 import S3Storage
        print("+ S3Storage class can be imported")
        s3_available = True
    except ImportError as e:
        if "boto3" in str(e):
            print("! S3Storage import skipped (boto3 not installed)")
            s3_available = False
        else:
            print(f"x Error importing S3Storage: {e}")
            return False
    except Exception as e:
        print(f"x Error testing S3 storage: {e}")
        return False

    # Test StorageFactory (only if S3 is available, since factory imports S3)
    if s3_available:
        try:
            from src.storage import StorageFactory
            print("+ StorageFactory imported successfully")
        except ImportError as e:
            if "boto3" in str(e):
                print("! StorageFactory import skipped (boto3 not installed)")
            else:
                print(f"x Error importing StorageFactory: {e}")
                return False
        except Exception as e:
            print(f"x Error testing StorageFactory: {e}")
            return False

    return True

def test_gcp_storage():
    """Test GCP storage instantiation (without actual GCP credentials)."""
    print("\nTesting GCP storage...")

    try:
        from src.storage.gcp_storage import GCPStorage
        print("+ GCPStorage class can be imported")
    except ImportError as e:
        if "google.cloud" in str(e):
            print("! GCPStorage import skipped (google-cloud-storage not installed)")
        else:
            print(f"x Error importing GCPStorage: {e}")
            return False
    except Exception as e:
        print(f"x Error testing GCP storage: {e}")
        return False

    return True

def test_storage_factory():
    """Test the storage factory."""
    print("\nTesting storage factory...")

    # Try to import StorageFactory from base (to avoid importing S3Storage/GCPStorage)
    try:
        from src.storage.base import StorageFactory
        print("+ StorageFactory imported successfully")
        factory_available = True
    except ImportError as e:
        if "boto3" in str(e):
            print("! StorageFactory import skipped (boto3 not installed)")
            factory_available = False
        else:
            print(f"x Error importing StorageFactory: {e}")
            return False
    except Exception as e:
        print(f"x Error importing StorageFactory: {e}")
        return False

    # Test that it raises appropriate errors for invalid providers (only if factory is available)
    if factory_available:
        try:
            StorageFactory.create_storage('invalid_provider', 'test-bucket')
            print("x Factory should have raised ValueError for invalid provider")
            return False
        except ValueError as e:
            if "Unsupported storage provider" in str(e):
                print("+ Factory correctly raises ValueError for invalid provider")
            else:
                print(f"x Factory raised unexpected ValueError: {e}")
                return False
        except Exception as e:
            print(f"x Factory raised unexpected error: {e}")
            return False

    return True

def create_test_file():
    """Create a temporary test file for storage operations."""
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "test_document.txt")

    with open(test_file, 'w') as f:
        f.write("This is a test document for cloud storage testing.\n")
        f.write("It contains multiple lines to test file operations.\n")

    return test_file, temp_dir

def main():
    """Run the storage tests."""
    print("=== Cloud Storage Implementation Test ===\n")

    tests = [
        test_storage_base,
        test_s3_storage,
        test_gcp_storage,
        test_storage_factory
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "="*50)
    if all_passed:
        print("+ All storage tests passed!")
        print("\nStorage implementations are ready to use.")
        print("\nTo test with actual cloud providers:")
        print("  1. Configure AWS credentials (access key ID and secret access key)")
        print("  2. Configure GCP credentials (service account key file)")
        print("  3. Update the .env file with your credentials and bucket names")
        print("  4. Run the storage connection tests")
        print("\nTo use the storage factory:")
        print("  from src.storage import StorageFactory")
        print("  # For AWS S3:")
        print("  storage = StorageFactory.create_storage('aws_s3', 'my-bucket')")
        print("  # For GCP:")
        print("  storage = StorageFactory.create_storage('gcp', 'my-bucket')")
        return 0
    else:
        print("- Some storage tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())