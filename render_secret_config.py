# Render Secret File: config.py
# This file contains sensitive configuration for production deployment

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if exists)
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key-here'
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    
    # File Storage Configuration
    USE_CLOUD_STORAGE = True  # Always use cloud storage on Render
    
    # AWS S3 Configuration (backup option)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', 'videovote-uploads')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    
    # Cloudinary Configuration (primary cloud storage)
    CLOUDINARY_CLOUD_NAME = 'dah47os9w'
    CLOUDINARY_API_KEY = '868181856457282'
    CLOUDINARY_API_SECRET = 'gInN33v-vwB9wkRXvIuaJ7fN7jw'
    CLOUDINARY_UPLOAD_PRESET = 'ml_default'
    
    # File extensions
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}
    
    # Mobile Money Configuration for Production
    MTN_MOMO_API_USER = os.environ.get('MTN_MOMO_API_USER', '')
    MTN_MOMO_API_KEY = os.environ.get('MTN_MOMO_API_KEY', '')
    MTN_MOMO_SUBSCRIPTION_KEY = os.environ.get('MTN_MOMO_SUBSCRIPTION_KEY', '')
    ORANGE_MONEY_CLIENT_ID = os.environ.get('ORANGE_MONEY_CLIENT_ID', '')
    ORANGE_MONEY_CLIENT_SECRET = os.environ.get('ORANGE_MONEY_CLIENT_SECRET', '')
    AIRTEL_MONEY_CLIENT_ID = os.environ.get('AIRTEL_MONEY_CLIENT_ID', '')
    AIRTEL_MONEY_CLIENT_SECRET = os.environ.get('AIRTEL_MONEY_CLIENT_SECRET', '')
    
    # Payment Configuration
    PAYMENT_AMOUNT = 35  # USD
    PAYMENT_CURRENCY = 'USD'
    PAYMENT_DESCRIPTION = 'Video Tournament Entry Fee'
