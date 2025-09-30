#!/usr/bin/env python3
"""
Debug script to check video view tracking system
"""

import sqlite3
from datetime import datetime

def check_views():
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    print("=== VIDEO VIEW TRACKING DEBUG ===\n")
    
    # Check videos table
    c.execute('SELECT id, title, view_count FROM videos ORDER BY id')
    videos = c.fetchall()
    
    print("VIDEOS:")
    for video in videos:
        print(f"  Video {video[0]}: '{video[1]}' - {video[2]} views")
    
    print("\n" + "="*50 + "\n")
    
    # Check video_views table
    c.execute('SELECT COUNT(*) FROM video_views')
    total_views = c.fetchone()[0]
    print(f"TOTAL UNIQUE VIEWS RECORDED: {total_views}")
    
    if total_views > 0:
        print("\nDETAILED VIEW RECORDS:")
        c.execute('''SELECT vv.video_id, v.title, u.username, vv.view_date, vv.ip_address
                     FROM video_views vv
                     JOIN videos v ON vv.video_id = v.id  
                     JOIN users u ON vv.user_id = u.id
                     ORDER BY vv.view_date DESC''')
        views = c.fetchall()
        
        for view in views:
            print(f"  Video {view[0]} ('{view[1]}') viewed by {view[2]} on {view[3]} from {view[4]}")
    else:
        print("No view records yet. Users need to visit video pages while logged in.")
    
    print("\n" + "="*50 + "\n")
    
    # Check users table
    c.execute('SELECT COUNT(*) FROM users')
    user_count = c.fetchone()[0]
    print(f"TOTAL USERS: {user_count}")
    
    c.execute('SELECT username FROM users ORDER BY id')
    users = c.fetchall()
    print("USERS:")
    for user in users:
        print(f"  - {user[0]}")
    
    conn.close()

if __name__ == '__main__':
    check_views()
