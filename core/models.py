from django.db import models
from django.contrib.auth.models import User


# ==============================
# STUDY TASK
# ==============================
class StudyTask(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    deadline = models.DateField()

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


# ==============================
# ACTIVITY LOG
# ==============================
class ActivityLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    action = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.timestamp.strftime('%H:%M %d-%m-%Y')})"


# ==============================
# LOGIN ATTEMPT (IDS)
# ==============================
class LoginAttempt(models.Model):

    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    success = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.username} - {status} ({self.ip_address}) [{self.timestamp.strftime('%H:%M %d-%m-%Y')}]"