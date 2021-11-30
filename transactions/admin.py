import json

from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from transactions.models import ExportTransaction, Transaction, TransactionRequest


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ("created_date",)
    list_display = ("transaction_id", "scheme_provider", "status", "transaction_date", "user_id", "amount")
    search_fields = ("transaction_id", "scheme_provider", "status", "transaction_date", "user_id", "amount")
    list_filter = ("status", "scheme_provider")
    ordering = ("-created_date",)


@admin.register(TransactionRequest)
class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = (
        "customer_number",
        "transaction_id",
        "request_timestamp",
        "message_uid",
        "status_code",
        "record_uid",
    )
    search_fields = (
        "customer_number",
        "transaction_id",
        "request_timestamp",
        "message_uid",
        "record_uid",
        "status_code",
        "membership_plan",
        "response",
    )
    list_filter = (("request_timestamp", DateRangeFilter), "membership_plan", "status_code")
    ordering = ("-created_date",)


@admin.register(ExportTransaction)
class ExportTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user_id",
        "spend_amount",
        "transaction_date",
        "loyalty_identifier",
        "record_uid",
        "created_date",
        "provider_slug",
    )
    search_fields = ("transaction_id", "user_id", "loyalty_identifier", "record_uid", "audit_data__audit_data")
    fields = list_display + ("audit_data_json",)
    readonly_fields = list_display + ("audit_data_json",)
    list_filter = (("transaction_date", DateRangeFilter), "provider_slug")
    ordering = ("-created_date",)

    def audit_data_json(self, obj):
        return json.dumps(obj.audit_data.audit_data, sort_keys=True, indent=4)
