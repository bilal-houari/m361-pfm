from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.mixins import AdminRequiredMixin
from .models import Holiday

class HolidayListView(AdminRequiredMixin, ListView):
    model = Holiday
    template_name = 'holidays/holiday_list.html'
    context_object_name = 'holidays'

class HolidayCreateView(AdminRequiredMixin, CreateView):
    model = Holiday
    fields = ['name', 'start_date', 'end_date', 'description']
    template_name = 'holidays/holiday_form.html'
    success_url = reverse_lazy('holiday-list')

class HolidayUpdateView(AdminRequiredMixin, UpdateView):
    model = Holiday
    fields = ['name', 'start_date', 'end_date', 'description']
    template_name = 'holidays/holiday_form.html'
    success_url = reverse_lazy('holiday-list')

class HolidayDeleteView(AdminRequiredMixin, DeleteView):
    model = Holiday
    template_name = 'holidays/holiday_confirm_delete.html'
    success_url = reverse_lazy('holiday-list')
