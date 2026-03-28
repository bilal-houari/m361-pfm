from django.contrib import admin
from .models import AdminProfile

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('get_admin_name', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'phone_number')

    def get_admin_name(self, obj):
        return obj.user.get_full_name()
    get_admin_name.short_description = 'Name'
