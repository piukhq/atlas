# Generated by Django 3.1 on 2020-09-08 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transactionrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionrequest',
            name='message_uid',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
