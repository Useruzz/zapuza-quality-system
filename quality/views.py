from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import InspectionForm
from .models import Inspection


def inspection_list(request):
    inspections = (
        Inspection.objects
        .select_related("production_job")
        .order_by("-inspected_at")
    )

    context = {
        "inspections": inspections,
        "total_inspections": inspections.count(),
        "passed_inspections": inspections.filter(
            result="PASS"
        ).count(),
        "failed_inspections": inspections.filter(
            result="FAIL"
        ).count(),
    }

    return render(
        request,
        "quality/inspection_list.html",
        context,
    )

def inspection_create(request):
    if request.method == "POST":
        form = InspectionForm(request.POST)

        if form.is_valid():
            inspection = form.save()

            messages.success(
                request,
                f"Inspection for {inspection.production_job.job_number} "
                f"saved with result: {inspection.result}.",
            )
            
            return redirect(
                "quality:inspection_detail",
                pk=inspection.pk,
            )
    else:
        form = InspectionForm()

    return render(
        request,
        "quality/inspection_form.html",
        {"form": form},
    )

def inspection_detail(request, pk):
    inspection = get_object_or_404(
        Inspection.objects.select_related("production_job"), 
        pk=pk,
    )

    return render(
        request,
        "quality/inspection_detail.html",
        {"inspection": inspection},
    )
