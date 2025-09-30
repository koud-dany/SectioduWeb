#!/usr/bin/env python3
"""
Migration script to add video views tracking table and update existing data
Run this once to migrate existing video view data to the new system
"""

import sqlite3
from datetime import datetime

def migrate_views():
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    print("Starting view system migration...")
    
    # Create video_views table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS video_views (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        video_id INTEGER,
        view_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT,
        user_agent TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (video_id) REFERENCES videos (id),
        UNIQUE(user_id, video_id)
    )''')
    
    print("Created video_views table")
    
    # Add view_count column to videos table if it doesn't exist
    try:
        c.execute('ALTER TABLE videos ADD COLUMN view_count INTEGER DEFAULT 0')
        print("Added view_count column to videos table")
    except sqlite3.OperationalError:
        print("view_count column already exists")
    
    # Reset all view counts to 0 (we'll start fresh with authenticated views only)
    c.execute('UPDATE videos SET view_count = 0')
    print("Reset all video view counts to 0")
    
    # Get count of videos
    c.execute('SELECT COUNT(*) FROM videos')
    video_count = c.fetchone()[0]
    
    print(f"Migration complete! Found {video_count} videos in database.")
    print("View counts have been reset to 0 and will be tracked per unique user going forward.")
    print("Users will need to re-watch videos to generate new view counts.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate_views()
