# Generated for Smart Electricity Billing System

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Consumer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("consumer_number", models.CharField(max_length=30, unique=True)),
                ("meter_number", models.CharField(max_length=30, unique=True)),
                ("address", models.TextField()),
                ("mobile_number", models.CharField(max_length=15)),
                (
                    "connection_type",
                    models.CharField(
                        choices=[
                            ("Domestic", "Domestic"),
                            ("Commercial", "Commercial"),
                            ("Industrial", "Industrial"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Bill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("previous_reading", models.PositiveIntegerField()),
                ("current_reading", models.PositiveIntegerField()),
                ("units_used", models.PositiveIntegerField(editable=False)),
                ("energy_charge", models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ("fixed_charge", models.DecimalField(decimal_places=2, default=100, max_digits=10)),
                ("tax_amount", models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ("total_amount", models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ("bill_date", models.DateField(auto_now_add=True)),
                ("due_date", models.DateField()),
                (
                    "status",
                    models.CharField(choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending", max_length=10),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "consumer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bills", to="billing.consumer"),
                ),
            ],
            options={"ordering": ["-bill_date", "-id"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("payment_date", models.DateField(auto_now_add=True)),
                ("amount_paid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("reference_number", models.CharField(blank=True, max_length=60)),
                (
                    "bill",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="billing.bill"),
                ),
            ],
            options={"ordering": ["-payment_date"]},
        ),
    ]
