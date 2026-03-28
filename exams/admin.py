from django.contrib import admin
from .models import Exam, ExamResult

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date', 'max_marks')
    list_filter = ('subject', 'date')
    search_fields = ('name',)

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained')
    list_filter = ('exam', 'student__grade')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'exam__name')
