#!/usr/bin/env python3
"""
Quick setup script for Video Tournament application
"""

import os
import shutil

def setup_mobile_money_config():
    """Copy the example mobile money config file if it doesn't exist."""
    example_file = 'mobile_money_config.py.example'
    config_file = 'mobile_money_config.py'
    
    if os.path.exists(config_file):
        print(f"✓ {config_file} already exists")
        return
    
    if os.path.exists(example_file):
        shutil.copy(example_file, config_file)
        print(f"✓ Created {config_file} from template")
        print(f"  → Please edit {config_file} and add your Mobile Money API keys")
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
    
    print("\n1. Setting up Mobile Money configuration...")
    setup_mobile_money_config()
    
    print("\n2. Checking directories...")
    check_directories()
    
    print("\n3. Next steps:")
    print("   • Edit mobile_money_config.py with your API credentials")
    print("   • Run: pip install -r requirements.txt")
    print("   • Run: python app.py")
    print("   • Visit: http://localhost:5000")
    
    print("\n✨ Setup complete!")

if __name__ == "__main__":
    main()
