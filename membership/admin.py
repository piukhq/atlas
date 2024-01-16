from django.contrib import admin

from membership.models import MembershipRequest, MembershipResponse, UserChannelIdentifier


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


@admin.register(UserChannelIdentifier)
class UserChannelIdentifierAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "bundle_id", "scheme_account_id", "scheme_id")
    readonly_fields = [field.name for field in UserChannelIdentifier._meta.get_fields()]
    search_fields = ("user_id", "scheme_account_id")
    list_filter = ("bundle_id",)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
