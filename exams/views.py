from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from core.mixins import AdminRequiredMixin, TeacherRequiredMixin, TeacherOnlyRequiredMixin
from .models import Exam, ExamResult
from .forms import TeacherExamForm
from students.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin

class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'STUDENT':
            student = getattr(self.request.user, 'student_profile', None)
            if student and student.school_class:
                return queryset.filter(school_class=student.school_class).order_by('-date')
            return queryset.none()
        elif self.request.user.role == 'TEACHER':
            teacher = getattr(self.request.user, 'teacher_profile', None)
            if teacher:
                return queryset.filter(subject=teacher.subject).order_by('-date')
            return queryset.none()
        return queryset.order_by('-date')

class ExamCreateView(TeacherOnlyRequiredMixin, CreateView):
    model = Exam
    form_class = TeacherExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exam-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.role == 'TEACHER':
            kwargs['teacher'] = self.request.user.teacher_profile
        return kwargs

    def form_valid(self, form):
        # Auto-assign teacher's subject
        if self.request.user.role == 'TEACHER':
            form.instance.subject = self.request.user.teacher_profile.subject
        return super().form_valid(form)

class ExamUpdateView(TeacherOnlyRequiredMixin, UpdateView):
    model = Exam
    form_class = TeacherExamForm
    template_name = 'exams/exam_form.html'
    success_url = reverse_lazy('exam-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.role == 'TEACHER':
            kwargs['teacher'] = self.request.user.teacher_profile
        return kwargs

class ExamDeleteView(TeacherOnlyRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/exam_confirm_delete.html'
    success_url = reverse_lazy('exam-list')

class ExamResultEntryView(TeacherOnlyRequiredMixin, TemplateView):
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
        # Admins should not be able to save marks (as per previous request, only academics)
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
