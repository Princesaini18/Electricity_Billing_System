from decimal import Decimal

from django.db import models
from django.urls import reverse


class Consumer(models.Model):
    DOMESTIC = "Domestic"
    COMMERCIAL = "Commercial"
    INDUSTRIAL = "Industrial"

    CONNECTION_CHOICES = [
        (DOMESTIC, "Domestic"),
        (COMMERCIAL, "Commercial"),
        (INDUSTRIAL, "Industrial"),
    ]

    name = models.CharField(max_length=120)
    consumer_number = models.CharField(max_length=30, unique=True)
    meter_number = models.CharField(max_length=30, unique=True)
    address = models.TextField()
    mobile_number = models.CharField(max_length=15)
    connection_type = models.CharField(max_length=20, choices=CONNECTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.consumer_number})"

    def get_absolute_url(self):
        return reverse("consumer_detail", args=[self.pk])


class Bill(models.Model):
    PAID = "Paid"
    PENDING = "Pending"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
    ]

    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name="bills")
    previous_reading = models.PositiveIntegerField()
    current_reading = models.PositiveIntegerField()
    units_used = models.PositiveIntegerField(editable=False)
    energy_charge = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    fixed_charge = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    bill_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-bill_date", "-id"]

    def __str__(self):
        return f"Bill #{self.id} - {self.consumer.name}"

    @staticmethod
    def calculate_energy_charge(units):
        if units <= 100:
            return Decimal(units) * Decimal("3")
        if units <= 300:
            return Decimal(100 * 3) + Decimal(units - 100) * Decimal("5")
        return Decimal(100 * 3) + Decimal(200 * 5) + Decimal(units - 300) * Decimal("7")

    def save(self, *args, **kwargs):
        self.units_used = max(self.current_reading - self.previous_reading, 0)
        self.energy_charge = self.calculate_energy_charge(self.units_used)
        subtotal = self.energy_charge + self.fixed_charge
        self.tax_amount = (subtotal * Decimal("0.05")).quantize(Decimal("0.01"))
        self.total_amount = (subtotal + self.tax_amount).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)


class Payment(models.Model):
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE, related_name="payment")
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Payment for Bill #{self.bill_id}"
