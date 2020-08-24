from django.contrib import admin

from membership.models import MembershipRequest


@admin.register(MembershipRequest)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'email', 'first_name', 'last_name', 'bink_message_uid', 'status_code')
    search_fields = ('id', 'email', 'bink_message_uid')
    ordering = ('-created_date',)
