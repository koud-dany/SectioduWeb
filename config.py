import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # Stripe Configuration - try to load from stripe_config.py or use environment variables
    try:
        from stripe_config import get_stripe_keys
        _stripe_keys = get_stripe_keys()
        STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY') or _stripe_keys['publishable_key']
        STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or _stripe_keys['secret_key']
    except ImportError:
        # Fallback to environment variables only (for production deployment)
        STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
        STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', '')
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///tournament.db'
    
    # File Upload Settings
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'jpg', 'jpeg', 'png', 'gif'}
    
    # App Settings
    VIDEOS_PER_PAGE = 12
    PARTICIPANT_FEE = 2500  # $25 in cents