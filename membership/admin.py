from django.contrib import admin

from membership.models import MembershipRequest, MembershipResponse


class ResponseAdminInline(admin.TabularInline):
    model = MembershipResponse
    extra = 0


@admin.register(MembershipRequest)
class RequestAdmin(admin.ModelAdmin):
    inlines = (ResponseAdminInline,)
    readonly_fields = ("created_date",)
    list_display = ("id", "email", "first_name", "last_name", "card_number", "message_uid")
    search_fields = (
        "id",
        "email",
        "last_name",
        "card_number",
        "timestamp",
        "message_uid",
        "record_uid",
        "membership_plan_slug",
        "channel",
    )
    ordering = ("-created_date",)


@admin.register(MembershipResponse)
class ResponseAdmin(admin.ModelAdmin):
    readonly_fields = ("created_date",)
    list_display = ("id", "timestamp", "status_code")
    search_fields = (
        "id",
        "timestamp",
        "status_code",
        "request__message_uid",
        "request__record_uid",
        "request__membership_plan_slug",
        "request__channel",
        "request__card_number",
    )
    ordering = ("-created_date",)
