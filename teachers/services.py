from django.db import transaction
from core.services import BaseService
from .models import Teacher
from users.services import UserService

class TeacherService(BaseService):
    model = Teacher

    @classmethod
    def get_subjects(cls, teacher_id):
        teacher = cls.get_by_id(teacher_id)
        return teacher.subjects.all().select_related('department')

    @classmethod
    def get_teaching_load(cls, teacher_id):
        teacher = cls.get_by_id(teacher_id)
        subjects = teacher.subjects.all()
        return {
            'subjects_count': subjects.count(),
            'departments': subjects.values_list('department__name', flat=True).distinct()
        }

    @classmethod
    @transaction.atomic
    def create_teacher(cls, user_data, teacher_data):
        # 1. Create User via UserService
        user = UserService.create_user(
            username=user_data.get('username'),
            password=user_data.get('password'),
            email=user_data.get('email'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role='TEACHER'
        )
        # 2. Create Teacher Profile
        teacher = cls.create(user=user, **teacher_data)
        return teacher

    @classmethod
    @transaction.atomic
    def update_teacher(cls, teacher_id, user_data=None, teacher_data=None):
        teacher = cls.get_by_id(teacher_id)
        if user_data:
            user = teacher.user
            for field, value in user_data.items():
                setattr(user, field, value)
            user.save()
        if teacher_data:
            for field, value in teacher_data.items():
                setattr(teacher, field, value)
            teacher.save()
        return teacher

    @classmethod
    @transaction.atomic
    def delete_teacher(cls, teacher_id):
        teacher = cls.get_by_id(teacher_id)
        user = teacher.user
        teacher.delete()
        user.delete()
        return True
        