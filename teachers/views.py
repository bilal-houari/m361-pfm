from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from core.mixins import AdminRequiredMixin, TeacherRequiredMixin
from .models import Teacher
from .forms import TeacherForm
from classes.models import ClassSubjectAssignment, SchoolClass
from students.models import Student

# Admin-only Views
class TeacherListView(AdminRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'

class TeacherCreateView(AdminRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher-list')

class TeacherUpdateView(AdminRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teacher-list')

class TeacherDeleteView(AdminRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher-list')

# Teacher-specific Views
class TeacherDashboardView(TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user.teacher_profile
        assignments = ClassSubjectAssignment.objects.filter(teacher=teacher)
        
        context['teacher'] = teacher
        context['assignments'] = assignments
        context['class_count'] = assignments.values('school_class').distinct().count()
        
        # Count total students across all assigned classes
        assigned_class_ids = assignments.values_list('school_class_id', flat=True)
        context['student_count'] = Student.objects.filter(school_class_id__in=assigned_class_ids).count()
        
        context['department'] = teacher.department
        return context

class TeacherClassListView(TeacherRequiredMixin, ListView):
    template_name = 'teachers/teacher_class_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        return ClassSubjectAssignment.objects.filter(teacher=self.request.user.teacher_profile).select_related('school_class', 'subject')

class TeacherClassDetailView(TeacherRequiredMixin, DetailView):
    model = SchoolClass
    template_name = 'teachers/teacher_class_detail.html'
    context_object_name = 'school_class'

    def get_object(self, queryset=None):
        # Security: Ensure teacher is actually assigned to this class
        obj = super().get_object(queryset)
        if not ClassSubjectAssignment.objects.filter(teacher=self.request.user.teacher_profile, school_class=obj).exists():
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You are not assigned to this class.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = self.object.students.all().select_related('user')
        # Find which subject the teacher teaches in this class
        assignment = ClassSubjectAssignment.objects.get(teacher=self.request.user.teacher_profile, school_class=self.object)
        context['subject'] = assignment.subject
        return context

class TeacherDepartmentView(TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_department.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.request.user.teacher_profile
        department = teacher.department
        
        context['department'] = department
        context['colleagues'] = Teacher.objects.filter(subject__department=department).exclude(id=teacher.id).select_related('user', 'subject')
        return context
