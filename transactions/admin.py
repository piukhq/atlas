from django.contrib import admin

from transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)
    list_display = ('transaction_id', 'scheme_provider', 'status', 'transaction_date', 'user_id', 'amount')
    search_fields = ('transaction_id', 'scheme_provider', 'status', 'transaction_date', 'user_id', 'amount')
    list_filter = ('status', 'scheme_provider')
    ordering = ('-created_date',)


admin.site.register(Transaction, TransactionAdmin)
