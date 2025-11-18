# Amazon S3 Integration for Image Storage

## Overview
This application now supports Amazon S3 for storing user avatars, video thumbnails, and other images. S3 provides scalable, reliable cloud storage that works seamlessly with deployment platforms like Render.

## Features Implemented

### 1. **S3 Storage Service** (`s3_storage.py`)
- Full-featured S3 upload/download/delete functionality
- Automatic content type detection
- Public URL generation for uploaded files
- Error handling and fallback mechanisms

### 2. **Image Upload Functions** (Updated in `app.py`)
- `upload_image_to_storage()`: Universal image upload function
- `get_image_url()`: Smart URL generation (works with S3 or local storage)
- Automatic fallback to local storage if S3 is unavailable

### 3. **Profile Avatar Integration**
- User avatars now upload to S3 when configured
- Automatic fallback to local storage
- Updated templates to display S3-hosted images

## Configuration

### Environment Variables
Add these to your `.env` file or Render environment variables:

```env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_BUCKET_NAME=videovote-uploads
AWS_REGION=us-east-1

# Enable cloud storage
USE_CLOUD_STORAGE=true
```

### AWS S3 Setup Steps

#### 1. Create an AWS Account
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Follow the registration process

#### 2. Create an S3 Bucket
1. Go to AWS Console → S3
2. Click "Create bucket"
3. Choose a unique bucket name (e.g., `videovote-uploads`)
4. Select a region (e.g., `us-east-1`)
5. **Uncheck** "Block all public access" (we need public read for images)
6. Acknowledge the warning
7. Click "Create bucket"

#### 3. Configure Bucket Permissions
1. Click on your bucket name
2. Go to "Permissions" tab
3. Scroll to "Bucket policy"
4. Click "Edit" and add this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::videovote-uploads/*"
        }
    ]
}
```

**Replace `videovote-uploads` with your actual bucket name**

#### 4. Create IAM User for API Access
1. Go to AWS Console → IAM
2. Click "Users" → "Add users"
3. Username: `videovote-app` (or your choice)
4. Select "Access key - Programmatic access"
5. Click "Next: Permissions"
6. Click "Attach existing policies directly"
7. Search for and select `AmazonS3FullAccess`
8. Click "Next" through to "Create user"
9. **IMPORTANT**: Copy the Access Key ID and Secret Access Key
   - You won't be able to see the secret key again!

#### 5. Configure Environment Variables

**For Local Development (.env file):**
```env
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_BUCKET_NAME=videovote-uploads
AWS_REGION=us-east-1
USE_CLOUD_STORAGE=true
```

**For Render Deployment:**
1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add the following environment variables:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_BUCKET_NAME`
   - `AWS_REGION`
   - `USE_CLOUD_STORAGE=true`
5. Click "Save Changes"

## Usage Examples

### Upload User Avatar
```python
from flask import request
from s3_storage import s3_storage

# In your route handler
if 'avatar' in request.files:
    avatar = request.files['avatar']
    result = upload_image_to_storage(
        avatar,
        'avatars',      # Folder name
        'avatar',       # File prefix
        user_id         # User ID for unique naming
    )
    
    if result['success']:
        avatar_url = result['url']
        avatar_filename = result['filename']
        # Save filename to database
    else:
        print(f"Upload failed: {result['error']}")
```

### Get Image URL in Templates
```html
<!-- Automatically works with S3 or local storage -->
<img src="{{ get_image_url(avatar_filename, 'avatars') }}" alt="Avatar">
```

### Direct S3 Operations
```python
from s3_storage import s3_storage

# Upload a file
result = s3_storage.upload_file(
    '/path/to/local/file.jpg',
    'images/photo.jpg',  # S3 key
    content_type='image/jpeg'
)

# Get public URL
url = s3_storage.get_file_url('images/photo.jpg')

# Delete a file
s3_storage.delete_file('images/photo.jpg')
```

## Folder Structure in S3

```
videovote-uploads/
├── avatars/
│   ├── user_1_avatar.jpg
│   ├── user_2_avatar.png
│   └── ...
├── thumbnails/
│   ├── video_1_thumb.jpg
│   └── ...
└── uploads/
    └── (videos - if needed)
```

## Fallback Behavior

The application intelligently handles storage:

1. **If S3 is configured and available**: Uploads go to S3
2. **If S3 fails or is unavailable**: Falls back to local storage
3. **Templates work with both**: `get_image_url()` automatically detects storage type

## Security Best Practices

### 1. Protect Your Credentials
- Never commit `.env` file to git
- Use environment variables in production
- Rotate access keys regularly

### 2. IAM Permissions
For production, create a more restricted IAM policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::videovote-uploads",
                "arn:aws:s3:::videovote-uploads/*"
            ]
        }
    ]
}
```

### 3. CORS Configuration (if needed for direct uploads)
In your S3 bucket → Permissions → CORS:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["https://your-domain.com"],
        "ExposeHeaders": []
    }
]
```

## Troubleshooting

### Images not uploading to S3
1. Check environment variables are set correctly
2. Verify IAM user has S3 permissions
3. Check bucket policy allows public read
4. Look at application logs for error messages

### 403 Forbidden errors
- Bucket policy not configured correctly
- IAM user lacks permissions
- Check bucket is not blocking public access

### Images not displaying
- Verify bucket policy allows `GetObject`
- Check CORS configuration if loading from different domain
- Ensure `USE_CLOUD_STORAGE=true` is set

## Cost Considerations

AWS S3 Pricing (as of 2024):
- **Storage**: $0.023 per GB/month
- **GET Requests**: $0.0004 per 1,000 requests
- **PUT Requests**: $0.005 per 1,000 requests
- **Data Transfer Out**: First 100 GB free, then $0.09/GB

For a typical video voting app with ~1000 users:
- Storage: ~10 GB = $0.23/month
- Requests: ~100K/month = $0.04/month
- **Total**: ~$0.27/month

## Testing

Install dependencies and test:

```bash
# Install boto3
pip install boto3

# Test S3 connection
python -c "from s3_storage import s3_storage; print('Available:', s3_storage.is_available())"
```

## Migration from Local Storage

To migrate existing images to S3:

```python
import os
from s3_storage import s3_storage

def migrate_local_to_s3(local_folder, s3_prefix):
    """Migrate local images to S3"""
    local_path = f"static/{local_folder}"
    
    for filename in os.listdir(local_path):
        file_path = os.path.join(local_path, filename)
        s3_key = f"{s3_prefix}/{filename}"
        
        result = s3_storage.upload_file(file_path, s3_key)
        if result['success']:
            print(f"✅ Migrated: {filename}")
        else:
            print(f"❌ Failed: {filename} - {result['error']}")

# Migrate avatars
migrate_local_to_s3('avatars', 'avatars')
```

## Support

For issues or questions:
1. Check application logs
2. Verify AWS credentials and permissions
3. Review bucket configuration
4. Check environment variables

## Future Enhancements

- [ ] Direct browser upload to S3 (pre-signed URLs)
- [ ] Image optimization before upload
- [ ] CloudFront CDN integration
- [ ] Automatic backup to secondary region
- [ ] Image thumbnail generation
