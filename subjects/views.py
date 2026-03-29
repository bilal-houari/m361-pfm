from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.mixins import AdminRequiredMixin
from .models import Subject

class SubjectListView(AdminRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'

class SubjectCreateView(AdminRequiredMixin, CreateView):
    model = Subject
    fields = ['name', 'code', 'department', 'teachers']
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subject-list')

class SubjectUpdateView(AdminRequiredMixin, UpdateView):
    model = Subject
    fields = ['name', 'code', 'department', 'teachers']
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subject-list')

class SubjectDeleteView(AdminRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    success_url = reverse_lazy('subject-list')
