from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Avg
from django.utils import timezone
from core.mixins import AdminRequiredMixin, StudentRequiredMixin
from exams.models import Exam, ExamResult
from holidays.models import Holiday
from .models import Student
from .forms import StudentForm

# Admin Views
class StudentListView(AdminRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

class StudentCreateView(AdminRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(AdminRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(AdminRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')

# Student Specific Views
class StudentDashboardView(StudentRequiredMixin, TemplateView):
    template_name = 'students/student_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student_profile
        
        # Latest 3 results
        results = ExamResult.objects.filter(student=student).order_by('-exam__date')
        context['recent_results'] = results[:3]
        
        # Overall Average
        context['overall_avg'] = results.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0
        
        # Upcoming Exam
        context['upcoming_exam'] = Exam.objects.filter(date__gte=timezone.now().date()).order_by('date').first()
        
        # Next Holiday
        context['next_holiday'] = Holiday.objects.filter(start_date__gte=timezone.now().date()).order_by('start_date').first()
        
        context['student'] = student
        return context

class StudentExamResultsView(StudentRequiredMixin, ListView):
    model = ExamResult
    template_name = 'students/student_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        return ExamResult.objects.filter(student=self.request.user.student_profile).order_by('-exam__date')

class StudentHolidayListView(StudentRequiredMixin, ListView):
    model = Holiday
    template_name = 'students/student_holidays.html'
    context_object_name = 'holidays'

    def get_queryset(self):
        return Holiday.objects.filter(start_date__gte=timezone.now().date()).order_by('start_date')
