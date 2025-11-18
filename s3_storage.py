"""
Amazon S3 Storage Service
Handles all image and video uploads to AWS S3
"""
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from werkzeug.utils import secure_filename
import mimetypes
from config import Config

class S3StorageService:
    """Service for managing uploads to Amazon S3"""
    
    def __init__(self):
        """Initialize S3 client"""
        self.s3_client = None
        self.bucket_name = Config.AWS_BUCKET_NAME
        self.region = Config.AWS_REGION
        
        # Initialize S3 client if credentials are available
        if Config.AWS_ACCESS_KEY_ID and Config.AWS_SECRET_ACCESS_KEY:
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                    region_name=self.region
                )
                print(f"✅ S3 client initialized successfully for bucket: {self.bucket_name}")
            except Exception as e:
                print(f"❌ Failed to initialize S3 client: {str(e)}")
                self.s3_client = None
        else:
            print("⚠️  AWS credentials not found. S3 uploads will not be available.")
    
    def is_available(self):
        """Check if S3 service is available"""
        return self.s3_client is not None
    
    def upload_file(self, file_path, s3_key, content_type=None, public_read=True):
        """
        Upload a file to S3 bucket
        
        Args:
            file_path: Local path to the file to upload
            s3_key: The key (path) to store the file in S3
            content_type: MIME type of the file (auto-detected if None)
            public_read: Whether to make the file publicly readable
            
        Returns:
            dict: {'success': bool, 'url': str, 'error': str}
        """
        if not self.is_available():
            return {
                'success': False,
                'url': None,
                'error': 'S3 service is not available'
            }
        
        try:
            # Auto-detect content type if not provided
            if content_type is None:
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
            
            # Extra arguments for the upload
            extra_args = {
                'ContentType': content_type
            }
            
            # Make file publicly readable if requested
            if public_read:
                extra_args['ACL'] = 'public-read'
            
            # Upload the file
            self.s3_client.upload_file(
                file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs=extra_args
            )
            
            # Construct the public URL
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"
            
            print(f"✅ Successfully uploaded to S3: {s3_key}")
            
            return {
                'success': True,
                'url': url,
                'error': None
            }
            
        except FileNotFoundError:
            error_msg = f"File not found: {file_path}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'url': None,
                'error': error_msg
            }
        except NoCredentialsError:
            error_msg = "AWS credentials not available"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'url': None,
                'error': error_msg
            }
        except ClientError as e:
            error_msg = f"S3 upload failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'url': None,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error during S3 upload: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'url': None,
                'error': error_msg
            }
    
    def upload_avatar(self, file, user_id, filename):
        """
        Upload user avatar to S3
        
        Args:
            file: File object from request.files
            user_id: ID of the user
            filename: Original filename
            
        Returns:
            dict: {'success': bool, 'url': str, 'error': str, 'filename': str}
        """
        try:
            # Secure the filename
            secure_name = secure_filename(filename)
            
            # Create a unique S3 key
            s3_key = f"avatars/user_{user_id}_{secure_name}"
            
            # Save file temporarily
            temp_path = f"temp_{secure_name}"
            file.save(temp_path)
            
            # Upload to S3
            result = self.upload_file(
                temp_path,
                s3_key,
                content_type='image/jpeg' if filename.lower().endswith(('.jpg', '.jpeg')) else None
            )
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Add filename to result
            if result['success']:
                result['filename'] = s3_key
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'url': None,
                'error': str(e),
                'filename': None
            }
    
    def upload_video_thumbnail(self, file, video_id, filename):
        """
        Upload video thumbnail to S3
        
        Args:
            file: File object from request.files
            video_id: ID of the video
            filename: Original filename
            
        Returns:
            dict: {'success': bool, 'url': str, 'error': str, 'filename': str}
        """
        try:
            # Secure the filename
            secure_name = secure_filename(filename)
            
            # Create a unique S3 key
            s3_key = f"thumbnails/video_{video_id}_{secure_name}"
            
            # Save file temporarily
            temp_path = f"temp_{secure_name}"
            file.save(temp_path)
            
            # Upload to S3
            result = self.upload_file(
                temp_path,
                s3_key,
                content_type='image/jpeg' if filename.lower().endswith(('.jpg', '.jpeg')) else None
            )
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Add filename to result
            if result['success']:
                result['filename'] = s3_key
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'url': None,
                'error': str(e),
                'filename': None
            }
    
    def delete_file(self, s3_key):
        """
        Delete a file from S3
        
        Args:
            s3_key: The key (path) of the file to delete
            
        Returns:
            dict: {'success': bool, 'error': str}
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'S3 service is not available'
            }
        
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            print(f"✅ Successfully deleted from S3: {s3_key}")
            
            return {
                'success': True,
                'error': None
            }
            
        except ClientError as e:
            error_msg = f"S3 deletion failed: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error during S3 deletion: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }
    
    def get_file_url(self, s3_key):
        """
        Get the public URL for a file in S3
        
        Args:
            s3_key: The key (path) of the file
            
        Returns:
            str: Public URL of the file
        """
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{s3_key}"

# Global instance
s3_storage = S3StorageService()
