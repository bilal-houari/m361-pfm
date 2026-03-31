from django.contrib import admin
from .models import Exam, ExamResult

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'school_class', 'date', 'max_marks')
    list_filter = ('subject', 'school_class', 'date')
    search_fields = ('name',)

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'get_exam_name', 'marks_obtained')
    list_filter = ('exam', 'student__school_class')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'exam__name')
    readonly_fields = ('marks_obtained',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_exam_name(self, obj):
        return obj.exam.name
    get_exam_name.short_description = 'Exam'
