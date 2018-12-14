# Generated by Django 2.1.4 on 2018-12-11 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('scheme_provider', models.CharField(db_index=True, max_length=100)),
                ('response', models.CharField(blank=True, max_length=3000)),
                ('transaction_id', models.CharField(db_index=True, max_length=100, unique=True)),
                ('status', models.CharField(db_index=True, max_length=50)),
                ('transaction_date', models.DateTimeField(blank=True)),
                ('user_id', models.CharField(blank=True, max_length=30)),
                ('amount', models.IntegerField(blank=True)),
            ],
        ),
    ]
