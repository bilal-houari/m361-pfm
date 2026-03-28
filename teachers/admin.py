from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_teacher_name', 'specialization', 'joining_date')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')

    def get_teacher_name(self, obj):
        return obj.user.get_full_name()
    get_teacher_name.short_description = 'Name'
