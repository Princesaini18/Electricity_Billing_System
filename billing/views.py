import json
from functools import wraps
from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .forms import BillForm, ConsumerForm, ConsumerPortalLoginForm
from .models import Bill, Consumer, Payment


def staff_required(view_func):
    return login_required(user_passes_test(lambda user: user.is_staff)(view_func))


def consumer_portal_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        consumer = _get_logged_in_consumer(request)
        if not consumer:
            request.session.pop("consumer_id", None)
            request.session.pop("consumer_name", None)
            return redirect("consumer_login")
        return view_func(request, *args, **kwargs)

    return _wrapped


def home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")
    if request.session.get("consumer_id"):
        return redirect("consumer_dashboard")
    return redirect("login")


@staff_required
def dashboard(request):
    total_consumers = Consumer.objects.count()
    total_bills = Bill.objects.count()
    paid_bills = Bill.objects.filter(status=Bill.PAID).count()
    pending_bills = Bill.objects.filter(status=Bill.PENDING).count()
    monthly_revenue = (
        Bill.objects.filter(status=Bill.PAID, bill_date__month=timezone.localdate().month)
        .aggregate(total=Sum("total_amount"))
        .get("total")
        or 0
    )

    monthly_usage = (
        Bill.objects.annotate(month=TruncMonth("bill_date"))
        .values("month")
        .annotate(units=Sum("units_used"), revenue=Sum("total_amount"))
        .order_by("month")
    )
    chart_labels = [item["month"].strftime("%b %Y") for item in monthly_usage]
    usage_data = [item["units"] or 0 for item in monthly_usage]
    revenue_data = [float(item["revenue"] or 0) for item in monthly_usage]

    recent_bills = Bill.objects.select_related("consumer")[:5]

    context = {
        "total_consumers": total_consumers,
        "total_bills": total_bills,
        "paid_bills": paid_bills,
        "pending_bills": pending_bills,
        "monthly_revenue": monthly_revenue,
        "chart_labels": json.dumps(chart_labels),
        "usage_data": json.dumps(usage_data),
        "revenue_data": json.dumps(revenue_data),
        "bill_status_labels": json.dumps(["Paid", "Pending"]),
        "bill_status_data": json.dumps([paid_bills, pending_bills]),
        "recent_bills": recent_bills,
    }
    return render(request, "dashboard.html", context)


@staff_required
def consumer_list(request):
    query = request.GET.get("q", "")
    consumers = Consumer.objects.all()
    if query:
        consumers = consumers.filter(Q(name__icontains=query) | Q(consumer_number__icontains=query)).distinct()
    return render(request, "consumer_list.html", {"consumers": consumers, "query": query})


@staff_required
def consumer_detail(request, pk):
    consumer = get_object_or_404(Consumer, pk=pk)
    bills = consumer.bills.all()
    return render(request, "consumer_detail.html", {"consumer": consumer, "bills": bills})


@staff_required
def consumer_create(request):
    form = ConsumerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Consumer added successfully.")
        return redirect("consumer_list")
    return render(request, "consumer_form.html", {"form": form, "title": "Add Consumer"})


@staff_required
def consumer_update(request, pk):
    consumer = get_object_or_404(Consumer, pk=pk)
    form = ConsumerForm(request.POST or None, instance=consumer)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Consumer updated successfully.")
        return redirect("consumer_detail", pk=consumer.pk)
    return render(request, "consumer_form.html", {"form": form, "title": "Edit Consumer"})


@staff_required
def consumer_delete(request, pk):
    consumer = get_object_or_404(Consumer, pk=pk)
    if request.method == "POST":
        consumer.delete()
        messages.success(request, "Consumer deleted successfully.")
        return redirect("consumer_list")
    return render(request, "confirm_delete.html", {"object": consumer, "cancel_url": reverse("consumer_list")})


@staff_required
def bill_list(request):
    status = request.GET.get("status", "")
    bills = Bill.objects.select_related("consumer").order_by("-bill_date", "-id")
    if status in [Bill.PAID, Bill.PENDING]:
        bills = bills.filter(status=status)

    paginator = Paginator(bills, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "bill_list.html",
        {
            "bills": page_obj.object_list,
            "status": status,
            "page_obj": page_obj,
        },
    )


@staff_required
def generate_bill(request):
    form = BillForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        bill = form.save()
        messages.success(request, "Bill generated successfully.")
        return redirect("bill_detail", pk=bill.pk)
    return render(request, "generate_bill.html", {"form": form})


@staff_required
def bill_detail(request, pk):
    bill = get_object_or_404(Bill.objects.select_related("consumer"), pk=pk)
    return render(request, "bill_detail.html", {"bill": bill})


