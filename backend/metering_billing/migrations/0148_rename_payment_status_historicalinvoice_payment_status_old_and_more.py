# Generated by Django 4.0.5 on 2023-01-13 21:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "metering_billing",
            "0147_rename_company_name_historicalorganization_organization_name_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalinvoice",
            old_name="payment_status",
            new_name="payment_status_old",
        ),
        migrations.RenameField(
            model_name="invoice",
            old_name="payment_status",
            new_name="payment_status_old",
        ),
    ]