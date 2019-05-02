from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from .models import Dayoff
admin.site.register(Permission)

class DayoffAdmin(admin.ModelAdmin):
    list_display = ['create_by', 'reason', 'date_start', 'end_date', 'approve_status']
    list_filter = ['create_by', 'reason', 'date_start', 'end_date', 'approve_status']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('type','create_by', 'reason', 'date_start', 'end_date')
        return self.readonly_fields

    # readonly_fields = ['create_by', 'reason', 'date_start', 'end_date']
    # fields = ['approve_status']
admin.site.register(Dayoff, DayoffAdmin)
