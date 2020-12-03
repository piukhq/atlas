from django.contrib import admin

from transactions.models import Transaction, TransactionRequest


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('transaction_id', 'scheme_provider', 'status', 'transaction_date', 'user_id', 'amount')
    search_fields = ('transaction_id', 'scheme_provider', 'status', 'transaction_date', 'user_id', 'amount')
    list_filter = ('status', 'scheme_provider')
    ordering = ('-created_date',)


@admin.register(TransactionRequest)
class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = (
        'customer_number',
        'transaction_id',
        'request_timestamp',
        'message_uid',
        'status_code',
        'record_uid'
    )
    search_fields = (
        'customer_number',
        'transaction_id',
        'request_timestamp',
        'message_uid',
        'record_uid',
        'status_code',
        'membership_plan',
        'response'
    )
    list_filter = ('membership_plan', 'status_code')
    ordering = ('-created_date',)
