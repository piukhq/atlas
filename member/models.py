from django.db import models


class Enrol(models.Model):
    """
    Enrol request and response
    """
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    email = models.CharField(max_length=128, db_index=True, blank=False)
    title = models.CharField(max_length=16, blank=True)
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=25, blank=True)
    request_datetime = models.DateTimeField(db_index=True, blank=True)
    membership_plan = models.CharField(max_length=64, db_index=True, blank=True)
    channel = models.CharField(max_length=32, db_index=True, blank=True)
    http_response_code = models.IntegerField(blank=True)
    response_body = models.JSONField(blank=True)
    payload = models.JSONField(blank=True)
    response_datetime = models.DateTimeField(db_index=True, blank=True)

    def __unicode__(self):
        return self.email
