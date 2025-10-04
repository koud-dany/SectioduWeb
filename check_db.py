#!/usr/bin/env python3
"""
Simple database schema checker
"""
import sqlite3

def check_users_table():
    """Check the users table schema"""
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Get table info
        c.execute("PRAGMA table_info(users)")
        columns = c.fetchall()
        
        print("Users table columns:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
        
        # Check for block-related columns
        column_names = [col[1] for col in columns]
        block_columns = ['is_blocked', 'block_reason', 'blocked_until']
        
        print("\nBlock-related columns status:")
        for col in block_columns:
            status = "✅ Present" if col in column_names else "❌ Missing"
            print(f"  {col}: {status}")
        
        # Check sample data
        c.execute("SELECT COUNT(*) FROM users")
        user_count = c.fetchone()[0]
        print(f"\nTotal users in database: {user_count}")
        
        if user_count > 0:
            c.execute("SELECT id, username, is_blocked FROM users LIMIT 3")
            users = c.fetchall()
            print("\nSample users:")
            for user in users:
                blocked_status = "Blocked" if user[2] else "Active"
                print(f"  ID: {user[0]}, Username: {user[1]}, Status: {blocked_status}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error checking database: {e}")
        return False

if __name__ == "__main__":
    check_users_table()
