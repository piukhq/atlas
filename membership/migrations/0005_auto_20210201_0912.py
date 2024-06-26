# Generated by Django 3.1.4 on 2021-02-01 09:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("membership", "0004_membershiprequest_date_of_birth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="membershiprequest",
            name="callback_url",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="membershiprequest",
            name="email",
            field=models.CharField(blank=True, db_index=True, max_length=250),
        ),
    ]
