from django.contrib import admin

from .models import Bill, Consumer, Payment


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ("name", "consumer_number", "meter_number", "mobile_number", "connection_type")
    search_fields = ("name", "consumer_number", "meter_number", "mobile_number")
    list_filter = ("connection_type",)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "consumer", "units_used", "total_amount", "due_date", "status")
    list_filter = ("status", "bill_date", "due_date")
    search_fields = ("consumer__name", "consumer__consumer_number", "consumer__meter_number")
    readonly_fields = ("units_used", "energy_charge", "tax_amount", "total_amount", "bill_date")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("bill", "amount_paid", "payment_date", "reference_number")
    search_fields = ("bill__consumer__name", "reference_number")
