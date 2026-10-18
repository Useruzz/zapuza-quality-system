from django import forms
from .models import Inspection

class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = [
            "production_job",
            "measurement_name",
            "measured_value",
            "minimum_value",
            "maximum_value"
        ]

        widgets = {
            "measured_value": forms.NumberInput(
                attrs={"step": "0.001"}
            ),
            "minimum_value": forms.NumberInput(
                attrs={"step": "0.001"}
            ),
            "maximum_value": forms.NumberInput(
                attrs={"step": "0.001"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        minimum = cleaned_data.get("minimum_value")
        maximum = cleaned_data.get("maximum_value")

        if (
            minimum is not None
            and maximum is not None
            and minimum > maximum
        ):
            raise forms.ValidationError(
                "Minimum value cannot exceed maximum value."
            )
        
        return cleaned_data