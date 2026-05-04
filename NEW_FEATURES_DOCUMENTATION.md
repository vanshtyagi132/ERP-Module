# ERP Module - New Features Documentation

## 📋 Overview
This document describes the two major features added to the College ERP Module:
1. **Admin Settings Management** - Configure administrator email and institution details
2. **File Sharing with Email Notifications** - Share files/attachments with staff/students with email alerts

---

## ✨ Feature 1: Admin Settings Management

### Purpose
Allows administrators to configure and manage system-wide settings including email addresses, contact information, and institution details. This eliminates the need to manually update hardcoded values and provides a centralized configuration interface.

### Models

#### `AdminSettings` Model
Located in `main_app/models.py`, this model stores all configurable admin settings:

```python
class AdminSettings(models.Model):
    admin_email            # Primary admin email for system notifications
    admin_phone            # Admin contact phone number
    admin_office_address   # Admin office address
    college_name           # College/Institution name
    college_website        # College website URL
    support_email          # Support email for queries
    enable_email_notifications  # Toggle for email notifications
    created_at            # Creation timestamp
    updated_at            # Last update timestamp
```

**Key Methods:**
- `AdminSettings.get_settings()` - Get or create the single settings object

### Views

#### `admin_settings_view(request)` - Admin Settings Page
- **URL**: `/admin/settings/`
- **Access**: HOD/Admin only
- **Functionality**: 
  - Display current admin settings in a form
  - Allow editing of all configurable settings
  - Save changes to database
  - Show success/error messages

### Forms

#### `AdminSettingsForm` (in `main_app/forms.py`)
- Handles form rendering for admin settings
- Uses Bootstrap styling for consistency
- Validates email formats and URLs
- Provides helpful tooltips and descriptions

### Frontend

#### `admin_settings.html` Template
Located in `main_app/templates/hod_template/admin_settings.html`

**Features:**
- Clean, organized form with sections:
  - Email Configuration
  - Institution Details
  - Contact Information
- Real-time validation
- Bootstrap styling and icons
- Help text for each field

### How to Use

1. **Login as Admin/HOD**
2. **Navigate to Settings**: Click "Admin Settings" in the admin menu
3. **Edit Settings**: Fill in or update the following:
   - Primary Admin Email
   - Support Email
   - Institution Name
   - Phone Number
   - Office Address
   - Website URL
4. **Enable/Disable Email Notifications**: Check the box to enable email alerts for file sharing
5. **Save**: Click "Save Settings"

**Example Configuration:**
```
College Name: ABC Engineering College
Admin Email: admin@collegeerp.com
Support Email: support@collegeerp.com
Phone: +91-XXXXXXXXXX
Website: https://www.collegeerp.com
```

---

## 📎 Feature 2: File Sharing with Email Notifications

### Purpose
Enables administrators and staff to share files and attachments with students and staff. When a file is shared, recipients are notified via:
1. **Push Notification** (FCM) - Immediate notification on mobile/web
2. **Email** (Optional) - Email with file details sent to recipient's inbox
3. **Notice Board** - Shared files appear in recipient's notification center

### Models

#### `Attachment` Model
Stores file attachments shared through the system:

```python
class Attachment(models.Model):
    uploaded_by           # CustomUser who uploaded the file
    file                  # File upload field
    title                 # Human-readable title
    description           # Optional description
    attachment_type       # Type: assignment, study_material, notice, other
    file_size            # File size in bytes
    created_at           # Creation timestamp
    updated_at           # Last update timestamp
```

#### Updated `NotificationStaff` & `NotificationStudent` Models
Both models now include an optional `attachment` field:

```python
class NotificationStaff(models.Model):
    staff               # ForeignKey to Staff
    message             # Notification message
    attachment          # NEW: FileField for attachments
    created_at          # Creation timestamp
    updated_at          # Last update timestamp

class NotificationStudent(models.Model):
    student             # ForeignKey to Student
    message             # Notification message
    attachment          # NEW: FileField for attachments
    created_at          # Creation timestamp
    updated_at          # Last update timestamp
```

### Views & Functions

#### `send_notification_with_file(recipient_type, recipient_id, message, file_obj, is_fcm)`
Core function in `admin_settings_views.py` that handles:
- Saving notification with attachment to database
- Sending FCM push notification
- Sending email if enabled
- Retrieving admin settings

**Parameters:**
- `recipient_type`: 'student' or 'staff'
- `recipient_id`: ID of recipient's CustomUser
- `message`: Notification message text
- `file_obj`: Optional file object
- `is_fcm`: Whether to send FCM notification (default: True)

**Returns:**
```python
{'success': True/False, 'message': 'status message'}
```

#### `send_student_notification_with_file(request)` - Send to Student
- **URL**: `/send_student_notification_with_file/`
- **Method**: POST
- **Parameters**: 
  - `id`: Student's CustomUser ID
  - `message`: Notification message
  - `attachment`: (Optional) File object

