from django import forms
from .models import ClassSubjectAssignment
from teachers.models import Teacher

class ClassSubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassSubjectAssignment
        fields = ['teacher']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = Teacher.objects.select_related('user', 'subject')
        # Customize the teacher labels to show Subject
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} ({obj.subject.name if obj.subject else 'No Subject'})"
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'
