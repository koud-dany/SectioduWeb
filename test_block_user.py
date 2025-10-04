#!/usr/bin/env python3
"""
Test script for admin block user functionality
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add current directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_block_user_route():
    """Test the admin block user route"""
    print("🔧 Testing Admin Block User Functionality")
    print("=" * 50)
    
    try:
        # Import the Flask app
        from app import app
        print("✅ Flask app: Imported successfully")
        
        # Test if the route exists by checking URL generation
        with app.app_context():
            from flask import url_for
            
            # Test block user route
            try:
                url = url_for('admin_block_user', user_id=1)
                print(f"✅ Route 'admin_block_user': {url}")
            except Exception as e:
                print(f"❌ Route 'admin_block_user': {str(e)}")
            
            # Test if database has required columns
            try:
                conn = sqlite3.connect('tournament.db')
                c = conn.cursor()
                
                # Check if users table has block-related columns
                c.execute("PRAGMA table_info(users)")
                columns = c.fetchall()
                column_names = [col[1] for col in columns]
                
                required_columns = ['is_blocked', 'block_reason', 'blocked_until']
                missing_cols = [col for col in required_columns if col not in column_names]
                
                if missing_cols:
                    print(f"❌ Database: Missing columns: {missing_cols}")
                else:
                    print("✅ Database: All block-related columns present")
                
                # Check if there are any users to test with
                c.execute("SELECT COUNT(*) FROM users")
                user_count = c.fetchone()[0]
                print(f"📊 Database: {user_count} users found")
                
                conn.close()
                
            except Exception as e:
                print(f"❌ Database error: {str(e)}")
        
        print("\n🎉 Admin block user route test completed!")
        
        print("\n📝 How to test block/unblock functionality:")
        print("1. Start app: python app.py")
        print("2. Login as admin")
        print("3. Visit: http://localhost:5000/admin/users")
        print("4. Look for block/unblock buttons (🚫/🔓) next to users")
        print("5. Click buttons to test AJAX functionality")
        print("6. Check browser console for any JavaScript errors")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    test_block_user_route()
