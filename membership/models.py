from django.db import models


class MembershipRequest(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    email = models.CharField(max_length=250, db_index=True, blank=True)
    title = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True, db_index=True)
    date_of_birth = models.DateField(null=True, blank=True)
    postcode = models.CharField(max_length=250, blank=True)
    address_1 = models.CharField(max_length=250, blank=True)
    address_2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    county = models.CharField(max_length=250, blank=True)
    country = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=250, blank=True)
    password = models.CharField(max_length=500, blank=True)
    card_number = models.CharField(max_length=250, blank=True)
    membership_plan_slug = models.CharField(max_length=64, db_index=True, blank=True)
    message_uid = models.UUIDField(blank=True, unique=True)
    record_uid = models.CharField(max_length=100, blank=True)
    callback_url = models.URLField(max_length=200, blank=True, null=True)
    handler_type = models.CharField(max_length=32, blank=True)
    timestamp = models.DateTimeField(blank=True)
    integration_service = models.CharField(max_length=32, blank=True)
    channel = models.CharField(max_length=100, blank=True)
    payload = models.JSONField(blank=True)
    request_url = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return self.id


class MembershipResponse(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    request = models.ForeignKey(MembershipRequest, on_delete=models.CASCADE, related_name="responses")
    response_body = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)
    status_code = models.IntegerField(blank=True)
