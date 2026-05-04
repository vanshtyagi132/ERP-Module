# Developer Quick Reference Guide

## 🎯 Feature Overview

### Feature 1️⃣ Admin Settings Management
**Problem Solved:** Admin email and details were hardcoded; no way to change them without code modification

**Solution:** 
- Centralized admin configuration interface
- Database storage for settings
- Web UI for non-technical users
- Admin panel integration

**Key Files:**
- Model: `main_app/models.py` - `AdminSettings` class
- View: `main_app/admin_settings_views.py` - `admin_settings_view()`
- Form: `main_app/forms.py` - `AdminSettingsForm`
- Template: `main_app/templates/hod_template/admin_settings.html`
- URL: `/admin/settings/`

---

### Feature 2️⃣ File Sharing with Email Notifications
**Problem Solved:** No way to share files with students/staff; no email notifications for shared content

**Solution:**
- File attachment support in notifications
- Dual delivery (FCM + Email)
- Notice board display of shared files
- Broadcast functionality
- File validation and storage

**Key Files:**
- Models: `main_app/models.py` - `Attachment`, updated `NotificationStaff/Student`
- Views: `main_app/admin_settings_views.py` - Multiple view functions
- Templates: Updated notification templates + new broadcast template
- URLs: `/send_student_notification_with_file/`, `/send_staff_notification_with_file/`, `/admin/broadcast/students/`, `/admin/broadcast/staff/`

---

## 🛠️ Key Functions & APIs

### Core Notification Function
```python
# File: main_app/admin_settings_views.py
def send_notification_with_file(recipient_type, recipient_id, message, file_obj=None, is_fcm=True):
    """
    Send notification with optional file attachment
    
    Args:
        recipient_type: 'student' or 'staff'
        recipient_id: CustomUser ID of recipient
        message: Notification message text
        file_obj: Optional file object to attach
        is_fcm: Whether to send FCM notification (default True)
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
```

### Email Notification Function
```python
# File: main_app/admin_settings_views.py
def send_email_notification(recipient_email, subject, message, file_obj=None, admin_settings=None):
    """
    Send email notification with optional attachment
    
    Args:
        recipient_email: Email address to send to
        subject: Email subject
        message: Email body message
        file_obj: Optional file object to attach
        admin_settings: AdminSettings object
    """
```

### Admin Settings Getter
```python
# File: main_app/models.py
AdminSettings.get_settings()  # Returns single AdminSettings object, creates if needed
```

---

## 📂 File Structure Reference

```
main_app/
├── models.py                          # AdminSettings, Attachment models
├── forms.py                           # AdminSettingsForm, NotificationWithAttachmentForm
├── admin.py                           # Admin customizations
├── admin_settings_views.py            # NEW - All admin settings & notification views
├── urls.py                            # Updated with new routes
├── hod_views.py                       # Updated imports
├── staff_views.py                     # (No changes, uses existing endpoints)
├── student_views.py                   # (No changes, uses existing endpoints)
├── templates/
│   ├── hod_template/
│   │   ├── admin_settings.html                  # NEW
│   │   ├── broadcast_notification.html          # NEW
│   │   ├── student_notification.html            # UPDATED
│   │   └── staff_notification.html              # UPDATED
│   ├── student_template/
│   │   └── student_view_notification.html       # UPDATED
│   └── staff_template/
│       └── staff_view_notification.html         # UPDATED
└── migrations/                        # Will be auto-created
    └── XXXX_add_new_models.py         # Auto-generated
```

---

## 🔌 API Endpoints

### Admin Settings
| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/admin/settings/` | GET/POST | HOD/Admin | View/edit admin settings |
| `/admin/main_app/adminsettings/` | GET/POST | Superuser | Django admin interface |

### Notifications
| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/send_student_notification/` | POST | HOD/Admin | Send to student (original) |
| `/send_staff_notification/` | POST | HOD/Admin | Send to staff (original) |
| `/send_student_notification_with_file/` | POST | HOD/Admin | Send to student with file |
| `/send_staff_notification_with_file/` | POST | HOD/Admin | Send to staff with file |
| `/admin/broadcast/students/` | GET/POST | HOD/Admin | Broadcast to all students |
| `/admin/broadcast/staff/` | GET/POST | HOD/Admin | Broadcast to all staff |

