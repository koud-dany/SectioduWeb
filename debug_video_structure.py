import sqlite3

conn = sqlite3.connect('tournament.db')
c = conn.cursor()

print("=== Video Detail Query Test ===")
c.execute('''SELECT v.*, u.username, u.avatar_filename FROM videos v 
             JOIN users u ON v.user_id = u.id WHERE v.id = 1''')
video_raw = c.fetchone()

if video_raw:
    print("Video data structure:")
    for i, value in enumerate(video_raw):
        print(f"Index {i}: {value}")
    
    print(f"\nUsername is at index: {len(video_raw)-2}")
    print(f"Avatar is at index: {len(video_raw)-1}")
    
print("\n=== Top Videos Query Test ===")
c.execute('''SELECT v.id, v.title, v.filename, v.total_votes, v.average_rating, u.username, u.avatar_filename 
             FROM videos v JOIN users u ON v.user_id = u.id 
             WHERE v.total_votes >= 0 AND v.is_approved = 1 AND v.is_blocked = 0
             ORDER BY v.average_rating DESC, v.total_votes DESC LIMIT 3''')
top_videos = c.fetchall()

print("Top videos data structure:")
for i, video in enumerate(top_videos):
    print(f"Video {i+1}:")
    for j, value in enumerate(video):
        print(f"  Index {j}: {value}")

conn.close()
