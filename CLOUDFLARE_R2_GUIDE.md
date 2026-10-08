# Cloudflare R2 Configuration Guide

Our storage abstractions can work with Cloudflare R2 since it's S3-compatible! This guide explains how to configure our S3Storage implementation to work with Cloudflare R2.

## Why Cloudflare R2 Works
Cloudflare R2 is designed to be S3-compatible, meaning it supports the same API as Amazon S3. Our S3Storage class can be pointed to any S3-compatible endpoint by overriding the URL.

## Step-by-Step Setup

### 1. Get Your Cloudflare R2 Credentials
1. Sign up/log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Navigate to **R2** in the left sidebar
3. Create a bucket if you haven't already (note the bucket name)
4. Go to **Manage R2 API Tokens**
5. Create an API Token with:
   - Permission to edit the bucket you created
   - Or use Global API Key if preferred (less secure)
6. Note down:
   - **Access Key ID** (from the API token)
   - **Secret Access Key** (from the API token)  
   - **Account ID** (found in your R2 overview, looks like a hash)
   - **Bucket Name** (the name you gave your R2 bucket)

### 2. Configure Environment Variables
Update your `.env` file with these Cloudflare R2 specific variables:

```env
# Cloudflare R2 Configuration
# Note: We use the S3Storage class but point it to Cloudflare's endpoint
CLOUDFLARE_R2_ACCESS_KEY_ID=your_access_key_id_here
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your_secret_access_key_here
CLOUDFLARE_R2_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_R2_BUCKET_NAME=your-bucket-name-here

# Optional: You can still use AWS variable names if preferred
# AWS_ACCESS_KEY_ID=your_access_key_id_here
# AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
# AWS_DEFAULT_REGION=weurope  # Any value works, R2 ignores this
# AWS_S3_BUCKET_NAME=your-bucket-name-here
# AWS_ENDPOINT_URL=https://your-account-id.r2.cloudflarestorage.com
```

### 3. Using Cloudflare R2 in Code
You can use our StorageFactory just like with AWS S3:

```python
from src.storage import StorageFactory

# Method 1: Using explicit Cloudflare R2 variables (recommended)
storage = StorageFactory.create_storage(
    'aws_s3',  # Still use the S3 storage class
    os.getenv('CLOUDFLARE_R2_BUCKET_NAME'),
    aws_access_key_id=os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY'),
    region_name='weurope',  # Required but ignored by R2
    endpoint_url=f"https://{os.getenv('CLOUDFLARE_R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
)

# Method 2: Using AWS variable names with endpoint override (alternative)
# storage = StorageFactory.create_storage(
#     'aws_s3',
#     os.getenv('AWS_S3_BUCKET_NAME'),
#     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
#     region_name=os.getenv('AWS_DEFAULT_REGION', 'weurope'),
#     endpoint_url=os.getenv('AWS_ENDPOINT_URL')  # Set this to your R2 endpoint
# )
```

### 4. Testing Your Configuration
Run the Cloudflare R2 connection test:

```bash
python test_cloudflare_r2.py
```

This will test:
- Connection to your R2 bucket
- Listing files in the bucket
- Uploading a test file
- Verifying file existence
- Generating a presigned URL
- Cleaning up the test file

## Benefits of Using Cloudflare R2
- **S3 Compatible**: Works with our existing S3Storage implementation
- **No Egress Fees**: Unlike AWS S3, Cloudflare R2 doesn't charge for data transfer out
- **Global Performance**: Built on Cloudflare's global network
- **Simple Pricing**: Predictable flat-rate pricing

## Troubleshooting
- **Authentication Errors**: Double-check your Access Key ID and Secret Access Key
- **Endpoint Issues**: Ensure your endpoint URL is correctly formatted as `https://<account-id>.r2.cloudflarestorage.com`
- **Bucket Not Found**: Verify the bucket name is correct and exists in your Cloudflare account
- **Permission Denied**: Make sure your API token has sufficient permissions for the bucket

## Next Steps
Once your Cloudflare R2 connection is working, you can:
1. Test the full document processing pipeline with R2 storage
2. Use the RAG system with documents stored in Cloudflare R2
3. Build API endpoints that leverage R2 for document storage and retrieval
4. Take advantage of R2's lack of egress fees for serving processed documents

You now have enterprise-grade cloud storage experience using a modern, cost-effective S3-compatible service!