# Generated by Django 2.1.4 on 2019-02-13 16:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ubiquity_users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="opt_out_timestamp",
            new_name="ubiquity_join_date",
        ),
    ]
