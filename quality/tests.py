from decimal import Decimal

from django.test import TestCase

from production.models import ProductionJob
from .models import Inspection

class InspectionTests(TestCase):
    def setUp(self):
        self.job = ProductionJob.objects.create(
            job_number="TEST-QA-001",
            part_name="Test Shaft",
            quantity=5,
        )
    
    def test_measurement_within_range_passes(self):
        inspection = Inspection.objects.create(
            production_job=self.job,
            measurement_name="Shaft diameter",
            measured_value=Decimal("25.000"),
            minimum_value=Decimal("23.780"),
            maximum_value=Decimal("26.450"),
        )
        self.assertEqual(inspection.result, "PASS")

    def test_measurement_outside_range_fails(self):
        inspection = Inspection.objects.create(
            production_job=self.job,
            measurement_name="Shaft diameter",
            measured_value=Decimal("22.100"),
            minimum_value=Decimal("23.780"),
            maximum_value=Decimal("26.450"),
        )
        self.assertEqual(inspection.result, "FAIL")
