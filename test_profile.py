#!/usr/bin/env python3
"""
Test script to initialize the database and create a test user profile
"""

import sqlite3
import sys
import os
from werkzeug.security import generate_password_hash

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import init_db

def test_profile_system():
    """Test the profile system by creating a sample user and checking profile data"""
    print("🔧 Initializing database with profile enhancements...")
    
    # Initialize the database
    init_db()
    
    print("✅ Database initialized successfully!")
    
    # Connect to database
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Check if profile columns exist
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]
    
    print("\n📋 Current user table columns:")
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col}")
    
    profile_columns = ['first_name', 'last_name', 'bio', 'location', 'website', 'avatar_filename', 'joined_date', 'subscriber_count', 'total_views']
    missing_columns = [col for col in profile_columns if col not in columns]
    
    if missing_columns:
        print(f"\n⚠️  Missing profile columns: {missing_columns}")
    else:
        print("\n✅ All profile columns are present!")
    
    # Create a test user with profile data (if doesn't exist)
    test_username = "testuser"
    c.execute("SELECT id FROM users WHERE username = ?", (test_username,))
    existing_user = c.fetchone()
    
    if not existing_user:
        print(f"\n👤 Creating test user: {test_username}")
        password_hash = generate_password_hash("testpass123")
        
        c.execute("""INSERT INTO users (username, email, password_hash, first_name, last_name, bio, location, website, subscriber_count, total_views)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (test_username, "test@example.com", password_hash, "Test", "User", 
                   "I'm a test user for the SectionduWeb platform! I love creating and sharing videos.", 
                   "Paris, France", "https://example.com", 42, 1337))
        
        user_id = c.lastrowid
        print(f"✅ Test user created with ID: {user_id}")
        
        # Create a sample video for the test user
        c.execute("""INSERT INTO videos (user_id, title, description, filename, total_votes, average_rating)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  ("1", "Sample Video", "This is a sample video for testing the profile system.", 
                   "sample.mp4", 10, 4.5))
        
        print("✅ Sample video created for test user")
        
    else:
        print(f"\n👤 Test user '{test_username}' already exists")
    
    # Test profile data retrieval
    c.execute("""SELECT username, email, first_name, last_name, bio, location, website, 
                        avatar_filename, registration_date, subscriber_count, total_views
                 FROM users WHERE username = ?""", (test_username,))
    
    profile_data = c.fetchone()
    
    if profile_data:
        print(f"\n📊 Profile data for {test_username}:")
        print(f"  📧 Email: {profile_data[1]}")
        print(f"  👤 Name: {profile_data[2]} {profile_data[3]}")
        print(f"  📝 Bio: {profile_data[4]}")
        print(f"  📍 Location: {profile_data[5]}")
        print(f"  🌐 Website: {profile_data[6]}")
        print(f"  🔔 Subscribers: {profile_data[9]}")
        print(f"  👀 Total Views: {profile_data[10]}")
    
    # Test video count for user
    c.execute("SELECT COUNT(*) FROM videos WHERE user_id = (SELECT id FROM users WHERE username = ?)", (test_username,))
    video_count = c.fetchone()[0]
    print(f"  🎥 Videos: {video_count}")
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Profile system test completed successfully!")
    print(f"🚀 You can now test the profile system by:")
    print(f"   1. Running the Flask app: python app.py")
    print(f"   2. Logging in as '{test_username}' with password 'testpass123'")
    print(f"   3. Visiting /profile to see your profile")
    print(f"   4. Visiting /profile/edit to edit your profile")

if __name__ == "__main__":
    test_profile_system()
