from django.db import transaction
from core.services import BaseService
from .models import Student
from users.services import UserService

class StudentService(BaseService):
    model = Student

    @classmethod
    def get_by_grade(cls, grade):
        return cls.model.objects.filter(grade=grade).select_related('user')

    @classmethod
    def get_academic_history(cls, student_id):
        from exams.services import ExamResultService
        return ExamResultService.get_student_report_card(student_id)

    @classmethod
    @transaction.atomic
    def create_student(cls, user_data, student_data):
        # 1. Create User via UserService
        user = UserService.create_user(
            username=user_data.get('username'),
            password=user_data.get('password'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role='STUDENT'
        )
        # 2. Create Student Profile
        student = cls.create(user=user, **student_data)
        return student

    @classmethod
    @transaction.atomic
    def update_student(cls, student_id, user_data=None, student_data=None):
        student = cls.get_by_id(student_id)
        if user_data:
            user = student.user
            for field, value in user_data.items():
                setattr(user, field, value)
            user.save()
        if student_data:
            for field, value in student_data.items():
                setattr(student, field, value)
            student.save()
        return student

    @classmethod
    @transaction.atomic
    def delete_student(cls, student_id):
        student = cls.get_by_id(student_id)
        user = student.user
        student.delete()
        user.delete()
        return True
