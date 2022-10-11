# Generated by Django 4.0.5 on 2022-09-15 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("metering_billing", "0009_remove_subscription_next_plan_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(
                choices=[
                    ("requires_payment_method", "Requires Payment Method"),
                    ("requires_action", "Requires Action"),
                    ("processing", "Processing"),
                    ("succeeded", "Succeeded"),
                    (
                        "organization_not_connected_to_stripe",
                        "Organization Not Connected to Stripe",
                    ),
                    (
                        "customer_not_connected_to_stripe",
                        "Customer Not Connected to Stripe",
                    ),
                ],
                max_length=40,
            ),
        ),
    ]