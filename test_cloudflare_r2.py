#!/usr/bin/env python3
"""Test Cloudflare R2 connection using our S3Storage implementation."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_cloudflare_r2_connection():
    """Test Cloudflare R2 connection using S3Storage with custom endpoint."""
    print("Testing Cloudflare R2 connection (via S3Storage compatibility)...")

    # Check if Cloudflare R2 credentials are configured
    access_key_id = os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
    secret_access_key = os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')
    account_id = os.getenv('CLOUDFLARE_R2_ACCOUNT_ID')
    bucket_name = os.getenv('CLOUDFLARE_R2_BUCKET_NAME')

    if not all([access_key_id, secret_access_key, account_id, bucket_name]):
        print("! Cloudflare R2 credentials not fully configured.")
        print("  To test Cloudflare R2, set these environment variables:")
        print("    CLOUDFLARE_R2_ACCESS_KEY_ID, CLOUDFLARE_R2_SECRET_ACCESS_KEY,")
        print("    CLOUDFLARE_R2_ACCOUNT_ID, CLOUDFLARE_R2_BUCKET_NAME")
        return None  # Skip test, don't count as failure

    try:
        from src.storage import StorageFactory

        # Create S3 storage instance configured for Cloudflare R2
        # Cloudflare R2 endpoint format: https://<account-id>.r2.cloudflarestorage.com
        endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"

        storage = StorageFactory.create_storage(
            'aws_s3',  # We still use the AWS S3 provider class
            bucket_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name='weurope',  # Region is ignored by R2 but required
            endpoint_url=endpoint_url  # This overrides the AWS endpoint
        )

        # Test basic operations
        print(f"✓ Connected to Cloudflare R2 bucket: {storage.bucket_name}")
        print(f"✓ Using endpoint: {endpoint_url}")

        # Test listing files (should work even if bucket is empty)
        files = storage.list_files()
        print(f"✓ Listed {len(files)} files in bucket")

        # Test creating a temporary file and uploading it
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file for Cloudflare R2 connection testing.\n")
            f.write(f"Timestamp: {Path(__file__).stat().st_mtime}\n")
            temp_file_path = f.name

        try:
            # Upload the file
            object_key = f"test-connection-{Path(__file__).stat().st_mtime}.txt"
            upload_success = storage.upload_file(temp_file_path, object_key)

            if upload_success:
                print(f"✓ Successfully uploaded test file to R2 bucket/{object_key}")

                # Test file existence
                if storage.file_exists(object_key):
                    print("✓ File existence check passed")
                else:
                    print("✗ File existence check failed")
                    return False

                # Test getting file URL (presigned URL)
                url = storage.get_file_url(object_key, expiration=300)  # 5 minute URL
                if url:
                    print(f"✓ Generated presigned URL (expires in 5 minutes)")
                    # Note: With Cloudflare R2, this will be a signed URL to their service
                else:
                    print("✗ Failed to generate presigned URL")
                    return False

                # Clean up: delete the test file
                if storage.delete_file(object_key):
                    print("✓ Successfully cleaned up test file")
                else:
                    print("! Warning: Failed to delete test file")

                return True
            else:
                print("✗ Failed to upload test file")
                return False

        finally:
            # Clean up local temp file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    except Exception as e:
        print(f"✗ Cloudflare R2 connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the Cloudflare R2 connection test."""
    print("=== Cloudflare R2 Connection Test ===")
    print("This script tests connection to Cloudflare R2 using our")
    print("S3Storage implementation (thanks to S3 compatibility).\n")

    # Run test
    result = test_cloudflare_r2_connection()

    print("\n" + "="*60)
    print("CONNECTION TEST SUMMARY:")
    print("="*60)

    if result is True:
        print("✓ Cloudflare R2 connection: SUCCESS")
        print("\nYour Cloudflare R2 is working correctly with our storage abstractions!")
    elif result is False:
        print("✗ Cloudflare R2 connection: FAILED")
        print("\nPlease check your credentials and endpoint configuration.")
        return 1
    else:
        print("- Cloudflare R2 connection: SKIPPED (credentials not configured)")
        print("\nPlease configure your Cloudflare R2 credentials to test the connection.")
        return 0

if __name__ == "__main__":
    sys.exit(main())