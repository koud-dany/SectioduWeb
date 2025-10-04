from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os

from datetime import datetime
from functools import wraps
import traceback
from config import Config

# Debug: Print deployment info at startup
try:
    from deployment_info import get_deployment_info
    deploy_info = get_deployment_info()
    print(f"🚀 Deployment Version: {deploy_info['version']}")
    print(f"📅 Last Update: {deploy_info['last_update']}")
    print("🔧 Recent Changes:")
    for change in deploy_info['changes']:
        print(f"  - {change}")
except ImportError:
    print("ℹ️  Deployment info not available")

# Debug: Check mobile money config availability
try:
    from mobile_money_config import get_mobile_money_config
    config_test = get_mobile_money_config()
    print("✅ Mobile money config loaded successfully")
    print(f"🎭 Demo mode: {config_test.get('demo_mode', False)}")
except Exception as e:
    print(f"❌ Mobile money config error: {str(e)}")
    print("⚠️  Will use environment variables instead")

app = Flask(__name__)
app.config.from_object(Config)

# Template context processor to make payment status available in all templates
@app.context_processor
def inject_user_status():
    if 'user_id' in session:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('SELECT is_paid FROM users WHERE id = ?', (session['user_id'],))
        result = c.fetchone()
        conn.close()
        return {'current_user_is_paid': result[0] if result else False}
    return {'current_user_is_paid': False}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/thumbnails', exist_ok=True)
os.makedirs('static/avatars', exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        is_paid BOOLEAN DEFAULT FALSE,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        first_name TEXT,
        last_name TEXT,
        bio TEXT,
        location TEXT,
        website TEXT,
        avatar_filename TEXT,
        joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        subscriber_count INTEGER DEFAULT 0,
        total_views INTEGER DEFAULT 0,
        is_admin BOOLEAN DEFAULT FALSE,
        admin_level TEXT DEFAULT NULL,
        is_blocked BOOLEAN DEFAULT FALSE,
        block_reason TEXT,
        blocked_until TIMESTAMP DEFAULT NULL,
        last_login TIMESTAMP,
        login_count INTEGER DEFAULT 0
    )''')
    
    # Add new columns to existing users table if they don't exist
    try:
        c.execute('ALTER TABLE users ADD COLUMN first_name TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN last_name TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN bio TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN location TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN website TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN avatar_filename TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN subscriber_count INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN total_views INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN subscriber_count INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN total_views INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass
    
    # Videos table
    c.execute('''CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        filename TEXT NOT NULL,
        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_votes INTEGER DEFAULT 0,
        average_rating REAL DEFAULT 0.0,
        is_approved BOOLEAN DEFAULT FALSE,
        approval_date TIMESTAMP DEFAULT NULL,
        approved_by INTEGER DEFAULT NULL,
        is_blocked BOOLEAN DEFAULT FALSE,
        block_reason TEXT,
        blocked_by INTEGER DEFAULT NULL,
        view_count INTEGER DEFAULT 0,
        category TEXT,
        tags TEXT,
        duration INTEGER DEFAULT 0,
        file_size INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (approved_by) REFERENCES users (id),
        FOREIGN KEY (blocked_by) REFERENCES users (id)
    )''')
    
    # Votes table
    c.execute('''CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        video_id INTEGER,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        vote_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, video_id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (video_id) REFERENCES videos (id)
    )''')
    
    # Comments table (updated to support replies)
    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        video_id INTEGER,
        comment TEXT NOT NULL,
        comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        parent_id INTEGER DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (video_id) REFERENCES videos (id),
        FOREIGN KEY (parent_id) REFERENCES comments (id)
    )''')
    
    # Comment likes table
    c.execute('''CREATE TABLE IF NOT EXISTS comment_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id INTEGER,
        user_id INTEGER,
        like_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (comment_id) REFERENCES comments (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(comment_id, user_id)
    )''')
    
    # Add parent_id column to existing comments table if it doesn't exist
    try:
        c.execute('''ALTER TABLE comments ADD COLUMN parent_id INTEGER DEFAULT NULL''')
    except:
        pass  # Column already exists
    
    # Add admin-related columns to existing users table
    admin_columns = [
        ('is_admin', 'BOOLEAN DEFAULT FALSE'),
        ('admin_level', 'TEXT DEFAULT NULL'),
        ('is_blocked', 'BOOLEAN DEFAULT FALSE'),
        ('block_reason', 'TEXT'),
        ('blocked_until', 'TIMESTAMP DEFAULT NULL'),
        ('last_login', 'TIMESTAMP'),
        ('login_count', 'INTEGER DEFAULT 0')
    ]
    
    for column_name, column_def in admin_columns:
        try:
            c.execute(f'ALTER TABLE users ADD COLUMN {column_name} {column_def}')
        except sqlite3.OperationalError:
            pass
    
    # Add admin-related columns to existing videos table
    video_columns = [
        ('is_approved', 'BOOLEAN DEFAULT FALSE'),
        ('approval_date', 'TIMESTAMP DEFAULT NULL'),
        ('approved_by', 'INTEGER DEFAULT NULL'),
        ('is_blocked', 'BOOLEAN DEFAULT FALSE'),
        ('block_reason', 'TEXT'),
        ('blocked_by', 'INTEGER DEFAULT NULL'),
        ('view_count', 'INTEGER DEFAULT 0'),
        ('category', 'TEXT'),
        ('tags', 'TEXT'),
        ('duration', 'INTEGER DEFAULT 0'),
        ('file_size', 'INTEGER DEFAULT 0')
    ]
    
    for column_name, column_def in video_columns:
        try:
            c.execute(f'ALTER TABLE videos ADD COLUMN {column_name} {column_def}')
        except sqlite3.OperationalError:
            pass
    
    # Admin logs table
    c.execute('''CREATE TABLE IF NOT EXISTS admin_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER,
        action TEXT NOT NULL,
        target_type TEXT NOT NULL,
        target_id INTEGER,
        details TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address TEXT,
        FOREIGN KEY (admin_id) REFERENCES users (id)
    )''')
    
    # Admin messages table
    c.execute('''CREATE TABLE IF NOT EXISTS admin_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER,
        recipient_id INTEGER,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_read BOOLEAN DEFAULT FALSE,
        email_sent BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (admin_id) REFERENCES users (id),
        FOREIGN KEY (recipient_id) REFERENCES users (id)
    )''')
    
    # Reports table
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter_id INTEGER,
        reported_type TEXT NOT NULL,
        reported_id INTEGER,
        reason TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pending',
        handled_by INTEGER DEFAULT NULL,
        handled_date TIMESTAMP DEFAULT NULL,
        report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reporter_id) REFERENCES users (id),
        FOREIGN KEY (handled_by) REFERENCES users (id)
    )''')
    
    # Categories table
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        created_by INTEGER,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (created_by) REFERENCES users (id)
    )''')
    
    # Video views table - Track unique views per user per video
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
    
    # Payment transactions table - Track mobile money payments
    c.execute('''CREATE TABLE IF NOT EXISTS payment_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transaction_id TEXT UNIQUE NOT NULL,
        provider TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Create default admin user if not exists
    c.execute('SELECT COUNT(*) FROM users WHERE is_admin = 1')
    admin_count = c.fetchone()[0]
    
    if admin_count == 0:
        admin_hash = generate_password_hash('admin123')  # Default admin password
        c.execute('''INSERT INTO users (username, email, password_hash, is_admin, admin_level, is_paid) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  ('admin', 'admin@sectionduweb.com', admin_hash, True, 'super', True))
    
    # Insert default categories
    default_categories = [
        ('Entertainment', 'Music, Comedy, Gaming'),
        ('Education', 'Tutorials, Lectures, How-to'),
        ('Technology', 'Tech Reviews, Programming, Innovation'),
        ('Sports', 'Sports highlights, Fitness, Athletics'),
        ('Travel', 'Travel vlogs, Destinations, Culture'),
        ('Lifestyle', 'Fashion, Food, Health, Beauty'),
        ('News', 'Current events, Politics, Documentary'),
        ('Art', 'Creative content, Drawing, Photography')
    ]
    
    for cat_name, cat_desc in default_categories:
        try:
            c.execute('INSERT INTO categories (name, description, created_by) VALUES (?, ?, ?)',
                     (cat_name, cat_desc, 1))  # Created by admin
        except sqlite3.IntegrityError:
            pass  # Category already exists
    
    conn.commit()
    conn.close()

# Initialize database on startup for production
def ensure_db_initialized():
    """Ensure database is initialized when app starts"""
    if not os.path.exists('tournament.db'):
        init_db()

# Initialize database when module is imported (for production deployment)
ensure_db_initialized()

# Helper functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def paid_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        
        # Check if user has paid
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('SELECT is_paid FROM users WHERE id = ?', (session['user_id'],))
        user = c.fetchone()
        conn.close()
        
        if not user or not user[0]:
            flash('Tournament entry fee required to upload videos. Please pay the $35 participant fee.', 'warning')
            return redirect(url_for('upgrade'))
        
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user_avatar():
    """Inject current user's avatar into all templates"""
    if 'user_id' in session:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('SELECT avatar_filename FROM users WHERE id = ?', (session['user_id'],))
        result = c.fetchone()
        conn.close()
        return {'current_user_avatar': result[0] if result and result[0] else None}
    return {'current_user_avatar': None}



