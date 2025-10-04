#!/usr/bin/env python3
"""
Test Flask app startup and routes
"""

try:
    print("🚀 Testing Flask App...")
    
    # Import the app
    from app import app
    print("✅ App imported successfully")
    
    # Test configuration
    print(f"✅ Debug mode: {app.debug}")
    print(f"✅ Config loaded: {bool(app.config)}")
    
    # List available routes
    print("\n📍 Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.rule} -> {rule.endpoint}")
    
    print(f"\n🌐 Starting server on http://localhost:5000")
    print("Available pages:")
    print("   • Home: http://localhost:5000/")
    print("   • Mobile Money: http://localhost:5000/upgrade")
    print("   • Login: http://localhost:5000/login")
    print("   • Register: http://localhost:5000/register")
    
    # Start the app
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
