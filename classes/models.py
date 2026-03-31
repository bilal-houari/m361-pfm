from django.db import models
from teachers.models import Teacher
from subjects.models import Subject

class SchoolClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    grade_level = models.IntegerField() # 1-12
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['grade_level', 'name']

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()

class ClassSubjectAssignment(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_assignments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school_class', 'subject')
        verbose_name = "Class Subject Assignment"
        verbose_name_plural = "Class Subject Assignments"

    def __str__(self):
        return f"{self.school_class.name} - {self.subject.name} ({self.teacher.user.get_full_name()})"
