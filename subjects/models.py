from django.db import models
from departments.models import Department
import random
import string

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate a unique code: DEPT-RANDOM
            dept_prefix = self.department.name[:3].upper()
            random_suffix = ''.join(random.choices(string.digits, k=3))
            self.code = f"{dept_prefix}-{random_suffix}"
            
            # Ensure uniqueness
            while Subject.objects.filter(code=self.code).exists():
                random_suffix = ''.join(random.choices(string.digits, k=3))
                self.code = f"{dept_prefix}-{random_suffix}"
                
        super().save(*args, **kwargs)
