from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()

class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to use email as password")

    class Meta:
        model = Student
        fields = ['date_of_birth', 'school_class', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['email', 'first_name', 'last_name', 'password']:
                field.widget.attrs['class'] = 'form-input'
        
        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['password'].widget = forms.HiddenInput()

    @transaction.atomic
    def save(self, commit=True):
        email = self.cleaned_data.get('email')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password') or email

        if self.instance.pk:
            user = self.instance.user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            student = super().save(commit=commit)
        else:
            user = User.objects.create_user(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role='STUDENT'
            )
            student = super().save(commit=False)
            student.user = user
            if commit:
                student.save()
        return student
