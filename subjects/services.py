from core.services import BaseService
from .models import Subject

class SubjectService(BaseService):
    model = Subject

    @classmethod
    def get_by_department(cls, department_id):
        return cls.model.objects.filter(department_id=department_id)

    @classmethod
    def get_exams(cls, subject_id):
        subject = cls.get_by_id(subject_id)
        return subject.exams.all().order_by('-date')

    @classmethod
    def assign_teacher(cls, subject_id, teacher):
        subject = cls.get_by_id(subject_id)
        subject.teachers.add(teacher)
        return subject

    @classmethod
    def assign_teachers_bulk(cls, subject_id, teachers):
        subject = cls.get_by_id(subject_id)
        subject.teachers.set(teachers)
        return subject

    @classmethod
    def remove_teacher(cls, subject_id, teacher):
        subject = cls.get_by_id(subject_id)
        subject.teachers.remove(teacher)
        return subject
