# Pre-Deployment Information Required

## Before deploying to Hostinger, please provide the following information:

---

## 1. 🏢 **Hostinger Account Information**

### Account Details:
- [ ] **Hostinger Username**: ___________________
- [ ] **Hosting Plan**: (Business/Cloud/VPS) ___________________
- [ ] **Python Version Available**: (Check hPanel → Advanced → Python) ___________________

### Access Information:
- [ ] **hPanel URL**: (Usually https://hpanel.hostinger.com)
- [ ] **SSH Access Enabled?**: Yes / No
- [ ] **FTP Access Enabled?**: Yes / No

---

## 2. 🌐 **Domain Information**

### Option A: Using Your Own Domain
- [ ] **Domain Name**: ___________________
- [ ] **Domain Registrar**: ___________________
- [ ] **DNS Management**: (Hostinger / External) ___________________

### Option B: Using Hostinger Subdomain
- [ ] **Preferred Subdomain**: ___________________.hostinger-site.com
  - Example: `videovote.hostinger-site.com`

### Option C: Creating New Subdomain
- [ ] **Main Domain**: ___________________
- [ ] **Subdomain Prefix**: ___________________
  - Example: `app.yourdomain.com` or `vote.yourdomain.com`

---

## 3. 🔐 **SSH Access Credentials**

To deploy via SSH, you need:
- [ ] **SSH Hostname**: ___________________
  - Usually: `your_domain.com` or provided by Hostinger
- [ ] **SSH Port**: (Usually 22 or 65002) ___________________
- [ ] **SSH Username**: ___________________
- [ ] **SSH Password**: (Keep this secure!) ___________________

**How to Get SSH Credentials:**
1. Log in to hPanel
2. Go to **Advanced** → **SSH Access**
3. Enable SSH if not already enabled
4. Copy your credentials

---

## 4. 📁 **File Access Preferences**

Which method do you prefer to upload files?

- [ ] **Git (Recommended)** - Clone from GitHub
- [ ] **File Manager** - Upload via hPanel
- [ ] **FTP** - Use FTP client like FileZilla
- [ ] **SSH** - Direct command-line access

---

## 5. 🔑 **Environment Variables & Secrets**

### Flask Secret Key:
- [ ] Generate a new secret key? (Recommended)
  - We'll generate one for you: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Or provide your own: ___________________

### AWS S3 Credentials (for image storage):
Do you have an AWS account with S3 bucket set up?
- [ ] **Yes** - I have AWS credentials
  - AWS Access Key ID: ___________________
  - AWS Secret Access Key: ___________________
  - S3 Bucket Name: ___________________
  - AWS Region: ___________________

- [ ] **No** - I'll set up later or use local storage
- [ ] **No** - Please help me set up AWS S3

### Cloudinary (Alternative to S3):
Do you have a Cloudinary account?
- [ ] **Yes** - I have Cloudinary credentials
  - Cloud Name: ___________________
  - API Key: ___________________
  - API Secret: ___________________

- [ ] **No** - I'll use S3 or local storage

### Mobile Money (Payment Integration):
Do you have mobile money provider credentials?
- [ ] **MTN Mobile Money**
  - API User: ___________________
  - API Key: ___________________
  - Subscription Key: ___________________

- [ ] **Orange Money**
  - Client ID: ___________________
  - Client Secret: ___________________

- [ ] **Airtel Money**
  - Client ID: ___________________
  - Client Secret: ___________________

- [ ] **Not using payments yet** - Will configure later

---

## 6. 🎯 **Deployment Preferences**

### Deployment Mode:
- [ ] **Production** - Full deployment with real credentials
- [ ] **Demo Mode** - Test deployment with demo data
- [ ] **Staging** - Test environment before production

### SSL Certificate:
- [ ] **Install free Let's Encrypt SSL** (Recommended)
- [ ] **I have my own SSL certificate**
- [ ] **Skip SSL for now** (Not recommended)

### Database:
- [ ] **Start fresh** - New empty database
- [ ] **Import existing data** - I have a database backup
- [ ] **Keep development data** - Use current database

---

## 7. 📧 **Admin Account**

Create initial admin account:
- [ ] **Admin Username**: ___________________
- [ ] **Admin Email**: ___________________
- [ ] **Admin Password**: ___________________ (Keep secure!)

---

## 8. 🌍 **Language & Localization**

- [ ] **Default Language**: English / Français
- [ ] **Enable Both Languages**: Yes / No
- [ ] **Timezone**: ___________________

---

## 9. 💰 **Payment Settings**

- [ ] **Participant Fee**: $_____ (Currently set to $35)
- [ ] **Currency**: USD / XAF / Other: _____
- [ ] **Payment Method**: Mobile Money / Card / Both

---

## 10. 📊 **Performance & Storage**

### Expected Usage:
- [ ] **Expected Users**: ___________________
- [ ] **Expected Videos per Month**: ___________________
- [ ] **Expected Storage Needs**: _____ GB

### Optimization Preferences:
- [ ] **Enable CDN**: Yes / No
- [ ] **Use Cloud Storage (S3)**: Yes / No
- [ ] **Compress Images**: Yes / No

---

## 🚀 **Next Steps After Providing Information**

Once you provide the above information, I will:

1. ✅ Update configuration files with your specific details
2. ✅ Generate secure credentials where needed
3. ✅ Create a personalized deployment script
4. ✅ Provide step-by-step instructions for YOUR specific setup
5. ✅ Help you test the deployment
6. ✅ Ensure everything is secure and optimized

---

## 📝 **How to Provide This Information**

You can provide this information in any of these ways:

### Option 1: Fill out this form
Copy this document and fill in your details, then share back.

### Option 2: Provide step-by-step
Just answer each question one at a time in the chat.

### Option 3: Minimal Quick Start
Just provide:
1. Domain name
2. SSH username
3. SSH password
4. Whether you want S3 or local storage

We can configure the rest later!

---

## ⚠️ **Security Note**

**IMPORTANT:** 
- Never share passwords in plain text publicly
- Use secure methods to share credentials
- We'll generate secure keys for production
- Change all default passwords before going live

---

## 🆘 **Don't Have This Information?**

### Don't worry! Here's what to do:

#### For Hostinger Account:
1. Go to https://hpanel.hostinger.com
2. Log in with your Hostinger credentials
3. Check **Advanced** → **Python** for Python support
4. Check **Advanced** → **SSH Access** for SSH details

#### For Domain:
1. If you don't have a domain, Hostinger provides a free subdomain
2. Or you can purchase a domain from Hostinger or other registrars

#### For AWS S3:
1. You can skip this initially and use local storage
2. We can add S3 later when needed
3. Or I can help you set up a free AWS account

#### For Mobile Money:
1. You can enable demo mode initially
2. Configure payment providers when ready
3. Or operate without payments initially

---

## 📞 **Ready to Deploy?**

Once you have this information ready:
1. Share the details with me
2. I'll create personalized deployment files
3. We'll deploy together step-by-step
4. Your site will be live!

---

## ✨ **Minimum Required to Start**

If you want to start with the bare minimum:

**Just provide these 3 things:**
1. **SSH Username**: ___________________
2. **Domain/Subdomain**: ___________________
3. **Python Version** (from hPanel): ___________________

We can configure everything else with defaults and update later!

---

**Ready when you are! What information can you provide?** 🚀
