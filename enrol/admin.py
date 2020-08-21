from django.contrib import admin

from enrol.models import EnrolRequest


@admin.register(EnrolRequest)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'email', 'first_name', 'last_name', 'bink_message_uid', 'status_code')
    search_fields = ('id', 'email', 'bink_message_uid')
    ordering = ('-created_date',)
