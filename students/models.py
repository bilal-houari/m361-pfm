from django.db import models
from django.conf import settings
from datetime import datetime
import random
import string

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField()
    school_class = models.ForeignKey('classes.SchoolClass', on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_date = models.DateField(auto_now_add=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"

    def save(self, *args, **kwargs):
        if not self.admission_number:
            year = datetime.now().year
            random_suffix = ''.join(random.choices(string.digits, k=3))
            self.admission_number = f"ADM-{year}-{random_suffix}"
            
            while Student.objects.filter(admission_number=self.admission_number).exists():
                random_suffix = ''.join(random.choices(string.digits, k=3))
                self.admission_number = f"ADM-{year}-{random_suffix}"
        
        super().save(*args, **kwargs)
