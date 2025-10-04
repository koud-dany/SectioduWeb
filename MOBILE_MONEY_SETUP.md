# Mobile Money Testing Setup Guide

## Overview
This app now uses Mobile Money instead of Stripe for payments. For testing, you need to set up MTN Mobile Money sandbox credentials.

## MTN Mobile Money Sandbox Setup

### Step 1: Register for MTN Developer Account
1. Go to https://momodeveloper.mtn.com/
2. Sign up for a developer account
3. Create a new app/product

### Step 2: Get Sandbox Credentials
After creating your app, you'll get:
- `Ocp-Apim-Subscription-Key` (Primary Key)
- API User ID
- API Key

### Step 3: Create API User (Important!)
You need to create an API user in the sandbox:

```bash
# 1. Create API User
curl -X POST \
  https://sandbox.momodeveloper.mtn.com/v1_0/apiuser \
  -H 'Content-Type: application/json' \
  -H 'X-Reference-Id: YOUR_UUID_HERE' \
  -H 'Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY' \
  -d '{
    "providerCallbackHost": "your-app-domain.com"
  }'

# 2. Create API Key for the user
curl -X POST \
  https://sandbox.momodeveloper.mtn.com/v1_0/apiuser/YOUR_UUID_HERE/apikey \
  -H 'Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY'
```

### Step 4: Configure Environment Variables
Set these in your Render Secret Files (.env):

```
MTN_MOMO_API_USER=your-uuid-from-step3
MTN_MOMO_API_KEY=your-api-key-from-step3
MTN_MOMO_SUBSCRIPTION_KEY=your-subscription-key-from-step2
PAYMENT_METHOD=mobile_money
SECRET_KEY=your-secret-key
```

## Test Phone Numbers

Use these MTN test numbers for different scenarios:

- `46733123450` - Payment will succeed
- `46733123451` - Payment will be pending
- `46733123452` - Payment will fail

## Testing Steps

1. Go to `/upgrade` page
2. Click "Pay with Mobile Money"
3. Select "MTN MoMo"
4. Enter test phone number: `46733123450`
5. Click "Pay $35"
6. Check payment status

## Debugging

- Check `/debug/payment_config` endpoint to verify configuration
- Look at server logs for detailed API request/response info
- Ensure all environment variables are set correctly

## Production Setup

For production:
1. Get live MTN MoMo credentials
2. Update base URLs to production endpoints
3. Set `PAYMENT_METHOD=mobile_money` in production environment
4. Use real phone numbers in production

## Alternative Providers

The system is designed to support:
- MTN Mobile Money (implemented)
- Orange Money (placeholder)
- Airtel Money (placeholder)

Additional providers can be implemented by extending the `MobileMoneyService` class.