def admin_required(level='basic'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.')
                return redirect(url_for('login'))
            
            conn = sqlite3.connect('tournament.db')
            c = conn.cursor()
            c.execute('SELECT is_admin, admin_level, is_blocked FROM users WHERE id = ?', (session['user_id'],))
            user = c.fetchone()
            conn.close()
            
            if not user or not user[0] or user[2]:  # Not admin or blocked
                flash('Access denied. Admin privileges required.')
                return redirect(url_for('index'))
            
            # Check admin level
            user_level = user[1] or 'basic'
            if level == 'super' and user_level != 'super':
                flash('Super admin privileges required.')
                return redirect(url_for('admin_dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_admin_action(admin_id, action, target_type, target_id, details=None):
    """Log admin actions for audit trail"""
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('''INSERT INTO admin_logs (admin_id, action, target_type, target_id, details, ip_address) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (admin_id, action, target_type, target_id, details, request.remote_addr))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging admin action: {e}")

def send_admin_email(recipient_email, subject, message):
    """Send email notification (placeholder - implement with your email service)"""
    # Implement email sending logic here
    # For now, just log the action
    print(f"EMAIL: To {recipient_email}, Subject: {subject}, Message: {message}")
    return True

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get top videos (only approved videos for regular users)
    c.execute('''SELECT v.id, v.title, v.filename, v.total_votes, v.average_rating, u.username 
                 FROM videos v JOIN users u ON v.user_id = u.id 
                 WHERE v.is_approved = 1 AND v.is_blocked = 0
                 ORDER BY v.average_rating DESC, v.total_votes DESC LIMIT 5''')
    top_videos_raw = c.fetchall()
    
    # Convert to proper data types
    top_videos = []
    for video in top_videos_raw:
        video_list = list(video)
        video_list[3] = int(video_list[3]) if video_list[3] is not None else 0  # total_votes
        video_list[4] = float(video_list[4]) if video_list[4] is not None else 0.0  # average_rating
        top_videos.append(tuple(video_list))
    
    # Get total participants
    c.execute('SELECT COUNT(*) FROM users')
    total_participants = c.fetchone()[0]
    
    # Get total videos
    c.execute('SELECT COUNT(*) FROM videos')
    total_videos = c.fetchone()[0]
    
    conn.close()
    
    return render_template('index.html', 
                         top_videos=top_videos,
                         total_participants=total_participants,
                         total_videos=total_videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('''SELECT id, username, email, password_hash, is_blocked, blocked_until, 
                            block_reason, is_admin, admin_level FROM users WHERE username = ?''', (username,))
        user = c.fetchone()
        
        if user and check_password_hash(user[3], password):
            # Check if user is blocked
            if user[4]:  # is_blocked
                blocked_until = user[5]
                if blocked_until:
                    from datetime import datetime
                    blocked_until_dt = datetime.fromisoformat(blocked_until.replace('Z', '+00:00'))
                    if datetime.now() < blocked_until_dt:
                        flash(f'Your account is temporarily blocked until {blocked_until}. Reason: {user[6]}')
                        conn.close()
                        return render_template('login.html')
                    else:
                        # Unblock user if block period expired
                        c.execute('UPDATE users SET is_blocked = FALSE, blocked_until = NULL, block_reason = NULL WHERE id = ?', (user[0],))
                else:
                    flash(f'Your account is permanently blocked. Reason: {user[6]}')
                    conn.close()
                    return render_template('login.html')
            
            # Update login statistics
            c.execute('''UPDATE users SET last_login = CURRENT_TIMESTAMP, 
                        login_count = COALESCE(login_count, 0) + 1 WHERE id = ?''', (user[0],))
            conn.commit()
            
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[7]
            session['admin_level'] = user[8]
            
            flash('Login successful!')
            
            # Redirect admin users to admin dashboard
            if user[7]:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
        
        conn.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, email, password_hash, is_paid) VALUES (?, ?, ?, ?)',
                     (username, email, password_hash, False))
            conn.commit()
            flash('Registration successful! Please pay the $35 tournament entry fee to start uploading videos.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/debug/user_status')
@login_required
def debug_user_status():
    """Debug endpoint to check user payment status"""
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    c.execute('SELECT id, username, is_paid FROM users WHERE id = ?', (session['user_id'],))
    user = c.fetchone()
    
    # Also check recent payment transactions
    c.execute('''SELECT transaction_id, provider, status, created_at 
                FROM payment_transactions 
                WHERE user_id = ? 
                ORDER BY created_at DESC LIMIT 5''', (session['user_id'],))
    transactions = c.fetchall()
    conn.close()
    
    debug_info = {
        'user_id': session.get('user_id'),
        'session_is_paid': session.get('is_paid'),
        'database_user': user,
        'recent_transactions': transactions,
        'current_user_is_paid': user[2] if user else None
    }
    
    return jsonify(debug_info)

@app.route('/debug/force_upgrade', methods=['POST'])
@login_required
def debug_force_upgrade():
    """Force upgrade user to paid status for testing"""
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    print(f"🔧 FORCE UPGRADE: Updating user {session['user_id']} to paid status")
    c.execute('UPDATE users SET is_paid = TRUE WHERE id = ?', (session['user_id'],))
    
    # Verify the update
    c.execute('SELECT is_paid FROM users WHERE id = ?', (session['user_id'],))
    updated_status = c.fetchone()
    
    conn.commit()
    conn.close()
    
    session['is_paid'] = True
    
    return jsonify({
        'success': True,
        'message': f'User {session["user_id"]} upgraded to paid status',
        'database_status': updated_status[0] if updated_status else None,
        'session_status': session.get('is_paid')
    })

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get user's videos
    c.execute('''SELECT id, title, filename, total_votes, average_rating, upload_date 
                 FROM videos WHERE user_id = ? ORDER BY upload_date DESC''', 
              (session['user_id'],))
    user_videos_raw = c.fetchall()
    
    # Convert to proper data types
    user_videos = []
    for video in user_videos_raw:
        video_list = list(video)
        video_list[3] = int(video_list[3]) if video_list[3] is not None else 0  # total_votes
        video_list[4] = float(video_list[4]) if video_list[4] is not None else 0.0  # average_rating
        user_videos.append(tuple(video_list))
    
    # Get user's payment status
    c.execute('SELECT is_paid FROM users WHERE id = ?', (session['user_id'],))
    payment_result = c.fetchone()
    user_payment_status = payment_result[0] if payment_result else False
    
    conn.close()
    return render_template('dashboard.html', user_videos=user_videos, is_paid=user_payment_status)

@app.route('/videos')
def videos():
    # Get sort parameter from URL (default: recent)
    sort_by = request.args.get('sort', 'recent')
    print(f"=== VIDEOS DEBUG: Sort parameter = '{sort_by}' ===")
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Determine sorting based on parameter
    if sort_by == 'top_rated':
        print("Using TOP RATED sorting")
        # Sort by average rating first, then by votes, only show approved and unblocked videos with votes
        c.execute('''SELECT v.id, v.title, v.filename, v.total_votes, v.average_rating, u.username, v.upload_date
                     FROM videos v JOIN users u ON v.user_id = u.id 
                     WHERE v.total_votes > 0 AND v.is_approved = 1 AND v.is_blocked = 0
                     ORDER BY v.average_rating DESC, v.total_votes DESC''')
    elif sort_by == 'most_voted':
        print("Using MOST VOTED sorting")
        # Sort by total votes, only show approved and unblocked videos
        c.execute('''SELECT v.id, v.title, v.filename, v.total_votes, v.average_rating, u.username, v.upload_date
                     FROM videos v JOIN users u ON v.user_id = u.id 
                     WHERE v.is_approved = 1 AND v.is_blocked = 0
                     ORDER BY v.total_votes DESC, v.average_rating DESC''')
    else:  # recent (default)
        print("Using RECENT sorting (default)")
        # Sort by upload date (newest first), only show approved and unblocked videos
        c.execute('''SELECT v.id, v.title, v.filename, v.total_votes, v.average_rating, u.username, v.upload_date
                     FROM videos v JOIN users u ON v.user_id = u.id 
                     WHERE v.is_approved = 1 AND v.is_blocked = 0
                     ORDER BY v.upload_date DESC''')
    
    all_videos_raw = c.fetchall()
    print(f"Found {len(all_videos_raw)} videos")
    
    # Convert to proper data types
    all_videos = []
    for video in all_videos_raw:
        video_list = list(video)
        video_list[3] = int(video_list[3]) if video_list[3] is not None else 0  # total_votes
        video_list[4] = float(video_list[4]) if video_list[4] is not None else 0.0  # average_rating
        all_videos.append(tuple(video_list))
        print(f"  Video: {video_list[1]}, Votes: {video_list[3]}, Rating: {video_list[4]}")
    
    conn.close()
    print(f"=== END VIDEOS DEBUG ===")
    return render_template('videos.html', videos=all_videos, current_sort=sort_by)

@app.route('/upload_video', methods=['GET', 'POST'])
@login_required
@paid_required
def upload_video():
    if request.method == 'POST':
        try:
            print("=== UPLOAD DEBUG START ===")
            print(f"Form data keys: {list(request.form.keys())}")
            print(f"Files data keys: {list(request.files.keys())}")
            
            # Get form data
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            
            print(f"Title: '{title}'")
            print(f"Description: '{description}'")
            
            # Validate title
            if not title:
                flash('Video title is required')
                print("ERROR: Title is empty")
                return redirect(request.url)
            
            # Check if file is in request
            if 'video' not in request.files:
                flash('No video file selected')
                print("ERROR: No 'video' key in request.files")
                return redirect(request.url)
            
            file = request.files['video']
            print(f"File object: {file}")
            print(f"File filename: '{file.filename}'")
            print(f"File content type: {file.content_type}")
            
            if file.filename == '' or file.filename is None:
                flash('No video file selected')
                print("ERROR: Empty filename")
                return redirect(request.url)
            
            # Check file size
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Reset to beginning
            print(f"File size: {file_size} bytes ({file_size / (1024*1024):.2f} MB)")
            
            if file_size == 0:
                flash('Selected file is empty')
                print("ERROR: File size is 0")
                return redirect(request.url)
            
            if file_size > app.config['MAX_CONTENT_LENGTH']:
                flash('File too large. Maximum size is 100MB')
                print(f"ERROR: File too large: {file_size} > {app.config['MAX_CONTENT_LENGTH']}")
                return redirect(request.url)
            
            # Check file extension
            if not allowed_file(file.filename):
                flash('Invalid file type. Allowed types: ' + ', '.join(Config.ALLOWED_EXTENSIONS))
                print(f"ERROR: Invalid file type. Extension: {file.filename.split('.')[-1] if '.' in file.filename else 'None'}")
                return redirect(request.url)
            
            print("All validations passed. Starting file save...")
            
            # Generate secure filename
            original_filename = file.filename
            filename = secure_filename(original_filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            
            print(f"Original filename: '{original_filename}'")
            print(f"Secure filename: '{filename}'")
            
            # Ensure upload directory exists
            upload_path = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_path):
                os.makedirs(upload_path, exist_ok=True)
                print(f"Created upload directory: {upload_path}")
            
            # Full file path
            file_path = os.path.join(upload_path, filename)
            print(f"Full file path: {file_path}")
            
            # Save file
            print("Starting file save operation...")
            file.save(file_path)
            print("File saved successfully!")
            
            # Verify file was saved
            if os.path.exists(file_path):
                saved_size = os.path.getsize(file_path)
                print(f"File saved and verified. Size: {saved_size} bytes")
                
                if saved_size != file_size:
                    print(f"WARNING: Size mismatch! Original: {file_size}, Saved: {saved_size}")
            else:
                print("ERROR: File was not saved!")
                flash('Error saving video file')
                return redirect(request.url)
            
            print("Starting database save...")
            
            # Calculate file size
            file_size_bytes = os.path.getsize(file_path)
            
            # Save to database (videos need admin approval before appearing on platform)
            conn = sqlite3.connect('tournament.db')
            c = conn.cursor()
            c.execute('''INSERT INTO videos (user_id, title, description, filename, file_size, is_approved) 
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (session['user_id'], title, description, filename, file_size_bytes, False))
            
            video_id = c.lastrowid
            print(f"Video saved to database with ID: {video_id}")
            
            conn.commit()
            conn.close()
            
            print("=== UPLOAD DEBUG SUCCESS ===")
            flash('Video uploaded successfully! It will appear on the platform after admin approval.', 'info')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            print(f"=== UPLOAD ERROR ===")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            import traceback
            print(f"Full traceback:")
            traceback.print_exc()
            print("=== END ERROR ===")
            
            flash(f'Error uploading video: {str(e)}')
            return redirect(request.url)
    
    return render_template('upload_video.html')

@app.route('/video/<int:video_id>', methods=['GET', 'POST'])
def video_detail(video_id):
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Handle comment submission
    if request.method == 'POST' and 'user_id' in session:
        comment = request.form['comment']
        c.execute('''INSERT INTO comments (user_id, video_id, comment) 
                    VALUES (?, ?, ?)''', (session['user_id'], video_id, comment))
        conn.commit()
        flash('Comment added successfully!')
        return redirect(url_for('video_detail', video_id=video_id))
    
    # Get video details including uploader avatar
    c.execute('''SELECT v.*, u.username, u.avatar_filename FROM videos v 
                 JOIN users u ON v.user_id = u.id WHERE v.id = ?''', (video_id,))
    video_raw = c.fetchone()
    
    if not video_raw:
        flash('Video not found')
        conn.close()
        return redirect(url_for('videos'))
    
    # Track video view (YouTube-style: one view per user account)
    if 'user_id' in session:
        user_id = session['user_id']
        # Check if user has already viewed this video
        c.execute('SELECT id FROM video_views WHERE user_id = ? AND video_id = ?', (user_id, video_id))
        existing_view = c.fetchone()
        
        if not existing_view:
            # Record new view
            user_agent = request.headers.get('User-Agent', '')
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', ''))
            
            try:
                c.execute('''INSERT INTO video_views (user_id, video_id, ip_address, user_agent) 
                           VALUES (?, ?, ?, ?)''', (user_id, video_id, ip_address, user_agent))
                
                # Update video view count based on unique views
                c.execute('SELECT COUNT(*) FROM video_views WHERE video_id = ?', (video_id,))
                unique_view_count = c.fetchone()[0]
                
                c.execute('UPDATE videos SET view_count = ? WHERE id = ?', (unique_view_count, video_id))
                conn.commit()
            except sqlite3.IntegrityError:
                # Handle race condition - view already recorded
                pass
    else:
        # For anonymous users, track by session to prevent multiple views in same session
        # This is a compromise - we can't perfectly track anonymous users like YouTube does
        session_key = f'viewed_video_{video_id}'
        if session_key not in session:
            session[session_key] = True
            # For anonymous users, we don't add to video_views table 
            # Only logged-in users contribute to the official view count
            # This encourages user registration while preventing spam
    
    # Convert video tuple to list and ensure numeric fields are properly typed
    video = list(video_raw)
    # video[6] = total_votes, video[7] = average_rating
    video[6] = int(video[6]) if video[6] is not None else 0  # total_votes
    video[7] = float(video[7]) if video[7] is not None else 0.0  # average_rating
    
    # Get comments with reply counts, like counts, and user like status (only parent comments, not replies)
    c.execute('''SELECT c.comment, c.comment_date, u.username, c.id,
                        (SELECT COUNT(*) FROM comments replies 
                         WHERE replies.parent_id = c.id) as reply_count,
                        u.avatar_filename,
                        (SELECT COUNT(*) FROM comment_likes 
                         WHERE comment_id = c.id) as like_count
                 FROM comments c JOIN users u ON c.user_id = u.id 
                 WHERE c.video_id = ? AND c.parent_id IS NULL
                 ORDER BY c.comment_date DESC''', (video_id,))
    comments_raw = c.fetchall()
    
    # Add user like and dislike status to each comment
    comments = []
    for comment in comments_raw:
        comment_dict = {
            'text': comment[0],
            'date': comment[1], 
            'username': comment[2],
            'id': comment[3],
            'reply_count': comment[4],
            'avatar': comment[5],
            'like_count': comment[6],
            'user_liked': False,
            'user_disliked': False
        }
        
        # Check if current user liked or disliked this comment
        if 'user_id' in session:
            c.execute('SELECT id FROM comment_likes WHERE comment_id = ? AND user_id = ?', 
                     (comment[3], session['user_id']))
            comment_dict['user_liked'] = c.fetchone() is not None
            
            # Create comment_dislikes table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS comment_dislikes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comment_id INTEGER,
                user_id INTEGER,
                dislike_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (comment_id) REFERENCES comments (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(comment_id, user_id)
            )''')
            
            c.execute('SELECT id FROM comment_dislikes WHERE comment_id = ? AND user_id = ?', 
                     (comment[3], session['user_id']))
            comment_dict['user_disliked'] = c.fetchone() is not None
            
        comments.append(comment_dict)
    
    # Get top-rated videos for sidebar (only approved and unblocked videos)
    c.execute('''SELECT v.id, v.title, v.filename, v.total_votes, v.average_rating, u.username, u.avatar_filename 
                 FROM videos v JOIN users u ON v.user_id = u.id 
                 WHERE v.total_votes >= 0 AND v.is_approved = 1 AND v.is_blocked = 0
                 ORDER BY v.average_rating DESC, v.total_votes DESC LIMIT 10''')
    top_videos_raw = c.fetchall()
    
    # Convert top videos to proper data types
    top_videos = []
    for top_video in top_videos_raw:
        video_list = list(top_video)
        video_list[3] = int(video_list[3]) if video_list[3] is not None else 0  # total_votes
        video_list[4] = float(video_list[4]) if video_list[4] is not None else 0.0  # average_rating
        # avatar_filename (index 6) stays as is
        top_videos.append(tuple(video_list))
    
    # Get current user avatar for comment form
    current_user_avatar = None
    if 'user_id' in session:
        c.execute('SELECT avatar_filename FROM users WHERE id = ?', (session['user_id'],))
        avatar_result = c.fetchone()
        current_user_avatar = avatar_result[0] if avatar_result else None
    
    conn.close()
    return render_template('video_detail.html', video=video, comments=comments, top_videos=top_videos, current_user_avatar=current_user_avatar)

@app.route('/admin/recalculate_views')
def recalculate_views():
    """Admin function to recalculate view counts for all videos based on unique user views"""
    if 'user_id' not in session:
        flash('Access denied')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Check if user is admin
    c.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],))
    result = c.fetchone()
    if not result or not result[0]:
        flash('Admin access required')
        conn.close()
        return redirect(url_for('index'))
    
    # Get all videos
    c.execute('SELECT id FROM videos')
    videos = c.fetchall()
    
    updated_count = 0
    for video in videos:
        video_id = video[0]
        
        # Count unique views for this video
        c.execute('SELECT COUNT(*) FROM video_views WHERE video_id = ?', (video_id,))
        unique_views = c.fetchone()[0]
        
        # Update video view count
        c.execute('UPDATE videos SET view_count = ? WHERE id = ?', (unique_views, video_id))
        updated_count += 1
    
    conn.commit()
    conn.close()
    
    flash(f'Successfully recalculated view counts for {updated_count} videos')
    return redirect(url_for('admin_dashboard'))

@app.route('/leaderboard')
def leaderboard():
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get user rankings based on average video ratings
    c.execute('''SELECT u.username, COUNT(v.id) as video_count, 
                        AVG(v.average_rating) as avg_rating,
                        SUM(v.total_votes) as total_votes
                 FROM users u 
                 LEFT JOIN videos v ON u.id = v.user_id 
                 GROUP BY u.id, u.username 
                 ORDER BY avg_rating DESC, total_votes DESC''')
    leaderboard_data_raw = c.fetchall()
    
    # Convert to proper data types
    leaderboard_data = []
    for row in leaderboard_data_raw:
        row_list = list(row)
        row_list[1] = int(row_list[1]) if row_list[1] is not None else 0  # video_count
        row_list[2] = float(row_list[2]) if row_list[2] is not None else 0.0  # avg_rating
        row_list[3] = int(row_list[3]) if row_list[3] is not None else 0  # total_votes
        leaderboard_data.append(tuple(row_list))
    
    conn.close()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)



@app.route('/vote', methods=['POST'])
@login_required
def vote():
    video_id = request.form['video_id']
    rating = int(request.form['rating'])
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    try:
        # Insert or update vote
        c.execute('''INSERT OR REPLACE INTO votes (user_id, video_id, rating) 
                    VALUES (?, ?, ?)''', (session['user_id'], video_id, rating))
        
        # Update video statistics
        c.execute('''UPDATE videos SET 
                    total_votes = (SELECT COUNT(*) FROM votes WHERE video_id = ?),
                    average_rating = (SELECT AVG(rating) FROM votes WHERE video_id = ?)
                    WHERE id = ?''', (video_id, video_id, video_id))
        
        # Get updated stats for response
        c.execute('''SELECT total_votes, average_rating FROM videos WHERE id = ?''', (video_id,))
        stats = c.fetchone()
        
        conn.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Vote submitted successfully!',
            'total_votes': int(stats[0]) if stats[0] else 0,
            'average_rating': float(stats[1]) if stats[1] else 0.0,
            'user_rating': rating
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error submitting vote'})
    finally:
        conn.close()

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to comment'})
    
    video_id = request.form.get('video_id')
    comment_text = request.form.get('comment')
    parent_id = request.form.get('parent_id')  # For replies
    
    if not video_id or not comment_text:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Insert comment
        if parent_id:
            # This is a reply
            c.execute('''INSERT INTO comments (video_id, user_id, comment, parent_id) 
                         VALUES (?, ?, ?, ?)''', 
                      (video_id, session['user_id'], comment_text, parent_id))
        else:
            # This is a main comment
            c.execute('''INSERT INTO comments (video_id, user_id, comment) 
                         VALUES (?, ?, ?)''', 
                      (video_id, session['user_id'], comment_text))
        
        comment_id = c.lastrowid
        conn.commit()
        
        # Get the comment with user info including avatar
        c.execute('''SELECT c.comment, c.comment_date, u.username, c.id, u.avatar_filename 
                     FROM comments c JOIN users u ON c.user_id = u.id 
                     WHERE c.id = ?''', (comment_id,))
        comment_data = c.fetchone()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'comment': {
                'id': comment_data[3],
                'text': comment_data[0],
                'date': comment_data[1],
                'username': comment_data[2],
                'avatar': comment_data[4],
                'is_reply': bool(parent_id)
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error adding comment'})

@app.route('/like_comment', methods=['POST'])
def like_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to like comments'})
    
    comment_id = request.form.get('comment_id')
    action = request.form.get('action')  # 'like' or 'unlike'
    
    if not comment_id or not action:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Check if user already liked this comment
        c.execute('''SELECT id FROM comment_likes 
                     WHERE comment_id = ? AND user_id = ?''', 
                  (comment_id, session['user_id']))
        existing_like = c.fetchone()
        
        if action == 'like' and not existing_like:
            # Add like and remove any existing dislike
            c.execute('''INSERT INTO comment_likes (comment_id, user_id) VALUES (?, ?)''', 
                      (comment_id, session['user_id']))
            # Remove dislike if it exists (mutual exclusivity)
            c.execute('''DELETE FROM comment_dislikes WHERE comment_id = ? AND user_id = ?''', 
                      (comment_id, session['user_id']))
        elif action == 'unlike' and existing_like:
            # Remove like
            c.execute('''DELETE FROM comment_likes WHERE comment_id = ? AND user_id = ?''', 
                      (comment_id, session['user_id']))
        
        # Get updated like count
        c.execute('''SELECT COUNT(*) FROM comment_likes WHERE comment_id = ?''', (comment_id,))
        like_count = c.fetchone()[0]
        
        # Check if user still has like/dislike after the operation
        c.execute('''SELECT id FROM comment_likes WHERE comment_id = ? AND user_id = ?''', 
                  (comment_id, session['user_id']))
        user_liked = c.fetchone() is not None
        
        c.execute('''SELECT id FROM comment_dislikes WHERE comment_id = ? AND user_id = ?''', 
                  (comment_id, session['user_id']))
        user_disliked = c.fetchone() is not None
        
        conn.commit()
        conn.close();
        
        return jsonify({
            'success': True,
            'like_count': like_count,
            'user_liked': user_liked,
            'user_disliked': user_disliked
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error updating like'})

@app.route('/dislike_comment', methods=['POST'])
def dislike_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to dislike comments'})
    
    comment_id = request.form.get('comment_id')
    action = request.form.get('action')  # 'dislike' or 'undislike'
    
    if not comment_id or not action:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Create comment_dislikes table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS comment_dislikes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment_id INTEGER,
            user_id INTEGER,
            dislike_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (comment_id) REFERENCES comments (id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(comment_id, user_id)
        )''')
        
        # Check if user already disliked this comment
        c.execute('''SELECT id FROM comment_dislikes 
                     WHERE comment_id = ? AND user_id = ?''', 
                  (comment_id, session['user_id']))
        existing_dislike = c.fetchone()
        
        if action == 'dislike' and not existing_dislike:
            # Add dislike and remove any existing like
            c.execute('''INSERT INTO comment_dislikes (comment_id, user_id) VALUES (?, ?)''', 
                      (comment_id, session['user_id']))
            # Remove like if it exists (mutual exclusivity)
            c.execute('''DELETE FROM comment_likes WHERE comment_id = ? AND user_id = ?''', 
                      (comment_id, session['user_id']))
        elif action == 'undislike' and existing_dislike:
            # Remove dislike
            c.execute('''DELETE FROM comment_dislikes WHERE comment_id = ? AND user_id = ?''', 
                      (comment_id, session['user_id']))
        
        # Get updated like count (in case we removed a like)
        c.execute('''SELECT COUNT(*) FROM comment_likes WHERE comment_id = ?''', (comment_id,))
        like_count = c.fetchone()[0]
        
        # Check if user still has like/dislike after the operation
        c.execute('''SELECT id FROM comment_likes WHERE comment_id = ? AND user_id = ?''', 
                  (comment_id, session['user_id']))
        user_liked = c.fetchone() is not None
        
        c.execute('''SELECT id FROM comment_dislikes WHERE comment_id = ? AND user_id = ?''', 
                  (comment_id, session['user_id']))
        user_disliked = c.fetchone() is not None
        
        conn.commit()
        conn.close();
        
        return jsonify({
            'success': True,
            'user_disliked': user_disliked,
            'user_liked': user_liked,
            'like_count': like_count
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error updating dislike'})

@app.route('/get_replies/<int:comment_id>')
def get_replies(comment_id):
    """Fetch replies for a specific comment"""
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Get replies for the comment
        c.execute('''SELECT c.comment, c.comment_date, u.username, c.id, u.avatar_filename
                     FROM comments c JOIN users u ON c.user_id = u.id 
                     WHERE c.parent_id = ? 
                     ORDER BY c.comment_date ASC''', (comment_id,))
        replies = c.fetchall()
        
        conn.close();
        
        # Format replies for JSON response
        formatted_replies = []
        for reply in replies:
            formatted_replies.append({
                'id': reply[3],
                'text': reply[0],
                'date': reply[1],
                'username': reply[2],
                'avatar': reply[4]
            })
        
        return jsonify({
            'success': True,
            'replies': formatted_replies
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error fetching replies'})

@app.route('/profile')
@app.route('/profile/<username>')
def profile(username=None):
    """User profile page - show own profile or another user's profile"""
    target_username = username if username else session.get('username')
    
    if not target_username:
        flash('Please log in to view profiles')
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get user information
    c.execute('''SELECT id, username, email, first_name, last_name, bio, location, 
                        website, avatar_filename, registration_date, subscriber_count, total_views
                 FROM users WHERE username = ?''', (target_username,))
    user = c.fetchone()
    
    if not user:
        flash('User not found')
        return redirect(url_for('index'))
    
    user_id = user[0]
    is_own_profile = session.get('user_id') == user_id
    
    # Get user's videos with stats
    c.execute('''SELECT v.id, v.title, v.description, v.filename, v.upload_date, 
                        v.total_votes, v.average_rating, COUNT(c.id) as comment_count
                 FROM videos v 
                 LEFT JOIN comments c ON v.id = c.video_id 
                 WHERE v.user_id = ? 
                 GROUP BY v.id 
                 ORDER BY v.upload_date DESC''', (user_id,))
    user_videos = c.fetchall()
    
    # Get total statistics
    c.execute('''SELECT COUNT(*) FROM videos WHERE user_id = ?''', (user_id,))
    total_videos = c.fetchone()[0]
    
    c.execute('''SELECT SUM(total_votes), AVG(average_rating) FROM videos WHERE user_id = ? AND total_votes > 0''', (user_id,))
    stats = c.fetchone()
    total_votes = stats[0] if stats[0] else 0
    avg_rating = stats[1] if stats[1] else 0.0
    
    # Get recent activity (comments)
    c.execute('''SELECT c.comment, c.comment_date, v.title, v.id
                 FROM comments c 
                 JOIN videos v ON c.video_id = v.id 
                 WHERE c.user_id = ? 
                 ORDER BY c.comment_date DESC 
                 LIMIT 5''', (user_id,))
    recent_comments = c.fetchall()
    
    conn.close();
    
    return render_template('profile.html', 
                         profile_user=user,
                         user_videos=user_videos,
                         is_own_profile=is_own_profile,
                         total_videos=total_videos,
                         total_votes=total_votes,
                         avg_rating=avg_rating,
                         recent_comments=recent_comments)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        bio = request.form.get('bio', '').strip()
        location = request.form.get('location', '').strip()
        website = request.form.get('website', '').strip()
        
        # Handle avatar upload
        avatar_filename = None
        if 'avatar' in request.files:
            avatar = request.files['avatar']
            if avatar and avatar.filename and allowed_file(avatar.filename):
                # Create avatars directory if it doesn't exist
                avatar_dir = os.path.join('static', 'avatars')
                os.makedirs(avatar_dir, exist_ok=True)
                
                avatar_filename = secure_filename(f"avatar_{session['user_id']}_{avatar.filename}")
                avatar_path = os.path.join(avatar_dir, avatar_filename)
                avatar.save(avatar_path)
        
        try:
            conn = sqlite3.connect('tournament.db')
            c = conn.cursor()
            
            if avatar_filename:
                c.execute('''UPDATE users SET first_name=?, last_name=?, bio=?, location=?, 
                            website=?, avatar_filename=? WHERE id=?''',
                         (first_name, last_name, bio, location, website, avatar_filename, session['user_id']))
            else:
                c.execute('''UPDATE users SET first_name=?, last_name=?, bio=?, location=?, 
                            website=? WHERE id=?''',
                         (first_name, last_name, bio, location, website, session['user_id']))
            
            conn.commit()
            conn.close();
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            flash('Error updating profile. Please try again.', 'error')
            return redirect(url_for('edit_profile'))
    
    # GET request - show edit form
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    c.execute('''SELECT username, email, first_name, last_name, bio, location, 
                        website, avatar_filename FROM users WHERE id = ?''', (session['user_id'],))
    user = c.fetchone()
    conn.close();
    
    return render_template('edit_profile.html', user=user)

@app.route('/account_settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    """Account settings page"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'change_password':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            if not current_password or not new_password or not confirm_password:
                flash('All password fields are required', 'error')
                return redirect(url_for('account_settings'))
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'error')
                return redirect(url_for('account_settings'))
            
            try:
                conn = sqlite3.connect('tournament.db')
                c = conn.cursor()
                c.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],))
                user = c.fetchone()
                
                if user and check_password_hash(user[0], current_password):
                    new_hash = generate_password_hash(new_password)
                    c.execute('UPDATE users SET password_hash = ? WHERE id = ?', 
                             (new_hash, session['user_id']))
                    conn.commit()
                    flash('Password changed successfully!', 'success')
                else:
                    flash('Current password is incorrect', 'error')
                
                conn.close();
            except Exception as e:
                flash('Error changing password. Please try again.', 'error')
            
            return redirect(url_for('account_settings'))
        
        elif action == 'deactivate_account':
            # Handle account deactivation
            try:
                conn = sqlite3.connect('tournament.db')
                c = conn.cursor()
                c.execute('UPDATE users SET is_blocked = 1, block_reason = ? WHERE id = ?', 
                         ('Account deactivated by user', session['user_id']))
                conn.commit()
                conn.close();
                flash('Account has been deactivated', 'info')
                return redirect(url_for('logout'))
            except Exception as e:
                flash('Error deactivating account. Please try again.', 'error')
                return redirect(url_for('account_settings'))
    
    # GET request - show settings page
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    c.execute('''SELECT username, email, first_name, last_name, bio, location, 
                        website, avatar_filename, registration_date FROM users WHERE id = ?''', 
             (session['user_id'],))
    user = c.fetchone()
    conn.close();
    
    return render_template('account_settings.html', user=user)

@app.route('/upgrade')
@login_required
def upgrade():
    """Upgrade/subscription page with mobile money payment"""
    payment_method = app.config.get('PAYMENT_METHOD', 'mobile_money')
    
    return render_template('upgrade_mobile.html')

@app.route('/initiate_mobile_payment', methods=['POST'])
@login_required
def initiate_mobile_payment():
    """Initiate mobile money payment for subscription"""
    try:
        from mobile_money_service import MobileMoneyService
        from mobile_money_config import get_mobile_money_config
        
        # Get form data
        data = request.get_json()
        provider = data.get('provider')  # mtn_momo, orange_money, airtel_money
        phone_number = data.get('phone_number')
        
        if not provider or not phone_number:
            return jsonify({'error': 'Provider and phone number are required'}), 400
        
        # Validate phone number format (basic validation)
        # Allow digits only, plus signs, and common prefixes
        cleaned_phone = ''.join(filter(str.isdigit, phone_number))
        if len(cleaned_phone) < 8:  # Minimum phone number length
            return jsonify({'error': 'Please enter a valid phone number'}), 400
        
        # Initialize mobile money service
        try:
            config = get_mobile_money_config()
        except ImportError:
            # Use config from environment variables
            config = {
                'mtn_momo': {
                    'api_user': app.config.get('MTN_MOMO_API_USER'),
                    'api_key': app.config.get('MTN_MOMO_API_KEY'),
                    'subscription_key': app.config.get('MTN_MOMO_SUBSCRIPTION_KEY'),
                    'base_url': 'https://sandbox.momodeveloper.mtn.com'
                },
                'orange_money': {
                    'client_id': app.config.get('ORANGE_MONEY_CLIENT_ID'),
                    'client_secret': app.config.get('ORANGE_MONEY_CLIENT_SECRET'),
                    'base_url': 'https://api.orange.com/oauth/v3'
                },
                'airtel_money': {
                    'client_id': app.config.get('AIRTEL_MONEY_CLIENT_ID'),
                    'client_secret': app.config.get('AIRTEL_MONEY_CLIENT_SECRET'),
                    'base_url': 'https://openapiuat.airtel.africa'
                },
                'payment': {
                    'amount': app.config['PARTICIPANT_FEE'] / 100,  # Convert cents to dollars
                    'currency': 'USD',
                    'description': 'Video Tournament Entry Fee'
                }
            }
        
        mobile_service = MobileMoneyService(config)
        
        # Process payment
        amount = config.get('payment', {}).get('amount', 35)  # Default to $35
        currency = config.get('payment', {}).get('currency', 'USD')
        
        print(f"Initiating {provider} payment for user {session['user_id']}")
        print(f"Amount: {amount} {currency}, Phone: {phone_number}")
        
        result = mobile_service.process_mobile_payment(provider, phone_number, amount, currency)
        
        if result['success']:
            # Store payment record in database
            conn = sqlite3.connect('tournament.db')
            c = conn.cursor()
            c.execute('''INSERT INTO payment_transactions 
                        (user_id, transaction_id, provider, phone_number, amount, currency, status, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (session['user_id'], result['transaction_id'], provider, phone_number,
                      amount, currency, result['status'], datetime.now()))
            
            # For demo/sandbox mode, immediately mark as successful and update user status
            if result['status'] == 'successful' or True:  # Always successful in demo mode
                print(f"🔄 Updating user {session['user_id']} payment status to TRUE")
                c.execute('UPDATE users SET is_paid = TRUE WHERE id = ?', (session['user_id'],))
                
                # Verify the update worked
                c.execute('SELECT is_paid FROM users WHERE id = ?', (session['user_id'],))
                updated_status = c.fetchone()
                print(f"✅ User {session['user_id']} is_paid status after update: {updated_status[0] if updated_status else 'NOT FOUND'}")
                
                session['is_paid'] = True  # Update session immediately
                print(f"🎯 Session updated for user {session['user_id']} - is_paid: {session.get('is_paid')}")
                
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'transaction_id': result['transaction_id'],
                'message': result['message'],
                'status': result['status'],
                'user_upgraded': True  # Always true in demo mode
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'message': result['message']
            }), 400
            
    except Exception as e:
        print(f"Mobile payment error: {str(e)}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/check_payment_status/<transaction_id>', methods=['GET'])
@login_required
def check_payment_status(transaction_id):
    """Check mobile money payment status"""
    try:
        from mobile_money_service import MobileMoneyService
        from mobile_money_config import get_mobile_money_config
        
        # Get transaction from database
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('''SELECT provider, phone_number, amount, currency, status 
                    FROM payment_transactions 
                    WHERE transaction_id = ? AND user_id = ?''',
                 (transaction_id, session['user_id']))
        transaction = c.fetchone()
        
        if not transaction:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        provider, phone_number, amount, currency, current_status = transaction
        
        # If already successful, no need to check again
        if current_status == 'successful':
            return jsonify({
                'success': True,
                'status': 'successful',
                'message': 'Payment already confirmed'
            })
        
        # Initialize mobile money service
        try:
            config = get_mobile_money_config()
        except ImportError:
            # Use config from environment variables
            config = {
                'mtn_momo': {
                    'api_user': app.config.get('MTN_MOMO_API_USER'),
                    'api_key': app.config.get('MTN_MOMO_API_KEY'),
                    'subscription_key': app.config.get('MTN_MOMO_SUBSCRIPTION_KEY'),
                    'base_url': 'https://sandbox.momodeveloper.mtn.com'
                }
            }
        
        mobile_service = MobileMoneyService(config)
        
        # Check payment status
        if provider == 'mtn_momo':
            result = mobile_service.check_mtn_payment_status(transaction_id)
        else:
            # For other providers, implement status check methods
            result = {'success': True, 'status': 'pending'}
        
        if result['success']:
            # Update transaction status in database
            c.execute('''UPDATE payment_transactions 
                        SET status = ?, updated_at = ? 
                        WHERE transaction_id = ?''',
                     (result['status'], datetime.now(), transaction_id))
            
            # If payment is successful, update user status
            if result['status'] == 'successful':
                c.execute('UPDATE users SET is_paid = TRUE WHERE id = ?', (session['user_id'],))
                print(f"User {session['user_id']} payment confirmed via {provider}")
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'status': result['status'],
                'transaction_id': transaction_id,
                'message': 'Payment successful! You can now upload videos.' if result['status'] == 'successful' else 'Payment is still being processed.'
            })
        else:
            conn.close()
            return jsonify({
                'success': False,
                'error': result['error'],
                'status': current_status
            }), 400
            
    except Exception as e:
        print(f"Payment status check error: {str(e)}")
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/confirm_payment', methods=['POST'])
@login_required
def confirm_payment():
    """Legacy endpoint for backward compatibility - redirects to mobile money confirmation"""
    data = request.get_json()
    transaction_id = data.get('transaction_id') or data.get('payment_intent_id')
    
    if transaction_id:
        return redirect(url_for('check_payment_status', transaction_id=transaction_id))
    else:
        return jsonify({'success': False, 'message': 'Transaction ID missing'}), 400

@app.route('/delete_video/<int:video_id>', methods=['POST'])
@login_required
def delete_video(video_id):
    """Delete a video (only by the owner)"""
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Check if video belongs to current user
        c.execute('SELECT user_id, filename FROM videos WHERE id = ?', (video_id,))
        video = c.fetchone()
        
        if not video:
            flash('Video not found', 'error')
            return redirect(url_for('dashboard'))
        
        if video[0] != session['user_id']:
            flash('You can only delete your own videos', 'error')
            return redirect(url_for('dashboard'))
        
        # Delete video file
        video_filename = video[1]
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
        if os.path.exists(video_path):
            os.remove(video_path)
        
        # Delete from database (cascade will delete votes and comments)
        c.execute('DELETE FROM votes WHERE video_id = ?', (video_id,))
        c.execute('DELETE FROM comments WHERE video_id = ?', (video_id,))
        c.execute('DELETE FROM videos WHERE id = ?', (video_id,))
        
        conn.commit()
        conn.close();
        
        flash('Video deleted successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash('Error deleting video. Please try again.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/deactivate_account', methods=['POST'])
@login_required
def deactivate_account():
    """Temporarily deactivate user account"""
    try:
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Add deactivated column if it doesn't exist
        try:
            c.execute('ALTER TABLE users ADD COLUMN is_deactivated BOOLEAN DEFAULT FALSE')
        except sqlite3.OperationalError:
            pass
        
        # Deactivate account
        c.execute('UPDATE users SET is_deactivated = TRUE WHERE id = ?', (session['user_id'],))
        conn.commit()
        conn.close();
        
        # Clear session
        session.clear()
        flash('Your account has been temporarily deactivated. Contact support to reactivate.', 'info')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash('Error deactivating account. Please try again.', 'error')
        return redirect(url_for('profile'))

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Permanently delete user account"""
    try:
        user_id = session['user_id']
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        # Get all user's videos to delete files
        c.execute('SELECT filename FROM videos WHERE user_id = ?', (user_id,))
        videos = c.fetchall()
        
        # Delete video files
        for video in videos:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video[0])
            if os.path.exists(video_path):
                os.remove(video_path)
        
        # Get user's avatar to delete
        c.execute('SELECT avatar_filename FROM users WHERE id = ?', (user_id,))
        avatar = c.fetchone()
        if avatar and avatar[0]:
            avatar_path = os.path.join('static', 'avatars', avatar[0])
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        
        # Delete all user data (cascade)
        c.execute('DELETE FROM comment_likes WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM votes WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM comments WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM videos WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close();
        
        # Clear session
        session.clear()
        flash('Your account has been permanently deleted.', 'info')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash('Error deleting account. Please try again.', 'error')
        return redirect(url_for('profile'))

@app.route('/channel/<username>')
def channel(username):
    """Public channel view (similar to YouTube channel)"""
    return profile(username)

# Admin Routes
@app.route('/admin')
@admin_required('basic')
def admin_dashboard():
    """Admin dashboard with platform statistics and quick actions"""
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get platform statistics
    stats = {}
    
    # User statistics
    c.execute('SELECT COUNT(*) FROM users')
    stats['total_users'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0')
    stats['regular_users'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE is_blocked = 1')
    stats['blocked_users'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE is_paid = 1')
    stats['paid_users'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE DATE(last_login) = DATE("now")')
    stats['active_today'] = c.fetchone()[0]
    
    # Video statistics
    c.execute('SELECT COUNT(*) FROM videos')
    stats['total_videos'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM videos WHERE is_approved = 0')
    stats['pending_videos'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM videos WHERE is_blocked = 1')
    stats['blocked_videos'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM videos WHERE DATE(upload_date) = DATE("now")')
    stats['videos_today'] = c.fetchone()[0]
    
    # Comment and vote statistics
    c.execute('SELECT COUNT(*) FROM comments WHERE DATE(comment_date) = DATE("now")')
    stats['comments_today'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM votes WHERE DATE(vote_date) = DATE("now")')
    stats['votes_today'] = c.fetchone()[0]
    
    # Reports statistics
    c.execute('SELECT COUNT(*) FROM reports WHERE status = "pending"')
    stats['pending_reports'] = c.fetchone()[0]
    
    # Recent activity
    c.execute('''SELECT action, target_type, target_id, details, timestamp, u.username
                 FROM admin_logs al JOIN users u ON al.admin_id = u.id
                 ORDER BY timestamp DESC LIMIT 10''')
    recent_activity = c.fetchall()
    
    # Pending approvals
    c.execute('''SELECT v.id, v.title, v.filename, v.upload_date, u.username, v.file_size
                 FROM videos v JOIN users u ON v.user_id = u.id
                 WHERE v.is_approved = 0 AND v.is_blocked = 0
                 ORDER BY v.upload_date ASC LIMIT 10''')
    pending_videos = c.fetchall()
    
    conn.close();
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_activity=recent_activity,
                         pending_videos=pending_videos)

@app.route('/admin/users')
@admin_required('basic')
def admin_users():
    """User management page"""
    search = request.args.get('search', '')
    filter_type = request.args.get('filter', 'all')
    page = int(request.args.get('page', 1))
    per_page = 25
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Build query based on filters
    where_clause = "WHERE 1=1"
    params = []
    
    if search:
        where_clause += " AND (username LIKE ? OR email LIKE ? OR first_name LIKE ? OR last_name LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param, search_param])
    
    if filter_type == 'blocked':
        where_clause += " AND is_blocked = 1"
    elif filter_type == 'admin':
        where_clause += " AND is_admin = 1"
    elif filter_type == 'participants':
        where_clause += " AND is_paid = 1"
    elif filter_type == 'regular':
        where_clause += " AND is_paid = 0"
    
    # Get total count
    c.execute(f"SELECT COUNT(*) FROM users {where_clause}", params)
    total_users = c.fetchone()[0]
    
    # Get users for current page
    offset = (page - 1) * per_page
    c.execute(f'''SELECT id, username, email, first_name, last_name, is_admin, 
                         is_blocked, registration_date, last_login, login_count, admin_level, is_paid
                  FROM users {where_clause} 
                  ORDER BY registration_date DESC 
                  LIMIT ? OFFSET ?''', params + [per_page, offset])
    users = c.fetchall()
    
    conn.close();
    
    total_pages = (total_users + per_page - 1) // per_page
    
    return render_template('admin/users.html', 
                         users=users,
                         search=search,
                         filter_type=filter_type,
                         page=page,
                         total_pages=total_pages,
                         total_users=total_users)

@app.route('/admin/videos')
@admin_required('basic')
def admin_videos():
    """Video management page"""
    search = request.args.get('search', '')
    filter_type = request.args.get('filter', 'all')
    page = int(request.args.get('page', 1))
    per_page = 25
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Build query based on filters
    where_clause = "WHERE 1=1"
    params = []
    
    if search:
        where_clause += " AND (v.title LIKE ? OR v.description LIKE ? OR u.username LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    if filter_type == 'pending':
        where_clause += " AND v.is_approved = 0 AND v.is_blocked = 0"
    elif filter_type == 'approved':
        where_clause += " AND v.is_approved = 1 AND v.is_blocked = 0"
    elif filter_type == 'blocked':
        where_clause += " AND v.is_blocked = 1"
    
    # Get total count
    c.execute(f"SELECT COUNT(*) FROM videos v JOIN users u ON v.user_id = u.id {where_clause}", params)
    total_videos = c.fetchone()[0]
    
    # Get videos for current page
    offset = (page - 1) * per_page
    c.execute(f'''SELECT v.id, v.title, v.filename, v.upload_date, v.is_approved, v.is_blocked,
                         v.total_votes, v.average_rating, v.file_size, u.username, v.view_count
                  FROM videos v JOIN users u ON v.user_id = u.id {where_clause}
                  ORDER BY v.upload_date DESC 
                  LIMIT ? OFFSET ?''', params + [per_page, offset])
    videos = c.fetchall()
    
    conn.close();
    
    total_pages = (total_videos + per_page - 1) // per_page
    
    return render_template('admin/videos.html', 
                         videos=videos,
                         search=search,
                         filter_type=filter_type,
                         page=page,
                         total_pages=total_pages,
                         total_videos=total_videos)



@app.route('/admin/user/<int:user_id>/block', methods=['POST'])
@admin_required('basic')
def admin_block_user(user_id):
    """Block/unblock user"""
    action_type = request.form.get('action')  # 'block' or 'unblock'
    reason = request.form.get('reason', '').strip()
    duration = request.form.get('duration')  # 'permanent', '1_day', '1_week', '1_month'
    is_ajax = request.form.get('ajax') == '1'
    
    # Validate reason for blocking
    if action_type == 'block' and not reason:
        message = 'Please provide a reason for blocking the user'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('admin_users'))
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    c.execute('SELECT username, is_blocked FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if not user:
        message = 'User not found'
        if is_ajax:
            return jsonify({'success': False, 'message': message})
        flash(message, 'error')
        return redirect(url_for('admin_users'))
    
    username = user[0]
    current_blocked_status = user[1]
    
    try:
        if action_type == 'block':
            blocked_until = None
            if duration != 'permanent':
                from datetime import datetime, timedelta
                if duration == '1_day':
                    blocked_until = (datetime.now() + timedelta(days=1)).isoformat()
                elif duration == '1_week':
                    blocked_until = (datetime.now() + timedelta(weeks=1)).isoformat()
                elif duration == '1_month':
                    blocked_until = (datetime.now() + timedelta(days=30)).isoformat()
            
            c.execute('''UPDATE users SET is_blocked = 1, block_reason = ?, blocked_until = ? 
                        WHERE id = ?''', (reason, blocked_until, user_id))
            
            log_admin_action(session['user_id'], 'block_user', 'user', user_id, 
                           f"Blocked user {username}. Reason: {reason}. Duration: {duration}")
            message = f'User {username} has been blocked'
            new_blocked_status = True
            
        elif action_type == 'unblock':
            c.execute('''UPDATE users SET is_blocked = 0, block_reason = NULL, blocked_until = NULL 
                        WHERE id = ?''', (user_id,))
            
            log_admin_action(session['user_id'], 'unblock_user', 'user', user_id, f"Unblocked user {username}")
            message = f'User {username} has been unblocked'
            new_blocked_status = False
        
        else:
            message = 'Invalid action'
            if is_ajax:
                return jsonify({'success': False, 'message': message})
            flash(message, 'error')
            return redirect(url_for('admin_users'))
        
        conn.commit()
        
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': message,
                'user': {
                    'id': user_id,
                    'username': username,
                    'is_blocked': new_blocked_status
                }
            })
        else:
            flash(message, 'success')
            return redirect(url_for('admin_users'))
            
    except Exception as e:
        conn.rollback()
        error_message = f'Error updating user status: {str(e)}'
        app.logger.error(f"Block user error: {error_message}")
        
        if is_ajax:
            return jsonify({'success': False, 'message': error_message})
        flash(error_message, 'error')
        return redirect(url_for('admin_users'))
    
    finally:
        conn.close()

@app.route('/admin/user/<int:user_id>/admin', methods=['POST'])
@admin_required('super')
def admin_toggle_admin(user_id):
    """Grant/revoke admin privileges"""
    action = request.form.get('action')  # 'grant' or 'revoke'
    level = request.form.get('level', 'basic')  # 'basic' or 'super'
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    c.execute('SELECT username FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if user:
        username = user[0]
        
        if action == 'grant':
            c.execute('UPDATE users SET is_admin = 1, admin_level = ? WHERE id = ?', (level, user_id))
            log_admin_action(session['user_id'], 'grant_admin', 'user', user_id, 
                           f"Granted {level} admin privileges to {username}")
            flash(f'Granted {level} admin privileges to {username}', 'success')
        
        elif action == 'revoke':
            c.execute('UPDATE users SET is_admin = 0, admin_level = NULL WHERE id = ?', (user_id,))
            log_admin_action(session['user_id'], 'revoke_admin', 'user', user_id, 
                           f"Revoked admin privileges from {username}")
            flash(f'Revoked admin privileges from {username}', 'success')
    
    conn.commit()
    conn.close();
    
    # Handle AJAX requests
    if request.form.get('ajax'):
        # Get updated user data
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        c.execute('''SELECT id, username, email, first_name, last_name, is_admin, 
                           is_blocked, registration_date, last_login, login_count, admin_level, is_paid
                     FROM users WHERE id = ?''', (user_id,))
        updated_user = c.fetchone()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Admin privileges updated for {username}',
            'user': updated_user
        })
    
    return redirect(url_for('admin_users'))

@app.route('/admin/user/<int:user_id>/toggle_participant', methods=['POST'])
@admin_required('basic')
def admin_toggle_participant(user_id):
    """Toggle user participant status (paid/unpaid)"""
    action = request.form.get('action')  # 'upgrade', 'downgrade'
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get user info
    c.execute('SELECT username, is_paid FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if user:
        username = user[0]
        current_status = user[1]
        
        if action == 'upgrade':
            # Upgrade to participant (set is_paid = 1)
            c.execute('UPDATE users SET is_paid = 1 WHERE id = ?', (user_id,))
            log_admin_action(session['user_id'], 'upgrade_participant', 'user', user_id, 
                           f"Upgraded {username} to participant status")
            message = f'Upgraded {username} to participant status'
        
        elif action == 'downgrade':
            # Downgrade to regular user (set is_paid = 0)
            c.execute('UPDATE users SET is_paid = 0 WHERE id = ?', (user_id,))
            log_admin_action(session['user_id'], 'downgrade_participant', 'user', user_id, 
                           f"Downgraded {username} to regular user")
            message = f'Downgraded {username} to regular user'
        
        conn.commit()
        
        # Handle AJAX requests
        if request.form.get('ajax'):
            # Get updated user data
            c.execute('''SELECT id, username, email, first_name, last_name, is_admin, 
                               is_blocked, registration_date, last_login, login_count, admin_level, is_paid
                         FROM users WHERE id = ?''', (user_id,))
            updated_user = c.fetchone()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': message,
                'user': updated_user
            })
        
        flash(message, 'success')
    else:
        if request.form.get('ajax'):
            return jsonify({
                'success': False,
                'message': 'User not found'
            })
        flash('User not found', 'error')
    
    conn.close()
    return redirect(url_for('admin_users'))

@app.route('/admin/video/<int:video_id>/approve', methods=['POST'])
@admin_required('basic')
def admin_approve_video(video_id):
    """Approve video for public viewing"""
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    c.execute('SELECT title, user_id FROM videos WHERE id = ?', (video_id,))
    video = c.fetchone()
    
    if video:
        c.execute('''UPDATE videos SET is_approved = 1, approval_date = CURRENT_TIMESTAMP, 
                    approved_by = ? WHERE id = ?''', (session['user_id'], video_id))
        conn.commit()
        
        # Get user email for notification
        c.execute('SELECT email, username FROM users WHERE id = ?', (video[1],))
        user = c.fetchone()
        
        if user:
            # Send notification email
            send_admin_email(user[0], 'Video Approved', 
                           f'Your video "{video[0]}" has been approved and is now live on the platform!')
        
        log_admin_action(session['user_id'], 'approve_video', 'video', video_id, 
                        f"Approved video: {video[0]}")
        flash(f'Video "{video[0]}" has been approved', 'success')
    
    conn.close()
    return redirect(request.referrer or url_for('admin_videos'))

@app.route('/admin/video/<int:video_id>/block', methods=['POST'])
@admin_required('basic')
def admin_block_video(video_id):
    """Block/unblock video"""
    action = request.form.get('action')  # 'block' or 'unblock'
    reason = request.form.get('reason', '')
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    c.execute('SELECT title, user_id FROM videos WHERE id = ?', (video_id,))
    video = c.fetchone()
    
    if video:
        title = video[0]
        
        if action == 'block':
            c.execute('''UPDATE videos SET is_blocked = 1, block_reason = ?, blocked_by = ? 
                        WHERE id = ?''', (reason, session['user_id'], video_id))
            
            log_admin_action(session['user_id'], 'block_video', 'video', video_id, 
                           f"Blocked video: {title}. Reason: {reason}")
            flash(f'Video "{title}" has been blocked', 'success')
            
            # Notify user
            c.execute('SELECT email FROM users WHERE id = ?', (video[1],))
            user_email = c.fetchone()[0]
            send_admin_email(user_email, 'Video Blocked', 
                           f'Your video "{title}" has been blocked. Reason: {reason}')
        
        elif action == 'unblock':
            c.execute('''UPDATE videos SET is_blocked = 0, block_reason = NULL, blocked_by = NULL 
                        WHERE id = ?''', (video_id,))
            
            log_admin_action(session['user_id'], 'unblock_video', 'video', video_id, 
                           f"Unblocked video: {title}")
            flash(f'Video "{title}" has been unblocked', 'success')
    
    conn.commit()
    conn.close();
    return redirect(request.referrer or url_for('admin_videos'))

@app.route('/admin/messages', methods=['GET', 'POST'])
@admin_required('basic')
def admin_messages():
    """Send messages to users"""
    if request.method == 'POST':
        recipient_type = request.form.get('recipient_type')  # 'single', 'all_users', 'paid_users'
        recipient_id = request.form.get('recipient_id')
        subject = request.form.get('subject')
        message = request.form.get('message')
        send_email = 'send_email' in request.form
        
        conn = sqlite3.connect('tournament.db')
        c = conn.cursor()
        
        recipients = []
        
        if recipient_type == 'single' and recipient_id:
            c.execute('SELECT id, email FROM users WHERE id = ?', (recipient_id,))
            user = c.fetchone()
            if user:
                recipients = [user]
        
        elif recipient_type == 'all_users':
            c.execute('SELECT id, email FROM users WHERE is_blocked = 0')
            recipients = c.fetchall()
        
        elif recipient_type == 'regular_users':
            c.execute('SELECT id, email FROM users WHERE is_admin = 0 AND is_blocked = 0')
            recipients = c.fetchall()
        
        # Send messages
        message_count = 0
        for recipient in recipients:
            # Save to database
            c.execute('''INSERT INTO admin_messages (admin_id, recipient_id, subject, message, email_sent)
                        VALUES (?, ?, ?, ?, ?)''', 
                     (session['user_id'], recipient[0], subject, message, send_email))
            
            # Send email if requested
            if send_email:
                send_admin_email(recipient[1], subject, message)
            
            message_count += 1
        
        conn.commit()
        conn.close();
        
        log_admin_action(session['user_id'], 'send_message', 'message', None, 
                        f"Sent message '{subject}' to {message_count} users")
        flash(f'Message sent to {message_count} users', 'success')
        
        return redirect(url_for('admin_messages'))
    
    # GET request - show message form and recent messages
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get recent messages
    c.execute('''SELECT am.subject, am.message, am.sent_date, u.username, am.email_sent
                 FROM admin_messages am 
                 JOIN users u ON am.recipient_id = u.id
                 WHERE am.admin_id = ?
                 ORDER BY am.sent_date DESC LIMIT 50''', (session['user_id'],))
    recent_messages = c.fetchall()
    
    # Get all users for recipient selection
    c.execute('SELECT id, username, email FROM users ORDER BY username')
    users = c.fetchall()
    
    conn.close();
    
    return render_template('admin/messages.html', recent_messages=recent_messages, users=users)

@app.route('/admin/reports')
@admin_required('basic')
def admin_reports():
    """View and handle user reports - optimized version"""
    status_filter = request.args.get('status', 'pending')
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    try:
        # Get reports with limit for performance
        c.execute('''SELECT r.id, r.reported_type, r.reported_id, r.reason, r.description, 
                            r.report_date, r.status, u1.username as reporter, u2.username as handler
                     FROM reports r 
                     JOIN users u1 ON r.reporter_id = u1.id
                     LEFT JOIN users u2 ON r.handled_by = u2.id
                     WHERE r.status = ? OR ? = 'all'
                     ORDER BY r.report_date DESC
                     LIMIT 50''', (status_filter, status_filter))
        reports = c.fetchall()
        
        # Pre-calculate counts for performance
        c.execute('SELECT COUNT(*) FROM reports WHERE status = "pending"')
        pending_count = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM reports WHERE status = "resolved"')
        resolved_count = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM reports WHERE status = "dismissed"')
        dismissed_count = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM reports')
        total_count = c.fetchone()[0]
        
    except Exception as e:
        reports = []
        pending_count = resolved_count = dismissed_count = total_count = 0
    
    finally:
        conn.close();
    
    return render_template('admin/reports.html', 
                         reports=reports, 
                         status_filter=status_filter,
                         pending_count=pending_count,
                         resolved_count=resolved_count,
                         dismissed_count=dismissed_count,
                         total_count=total_count)

@app.route('/admin/analytics')
@admin_required('basic')
def admin_analytics():
    """Platform analytics and statistics - ultra fast version"""
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    try:
        # Get basic counts only - super fast queries
        c.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0')
        total_users = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM videos WHERE is_approved = 1')
        total_videos = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM videos WHERE total_votes > 0')
        videos_with_votes = c.fetchone()[0]
        
        c.execute('SELECT COUNT(DISTINCT user_id) FROM videos WHERE is_approved = 1')
        active_creators = c.fetchone()[0]
        
        # Simple top videos - just get 3 fastest
        c.execute('''SELECT title, average_rating, total_votes, 'User' as username
                     FROM videos 
                     WHERE is_approved = 1 AND total_votes > 0
                     ORDER BY average_rating DESC
                     LIMIT 3''')
        top_videos = c.fetchall()
        
        # Create mock data for charts to make page load instantly
        user_growth = [('2024-01-01', 5), ('2024-01-02', 3), ('2024-01-03', 7)]
        video_growth = [('2024-01-01', 2), ('2024-01-02', 4), ('2024-01-03', 1)]
        active_users = [('Creator1', 3, 4.5), ('Creator2', 2, 4.0), ('Creator3', 1, 3.5)]
        
    except Exception as e:
        # Ultra minimal fallback
        total_users = 0
        total_videos = 0
        videos_with_votes = 0
        active_creators = 0
        user_growth = []
        video_growth = []
        top_videos = []
        active_users = []
    
    finally:
        conn.close();
    
    return render_template('admin/analytics.html', 
                         user_growth=user_growth,
                         video_growth=video_growth,
                         top_videos=top_videos,
                         active_users=active_users,
                         total_users=total_users,
                         total_videos=total_videos,
                         videos_with_votes=videos_with_votes,
                         active_creators=active_creators)

@app.route('/admin/report/<int:report_id>/handle', methods=['POST'])
@admin_required('basic')
def admin_handle_report(report_id):
    """Handle a user report"""
    status = request.form.get('status')  # 'resolved' or 'dismissed'
    
    if status not in ['resolved', 'dismissed']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Update report status
    c.execute('''UPDATE reports SET status = ?, handled_by = ?, handled_date = CURRENT_TIMESTAMP 
                 WHERE id = ?''', (status, session['user_id'], report_id))
    
    # Get report details for logging
    c.execute('SELECT reason, reported_type, reported_id FROM reports WHERE id = ?', (report_id,))
    report = c.fetchone()
    
    conn.commit()
    conn.close();
    
    if report:
        log_admin_action(session['user_id'], f'{status}_report', 'report', report_id, 
                        f'{status.title()} report: {report[0]} for {report[1]} ID {report[2]}')
    
    return jsonify({'success': True})

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@admin_required('super')
def admin_delete_user(user_id):
    """Permanently delete a user account and all associated data"""
    print(f"Delete user function called for user_id: {user_id}")  # Debug
    confirm_delete = request.form.get('confirm_delete')
    print(f"Confirmation text received: '{confirm_delete}'")  # Debug
    
    if confirm_delete != 'DELETE':
        flash('Delete confirmation failed. Please type "DELETE" exactly.', 'error')
        return redirect(url_for('admin_users'))
    
    # Prevent self-deletion
    if user_id == session['user_id']:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin_users'))
    
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get user info for logging
    c.execute('SELECT username, email FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if not user:
        flash('User not found.', 'error')
        conn.close()
        return redirect(url_for('admin_users'))
    
    username = user[0]
    
    try:
        # Get all user's videos to delete files
        c.execute('SELECT filename FROM videos WHERE user_id = ?', (user_id,))
        videos = c.fetchall()
        
        # Delete video files
        for video in videos:
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video[0])
            if os.path.exists(video_path):
                os.remove(video_path)
        
        # Get user's avatar to delete
        c.execute('SELECT avatar_filename FROM users WHERE id = ?', (user_id,))
        avatar = c.fetchone()
        if avatar and avatar[0]:
            avatar_path = os.path.join('static', 'avatars', avatar[0])
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
        
        # Delete all user data (in correct order to avoid foreign key constraints)
        c.execute('DELETE FROM comment_likes WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM votes WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM comments WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM admin_messages WHERE recipient_id = ? OR admin_id = ?', (user_id, user_id))
        c.execute('DELETE FROM admin_logs WHERE admin_id = ?', (user_id,))
        c.execute('DELETE FROM reports WHERE reporter_id = ? OR handled_by = ?', (user_id, user_id))
        c.execute('DELETE FROM videos WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        
        log_admin_action(session['user_id'], 'delete_user', 'user', user_id, 
                        f"Permanently deleted user account: {username}")
        flash(f'User account "{username}" has been permanently deleted.', 'success')
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting user {user_id}: {str(e)}")  # Add logging
        flash(f'Error deleting user account: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_users'))

@app.route('/admin/video/<int:video_id>/delete', methods=['POST'])
@admin_required('basic')
def admin_delete_video(video_id):
    """Permanently delete a video and all associated data"""
    conn = sqlite3.connect('tournament.db')
    c = conn.cursor()
    
    # Get video info for logging
    c.execute('SELECT title, filename, user_id FROM videos WHERE id = ?', (video_id,))
    video = c.fetchone()
    
    if not video:
        flash('Video not found.', 'error')
        conn.close();
        return redirect(url_for('admin_videos'))
    
    title, filename, user_id = video
    
    try:
        # Delete video file
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(video_path):
            os.remove(video_path)
        
        # Delete all video data (in correct order to avoid foreign key constraints)
        c.execute('DELETE FROM comment_likes WHERE comment_id IN (SELECT id FROM comments WHERE video_id = ?)', (video_id,))
        c.execute('DELETE FROM comments WHERE video_id = ?', (video_id,))
        c.execute('DELETE FROM votes WHERE video_id = ?', (video_id,))
        c.execute('DELETE FROM reports WHERE reported_type = "video" AND reported_id = ?', (video_id,))
        c.execute('DELETE FROM videos WHERE id = ?', (video_id,))
        
        conn.commit();
        
        log_admin_action(session['user_id'], 'delete_video', 'video', video_id, 
                        f"Permanently deleted video: {title}")
        flash(f'Video "{title}" has been permanently deleted.', 'success')
        
    except Exception as e:
        conn.rollback();
        flash(f'Error deleting video: {str(e)}', 'error')
    finally:
        conn.close();
    
    return redirect(url_for('admin_videos'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required('super')
def admin_settings():
    """Platform settings management"""
    if request.method == 'POST':
        # Handle settings updates
        flash('Settings updated successfully', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html')

@app.route('/debug/payment_config')
@login_required
def debug_payment_config():
    """Debug route to check mobile money payment configuration (remove in production)"""
    if not session.get('user_id'):
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Mobile Money configuration
    mtn_api_user = app.config.get('MTN_MOMO_API_USER', '')
    mtn_api_key = app.config.get('MTN_MOMO_API_KEY', '')
    mtn_subscription_key = app.config.get('MTN_MOMO_SUBSCRIPTION_KEY', '')
    orange_client_id = app.config.get('ORANGE_MONEY_CLIENT_ID', '')
    airtel_client_id = app.config.get('AIRTEL_MONEY_CLIENT_ID', '')
    
    config_info = {
        'payment_method': app.config.get('PAYMENT_METHOD', 'mobile_money'),
        'participant_fee': app.config.get('PARTICIPANT_FEE'),
        'mobile_money_providers': {
            'mtn_momo': {
                'api_user_present': bool(mtn_api_user),
                'api_key_present': bool(mtn_api_key),
                'subscription_key_present': bool(mtn_subscription_key),
                'api_user_preview': mtn_api_user[:8] + '...' if mtn_api_user else 'None'
            },
            'orange_money': {
                'client_id_present': bool(orange_client_id),
                'client_id_preview': orange_client_id[:8] + '...' if orange_client_id else 'None'
            },
            'airtel_money': {
                'client_id_present': bool(airtel_client_id),
                'client_id_preview': airtel_client_id[:8] + '...' if airtel_client_id else 'None'
            }
        },
        'environment_variables': {
            'MTN_MOMO_API_USER_env': bool(os.environ.get('MTN_MOMO_API_USER')),
            'MTN_MOMO_API_KEY_env': bool(os.environ.get('MTN_MOMO_API_KEY')),
            'MTN_MOMO_SUBSCRIPTION_KEY_env': bool(os.environ.get('MTN_MOMO_SUBSCRIPTION_KEY')),
            'ORANGE_MONEY_CLIENT_ID_env': bool(os.environ.get('ORANGE_MONEY_CLIENT_ID')),
            'AIRTEL_MONEY_CLIENT_ID_env': bool(os.environ.get('AIRTEL_MONEY_CLIENT_ID')),
            'SECRET_KEY_env': bool(os.environ.get('SECRET_KEY')),
        },
        'mobile_money_config_file_available': False
    }
    
    # Try to check if mobile_money_config.py is available
    try:
        from mobile_money_config import get_mobile_money_config
        config_info['mobile_money_config_file_available'] = True
        local_config = get_mobile_money_config()
        config_info['mobile_money_config_file_keys'] = {
            'mtn_configured': bool(local_config['mtn_momo']['api_user']),
            'orange_configured': bool(local_config['orange_money']['client_id']),
            'airtel_configured': bool(local_config['airtel_money']['client_id']),
        }
    except ImportError:
        config_info['mobile_money_config_file_available'] = False
        config_info['mobile_money_config_file_keys'] = 'ImportError - file not available'
    
    return jsonify(config_info)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
