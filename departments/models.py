from django.db import models
from teachers.models import Teacher

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='led_departments')

    def __str__(self):
        return f"{self.name}"
