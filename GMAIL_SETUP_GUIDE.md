# 📧 GMAIL SETUP FOR HOSTINGER DEPLOYMENT
## Configure Email Services for lasectionduweb.org

Your email credentials have been configured, but Gmail requires special setup for external applications.

---

## 🔐 GMAIL APP PASSWORD SETUP (RECOMMENDED)

For better security, use Gmail App Passwords instead of your main password:

### **Step 1: Enable 2-Factor Authentication**
1. Go to **Google Account Settings**: https://myaccount.google.com
2. **Security** → **2-Step Verification**
3. **Turn on 2-Step Verification**

### **Step 2: Generate App Password**
1. **Google Account** → **Security** → **App passwords**
2. **Select app**: Mail
3. **Select device**: Other (custom name)
4. **Enter name**: "SectionduWeb Hostinger"
5. **Generate** and **copy the 16-character password**

### **Step 3: Update .env File**
Replace in your `.env` file on Hostinger:
```bash
MAIL_PASSWORD=your_16_character_app_password_here
```

---

## 📧 EMAIL FEATURES CONFIGURED

Your site will now support:
- ✅ **Password Reset Emails**
- ✅ **Welcome Email Notifications** 
- ✅ **Tournament Notifications**
- ✅ **Admin Alerts**
- ✅ **Contact Form Messages**

---

## 🧪 TESTING EMAIL

After deployment, test email functionality:

### **Test Password Reset:**
1. Go to login page
2. Click "Forgot Password"
3. Enter: `barbeblanche89@gmail.com`
4. Check email for reset link

### **Test Admin Notifications:**
1. Have users register accounts
2. Check admin email for notifications
3. Create test tournaments
4. Verify email alerts

---

## 🛠️ TROUBLESHOOTING

### **Common Email Issues:**

**🔸 "Authentication failed"**
- Use App Password instead of main password
- Verify 2FA is enabled
- Check email/password spelling

**🔸 "Connection refused"**
- Verify SMTP settings:
  - Server: `smtp.gmail.com`
  - Port: `587`
  - TLS: `True`

**🔸 "Emails not sending"**
- Check Hostinger firewall settings
- Verify Gmail account not locked
- Test with different email provider

---

## 🔧 CURRENT EMAIL CONFIGURATION

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=barbeblanche89@gmail.com
MAIL_PASSWORD=Trafalgar$89  # Consider replacing with App Password
```

---

## 🚨 SECURITY RECOMMENDATIONS

1. **Use App Password**: More secure than main password
2. **Monitor Login Activity**: Check Google Account activity regularly
3. **Rotate Passwords**: Change passwords periodically
4. **Backup Access**: Set up recovery options

---

## 📞 SUPPORT

If email issues persist:
- **Gmail Help**: https://support.google.com/mail
- **Hostinger Support**: Contact for SMTP troubleshooting
- **App Documentation**: Check Flask-Mail docs

**Your email system is ready for https://lasectionduweb.org** ✉️
