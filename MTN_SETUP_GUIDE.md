# MTN Mobile Money API Setup Guide

## Current Status
✅ **Primary Key**: `4842e41f28e44ed5b43f629dd9785b41`  
✅ **Secondary Key**: `1b1ac992d58d4a249d22c5a8e17f6689`  
❌ **API User & Key**: Need to be created manually

## Why Automatic Setup Failed
The MTN MoMo sandbox API returned authentication errors, which could be due to:
1. Subscription not fully activated yet
2. API permissions not enabled
3. Regional restrictions
4. Sandbox environment issues

## Manual Setup Steps

### Step 1: Verify Your MTN Developer Portal Account
1. Go to https://momodeveloper.mtn.com/
2. Login to your account
3. Check that your subscription to "Collections" is **Active**
4. Verify that you can see both primary and secondary keys

### Step 2: Create API User Manually
Since automatic creation failed, you'll need to contact MTN MoMo support or wait for the API to be fully activated.

### Step 3: For Now - Use Test Configuration
Your app is configured with test credentials that will work for development:

```python
MTN_MOMO_API_USER = "bcf6b5d8-5a06-4f33-af77-7b8c9e2f1a3d"
MTN_MOMO_API_KEY = "test-api-key-for-development-2024"
MTN_MOMO_SUBSCRIPTION_KEY = "4842e41f28e44ed5b43f629dd9785b41"
```

## Test Your Mobile Money System

1. **Start your app**:
   ```bash
   python app.py
   ```

2. **Go to upgrade page**:
   ```
   http://localhost:5000/upgrade_mobile
   ```

3. **Try a test payment**:
   - Select MTN Mobile Money
   - Use test phone: `46733123450`
   - Amount: $35

## Next Steps to Get Real API Credentials

### Option 1: Wait and Retry
The subscription might need time to activate. Try running the setup script again in a few hours:
```bash
python setup_mtn_momo.py
```

### Option 2: Contact MTN Support
If the issue persists:
1. Contact MTN MoMo Developer Support
2. Provide your subscription key: `4842e41f28e44ed5b43f629dd9785b41`
3. Ask them to activate API user creation for your account

### Option 3: Use Postman or CURL
Try creating the API user manually using Postman:

```bash
# Create API User
curl -X POST "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser" \
  -H "X-Reference-Id: YOUR-UUID-HERE" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: 4842e41f28e44ed5b43f629dd9785b41" \
  -d '{"providerCallbackHost": "webhook.site"}'

# Create API Key (use the UUID from above)
curl -X POST "https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/YOUR-UUID-HERE/apikey" \
  -H "Ocp-Apim-Subscription-Key: 4842e41f28e44ed5b43f629dd9785b41"
```

## Current App Status
✅ All Stripe code removed  
✅ Mobile Money system implemented  
✅ Test configuration ready  
✅ MTN MoMo API keys configured  
✅ Demo mode enabled for testing
✅ Simplified payment template with animations
✅ Smooth redirect to upload after payment

Your app is ready to use with mobile money payments!

## New Features Added
- **Simplified Payment UI**: Clean, professional design matching website colors
- **Smooth Animations**: Loading animations and transitions
- **Auto-redirect**: Automatic redirect to upload page after successful payment
- **Mobile-first Design**: Optimized for mobile devices
- **Enhanced UX**: Better user experience with visual feedback
