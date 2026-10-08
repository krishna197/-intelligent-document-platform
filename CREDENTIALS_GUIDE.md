# Cloud Storage Credentials Configuration Guide

This guide explains how to configure AWS and GCP credentials for testing the cloud storage integrations in the intelligent document platform.

## AWS S3 Configuration

### 1. Obtain AWS Credentials
To use AWS S3 storage, you need:
- AWS Access Key ID
- AWS Secret Access Key
- AWS Region (optional, defaults to us-east-1)

You can obtain these by:
1. Signing into the [AWS Management Console](https://aws.amazon.com/console/)
2. Navigating to IAM (Identity and Access Management)
3. Creating a new user or using an existing user
4. Generating access keys for the user
5. Optionally, attaching the `AmazonS3FullAccess` policy (or more restrictive policy as needed)

### 2. Create an S3 Bucket
You'll need an S3 bucket for testing. You can:
- Use the AWS Console to create a bucket
- Use AWS CLI: `aws s3 mb s3://your-bucket-name`
- Let the application create it automatically (the S3Storage class will attempt to create the bucket if it doesn't exist)

### 3. Configure Environment Variables
Add the following to your `.env` file (copy from `.env.template`):

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_actual_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
AWS_S3_BUCKET_NAME=your-test-bucket-name
```

## GCP Cloud Storage Configuration

### 1. Obtain GCP Credentials
To use GCP Cloud Storage, you need:
- A GCP service account key file (JSON format)
- GCP Project ID

You can obtain these by:
1. Going to the [Google Cloud Console](https://console.cloud.google.com/)
2. Creating a new project or selecting an existing one
3. Navigating to IAM & Admin > Service Accounts
4. Creating a new service account
5. Granting the service account the `Storage Admin` role (or more restrictive role as needed)
6. Creating a key for the service account (JSON format)
7. Downloading the JSON key file

### 2. Create a GCS Bucket
You'll need a GCS bucket for testing. You can:
- Use the Google Cloud Console to create a bucket
- Use gsutil: `gsutil mb gs://your-bucket-name`
- Let the application create it automatically (the GCPStorage class will attempt to create the bucket if it doesn't exist)

### 3. Configure Environment Variables
Add the following to your `.env` file:

```env
# GCP Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCP_PROJECT_ID=your-gcp-project-id
GCP_STORAGE_BUCKET_NAME=your-gcp-test-bucket
GCP_BIGQUERY_DATASET=document_analytics
```

## Testing the Configuration

Once you've configured your credentials, you can test the storage connections using the provided test scripts:

### Run the Storage Tests
```bash
python test_storage.py
```

### Run a Manual Connection Test
You can also create a simple test script to verify connections:

```python
#!/usr/bin/env python3
"""Manual storage connection test."""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_aws_connection():
    """Test AWS S3 connection."""
    print("Testing AWS S3 connection...")
    try:
        from src.storage import StorageFactory
        
        # Create S3 storage instance
        storage = StorageFactory.create_storage(
            'aws_s3',
            os.getenv('AWS_S3_BUCKET_NAME'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
        
        # Test basic operations
        print(f"✓ Connected to S3 bucket: {storage.bucket_name}")
        
        # Test listing files (should work even if bucket is empty)
        files = storage.list_files()
        print(f"✓ Listed {len(files)} files in bucket")
        
        return True
    except Exception as e:
        print(f"✗ AWS S3 connection failed: {e}")
        return False

def test_gcp_connection():
    """Test GCP Cloud Storage connection."""
    print("Testing GCP Cloud Storage connection...")
    try:
        from src.storage import StorageFactory
        
        # Create GCP storage instance
        storage = StorageFactory.create_storage(
            'gcp',
            os.getenv('GCP_STORAGE_BUCKET_NAME'),
            project_id=os.getenv('GCP_PROJECT_ID'),
            credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        )
        
        # Test basic operations
        print(f"✓ Connected to GCS bucket: {storage.bucket_name}")
        
        # Test listing files (should work even if bucket is empty)
        files = storage.list_files()
        print(f"✓ Listed {len(files)} files in bucket")
        
        return True
    except Exception as e:
        print(f"✗ GCP Cloud Storage connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Cloud Storage Connection Test ===\n")
    
    aws_success = test_aws_connection()
    print()
    gcp_success = test_gcp_connection()
    
    print("\n" + "="*50)
    if aws_success and gcp_success:
        print("✓ All cloud storage connections successful!")
    elif aws_success:
        print("✓ AWS S3 connection successful")
        print("✗ GCP Cloud Storage connection failed")
    elif gcp_success:
        print("✗ AWS S3 connection failed")
        print("✓ GCP Cloud Storage connection successful")
    else:
        print("✗ All cloud storage connections failed!")
```

## Security Notes

1. **Never commit credentials to version control**: The `.env` file should be added to `.gitignore` (which it already is in this project)
2. **Use least privilege principles**: Create service accounts/users with only the permissions needed for testing
3. **Rotate credentials regularly**: Especially if you're using these in any kind of persistent environment
4. **Consider using AWS IAM roles or GCP Workload Identity** for production deployments instead of static keys

## Troubleshooting

### Common AWS Issues
- **Invalid credentials**: Double-check your access key ID and secret access key
- **Bucket permissions**: Ensure your user has permission to create buckets or that the bucket exists
- **Region mismatches**: Make sure your region matches where you're creating/accessing buckets
- **Network issues**: Ensure you can reach AWS endpoints from your network

### Common GCP Issues
- **Authentication errors**: Verify your service account key file path is correct and the file is valid
- **Permission denied**: Ensure your service account has sufficient permissions (Storage Admin is recommended for testing)
- **Project not found**: Verify your project ID is correct and the service account has access to it
- **API not enabled**: Make sure the Cloud Storage API is enabled for your GCP project

## Next Steps

Once you have your cloud storage connections working, you can:
1. Test the full document processing pipeline with cloud storage integration
2. Test the RAG system with documents stored in the cloud
3. Build API endpoints that leverage cloud storage for document processing
4. Create automated backup/archival solutions using the storage abstractions