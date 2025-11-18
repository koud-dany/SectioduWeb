# Hostinger Deployment Checklist

## Pre-Deployment
- [ ] Hostinger account with Python support activated
- [ ] Domain name configured (or using Hostinger subdomain)
- [ ] SSH access enabled in hPanel
- [ ] Git repository up to date on GitHub
- [ ] All sensitive data in .env file (not in code)

## File Preparation
- [ ] `passenger_wsgi.py` created
- [ ] `.htaccess` created
- [ ] `deploy_hostinger.sh` created
- [ ] `.env.example` updated with all variables
- [ ] All changes committed to Git

## Hostinger Setup
- [ ] Logged into hPanel
- [ ] Python application feature enabled
- [ ] SSH access tested
- [ ] File Manager accessible

## Deployment Steps

### 1. Upload Files
Choose ONE method:

#### Method A: Git (Recommended)
```bash
ssh username@yourdomain.com
cd ~/public_html
git clone https://github.com/koud-dany/SectioduWeb.git videovote
cd videovote
chmod +x deploy_hostinger.sh
```

#### Method B: File Manager
- [ ] Zip project locally
- [ ] Upload via hPanel File Manager
- [ ] Extract to `public_html/videovote`

#### Method C: FTP
- [ ] Connect via FTP client
- [ ] Upload all files to `public_html/videovote`

### 2. Configure Environment
```bash
cd ~/public_html/videovote
nano .env
```
- [ ] Set SECRET_KEY (generate a random one)
- [ ] Set AWS credentials (if using S3)
- [ ] Set Cloudinary credentials (if using)
- [ ] Set FLASK_ENV=production
- [ ] Set DEMO_MODE=false
- [ ] Save and exit (Ctrl+X, Y, Enter)

### 3. Run Deployment Script
```bash
chmod +x deploy_hostinger.sh
./deploy_hostinger.sh
```
- [ ] Script completed successfully
- [ ] No critical errors reported

### 4. Configure Python in hPanel
- [ ] Open hPanel → Advanced → Python
- [ ] Click "Create Application"
- [ ] Settings:
  - [ ] Python Version: 3.8+
  - [ ] Application Root: `/home/username/public_html/videovote`
  - [ ] Application URL: your domain
  - [ ] Startup File: `passenger_wsgi.py`
  - [ ] Entry Point: `application`
- [ ] Click Create

### 5. Update .htaccess Paths
```bash
nano .htaccess
```
- [ ] Replace `username` with your actual Hostinger username
- [ ] Replace paths with correct values
- [ ] Save changes

### 6. Update passenger_wsgi.py
```bash
nano passenger_wsgi.py
```
- [ ] Update HOME path if needed
- [ ] Update Python version if different
- [ ] Save changes

### 7. Set Up Domain/Subdomain
#### Main Domain:
- [ ] hPanel → Domains → Point to videovote directory

#### Subdomain:
- [ ] hPanel → Domains → Subdomains
- [ ] Create subdomain (e.g., `app.yourdomain.com`)
- [ ] Point to `/public_html/videovote`

### 8. Enable SSL
- [ ] hPanel → Security → SSL
- [ ] Install Let's Encrypt certificate
- [ ] Enable "Force HTTPS"
- [ ] Test HTTPS access

### 9. Initialize Database
```bash
cd ~/public_html/videovote
python3 app.py
# Or
python3 -c "from app import init_db; init_db()"
```
- [ ] Database created successfully
- [ ] No errors reported

### 10. Test Application
Visit your domain:
- [ ] Homepage loads correctly
- [ ] No 500 errors
- [ ] Static files loading
- [ ] Can register new user
- [ ] Can login
- [ ] Can upload video (if paid)
- [ ] Images display correctly

## Post-Deployment

### Security
- [ ] .env file protected (chmod 600)
- [ ] Database file protected
- [ ] HTTPS working
- [ ] Security headers enabled
- [ ] Directory browsing disabled

### Performance
- [ ] Gzip compression enabled
- [ ] Static file caching working
- [ ] CDN configured (if needed)
- [ ] Images optimized

### Monitoring
- [ ] Check error logs: `tail -f ~/logs/error.log`
- [ ] Check access logs: `tail -f ~/logs/access.log`
- [ ] Test all features thoroughly
- [ ] Monitor resource usage

### Backups
```bash
# Set up automated backup (cron job)
crontab -e
```
Add this line:
```
0 2 * * * cp ~/public_html/videovote/tournament.db ~/backups/tournament_$(date +\%Y\%m\%d).db
```
- [ ] Backup script added to cron
- [ ] Test backup manually
- [ ] Verify backup location

### Documentation
- [ ] Document your deployment
- [ ] Save credentials securely
- [ ] Note any custom configurations
- [ ] Update team about deployment

## Troubleshooting

### Application won't start
```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip3 install --user -r requirements.txt --force-reinstall

# Restart application
touch ~/public_html/videovote/tmp/restart.txt
```

### Database errors
```bash
# Check database exists
ls -la ~/public_html/videovote/tournament.db

# Fix permissions
chmod 644 ~/public_html/videovote/tournament.db
chmod 755 ~/public_html/videovote
```

### Static files not loading
```bash
# Fix permissions
chmod -R 755 ~/public_html/videovote/static

# Clear cache
rm -rf ~/public_html/videovote/__pycache__
```

### Import errors
```bash
# Check installed packages
pip3 list

# Reinstall specific package
pip3 install --user package_name --force-reinstall
```

## Quick Commands Reference

### Restart Application
```bash
touch ~/public_html/videovote/tmp/restart.txt
```

### View Logs
```bash
# Error log
tail -f ~/logs/error.log

# Access log
tail -f ~/logs/access.log

# Application log (if configured)
tail -f ~/public_html/videovote/logs/app.log
```

### Update Application
```bash
cd ~/public_html/videovote
git pull origin main
pip3 install --user -r requirements.txt
touch tmp/restart.txt
```

### Backup Database
```bash
cp ~/public_html/videovote/tournament.db ~/backups/tournament_$(date +%Y%m%d).db
```

### Check Disk Space
```bash
df -h
du -sh ~/public_html/videovote
```

## Support Contacts

- **Hostinger Support**: https://support.hostinger.com
- **Live Chat**: Available 24/7 in hPanel
- **Email**: support@hostinger.com
- **Knowledge Base**: https://support.hostinger.com/en/collections/1588829-python

## Success Criteria

Your deployment is successful when:
- ✅ Website loads at your domain
- ✅ All pages render correctly
- ✅ User registration works
- ✅ Login/logout functional
- ✅ Video uploads working
- ✅ Database operations successful
- ✅ Images displaying properly
- ✅ HTTPS enabled
- ✅ No errors in logs
- ✅ Performance acceptable

## Congratulations! 🎉

Your SectionduWeb application is now live on Hostinger!

**Live URL**: https://yourdomain.com

Remember to:
- Monitor logs regularly
- Keep dependencies updated
- Backup database frequently
- Test all features periodically
- Keep your credentials secure
