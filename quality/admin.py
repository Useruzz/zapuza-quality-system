from django.contrib import admin
from .models import Inspection


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "production_job",
        "measurement_name",
        "measured_value",
        "minimum_value",
        "maximum_value",
        "result",
        "inspected_at",
    )

    list_filter = ("result", "inspected_at")

    search_fields = (
        "production_job__job_number",
        "measurement_name",
    )

    readonly_fields = ("result", "inspected_at")
