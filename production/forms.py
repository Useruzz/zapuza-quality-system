from django import forms
from .models import ProductionJob


class ProductionJobForm(forms.ModelForm):
    class Meta:
        model = ProductionJob
        fields = ["job_number", "part_name", "quantity"]

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 1:
            raise forms.ValidationError(
                "Quantity must be at least 1."
            )

        return quantity

class ProductionStatusForm(forms.Form):
    status = forms.ChoiceField(
        label="New production status",
        choices=ProductionJob.STATUS_CHOICES,
    )