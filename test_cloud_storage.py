#!/usr/bin/env python3
"""
Test script for cloud storage functionality
"""
import requests
import json

def test_video_files_debug():
    """Test the video files debug endpoint"""
    try:
        # You'll need to be logged in to access this endpoint
        print("Testing video files debug endpoint...")
        print("Note: You need to log in first through the web interface")
        print("Then visit: http://127.0.0.1:5000/debug/video_files")
        print()
        
        # Check if requests work
        response = requests.get("http://127.0.0.1:5000")
        if response.status_code == 200:
            print("✅ Flask app is running and accessible")
        else:
            print(f"❌ Flask app returned status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on port 5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_cloud_storage_config():
    """Test cloud storage configuration"""
    print("Testing cloud storage configuration...")
    
    # Import the config to check values
    try:
        import os
        from config import Config
        
        print(f"CLOUDINARY_CLOUD_NAME: {getattr(Config, 'CLOUDINARY_CLOUD_NAME', 'Not set')}")
        print(f"USE_CLOUD_STORAGE: {getattr(Config, 'USE_CLOUD_STORAGE', 'Not set')}")
        print(f"RENDER environment variable: {os.environ.get('RENDER', 'Not set')}")
        
        # Test should_use_cloud_storage logic
        from app import should_use_cloud_storage
        print(f"should_use_cloud_storage(): {should_use_cloud_storage()}")
        
    except Exception as e:
        print(f"❌ Error importing config: {e}")

if __name__ == "__main__":
    print("🧪 Testing Cloud Storage Setup")
    print("=" * 40)
    
    test_cloud_storage_config()
    print()
    test_video_files_debug()
    
    print()
    print("💡 Next steps:")
    print("1. Log in to the app through the web interface")
    print("2. Upload a video to test the cloud storage functionality")
    print("3. Visit /debug/video_files to see file status")
    print("4. Set up Cloudinary credentials in config.py for cloud storage")
