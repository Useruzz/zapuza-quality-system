from django.db import models
from production.models import ProductionJob

class Inspection(models.Model):
    RESULT_CHOICES = [
        ("PASS", "Pass"),
        ("FAIL", "Fail"),
    ]

    production_job = models.ForeignKey(
        ProductionJob,
        on_delete=models.CASCADE,
        related_name="inspections",
    )

    measurement_name = models.CharField(max_length=100)

    measured_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    minimum_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    maximum_value = models.DecimalField(
        max_digits=10,
        decimal_places=3,
    )

    result = models.CharField(
        max_length=4,
        choices=RESULT_CHOICES,
        blank=True,
    )

    inspected_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.minimum_value > self.maximum_value:
            raise ValueError(
                "Minimum value cannot exceed maximum value."
            )

        self.result = (
            "PASS"
            if self.minimum_value <= self.measured_value
            <= self.maximum_value
            else "FAIL"
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.production_job.job_number} - "
            f"{self.measurement_name} - {self.result}"
        )