#### `send_staff_notification_with_file(request)` - Send to Staff
- **URL**: `/send_staff_notification_with_file/`
- **Method**: POST
- **Parameters**:
  - `id`: Staff's CustomUser ID
  - `message`: Notification message
  - `attachment`: (Optional) File object

#### `broadcast_notification_to_all_students(request)` - Broadcast to All Students
- **URL**: `/admin/broadcast/students/`
- **Functionality**: Send notification to all students in the system
- **Returns**: Success message with count of recipients

#### `broadcast_notification_to_all_staff(request)` - Broadcast to All Staff
- **URL**: `/admin/broadcast/staff/`
- **Functionality**: Send notification to all staff members in the system
- **Returns**: Success message with count of recipients

### Email Sending

#### `send_fcm_notification(fcm_token, title, message, click_action)`
Sends push notification via Firebase Cloud Messaging

#### `send_email_notification(recipient_email, subject, message, file_obj, admin_settings)`
Sends email with:
- HTML formatted message with institution branding
- Optional file attachment
- Support email footer
- Institution contact information

**Email Features:**
- HTML template with styling
- Professional formatting
- Attachment support
- College branding included
- Contact information in footer

### Frontend

#### Updated Templates

**`student_notification.html` (HOD Template)**
- Updated modal with file upload support
- File size validation (5MB limit)
- File type restrictions
- Real-time file info display
- Enhanced send functionality via FormData

**`staff_notification.html` (HOD Template)**
- Same enhancements as student notification
- File upload modal with validation
- Support for large files

**`student_view_notification.html` (Student Template)**
- Added "Attachment" column to notification table
- Download button for attached files
- File size display
- Visual indicators for files

**`staff_view_notification.html` (Staff Template)**
- Same enhancements as student template
- Download links for all attachments
- File information display

**`broadcast_notification.html`**
- New template for broadcasting to all students/staff
- Large message textarea
- File upload support
- Batch send functionality

### Forms

#### `NotificationWithAttachmentForm` (in `main_app/forms.py`)
Form for sending notifications with files:
- Message textarea
- File upload field with validation
- Accepted file types: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, JPG, PNG, JPEG, ZIP

### File Storage

Files are stored in:
```
media/notifications/student/    # Student notification attachments
media/notifications/staff/      # Staff notification attachments
media/attachments/YYYY/MM/DD/   # General attachments
```

### How to Use

#### Sending File to Individual Student/Staff

1. **Login as Admin/HOD**
2. **Navigate to Notifications**:
   - Click "Send Notifications To Students" or "Send Notifications To Staff"
3. **Select Recipient**: Click "Send Notification" button for desired person
4. **Fill in Details**:
   - Enter notification message
   - (Optional) Select a file to attach
   - File size limit: 5MB
5. **Submit**: Click "Send Notification"
   - Recipient receives push notification immediately
   - Email sent (if enabled in settings)
   - File appears in their notice board

#### Broadcasting to All

1. **Navigate to**: `/admin/broadcast/students/` or `/admin/broadcast/staff/`
2. **Enter Message**: Type notification message
3. **Attach File** (Optional)
4. **Send**: Click "Send Broadcast"
5. **Confirmation**: See success message with number of recipients

#### Viewing Shared Files (Student/Staff)

1. **Login as Student/Staff**
2. **Go to Notifications**: "View Notifications" menu option
3. **View Files**: See all notifications with attachments
4. **Download**: Click "Download" button to save file
5. **File Info**: See file size and upload date

---

## 🔧 Admin Interface

All new models are registered in Django Admin at `/admin/`:

### AdminSettings Admin
- View all system settings
- Edit settings directly from admin
- Timestamp tracking

### Attachment Admin
- View all uploaded attachments
- Search by title or uploader
- Filter by attachment type and date
- See file size information

### NotificationStaff Admin
- View all staff notifications
- Search by staff email or message content
- Filter by date
- See which notifications have attachments

### NotificationStudent Admin
- View all student notifications
- Search by student email or message
- Filter by date
- Identify notifications with files

---

## 📧 Email Configuration

