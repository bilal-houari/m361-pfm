from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'get_student_name', 'grade', 'enrollment_date')
    search_fields = ('admission_number', 'user__first_name', 'user__last_name')

    def get_student_name(self, obj):
        return obj.user.get_full_name()
    get_student_name.short_description = 'Name'
