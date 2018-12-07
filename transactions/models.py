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
