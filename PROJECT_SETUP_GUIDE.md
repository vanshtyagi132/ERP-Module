# College ERP Module - Complete Setup Guide (A to Z)

Complete step-by-step guide to set up and run the College ERP Module from scratch.

---

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.7+ installed
- pip package manager
- Git (optional, for version control)
- A text editor or IDE (VS Code, PyCharm, etc.)

**Check Python Installation:**
```bash
python --version
# or
python3 --version
```

---

## 🚀 Complete Setup Steps

### Step 1: Navigate to Project Directory

```bash
cd d:\GitHub\ERP-Module
```

Or if using different path:
```bash
cd /path/to/ERP-Module
```

---

### Step 2: Create Virtual Environment

#### Windows (PowerShell / Command Prompt)
```bash
# Using python
python -m venv venv

# Or using python3
python3 -m venv venv
```

#### macOS / Linux
```bash
python3 -m venv venv
```

---

### Step 3: Activate Virtual Environment

#### Windows (PowerShell)
```bash
.\venv\Scripts\Activate.ps1
```

**If you get execution policy error**, run:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt / CMD)
```bash
venv\Scripts\activate.bat
```

#### macOS / Linux (Bash)
```bash
source venv/bin/activate
```

#### macOS / Linux (Zsh)
```bash
source venv/bin/activate
```

**Verify Activation** - Your prompt should show `(venv)` prefix:
```
(venv) D:\GitHub\ERP-Module>
```

---

### Step 4: Upgrade pip

#### Windows
```bash
python -m pip install --upgrade pip
```

#### macOS / Linux
```bash
python3 -m pip install --upgrade pip
```

---

### Step 5: Install Required Dependencies

```bash
# Install all packages from requirements.txt
pip install -r requirements.txt
```

**Expected packages to install:**
- Django 3.1+
- requests
- python-dotenv
- whitenoise
- gunicorn
- Pillow (for image handling)
- And other dependencies

**Progress indicator** - You should see output like:
```
Collecting Django==3.1.7
  Downloading Django-3.1.7-py3-none-any.whl (7.6 MB)
Installing collected packages: ...
Successfully installed ...
```

---

### Step 6: Create Environment Variables File

Create a `.env` file in the project root directory:

```bash
# Windows (PowerShell)
New-Item -Path .env -Type File

# Windows (CMD)
type nul > .env

# macOS / Linux
touch .env
```

**Edit `.env` file** (add the following content):

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-this-in-production

# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email Configuration (for Gmail SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=College ERP <noreply@collegeerp.com>
EMAIL_USE_TLS=True

# reCAPTCHA Keys (if needed)
RECAPTCHA_SITE_KEY=your-site-key
RECAPTCHA_SECRET_KEY=your-secret-key

# Firebase FCM Key
FCM_KEY=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB

# Allowed Hosts (for production)
ALLOWED_HOSTS=localhost,127.0.0.1
```

**For Gmail SMTP Authentication:**
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use the 16-character password as `EMAIL_HOST_PASSWORD`

---

### Step 7: Create Media Directories

#### Windows (PowerShell)
```bash
# Create notification directories
New-Item -ItemType Directory -Path "media\notifications\student" -Force
New-Item -ItemType Directory -Path "media\notifications\staff" -Force
New-Item -ItemType Directory -Path "media\attachments" -Force
```

#### Windows (CMD)
```bash
# Create notification directories
mkdir media\notifications\student
mkdir media\notifications\staff
mkdir media\attachments
```

#### macOS / Linux
```bash
# Create notification directories
mkdir -p media/notifications/student
mkdir -p media/notifications/staff
mkdir -p media/attachments
```

---

### Step 8: Apply Database Migrations

```bash
# Make migrations for any pending model changes
python manage.py makemigrations

# Apply all migrations to database
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, main_app, sessions
Running migrations:
  Applying main_app.0001_initial... OK
  Applying main_app.0002_add_admin_settings... OK
  ... (more migrations) ...
```

---

### Step 9: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

**Interactive prompts** - Fill in the following:

```
Username: admin
Email address: admin@collegeerp.com
Password: (enter a strong password)
Password (again): (repeat password)
Superuser created successfully.
```

**Remember your admin credentials:**
- Username: `admin`
- Email: `admin@collegeerp.com`
- Password: `(your chosen password)`

---

### Step 10: Collect Static Files (Optional, for Production)

```bash
python manage.py collectstatic --noinput
```

This will gather all static files (CSS, JS, images) into a single directory.

---

### Step 11: Create Admin Settings Record

```bash
python manage.py shell
```

**In the Django shell, execute:**

```python
from main_app.models import AdminSettings

# Create or get settings
settings = AdminSettings.get_settings()

