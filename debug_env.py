#!/usr/bin/env python3
"""Debug environment variable loading."""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=== Environment Variables Related to AWS/Supabase ===")
aws_vars = [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_S3_BUCKET_NAME',
    'AWS_DEFAULT_REGION',
    'AWS_ENDPOINT_URL'
]

for var in aws_vars:
    value = os.getenv(var)
    if value:
        # Show first and last few chars for security
        if len(value) > 10:
            display_value = value[:4] + "*" * (len(value)-8) + value[-4:]
        else:
            display_value = "****"
        print(f"{var}: {display_value} (set)")
    else:
        print(f"{var}: NOT SET")

print("\n=== Supabase Variables ===")
supabase_vars = [
    'SUPABASE_PROJECT_URL',
    'SUPABASE_SERVICE_ROLE_KEY',
    'SUPABASE_STORAGE_BUCKET'
]

for var in supabase_vars:
    value = os.getenv(var)
    if value:
        # Show first and last few chars for security
        if len(value) > 10:
            display_value = value[:4] + "*" * (len(value)-8) + value[-4:]
        else:
            display_value = "****"
        print(f"{var}: {display_value} (set)")
    else:
        print(f"{var}: NOT SET")