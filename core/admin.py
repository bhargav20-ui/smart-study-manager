from django.contrib import admin
from .models import StudyTask, ActivityLog, LoginAttempt


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'action')


class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'success', 'timestamp')
    list_filter = ('success', 'timestamp')
    search_fields = ('username', 'ip_address')


admin.site.register(StudyTask)
admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(LoginAttempt, LoginAttemptAdmin)