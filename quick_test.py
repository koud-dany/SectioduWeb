#!/usr/bin/env python3
"""
Quick Flask app test
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_start():
    """Test if the Flask app can start"""
    try:
        print("🚀 Testing Flask App Import...")
        from app import app
        print("✅ App imported successfully!")
        
        print("\n📍 Available Routes:")
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"   {rule.rule} -> {rule.endpoint}")
        
        # Show key routes
        key_routes = [r for r in routes if any(x in r for x in ['/upgrade', '/login', '/register', '/', '/initiate_mobile'])]
        for route in key_routes:
            print(route)
        
        print(f"\n🔧 Total routes: {len(routes)}")
        
        print("\n✅ App is ready to start!")
        print("🌐 Run: python app.py")
        print("📱 Then visit: http://localhost:5000/upgrade")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_app_start():
        print("\n🎉 Your mobile money payment system is ready!")
        print("\n📝 How to test:")
        print("1. Start the app: python app.py")
        print("2. Register/Login at: http://localhost:5000/")
        print("3. Go to payments: http://localhost:5000/upgrade")
        print("4. Use test number: 46733123450")
        print("5. Select MTN Mobile Money")
        print("6. Click 'Pay $35' button")
    else:
        print("\n💡 Fix the errors above and try again")
