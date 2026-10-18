from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from quality.models import Inspection

from .models import ProductionJob

class ProductionJobTests(TestCase):
    def setUp(self):
        self.job = ProductionJob.objects.create(
            job_number="TEST-001",
            part_name="Test Shaft",
            quantity=10,
        )

    def test_job_is_created_with_pending_status(self):
        self.assertEqual(self.job.status, "PENDING")

    def test_job_detail_page_loads(self):
        response = self.client.get(
            reverse("production:job_detail", args=[self.job.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEST-001")

class ProductionWorkflowTests(TestCase):
    def setUp(self):
        self.job = ProductionJob.objects.create(
            job_number="WORKFLOW-001",
            part_name="Workflow Test Shaft",
            quantity=10,            
        )
        self.status_url = reverse(
            "production:update_job_status",
            args=[self.job.pk],
        )

    def change_status(self, status):
        return self.client.post(
            self.status_url,
            {"status": status},
        )

    def add_inspection(self, value, minimum="23.780", maximum="26.450"):
        return Inspection.objects.create(
            production_job=self.job,
            measurement_name="Shaft diameter",
            measured_value=Decimal(value),
            minimum_value=Decimal(minimum),
            maximum_value=Decimal(maximum),
        )

    def test_valid_progression_to_inspection(self):
        self.change_status("IN_PROGRESS")
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "IN_PROGRESS")

        self.change_status("INSPECTION")
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "INSPECTION")

    def test_cannot_skip_production_stage(self):
        self.change_status("APPROVED")
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, "PENDING")

    def test_approval_blocked_without_inspections(self):
        self.job.status = "INSPECTION"
        self.job.save(update_fields=["status"])

        self.change_status("APPROVED")
        self.job.refresh_from_db()

        self.assertEqual(self.job.status, "INSPECTION")

    def test_approval_blocked_when_latest_result_fails(self):
        self.job.status = "INSPECTION"
        self.job.save(update_fields=["status"])

        self.add_inspection(value="25.000")
        self.add_inspection(value="22.100")

        self.change_status("APPROVED")
        self.job.refresh_from_db()

        self.assertEqual(self.job.status, "INSPECTION")
    
    def test_approval_allowed_when_latest_results_passes(self):
        self.job.status = "INSPECTION"
        self.job.save(update_fields=["status"])

        self.add_inspection(value="22.100")
        self.add_inspection(value="25.000")

        self.change_status("APPROVED")
        self.job.refresh_from_db()

        self.assertEqual(self.job.status, "APPROVED")

    def test_dispatched_job_cannot_change_status(self):
        self.job.status = "DISPATCHED"
        self.job.save(update_fields=["status"])

        self.change_status("IN_PROGRESS")
        self.job.refresh_from_db()

        self.assertEqual(self.job.status, "DISPATCHED")
    
    def test_approval_blocked_when_no_inspections_exist(self):
        self.change_status("APPROVED")
        self.job.refresh_from_db()

        self.assertNotEqual(self.job.status, "APPROVED")
