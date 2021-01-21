from django.db import models


class Transaction(models.Model):
    """
    Transaction export status
    """
    created_date = models.DateTimeField(auto_now_add=True, db_index=True, blank=False)
    scheme_provider = models.CharField(max_length=100, db_index=True)
    response = models.CharField(max_length=3000, blank=True)
    transaction_id = models.CharField(max_length=100, db_index=True, unique=True)
    status = models.CharField(max_length=50, db_index=True)
    transaction_date = models.DateTimeField(blank=True)
    user_id = models.CharField(max_length=30, blank=True)
    amount = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.created_date


class TransactionRequest(models.Model):
    """
    Transaction request for audit
    """
    created_date = models.DateTimeField(auto_now_add=True)
    customer_number = models.CharField(max_length=250, blank=True, db_index=True)
    transaction_id = models.CharField(max_length=100, db_index=True, unique=True)
    request_timestamp = models.DateTimeField(db_index=True, blank=True)
    membership_plan = models.CharField(max_length=64, db_index=True, blank=True)
    message_uid = models.CharField(max_length=250, blank=True, null=True)
    record_uid = models.CharField(max_length=100, blank=True, null=True)
    request = models.JSONField(blank=True)
    status_code = models.IntegerField(blank=True)
    response = models.JSONField(blank=True)
    response_timestamp = models.DateTimeField(db_index=True, blank=True)

    def __unicode__(self):
        return self.transaction_id


class AuditData(models.Model):
    """
    Audit data for an export received from the transaction matching engine
    e.g. scheme, transactions, requests, responses, file location, in JSON format
    """
    audit_data = models.JSONField()


class ExportTransaction(models.Model):
    """
    Transaction export audit
    """
    transaction_id = models.CharField(max_length=100, db_index=True)
    user_id = models.CharField(max_length=30, blank=True)
    spend_amount = models.IntegerField(blank=True, help_text="Spend amount (pennies)")
    transaction_date = models.DateTimeField(blank=True, db_index=True)
    loyalty_identifier = models.CharField(max_length=250, blank=True, db_index=True)
    record_uid = models.CharField(max_length=500, null=True, blank=True, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True, blank=False)
    provider_slug = models.CharField(max_length=100, db_index=True)
    audit_data = models.ForeignKey(AuditData, on_delete=models.CASCADE)
