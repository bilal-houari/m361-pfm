from core.services import BaseService
from .models import Department

class DepartmentService(BaseService):
    model = Department

    @classmethod
    def get_teachers(cls, department_id):
        department = cls.get_by_id(department_id)
        # Teachers who teaching subjects in this department
        return department.subjects.values_list('teachers', flat=True).distinct()

    @classmethod
    def get_summary(cls, department_id):
        department = cls.get_by_id(department_id)
        return {
            'name': department.name,
            'subjects_count': department.subjects.count(),
            'teachers_count': department.subjects.values('teachers').distinct().count()
        }