### Viewing
| Endpoint | Method | Access | Purpose |
|----------|--------|--------|---------|
| `/student/view/notification/` | GET | Student | View own notifications |
| `/staff/view/notification/` | GET | Staff | View own notifications |

---

## 💾 Database Schema

### AdminSettings Table
```sql
CREATE TABLE main_app_adminsettings (
    id INTEGER PRIMARY KEY,
    admin_email VARCHAR(254) UNIQUE NOT NULL,
    admin_phone VARCHAR(15),
    admin_office_address TEXT,
    college_name VARCHAR(255),
    college_website VARCHAR(200),
    support_email VARCHAR(254),
    enable_email_notifications BOOLEAN DEFAULT true,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW
);
```

### Attachment Table
```sql
CREATE TABLE main_app_attachment (
    id INTEGER PRIMARY KEY,
    uploaded_by_id INTEGER NOT NULL,
    file VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    attachment_type VARCHAR(20) DEFAULT 'other',
    file_size BIGINT DEFAULT 0,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW,
    FOREIGN KEY(uploaded_by_id) REFERENCES main_app_customuser(id)
);
```

### NotificationStudent & NotificationStaff (Updated)
```sql
ALTER TABLE main_app_notificationstudent ADD COLUMN attachment VARCHAR(100);
ALTER TABLE main_app_notificationstaff ADD COLUMN attachment VARCHAR(100);
```

---

## 🔄 Data Flow Diagrams

### File Sharing Flow
```
Admin selects file + message
         ↓
send_student_notification_with_file() endpoint
         ↓
         ├→ save_notification_with_file() to DB
         ├→ send_fcm_notification() via Firebase
         └→ send_email_notification() via SMTP
         ↓
Student receives:
├→ Push notification (mobile/web)
├→ Email with file details
└→ File appears in notice board
         ↓
Student downloads file from notice board
```

### Admin Settings Flow
```
Admin navigates to /admin/settings/
         ↓
admin_settings_view() retrieves AdminSettings.get_settings()
         ↓
Display form with current values
         ↓
Admin fills form and submits
         ↓
AdminSettingsForm validates input
         ↓
Save to database
         ↓
Success message displayed
```

---

## 🎨 Frontend Components

### File Upload Handler (JavaScript)
```javascript
// In student_notification.html and staff_notification.html
$("#attachment").change(function(){
    var file = this.files[0];
    if (file) {
        var fileSize = (file.size / 1024 / 1024).toFixed(2);
        if (fileSize > 5) {
            alert("File size exceeds 5MB limit!");
            $(this).val("")
        } else {
            $("#file-info").html(file.name + " (" + fileSize + " MB)")
        }
    }
})
```

### File Download Template
```html
{% if notification.attachment %}
    <a href="{{ notification.attachment.url }}" class="btn btn-sm btn-primary" download>
        <i class="fas fa-download"></i> Download
    </a>
    <br>
    <small class="text-muted">{{ notification.attachment|filesizeformat }}</small>
{% else %}
    <span class="text-muted">-</span>
{% endif %}
```

---

## 🔐 Security Checklist

- ✅ CSRF protection on all POST requests
- ✅ Login required for all views
- ✅ Permission checking (user_type == 1)
- ✅ File type whitelist validation
- ✅ File size limit (5MB)
- ✅ Email format validation
- ✅ SQL injection prevention (ORM)
- ✅ XSS prevention (template escaping)
- ✅ Secure file storage (media directory)
- ✅ FCM key properly configured

---

## 🚀 Deployment Checklist

- [ ] Run migrations: `python manage.py migrate`
- [ ] Create media directories with proper permissions
- [ ] Set environment variables (.env):
  - EMAIL_HOST
  - EMAIL_PORT
  - EMAIL_HOST_USER
  - EMAIL_HOST_PASSWORD
  - DEFAULT_FROM_EMAIL
- [ ] Test email sending with `python manage.py shell`
- [ ] Create AdminSettings record
- [ ] Test file upload with small file
- [ ] Test notification to student
- [ ] Verify email received
- [ ] Verify file downloaded successfully
- [ ] Test broadcast functionality
- [ ] Verify all permissions working

---

## 📊 Configuration Examples

