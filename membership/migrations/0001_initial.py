# Generated by Django 3.1 on 2020-08-24 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MembershipRequest",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("email", models.CharField(db_index=True, max_length=250)),
                ("title", models.CharField(blank=True, max_length=250)),
                ("first_name", models.CharField(blank=True, max_length=250)),
                ("last_name", models.CharField(blank=True, db_index=True, max_length=250)),
                ("postcode", models.CharField(blank=True, max_length=250)),
                ("address_1", models.CharField(blank=True, max_length=250)),
                ("address_2", models.CharField(blank=True, max_length=250)),
                ("city", models.CharField(blank=True, max_length=250)),
                ("county", models.CharField(blank=True, max_length=250)),
                ("country", models.CharField(blank=True, max_length=250)),
                ("phone_number", models.CharField(blank=True, max_length=250)),
                ("password", models.CharField(blank=True, max_length=500)),
                ("card_number", models.CharField(blank=True, max_length=250)),
                ("membership_plan_slug", models.CharField(blank=True, db_index=True, max_length=64)),
                ("bink_message_uid", models.UUIDField(blank=True, db_index=True)),
                ("bink_record_uid", models.CharField(blank=True, max_length=100)),
                ("callback_url", models.URLField(blank=True)),
                ("handler_type", models.CharField(blank=True, max_length=32)),
                ("request_timestamp", models.DateTimeField(blank=True)),
                ("integration_service", models.CharField(blank=True, max_length=32)),
                ("channel", models.CharField(blank=True, max_length=100)),
                ("payload", models.JSONField(blank=True)),
                ("response_body", models.TextField(blank=True, null=True)),
                ("response_timestamp", models.DateTimeField(blank=True, null=True)),
                ("status_code", models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
