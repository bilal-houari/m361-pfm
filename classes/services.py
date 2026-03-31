from core.services import BaseService
from .models import SchoolClass, ClassSubjectAssignment

class SchoolClassService(BaseService):
    model = SchoolClass

    @classmethod
    def get_all_with_counts(cls):
        return cls.model.objects.prefetch_related('students', 'assignments__teacher__user', 'assignments__subject')

    @classmethod
    def get_by_grade_level(cls, level):
        return cls.model.objects.filter(grade_level=level)

    @classmethod
    def assign_student(cls, class_id, student):
        school_class = cls.get_by_id(class_id)
        student.school_class = school_class
        student.save()
        return school_class

    @classmethod
    def create_assignment(cls, class_id, subject_id, teacher_id):
        return ClassSubjectAssignment.objects.update_or_create(
            school_class_id=class_id,
            subject_id=subject_id,
            defaults={'teacher_id': teacher_id}
        )

    @classmethod
    def delete_assignment(cls, assignment_id):
        return ClassSubjectAssignment.objects.filter(id=assignment_id).delete()
