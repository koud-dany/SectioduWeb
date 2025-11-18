# Hostinger Deployment Guide for SectionduWeb

## Prerequisites

- Hostinger account with Python support (Business or Cloud hosting)
- Domain name (optional, Hostinger provides a subdomain)
- SSH access enabled
- Python 3.8+ support

## Deployment Steps

### 1. Prepare Your Application

#### A. Update Requirements for Hostinger
Your `requirements.txt` is already ready. Ensure it includes:
```
Flask==2.3.3
Werkzeug==2.3.7
gunicorn==21.2.0
python-dotenv==1.0.0
requests==2.31.0
cloudinary==1.36.0
boto3==1.34.14
pillow==10.2.0
```

#### B. Create a `.htaccess` file (if using shared hosting)
Create this file in your project root:

```apache
# .htaccess for Hostinger
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ /passenger_wsgi.py/$1 [QSA,L]
```

#### C. Create `passenger_wsgi.py` (for Hostinger's Python support)
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/your_username/public_html/videovote'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment to production
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from app import app as application
```

### 2. Connect to Hostinger via SSH

#### Using Hostinger File Manager:
1. Log in to hPanel
2. Go to **Files** → **File Manager**
3. Navigate to `public_html`

#### Using SSH (Recommended):
```bash
ssh your_username@your_domain.com
# Enter your password when prompted
```

### 3. Upload Your Files

#### Option A: Using Git (Recommended)
```bash
# Connect via SSH
cd ~/public_html

# Clone your repository
git clone https://github.com/koud-dany/SectioduWeb.git videovote
cd videovote

# Install Python packages
python3 -m pip install --user -r requirements.txt
```

#### Option B: Using File Manager
1. Compress your project: `zip -r videovote.zip .`
2. Upload via Hostinger File Manager
3. Extract in `public_html/videovote`

#### Option C: Using FTP
1. Get FTP credentials from hPanel
2. Use FileZilla or similar
3. Upload to `public_html/videovote`

### 4. Set Up Environment Variables

Create `.env` file in your project directory:

```bash
# Navigate to your project
cd ~/public_html/videovote

# Create .env file
nano .env
```

Add your environment variables:
```env
# Flask Configuration
SECRET_KEY=your_super_secret_key_here_change_this
FLASK_ENV=production

# Database
DATABASE_URL=sqlite:///tournament.db

# Cloud Storage
USE_CLOUD_STORAGE=true

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_BUCKET_NAME=videovote-uploads
AWS_REGION=us-east-1

# Cloudinary (Alternative)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Mobile Money (if using)
MTN_MOMO_API_USER=your_mtn_api_user
MTN_MOMO_API_KEY=your_mtn_api_key
MTN_MOMO_SUBSCRIPTION_KEY=your_mtn_subscription_key

# Demo Mode
DEMO_MODE=false
```

Save and exit: `Ctrl+X`, then `Y`, then `Enter`

### 5. Configure Database

```bash
# Create database
python3 app.py

# Or initialize manually
python3 -c "from app import init_db; init_db()"
```

### 6. Set Up Python Application in hPanel

1. Log in to **hPanel**
2. Go to **Advanced** → **Python**
3. Click **Create Application**
4. Configure:
   - **Python Version**: 3.8 or higher
   - **Application Root**: `/home/username/public_html/videovote`
   - **Application URL**: Your domain or subdomain
   - **Application Startup File**: `passenger_wsgi.py`
   - **Application Entry Point**: `application`

5. Click **Create**

### 7. Configure Directory Permissions

```bash
# Set correct permissions
cd ~/public_html/videovote
chmod 755 .
chmod 644 app.py
chmod 644 config.py
chmod 600 .env
chmod 755 static
chmod 755 templates
chmod 755 static/uploads
chmod 755 static/avatars
chmod 755 static/thumbnails
```

### 8. Test Your Application

Visit your domain:
- `https://yourdomain.com`
- Or subdomain: `https://videovote.yourdomain.com`

Check for errors:
```bash
# View error logs
tail -f ~/public_html/videovote/logs/error.log
```

### 9. Set Up Domain (if needed)

#### A. Main Domain
1. Go to hPanel → **Domains**
2. Point domain to your application

#### B. Subdomain
1. Go to hPanel → **Domains** → **Subdomains**
2. Create subdomain (e.g., `videovote.yourdomain.com`)
3. Point to `/public_html/videovote`

### 10. Enable SSL Certificate

1. Go to hPanel → **Security** → **SSL**
2. Install free Let's Encrypt SSL certificate
3. Enable **Force HTTPS**

