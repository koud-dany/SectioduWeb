# Mobile Money Configuration
# Store your mobile money API keys and configuration here

# MTN Mobile Money Configuration (Sandbox/Test)
# IMPORTANT: Replace these with real credentials from MTN Developer Portal
# Follow these steps:
# 1. Go to https://momodeveloper.mtn.com/
# 2. Register and subscribe to Collection API
# 3. Run setup_mtn_momo.py script to get your credentials
MTN_MOMO_API_USER = "bcf6b5d8-5a06-4f33-af77-7b8c9e2f1a3d"  # Test UUID for development
MTN_MOMO_API_KEY = "test-api-key-for-development-2024"      # Test API key for development  
MTN_MOMO_SUBSCRIPTION_KEY = "4842e41f28e44ed5b43f629dd9785b41" # Your Primary key from MTN portal
MTN_MOMO_BASE_URL = "https://sandbox.momodeveloper.mtn.com"  # Use production URL for live

# MTN MoMo Test Phone Numbers (use these for testing)
MTN_TEST_PHONE_NUMBERS = [
    "46733123450",  # Success scenario
    "46733123451",  # Pending scenario
    "46733123452",  # Failed scenario
]

# Orange Money Configuration
ORANGE_MONEY_CLIENT_ID = "demo-orange-client-id"
ORANGE_MONEY_CLIENT_SECRET = "demo-orange-client-secret"
ORANGE_MONEY_BASE_URL = "https://api.orange.com/oauth/v3"  # Orange Money API

# Airtel Money Configuration
AIRTEL_MONEY_CLIENT_ID = "demo-airtel-client-id"
AIRTEL_MONEY_CLIENT_SECRET = "demo-airtel-client-secret"
AIRTEL_MONEY_BASE_URL = "https://openapiuat.airtel.africa"  # Use production URL for live

# Demo Mode Configuration
DEMO_MODE = True  # Always run in demo mode for testing

# Payment Configuration
PAYMENT_AMOUNT = 35  # $35 equivalent in local currency
PAYMENT_CURRENCY = "USD"  # Change to local currency (XOF, XAF, UGX, etc.)
PAYMENT_DESCRIPTION = "Video Tournament Entry Fee"

# Helper function to get mobile money configuration
def get_mobile_money_config():
    return {
        'mtn_momo': {
            'api_user': MTN_MOMO_API_USER,
            'api_key': MTN_MOMO_API_KEY,
            'subscription_key': MTN_MOMO_SUBSCRIPTION_KEY,
            'base_url': MTN_MOMO_BASE_URL
        },
        'orange_money': {
            'client_id': ORANGE_MONEY_CLIENT_ID,
            'client_secret': ORANGE_MONEY_CLIENT_SECRET,
            'base_url': ORANGE_MONEY_BASE_URL
        },
        'airtel_money': {
            'client_id': AIRTEL_MONEY_CLIENT_ID,
            'client_secret': AIRTEL_MONEY_CLIENT_SECRET,
            'base_url': AIRTEL_MONEY_BASE_URL
        },
        'payment': {
            'amount': PAYMENT_AMOUNT,
            'currency': PAYMENT_CURRENCY,
            'description': PAYMENT_DESCRIPTION
        },
        'demo_mode': DEMO_MODE,
        'demo_success_rate': 1.0  # 100% success rate in demo mode
    }
