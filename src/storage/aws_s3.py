"""AWS S3 storage implementation."""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import BinaryIO, Optional, List
import logging
import os

from .base import BaseStorage, StorageFactory

logger = logging.getLogger(__name__)


class S3Storage(BaseStorage):
    """AWS S3 storage implementation."""

    def __init__(self, bucket_name: str, aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None, region_name: str = 'us-east-1',
                 endpoint_url: Optional[str] = None):
        """
        Initialize AWS S3 storage.

        Args:
            bucket_name: Name of the S3 bucket
            aws_access_key_id: AWS access key ID (optional, uses default credentials if not provided)
            aws_secret_access_key: AWS secret access key (optional, uses default credentials if not provided)
            region_name: AWS region name (default: us-east-1)
            endpoint_url: Custom endpoint URL (optional, for S3-compatible services)
        """
        super().__init__(bucket_name)
        self.region_name = region_name

        try:
            if aws_access_key_id and aws_secret_access_key:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name,
                    endpoint_url=endpoint_url
                )
            else:
                # Use default credentials (from environment, ~/.aws/credentials, or IAM role)
                self.s3_client = boto3.client('s3', region_name=region_name, endpoint_url=endpoint_url)

            # Verify bucket exists or create it
            self._ensure_bucket_exists()
            self.logger.info(f"S3 storage initialized for bucket: {bucket_name} in region: {region_name}")

        except NoCredentialsError:
            self.logger.error("AWS credentials not found. Please configure AWS credentials.")
            raise
        except Exception as e:
            self.logger.error(f"Failed to initialize S3 storage: {e}")
            raise

    def _ensure_bucket_exists(self) -> None:
        """Ensure the S3 bucket exists, create it if it doesn't."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            self.logger.debug(f"Bucket {self.bucket_name} already exists")
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                # Bucket doesn't exist, create it
                self.logger.info(f"Bucket {self.bucket_name} does not exist, creating...")
                try:
                    if self.region_name == 'us-east-1':
                        # us-east-1 doesn't need CreateBucketConfiguration
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region_name}
                        )
                    self.logger.info(f"Bucket {self.bucket_name} created successfully")
                except ClientError as create_error:
                    self.logger.error(f"Failed to create bucket {self.bucket_name}: {create_error}")
                    raise
            elif error_code == 403:
                # Forbidden - might not have permission to check bucket existence
                # but credentials might still be valid for other operations
                self.logger.warning(f"Forbidden access to bucket {self.bucket_name}. "
                                  f"Assuming bucket exists and continuing with limited permissions.")
            else:
                # Some other error
                self.logger.error(f"Error checking bucket {self.bucket_name}: {e}")
                raise

    def upload_file(self, file_path: str, object_key: Optional[str] = None) -> bool:
        """
        Upload a file to S3.

        Args:
            file_path: Local path to the file to upload
            object_key: Optional key/object name in S3 (defaults to filename)

        Returns:
            True if upload successful, False otherwise
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False

        if object_key is None:
            object_key = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_key)
            self.logger.info(f"Uploaded {file_path} to s3://{self.bucket_name}/{object_key}")
            return True
        except FileNotFoundError:
            self.logger.error(f"File not found: {file_path}")
            return False
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return False
        except ClientError as e:
            self.logger.error(f"Failed to upload {file_path} to S3: {e}")
            return False

    def download_file(self, object_key: str, file_path: str) -> bool:
        """
        Download a file from S3.

        Args:
            object_key: Key/object name in S3
            file_path: Local path where file should be saved

        Returns:
            True if download successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

            self.s3_client.download_file(self.bucket_name, object_key, file_path)
            self.logger.info(f"Downloaded s3://{self.bucket_name}/{object_key} to {file_path}")
            return True
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return False
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                self.logger.error(f"File not found in S3: s3://{self.bucket_name}/{object_key}")
            else:
                self.logger.error(f"Failed to download from S3: {e}")
            return False

    def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from S3.

        Args:
            object_key: Key/object name in S3

        Returns:
            True if deletion successful, False otherwise
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            self.logger.info(f"Deleted s3://{self.bucket_name}/{object_key}")
            return True
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return False
        except ClientError as e:
            self.logger.error(f"Failed to delete from S3: {e}")
            return False

    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """
        List files in S3 bucket.

        Args:
            prefix: Optional prefix to filter objects

        Returns:
            List of object keys
        """
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=prefix or '')

            keys = []
            for page in page_iterator:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        keys.append(obj['Key'])

            self.logger.debug(f"Listed {len(keys)} objects from bucket {self.bucket_name}")
            return keys
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return []
        except ClientError as e:
            self.logger.error(f"Failed to list objects from S3: {e}")
            return []

    def file_exists(self, object_key: str) -> bool:
        """
        Check if a file exists in S3.

        Args:
            object_key: Key/object name in S3

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return False
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                return False
            else:
                self.logger.error(f"Error checking file existence: {e}")
                return False

    def get_file_url(self, object_key: str, expiration: int = 3600) -> Optional[str]:
        """
        Get a presigned URL for accessing a file in S3.

        Args:
            object_key: Key/object name in S3
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL string or None if not supported
        """
        try:
            if not self.file_exists(object_key):
                self.logger.warning(f"File does not exist: s3://{self.bucket_name}/{object_key}")
                return None

            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expiration
            )
            self.logger.debug(f"Generated presigned URL for s3://{self.bucket_name}/{object_key}")
            return url
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return None
        except ClientError as e:
            self.logger.error(f"Failed to generate presigned URL: {e}")
            return None

    def upload_fileobj(self, file_obj: BinaryIO, object_key: str) -> bool:
        """
        Upload a file-like object to S3.

        Args:
            file_obj: File-like object to upload
            object_key: Key/object name in S3

        Returns:
            True if upload successful, False otherwise
        """
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_key)
            self.logger.info(f"Uploaded fileobj to s3://{self.bucket_name}/{object_key}")
            return True
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return False
        except ClientError as e:
            self.logger.error(f"Failed to upload fileobj to S3: {e}")
            return False

    def download_fileobj(self, object_key: str, file_obj: BinaryIO) -> bool:
        """
        Download a file from S3 to a file-like object.

        Args:
            object_key: Key/object name in S3
            file_obj: File-like object to write to

        Returns:
            True if download successful, False otherwise
        """
        try:
            self.s3_client.download_fileobj(self.bucket_name, object_key, file_obj)
            self.logger.info(f"Downloaded s3://{self.bucket_name}/{object_key} to fileobj")
            return True
        except NoCredentialsError:
            self.logger.error("AWS credentials not available")
            return False
        except ClientError as e:
            self.logger.error(f"Failed to download fileobj from S3: {e}")
            return False