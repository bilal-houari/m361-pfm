from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from core.mixins import AdminRequiredMixin
from .models import Exam, ExamResult
from students.models import Student

class ExamListView(AdminRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

class ExamCreateView(AdminRequiredMixin, CreateView):
    model = Exam
    fields = ['name', 'date', 'subject', 'max_marks']
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exam-list')

class ExamUpdateView(AdminRequiredMixin, UpdateView):
    model = Exam
    fields = ['name', 'date', 'subject', 'max_marks']
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exam-list')

class ExamDeleteView(AdminRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/exam_confirm_delete.html'
    success_url = reverse_lazy('exam-list')

class ExamResultEntryView(AdminRequiredMixin, TemplateView):
    template_name = 'exams/exam_result_entry.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = get_object_or_404(Exam, pk=self.kwargs['pk'])
        context['exam'] = exam
        # Get existing results for this exam
        results = {r.student_id: r.marks_obtained for r in ExamResult.objects.filter(exam=exam)}
        # Only get students belonging to the class concerned by the exam
        students = Student.objects.filter(school_class=exam.school_class).select_related('user')
        
        student_list = []
        for student in students:
            student_list.append({
                'id': student.id,
                'name': student.user.get_full_name(),
                'adm_no': student.admission_number,
                'marks': results.get(student.id, '')
            })
        context['students'] = student_list
        return context

    def post(self, request, *args, **kwargs):
        # Admins should not be able to save marks
        if request.user.role == 'ADMIN':
            return redirect('exam-list')
            
        exam = get_object_or_404(Exam, pk=self.kwargs['pk'])
        for key, value in request.POST.items():
            if key.startswith('marks_'):
                student_id = key.split('_')[1]
                if value: # Only save if value is provided
                    ExamResult.objects.update_or_create(
                        exam=exam,
                        student_id=student_id,
                        defaults={'marks_obtained': value}
                    )
        return redirect('exam-list')
