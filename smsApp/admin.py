from django.contrib import admin
from .models import SMSStatistic

class SMSStatisticAdmin(admin.ModelAdmin):
    list_display = ('filed_count', 'success_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('filed_count', 'success_count')

admin.site.register(SMSStatistic, SMSStatisticAdmin)
