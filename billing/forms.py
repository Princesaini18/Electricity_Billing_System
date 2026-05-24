from django import forms

from .models import Bill, Consumer


class ConsumerPortalLoginForm(forms.Form):
    consumer_number = forms.CharField(max_length=30, label="Consumer Number")
    meter_number = forms.CharField(max_length=30, label="Meter Number")

    def clean_consumer_number(self):
        return self.cleaned_data["consumer_number"].strip()

    def clean_meter_number(self):
        return self.cleaned_data["meter_number"].strip()


class ConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = [
            "name",
            "consumer_number",
            "meter_number",
            "address",
            "mobile_number",
            "connection_type",
        ]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            "consumer",
            "previous_reading",
            "current_reading",
            "due_date",
            "status",
        ]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        previous = cleaned_data.get("previous_reading")
        current = cleaned_data.get("current_reading")
        if previous is not None and current is not None and current < previous:
            raise forms.ValidationError("Current reading must be greater than or equal to previous reading.")
        return cleaned_data
