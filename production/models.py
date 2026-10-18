from django.db import models

class ProductionJob(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("INSPECTION", "Inspection"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("DISPATCHED", "Dispatched"),
    ]

    job_number = models.CharField(
        max_length=30,
        unique=True
    )

    part_name = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_number} - {self.part_name}"
