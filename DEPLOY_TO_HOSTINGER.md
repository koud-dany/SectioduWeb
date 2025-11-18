# 🚀 Hostinger Deployment - Quick Start Guide

## Your SectionduWeb is Ready to Deploy!

All necessary files have been created and pushed to GitHub. Here's how to get your website live on Hostinger in **under 30 minutes**!

---

## 📋 **What You Need**

1. **Hostinger Account** with Python support
   - Business Plan ($3.99/month) or higher
   - Activate Python application in hPanel

2. **Domain Name** (or use Hostinger's free subdomain)

3. **Your Credentials**:
   - AWS S3 (for image storage) - Optional
   - Secret keys for Flask

---

## ⚡ **Quick Deployment (5 Steps)**

### **Step 1: Connect to Hostinger**
```bash
# Via SSH (get credentials from hPanel → Advanced → SSH Access)
ssh your_username@your_domain.com
```

### **Step 2: Clone Your Repository**
```bash
cd ~/public_html
git clone https://github.com/koud-dany/SectioduWeb.git videovote
cd videovote
```

### **Step 3: Run Deployment Script**
```bash
chmod +x deploy_hostinger.sh
./deploy_hostinger.sh
```

### **Step 4: Configure Environment**
```bash
nano .env
```
Add your credentials (see template in `.env`):
- SECRET_KEY (generate a random string)
- AWS credentials (if using S3)
- Mobile money credentials (if using payments)

Save: `Ctrl+X`, then `Y`, then `Enter`

### **Step 5: Set Up in hPanel**
1. Go to hPanel → **Advanced** → **Python**
2. Click **"Create Application"**
3. Fill in:
   - Python Version: **3.8+**
   - App Root: `/home/username/public_html/videovote`
   - App URL: **your domain**
   - Startup File: **passenger_wsgi.py**
4. Click **Create**

**🎉 Done! Your site is now live!**

Visit: `https://yourdomain.com`

---

## 🔧 **Configuration Files Created**

| File | Purpose |
|------|---------|
| `passenger_wsgi.py` | Hostinger Python application entry point |
| `.htaccess` | Apache configuration (security, HTTPS, caching) |
| `deploy_hostinger.sh` | Automated deployment script |
| `HOSTINGER_DEPLOYMENT_GUIDE.md` | Detailed step-by-step instructions |
| `HOSTINGER_CHECKLIST.md` | Complete deployment checklist |

---

## 🛠️ **Common Tasks**

### Restart Application
```bash
touch ~/public_html/videovote/tmp/restart.txt
```

### Update Application
```bash
cd ~/public_html/videovote
git pull origin main
pip3 install --user -r requirements.txt
touch tmp/restart.txt
```

### View Logs
```bash
tail -f ~/logs/error.log
```

### Backup Database
```bash
cp ~/public_html/videovote/tournament.db ~/backups/tournament_backup.db
```

---

## 🔐 **Important Security Steps**

1. **Enable HTTPS**: hPanel → Security → SSL → Install Free Certificate
2. **Force HTTPS**: Already configured in `.htaccess`
3. **Protect .env**: `chmod 600 .env` (done by script)
4. **Strong SECRET_KEY**: Generate random 50+ character string

---

## 📊 **Expected Costs**

- **Hostinger Business**: $3.99/month
- **AWS S3 Storage**: ~$0.30/month (10GB)
- **Domain**: $9.99/year (if not included)
- **Total**: ~$5-6/month

---

## ✅ **Pre-Flight Checklist**

Before going live, ensure:
- [ ] `.env` file configured with production values
- [ ] `DEMO_MODE=false` in .env
- [ ] `SECRET_KEY` is unique and secure
- [ ] AWS S3 bucket created and configured (if using)
- [ ] SSL certificate installed
- [ ] Database initialized
- [ ] All features tested

---

## 📚 **Documentation Files**

### For Detailed Instructions:
- **`HOSTINGER_DEPLOYMENT_GUIDE.md`** - Complete guide with troubleshooting
- **`HOSTINGER_CHECKLIST.md`** - Step-by-step deployment checklist

### For S3 Setup:
- **`S3_SETUP_GUIDE.md`** - Complete S3 configuration guide
- **`S3_QUICK_SETUP.md`** - Quick S3 setup reference
- **`S3_VISUAL_GUIDE.md`** - Visual diagrams and flow charts

---

## 🆘 **Getting Help**

### Hostinger Support:
- **24/7 Live Chat**: Available in hPanel
- **Email**: support@hostinger.com
- **Knowledge Base**: https://support.hostinger.com

### Application Issues:
1. Check logs: `tail -f ~/logs/error.log`
2. Restart app: `touch ~/public_html/videovote/tmp/restart.txt`
3. Verify .env: `cat .env` (careful - contains secrets!)
4. Test imports: `python3 -c "import flask; print('OK')"`

---

## 🎯 **Deployment Flow Diagram**

```
GitHub Repository
       ↓
  SSH to Hostinger
       ↓
  Git Clone Project
       ↓
Run Deployment Script
       ↓
Configure .env File
       ↓
Set Up Python in hPanel
       ↓
  Enable SSL/HTTPS
       ↓
   Test Website
       ↓
  🎉 LIVE!
```

---

## 📱 **Testing Your Deployment**

Once deployed, test these features:

1. **Homepage**: Loads without errors
2. **Registration**: Can create new account
3. **Login**: Can authenticate
4. **Upload**: Can upload video (requires payment)
5. **Profile**: Can edit profile and upload avatar
6. **Voting**: Can vote on videos
7. **Leaderboard**: Displays correctly
8. **Mobile**: Responsive design works
9. **HTTPS**: All pages load over HTTPS
10. **Performance**: Pages load in < 3 seconds

---

## 🔄 **Update Workflow**

When you make changes:

1. **Local Development**:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```

2. **Deploy to Hostinger**:
   ```bash
   ssh username@domain.com
   cd ~/public_html/videovote
   git pull origin main
   touch tmp/restart.txt
   ```

---

## 💡 **Pro Tips**

1. **Always backup before updates**: `cp tournament.db tournament.db.backup`
2. **Test in local first**: Run `python app.py` locally before deploying
3. **Monitor logs regularly**: Check for errors and unusual activity
4. **Keep dependencies updated**: But test updates locally first
5. **Use environment variables**: Never hardcode secrets in code
6. **Set up automated backups**: Use cron for daily database backups

---

## 🚨 **If Something Goes Wrong**

### App won't start:
```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip3 install --user -r requirements.txt --force-reinstall

# Restart
touch tmp/restart.txt
```

### Database errors:
```bash
# Check permissions
ls -la tournament.db
chmod 644 tournament.db
```

### Can't access site:
1. Check DNS settings in hPanel
2. Verify Python app is running
3. Check error logs
4. Ensure .htaccess is correct

---

## 🎊 **Success!**

Your SectionduWeb video voting platform is now:
- ✅ Live on the internet
- ✅ Secure with HTTPS
- ✅ Scalable with S3 storage
- ✅ Professional and fast
- ✅ Ready for users!

### Next Steps:
1. Share your website URL
2. Invite users to register
3. Monitor performance
4. Collect feedback
5. Iterate and improve

---

## 📞 **Need Help?**

Check the detailed guides:
- `HOSTINGER_DEPLOYMENT_GUIDE.md` - Full deployment instructions
- `HOSTINGER_CHECKLIST.md` - Step-by-step checklist
- `S3_SETUP_GUIDE.md` - Cloud storage setup

**Happy Deploying! 🚀**

---

*Last Updated: 2025*
*SectionduWeb - Video Voting Platform*
