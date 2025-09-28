# Stripe Configuration Instructions

To enable payment processing, you need to set up your Stripe API keys:

## 1. Get Stripe API Keys
- Sign up at https://stripe.com
- Go to your Stripe Dashboard
- Navigate to Developers > API keys
- Copy your Publishable key and Secret key

## 2. Create Stripe Configuration File
- Copy `stripe_config.py.example` to `stripe_config.py`
- Replace the placeholder keys with your actual Stripe API keys:
```python
# In stripe_config.py
STRIPE_PUBLISHABLE_KEY_TEST = "pk_test_your_actual_test_key_here"
STRIPE_SECRET_KEY_TEST = "sk_test_your_actual_test_key_here"

# For production (optional)
STRIPE_PUBLISHABLE_KEY_LIVE = "pk_live_your_actual_live_key_here"
STRIPE_SECRET_KEY_LIVE = "sk_live_your_actual_live_key_here"
```

## 3. Alternative: Environment Variables (Recommended for Production)
Set environment variables (these will override the config file):
```bash
# Windows
set STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
set STRIPE_SECRET_KEY=sk_test_your_secret_key_here

# Linux/Mac
export STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
export STRIPE_SECRET_KEY=sk_test_your_secret_key_here
```

## 4. Test Payment
- Use Stripe test card numbers for testing:
  - Visa: 4242 4242 4242 4242
  - Any future expiry date (e.g., 12/25)
  - Any 3-digit CVC

## 5. Production Setup
- Use live keys (pk_live_... and sk_live_...) for production
- Set up proper webhook handling for production reliability
- Configure proper SSL/HTTPS
