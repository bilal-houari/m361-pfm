from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from core.mixins import AdminRequiredMixin
from .models import SchoolClass, ClassSubjectAssignment
from teachers.models import Teacher
from subjects.models import Subject

class SchoolClassListView(AdminRequiredMixin, ListView):
    model = SchoolClass
    template_name = 'classes/class_list.html'
    context_object_name = 'classes'

class SchoolClassDetailView(AdminRequiredMixin, DetailView):
    model = SchoolClass
    template_name = 'classes/class_detail.html'
    context_object_name = 'school_class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school_class = self.get_object()
        context['students'] = school_class.students.all().select_related('user')
        # Map assignments
        context['assignments'] = school_class.assignments.all().select_related('subject', 'teacher__user')
        # For the assignment form modal/section
        context['all_subjects'] = Subject.objects.all()
        context['all_teachers'] = Teacher.objects.all().select_related('user')
        return context

class SchoolClassCreateView(AdminRequiredMixin, CreateView):
    model = SchoolClass
    fields = ['name', 'grade_level'] # Removed section and class_teacher
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('class-list')

class SchoolClassUpdateView(AdminRequiredMixin, UpdateView):
    model = SchoolClass
    fields = ['name', 'grade_level']
    template_name = 'classes/class_form.html'
    success_url = reverse_lazy('class-list')

class SchoolClassDeleteView(AdminRequiredMixin, DeleteView):
    model = SchoolClass
    template_name = 'classes/class_confirm_delete.html'
    success_url = reverse_lazy('class-list')

# Assignment Management
class ClassSubjectAssignmentCreateView(AdminRequiredMixin, CreateView):
    model = ClassSubjectAssignment
    fields = ['subject', 'teacher']
    
    def form_valid(self, form):
        school_class = get_object_or_404(SchoolClass, pk=self.kwargs['class_pk'])
        subject = form.cleaned_data['subject']
        teacher = form.cleaned_data['teacher']
        
        # Validation: Teacher must teach the subject
        if teacher.subject != subject:
            from django.core.exceptions import ValidationError
            form.add_error('teacher', f"This teacher only teaches {teacher.subject.name if teacher.subject else 'nothing'}.")
            return self.form_invalid(form)

        # Handle update_or_create to enforce "one teacher per subject per class"
        ClassSubjectAssignment.objects.update_or_create(
            school_class=school_class,
            subject=subject,
            defaults={'teacher': teacher}
        )
        return redirect('class-detail', pk=school_class.pk)

class ClassSubjectAssignmentDeleteView(AdminRequiredMixin, DeleteView):
    model = ClassSubjectAssignment
    
    def get_success_url(self):
        return reverse_lazy('class-detail', kwargs={'pk': self.object.school_class.pk})