# Update with your college details
settings.admin_email = "admin@collegeerp.com"
settings.college_name = "ABC Engineering College"
settings.support_email = "support@collegeerp.com"
settings.admin_phone = "+91-9876543210"
settings.admin_office_address = "123 College Street, City, State 12345"
settings.college_website = "https://www.abc-college.com"
settings.enable_email_notifications = True

# Save
settings.save()

print("Admin settings configured successfully!")
exit()
```

---

### Step 12: Run the Development Server

```bash
# Start the Django development server
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
May 04, 2026 - 12:00:00
Django version 3.1.7, Python 3.9.0
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 Access the Application

### Local Access

Open your browser and navigate to:

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Admin Settings**: http://127.0.0.1:8000/admin/settings/

### Login Credentials

**Admin Panel:**
- Username: `admin`
- Password: `(your chosen password)`

---

## 🧪 Testing the Features

### Test Admin Settings

1. Go to http://127.0.0.1:8000/admin/settings/
2. Verify that admin details are displayed
3. Update a field and click "Save Settings"
4. Verify the change was saved

### Test File Sharing

1. Login as admin
2. Go to "Send Notifications to Students"
3. Select a student
4. Add a message and attach a file
5. Click "Send Notification"
6. Verify:
   - Push notification sent (FCM)
   - Email sent (check inbox)
   - File appears in student's notice board

---

## ⚙️ Troubleshooting

### Virtual Environment Not Activating

**Windows PowerShell - Execution Policy Error:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then activate again
.\venv\Scripts\Activate.ps1
```

### Dependency Installation Fails

```bash
# Clear pip cache and retry
pip install --no-cache-dir -r requirements.txt

# Or install specific problematic package
pip install --upgrade pillow
```

### Migration Issues

```bash
# If migrations are stuck
python manage.py migrate --fake-initial

# Or reset migrations (⚠️ deletes all data)
python manage.py migrate main_app zero
python manage.py migrate
```

### Port 8000 Already in Use

```bash
# Use a different port
python manage.py runserver 8080

# Or kill the process using port 8000
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

### Database File Not Found

```bash
# Ensure db.sqlite3 file exists after migrations
python manage.py migrate
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# In settings.py, ensure STATIC_URL is set correctly
STATIC_URL = '/static/'
```

---

## 📦 Quick Reference Commands

### Regular Development Workflow

```bash
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1           # Windows PowerShell
source venv/bin/activate             # macOS/Linux

# 2. Check installed packages
pip list

# 3. Make migrations (if models changed)
python manage.py makemigrations

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser (if needed)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver

# 7. Access application
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/admin/
```

### Database Management

```bash
# Show all migrations
python manage.py showmigrations

# Show specific app migrations
python manage.py showmigrations main_app

# Migrate to specific version
python manage.py migrate main_app 0002

# Reverse migrations
python manage.py migrate main_app zero

# Create new migration
python manage.py makemigrations
```

### Django Shell (Interactive)

```bash
# Start Django shell
python manage.py shell

# Example commands:
from main_app.models import Student, Staff, AdminSettings
students = Student.objects.all()
print(f"Total students: {students.count()}")

# Exit shell
exit()
```

### Cleanup & Reset

```bash
# Clear all caches
python manage.py clear_cache

# Remove compiled Python files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Reset entire database (⚠️ caution!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🔧 Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `DEBUG` | Debug mode (True for dev, False for prod) | `True` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `EMAIL_HOST` | SMTP server address | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | Email sender address | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email app password | `xxxx xxxx xxxx xxxx` |
| `DEFAULT_FROM_EMAIL` | From email header | `College ERP <noreply@collegeerp.com>` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |

---

## 📝 Complete Setup Script

### Windows PowerShell (Save as `setup.ps1`)

```powershell
# Complete setup script for Windows PowerShell

Write-Host "Starting College ERP Setup..." -ForegroundColor Green

# Step 1: Create virtual environment
Write-Host "`n[1/10] Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Step 2: Activate virtual environment
Write-Host "[2/10] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Step 3: Upgrade pip
Write-Host "[3/10] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 4: Install dependencies
Write-Host "[4/10] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 5: Create media directories
Write-Host "[5/10] Creating media directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "media\notifications\student" -Force | Out-Null
New-Item -ItemType Directory -Path "media\notifications\staff" -Force | Out-Null
New-Item -ItemType Directory -Path "media\attachments" -Force | Out-Null

# Step 6: Create .env file
Write-Host "[6/10] Creating .env file..." -ForegroundColor Yellow
$envContent = @"
DEBUG=True
SECRET_KEY=your-secret-key-here-change-this-in-production
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=College ERP <noreply@collegeerp.com>
EMAIL_USE_TLS=True
ALLOWED_HOSTS=localhost,127.0.0.1
"@
$envContent | Out-File -FilePath .env -Encoding UTF8

# Step 7: Make migrations
Write-Host "[7/10] Making migrations..." -ForegroundColor Yellow
python manage.py makemigrations