@staff_required
def mark_bill_paid(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    bill.status = Bill.PAID
    bill.save()
    Payment.objects.get_or_create(bill=bill, defaults={"amount_paid": bill.total_amount})
    messages.success(request, "Bill marked as paid.")
    return redirect("bill_detail", pk=bill.pk)


@staff_required
def bill_pdf(request, pk):
    bill = get_object_or_404(Bill.objects.select_related("consumer"), pk=pk)
    return _render_bill_pdf(bill)


@consumer_portal_required
def consumer_bill_pdf(request, pk):
    consumer = _get_logged_in_consumer(request)
    bill = get_object_or_404(Bill.objects.select_related("consumer"), pk=pk, consumer=consumer)
    return _render_bill_pdf(bill)


def _render_bill_pdf(bill):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Smart Electricity Billing System", styles["Title"]))
    elements.append(Paragraph("Official Electricity Bill", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    consumer_data = [
        ["Consumer Name", bill.consumer.name, "Consumer No.", bill.consumer.consumer_number],
        ["Meter Number", bill.consumer.meter_number, "Connection", bill.consumer.connection_type],
        ["Mobile", bill.consumer.mobile_number, "Bill Status", bill.status],
        ["Address", bill.consumer.address, "Due Date", bill.due_date.strftime("%d %b %Y")],
    ]
    elements.append(_styled_table(consumer_data))
    elements.append(Spacer(1, 0.25 * inch))

    bill_data = [
        ["Previous Reading", bill.previous_reading],
        ["Current Reading", bill.current_reading],
        ["Units Used", bill.units_used],
        ["Energy Charge", f"Rs. {bill.energy_charge}"],
        ["Fixed Charge", f"Rs. {bill.fixed_charge}"],
        ["Tax (5%)", f"Rs. {bill.tax_amount}"],
        ["Total Amount", f"Rs. {bill.total_amount}"],
    ]
    elements.append(_styled_table(bill_data, col_widths=[2.5 * inch, 3 * inch]))
    elements.append(Spacer(1, 0.25 * inch))
    elements.append(Paragraph("Please pay before the due date to avoid late payment charges.", styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    filename = f"bill-{bill.id}-{bill.consumer.consumer_number}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)


def consumer_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard")
    if request.session.get("consumer_id"):
        return redirect("consumer_dashboard")

    form = ConsumerPortalLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        consumer_number = form.cleaned_data["consumer_number"]
        meter_number = form.cleaned_data["meter_number"]
        consumer = Consumer.objects.filter(
            consumer_number__iexact=consumer_number, meter_number__iexact=meter_number
        ).first()

        if consumer:
            request.session["consumer_id"] = consumer.id
            request.session["consumer_name"] = consumer.name
            messages.success(request, "Consumer login successful.")
            return redirect("consumer_dashboard")
        form.add_error(None, "Invalid consumer number or meter number.")

    return render(request, "consumer/login.html", {"form": form})


@consumer_portal_required
def consumer_logout(request):
    request.session.pop("consumer_id", None)
    request.session.pop("consumer_name", None)
    messages.success(request, "Logged out successfully.")
    return redirect("consumer_login")


@consumer_portal_required
def consumer_dashboard(request):
    consumer = _get_logged_in_consumer(request)
    bills_qs = Bill.objects.filter(consumer=consumer).order_by("-bill_date", "-id")
    paid_bills = bills_qs.filter(status=Bill.PAID)
    pending_bills = bills_qs.filter(status=Bill.PENDING)

    monthly_usage = (
        bills_qs.annotate(month=TruncMonth("bill_date"))
        .values("month")
        .annotate(units=Sum("units_used"), amount=Sum("total_amount"))
        .order_by("month")
    )
    chart_labels = [item["month"].strftime("%b %Y") for item in monthly_usage]
    usage_data = [item["units"] or 0 for item in monthly_usage]
    amount_data = [float(item["amount"] or 0) for item in monthly_usage]

    context = {
        "consumer": consumer,
        "total_bills": bills_qs.count(),
        "paid_bills": paid_bills.count(),
        "pending_bills": pending_bills.count(),
        "total_amount": bills_qs.aggregate(total=Sum("total_amount")).get("total") or 0,
        "pending_amount": pending_bills.aggregate(total=Sum("total_amount")).get("total") or 0,
        "recent_bills": bills_qs[:6],
        "chart_labels": json.dumps(chart_labels),
        "usage_data": json.dumps(usage_data),
        "amount_data": json.dumps(amount_data),
        "status_labels": json.dumps(["Paid", "Pending"]),
        "status_data": json.dumps([paid_bills.count(), pending_bills.count()]),
    }
    return render(request, "consumer/dashboard.html", context)


@consumer_portal_required
def consumer_bill_list(request):
    consumer = _get_logged_in_consumer(request)
    status = request.GET.get("status", "")
    bills = Bill.objects.filter(consumer=consumer).order_by("-bill_date", "-id")
    if status in [Bill.PAID, Bill.PENDING]:
        bills = bills.filter(status=status)

    paginator = Paginator(bills, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "consumer/bill_list.html",
        {"consumer": consumer, "bills": page_obj.object_list, "page_obj": page_obj, "status": status},
    )


@consumer_portal_required
def consumer_bill_detail(request, pk):
    consumer = _get_logged_in_consumer(request)
    bill = get_object_or_404(Bill, pk=pk, consumer=consumer)
    return render(request, "consumer/bill_detail.html", {"consumer": consumer, "bill": bill})


def _styled_table(data, col_widths=None):
    table = Table(data, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def _get_logged_in_consumer(request):
    consumer_id = request.session.get("consumer_id")
    if not consumer_id:
        return None
    return Consumer.objects.filter(pk=consumer_id).first()
