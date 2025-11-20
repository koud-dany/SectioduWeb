#!/usr/bin/env python3
"""
Admin Account Setup Script for lasectionduweb.org
Run this script after deployment to create your admin account
"""

import sys
import os
import sqlite3
import hashlib
from werkzeug.security import generate_password_hash

def create_admin_account():
    """Create admin account with provided credentials"""
    
    # Admin credentials
    admin_email = "barbeblanche89@gmail.com"
    admin_password = "Trafalgar$89"
    admin_username = "admin"
    admin_full_name = "Administrator"
    
    # Database path (adjust if needed)
    db_path = "tournament.db"
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM users WHERE email = ? OR username = ?", (admin_email, admin_username))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print(f"❌ Admin user already exists with email: {admin_email}")
            return False
        
        # Hash the password securely
        password_hash = generate_password_hash(admin_password)
        
        # Insert admin user
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name, is_admin, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (admin_username, admin_email, password_hash, admin_full_name, 1))
        
        # Get the new user ID
        admin_id = cursor.lastrowid
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("✅ Admin account created successfully!")
        print(f"📧 Email: {admin_email}")
        print(f"👤 Username: {admin_username}")
        print(f"🆔 User ID: {admin_id}")
        print(f"🔐 Password: [HIDDEN FOR SECURITY]")
        print("\n🌟 You can now login to your admin panel!")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating admin account: {e}")
        return False

def verify_database():
    """Verify database exists and has required tables"""
    db_path = "tournament.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("🔧 Make sure you've uploaded tournament.db to your server")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Users table not found in database")
            print("🔧 Make sure your database is properly initialized")
            return False
        
        conn.close()
        print("✅ Database verification passed")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Database verification failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 SectionduWeb Admin Account Setup")
    print("=" * 50)
    
    # Verify database first
    if not verify_database():
        print("\n💡 Fix database issues and run this script again")
        sys.exit(1)
    
    # Create admin account
    if create_admin_account():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Visit https://lasectionduweb.org/admin")
        print("2. Login with your admin credentials")
        print("3. Configure your site settings")
        print("4. Create test tournaments")
        print("5. Upload test videos")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
