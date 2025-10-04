#!/usr/bin/env python3
"""
MTN MoMo Sandbox Setup Script
Run this script to create API user and key for testing
"""

import requests
import uuid
import json

# Configuration
SUBSCRIPTION_KEY = "4842e41f28e44ed5b43f629dd9785b41"  # Your MTN MoMo Primary Key
BASE_URL = "https://sandbox.momodeveloper.mtn.com"
CALLBACK_HOST = "webhook.site"  # You can use any domain for testing

def create_api_user():
    """Create API user for MTN MoMo sandbox"""
    
    # Generate a UUID for the API user
    api_user_id = str(uuid.uuid4())
    
    # Create API user
    url = f"{BASE_URL}/v1_0/apiuser"
    headers = {
        'X-Reference-Id': api_user_id,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    
    payload = {
        'providerCallbackHost': CALLBACK_HOST
    }
    
    print(f"Creating API user with ID: {api_user_id}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("✅ API user created successfully!")
        
        # Create API key for the user
        key_url = f"{BASE_URL}/v1_0/apiuser/{api_user_id}/apikey"
        key_headers = {
            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
        }
        
        print("Creating API key...")
        key_response = requests.post(key_url, headers=key_headers)
        
        if key_response.status_code == 201:
            api_key = key_response.json().get('apiKey')
            print("✅ API key created successfully!")
            
            print("\n" + "="*50)
            print("🎉 SETUP COMPLETE!")
            print("="*50)
            print(f"MTN_MOMO_API_USER = \"{api_user_id}\"")
            print(f"MTN_MOMO_API_KEY = \"{api_key}\"")
            print(f"MTN_MOMO_SUBSCRIPTION_KEY = \"{SUBSCRIPTION_KEY}\"")
            print("="*50)
            print("\n📝 Copy these values to your mobile_money_config.py file")
            print("🌐 Or set them as environment variables in Render")
            
            return api_user_id, api_key
        else:
            print(f"❌ Failed to create API key: {key_response.status_code}")
            print(f"Response: {key_response.text}")
            return None, None
    else:
        print(f"❌ Failed to create API user: {response.status_code}")
        print(f"Response: {response.text}")
        return None, None

def test_credentials(api_user, api_key):
    """Test the created credentials"""
    print("\n🧪 Testing credentials...")
    
    # Test by getting access token
    token_url = f"{BASE_URL}/collection/token/"
    
    import base64
    auth_string = f"{api_user}:{api_key}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Authorization': f'Basic {encoded_auth}'
    }
    
    response = requests.post(token_url, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("✅ Credentials test successful!")
        print(f"Access token received: {token[:20]}...")
        return True
    else:
        print(f"❌ Credentials test failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    print("🚀 MTN MoMo Sandbox Setup")
    print("="*50)
    
    if SUBSCRIPTION_KEY == "YOUR_PRIMARY_KEY_FROM_MTN_PORTAL":
        print("❌ Please update SUBSCRIPTION_KEY with your actual key from MTN Developer Portal")
        exit(1)
    
    api_user, api_key = create_api_user()
    
    if api_user and api_key:
        test_credentials(api_user, api_key)
        print("\n✅ Setup complete! You can now use mobile money payments.")
    else:
        print("\n❌ Setup failed. Please check your subscription key and try again.")
