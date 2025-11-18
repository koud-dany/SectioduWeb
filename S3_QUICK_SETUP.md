# Quick S3 Setup - Environment Variables

## Add these to your .env file or Render Environment Variables:

```env
# Required S3 Configuration
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_BUCKET_NAME=videovote-uploads
AWS_REGION=us-east-1
USE_CLOUD_STORAGE=true
```

## Quick AWS Setup Checklist:

- [ ] Create AWS account at aws.amazon.com
- [ ] Create S3 bucket with unique name
- [ ] Disable "Block all public access" for the bucket
- [ ] Add bucket policy for public read (see S3_SETUP_GUIDE.md)
- [ ] Create IAM user with programmatic access
- [ ] Attach AmazonS3FullAccess policy to user
- [ ] Copy Access Key ID and Secret Access Key
- [ ] Add credentials to environment variables
- [ ] Run `python test_s3_connection.py` to verify

## Bucket Policy Template:

Replace `YOUR-BUCKET-NAME` with your actual bucket name:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

## Testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Test S3 connection
python test_s3_connection.py
```

## For Render Deployment:

1. Dashboard → Your Service → Environment
2. Add environment variables (click "Add Environment Variable"):
   - Key: `AWS_ACCESS_KEY_ID`, Value: `your_access_key`
   - Key: `AWS_SECRET_ACCESS_KEY`, Value: `your_secret_key`
   - Key: `AWS_BUCKET_NAME`, Value: `your_bucket_name`
   - Key: `AWS_REGION`, Value: `us-east-1`
   - Key: `USE_CLOUD_STORAGE`, Value: `true`
3. Click "Save Changes"
4. Render will automatically redeploy

## Verification:

After deployment, check the logs for:
- ✅ Amazon S3 storage initialized successfully
- ✅ Image uploaded to S3 successfully

## Cost Estimate:

- Storage: $0.023/GB/month
- Requests: Negligible for typical usage
- Expected monthly cost: <$1 for small apps

## Support:

See S3_SETUP_GUIDE.md for detailed instructions and troubleshooting.
