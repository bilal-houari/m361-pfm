from core.services import BaseService
from .models import Exam, ExamResult

class ExamService(BaseService):
    model = Exam

    @classmethod
    def get_by_subject(cls, subject_id):
        return cls.model.objects.filter(subject_id=subject_id).order_by('-date')

    @classmethod
    def get_upcoming_exams(cls, limit=5):
        from django.utils import timezone
        return cls.model.objects.filter(date__gte=timezone.now().date()).order_by('date')[:limit]

class ExamResultService(BaseService):
    model = ExamResult

    @classmethod
    def get_by_exam(cls, exam_id):
        return cls.model.objects.filter(exam_id=exam_id).select_related('student__user')

    @classmethod
    def get_by_student(cls, student_id):
        return cls.model.objects.filter(student_id=student_id).select_related('exam__subject')

    @classmethod
    def get_student_report_card(cls, student_id):
        results = cls.get_by_student(student_id)
        if not results:
            return None
        
        total_marks = sum(r.marks_obtained for r in results)
        max_possible = sum(r.exam.max_marks for r in results)
        percentage = (total_marks / max_possible * 100) if max_possible > 0 else 0
        
        return {
            'results': results,
            'total_marks': total_marks,
            'max_possible': max_possible,
            'percentage': round(percentage, 2)
        }

    @classmethod
    def record_result(cls, exam, student, marks_obtained):
        result, created = ExamResult.objects.update_or_create(
            exam=exam,
            student=student,
            defaults={'marks_obtained': marks_obtained}
        )
        return result

    @classmethod
    @transaction.atomic
    def record_bulk_results(cls, exam_id, results_data):
        """
        results_data: list of dicts [{'student_id': 1, 'marks': 85}, ...]
        """
        exam = Exam.objects.get(id=exam_id)
        created_results = []
        for item in results_data:
            from students.models import Student
            student = Student.objects.get(id=item['student_id'])
            res = cls.record_result(exam, student, item['marks'])
            created_results.append(res)
        return created_results
