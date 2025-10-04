#!/usr/bin/env python3
"""
Test admin user management functionality
"""

def test_admin_routes():
    """Test admin routes for user management"""
    try:
        print("🔧 Testing Admin User Management")
        print("=" * 40)
        
        # Test Flask app import
        from app import app
        print("✅ Flask app: Imported successfully")
        
        # Test admin routes exist
        routes_to_check = [
            '/admin/users',
            '/admin/user/<int:user_id>/toggle_participant',
            '/admin/user/<int:user_id>/admin',
            '/admin/user/<int:user_id>/block'
        ]
        
        with app.test_client() as client:
            with app.test_request_context():
                from flask import url_for
                
                for route_template in routes_to_check:
                    if '<int:user_id>' in route_template:
                        # Test with a sample user ID
                        route = route_template.replace('<int:user_id>', '1')
                        
                        # Check if route exists by trying to build URL
                        try:
                            if 'toggle_participant' in route:
                                url = url_for('admin_toggle_participant', user_id=1)
                                print(f"✅ Route 'admin_toggle_participant': {url}")
                            elif 'admin' in route and 'block' not in route:
                                url = url_for('admin_toggle_admin', user_id=1)
                                print(f"✅ Route 'admin_toggle_admin': {url}")
                            elif 'block' in route:
                                url = url_for('admin_block_user', user_id=1)
                                print(f"✅ Route 'admin_block_user': {url}")
                        except Exception as e:
                            print(f"❌ Route error: {e}")
                    else:
                        try:
                            if 'users' in route:
                                url = url_for('admin_users')
                                print(f"✅ Route 'admin_users': {url}")
                        except Exception as e:
                            print(f"❌ Route error: {e}")
        
        print("\n🎉 Admin routes test completed!")
        print("\n📝 How to test upgrade/downgrade:")
        print("1. Start app: python app.py")
        print("2. Login as admin")
        print("3. Visit: http://localhost:5000/admin/users")
        print("4. Look for upgrade/downgrade buttons next to users")
        print("5. Click buttons to test functionality")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_admin_routes()
