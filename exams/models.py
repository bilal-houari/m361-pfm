from django.db import models
from subjects.models import Subject
from students.models import Student

class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    max_marks = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.name} - {self.subject.name}"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.name}: {self.marks_obtained}"

    @property
    def percentage(self):
        if self.exam.max_marks > 0:
            return (self.marks_obtained / self.exam.max_marks) * 100
        return 0
