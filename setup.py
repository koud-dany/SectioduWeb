#!/usr/bin/env python3
"""
Quick setup script for Video Tournament application
"""

import os
import shutil

def setup_stripe_config():
    """Copy the example stripe config file if it doesn't exist."""
    example_file = 'stripe_config.py.example'
    config_file = 'stripe_config.py'
    
    if os.path.exists(config_file):
        print(f"✓ {config_file} already exists")
        return
    
    if os.path.exists(example_file):
        shutil.copy(example_file, config_file)
        print(f"✓ Created {config_file} from template")
        print(f"  → Please edit {config_file} and add your Stripe API keys")
    else:
        print(f"✗ {example_file} not found")

def check_directories():
    """Ensure required directories exist."""
    directories = [
        'static/uploads',
        'static/thumbnails',
        'templates'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✓ Directory {directory} exists")
        else:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ Created directory {directory}")

def main():
    print("🎬 Video Tournament Setup")
    print("=" * 30)
    
    print("\n1. Setting up Stripe configuration...")
    setup_stripe_config()
    
    print("\n2. Checking directories...")
    check_directories()
    
    print("\n3. Next steps:")
    print("   • Edit stripe_config.py with your Stripe API keys")
    print("   • Run: pip install -r requirements.txt")
    print("   • Run: python app.py")
    print("   • Visit: http://localhost:5000")
    
    print("\n✨ Setup complete!")

if __name__ == "__main__":
    main()
