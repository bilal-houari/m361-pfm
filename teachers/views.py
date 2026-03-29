from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.mixins import AdminRequiredMixin
from .models import Teacher
from .forms import TeacherForm

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