For email notifications to work, ensure these environment variables are set in `.env`:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=College ERP <noreply@collegeerp.com>
```

### Gmail Setup (if using Gmail):
1. Enable 2-Factor Authentication
2. Create an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the App Password as `EMAIL_HOST_PASSWORD`

---

## 🚀 Setup Instructions

### 1. Install/Update Django
```bash
pip install -r requirements.txt
```

### 2. Create and Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Media Directories
```bash
mkdir -p media/notifications/student
mkdir -p media/notifications/staff
mkdir -p media/attachments
```

### 4. Configure Admin Settings
- Login to admin panel as superuser
- Go to `/admin/main_app/adminsettings/`
- Create initial admin settings (or use the web interface)
- Fill in your institution details
- Save

### 5. Set Email Credentials
Update `.env` file with your email configuration

### 6. Test Features
- Send a test notification with file attachment
- Verify file appears in recipient's notice board
- Check email inbox for notification

---

## 📱 Features Summary

### Feature 1: Admin Settings ✓
- ✓ Centralized admin configuration
- ✓ Email management
- ✓ Institution details
- ✓ Contact information
- ✓ Email notification toggle

### Feature 2: File Sharing ✓
- ✓ Send files to individual students
- ✓ Send files to individual staff
- ✓ Broadcast files to all students
- ✓ Broadcast files to all staff
- ✓ Push notifications (FCM)
- ✓ Email notifications (optional)
- ✓ File download from notice board
- ✓ File type validation
- ✓ File size validation (5MB limit)
- ✓ Admin interface for attachments

---

## 🐛 Troubleshooting

### Email Not Sending?
1. Check environment variables are set correctly
2. Verify SMTP credentials are valid
3. Check `EMAIL_USE_TLS = True` in settings
4. Enable "Less secure app access" (if using Gmail)
5. Check Django logs for errors

### Files Not Uploading?
1. Verify `media` directory exists and is writable
2. Check file size is under 5MB
3. Verify file type is in allowed list
4. Check form validation errors

### Notifications Not Appearing?
1. Verify FCM token is set for recipient
2. Check internet connection
3. Ensure FCM credentials are valid
4. Check browser console for JavaScript errors

### Admin Settings Not Saving?
1. Ensure you're logged in as HOD/Admin
2. Check all required fields are filled
3. Verify email format is valid
4. Check database permissions

---

## 📊 Database Schema

### AdminSettings Table
```sql
CREATE TABLE main_app_adminsettings (
    id INTEGER PRIMARY KEY,
    admin_email VARCHAR(254) UNIQUE,
    admin_phone VARCHAR(15),
    admin_office_address TEXT,
    college_name VARCHAR(255),
    college_website VARCHAR(200),
    support_email VARCHAR(254),
    enable_email_notifications BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Attachment Table
```sql
CREATE TABLE main_app_attachment (
    id INTEGER PRIMARY KEY,
    uploaded_by_id INTEGER,
    file VARCHAR(100),
    title VARCHAR(255),
    description TEXT,
    attachment_type VARCHAR(20),
    file_size BIGINT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY(uploaded_by_id) REFERENCES main_app_customuser(id)
);
```

### NotificationStudent/Staff Tables
Updated with:
```sql
ALTER TABLE main_app_notificationstudent ADD COLUMN attachment VARCHAR(100);
ALTER TABLE main_app_notificationstaff ADD COLUMN attachment VARCHAR(100);
```

---

## 🔐 Security Notes

1. **File Validation**: All files are validated for type and size
2. **Access Control**: Only HOD/Admin can send notifications
3. **Email Verification**: Recipient emails must be valid
4. **FCM Token**: Used for push notifications only
5. **Django Security**: All forms are CSRF protected

---

## 📝 Sample Usage

### Example 1: Send Assignment to Student
```
1. Login as Admin
2. Go to "Send Notifications To Students"
3. Find "John Doe" and click "Send Notification"
4. Message: "Submit Assignment 1 by Friday"
5. Attach: "Assignment1.pdf"
6. Click "Send Notification"
7. John receives:
   - Push notification on app
   - Email with file link
   - File in his notice board
```

### Example 2: Broadcast Notice to All
```
1. Login as Admin
2. Go to "/admin/broadcast/students/"
3. Message: "College closed for festival holidays"
4. Attach: "Holiday_Notice.pdf"
5. Click "Send Broadcast"
6. All 500+ students receive notification & email
```

### Example 3: Update Admin Settings
```
1. Login as Admin
2. Go to "Admin Settings"
3. Update:
   - Admin Email: newemail@college.com
   - Support Email: support@college.com
   - College Name: ABC Engineering College
   - Phone: +91-9876543210
4. Check "Enable Email Notifications"
5. Click "Save Settings"
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Django and email logs
3. Verify all environment variables are set
4. Check file permissions on media directory

---

## 📄 Version Info
- Created: May 4, 2026
- Django Version: 3.1+
- Python Version: 3.7+
- Database: SQLite/PostgreSQL compatible

---

## 🎯 Future Enhancements

Potential improvements for future versions:
- Scheduling notifications for future dates
- Recurring notifications
- Read receipts for notifications
- File versioning and history
- Bulk file uploads
- Integration with Google Drive/OneDrive
- SMS notifications
- WhatsApp notifications
- Notification templates
- Multi-language support

---

**All features have been successfully implemented and tested!** 🎉
