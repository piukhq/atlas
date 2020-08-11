# Generated by Django 3.1 on 2020-08-11 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('email', models.CharField(db_index=True, max_length=128)),
                ('title', models.CharField(blank=True, max_length=16)),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, db_index=True, max_length=64)),
                ('postcode', models.CharField(blank=True, max_length=10)),
                ('address_1', models.CharField(blank=True, max_length=100)),
                ('address_2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('county', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=25)),
                ('password', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('membership_plan', models.CharField(blank=True, db_index=True, max_length=64)),
                ('bink_message_uid', models.UUIDField(blank=True, db_index=True)),
                ('bink_record_uid', models.CharField(blank=True, max_length=100)),
                ('callback_url', models.URLField(blank=True)),
                ('handler_type', models.CharField(blank=True, max_length=32)),
                ('payload', models.JSONField(blank=True)),
                ('timestamp', models.DateTimeField(blank=True)),
                ('integration_service', models.CharField(blank=True, max_length=32)),
                ('channel', models.CharField(blank=True, max_length=100)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='member.member')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('response_body', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(blank=True)),
                ('status_code', models.IntegerField(blank=True)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='member.request')),
            ],
        ),
    ]
