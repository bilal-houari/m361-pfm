from django import forms
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()

class TeacherForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to use email as password")

    class Meta:
        model = Teacher
        fields = ['date_of_birth', 'specialization', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['password'].widget = forms.HiddenInput() # Don't change password here for simplicity

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
            teacher = super().save(commit=commit)
        else:
            user = User.objects.create_user(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                role='TEACHER'
            )
            teacher = super().save(commit=False)
            teacher.user = user
            if commit:
                teacher.save()
        return teacher
