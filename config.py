import os
from dotenv import load_dotenv

# Load environment variables from .env file (Secret Files in Render)
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # Stripe Configuration - Load from environment variables (set via .env Secret File in Render)
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
    
    # Fallback to local stripe_config.py for development
    if not STRIPE_PUBLISHABLE_KEY or not STRIPE_SECRET_KEY:
        try:
            from stripe_config import get_stripe_keys
            _stripe_keys = get_stripe_keys()
            STRIPE_PUBLISHABLE_KEY = STRIPE_PUBLISHABLE_KEY or _stripe_keys['publishable_key']
            STRIPE_SECRET_KEY = STRIPE_SECRET_KEY or _stripe_keys['secret_key']
            print("Using keys from stripe_config.py (local development)")
        except ImportError:
            print("Warning: No Stripe keys found in environment variables or stripe_config.py")
    
    # Debug information
    print(f"Config Debug: Stripe keys loaded - Publishable: {'✓' if STRIPE_PUBLISHABLE_KEY else '✗'}, Secret: {'✓' if STRIPE_SECRET_KEY else '✗'}")
    if STRIPE_PUBLISHABLE_KEY:
        print(f"Publishable Key Preview: {STRIPE_PUBLISHABLE_KEY[:12]}...")
        print(f"Loading method: {'Environment variables (.env file)' if os.environ.get('STRIPE_PUBLISHABLE_KEY') else 'Local stripe_config.py'}")
    else:
        print("❌ No Stripe publishable key found! Payment system will not work.")
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///tournament.db'
    
    # File Upload Settings
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'jpg', 'jpeg', 'png', 'gif'}
    
    # App Settings
    VIDEOS_PER_PAGE = 12
    PARTICIPANT_FEE = 3500  # $35 in cents