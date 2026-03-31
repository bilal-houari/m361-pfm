from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, related_name='teachers', null=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.SET_NULL, null=True, related_name='teachers')
    date_of_birth = models.DateField()
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialization})"
