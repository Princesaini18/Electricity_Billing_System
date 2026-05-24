from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("consumers/", views.consumer_list, name="consumer_list"),
    path("consumers/add/", views.consumer_create, name="consumer_create"),
    path("consumers/<int:pk>/", views.consumer_detail, name="consumer_detail"),
    path("consumers/<int:pk>/edit/", views.consumer_update, name="consumer_update"),
    path("consumers/<int:pk>/delete/", views.consumer_delete, name="consumer_delete"),
    path("bills/", views.bill_list, name="bill_list"),
    path("bills/generate/", views.generate_bill, name="generate_bill"),
    path("bills/<int:pk>/", views.bill_detail, name="bill_detail"),
    path("bills/<int:pk>/paid/", views.mark_bill_paid, name="mark_bill_paid"),
    path("bills/<int:pk>/pdf/", views.bill_pdf, name="bill_pdf"),
    path("consumer/login/", views.consumer_login, name="consumer_login"),
    path("consumer/logout/", views.consumer_logout, name="consumer_logout"),
    path("consumer/dashboard/", views.consumer_dashboard, name="consumer_dashboard"),
    path("consumer/bills/", views.consumer_bill_list, name="consumer_bill_list"),
    path("consumer/bills/<int:pk>/", views.consumer_bill_detail, name="consumer_bill_detail"),
    path("consumer/bills/<int:pk>/pdf/", views.consumer_bill_pdf, name="consumer_bill_pdf"),
]
