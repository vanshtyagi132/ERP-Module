"""
Admin Settings Management Views
Handles admin configuration and settings management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import json
import requests
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import AdminSettings, NotificationStaff, NotificationStudent, Staff, Student, CustomUser
from .forms import AdminSettingsForm, NotificationWithAttachmentForm


@login_required(login_url='login')
def admin_settings_view(request):
    """View and manage admin settings"""
    if request.user.user_type != 1:  # Only HOD/Admin can access
        messages.error(request, "You don't have permission to access this page.")
        return redirect('admin_home')
    
    settings_obj = AdminSettings.get_settings()
    
    if request.method == 'POST':
        form = AdminSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin settings updated successfully!")
            return redirect('admin_settings_view')
    else:
        form = AdminSettingsForm(instance=settings_obj)
    
    context = {
        'form': form,
        'settings': settings_obj
    }
    return render(request, 'hod_template/admin_settings.html', context)


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
    try:
        admin_settings = AdminSettings.get_settings()
        
        if recipient_type == 'student':
            student = get_object_or_404(Student, admin_id=recipient_id)
            recipient_user = student.admin
            
            # Save notification with attachment
            notification = NotificationStudent(
                student=student,
                message=message
            )
            if file_obj:
                notification.attachment = file_obj
            notification.save()
            
            # Send FCM notification if enabled
            if is_fcm and recipient_user.fcm_token:
                send_fcm_notification(
                    recipient_user.fcm_token,
                    f"New Notice with Attachment",
                    message[:100] + "...",
                    reverse('student_view_notification')
                )
            
            # Send email if enabled
            if admin_settings.enable_email_notifications and recipient_user.email:
                send_email_notification(
                    recipient_user.email,
                    "New Notice/Assignment",
                    message,
                    file_obj,
                    admin_settings
                )
            
            return {'success': True, 'message': 'Notification sent to student'}
        
        elif recipient_type == 'staff':
            staff = get_object_or_404(Staff, admin_id=recipient_id)
            recipient_user = staff.admin
            
            # Save notification with attachment
            notification = NotificationStaff(
                staff=staff,
                message=message
            )
            if file_obj:
                notification.attachment = file_obj
            notification.save()
            
            # Send FCM notification if enabled
            if is_fcm and recipient_user.fcm_token:
                send_fcm_notification(
                    recipient_user.fcm_token,
                    f"New Notice with Attachment",
                    message[:100] + "...",
                    reverse('staff_view_notification')
                )
            
            # Send email if enabled
            if admin_settings.enable_email_notifications and recipient_user.email:
                send_email_notification(
                    recipient_user.email,
                    "New Notice/Assignment",
                    message,
                    file_obj,
                    admin_settings
                )
            
            return {'success': True, 'message': 'Notification sent to staff'}
        
        else:
            return {'success': False, 'message': 'Invalid recipient type'}
    
    except Exception as e:
        return {'success': False, 'message': f'Error: {str(e)}'}


def send_fcm_notification(fcm_token, title, message, click_action):
    """
    Send Firebase Cloud Messaging notification
    
    Args:
        fcm_token: FCM token of recipient
        title: Notification title
        message: Notification message
        click_action: URL to open when notification clicked
    """
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': title,
                'body': message,
                'click_action': click_action,
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': fcm_token
        }
        headers = {
            'Authorization': 'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
            'Content-Type': 'application/json'
        }
        requests.post(url, data=json.dumps(body), headers=headers)
    except Exception as e:
        print(f"FCM Error: {str(e)}")


def send_email_notification(recipient_email, subject, message, file_obj=None, admin_settings=None):
    """
    Send email notification with optional attachment
    
    Args:
        recipient_email: Email address to send to
        subject: Email subject
        message: Email body message
        file_obj: Optional file object to attach
        admin_settings: AdminSettings object containing email configuration
    """
    if not admin_settings:
        admin_settings = AdminSettings.get_settings()
    
    try:
        # Prepare email content
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px;">
                    <h2 style="color: #007bff;">New Notice/Assignment from {admin_settings.college_name}</h2>
                    <div style="background-color: white; padding: 15px; border-left: 4px solid #007bff;">
                        <p>{message}</p>
                        <hr>
                        <p style="font-size: 12px; color: #666;">
                            Sent from {admin_settings.college_name}<br>
                            Contact: {admin_settings.support_email}
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=message,  # Plain text fallback
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Email Error: {str(e)}")
        return False


@csrf_exempt
@login_required(login_url='login')
def send_student_notification_with_file(request):
    """
    Enhanced student notification endpoint with file support
    """
    if request.user.user_type != 1:  # Only HOD/Admin
        return HttpResponse("False")
    
    try:
        student_id = request.POST.get('id')
        message = request.POST.get('message')
        file_obj = request.FILES.get('attachment', None)
        
        result = send_notification_with_file(
            'student', student_id, message, file_obj
        )
        
        return HttpResponse("True" if result['success'] else "False")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
@login_required(login_url='login')
def send_staff_notification_with_file(request):
    """
    Enhanced staff notification endpoint with file support
    """
    if request.user.user_type != 1:  # Only HOD/Admin
        return HttpResponse("False")
    
    try:
        staff_id = request.POST.get('id')
        message = request.POST.get('message')
        file_obj = request.FILES.get('attachment', None)
        
        result = send_notification_with_file(
            'staff', staff_id, message, file_obj
        )
        
        return HttpResponse("True" if result['success'] else "False")
    except Exception as e:
        return HttpResponse("False")


@login_required(login_url='login')
def broadcast_notification_to_all_students(request):
    """Broadcast notification to all students"""
    if request.user.user_type != 1:
        messages.error(request, "Only admin can broadcast notifications")
        return redirect('admin_home')
    
    if request.method == 'POST':
        message = request.POST.get('message')
        file_obj = request.FILES.get('attachment', None)
        
        try:
            students = Student.objects.all()
            success_count = 0
            
            for student in students:
                result = send_notification_with_file(
                    'student', student.admin_id, message, file_obj
                )
                if result['success']:
                    success_count += 1
            
            messages.success(request, f"Notification sent to {success_count} students")
            return redirect('admin_home')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('admin_home')
    
    return render(request, 'hod_template/broadcast_notification.html')


@login_required(login_url='login')
def broadcast_notification_to_all_staff(request):
    """Broadcast notification to all staff"""
    if request.user.user_type != 1:
        messages.error(request, "Only admin can broadcast notifications")
        return redirect('admin_home')
    
    if request.method == 'POST':
        message = request.POST.get('message')
        file_obj = request.FILES.get('attachment', None)
        
        try:
            staff_members = Staff.objects.all()
            success_count = 0
            
            for staff in staff_members:
                result = send_notification_with_file(
                    'staff', staff.admin_id, message, file_obj
                )
                if result['success']:
                    success_count += 1
            
            messages.success(request, f"Notification sent to {success_count} staff members")
            return redirect('admin_home')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('admin_home')
    
    return render(request, 'hod_template/broadcast_notification.html')
