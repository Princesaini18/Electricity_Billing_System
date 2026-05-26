from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "billing"

    def ready(self):
        from django.contrib.auth.models import User
        from .models import Consumer

        # Super Admin Create
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@gmail.com",
                password="admin123"
            )

        # Test Consumer Create
        Consumer.objects.get_or_create(
            consumer_number="1234567898",
            defaults={
                "meter_number": "111",
                "name": "Test User"
            }
        )