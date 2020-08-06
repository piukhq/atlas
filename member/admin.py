from django.contrib import admin

from member.models import Enrol


@admin.register(Enrol)
class EnrolAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'email', 'first_name', 'last_name', 'membership_plan', 'channel')
    search_fields = ('id', 'email', 'last_name', 'membership_plan', 'channel')
    list_filter = ('channel', 'http_response_code')
    ordering = ('-created_date',)
