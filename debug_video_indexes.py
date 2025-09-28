import sqlite3

conn = sqlite3.connect('tournament.db')
c = conn.cursor()

print("=== Videos Table Schema ===")
c.execute("PRAGMA table_info(videos)")
columns = c.fetchall()
print("Videos table columns:")
for i, col in enumerate(columns):
    print(f"  {i}: {col[1]} ({col[2]})")

print("\n=== Video Detail Query Test ===")
c.execute('''SELECT v.*, u.username, u.avatar_filename FROM videos v 
             JOIN users u ON v.user_id = u.id WHERE v.id = 1''')
video_raw = c.fetchone()

if video_raw:
    print("Video data structure:")
    for i, value in enumerate(video_raw):
        print(f"Index {i}: {value}")
    
    print(f"\nUsername is at index: {len(video_raw)-2}")
    print(f"Avatar is at index: {len(video_raw)-1}")

conn.close()