# Step 8: Apply migrations
Write-Host "[8/10] Applying migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 9: Create superuser
Write-Host "[9/10] Creating superuser..." -ForegroundColor Yellow
Write-Host "Please enter admin credentials:" -ForegroundColor Cyan
python manage.py createsuperuser

# Step 10: Collect static files
Write-Host "[10/10] Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host "`n✅ Setup completed successfully!" -ForegroundColor Green
Write-Host "Run 'python manage.py runserver' to start the development server" -ForegroundColor Green
Write-Host "Access admin at http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
```

**Run the script:**
```bash
.\setup.ps1
```

### macOS / Linux (Save as `setup.sh`)

```bash
#!/bin/bash
# Complete setup script for macOS/Linux

echo "Starting College ERP Setup..."

# Step 1: Create virtual environment
echo -e "\n[1/10] Creating virtual environment..."
python3 -m venv venv

# Step 2: Activate virtual environment
echo "[2/10] Activating virtual environment..."
source venv/bin/activate

# Step 3: Upgrade pip
echo "[3/10] Upgrading pip..."
python3 -m pip install --upgrade pip

# Step 4: Install dependencies
echo "[4/10] Installing dependencies..."
pip install -r requirements.txt

# Step 5: Create media directories
echo "[5/10] Creating media directories..."
mkdir -p media/notifications/student
mkdir -p media/notifications/staff
mkdir -p media/attachments

# Step 6: Create .env file
echo "[6/10] Creating .env file..."
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-secret-key-here-change-this-in-production
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=College ERP <noreply@collegeerp.com>
EMAIL_USE_TLS=True
ALLOWED_HOSTS=localhost,127.0.0.1
EOF

# Step 7: Make migrations
echo "[7/10] Making migrations..."
python manage.py makemigrations

# Step 8: Apply migrations
echo "[8/10] Applying migrations..."
python manage.py migrate

# Step 9: Create superuser
echo "[9/10] Creating superuser..."
echo "Please enter admin credentials:"
python manage.py createsuperuser

# Step 10: Collect static files
echo "[10/10] Collecting static files..."
python manage.py collectstatic --noinput

echo -e "\n✅ Setup completed successfully!"
echo "Run 'python manage.py runserver' to start the development server"
echo "Access admin at http://127.0.0.1:8000/admin/"
```

**Make it executable and run:**
```bash
chmod +x setup.sh
./setup.sh
```

---

## 🎯 Post-Setup Checklist

- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] `.env` file created with proper configuration
- [ ] Media directories created
- [ ] Database migrations applied
- [ ] Superuser account created
- [ ] Development server runs without errors
- [ ] Can access http://127.0.0.1:8000/
- [ ] Can access admin panel at http://127.0.0.1:8000/admin/
- [ ] Admin settings configured
- [ ] Can send test notification

---

## 📞 Quick Troubleshooting Commands

```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Show Django version
python -c "import django; print(django.get_version())"

# Check database status
python manage.py dbshell

# Verify static files
python manage.py findstatic --list

# Check admin settings
python manage.py shell -c "from main_app.models import AdminSettings; print(AdminSettings.get_settings())"

# Run tests
python manage.py test

# Check system checks
python manage.py check
```

---

## 🚀 Next Steps After Setup

1. **Configure Admin Settings**: Go to `/admin/settings/` and fill in college details
2. **Add Students**: Use admin panel to add student users
3. **Add Staff**: Use admin panel to add staff members
4. **Test Features**: Send test notifications with files
5. **Customize Templates**: Modify HTML templates as needed
6. **Set Up Email**: Configure Gmail SMTP settings
7. **Configure FCM**: Set up Firebase Cloud Messaging

---

## 📚 Useful Resources

- [Django Documentation](https://docs.djangoproject.com/en/3.1/)
- [Django File Upload Guide](https://docs.djangoproject.com/en/3.1/topics/files/)
- [Django Email Backend](https://docs.djangoproject.com/en/3.1/topics/email/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## 📋 Summary

### Complete Command List (Copypaste)

#### Windows PowerShell
```bash
# Navigate to project
cd d:\GitHub\ERP-Module

# Create venv
python -m venv venv

# Activate venv
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create media directories
New-Item -ItemType Directory -Path "media\notifications\student" -Force
New-Item -ItemType Directory -Path "media\notifications\staff" -Force
New-Item -ItemType Directory -Path "media\attachments" -Force

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Access: http://127.0.0.1:8000/admin/
```

#### macOS / Linux Bash
```bash
# Navigate to project
cd /path/to/ERP-Module

# Create venv
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create media directories
mkdir -p media/notifications/student
mkdir -p media/notifications/staff
mkdir -p media/attachments

# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Access: http://127.0.0.1:8000/admin/
```

---

**You're all set! Follow these steps in order and your College ERP Module will be up and running.** 🎉

Last Updated: May 4, 2026