### Environment Variables (.env)
```
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=sender@gmail.com
EMAIL_HOST_PASSWORD=app_specific_password
DEFAULT_FROM_EMAIL=College ERP <noreply@collegeerp.com>

# For Gmail App Password Setup:
# 1. Enable 2-Factor Authentication
# 2. Go to https://myaccount.google.com/apppasswords
# 3. Select Mail and Windows Computer
# 4. Copy the 16-character password
# 5. Use as EMAIL_HOST_PASSWORD
```

### AdminSettings Configuration (via Web UI)
```
College Name: ABC Engineering College
Admin Email: admin@collegeerp.com
Support Email: support@collegeerp.com
Phone: +91-98765432**
Office Address: 123 College Street, City, State 12345
Website: https://www.abc-college.edu.in
Enable Email Notifications: ✓ (checked)
```

---

## 🧪 Testing Guide

### Test 1: Admin Settings
```bash
# Via Django Shell
python manage.py shell
>>> from main_app.models import AdminSettings
>>> settings = AdminSettings.get_settings()
>>> settings.admin_email = "test@college.com"
>>> settings.save()
>>> print(settings.college_name)
```

### Test 2: Send Notification with File
```python
# Via Django Shell
from main_app.admin_settings_views import send_notification_with_file
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

file_obj = ContentFile(b"test content", name="test.txt")
result = send_notification_with_file('student', 1, 'Test message', file_obj)
print(result)  # {'success': True, 'message': 'Notification sent to student'}
```

### Test 3: Email Sending
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail(
...     'Test Subject',
...     'Test message',
...     'from@college.com',
...     ['to@student.com']
... )
# Should return 1 if successful
```

---

## 📝 Code Examples

### Example 1: Send File Programmatically
```python
from main_app.admin_settings_views import send_notification_with_file
from main_app.models import Student

# Get student
student = Student.objects.first()

# Send notification with message only
result = send_notification_with_file(
    'student',
    student.admin_id,
    'Your assignment grades are ready'
)

# Send with file
with open('assignment_grades.pdf', 'rb') as f:
    result = send_notification_with_file(
        'student',
        student.admin_id,
        'Your assignment grades are ready',
        f
    )

print(result['message'])
```

### Example 2: Broadcast to All Students
```python
from main_app.models import Student
from main_app.admin_settings_views import send_notification_with_file

students = Student.objects.all()
sent = 0

for student in students:
    result = send_notification_with_file(
        'student',
        student.admin_id,
        'Important notice regarding exam schedule'
    )
    if result['success']:
        sent += 1

print(f"Sent to {sent} students")
```

### Example 3: Get Admin Settings
```python
from main_app.models import AdminSettings

# Get settings (creates if doesn't exist)
settings = AdminSettings.get_settings()

# Use in view
context = {
    'college_name': settings.college_name,
    'support_email': settings.support_email,
    'admin_email': settings.admin_email,
}
```

---

## 🐛 Debugging Tips

### Enable Django Debug Mode
```python
# settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Check Email Logs
```bash
# Gmail SMTP Logs
tail -f /tmp/email.log
```

### Database Query Logging
```python
# In Django Shell
from django.db import connection
from django.db import reset_queries

reset_queries()
# ... do something ...
print(connection.queries)
```

---

## 📚 Related Documentation

- Django File Upload: https://docs.djangoproject.com/en/3.1/topics/files/
- Django Email: https://docs.djangoproject.com/en/3.1/topics/email/
- Firebase Cloud Messaging: https://firebase.google.com/docs/cloud-messaging
- HTML Email Best Practices: https://www.campaignmonitor.com/resources/

---

## ✅ Quick Verification

After implementation, verify:

```bash
# 1. Check migrations created
python manage.py showmigrations main_app | grep -i "admin\|attachment\|notification"

# 2. Check models loaded
python manage.py shell
>>> from main_app.models import AdminSettings, Attachment
>>> print("Models loaded successfully")

# 3. Check URLs configured
python manage.py shell
>>> from django.urls import resolve
>>> print(resolve('/admin/settings/'))

# 4. Check admin registered
python manage.py shell
>>> from django.contrib.admin import site
>>> list(site._registry.keys())
```

---

**Implementation Complete!** 🎉

This guide should help developers understand and work with the new features. For more details, refer to the main documentation file.
