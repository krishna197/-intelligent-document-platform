#!/usr/bin/env python3
"""Test cloud storage connections with actual credentials."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_aws_connection():
    """Test AWS S3 connection with credentials from environment."""
    print("Testing AWS S3 connection...")

    # Check if AWS credentials are configured
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

    if not all([aws_access_key_id, aws_secret_access_key, aws_bucket_name]):
        print("! AWS credentials not fully configured. Skipping AWS S3 test.")
        print("  To test AWS S3, set these environment variables:")
        print("    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET_NAME")
        return None  # Skip test, don't count as failure

    try:
        from src.storage import StorageFactory

        # Create S3 storage instance
        storage = StorageFactory.create_storage(
            'aws_s3',
            aws_bucket_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
    except Exception as e:
        # Re-raise the exception - the S3Storage class now handles 403 errors gracefully
        raise

        # Test basic operations
        print(f"+ Connected to S3 bucket: {storage.bucket_name}")

        # Test listing files (should work even if bucket is empty)
        files = storage.list_files()
        print(f"+ Listed {len(files)} files in bucket")

        # Test creating a temporary file and uploading it
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file for AWS S3 connection testing.\n")
            f.write(f"Timestamp: {Path(__file__).stat().st_mtime}\n")
            temp_file_path = f.name

        try:
            # Upload the file
            object_key = f"test-connection-{Path(__file__).stat().st_mtime}.txt"
            upload_success = storage.upload_file(temp_file_path, object_key)

            if upload_success:
                print(f"+ Successfully uploaded test file to s3://{storage.bucket_name}/{object_key}")

                # Test file existence
                if storage.file_exists(object_key):
                    print("+ File existence check passed")
                else:
                    print("x File existence check failed")
                    return False

                # Test getting file URL
                url = storage.get_file_url(object_key, expiration=300)  # 5 minute URL
                if url:
                    print(f"+ Generated presigned URL (expires in 5 minutes)")
                else:
                    print("x Failed to generate presigned URL")
                    return False

                # Clean up: delete the test file
                if storage.delete_file(object_key):
                    print("+ Successfully cleaned up test file")
                else:
                    print("! Warning: Failed to delete test file")

                return True
            else:
                print("x Failed to upload test file")
                return False

        finally:
            # Clean up local temp file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    except Exception as e:
        print(f"x AWS S3 connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gcp_connection():
    """Test GCP Cloud Storage connection with credentials from environment."""
    print("\nTesting GCP Cloud Storage connection...")

    # Check if GCP credentials are configured
    gcp_credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    gcp_project_id = os.getenv('GCP_PROJECT_ID')
    gcp_bucket_name = os.getenv('GCP_STORAGE_BUCKET_NAME')

    if not all([gcp_credentials_path, gcp_project_id, gcp_bucket_name]):
        print("! GCP credentials not fully configured. Skipping GCP test.")
        print("  To test GCP Cloud Storage, set these environment variables:")
        print("    GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, GCP_STORAGE_BUCKET_NAME")
        return None  # Skip test, don't count as failure

    # Check if credentials file exists
    if not os.path.exists(gcp_credentials_path):
        print(f"! GCP credentials file not found: {gcp_credentials_path}")
        print("  Please check the GOOGLE_APPLICATION_CREDENTIALS path")
        return None  # Skip test, don't count as failure

    try:
        from src.storage import StorageFactory

        # Create GCP storage instance
        storage = StorageFactory.create_storage(
            'gcp',
            gcp_bucket_name,
            project_id=gcp_project_id,
            credentials_path=gcp_credentials_path
        )

        # Test basic operations
        print(f"+ Connected to GCS bucket: {storage.bucket_name}")

        # Test listing files (should work even if bucket is empty)
        files = storage.list_files()
        print(f"+ Listed {len(files)} files in bucket")

        # Test creating a temporary file and uploading it
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file for GCP Cloud Storage connection testing.\n")
            f.write(f"Timestamp: {Path(__file__).stat().st_mtime}\n")
            temp_file_path = f.name

        try:
            # Upload the file
            object_key = f"test-connection-{Path(__file__).stat().st_mtime}.txt"
            upload_success = storage.upload_file(temp_file_path, object_key)

            if upload_success:
                print(f"+ Successfully uploaded test file to gs://{storage.bucket_name}/{object_key}")

                # Test file existence
                if storage.file_exists(object_key):
                    print("+ File existence check passed")
                else:
                    print("x File existence check failed")
                    return False

                # Test getting file URL
                url = storage.get_file_url(object_key, expiration=300)  # 5 minute URL
                if url:
                    print(f"+ Generated signed URL (expires in 5 minutes)")
                else:
                    print("x Failed to generate signed URL")
                    return False

                # Clean up: delete the test file
                if storage.delete_file(object_key):
                    print("+ Successfully cleaned up test file")
                else:
                    print("! Warning: Failed to delete test file")

                return True
            else:
                print("x Failed to upload test file")
                return False

        finally:
            # Clean up local temp file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    except Exception as e:
        print(f"x GCP Cloud Storage connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the cloud storage connection tests."""
    print("=== Cloud Storage Connection Test ===")
    print("This script tests connections to AWS S3 and GCP Cloud Storage")
    print("using credentials from environment variables.\n")

    # Run tests
    aws_result = test_aws_connection()
    gcp_result = test_gcp_connection()

    print("\n" + "="*60)
    print("CONNECTION TEST SUMMARY:")
    print("="*60)

    if aws_result is True:
        print("+ AWS S3 connection: SUCCESS")
    elif aws_result is False:
        print("x AWS S3 connection: FAILED")
    else:
        print("- AWS S3 connection: SKIPPED (credentials not configured)")

    if gcp_result is True:
        print("+ GCP Cloud Storage connection: SUCCESS")
    elif gcp_result is False:
        print("x GCP Cloud Storage connection: FAILED")
    else:
        print("- GCP Cloud Storage connection: SKIPPED (credentials not configured)")

    # Determine overall result
    if aws_result is False or gcp_result is False:
        print("\nRESULT: Some connections failed. Please check the error messages above.")
        return 1
    elif aws_result is True or gcp_result is True:
        print("\nRESULT: At least one cloud storage connection is working!")
        return 0
    else:
        print("\nRESULT: No connections tested (credentials not configured).")
        print("        Please configure credentials to test connections.")
        return 0

if __name__ == "__main__":
    sys.exit(main())