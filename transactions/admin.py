from django.contrib import admin
from transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date',)


admin.site.register(Transaction, TransactionAdmin)
