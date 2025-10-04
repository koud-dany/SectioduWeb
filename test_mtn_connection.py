#!/usr/bin/env python3
"""
Simple test to check MTN MoMo API connection
"""

import requests

# Your keys
PRIMARY_KEY = "4842e41f28e44ed5b43f629dd9785b41"
SECONDARY_KEY = "1b1ac992d58d4a249d22c5a8e17f6689"

def test_connection(subscription_key, key_name):
    """Test basic connection to MTN MoMo API"""
    print(f"\n🧪 Testing {key_name}...")
    
    # Try a simple endpoint first
    url = "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/json'
    }
    
    try:
        # Try a GET request first (less intrusive)
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 405:  # Method not allowed is better than 401
            print(f"✅ {key_name} is valid (endpoint exists)")
            return True
        elif response.status_code == 401:
            print(f"❌ {key_name} authentication failed")
            return False
        else:
            print(f"ℹ️  {key_name} - Unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing MTN MoMo API Keys")
    print("="*50)
    
    primary_works = test_connection(PRIMARY_KEY, "Primary Key")
    secondary_works = test_connection(SECONDARY_KEY, "Secondary Key")
    
    if primary_works or secondary_works:
        print("\n✅ At least one key is working!")
        working_key = PRIMARY_KEY if primary_works else SECONDARY_KEY
        print(f"Use this key: {working_key}")
    else:
        print("\n❌ Neither key is working. Please check:")
        print("1. Keys are correctly copied")
        print("2. Subscription is active in MTN Developer Portal")
        print("3. APIs are enabled for your subscription")
