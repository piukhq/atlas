from django.contrib import admin

from member.models import Member, Request, Response


@admin.register(Member)
class EnrolAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'email', 'first_name', 'last_name')
    search_fields = ('id', 'email', 'last_name')
    ordering = ('-created_date',)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'bink_message_uid',)
    search_fields = ('id', 'bink_message_uid')
    ordering = ('-created_date',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('id', 'timestamp', 'status_code')
    search_fields = ('id', 'timestamp', 'status_code')
    ordering = ('-created_date',)
