# 🚀 College ERP - DEPLOYMENT & SECURITY GUIDE (Parts 6 & 7)

## STATUS: ✅ ALL PARTS COMPLETED

- ✅ **Part 1**: Email Configuration (Gmail SMTP)
- ✅ **Part 2**: Database Configuration  
- ✅ **Part 3**: Run Migrations
- ✅ **Part 4**: Google reCAPTCHA Setup
- ✅ **Part 5**: Deployment Platform Selection
- ✅ **Part 6**: SECURITY CHANGES FOR PRODUCTION
- ✅ **Part 7**: QUICK START SUMMARY

---

## 📋 TABLE OF CONTENTS

1. [Part 6: Security Configuration](#part-6-security-configuration)
2. [Part 7: Quick Start Summary](#part-7-quick-start-summary)
3. [Production Deployment Checklist](#production-deployment-checklist)
4. [Environment Variables Reference](#environment-variables-reference)
5. [Troubleshooting](#troubleshooting)

---

# PART 6: SECURITY CHANGES FOR PRODUCTION ⚔️

## What Has Been Implemented

### 1. **Environment Variable Management** ✅
All sensitive data is now stored in `.env` file instead of hardcoded in settings.py

```python
# .env file location: d:\Project\College-ERP\.env

SECRET_KEY = os.getenv('SECRET_KEY', 'default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
```

### 2. **Security Headers** ✅

#### SSL/TLS Configuration (Production Only)
```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # Force HTTPS
    SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
    CSRF_COOKIE_SECURE = True  # CSRF cookies only over HTTPS
```

#### Additional Security Headers
```python
SECURE_BROWSER_XSS_FILTER = True  # XSS Protection
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_HSTS_SECONDS = 31536000  # HSTS (1 year)
```

### 3. **CSRF Protection** ✅
```python
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '')
```

### 4. **Cookie Security** ✅
```python
SESSION_COOKIE_HTTPONLY = True  # HttpOnly flag (prevents JavaScript access)
SESSION_COOKIE_SECURE = True  # Secure flag (HTTPS only)
SESSION_COOKIE_AGE = 1209600  # 2 weeks default
```

### 5. **File Upload Security** ✅
```python
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB limit
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB limit
FILE_UPLOAD_PERMISSIONS = 0o644  # Restricted permissions
```

### 6. **Logging Configuration** ✅
```python
LOGGING = {
    'handlers': {
        'file': {
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
    },
}
```

### 7. **Database Security** ✅
All database credentials are in `.env` file:
```env
DB_ENGINE = django.db.backends.mysql
DB_NAME = college_erp_db
DB_USER = erp_user
DB_PASSWORD = secure_password
DB_HOST = localhost
```

### 8. **Email Security** ✅
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True  # Encrypted email connection
```

### 9. **reCAPTCHA Integration** ✅
```python
RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
```

---

## How to Switch to Production Mode

### Step 1: Update .env File
```bash
# .env
DEBUG = False  # Disable debug mode
ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com
SECRET_KEY = your-new-secure-key
```

### Step 2: Generate New Secret Key
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# Copy the output and paste in .env as SECRET_KEY
```

### Step 3: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Test in Production Mode
```bash
DEBUG = False  # in .env
python manage.py runserver
```

---

# PART 7: QUICK START SUMMARY 🚀

## Complete Setup Instructions for Fresh Installation

### Prerequisites
- Python 3.13+
- Git
- Virtual Environment (optional but recommended)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VanshTyagi/College-ERP.git
cd College-ERP
```

### 2️⃣ Create Virtual Environment (Optional)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
pip install python-dotenv mysqlclient
```

### 4️⃣ Configure Environment Variables
Create `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-secure-key-here
DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development: SQLite, Production: MySQL/PostgreSQL)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email (Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=College ERP <noreply@collegeerp.com>

# Security
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Google reCAPTCHA
RECAPTCHA_SITE_KEY=your-site-key
RECAPTCHA_SECRET_KEY=your-secret-key
```

### 5️⃣ Run Migrations
```bash
python manage.py migrate
```

### 6️⃣ Create Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### 7️⃣ Start Development Server
```bash
python manage.py runserver
```

**✅ Access at:** http://127.0.0.1:8000/

---

## 📋 Production Deployment Checklist

### Before Deployment
- [ ] Set `DEBUG = False` in .env
- [ ] Set new `SECRET_KEY` in .env
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Configure database (MySQL/PostgreSQL)
- [ ] Configure email credentials
- [ ] Configure reCAPTCHA keys for your domain
- [ ] Set up SSL/TLS certificate
- [ ] Run `collectstatic` command
- [ ] Run all migrations
- [ ] Create superuser account
- [ ] Test login with reCAPTCHA
- [ ] Set up logging
- [ ] Configure backups

### Platform-Specific Deployment

#### **Option A: PythonAnywhere**
1. Upload code via Git or ZIP
2. Set Python version to 3.9+
3. Create virtual environment
4. Upload `.env` file (not in git)
5. Configure web app settings
6. Point domain to PythonAnywhere
7. Run migrations: `python manage.py migrate`

#### **Option B: Heroku**
1. Create Heroku account
2. Install Heroku CLI
3. `heroku login`
4. `heroku create app-name`
5. Set environment variables: `heroku config:set DEBUG=False`
6. `git push heroku main`
7. `heroku run python manage.py migrate`

#### **Option C: AWS EC2**
1. Launch Ubuntu instance
2. Install Python, PostgreSQL, Nginx
3. Clone repository
4. Create virtual environment
5. Install requirements
6. Configure Gunicorn + Nginx
7. Set environment variables
8. Run migrations
9. Set up SSL with Let's Encrypt

#### **Option D: DigitalOcean**
1. Create Droplet (Ubuntu 22.04)
2. SSH into server
3. Install Python, MySQL/PostgreSQL
4. Clone repository
5. Set up virtual environment
6. Install dependencies
7. Configure Gunicorn
8. Set up Nginx reverse proxy
9. Configure SSL
10. Run migrations

---

## 🔐 Environment Variables Reference

### Required Variables
```env
SECRET_KEY=                 # Django secret key
DEBUG=True|False           # Development mode
ALLOWED_HOSTS=             # Comma-separated domain list
```

### Email Variables
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=           # Gmail address
EMAIL_HOST_PASSWORD=       # Gmail app password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=        # From address
```

### Database Variables (for MySQL/PostgreSQL)
```env
DB_ENGINE=                 # Database backend
DB_NAME=                   # Database name
DB_USER=                   # Database user
DB_PASSWORD=               # Database password
DB_HOST=localhost          # Database host
DB_PORT=3306|5432          # Database port
```

### Or use DATABASE_URL (for production)
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Security Variables
```env
CSRF_TRUSTED_ORIGINS=      # Trusted origins (comma-separated)
```

### reCAPTCHA Variables
```env
RECAPTCHA_SITE_KEY=        # Public reCAPTCHA key
RECAPTCHA_SECRET_KEY=      # Secret reCAPTCHA key
```

---

## 🔧 Environment-Specific Configurations

### Development Environment
```bash
# .env
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Staging Environment
```bash
# .env
DEBUG=False
DB_ENGINE=django.db.backends.mysql
ALLOWED_HOSTS=staging.yourdomain.com
```

### Production Environment
```bash
# .env
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'dotenv'`
**Solution:**
```bash
pip install python-dotenv
```

### Issue: Database connection error
**Solution:** Verify database credentials in `.env`:
```bash
# Test MySQL connection
mysql -u erp_user -p college_erp_db

# Or check .env has correct values
cat .env | grep DB_
```

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: reCAPTCHA validation fails
**Solution:**
1. Verify Site Key and Secret Key match domains
2. Check reCAPTCHA checkbox on form
3. Ensure keys are in settings.py or .env
4. Or recreate reCAPTCHA keys in Google Admin Console

### Issue: Email not sending
**Solution:**
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password (not regular password)
3. Update EMAIL_HOST_PASSWORD in .env with App Password
4. Verify EMAIL_HOST_USER is correct
5. Test with: `python manage.py shell`
   ```python
   from django.core.mail import send_mail
   send_mail('Test', 'Body', 'from@gmail.com', ['to@example.com'])
   ```

### Issue: DEBUG mode won't disable
**Solution:**
```bash
# Make sure .env has exact value
DEBUG=False  # Not True, not true, not FALSE

# Restart server after changing
python manage.py runserver
```

### Issue: CSRF token missing
**Solution:**
1. Add `{% csrf_token %}` in all POST forms
2. Verify CSRF_TRUSTED_ORIGINS in settings
3. Check CSRF_COOKIE_SECURE setting

---

## 📚 Additional Resources

### Official Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Google reCAPTCHA](https://www.google.com/recaptcha/admin)

### Hosting Recommendations
- [PythonAnywhere](https://www.pythonanywhere.com) - Easiest for beginners
- [Heroku](https://www.heroku.com) - Good for quick deployment
- [DigitalOcean](https://www.digitalocean.com) - Most flexible
- [AWS](https://aws.amazon.com) - Enterprise-grade

### Security Best Practices
- Always use HTTPS in production
- Keep SECRET_KEY secret (not in git)
- Use strong database passwords
- Enable CSRF protection
- Use HttpOnly and Secure cookie flags
- Implement rate limiting
- Keep dependencies updated

---

## ✅ Final Checklist

**Development Ready:**
- [x] Environment variables configured
- [x] Database set up (SQLite/MySQL/PostgreSQL)
- [x] Email configured
- [x] reCAPTCHA keys added
- [x] Security headers configured
- [x] Logging set up
- [x] Static files handled
- [x] Server running

**Production Ready:**
- [ ] DEBUG = False
- [ ] New SECRET_KEY generated
- [ ] ALLOWED_HOSTS configured
- [ ] SSL/TLS certificate installed
- [ ] Database migrated
- [ ] Superuser created
- [ ] Backups configured
- [ ] Monitoring set up

---

## 🎉 You're Ready!

Your **College ERP** project is fully configured for both development and production deployment.

**For Help:**
- Visit: [GitHub Repository](https://github.com/VanshTyagi/College-ERP)
- Create an Issue for bugs
- Contact support for deployment help

**Happy Coding! 🚀**

---

*Last Updated: April 23, 2026*  
*College ERP Suite v2.0.0*
