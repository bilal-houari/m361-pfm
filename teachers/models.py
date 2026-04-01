from django.db import models
from django.conf import settings
import random
import string

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    staff_id = models.CharField(max_length=20, unique=True, blank=True)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.SET_NULL, null=True, related_name='teachers')
    date_of_birth = models.DateField()
    specialization = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.staff_id})"

    @property
    def department(self):
        if self.subject:
            return self.subject.department
        return None

    def save(self, *args, **kwargs):
        # Auto-generate staff_id if it doesn't exist
        if not self.staff_id:
            random_suffix = ''.join(random.choices(string.digits, k=3))
            self.staff_id = f"STAFF-{random_suffix}"
            while Teacher.objects.filter(staff_id=self.staff_id).exists():
                random_suffix = ''.join(random.choices(string.digits, k=3))
                self.staff_id = f"STAFF-{random_suffix}"
        
        # Detect if subject has changed
        if self.pk:
            old_teacher = Teacher.objects.get(pk=self.pk)
            if old_teacher.subject != self.subject:
                # Subject has changed, unassign from all classes
                from classes.models import ClassSubjectAssignment
                ClassSubjectAssignment.objects.filter(teacher=self).delete()
        
        super().save(*args, **kwargs)
