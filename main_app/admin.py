from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ('college_name', 'admin_email', 'support_email', 'enable_email_notifications')
    fields = ('admin_email', 'admin_phone', 'admin_office_address', 'college_name', 
              'college_website', 'support_email', 'enable_email_notifications')
    readonly_fields = ('created_at', 'updated_at')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'attachment_type', 'created_at', 'file_size')
    list_filter = ('attachment_type', 'created_at')
    search_fields = ('title', 'description', 'uploaded_by__email')
    readonly_fields = ('file_size', 'created_at', 'updated_at')


class NotificationStaffAdmin(admin.ModelAdmin):
    list_display = ('staff', 'created_at', 'has_attachment')
    list_filter = ('created_at',)
    search_fields = ('staff__admin__email', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = 'Has Attachment'


class NotificationStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'created_at', 'has_attachment')
    list_filter = ('created_at',)
    search_fields = ('student__admin__email', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = 'Has Attachment'


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Book)
admin.site.register(IssuedBook)
admin.site.register(Library)
admin.site.register(Subject)
admin.site.register(Session)
admin.site.register(AdminSettings, AdminSettingsAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(NotificationStaff, NotificationStaffAdmin)
admin.site.register(NotificationStudent, NotificationStudentAdmin)
