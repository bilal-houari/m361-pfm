from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.mixins import AdminRequiredMixin
from .models import Department

class DepartmentListView(AdminRequiredMixin, ListView):
    model = Department
    template_name = 'departments/department_list.html'
    context_object_name = 'departments'

class DepartmentCreateView(AdminRequiredMixin, CreateView):
    model = Department
    fields = ['name', 'description']
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department-list')

class DepartmentUpdateView(AdminRequiredMixin, UpdateView):
    model = Department
    fields = ['name', 'description']
    template_name = 'departments/department_form.html'
    success_url = reverse_lazy('department-list')

class DepartmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('department-list')
