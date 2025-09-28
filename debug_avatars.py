import sqlite3
import os

# Check database structure and avatar data
conn = sqlite3.connect('tournament.db')
c = conn.cursor()

print("=== Database Schema Check ===")
c.execute("PRAGMA table_info(users)")
columns = c.fetchall()
print("Users table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n=== Sample User Data ===")
c.execute("SELECT id, username, avatar_filename FROM users LIMIT 5")
users = c.fetchall()
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}, Avatar: {user[2]}")

print("\n=== Avatar Files Check ===")
avatar_dir = "static/avatars"
if os.path.exists(avatar_dir):
    files = os.listdir(avatar_dir)
    print(f"Files in {avatar_dir}:")
    for file in files[:10]:  # Show first 10 files
        print(f"  {file}")
else:
    print(f"Avatar directory {avatar_dir} does not exist!")

print("\n=== Video Query Test ===")
c.execute("""SELECT v.id, v.title, u.username, u.avatar_filename 
             FROM videos v JOIN users u ON v.user_id = u.id LIMIT 3""")
video_data = c.fetchall()
print("Sample video with user data:")
for video in video_data:
    print(f"Video ID: {video[0]}, Title: {video[1]}, User: {video[2]}, Avatar: {video[3]}")

conn.close()
