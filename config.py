import os
from dotenv import load_dotenv

# Load environment variables from .env file (Secret Files in Render)
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # Mobile Money Configuration - Load from environment variables (set via .env Secret File in Render)
    MTN_MOMO_API_USER = os.environ.get('MTN_MOMO_API_USER', '')
    MTN_MOMO_API_KEY = os.environ.get('MTN_MOMO_API_KEY', '')
    MTN_MOMO_SUBSCRIPTION_KEY = os.environ.get('MTN_MOMO_SUBSCRIPTION_KEY', '')
    ORANGE_MONEY_CLIENT_ID = os.environ.get('ORANGE_MONEY_CLIENT_ID', '')
    ORANGE_MONEY_CLIENT_SECRET = os.environ.get('ORANGE_MONEY_CLIENT_SECRET', '')
    AIRTEL_MONEY_CLIENT_ID = os.environ.get('AIRTEL_MONEY_CLIENT_ID', '')
    AIRTEL_MONEY_CLIENT_SECRET = os.environ.get('AIRTEL_MONEY_CLIENT_SECRET', '')
    
    # Fallback to local mobile_money_config.py for development
    if not any([MTN_MOMO_API_USER, ORANGE_MONEY_CLIENT_ID, AIRTEL_MONEY_CLIENT_ID]):
        try:
            from mobile_money_config import get_mobile_money_config
            _mobile_config = get_mobile_money_config()
            MTN_MOMO_API_USER = MTN_MOMO_API_USER or _mobile_config['mtn_momo']['api_user']
            MTN_MOMO_API_KEY = MTN_MOMO_API_KEY or _mobile_config['mtn_momo']['api_key']
            MTN_MOMO_SUBSCRIPTION_KEY = MTN_MOMO_SUBSCRIPTION_KEY or _mobile_config['mtn_momo']['subscription_key']
            ORANGE_MONEY_CLIENT_ID = ORANGE_MONEY_CLIENT_ID or _mobile_config['orange_money']['client_id']
            ORANGE_MONEY_CLIENT_SECRET = ORANGE_MONEY_CLIENT_SECRET or _mobile_config['orange_money']['client_secret']
            AIRTEL_MONEY_CLIENT_ID = AIRTEL_MONEY_CLIENT_ID or _mobile_config['airtel_money']['client_id']
            AIRTEL_MONEY_CLIENT_SECRET = AIRTEL_MONEY_CLIENT_SECRET or _mobile_config['airtel_money']['client_secret']
            print("Using mobile money config from mobile_money_config.py (local development)")
        except ImportError:
            print("Warning: No mobile money keys found in environment variables or mobile_money_config.py")
    
    # Payment method
    PAYMENT_METHOD = 'mobile_money'
    
    # Debug information
    mobile_providers = []
    if MTN_MOMO_API_USER: mobile_providers.append('MTN MoMo')
    if ORANGE_MONEY_CLIENT_ID: mobile_providers.append('Orange Money')
    if AIRTEL_MONEY_CLIENT_ID: mobile_providers.append('Airtel Money')
    
    print(f"Config Debug: Payment method - {PAYMENT_METHOD}")
    print(f"Mobile Money providers available: {', '.join(mobile_providers) if mobile_providers else 'None'}")
    if not mobile_providers:
        print("❌ No mobile money providers configured! Payment system will not work.")
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///tournament.db'
    
    # File Upload Settings
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'jpg', 'jpeg', 'png', 'gif'}
    
    # App Settings
    VIDEOS_PER_PAGE = 12
    PARTICIPANT_FEE = 3500  # $35 in cents