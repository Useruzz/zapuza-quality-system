from django.contrib import admin
from .models import ProductionJob


@admin.register(ProductionJob)
class ProductionJobAdmin(admin.ModelAdmin):
    list_display = (
        "job_number",
        "part_name",
        "quantity",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")

    search_fields = ("job_number", "part_name")
