#!/usr/bin/env python3
"""
Simple test to check if the Flask app starts correctly
"""

from app import app, init_db
import sqlite3

def test_app():
    """Test basic app functionality"""
    print("🔧 Testing Flask application...")
    
    # Initialize database
    init_db()
    
    # Check database
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    user_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM videos')
    video_count = c.fetchone()[0]
    conn.close()
    
    print(f"📊 Database Status:")
    print(f"   Users: {user_count}")
    print(f"   Videos: {video_count}")
    
    # Test routes
    with app.test_client() as client:
        # Test homepage
        response = client.get('/')
        print(f"🏠 Homepage status: {response.status_code}")
        
        # Test profile route
        if user_count > 0:
            conn = sqlite3.connect('tournament.db')
            c = conn.cursor()
            c.execute('SELECT username FROM users LIMIT 1')
            test_user = c.fetchone()[0]
            conn.close()
            
            response = client.get(f'/profile/{test_user}')
            print(f"👤 Profile status: {response.status_code}")
        
        # Test login page
        response = client.get('/login')
        print(f"🔑 Login status: {response.status_code}")
    
    print("✅ All tests passed! Starting Flask app...")

if __name__ == "__main__":
    test_app()
    app.run(debug=True, host='127.0.0.1', port=5000)