## Hostinger-Specific Configuration Files

### passenger_wsgi.py
```python
import sys
import os

# Adjust paths for Hostinger
INTERP = os.path.join(os.environ['HOME'], 'virtualenv', 'public_html', 'videovote', '3.8', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add project to path
sys.path.insert(0, os.path.join(os.environ['HOME'], 'public_html', 'videovote'))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.environ['HOME'], 'public_html', 'videovote', '.env'))

# Import Flask application
from app import app as application
```

### .htaccess
```apache
PassengerEnabled On
PassengerAppRoot /home/username/public_html/videovote

# Python version
PassengerPython /home/username/virtualenv/public_html/videovote/3.8/bin/python3

# Error handling
ErrorDocument 404 /404.html
ErrorDocument 500 /500.html

# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

## Troubleshooting

### Issue: Application not starting
**Solution:**
```bash
# Check Python version
python3 --version

# Check if all dependencies installed
pip3 list

# Restart application
touch ~/public_html/videovote/tmp/restart.txt
```

### Issue: Database errors
**Solution:**
```bash
# Check database file exists
ls -la ~/public_html/videovote/tournament.db

# Ensure write permissions
chmod 644 ~/public_html/videovote/tournament.db
chmod 755 ~/public_html/videovote
```

### Issue: Static files not loading
**Solution:**
```bash
# Check permissions
chmod -R 755 ~/public_html/videovote/static

# Clear cache
rm -rf ~/public_html/videovote/__pycache__
```

### Issue: Environment variables not loading
**Solution:**
```bash
# Verify .env file
cat ~/public_html/videovote/.env

# Ensure python-dotenv is installed
pip3 install --user python-dotenv
```

### Issue: Import errors
**Solution:**
```bash
# Reinstall all dependencies
cd ~/public_html/videovote
pip3 install --user -r requirements.txt --force-reinstall
```

## Performance Optimization

### 1. Enable Caching
Add to your Flask app:
```python
# In app.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})
```

### 2. Use CDN for Static Files
Update base.html to use CDN:
```html
<!-- Already using CDN for Bootstrap and Font Awesome -->
```

### 3. Enable Gzip Compression
Add to `.htaccess`:
```apache
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>
```

## Updating Your Application

### Using Git:
```bash
cd ~/public_html/videovote
git pull origin main
pip3 install --user -r requirements.txt
touch tmp/restart.txt
```

### Manual Update:
1. Upload changed files via File Manager or FTP
2. Restart application:
```bash
touch ~/public_html/videovote/tmp/restart.txt
```

## Backup Strategy

### Database Backup:
```bash
# Create backup
cp ~/public_html/videovote/tournament.db ~/backups/tournament_$(date +%Y%m%d).db

# Automated daily backup (add to cron)
0 2 * * * cp ~/public_html/videovote/tournament.db ~/backups/tournament_$(date +\%Y\%m\%d).db
```

### Full Application Backup:
```bash
# Backup entire application
cd ~/public_html
tar -czf ~/backups/videovote_$(date +%Y%m%d).tar.gz videovote/
```

## Monitoring

### Check Application Status:
```bash
# View access logs
tail -f ~/logs/access.log

# View error logs
tail -f ~/logs/error.log

# Monitor resource usage
top
```

## Support Resources

- **Hostinger Knowledge Base**: https://support.hostinger.com
- **Python on Hostinger**: https://support.hostinger.com/en/articles/1583245-how-to-install-python-on-hostinger
- **Flask Documentation**: https://flask.palletsprojects.com/

## Cost Estimation (Hostinger)

- **Business Hosting**: ~$3.99/month (supports Python)
- **Cloud Hosting**: ~$9.99/month (better performance)
- **VPS Hosting**: ~$3.95/month (full control)

## Security Checklist

- ✅ Enable HTTPS/SSL
- ✅ Set strong SECRET_KEY
- ✅ Disable DEBUG mode in production
- ✅ Secure .env file (chmod 600)
- ✅ Regular backups
- ✅ Keep dependencies updated
- ✅ Monitor logs regularly
- ✅ Use strong database passwords
- ✅ Enable firewall rules
- ✅ Regular security updates

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Monitor error logs for issues
3. ✅ Set up regular backups
4. ✅ Configure AWS S3 for production
5. ✅ Set up monitoring/analytics
6. ✅ Configure email notifications
7. ✅ Test payment integration
8. ✅ Optimize performance
9. ✅ Set up CDN (if needed)
10. ✅ Document your deployment

Your SectionduWeb application is now ready for Hostinger deployment! 🚀
