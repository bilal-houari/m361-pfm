from django import forms
from .models import Exam
from classes.models import ClassSubjectAssignment, SchoolClass

class TeacherExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'date', 'school_class', 'max_marks']

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if field_name == 'date':
                field.widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-input'})
        
        if teacher:
            # Teacher can only create exams for classes they are assigned to
            assignments = ClassSubjectAssignment.objects.filter(teacher=teacher)
            class_ids = assignments.values_list('school_class_id', flat=True)
            self.fields['school_class'].queryset = SchoolClass.objects.filter(id__in=class_ids)
