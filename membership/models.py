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

    def __unicode__(self):
        return self.id


class MembershipResponse(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    request = models.ForeignKey(MembershipRequest, on_delete=models.CASCADE, related_name="responses")
    response_body = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True)
    status_code = models.IntegerField(blank=True)


class UserChannelIdentifier(models.Model):
    user_id = models.IntegerField()
    date_joined = models.DateTimeField(help_text="User created date")
    bundle_id = models.TextField(help_text="Channel identifier")
    created_link = models.DateTimeField(null=True, help_text="Creation date of user to scheme account association")
    scheme_account_id = models.IntegerField()
    created_scheme_account = models.DateTimeField(help_text="Scheme account created date")
    join_date = models.DateTimeField(null=True, help_text="Scheme account join date (if applicable)")
    link_date = models.DateTimeField(null=True, help_text="Scheme account link date (if applicable)")
    card_number = models.TextField(blank=True, null=True)
    barcode = models.TextField(blank=True, null=True)
    alt_main_answer = models.TextField(blank=True, null=True)
    merchant_identifier = models.TextField(blank=True, null=True)
    originating_journey = models.IntegerField(help_text="Journey type ID (Join = 0, Link = 1, Add = 2, Update = 3, Register = 4, Unknown = 5)")
    scheme_id = models.IntegerField()

    def __str__(self):
        return f"UserChannelIdentifier - User {self.user_id} in channel {self.bundle_id}"
