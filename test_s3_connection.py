"""
Test Amazon S3 Storage Connection
Run this script to verify your S3 configuration
"""
import os
from s3_storage import s3_storage
from config import Config

def test_s3_connection():
    """Test S3 connectivity and configuration"""
    print("=" * 60)
    print("Amazon S3 Storage Connection Test")
    print("=" * 60)
    print()
    
    # Check configuration
    print("1. Checking Configuration...")
    print(f"   AWS Access Key ID: {'✅ Set' if Config.AWS_ACCESS_KEY_ID else '❌ Not set'}")
    print(f"   AWS Secret Key: {'✅ Set' if Config.AWS_SECRET_ACCESS_KEY else '❌ Not set'}")
    print(f"   AWS Bucket Name: {Config.AWS_BUCKET_NAME}")
    print(f"   AWS Region: {Config.AWS_REGION}")
    print(f"   Cloud Storage Enabled: {Config.USE_CLOUD_STORAGE}")
    print()
    
    # Check S3 availability
    print("2. Checking S3 Service Availability...")
    if s3_storage.is_available():
        print("   ✅ S3 service is available and ready")
    else:
        print("   ❌ S3 service is not available")
        print("   Please check your AWS credentials in .env or environment variables")
        return False
    print()
    
    # Test upload
    print("3. Testing File Upload...")
    try:
        # Create a test file
        test_filename = 'test_upload.txt'
        with open(test_filename, 'w') as f:
            f.write('This is a test file for S3 upload verification.')
        
        # Upload to S3
        s3_key = 'test/test_upload.txt'
        result = s3_storage.upload_file(
            test_filename,
            s3_key,
            content_type='text/plain'
        )
        
        # Clean up local test file
        os.remove(test_filename)
        
        if result['success']:
            print("   ✅ Upload successful!")
            print(f"   📍 File URL: {result['url']}")
            
            # Test delete
            print()
            print("4. Testing File Deletion...")
            delete_result = s3_storage.delete_file(s3_key)
            
            if delete_result['success']:
                print("   ✅ Deletion successful!")
                print()
                print("=" * 60)
                print("🎉 All tests passed! S3 is configured correctly.")
                print("=" * 60)
                return True
            else:
                print(f"   ❌ Deletion failed: {delete_result['error']}")
                return False
        else:
            print(f"   ❌ Upload failed: {result['error']}")
            print()
            print("Common issues:")
            print("   - Invalid AWS credentials")
            print("   - Bucket does not exist")
            print("   - Insufficient IAM permissions")
            print("   - Incorrect region")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed with exception: {str(e)}")
        return False

if __name__ == '__main__':
    try:
        success = test_s3_connection()
        
        if not success:
            print()
            print("Troubleshooting Steps:")
            print("1. Create an S3 bucket in AWS Console")
            print("2. Create an IAM user with S3 permissions")
            print("3. Add credentials to .env file:")
            print("   AWS_ACCESS_KEY_ID=your_key")
            print("   AWS_SECRET_ACCESS_KEY=your_secret")
            print("   AWS_BUCKET_NAME=your_bucket_name")
            print("   AWS_REGION=us-east-1")
            print()
            print("See S3_SETUP_GUIDE.md for detailed instructions.")
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        print()
        print("Please ensure:")
        print("1. boto3 is installed: pip install boto3")
        print("2. .env file exists with AWS credentials")
        print("3. config.py is properly configured")
