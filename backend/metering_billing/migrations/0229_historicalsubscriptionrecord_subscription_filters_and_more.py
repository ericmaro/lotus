# Generated by Django 4.0.5 on 2023-03-18 21:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metering_billing', '0228_auto_20230315_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalsubscriptionrecord',
            name='subscription_filters',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=2), default=list, size=None),
        ),
        migrations.AddField(
            model_name='subscriptionrecord',
            name='subscription_filters',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=2), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='webhooktrigger',
            name='trigger_name',
            field=models.CharField(choices=[('customer.created', 'customer.created'), ('invoice.created', 'invoice.created'), ('invoice.paid', 'invoice.paid'), ('invoice.past_due', 'invoice.past_due'), ('subscription.created', 'subscription.created'), ('usage_alert.triggered', 'usage_alert.triggered'), ('subscription.cancelled', 'subscription.cancelled'), ('subscription.renewed', 'subscription.renewed')], max_length=40),
        ),
    ]