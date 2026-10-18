from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ProductionJobForm
from .forms import ProductionStatusForm
from .models import ProductionJob
from quality.models import Inspection


def job_list(request):
    jobs = ProductionJob.objects.order_by("-created_at")

    return render(
        request,
        "production/job_list.html",
        {"jobs": jobs},
    )


def job_create(request):
    if request.method == "POST":
        form = ProductionJobForm(request.POST)

        if form.is_valid():
            job = form.save()
            messages.success(
                request,
                f"Production job {job.job_number} created successfully.",
            )
            return redirect("production:job_list")
    else:
        form = ProductionJobForm()

    return render(
        request,
        "production/job_form.html",
        {"form": form},
    )


def job_detail(request, pk):
    job = get_object_or_404(ProductionJob, pk=pk)

    return render(
        request,
        "production/job_detail.html",
        {"job": job},
    )

@require_POST
def update_job_status(request, pk):
    job = get_object_or_404(ProductionJob, pk=pk)

    form = ProductionStatusForm(request.POST)

    if not form.is_valid():
        messages.error(request, "Invalid status selection.")
        return redirect("production:job_detail", pk=job.pk)

    new_status = form.cleaned_data["status"]
    current_status = job.status

    allowed_transitions = {
        "PENDING": ["IN_PROGRESS"],
        "IN_PROGRESS": ["INSPECTION"],
        "INSPECTION": ["APPROVED", "REJECTED"],
        "REJECTED": ["IN_PROGRESS"],
        "APPROVED": ["DISPATCHED"],
        "DISPATCHED": [],
    }

    if new_status not in allowed_transitions.get(current_status, []):
        messages.error(
            request,
            f"Transition from {current_status} to {new_status} is not allowed.",
        )
        return redirect("production:job_detail", pk=job.pk)

    if new_status == "APPROVED":
        inspections = Inspection.objects.filter(production_job=job)

        if not inspections.exists():
            messages.error(
                request,
                "Approval blocked: this job has no quality inspections. ",
            )
            return redirect("production:job_detail", pk=job.pk)

        latest_results = {}

        for inspection in inspections.order_by("inspected_at", "pk"):
            latest_results[inspection.measurement_name] = inspection.result

        if not latest_results or any(
            result != "PASS" for result in latest_results.values()
        ):
            messages.error(
                request,
                "Approval blocked: the latest result for every recorded "
                "measurement must be PASS.",
            )
            return redirect("production:job_detail", pk=job.pk)

    job.status = new_status
    job.save(update_fields=["status"])

    messages.success(
        request,
        f"Job {job.job_number} status changed to {job.get_status_display()}.",
    )

    return redirect("production:job_detail", pk=job.pk)
